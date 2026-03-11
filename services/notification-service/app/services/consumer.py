from kafka import KafkaConsumer
import json
import logging
from app.core.config import settings
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

def start_consumer():
    try:
        consumer = KafkaConsumer(
            'orders.processed',
            'inventory.reserved',
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='notification-service-group',
            auto_offset_reset='earliest'
        )
        
        logger.info("Notification consumer started")
        
        for message in consumer:
            event = message.value
            topic = message.topic
            
            logger.info(f"Received event from {topic}: {event}")
            
            if topic == 'orders.processed':
                NotificationService.send_notification('order_processed', event)
            elif topic == 'inventory.reserved':
                NotificationService.send_notification('inventory_reserved', event)
                
    except Exception as e:
        logger.error(f"Consumer error: {str(e)}")
