"""Data model for the Contact entity in the Service-Repository pattern.

This module represents the Repository layer of the Service-Repository
layered architecture. The Contact class is responsible for enforcing
field-level data integrity rules, ensuring that individual field values
are valid before they are stored. Collection-level business rules such as
duplicate ID prevention are handled separately in ContactService,
keeping each layer focused on a single responsibility.
"""

from dataclasses import dataclass

# Validation constants replace magic numbers throughout the class.
# Defined at module level so limits are visible and maintainable
# in one place without searching through validation logic.
MAX_ID_LENGTH = 10
MAX_FIRST_NAME_LENGTH = 10
MAX_LAST_NAME_LENGTH = 10
REQUIRED_NUMBER_LENGTH = 10
MAX_ADDRESS_LENGTH = 30


# @dataclass generates __eq__ automatically, allowing Contact objects
# to be compared by field values rather than memory references.
# This is essential for meaningful equality checks in unit tests and
# service layer operations. init=False disables the auto-generated
# __init__ so inputs can be routed through setter methods for validation,
# ensuring validation runs consistently on both creation and future updates
# rather than only at construction time.
@dataclass(init=False)
class Contact:
    """Represent a contact with an ID, first name, last name, phone number, and address.

    Follows the Repository layer of the Service-Repository pattern,
    enforcing field-level data integrity rules. The ID is immutable
    once set, making _set_id() private to prevent external code from
    bypassing the immutability rule after construction. All other fields
    are mutable and expose public setters because the service layer's
    edit() method requires updating those fields after creation.

    String fields are returned directly rather than copied because strings
    are immutable in Python. Unlike mutable objects, string values cannot
    be modified in place by external code, so returning the stored
    reference directly is safe.
    """

    _contact_id: str
    _first_name: str
    _last_name: str
    _number: str
    _address: str

    def __init__(self, contact_id: str, first_name: str, last_name: str,
                 number: str, address: str) -> None:
        """Initialize a Contact with the provided fields.

        All inputs are routed through setter methods rather than assigned
        directly. This ensures validation runs consistently on creation,
        since the same setters are used for future updates. If validation
        were only in __init__, updating a field later could bypass it.

        Args:
            contact_id: Unique identifier, 1-10 characters,
                cannot be updated after creation.
            first_name: Contact first name, 1-10 characters.
            last_name: Contact last name, 1-10 characters.
            number: Contact phone number, must be exactly 10 characters.
            address: Contact address, 1-30 characters.
        """
        self._set_id(contact_id)
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_number(number)
        self.set_address(address)

    @classmethod
    def from_contact(cls, other_contact: 'Contact') -> 'Contact':
        """Create an independent copy of an existing Contact.

        Used by ContactService.get() to return copies rather than stored
        references. Returning copies prevents external code from obtaining
        a reference to the internally stored object and modifying it
        directly, which would bypass the service layer's validation and
        business rules. Also enables value-based equality comparisons in
        tests rather than reference-based comparisons.

        Args:
            other_contact: The Contact instance to copy.

        Returns:
            A new independent Contact with the same field values.
        """
        return cls(
            other_contact.get_id(),
            other_contact.get_first_name(),
            other_contact.get_last_name(),
            other_contact.get_number(),
            other_contact.get_address()
        )

    def get_id(self) -> str:
        """Return the contact ID."""
        return self._contact_id

    def _set_id(self, contact_id: str) -> None:
        """Validate and store the contact ID.

        Private because ID immutability is a core business rule. An ID
        that changes after creation would break the service layer's ability
        to reliably locate, update, and delete records. Only called once
        during construction through __init__.

        Args:
            contact_id: The contact ID to validate and store.

        Raises:
            ValueError: If the ID is None, empty, or exceeds 10 characters.
        """
        if contact_id is None:
            raise ValueError("ID cannot be null.")
        elif len(contact_id) > MAX_ID_LENGTH:
            raise ValueError(f"ID cannot exceed {MAX_ID_LENGTH} characters in length.")
        elif len(contact_id) == 0:
            raise ValueError("ID must be at least 1 character in length.")

        self._contact_id = contact_id

    def get_first_name(self) -> str:
        """Return the contact first name."""
        return self._first_name

    def set_first_name(self, first_name: str) -> None:
        """Validate and store the contact first name.

        Public because first name is a legitimately editable field. The
        service layer's edit() method relies on this setter to update
        contact fields after creation while still enforcing validation rules.

        Args:
            first_name: The first name to validate and store.

        Raises:
            ValueError: If the first name is None, empty, or exceeds 10 characters.
        """
        if first_name is None:
            raise ValueError("First name cannot be null.")
        elif len(first_name) > MAX_FIRST_NAME_LENGTH:
            raise ValueError(f"First name cannot exceed {MAX_FIRST_NAME_LENGTH} characters in length.")
        elif len(first_name) == 0:
            raise ValueError("First name must be at least 1 character in length.")

        self._first_name = first_name

    def get_last_name(self) -> str:
        """Return the contact last name."""
        return self._last_name

    def set_last_name(self, last_name: str) -> None:
        """Validate and store the contact last name.

        Public because last name is a legitimately editable field. The
        service layer's edit() method relies on this setter to update
        contact fields after creation while still enforcing validation rules.

        Args:
            last_name: The last name to validate and store.

        Raises:
            ValueError: If the last name is None, empty, or exceeds 10 characters.
        """
        if last_name is None:
            raise ValueError("Last name cannot be null.")
        elif len(last_name) > MAX_LAST_NAME_LENGTH:
            raise ValueError(f"Last name cannot exceed {MAX_LAST_NAME_LENGTH} characters in length.")
        elif len(last_name) == 0:
            raise ValueError("Last name must be at least 1 character in length.")

        self._last_name = last_name

    def get_number(self) -> str:
        """Return the contact phone number."""
        return self._number

    def set_number(self, number: str) -> None:
        """Validate and store the contact phone number.

        Phone number validation uses an exact length check rather than a
        maximum length check because a valid phone number must be exactly
        10 digits. A number shorter than 10 is just as invalid as one
        longer than 10, so a single equality check covers both cases.

        Public because phone number is a legitimately editable field.

        Args:
            number: The phone number to validate and store.

        Raises:
            ValueError: If the number is None or not exactly 10 characters.
        """
        if number is None:
            raise ValueError("Number cannot be null.")
        elif len(number) != REQUIRED_NUMBER_LENGTH:
            raise ValueError(f"Number must be exactly {REQUIRED_NUMBER_LENGTH} characters in length.")

        self._number = number

    def get_address(self) -> str:
        """Return the contact address."""
        return self._address

    def set_address(self, address: str) -> None:
        """Validate and store the contact address.

        Public because address is a legitimately editable field. The
        service layer's edit() method relies on this setter to update
        contact fields after creation while still enforcing validation rules.

        Args:
            address: The address to validate and store.

        Raises:
            ValueError: If the address is None, empty, or exceeds 30 characters.
        """
        if address is None:
            raise ValueError("Address cannot be null.")
        elif len(address) > MAX_ADDRESS_LENGTH:
            raise ValueError(f"Address cannot exceed {MAX_ADDRESS_LENGTH} characters in length.")
        elif len(address) == 0:
            raise ValueError("Address must be at least 1 character in length.")

        self._address = address