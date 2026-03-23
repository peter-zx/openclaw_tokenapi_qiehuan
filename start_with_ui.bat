@echo off
cd /d "%~dp0"
chcp 65001 >nul
title OpenClaw Model Switcher

REM Helper function to check Node.js
:check_nodejs
node --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Node.js not found!
    echo  Please install Node.js: https://nodejs.org/
    pause
    exit /b 1
)
echo  [OK] Node.js detected
exit /b 0

setlocal enabledelayedexpansion
set "CURRENT_VERSION=1.1.0"
set "REPO_OWNER=peter-zx"
set "REPO_NAME=openclaw_tokenapi_qiehuan"
set "REPO_URL=https://github.com/%REPO_OWNER%/%REPO_NAME%"
set "API_URL=https://api.github.com/repos/%REPO_OWNER%/%REPO_NAME%/releases/latest"

echo.
echo ========================================
echo   OpenClaw Model Switcher v%CURRENT_VERSION%
echo ========================================
echo.

echo  [Step 1/7] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo  Please install Python 3.10+: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo  [OK] Python detected

echo.
echo  [Step 2/7] Checking for updates...
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri '%API_URL%' -UseBasicParsing -TimeoutSec 10; $j = $r.Content | ConvertFrom-Json; Write-Host ('LATEST:' + $j.tag_name) } catch { Write-Host 'ERROR' }" > "%TEMP%\gh_ver.tmp" 2>nul

set "LATEST_TAG="
for /f "tokens=2" %%a in ('type "%TEMP%\gh_ver.tmp"') do set "LATEST_TAG=%%a"
del /f /q "%TEMP%\gh_ver.tmp" 2>nul

set "LATEST_TAG=!LATEST_TAG: =!"
set "LATEST_VERSION=!LATEST_TAG!"
if "!LATEST_TAG:~0,1!"=="v" set "LATEST_VERSION=!LATEST_TAG:~1!"

if "!LATEST_TAG!"=="ERROR" (
    echo  [WARN] Unable to check remote version
) else (
    echo  [INFO] Current: v%CURRENT_VERSION%  Latest: !LATEST_TAG!
    if not "!LATEST_VERSION!"=="%CURRENT_VERSION%" (
        echo  [INFO] New version available: !REPO_URL!/releases
    ) else (
        echo  [OK] Already up to date
    )
)

echo.
echo  [Step 3/7] Setting up virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo  [INFO] Creating venv...
    python -m venv venv
)
echo  [OK] Virtual environment ready

echo.
echo  [Step 4/7] Activating virtual environment...
call venv\Scripts\activate.bat
echo  [OK] Virtual environment activated

echo.
echo  [Step 5/7] Checking frontend build...
if not exist "frontend\dist\index.html" (
    echo  [INFO] Frontend not built, installing dependencies...
    call :check_nodejs || exit /b 1
    cd frontend
    call npm install
    if errorlevel 1 (
        echo  [ERROR] npm install failed
        pause
        exit /b 1
    )
    echo  [INFO] Building frontend...
    call npm run build
    if errorlevel 1 (
        echo  [ERROR] npm build failed
        pause
        exit /b 1
    )
    cd ..
    echo  [OK] Frontend built
) else (
    echo  [OK] Frontend already built
)

echo.
echo  [Step 6/7] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo  [INFO] Installing dependencies...
    pip install -r backend\requirements.txt
)
echo  [OK] Dependencies ready

echo.
echo  [Step 7/7] Starting service...

if not exist "backend\start.py" (
    echo  [ERROR] backend\start.py not found
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Service starting...
echo.
echo   Web UI: http://127.0.0.1:9131
echo   Press CTRL+C to stop
echo ========================================
echo.

start http://127.0.0.1:9131

"venv\Scripts\python.exe" "backend\start.py"
pause
