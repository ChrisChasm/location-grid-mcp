# Location Grid MCP Server

This MCP (Model Context Protocol) server exposes the Location Grid Geocoder functionality to LLMs, allowing them to geocode addresses and retrieve grid IDs for coordinates.

## Features

- **Address Geocoding**: Convert addresses to longitude, latitude coordinates and grid IDs
- **Coordinate Lookup**: Get grid IDs for specific longitude/latitude coordinates  
- **MCP Integration**: Full MCP server implementation for LLM integration
- **JSON Responses**: Clean JSON output for all operations
- **Error Handling**: Comprehensive error handling with JSON error responses

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the location grid database exists at `db/location_grid.db`

## MCP Server Tools

The server provides two main tools:

### 1. `geocode_address`
Geocode an address to get longitude, latitude, and grid ID.

**Input:**
```json
{
  "address": "New York City"
}
```

**Output:**
```json
{
  "lng": -74.0060152,
  "lat": 40.7127281,
  "grid_id": 100366035
}
```

### 2. `geocode_coordinates`
Get grid ID for given longitude and latitude coordinates.

**Input:**
```json
{
  "longitude": -74.0060152,
  "latitude": 40.7127281
}
```

**Output:**
```json
{
  "lng": -74.0060152,
  "lat": 40.7127281,
  "grid_id": 100366035
}
```

## Configuration

To use this MCP server, add it to your MCP client configuration:

```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "python",
      "args": ["/path/to/location-grid-mcp/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/location-grid-mcp"
      }
    }
  }
}
```

## Usage Examples

### With Claude Desktop
Add the server to your Claude Desktop configuration file (usually `~/.claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "python",
      "args": ["/Users/chris/Documents/MCP_SERVERS/location-grid-mcp/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/chris/Documents/MCP_SERVERS/location-grid-mcp"
      }
    }
  }
}
```

### With Other MCP Clients
The server implements the standard MCP protocol and can be used with any MCP-compatible client.

## Testing

Run the test script to verify functionality:

```bash
python test_mcp.py
```

This will test both address geocoding and coordinate lookup functionality.

## Error Handling

The server returns JSON error responses for various failure conditions:

```json
{
  "error": "Could not geocode address 'invalid_address' using Nominatim"
}
```

```json
{
  "error": "No location grid found for coordinates 40.7127281,-74.0060152"
}
```

## API Reference

### Tools

#### `geocode_address`
- **Description**: Geocode an address to get longitude, latitude, and grid ID
- **Input**: `address` (string) - The address or location name to geocode
- **Output**: JSON object with `lng`, `lat`, `grid_id` or `error`

#### `geocode_coordinates`
- **Description**: Get grid ID for given longitude and latitude coordinates
- **Input**: `longitude` (number), `latitude` (number) - The coordinates
- **Output**: JSON object with `lng`, `lat`, `grid_id` or `error`

### Resources

#### `location-grid://database`
- **Description**: SQLite database containing location grid information
- **Type**: `application/x-sqlite3`

## Requirements

- Python 3.6+
- Internet connection (for Nominatim API)
- SQLite database file (`db/location_grid.db`)
- MCP client for integration

## Architecture

The MCP server wraps the existing `SimpleGeocoder` class and exposes its functionality through the MCP protocol:

1. **MCP Server**: Handles MCP protocol communication
2. **Geocoder**: Core geocoding functionality using Nominatim
3. **Database**: SQLite database with location grid information
4. **Tools**: MCP tools that expose geocoding operations

## Development

To modify or extend the server:

1. Edit `mcp_server.py` to add new tools or modify existing ones
2. Update the test script `test_mcp.py` to test new functionality
3. Update this README with new features

## License

This project is open source. Please check the license file for details.
