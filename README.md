# Location Grid Geocoder

A Python geocoder that combines Nominatim geocoding with location grid database lookup to return coordinates and grid IDs in JSON format.

## Features

- **Address Geocoding**: Convert addresses to longitude, latitude coordinates using Nominatim
- **Grid ID Lookup**: Find corresponding grid IDs from a location grid database
- **JSON Output**: Returns results in clean JSON format with `lng`, `lat`, and `grid_id`
- **Error Handling**: Comprehensive error handling with JSON error responses
- **SQLite Integration**: Uses SQLite database for efficient grid ID lookups

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.6+ installed
3. The required dependencies are part of Python's standard library:
   - `sqlite3`
   - `json`
   - `urllib`
   - `math`

## Usage

### Command Line Interface

```bash
python geocoder.py "New York City"
```

**Output:**
```json
{
  "lng": -74.0060152,
  "lat": 40.7127281,
  "grid_id": 100366035
}
```

### Python API

```python
from geocoder import SimpleGeocoder

# Initialize the geocoder
geocoder = SimpleGeocoder()

# Geocode an address (returns dictionary)
result = geocoder.geocode_address("London, UK")
print(result)
# Output: {"lng": -0.1277653, "lat": 51.5074456, "grid_id": 100130785}

# Get result as JSON string
json_result = geocoder.geocode_address_json("Tokyo, Japan")
print(json_result)
# Output: '{"lng": 139.7638947, "lat": 35.6768601, "grid_id": 100232965}'
```

### Response Format

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

## Database Structure

The geocoder uses a SQLite database (`db/location_grid.db`) with a `location_grid` table containing:

- `grid_id`: Unique identifier for the grid cell
- `longitude`: Center longitude of the grid cell
- `latitude`: Center latitude of the grid cell
- `north_latitude`: Northern boundary of the grid cell
- `south_latitude`: Southern boundary of the grid cell
- `west_longitude`: Western boundary of the grid cell
- `east_longitude`: Eastern boundary of the grid cell
- `level`: Grid level (higher numbers = more detailed grids)

## How It Works

1. **Address Input**: Takes an address string as input
2. **Nominatim Geocoding**: Uses OpenStreetMap's Nominatim service to convert address to coordinates
3. **Grid Lookup**: Searches the location grid database for the best matching grid cell
4. **Coordinate Matching**: Uses bounding box matching first, then falls back to nearest centerpoint
5. **JSON Response**: Returns longitude, latitude, and grid_id in JSON format

## Error Handling

The geocoder handles various error conditions:

- **Geocoding Failures**: When Nominatim cannot find the address
- **Grid Lookup Failures**: When no grid cell is found for the coordinates
- **Network Issues**: When Nominatim API is unavailable
- **Database Issues**: When the location grid database is inaccessible

All errors are returned as JSON objects with an `error` key.

## Examples

### Successful Geocoding
```bash
$ python geocoder.py "Sydney, Australia"
{
  "lng": 151.2082848,
  "lat": -33.8698439,
  "grid_id": 100003047
}
```

### Error Handling
```bash
$ python geocoder.py "nonexistent_place_xyz"
{
  "error": "Could not geocode address 'nonexistent_place_xyz' using Nominatim"
}
```

## API Reference

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

## Requirements

- Python 3.6+
- Internet connection (for Nominatim API)
- SQLite database file (`db/location_grid.db`)

## License

This project is open source. Please check the license file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions, please create an issue in the repository or contact the maintainers.
