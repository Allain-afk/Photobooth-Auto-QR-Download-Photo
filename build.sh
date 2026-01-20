#!/bin/bash
# Build script for bash/Git Bash on Windows

echo "========================================"
echo "Building Photobooth EXE"
echo "========================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found!"
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Use python or python3, whichever is available
if command -v python &> /dev/null; then
    PYTHON=python
else
    PYTHON=python3
fi

echo "Using: $PYTHON"
echo ""

# Run the Python build script
$PYTHON build.py

# Check if build was successful
if [ -f "dist/Photobooth-QR.exe" ]; then
    echo ""
    echo "✓ Build successful!"
    echo "✓ EXE location: dist/Photobooth-QR.exe"
else
    echo ""
    echo "✗ Build failed - EXE not found"
    exit 1
fi
