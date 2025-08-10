from typing import Dict, Optional, List
from uuid import uuid4
from enum import Enum, auto

class TaskStatus(Enum):
    TODO = auto()
    IN_PROGRESS = auto()
    DONE = auto()

class Task:
    def __init__(self, title: str, project_id: str, assigned_to: Optional[List[str]] = None, 
                 status: TaskStatus = TaskStatus.TODO):
        self.id = str(uuid4())
        self.title = title
        self.project_id = project_id
        self.assigned_to = assigned_to or []
        self.status = status
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to,
            "status": self.status.name
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(
            data["title"],
            data["project_id"],
            data.get("assigned_to", []),
            TaskStatus[data["status"]]
        )
        task.id = data["id"]
        return task