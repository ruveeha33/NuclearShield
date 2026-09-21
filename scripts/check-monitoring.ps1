$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
$appPort = 8000
$prometheusPort = 9090
$runtimeFile = Join-Path (Get-Location) ".runtime-ports.env"
if (Test-Path $runtimeFile) {
    Get-Content $runtimeFile | ForEach-Object {
        if ($_ -match '^APP_PORT=(\d+)$') { $appPort = [int]$matches[1] }
        if ($_ -match '^PROMETHEUS_PORT=(\d+)$') { $prometheusPort = [int]$matches[1] }
    }
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker is not available. Start Docker Desktop and reopen PowerShell."
}
docker compose ps -a
docker compose logs --tail 60 prometheus
docker compose exec -T prometheus promtool check config /etc/prometheus/prometheus.yml
try {
    $readiness = Invoke-WebRequest "http://localhost:$prometheusPort/-/ready" -TimeoutSec 8 -UseBasicParsing
    Write-Host "Prometheus readiness:" $readiness.StatusCode
    $targets = Invoke-RestMethod "http://localhost:$prometheusPort/api/v1/targets" -TimeoutSec 8
    $targets.data.activeTargets |
        Select-Object scrapeUrl, health, lastError, lastScrape |
        Format-Table -Wrap
} catch {
    Write-Host "Prometheus HTTP check failed:" $_.Exception.Message
}
try {
    $metrics = Invoke-WebRequest "http://localhost:$appPort/metrics" -TimeoutSec 8 -UseBasicParsing
    Write-Host "NuclearShield metrics HTTP status:" $metrics.StatusCode
} catch {
    Write-Host "Application metrics check failed:" $_.Exception.Message
}
Write-Host "This diagnostic does not pull images or delete volumes."
