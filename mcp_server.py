#!/usr/bin/env python3
"""
MCP Server for Location Grid Geocoder

This MCP server exposes the geocoding functionality to LLMs,
allowing them to geocode addresses and get coordinates with grid IDs.
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from geocoder import SimpleGeocoder

# Initialize the MCP server
server = Server("location-grid-geocoder")

# Initialize the geocoder
geocoder = SimpleGeocoder()

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="location-grid://database",
            name="Location Grid Database",
            description="SQLite database containing location grid information",
            mimeType="application/x-sqlite3"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a resource."""
    if uri == "location-grid://database":
        return "Location Grid Database - Contains grid cells with coordinates and boundaries"
    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="geocode_address",
            description="Geocode an address to get longitude, latitude, and grid ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "The address or location name to geocode"
                    }
                },
                "required": ["address"]
            }
        ),
        Tool(
            name="geocode_coordinates",
            description="Get grid ID for given longitude and latitude coordinates",
            inputSchema={
                "type": "object",
                "properties": {
                    "longitude": {
                        "type": "number",
                        "description": "Longitude coordinate"
                    },
                    "latitude": {
                        "type": "number", 
                        "description": "Latitude coordinate"
                    }
                },
                "required": ["longitude", "latitude"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        if name == "geocode_address":
            address = arguments.get("address")
            if not address:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "Address parameter is required"}, indent=2)
                )]
            
            # Geocode the address
            result = geocoder.geocode_address(address)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        elif name == "geocode_coordinates":
            longitude = arguments.get("longitude")
            latitude = arguments.get("latitude")
            
            if longitude is None or latitude is None:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "Both longitude and latitude parameters are required"}, indent=2)
                )]
            
            # Get grid ID for coordinates
            grid_id = geocoder._get_grid_id_by_coordinates(longitude, latitude)
            
            if grid_id is None:
                result = {"error": f"No location grid found for coordinates {latitude},{longitude}"}
            else:
                result = {
                    "lng": longitude,
                    "lat": latitude,
                    "grid_id": grid_id
                }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
            )]
            
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]

async def main():
    """Main entry point for the MCP server."""
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())