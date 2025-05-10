from proto.messages_pb2 import Batch, GpuInfo
import asyncio
import aiohttp
import signal
import logging
import time
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('/var/log/datasim.log', mode='a')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# url = "http://nginx/incoming-data"
url = "http://controller:8060/incoming-data"

registered_gpus = {}

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

                    if gpu_id not in registered_gpus:
                        gpu_info = GpuInfo(
                            gpu_id=gpu_id,
                            model=random.choice(["RTX 3090", "A100", "RTX 4080", "TITAN V"]),
                            max_ker_temp=int(random.uniform(90.0, 100.0)),
                            max_mem_temp=int(random.uniform(110.0, 120.0)),
                        )
                        registered_gpus[gpu_id] = gpu_info
                    else:
                        gpu_info = registered_gpus[gpu_id]

                    batch = Batch(
                        gpu_info=gpu_info,
                        ker_temp=random.uniform(30.0, 110.0),
                        ker_load=random.uniform(0.0, 100.0),
                        mem_temp=random.uniform(30.0, 170.0),
                        mem_load=random.uniform(0.0, 100.0),
                        timestamp=str(time.time()),
                    )

                    logging.info(
                        f"Отправляем данные. "
                        f"gpu_info: {batch.gpu_info}"
                        f"ker_temp: {batch.ker_temp:.2f}, "
                        f"ker_load: {batch.ker_load:.2f}, "
                        f"mem_temp: {batch.mem_temp:.2f}, "
                        f"mem_load: {batch.mem_load:.2f}, "
                        f"timestamp: {batch.timestamp}"
                    )

                    try:
                        async with session.post(url, data=batch.SerializeToString()) as response:
                            if response.status == 200:
                                logging.info(f"Ответ от IOT контроллера: {await response.text()}")
                            else:
                                error_text = await response.text()
                                logging.error(f"Ошибка при отправке. Статус: {response.status}, тело ошибки: {error_text}")
                    except Exception as ex:
                        logging.error(f"Ошибка при отправке данных. {ex}")
                    logging.info(f"Async sleep на {1 / self.frequency} секунд.")
                    await asyncio.sleep(1 / self.frequency)
        except Exception as ex:
            logging.error(f"Возникла ошибка при формировании async task для видеокарты {gpu_id}: {ex}")
        finally:
            logging.info(f"Async task остановлено для видеокарты {gpu_id}")

    def stop(self):
        self.stop_event.set()

    async def start(self):
        for gpu_id in range(1, self.num_devices + 1):
            self.tasks.append(self.generate_message(gpu_id))

        await asyncio.gather(*self.tasks)


def main():
    num_devices = 1
    frequency = 0.5
    generator = DataSimulator(num_devices, frequency)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, generator.stop)
    loop.add_signal_handler(signal.SIGINT, generator.stop)

    try:
        loop.run_until_complete(generator.start())
    finally:
        loop.close()

if __name__ == "__main__":
    main()

