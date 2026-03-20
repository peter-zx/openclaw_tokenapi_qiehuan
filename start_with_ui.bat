@echo off
cd /d "%~dp0"
chcp 65001 >nul
title OpenClaw Model Switcher

setlocal enabledelayedexpansion

set "CURRENT_VERSION=1.0.0"
set "REPO_URL=https://github.com/peter-zx/openclaw_tokenapi_qiehuan"

echo.
echo ========================================
echo   OpenClaw Model Switcher v%CURRENT_VERSION%
echo ========================================
echo.

REM 检查更新提示
echo  [INFO] 当前版本: v%CURRENT_VERSION%
echo  [INFO] 检查更新: %REPO_URL%/releases
echo.

echo  [Step 1/6] Checking Python environment...

python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo  Please install Python 3.10+: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo  [OK] Python detected

echo.
echo  [Step 2/6] Checking for updates...

REM 尝试获取远程版本（如果 git 可用）
set "LATEST_VERSION="
for /f "delims=" %%i in ('git ls-remote --tags %REPO_URL% 2^>nul') do (
    set "LATEST_VERSION=%%i"
)

if defined LATEST_VERSION (
    echo  [INFO] 远程版本: !LATEST_VERSION!
) else (
    echo  [INFO] 无法检测远程版本，请手动检查更新
)

echo.
echo  [Step 3/6] Setting up virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo  [INFO] Creating venv...
    python -m venv venv
)
echo  [OK] Virtual environment ready

echo.
echo  [Step 4/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo  [OK] Virtual environment activated

echo.
echo  [Step 5/6] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo  [INFO] Installing dependencies...
    pip install -r backend\requirements.txt
)
echo  [OK] Dependencies ready

echo.
echo  [Step 6/6] Starting service...
echo.

if not exist "backend\start.py" (
    echo  [ERROR] backend\start.py not found
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

"venv\Scripts\python.exe" "backend\start.py"
