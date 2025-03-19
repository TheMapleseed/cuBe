#!/usr/bin/env python3
import socket
import json
import time
import base64
import os
import sys

def test_viewport_capture():
    """Test the viewport capture functionality"""
    print("Testing viewport capture...")
    
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 9876))
        print("Connected to BlenderMCP server!")
        
        # Request viewport image
        command = {
            "type": "get_viewport_image",
            "params": {
                "width": 512,
                "height": 512,
                "format": "JPEG"
            }
        }
        
        print("Requesting viewport image...")
        client.sendall(json.dumps(command).encode('utf-8'))
        
        # Wait for response
        response = client.recv(100000000).decode('utf-8')  # Large buffer for image data
        response_data = json.loads(response)
        
        if "result" in response_data and response_data.get("status") == "success":
            result = response_data["result"]
            if "image" in result:
                # Save the image to a file
                img_data = base64.b64decode(result["image"])
                output_path = os.path.join(os.getcwd(), "viewport_capture.jpg")
                with open(output_path, "wb") as f:
                    f.write(img_data)
                
                print(f"Viewport image saved to: {output_path}")
                print(f"Image size: {result.get('width')}x{result.get('height')}")
            else:
                print("No image data in response")
        else:
            print(f"Failed to capture viewport: {response_data}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def test_scene_metrics():
    """Test the scene metrics functionality"""
    print("\nTesting scene metrics...")
    
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 9876))
        
        # Request scene metrics
        command = {
            "type": "get_scene_metrics",
            "params": {}
        }
        
        print("Requesting scene metrics...")
        client.sendall(json.dumps(command).encode('utf-8'))
        
        # Wait for response
        response = client.recv(8192).decode('utf-8')
        response_data = json.loads(response)
        
        if "result" in response_data and response_data.get("status") == "success":
            metrics = response_data["result"]
            print("\nScene Metrics:")
            print(f"FPS: {metrics.get('fps')}")
            print(f"Frame: {metrics.get('frame_current')} / {metrics.get('frame_start')}-{metrics.get('frame_end')}")
            
            objects = metrics.get('objects', {})
            print(f"Objects: {objects.get('total')} total, {objects.get('meshes')} meshes, "
                  f"{objects.get('lights')} lights, {objects.get('cameras')} cameras")
            
            print(f"Polygons: {metrics.get('polygons')}")
            print(f"Vertices: {metrics.get('vertices')}")
            
            memory = metrics.get('memory', {})
            if 'total' in memory:
                print(f"Memory: {memory.get('total') / (1024*1024):.2f} MB total, "
                      f"{memory.get('images', 0) / (1024*1024):.2f} MB images")
        else:
            print(f"Failed to get scene metrics: {response_data}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def start_live_preview():
    """Start the live preview server"""
    print("\nStarting live preview...")
    
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 9876))
        
        # Start live preview
        command = {
            "type": "start_live_preview",
            "params": {
                "port": 9877,
                "fps": 5
            }
        }
        
        print("Requesting live preview start...")
        client.sendall(json.dumps(command).encode('utf-8'))
        
        # Wait for response
        response = client.recv(8192).decode('utf-8')
        response_data = json.loads(response)
        
        if "result" in response_data and response_data.get("status") == "success":
            result = response_data["result"]
            print(f"Live preview started: {result.get('message')}")
            
            # Connect to preview server and receive a few frames
            preview_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            preview_client.connect(('localhost', result.get('port', 9877)))
            
            print("Connected to preview server. Receiving 3 frames...")
            for i in range(3):
                # Receive a frame
                frame_data = b''
                while True:
                    chunk = preview_client.recv(4096)
                    if not chunk:
                        break
                    
                    frame_data += chunk
                    if chunk.endswith(b'\n'):
                        break
                
                frame_json = json.loads(frame_data.decode('utf-8'))
                
                # Save the frame
                if "image" in frame_json:
                    img_data = base64.b64decode(frame_json["image"])
                    output_path = os.path.join(os.getcwd(), f"preview_frame_{i+1}.jpg")
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                    
                    print(f"Frame {i+1} saved to: {output_path}")
                else:
                    print(f"Frame {i+1}: No image data")
            
            preview_client.close()
            
            # Stop the preview
            stop_command = {
                "type": "stop_live_preview",
                "params": {}
            }
            
            print("Stopping live preview...")
            client.sendall(json.dumps(stop_command).encode('utf-8'))
            
            stop_response = client.recv(8192).decode('utf-8')
            stop_data = json.loads(stop_response)
            if "result" in stop_data and stop_data.get("status") == "success":
                print(f"Live preview stopped: {stop_data['result'].get('message')}")
            else:
                print(f"Failed to stop live preview: {stop_data}")
        else:
            print(f"Failed to start live preview: {response_data}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("BlenderMCP Enhanced Features Test")
    print("================================")
    print("Please make sure Blender is running with the enhanced BlenderMCP addon")
    print("and the MCP Server is started. Then press Enter to continue...")
    input()
    
    # Test viewport capture
    test_viewport_capture()
    
    # Test scene metrics
    test_scene_metrics()
    
    # Test live preview (optional)
    choice = input("\nDo you want to test the live preview feature? (y/n): ")
    if choice.lower() == 'y':
        start_live_preview()
    
    print("\nTest completed!") 