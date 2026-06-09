-- Base tables
CREATE TABLE IF NOT EXISTS people (
    person_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    DOB INTEGER NOT NULL,
    email TEXT,
    phone_num TEXT
);
CREATE TABLE IF NOT EXISTS plane_models (
    model TEXT PRIMARY KEY,
    capacity_kg INTEGER,
    range_km INTEGER,
    airspeed_kmh INTEGER
);
CREATE TABLE IF NOT EXISTS destinations (
    airport_code TEXT PRIMARY KEY,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
	parking_location TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS flights (
    fli_date INTEGER,
    fli_num TEXT,
    fli_status TEXT,
    PRIMARY KEY (fli_date, fli_num)
);

-- References to base tables
CREATE TABLE IF NOT EXISTS pilots (
    pil_id INTEGER PRIMARY KEY,
    flying_time_min INTEGER,
    FOREIGN KEY (pil_id) REFERENCES people (person_id)
    CHECK (pil_id < 100)
);
CREATE TABLE IF NOT EXISTS planes (
    reg TEXT PRIMARY KEY,
    model TEXT,
    FOREIGN KEY (model) REFERENCES plane_models (model)
);
CREATE TABLE IF NOT EXISTS crew (
    crew_id INTEGER PRIMARY KEY,
    role TEXT,
    FOREIGN KEY (crew_id) REFERENCES people (person_id)
    CHECK (crew_id >= 100 AND crew_id < 1000)
);

-- References to the previous tables
CREATE TABLE IF NOT EXISTS certifications (
    pil_id INTEGER,
    model TEXT,
    PRIMARY KEY (pil_id, model)
    FOREIGN KEY (pil_id) REFERENCES pilots (pil_id)
    FOREIGN KEY (model) REFERENCES plane_models (model)
);
CREATE TABLE IF NOT EXISTS manifests (
    man_id INTEGER PRIMARY KEY,
    pil_id INTEGER NOT NULL,
    copil_id INTEGER NOT NULL,
    FOREIGN KEY (pil_id) REFERENCES pilots (pil_id),
    FOREIGN KEY (copil_id) REFERENCES pilots (pil_id),
    CHECK (pil_id <> copil_id)
);

-- References to manifests
CREATE TABLE IF NOT EXISTS crew_manifests (
    c_man_id INTEGER,
    crew_id INTEGER,
    PRIMARY KEY (c_man_id, crew_id),
    FOREIGN KEY (c_man_id) REFERENCES manifests (man_id),
    FOREIGN KEY (crew_id) REFERENCES crew (crew_id)
);
CREATE TABLE IF NOT EXISTS passenger_manifests (
    p_man_id INTEGER,
    person_id INTEGER,
    PRIMARY KEY (p_man_id, person_id),
    FOREIGN KEY (p_man_id) REFERENCES manifests (man_id),
    FOREIGN KEY (person_id) REFERENCES people (person_id)
);
CREATE TABLE IF NOT EXISTS legs (
    fli_date INTEGER,
    fli_num TEXT,
    leg_id INTEGER,
    orig TEXT NOT NULL,
    dest TEXT NOT NULL,
    reg TEXT NOT NULL,
    man_id INTEGER NOT NULL,
    STD INTEGER,
    ATA INTEGER,
    PRIMARY KEY (fli_date, fli_num, leg_id),
    FOREIGN KEY (fli_date, fli_num) REFERENCES flights (fli_date, fli_num),
    FOREIGN KEY (orig) REFERENCES destinations (airport_code),
    FOREIGN KEY (dest) REFERENCES destinations (airport_code),
    FOREIGN KEY (reg) REFERENCES planes (reg),
    FOREIGN KEY (man_id) REFERENCES manifests (man_id)
);

-- Top level tables (views) are: pilots, manifests, destinations, planes, flights
-- columns in SELECT need to match fields in db_objects
CREATE VIEW IF NOT EXISTS PilotsView AS
    SELECT
        pil_id,
        flying_time_min,
        first_name,
        last_name,
        DOB,
        email,
        phone_num,
        model
    FROM pilots AS p
        JOIN people ON pil_id = person_id
        -- left join so that pilots without certs still appear
        NATURAL LEFT JOIN certifications
        NATURAL LEFT JOIN plane_models
    ORDER BY pil_id;

CREATE VIEW IF NOT EXISTS ManifestsView AS
    SELECT 
        man_id,
        m.pil_id,
        ppl.first_name,
        ppl.last_name,
        p.flying_time_min,
        m.copil_id,
        cppl.first_name,
        cppl.last_name,
        cp.flying_time_min AS copil_flying_time_min 
    FROM manifests AS m 
        JOIN pilots AS p ON m.pil_id = p.pil_id
        JOIN people AS ppl ON m.pil_id = ppl.person_id
        JOIN pilots AS cp ON m.copil_id = cp.pil_id
        JOIN people AS cppl ON m.copil_id = cppl.person_id;

CREATE VIEW IF NOT EXISTS DestinationsView AS
    SELECT
        airport_code,
        latitude,
        longitude,
        parking_location
    FROM destinations;

CREATE VIEW IF NOT EXISTS PlanesView AS
    SELECT
        reg,
        model,
        capacity_kg,
        range_km,
        airspeed_kmh
    FROM planes 
        NATURAL JOIN plane_models
        NATURAL JOIN planes;

-- Use WHERE clause to have the schedule of a pilot and JOIN with people
CREATE VIEW IF NOT EXISTS FlightsView AS
    SELECT
        fli_date,
        fli_num,
        fli_status,
        leg_id,
        orig,
        dest,
        reg,
        man_id,
        STD,
        ATA,
        pil_id,
        copil_id,
        model
    FROM flights 
        NATURAL JOIN legs
        NATURAL JOIN manifests
        NATURAL JOIN planes;

-- View to display details, this needs WHERE clause at query time
CREATE VIEW IF NOT EXISTS PilotDetails AS
    SELECT *
    FROM pilots
        JOIN people ON pil_id = person_id
        NATURAL JOIN certifications
        NATURAL JOIN plane_models;