# Local evidence packet

After uploading fictional training evidence, open **Compliance** or **Reports**
and select **Evidence packet JSON**. The endpoint `/api/compliance-packet` can
also take a retained `analysis_id`. It exports the selected analysis only:

- the analysis ID, filename, ingestion time and source file's recorded SHA-256;
- accepted and rejected counts and evidence counts by domain;
- evidence-presence mappings to IEC 62645, NRC RG 5.71 and IAEA themes;
- finding references, local MC&A/PACS-like joins and declared inventory differences;
- audit entries linked by that exact analysis ID while it is retained;
- an independent packet content checksum that is **not a signature**.

The packet does not retain the uploaded raw file, prove legal compliance,
confirm material movements, satisfy official safeguards reporting formats,
or transmit records to a regulator. Human review and facility authority are
required for any actual reporting or response.
