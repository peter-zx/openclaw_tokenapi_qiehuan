@echo off
echo 正在停止 OpenClaw 服务...

REM 查找并终止 Python 进程
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *OpenClaw Model Switcher*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *backend*" 2>nul

REM 备用方法：杀死所有包含 main.py 的 Python 进程
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *main.py*" 2>nul

echo 服务已停止
timeout /t 3
