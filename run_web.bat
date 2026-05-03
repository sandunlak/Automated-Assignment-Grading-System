@echo off
echo ========================================
echo Starting Web Interface
echo Automated Assignment Grading System
echo ========================================
echo.

REM Check if Streamlit is installed
streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Streamlit is not installed
    echo Installing Streamlit...
    pip install streamlit pandas
)

echo Starting Streamlit application...
echo.
echo The web interface will open in your browser automatically.
echo If it doesn't, visit: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run web_app.py --server.headless true

pause
