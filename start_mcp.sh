#!/bin/bash
# MCP Server Startup Script
# This script handles path setup automatically

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set the Python path to the script directory
export PYTHONPATH="$SCRIPT_DIR"

# Run the MCP server
exec python "$SCRIPT_DIR/mcp_server.py"
