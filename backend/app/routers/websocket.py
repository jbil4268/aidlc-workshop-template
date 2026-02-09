"""WebSocket Router for real-time updates"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.websocket import manager

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/admin/{store_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    store_id: int
):
    """
    WebSocket endpoint for admin real-time order updates.
    
    Args:
        websocket: WebSocket connection
        store_id: Store ID for filtering orders
    """
    await manager.connect(websocket, store_id)
    
    try:
        while True:
            # Keep connection alive and receive messages
            data = await websocket.receive_text()
            
            # Echo back for heartbeat
            await websocket.send_json({"type": "pong", "message": "Connection alive"})
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, store_id)
