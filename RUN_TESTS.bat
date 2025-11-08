@echo off
echo ============================================================
echo PHISHING DETECTION SYSTEM - AUTOMATED TEST SUITE
echo ============================================================
echo.

cd backend

echo [1/4] Running Feature Extraction Tests...
echo ------------------------------------------------------------
python test_features.py
if %errorlevel% neq 0 (
    echo FAILED: Feature extraction tests
    pause
    exit /b 1
)
echo.

echo [2/4] Running ML Model Tests...
echo ------------------------------------------------------------
python test_model.py
if %errorlevel% neq 0 (
    echo FAILED: ML model tests
    pause
    exit /b 1
)
echo.

echo [3/4] Running API Component Tests...
echo ------------------------------------------------------------
python test_api_simple.py
if %errorlevel% neq 0 (
    echo FAILED: API component tests
    pause
    exit /b 1
)
echo.

echo [4/4] All Tests Completed!
echo ============================================================
echo.
echo TEST SUMMARY:
echo   Feature Extraction: PASSED
echo   ML Model: PASSED
echo   API Components: PASSED
echo.
echo Overall Status: ALL TESTS PASSED
echo ============================================================
echo.
echo To test the live API server:
echo   1. Run: python app.py
echo   2. In another terminal: python test_live_api.py
echo.
pause
