@echo off
chcp 65001 > nul
title Equipment Manager

REM Check if server is already running
wsl -d Ubuntu-24.04 -e bash -c "ps aux | grep 'streamlit run main.py' | grep -v grep" > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Server is already running!
    echo Opening browser...
    start http://localhost:8502
    timeout /t 2 /nobreak > nul
    exit
)

REM Server not running, start it
cls
echo.
echo ========================================
echo   Equipment Manager
echo   Starting Server...
echo ========================================
echo.

REM Start server in background
start /B wsl -d Ubuntu-24.04 -e bash -c "cd /home/snowwon5/m-coding/20260322/equipment_manager && nohup ./start.sh > /dev/null 2>&1 &"

REM Wait for server to start
echo Initializing server...
timeout /t 4 /nobreak > nul

REM Open browser
echo Opening browser...
start http://localhost:8502

echo.
echo ========================================
echo   Server Started!
echo ========================================
echo.
echo   Access: http://localhost:8502
echo.
echo   * Keep this window open while using
echo   * Close this window to stop server
echo.
echo ========================================
echo.

REM Keep window open
pause > nul
