CREATE TABLE drone (
    drone_id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL UNIQUE,
    prop_size REAL
);

CREATE TABLE battery (
    battery_id INTEGER PRIMARY KEY NOT NULL,
    battery_code TEXT NOT NULL UNIQUE,
    cell_count INTEGER NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE charger (
    charger_id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    min_output_voltage REAL,
    max_output_voltage REAL,
    min_output_current REAL,
    max_output_current REAL
);

CREATE TABLE power_source (
    power_source_id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE flight (
    flight_id INTEGER PRIMARY KEY NOT NULL,
    timestamp DATETIME NOO NULL,
    drone_id INTEGER NOT NULL,
    battery_id INTEGER NOT NULL,
    initial_volts REAL,
    final_volts REAL,
    min_volts REAL,
    armed_time INTEGER,
    total_time INTEGER,
    FOREIGN KEY (drone_id) REFERENCES drone (drone_id),
    FOREIGN KEY (battery_id) REFERENCES battery (battery_id)
);

CREATE TABLE charge_session (
    charge_session_id INTEGER PRIMARY KEY NOT NULL,
    batteries TEXT NOT NULL,
    charger_id INTEGER NOT NULL,
    power_source_id INTEGER NOT NULL,
    FOREIGN KEY (charger_id) REFERENCES charger (charger_id),
    FOREIGN KEY (power_source_id) REFERENCES power_source (power_source_id)
);

CREATE TABLE charge_value (
    charge_value_id INTEGER PRIMARY KEY NOT NULL,
    charge_session_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    voltage_value REAL NOT NULL,
    FOREIGN KEY (charge_session_id) REFERENCES charge_session (charge_session_id)
);

