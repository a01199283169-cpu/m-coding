@echo off
REM 기자재 관리 시스템 종료 스크립트
echo.
echo ========================================
echo   기자재 관리 시스템 종료 중...
echo ========================================
echo.

REM WSL에서 서버 종료
wsl -d Ubuntu-24.04 -e bash -c "cd /home/snowwon5/m-coding/20260322/equipment_manager && ./stop.sh"

REM 결과 확인
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   서버가 종료되었습니다!
    echo ========================================
    echo.
) else (
    echo.
    echo ========================================
    echo   오류가 발생했습니다!
    echo ========================================
    echo.
)

echo.
pause
