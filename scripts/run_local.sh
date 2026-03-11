#!/bin/bash

set -e

echo "Starting Event-Driven Microservices Platform locally..."

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose"
    exit 1
fi

echo "Building Docker images..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo "Waiting for services to be healthy..."
sleep 30

echo ""
echo "Services are starting up!"
echo ""
echo "API Gateway: http://localhost:8000"
echo "Order Service: http://localhost:8001"
echo "Inventory Service: http://localhost:8002"
echo "Notification Service: http://localhost:8003"
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "To view logs, run: docker-compose logs -f"
echo "To stop services, run: docker-compose down"
