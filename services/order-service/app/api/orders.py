from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService

router = APIRouter()

@router.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_obj = OrderService.create_order(db, order)
    return OrderResponse(
        order_id=order_obj.id,
        product_id=order_obj.product_id,
        quantity=order_obj.quantity,
        customer_id=order_obj.customer_id,
        status=order_obj.status
    )

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse(
        order_id=order.id,
        product_id=order.product_id,
        quantity=order.quantity,
        customer_id=order.customer_id,
        status=order.status
    )
