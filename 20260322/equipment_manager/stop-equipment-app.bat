@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   Equipment Manager - Stopping...
echo ========================================
echo.

wsl -d Ubuntu-24.04 -e bash -c "cd /home/snowwon5/m-coding/20260322/equipment_manager && ./stop.sh"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   Server Stopped Successfully!
    echo ========================================
    echo.
) else (
    echo.
    echo ========================================
    echo   Error Occurred!
    echo ========================================
    echo.
)

echo.
pause
