from proto.messages_pb2 import Batch
from google.protobuf.json_format import MessageToDict
from .rabbitmq import rabbitmq_connection
from .rabbitmq_utils import gpu_channels, create_channel_for_device
from fastapi import Request, Response, HTTPException
from .router import router
from .database import db
from  .report import metrics_reporter, r, report_key
import logging
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .prometheus import REQUESTS, CPU_USAGE, MEM_USAGE
import json
import psutil
import base64
import socket
import time

@router.get("/metrics")
def metrics():
    process = psutil.Process()

    cpu_usage = process.cpu_percent(interval=1)

    hostname = socket.gethostname()

    CPU_USAGE.labels(hostname=hostname).set(cpu_usage)
    logging.info(f"Использование CPU: {cpu_usage}, %")

    mem_usage_mb = process.memory_info().rss / (1024 * 1024)
    MEM_USAGE.labels(hostname=hostname).set(mem_usage_mb)
    logging.info(f"Памяти занято в МБ: {mem_usage_mb}")

    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@router.post("/incoming-data")
async def incoming_data(request: Request):
    try:
        hostname = socket.gethostname()
        print(f"Имя пода: {hostname}")
        REQUESTS.labels(hostname=hostname).inc()

        encoded_body = await request.body()
        body = base64.b64decode(encoded_body)

        if not body:
                raise HTTPException(status_code=500, detail="Request body is empty")

        batch = Batch()
        batch.ParseFromString(body)
        logging.info(f"Получен пакет: {batch}")

        if batch.gpu_info.gpu_id not in gpu_channels:
            logging.info("Канала нет, создаем новый.")
            rabbitmq_channel = create_channel_for_device(rabbitmq_connection, batch.gpu_info.gpu_id)
        else:
            logging.info("Используем существующий канал.")
            rabbitmq_channel = gpu_channels[batch.gpu_info.gpu_id]

        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key='batch_queue',
            body=body
        )

        metrics_reporter.register_graphics_card(batch.gpu_info)
        metrics_reporter.add_fields_data(batch)

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

        return Response(f"Принято. ID отправителя: {batch.gpu_info.gpu_id},"
                        f"ID объекта в коллекции: {result.inserted_id}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Ошибка: {str(e)}")

@router.get("/report", response_model=dict)
async def cached_report():
    report_data = r.get(report_key)

    if report_data:
        return json.loads(report_data.decode())
    else:
        raise HTTPException(status_code=404, detail=f"Report for controller {report_key} not found")

@router.get("/dbwise-report", response_model=dict)
async def cached_report():
    now = time.time()
    thirty_seconds_ago = now - 30

    print(f"Время запроса данных: {now}")
    cursor = db.data.find(
        {"ker_load": {"$gte": 0}},
        {
            "timestamp": 1,
            "ker_load": 1,
            "ker_temp": 1,
            "mem_temp": 1,
            "mem_load": 1,
            "gpu_info": 1,
            "_id": 0
        }
    )
    data = await cursor.to_list(length=None)

    recent_data = [
        doc for doc in data
        if float(doc.get("timestamp", "0")) > thirty_seconds_ago
    ]
    print(f"Современные данные: {recent_data}")
    if recent_data:
        return {"report": recent_data}
    else:
        raise HTTPException(status_code=404, detail="No recent data found in the last 30 seconds")

