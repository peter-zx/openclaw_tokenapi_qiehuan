@echo off
start powershell -NoExit -Command "Get-Process | Where-Object { $_.Name -like '*openclaw*' } | Stop-Process -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 8; openclaw gateway"
