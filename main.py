import uvicorn
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from lib.Connections.ConnectionManager import ConnectionManager
from lib.schemas.Broadcasts import MessageBroadcast, DeleteBroadcast

app = FastAPI()
manager = ConnectionManager()
prev_messages: List[MessageBroadcast] = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await manager.add_connection(websocket)
    for msg in prev_messages[len(prev_messages)-11:]:
        await websocket.send_json(msg.dict())
    try:
        while True:
            data = await websocket.receive_json()
            if data['type'] == 'msg':
                outgoing_msg: MessageBroadcast = MessageBroadcast.parse_obj(data)
                outgoing_msg.id = (len(prev_messages)-1 + 1)
                await manager.broadcast_json(outgoing_msg.dict())
                prev_messages.append(outgoing_msg)
            if data['type'] == 'delete':
                outgoing_delete: DeleteBroadcast = DeleteBroadcast.parse_obj(data)
                for index, msg in enumerate(prev_messages):
                    if outgoing_delete.id == msg.id:
                        msg.message_text = "Deleted Message"
                        prev_messages[index] = msg
                        break
                await manager.broadcast_json(outgoing_delete.dict())
    except WebSocketDisconnect:
        await manager.remove_connection(websocket)


if __name__ == "__main__":
    uvicorn.run("app", reload=True)
