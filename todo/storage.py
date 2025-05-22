from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Iterable, Dict
import csv
from .models import Task

class StorageInterface(ABC):
    """Interface object defining contract for task storage."""

    @abstractmethod
    def load_tasks(self) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def save_tasks(self, tasks: Iterable[Task]) -> None:
        raise NotImplementedError

class CSVStorage(StorageInterface):
    """Base CSV storage implementing basic read/write."""
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def load_rows(self) -> List[Dict[str, str]]:
        try:
            with open(self.filename, newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            return []

    def save_rows(self, rows: Iterable[Dict[str, str]]) -> None:
        fieldnames = ["id", "title", "description", "completed", "due_date"]
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    # Implement interface methods
    def load_tasks(self) -> List[Task]:
        rows = self.load_rows()
        return [Task.from_row(r) for r in rows]

    def save_tasks(self, tasks: Iterable[Task]) -> None:
        rows = [t.to_row() for t in tasks]
        self.save_rows(rows)

class CSVTaskStorage(CSVStorage):
    """Specialized CSV storage for Tasks (multi-level inheritance example)."""
    pass
