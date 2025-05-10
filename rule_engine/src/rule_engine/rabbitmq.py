from proto.messages_pb2 import Batch, GpuInfo
from google.protobuf.json_format import MessageToDict
import time
import aiormq, asyncio
from .database import instant, ongoing, db
from .prometheus import  INSTANT_RULES_COUNTER, ONGOING_RULES_COUNTER
import logging

async def connect_to_rabbitmq():
    while True:
        try:
            connection = await aiormq.connect("amqp://pavel:popov@rabbitmq/")
            channel = await connection.channel(publisher_confirms=False)
            await channel.basic_consume('batch_queue', on_message)
            logging.info("Подключён к брокеру.")
            return connection, channel
        except aiormq.AMQPConnectionError as e:
            logging.error(f"Ошибка при подключении: {e}. Попробуем снова через 1 секунду.")
            await asyncio.sleep(2)

async def on_message(message: aiormq.abc.DeliveredMessage):
    try:
        batch = Batch()
        batch.ParseFromString(message.body)

        message_data = {
            "gpu_info": MessageToDict(batch.gpu_info,
                                      preserving_proto_field_name=True),
            "ker_temp": batch.ker_temp,
            "ker_load": batch.ker_load,
            "mem_temp": batch.mem_temp,
            "mem_load": batch.mem_load,
            "timestamp": batch.timestamp
        }

        logging.info(f"Принято сообщение {message_data}")

        if batch.ker_temp >= batch.gpu_info.max_ker_temp:
            logging.info(f"Превышена максимальная температура ядра у видеокарты: {batch.gpu_info.gpu_id}!")
            INSTANT_RULES_COUNTER.inc()
            await instant.insert_one({
                "gpu_info": MessageToDict(batch.gpu_info,
                                          preserving_proto_field_name=True),
                "ker_temp": batch.ker_temp,
                "alert_message": f"Превышена максимальная температура ядра у видеокарты: {batch.gpu_info.gpu_id}!",
                "timestamp": batch.timestamp
            })

        current_id_stack = ongoing[f"{batch.gpu_info.gpu_id}_stack"]
        await current_id_stack.insert_one(message_data)

        pipeline = [
            {"$match": {"gpu_info.gpu_id": batch.gpu_info.gpu_id,
                        "mem_temp": {"$gte": batch.gpu_info.max_mem_temp}}},
            {"$count": "total_count"}
        ]
        result = await current_id_stack.aggregate(pipeline).to_list(length=None)

        if result:
            total_count = result[0]['total_count']
            if total_count >= 5:
                ONGOING_RULES_COUNTER.inc()
                logging.info(f"Температура памяти видеокарты {batch.gpu_info.gpu_id} превышает максимальную"
                             f" 5 раз из 10 последних сообщений!")
                await ongoing.insert_one({
                    "gpu_info": MessageToDict(batch.gpu_info,
                                              preserving_proto_field_name=True),
                    "alert_message": f"Температура памяти видеокарты {batch.gpu_info.gpu_id} превышает максимальную"
                                     f" 5 раз из 10 последних сообщений!",
                    "timestamp": str(time.time())
                })

                await db.drop_collection(current_id_stack)

            if await current_id_stack.count_documents({}) >= 10:
                await db.drop_collection(current_id_stack)

        logging.info(f"Сообщение добавлено в коллекцию data: {message_data}.")
        await message.channel.basic_ack(message.delivery_tag)

    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}.")
        await message.channel.basic_nack(message.delivery_tag)
