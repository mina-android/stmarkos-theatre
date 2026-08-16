-- Seed Data imported from Copy of Neiruz Tickets 2026.xlsm
BEGIN;

TRUNCATE TABLE shows CASCADE;

-- Show 1
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (1, 'اوبريت '''' اسرة عمانوئيل', '11', '2026-09-01', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (1, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (1, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (1, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (1, 'D', 155, 155);

-- Show 2
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (2, 'كورال '''' اسرة البابا كيرلس والمريمات', '12', '2026-09-01', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (2, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (2, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (2, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (2, 'D', 155, 155);

-- Show 3
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (3, 'اوبريت '''' اسرة رسل بنات', '13', '2026-09-02', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (3, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (3, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (3, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (3, 'D', 155, 155);

-- Show 4
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (4, 'اوبريت '''' اسرة تيموثاوس و مورا', '14', '2026-09-02', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (4, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (4, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (4, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (4, 'D', 155, 155);

-- Show 5
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (5, 'اوبريت '''' اسرة ابرار 1', '15', '2026-09-03', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (5, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (5, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (5, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (5, 'D', 155, 155);

-- Show 6
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (6, 'مسرحية '''' اسرة ابرار 2', '16', '2026-09-03', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (6, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (6, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (6, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (6, 'D', 155, 155);

-- Show 7
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (7, 'كورال '''' اسرة قديسين', '17', '2026-09-05', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (7, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (7, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (7, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (7, 'D', 155, 155);

-- Show 8
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (8, 'مسرحية '''' اسرة قديسين', '18', '2026-09-05', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (8, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (8, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (8, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (8, 'D', 155, 155);

-- Show 9
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (9, 'اوبريت '''' اسرة رسل ولاد', '19', '2026-09-06', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (9, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (9, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (9, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (9, 'D', 155, 155);

-- Show 10
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (10, 'مسرحية '''' اسرة محبة', '20', '2026-09-06', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (10, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (10, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (10, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (10, 'D', 155, 155);

-- Show 11
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (11, 'كورال '''' اسرة سمعان الشيخ', '21', '2026-09-07', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (11, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (11, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (11, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (11, 'D', 155, 155);

-- Show 12
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (12, 'مسرحية '''' اسرة أباء', '22', '2026-09-07', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (12, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (12, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (12, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (12, 'D', 155, 155);

-- Show 13
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (13, 'اوبريت '''' اسرة ماربنهام و سارة أولاد', '23', '2026-09-08', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (13, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (13, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (13, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (13, 'D', 155, 155);

-- Show 14
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (14, 'مسرحية '''' اسرة ماربنهام و سارة بنات', '24', '2026-09-08', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (14, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (14, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (14, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (14, 'D', 155, 155);

-- Show 15
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (15, 'اوبريت '''' اسرة اباء بنات', '25', '2026-09-09', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (15, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (15, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (15, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (15, 'D', 155, 155);

-- Show 16
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (16, 'كورال '''' اسرة الشهيد بروفوريوس', '26', '2026-09-09', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (16, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (16, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (16, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (16, 'D', 155, 155);

-- Show 17
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (17, 'اوبريت '''' اسرة نبيات', '27', '2026-09-12', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (17, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (17, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (17, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (17, 'D', 155, 155);

-- Show 18
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (18, 'كورال '''' اسرة محبة', '28', '2026-09-12', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (18, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (18, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (18, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (18, 'D', 155, 155);

-- Show 19
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (19, 'كورال '''' اسرة نيقولاوس', '29', '2026-09-13', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (19, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (19, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (19, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (19, 'D', 155, 155);

-- Show 20
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (20, 'كورال '''' اسرة الانبا رويس', '30', '2026-09-13', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (20, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (20, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (20, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (20, 'D', 155, 155);

-- Show 21
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (21, 'كورال '''' اسرة شهيدات', '31', '2026-09-14', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (21, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (21, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (21, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (21, 'D', 155, 155);

-- Show 22
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (22, 'اوبريت '''' اسرة الانبا كاراس', '32', '2026-09-14', '18:30', '20:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (22, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (22, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (22, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (22, 'D', 155, 155);

-- Show 23
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (23, 'مسرحية '''' اسرة انبياء اولاد', '33', '2026-09-15', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (23, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (23, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (23, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (23, 'D', 155, 155);

-- Show 24
INSERT INTO shows (id, name, prefix, date, time, end_time) VALUES (24, 'مسرحية '''' اسرة الكاروز', '34', '2026-09-15', '20:00', '22:00');
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (24, 'A', 125, 125);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (24, 'B', 20, 20);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (24, 'C', 110, 110);
INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (24, 'D', 155, 155);

COMMIT;
