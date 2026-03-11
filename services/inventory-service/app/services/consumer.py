from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from app.core.config import settings
from app.services.inventory_service import InventoryService

logger = logging.getLogger(__name__)

def start_consumer():
    try:
        consumer = KafkaConsumer(
            'orders.created',
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='inventory-service-group',
            auto_offset_reset='earliest'
        )
        
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        logger.info("Inventory consumer started")
        
        for message in consumer:
            event = message.value
            logger.info(f"Received order event: {event}")
            
            order_id = event.get('order_id')
            product_id = event.get('product_id')
            quantity = event.get('quantity')
            
            if InventoryService.reserve_inventory(product_id, quantity):
                inventory_event = {
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "status": "reserved"
                }
                producer.send('inventory.reserved', inventory_event)
                producer.flush()
                logger.info(f"Inventory reserved for order {order_id}")
            else:
                logger.warning(f"Insufficient inventory for order {order_id}")
                
    except Exception as e:
        logger.error(f"Consumer error: {str(e)}")
