from typing import List, Dict, Optional
from uuid import uuid4
from datetime import datetime

class Project:
    def __init__(self, title: str, user_id: str, description: Optional[str] = None, 
                 due_date: Optional[str] = None):
        self.id = str(uuid4())
        self.title = title
        self.user_id = user_id
        self.description = description
        self.due_date = due_date
        self.tasks: List[str] = []  # List of task IDs
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": self.tasks
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        project = cls(
            data["title"],
            data["user_id"],
            data.get("description"),
            data.get("due_date")
        )
        project.id = data["id"]
        project.tasks = data.get("tasks", [])
        return project