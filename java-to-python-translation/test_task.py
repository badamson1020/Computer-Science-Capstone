"""Tests for the Task data model.

Covers all validation rules for each field through both the constructor
and public setter methods where applicable.
"""

import unittest
from task import Task


class TestTask(unittest.TestCase):
    """Test the Task data model validation rules.

    Each field is tested through both the constructor and its public setter
    method where one exists. Testing both paths verifies that validation
    logic lives in the setter methods rather than only in __init__, ensuring
    the same rules apply whether a field is set at construction or updated later.

    The ID field is only tested through the constructor because _set_id() is
    private and intentionally has no public setter. ID immutability is a core
    business rule enforced by making the setter private and only calling it once.

    Equality assertions compare field values through getter methods rather than
    comparing object references directly. The @dataclass decorator generates
    __eq__ based on field values, enabling meaningful equality checks between
    Task instances rather than checking if two variables point to the same object.

    VALID constants represent the minimum allowed length for their field,
    testing the lower boundary of valid input. Length input constants such
    as TEN_LENGTH_INPUT and TWENTY_LENGTH_INPUT test the upper boundary by
    representing the maximum allowed length, and are also used with an
    appended character to test values just beyond the maximum.

    No tearDown method is needed. Python's garbage collector automatically
    reclaims memory for in-memory objects when they go out of scope after
    each test. tearDown is only necessary for external resources like database
    connections or file handles.
    """

    # Test constants
    VALID_ID = "1"
    VALID_NAME = "A"
    VALID_DESCRIPTION = "B"
    TEN_LENGTH_INPUT = "123456789A"
    TWENTY_LENGTH_INPUT = "12345678901234567890"
    FIFTY_LENGTH_INPUT = "12345678901234567890123456789012345678901234567890"

    ###########################################################
    # Test task_id
    # ID is only tested through the constructor because _set_id()
    # is private and has no public setter by design. ID immutability
    # is enforced by restricting modification to construction time only.
    ###########################################################

    def test_id_with_min_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        self.assertEqual(self.VALID_ID, test_task.get_id())

    def test_id_with_max_length_is_valid(self):
        test_task = Task(self.TEN_LENGTH_INPUT, self.VALID_NAME, self.VALID_DESCRIPTION)
        self.assertEqual(self.TEN_LENGTH_INPUT, test_task.get_id())

    def test_id_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(None, self.VALID_NAME, self.VALID_DESCRIPTION)

    def test_id_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(self.TEN_LENGTH_INPUT + "A", self.VALID_NAME, self.VALID_DESCRIPTION)

    def test_id_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task("", self.VALID_NAME, self.VALID_DESCRIPTION)

    ###########################################################
    # Test name
    # Each test type is run once through the constructor and once
    # through the public setter to verify validation runs consistently
    # on both creation and future updates.
    ###########################################################

    def test_name_with_min_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        self.assertEqual(self.VALID_NAME, test_task.get_name())

    def test_set_name_with_min_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.TEN_LENGTH_INPUT, self.VALID_DESCRIPTION)
        test_task.set_name(self.VALID_NAME)
        self.assertEqual(self.VALID_NAME, test_task.get_name())

    def test_name_with_max_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.TWENTY_LENGTH_INPUT, self.VALID_DESCRIPTION)
        self.assertEqual(self.TWENTY_LENGTH_INPUT, test_task.get_name())

    def test_set_name_with_max_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        test_task.set_name(self.TWENTY_LENGTH_INPUT)
        self.assertEqual(self.TWENTY_LENGTH_INPUT, test_task.get_name())

    def test_name_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(self.VALID_ID, None, self.VALID_DESCRIPTION)

    def test_set_name_with_null_value_raises_value_error(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_task.set_name(None)

    def test_name_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(self.VALID_ID, self.TWENTY_LENGTH_INPUT + "A", self.VALID_DESCRIPTION)

    def test_set_name_with_more_than_max_length_raises_value_error(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_task.set_name(self.TWENTY_LENGTH_INPUT + "A")

    def test_name_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(self.VALID_ID, "", self.VALID_DESCRIPTION)

    def test_set_name_with_empty_value_raises_value_error(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_task.set_name("")

    ###########################################################
    # Test description
    # Each test type is run once through the constructor and once
    # through the public setter to verify validation runs consistently
    # on both creation and future updates.
    ###########################################################

    def test_description_with_min_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        self.assertEqual(self.VALID_DESCRIPTION, test_task.get_description())

    def test_set_description_with_min_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.TEN_LENGTH_INPUT)
        test_task.set_description(self.VALID_DESCRIPTION)
        self.assertEqual(self.VALID_DESCRIPTION, test_task.get_description())

    def test_description_with_max_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.FIFTY_LENGTH_INPUT)
        self.assertEqual(self.FIFTY_LENGTH_INPUT, test_task.get_description())

    def test_set_description_with_max_length_is_valid(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        test_task.set_description(self.FIFTY_LENGTH_INPUT)
        self.assertEqual(self.FIFTY_LENGTH_INPUT, test_task.get_description())

    def test_description_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(self.VALID_ID, self.VALID_NAME, None)

    def test_set_description_with_null_value_raises_value_error(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_task.set_description(None)

    def test_description_with_more_than_max_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(self.VALID_ID, self.VALID_NAME, self.FIFTY_LENGTH_INPUT + "A")

    def test_set_description_with_more_than_max_length_raises_value_error(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_task.set_description(self.FIFTY_LENGTH_INPUT + "A")

    def test_description_with_empty_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(self.VALID_ID, self.VALID_NAME, "")

    def test_set_description_with_empty_value_raises_value_error(self):
        test_task = Task(self.VALID_ID, self.VALID_NAME, self.VALID_DESCRIPTION)
        with self.assertRaises(ValueError):
            test_task.set_description("")


if __name__ == "__main__":
    unittest.main()