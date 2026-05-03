@echo off
echo ========================================
echo Starting Automated Assignment Grading System
echo ========================================
echo.

REM Check if Ollama is running
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama does not appear to be running
    echo Please start Ollama and ensure the llama3:8b model is downloaded
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

echo Running the grading system...
echo.

python main.py

echo.
echo ========================================
echo Grading Complete!
echo Check the logs/ directory for details
echo ========================================
pause
