@echo off
chcp 65001 >nul
title 我的导航 - 启动中...

echo.
echo  ========================================
echo       我的导航 - 一键启动
echo  ========================================
echo.

:: 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [错误] 未检测到 Python！
    echo.
    echo  请先安装 Python：
    echo  1. 打开浏览器访问 https://www.python.org/downloads/
    echo  2. 下载并安装最新版本
    echo  3. 安装时务必勾选 "Add Python to PATH"
    echo  4. 安装完成后重新双击本文件
    echo.
    pause
    exit /b 1
)

:: 安装依赖
echo  [1/4] 安装依赖（首次运行需要一点时间）...
cd /d "%~dp0backend"
pip install -r requirements.txt -q --disable-pip-version-check
echo        完成

:: 检查MySQL并输入密码
echo.
echo  [2/4] 连接数据库
echo        请输入您的 MySQL root 密码（如果没有密码直接按回车）：
echo.
set /p "MYSQL_PASSWORD=  密码: "

:: 测试数据库连接
echo.
echo  [3/4] 测试数据库连接...
python -c "import pymysql; pymysql.connect(host='localhost',user='root',password='%MYSQL_PASSWORD%',port=3306).close(); print('  连接成功')" 2>nul
if errorlevel 1 (
    echo.
    echo  [错误] 数据库连接失败！请检查：
    echo  1. MySQL 服务是否已启动
    echo     - 按 Win+R，输入 services.msc，找到 MySQL 并启动
    echo  2. 密码是否正确
    echo.
    pause
    exit /b 1
)

:: 启动后端
echo.
echo  [4/4] 启动服务...
start /b python app.py

:: 等待服务启动
echo        等待服务就绪...
timeout /t 3 /nobreak >nul

:: 自动打开浏览器
echo        打开浏览器...
start http://localhost:5000

echo.
echo  ========================================
echo   服务已启动！浏览器将自动打开
echo   访问地址: http://localhost:5000
echo   关闭此窗口将停止服务
echo  ========================================
echo.

:: 保持窗口开着（让后端继续运行）
:loop
timeout /t 60 /nobreak >nul
goto loop
