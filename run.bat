@echo off
REM Quick Run Script for Digital Notes Platform

echo ========================================
echo Digital Notes Platform
echo ========================================
echo.
echo Select an option:
echo 1. Run Development Server
echo 2. Create Superuser
echo 3. Make Migrations
echo 4. Apply Migrations
echo 5. Open Django Shell
echo 6. Create Sample Categories
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo.
    echo Starting development server...
    echo Visit http://127.0.0.1:8000/
    echo Press Ctrl+C to stop the server
    echo.
    call venv\Scripts\activate.bat
    python manage.py runserver
)

if "%choice%"=="2" (
    echo.
    echo Creating superuser account...
    call venv\Scripts\activate.bat
    python manage.py createsuperuser
    pause
)

if "%choice%"=="3" (
    echo.
    echo Making migrations...
    call venv\Scripts\activate.bat
    python manage.py makemigrations
    pause
)

if "%choice%"=="4" (
    echo.
    echo Applying migrations...
    call venv\Scripts\activate.bat
    python manage.py migrate
    pause
)

if "%choice%"=="5" (
    echo.
    echo Opening Django shell...
    call venv\Scripts\activate.bat
    python manage.py shell
)

if "%choice%"=="6" (
    echo.
    echo Creating sample categories...
    call venv\Scripts\activate.bat
    python manage.py shell < create_categories.py
    pause
)

if "%choice%"=="7" (
    exit
)

echo.
echo Invalid choice. Please run the script again.
pause
