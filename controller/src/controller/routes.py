from ..proto.messages_pb2 import Batch, GpuInfo
from google.protobuf.json_format import MessageToDict
from .rabbitmq import gpu_channels, create_channel_for_device, rabbitmq_connection
from fastapi import Request, Response, HTTPException, APIRouter
from .database import db

import logging
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
        # REQUESTS.inc()
        body = await request.body()
        batch = Batch()
        batch.ParseFromString(body)
        logging.info(f"Получен пакет: {batch}")

        # # metrics_reporter.add_fields_data(batch.ker_load, batch.mem_load)

        if batch.gpu_info.gpu_id not in gpu_channels:
            # metrics_reporter.increment_accepted_requests()
            # BATCHES_ACCEPTED.inc()
            logging.info("Канала нет, создаем новый.")
            rabbitmq_channel = create_channel_for_device(rabbitmq_connection, batch.gpu_info.gpu_id)
        else:
            # metrics_reporter.increment_accepted_requests()
            # BATCHES_ACCEPTED.inc()
            logging.info("Используем существующий канал.")
            rabbitmq_channel = gpu_channels[batch.gpu_info.gpu_id]

        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key='batch_queue',
            body=body
        )

        #     # BATCHES_DECLINED.inc()
        #     # metrics_reporter.increment_declined_requests()
        #     # raise HTTPException(501,"Не принято! Ожидается alpha >= 25")
        #     pass

        data = {
            "gpu_info": MessageToDict(batch.gpu_info,
                                      preserving_proto_field_name=True),
            "ker_temp": batch.ker_temp,
            "ker_load": batch.ker_load,
            "mem_temp": batch.mem_temp,
            "mem_load": batch.mem_load,
            "timestamp": batch.timestamp
        }

        result = await db.data.insert_one(data)


        return Response(f"Принято. ID отправителя: {batch.gpu_info.gpu_id}, ID объекта в коллекции: {result.inserted_id}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Ошибка: {str(e)}")


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

