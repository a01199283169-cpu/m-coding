@echo off
chcp 65001 > nul
echo ============================================
echo  회의록분석기 v2.0 — .exe 빌드 시작
echo ============================================
echo.

:: ── 1. 필수 패키지 설치 ──────────────────────
echo [1/4] 필수 패키지 설치 중...
pip install pyinstaller Pillow PyQt6 pdfplumber pandas python-docx xlsxwriter cryptography --quiet
if errorlevel 1 (
    echo [오류] 패키지 설치 실패. pip 를 확인해주세요.
    pause & exit /b 1
)
echo       완료.
echo.

:: ── 2. 아이콘 생성 ──────────────────────────
echo [2/4] 아이콘 생성 중...
python icon_creator.py
if errorlevel 1 (
    echo [경고] 아이콘 생성 실패 — 기본 아이콘으로 계속 진행합니다.
)
echo.

:: ── 3. 이전 빌드 캐시 정리 ──────────────────
echo [3/4] 이전 빌드 정리 중...
if exist build  rmdir /s /q build
if exist dist   rmdir /s /q dist
echo       완료.
echo.

:: ── 4. PyInstaller 빌드 ─────────────────────
echo [4/4] .exe 빌드 중 (수 분 소요)...
pyinstaller 회의록분석기_v2.0.spec
if errorlevel 1 (
    echo.
    echo [오류] 빌드 실패. 위 오류 메시지를 확인하세요.
    pause & exit /b 1
)

echo.
echo ============================================
echo  빌드 완료!
echo  실행 파일 위치:
echo    %~dp0dist\회의록분석기_v2.0.exe
echo ============================================
echo.
explorer "%~dp0dist"
pause
