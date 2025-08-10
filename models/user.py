from typing import List, Dict, Optional
from uuid import uuid4

class User:
    def __init__(self, name: str, email: Optional[str] = None):
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.projects: List[str] = []  # List of project IDs
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": self.projects
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        user = cls(data["name"], data.get("email"))
        user.id = data["id"]
        user.projects = data.get("projects", [])
        return user