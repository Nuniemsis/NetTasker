import asyncio
import pytest
from schemas.task_status_enum import TaskStatus
from schemas.notification_type_enum import NotificationType
import logging
from starlette.testclient import WebSocketTestSession

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG

def test_create_task(client):
    response = client.post("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == TaskStatus.pending.value

def test_list_tasks(client):
    # Create tasks for testing
    client.post("/tasks")
    client.post("/tasks")
    
    response = client.get("/tasks?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "total_count" in data
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_task_count(client):
    status = TaskStatus.pending.value
    response = client.get(f"/tasks/count?status={status}")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "count" in data
    assert data["status"] == status


@pytest.mark.asyncio
async def test_notifications_received(client):
    # Step 1: Start the WebSocket connection
    logger.info("Starting WebSocket listener...")
    websocket_task = asyncio.create_task(start_websocket_listener(client=client, endpoint="/ws", max_notifications=5))

    # Step 3: Wait for WebSocket notifications
    logger.info("Waiting for WebSocket notifications...")
    notifications = await websocket_task
    logger.info(f"Notifications received: {notifications}")

    assert len(notifications) > 0, "No notifications received from WebSocket"
    for notification in notifications:
        logger.info(f"Notification received: {notification}")
        assert "type" in notification, "Notification missing 'type' field"
        assert notification["type"] == NotificationType.task_update.value, (
            f"Unexpected notification type: {notification['type']}"
        )


async def start_websocket_listener(client, endpoint, max_notifications=5, timeout=10):
    """Listen to WebSocket notifications."""
    notifications = []
    logger.info(f"Connecting to WebSocket endpoint: {endpoint}")
    with client.websocket_connect(endpoint) as websocket:
        assert isinstance(websocket, WebSocketTestSession)
        try:
            logger.info("Listening for WebSocket messages...")
            while len(notifications) < max_notifications:
                notification = websocket.receive_json()
                notifications.append(notification)
                logger.info(f"Notification received: {notification}")
        except Exception as e:
            logger.error(f"WebSocket listener encountered an error: {e}")
        finally:
            logger.info("Closing WebSocket connection...")
            websocket.close()
    logger.info("WebSocket listener finished.")
    return notifications
