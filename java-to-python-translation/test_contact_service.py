"""Tests for the ContactService service layer.

Covers all CRUD operations for both happy path and error path scenarios.
"""

import unittest
from contact import Contact
from contact_service import ContactService

# NoSuchElementException is a custom exception that mirrors Java's
# NoSuchElementException behavior. Python has no direct built-in equivalent,
# so a custom class was created to preserve the same exception hierarchy
# and semantics as the original Java implementation during translation.
from exceptions import NoSuchElementException


class TestContactService(unittest.TestCase):
    """Test the ContactService CRUD operations.

    Tests cover happy path and error path scenarios for all operations.
    Equality assertions compare Contact objects by field values rather
    than object references. The @dataclass decorator generates __eq__ based
    on field values, and get() returns copies rather than stored references,
    so assertEqual verifies the correct data was stored and retrieved rather
    than checking if two variables point to the same object in memory.

    No tearDown method is needed. Python's garbage collector automatically
    reclaims memory for in-memory objects when they go out of scope after
    each test. tearDown is only necessary for external resources like database
    connections or file handles.
    """

    def setUp(self) -> None:
        """Initialize a fresh ContactService and default Contact before each test.

        A new service and default contact are created before every test to
        prevent shared state issues between tests that modify contact fields.
        If a single service instance were shared across tests, state changes
        from one test such as adding or deleting contacts could affect
        subsequent tests in unpredictable ways.
        """
        self.service = ContactService()
        self.default_contact = Contact("12", "Beth", "Adams", "1234567890", "Colorado")

    ###########################################################
    # Test Add
    ###########################################################

    def test_add_with_new_element_successfully_adds(self):
        self.service.add(self.default_contact)
        self.assertEqual(self.service.get(self.default_contact.get_id()), self.default_contact)

    def test_add_with_duplicate_element_raises_value_error(self):
        self.service.add(self.default_contact)
        self.assertIsNotNone(self.service.get(self.default_contact.get_id()))
        with self.assertRaises(ValueError):
            self.service.add(self.default_contact)

    def test_add_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.add(None)

    ###########################################################
    # Test Delete
    ###########################################################

    def test_delete_with_existing_element_successfully_deletes(self):
        self.service.add(self.default_contact)
        self.assertIsNotNone(self.service.get(self.default_contact.get_id()))
        self.service.delete(self.default_contact.get_id())
        self.assertIsNone(self.service.get(self.default_contact.get_id()))

    def test_delete_with_non_existent_id_raises_no_such_element_exception(self):
        non_existent_id = "123"
        self.assertIsNone(self.service.get(non_existent_id))
        with self.assertRaises(NoSuchElementException):
            self.service.delete(non_existent_id)

    def test_delete_with_null_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.delete(None)

    ###########################################################
    # Test Edit
    ###########################################################

    def test_edit_with_updated_contact_updates_fields_successfully(self):
        self.service.add(self.default_contact)
        updated_contact = Contact("12", "Josh", "Smith", "0987654321", "NewJersey123")
        self.service.edit(updated_contact)
        checked_contact = self.service.get("12")
        self.assertEqual("Josh", checked_contact.get_first_name())
        self.assertEqual("Smith", checked_contact.get_last_name())
        self.assertEqual("0987654321", checked_contact.get_number())
        self.assertEqual("NewJersey123", checked_contact.get_address())

    def test_edit_with_non_existing_contact_raises_no_such_element_exception(self):
        # A new contact is created but never added to the ContactService
        non_existing_contact = Contact("123", "Non", "Existent", "0987654321", "Nowhere123")
        with self.assertRaises(NoSuchElementException):
            self.service.edit(non_existing_contact)

    def test_edit_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.edit(None)

    ###########################################################
    # Test Get
    ###########################################################

    def test_get_with_valid_id_returns_correct_contact(self):
        self.service.add(self.default_contact)
        selected_contact = self.service.get(self.default_contact.get_id())
        self.assertIsNotNone(selected_contact)
        self.assertEqual(self.default_contact, selected_contact)

    def test_get_with_invalid_id_returns_none(self):
        self.service.add(self.default_contact)
        selected_contact = self.service.get("234")
        self.assertIsNone(selected_contact)

    def test_get_with_null_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.get(None)

    ###########################################################
    # Test GetAll
    ###########################################################

    def test_get_all_with_multiple_contacts_returns_all_contacts(self):
        contact2 = Contact("2", "Josh", "Smith", "0987654321", "California")
        self.service.add(self.default_contact)
        self.service.add(contact2)
        all_contacts = self.service.get_all()
        self.assertEqual(2, len(all_contacts))
        self.assertIn(self.default_contact, all_contacts)
        self.assertIn(contact2, all_contacts)

    def test_get_all_with_no_contacts_returns_empty_list(self):
        all_contacts = self.service.get_all()
        self.assertEqual(0, len(all_contacts))

    def test_get_all_after_deleting_contact_returns_remaining_contacts(self):
        contact2 = Contact("2", "Josh", "Smith", "0987654321", "California")
        self.service.add(self.default_contact)
        self.service.add(contact2)
        self.service.delete(self.default_contact.get_id())
        all_contacts = self.service.get_all()
        self.assertEqual(1, len(all_contacts))
        self.assertIn(contact2, all_contacts)
        self.assertNotIn(self.default_contact, all_contacts)


if __name__ == "__main__":
    unittest.main()