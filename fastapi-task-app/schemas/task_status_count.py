from pydantic import BaseModel
from typing import List, Optional
from schemas.task_status_enum import TaskStatus


class CountStatusResponseModel(BaseModel):
    status: TaskStatus  # Use the enum here
    count: int = 0

    class Config:
        from_attributes = True  # Enable ORM compatibility (Pydantic v2)