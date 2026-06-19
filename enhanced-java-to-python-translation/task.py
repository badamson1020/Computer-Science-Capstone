"""Data model for the Task entity in the Service-Repository pattern.

This module represents the Repository layer of the Service-Repository
layered architecture. The Task class is responsible for enforcing
field-level data integrity rules, ensuring that individual field values
are valid before they are stored. Collection-level business rules such as
duplicate ID prevention are handled separately in TaskService,
keeping each layer focused on a single responsibility.
"""

from dataclasses import dataclass

# Validation constants replace magic numbers throughout the class.
# Defined at module level so limits are visible and maintainable
# in one place without searching through validation logic.
MAX_ID_LENGTH = 10
MAX_NAME_LENGTH = 20
MAX_DESCRIPTION_LENGTH = 50


# @dataclass generates __eq__ automatically, allowing Task objects
# to be compared by field values rather than memory references.
# This is essential for meaningful equality checks in unit tests and
# service layer operations. init=False disables the auto-generated
# __init__ so inputs can be routed through setter methods for validation,
# ensuring validation runs consistently on both creation and future updates
# rather than only at construction time.
@dataclass(init=False)
class Task:
    """Represent a task with an ID, name, and description.

    Follows the Repository layer of the Service-Repository pattern,
    enforcing field-level data integrity rules. The ID is immutable
    once set, making _set_id() private to prevent external code from
    bypassing the immutability rule after construction. Name and
    description are mutable and expose public setters because the
    service layer's edit() method requires updating those fields
    after creation.

    String fields are returned directly rather than copied because strings
    are immutable in Python. Unlike mutable objects, string values cannot
    be modified in place by external code, so returning the stored
    reference directly is safe.
    """

    _task_id: str
    _name: str
    _description: str

    def __init__(self, task_id: str, name: str, description: str) -> None:
        """Initialize a Task with the provided ID, name, and description.

        All inputs are routed through setter methods rather than assigned
        directly. This ensures validation runs consistently on creation,
        since the same setters are used for future updates. If validation
        were only in __init__, updating a field later could bypass it.

        Args:
            task_id: Unique identifier, 1-10 characters,
                cannot be updated after creation.
            name: Task name, 1-20 characters.
            description: Task description, 1-50 characters.
        """
        self._set_id(task_id)
        self.set_name(name)
        self.set_description(description)

    @classmethod
    def from_task(cls, other_task: 'Task') -> 'Task':
        """Create an independent copy of an existing Task.

        Used by TaskService.get() to return copies rather than stored
        references. Returning copies prevents external code from obtaining
        a reference to the internally stored object and modifying it
        directly, which would bypass the service layer's validation and
        business rules. Also enables value-based equality comparisons in
        tests rather than reference-based comparisons.

        Args:
            other_task: The Task instance to copy.

        Returns:
            A new independent Task with the same field values.
        """
        return cls(other_task.get_id(), other_task.get_name(), other_task.get_description())

    def get_id(self) -> str:
        """Return the task ID."""
        return self._task_id

    def _set_id(self, task_id: str) -> None:
        """Validate and store the task ID.

        Private because ID immutability is a core business rule. An ID
        that changes after creation would break the service layer's ability
        to reliably locate, update, and delete records. Only called once
        during construction through __init__.

        Args:
            task_id: The task ID to validate and store.

        Raises:
            ValueError: If the ID is None, empty, or exceeds 10 characters.
        """
        if task_id is None:
            raise ValueError("ID cannot be null.")
        elif len(task_id) > MAX_ID_LENGTH:
            raise ValueError(f"ID cannot exceed {MAX_ID_LENGTH} characters in length.")
        elif len(task_id) == 0:
            raise ValueError("ID must be at least 1 character in length.")

        self._task_id = task_id

    def get_name(self) -> str:
        """Return the task name."""
        return self._name

    def set_name(self, name: str) -> None:
        """Validate and store the task name.

        Public because name is a legitimately editable field. The service
        layer's edit() method relies on this setter to update task fields
        after creation while still enforcing validation rules.

        Args:
            name: The task name to validate and store.

        Raises:
            ValueError: If the name is None, empty, or exceeds 20 characters.
        """
        if name is None:
            raise ValueError("Name cannot be null.")
        elif len(name) > MAX_NAME_LENGTH:
            raise ValueError(f"Name cannot exceed {MAX_NAME_LENGTH} characters in length.")
        elif len(name) == 0:
            raise ValueError("Name must be at least 1 character in length.")

        self._name = name

    def get_description(self) -> str:
        """Return the task description."""
        return self._description

    def set_description(self, description: str) -> None:
        """Validate and store the task description.

        Public because description is a legitimately editable field. The
        service layer's edit() method relies on this setter to update task
        fields after creation while still enforcing validation rules.

        Args:
            description: The task description to validate and store.

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