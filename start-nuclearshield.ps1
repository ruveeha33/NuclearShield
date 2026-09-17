$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "============================================"
Write-Host " NuclearShield - Defensive Assurance Console"
Write-Host "============================================"
Write-Host ""

# Verify Docker CLI.
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker was not found. Install and start Docker Desktop before launching NuclearShield."
}

# Verify Docker Engine.
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Docker Desktop is installed but the Docker Engine is not running. Start Docker Desktop, wait for the engine to become ready, and run this launcher again."
}

# Create local environment configuration when missing.
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example."
}

# Read configured host ports.
$settings = @{}
Get-Content ".env" | ForEach-Object {
    $line = $_.Trim()

    if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
        $key, $value = $line.Split("=", 2)
        $settings[$key.Trim()] = $value.Trim()
    }
}

$appPort = if ($settings["APP_PORT"]) { [int]$settings["APP_PORT"] } else { 8000 }
$prometheusPort = if ($settings["PROMETHEUS_PORT"]) { [int]$settings["PROMETHEUS_PORT"] } else { 9090 }
$grafanaPort = if ($settings["GRAFANA_PORT"]) { [int]$settings["GRAFANA_PORT"] } else { 3000 }

Write-Host "Stopping any existing NuclearShield containers for this checkout..."
docker compose down --remove-orphans
if ($LASTEXITCODE -ne 0) { throw "Could not stop the existing NuclearShield Compose stack." }

function Test-HostPort {
    param(
        [int]$Port,
        [string]$Service
    )

    $listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue

    if ($listeners) {
        Write-Host ""
        Write-Host "PORT CONFLICT: $Service requires host port $Port." -ForegroundColor Yellow

        $owners = $listeners |
            Select-Object -ExpandProperty OwningProcess -Unique

        foreach ($ownerPid in $owners) {
            try {
                $process = Get-Process -Id $ownerPid -ErrorAction Stop
                Write-Host "  PID $ownerPid - $($process.ProcessName)"
            }
            catch {
                Write-Host "  PID $ownerPid"
            }
        }

        Write-Host ""
        Write-Host "Docker containers currently publishing this port:"

        $published = docker ps --format "{{.Names}}|{{.Ports}}" |
            Select-String ":$Port->"

        if ($published) {
            $published | ForEach-Object {
                Write-Host "  $($_.Line)"
            }
        }
        else {
            Write-Host "  No running Docker container identified."
        }

        Write-Host ""
        Write-Host "Resolve the conflict or change the corresponding value in .env:"
        Write-Host "  APP_PORT=$appPort"
        Write-Host "  PROMETHEUS_PORT=$prometheusPort"
        Write-Host "  GRAFANA_PORT=$grafanaPort"
        Write-Host ""

        return $false
    }

    return $true
}

Write-Host "Checking required host ports..."

$portsReady = $true

if (-not (Test-HostPort -Port $appPort -Service "NuclearShield")) {
    $portsReady = $false
}

if (-not (Test-HostPort -Port $prometheusPort -Service "Prometheus")) {
    $portsReady = $false
}

if (-not (Test-HostPort -Port $grafanaPort -Service "Grafana")) {
    $portsReady = $false
}

if (-not $portsReady) {
    throw "One or more configured host ports are already in use. NuclearShield was not started."
}

Write-Host "Ports are available."
Write-Host "Starting NuclearShield, Prometheus and Grafana from cached images..."

docker compose up --build --pull missing --force-recreate -d

if ($LASTEXITCODE -ne 0) {
    throw "Docker Compose could not start NuclearShield. Run 'docker compose ps -a' and 'docker compose logs' for details."
}

$appUrl = "http://localhost:$appPort"
$prometheusUrl = "http://localhost:$prometheusPort"
$grafanaUrl = "http://localhost:$grafanaPort"

Write-Host "Waiting for NuclearShield health check..."

$deadline = (Get-Date).AddMinutes(2)
$ready = $false

do {
    try {
        $health = Invoke-RestMethod "$appUrl/api/health" -TimeoutSec 3

        if ($health.status -eq "ok") {
            $ready = $true
            break
        }
    }
    catch {
        Start-Sleep -Seconds 2
    }
} while ((Get-Date) -lt $deadline)

if (-not $ready) {
    docker compose ps
    throw "NuclearShield did not become ready within two minutes."
}

Write-Host ""
Write-Host "NuclearShield is ready." -ForegroundColor Green
Write-Host "Application : $appUrl"
Write-Host "Prometheus  : $prometheusUrl"
Write-Host "Grafana     : $grafanaUrl"
Write-Host ""
Write-Host "Opening NuclearShield..."

Start-Process $appUrl

docker compose ps
