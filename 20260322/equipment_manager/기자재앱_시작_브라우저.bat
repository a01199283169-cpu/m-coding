@echo off
REM 기자재 관리 시스템 시작 + 브라우저 자동 실행
echo.
echo ========================================
echo   기자재 관리 시스템 시작 중...
echo ========================================
echo.

REM WSL에서 서버 시작
start /B wsl -d Ubuntu-24.04 -e bash -c "cd /home/snowwon5/m-coding/20260322/equipment_manager && ./start.sh"

REM 서버 시작 대기 (3초)
echo   서버 초기화 중...
timeout /t 3 /nobreak > nul

REM 브라우저 자동 실행
echo   브라우저 실행 중...
start http://localhost:8502

echo.
echo ========================================
echo   서버가 시작되었습니다!
echo ========================================
echo.
echo   접속 주소: http://localhost:8502
echo   브라우저가 자동으로 열립니다.
echo.
echo ========================================
echo.
echo   서버를 종료하려면 "기자재앱_종료.bat"를
echo   실행하세요.
echo.
echo ========================================
echo.
echo   5초 후 이 창이 자동으로 닫힙니다...
timeout /t 5 /nobreak > nul
