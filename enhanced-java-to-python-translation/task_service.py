"""Service layer for managing a collection of Task objects.

This module represents the Service Layer of the Service-Repository
layered architecture. TaskService is responsible for enforcing
collection-level business rules, ensuring the task list remains
valid, consistent, and well-organized. Field-level data integrity rules
such as length and format validation are handled separately in the
Task class, keeping each layer focused on a single responsibility.
"""

from task import Task

# NoSuchElementException is a custom exception that mirrors Java's
# NoSuchElementException behavior. Python has no direct built-in equivalent,
# so a custom class was created to preserve the same exception hierarchy
# and semantics as the original Java implementation during translation.
from exceptions import NoSuchElementException


class TaskService:
    """Manage a collection of Task objects following the Service Layer pattern.

    Provides add, delete, edit, get, and get_all operations with full input
    validation before processing. The internal _tasks list is private to
    enforce that all modifications go through the service layer's validation
    logic. Direct list access would bypass duplicate ID checks and allow
    external code to insert unvalidated objects.

    Copies are returned from get() and get_all() rather than stored
    references to prevent external code from modifying internal state
    directly and bypassing the service layer's business rules.
    """

    def __init__(self) -> None:
        """Initialize the TaskService with an empty task list."""
        self._tasks = []

    def add(self, new_task: Task) -> None:
        """Add a new task to the service.

        Validates that the task is not None and that the ID is unique
        before adding. Duplicate ID prevention is a service layer
        responsibility since it is a collection-level business rule
        rather than a field-level data rule belonging in the Task class.

        Args:
            new_task: The Task object to add.

        Raises:
            ValueError: If the task is None or a duplicate ID exists.
        """
        if new_task is None:
            raise ValueError("Task cannot be null.")

        if self._find_task(new_task.get_id()) is not None:
            raise ValueError(f"Cannot add task with duplicate ID: {new_task.get_id()}")

        self._tasks.append(new_task)

    def delete(self, task_id: str) -> None:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Raises:
            ValueError: If the ID is None.
            NoSuchElementException: If no task with the given ID exists.
        """
        if task_id is None:
            raise ValueError("ID cannot be null.")

        task_to_delete = self._find_task(task_id)

        if task_to_delete is None:
            raise NoSuchElementException(f"Task with ID {task_id} does not exist.")

        self._tasks.remove(task_to_delete)

    def edit(self, updated_task: Task) -> None:
        """Update an existing task's name and description.

        The task ID cannot be updated since it is immutable by design in
        the Task class. Only name and description are editable fields.
        The update is applied directly to the stored object using the
        Task class's public setters, which enforce validation rules on
        the new values before storing them.

        Args:
            updated_task: A Task object containing the updated fields.

        Raises:
            ValueError: If the updated task or its ID is None.
            NoSuchElementException: If no task with the given ID exists.
        """
        if updated_task is None or updated_task.get_id() is None:
            raise ValueError("The task and/or its ID cannot be null.")

        existing_task = self._find_task(updated_task.get_id())

        if existing_task is None:
            raise NoSuchElementException(f"Task with ID {updated_task.get_id()} does not exist.")

        existing_task.set_name(updated_task.get_name())
        existing_task.set_description(updated_task.get_description())

    def get(self, task_id: str) -> Task | None:
        """Retrieve a copy of the task with the given ID.

        Returns a copy rather than the stored reference to prevent external
        code from obtaining a direct reference to the internal object and
        modifying it in ways that bypass the service layer's validation.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            A copy of the matching Task, or None if not found.

        Raises:
            ValueError: If the ID is None.
        """
        if task_id is None:
            raise ValueError("ID cannot be null.")

        found_task = self._find_task(task_id)

        if found_task is not None:
            return Task.from_task(found_task)
        else:
            return None

    def get_all(self) -> list:
        """Return a list of copies of all tasks in the service.

        Copies are returned rather than stored references to prevent external
        code from modifying internal state directly. Returns an empty list
        if no tasks exist.

        Returns:
            A list of independent Task copies.
        """
        return [Task.from_task(task) for task in self._tasks]

    def _find_task(self, task_id: str) -> Task | None:
        """Search the internal list for a task matching the given ID.

        Private because it exposes a direct reference to the stored object
        rather than a copy. Only used internally by add(), delete(), get(),
        and edit() where direct reference access is needed for modification
        or removal. External callers should use get() which returns a safe
        copy instead.

        Args:
            task_id: The ID to search for.

        Returns:
            The matching Task reference, or None if not found.
        """
        found_task = None

        for task in self._tasks:
            if task.get_id() == task_id:
                found_task = task
                break

        return found_task