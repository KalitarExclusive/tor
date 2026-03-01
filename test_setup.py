#!/usr/bin/env python3
"""
Quick test script to verify Tor and Python dependencies are properly installed.
"""

import sys

def test_imports():
    """Test if required Python packages are installed."""
    print("Testing Python dependencies...")
    try:
        import requests
        print("  ✓ requests installed")
    except ImportError:
        print("  ✗ requests not installed")
        print("    Install: pip3 install requests")
        return False
    
    try:
        import socks
        print("  ✓ PySocks installed")
    except ImportError:
        print("  ✗ PySocks not installed")
        print("    Install: pip3 install PySocks")
        return False
    
    return True

def test_tor_connection():
    """Test if Tor is running and accessible."""
    print("\nTesting Tor connection...")
    import requests
    
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    
    try:
        response = requests.get(
            'https://check.torproject.org/api/ip',
            proxies=proxies,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('IsTor'):
                print(f"  ✓ Tor connection working! IP: {data.get('IP')}")
                return True
            else:
                print("  ✗ Connected but not through Tor")
                return False
    except Exception as e:
        print(f"  ✗ Cannot connect to Tor: {e}")
        print("\n  Troubleshooting:")
        print("    1. Check if Tor is running: sudo systemctl status tor")
        print("    2. Start Tor: sudo systemctl start tor")
        print("    3. Check port 9050: sudo netstat -tlnp | grep 9050")
        return False

def main():
    print("=" * 50)
    print("Tor Setup Verification")
    print("=" * 50)
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Python dependencies missing. Run:")
        print("   pip3 install -r requirements.txt")
        sys.exit(1)
    
    # Test Tor
    if not test_tor_connection():
        print("\n❌ Tor connection failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! You're ready to go.")
    print("=" * 50)
    print("\nRun the main script:")
    print("  python3 check_onions_parallel.py --limit 10")

if __name__ == "__main__":
    main()
