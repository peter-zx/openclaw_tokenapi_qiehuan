#!/bin/bash
cd "$(dirname "$0")"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found"
    exit 1
fi

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r backend/requirements.txt

# Start server
echo "Starting OpenClaw Model Switcher..."
echo "Access: http://127.0.0.1:9131"
python backend/main.py
