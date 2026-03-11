from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.services.consumer import start_consumer
from app.core.logging import setup_logging
import threading

setup_logging()

app = FastAPI(title="Notification Service", version="1.0.0")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.on_event("startup")
async def startup_event():
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "notification-service"}
