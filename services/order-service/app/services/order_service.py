from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate
from app.services.kafka_service import kafka_service
import uuid
import logging

logger = logging.getLogger(__name__)

class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate):
        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            customer_id=order_data.customer_id,
            status="pending"
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        
        event = {
            "order_id": order_id,
            "product_id": order_data.product_id,
            "quantity": order_data.quantity,
            "customer_id": order_data.customer_id
        }
        kafka_service.publish_event("orders.created", event)
        
        logger.info(f"Order created: {order_id}")
        return order
    
    @staticmethod
    def get_order(db: Session, order_id: str):
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def update_order_status(db: Session, order_id: str, status: str):
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            db.commit()
            
            event = {
                "order_id": order_id,
                "status": status
            }
            kafka_service.publish_event("orders.processed", event)
            logger.info(f"Order {order_id} status updated to {status}")
        return order
