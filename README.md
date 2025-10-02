# Location Grid MCP Server

A comprehensive geocoding service that combines Nominatim geocoding with location grid database lookup, available as both a standalone Python library and a Model Context Protocol (MCP) server for AI assistants.

## 🚀 Features

- **Address Geocoding**: Convert addresses to longitude, latitude coordinates using Nominatim
- **Grid ID Lookup**: Find corresponding grid IDs from a location grid database
- **MCP Server**: Full Model Context Protocol server for AI assistant integration
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **JSON API**: Clean JSON responses with `lng`, `lat`, and `grid_id`
- **Error Handling**: Comprehensive error handling with JSON error responses
- **SQLite Integration**: Efficient grid ID lookups using SQLite database
- **Health Checks**: Built-in health monitoring for containerized deployments

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Standalone Python Library](#standalone-python-library)
  - [MCP Server](#mcp-server)
  - [Docker Deployment](#docker-deployment)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Database Structure](#database-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🛠 Installation

### Prerequisites

- Python 3.6+ (Python 3.11+ recommended for Docker)
- Internet connection (for Nominatim API)
- SQLite database file (`db/location_grid.db`)

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd location-grid-mcp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python geocoder.py "New York City"
   ```

### Docker Installation

1. **Build the Docker image:**
   ```bash
   docker build -t location-grid-mcp .
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

## 🚀 Quick Start

### Standalone Usage

```bash
# Command line geocoding
python geocoder.py "London, UK"

# Output:
{
  "lng": -0.1277653,
  "lat": 51.5074456,
  "grid_id": 100130785
}
```

### MCP Server Usage

1. **Start the MCP server:**
   ```bash
   python mcp_server.py
   ```

2. **Configure your MCP client** (e.g., in `mcp_config.json`):
   ```json
   {
     "mcpServers": {
       "location-grid-geocoder": {
         "command": "python",
         "args": ["/path/to/mcp_server.py"],
         "env": {
           "PYTHONPATH": "/path/to/location-grid-mcp"
         }
       }
     }
   }
   ```

### Docker Usage

```bash
# Run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f location-grid-mcp
```

## 📖 Usage

### Standalone Python Library

```python
from geocoder import SimpleGeocoder

# Initialize the geocoder
geocoder = SimpleGeocoder()

# Geocode an address (returns dictionary)
result = geocoder.geocode_address("Tokyo, Japan")
print(result)
# Output: {"lng": 139.7638947, "lat": 35.6768601, "grid_id": 100232965}

# Get result as JSON string
json_result = geocoder.geocode_address_json("Paris, France")
print(json_result)
# Output: '{"lng": 2.3522219, "lat": 48.856614, "grid_id": 100123456}'

# Get grid ID for specific coordinates
grid_id = geocoder._get_grid_id_by_coordinates(-74.006, 40.7128)
print(grid_id)  # Output: 100366035
```

### MCP Server Tools

The MCP server provides two main tools:

#### 1. `geocode_address`
Geocode an address to get longitude, latitude, and grid ID.

**Parameters:**
- `address` (string): The address or location name to geocode

**Example:**
```json
{
  "address": "Sydney, Australia"
}
```

**Response:**
```json
{
  "lng": 151.2082848,
  "lat": -33.8698439,
  "grid_id": 100003047
}
```

#### 2. `geocode_coordinates`
Get grid ID for given longitude and latitude coordinates.

**Parameters:**
- `longitude` (number): Longitude coordinate
- `latitude` (number): Latitude coordinate

**Example:**
```json
{
  "longitude": -74.006,
  "latitude": 40.7128
}
```

**Response:**
```json
{
  "lng": -74.006,
  "lat": 40.7128,
  "grid_id": 100366035
}
```

### Docker Deployment

#### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

#### Using Docker directly

```bash
# Build image
docker build -t location-grid-mcp .

# Run container
docker run -d \
  --name location-grid-mcp \
  -v $(pwd)/db:/app/db \
  -v $(pwd)/logs:/app/logs \
  location-grid-mcp

# Check container status
docker ps

# View logs
docker logs location-grid-mcp
```

## ⚙️ Configuration

### MCP Server Configuration

Create or update your MCP client configuration file:

```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/location-grid-mcp"
      }
    }
  }
}
```

### Docker Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHONPATH` | `/app` | Python path for the application |
| `PYTHONUNBUFFERED` | `1` | Unbuffered Python output |

### Database Configuration

The geocoder uses a SQLite database located at `db/location_grid.db`. Ensure this file exists and is accessible.

## 🗄️ Database Structure

The geocoder uses a SQLite database (`db/location_grid.db`) with a `location_grid` table containing:

| Column | Type | Description |
|--------|------|-------------|
| `grid_id` | INTEGER | Unique identifier for the grid cell |
| `longitude` | REAL | Center longitude of the grid cell |
| `latitude` | REAL | Center latitude of the grid cell |
| `north_latitude` | REAL | Northern boundary of the grid cell |
| `south_latitude` | REAL | Southern boundary of the grid cell |
| `west_longitude` | REAL | Western boundary of the grid cell |
| `east_longitude` | REAL | Eastern boundary of the grid cell |
| `level` | INTEGER | Grid level (higher numbers = more detailed grids) |

## 🔧 API Reference

### SimpleGeocoder Class

#### `__init__(db_path=None)`
Initialize the geocoder with optional database path.

**Parameters:**
- `db_path` (str, optional): Path to SQLite database. Defaults to `./db/location_grid.db`

#### `geocode_address(address)`
Geocode an address and return coordinates with grid ID.

**Parameters:**
- `address` (str): Address or location name to geocode

**Returns:**
- `dict`: Dictionary with `lng`, `lat`, `grid_id` keys on success, or `error` key on failure

#### `geocode_address_json(address)`
Geocode an address and return the result as a JSON string.

**Parameters:**
- `address` (str): Address or location name to geocode

**Returns:**
- `str`: JSON string containing the geocoding result

### Response Formats

#### Success Response
```json
{
  "lng": -74.0060152,
  "lat": 40.7127281,
  "grid_id": 100366035
}
```

#### Error Response
```json
{
  "error": "Could not geocode address 'invalid_address' using Nominatim"
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Errors
```
Error: Failed to connect to database
```
**Solution:** Ensure the database file exists at `db/location_grid.db` and is accessible.

#### 2. Nominatim API Errors
```
Error: Could not geocode address using Nominatim
```
**Solution:** Check your internet connection and verify the address format.

#### 3. Docker Container Issues
```
Error: Container failed to start
```
**Solution:** 
- Check Docker logs: `docker logs location-grid-mcp`
- Verify database file exists
- Check container health: `docker-compose ps`

#### 4. MCP Server Connection Issues
```
Error: MCP server not responding
```
**Solution:**
- Verify the server is running: `python mcp_server.py`
- Check MCP configuration file
- Ensure correct file paths in configuration

### Health Checks

#### Docker Health Check
```bash
# Check container health
docker ps

# View health check logs
docker inspect location-grid-mcp | grep -A 10 Health
```

#### Manual Health Check
```bash
# Test geocoder functionality
python -c "from geocoder import SimpleGeocoder; g = SimpleGeocoder(); print(g.geocode_address('Test'))"
```

### Logs

#### Docker Logs
```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f location-grid-mcp

# View specific service logs
docker-compose logs location-grid-mcp
```

#### Application Logs
Logs are stored in the `logs/` directory when running in Docker.

## 📁 Project Structure

```
location-grid-mcp/
├── db/
│   └── location_grid.db          # SQLite database
├── documents/                     # Additional documentation
├── logs/                         # Application logs
├── backups/                      # Database backups
├── geocoder.py                   # Core geocoding library
├── mcp_server.py                 # MCP server implementation
├── mcp_config.json              # MCP client configuration
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── docker-build.sh             # Docker build script
├── docker-run.sh               # Docker run script
├── docker-test.sh              # Docker test script
└── README.md                    # This file
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly:**
   ```bash
   # Test standalone functionality
   python geocoder.py "Test Location"
   
   # Test MCP server
   python mcp_server.py
   
   # Test Docker deployment
   docker-compose up --build
   ```
5. **Commit your changes:** `git commit -m 'Add amazing feature'`
6. **Push to the branch:** `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd location-grid-mcp

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/  # If tests exist

# Run linting
flake8 .  # If flake8 is configured
```

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Support

For issues, questions, or contributions:

1. **Create an issue** in the repository
2. **Check existing issues** for similar problems
3. **Contact the maintainers** for urgent issues

### Getting Help

- **Documentation**: Check this README and the `documents/` directory
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for urgent issues

---

**Made with ❤️ for the geocoding community**