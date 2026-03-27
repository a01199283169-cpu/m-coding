@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   Equipment Manager - Starting...
echo ========================================
echo.

start /B wsl -d Ubuntu-24.04 -e bash -c "cd /home/snowwon5/m-coding/20260322/equipment_manager && ./start.sh"

echo   Initializing server...
timeout /t 3 /nobreak > nul

echo   Opening browser...
start http://localhost:8502

echo.
echo ========================================
echo   Server Started!
echo ========================================
echo.
echo   Access: http://localhost:8502
echo   Browser will open automatically.
echo.
echo   To stop server, run: stop-equipment-app.bat
echo.
echo ========================================
echo.
echo   This window will close in 5 seconds...
timeout /t 5 /nobreak > nul
