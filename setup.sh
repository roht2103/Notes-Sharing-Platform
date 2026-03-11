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

# Create media directory
echo "[4/8] Creating media directories..."
mkdir -p media/notes
echo "Media directories created"
echo

# Run migrations
echo "[5/8] Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo

# Create sample categories
echo "[6/8] Creating sample categories..."
python manage.py shell < create_categories.py
echo "Categories created successfully"
echo

# Prompt for superuser creation
echo "[7/8] Create admin account"
echo "You can create a custom admin or use default (admin/admin123)"
echo
read -p "Create custom admin? (y/N): " CREATE_CUSTOM
if [[ "$CREATE_CUSTOM" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
else
    python manage.py create_default_admin
    echo "Default admin created: username=admin, password=admin123"
fi
echo

# Final instructions
echo "[8/8] Setup Complete!"
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
