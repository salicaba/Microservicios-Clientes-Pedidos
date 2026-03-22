import pika
import json
import os
import threading
import logging
from typing import Callable
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClienteEventConsumer:
    def __init__(self, callback: Callable):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://admin:admin123@rabbitmq:5672/")
        self.callback = callback
        self.connection = None
        self.channel = None
        self.consumer_thread = None
        self.running = False
    
    def _connect(self):
        try:
            logger.info(f"Conectando a RabbitMQ en {self.rabbitmq_url}")
            params = pika.URLParameters(self.rabbitmq_url)
            # Aumentar timeout de conexión
            params.connection_attempts = 10
            params.retry_delay = 5
            
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='clientes_eventos', durable=True)
            logger.info("Consumer conectado a RabbitMQ exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error en consumer al conectar: {e}")
            return False
    
    def _callback(self, ch, method, properties, body):
        try:
            event = json.loads(body)
            logger.info(f"Evento recibido: {event}")
            self.callback(event)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Error procesando evento: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)
    
    def start(self):
        if self.running:
            return
        
        # Intentar conectar con reintentos
        max_retries = 5
        for attempt in range(max_retries):
            if self._connect():
                break
            logger.warning(f"Reintentando conexión a RabbitMQ ({attempt + 1}/{max_retries})...")
            time.sleep(5)
        
        if not self.channel:
            logger.error("No se pudo conectar a RabbitMQ después de varios intentos")
            return
        
        self.running = True
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='clientes_eventos',
            on_message_callback=self._callback
        )
        
        def consume():
            logger.info("Iniciando consumo de eventos...")
            try:
                self.channel.start_consuming()
            except Exception as e:
                logger.error(f"Error en consumo: {e}")
            finally:
                self.running = False
        
        self.consumer_thread = threading.Thread(target=consume, daemon=True)
        self.consumer_thread.start()
    
    def stop(self):
        self.running = False
        if self.channel and self.channel.is_open:
            try:
                self.channel.stop_consuming()
            except:
                pass
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
            except:
                pass