# Equipment Manager Server Starter
Write-Host ""
Write-Host "========================================"
Write-Host "  Equipment Manager - Starting Server"
Write-Host "========================================"
Write-Host ""

# Start server in background
Write-Host "Starting WSL server..."
Start-Process wsl -ArgumentList "-d", "Ubuntu-24.04", "-e", "bash", "-c", "cd /home/snowwon5/m-coding/20260322/equipment_manager && ./start.sh" -WindowStyle Hidden

# Wait for server initialization
Write-Host "Waiting for server to initialize..."
Start-Sleep -Seconds 3

# Open browser
Write-Host "Opening browser..."
Start-Process "http://localhost:8502"

Write-Host ""
Write-Host "========================================"
Write-Host "  Server Started Successfully!"
Write-Host "========================================"
Write-Host ""
Write-Host "  Access: http://localhost:8502"
Write-Host ""
Write-Host "  To stop: Run stop-server.ps1"
Write-Host "========================================"
Write-Host ""
Write-Host "Closing in 5 seconds..."
Start-Sleep -Seconds 5
