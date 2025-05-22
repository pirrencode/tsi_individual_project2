import os
import tempfile
import unittest
from datetime import datetime

from todo.manager import TodoManager
from todo.storage import CSVTaskStorage


def create_manager(tmpdir):
    storage = CSVTaskStorage(os.path.join(tmpdir, "tasks.csv"))
    manager = TodoManager(storage)
    manager.load()
    return manager


class TodoManagerTests(unittest.TestCase):
    def test_add_and_persist_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = create_manager(tmp)
            manager.add_task("Test", description="desc", due_date=datetime(2023, 1, 1, 10, 0))
            manager.save()

            manager2 = TodoManager(CSVTaskStorage(os.path.join(tmp, "tasks.csv")))
            manager2.load()

            self.assertEqual(len(manager2.list_tasks()), 1)
            t = manager2.list_tasks()[0]
            self.assertEqual(t.title, "Test")
            self.assertEqual(t.description, "desc")
            self.assertEqual(t.due_date, datetime(2023, 1, 1, 10, 0))

    def test_mark_complete_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = create_manager(tmp)
            task = manager.add_task("Task")
            self.assertTrue(manager.mark_complete(task.id))
            self.assertTrue(manager.list_tasks()[0].completed)

    def test_mark_complete_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = create_manager(tmp)
            manager.add_task("Task")
            self.assertFalse(manager.mark_complete(999))

    def test_filter_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = create_manager(tmp)
            t1 = manager.add_task("A")
            t2 = manager.add_task("B")
            manager.mark_complete(t2.id)
            completed = manager.filter_tasks(lambda t: t.completed)
            self.assertEqual([t.id for t in completed], [t2.id])


if __name__ == "__main__":
    unittest.main()
