#!/bin/bash

set -e

echo "Setting up Event-Driven Microservices Platform..."

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose"
    exit 1
fi

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing development dependencies..."
pip install --upgrade pip
pip install pytest pytest-cov flake8 black

echo "Installing service dependencies..."
for service in services/*/; do
    if [ -f "$service/requirements.txt" ]; then
        echo "Installing dependencies for $service"
        pip install -r "$service/requirements.txt"
    fi
done

echo "Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the platform locally, run:"
echo "  ./scripts/run_local.sh"
