$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "Starting NuclearShield, Prometheus and Grafana from cached images..."
docker compose up --build --pull never --force-recreate -d
if ($LASTEXITCODE -ne 0) { throw "Docker Compose could not start NuclearShield." }
$deadline = (Get-Date).AddMinutes(2)
do {
    try {
        $health = Invoke-RestMethod "http://localhost:8000/api/health" -TimeoutSec 3
        if ($health.status -eq "ok") { break }
    } catch { Start-Sleep -Seconds 2 }
} while ((Get-Date) -lt $deadline)
if ((Get-Date) -ge $deadline) {
    docker compose ps
    throw "NuclearShield did not become ready within two minutes."
}
Write-Host "NuclearShield is ready. Opening the application..."
Start-Process "http://localhost:8000"
docker compose ps
