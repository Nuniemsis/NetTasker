from pydantic import BaseModel, ConfigDict
from app.schemas.task_status_enum import TaskStatus

class CountStatusResponseModel(BaseModel):
    status: TaskStatus  # Use the enum here
    count: int = 0

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True
    )