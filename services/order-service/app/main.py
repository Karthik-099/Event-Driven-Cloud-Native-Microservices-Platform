from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.api import orders
from app.core.database import engine, Base
from app.core.logging import setup_logging

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", version="1.0.0")

app.include_router(orders.router)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "order-service"}
