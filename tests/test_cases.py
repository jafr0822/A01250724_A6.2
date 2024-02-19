"""
Module that defines test cases for the hotel reservations project
"""
import sqlite3
import unittest

from reservation_system.res_system import (
    Customer,
    DatabaseHandler,
    Hotel,
    Reservation,
)


class TestDatabaseHandler(unittest.TestCase):
    """
    A class containing unit tests for the DatabaseHandler class.
    """
    def setUp(self):
        # Create a temporary database
        self.db_name = ":memory:"
        # self.db_name = "data/database.db"
        self.db_handler = DatabaseHandler(self.db_name)

    def tearDown(self):
        # Close the database connection
        self.db_handler.close_connection()

    def test_update_hotel(self):
        """
        Test the hotel updating methods
        """
        hotel = self.db_handler.create_hotel("Hotel A", "Location A")
        self.db_handler.update_hotel(
            hotel.hotel_id,
            "Updated Hotel A",
            "Updated Location A"
        )
        updated_hotel = self.db_handler.get_hotel_by_id(hotel.hotel_id)

        self.assertEqual(updated_hotel.name, "Updated Hotel A")
        self.assertEqual(updated_hotel.location, "Updated Location A")

    def test_delete_hotel(self):
        """
        Test the hotel deleting methods
        """
        hotel = self.db_handler.create_hotel("Hotel A", "Location A")
        self.db_handler.delete_hotel(hotel.hotel_id)
        deleted_hotel = self.db_handler.get_hotel_by_id(hotel.hotel_id)

        self.assertIsNone(deleted_hotel)

    def test_update_customer(self):
        """
        Test the customer updating methods
        """
        customer = self.db_handler.create_customer(
            "John Doe",
            "john@example.com"
        )
        self.db_handler.update_customer(
            customer.customer_id,
            "Jane Smith",
            "jane@example.com"
        )
        updated_customer = self.db_handler.get_customer_by_id(
            customer.customer_id
        )

        self.assertEqual(updated_customer.name, "Jane Smith")
        self.assertEqual(updated_customer.email, "jane@example.com")

    def test_delete_customer(self):
        """
        Test the customer deleting methods
        """
        customer = self.db_handler.create_customer(
            "John Doe",
            "john@example.com"
        )
        self.db_handler.delete_customer(customer.customer_id)
        deleted_customer = self.db_handler.get_customer_by_id(
            customer.customer_id
        )

        self.assertIsNone(deleted_customer)

    def test_update_reservation(self):
        """
        Test the reservation updating methods
        """
        hotel = self.db_handler.create_hotel("Hotel A", "Location A")
        customer = self.db_handler.create_customer(
            "John Doe",
            "john@example.com"
        )

        reservation = self.db_handler.create_reservation(
            hotel.hotel_id,
            customer.customer_id,
            "2024-02-20",
            5
        )

        self.db_handler.update_reservation(
            reservation.reservation_id,
            hotel.hotel_id,
            customer.customer_id,
            "2024-03-10",
            7
        )

        updated_reservation = self.db_handler.get_reservation_by_id(
            reservation.reservation_id
        )

        self.assertEqual(updated_reservation.check_in_date, "2024-03-10")
        self.assertEqual(updated_reservation.nights, 7)

    def test_delete_reservation(self):
        """
        Test the reservation deleting methods
        """
        hotel = self.db_handler.create_hotel("Hotel A", "Location A")
        customer = self.db_handler.create_customer(
            "John Doe",
            "john@example.com"
        )

        reservation = self.db_handler.create_reservation(
            hotel.hotel_id,
            customer.customer_id,
            "2024-02-20",
            6
        )

        self.db_handler.delete_reservation(reservation.reservation_id)
        deleted_reservation = self.db_handler.get_reservation_by_id(
            reservation.reservation_id
        )

        self.assertIsNone(deleted_reservation)


class TestNegativeCases(unittest.TestCase):
    """
    A class containing negative tests for the DatabaseHandler class.
    """
    def setUp(self):
        self.db_name = ":memory:"
        self.db_handler = DatabaseHandler(self.db_name)

    def tearDown(self):
        self.db_handler.close_connection()

    def test_create_hotel_invalid_data(self):
        """
        Test creating hotels with invalid data
        """
        self.db_handler.create_hotel("Hotel A", "Location A")
        self.assertIsNone(
            self.db_handler.create_hotel("Hotel A", "Location A")
        )

    def test_create_customer_invalid_data(self):
        """
        Test creating customers with invalid data
        """
        self.db_handler.create_customer("John Doe", "john@example.com")
        self.assertIsNone(
            self.db_handler.create_customer("John Doe", "john@example.com")
        )

    def test_create_reservation_invalid_data(self):
        """
        Test creating reservations with invalid data
        """
        self.assertIsNone(
            self.db_handler.create_reservation(999, 1, "2024-02-20", 10)
        )

    def test_delete_non_existing_customer(self):
        """
        Test delete non-existing customer
        """
        with self.assertRaises(ValueError):
            self.db_handler.delete_customer(999)

    def test_delete_non_existing_hotel(self):
        """
        Test delete non-existing hotel
        """
        with self.assertRaises(ValueError):
            self.db_handler.delete_hotel(999)

    def test_delete_non_existing_reservatio(self):
        """
        Test delete non-existing reservation
        """
        with self.assertRaises(ValueError):
            self.db_handler.delete_reservation(999)


if __name__ == "__main__":
    unittest.main()
