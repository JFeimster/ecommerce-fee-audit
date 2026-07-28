# Data Quality Recovery Runbook

## Triage

Classify the issue using the data-quality and quarantine policies: malformed file, missing fields, mixed currency, duplicate conflict, truncated export, wrong provider detection, reconciliation variance, or sensitive data. Record source reference, rule ID, confidence, review status, and idempotency context.

## Corrective actions

- Malformed or incomplete files: request a fresh provider export; do not infer missing values.
- Missing fields or currency: keep the value `null`, request clarification, and do not turn blanks into zero.
- Mixed currency: split reconciliation by ISO 4217 currency. Do not convert without an explicit conversion source and rate.
- Duplicate conflict: preserve both records and route for review; exact duplicates may return the original result idempotently.
- Wrong detection: capture the user-selected source and run the correct provisional mapping only after confirmation.
- Reconciliation variance: label the relationship and period, report the variance, and avoid accounting conclusions.

## Quarantine and reprocessing

Quarantined material remains inaccessible to normal processing until validation, redaction, and release requirements are met. Delete securely after resolution or configured expiry. Reprocessing creates an audit-traceable new idempotency key and must not erase the original result.
