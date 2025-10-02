#!/usr/bin/env python3
"""
Test script for the Location Grid MCP Server
"""

import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from geocoder import SimpleGeocoder

def test_geocoder():
    """Test the geocoder functionality directly."""
    print("Testing geocoder functionality...")
    
    try:
        geocoder = SimpleGeocoder()
        
        # Test cases
        test_addresses = [
            "New York City",
            "London, UK", 
            "Tokyo, Japan",
            "Sydney, Australia"
        ]
        
        for address in test_addresses:
            print(f"\nTesting address: {address}")
            result = geocoder.geocode_address(address)
            print(f"Result: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        print(f"Error testing geocoder: {e}")

def test_coordinates():
    """Test coordinate lookup functionality."""
    print("\nTesting coordinate lookup...")
    
    try:
        geocoder = SimpleGeocoder()
        
        # Test coordinates
        test_coords = [
            (-74.0060152, 40.7127281),  # New York
            (-0.1277653, 51.5074456),   # London
            (139.7638947, 35.6768601),  # Tokyo
            (151.2082848, -33.8698439)  # Sydney
        ]
        
        for lng, lat in test_coords:
            print(f"\nTesting coordinates: {lat}, {lng}")
            grid_id = geocoder._get_grid_id_by_coordinates(lng, lat)
            if grid_id:
                print(f"Grid ID: {grid_id}")
            else:
                print("No grid ID found")
                
    except Exception as e:
        print(f"Error testing coordinates: {e}")

if __name__ == "__main__":
    print("Location Grid MCP Server Test")
    print("=" * 40)
    
    test_geocoder()
    test_coordinates()
    
    print("\nTest completed!")
