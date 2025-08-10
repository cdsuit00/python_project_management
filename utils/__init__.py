import json
from pathlib import Path

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