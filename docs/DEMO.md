# Oral demonstration runbook

This sequence fits a 15 to 20 minute presentation and leaves the deeper trade-offs for the interview.

1. Open `http://localhost:8000` and point to the synthetic/read-only banner.
2. Explain the five trust zones. Emphasize that safety evidence crosses a conceptual data diode outward and no command path returns.
3. Select **Load included demo file**. Explain schema validation and SHA-256 evidence hashing.
4. Walk through three findings: a passive network burst, a safety-integrity mismatch, and access without work authorization.
5. Explain that scores prioritize review. They never cause automatic plant action.
6. Open the HTML report. Show the evidence digest, findings, authorization note and audit entries.
7. Open Prometheus, query `nuclearshield_ingestions_total`, then open the provisioned Grafana dashboard.
8. Stop the application container with `docker compose stop nuclearshield`; show that Prometheus marks the target unavailable.
9. Recover with `docker compose start nuclearshield`; show `/api/health` and the target returning to healthy.
10. Close with the compliance map and the trade-offs in `DECISIONS.md`.

## Interview defense prompts

- Why passive monitoring? It reduces the chance that monitoring changes deterministic OT behavior, but visibility depends on reliable mirror points and evidence quality.
- Why a data diode? It provides a strong one-way property for safety evidence, but acknowledgements and interactive troubleshooting need separate approved procedures.
- Why simple explainable scoring? The demonstrator makes the reason for every finding visible. A production model would need validated training data, drift controls, independent testing and safety governance.
- Why no automated isolation? A generic cyber response may harm safety or availability. Qualified operators must apply approved, state-aware procedures.
- What fails safely? Invalid files are rejected, the app has no control channel, monitoring failure cannot affect safety functions, and evidence remains attributable by digest.

