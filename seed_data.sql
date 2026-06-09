-- Generated with the help of Copilot

BEGIN TRANSACTION;

INSERT OR IGNORE INTO people (person_id, first_name, last_name, DOB, email, phone_num) VALUES
    -- Pilots (1-10)
    (1,  'Luca',   'Martel',   '1982-05-14', 'luca.martel@example.com',   '+41790001001'),
    (2,  'Nina',   'Keller',   '1988-11-03', 'nina.keller@example.com',   '+41790001002'),
    (3,  'Jonas',  'Meyer',    '1979-07-22', 'jonas.meyer@example.com',   '+41790001003'),
    (4,  'Sofia',  'Baumann',  '1986-04-18', 'sofia.baumann@example.com', '+41790001004'),
    (5,  'Marco',  'Rossi',    '1981-01-29', 'marco.rossi@example.com',   '+41790001005'),
    (6,  'Elena',  'Weber',    '1990-02-11', 'elena.weber@example.com',   '+41790001006'),
    (7,  'David',  'Frei',     '1987-09-09', 'david.frei@example.com',    '+41790001007'),
    (8,  'Anna',   'Lombard',  '1991-11-26', 'anna.lombard@example.com',  '+41790001008'),
    (9,  'Matteo', 'Gruber',   '1983-04-05', 'matteo.gruber@example.com', '+41790001009'),
    (10, 'Clara',  'Steiner',  '1993-05-17', 'clara.steiner@example.com', '+41790001010'),
    -- Crew (11-20)
    (111, 'Julie',  'Morel',    '1995-08-02', 'julie.morel@example.com',   '+41790001011'),
    (112, 'Ruben',  'Schmid',   '1992-12-14', 'ruben.schmid@example.com',  '+41790001012'),
    (113, 'Maya',   'Lopez',    '1997-02-27', 'maya.lopez@example.com',    '+41790001013'),
    (114, 'Theo',   'Vargas',   '1994-10-31', 'theo.vargas@example.com',   '+41790001014'),
    (115, 'Lea',    'Dupont',   '1996-08-19', 'lea.dupont@example.com',    '+41790001015'),
    (116, 'Victor', 'Rey',      '1989-03-08', 'victor.rey@example.com',    '+41790001016'),
    (117, 'Aline',  'Perrin',   '1990-06-21', 'aline.perrin@example.com',  '+41790001017'),
    (118, 'Noah',   'Berger',   '1994-01-12', 'noah.berger@example.com',   '+41790001018'),
    (119, 'Emma',   'Guidi',    '1993-09-23', 'emma.guidi@example.com',    '+41790001019'),
    (120, 'Ilan',   'Kunz',     '1991-07-30', 'ilan.kunz@example.com',     '+41790001020'),
    -- Passengers (21-25)
    (1021, 'Sarah',  'Renaud',   '1998-03-15', 'sarah.renaud@example.com',  '+41790001021'),
    (1022, 'Owen',   'Blanc',    '1985-11-07', 'owen.blanc@example.com',    '+41790001022'),
    (1023, 'Ines',   'Caruso',   '2000-01-24', 'ines.caruso@example.com',   '+41790001023'),
    (1024, 'Hugo',   'Muller',   '1996-09-05', 'hugo.muller@example.com',   '+41790001024'),
    (1025, 'Camille','Fournier', '1999-12-18', 'camille.fournier@example.com', '+41790001025');

INSERT OR IGNORE INTO plane_models (model, capacity_kg, range_km, airspeed_kmh) VALUES
    ('Cessna 208B GC EX',            1438, 1689, 343),
    ('Pilatus PC-12 NGX',            1060, 3269, 537),
    ('Beechcraft KA 360',            2334, 3345, 578),
    ('DHC-6-400 Twin Otter',         1842,  898, 337),
    ('ATR 42-600',                   5250, 1528, 535),
    ('ATR 72-600',                   7400,  930, 500),
    ('Dash 8-300',                   5166, 1483, 532),
    ('Embraer ERJ-145',              5322, 2873, 833),
    ('Embraer E175',                 9814, 3982, 871),
    ('Airbus A320-200',             16600, 5700, 904);

INSERT OR IGNORE INTO destinations (airport_code, latitude, longitude, parking_location) VALUES
    ('GVA', 46.238333,  6.109444, 'Terminal 1'),
    ('ZRH', 47.464720,  8.549170, 'Terminal 1'),
    ('BSL', 47.589600,  7.529910, 'Terminal A'),
    ('BRN', 46.914100,  7.497150, 'Terminal 1'),
    ('LYS', 45.725556,  5.081111, 'Terminal 1'),
    ('MXP', 45.630606,  8.728111, 'Terminal 2'),
    ('NCE', 43.658400,  7.215870, 'Terminal 1'),
    ('FRA', 50.026400,  8.543130, 'Terminal 1'),
    ('MUC', 48.353800, 11.786100, 'Terminal 3'),
    ('VIE', 48.110278, 16.569722, 'Terminal 1');

INSERT OR IGNORE INTO flights (fli_date, fli_num, fli_status) VALUES
    ('2026-06-10', 'BT101', 'arrived'),
    ('2026-06-10', 'BT102', 'arrived'),
    ('2026-06-10', 'BT103', 'arrived'),
    ('2026-06-11', 'BT104', 'arrived'),
    ('2026-06-11', 'BT105', 'arrived'),
    ('2026-06-11', 'BT106', 'arrived'),
    ('2026-06-12', 'BT107', 'arrived'),
    ('2026-06-12', 'BT108', 'arrived'),
    ('2026-06-13', 'BT109', 'arrived'),
    ('2026-06-13', 'BT110', 'scheduled');

INSERT OR IGNORE INTO pilots (pil_id, flying_time_min) VALUES
    (1, 756000),
    (2, 684000),
    (3, 822000),
    (4, 618000),
    (5, 792000),
    (6, 540000),
    (7, 588000),
    (8, 564000),
    (9, 726000),
    (10, 492000);

INSERT OR IGNORE INTO planes (reg, model) VALUES
    ('HB-TBA', 'Cessna 208B GC EX'),
    ('HB-TBB', 'Pilatus PC-12 NGX'),
    ('HB-TBC', 'Beechcraft KA 360'),
    ('HB-TBD', 'DHC-6-400 Twin Otter'),
    ('HB-TBE', 'ATR 42-600'),
    ('HB-TBF', 'ATR 72-600'),
    ('HB-TBG', 'Dash 8-300'),
    ('HB-TBH', 'Embraer ERJ-145'),
    ('HB-TBI', 'Embraer E175'),
    ('HB-TBJ', 'Airbus A320-200');

INSERT OR IGNORE INTO crew (crew_id, role) VALUES
    (111, 'Safety Officer'),
    (112, 'Flight Attendant'),
    (113, 'Flight Attendant'),
    (114, 'Cabin Crew'),
    (115, 'Loadmaster'),
    (116, 'Flight Attendant'),
    (117, 'Cabin Crew'),
    (118, 'Flight Medic'),
    (119, 'Loadmaster'),
    (120, 'Operations Escort');

INSERT OR IGNORE INTO certifications (pil_id, model) VALUES
    (1, 'Pilatus PC-12 NGX'),
    (2, 'Pilatus PC-12 NGX'),
    (3, 'Cessna 208B GC EX'),
    (4, 'Cessna 208B GC EX'),
    (5, 'DHC-6-400 Twin Otter'),
    (6, 'DHC-6-400 Twin Otter'),
    (7, 'ATR 42-600'),
    (8, 'ATR 42-600'),
    (9, 'ATR 72-600'),
    (10, 'Dash 8-300'),
    (2, 'Embraer ERJ-145'),
    (3, 'Embraer E175'),
    (4, 'Beechcraft KA 360'),
    (1, 'Airbus A320-200');

INSERT OR IGNORE INTO manifests (man_id, pil_id, copil_id) VALUES
    (1001, 1, 2),
    (1002, 3, 4),
    (1003, 5, 6),
    (1004, 7, 8),
    (1005, 9, 10),
    (1006, 2, 3),
    (1007, 4, 5),
    (1008, 6, 7),
    (1009, 8, 9),
    (1010, 1, 10);

INSERT OR IGNORE INTO crew_manifests (c_man_id, crew_id) VALUES
    (1001, 112),
    (1001, 115),
    (1002, 113),
    (1003, 118),
    (1003, 120),
    (1004, 116),
    (1005, 117),
    (1005, 119),
    (1006, 111),
    (1007, 114),
    (1007, 115),
    (1008, 118),
    (1009, 116),
    (1009, 120),
    (1010, 117);

INSERT OR IGNORE INTO passenger_manifests (p_man_id, person_id) VALUES
    (1001, 1021),
    (1001, 1022),
    (1002, 1023),
    (1002, 1024),
    (1003, 1025),
    (1004, 1021),
    (1004, 1023),
    (1005, 1022),
    (1006, 1024),
    (1006, 1025),
    (1007, 1021),
    (1008, 1022),
    (1009, 1023),
    (1010, 1024),
    (1010, 1025);

INSERT OR IGNORE INTO legs (fli_date, fli_num, leg_id, orig, dest, reg, man_id, STD, ATA) VALUES
    ('2026-06-10', 'BT101', 1, 'BRN', 'GVA', 'HB-TBB', 1001, '2026-06-10 07:45', '2026-06-10 08:40'),
    ('2026-06-10', 'BT102', 1, 'GVA', 'BRN', 'HB-TBA', 1002, '2026-06-10 09:30', '2026-06-10 10:25'),
    ('2026-06-10', 'BT103', 1, 'BSL', 'ZRH', 'HB-TBD', 1003, '2026-06-10 11:10', '2026-06-10 12:00'),
    ('2026-06-11', 'BT104', 1, 'ZRH', 'BRN', 'HB-TBE', 1004, '2026-06-11 12:35', '2026-06-11 13:20'),
    ('2026-06-11', 'BT104', 2, 'BRN', 'LYS', 'HB-TBE', 1004, '2026-06-11 14:00', '2026-06-11 14:55'),
    ('2026-06-11', 'BT105', 1, 'LYS', 'MXP', 'HB-TBF', 1005, '2026-06-11 14:15', '2026-06-11 15:10'),
    ('2026-06-11', 'BT106', 1, 'MXP', 'NCE', 'HB-TBG', 1006, '2026-06-11 16:10', '2026-06-11 17:00'),
    ('2026-06-12', 'BT107', 1, 'NCE', 'VIE', 'HB-TBH', 1007, '2026-06-12 17:50', '2026-06-12 19:15'),
    ('2026-06-12', 'BT108', 1, 'VIE', 'MUC', 'HB-TBI', 1008, '2026-06-12 20:20', '2026-06-12 21:25'),
    ('2026-06-13', 'BT109', 1, 'MUC', 'FRA', 'HB-TBC', 1009, '2026-06-13 08:15', '2026-06-13 09:05'),
    ('2026-06-13', 'BT110', 1, 'FRA', 'GVA', 'HB-TBJ', 1010, '2026-06-13 10:40', NULL);

COMMIT;