from database import Database

class BatteryLogger:
    def __init__(self, db_name):
        self.db = Database(db_name)
        self.db.connect()

    def log_battery(self):
        battery_code = input("Enter the battery code: ")
        cell_count = int(input("Enter the cell count: "))
        capacity = int(input("Enter the capacity in mAh: "))

        self.db.insert('battery', {
            'battery_code': battery_code,
            'cell_count': cell_count,
            'capacity': capacity
        })

        print("\nBattery successfully logged.")

    def close_database(self):
        self.db.close()


if __name__ == "__main__":
    db_name = "your_database_name.db"  # Replace with your database file name
    battery_logger = BatteryLogger(db_name)

    try:
        print("\nBattery Logger")
        while True:
            battery_logger.log_battery()

            option = input("\nDo you want to log another battery? (Y/N): ").strip().lower()
            if option == 'n':
                print("\nBattery Logger terminated.")
                break

    except KeyboardInterrupt:
        print("\nBattery Logger terminated.")

    battery_logger.close_database()

