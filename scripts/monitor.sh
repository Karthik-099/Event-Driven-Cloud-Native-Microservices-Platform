#!/bin/bash

set -e

echo "Monitoring Microservices Platform..."
echo ""

if command -v kubectl &> /dev/null; then
    echo "=== Kubernetes Cluster Status ==="
    kubectl get nodes
    echo ""
    
    echo "=== Microservices Pods ==="
    kubectl get pods -n microservices
    echo ""
    
    echo "=== Services ==="
    kubectl get svc -n microservices
    echo ""
    
    echo "=== Resource Usage ==="
    kubectl top pods -n microservices 2>/dev/null || echo "Metrics server not available"
    echo ""
fi

if command -v docker-compose &> /dev/null; then
    echo "=== Docker Compose Services ==="
    docker-compose ps
    echo ""
fi

echo "=== Service Health Checks ==="
for port in 8000 8001 8002 8003; do
    if curl -s http://localhost:$port/health > /dev/null 2>&1; then
        echo "✓ Service on port $port is healthy"
    else
        echo "✗ Service on port $port is not responding"
    fi
done
