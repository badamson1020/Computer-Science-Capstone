"""Service layer for managing a collection of Contact objects.

This module represents the Service Layer of the Service-Repository
layered architecture. ContactService is responsible for enforcing
collection-level business rules, ensuring the contact list remains
valid, consistent, and well-organized. Field-level data integrity rules
such as length and format validation are handled separately in the
Contact class, keeping each layer focused on a single responsibility.
"""

from contact import Contact

# NoSuchElementException is a custom exception that mirrors Java's
# NoSuchElementException behavior. Python has no direct built-in equivalent,
# so a custom class was created to preserve the same exception hierarchy
# and semantics as the original Java implementation during translation.
from exceptions import NoSuchElementException


class ContactService:
    """Manage a collection of Contact objects following the Service Layer pattern.

    Provides add, delete, edit, get, and get_all operations with full input
    validation before processing. The internal _contacts list is private to
    enforce that all modifications go through the service layer's validation
    logic. Direct list access would bypass duplicate ID checks and allow
    external code to insert unvalidated objects.

    Copies are returned from get() and get_all() rather than stored
    references to prevent external code from modifying internal state
    directly and bypassing the service layer's business rules.
    """

    def __init__(self) -> None:
        """Initialize the ContactService with an empty contact list."""
        self._contacts = []

    def add(self, new_contact: Contact) -> None:
        """Add a new contact to the service.

        Validates that the contact is not None and that the ID is unique
        before adding. Duplicate ID prevention is a service layer
        responsibility since it is a collection-level business rule
        rather than a field-level data rule belonging in the Contact class.

        Args:
            new_contact: The Contact object to add.

        Raises:
            ValueError: If the contact is None or a duplicate ID exists.
        """
        if new_contact is None:
            raise ValueError("Contact cannot be null.")

        if self._find_contact(new_contact.get_id()) is not None:
            raise ValueError(f"Cannot add contact with duplicate ID: {new_contact.get_id()}")

        self._contacts.append(new_contact)

    def delete(self, contact_id: str) -> None:
        """Delete a contact by its ID.

        Args:
            contact_id: The ID of the contact to delete.

        Raises:
            ValueError: If the ID is None.
            NoSuchElementException: If no contact with the given ID exists.
        """
        if contact_id is None:
            raise ValueError("ID cannot be null.")

        contact_to_delete = self._find_contact(contact_id)

        if contact_to_delete is None:
            raise NoSuchElementException(f"Contact with ID {contact_id} does not exist.")

        self._contacts.remove(contact_to_delete)

    def edit(self, updated_contact: Contact) -> None:
        """Update an existing contact's fields.

        The contact ID cannot be updated since it is immutable by design in
        the Contact class. All other fields are editable. The update is
        applied directly to the stored object using the Contact class's
        public setters, which enforce validation rules on the new values
        before storing them.

        Args:
            updated_contact: A Contact object containing the updated fields.

        Raises:
            ValueError: If the updated contact or its ID is None.
            NoSuchElementException: If no contact with the given ID exists.
        """
        if updated_contact is None or updated_contact.get_id() is None:
            raise ValueError("The contact and/or its ID cannot be null.")

        existing_contact = self._find_contact(updated_contact.get_id())

        if existing_contact is None:
            raise NoSuchElementException(f"Contact with ID {updated_contact.get_id()} does not exist.")

        existing_contact.set_first_name(updated_contact.get_first_name())
        existing_contact.set_last_name(updated_contact.get_last_name())
        existing_contact.set_number(updated_contact.get_number())
        existing_contact.set_address(updated_contact.get_address())

    def get(self, contact_id: str) -> Contact | None:
        """Retrieve a copy of the contact with the given ID.

        Returns a copy rather than the stored reference to prevent external
        code from obtaining a direct reference to the internal object and
        modifying it in ways that bypass the service layer's validation.

        Args:
            contact_id: The ID of the contact to retrieve.

        Returns:
            A copy of the matching Contact, or None if not found.

        Raises:
            ValueError: If the ID is None.
        """
        if contact_id is None:
            raise ValueError("ID cannot be null.")

        found_contact = self._find_contact(contact_id)

        if found_contact is not None:
            return Contact.from_contact(found_contact)
        else:
            return None

    def get_all(self) -> list:
        """Return a list of copies of all contacts in the service.

        Copies are returned rather than stored references to prevent external
        code from modifying internal state directly. Returns an empty list
        if no contacts exist.

        Returns:
            A list of independent Contact copies.
        """
        return [Contact.from_contact(contact) for contact in self._contacts]

    def _find_contact(self, contact_id: str) -> Contact | None:
        """Search the internal list for a contact matching the given ID.

        Private because it exposes a direct reference to the stored object
        rather than a copy. Only used internally by add(), delete(), get(),
        and edit() where direct reference access is needed for modification
        or removal. External callers should use get() which returns a safe
        copy instead.

        Args:
            contact_id: The ID to search for.

        Returns:
            The matching Contact reference, or None if not found.
        """
        found_contact = None

        for contact in self._contacts:
            if contact.get_id() == contact_id:
                found_contact = contact
                break

        return found_contact