# Equipment Manager - Automated Setup for Team Members
# Run as Administrator

param(
    [string]$WSLUsername = $env:USERNAME
)

Write-Host ""
Write-Host "========================================"
Write-Host "  Equipment Manager Setup"
Write-Host "========================================"
Write-Host ""

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host ""
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Check/Install WSL
Write-Host "Step 1: Checking WSL..." -ForegroundColor Cyan

try {
    $wslVersion = wsl --version 2>&1
    Write-Host "WSL is already installed" -ForegroundColor Green
} catch {
    Write-Host "WSL not found. Installing..." -ForegroundColor Yellow
    wsl --install -d Ubuntu-24.04
    Write-Host ""
    Write-Host "========================================"
    Write-Host "  REBOOT REQUIRED"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Please restart your computer and run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 0
}

# Step 2: Check Ubuntu installation
Write-Host ""
Write-Host "Step 2: Checking Ubuntu..." -ForegroundColor Cyan

$distros = wsl -l -q
if ($distros -notcontains "Ubuntu-24.04") {
    Write-Host "Ubuntu-24.04 not found. Installing..." -ForegroundColor Yellow
    wsl --install -d Ubuntu-24.04
    Write-Host ""
    Write-Host "Please complete Ubuntu setup (username/password)" -ForegroundColor Yellow
    Write-Host "Then run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 0
}

Write-Host "Ubuntu-24.04 is installed" -ForegroundColor Green

# Step 3: Get WSL username
Write-Host ""
Write-Host "Step 3: WSL Username Configuration" -ForegroundColor Cyan

$WSLUsername = Read-Host "Enter your WSL Ubuntu username (default: $env:USERNAME)"
if ([string]::IsNullOrWhiteSpace($WSLUsername)) {
    $WSLUsername = $env:USERNAME
}

Write-Host "Using WSL username: $WSLUsername" -ForegroundColor Green

# Step 4: Check equipment_manager folder
Write-Host ""
Write-Host "Step 4: Checking equipment_manager folder..." -ForegroundColor Cyan

$SourcePath = "\\wsl.localhost\Ubuntu-24.04\home\$WSLUsername\equipment_manager"

if (-not (Test-Path $SourcePath)) {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "  MANUAL ACTION REQUIRED"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Please copy the 'equipment_manager' folder to:" -ForegroundColor Yellow
    Write-Host $SourcePath -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Then run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 0
}

Write-Host "equipment_manager folder found" -ForegroundColor Green

# Step 5: Create desktop shortcut
Write-Host ""
Write-Host "Step 5: Creating desktop shortcut..." -ForegroundColor Cyan

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\기자재 관리.lnk")
$Shortcut.TargetPath = "$SourcePath\EquipmentManager.bat"
$Shortcut.WorkingDirectory = $SourcePath
$Shortcut.Description = "Equipment Manager - 기자재 관리 시스템"
$Shortcut.IconLocation = "%SystemRoot%\system32\imageres.dll,1"
$Shortcut.Save()

Write-Host "Desktop shortcut created" -ForegroundColor Green

# Step 6: Test server
Write-Host ""
Write-Host "Step 6: Testing server..." -ForegroundColor Cyan

$testResult = wsl -d Ubuntu-24.04 -e bash -c "cd /home/$WSLUsername/equipment_manager && test -f start.sh && echo 'OK'"

if ($testResult -eq "OK") {
    Write-Host "Server files verified" -ForegroundColor Green
} else {
    Write-Host "WARNING: start.sh not found" -ForegroundColor Yellow
    Write-Host "Please verify equipment_manager folder contents" -ForegroundColor Yellow
}

# Done
Write-Host ""
Write-Host "========================================"
Write-Host "  SETUP COMPLETED!"
Write-Host "========================================"
Write-Host ""
Write-Host "Desktop shortcut created: 기자재 관리" -ForegroundColor Green
Write-Host ""
Write-Host "To start the server:" -ForegroundColor Cyan
Write-Host "  1. Double-click '기자재 관리' icon on desktop"
Write-Host "  2. Wait 3 seconds"
Write-Host "  3. Browser will open automatically"
Write-Host "  4. Login and use!"
Write-Host ""
Write-Host "========================================"
Write-Host ""
Read-Host "Press Enter to exit"
