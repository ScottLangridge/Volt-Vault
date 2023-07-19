# Volt Vault

The Volt Vault is a powerful tool for storing and monitoring statistics about your LiPo batteries. With Volt Vault, you can keep track of various battery metrics, such as cycle count, performance, and charging characteristics. This document outlines the system's interfaces, database tables, and the latest schema to help you get started with Volt Vault.

(Apologies for the over-enthusiasm of this readme... it, and half of this code, was written by Chat-GPT)

## Interfaces

### Charge Logger

The Charge Logger interface allows you to set up charge sessions and record battery charging information. Here's how it works:

1. **Start a Charge Session**: Begin a new charge session by specifying the batteries you are charging, the charger you are using, and the power source.
    
2. **Log Charging Details**: During the charge session, Volt Vault will prompt you to record the charging data, including voltage values.
    
3. **Monitor Charging Performance**: Volt Vault will store the charging information for future reference, enabling you to monitor the charging performance of your batteries and chargers.
    

## Database Tables

### Battery

- `id` (INTEGER PRIMARY KEY NOT NULL): Unique identifier for each battery.
- `code` (TEXT NOT NULL UNIQUE): Battery code, ensuring each code is unique.
- `cell_count` (INTEGER NOT NULL): Number of cells in the battery.
- `capacity` (INTEGER NOT NULL): Battery capacity in mAh.

### Drone

- `id` (INTEGER PRIMARY KEY NOT NULL): Unique identifier for each drone.
- `name` (TEXT NOT NULL UNIQUE): Drone name, ensuring each name is unique.
- `prop_size` (REAL): Propeller size used by the drone.

### Charger

- `id` (INTEGER PRIMARY KEY NOT NULL): Unique identifier for each charger.
- `name` (TEXT NOT NULL): Charger name.
- `min_output_voltage` (REAL): Minimum output voltage of the charger.
- `max_output_voltage` (REAL): Maximum output voltage of the charger.
- `min_output_current` (REAL): Minimum output current of the charger.
- `max_output_current` (REAL): Maximum output current of the charger.

### Power Source

- `id` (INTEGER PRIMARY KEY NOT NULL): Unique identifier for each power source.
- `name` (TEXT NOT NULL): Power source name.

### Flight

- `id` (INTEGER PRIMARY KEY NOT NULL): Unique identifier for each flight.
- `timestamp` (DATETIME NOT NULL): Date and time of the flight.
- `drone_id` (INTEGER NOT NULL): Foreign key referencing the Drone table.
- `battery_id` (INTEGER NOT NULL): Foreign key referencing the Battery table.
- `initial_volts` (REAL): Initial voltage of the battery before the flight.
- `final_volts` (REAL): Final voltage of the battery after the flight.
- `min_volts` (REAL): Minimum voltage recorded during the flight.
- `armed_time` (INTEGER): Duration the drone was armed during the flight (in seconds).
- `total_time` (INTEGER): Total duration of the flight (in seconds).
- Foreign key constraints reference the Drone and Battery tables.

### Charge Session

- `id` (INTEGER PRIMARY KEY NOT NULL): Unique identifier for each charge session.
- `batteries` (TEXT NOT NULL): Batteries being charged (stored as a string).
- `charger_id` (INTEGER NOT NULL): Foreign key referencing the Charger table.
- `power_source_id` (INTEGER NOT NULL): Foreign key referencing the Power Source table.
- Foreign key constraints reference the Charger and Power Source tables.

### Charge Value

- `id` (INTEGER PRIMARY KEY NOT NULL): Unique identifier for each charge value.
- `charge_session_id` (INTEGER NOT NULL): Foreign key referencing the Charge Session table.
- `timestamp` (DATETIME NOT NULL): Date and time of the charge value recording.
- `voltage_value` (REAL NOT NULL): Voltage value recorded during charging.
- Foreign key constraints reference the Charge Session table.

## Schema

The latest database schema is provided in the [initialize_database.sql](https://github.com/ScottLangridge/Volt-Vault/blob/master/initialise_db.sql) file. Please ensure that your database is set up correctly with this schema to use Volt Vault effectively.

To get started, run the `flight_logger.py` and `battery_logger.py` tools to log flight and battery details respectively. Enjoy using Volt Vault to keep track of your LiPo battery statistics!
