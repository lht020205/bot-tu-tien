@echo off
chcp 65001 >nul
echo Đang tắt tiến trình Bot Tu Tiên...
wmic process where "commandline like '%%bot.py%%'" delete >nul 2>&1
echo Đã tắt bot thành công!
pause
