from kafka import KafkaProducer
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class KafkaService:
    def __init__(self):
        self.producer = None
        
    def get_producer(self):
        if not self.producer:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
            except Exception as e:
                logger.error(f"Failed to create Kafka producer: {str(e)}")
        return self.producer
    
    def publish_event(self, topic: str, event: dict):
        try:
            producer = self.get_producer()
            if producer:
                producer.send(topic, event)
                producer.flush()
                logger.info(f"Published event to {topic}: {event}")
        except Exception as e:
            logger.error(f"Failed to publish event: {str(e)}")

kafka_service = KafkaService()
