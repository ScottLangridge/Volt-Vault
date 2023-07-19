from database import Database

class ChargerLogger:
    def __init__(self, db_name):
        self.db = Database(db_name)
        self.db.connect()

    def log_charger(self):
        name = input("Enter the charger name: ")
        min_output_voltage = float(input("Enter the minimum output voltage: "))
        max_output_voltage = float(input("Enter the maximum output voltage: "))
        min_output_current = float(input("Enter the minimum output current: "))
        max_output_current = float(input("Enter the maximum output current: "))

        self.db.insert('charger', {
            'name': name,
            'min_output_voltage': min_output_voltage,
            'max_output_voltage': max_output_voltage,
            'min_output_current': min_output_current,
            'max_output_current': max_output_current
        })

        print("\nCharger successfully logged.")

    def close_database(self):
        self.db.close()


if __name__ == "__main__":
    db_name = "your_database_name.db"  # Replace with your database file name
    charger_logger = ChargerLogger(db_name)

    try:
        print("\nCharger Logger")
        while True:
            charger_logger.log_charger()

            option = input("\nDo you want to log another charger? (Y/N): ").strip().lower()
            if option == 'n':
                print("\nCharger Logger terminated.")
                break

    except KeyboardInterrupt:
        print("\nCharger Logger terminated.")

    charger_logger.close_database()

