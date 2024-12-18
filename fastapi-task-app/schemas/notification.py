from pydantic import BaseModel, ConfigDict
from schemas.notification_type_enum import NotificationType

class Notification(BaseModel):
    type: NotificationType  # Use the enum here

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True
    )