# Blender MCP + Cursor AI MCP = cuBe

This package provides tools to install and configure the BlenderMCP addon for integrating Blender with Cursor AI through the Model Context Protocol (MCP).

## What is cuBe
cuBe is an addon for Blender that allows you to control Blender programmatically through a socket connection. This enables AI assistants like Cursor AI to create and manipulate 3D objects in Blender.

## Official Repository

The official BlenderMCP repository is hosted on GitHub:
[https://github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)

Please visit the repository for the latest updates, features, and community contributions.

## The official cuBe Repository

The officials cuBe reposistory is hosted on 
Github:
[https://github.com/TheMapleseed/cuBe](https://github.com/TheMapleseed/cuBe)

## Features

- **Two-way communication**: Connect Claude AI or Cursor to Blender through a socket-based server
- **Object manipulation**: Create, modify, and delete 3D objects in Blender
- **Material control**: Apply and modify materials and colors
- **Scene inspection**: Get detailed information about the current Blender scene
- **Code execution**: Run arbitrary Python code in Blender
- **Viewport capture**: Capture the current Blender viewport and receive it as an image
- **Scene metrics**: Get detailed performance and scene statistics from Blender
- **Live preview**: Stream continuous viewport updates in real-time

## Installation

### Prerequisites

- Python 3.6 or later
- Blender 2.80 or later

### Installation Steps

#### Windows

1. Download or clone this repository
2. Double-click `install.bat`
3. Follow the prompts in the installer

#### macOS/Linux

1. Download or clone this repository
2. Open Terminal and navigate to the repository folder
3. Make the install script executable: `chmod +x install.sh`
4. Run the installer: `./install.sh`
5. Follow the prompts in the installer

### Manual Installation

If the automatic installer doesn't work for your system, you can manually install the addon:

1. Copy `addon.py` to your Blender addons directory:
   - Windows: `C:\Program Files\Blender Foundation\Blender\[version]\scripts\addons\`
   - macOS: `/Applications/Blender.app/Contents/Resources/scripts/addons/` or `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - Linux: `/usr/share/blender/scripts/addons/` or `~/.config/blender/scripts/addons/`

2. Rename the file to `blendermcp.py`

3. Start Blender and enable the addon:
   - Go to Edit > Preferences > Add-ons
   - Search for "BlenderMCP"
   - Check the box to enable it

## Usage

1. After installation, start Blender
2. In the 3D Viewport, press N to open the sidebar
3. Find the "BlenderMCP" tab
4. Click "Start MCP Server" to start the server on the default port (9876)
5. Connect to the server from Cursor AI or other MCP clients

## Advanced Features

### Viewport Capture

The addon supports capturing the current viewport as an image, which can be sent to Cursor or other clients. Use the `get_viewport_image` command:

```json
{
    "type": "get_viewport_image",
    "params": {
        "width": 512,
        "height": 512,
        "format": "JPEG"
    }
}
```

### Scene Metrics

Get detailed performance and scene statistics from Blender with the `get_scene_metrics` command:

```json
{
    "type": "get_scene_metrics",
    "params": {}
}
```

This returns information about polygon count, objects, memory usage, and more.

### Live Preview

Stream continuous viewport updates in real-time with the `start_live_preview` command:

```json
{
    "type": "start_live_preview",
    "params": {
        "port": 9877,
        "fps": 10
    }
}
```

This starts a separate server on the specified port that clients can connect to for receiving continuous viewport updates.

## Testing the Connection

The installer automatically tests the connection by creating a sphere on top of the default cube. If you see a sphere appear above the cube, the installation was successful!

You can also run the included test scripts:

- `test_blendermcp.py` - Basic connection test
- `test_viewport.py` - Test the advanced viewport and metrics features

## Integration with Cursor AI

The BlenderMCP addon works seamlessly with Cursor AI. To configure Cursor:

1. Open Cursor Settings
2. Navigate to MCP settings
3. Add the BlenderMCP command: `uvx blender-mcp`

## Troubleshooting

- **Port already in use**: If port 9876 is already in use, you can change the port in the BlenderMCP panel in Blender.
- **Addon not found**: Make sure the addon is properly installed and enabled in Blender's preferences.
- **Connection failed**: Check that the server is running and that no firewall is blocking the connection.
- **Viewport capture issues**: Make sure you have a 3D viewport area in your Blender setup.
- **Live preview not working**: Check if another service is already using the specified preview port.

## Contributing

Contributions are welcome!

## License

This software is provided under the GPLv3 License. 
