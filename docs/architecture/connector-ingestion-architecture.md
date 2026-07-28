# Connector, Ingestion, and Source Normalization Architecture

## Scope

Batch 5 defines contracts only. It does not implement provider APIs, OAuth exchanges, storage, or serverless route files. The connector catalog supports manual uploads first, then user-selected cloud files, and future authorized platform reads.

## Flows

1. An upload session uses `/api/uploads` (slot 3), then sends source bytes directly to approved storage.
2. Validation checks type, content, checksum, malware, size, and sensitive data. Valid files are finalized asynchronously through `/api/jobs` (slot 9).
3. A connector request uses `/api/connectors` (slot 6); callback completion is reserved for `/api/oauth-callback` (slot 7); verified inbound provider events use `/api/webhooks/{provider}` (slot 8).
4. Source detection assigns only confirmed or high-confidence provider profiles automatically. Low or unknown confidence does not silently select a provider.
5. Normalization produces canonical audit-source fields with masked/provider-generated references, ISO dates, ISO 4217 currency codes, source references, confidence, and review status.
6. Deduplication precedes reconciliation. Reconciliation compares labeled periods and source totals; it does not make accounting, tax, lending, or underwriting conclusions.

## Account selection and privacy

Multiple financial, commerce, marketplace, store, and ad accounts require explicit selection and ownership verification. No raw credentials or full account numbers are retained in contracts, examples, or logs. Redaction and quarantine occur before downstream use when sensitive data or unsafe structures are detected.

## Jobs, events, and budget

Existing `connector_sync`, `connector_reauthorize`, `upload_finalize`, and `audit_reprocess` job types remain on `/api/jobs` slot 9. Existing connector, upload, job, and system events retain their Batch 4 names and versions. The architecture uses slots 3 and 6–9 only; slots 11 and 12 remain reserved. Production activation remains subject to approved security, storage, authentication, and provider-specific controls.

## Future provider implementation

Provider field mappings and scopes are provisional. A provider implementation requires separate approval of its actual scopes, endpoints, API version, rate limits, credential handling, webhook verification, retention settings, and test fixtures.
