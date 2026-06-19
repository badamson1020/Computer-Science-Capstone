"""Service layer for managing a collection of Appointment objects.

This module represents the Service Layer of the Service-Repository
layered architecture. AppointmentService is responsible for enforcing
collection-level business rules, ensuring the appointment list remains
valid, consistent, and well-organized. Field-level data integrity rules
such as length and format validation are handled separately in the
Appointment class, keeping each layer focused on a single responsibility.
"""

from appointment import Appointment

# NoSuchElementException is a custom exception that mirrors Java's
# NoSuchElementException behavior. Python has no direct built-in equivalent,
# so a custom class was created to preserve the same exception hierarchy
# and semantics as the original Java implementation during translation.
from exceptions import NoSuchElementException


class AppointmentService:
    """Manage a collection of Appointment objects following the Service Layer pattern.

    Provides add, delete, get, and get_all operations with full input
    validation before processing. The internal appointment list is private
    to ensure all modifications go through the service layer's validation
    logic. Direct list access would bypass duplicate ID checks and allow
    external code to insert unvalidated objects.

    AppointmentService intentionally does not include an edit method.
    Appointments are considered immutable once created. If changes are
    needed the appointment must be deleted and recreated. This reflects
    the original Java design decision and ensures appointment integrity
    is maintained throughout the lifecycle of each record.

    Copies are returned from get() and get_all() rather than stored
    references to prevent external code from modifying internal state
    directly and bypassing the service layer's business rules.
    """

    def __init__(self) -> None:
        """Initialize the AppointmentService with an empty appointment list.

        The internal _appointments list is private to enforce that all
        modifications go through the service layer's validation logic.
        Direct list access would bypass duplicate ID checks and allow
        insertion of invalid objects.
        """
        self._appointments = []

    def add(self, new_appointment: Appointment) -> None:
        """Add a new appointment to the service.

        Validates that the appointment is not None and that the ID is unique
        before adding. Duplicate ID prevention is a service layer responsibility
        since it is a collection-level business rule rather than a field-level
        data rule belonging in the Appointment class.

        Args:
            new_appointment: The Appointment object to add.

        Raises:
            ValueError: If the appointment is None or a duplicate ID exists.
        """
        if new_appointment is None:
            raise ValueError("Appointment cannot be null.")

        if self._find_appointment(new_appointment.get_id()) is not None:
            raise ValueError(f"Cannot add appointment with duplicate ID: {new_appointment.get_id()}")

        self._appointments.append(new_appointment)

    def delete(self, appointment_id: str) -> None:
        """Delete an appointment by its ID.

        Args:
            appointment_id: The ID of the appointment to delete.

        Raises:
            ValueError: If the ID is None.
            NoSuchElementException: If no appointment with the given ID exists.
        """
        if appointment_id is None:
            raise ValueError("ID cannot be null.")

        appointment_to_delete = self._find_appointment(appointment_id)

        if appointment_to_delete is None:
            raise NoSuchElementException(f"Appointment with ID {appointment_id} does not exist.")

        self._appointments.remove(appointment_to_delete)

    def get(self, appointment_id: str) -> Appointment | None:
        """Retrieve a copy of the appointment with the given ID.

        Returns a copy rather than the stored reference to prevent external
        code from obtaining a direct reference to the internal object and
        modifying it in ways that bypass the service layer's validation.

        Args:
            appointment_id: The ID of the appointment to retrieve.

        Returns:
            A copy of the matching Appointment, or None if not found.

        Raises:
            ValueError: If the ID is None.
        """
        if appointment_id is None:
            raise ValueError("ID cannot be null.")

        found_appointment = self._find_appointment(appointment_id)

        if found_appointment is not None:
            return Appointment.from_appointment(found_appointment)
        else:
            return None

    def get_all(self) -> list:
        """Return a list of copies of all appointments in the service.

        Copies are returned rather than stored references to prevent external
        code from modifying internal state directly. Returns an empty list
        if no appointments exist.

        Returns:
            A list of independent Appointment copies.
        """
        return [Appointment.from_appointment(appointment) for appointment in self._appointments]

    def _find_appointment(self, appointment_id: str) -> Appointment | None:
        """Search the internal list for an appointment matching the given ID.

        Private because it exposes a direct reference to the stored object
        rather than a copy. Only used internally by add(), delete(), and get()
        where direct reference access is needed for modification or removal.
        External callers should use get() which returns a safe copy instead.

        Args:
            appointment_id: The ID to search for.

        Returns:
            The matching Appointment reference, or None if not found.
        """
        found_appointment = None

        for appointment in self._appointments:
            if appointment.get_id() == appointment_id:
                found_appointment = appointment
                break

        return found_appointment