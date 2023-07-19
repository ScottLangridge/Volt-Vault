from database import Database
import datetime

class FlightLogger:
    def __init__(self, db_name):
        self.db = Database(db_name)
        self.db.connect()

    def log_flight(self, drone_id):
        drone_name = self.get_drone_name(drone_id)

        battery_code = input("Enter the battery code: ")
        battery_id = self.get_battery_id(battery_code)
        initial_voltage = float(input("Enter the initial voltage: "))

        input("Hit enter to begin the flight.")
        timestamp = datetime.datetime.now()

        print("\nFlight in progress.")
        input("Hit enter to end the flight.")

        final_voltage = float(input("Enter the final voltage: "))
        min_voltage = float(input("Enter the minimum voltage: "))
        armed_time = int(input("Enter the arm time (in seconds): "))
        total_time = int(input("Enter the total time (in seconds): "))

        print("\nFlight Summary:")
        print(f"Drone: {drone_name}")
        print(f"Battery: {battery_code}")
        print(f"Initial Voltage: {initial_voltage}")
        print(f"Final Voltage: {final_voltage}")
        print(f"Minimum Voltage: {min_voltage}")
        print(f"Armed Time: {armed_time} seconds")
        print(f"Total Time: {total_time} seconds")

        confirm = input("\nAre you happy with these choices? (Y/N): ").strip().lower()

        if confirm == 'n':
            drone_id, battery_id, initial_voltage, final_voltage, min_voltage, armed_time, total_time = self.change_flight_details(
                drone_id, battery_id, initial_voltage,
                final_voltage, min_voltage, armed_time, total_time
            )

        self.db.insert('flight', {
            'timestamp': timestamp,
            'drone_id': drone_id,
            'battery_id': battery_id,
            'initial_volts': initial_voltage,
            'final_volts': final_voltage,
            'min_volts': min_voltage,
            'armed_time': armed_time,
            'total_time': total_time
        })

        print("\nFlight successfully logged.")

    def change_flight_details(self, drone_id, battery_id, initial_voltage,
                              final_voltage, min_voltage, armed_time, total_time):
        while True:
            print("\nChange Flight Details:")
            print("1. Change Drone")
            print("2. Change Battery")
            print("3. Change Initial Voltage")
            print("4. Change Final Voltage")
            print("5. Change Minimum Voltage")
            print("6. Change Armed Time")
            print("7. Change Total Time")
            print("8. Confirm and Log Flight")
            choice = input("Enter your choice (1-8): ")

            if choice == '1':
                drone_name = input("Enter the new drone name: ")
                drone_id = self.get_drone_id(drone_name)
            elif choice == '2':
                battery_code = input("Enter the new battery code: ")
                battery_id = self.get_battery_id(battery_code)
            elif choice == '3':
                initial_voltage = float(input("Enter the new initial voltage: "))
            elif choice == '4':
                final_voltage = float(input("Enter the new final voltage: "))
            elif choice == '5':
                min_voltage = float(input("Enter the new minimum voltage: "))
            elif choice == '6':
                armed_time = int(input("Enter the new arm time (in seconds): "))
            elif choice == '7':
                total_time = int(input("Enter the new total time (in seconds): "))
            elif choice == '8':
                break
            else:
                print("Invalid choice. Please try again.")

        return drone_id, battery_id, initial_voltage, final_voltage, min_voltage, armed_time, total_time

    def get_drone_id(self, drone_name):
        while True:
            drone_data = self.db.select('drone', f"name = '{drone_name}'")
            if drone_data:
                return drone_data[0][0]
            else:
                print(f"Drone '{drone_name}' not found.")
                drone_name = input("Please enter a valid drone name: ")

    def get_drone_name(self, drone_id):
        drone_data = self.db.select('drone', f"drone_id = {drone_id}")
        if drone_data:
            return drone_data[0][1]
        else:
            return None

    def get_battery_id(self, battery_code):
        while True:
            battery_data = self.db.select('battery', f"battery_code = '{battery_code}'")
            if battery_data:
                return battery_data[0][0]
            else:
                print(f"Battery '{battery_code}' not found.")
                battery_code = input("Please enter a valid battery code: ")

    def close_database(self):
        self.db.close()


if __name__ == "__main__":
    db_name = "your_database_name.db"  # Replace with your database file name
    drone_name = input("Enter the drone name: ")
    flight_logger = FlightLogger(db_name)

    try:
        print("\nFlight Logger")
        drone_id = flight_logger.get_drone_id(drone_name)
        while True:
            flight_logger.log_flight(drone_id)

            option = input("\nDo you want to log another flight? (Y/N): ").strip().lower()
            if option == 'n':
                print("\nFlight Logger terminated.")
                break

    except KeyboardInterrupt:
        print("\nFlight Logger terminated.")

    flight_logger.close_database()

