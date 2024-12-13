from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.schemas.notification import Notification

router = APIRouter()
connected_clients = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def notify_clients(notification: Notification):
    for websocket in connected_clients:
        await websocket.send_json(notification.model_dump())
