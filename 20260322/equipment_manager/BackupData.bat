@echo off
REM Equipment Manager - Daily Backup Script
REM 매일 자동으로 데이터를 백업합니다.

title Equipment Manager - Backup

echo.
echo ========================================
echo   Equipment Manager - Data Backup
echo ========================================
echo.

REM Set backup directory (modify as needed)
set BACKUP_ROOT=D:\Backups\EquipmentManager
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set TIME=%time:~0,2%%time:~3,2%
set BACKUP_DIR=%BACKUP_ROOT%\%DATE%

echo Backup Date: %DATE%
echo Backup Time: %TIME%
echo.

REM Create backup directory
if not exist "%BACKUP_ROOT%" (
    echo Creating backup root directory...
    mkdir "%BACKUP_ROOT%"
)

if not exist "%BACKUP_DIR%" (
    echo Creating today's backup directory...
    mkdir "%BACKUP_DIR%"
)

REM Check if source data exists
if not exist "\\wsl.localhost\Ubuntu-24.04\home\server\equipment_manager\data" (
    echo.
    echo ERROR: Source data folder not found!
    echo Expected: \\wsl.localhost\Ubuntu-24.04\home\server\equipment_manager\data
    echo.
    pause
    exit /b 1
)

REM Copy data folder
echo.
echo [1/3] Copying data folder...
xcopy /E /I /Y /Q "\\wsl.localhost\Ubuntu-24.04\home\server\equipment_manager\data" "%BACKUP_DIR%\data" > nul
if %ERRORLEVEL% EQU 0 (
    echo   ✓ Data copied successfully
) else (
    echo   ✗ Failed to copy data
    pause
    exit /b 1
)

REM Create ZIP archive
echo.
echo [2/3] Creating ZIP archive...
powershell -command "try { Compress-Archive -Path '%BACKUP_DIR%\*' -DestinationPath '%BACKUP_ROOT%\backup_%DATE%_%TIME%.zip' -Force; Write-Host '  ✓ ZIP archive created' } catch { Write-Host '  ✗ Failed to create ZIP'; exit 1 }"
if %ERRORLEVEL% NEQ 0 (
    pause
    exit /b 1
)

REM Delete old backups (keep last 30 days)
echo.
echo [3/3] Cleaning old backups (keeping last 30 days)...
forfiles /P "%BACKUP_ROOT%" /M backup_*.zip /D -30 /C "cmd /c del @path" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   ✓ Old backups deleted
) else (
    echo   ⓘ No old backups to delete
)

REM Count backup files
echo.
echo ========================================
echo   Backup Completed Successfully!
echo ========================================
echo.
echo   Location: %BACKUP_ROOT%
echo   File:     backup_%DATE%_%TIME%.zip
echo.

REM List recent backups
echo   Recent backups:
dir /B /O-D "%BACKUP_ROOT%\backup_*.zip" 2>nul | findstr /R "^backup_" | head -5
echo.

REM Calculate backup size
for %%A in ("%BACKUP_ROOT%\backup_%DATE%_%TIME%.zip") do (
    set SIZE=%%~zA
)
echo   Backup size: %SIZE% bytes
echo.
echo ========================================
echo.

REM Auto-close after 10 seconds if running automatically
if "%1"=="auto" (
    echo Window will close in 10 seconds...
    timeout /t 10 /nobreak > nul
) else (
    pause
)
