@echo off
echo ================================================
echo Creative Portfolio Bot - Setup Script
echo ================================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)

echo [2/4] Installing Python dependencies...
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo [3/4] Installing Playwright browser...
venv\Scripts\python.exe -m playwright install chromium
if errorlevel 1 (
    echo ERROR: Failed to install Playwright browser
    exit /b 1
)

echo [4/4] Running tests...
echo n | venv\Scripts\python.exe test_components.py
if errorlevel 1 (
    echo WARNING: Tests failed, but setup is complete
) else (
    echo Tests passed!
)

echo.
echo ================================================
echo Setup complete!
echo ================================================
echo.
echo Next steps:
echo 1. Configure .env file with your tokens
echo 2. Run: venv\Scripts\python.exe bot.py
echo.
pause
