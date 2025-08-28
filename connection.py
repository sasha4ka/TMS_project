import websockets
import json


async def websocket_handler(websocket, path):
    pass


async def inbound_handler(websocket: websockets.ServerConnection, path):
    while True:
        message = await websocket.recv()
        message = json.loads(message)
        
