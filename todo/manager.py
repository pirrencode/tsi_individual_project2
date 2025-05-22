from __future__ import annotations
from typing import Callable, List
from dataclasses import dataclass, field

from .models import Task
from .storage import StorageInterface, CSVTaskStorage

class Filterable:
    """Interface defining a filter method."""
    def filter_tasks(self, predicate: Callable[[Task], bool]) -> List[Task]:
        raise NotImplementedError

@dataclass
class TodoManager(Filterable):
    storage: StorageInterface
    tasks: List[Task] = field(default_factory=list)

    def load(self) -> None:
        self.tasks = self.storage.load_tasks()

    def save(self) -> None:
        self.storage.save_tasks(self.tasks)

    def add_task(self, title: str, description: str = "", due_date=None) -> Task:
        task_id = (max((t.id for t in self.tasks), default=0) + 1)
        task = Task(id=task_id, title=title, description=description, due_date=due_date)
        self.tasks.append(task)
        return task

    def mark_complete(self, task_id: int) -> None:
        for t in self.tasks:
            if t.id == task_id:
                t.completed = True
                break

    def filter_tasks(self, predicate: Callable[[Task], bool]) -> List[Task]:
        return [t for t in self.tasks if predicate(t)]

    def list_tasks(self) -> List[Task]:
        return self.tasks
