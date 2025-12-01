# Script para matar todos los procesos Python
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Todos los procesos Python han sido detenidos"
