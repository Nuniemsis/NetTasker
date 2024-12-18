# crud.py: Handles database operations for tasks
from uuid import uuid4
from sqlalchemy.orm import Session
from models.task_model import TaskModel
from schemas.task_status_enum import TaskStatus
from datetime import datetime, timezone
from typing import List

def create_task_in_db(db: Session) -> TaskModel:
    """Creates a new task in the database."""
    task_id = str(uuid4())
    start_date = datetime.now(tz=timezone.utc)
    new_task = TaskModel(id=task_id, start_date=start_date)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
def update_task_status(task_id: str, status: str, result: str, db: Session):
    """Update the status and result of a task."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        task.status = status
        task.result = result
        task.end_date = datetime.now(tz=timezone.utc)
        db.commit()
        db.refresh(task)
    return task
def count_tasks_by_status(db: Session, status: TaskStatus) -> int:
    """Counts tasks in the database by their status."""
    return db.query(TaskModel).filter(TaskModel.status == status.value).count()

def get_paginated_tasks(db: Session, limit: int, offset: int) -> List[TaskModel]:
    """Fetches paginated tasks from the database."""
    return db.query(TaskModel).offset(offset).limit(limit).all()
def count_total_tasks(db: Session) -> int:
    """Counts the total number of tasks in the database."""
    return db.query(TaskModel).count()


def list_all_tasks(db: Session):
    """Retrieve all tasks from the database."""
    return db.query(TaskModel).all()
