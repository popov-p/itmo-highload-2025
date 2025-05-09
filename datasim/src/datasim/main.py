import os
from proto.messages_pb2 import Batch, HealthStatus
from .prometheus import REQUESTS_TOTAL, REQUESTS_FAILED, REQUEST_DURATION, DEVICE_FREQ, DEVICE_COUNT
from prometheus_client import start_http_server
import asyncio
import aiohttp
import signal
import logging
import time
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('/var/log/datasim.log', mode='a')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# url = "http://nginx/incoming-data"
url = "http://controller:8060/incoming-data"

class DataSimulator:
    def __init__(self, num_devices: int, frequency: float):
        self.num_devices = num_devices
        self.frequency = frequency
        self.tasks = []
        self.stop_event = asyncio.Event()

    async def generate_message(self, gpu_id:int):
        try:
            async with aiohttp.ClientSession() as session:
                while not self.stop_event.is_set():
                    batch = Batch(
                        gpu_id=gpu_id,
                        ker_temp=random.uniform(30.0, 90.0),
                        ker_load=random.uniform(0.0, 100.0),
                        mem_temp=random.uniform(30.0, 95.0),
                        mem_load=random.uniform(0.0, 100.0),
                        health_status=random.choice([
                            HealthStatus.OK,
                            HealthStatus.WARNING,
                            HealthStatus.CRITICAL
                        ]),
                        timestamp=str(time.time())
                    )

                    logging.info(
                        f"Отправляем данные. "
                        f"ID: {batch.gpu_id}, "
                        f"ker_temp: {batch.ker_temp:.2f}, "
                        f"ker_load: {batch.ker_load:.2f}, "
                        f"mem_temp: {batch.mem_temp:.2f}, "
                        f"mem_load: {batch.mem_load:.2f}, "
                        f"health_status: {batch.health_status}, "
                        f"timestamp: {batch.timestamp}"
                    )
                    start_time = time.time()

                    try:
                        async with session.post(url, data=batch.SerializeToString()) as response:
                            logging.info("Попытка отправить пакет.")
                            duration = time.time() - start_time
                            REQUEST_DURATION.labels(gpu_id=gpu_id).set(duration)
                            if response.status == 200:
                                logging.info(f"Ответ от IOT контроллера: {await response.text()}")
                                REQUESTS_TOTAL.labels(status="success").inc()
                            else:
                                error_text = await response.text()
                                logging.error(f"Ошибка при отправке. Статус: {response.status}, тело ошибки: {error_text}")
                    except Exception as ex:
                        logging.error(f"Ошибка при отправке данных. {ex}")
                        REQUESTS_FAILED.labels(gpu_id=gpu_id).inc()
                    logging.info(f"Async sleep на {1 / self.frequency} секунд.")
                    await asyncio.sleep(1 / self.frequency)
        except Exception as ex:
            logging.error(f"Возникла ошибка при формировании async task для видеокарты {gpu_id}: {ex}")
        finally:
            logging.info(f"Async task остановлено для видеокарты {gpu_id}")

    def stop(self):
        self.stop_event.set()

    async def start(self):
        DEVICE_COUNT.set(self.num_devices)
        DEVICE_FREQ.set(self.frequency)
        for gpu_id in range(1, self.num_devices + 1):
            self.tasks.append(self.generate_message(gpu_id))

        await asyncio.gather(*self.tasks)


def main():
    num_devices = 1
    frequency = 1
    generator = DataSimulator(num_devices, frequency)

    start_http_server(8070)
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, generator.stop)
    loop.add_signal_handler(signal.SIGINT, generator.stop)

    try:
        loop.run_until_complete(generator.start())
    finally:
        loop.close()

if __name__ == "__main__":
    main()

