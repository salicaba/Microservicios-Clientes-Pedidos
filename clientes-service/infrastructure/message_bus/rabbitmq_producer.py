import pika
import json
import os
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQProducer:
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://admin:admin123@localhost:5672/")
        self.connection = None
        self.channel = None
        self._connect()
    
    def _connect(self):
        try:
            params = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='clientes_eventos', durable=True)
            logger.info("Conectado a RabbitMQ")
        except Exception as e:
            logger.error(f"Error conectando a RabbitMQ: {e}")
    
    def publish_event(self, event_type: str, data: Dict):
        try:
            if not self.channel or not self.connection.is_open:
                self._connect()
            
            message = {
                'event_type': event_type,
                'data': data
            }
            
            self.channel.basic_publish(
                exchange='',
                routing_key='clientes_eventos',
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            logger.info(f"Evento publicado: {event_type}")
        except Exception as e:
            logger.error(f"Error publicando evento: {e}")
    
    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
