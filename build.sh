#!/bin/bash
# build.sh - Render build script

# Upgrade pip first
python -m pip install --upgrade pip

# Install build dependencies
pip install setuptools wheel Cython

# Install requirements
pip install -r requirements.txt

echo "Build completed successfully"