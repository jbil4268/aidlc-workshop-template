"""WebSocket Connection Manager for real-time order updates"""
from fastapi import WebSocket
from typing import Dict, List
import json


class ConnectionManager:
    """Manages WebSocket connections for admin clients"""
    
    def __init__(self):
        # Store active connections by store_id
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, store_id: int):
        """
        Accept and register a new WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            store_id: Store ID for grouping connections
        """
        await websocket.accept()
        
        if store_id not in self.active_connections:
            self.active_connections[store_id] = []
        
        self.active_connections[store_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, store_id: int):
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
            store_id: Store ID
        """
        if store_id in self.active_connections:
            if websocket in self.active_connections[store_id]:
                self.active_connections[store_id].remove(websocket)
            
            # Clean up empty lists
            if not self.active_connections[store_id]:
                del self.active_connections[store_id]
    
    async def broadcast_to_store(self, store_id: int, message: dict):
        """
        Broadcast message to all connections for a specific store.
        
        Args:
            store_id: Store ID
            message: Message dictionary to broadcast
        """
        if store_id not in self.active_connections:
            return
        
        # Remove disconnected clients
        disconnected = []
        
        for connection in self.active_connections[store_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection, store_id)
    
    async def send_order_update(self, store_id: int, order_data: dict):
        """
        Send order update notification to all admin clients.
        
        Args:
            store_id: Store ID
            order_data: Order data dictionary
        """
        message = {
            "type": "order_update",
            "data": order_data
        }
        
        await self.broadcast_to_store(store_id, message)
    
    async def send_new_order(self, store_id: int, order_data: dict):
        """
        Send new order notification to all admin clients.
        
        Args:
            store_id: Store ID
            order_data: Order data dictionary
        """
        message = {
            "type": "new_order",
            "data": order_data
        }
        
        await self.broadcast_to_store(store_id, message)


# Global connection manager instance
manager = ConnectionManager()
