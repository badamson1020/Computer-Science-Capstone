"""Tests for the AppointmentService service layer.

Covers all CRUD operations for both happy path and error path scenarios.
AppointmentService does not include an edit operation since appointments
are considered immutable once created.
"""

import unittest
from datetime import datetime, timedelta
from appointment import Appointment
from appointment_service import AppointmentService

# NoSuchElementException is a custom exception that mirrors Java's
# NoSuchElementException behavior. Python has no direct built-in equivalent,
# so a custom class was created to preserve the same exception hierarchy
# and semantics as the original Java implementation during translation.
from exceptions import NoSuchElementException


class TestAppointmentService(unittest.TestCase):
    """Test the AppointmentService CRUD operations.

    Tests cover happy path and error path scenarios for all operations.
    Equality assertions compare Appointment objects by field values rather
    than object references. The @dataclass decorator generates __eq__ based
    on field values, and get() returns copies rather than stored references,
    so assertEqual verifies the correct data was stored and retrieved rather
    than checking if two variables point to the same object in memory.

    No tearDown method is needed. Python's garbage collector automatically
    reclaims memory for in-memory objects when they go out of scope after
    each test. tearDown is only necessary for external resources like database
    connections or file handles.
    """

    @staticmethod
    def get_future_date(days: int) -> datetime:
        """Return a future datetime the specified number of days from now."""
        return datetime.now() + timedelta(days=days)

    def setUp(self) -> None:
        """Initialize a fresh AppointmentService and default Appointment before each test.

        A new service and default appointment are created before every test to
        prevent shared state issues between tests that modify appointment fields.
        If a single service instance were shared across tests, state changes
        from one test such as adding or deleting appointments could affect
        subsequent tests in unpredictable ways.
        """
        self.service = AppointmentService()
        self.default_appointment = Appointment("32", self.get_future_date(1), "Meet with new contact")

    ###########################################################
    # Test Add
    ###########################################################

    def test_add_with_new_element_successfully_adds(self):
        self.service.add(self.default_appointment)
        self.assertEqual(self.service.get(self.default_appointment.get_id()), self.default_appointment)

    def test_add_with_duplicate_element_raises_value_error(self):
        self.service.add(self.default_appointment)
        self.assertIsNotNone(self.service.get(self.default_appointment.get_id()))
        with self.assertRaises(ValueError):
            self.service.add(self.default_appointment)

    def test_add_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.add(None)

    ###########################################################
    # Test Delete
    ###########################################################

    def test_delete_with_existing_element_successfully_deletes(self):
        self.service.add(self.default_appointment)
        self.assertIsNotNone(self.service.get(self.default_appointment.get_id()))
        self.service.delete(self.default_appointment.get_id())
        self.assertIsNone(self.service.get(self.default_appointment.get_id()))

    def test_delete_with_non_existent_id_raises_no_such_element_exception(self):
        non_existent_id = "123"
        self.assertIsNone(self.service.get(non_existent_id))
        with self.assertRaises(NoSuchElementException):
            self.service.delete(non_existent_id)

    def test_delete_with_null_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.delete(None)

    ###########################################################
    # Test Get
    ###########################################################

    def test_get_with_valid_id_returns_correct_appointment(self):
        self.service.add(self.default_appointment)
        selected_appointment = self.service.get(self.default_appointment.get_id())
        self.assertIsNotNone(selected_appointment)
        self.assertEqual(self.default_appointment, selected_appointment)

    def test_get_with_invalid_id_returns_none(self):
        self.service.add(self.default_appointment)
        selected_appointment = self.service.get("234")
        self.assertIsNone(selected_appointment)

    def test_get_with_null_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.get(None)

    ###########################################################
    # Test GetAll
    ###########################################################

    def test_get_all_with_multiple_appointments_returns_all_appointments(self):
        appointment2 = Appointment("2", self.get_future_date(3), "Discuss new business plans")
        self.service.add(self.default_appointment)
        self.service.add(appointment2)
        all_appointments = self.service.get_all()
        self.assertEqual(2, len(all_appointments))
        self.assertIn(self.default_appointment, all_appointments)
        self.assertIn(appointment2, all_appointments)

    def test_get_all_with_no_appointments_returns_empty_list(self):
        all_appointments = self.service.get_all()
        self.assertEqual(0, len(all_appointments))

    def test_get_all_after_deleting_appointment_returns_remaining_appointments(self):
        appointment2 = Appointment("2", self.get_future_date(3), "Discuss new business plans")
        self.service.add(self.default_appointment)
        self.service.add(appointment2)
        self.service.delete(self.default_appointment.get_id())
        all_appointments = self.service.get_all()
        self.assertEqual(1, len(all_appointments))
        self.assertIn(appointment2, all_appointments)
        self.assertNotIn(self.default_appointment, all_appointments)


if __name__ == "__main__":
    unittest.main()