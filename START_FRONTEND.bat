@echo off
echo ============================================================
echo PHISHING DETECTION SYSTEM - FRONTEND SERVER
echo ============================================================
echo.
echo Starting frontend server on http://localhost:8080
echo.
echo Make sure the backend API is running on http://localhost:8000
echo If not, open another terminal and run:
echo   cd backend
echo   python app.py
echo.
echo ============================================================
echo.

cd frontend
python -m http.server 8080
