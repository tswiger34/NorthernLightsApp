#!/bin/bash

echo "Starting build process..."

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Building executable file..."
pyinstaller --onefile --name="NorthernLightsApp" --icon="app/gui/PorscheNorthernLightsSmall.ico" app/run.py

echo "Build process completed!"