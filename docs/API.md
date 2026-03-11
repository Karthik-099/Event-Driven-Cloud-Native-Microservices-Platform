# API Documentation

## Overview

This document describes the REST API endpoints for the Event-Driven Microservices Platform.

## Base URL

- Local: `http://localhost:8000`
- Production: `https://api.microservices.example.com`

## Authentication

Currently, the API does not require authentication. In production, implement OAuth2/JWT.

## Endpoints

### Health Check

Check service health status.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "api-gateway"
}
```

### Create Order

Create a new order.

**Endpoint**: `POST /api/v1/orders`

**Request Body**:
```json
{
  "product_id": "prod-123",
  "quantity": 2,
  "customer_id": "cust-456"
}
```

**Response**: `200 OK`
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "product_id": "prod-123",
  "quantity": 2,
  "customer_id": "cust-456",
  "status": "pending"
}
```

**Error Response**: `500 Internal Server Error`
```json
{
  "detail": "Failed to create order"
}
```

### Get Order

Retrieve order details by ID.

**Endpoint**: `GET /api/v1/orders/{order_id}`

**Path Parameters**:
- `order_id` (string, required): UUID of the order

**Response**: `200 OK`
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "product_id": "prod-123",
  "quantity": 2,
  "customer_id": "cust-456",
  "status": "pending"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Order not found"
}
```

## Event Topics

### orders.created

Published when a new order is created.

**Schema**:
```json
{
  "order_id": "string",
  "product_id": "string",
  "quantity": "integer",
  "customer_id": "string"
}
```

### orders.processed

Published when order processing completes.

**Schema**:
```json
{
  "order_id": "string",
  "status": "string"
}
```

### inventory.reserved

Published when inventory is reserved for an order.

**Schema**:
```json
{
  "order_id": "string",
  "product_id": "string",
  "quantity": "integer",
  "status": "reserved"
}
```

## Rate Limiting

Currently not implemented. Recommended: 100 requests per minute per IP.

## Error Codes

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Examples

### cURL Examples

Create order:
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id":"prod-123","quantity":2,"customer_id":"cust-456"}'
```

Get order:
```bash
curl http://localhost:8000/api/v1/orders/550e8400-e29b-41d4-a716-446655440000
```

### Python Example

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/orders",
    json={
        "product_id": "prod-123",
        "quantity": 2,
        "customer_id": "cust-456"
    }
)
order = response.json()
print(f"Order created: {order['order_id']}")
```
