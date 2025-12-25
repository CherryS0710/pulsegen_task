#!/bin/bash

# Start Backend Server
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
    touch venv/.dependencies_installed
fi

# Check for .env file
if [ ! -f "../.env" ]; then
    echo "Warning: .env file not found. Please create one from .env.example"
    echo "The server will start but API calls will fail without OPENAI_API_KEY"
fi

echo "Starting backend server on http://localhost:8000"
uvicorn main:app --reload --host 0.0.0.0 --port 8000


