# Manual Upload Runbook

1. Request a signed, expiring upload session on `/api/uploads` (slot 3) after recording the user’s selected source and period.
2. Send large files directly to approved storage; never place full files in a serverless request body.
3. Finalize with checksum and manifest metadata. Validate type, MIME, magic bytes, archive safety, malware status, encoding, structure, and sensitive-data policy.
4. Detect the provider using file and content signals. Confirmed/high profiles may proceed; medium requires correction or review; low/unknown must not be assumed.
5. Queue `upload_finalize` on `/api/jobs` (slot 9), normalize only supported values, and preserve `null` for unavailable values and numeric `0` only for verified zero.
6. Deduplicate, reconcile labeled periods, and emit existing upload/job/audit events. Deliver only results supported by available data; no recovery, funding, or accounting outcome is guaranteed.

## Recovery

Malformed, incomplete, encrypted, unsafe, or sensitive files enter quarantine. Explain the user-safe reason, request a corrected export or manual mapping, retain an audit trail, and reprocess with a new idempotency key only after release requirements are met.
