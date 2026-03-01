#!/bin/bash
# Quick fix script for "Missing dependencies for SOCKS support" error

echo "=========================================="
echo "Fixing SOCKS Dependencies"
echo "=========================================="
echo ""

# Upgrade pip
echo "[1/3] Upgrading pip..."
pip3 install --upgrade pip

# Force reinstall packages
echo "[2/3] Reinstalling packages..."
pip3 install --force-reinstall requests PySocks

# Verify installation
echo "[3/3] Verifying installation..."
python3 -c "import requests, socks; print('✓ All packages imported successfully')" && {
    echo ""
    echo "=========================================="
    echo "✅ Fix complete!"
    echo "=========================================="
    echo ""
    echo "Test your setup:"
    echo "  python3 test_setup.py"
    echo ""
    echo "Run the main script:"
    echo "  python3 check_onions_parallel.py --limit 10"
} || {
    echo ""
    echo "=========================================="
    echo "❌ Fix failed"
    echo "=========================================="
    echo ""
    echo "Try manual installation:"
    echo "  pip3 install --user requests PySocks"
    echo ""
    echo "Or use system package manager:"
    echo "  sudo apt install python3-requests python3-socks"
}
