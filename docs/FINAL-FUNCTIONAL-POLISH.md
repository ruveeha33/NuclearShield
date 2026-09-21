# Final functional polish

- Domain order is now: statistics -> domain visualizations -> vertically scrollable full-width alert stream -> supporting evidence/queue.
- Material and AI Detection chart types were preserved; only alert placement changed.
- DevSecOps workflow is evidence-derived: Identify, Verify, Approve, and Recover statuses/counts are computed from the newest change/integrity records.
- Audit now includes action distribution, audit-assurance context, action filtering, search, and JSON access.
- Monitoring performs field-based Zeek and Suricata classification and exposes parsed protocols, conversations, Suricata signatures/categories, linked findings, and classification coverage.
- Added synthetic Zeek conn.log and Suricata EVE JSONL files in sample-data for functional demonstration.
