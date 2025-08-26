@echo off
echo 🎵 Starting ZumbaFit Pro Backend...
echo 📍 API will be available at: http://localhost:8000
echo 📚 API Documentation at: http://localhost:8000/docs
echo 🔄 Auto-reload enabled for development
echo ==================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then activate it and install requirements
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Start the server
python start_backend.py

pause
