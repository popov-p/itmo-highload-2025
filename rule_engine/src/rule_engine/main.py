import asyncio
from prometheus_client import start_http_server
from .rabbitmq import connect_to_rabbitmq
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('/var/log/rule_engine.log', mode='a')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


async def main():
    start_http_server(8080)
    connection, channel = await connect_to_rabbitmq()
    try:
        await asyncio.Future()
    finally:
        await channel.close()
        await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())