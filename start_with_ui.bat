@echo off
cd /d "%~dp0"
chcp 65001 >nul
title OpenClaw Model Switcher

set PROJECT_DIR=%~dp0openclaw-manager

echo.
echo ========================================
echo   OpenClaw Model Switcher
echo ========================================
echo.
echo  [Step 1/5] Checking Python environment...

python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo  Please install Python 3.10+: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo  [OK] Python detected

echo.
echo  [Step 2/5] Setting up virtual environment...
if not exist "%PROJECT_DIR%\venv\Scripts\python.exe" (
    echo  [INFO] Creating venv...
    python -m venv "%PROJECT_DIR%\venv"
)
echo  [OK] Virtual environment ready

echo.
echo  [Step 3/5] Activating virtual environment...
call "%PROJECT_DIR%\venv\Scripts\activate.bat"
echo  [OK] Virtual environment activated

echo.
echo  [Step 4/5] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo  [INFO] Installing dependencies...
    pip install -r "%PROJECT_DIR%\backend\requirements.txt"
)
echo  [OK] Dependencies ready

echo.
echo  [Step 5/5] Starting service...
echo.

if not exist "%PROJECT_DIR%\backend\main.py" (
    echo  [ERROR] backend\main.py not found
    pause
    exit /b 1
)

REM Open browser
start http://127.0.0.1:9131

echo.
echo ========================================
echo   Service starting...
echo.
echo   Web UI: http://127.0.0.1:9131
echo   Press CTRL+C to stop
echo ========================================
echo.

"%PROJECT_DIR%\venv\Scripts\python.exe" "%PROJECT_DIR%\backend\main.py"
