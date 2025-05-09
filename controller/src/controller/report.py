import redis
import asyncio
from statistics import mean
import logging
import json
import os

# controller_port = os.getenv("CONTROLLER_PORT_FIRST") or os.getenv("CONTROLLER_PORT_SECOND") or "UNDEFINED"

logger = logging.getLogger()

# r = redis.Redis(host='redis', port=6379, db=0)
#
# class RedisMetricsReporter:
#     def __init__(self, host='redis', port=6379, db=0):
#         print("RedisMetricsReporter __init__(...)")
#         self.r = redis.Redis(host=host, port=port, db=db)
#         self.total_requests_by_segment = 0
#         self.accepted_requests_by_segment = 0
#         self.declined_requests_by_segment = 0
#         self.segment_ker_load_values = []
#         self.segment_mem_load_values = []
#
#     def connect_to_redis(self):
#         try:
#             response = self.r.ping()
#             if response:
#                 print("Подключение к Redis успешно!")
#             else:
#                 print("Ошибка подключения к Redis.")
#         except Exception as e:
#             print(f"Ошибка подключения к Redis: {e}")
#
#     async def send_metrics_to_redis(self):
#         while True:
#             await asyncio.sleep(30)
#             if self.segment_ker_load_values and self.segment_mem_load_values:
#                 avg_ker_load = mean(self.segment_ker_load_values)
#                 avg_mem_load = mean(self.segment_mem_load_values)
#             else:
#                 avg_ker_load = avg_mem_load = 0
#
#             report_data = {
#                 "accepted_segment_requests": self.accepted_requests_by_segment,
#                 "declined_segment_requests": self.declined_requests_by_segment,
#                 "avg_segment_ker_load": avg_ker_load,
#                 "avg_segment_mem_load": avg_mem_load
#             }
#
#             self.r.set(f"report-{controller_port}", json.dumps(report_data))
#
#             print(f"Отчет в Redis обновлен: {report_data}")
#
#             self.reset_metrics()
#
#     async def start_background_tasks(self):
#         asyncio.create_task(self.send_metrics_to_redis())
#
#     def increment_accepted_requests(self):
#         self.accepted_requests_by_segment += 1
#
#     def increment_declined_requests(self):
#         self.declined_requests_by_segment += 1
#
#     def add_fields_data(self, ker_load, mem_load):
#         self.segment_ker_load_values.append(ker_load)
#         self.segment_mem_load_values.append(mem_load)
#
#     def reset_metrics(self):
#         self.segment_ker_load_values = []
#         self.segment_mem_load_values = []
#         self.total_requests_by_segment = 0
#         self.accepted_requests_by_segment = 0
#         self.declined_requests_by_segment = 0
#         print("Данные сброшены. Кэш-метрики очищены.")
#
#
# metrics_reporter = RedisMetricsReporter()


