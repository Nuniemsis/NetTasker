import random
import logging
from time import sleep
import asyncio
from sqlalchemy.orm import Session
from schemas.notification import Notification
from schemas.notification_type_enum import NotificationType
from crud.task_crud import update_task_status
from routes.websocket_routes import notify_clients
from schemas.task_status_enum import TaskStatus

# Configure logger
logger = logging.getLogger(__name__)

async def process_task(task_id: str, db: Session):
    """Simulate a time-consuming task with random failure and random delay."""
    try:
        logger.info(f"Starting task processing for task_id={task_id}")

        await notify_clients(notification=Notification(type=NotificationType.task_update))
        logger.info(f"Clients notified about task {task_id} update.")

        delay = random.randint(1, 10)
        logger.info(f"Task {task_id} will run for {delay} seconds.")
        await asyncio.sleep(delay)
        
        # Introduce random failure
        if random.choice([True, False]):  # 50% chance of failure
            raise Exception("Random failure occurred.")
        
        update_task_status(task_id, TaskStatus.completed.value, f"Result of task {task_id}", db)
        logger.info(f"Task {task_id} marked as completed.")
        await notify_clients(notification=Notification(type=NotificationType.task_update))
        logger.info(f"Clients notified about task {task_id} completion.")
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}", exc_info=True)
        update_task_status(task_id, TaskStatus.failed.value, f"Task failed: {str(e)}", db)
        await notify_clients(notification=Notification(type=NotificationType.task_update))
        logger.info(f"Clients notified about task {task_id} failure.")
        db.close()
    finally:
        logger.info(f"Finished task processing for task_id={task_id}")
        db.close()
