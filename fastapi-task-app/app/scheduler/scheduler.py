from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging
from app.routes.websocket_routes import notify_clients
from app.schemas.notification import Notification
from app.schemas.notification_type_enum import NotificationType

# Logger setup
logger = logging.getLogger(__name__)

# Initialize the scheduler
scheduler = AsyncIOScheduler()

async def scheduled_task():
    """An example scheduled task."""
    logger.info("Running scheduled task!")
    # Add any task-specific logic here
    await notify_clients(notification=Notification(type=NotificationType.task_update))

# Function to add jobs to the scheduler
def setup_scheduler():
    scheduler.add_job(scheduled_task, "interval", seconds=2)  # Example: runs every 10 seconds
    scheduler.start()
    logger.info("Scheduler started with tasks.")
