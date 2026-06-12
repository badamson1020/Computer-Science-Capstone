"""Tests for the TaskService service layer.

Covers all CRUD operations for both happy path and error path scenarios.
"""

import unittest
from task import Task
from task_service import TaskService

# NoSuchElementException is a custom exception that mirrors Java's
# NoSuchElementException behavior. Python has no direct built-in equivalent,
# so a custom class was created to preserve the same exception hierarchy
# and semantics as the original Java implementation during translation.
from exceptions import NoSuchElementException


class TestTaskService(unittest.TestCase):
    """Test the TaskService CRUD operations.

    Tests cover happy path and error path scenarios for all operations.
    Equality assertions compare Task objects by field values rather than
    object references. The @dataclass decorator generates __eq__ based on
    field values, and get() returns copies rather than stored references,
    so assertEqual verifies the correct data was stored and retrieved rather
    than checking if two variables point to the same object in memory.

    No tearDown method is needed. Python's garbage collector automatically
    reclaims memory for in-memory objects when they go out of scope after
    each test. tearDown is only necessary for external resources like database
    connections or file handles.
    """

    def setUp(self) -> None:
        """Initialize a fresh TaskService and default Task before each test.

        A new service and default task are created before every test to
        prevent shared state issues between tests that modify task fields.
        If a single service instance were shared across tests, state changes
        from one test such as adding or deleting tasks could affect subsequent
        tests in unpredictable ways.
        """
        self.service = TaskService()
        self.default_task = Task("32", "Clean", "Removes junk data")

    ###########################################################
    # Test Add
    ###########################################################

    def test_add_with_new_element_successfully_adds(self):
        self.service.add(self.default_task)
        self.assertEqual(self.service.get(self.default_task.get_id()), self.default_task)

    def test_add_with_duplicate_element_raises_value_error(self):
        self.service.add(self.default_task)
        self.assertIsNotNone(self.service.get(self.default_task.get_id()))
        with self.assertRaises(ValueError):
            self.service.add(self.default_task)

    def test_add_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.add(None)

    ###########################################################
    # Test Delete
    ###########################################################

    def test_delete_with_existing_element_successfully_deletes(self):
        self.service.add(self.default_task)
        self.assertIsNotNone(self.service.get(self.default_task.get_id()))
        self.service.delete(self.default_task.get_id())
        self.assertIsNone(self.service.get(self.default_task.get_id()))

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

    def test_edit_with_updated_task_updates_fields_successfully(self):
        self.service.add(self.default_task)
        updated_task = Task("32", "Compress", "Compresses files")
        self.service.edit(updated_task)
        checked_task = self.service.get("32")
        self.assertEqual("Compress", checked_task.get_name())
        self.assertEqual("Compresses files", checked_task.get_description())

    def test_edit_with_non_existing_task_raises_no_such_element_exception(self):
        # A new task is created but never added to the TaskService
        non_existing_task = Task("123", "Non", "Existent")
        with self.assertRaises(NoSuchElementException):
            self.service.edit(non_existing_task)

    def test_edit_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.edit(None)

    ###########################################################
    # Test Get
    ###########################################################

    def test_get_with_valid_id_returns_correct_task(self):
        self.service.add(self.default_task)
        selected_task = self.service.get(self.default_task.get_id())
        self.assertIsNotNone(selected_task)
        self.assertEqual(self.default_task, selected_task)

    def test_get_with_invalid_id_returns_none(self):
        self.service.add(self.default_task)
        selected_task = self.service.get("234")
        self.assertIsNone(selected_task)

    def test_get_with_null_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.get(None)

    ###########################################################
    # Test GetAll
    ###########################################################

    def test_get_all_with_multiple_tasks_returns_all_tasks(self):
        task2 = Task("12", "Compress", "Compresses files")
        self.service.add(self.default_task)
        self.service.add(task2)
        all_tasks = self.service.get_all()
        self.assertEqual(2, len(all_tasks))
        self.assertIn(self.default_task, all_tasks)
        self.assertIn(task2, all_tasks)

    def test_get_all_with_no_tasks_returns_empty_list(self):
        all_tasks = self.service.get_all()
        self.assertEqual(0, len(all_tasks))

    def test_get_all_after_deleting_task_returns_remaining_tasks(self):
        task2 = Task("12", "Compress", "Compresses files")
        self.service.add(self.default_task)
        self.service.add(task2)
        self.service.delete(self.default_task.get_id())
        all_tasks = self.service.get_all()
        self.assertEqual(1, len(all_tasks))
        self.assertIn(task2, all_tasks)
        self.assertNotIn(self.default_task, all_tasks)


if __name__ == "__main__":
    unittest.main()