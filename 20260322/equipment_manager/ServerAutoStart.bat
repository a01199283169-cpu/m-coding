@echo off
REM Equipment Manager Server - Auto Start Script
REM 부팅 시 자동으로 서버를 시작합니다.

title Equipment Manager Server - Auto Start

echo.
echo ========================================
echo   Equipment Manager Server
echo   Auto Start Mode
echo ========================================
echo.

REM Wait for network initialization (30 seconds)
echo [1/4] Waiting for network initialization...
timeout /t 30 /nobreak > nul

REM Check if WSL is ready
echo [2/4] Checking WSL...
wsl --list --running > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Starting WSL...
    wsl -d Ubuntu-24.04 -e true
    timeout /t 5 /nobreak > nul
)

REM Check if server is already running
echo [3/4] Checking if server is already running...
wsl -d Ubuntu-24.04 -e bash -c "ps aux | grep 'streamlit run main.py' | grep -v grep" > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   Server is already running!
    echo ========================================
    echo.
    echo   Access: http://localhost:8502
    echo.
    timeout /t 5 /nobreak > nul
    exit /b 0
)

REM Start server
echo [4/4] Starting server...
start /B wsl -d Ubuntu-24.04 -e bash -c "cd /home/server/equipment_manager && nohup ./start.sh > /dev/null 2>&1 &"

REM Wait for server startup
echo.
echo Initializing server...
timeout /t 10 /nobreak > nul

REM Verify server is running
echo.
echo Verifying...
wsl -d Ubuntu-24.04 -e bash -c "ps aux | grep 'streamlit run main.py' | grep -v grep" > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   Server Started Successfully!
    echo ========================================
    echo.
    echo   Local Access:   http://localhost:8502
    echo.
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
        echo   Network Access: http://%%a:8502
        goto :found_ip
    )
    :found_ip
    echo.
    echo   This window will minimize in 10 seconds...
    echo ========================================
    echo.
    timeout /t 10 /nobreak > nul

    REM Minimize window (keep running in background)
    powershell -command "$wshell = New-Object -ComObject WScript.Shell; $wshell.SendKeys('% n')"
) else (
    echo.
    echo ========================================
    echo   ERROR: Server failed to start!
    echo ========================================
    echo.
    echo   Please check:
    echo   1. WSL Ubuntu is installed
    echo   2. equipment_manager folder exists
    echo   3. start.sh file exists
    echo.
    echo   Press any key to exit...
    pause > nul
)
