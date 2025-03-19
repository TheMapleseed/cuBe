#!/usr/bin/env python3
import socket
import json
import time

def test_connection():
    print("Testing connection to BlenderMCP...")
    
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 9876))
        print("Connected to BlenderMCP server!")
        
        # Test creating a sphere
        command = {
            "type": "create_object",
            "params": {
                "type": "SPHERE",
                "location": [0, 0, 3],
                "scale": [1, 1, 1]
            }
        }
        
        print("Sending command to create a sphere...")
        client.sendall(json.dumps(command).encode('utf-8'))
        
        # Wait for response
        response = client.recv(8192).decode('utf-8')
        response_data = json.loads(response)
        
        print(f"Response: {response_data}")
        
        if "result" in response_data and response_data.get("status") == "success":
            print(f"Successfully created object: {response_data['result'].get('name', 'unknown')}")
        else:
            print("Failed to create object.")
        
    except ConnectionRefusedError:
        print("Connection refused. Make sure BlenderMCP server is running in Blender.")
    except Exception as e:
        print(f"Error connecting to BlenderMCP: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("BlenderMCP connection test")
    print("=========================")
    print("Please start Blender and enable the BlenderMCP addon:")
    print("1. Start Blender")
    print("2. Go to Edit > Preferences > Add-ons")
    print("3. Search for 'BlenderMCP'")
    print("4. Enable the addon by checking the box")
    print("5. In the 3D Viewport, press N to open the sidebar")
    print("6. Find the 'BlenderMCP' tab")
    print("7. Click 'Start MCP Server'")
    print("8. Then press Enter in this terminal to continue...")
    input()
    
    test_connection() 