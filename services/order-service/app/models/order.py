from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    customer_id = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
