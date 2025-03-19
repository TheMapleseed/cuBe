#!/usr/bin/env python3
import os
import sys
import platform
import shutil
import subprocess
import time
import json
import socket
import argparse
from pathlib import Path

def get_blender_path():
    """Detect Blender installation based on operating system"""
    system = platform.system()
    
    if system == "Windows":
        # Check common Windows installation paths
        possible_paths = [
            r"C:\Program Files\Blender Foundation\Blender",
            r"C:\Program Files (x86)\Blender Foundation\Blender",
        ]
        
        # Check if any of these paths exist
        for base_path in possible_paths:
            if os.path.exists(base_path):
                # Find the latest Blender version by listing directories
                blender_versions = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
                if blender_versions:
                    # Sort to get the latest version
                    latest_version = sorted(blender_versions)[-1]
                    return os.path.join(base_path, latest_version)
                else:
                    return base_path
        
        print("Blender installation not found in common locations.")
        blender_path = input("Please enter the path to your Blender installation: ")
        return blender_path.strip()
        
    elif system == "Darwin":  # macOS
        # Check common macOS installation path
        standard_path = "/Applications/Blender.app"
        if os.path.exists(standard_path):
            return standard_path
        
        print("Blender installation not found in /Applications")
        blender_path = input("Please enter the path to your Blender.app: ")
        return blender_path.strip()
        
    elif system == "Linux":
        # Check common Linux installation paths
        possible_paths = [
            "/usr/bin/blender",
            "/usr/local/bin/blender",
            "/snap/bin/blender"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.dirname(os.path.realpath(path))
        
        print("Blender installation not found in common locations.")
        blender_path = input("Please enter the path to your Blender installation: ")
        return blender_path.strip()
    
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)

def get_addon_install_path(blender_path):
    """Get the appropriate addons directory path based on OS and Blender path"""
    system = platform.system()
    
    if system == "Windows":
        return os.path.join(blender_path, "scripts", "addons")
    
    elif system == "Darwin":  # macOS
        return os.path.join(blender_path, "Contents", "Resources", "scripts", "addons")
    
    elif system == "Linux":
        # For Linux, we need to handle both system-wide and user-specific installations
        # First check if the provided path is a system-wide installation
        system_addons_path = os.path.join(blender_path, "scripts", "addons")
        if os.path.exists(system_addons_path) and os.access(system_addons_path, os.W_OK):
            return system_addons_path
        
        # If not, use the user-specific addons directory
        user_addons_path = os.path.expanduser("~/.config/blender/scripts/addons")
        # Create the directory if it doesn't exist
        os.makedirs(user_addons_path, exist_ok=True)
        return user_addons_path
    
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)

def get_blender_executable(blender_path):
    """Get the path to the Blender executable based on the OS"""
    system = platform.system()
    
    if system == "Windows":
        return os.path.join(blender_path, "blender.exe")
    
    elif system == "Darwin":  # macOS
        return os.path.join(blender_path, "Contents", "MacOS", "blender")
    
    elif system == "Linux":
        # For Linux, the executable might be in different locations
        # Check if blender_path itself is the executable
        if os.path.basename(blender_path) == "blender" and os.access(blender_path, os.X_OK):
            return blender_path
        
        # Otherwise check common locations relative to blender_path
        possible_execs = [
            os.path.join(blender_path, "blender"),
            "/usr/bin/blender",
            "/usr/local/bin/blender",
            "/snap/bin/blender"
        ]
        
        for exec_path in possible_execs:
            if os.path.exists(exec_path) and os.access(exec_path, os.X_OK):
                return exec_path
        
        print("Blender executable not found.")
        sys.exit(1)
    
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)

def install_addon(addon_path, blender_path):
    """Install the BlenderMCP addon to the appropriate Blender directory"""
    # Get the addon installation path
    addons_dir = get_addon_install_path(blender_path)
    
    # Ensure the addons directory exists
    if not os.path.exists(addons_dir):
        print(f"Creating addons directory: {addons_dir}")
        os.makedirs(addons_dir, exist_ok=True)
    
    # Destination path for the addon
    addon_dest = os.path.join(addons_dir, "blendermcp.py")
    
    print(f"Installing BlenderMCP addon to: {addon_dest}")
    try:
        shutil.copy2(addon_path, addon_dest)
        print("BlenderMCP addon installed successfully!")
        return True
    except Exception as e:
        print(f"Error installing addon: {e}")
        return False

def is_port_available(port, host='localhost'):
    """Check if a port is available on the specified host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.bind((host, port))
        sock.close()
        return True
    except (socket.error, OSError):
        return False

def send_blender_command(port, command_type, params=None):
    """Send a command to the Blender MCP server and return the response"""
    if params is None:
        params = {}
    
    command = {
        "type": command_type,
        "params": params
    }
    
    try:
        # Create socket and connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 second timeout
        sock.connect(('localhost', port))
        
        # Send command
        sock.sendall(json.dumps(command).encode('utf-8'))
        
        # Receive response
        response = b''
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
            try:
                # Try to parse JSON to see if we have a complete response
                json.loads(response.decode('utf-8'))
                break
            except json.JSONDecodeError:
                # Not complete yet, continue receiving
                continue
        
        sock.close()
        
        if response:
            return json.loads(response.decode('utf-8'))
        else:
            return {"status": "error", "message": "No response from server"}
    
    except Exception as e:
        return {"status": "error", "message": f"Error communicating with Blender: {str(e)}"}

def test_connection(port):
    """Test the connection to the Blender MCP server"""
    # First, check if the port is in use (server should be running)
    if is_port_available(port):
        print(f"Error: No server detected on port {port}")
        return False
    
    # Get scene info to check the connection
    print("Testing connection to Blender MCP server...")
    response = send_blender_command(port, "get_scene_info")
    
    if response.get("status") == "success":
        print("Connection successful!")
        scene_info = response.get("result", {})
        objects = scene_info.get("objects", [])
        print(f"Scene contains {len(objects)} objects")
        
        # Create a sphere on top of the default cube
        # First, find the cube
        cube_location = None
        for obj in objects:
            if obj.get("name") == "Cube":
                cube_location = obj.get("location")
                break
        
        if cube_location:
            # Position the sphere 2 units above the cube
            sphere_location = [cube_location[0], cube_location[1], cube_location[2] + 2]
            
            # Create the sphere
            print("Creating a sphere above the cube...")
            response = send_blender_command(port, "create_object", {
                "type": "SPHERE",
                "name": "TestSphere",
                "location": sphere_location,
                "scale": [0.5, 0.5, 0.5]
            })
            
            if response.get("status") == "success":
                print("Test sphere created successfully!")
                return True
            else:
                print(f"Error creating test sphere: {response.get('message', 'Unknown error')}")
                return False
        else:
            print("No cube found in the scene. Creating a standalone test sphere...")
            response = send_blender_command(port, "create_object", {
                "type": "SPHERE",
                "name": "TestSphere",
                "location": [0, 0, 2],
                "scale": [0.5, 0.5, 0.5]
            })
            
            if response.get("status") == "success":
                print("Test sphere created successfully!")
                return True
            else:
                print(f"Error creating test sphere: {response.get('message', 'Unknown error')}")
                return False
    else:
        print(f"Connection failed: {response.get('message', 'Unknown error')}")
        return False

def start_blender_with_addon(blender_path, port):
    """Start Blender with the MCP addon enabled and listening on the specified port"""
    blender_exe = get_blender_executable(blender_path)
    
    # Create a Python script to run in Blender
    temp_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_startup.py")
    with open(temp_script, "w") as f:
        f.write(f'''
import bpy

# Check if addon is already registered
if not "blendermcp" in bpy.context.preferences.addons:
    # Enable the addon
    bpy.ops.preferences.addon_enable(module="blendermcp")

# Set the port
bpy.context.scene.blendermcp_port = {port}

# Start the server
if hasattr(bpy.types, "BLENDERMCP_OT_StartServer"):
    bpy.ops.blendermcp.start_server()
else:
    print("ERROR: BlenderMCP addon not properly installed or registered")
''')
    
    # Command to start Blender with the script
    cmd = [blender_exe, "--python", temp_script]
    
    print(f"Starting Blender with command: {' '.join(cmd)}")
    try:
        # Start Blender in a new process
        process = subprocess.Popen(cmd)
        
        # Wait for Blender to start up and the server to initialize
        print("Waiting for Blender MCP server to start...")
        for i in range(30):  # Wait up to 30 seconds
            time.sleep(1)
            if not is_port_available(port):
                print(f"Blender MCP server detected on port {port}")
                # Clean up the temporary script
                try:
                    os.remove(temp_script)
                except:
                    pass
                return True
        
        print("Timeout waiting for Blender MCP server to start")
        # Clean up the temporary script
        try:
            os.remove(temp_script)
        except:
            pass
        return False
        
    except Exception as e:
        print(f"Error starting Blender: {e}")
        # Clean up the temporary script
        try:
            os.remove(temp_script)
        except:
            pass
        return False

def main():
    """Main function to install and test the BlenderMCP addon"""
    parser = argparse.ArgumentParser(description='Install and test BlenderMCP addon')
    parser.add_argument('--addon-path', help='Path to the BlenderMCP addon file (addon.py)', default='addon.py')
    parser.add_argument('--port', type=int, help='Port for Blender MCP server', default=9876)
    args = parser.parse_args()
    
    # Verify addon file exists
    if not os.path.exists(args.addon_path):
        print(f"Error: Addon file not found at {args.addon_path}")
        sys.exit(1)
    
    # Get Blender installation path
    print("Detecting Blender installation...")
    blender_path = get_blender_path()
    print(f"Blender found at: {blender_path}")
    
    # Install the addon
    if not install_addon(args.addon_path, blender_path):
        print("Installation failed. Exiting.")
        sys.exit(1)
    
    # Check if the port is already in use
    if not is_port_available(args.port):
        print(f"Warning: Port {args.port} is already in use. This may indicate that a Blender MCP server is already running.")
        choice = input("Do you want to continue and try to connect to the existing server? (y/n): ")
        if choice.lower() != 'y':
            print("Exiting.")
            sys.exit(0)
        
        # Test the connection to the existing server
        if test_connection(args.port):
            print("Successfully connected to existing Blender MCP server!")
        else:
            print("Failed to connect to the existing server. You may need to restart Blender or choose a different port.")
            sys.exit(1)
    else:
        # Start Blender with the addon
        print(f"Starting Blender with BlenderMCP addon on port {args.port}...")
        if not start_blender_with_addon(blender_path, args.port):
            print("Failed to start Blender with the addon. Please check the installation and try again.")
            sys.exit(1)
        
        # Test the connection
        if test_connection(args.port):
            print("Installation and testing complete! BlenderMCP is working correctly.")
        else:
            print("Connection test failed. BlenderMCP may not be configured correctly.")
            sys.exit(1)
    
    print("\nSetup Summary:")
    print(f"- Blender installation: {blender_path}")
    print(f"- BlenderMCP addon installed to: {get_addon_install_path(blender_path)}")
    print(f"- Blender MCP server running on port: {args.port}")
    print("\nYou can now use Cursor AI with Blender through the MCP protocol!")

if __name__ == "__main__":
    main() 