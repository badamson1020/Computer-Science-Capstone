"""Tests for the Appointment data model.

Covers all validation rules for each field through both the constructor
and public setter methods where applicable.
"""

import unittest
from datetime import datetime, timedelta
from appointment import Appointment


class TestAppointment(unittest.TestCase):
    """Test the Appointment data model validation rules.

    Each field is tested through both the constructor and its public setter
    method where one exists. Testing both paths verifies that validation
    logic lives in the setter methods rather than only in __init__, ensuring
    the same validation rules apply regardless of how the field is set.
    Although AppointmentService does not expose an edit operation, testing
    the public setters directly confirms the validation is correctly
    implemented in the setters themselves rather than duplicated in __init__.

    The ID field is only tested through the constructor because _set_id() is
    private and intentionally has no public setter. ID immutability is a core
    business rule enforced by making the setter private and only calling it once.

    Date tests use future dates to satisfy the not-in-the-past validation rule.
    Past dates are expected to raise ValueError since appointments cannot be
    scheduled for times that have already passed.

    Equality assertions compare field values through getter methods rather than
    comparing object references directly. The @dataclass decorator generates
    __eq__ based on field values, enabling meaningful equality checks between
    Appointment instances rather than checking if two variables point to the
    same object.

    VALID constants represent the minimum allowed length for their field,
    testing the lower boundary of valid input. Length input constants such
    as TEN_LENGTH_INPUT test the upper boundary by representing the maximum
    allowed length, and are also used with an appended character to test
    values just beyond the maximum.

    No tearDown method is needed. Python's garbage collector automatically
    reclaims memory for in-memory objects when they go out of scope after
    each test. tearDown is only necessary for external resources like database
    connections or file handles.
    """

    # Test constants
    VALID_ID = "1"
    VALID_DESCRIPTION = "B"
    TEN_LENGTH_INPUT = "123456789A"
    FIFTY_LENGTH_INPUT = "12345678901234567890123456789012345678901234567890"

    @staticmethod
    def get_future_date(days: int) -> datetime:
        """Return a future datetime the specified number of days from now."""
        return datetime.now() + timedelta(days=days)

    @staticmethod
    def get_past_date() -> datetime:
        """Return a fixed datetime in the past for testing."""
        return datetime(2021, 12, 22, 10, 0, 0)

    @staticmethod
    def get_today() -> datetime:
        """Return a datetime one second from now.

        A one-second buffer is used to avoid timing issues where
        datetime.now() inside set_date could be fractionally later
        than the datetime created in the test, causing a valid future
        date to incorrectly fail the not-in-the-past validation check.
        """
        return datetime.now() + timedelta(seconds=1)

    ###########################################################
    # Test appointment_id
    # ID is only tested through the constructor because _set_id()
    # is private and has no public setter by design. ID immutability
    # is enforced by restricting modification to construction time only.
    ###########################################################

    def test_id_with_min_length_is_valid(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        self.assertEqual(self.VALID_ID, test_appointment.get_id())

    def test_id_with_max_length_is_valid(self):
        test_appointment = Appointment(self.TEN_LENGTH_INPUT, self.get_future_date(1), self.VALID_DESCRIPTION)
        self.assertEqual(self.TEN_LENGTH_INPUT, test_appointment.get_id())

    def test_id_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Appointment(None, self.get_future_date(1), self.VALID_DESCRIPTION)

    def test_id_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Appointment(self.TEN_LENGTH_INPUT + "A", self.get_future_date(1), self.VALID_DESCRIPTION)

    def test_id_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Appointment("", self.get_future_date(1), self.VALID_DESCRIPTION)

    ###########################################################
    # Test date
    # Each test type is run once through the constructor and once
    # through the public setter to verify that validation logic
    # lives in set_date() rather than only in __init__.
    ###########################################################

    def test_date_with_future_date_is_valid(self):
        future_date = self.get_future_date(1)
        test_appointment = Appointment(self.VALID_ID, future_date, self.VALID_DESCRIPTION)
        self.assertEqual(future_date, test_appointment.get_date())

    def test_set_date_with_future_date_is_valid(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        future_date = self.get_future_date(2)
        test_appointment.set_date(future_date)
        self.assertEqual(future_date, test_appointment.get_date())

    def test_date_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Appointment(self.VALID_ID, None, self.VALID_DESCRIPTION)

    def test_set_date_with_null_value_raises_value_error(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_appointment.set_date(None)

    def test_date_with_past_date_raises_value_error(self):
        with self.assertRaises(ValueError):
            Appointment(self.VALID_ID, self.get_past_date(), self.VALID_DESCRIPTION)

    def test_set_date_with_past_date_raises_value_error(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_appointment.set_date(self.get_past_date())

    def test_date_with_today_is_valid(self):
        today = self.get_today()
        test_appointment = Appointment(self.VALID_ID, today, self.VALID_DESCRIPTION)
        self.assertEqual(today, test_appointment.get_date())

    def test_set_date_with_today_is_valid(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        today = self.get_today()
        test_appointment.set_date(today)
        self.assertEqual(today, test_appointment.get_date())

    ###########################################################
    # Test description
    # Each test type is run once through the constructor and once
    # through the public setter to verify that validation logic
    # lives in set_description() rather than only in __init__.
    ###########################################################

    def test_description_with_min_length_is_valid(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        self.assertEqual(self.VALID_DESCRIPTION, test_appointment.get_description())

    def test_set_description_with_min_length_is_valid(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.TEN_LENGTH_INPUT)
        test_appointment.set_description(self.VALID_DESCRIPTION)
        self.assertEqual(self.VALID_DESCRIPTION, test_appointment.get_description())

    def test_description_with_max_length_is_valid(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.FIFTY_LENGTH_INPUT)
        self.assertEqual(self.FIFTY_LENGTH_INPUT, test_appointment.get_description())

    def test_set_description_with_max_length_is_valid(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        test_appointment.set_description(self.FIFTY_LENGTH_INPUT)
        self.assertEqual(self.FIFTY_LENGTH_INPUT, test_appointment.get_description())

    def test_description_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Appointment(self.VALID_ID, self.get_future_date(1), None)

    def test_set_description_with_null_value_raises_value_error(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_appointment.set_description(None)

    def test_description_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Appointment(self.VALID_ID, self.get_future_date(1), self.FIFTY_LENGTH_INPUT + "A")

    def test_set_description_with_more_than_max_length_raises_value_error(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_appointment.set_description(self.FIFTY_LENGTH_INPUT + "A")

    def test_description_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Appointment(self.VALID_ID, self.get_future_date(1), "")

    def test_set_description_with_empty_value_raises_value_error(self):
        test_appointment = Appointment(self.VALID_ID, self.get_future_date(1), self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_appointment.set_description("")


if __name__ == "__main__":
    unittest.main()