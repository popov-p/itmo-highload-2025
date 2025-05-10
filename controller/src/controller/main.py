from fastapi import FastAPI
from .routes import router
import logging
# from .report import metrics_reporter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('/var/log/controller.log', mode='a')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

app = FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     print("Запуск фоновой корутины для формирования отчёта.")
#     metrics_reporter.connect_to_redis()
#     await metrics_reporter.start_background_tasks()

app.include_router(router)
