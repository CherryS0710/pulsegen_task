#!/bin/bash

# Start Frontend Server
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting frontend server on http://localhost:3000"
npm run dev


