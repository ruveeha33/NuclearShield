# NuclearShield Topic 132 exam requirements map

This map distinguishes working software from target deployment concepts. All supplied evidence is synthetic or safely exported; the application is read only and has no connection to a plant.

| Topic 132 objective | Status in this project | Evidence and limit |
|---|---|---|
| Air gap, defense in depth and data diode | Architecture and finite policy demonstration | Diagrams and Assurance Lab enumerate one-way evidence policy cases and reject inbound commands. No physical air gap, diode or gateway is deployed. |
| SCADA / I&C anomaly detection | Demonstrated on uploaded evidence | Rules, median/MAD and optional per-upload Isolation Forest analyze records tagged network. No connection to reactor protection or live instrumentation. |
| Safety software/firmware integrity | Repeated offline snapshot demonstration | Declared baselines, signature states and authorization mismatches are flagged; Assurance Lab compares assets across stored uploads. No continuous connection to safety controllers. |
| Material control/accounting and safeguards | Offline evidence demonstration | Uploaded PACS-like and MC&A-like exports are joined by actor/asset and declared inventory differences listed for review; no facility MC&A or PACS integration. |
| Insider-risk analytics | Limited demonstration | Shared actor/asset joins and unauthorized access signals support human review; behavior/intent is not inferred. |
| Machine learning network anomaly model | Implemented for eligible uploads | `scikit-learn` Isolation Forest fits and scores 20+ numeric network rows in the current uploaded file. Results show input fields, eligible rows and decision scores. Insufficient evidence skips ML; no validated nuclear baseline or confirmed threat classification. |
| Nuclear threat intelligence integration | Offline indicator-review demonstration | A user-supplied JSON catalog can be checked by exact IP/signature value against selected network evidence. The supplied catalog is unverified; no live or curated nuclear-sector feed is ingested. |
| Automated safety-preserving incident response | Human-gated proposal only | An indicator match returns a five-step evidence preservation and review checklist. No automatic containment or plant write endpoint. Real response requires separate approved operating procedures. |
| DevSecOps, change control and formal methods | Partial with bounded policy check | CI tests, static scans, change evidence and integrity checks exist. Assurance Lab exhaustively enumerates a four-condition review policy. Formal verification of safety code and regulated deployment are not implemented. |
| IEC 62645 / NRC / IAEA compliance automation | Demonstration mapping and downloadable packet | Pages map uploaded evidence to control themes, and a per-analysis JSON packet exports evidence counts and limitations. No certification, regulatory determination or automatic proof of compliance. |
| Safeguards reporting and audit | Implemented locally with limits | HTML reports, a local safeguards evidence packet, SQLite history and analysis-ID-linked audit entries with SHA-256 references. No regulator submission or immutable external retention. |
| Zeek / Suricata, Prometheus / Grafana | File parsing and monitoring | Passive log exports can be uploaded. Prometheus scrapes application metrics and Grafana displays them; no production ICS sensor deployment. |

For a short exam demonstration, upload `sample-data/isolation-forest-network-synthetic.csv` and open AI Detection. The file contains fictional network observations and a deliberately unusual record. Explain that a negative Isolation Forest decision score prioritizes human investigation and is not a confirmed attack. The standard 24-row example has fewer than 20 suitable network rows, so the model correctly reports insufficient data.
