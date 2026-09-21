# Architecture decisions and trade-offs

## Evidence-only boundary

NuclearShield accepts offline evidence files and exposes no control endpoint. This preserves a clear teaching boundary and demonstrates unidirectional isolation concepts. It cannot prove the behavior of a physical diode or a production OT sensor.

## Explainable anomaly rules

The analyzer compares numeric or categorical values with declared baselines and adds authorization/integrity signals. This is transparent enough to defend in an oral exam. It is not a trained nuclear process model and must never be presented as one.

## Single-process student build

FastAPI serves the API and static frontend, reducing operational overhead for one student. Prometheus and Grafana remain separate containers because that matches their real operational roles and makes failure boundaries visible.

## SQLite audit trail

SQLite gives a durable, inspectable demo audit trail. Production systems would require write-once retention, trusted time, access segregation, cryptographic signing and regulator-approved records management.

## Standards mapping

The controls view maps demonstrator evidence to themes from IEC 62645, NRC RG 5.71 and IAEA guidance. It supports learning and design discussion; it does not claim compliance, certification or regulatory approval.

