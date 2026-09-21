$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$logFile = Join-Path $PSScriptRoot "launcher-diagnostics.log"
Start-Transcript -Path $logFile -Append | Out-Null

function Fail([string]$Message) {
    Write-Host ""
    Write-Host "STARTUP ERROR: $Message" -ForegroundColor Red
    Write-Host "Diagnostics: $logFile" -ForegroundColor Yellow
    throw $Message
}

function Test-DockerEngine {
    try {
        docker info --format '{{.ServerVersion}}' 2>$null | Out-Null
        return ($LASTEXITCODE -eq 0)
    } catch { return $false }
}

function Start-DockerDesktopIfAvailable {
    $candidates = @(
        "$Env:ProgramFiles\Docker\Docker\Docker Desktop.exe",
        "$Env:LOCALAPPDATA\Docker\Docker Desktop.exe"
    )
    foreach ($path in $candidates) {
        if (Test-Path $path) {
            Write-Host "Docker Desktop is installed but its engine is not ready. Starting Docker Desktop..."
            Start-Process $path | Out-Null
            return $true
        }
    }
    return $false
}

function Test-PortFree([int]$Port) {
    # Check Windows listeners first, including Docker/WSL port proxies.
    try {
        $tcp = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
        if ($tcp) { return $false }
    } catch { }

    # Docker may publish a port even when Windows' listener view is delayed.
    try {
        $published = docker ps --format "{{.Ports}}" 2>$null
        if ($published -match "(?:0\.0\.0\.0|127\.0\.0\.1|\[::\]):$Port->") { return $false }
    } catch { }

    # Final OS-level bind test on ANY, not only loopback.
    $listener = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        $listener.ExclusiveAddressUse = $true
        $listener.Start()
        return $true
    } catch { return $false }
    finally { if ($listener) { try { $listener.Stop() } catch { } } }
}

function Find-FreePort([int]$Preferred, [int[]]$Reserved) {
    $candidate = $Preferred
    while ($candidate -le 65535) {
        if (($Reserved -notcontains $candidate) -and (Test-PortFree $candidate)) { return $candidate }
        $candidate++
    }
    Fail "No free TCP port could be found starting at $Preferred."
}

function Select-RuntimePorts([int]$AppStart = 8000, [int]$PromStart = 9090, [int]$GrafanaStart = 3000) {
    $env:APP_PORT = [string](Find-FreePort $AppStart @())
    $env:PROMETHEUS_PORT = [string](Find-FreePort $PromStart @([int]$env:APP_PORT))
    $env:GRAFANA_PORT = [string](Find-FreePort $GrafanaStart @([int]$env:APP_PORT, [int]$env:PROMETHEUS_PORT))
    @(
        "APP_PORT=$($env:APP_PORT)"
        "PROMETHEUS_PORT=$($env:PROMETHEUS_PORT)"
        "GRAFANA_PORT=$($env:GRAFANA_PORT)"
    ) | Set-Content -Encoding ascii (Join-Path $PSScriptRoot ".runtime-ports.env")
}

try {
    Write-Host "[1/7] Checking Docker..."
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Fail "Docker CLI was not found. Install/start Docker Desktop and retry."
    }
    if (-not (Test-DockerEngine)) {
        $started = Start-DockerDesktopIfAvailable
        if (-not $started) { Fail "Docker Desktop/engine is not running." }
        $deadline = (Get-Date).AddMinutes(2)
        do {
            Start-Sleep -Seconds 3
            Write-Host "  Waiting for Docker engine..."
        } while (-not (Test-DockerEngine) -and (Get-Date) -lt $deadline)
        if (-not (Test-DockerEngine)) { Fail "Docker Desktop did not become ready within two minutes." }
    }

    Write-Host "[2/7] Checking Docker Compose..."
    docker compose version | Out-Host
    if ($LASTEXITCODE -ne 0) { Fail "Docker Compose v2 is unavailable." }

    # Never kill another application just to reclaim a preferred port. If this
    # NuclearShield compose project has leftovers from an interrupted start,
    # clean up only this project's containers/network (volumes/history remain).
    docker compose down --remove-orphans 2>$null | Out-Null
    Select-RuntimePorts 8000 9090 3000

    Write-Host "[3/7] Validating configuration..."
    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { Fail "docker-compose.yml validation failed." }

    Write-Host "[4/7] Preparing monitoring images..."
    $requiredImages = @("prom/prometheus:latest", "grafana/grafana:latest")
    $missingImages = @()
    foreach ($image in $requiredImages) {
        docker image inspect $image *> $null
        if ($LASTEXITCODE -ne 0) { $missingImages += $image }
    }
    $env:MONITORING_PULL_POLICY = if ($missingImages.Count -gt 0) { "missing" } else { "never" }
    if ($missingImages.Count -gt 0) {
        Write-Host "  First run requires monitoring images: $($missingImages -join ', ')"
    }

    Write-Host "[5/7] Building and starting services..."
    $startedStack = $false
    $maxPortAttempts = 20
    for ($attempt = 1; $attempt -le $maxPortAttempts; $attempt++) {
        Write-Host "  Port set $attempt/$maxPortAttempts"
        Write-Host "  App        : http://localhost:$($env:APP_PORT)"
        Write-Host "  Prometheus : http://localhost:$($env:PROMETHEUS_PORT)"
        Write-Host "  Grafana    : http://localhost:$($env:GRAFANA_PORT)"

        docker compose up --build -d --remove-orphans
        if ($LASTEXITCODE -eq 0) {
            $startedStack = $true
            break
        }

        # A port can be claimed in the tiny interval between probing and Docker
        # publishing it. Do not stop the owner: clean up only this compose
        # project's partial containers and automatically move to new ports.
        Write-Host "  Startup collision detected. Keeping existing port owners untouched and trying new ports..." -ForegroundColor Yellow
        docker compose down --remove-orphans 2>$null | Out-Null
        $nextApp = [int]$env:APP_PORT + 1
        $nextProm = [int]$env:PROMETHEUS_PORT + 1
        $nextGrafana = [int]$env:GRAFANA_PORT + 1
        Select-RuntimePorts $nextApp $nextProm $nextGrafana
    }
    if (-not $startedStack) { Fail "Docker Compose could not start after $maxPortAttempts automatic port selections." }

    Write-Host "[6/7] Waiting for NuclearShield health check..."
    $deadline = (Get-Date).AddMinutes(3)
    $ready = $false
    do {
        try {
            $health = Invoke-RestMethod "http://127.0.0.1:$($env:APP_PORT)/api/health" -TimeoutSec 3
            if ($health.status -eq "ok") { $ready = $true; break }
        } catch { }
        Start-Sleep -Seconds 2
    } while ((Get-Date) -lt $deadline)

    if (-not $ready) {
        Write-Host ""
        docker compose ps | Out-Host
        Write-Host ""
        docker compose logs --tail 80 nuclearshield | Out-Host
        Fail "The web application did not become healthy. Container logs are shown above."
    }

    Write-Host "[7/7] Verifying services..."
    docker compose ps | Out-Host
    Write-Host ""
    Write-Host "NuclearShield is READY." -ForegroundColor Green
    Write-Host "Application: http://localhost:$($env:APP_PORT)"
    Write-Host "Prometheus : http://localhost:$($env:PROMETHEUS_PORT)"
    Write-Host "Grafana    : http://localhost:$($env:GRAFANA_PORT)  (admin / nuclearshield-demo)"
    Start-Process "http://localhost:$($env:APP_PORT)"
    Stop-Transcript | Out-Null
    exit 0
} catch {
    Write-Host ""
    Write-Host $_.Exception.Message -ForegroundColor Red
    try { docker compose ps | Out-Host } catch { }
    try { docker compose logs --tail 60 | Out-Host } catch { }
    try { Stop-Transcript | Out-Null } catch { }
    exit 1
}
