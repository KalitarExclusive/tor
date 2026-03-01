#!/bin/bash
# Setup script for Onion URL Checker on Ubuntu/Debian

set -e

echo "=========================================="
echo "Onion URL Checker - Ubuntu Setup"
echo "=========================================="
echo ""

# Check if running on Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo "Error: This script is for Ubuntu/Debian systems only"
    exit 1
fi

# Update package list
echo "[1/5] Updating package list..."
sudo apt update

# Install Tor
echo "[2/5] Installing Tor..."
if command -v tor &> /dev/null; then
    echo "  Tor is already installed"
else
    sudo apt install tor -y
fi

# Start and enable Tor service
echo "[3/5] Starting Tor service..."
sudo systemctl start tor
sudo systemctl enable tor

# Wait a moment for Tor to initialize
sleep 2

# Check Tor status
echo "[4/5] Checking Tor status..."
if sudo systemctl is-active --quiet tor; then
    echo "  ✓ Tor is running"
else
    echo "  ✗ Tor failed to start"
    sudo systemctl status tor
    exit 1
fi

# Install Python dependencies
echo "[5/5] Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "  Warning: pip not found. Please install Python dependencies manually:"
    echo "  pip install -r requirements.txt"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "You can now run the script:"
echo "  python3 check_onions_parallel.py --limit 100 --workers 10"
echo ""
echo "Useful commands:"
echo "  Check Tor status:  sudo systemctl status tor"
echo "  Stop Tor:          sudo systemctl stop tor"
echo "  Start Tor:         sudo systemctl start tor"
echo "  Restart Tor:       sudo systemctl restart tor"
echo ""
