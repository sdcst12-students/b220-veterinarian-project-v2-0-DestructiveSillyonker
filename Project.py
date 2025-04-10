import sqlite3
import os
import platform

# Client class to handle client data and updates
class Client:
    def __init__(self, client_id, first_name, last_name, phone_num, email, address, city, postal_code):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_num = phone_num
        self.email = email
        self.address = address
        self.city = city
        self.postal_code = postal_code

    def update(self, field, new_value):
        setattr(self, field, new_value)

    def display(self):
        print(f"ID         : {self.client_id}")
        print(f"First Name : {self.first_name}")
        print(f"Last Name  : {self.last_name}")
        print(f"Phone Num  : {self.phone_num}")
        print(f"Email      : {self.email}")
        print(f"Address    : {self.address}")
        print(f"City       : {self.city}")
        print(f"Postal Code: {self.postal_code}")

# Database class to handle interactions with SQLite
class VeterinaryDatabase:
    def __init__(self, db_name='veterinary_db.sqlite3'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            phone_num TEXT,
            email TEXT,
            address TEXT,
            city TEXT,
            postal_code TEXT
        )
        ''')
        self.conn.commit()

    def fetch_client(self, client_id):
        self.cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        client = self.cursor.fetchone()
        if client:
            return Client(*client)
        return None

    def update_client_in_db(self, client_id, field, new_value):
        field_map = {
            "first_name": "first_name",
            "last_name": "last_name",
            "phone_num": "phone_num",
            "email": "email",
            "address": "address",
            "city": "city",
            "postal_code": "postal_code"
        }
        if field not in field_map:
            print("Invalid field!")
            return

        self.cursor.execute(f"UPDATE clients SET {field_map[field]} = ? WHERE id = ?", (new_value, client_id))
        self.conn.commit()
        print(f"{field.replace('_', ' ').title()} updated to: {new_value}")

    def insert_sample_data(self):
        # Ensure there's data with client ID 50
        self.cursor.execute("SELECT * FROM clients WHERE id = 50")
        if not self.cursor.fetchone():  # If no client with ID 50 exists, insert one
            self.cursor.execute('''
            INSERT INTO clients (id, first_name, last_name, phone_num, email, address, city, postal_code) 
            VALUES (50, 'Joe', 'Mama', '6049222222', 'joe@lunchbox.ca', '950 53rd Street', 'Delta', 'V4M3B7')
            ''')
            self.conn.commit()

    def save_info(self):
        print("Information saved successfully.")

    def close(self):
        self.conn.close()

# Function to clear the terminal screen
def clear_screen():
    system_name = platform.system()
    if system_name == "Windows":
        os.system('cls')  # Clear for Windows
    else:
        os.system('clear')  # Clear for Unix/Linux/Mac

# Main system class to interact with the user
class VeterinarySystem:
    def __init__(self):
        self.db = VeterinaryDatabase()
        self.db.insert_sample_data()  # Ensure data is inserted
        self.client_id = 50  # Assume we are working with client ID 50

    def display_menu(self):
        print("\nChoose:")
        print("A: change first name")
        print("B: change last name")
        print("C: change phone number")
        print("D: change email")
        print("E: change address")
        print("F: change city")
        print("G: change postal code")
        print("I: update information")
        print("> ", end="")

    def run(self):
        client = self.db.fetch_client(self.client_id)

        if not client:
            print("Client not found!")
            return
        
        while True:
            clear_screen()  # Clear the terminal screen after every update
            client.display()  # Display current client information
            self.display_menu()  # Show menu options

            choice = input().strip().lower()

            if choice == "a":
                new_first_name = input("Enter new First Name: ")
                client.update("first_name", new_first_name)
                self.db.update_client_in_db(self.client_id, "first_name", new_first_name)
            elif choice == "b":
                new_last_name = input("Enter new Last Name: ")
                client.update("last_name", new_last_name)
                self.db.update_client_in_db(self.client_id, "last_name", new_last_name)
            elif choice == "c":
                new_phone_num = input("Enter new Phone Number: ")
                client.update("phone_num", new_phone_num)
                self.db.update_client_in_db(self.client_id, "phone_num", new_phone_num)
            elif choice == "d":
                new_email = input("Enter new Email: ")
                client.update("email", new_email)
                self.db.update_client_in_db(self.client_id, "email", new_email)
            elif choice == "e":
                new_address = input("Enter new Address: ")
                client.update("address", new_address)
                self.db.update_client_in_db(self.client_id, "address", new_address)
            elif choice == "f":
                new_city = input("Enter new City: ")
                client.update("city", new_city)
                self.db.update_client_in_db(self.client_id, "city", new_city)
            elif choice == "g":
                new_postal_code = input("Enter new Postal Code: ")
                client.update("postal_code", new_postal_code)
                self.db.update_client_in_db(self.client_id, "postal_code", new_postal_code)
            elif choice == "i":
                self.db.save_info()  # Simulate saving info
            elif choice == "q":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")

# Start the program
if __name__ == "__main__":
    system = VeterinarySystem()
    system.run()

    # Close the database connection when finished
    system.db.close()
 