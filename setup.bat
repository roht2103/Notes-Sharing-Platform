@echo off
REM Digital Notes Platform - Quick Setup Script for Windows
REM This script automates the initial setup process

echo ========================================
echo Digital Notes Platform - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/7] Python detected successfully
echo.

REM Create virtual environment
if not exist "venv\" (
    echo [2/7] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo [2/7] Virtual environment already exists
)
echo.

REM Activate virtual environment and install dependencies
echo [3/7] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

REM Run migrations
echo [4/7] Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

REM Note about categories
echo [5/7] Categories setup...
echo Note: Run 'python manage.py shell < create_categories.py' after setup
echo to create sample categories, or create them via admin panel.
echo.

REM Prompt for superuser creation
echo [6/7] Create admin account
echo.
python manage.py createsuperuser
echo.

REM Final instructions
echo [7/7] Setup Complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Run the server:
echo    python manage.py runserver
echo.
echo 2. Visit: http://127.0.0.1:8000/
echo.
echo 3. Admin panel: http://127.0.0.1:8000/admin/
echo.
echo 4. Create categories via admin panel before uploading notes
echo ========================================
echo.
pause
