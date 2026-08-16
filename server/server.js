const express = require('express');
const cors = require('cors');
const { pool } = require('./db');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Get all shows with their zones
app.get('/api/shows', async (req, res) => {
  try {
    const showsRes = await pool.query(
      `SELECT s.id, s.name, s.date, s.time,
              json_agg(
                json_build_object(
                  'id', z.id,
                  'zone_name', z.zone_name,
                  'total_capacity', z.total_capacity,
                  'available_seats', z.available_seats
                ) ORDER BY z.zone_name
              ) as zones
       FROM shows s
       LEFT JOIN zones z ON s.id = z.show_id
       GROUP BY s.id
       ORDER BY s.date, s.time`
    );
    res.json(showsRes.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database error fetching shows' });
  }
});

// Create a new show with dynamic zones
app.post('/api/shows', async (req, res) => {
  const { name, date, time, zones } = req.body;
  
  if (!name || !date || !time || !zones || !Array.isArray(zones) || zones.length === 0) {
    return res.status(400).json({ error: 'Invalid show configuration data' });
  }

  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    
    // Insert Show
    const showRes = await client.query(
      'INSERT INTO shows (name, date, time) VALUES ($1, $2, $3) RETURNING id',
      [name, date, time]
    );
    const showId = showRes.rows[0].id;
    
    // Insert Zones
    for (const z of zones) {
      await client.query(
        'INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES ($1, $2, $3, $3)',
        [showId, z.zone_name, parseInt(z.capacity)]
      );
    }
    
    await client.query('COMMIT');
    res.status(201).json({ success: true, showId });
  } catch (err) {
    await client.query('ROLLBACK');
    console.error(err);
    res.status(500).json({ error: 'Database error creating show: ' + err.message });
  } finally {
    client.release();
  }
});

// Device registration / update
app.post('/api/devices/register', async (req, res) => {
  const { id, deviceName } = req.body;
  if (!id || !deviceName) {
    return res.status(400).json({ error: 'Missing device ID or Name' });
  }
  
  try {
    await pool.query(
      `INSERT INTO devices (id, device_name) 
       VALUES ($1, $2) 
       ON CONFLICT (id) DO UPDATE SET device_name = EXCLUDED.device_name`,
      [id, deviceName]
    );
    res.json({ success: true, message: 'Device registered successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database error registering device' });
  }
});

// Print ticket (atomic booking transaction)
app.post('/api/tickets/print', async (req, res) => {
  const { showId, zoneName, deviceId } = req.body;
  
  if (!showId || !zoneName || !deviceId) {
    return res.status(400).json({ error: 'Missing showId, zoneName, or deviceId' });
  }
  
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    
    // Lock the specific zone row to prevent race conditions from other clients
    const zoneRes = await client.query(
      `SELECT z.id, z.available_seats, z.total_capacity, s.name as show_name, s.date as show_date, s.time as show_time
       FROM zones z
       JOIN shows s ON s.id = z.show_id
       WHERE z.show_id = $1 AND z.zone_name = $2
       FOR UPDATE`,
      [showId, zoneName]
    );
    
    if (zoneRes.rows.length === 0) {
      throw new Error('Show zone not found');
    }
    
    const zone = zoneRes.rows[0];
    if (zone.available_seats <= 0) {
      throw new Error('No seats are available in this zone');
    }
    
    // Calculate ticket number sequentially
    const ticketNumber = zone.total_capacity - zone.available_seats + 1;
    
    // Decrement seats
    await client.query(
      'UPDATE zones SET available_seats = available_seats - 1 WHERE id = $1',
      [zone.id]
    );
    
    // Insert ticket log
    await client.query(
      `INSERT INTO ticket_logs (show_id, zone_id, device_id, action, ticket_number)
       VALUES ($1, $2, $3, 'PRINTED', $4)`,
      [showId, zone.id, deviceId, ticketNumber]
    );
    
    await client.query('COMMIT');
    
    // Format Date for Ticket Print output (YYYY-MM-DD or readable string)
    const formattedDate = new Date(zone.show_date).toLocaleDateString('ar-EG', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
    
    res.json({
      success: true,
      ticket: {
        showName: zone.show_name,
        date: formattedDate,
        time: zone.show_time,
        zoneName: zoneName,
        ticketNumber: ticketNumber,
        ticketId: `${zoneName} - ${ticketNumber}`
      }
    });
  } catch (err) {
    await client.query('ROLLBACK');
    console.error('Print transaction failed:', err.message);
    res.status(400).json({ error: err.message });
  } finally {
    client.release();
  }
});

// Get ticketing logs (audit page helper)
app.get('/api/logs', async (req, res) => {
  try {
    const logsRes = await pool.query(
      `SELECT l.id, s.name as show_name, z.zone_name, d.device_name, l.action, l.ticket_number, l.printed_at
       FROM ticket_logs l
       JOIN shows s ON s.id = l.show_id
       JOIN zones z ON z.id = l.zone_id
       LEFT JOIN devices d ON d.id = l.device_id
       ORDER BY l.printed_at DESC
       LIMIT 100`
    );
    res.json(logsRes.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database error fetching logs' });
  }
});

app.listen(PORT, () => {
  console.log(`Theatre ticketing backend running on port ${PORT}`);
});
