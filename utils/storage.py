import json
from pathlib import Path
from typing import Dict, List, TypeVar, Type
from models.user import User
from models.project import Project
from models.task import Task

T = TypeVar('T')

class Storage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.users_file = self.data_dir / "users.json"
        self.projects_file = self.data_dir / "projects.json"
        self.tasks_file = self.data_dir / "tasks.json"
        
        # Initialize files with empty arrays if they don't exist or are empty
        for file in [self.users_file, self.projects_file, self.tasks_file]:
            if not file.exists() or file.stat().st_size == 0:
                with open(file, "w") as f:
                    json.dump([], f)
    
    def _load_data(self, file_path: Path, model_class: Type[T]) -> List[T]:
        try:
            with open(file_path, "r") as f:
                # Check if file is empty
                content = f.read().strip()
                if not content:
                    return []
                
                data = json.loads(content)
                return [model_class.from_dict(item) for item in data]
        except json.JSONDecodeError:
            # If JSON is invalid, return empty list
            return []
    
    def _save_data(self, file_path: Path, data: List[T]):
        with open(file_path, "w") as f:
            json.dump([item.to_dict() for item in data], f, indent=2)
    
    # User operations
    def get_users(self) -> List[User]:
        return self._load_data(self.users_file, User)
    
    def save_users(self, users: List[User]):
        self._save_data(self.users_file, users)
    
    # Project operations
    def get_projects(self) -> List[Project]:
        return self._load_data(self.projects_file, Project)
    
    def save_projects(self, projects: List[Project]):
        self._save_data(self.projects_file, projects)
    
    # Task operations
    def get_tasks(self) -> List[Task]:
        return self._load_data(self.tasks_file, Task)
    
    def save_tasks(self, tasks: List[Task]):
        self._save_data(self.tasks_file, tasks)