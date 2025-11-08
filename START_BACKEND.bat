@echo off
echo ============================================================
echo PHISHING DETECTION SYSTEM - BACKEND API
echo ============================================================
echo.
echo Starting backend API on http://localhost:8000
echo.
echo Keep this window open!
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%backend"
python app.py

pause
