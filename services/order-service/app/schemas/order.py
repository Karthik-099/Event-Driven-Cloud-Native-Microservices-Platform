from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    product_id: str
    quantity: int
    customer_id: str

class OrderResponse(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    customer_id: str
    status: str
    
    class Config:
        from_attributes = True
