@echo off
chcp 65001 >nul
title Bot Tu Tien Discord
echo Đang khởi động Bot Tu Tiên...
cd /d "%~dp0"
python bot.py
pause
