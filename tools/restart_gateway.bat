@echo off
chcp 65001 >nul
title OpenClaw 深度重启助手

echo ==========================================
echo   🦞 OpenClaw 深度重启助手
echo ==========================================
echo.

:: 1. 强力停止进程
echo [1/4] 正在查杀 openclaw 及相关残留进程...
powershell -NoProfile -Command ^
    "Get-Process | Where-Object { $_.Name -like '*openclaw*' -or $_.Name -eq 'node' } | Stop-Process -Force -ErrorAction SilentlyContinue"
echo     ✅ 进程已强制终止。

:: 2. 删除锁文件 (关键步骤！解决 lock timeout)
echo [2/4] 正在清理残留锁文件 (.lock)...
powershell -NoProfile -Command ^
    "Remove-Item -Path '$env:APPDATA\openclaw\*.lock' -Force -ErrorAction SilentlyContinue; ^
     Remove-Item -Path '$env:LOCALAPPDATA\openclaw\*.lock' -Force -ErrorAction SilentlyContinue; ^
     Write-Host '     ✅ 锁文件已清除。'"

:: 3. 等待端口释放
echo [3/4] 等待网络端口释放 (8秒)...
timeout /t 8 /nobreak >nul
echo     ✅ 等待完毕。

:: 4. 启动新服务
echo [4/4] 正在启动新服务窗口...
echo.
echo 💡 提示：新窗口弹出后，请观察日志。
echo    如果出现 "Listening on" 或插件注册信息，表示成功。
echo    如果再次出现 "lock timeout"，请手动删除 D:\aitoolwork\LOLweb0108\node-v24.12.0-win-x64\node_modules\openclaw 目录下的 .lock 文件。
echo.

start powershell -NoExit -Command "Write-Host '🚀 OpenClaw 启动中...' -ForegroundColor Cyan; openclaw gateway"

echo.
echo 新窗口已打开，本窗口将在 5 秒后关闭...
timeout /t 5 >nul
exit