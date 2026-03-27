@echo off
REM 기자재 관리 시스템 시작 스크립트
echo.
echo ========================================
echo   기자재 관리 시스템 시작 중...
echo ========================================
echo.

REM WSL에서 서버 시작
wsl -d Ubuntu-24.04 -e bash -c "cd /home/snowwon5/m-coding/20260322/equipment_manager && ./start.sh"

REM 결과 확인
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   서버가 시작되었습니다!
    echo ========================================
    echo.
    echo   접속 주소: http://localhost:8502
    echo.
    echo   브라우저를 열어 위 주소로 접속하세요.
    echo   또는 북마크를 클릭하세요.
    echo.
    echo ========================================
    echo.
    echo   이 창을 닫지 마세요!
    echo   서버를 중지하려면 Ctrl+C를 누르세요.
    echo ========================================
    echo.
) else (
    echo.
    echo ========================================
    echo   오류가 발생했습니다!
    echo ========================================
    echo.
    echo   WSL이 실행 중인지 확인하세요.
    echo.
    pause
)

REM 창 유지
pause
