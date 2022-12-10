from typing import List

from fastapi import WebSocket


class ConnectionManager:
    connections: List[WebSocket]

    def __init__(self):
        self.connections = []

    async def add_connection(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def remove_connection(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast_text(self, msg: str):
        for sock in self.connections:
            await sock.send_text(msg)

    async def broadcast_json(self, json_dict: dict):
        for sock in self.connections:
            await sock.send_json(json_dict)
