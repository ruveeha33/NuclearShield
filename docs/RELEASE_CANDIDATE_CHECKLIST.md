# NuclearShield v1.0.0 Release Candidate Checklist

Status: **v1.0.0rc1 on `develop`**

This checklist is intentionally conservative. `main` must not be updated until review and approval.

## Functional checks

- [x] Terminal command-center layout matches current dashboard tests.
- [x] Synthetic scenarios: normal, SCADA anomaly, safety integrity, insider risk, material variance, combined.
- [x] Safety, instrumentation and firmware integrity evidence.
- [x] SCADA / OT zone monitoring and conceptual one-way evidence boundary.
- [x] MC&A and physical-cyber safeguards evidence.
- [x] IsolationForest-based anomaly scoring and cross-domain risk fusion.
- [x] End-of-session evidence report and JSON/text export.
- [x] Architecture, assurance-gate and defensive threat-context views.
- [x] Prometheus metrics and provisioned Grafana dashboard.
- [x] Windows exam launcher and monitoring shutdown scripts.

## Safety checks

- [x] Synthetic data only.
- [x] No real reactor, PLC, SCADA, safety-I&C, physical-access or MC&A connectivity.
- [x] No exploit chains, malware, persistence, credential theft or security-bypass guidance.
- [x] No industrial control write path.
- [x] Automated response remains advisory / human-review oriented.
- [x] Threat context is high-level and defensive only.

## Release validation

GitHub Actions must pass before promoting this candidate to v1.0.0:

- [ ] Python 3.10 tests pass.
- [ ] Python 3.12 tests pass.
- [ ] Package compile check passes.
- [ ] Grafana JSON validates.
- [ ] Readiness command executes.
- [ ] Architecture / assurance / threat-context CLI smoke tests execute.
- [ ] Finite combined simulation completes and exports evidence.

## Manual exam-machine validation

Run these on the Windows machine that will be used for the oral examination:

1. `NuclearShield.bat` → **SYSTEM SELF-CHECK**.
2. `run_exam_demo.bat` and confirm the terminal opens correctly.
3. Confirm Grafana opens at port 3000 and Prometheus at port 9090 when Docker Desktop is available.
4. Let the combined scenario rotate long enough to demonstrate multiple domains.
5. End the session with `Ctrl+C` and confirm the defensive evidence report appears.
6. Confirm report files are created under `reports/`.
7. Run `stop.bat` after the demonstration.

## Promotion rule

Only after automated CI and the manual exam-machine checks pass should `1.0.0rc1` be changed to `1.0.0` and a final release be prepared. Do not merge `develop` into `main` without explicit approval.
