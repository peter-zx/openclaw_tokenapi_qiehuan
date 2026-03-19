@echo off
cd /d "%~dp0"
chcp 65001 >nul
title 构建 OpenClaw 前端

echo ========================================
echo OpenClaw 模型切换工具 - 前端构建脚本
echo ========================================
echo.

echo [1/3] 检查 Node.js 安装...
node --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Node.js 未安装或未添加到 PATH
    echo 请先安装 Node.js 16+
    pause
    exit /b 1
)
echo Node.js 版本: 
node --version

echo [2/3] 安装依赖...
cd frontend
if exist "node_modules" (
    echo 已存在 node_modules 目录，跳过依赖安装
) else (
    echo 正在安装依赖...
    npm install
    if errorlevel 1 (
        echo 依赖安装失败
        pause
        exit /b 1
    )
)

echo [3/3] 构建前端...
echo 正在构建，请稍候...
npm run build
if errorlevel 1 (
    echo 构建失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 前端构建成功！
echo 请重新启动服务以使用 Web UI
echo ========================================
echo.
pause