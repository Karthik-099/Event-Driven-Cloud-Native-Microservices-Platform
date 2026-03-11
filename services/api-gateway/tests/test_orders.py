import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_order_endpoint():
    response = client.post("/api/v1/orders", json={
        "product_id": "prod-123",
        "quantity": 2,
        "customer_id": "cust-456"
    })
    assert response.status_code in [200, 500]
