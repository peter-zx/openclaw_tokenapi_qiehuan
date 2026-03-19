@echo off
cd /d "%~dp0"
chcp 65001 >nul
title OpenClaw Model Switcher

echo ========================================
echo OpenClaw Model Switcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ first:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python detected
for /f "delims=" %%i in ('python --version') do set PY_VERSION=%%i
echo      %PY_VERSION%
echo.

REM Check if virtual environment exists, create if not
if not exist "venv\Scripts\python.exe" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Check and install dependencies
echo [INFO] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r backend\requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)
echo.

REM Check backend program
if not exist "backend\main.py" (
    echo [ERROR] Backend program not found
    pause
    exit /b 1
)

REM Check port availability
netstat -ano | findstr :9131 >nul
if not errorlevel 1 (
    echo [WARNING] Port 9131 is already in use
    echo Please stop the existing service or wait...
    echo.
)

REM Open browser
echo [INFO] Opening web browser...
start http://127.0.0.1:9131

REM Start service
echo.
echo ========================================
echo Starting service...
echo Please visit: http://127.0.0.1:9131
echo Press CTRL+C to stop
echo ========================================
echo.

"venv\Scripts\python.exe" "backend\main.py"
