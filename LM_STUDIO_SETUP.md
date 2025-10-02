# LM Studio MCP Server Configuration

## 🎯 **LM Studio MCP Configuration Guide**

This guide shows you how to configure the Location Grid MCP Server with LM Studio.

## 📁 **Configuration Files**

### **LM Studio MCP Config:**
- **`lm-studio-mcp-config.json`** - LM Studio MCP server configuration

## 🔧 **LM Studio Setup**

### **1. Install LM Studio**
Download and install LM Studio from: https://lmstudio.ai/

### **2. Configure MCP Server**

#### **Option A: Use the provided config file**
Copy the contents of `lm-studio-mcp-config.json` to your LM Studio MCP configuration.

#### **Option B: Manual configuration**
In LM Studio, go to **Settings** → **MCP Servers** and add:

```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "python",
      "args": ["/Users/chris/Documents/MCP_SERVERS/location-grid-mcp/simple_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/chris/Documents/MCP_SERVERS/location-grid-mcp"
      }
    }
  }
}
```

### **3. Alternative: Docker Configuration**

If you prefer to use Docker:

```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/chris/Documents/MCP_SERVERS/location-grid-mcp/db:/app/db",
        "location-grid-mcp:latest"
      ]
    }
  }
}
```

## 🚀 **Quick Start**

### **1. Fix the MCP Server (if needed)**
The server has been updated to fix the initialization issue. If you're still getting errors, rebuild:

```bash
cd /Users/chris/Documents/MCP_SERVERS/location-grid-mcp
python simple_mcp_server.py --help
```

### **2. Test the Server**
```bash
# Test the geocoder functionality
python test_mcp.py

# Test the MCP server
python simple_mcp_server.py
```

### **3. Configure LM Studio**
1. Open LM Studio
2. Go to **Settings** → **MCP Servers**
3. Add the configuration from `lm-studio-mcp-config.json`
4. Save and restart LM Studio

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **"Field required" error:**
   - The server has been fixed with proper `capabilities` field
   - Rebuild the Docker image if using Docker

2. **"Connection closed" error:**
   - Check that the Python path is correct
   - Ensure the database file exists
   - Check LM Studio logs for more details

3. **"Module not found" error:**
   - Ensure `PYTHONPATH` is set correctly
   - Install MCP dependencies: `pip install mcp`

### **Debug Steps:**

1. **Test the server directly:**
   ```bash
   cd /Users/chris/Documents/MCP_SERVERS/location-grid-mcp
   python simple_mcp_server.py
   ```

2. **Check LM Studio logs:**
   - Look for MCP server logs in LM Studio
   - Check for connection errors

3. **Verify file paths:**
   ```bash
   ls -la /Users/chris/Documents/MCP_SERVERS/location-grid-mcp/
   ls -la /Users/chris/Documents/MCP_SERVERS/location-grid-mcp/db/
   ```

## 📋 **Available Tools**

Once configured, LM Studio will have access to:

### **1. `geocode_address`**
Convert an address to coordinates + grid ID.

**Example:**
```
User: "What's the grid ID for New York City?"
LM Studio: [Uses geocode_address tool] → Returns coordinates + grid_id
```

### **2. `geocode_coordinates`**
Get grid ID for specific coordinates.

**Example:**
```
User: "What grid covers coordinates -74.006, 40.712?"
LM Studio: [Uses geocode_coordinates tool] → Returns grid_id
```

## 🔄 **Docker Alternative**

If you prefer using Docker:

### **1. Build the Docker image:**
```bash
./docker-build.sh
```

### **2. Use Docker configuration:**
```json
{
  "mcpServers": {
    "location-grid-geocoder": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/chris/Documents/MCP_SERVERS/location-grid-mcp/db:/app/db",
        "location-grid-mcp:latest"
      ]
    }
  }
}
```

## ✅ **Verification**

### **Test the configuration:**
1. **Start LM Studio**
2. **Check MCP server status** in LM Studio settings
3. **Try asking:** "What's the grid ID for New York City?"
4. **Expected response:** Coordinates and grid ID

### **Success indicators:**
- ✅ MCP server shows as "Connected" in LM Studio
- ✅ No error messages in LM Studio logs
- ✅ Tools are available in LM Studio
- ✅ Geocoding requests work correctly

## 🎯 **Next Steps**

1. **Test the tools** - Try geocoding different addresses
2. **Explore the database** - Ask about different locations
3. **Integrate with your workflow** - Use the geocoding in your projects

The Location Grid MCP Server is now ready to use with LM Studio! 🚀
