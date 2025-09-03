from functools import wraps
from typing import Callable
import websockets
import json
import logging
import os

from classes import Debug, Response

sockets: list[websockets.ServerConnection] = []
authenticated: list[websockets.ServerConnection] = []
logger = logging.getLogger('Listener')
logger.setLevel(logging.INFO)
token = os.getenv('API_TOKEN')

message_types: dict[str, Callable] = {}


async def connection_handler(websocket: websockets.ServerConnection):
    sockets.append(websocket)
    await inbound_handler(websocket)


def add_handler(message_type: str):
    def decorator(handler: Callable):
        @wraps(handler)
        async def wrapper(*args, **kwargs):
            websocket, message = args
            if not (websocket in authenticated or
                    message.get('type', '') == 'authentication'):
                logger.warning('not authenticated user ' +
                               f'{websocket.remote_address[0]}:{message}')
                await websocket.send(json.dumps({
                    'type': 'error',
                    'text': 'non_authorized'
                }))
                return
            await handler(*args, **kwargs)
        message_types[message_type] = wrapper
        return wrapper
    return decorator


async def empty_handler(websocket, message: dict):
    logger.warning(f'message not handled: {message}')


async def close_connection(websocket):
    try:
        sockets.remove(websocket)
    except ValueError:
        pass
    try:
        authenticated.remove(websocket)
    except ValueError:
        pass
    await websocket.close()


async def handle_message(websocket, message: dict):
    message_type = message.get('type', '')
    await message_types.get(message_type, empty_handler)(websocket, message)


async def inbound_handler(websocket: websockets.ServerConnection):
    logger.info(f'Connection open: {websocket.remote_address[0]}')
    while True:
        try:
            message = await websocket.recv()
            message = json.loads(message)
            print(message)
            await handle_message(websocket, message)

        except websockets.ConnectionClosed:
            logger.info(f'Connection closed: {websocket.remote_address[0]}')
            break

        except Exception as er:
            logger.exception(er)
            break
    await close_connection(websocket)


async def broadcast_message(message: dict | Response | Debug):
    if isinstance(message, Response) or \
       isinstance(message, Debug):
        message = message.serialize()

    global sockets
    for socket in sockets:
        await socket.send(json.dumps(message))


@add_handler('authentication')
async def authentication_handler(websocket, message: dict):
    if message.get('token') != token:
        await websocket.send(json.dumps(
            {
                'type': 'authentication',
                'success': False
            }
        ))
        await close_connection(websocket)
    else:
        await websocket.send(json.dumps(
            {
                'type': 'authentication',
                'success': True
            }
        ))
        authenticated.append(websocket)


@add_handler('echo')
async def echo_handler(websocket: websockets.ServerConnection, message: dict):
    await websocket.send(json.dumps(message))


@add_handler('close')
async def close_handler(websocket: websockets.ServerConnection, message: dict):
    await close_connection(websocket)
