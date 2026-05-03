@echo off
echo ========================================
echo Automated Assignment Grading System
echo Setup and Installation Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python detected successfully
echo.

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama is not installed or not in PATH
    echo Please install Ollama from https://ollama.ai/
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
) else (
    echo [2/4] Ollama detected
)

echo.
echo [3/4] Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/4] Setup complete!
echo.
echo Next steps:
echo 1. Make sure Ollama is running
echo 2. Pull the llama3:8b model: ollama pull llama3:8b
echo 3. Run the system: python main.py
echo.
pause
