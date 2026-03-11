#!/bin/bash

set -e

echo "Deploying to Kubernetes..."

if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl"
    exit 1
fi

echo "Creating namespace..."
kubectl apply -f kubernetes/base/namespace.yaml

echo "Applying ConfigMaps..."
kubectl apply -f kubernetes/configmaps/

echo "Applying Secrets..."
kubectl apply -f kubernetes/secrets/

echo "Deploying infrastructure services..."
kubectl apply -f kubernetes/deployments/postgres.yaml
kubectl apply -f kubernetes/deployments/redis.yaml
kubectl apply -f kubernetes/deployments/kafka.yaml

echo "Waiting for infrastructure to be ready..."
sleep 30

echo "Deploying microservices..."
kubectl apply -f kubernetes/deployments/order-service.yaml
kubectl apply -f kubernetes/deployments/inventory-service.yaml
kubectl apply -f kubernetes/deployments/notification-service.yaml
kubectl apply -f kubernetes/deployments/api-gateway.yaml

echo "Applying services..."
kubectl apply -f kubernetes/services/

echo "Deploying observability stack..."
kubectl apply -f kubernetes/deployments/prometheus.yaml
kubectl apply -f kubernetes/deployments/grafana.yaml

echo "Applying ingress..."
kubectl apply -f kubernetes/ingress/

echo ""
echo "Deployment complete!"
echo ""
echo "To check status, run:"
echo "  kubectl get pods -n microservices"
echo ""
echo "To get API Gateway URL, run:"
echo "  kubectl get svc api-gateway -n microservices"
