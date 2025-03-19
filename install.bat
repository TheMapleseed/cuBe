@echo off
echo BlenderMCP Installer for Windows
echo ================================

:: Check for Python 3
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3 and try again.
    exit /b 1
)

:: Run the Python installer
python install_blendermcp.py

:: Check if the installation succeeded
if %ERRORLEVEL% NEQ 0 (
    echo BlenderMCP installation failed.
    exit /b 1
) else (
    echo BlenderMCP installation completed successfully!
)

pause 