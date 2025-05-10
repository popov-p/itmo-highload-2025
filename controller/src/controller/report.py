import redis
import asyncio
from statistics import mean
import logging
import json
import socket
from google.protobuf.json_format import MessageToDict
from ..proto.messages_pb2 import GpuInfo, Batch
from statistics import mean

r = redis.Redis(host='redis', port=6379, db=0)
report_key = socket.gethostname()

class RedisMetricsReporter:
    def __init__(self, host='redis', port=6379, db=0):
        logging.info("RedisMetricsReporter __init__ call")
        self.r = redis.Redis(host=host, port=port, db=db)
        self.gpu_statistics = {}

    def connect_to_redis(self):
        try:
            response = self.r.ping()
            if response:
                logging.info("Подключение к Redis успешно!")
            else:
                logging.info("Ошибка подключения к Redis.")
        except Exception as e:
            logging.info(f"Ошибка подключения к Redis: {e}")

    async def send_metrics_to_redis(self):
        while True:
            await asyncio.sleep(7)

            detailed_report = {}

            for gpu_info, stats in self.gpu_statistics.items():
                avg_ker_temp = mean(stats["ker_temps"]) if stats["ker_temps"] else 0
                avg_mem_temp = mean(stats["mem_temps"]) if stats["mem_temps"] else 0
                avg_ker_load = mean(stats["ker_loads"]) if stats["ker_loads"] else 0
                avg_mem_load = mean(stats["mem_loads"]) if stats["mem_loads"] else 0

                detailed_report[gpu_info] = {
                    "avg_ker_temp": avg_ker_temp,
                    "avg_ker_load": avg_ker_load,
                    "avg_mem_temp": avg_mem_temp,
                    "avg_mem_load": avg_mem_load,
                    "ker_temps": stats["ker_temps"],
                    "ker_loads": stats["ker_loads"],
                    "mem_temps": stats["mem_temps"],
                    "mem_loads": stats["mem_loads"],
                }

            report_data = {
                "detailed_report": detailed_report
            }

            self.r.set(report_key, json.dumps(report_data))

            logging.info(f"Отчет в Redis обновлен: {report_data}")

            self.reset_metrics()

    async def start_background_tasks(self):
        asyncio.create_task(self.send_metrics_to_redis())

    def register_graphics_card(self, gpu_info: GpuInfo):
        logging.info(f"сюда мы дошли а дальше нет")
        gpu_info_key = json.dumps(MessageToDict(gpu_info,
                                                preserving_proto_field_name=True), sort_keys=True)
        if gpu_info_key not in self.gpu_statistics:
            logging.info(f"Зарегистрировано новое устройство {gpu_info_key}")
            self.gpu_statistics[gpu_info_key] = {
                "ker_temps": [],
                "ker_loads": [],
                "mem_temps": [],
                "mem_loads": [],
            }
        else:
            logging.info(f"Карта уже зарегистрирована.")

    def add_fields_data(self, batch: Batch):
        gpu_info_key = json.dumps(MessageToDict(batch.gpu_info,
                                                preserving_proto_field_name=True), sort_keys=True)
        self.gpu_statistics[gpu_info_key]["ker_temps"].append(batch.ker_temp)
        self.gpu_statistics[gpu_info_key]["ker_loads"].append(batch.ker_load)
        self.gpu_statistics[gpu_info_key]["mem_temps"].append(batch.mem_temp)
        self.gpu_statistics[gpu_info_key]["mem_loads"].append(batch.mem_load)

        logging.info("Добавлены данные для подсчёта средних значений в Redis")

        logging.info(self.gpu_statistics)

    def reset_metrics(self):
        self.gpu_statistics.clear()
        logging.info("Данные сброшены. Кэш-метрики очищены.")

metrics_reporter = RedisMetricsReporter()


