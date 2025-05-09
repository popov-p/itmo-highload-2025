import logging

from ..proto.messages_pb2 import Batch, HealthStatus
# from .rabbitmq import gpu_channels, create_channel_for_device, rabbitmq_connection
from fastapi import Request, Response, HTTPException, APIRouter
from .database import db
# from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
# from .prometheus import REQUESTS, BATCHES_ACCEPTED, BATCHES_DECLINED
# from  .report import metrics_reporter, r, controller_port
import json



router = APIRouter()

# @router.get("/metrics")
# def metrics():
#     # REQUESTS.inc()
#     return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@router.post("/incoming-data")
async def incoming_data(request: Request):
    try:
        logging.info("Принято хоть что-то!")
        # REQUESTS.inc()
        body = await request.body()
        batch = Batch()
        batch.ParseFromString(body)
        print(f"Получен пакет: {batch}")
        #
        # # metrics_reporter.add_fields_data(batch.ker_load, batch.mem_load)
        #
        # if batch.health_status == HealthStatus.CRITICAL:
        #     # BATCHES_DECLINED.inc()
        #     # metrics_reporter.increment_declined_requests()
        #     # raise HTTPException(501,"Не принято! Ожидается alpha >= 25")
        #     pass
        #
        # if batch.gpu_id not in gpu_channels:
        #     # metrics_reporter.increment_accepted_requests()
        #     # BATCHES_ACCEPTED.inc()
        #     logging.info("Канала нет, создаем новый.")
        #     print("Канала нет, создаем новый.")
        #     rabbitmq_channel = create_channel_for_device(rabbitmq_connection, batch.gpu_id)
        # else:
        #     # metrics_reporter.increment_accepted_requests()
        #     # BATCHES_ACCEPTED.inc()
        #     logging.info("Используем существующий канал.")
        #     print("Используем существующий канал.")
        #     rabbitmq_channel = gpu_channels[batch.gpu_id]
        # rabbitmq_channel.basic_publish(
        #     exchange='',
        #     routing_key='critical_devices_queue',
        #     body=body
        # )
        #
        # data = {
        #     "gpu_id": batch.gpu_id,
        #     "ker_temp": batch.ker_temp,
        #     "ker_load": batch.ker_load,
        #     "mem_temp": batch.mem_temp,
        #     "mem_load": batch.mem_load,
        #     "health_status": batch.health_status,
        #     "timestamp": batch.timestamp
        # }
        #
        # result = await db.data.insert_one(data)
        #
        # return Response(f"Принято. ID отправителя: {batch.gpu_id}, ID объекта в коллекции: {result.inserted_id}")
        return Response(status_code=200, content="Ok")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500,f"Ошибка: {str(e)}")


# @router.get("/report", response_model=dict)
# async def cached_report():
#     report_key = f"report-{controller_port}"
#
#     report_data = r.get(report_key)
#
#     if report_data:
#         return json.loads(report_data.decode())
#     else:
#         raise HTTPException(status_code=404, detail=f"Report for controller at port {controller_port} not found")

