#!/bin/bash

# Docker Compose Setup
# Run the Voice Bot with Docker

echo "🐳 Starting Voice Bot with Docker..."

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    exit 1
fi

echo "✅ Docker Compose found"
echo "📦 Building and starting services..."

docker-compose up -d

echo "✅ Services started!"
echo "🌐 Access dashboard at: http://localhost:5000"
echo ""
echo "📋 Useful commands:"
echo "- View logs: docker-compose logs -f app"
echo "- Stop services: docker-compose down"
echo "- Restart services: docker-compose restart"
