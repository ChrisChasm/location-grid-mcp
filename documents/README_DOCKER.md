# Location Grid MCP Server - Docker Deployment

## 🐳 **Docker Setup Complete**

This repository now includes a complete Docker setup for the Location Grid MCP Server, making it easy to deploy and run in any containerized environment.

## 📁 **Docker Files Created**

### **Core Docker Files:**
- **`Dockerfile`** - Main Docker image definition
- **`docker-compose.yml`** - Multi-service Docker Compose setup
- **`requirements-docker.txt`** - Docker-specific dependencies

### **Docker Scripts:**
- **`docker-build.sh`** - Build the Docker image
- **`docker-run.sh`** - Run the container
- **`docker-test.sh`** - Test the Docker setup

## 🚀 **Quick Start**

### **1. Build the Docker Image**
```bash
./docker-build.sh
```

### **2. Test the Setup**
```bash
./docker-test.sh
```

### **3. Run the Server**
```bash
./docker-run.sh
```

## 📋 **Detailed Usage**

### **Building the Image**
```bash
# Build the Docker image
docker build -t location-grid-mcp:latest .

# Or use the script
./docker-build.sh
```

### **Running with Docker Compose (Recommended)**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f location-grid-mcp

# Stop services
docker-compose down
```

### **Running with Docker Directly**
```bash
# Run the container
docker run -it --rm \
    --name location-grid-mcp-server \
    -v "$(pwd)/db:/app/db" \
    -v "$(pwd)/logs:/app/logs" \
    location-grid-mcp:latest
```

## 🏗️ **Docker Architecture**

### **Services:**
1. **`location-grid-mcp`** - Main MCP server container
2. **`db-backup`** - Optional database backup service

### **Volumes:**
- **`./db:/app/db`** - Database persistence
- **`./logs:/app/logs`** - Log files
- **`./backups:/app/backups`** - Database backups

### **Health Checks:**
- Container health check every 30 seconds
- Automatic restart on failure
- Database backup every hour

## 🔧 **Configuration**

### **Environment Variables:**
```bash
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### **Ports:**
- **8000** - Exposed for health checks (if needed)

### **Volumes:**
```yaml
volumes:
  - ./db:/app/db          # Database persistence
  - ./logs:/app/logs      # Log files
```

## 🧪 **Testing**

### **Automated Testing:**
```bash
./docker-test.sh
```

This script will:
1. ✅ Check if Docker is running
2. ✅ Verify the image exists
3. ✅ Test container startup
4. ✅ Test MCP server functionality
5. ✅ Clean up test containers

### **Manual Testing:**
```bash
# Test the geocoder inside the container
docker exec location-grid-mcp-server python -c "
from geocoder import SimpleGeocoder
geocoder = SimpleGeocoder()
result = geocoder.geocode_address('New York City')
print(result)
"
```

## 📊 **Monitoring**

### **Container Status:**
```bash
# Check running containers
docker ps

# Check container logs
docker logs location-grid-mcp-server

# Check health status
docker inspect location-grid-mcp-server | grep Health
```

### **Docker Compose Status:**
```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs -f

# Check specific service logs
docker-compose logs -f location-grid-mcp
```

## 🔄 **Backup & Recovery**

### **Automatic Backups:**
The `db-backup` service automatically creates hourly backups:
- **Location**: `./backups/`
- **Format**: `location_grid_YYYYMMDD_HHMMSS.db`
- **Frequency**: Every hour

### **Manual Backup:**
```bash
# Create manual backup
docker exec location-grid-mcp-server cp /app/db/location_grid.db /app/backups/manual_backup.db
```

### **Restore from Backup:**
```bash
# Stop the service
docker-compose down

# Restore database
cp ./backups/location_grid_20240101_120000.db ./db/location_grid.db

# Start the service
docker-compose up -d
```

## 🛠️ **Development**

### **Development Mode:**
```bash
# Run with volume mounts for development
docker run -it --rm \
    --name location-grid-mcp-dev \
    -v "$(pwd):/app" \
    -w /app \
    python:3.11-slim \
    bash
```

### **Debugging:**
```bash
# Access container shell
docker exec -it location-grid-mcp-server bash

# View real-time logs
docker logs -f location-grid-mcp-server

# Check container resources
docker stats location-grid-mcp-server
```

## 🚀 **Production Deployment**

### **Production Considerations:**
1. **Resource Limits**: Set memory and CPU limits
2. **Security**: Use non-root user
3. **Networking**: Configure proper network access
4. **Monitoring**: Set up logging and monitoring
5. **Backups**: Ensure regular database backups

### **Production Docker Compose:**
```yaml
version: '3.8'
services:
  location-grid-mcp:
    build: .
    container_name: location-grid-mcp-prod
    restart: always
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
    environment:
      - PYTHONPATH=/app
      - PYTHONUNBUFFERED=1
    volumes:
      - ./db:/app/db
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "python", "-c", "import simple_mcp_server"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 📝 **Troubleshooting**

### **Common Issues:**

1. **Container won't start:**
   ```bash
   docker logs location-grid-mcp-server
   ```

2. **Database issues:**
   ```bash
   # Check database file
   ls -la db/
   
   # Test database connection
   docker exec location-grid-mcp-server sqlite3 /app/db/location_grid.db ".tables"
   ```

3. **Permission issues:**
   ```bash
   # Fix volume permissions
   sudo chown -R $USER:$USER db/ logs/
   ```

### **Debug Commands:**
```bash
# Check container status
docker ps -a

# View container logs
docker logs location-grid-mcp-server

# Access container shell
docker exec -it location-grid-mcp-server bash

# Check container resources
docker stats location-grid-mcp-server
```

## 🎯 **Next Steps**

1. **Deploy to Production**: Use the production Docker Compose configuration
2. **Set up Monitoring**: Add monitoring and alerting
3. **Configure Backups**: Set up automated backup retention
4. **Scale**: Consider horizontal scaling if needed

The Docker setup is now complete and ready for deployment! 🚀
