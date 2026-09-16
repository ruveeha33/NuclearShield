$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker is not available. Start Docker Desktop, wait until it is ready, then double-click START-NUCLEARSHIELD.cmd again."
}

function Test-PortFree([int]$Port) {
    $listener = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        return $true
    } catch {
        return $false
    } finally {
        if ($listener) { $listener.Stop() }
    }
}

function Find-FreePort([int]$Preferred, [int[]]$Reserved) {
    $candidate = $Preferred
    while (($Reserved -contains $candidate) -or -not (Test-PortFree $candidate)) { $candidate++ }
    return $candidate
}

$runtimeFile = Join-Path $PSScriptRoot ".runtime-ports.env"
$running = docker compose ps --status running -q nuclearshield 2>$null
if ($running -and (Test-Path $runtimeFile)) {
    Get-Content $runtimeFile | ForEach-Object {
        if ($_ -match '^([^=]+)=(\d+)$') { Set-Item "Env:$($matches[1])" $matches[2] }
    }
} else {
    $env:APP_PORT = Find-FreePort 8000 @()
    $env:PROMETHEUS_PORT = Find-FreePort 9090 @([int]$env:APP_PORT)
    $env:GRAFANA_PORT = Find-FreePort 3000 @([int]$env:APP_PORT, [int]$env:PROMETHEUS_PORT)
    @(
        "APP_PORT=$($env:APP_PORT)"
        "PROMETHEUS_PORT=$($env:PROMETHEUS_PORT)"
        "GRAFANA_PORT=$($env:GRAFANA_PORT)"
    ) | Set-Content -Encoding ascii $runtimeFile
}

$requiredImages = @("prom/prometheus:latest", "grafana/grafana:latest")
$missingImages = @($requiredImages | Where-Object {
    docker image inspect $_ *> $null
    $LASTEXITCODE -ne 0
})
$pullMode = "never"
$env:MONITORING_PULL_POLICY = "never"
if ($missingImages.Count -gt 0) {
    $pullMode = "missing"
    $env:MONITORING_PULL_POLICY = "missing"
    Write-Host "First run: downloading missing monitoring images once. Future starts will reuse them."
}

Write-Host "Starting NuclearShield on port $($env:APP_PORT), Prometheus on $($env:PROMETHEUS_PORT), and Grafana on $($env:GRAFANA_PORT)..."
docker compose up --build --pull $pullMode --force-recreate -d
if ($LASTEXITCODE -ne 0) { throw "Docker Compose could not start NuclearShield." }
$deadline = (Get-Date).AddMinutes(2)
do {
    try {
        $health = Invoke-RestMethod "http://localhost:$($env:APP_PORT)/api/health" -TimeoutSec 3
        if ($health.status -eq "ok") { break }
    } catch { Start-Sleep -Seconds 2 }
} while ((Get-Date) -lt $deadline)
if ((Get-Date) -ge $deadline) {
    docker compose ps
    throw "NuclearShield did not become ready within two minutes."
}
Write-Host "NuclearShield is ready. Opening the application..."
Start-Process "http://localhost:$($env:APP_PORT)"
docker compose ps
