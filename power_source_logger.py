from database import Database

class PowerSourceLogger:
    def __init__(self, db_name):
        self.db = Database(db_name)
        self.db.connect()  # Add this line to establish the database connection

    def log_power_source(self):
        name = input("Enter the name of the power source: ")

        self.db.insert('power_source', {
            'name': name
        })

        print("\nPower source successfully logged.")

    def close_database(self):
        self.db.close()


if __name__ == "__main__":
    db_name = "your_database_name.db"  # Replace with your database file name
    power_source_logger = PowerSourceLogger(db_name)

    try:
        print("\nPower Source Logger")
        while True:
            power_source_logger.log_power_source()

            option = input("\nDo you want to log another power source? (Y/N): ").strip().lower()
            if option == 'n':
                print("\nPower Source Logger terminated.")
                break

    except KeyboardInterrupt:
        print("\nPower Source Logger terminated.")

    power_source_logger.close_database()

