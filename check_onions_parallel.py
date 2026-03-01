#!/usr/bin/env python3
"""
Onion URL Checker - Parallel version

Prerequisites (Ubuntu/Debian):
    1. Install Tor:
       sudo apt update
       sudo apt install tor -y
    
    2. Start Tor service:
       sudo systemctl start tor
       sudo systemctl enable tor
    
    3. Verify Tor is running:
       sudo systemctl status tor
       # Tor should be listening on 127.0.0.1:9050
    
    4. Install Python dependencies:
       pip3 install -r requirements.txt
       # Or manually:
       pip3 install requests PySocks

Usage:
    python check_onions_parallel.py --limit 100 --workers 10 --timeout 10
"""

import random
import string
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse

LOCK = threading.Lock()
OUTPUT_FILE = "accessible_onions.txt"


def generate_onion_url():
    # NOTE: truly valid .onion addresses are derived from keys, so
    # random generation will almost never hit a real service.
    return 'http://' + ''.join(random.choices(string.ascii_letters + string.digits, k=56)) + '.onion'


def check_onion_url(url, timeout=10):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        # verify=False because many onion services use self-signed certs (or none)
        response = requests.get(url, proxies=proxies, timeout=timeout, verify=False)
        # Accept any response that is not a client/server error
        if response.status_code < 400:
            return url
    except requests.RequestException:
        return None
    return None


def save_accessible_url(url):
    # Thread-safe append with explicit encoding
    with LOCK:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
            file.write(url + "\n")


def process_url(_index):
    onion_url = generate_onion_url()
    accessible_url = check_onion_url(onion_url)
    if accessible_url:
        save_accessible_url(accessible_url)
        print(f"{accessible_url} is accessible and saved.")
    else:
        # Keep this quiet if you prefer; printing all misses is noisy
        print(f"{onion_url} is not accessible.")


def check_tor_connection():
    """Verify that Tor is running and accessible."""
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        # Try to connect through Tor to check.torproject.org
        response = requests.get(
            'https://check.torproject.org/api/ip',
            proxies=proxies,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('IsTor'):
                print(f"✓ Tor connection verified! Your IP: {data.get('IP')}")
                return True
        print("✗ Connected but not through Tor")
        return False
    except ImportError as e:
        print(f"✗ Missing Python dependencies: {e}")
        print("\nPlease install required packages:")
        print("  pip3 install requests PySocks")
        print("  # or")
        print("  pip3 install -r requirements.txt")
        return False
    except requests.RequestException as e:
        error_msg = str(e)
        print(f"✗ Cannot connect to Tor proxy at 127.0.0.1:9050")
        
        if "SOCKS" in error_msg or "dependencies" in error_msg.lower():
            print("  Error: Missing SOCKS support")
            print("\nPlease install PySocks:")
            print("  pip3 install PySocks")
        else:
            print(f"  Error: {e}")
            print("\nPlease ensure Tor is installed and running:")
            print("  sudo apt update && sudo apt install tor -y")
            print("  sudo systemctl start tor")
            print("\nVerify Tor is listening:")
            print("  sudo systemctl status tor")
            print("  sudo netstat -tlnp | grep 9050")
        return False


def main():
    parser = argparse.ArgumentParser(description="Check onion urls in parallel (best-effort).")
    parser.add_argument("--limit", type=int, default=100, help="Number of random checks to perform")
    parser.add_argument("--workers", type=int, default=10, help="Number of concurrent worker threads")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument("--skip-tor-check", action="store_true", help="Skip Tor connection verification")
    args = parser.parse_args()

    # Verify Tor connection first
    if not args.skip_tor_check:
        print("Checking Tor connection...")
        if not check_tor_connection():
            print("\nExiting. Use --skip-tor-check to bypass this check.")
            return 1

    total = args.limit
    workers = args.workers
    timeout = args.timeout

    print(f"\nStarting: total={total}, workers={workers}, timeout={timeout}")
    print(f"Results will be saved to: {OUTPUT_FILE}\n")

    try:
        # Use executor.map to submit a bounded batch of tasks
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # map will block until all tasks are submitted and completed
            list(executor.map(lambda i: process_url(i), range(total)))
    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
    main()