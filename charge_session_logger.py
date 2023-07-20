from database import Database
import datetime

class ChargeSessionLogger:
    def __init__(self, db_name):
        self.db = Database(db_name)
        self.db.connect()

    def log_charge_session(self):
        battery_codes, battery_ids = self.get_batteries()
        charger_name, charger_id = self.get_charger()
        power_source_name, power_source_id = self.get_power_source()

        initial_voltage = float(input("Enter the initial charge voltage: "))

        print("\nCharge Session Summary:")
        print(f"Batteries: {', '.join(battery_codes)}")
        print(f"Charger: {charger_name}")
        print(f"Power Source: {power_source_name}")
        print(f"Initial Voltage: {initial_voltage}V")

        input("\nPress enter to start the charge session.")
        timestamp = datetime.datetime.now()
        charge_values = [[timestamp, initial_voltage]]

        print("\nCharge Session in progress.")
        while True:
            voltage = input("Enter the current voltage (or 'done' to finish): ")
            if voltage.lower() == 'done':
                break

            try:
                voltage = float(voltage)
                timestamp = datetime.datetime.now()
                charge_values.append([timestamp, voltage])
            except ValueError:
                print("Invalid voltage value. Please enter a valid number.")

        print("\nCharge Session Summary:")
        print(f"Batteries: {', '.join(battery_codes)}")
        print(f"Charger: {charger_name}")
        print(f"Power Source: {power_source_name}")
        print(f"Initial Voltage: {initial_voltage}V")

        confirm = input("\nAre you happy with these choices? (Y/N): ").strip().lower()

        charge_session_details = battery_ids, charger_id, power_source_id, initial_voltage, charge_values
        if confirm == 'n':
            charge_session_details = self.change_charge_session_details(charge_session_details)

        self.commit_charge_session(charge_session_details)
        print("\nCharge session successfully logged.")

    def change_charge_session_details(self, charge_session_details):
        battery_ids, charger_id, power_source_id, initial_voltage, charge_values = charge_session_details
        while True:
            print("\nChange Charge Session Details:")
            print("1. Change Batteries")
            print("2. Change Charger")
            print("3. Change Power Source")
            print("4. Change Initial Voltage")
            print("5. Change charge values")
            print("6. Confirm charge session details")
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                battery_codes, battery_ids = self.get_batteries()
            elif choice == '2':
                charger_name, charger_id = self.get_charger()
            elif choice == '3':
                power_source_name, power_source_id = self.get_power_source()
            elif choice == '4':
                initial_voltage = float(input("Enter the new initial voltage: "))
            elif choice == '5':
                charge_values = self.change_charge_values(charge_values)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

        return battery_ids, charger_id, power_source_id, initial_voltage, charge_values

    def change_charge_values(self, charge_values):
        while True:
            print("\nCharge Values:")
            [print(f'Timestamp: {v[0]}, Voltage: {v[1]}') for i, v in enumerate(charge_values)]

            print("\n1. Update Voltage")
            print("2. Delete Voltage")
            print("3. Confirm and return to session details")
            choice = input("Enter your choice (1-3): ")

            if choice == '3':
                break
            
            if choice not in ['1', '2']:
                print("Invalid choice. Please try again.")
                continue

            print("\nSelect Charge Value:")
            [print(f'{i + 1}. Timestamp: {v[0]}, Voltage: {v[1]}') for i, v in enumerate(charge_values)]
            index = int(input("Enter your choice: ")) - 1

            if choice == '1':
                while True:
                    try:
                        new_voltage = float(input("Enter the new charge voltage: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid numeric value for the voltage.")

                charge_values[index][1] = new_voltage
                print("Voltage updated.")
            elif choice == '2':
                charge_values.pop(index)
                print("Voltage deleted.")

        return charge_values

    def get_batteries(self):
        battery_ids = []
        battery_codes = []
        num_batteries = int(input("Enter the number of batteries you are charging in parallel: "))
        for i in range(num_batteries):
            battery_code, battery_id = self.get_battery()
            battery_ids.append(battery_id)
            battery_codes.append(battery_code)

        return battery_codes, battery_ids

    def get_battery(self):
        while True:
            battery_code = input("Enter the battery code: ")
            battery_data = self.db.select('battery', f"battery_code = '{battery_code}'")
            if battery_data:
                battery_id = battery_data[0][0]
                return battery_code, battery_id
            else:
                print(f"Battery '{battery_code}' not found.")

    def get_charger(self):
        while True:
            charger_name = input("Enter the charger name: ")
            charger_data = self.db.select('charger', f"name = '{charger_name}'")
            if charger_data:
                charger_id = charger_data[0][0]
                return charger_name, charger_id
            else:
                print(f"Charger '{charger_name}' not found.")

    def get_power_source(self):
        while True:
            power_source_name = input("Enter the name of the power source: ")
            power_source_data = self.db.select('power_source', f"name = '{power_source_name}'")
            if power_source_data:
                power_source_id = power_source_data[0][0]
                return power_source_name, power_source_id
            else:
                print(f"Power source '{power_source_name}' not found.")

    def commit_charge_session(self, charge_session_details):
        battery_ids, charger_id, power_source_id, initial_voltage, charge_values = charge_session_details

        with self.db.conn:
            cursor = self.db.conn.cursor()
            batteries_str = ','.join(str(battery_id) for battery_id in battery_ids)
            query = "INSERT INTO charge_session (batteries, charger_id, power_source_id) VALUES (?, ?, ?)"
            cursor.execute(query, (batteries_str, charger_id, power_source_id))
            charge_session_id = cursor.lastrowid

            query = "INSERT INTO charge_value (charge_session_id, timestamp, voltage_value) VALUES (?, ?, ?)"
            cursor.executemany(query, [(charge_session_id, ts, voltage) for ts, voltage in charge_values])

    def close_database(self):
        self.db.close()


if __name__ == "__main__":
    db_name = "your_database_name.db"  # Replace with your database file name
    charge_session_logger = ChargeSessionLogger(db_name)

    try:
        print("\nCharge Session Logger")
        charge_session_logger.log_charge_session()

    except KeyboardInterrupt:
        print("\nCharge Session Logger terminated.")

    charge_session_logger.close_database()

