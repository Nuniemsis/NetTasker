from pydantic import BaseModel
from typing import List, Optional
from app.schemas.task_status_enum import TaskStatus


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus  # Use the enum here
    result: Optional[str] = None  # Mark as Optional with a default value of None

    class Config:
        from_attributes = True  # Enable ORM compatibility (Pydantic v2)
class PaginatedTasksResponse(BaseModel):
    total_count: int
    items: List[TaskResponse]