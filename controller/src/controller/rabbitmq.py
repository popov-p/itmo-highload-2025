import pika, time
import logging

def create_connection():
    while True:
        try:
            credentials = pika.PlainCredentials('pavel', 'popov')
            parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
            new_connection = pika.BlockingConnection(parameters)
            logging.info("Подключён к брокеру.")
            return new_connection
        except pika.exceptions.AMQPConnectionError as e:
            logging.info(f"Ошибка при подключении: {e}. Попробуем снова через 1 секунду.")
            time.sleep(2)

rabbitmq_connection = create_connection() #rabbitmq


