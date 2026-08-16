-- ==========================================================================
-- Live Database Snapshot & Seed Entries
-- St. Markos Church (Heliopolis) - Neiruz 2026 Ticketing System
-- ==========================================================================
BEGIN;

TRUNCATE TABLE ticket_logs CASCADE;
TRUNCATE TABLE zones CASCADE;
TRUNCATE TABLE shows CASCADE;
TRUNCATE TABLE users CASCADE;
TRUNCATE TABLE devices CASCADE;

-- --------------------------------------------------------------------------
-- System Operators & Roles
-- --------------------------------------------------------------------------
INSERT INTO users (id, username, password_hash, full_name, role, is_active) VALUES (5, 'minaashraf', 'b8dfd6a2dedd850c3783d3e481312a90$ee549e14b0400c936a234cc3346a8609b2901d83467551ab69f5ddabf7591da8', 'Mina Ashraf', 'superuser', TRUE);
INSERT INTO users (id, username, password_hash, full_name, role, is_active) VALUES (6, 'admin1', '854459921a8834b2069baf20dbd66799$ddbfbeff965d9624cec1fbc37a29d1e2ec24689eeb224296390b7f355f109584', 'admin', 'admin', TRUE);
INSERT INTO users (id, username, password_hash, full_name, role, is_active) VALUES (7, 'user1', '0637b3c53824aa9961b70b2095a20401$451810024e95fbf3aedc54d401c98a5095ec426af4c289d9de3058a89c8cdaee', 'user', 'ticket_seller', TRUE);
INSERT INTO users (id, username, password_hash, full_name, role, is_active) VALUES (9, 'scanner1', 'b020a77b7779f21530dc8ca63a3e4363$c04c4c742e959610981839daed7c90ee916af90db872d93f030d2ec4e4a0b8bb', 'scanner', 'scanner', TRUE);
SELECT setval('users_id_seq', (SELECT COALESCE(MAX(id), 1) FROM users));

-- --------------------------------------------------------------------------
-- Shows and Seating Zones
-- --------------------------------------------------------------------------
INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (1, 'اوبريت '''' اسرة عمانوئيل', '11', '2026-09-01', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (98, 1, 'A', 125, 124);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (99, 1, 'B', 20, 19);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (100, 1, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (101, 1, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (2, 'كورال '''' اسرة البابا كيرلس والمريمات', '12', '2026-09-01', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (102, 2, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (103, 2, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (104, 2, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (105, 2, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (3, 'اوبريت '''' اسرة رسل بنات', '13', '2026-09-02', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (106, 3, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (107, 3, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (108, 3, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (109, 3, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (4, 'اوبريت '''' اسرة تيموثاوس و مورا', '14', '2026-09-02', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (110, 4, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (111, 4, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (112, 4, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (113, 4, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (5, 'اوبريت '''' اسرة ابرار 1', '15', '2026-09-03', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (114, 5, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (115, 5, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (116, 5, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (117, 5, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (6, 'مسرحية '''' اسرة ابرار 2', '16', '2026-09-03', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (118, 6, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (119, 6, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (120, 6, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (121, 6, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (7, 'كورال '''' اسرة قديسين', '17', '2026-09-05', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (122, 7, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (123, 7, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (124, 7, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (125, 7, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (8, 'مسرحية '''' اسرة قديسين', '18', '2026-09-05', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (126, 8, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (127, 8, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (128, 8, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (129, 8, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (9, 'اوبريت '''' اسرة رسل ولاد', '19', '2026-09-06', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (130, 9, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (131, 9, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (132, 9, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (133, 9, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (10, 'مسرحية '''' اسرة محبة', '20', '2026-09-06', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (134, 10, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (135, 10, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (136, 10, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (137, 10, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (11, 'كورال '''' اسرة سمعان الشيخ', '21', '2026-09-07', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (138, 11, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (139, 11, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (140, 11, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (141, 11, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (12, 'مسرحية '''' اسرة أباء', '22', '2026-09-07', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (142, 12, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (143, 12, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (144, 12, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (145, 12, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (13, 'اوبريت '''' اسرة ماربنهام و سارة أولاد', '23', '2026-09-08', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (146, 13, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (147, 13, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (148, 13, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (149, 13, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (14, 'مسرحية '''' اسرة ماربنهام و سارة بنات', '24', '2026-09-08', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (150, 14, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (151, 14, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (152, 14, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (153, 14, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (15, 'اوبريت '''' اسرة اباء بنات', '25', '2026-09-09', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (154, 15, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (155, 15, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (156, 15, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (157, 15, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (16, 'كورال '''' اسرة الشهيد بروفوريوس', '26', '2026-09-09', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (158, 16, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (159, 16, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (160, 16, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (161, 16, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (17, 'اوبريت '''' اسرة نبيات', '27', '2026-09-12', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (162, 17, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (163, 17, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (164, 17, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (165, 17, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (18, 'كورال '''' اسرة محبة', '28', '2026-09-12', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (166, 18, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (167, 18, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (168, 18, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (169, 18, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (19, 'كورال '''' اسرة نيقولاوس', '29', '2026-09-13', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (170, 19, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (171, 19, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (172, 19, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (173, 19, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (20, 'كورال '''' اسرة الانبا رويس', '30', '2026-09-13', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (174, 20, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (175, 20, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (176, 20, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (177, 20, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (21, 'كورال '''' اسرة شهيدات', '31', '2026-09-14', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (178, 21, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (179, 21, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (180, 21, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (181, 21, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (22, 'اوبريت '''' اسرة الانبا كاراس', '32', '2026-09-14', '18:30', '20:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (182, 22, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (183, 22, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (184, 22, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (185, 22, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (23, 'مسرحية '''' اسرة انبياء اولاد', '33', '2026-09-15', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (186, 23, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (187, 23, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (188, 23, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (189, 23, 'D', 155, 155);

INSERT INTO shows (id, name, prefix, date, time, end_time, is_gate_active) VALUES (24, 'مسرحية '''' اسرة الكاروز', '34', '2026-09-15', '20:00', '22:00', FALSE);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (190, 24, 'A', 125, 125);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (191, 24, 'B', 20, 20);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (192, 24, 'C', 110, 110);
INSERT INTO zones (id, show_id, zone_name, total_capacity, available_seats) VALUES (193, 24, 'D', 155, 155);

SELECT setval('shows_id_seq', (SELECT COALESCE(MAX(id), 1) FROM shows));
SELECT setval('zones_id_seq', (SELECT COALESCE(MAX(id), 1) FROM zones));

-- --------------------------------------------------------------------------
-- Registered Devices & Terminals
-- --------------------------------------------------------------------------
INSERT INTO devices (id, device_name) VALUES ('68ca40a4-599b-42f4-a02b-fe0ac43bbd65', 'Terminal') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('b3d02bde-3553-4fc7-b174-83e05aa85293', 'Terminal 137') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('3cd37ce8-37af-4297-b55f-4f1c15aff4fd', 'Terminal 309') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('69a5250c-5558-4abb-895c-0ab64a5849c3', 'Terminal 328') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('277055b5-bd7b-4d0b-9653-6be79a9948ff', 'Terminal 514') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('00816aa8-a97e-4fe7-82ca-50e2f42936cc', 'Terminal 650') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('72f191e5-6a5c-4951-b884-e43c3df739e2', 'Terminal 758') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('4d712aee-07a2-404c-97f0-be9f4c544dd4', 'Terminal 865') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('dc78e52b-843d-4b9a-a285-e4d605b7e9f0', 'Web Terminal') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('6663c85e-0c87-4f09-9ac8-95925adb66d7', 'Web Terminal') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('bd96c738-5e32-45c1-a9d5-2755f04c7d3b', 'Web Terminal') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('080e541c-e997-4538-a9ef-beda891c56c8', 'Web Terminal') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('17399d0f-18e6-464b-a68a-475f7c1a0be0', 'Web Terminal') ON CONFLICT (id) DO NOTHING;
INSERT INTO devices (id, device_name) VALUES ('f31a5bdc-44ba-4f67-a8f0-031f4efe6b31', 'Web Terminal') ON CONFLICT (id) DO NOTHING;

-- --------------------------------------------------------------------------
-- Initial Audit Logs & Issued Tickets
-- --------------------------------------------------------------------------
INSERT INTO ticket_logs (id, show_id, zone_id, device_id, action, ticket_number, passcode, printed_at) VALUES (1, 1, 99, '277055b5-bd7b-4d0b-9653-6be79a9948ff', 'PRINTED', 1, 'DL6RST', '2026-08-16 17:52:49.607519+03:00');
INSERT INTO ticket_logs (id, show_id, zone_id, device_id, action, ticket_number, passcode, printed_at) VALUES (2, 1, 99, '277055b5-bd7b-4d0b-9653-6be79a9948ff', 'ENTERED', 1, '', '2026-08-16 17:53:17.524005+03:00');
INSERT INTO ticket_logs (id, show_id, zone_id, device_id, action, ticket_number, passcode, printed_at) VALUES (3, 1, 98, '277055b5-bd7b-4d0b-9653-6be79a9948ff', 'PRINTED', 1, 'A62HDR', '2026-08-16 17:56:36.824503+03:00');
SELECT setval('ticket_logs_id_seq', (SELECT COALESCE(MAX(id), 1) FROM ticket_logs));

COMMIT;
