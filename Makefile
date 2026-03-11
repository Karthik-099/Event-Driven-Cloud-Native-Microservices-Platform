.PHONY: help setup test lint format build run deploy clean

help:
	@echo "Available commands:"
	@echo "  make setup    - Set up development environment"
	@echo "  make test     - Run all tests"
	@echo "  make lint     - Run linting"
	@echo "  make format   - Format code with black"
	@echo "  make build    - Build Docker images"
	@echo "  make run      - Run services locally"
	@echo "  make deploy   - Deploy to Kubernetes"
	@echo "  make clean    - Clean up containers and volumes"

setup:
	./scripts/setup.sh

test:
	pytest services/*/tests/ -v

lint:
	flake8 services/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 services/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black services/

build:
	docker-compose build

run:
	./scripts/run_local.sh

deploy:
	./scripts/deploy.sh

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
