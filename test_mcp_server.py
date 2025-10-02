#!/usr/bin/env python3
"""
Test the MCP server functionality
"""

import asyncio
import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from mcp_server import server, geocoder

async def test_tools():
    """Test the MCP server tools directly."""
    print("Testing MCP server tools...")
    
    # Test geocode_address tool
    print("\n1. Testing geocode_address tool:")
    try:
        result = await server._call_tool_handler("geocode_address", {"address": "New York City"})
        print(f"Result: {result[0].text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test geocode_coordinates tool
    print("\n2. Testing geocode_coordinates tool:")
    try:
        result = await server._call_tool_handler("geocode_coordinates", {
            "longitude": -74.0060152, 
            "latitude": 40.7127281
        })
        print(f"Result: {result[0].text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test list_tools
    print("\n3. Testing list_tools:")
    try:
        tools = await server._list_tools_handler()
        print(f"Available tools: {[tool.name for tool in tools]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("MCP Server Test")
    print("=" * 40)
    asyncio.run(test_tools())
