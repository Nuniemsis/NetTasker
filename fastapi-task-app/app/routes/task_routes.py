from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.task_status_count import CountStatusResponseModel
from app.schemas.task_status_enum import TaskStatus
from app.schemas.task_schema import PaginatedTasksResponse, TaskResponse
from app.database.database import SessionLocal
from app.utils.task_processing import process_task
from app.crud.task_crud import (
    create_task_in_db,
    get_paginated_tasks,
    count_total_tasks,
    count_tasks_by_status,
)

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
    new_task = create_task_in_db(db)
    background_tasks.add_task(process_task, new_task.id, db)
    return TaskResponse(
        task_id=new_task.id, 
        status=TaskStatus.pending.value, 
        start_date=new_task.start_date
    )


@router.get("/tasks", response_model=PaginatedTasksResponse)
def list_tasks(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    total_count = count_total_tasks(db)
    tasks = get_paginated_tasks(db, limit, offset)
    task_responses = [
        TaskResponse(
            task_id=task.id,
            status=task.status,
            result=task.result,
            start_date=task.start_date,
            end_date=task.end_date
        ) for task in tasks
    ]
    return PaginatedTasksResponse(
        total_count=total_count,
        items=task_responses
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
    total_count = count_tasks_by_status(db, status)
    return CountStatusResponseModel(status=status.value, count=total_count)
