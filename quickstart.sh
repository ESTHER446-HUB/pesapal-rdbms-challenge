#!/bin/bash

echo "=========================================="
echo "Pesapal RDBMS Challenge - Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
echo ""

# Run tests
echo "=========================================="
echo "Running RDBMS Tests..."
echo "=========================================="
python3 test_rdbms.py
echo ""

# Prompt for next steps
echo "=========================================="
echo "What would you like to do next?"
echo "=========================================="
echo "1. Start Interactive REPL: python3 rdbms.py"
echo "2. Start Web Application: python3 app.py"
echo "3. Run tests again: python3 test_rdbms.py"
echo ""
echo "For the web app, visit: http://localhost:5000"
echo ""
