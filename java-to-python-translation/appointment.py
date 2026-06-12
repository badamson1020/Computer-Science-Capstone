"""Data model for the Appointment entity in the Service-Repository pattern.

This module represents the Repository layer of the Service-Repository
layered architecture. The Appointment class is responsible for enforcing
field-level data integrity rules, ensuring that individual field values
are valid before they are stored. Collection-level business rules such as
duplicate ID prevention are handled separately in AppointmentService,
keeping each layer focused on a single responsibility.
"""

from dataclasses import dataclass
from datetime import datetime

# Validation constants replace magic numbers throughout the class.
# Defined at module level so limits are visible and maintainable
# in one place without searching through validation logic.
MAX_ID_LENGTH = 10
MAX_DESCRIPTION_LENGTH = 50


# @dataclass generates __eq__ automatically, allowing Appointment objects
# to be compared by field values rather than memory references.
# This is essential for meaningful equality checks in unit tests and
# service layer operations. init=False disables the auto-generated
# __init__ so inputs can be routed through setter methods for validation,
# ensuring validation runs consistently on both creation and future updates
# rather than only at construction time.
@dataclass(init=False)
class Appointment:
    """Represent an appointment with an ID, date, and description.

    Follows the Repository layer of the Service-Repository pattern,
    enforcing field-level data integrity rules. The ID is immutable
    once set. Making it private prevents external code from bypassing
    the immutability rule after construction. The date must not be in
    the past and is defensively copied on both storage and retrieval
    to prevent external modification of internal state from bypassing
    validation.

    String fields are returned directly rather than copied because strings
    are immutable in Python. Unlike the date field which returns a defensive
    copy, string values cannot be modified in place by external code, so
    returning the stored reference directly is safe.
    """

    _appointment_id: str
    _date: datetime
    _description: str

    def __init__(self, appointment_id: str, date: datetime, description: str) -> None:
        """Initialize an Appointment with the provided ID, date, and description.

        All inputs are routed through setter methods rather than assigned
        directly. This ensures validation runs consistently on creation,
        since the same setters are used for future updates. If validation
        were only in __init__, updating a field later could bypass it.

        Args:
            appointment_id: Unique identifier, 1-10 characters,
                cannot be updated after creation.
            date: Appointment datetime, must not be in the past.
            description: Appointment description, 1-50 characters.
        """
        self._set_id(appointment_id)
        self.set_date(date)
        self.set_description(description)

    @classmethod
    def from_appointment(cls, other_appointment: 'Appointment') -> 'Appointment':
        """Create an independent copy of an existing Appointment.

        Used by AppointmentService.get() to return copies rather than
        stored references. Returning copies prevents external code from
        obtaining a reference to the internally stored object and modifying
        it directly, which would bypass the service layer's validation and
        business rules. Also enables value-based equality comparisons in
        tests rather than reference-based comparisons.

        Args:
            other_appointment: The Appointment instance to copy.

        Returns:
            A new independent Appointment with the same field values.
        """
        return cls(
            other_appointment.get_id(),
            other_appointment.get_date(),
            other_appointment.get_description()
        )

    def get_id(self) -> str:
        """Return the appointment ID."""
        return self._appointment_id

    def _set_id(self, appointment_id: str) -> None:
        """Validate and store the appointment ID.

        Private because ID immutability is a core business rule. An ID
        that changes after creation would break the service layer's ability
        to reliably locate, update, and delete records. Only called once
        during construction through __init__.

        Args:
            appointment_id: The appointment ID to validate and store.

        Raises:
            ValueError: If the ID is None, empty, or exceeds 10 characters.
        """
        if appointment_id is None:
            raise ValueError("ID cannot be null.")
        elif len(appointment_id) > MAX_ID_LENGTH:
            raise ValueError(f"ID cannot exceed {MAX_ID_LENGTH} characters in length.")
        elif len(appointment_id) == 0:
            raise ValueError("ID must be at least 1 character in length.")

        self._appointment_id = appointment_id

    def get_date(self) -> datetime:
        """Return a defensive copy of the stored appointment date.

        Unlike string fields which are immutable in Python and safe to return
        directly, datetime objects are mutable and could be modified in place
        by external code. A copy is returned to prevent external modification
        from bypassing the validation in set_date() and introducing a past
        date without raising an error.

        Returns:
            An independent copy of the stored appointment datetime.
        """
        return self._date.replace()

    def set_date(self, date: datetime) -> None:
        """Validate and store a defensive copy of the appointment date.

        A copy is stored rather than the reference passed in to prevent
        the caller from modifying the internal date after construction
        by mutating the original object, which would bypass validation.

        Args:
            date: The appointment datetime to validate and store.

        Raises:
            ValueError: If the date is None or is in the past.
        """
        now = datetime.now()

        if date is None:
            raise ValueError("Date cannot be null.")
        elif date < now:
            raise ValueError("Date and time cannot be in the past.")

        self._date = date.replace()

    def get_description(self) -> str:
        """Return the appointment description."""
        return self._description

    def set_description(self, description: str) -> None:
        """Validate and store the appointment description.

        Args:
            description: The appointment description to validate and store.

        Raises:
            ValueError: If the description is None, empty, or exceeds 50 characters.
        """
        if description is None:
            raise ValueError("Description cannot be null.")
        elif len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description cannot exceed {MAX_DESCRIPTION_LENGTH} characters in length.")
        elif len(description) == 0:
            raise ValueError("Description must be at least 1 character in length.")

        self._description = description