# Ecommerce Fee Audit Site Variations

This directory preserves alternate site builds without changing the canonical production source in `/site/`.

| Variation | Repository path | Generator | Status | Live reference |
|---|---|---|---|---|
| Production | `/site/` | Project workflow | Canonical production | https://ecommerce-fee-audit.vercel.app |
| Platform Fee Audit | `/variants/platform-fee-audit-chatgpt-site/` | ChatGPT Sites | Reference variation | https://platform-fee-audit.feimster.chatgpt.site/ |
| Fee Audit Copilot | `/variants/fee-audit-copilot-agent-launch/` | Agent Launch Site Builder | Candidate variation | Not independently deployed |

## Promotion rule

`/site/` remains the only canonical production source for the primary Vercel project.

A variation may replace `/site/` only through a reviewed change after:

1. Static QA passes.
2. CTA URLs are verified.
3. Embed behavior is tested.
4. Mobile layouts are reviewed.
5. Privacy, redaction, funding, and human-review language is preserved.
6. Public assets contain no credentials or private customer data.
7. Production approval is recorded.

## Optional separate deployments

Each variant can later be connected to its own Vercel project by setting the project root to the corresponding variant directory.

## Source provenance

- ChatGPT Sites build: `platform-fee-audit-chatgpt-site(2).zip`
- Agent Launch build: `fee-audit-copilot-agent-launch(1).zip`
- Import date: 2026-07-28
