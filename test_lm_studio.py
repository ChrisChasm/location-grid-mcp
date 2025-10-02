#!/usr/bin/env python3
"""
Test script for LM Studio MCP Server
"""

import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_geocoder():
    """Test the geocoder functionality."""
    print("🧪 Testing Location Grid MCP Server for LM Studio...")
    print("=" * 60)
    
    try:
        from geocoder import SimpleGeocoder
        
        # Initialize geocoder
        geocoder = SimpleGeocoder()
        print("✅ Geocoder initialized successfully")
        
        # Test geocoding
        test_addresses = [
            "New York City",
            "London, UK",
            "Tokyo, Japan"
        ]
        
        for address in test_addresses:
            print(f"\n🔍 Testing: {address}")
            result = geocoder.geocode_address(address)
            print(f"   Result: {json.dumps(result, indent=2)}")
            
        print("\n✅ All geocoding tests passed!")
        
    except Exception as e:
        print(f"❌ Error testing geocoder: {e}")
        return False
    
    return True

def test_mcp_server():
    """Test the MCP server functionality."""
    print("\n🔧 Testing MCP server functionality...")
    
    try:
        from simple_mcp_server import app, geocoder
        
        print("✅ MCP server imports successfully")
        print(f"✅ Server name: {app.name}")
        print(f"✅ Geocoder initialized: {geocoder is not None}")
        
        # Test a simple geocoding operation
        result = geocoder.geocode_address("New York City")
        print(f"✅ Test geocoding: {json.dumps(result, indent=2)}")
        
        print("✅ MCP server functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Location Grid MCP Server - LM Studio Test")
    print("=" * 60)
    
    # Test geocoder
    geocoder_ok = test_geocoder()
    
    # Test MCP server
    mcp_ok = test_mcp_server()
    
    print("\n" + "=" * 60)
    if geocoder_ok and mcp_ok:
        print("🎉 All tests passed! MCP server is ready for LM Studio.")
        print("\n📋 Next steps:")
        print("1. Copy the configuration from 'lm-studio-mcp-config.json'")
        print("2. Add it to LM Studio MCP settings")
        print("3. Restart LM Studio")
        print("4. Test with: 'What's the grid ID for New York City?'")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
