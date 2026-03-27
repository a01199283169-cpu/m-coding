# Create Desktop Shortcuts for Equipment Manager

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$SourcePath = "\\wsl.localhost\Ubuntu-24.04\home\snowwon5\m-coding\20260322\equipment_manager"

# Create WScript.Shell COM object
$WshShell = New-Object -ComObject WScript.Shell

# Create START shortcut
$StartShortcut = $WshShell.CreateShortcut("$DesktopPath\Equipment Manager START.lnk")
$StartShortcut.TargetPath = "powershell.exe"
$StartShortcut.Arguments = "-ExecutionPolicy Bypass -File `"$SourcePath\start-server.ps1`""
$StartShortcut.WorkingDirectory = $SourcePath
$StartShortcut.Description = "Start Equipment Manager Server"
$StartShortcut.IconLocation = "%SystemRoot%\system32\SHELL32.dll,21"
$StartShortcut.Save()

# Create STOP shortcut
$StopShortcut = $WshShell.CreateShortcut("$DesktopPath\Equipment Manager STOP.lnk")
$StopShortcut.TargetPath = "powershell.exe"
$StopShortcut.Arguments = "-ExecutionPolicy Bypass -File `"$SourcePath\stop-server.ps1`""
$StopShortcut.WorkingDirectory = $SourcePath
$StopShortcut.Description = "Stop Equipment Manager Server"
$StopShortcut.IconLocation = "%SystemRoot%\system32\SHELL32.dll,28"
$StopShortcut.Save()

Write-Host ""
Write-Host "========================================"
Write-Host "  Shortcuts Created Successfully!"
Write-Host "========================================"
Write-Host ""
Write-Host "Desktop shortcuts:"
Write-Host "  - Equipment Manager START.lnk"
Write-Host "  - Equipment Manager STOP.lnk"
Write-Host ""
Write-Host "========================================"
Write-Host ""
Read-Host "Press Enter to close"
