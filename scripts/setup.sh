#!/bin/bash
# Environment setup script for Sentience Layer.

echo "Setting up development environment..."

# Check dependencies
echo "Checking Python version..."
python --version

echo "Checking Node.js version..."
node --version

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Node dependencies..."
npm run install:all

echo "Setup complete! Run 'npm run dev' to start."
