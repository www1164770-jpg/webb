@echo off
title 我的导航 - 启动

echo.
echo  ========================================
echo       我的导航 - 一键启动
echo  ========================================
echo.

cd /d "%~dp0"

echo  [1/3] 安装依赖...
pip install -r requirements.txt -q --disable-pip-version-check
echo        完成

echo.
echo  [2/3] 请输入 MySQL root 密码（没有密码直接回车）:
set /p MYSQL_PASSWORD=  MySQL密码: 

echo.
echo  [3/3] 请输入通义千问 API Key（不用AI功能直接回车跳过）:
echo        获取地址: https://bailian.console.aliyun.com/
set /p DASHSCOPE_API_KEY=  千问Key: 

echo.
echo  启动中... 访问 http://localhost:5000
echo.
python app.py

pause
