from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    product_id: str
    quantity: int
    customer_id: str

class OrderResponse(BaseModel):
    order_id: str
    status: str
    product_id: str
    quantity: int
    customer_id: str
