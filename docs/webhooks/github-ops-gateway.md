# GitHub Ops Gateway

## Status

Specification only. Do not create the repository webhook until a controlled HTTPS receiver and unique secret exist.

## Repository webhook configuration

- Repository: `JFeimster/ecommerce-fee-audit`
- Content type: `application/json`
- SSL verification: enabled
- Events: `push`, `pull_request`, `workflow_run`, `release`, `issues`, `issue_comment`
- Do not use **Send me everything**.

## Receiver requirements

1. Validate `X-Hub-Signature-256` with a server-side secret.
2. Deduplicate with `X-GitHub-Delivery`.
3. Allow only this repository and approved events.
4. Allow `main` for push/release automation unless an explicit review workflow needs PR refs.
5. Return a fast 2xx response and process asynchronously.
6. Log event, delivery ID, repository, branch/ref, action, and outcome without logging secrets or sensitive payload data.
7. Keep every handler retry-safe and idempotent.

## Workflow A — Knowledge Change Notice

Trigger: push to `main` affecting `knowledge/**` or action-definition files.

Allowed behavior:

- Record commit and changed paths.
- Notify the Knowledge maintainer.
- Create or update a review record.
- Require human approval before publishing GPT instruction changes.

Prohibited: starting client audits or publishing GPT changes automatically.

## Workflow B — Release Public Audit Assets

Trigger: published release.

Allowed behavior:

- Package approved public site assets, templates, taxonomy, and schemas.
- Generate a manifest, checksums, release version, and source commit.
- Sync approved No-Auth resources.

Prohibited: including client data, raw platform exports, bank files, secrets, or credentials.

## Workflow C — Failed Workflow Alert

Trigger: tracked workflow completes with failure.

Allowed behavior:

- Notify the operator.
- Create or update one incident record containing workflow, run ID, branch, commit, and failed job.
- Deduplicate by workflow run ID.

## Workflow D — Approved Issue Sync

Trigger: issue receives an approved automation label.

Allowed behavior:

- Sync issue URL, title, acceptance criteria, labels, and owner to an external workspace.
- Update an existing record rather than duplicate it.

The label is the human approval signal. GitHub events must not execute financial actions.

## Workflow E — Schema Version Published

Trigger: release containing changes to:

- `knowledge/master-transaction-schema.json`
- `knowledge/output-schema.json`
- `knowledge/normalized-platform-fee-taxonomy.yaml`

Allowed behavior:

- Revalidate schemas and examples.
- Generate a schema change log.
- Flag breaking changes.
- Publish approved public versions.
- Notify downstream consumers.

## Hard guardrail

Repository webhooks must never directly trigger Shopify, Amazon, Stripe, bank, QuickBooks/Xero, dispute-submission, funding-lead, customer-message, or client-file operations. Those actions require separate authentication, narrow scopes, data minimization, and explicit user confirmation.
