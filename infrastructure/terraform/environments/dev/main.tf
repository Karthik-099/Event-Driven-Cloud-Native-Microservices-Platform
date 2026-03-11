terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "microservices-cluster"
}

module "vpc" {
  source       = "../../modules/vpc"
  cluster_name = var.cluster_name
}

module "eks" {
  source       = "../../modules/eks"
  cluster_name = var.cluster_name
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = concat(module.vpc.public_subnet_ids, module.vpc.private_subnet_ids)
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "cluster_name" {
  value = var.cluster_name
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
