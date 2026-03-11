# Deployment Guide

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- kubectl installed
- Terraform installed
- Docker installed

## Step-by-Step Deployment

### 1. Provision Infrastructure

```bash
cd infrastructure/terraform/environments/dev
terraform init
terraform plan
terraform apply
```

### 2. Configure kubectl

```bash
aws eks update-kubeconfig --name microservices-cluster --region us-east-1
```

### 3. Verify Cluster

```bash
kubectl get nodes
kubectl cluster-info
```

### 4. Build Docker Images

```bash
docker build -t api-gateway:latest ./services/api-gateway
docker build -t order-service:latest ./services/order-service
docker build -t inventory-service:latest ./services/inventory-service
docker build -t notification-service:latest ./services/notification-service
```

### 5. Push to ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag api-gateway:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/api-gateway:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/api-gateway:latest
```

### 6. Deploy to Kubernetes

```bash
./scripts/deploy.sh
```

### 7. Verify Deployment

```bash
kubectl get pods -n microservices
kubectl get svc -n microservices
```

### 8. Access Services

```bash
kubectl get svc api-gateway -n microservices
```

## Rollback

```bash
kubectl rollout undo deployment/api-gateway -n microservices
```

## Cleanup

```bash
kubectl delete namespace microservices
cd infrastructure/terraform/environments/dev
terraform destroy
```
