# Job Recovery Runbook

For stalled, timed-out, duplicate, partial, or ambiguous jobs, inspect the audit trail and idempotency key first. Verify any external destination state before requeue. Persist partial results, apply compensation where defined, then requeue within policy or dead-letter for review. Escalate provider outages and unresolved submissions; never silently repeat a consequential external submission.
