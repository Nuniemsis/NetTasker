# routes/task_routes.py: Define rutas relacionadas con tareas
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.task_status_count import CountStatusResponseModel
from app.schemas.task_status_enum import TaskStatus
from schemas.task_schema import PaginatedTasksResponse, TaskResponse
from database.database import SessionLocal
from models.task_model import Task
from utils.task_processing import process_task
from uuid import uuid4

router = APIRouter()

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks")
def create_task(background_tasks: BackgroundTasks, 
                db: Session = Depends(get_db)
                ):
    """Create a new task and process it in the background."""
    task_id = str(uuid4())
    new_task = Task(id=task_id)
    db.add(new_task)
    db.commit()
    background_tasks.add_task(process_task, task_id, db)
    return TaskResponse(task_id=task_id, status=TaskStatus.pending.value)

@router.get("/tasks", response_model=PaginatedTasksResponse)
def list_tasks(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    # Get total count of tasks (without limit or offset)
    total_count = db.query(Task).count()

    # Fetch the paginated tasks
    tasks = db.query(Task).offset(offset).limit(limit).all()
    tasks = [
        TaskResponse(
            task_id=task.id,
            status=task.status,
            result=task.result
        ) for task in tasks
    ]

    # Return the paginated response with total_count included
    return PaginatedTasksResponse(
        total_count=total_count,
        items=tasks
    )


@router.get("/tasks/count", response_model=CountStatusResponseModel)
def get_task_count(
    status: TaskStatus, 
    db: Session = Depends(get_db)
):
    """
    Get the total count of tasks based on their status.
    Args:
        status: The status of the tasks to count ('pending', 'completed', 'failed').

    Returns:
        A dictionary containing the total count of tasks with the given status.
    """
    valid_statuses = ["pending", "completed", "failed"]
    if status not in valid_statuses:
        return {"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}

    total_count = db.query(Task).filter(Task.status == status.value).count()
    count_response = CountStatusResponseModel(status=status.value, count=total_count)
    return count_response
