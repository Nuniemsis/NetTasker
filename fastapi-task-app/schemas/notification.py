from pydantic import BaseModel
from typing import List, Optional
from app.schemas.notification_type_enum import NotificationType


class Notification(BaseModel):
    type: NotificationType  # Use the enum here

    class Config:
        from_attributes = True  # Enable ORM compatibility (Pydantic v2)