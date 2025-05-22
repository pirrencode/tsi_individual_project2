from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    due_date: Optional[datetime] = None

    def to_row(self) -> Dict[str, str]:
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "completed": str(int(self.completed)),
            "due_date": self.due_date.isoformat() if self.due_date else ""
        }

    @staticmethod
    def from_row(row: Dict[str, str]) -> 'Task':
        due = row.get("due_date")
        due_date = datetime.fromisoformat(due) if due else None
        return Task(
            id=int(row.get("id", 0)),
            title=row.get("title", ""),
            description=row.get("description", ""),
            completed=row.get("completed", "0") in ("1", "True", "true"),
            due_date=due_date,
        )
