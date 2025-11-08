@echo off
echo ============================================================
echo PHISHING DETECTION SYSTEM - COMPLETE STARTUP
echo ============================================================
echo.
echo This will start both the backend API and frontend server
echo.
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo Press Ctrl+C to stop the servers
echo ============================================================
echo.

set SCRIPT_DIR=%~dp0
start "Backend API" cmd /k "cd /d "%SCRIPT_DIR%backend" && python app.py"
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd /d "%SCRIPT_DIR%frontend" && python -m http.server 8080"

echo.
echo Both servers are starting...
echo.
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo Open your browser and go to: http://localhost:8080
echo.
pause
