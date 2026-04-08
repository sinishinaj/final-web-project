#!/bin/bash
set -e

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete! Run tests with:"
echo "  source venv/bin/activate"
echo "  pytest st12345678_py_test.py -v"
