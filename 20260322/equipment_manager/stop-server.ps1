# Equipment Manager Server Stopper
Write-Host ""
Write-Host "========================================"
Write-Host "  Equipment Manager - Stopping Server"
Write-Host "========================================"
Write-Host ""

# Stop server
Write-Host "Stopping server..."
wsl -d Ubuntu-24.04 -e bash -c "cd /home/snowwon5/m-coding/20260322/equipment_manager && ./stop.sh"

Write-Host ""
Write-Host "========================================"
Write-Host "  Server Stopped Successfully!"
Write-Host "========================================"
Write-Host ""
Read-Host "Press Enter to close"
