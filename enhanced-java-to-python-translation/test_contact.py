"""Tests for the Contact data model.

Covers all validation rules for each field through both the constructor
and public setter methods where applicable.
"""

import unittest
from contact import Contact


class TestContact(unittest.TestCase):
    """Test the Contact data model validation rules.

    Each field is tested through both the constructor and its public setter
    method where one exists. Testing both paths verifies that validation
    logic lives in the setter methods rather than only in __init__, ensuring
    the same rules apply whether a field is set at construction or updated later.

    The ID field is only tested through the constructor because _set_id() is
    private and intentionally has no public setter. ID immutability is a core
    business rule enforced by making the setter private and only calling it once.

    Contact tests do not use a setUp method because the five required fields
    need different combinations of valid and invalid values across tests.
    A single default contact object would not serve as a clean baseline for
    all test cases, so objects are created inline with the exact values
    each test requires.

    Equality assertions compare field values through getter methods rather than
    comparing object references directly. The @dataclass decorator generates
    __eq__ based on field values, enabling meaningful equality checks between
    Contact instances rather than checking if two variables point to the
    same object.

    VALID constants represent the minimum allowed length for their field,
    testing the lower boundary of valid input. Length input constants such
    as TEN_LENGTH_INPUT and THIRTY_LENGTH_INPUT test the upper boundary by
    representing the maximum allowed length, and are also used with an
    appended character to test values just beyond the maximum.

    No tearDown method is needed. Python's garbage collector automatically
    reclaims memory for in-memory objects when they go out of scope after
    each test. tearDown is only necessary for external resources like database
    connections or file handles.
    """

    # Test constants
    VALID_ID = "1"
    VALID_FIRST_NAME = "A"
    VALID_LAST_NAME = "B"
    VALID_NUMBER = "1234567890"
    VALID_ADDRESS = "C"
    TEN_LENGTH_INPUT = "123456789A"
    THIRTY_LENGTH_INPUT = "123456789012345678901234567890"
    SHORT_INPUT = "2A"

    ###########################################################
    # Test contact_id
    # ID is only tested through the constructor because _set_id()
    # is private and has no public setter by design. ID immutability
    # is enforced by restricting modification to construction time only.
    ###########################################################

    def test_id_with_min_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        self.assertEqual(self.VALID_ID, test_contact.get_id())

    def test_id_with_max_length_is_valid(self):
        test_contact = Contact(self.TEN_LENGTH_INPUT, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        self.assertEqual(self.TEN_LENGTH_INPUT, test_contact.get_id())

    def test_id_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(None, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)

    def test_id_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.TEN_LENGTH_INPUT + "A", self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)

    def test_id_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact("", self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)

    ###########################################################
    # Test first_name
    # Each test type is run once through the constructor and once
    # through the public setter to verify validation runs consistently
    # on both creation and future updates.
    ###########################################################

    def test_first_name_with_min_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        self.assertEqual(self.VALID_FIRST_NAME, test_contact.get_first_name())

    def test_set_first_name_with_min_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.TEN_LENGTH_INPUT, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        test_contact.set_first_name(self.VALID_FIRST_NAME)
        self.assertEqual(self.VALID_FIRST_NAME, test_contact.get_first_name())

    def test_first_name_with_max_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.TEN_LENGTH_INPUT, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        self.assertEqual(self.TEN_LENGTH_INPUT, test_contact.get_first_name())

    def test_set_first_name_with_max_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        test_contact.set_first_name(self.TEN_LENGTH_INPUT)
        self.assertEqual(self.TEN_LENGTH_INPUT, test_contact.get_first_name())

    def test_first_name_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, None, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)

    def test_set_first_name_with_null_value_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_first_name(None)

    def test_first_name_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.TEN_LENGTH_INPUT + "A", self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)

    def test_set_first_name_with_more_than_max_length_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_first_name(self.TEN_LENGTH_INPUT + "A")

    def test_first_name_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, "", self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)

    def test_set_first_name_with_empty_value_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_first_name("")

    ###########################################################
    # Test last_name
    # Each test type is run once through the constructor and once
    # through the public setter to verify validation runs consistently
    # on both creation and future updates.
    ###########################################################

    def test_last_name_with_min_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        self.assertEqual(self.VALID_LAST_NAME, test_contact.get_last_name())

    def test_set_last_name_with_min_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.TEN_LENGTH_INPUT, self.VALID_NUMBER, self.VALID_ADDRESS)
        test_contact.set_last_name(self.VALID_LAST_NAME)
        self.assertEqual(self.VALID_LAST_NAME, test_contact.get_last_name())

    def test_last_name_with_max_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.TEN_LENGTH_INPUT, self.VALID_NUMBER, self.VALID_ADDRESS)
        self.assertEqual(self.TEN_LENGTH_INPUT, test_contact.get_last_name())

    def test_set_last_name_with_max_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        test_contact.set_last_name(self.TEN_LENGTH_INPUT)
        self.assertEqual(self.TEN_LENGTH_INPUT, test_contact.get_last_name())

    def test_last_name_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, None, self.VALID_NUMBER, self.VALID_ADDRESS)

    def test_set_last_name_with_null_value_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_last_name(None)

    def test_last_name_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.TEN_LENGTH_INPUT + "A", self.VALID_NUMBER, self.VALID_ADDRESS)

    def test_set_last_name_with_more_than_max_length_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_last_name(self.TEN_LENGTH_INPUT + "A")

    def test_last_name_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, "", self.VALID_NUMBER, self.VALID_ADDRESS)

    def test_set_last_name_with_empty_value_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_last_name("")

    ###########################################################
    # Test number
    # Each test type is run once through the constructor and once
    # through the public setter to verify validation runs consistently
    # on both creation and future updates.
    ###########################################################

    def test_number_with_ten_characters_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        self.assertEqual(self.VALID_NUMBER, test_contact.get_number())

    def test_set_number_with_ten_characters_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.TEN_LENGTH_INPUT, self.VALID_ADDRESS)
        test_contact.set_number(self.VALID_NUMBER)
        self.assertEqual(self.VALID_NUMBER, test_contact.get_number())

    def test_number_with_less_than_ten_characters_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.SHORT_INPUT, self.VALID_ADDRESS)

    def test_set_number_with_less_than_ten_characters_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_number(self.SHORT_INPUT)

    def test_number_with_more_than_ten_characters_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.THIRTY_LENGTH_INPUT, self.VALID_ADDRESS)

    def test_set_number_with_more_than_ten_characters_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_number(self.THIRTY_LENGTH_INPUT)

    def test_number_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, None, self.VALID_ADDRESS)

    def test_set_number_with_null_value_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_number(None)

    ###########################################################
    # Test address
    # Each test type is run once through the constructor and once
    # through the public setter to verify validation runs consistently
    # on both creation and future updates.
    ###########################################################

    def test_address_with_min_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        self.assertEqual(self.VALID_ADDRESS, test_contact.get_address())

    def test_set_address_with_min_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.TEN_LENGTH_INPUT)
        test_contact.set_address(self.VALID_ADDRESS)
        self.assertEqual(self.VALID_ADDRESS, test_contact.get_address())

    def test_address_with_max_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.THIRTY_LENGTH_INPUT)
        self.assertEqual(self.THIRTY_LENGTH_INPUT, test_contact.get_address())

    def test_set_address_with_max_length_is_valid(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        test_contact.set_address(self.THIRTY_LENGTH_INPUT)
        self.assertEqual(self.THIRTY_LENGTH_INPUT, test_contact.get_address())

    def test_address_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, None)

    def test_set_address_with_null_value_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_address(None)

    def test_address_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.THIRTY_LENGTH_INPUT + "A")

    def test_set_address_with_more_than_max_length_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_address(self.THIRTY_LENGTH_INPUT + "A")

    def test_address_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, "")

    def test_set_address_with_empty_value_raises_value_error(self):
        test_contact = Contact(self.VALID_ID, self.VALID_FIRST_NAME, self.VALID_LAST_NAME, self.VALID_NUMBER, self.VALID_ADDRESS)
        with self.assertRaises(ValueError):
            test_contact.set_address("")


if __name__ == "__main__":
    unittest.main()