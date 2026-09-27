$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$failed = 0

function Check([string]$name, [scriptblock]$action) {
    try {
        & $action
        Write-Host "PASS $name" -ForegroundColor Green
    } catch {
        Write-Host "FAIL $name : $($_.Exception.Message)" -ForegroundColor Red
        $script:failed++
    }
}

Push-Location $root
try {
    foreach ($name in @('NuclearShield-Full-Platform-100-Records.jsonl', 'NuclearShield-IsolationForest-80-Network-Records.csv', '08-later-integrity-snapshot.csv')) {
        Check "Demo file $name" { if (-not (Test-Path (Join-Path 'sample-data' $name))) { throw 'Missing file' } }
    }
    Check 'Docker Compose configuration' {
        if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker is unavailable; start Docker Desktop' }
        $result = & docker compose config --quiet 2>&1
        if ($LASTEXITCODE -ne 0) { throw ($result | Out-String) }
    }
    $ports = @{ APP_PORT = 8000; PROMETHEUS_PORT = 9090; GRAFANA_PORT = 3000 }
    $runtime = Join-Path $root '.runtime-ports.env'
    if (Test-Path $runtime) {
        foreach ($line in (Get-Content $runtime)) {
            if ($line -match '^\s*(APP_PORT|PROMETHEUS_PORT|GRAFANA_PORT)=(\d+)\s*$') {
                $ports[$matches[1]] = [int]$matches[2]
            }
        }
    }
    Write-Host "Checking localhost ports: app $($ports.APP_PORT), Prometheus $($ports.PROMETHEUS_PORT), Grafana $($ports.GRAFANA_PORT)"
    Check 'Application health' {
        $health = Invoke-RestMethod "http://localhost:$($ports.APP_PORT)/api/health" -TimeoutSec 8
        if ($null -eq $health) { throw 'Empty response' }
    }
    Check 'Prometheus readiness' {
        $response = Invoke-WebRequest "http://localhost:$($ports.PROMETHEUS_PORT)/-/ready" -UseBasicParsing -TimeoutSec 8
        if ($response.StatusCode -ne 200) { throw "HTTP $($response.StatusCode)" }
    }
    Check 'Grafana health' {
        $health = Invoke-RestMethod "http://localhost:$($ports.GRAFANA_PORT)/api/health" -TimeoutSec 8
        if ($null -eq $health) { throw 'Empty response' }
    }
    Check 'Prometheus targets API' {
        $response = Invoke-RestMethod "http://localhost:$($ports.APP_PORT)/api/prometheus-targets" -TimeoutSec 8
        if ($null -eq $response) { throw 'Empty response' }
    }
} finally {
    Pop-Location
}
if ($failed -gt 0) {
    Write-Host "$failed pre-exam check(s) failed. See the messages above." -ForegroundColor Yellow
    exit 1
}
Write-Host 'All pre-exam checks passed.' -ForegroundColor Green
