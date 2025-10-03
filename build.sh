#!/bin/bash
# build.sh - Render build script with explicit Python version handling

set -e  # Exit on error

echo "🚀 Starting build process..."

# Ensure we're using Python 3.11
python --version

# Upgrade pip and install build tools separately
echo "📦 Installing build tools..."
python -m pip install --upgrade pip
pip install setuptools>=70.0.0 wheel>=0.41.0

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Build completed successfully"