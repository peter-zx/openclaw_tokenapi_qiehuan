@echo off
chcp 65001 >nul
echo ========================================
echo OpenClaw Gateway 重启脚本
echo ========================================
echo.

echo 正在启动 Gateway 服务...
cd /d C:\Users\Administrator\.openclaw
start "" cmd /k "gateway.cmd"

echo.
echo 完成！请查看新窗口
