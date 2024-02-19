"""
Module that defines the functionality of the hotel reservations project
"""
import sqlite3


class DatabaseHandler:
    """
    A class to handle database operations for
    Hotel, Customer, and Reservation entities.
    """

    def __init__(self, db_name):
        """
        Initialize the DatabaseHandler with the given database name.
        """
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA SQLITE_ALLOW_EMPTY_STRING = 0")
        self.cursor = self.connection.cursor()
        self.create_tables_if_not_exist()

    def create_tables_if_not_exist(self):
        """
        Create the tables if they don't already exist in the database.
        """
        create_hotel_table = """
            CREATE TABLE IF NOT EXISTS "Hotel" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "NAME"	TEXT NOT NULL UNIQUE,
                "LOCATION"	TEXT NOT NULL UNIQUE,
                PRIMARY KEY("ID" AUTOINCREMENT)
            )
        """
        create_customer_table = """
            CREATE TABLE IF NOT EXISTS "Customer" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "NAME"	TEXT NOT NULL,
                "EMAIL"	TEXT NOT NULL UNIQUE,
                PRIMARY KEY("ID" AUTOINCREMENT)
            )
        """
        create_reservation_table = """
            CREATE TABLE IF NOT EXISTS "Reservation" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "HOTEL_ID"	INTEGER NOT NULL,
                "CUSTOMER_ID"	INTEGER NOT NULL,
                "DATE"	TEXT NOT NULL,
                "NIGHTS"	INTEGER NOT NULL,
                FOREIGN KEY("HOTEL_ID")
                    REFERENCES "Hotel"("ID") ON DELETE RESTRICT,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("CUSTOMER_ID")
                    REFERENCES "Customer"("ID") ON DELETE RESTRICT
            )
        """

        self.cursor.execute(create_hotel_table)
        self.cursor.execute(create_customer_table)
        self.cursor.execute(create_reservation_table)
        self.connection.commit()

    def close_connection(self):
        """
        Close the database connection.
        """
        self.connection.close()

    def create_hotel(self, name=None, location=None):
        """
        Create a new hotel record in the database.
        """
        try:
            self.cursor.execute(
                "INSERT INTO Hotel (NAME, LOCATION) VALUES (?, ?)",
                (name, location)
            )
            self.connection.commit()
            return Hotel(self.cursor.lastrowid, name, location)
        except sqlite3.IntegrityError as ex:
            print("No hotel was created. Review the entered data")
            print(ex)
            return None

    def create_customer(self, name=None, email=None):
        """
        Create a new customer record in the database.
        """
        try:
            self.cursor.execute(
                "INSERT INTO Customer (NAME, EMAIL) VALUES (?, ?)",
                (name, email)
            )
            self.connection.commit()
            return Customer(self.cursor.lastrowid, name, email)
        except sqlite3.IntegrityError as ex:
            print("No customer was created. Review the entered data")
            print(ex)
            return None

    def create_reservation(self,
                           hotel_id=None,
                           customer_id=None,
                           date=None,
                           nights=None):
        """
        Create a new reservation record in the database.
        """
        try:
            self.cursor.execute(
                (
                    "INSERT INTO Reservation "
                    "(HOTEL_ID, CUSTOMER_ID, DATE, NIGHTS) "
                    "VALUES (?, ?, ?, ?)"
                ),
                (hotel_id, customer_id, date, nights)
            )
            self.connection.commit()
            return Reservation(
                self.cursor.lastrowid,
                hotel_id, customer_id,
                date,
                nights
            )
        except sqlite3.IntegrityError as ex:
            print("No reservation was created. Review the entered data")
            print(ex)
            return None

    def update_hotel(self, hotel_id, name, location):
        """
        Update the attributes of a hotel record in the database.
        """
        self.cursor.execute(
            "UPDATE Hotel SET NAME = ?, LOCATION = ? WHERE ID = ?",
            (name, location, hotel_id)
        )
        self.connection.commit()

    def update_customer(self, customer_id, name, email):
        """
        Update the attributes of a customer record in the database.
        """
        self.cursor.execute(
            "UPDATE Customer SET name = ?, email = ? WHERE ID = ?",
            (name, email, customer_id)
        )
        self.connection.commit()

    def update_reservation(self,
                           reservation_id,
                           hotel_id,
                           customer_id,
                           date,
                           nights):
        """
        Update the attributes of a reservation record in the database.
        """
        self.cursor.execute(
            (
                "UPDATE Reservation SET HOTEL_ID = ?, "
                "CUSTOMER_ID = ?, DATE = ?, NIGHTS = ? WHERE ID = ?"
            ),
            (hotel_id, customer_id, date, nights, reservation_id)
        )
        self.connection.commit()

    def delete_hotel(self, hotel_id):
        """
        Delete a hotel record from the database.
        """
        if not self.get_hotel_by_id(hotel_id):
            raise ValueError("No hotel was deleted. Review the entered data")
        self.cursor.execute("DELETE FROM Hotel WHERE ID = ?", (hotel_id,))
        self.connection.commit()

    def delete_customer(self, customer_id):
        """
        Delete a customer record from the database.
        """
        if not self.get_customer_by_id(customer_id):
            raise ValueError
        self.cursor.execute(
            "DELETE FROM Customer WHERE ID = ?",
            (customer_id,)
        )
        self.connection.commit()

    def delete_reservation(self, reservation_id):
        """
        Delete a reservation record from the database.
        """
        if not self.get_reservation_by_id(reservation_id):
            raise ValueError(
                "No reservation was deleted. Review the entered data"
            )

        self.cursor.execute(
            "DELETE FROM Reservation WHERE ID = ?",
            (reservation_id,)
        )
        self.connection.commit()

    def get_hotel_by_id(self, hotel_id):
        """
        Retrieve a hotel record from the database by its ID.
        """
        self.cursor.execute("SELECT * FROM Hotel WHERE ID = ?", (hotel_id,))
        result = self.cursor.fetchone()
        return Hotel(*result) if result else None

    def get_customer_by_id(self, customer_id):
        """
        Retrieve a customer record from the database by its ID.
        """
        self.cursor.execute(
            "SELECT * FROM Customer WHERE ID = ?",
            (customer_id,)
        )
        result = self.cursor.fetchone()
        return Customer(*result) if result else None

    def get_reservation_by_id(self, reservation_id):
        """
        Retrieve a reservation record from the database by its ID.
        """
        self.cursor.execute(
            "SELECT * FROM Reservation WHERE ID = ?",
            (reservation_id,)
        )
        result = self.cursor.fetchone()
        return Reservation(*result) if result else None

    def get_hotel_by_name(self, hotel_name):
        """
        Retrieve a hotel record from the database by its name.
        """
        self.cursor.execute(
            "SELECT * FROM Hotel WHERE NAME = ?",
            (hotel_name,)
        )
        result = self.cursor.fetchone()
        return Hotel(*result) if result else None

    def get_customer_by_email(self, customer_email):
        """
        Retrieve a customer record from the database by its email.
        """
        self.cursor.execute(
            "SELECT * FROM Customer WHERE EMAIL = ?",
            (customer_email,)
        )
        result = self.cursor.fetchone()
        return Customer(*result) if result else None

    def get_reservation_by_details(self, hotel_name, customer_email, date):
        """
        Retrieve a reservation record from the database by its ID.
        """
        hotel = self.get_hotel_by_name(hotel_name)
        customer = self.get_customer_by_email(customer_email)

        self.cursor.execute(
            (
                "SELECT * FROM Reservation WHERE"
                "HOTEL_ID = ? AND CUSTOMER_ID = ? AND DATE = ?"
            ),
            (hotel.hotel_id, customer.customer_id, date)
        )
        result = self.cursor.fetchone()
        return Reservation(*result) if result else None


class Hotel:
    """
    A class to represent a hotel entity.
    """

    def __init__(self, hotel_id, name, location):
        """
        Initialize the Hotel object with the given attributes.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location

    def __str__(self):
        """
        Return a string representation of the Hotel object.
        """
        return f"{self.name} ({self.location})"


class Customer:
    """
    A class to represent a customer entity.
    """

    def __init__(self, customer_id, name, email):
        """
        Initialize the Customer object with the given attributes.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def __str__(self):
        """
        Return a string representation of the Customer object.
        """
        return f"{self.name} ({self.email})"


class Reservation:
    """
    A class to represent a reservation entity.
    """

    def __init__(self,
                 reservation_id,
                 hotel_id,
                 customer_id,
                 check_in_date,
                 nights
                 ):
        """
        Initialize the Reservation object with the given attributes.
        """
        self.reservation_id = reservation_id
        self.hotel_id = hotel_id
        self.customer_id = customer_id
        self.check_in_date = check_in_date
        self.nights = nights

    def __str__(self):
        """
        Return a string representation of the Reservation object.
        """
        return f"Reservation ID: {self.reservation_id},"\
            f"Hotel ID: {self.hotel_id},"\
            f"Customer ID: {self.customer_id},"\
            f"Check-in: {self.check_in_date},"\
            f"Nights: {self.nights}"
