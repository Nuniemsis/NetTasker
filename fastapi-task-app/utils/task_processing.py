from time import sleep
import asyncio
from sqlalchemy.orm import Session
from app.schemas.notification import Notification
from app.schemas.notification_type_enum import NotificationType
from crud.task_crud import update_task_status
from routes.websocket_routes import notify_clients
from app.schemas.task_status_enum import TaskStatus

async def process_task(task_id: str, db: Session):
    """Simulate a time-consuming task and notify clients."""
    try:
        print(f"Starting task processing for task_id={task_id}")

        await notify_clients(notification=Notification(type=NotificationType.task_update))
        
        # Simulate a long-running process
        await asyncio.sleep(10)
        
        # Update status to 'completed'
        update_task_status(task_id, TaskStatus.completed.value, f"Result of task {task_id}", db)
        await notify_clients(notification=Notification(type=NotificationType.task_update))
    except Exception as e:
        # Update status to 'failed' in case of an error
        update_task_status(task_id, TaskStatus.failed.value, f"Task failed: {str(e)}", db)

        await notify_clients(notification=Notification(type=NotificationType.task_update))
    finally:
        print(f"Finished task processing for task_id={task_id}")
