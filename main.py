import asyncio
import logging
import websockets
import dotenv
import os

from listener import connection_handler


dotenv.load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.info("HELLO")

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', '9005'))


async def main():
    async with websockets.serve(connection_handler, HOST, PORT):
        logger.info(f'server started on {HOST}:{PORT}')
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
