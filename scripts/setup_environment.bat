@echo off
echo 🎵 ZumbaFit Pro Environment Setup
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python detected
python --version

REM Run the setup script
echo.
echo 🔄 Running setup script...
python setup_environment.py

if errorlevel 1 (
    echo ❌ Setup failed
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Start backend: python start_backend.py
echo 3. Start frontend: python start_frontend.py
echo.
pause
