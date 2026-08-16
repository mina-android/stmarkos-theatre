-- Drops existing tables if they exist to start fresh
DROP TABLE IF EXISTS ticket_logs CASCADE;
DROP TABLE IF EXISTS devices CASCADE;
DROP TABLE IF EXISTS zones CASCADE;
DROP TABLE IF EXISTS shows CASCADE;

-- Shows Table
CREATE TABLE shows (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    prefix VARCHAR(50) DEFAULT '',
    date DATE NOT NULL,
    time VARCHAR(50) NOT NULL, -- Start time e.g. "18:30"
    end_time VARCHAR(50) DEFAULT '' -- End time e.g. "20:00"
);

-- Zones Table
CREATE TABLE zones (
    id SERIAL PRIMARY KEY,
    show_id INT REFERENCES shows(id) ON DELETE CASCADE,
    zone_name VARCHAR(50) NOT NULL,
    total_capacity INT NOT NULL,
    available_seats INT NOT NULL,
    CONSTRAINT unique_show_zone UNIQUE (show_id, zone_name)
);

-- Devices Table
CREATE TABLE devices (
    id UUID PRIMARY KEY,
    device_name VARCHAR(100) NOT NULL
);

-- Ticket Logs Table
CREATE TABLE ticket_logs (
    id SERIAL PRIMARY KEY,
    show_id INT REFERENCES shows(id) ON DELETE CASCADE,
    zone_id INT REFERENCES zones(id) ON DELETE CASCADE,
    device_id UUID,
    action VARCHAR(50) NOT NULL DEFAULT 'PRINTED',
    ticket_number INT NOT NULL,
    passcode VARCHAR(50),
    printed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'ticket_seller', -- 'ticket_seller', 'admin', 'superuser'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
