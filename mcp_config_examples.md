# MCP Configuration Examples

## Option 1: Relative Paths (Current)
```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "python",
      "args": ["./mcp_server.py"],
      "cwd": ".",
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

## Option 2: Environment Variable
```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "python",
      "args": ["${LOCATION_GRID_MCP_PATH}/mcp_server.py"],
      "env": {
        "PYTHONPATH": "${LOCATION_GRID_MCP_PATH}"
      }
    }
  }
}
```

## Option 3: Docker (Most Portable)
```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "${PWD}/db:/app/db",
        "location-grid-mcp:latest"
      ]
    }
  }
}
```

## Option 4: Shell Script Wrapper
```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "./start_mcp.sh"
    }
  }
}
```

## Option 5: Python Module (if installed)
```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "python",
      "args": ["-m", "location_grid_mcp.mcp_server"]
    }
  }
}
```

## Usage Instructions

### For Option 1 (Relative Paths):
- Place this config in the same directory as your MCP server
- Run the MCP client from that directory
- Works for: Claude Desktop, LM Studio, etc.

### For Option 2 (Environment Variable):
- Set `LOCATION_GRID_MCP_PATH` to your project directory
- Example: `export LOCATION_GRID_MCP_PATH=/path/to/location-grid-mcp`

### For Option 3 (Docker):
- Build the Docker image first: `docker build -t location-grid-mcp .`
- Most portable across different systems

### For Option 4 (Shell Script):
- Create a `start_mcp.sh` script that handles the path setup
- Make it executable: `chmod +x start_mcp.sh`

### For Option 5 (Python Module):
- Install your package: `pip install -e .`
- Most professional approach for distribution
