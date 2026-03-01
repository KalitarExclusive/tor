# Installation Guide for Ubuntu

This guide will help you set up the Onion URL Checker on Ubuntu/Debian systems.

## Prerequisites

- Ubuntu/Debian Linux
- Python 3.6 or higher
- Internet connection
- sudo privileges

## Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

This will:
1. Update package lists
2. Install Tor
3. Start and enable Tor service
4. Install Python dependencies
5. Verify the installation

## Option 2: Manual Setup

### Step 1: Install Tor

```bash
sudo apt update
sudo apt install tor -y
sudo systemctl start tor
sudo systemctl enable tor
```

### Step 2: Verify Tor is Running

```bash
sudo systemctl status tor
```

You should see "active (running)" in the output.

### Step 3: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

Or install individually:

```bash
pip3 install requests PySocks
```

### Step 4: Test the Setup

```bash
python3 test_setup.py
```

## Common Issues and Fixes

### Issue 1: "Missing dependencies for SOCKS support"

This means PySocks is not properly installed.

**Fix:**
```bash
chmod +x fix_dependencies.sh
./fix_dependencies.sh
```

Or manually:
```bash
pip3 install --upgrade pip
pip3 install --force-reinstall requests PySocks
```

### Issue 2: "Cannot connect to Tor proxy at 127.0.0.1:9050"

This means Tor is not running or not listening on the correct port.

**Fix:**
```bash
# Check if Tor is running
sudo systemctl status tor

# If not running, start it
sudo systemctl start tor

# Check if port 9050 is listening
sudo netstat -tlnp | grep 9050
# or
sudo ss -tlnp | grep 9050
```

### Issue 3: Tor service fails to start

**Fix:**
```bash
# Check Tor logs
sudo journalctl -u tor -n 50

# Try restarting
sudo systemctl restart tor

# If still failing, reinstall Tor
sudo apt remove tor -y
sudo apt install tor -y
sudo systemctl start tor
```

### Issue 4: pip3 not found

**Fix:**
```bash
sudo apt update
sudo apt install python3-pip -y
```

## Verification

After installation, run the test script:

```bash
python3 test_setup.py
```

You should see:
```
✓ requests installed
✓ PySocks installed
✓ Tor connection working! IP: [some IP address]
✅ All tests passed! You're ready to go.
```

## Running the Script

Once everything is set up:

```bash
# Basic usage
python3 check_onions_parallel.py --limit 100

# With custom settings
python3 check_onions_parallel.py --limit 500 --workers 20 --timeout 15

# Quick test
python3 check_onions_parallel.py --limit 10 --workers 5
```

## Useful Commands

```bash
# Check Tor status
sudo systemctl status tor

# Start Tor
sudo systemctl start tor

# Stop Tor
sudo systemctl stop tor

# Restart Tor
sudo systemctl restart tor

# View Tor logs
sudo journalctl -u tor -f

# Check if port 9050 is open
sudo netstat -tlnp | grep 9050
```

## Getting Help

If you encounter issues:

1. Run the test script: `python3 test_setup.py`
2. Check Tor status: `sudo systemctl status tor`
3. Check Tor logs: `sudo journalctl -u tor -n 50`
4. Verify Python packages: `pip3 list | grep -E "requests|PySocks"`

## Security Notes

- Tor provides anonymity but not complete security
- Be cautious when accessing unknown .onion sites
- Random generation rarely finds real services
- Consider using known onion lists for better results
