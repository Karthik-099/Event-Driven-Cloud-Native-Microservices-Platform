import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def send_notification(event_type: str, data: dict):
        logger.info(f"Sending {event_type} notification: {data}")
        
        if event_type == "order_processed":
            NotificationService._send_order_notification(data)
        elif event_type == "inventory_reserved":
            NotificationService._send_inventory_notification(data)
    
    @staticmethod
    def _send_order_notification(data: dict):
        order_id = data.get('order_id')
        status = data.get('status')
        logger.info(f"EMAIL: Order {order_id} has been {status}")
    
    @staticmethod
    def _send_inventory_notification(data: dict):
        order_id = data.get('order_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        logger.info(f"EMAIL: Inventory reserved for order {order_id}: {quantity} units of {product_id}")
