from database import Database

class DroneLogger:
    def __init__(self, db_name):
        self.db = Database(db_name)
        self.db.connect()

    def log_drone(self):
        drone_name = input("Enter the drone name: ")
        prop_size = float(input("Enter the prop size in inches: "))

        self.db.insert('drone', {
            'name': drone_name,
            'prop_size': prop_size
        })

        print("\nDrone successfully logged.")

    def close_database(self):
        self.db.close()


if __name__ == "__main__":
    db_name = "your_database_name.db"  # Replace with your database file name
    drone_logger = DroneLogger(db_name)

    try:
        print("\nDrone Logger")
        while True:
            drone_logger.log_drone()

            option = input("\nDo you want to log another drone? (Y/N): ").strip().lower()
            if option == 'n':
                print("\nDrone Logger terminated.")
                break

    except KeyboardInterrupt:
        print("\nDrone Logger terminated.")

    drone_logger.close_database()

