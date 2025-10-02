#!/bin/bash
# Docker build script for Location Grid MCP Server

set -e

echo "🐳 Building Location Grid MCP Server Docker Image..."

# Build the Docker image
docker build -t location-grid-mcp:latest .

echo "✅ Docker image built successfully!"
echo "📦 Image name: location-grid-mcp:latest"

# Show image details
echo ""
echo "📋 Image details:"
docker images location-grid-mcp:latest

echo ""
echo "🚀 To run the container:"
echo "   docker run -it --rm location-grid-mcp:latest"
echo ""
echo "🔧 To run with docker-compose:"
echo "   docker-compose up -d"
