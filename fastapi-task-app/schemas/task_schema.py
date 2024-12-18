from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from schemas.task_status_enum import TaskStatus


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus  # Use the enum here
    result: Optional[str] = None  # Mark as Optional with a default value of None
    start_date: Optional[datetime] = None  # Optional start_date
    end_date: Optional[datetime] = None  # Optional end_date

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True
    )
class PaginatedTasksResponse(BaseModel):
    total_count: int
    items: List[TaskResponse]