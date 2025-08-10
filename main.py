import typer
from rich.console import Console
from rich.table import Table
from typing import Optional, List
from models.user import User
from models.project import Project
from models.task import Task, TaskStatus
from utils.storage import Storage

app = typer.Typer()
console = Console()
storage = Storage()

@app.command()
def add_user(name: str, email: Optional[str] = None):
    """Add a new user"""
    users = storage.get_users()
    if any(user.name == name for user in users):
        console.print(f"[red]User '{name}' already exists![/red]")
        raise typer.Exit(1)
    
    new_user = User(name, email)
    users.append(new_user)
    storage.save_users(users)
    console.print(f"[green]User '{name}' added successfully![/green]")

@app.command()
def list_users():
    """List all users"""
    users = storage.get_users()
    if not users:
        console.print("[yellow]No users found![/yellow]")
        return
    
    table = Table(title="Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="blue")
    table.add_column("Project Count", style="green")
    
    for user in users:
        projects = [p for p in storage.get_projects() if p.user_id == user.id]
        table.add_row(user.id[:8], user.name, user.email or "-", str(len(projects)))
    
    console.print(table)

@app.command()
def add_project(title: str, user_name: str, description: Optional[str] = None):
    """Add a new project for a user"""
    users = storage.get_users()
    user = next((u for u in users if u.name == user_name), None)
    
    if not user:
        console.print(f"[red]User '{user_name}' not found![/red]")
        raise typer.Exit(1)
    
    projects = storage.get_projects()
    if any(p.title == title and p.user_id == user.id for p in projects):
        console.print(f"[red]Project '{title}' already exists for user '{user_name}'![/red]")
        raise typer.Exit(1)
    
    new_project = Project(title, user.id, description)
    projects.append(new_project)
    user.projects.append(new_project.id)
    
    storage.save_projects(projects)
    storage.save_users(users)
    console.print(f"[green]Project '{title}' added for user '{user_name}'![/green]")

@app.command()
def list_projects(user_name: Optional[str] = None):
    """List projects, optionally filtered by user"""
    projects = storage.get_projects()
    users = storage.get_users()
    
    if user_name:
        user = next((u for u in users if u.name == user_name), None)
        if not user:
            console.print(f"[red]User '{user_name}' not found![/red]")
            raise typer.Exit(1)
        projects = [p for p in projects if p.user_id == user.id]
    
    if not projects:
        console.print("[yellow]No projects found![/yellow]")
        return
    
    table = Table(title="Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("User", style="blue")
    table.add_column("Description", style="green")
    table.add_column("Task Count", style="yellow")
    
    for project in projects:
        user = next((u for u in users if u.id == project.user_id), None)
        tasks = [t for t in storage.get_tasks() if t.project_id == project.id]
        table.add_row(
            project.id[:8],
            project.title,
            user.name if user else "Unknown",
            project.description or "-",
            str(len(tasks))
        )
    
    console.print(table)

@app.command()
def add_task(title: str, project_title: str, assigned_to: Optional[List[str]] = None):
    """Add a new task to a project"""
    projects = storage.get_projects()
    project = next((p for p in projects if p.title == project_title), None)
    
    if not project:
        console.print(f"[red]Project '{project_title}' not found![/red]")
        raise typer.Exit(1)
    
    tasks = storage.get_tasks()
    if any(t.title == title and t.project_id == project.id for t in tasks):
        console.print(f"[red]Task '{title}' already exists in project '{project_title}'![/red]")
        raise typer.Exit(1)
    
    # Validate assigned users
    users = storage.get_users()
    if assigned_to:
        invalid_users = [name for name in assigned_to if not any(u.name == name for u in users)]
        if invalid_users:
            console.print(f"[red]Users not found: {', '.join(invalid_users)}[/red]")
            raise typer.Exit(1)
    
    assigned_user_ids = [u.id for u in users if u.name in (assigned_to or [])]
    
    new_task = Task(title, project.id, assigned_user_ids)
    tasks.append(new_task)
    project.tasks.append(new_task.id)
    
    storage.save_tasks(tasks)
    storage.save_projects(projects)
    console.print(f"[green]Task '{title}' added to project '{project_title}'![/green]")

@app.command()
def list_tasks(project_title: Optional[str] = None):
    """List tasks, optionally filtered by project"""
    tasks = storage.get_tasks()
    projects = storage.get_projects()
    users = storage.get_users()
    
    if project_title:
        project = next((p for p in projects if p.title == project_title), None)
        if not project:
            console.print(f"[red]Project '{project_title}' not found![/red]")
            raise typer.Exit(1)
        tasks = [t for t in tasks if t.project_id == project.id]
    
    if not tasks:
        console.print("[yellow]No tasks found![/yellow]")
        return
    
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Project", style="blue")
    table.add_column("Assigned To", style="green")
    table.add_column("Status", style="yellow")
    
    for task in tasks:
        project = next((p for p in projects if p.id == task.project_id), None)
        assigned_names = [u.name for u in users if u.id in task.assigned_to]
        table.add_row(
            task.id[:8],
            task.title,
            project.title if project else "Unknown",
            ", ".join(assigned_names) or "Unassigned",
            task.status.name
        )
    
    console.print(table)

@app.command()
def complete_task(task_title: str, project_title: str):
    """Mark a task as complete"""
    projects = storage.get_projects()
    project = next((p for p in projects if p.title == project_title), None)
    
    if not project:
        console.print(f"[red]Project '{project_title}' not found![/red]")
        raise typer.Exit(1)
    
    tasks = storage.get_tasks()
    task = next((t for t in tasks if t.title == task_title and t.project_id == project.id), None)
    
    if not task:
        console.print(f"[red]Task '{task_title}' not found in project '{project_title}'![/red]")
        raise typer.Exit(1)
    
    if task.status == TaskStatus.DONE:
        console.print(f"[yellow]Task '{task_title}' is already marked as done![/yellow]")
        return
    
    task.status = TaskStatus.DONE
    storage.save_tasks(tasks)
    console.print(f"[green]Task '{task_title}' marked as done![/green]")

if __name__ == "__main__":
    app()