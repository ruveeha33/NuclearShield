# Offline Assurance Lab: what the new checks prove

Assurance Lab is an **educational, read-only software demonstration**. It adds
four independent checks to the NuclearShield evidence workflow:

1. **One-way gateway policy:** enumerates 48 combinations of source, destination
   and message type. The policy permits only outward evidence delivery to
   analytics. This verifies a finite software rule, not a physical diode or
   plant network separation.
2. **Change review policy:** enumerates 16 combinations of declared approval,
   signature validity, independent review and safety independence. Only the
   all-true case is review-ready. No deployment or control action results.
3. **Offline PACS/MC&A review:** compares access and material records within
   the selected uploaded file by shared actor or asset. It lists numerical
   differences from *declared* inventory baselines. It cannot verify actual
   inventory or infer a person's intent.
4. **Repeated integrity snapshots:** compares observations for the same asset
   across up to 50 recent retained uploads. New checks happen when a user
   uploads evidence; the app does not continuously monitor plant firmware.
5. **Offline indicator review:** upload the included JSON catalog while the
   full-platform analysis is selected. Exact IP/signature matches return
   linked event IDs and an advisory five-step human review guide. The catalog
   is fictional and unverified; this is not a real nuclear-sector feed or
   automated incident response.

To show the workflow, upload `sample-data/NuclearShield-Full-Platform-100-Records.jsonl`
and open Assurance Lab to inspect the offline joins. Then upload
`sample-data/08-later-integrity-snapshot.csv` and return to Assurance Lab to
inspect the change on fictional `training-controller`. The first file is bundled
in the final exam ZIP. All names and measurements are synthetic.

The app still has no live PACS or MC&A connector, licensed formal verification
of safety code, physical air gap, data diode, or nuclear system interface.
