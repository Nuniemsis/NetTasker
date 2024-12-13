# crud/task_crud.py: CRUD operations for task management
from sqlalchemy.orm import Session
from models.task_model import Task

def create_task(task_id: str, db: Session):
    """Create a new task in the database."""
    new_task = Task(id=task_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_task(task_id: str, db: Session):
    """Retrieve a task by its ID."""
    return db.query(Task).filter(Task.id == task_id).first()

def update_task_status(task_id: str, status: str, result: str, db: Session):
    """Update the status and result of a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        task.result = result
        db.commit()
        db.refresh(task)
    return task

def list_all_tasks(db: Session):
    """Retrieve all tasks from the database."""
    return db.query(Task).all()
