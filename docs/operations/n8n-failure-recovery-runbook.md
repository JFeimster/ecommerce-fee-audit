# n8n Failure Recovery Runbook

Classify failed node/workflow, outage, expired credential, duplicate, ambiguous submission, or dead letter. Do not blindly retry consequential ambiguous submissions; verify idempotency or provider status, then use manual requeue, compensation, review, and audited closure.
