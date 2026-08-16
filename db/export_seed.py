import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))
from main import get_db_connection, query_as_dicts

def export_db_to_seed():
    conn = get_db_connection()
    shows = query_as_dicts(conn, "SELECT id, name, prefix, date, time, end_time, COALESCE(is_gate_active, TRUE) as is_gate_active FROM shows ORDER BY id ASC;")
    zones = query_as_dicts(conn, "SELECT id, show_id, zone_name, total_capacity, available_seats FROM zones ORDER BY show_id ASC, zone_name ASC;")
    users = query_as_dicts(conn, "SELECT id, username, password_hash, full_name, role, is_active FROM users ORDER BY id ASC;")
    devices = query_as_dicts(conn, "SELECT id, device_name FROM devices ORDER BY device_name ASC;")
    logs = query_as_dicts(conn, "SELECT id, show_id, zone_id, device_id, action, ticket_number, passcode, printed_at FROM ticket_logs ORDER BY id ASC;")

    out = []
    out.append("-- ==========================================================================")
    out.append("-- Live Database Snapshot & Seed Entries")
    out.append("-- St. Markos Church (Heliopolis) - Neiruz 2026 Ticketing System")
    out.append("-- ==========================================================================")
    out.append("BEGIN;")
    out.append("")
    out.append("TRUNCATE TABLE ticket_logs CASCADE;")
    out.append("TRUNCATE TABLE zones CASCADE;")
    out.append("TRUNCATE TABLE shows CASCADE;")
    out.append("TRUNCATE TABLE users CASCADE;")
    out.append("TRUNCATE TABLE devices CASCADE;")
    out.append("")
    out.append("-- --------------------------------------------------------------------------")
    out.append("-- System Operators & Roles")
    out.append("-- --------------------------------------------------------------------------")
    for u in users:
        fn = u['full_name'].replace("'", "''")
        un = u['username'].replace("'", "''")
        pw = u['password_hash'].replace("'", "''")
        role = u['role']
        act = "TRUE" if u['is_active'] else "FALSE"
        out.append(f"INSERT INTO users (id, username, password_hash, full_name, role, is_active) VALUES ({u['id']}, '{un}', '{pw}', '{fn}', '{role}', {act});")

    out.append("SELECT setval('users_id_seq', (SELECT COALESCE(MAX(id), 1) FROM users));")
    out.append("")
    out.append("-- --------------------------------------------------------------------------")
    out.append("-- Shows and Seating Zones")
    out.append("-- --------------------------------------------------------------------------")
    zones_by_show = {}
    for z in zones:
        zones_by_show.setdefault(z['show_id'], []).append(z)

    for s in shows:
        s_name = s['name'].replace("'", "''")
        pfx = s['prefix'].replace("'", "''")
        d_val = str(s['date'])
        t_val = str(s['time']).replace("'", "''")
        e_val = str(s['end_time'] or '').replace("'", "''")
        g_act = "TRUE" if s['is_gate_active'] else "FALSE"
        out.append(f"INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES ({s['id']}, '{s_name}', '{pfx}', '{d_val}', '{t_val}', '{e_val}', {g_act});")
        for z in zones_by_show.get(s['id'], []):
            z_name = z['zone_name']
            tot = z['total_capacity']
            avail = z['available_seats']
            out.append(f"INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES ({z['id']}, {s['id']}, '{z_name}', {tot}, {avail});")
        out.append("")

    out.append("SELECT setval('shows_id_seq', (SELECT COALESCE(MAX(id), 1) FROM shows));")
    out.append("SELECT setval('zones_id_seq', (SELECT COALESCE(MAX(id), 1) FROM zones));")
    out.append("")

    if devices:
        out.append("-- --------------------------------------------------------------------------")
        out.append("-- Registered Devices & Terminals")
        out.append("-- --------------------------------------------------------------------------")
        for d in devices:
            d_name = d['device_name'].replace("'", "''")
            out.append(f"INSERT INTO devices (id, device_name) VALUES ('{d['id']}', '{d_name}') ON CONFLICT (id) DO NOTHING;")
        out.append("")

    if logs:
        out.append("-- --------------------------------------------------------------------------")
        out.append("-- Initial Audit Logs & Issued Tickets")
        out.append("-- --------------------------------------------------------------------------")
        for l in logs:
            dev_val = f"'{l['device_id']}'" if l['device_id'] else "NULL"
            pass_val = f"'{l['passcode']}'" if l['passcode'] else "''"
            ts_val = f"'{l['printed_at']}'" if l['printed_at'] else "CURRENT_TIMESTAMP"
            out.append(f"INSERT INTO ticket_logs (id, show_id, zone_id, device_id, action, ticket_number, passcode, printed_at) VALUES ({l['id']}, {l['show_id']}, {l['zone_id']}, {dev_val}, '{l['action']}', {l['ticket_number']}, {pass_val}, {ts_val});")
        out.append("SELECT setval('ticket_logs_id_seq', (SELECT COALESCE(MAX(id), 1) FROM ticket_logs));")
        out.append("")

    out.append("COMMIT;")
    out.append("")

    target_path = os.path.join(os.path.dirname(__file__), 'seed.sql')
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

    print(f"Successfully exported {len(shows)} shows, {len(zones)} zones, {len(users)} users, {len(devices)} devices, {len(logs)} logs to {target_path}")
    conn.close()

if __name__ == '__main__':
    export_db_to_seed()
