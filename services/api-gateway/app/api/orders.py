from fastapi import APIRouter, HTTPException
import httpx
import logging
from app.schemas.order import OrderCreate, OrderResponse
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.ORDER_SERVICE_URL}/orders",
                json=order.dict(),
                timeout=10.0
            )
            response.raise_for_status()
            logger.info(f"Order created: {response.json()}")
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create order")

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.ORDER_SERVICE_URL}/orders/{order_id}",
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Order not found")
        raise HTTPException(status_code=500, detail="Failed to fetch order")
