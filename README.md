# Onion URL Finder

Onion URL Finder is a Python script that generates random .onion URLs and checks their accessibility using the Tor network. Accessible URLs are saved to a file.

## Requirements

- Python 3.x
- Tor

## Quick Start

After cloning the repository:

```sh
# Make scripts executable
chmod +x setup_ubuntu.sh fix_dependencies.sh

# Run automated setup
./setup_ubuntu.sh

# If you get SOCKS dependency errors, run:
./fix_dependencies.sh

# Test your setup
python3 test_setup.py

# Start checking onion URLs
python3 check_onions_parallel.py --limit 10
```

## Installation

### Quick Setup (Ubuntu/Debian)

Run the automated setup script:

```sh
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

This will automatically install Tor, start the service, and install Python dependencies.

### Manual Installation

#### Step 1: Clone the repository

```sh
git clone https://github.com/PASSW0RDZ/OnionV3-Link-Generator.git
cd OnionV3-Link-Generator
```

#### Step 2: Install Tor

On Ubuntu/Debian:

```sh
sudo apt update
sudo apt install tor -y
sudo systemctl start tor
sudo systemctl enable tor
```

Verify Tor is running:

```sh
sudo systemctl status tor
# Tor should be listening on 127.0.0.1:9050
```

#### Step 3: Install Python packages

Make sure you have Python 3 and `pip` installed. Then, install the required Python packages:

```sh
pip3 install -r requirements.txt
```

Or install packages individually:

```sh
pip3 install requests PySocks
```

#### Step 4: Verify Installation

Run the test script to verify everything is working:

```sh
python3 test_setup.py
```

This will check if Tor is running and Python dependencies are properly installed.

## Usage

The script will automatically verify your Tor connection before starting. Run it with optional command-line arguments:

```sh
python3 check_onions_parallel.py --limit 100 --workers 10 --timeout 10
```

### Command-line Options

- `--limit`: Number of onion URLs to check (default: 100)
- `--workers`: Number of parallel worker threads (default: 10)
- `--timeout`: Timeout in seconds for each URL check (default: 10)
- `--skip-tor-check`: Skip Tor connection verification (not recommended)

### Examples

Check 500 URLs with 20 workers:
```sh
python3 check_onions_parallel.py --limit 500 --workers 20
```

Quick test with 10 URLs:
```sh
python3 check_onions_parallel.py --limit 10 --workers 5
```

The script generates and checks onion URLs based on these parameters. Results are written to `accessible_onions.txt` in a thread-safe manner using UTF-8 encoding.

## Configuration

### Logging

The script prints the status of each URL (whether it is accessible or not) to the console. Accessible URLs are also saved to `accessible_onions.txt`.

## Troubleshooting

### Tor Connection Issues

If you get a connection error:

1. Check if Tor is running:
   ```sh
   sudo systemctl status tor
   ```

2. Restart Tor if needed:
   ```sh
   sudo systemctl restart tor
   ```

3. Verify Tor is listening on port 9050:
   ```sh
   sudo netstat -tlnp | grep 9050
   # or
   sudo ss -tlnp | grep 9050
   ```

### Python Dependencies

If you get "Missing dependencies for SOCKS support" error:

```sh
pip3 install --upgrade pip
pip3 install --force-reinstall requests PySocks
```

Verify the installation:
```sh
python3 test_setup.py
```

If you encounter import errors, reinstall dependencies:
```sh
pip3 install --upgrade -r requirements.txt
```

## Notes

- The script automatically verifies Tor connectivity before starting
- Random onion generation is unlikely to find real services; it is more effective to provide known onion lists for checking
- The script may consume significant CPU and network resources depending on the number of threads used
- Accessible URLs are saved to `accessible_onions.txt` with thread-safe file operations

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.
