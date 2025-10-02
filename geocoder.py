#!/usr/bin/env python3
"""
Geocoder Module

Geocoding functionality that combines Nominatim geocoding
with location grid database lookup to return coordinates and grid_id.
"""

import sqlite3
import json
import math
import os
import sys
from typing import Optional, Dict, Any
import urllib.request
import urllib.parse


class SimpleGeocoder:
    """
    Geocoder that takes an address and returns longitude, latitude, and grid_id.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the geocoder
        
        Args:
            db_path: Path to SQLite database file. Defaults to ./db/location_grid.db
        """
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'db', 'location_grid.db')
        
        self.db_path = db_path
        self.grid_table = 'location_grid'
        
        # Test database connection
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        except sqlite3.Error as e:
            raise Exception(f"Failed to connect to database: {e}")
    
    def __del__(self):
        """Close database connection on cleanup"""
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def geocode_address(self, address: str) -> Dict[str, Any]:
        """
        Geocode an address and return longitude, latitude, and grid_id as JSON.
        
        Args:
            address: Address or location name to geocode
            
        Returns:
            Dictionary with keys: lng, lat, grid_id (on success) or error (on failure)
        """
        try:
            # First geocode using Nominatim
            coordinates = self._geocode_with_nominatim(address)
            if not coordinates:
                return {"error": f"Could not geocode address '{address}' using Nominatim"}
            
            longitude, latitude = coordinates
            
            # Get grid_id from location grid database
            grid_id = self._get_grid_id_by_coordinates(longitude, latitude)
            if grid_id is None:
                return {"error": f"Address geocoded to {latitude},{longitude} but no location grid found for those coordinates"}
            
            # Return JSON format
            return {
                "lng": longitude,
                "lat": latitude,
                "grid_id": grid_id
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def geocode_address_json(self, address: str) -> str:
        """
        Geocode an address and return the result as a JSON string.
        
        Args:
            address: Address or location name to geocode
            
        Returns:
            JSON string containing lng, lat, grid_id or error
        """
        result = self.geocode_address(address)
        return json.dumps(result)
    
    def _geocode_with_nominatim(self, address: str) -> Optional[tuple]:
        """
        Geocode address using Nominatim API.
        
        Args:
            address: Address to geocode
            
        Returns:
            Tuple of (longitude, latitude) or None if failed
        """
        try:
            # URL encode the address
            encoded_address = urllib.parse.quote(address)
            url = f"https://nominatim.openstreetmap.org/search?q={encoded_address}&format=json&limit=1"
            
            # Add user agent header (required by Nominatim)
            headers = {
                'User-Agent': 'LocationGridMCP/1.0'
            }
            
            request = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(request) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data and len(data) > 0:
                    result = data[0]
                    longitude = float(result['lon'])
                    latitude = float(result['lat'])
                    return (longitude, latitude)
                
                return None
                
        except Exception as e:
            print(f"Nominatim geocoding error: {e}")
            return None
    
    def _get_grid_id_by_coordinates(self, longitude: float, latitude: float) -> Optional[int]:
        """
        Get grid_id by longitude and latitude coordinates from location grid database.
        
        Args:
            longitude: Longitude coordinate
            latitude: Latitude coordinate
            
        Returns:
            Grid ID number or None if not found
        """
        longitude = float(longitude)
        latitude = float(latitude)
        
        # Normalize longitude to -180 to 180 range
        if longitude > 180:
            longitude = longitude - 180
            longitude = -1 * abs(longitude)
        elif longitude < -180:
            longitude = longitude + 180
            longitude = abs(longitude)
        
        # Query for the best match using bounding box
        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT grid_id, longitude, latitude, level
            FROM {self.grid_table}
            WHERE north_latitude >= ? AND south_latitude <= ? 
            AND west_longitude <= ? AND east_longitude >= ?
            ORDER BY level DESC
            LIMIT 1
        """, (latitude, latitude, longitude, longitude))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return result['grid_id']
        
        # If no exact match, try nearest centerpoint
        return self._get_nearest_centerpoint(longitude, latitude)
    
    def _get_nearest_centerpoint(self, longitude: float, latitude: float) -> Optional[int]:
        """
        Get grid_id by nearest centerpoint when no bounding box match is found.
        
        Args:
            longitude: Longitude coordinate
            latitude: Latitude coordinate
            
        Returns:
            Grid ID number or None if not found
        """
        # Create bounding box for search
        north_latitude = math.ceil(latitude) + 1
        south_latitude = math.floor(latitude) - 1
        west_longitude = math.floor(longitude) - 1
        east_longitude = math.ceil(longitude) + 1
        
        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT grid_id, longitude, latitude
            FROM {self.grid_table}
            WHERE longitude < ? AND longitude > ? 
            AND latitude < ? AND latitude > ?
            AND level > 1
        """, (east_longitude, west_longitude, north_latitude, south_latitude))
        
        results = cursor.fetchall()
        cursor.close()
        
        if results:
            # Find the closest centerpoint
            distances = {}
            for result in results:
                distance = self._calculate_distance(
                    result['longitude'], result['latitude'], longitude, latitude
                )
                distances[result['grid_id']] = distance
            
            return min(distances.keys(), key=lambda k: distances[k])
        
        return None
    
    def _calculate_distance(self, lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """Calculate distance between two points using Haversine formula."""
        theta = lon1 - lon2
        dist = (math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + 
                math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
                math.cos(math.radians(theta)))
        dist = math.acos(dist)
        dist = math.degrees(dist)
        miles = dist * 60 * 1.1515
        return miles


def main():
    """Command line interface for testing."""
    if len(sys.argv) != 2:
        print("Usage: python geocoder.py <address>")
        sys.exit(1)
    
    try:
        address = sys.argv[1]
        geocoder = SimpleGeocoder()
        result = geocoder.geocode_address(address)
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
