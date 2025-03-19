#!/bin/bash

echo "BlenderMCP Installer for macOS/Linux"
echo "===================================="

# Check for Python 3
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null && [[ $(python --version 2>&1) == *"Python 3"* ]]; then
    PYTHON=python
else
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Make sure the installer script is executable
chmod +x install_blendermcp.py

# Run the Python installer
$PYTHON install_blendermcp.py

# Check if the installation succeeded
if [ $? -eq 0 ]; then
    echo "BlenderMCP installation completed successfully!"
else
    echo "BlenderMCP installation failed."
    exit 1
fi 