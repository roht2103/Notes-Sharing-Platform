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

REM Create media directory
if not exist "media\notes" (
    echo [4/8] Creating media directories...
    mkdir media\notes
    echo Media directories created
) else (
    echo [4/8] Media directories already exist
)
echo.

REM Run migrations
echo [5/8] Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

REM Create categories
echo [6/8] Creating categories...
python manage.py shell < create_categories.py
echo Categories created successfully
echo.

REM Prompt for superuser creation
echo [7/8] Create admin account
echo You can create a custom admin or use default (admin/admin123)
echo.
set /p CREATE_CUSTOM="Create custom admin? (Y/N, default is N for admin/admin123): "
if /i "%CREATE_CUSTOM%"=="Y" (
    python manage.py createsuperuser
) else (
    python manage.py create_default_admin
    echo Default admin created: username=admin, password=admin123
)
echo.

REM Final instructions
echo [8/8] Setup Complete!
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
