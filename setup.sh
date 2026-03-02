#!/bin/bash
# Digital Notes Platform - Quick Setup Script for Linux/Mac
# This script automates the initial setup process

echo "========================================"
echo "Digital Notes Platform - Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.10+ from your package manager"
    exit 1
fi

echo "[1/7] Python detected successfully"
echo

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "[2/7] Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "[2/7] Virtual environment already exists"
fi
echo

# Activate virtual environment and install dependencies
echo "[3/7] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo

# Run migrations
echo "[4/7] Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo

# Create sample categories
echo "[5/7] Creating sample categories..."
echo "Note: You can create categories via admin panel"
echo

# Prompt for superuser creation
echo "[6/7] Create admin account"
echo
python manage.py createsuperuser
echo

# Final instructions
echo "[7/7] Setup Complete!"
echo
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo "1. Run the server:"
echo "   python manage.py runserver"
echo
echo "2. Visit: http://127.0.0.1:8000/"
echo
echo "3. Admin panel: http://127.0.0.1:8000/admin/"
echo
echo "4. Create categories via admin panel before uploading notes"
echo "========================================"
echo
