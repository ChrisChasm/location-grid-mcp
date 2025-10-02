#!/bin/bash
# Docker test script for Location Grid MCP Server

set -e

echo "🧪 Testing Location Grid MCP Server Docker Container..."

# Test if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Test if image exists
if ! docker images location-grid-mcp:latest &> /dev/null; then
    echo "❌ Docker image 'location-grid-mcp:latest' not found."
    echo "   Run './docker-build.sh' first to build the image."
    exit 1
fi

echo "✅ Docker is running"
echo "✅ Docker image exists"

# Test container startup
echo ""
echo "🔍 Testing container startup..."

# Run container in background for testing
CONTAINER_ID=$(docker run -d --rm \
    --name location-grid-mcp-test \
    -v "$(pwd)/db:/app/db" \
    location-grid-mcp:latest)

echo "📦 Container started with ID: $CONTAINER_ID"

# Wait a moment for startup
sleep 5

# Check if container is still running
if docker ps | grep -q location-grid-mcp-test; then
    echo "✅ Container is running successfully"
    
    # Test the MCP server functionality
    echo ""
    echo "🔍 Testing MCP server functionality..."
    
    # Run a simple test inside the container
    docker exec location-grid-mcp-test python -c "
import sys
sys.path.append('/app')
from geocoder import SimpleGeocoder
geocoder = SimpleGeocoder()
result = geocoder.geocode_address('New York City')
print('Test result:', result)
"
    
    echo "✅ MCP server functionality test passed"
    
else
    echo "❌ Container failed to start or crashed"
    echo "📝 Container logs:"
    docker logs location-grid-mcp-test
    exit 1
fi

# Clean up test container
echo ""
echo "🧹 Cleaning up test container..."
docker stop location-grid-mcp-test

echo "✅ Docker test completed successfully!"
echo ""
echo "🚀 Ready to deploy! Run './docker-run.sh' to start the server."
