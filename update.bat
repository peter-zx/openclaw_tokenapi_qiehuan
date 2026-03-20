@echo off
cd /d "%~dp0"
chcp 65001 >nul
title OpenClaw Auto Update

setlocal enabledelayedexpansion

set "CURRENT_VERSION=1.0.0"
set "REPO_OWNER=peter-zx"
set "REPO_NAME=openclaw_tokenapi_qiehuan"
set "API_URL=https://api.github.com/repos/%REPO_OWNER%/%REPO_NAME%/releases/latest"
set "REPO_URL=https://github.com/%REPO_OWNER%/%REPO_NAME%"

echo.
echo ========================================
echo   OpenClaw Update Tool
echo ========================================
echo.

echo  [INFO] 当前版本: v%CURRENT_VERSION%
echo.

echo  [Step 1/3] 获取最新版本信息...

REM 使用 PowerShell 获取最新 release 信息
powershell -NoProfile -Command "try { $resp = Invoke-WebRequest -Uri '%API_URL%' -UseBasicParsing -TimeoutSec 15; $json = $resp.Content | ConvertFrom-Json; Write-Output ('TAG:' + $json.tag_name); Write-Output ('URL:' + $json.html_url); Write-Output ('ZIP:' + $json.zipball_url) } catch { Write-Output 'ERROR' }" > "%TEMP%\github_release.txt" 2>nul

set "LATEST_TAG="
set "DOWNLOAD_PAGE="
set "ZIP_URL="

for /f "tokens=1,* delims=: " %%a in ('type "%TEMP%\github_release.txt"') do (
    if "%%a"=="TAG" set "LATEST_TAG=%%b"
    if "%%a"=="URL" set "DOWNLOAD_PAGE=%%b"
    if "%%a"=="ZIP" set "ZIP_URL=%%b"
)

REM 清理临时文件
del /f /q "%TEMP%\github_release.txt" 2>nul

REM 清理版本号前面的 v
set "LATEST_VERSION=%LATEST_TAG%"
if "%LATEST_TAG:~0,1%"=="v" set "LATEST_VERSION=%LATEST_TAG:~1%"

if "%LATEST_TAG%"=="" (
    echo  [ERROR] 无法连接 GitHub，请检查网络
    echo  [INFO] 请手动访问: %REPO_URL%/releases
    pause
    exit /b 1
)

echo  [INFO] 最新版本: %LATEST_TAG%
echo.

REM 版本比较
if "%LATEST_VERSION%"=="%CURRENT_VERSION%" (
    echo  *********************************************
    echo  * 恭喜！您已使用最新版本！
    echo  *********************************************
    echo.
    pause
    exit /b 0
)

echo  *********************************************
echo  * 发现新版本！
echo  *********************************************
echo.
echo  当前版本: v%CURRENT_VERSION%
echo  最新版本: %LATEST_TAG%
echo.

choice /c YNC /m "是否下载最新版本? (Y=下载更新 N=查看下载地址 C=取消)"
if errorlevel 3 (
    echo  [INFO] 已取消更新
    exit /b 0
)
if errorlevel 2 (
    echo  [INFO] 正在打开下载页面...
    start %DOWNLOAD_PAGE%
    echo  [INFO] 请手动下载最新版本
    pause
    exit /b 0
)

echo.
echo  [Step 2/3] 正在准备下载...

REM 创建更新目录
if not exist "update_temp" mkdir update_temp

echo  [INFO] 下载地址: %DOWNLOAD_PAGE%
echo  [INFO] 请手动下载最新版本的 Source code (zip)
echo.
echo  下载完成后，请解压覆盖当前文件，然后重新运行 start_with_ui.bat
echo.

pause
start %DOWNLOAD_PAGE%

echo.
echo  [Step 3/3] 更新说明
echo.
echo  ========================================
echo  手动更新步骤：
echo  1. 点击上方链接打开 GitHub 下载页面
echo  2. 下载最新版本的 Source code (zip)
echo  3. 解压 zip 文件
echo  4. 将解压内容覆盖到当前目录
echo  5. 重新运行 start_with_ui.bat
echo  ========================================
echo.

pause
