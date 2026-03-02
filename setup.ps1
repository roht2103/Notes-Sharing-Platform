# Digital Notes Platform - Setup Script for PowerShell
# This script automates the initial setup process

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Digital Notes Platform - Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/7] Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "[2/7] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "[2/7] Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment and install dependencies
Write-Host "[3/7] Installing dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
pip install -r requirements.txt
Write-Host ""

# Run migrations
Write-Host "[4/7] Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
Write-Host ""

# Note about categories
Write-Host "[5/7] Categories setup..." -ForegroundColor Yellow
Write-Host "Note: Run 'python manage.py shell < create_categories.py' after setup" -ForegroundColor Cyan
Write-Host "to create sample categories, or create them via admin panel." -ForegroundColor Cyan
Write-Host ""

# Prompt for superuser creation
Write-Host "[6/7] Create admin account" -ForegroundColor Yellow
Write-Host ""
python manage.py createsuperuser
Write-Host ""

# Final instructions
Write-Host "[7/7] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Create sample categories:" -ForegroundColor White
Write-Host "   python manage.py shell < create_categories.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Run the server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Visit: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host ""
Write-Host "4. Admin panel: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"
