# Monitoring and typography update

Preserve your existing .env file and Docker volumes. Extract the updated source
into the same NuclearShield project folder so Compose uses the same project name.

```powershell
docker compose up --build --pull never --force-recreate -d
docker compose ps
powershell -ExecutionPolicy Bypass -File scripts/check-monitoring.ps1
```

The monitoring images use pull_policy: never. All required images, including the
Python build base, must already be cached. No images or volumes need deletion.
Build dependencies may still require package downloads when the build cache is absent.

Open http://localhost:9090/targets and confirm nuclearshield is UP. A working
metrics endpoint alone does not prove that Prometheus is running or scraping.
The diagnostic script prints container logs, readiness and each target's last
error without downloading images or deleting data.

## Changes

- Explicit Docker service URLs; local Python runs check localhost by default.
- Prometheus waits for the application health check before starting.
- Latest finding gauges restore from SQLite on every scrape.
- Known metric label series exist before the first upload.
- Critical badges and Inspect buttons have unbroken labels and consistent sizing.
- Report tables no longer force cells to zero maximum width; long identifiers
  wrap, severity labels stay intact, and print layout permits long finding cards
  to continue across pages.
- Removed advice to delete the Grafana volume.

## Remaining limitations found in review

- Docker is unavailable in the authoring environment; live container verification
  on the student's machine is still required. The cause of any local container
  failure cannot be established without its logs.
- Statistical anomaly scoring groups records by event class, which can mix
  unrelated quantities. It needs unit/asset-specific profiles before wider use.
- Confidence is a heuristic score, not a calibrated probability of an attack.
- Correlation matches actors or assets without a time window.
- Missing authorization/integrity values currently receive permissive defaults.
- Audit logs are editable by someone with database access; no RBAC is implemented.
- The evidence UI renders all rows; large datasets need frontend pagination.
- Monitoring totals use bounded history queries, not unlimited lifetime totals.
- Framework mapping is thematic; formal compliance and complete rubric coverage
  have not been independently established.
- Threat intelligence is represented by an offline nuclear-sector context catalogue;
  no live classified, commercial or internet feed is connected.
- Formal-methods governance is documented, but the demonstrator does not run a
  nuclear-qualified theorem prover or model checker.
