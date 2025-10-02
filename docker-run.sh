#!/bin/bash
# Docker run script for Location Grid MCP Server

set -e

echo "🚀 Starting Location Grid MCP Server..."

# Create necessary directories
mkdir -p logs backups

# Run with docker-compose (recommended)
if command -v docker-compose &> /dev/null; then
    echo "📦 Using docker-compose..."
    docker-compose up -d
    
    echo "✅ Services started!"
    echo ""
    echo "📊 Container status:"
    docker-compose ps
    
    echo ""
    echo "📝 View logs:"
    echo "   docker-compose logs -f location-grid-mcp"
    echo ""
    echo "🛑 Stop services:"
    echo "   docker-compose down"
    
else
    echo "🐳 Using direct Docker run..."
    docker run -it --rm \
        --name location-grid-mcp-server \
        -v "$(pwd)/db:/app/db" \
        -v "$(pwd)/logs:/app/logs" \
        location-grid-mcp:latest
fi
