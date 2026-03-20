@echo off
cd /d "%~dp0"
chcp 65001 >nul
title OpenClaw Backend Dev Mode

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   OpenClaw Backend Dev Mode
echo ========================================
echo.

echo  [Step 1/5] Cleaning up old processes...

echo  [INFO] Killing node.exe processes...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo  [INFO] Running OpenClaw gateway cleanup...
openclaw gateway >nul 2>&1
timeout /t 8 /nobreak >nul
echo  [OK] Cleanup complete

echo.
echo  [Step 2/5] Setting up virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo  [INFO] Creating venv...
    python -m venv venv
)
echo  [OK] Virtual environment ready

echo.
echo  [Step 3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo  [OK] Virtual environment activated

echo.
echo  [Step 4/5] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo  [INFO] Installing dependencies...
    pip install -r backend\requirements.txt
)
echo  [OK] Dependencies ready

echo.
echo  [Step 5/5] Starting backend in DEV mode (with auto-reload)...
echo.

REM 打开浏览器
start http://127.0.0.1:9131

echo.
echo ========================================
echo   Backend Dev Mode
echo.
echo   Web UI: http://127.0.0.1:9131
echo   API Docs: http://127.0.0.1:9131/docs
echo.
echo   Press CTRL+C to stop
echo ========================================
echo.

REM 使用 uvicorn 的 reload 模式进行开发
"venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 9131 --reload --log-level info
