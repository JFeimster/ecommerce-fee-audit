---
title: "Fee Dispute Documentation Playbook"
filename: "fee-dispute-documentation-playbook.md"
version: "1.0.0"
status: "production-ready"
purpose: "Evidence, approval, support-message, escalation, and case-control standards for platform-fee disputes and reimbursement requests."
primary_users:
  - "ecommerce operators"
  - "finance operations teams"
  - "funding advisors"
  - "platform support owners"
related_files:
  - "normalized-platform-fee-taxonomy.yaml"
  - "master-transaction-schema.json"
  - "reconciliation-and-calculation-rules.md"
  - "shopify-payout-reconciliation-guide.md"
  - "amazon-settlement-analyzer-guide.md"
  - "stripe-fee-calculation-guide.md"
  - "privacy-redaction-and-data-handling.md"
  - "action-usage-and-confirmation-policy.md"
  - "output-schema.json"
last_updated: "2026-07-27"
---

# Fee Dispute Documentation Playbook

## 1. Purpose and operating rule

Use this playbook to identify, document, submit, and track a potentially disputable platform deduction, missing credit, missing reimbursement, or incorrect reserve treatment.

A variance is not automatically an error. An error is not automatically reimbursable. Platform rules, contracts, evidence requirements, filing windows, and response timelines may change.

The AI Platform Fee Audit Copilot may:

- identify a dispute candidate;
- calculate an evidence-supported variance;
- assemble a draft case package;
- draft support messages;
- track status, evidence, and deadlines;
- recommend escalation for human review.

The Copilot must not:

- guarantee reimbursement;
- fabricate a policy, contract term, document, timestamp, shipment event, tracking event, support response, or case outcome;
- submit a dispute, send a message, upload evidence, or change an external record without explicit user confirmation;
- present an expected fee as authoritative without a dated supporting source;
- characterize a normal contracted fee as leakage merely because it is expensive.

## 2. Core definitions

| Term | Definition |
|---|---|
| Dispute candidate | A deduction, missing credit, missing reimbursement, duplicate charge, or calculation variance supported by enough evidence to justify review. |
| Supported expected amount | Amount derived from a dated agreement, rate card, platform policy, invoice, product data, shipment data, or other authoritative evidence. |
| Potential leakage | Unsupported positive difference between actual and supported expected amounts. |
| Case package | Structured evidence, calculations, timeline, requested resolution, limitations, and approval record. |
| Platform case ID | Identifier assigned by the platform or processor after submission. |
| Recovery | Confirmed credit, reimbursement, refund, reserve release, or correction linked to the case. |
| Human approval | Explicit confirmation by an authorized user before an external write action. |

Use canonical classifications from `normalized-platform-fee-taxonomy.yaml`. Common dispute-related codes include:

- `FEE_PROCESSING`
- `FEE_REFERRAL`
- `FEE_MARKETPLACE`
- `FEE_FBA`
- `FEE_STORAGE`
- `FEE_ADVERTISING`
- `FEE_FX`
- `FEE_INTERNATIONAL`
- `FEE_INSTANT_PAYOUT`
- `REC_REIMBURSEMENT`
- `REC_CREDIT`
- `ADJ_MANUAL`
- `RISK_CHARGEBACK`
- `RISK_DISPUTE`
- `LIQ_RESERVE_HOLD`
- `LIQ_HOLD`
- `UNCLASSIFIED`

## 3. Eligibility screening

### 3.1 Candidate reasons

A case may proceed to documentation when evidence suggests one or more of the following:

- duplicate fee or deduction;
- contracted-rate mismatch;
- unsupported fee category or label;
- incorrect weight, dimensions, product category, geography, card type, service level, or fulfillment basis;
- fee retained contrary to documented refund treatment;
- missing approved reimbursement or credit;
- duplicated advertising charge or billing representation;
- reserve or hold applied contrary to documented release or account status;
- incorrect currency-conversion or international-fee treatment;
- repeated unexplained adjustment;
- incorrect chargeback or dispute lifecycle treatment.

### 3.2 Screen-out reasons

Do not recommend submission when:

- the fee matches the documented rate and basis;
- the expected amount lacks a dated source;
- the difference is solely a valid timing or cutoff difference;
- source rows are duplicates of the same economic event;
- the record is already fully resolved or credited;
- the user lacks authorization to represent the account;
- the claim depends on altered or fabricated evidence;
- the issue requires a legal, tax, accounting, or underwriting conclusion;
- the current filing window or process cannot be verified.

### 3.3 Eligibility decisions

| Decision | Minimum condition | Required output |
|---|---|---|
| `eligible_for_human_review` | Actual amount, expected basis, variance, affected records, and evidence are identified | Draft case package and approval request |
| `needs_more_data` | Plausible issue, but material evidence is missing | Data Gap Report and evidence request |
| `not_supported` | Available evidence supports the charge or contradicts the claim | Advisor-style explanation; no submission |
| `unable_to_determine` | Expected rule, transaction identity, or lifecycle cannot be established | Confidence `Unable to Determine`; human review |
| `duplicate_case` | Same issue and affected records already exist in another case | Link to existing case; do not resubmit |

## 4. Evidence requirements

### 4.1 Required evidence for every case

1. Platform and masked account identifier
2. Audit period and analysis timezone
3. Affected transaction, order, settlement, payout, SKU, reserve, or bank IDs
4. Source file name and source-row reference
5. Actual charged, withheld, or missing amount
6. Supported expected amount or treatment
7. Dated source for the expected treatment
8. Calculation showing the variance
9. Transaction timeline
10. Requested resolution
11. Confidence and unresolved limitations
12. Authorized human approver

### 4.2 Evidence by issue type

| Issue | Strong evidence | Supporting evidence |
|---|---|---|
| Duplicate fee | Two distinct charged rows tied to one economic event | Settlement report, invoice, balance transaction |
| Rate mismatch | Dated contract, pricing plan, rate card, or platform policy | Fee detail, order attributes, card or geography data |
| Fulfillment mismatch | Product dimensions, weight, size tier, shipment or fulfillment record | Catalog history, fee preview, warehouse measurement |
| Missing reimbursement | Approved reimbursement event or documented qualifying loss/damage event | Inventory ledger, case history, shipment evidence |
| Advertising issue | Campaign invoice, spend export, billing statement, account timezone | Platform deduction, card, or bank payment |
| Refund-fee issue | Refund event, original charge, dated refund policy | Balance transaction, settlement line, order timeline |
| FX/international issue | Transaction and settlement currencies, exchange-rate source, card country | Fee detail, payout currency, dated pricing rules |
| Reserve/hold issue | Reserve ledger, hold notice, release criteria, balance history | Payout history, support correspondence |

Apply `privacy-redaction-and-data-handling.md` to every evidence package.

## 5. Case-intake checklist

- [ ] Confirm the user is authorized to act for the account.
- [ ] Assign a unique `case_id`.
- [ ] Record platform, account, currency, timezone, and audit period.
- [ ] Link all affected normalized transaction IDs.
- [ ] Run duplicate detection before calculating leakage.
- [ ] Record actual amount as a non-negative magnitude.
- [ ] Record expected amount and dated evidence source.
- [ ] Separate permanent cost, temporary reserve, timing difference, and transfer activity.
- [ ] Verify the current filing process and response window.
- [ ] Redact prohibited data.
- [ ] Assign confidence, priority, owner, and next action.
- [ ] Obtain explicit confirmation before submission.

## 6. Calculation standards

```text
potential_leakage_amount = max(
    0,
    actual_amount - supported_expected_amount
)
```

For missing reimbursements:

```text
potential_recovery_amount =
    supported_expected_recovery
    - confirmed_recovery_received
```

For multiple affected records:

```text
total_case_amount =
    sum(deduplicated_record_variances)
```

Rules:

- Preserve native currency.
- Do not aggregate currencies without a documented exchange rate and quote direction.
- Use source precision for calculations.
- Round only presentation values to the currency minor unit.
- Use `null`, not zero, when expected amount is unknown.
- Assign `Unable to Determine` when the minimum expected-fee evidence is absent.
- Do not count both a platform credit and its resulting payout increase as two recoveries.
- Do not treat a reserve release as a fee reimbursement unless evidence supports that classification.

## 7. Transaction timeline

Use ISO 8601 dates and timestamps.

| Field | Required | Description |
|---|---:|---|
| `event_at` | Yes | Source timestamp or date |
| `event_type` | Yes | Charge, refund, settlement, payout, deposit, case submission, reply, credit, closure |
| `source_system` | Yes | Platform, processor, bank, or support channel |
| `source_record_id` | When available | Immutable source identifier |
| `amount` | When financial | Amount and currency |
| `evidence_reference` | Yes | File, row, policy, message ID, or case ID |
| `notes` | Optional | Facts only; keep inference separate |

The timeline must show whether the issue is:

- a permanent deduction;
- a temporary liquidity restriction;
- a timing difference;
- an unresolved classification;
- a confirmed recovery.

## 8. Case package structure

Every case package must contain:

1. **Case header** — case ID, owner, platform, account, amount, currency, priority, status.
2. **Finding** — one-sentence issue description.
3. **Evidence** — source records and policy or contract basis.
4. **Calculation** — actual, expected, variance, and method.
5. **Impact** — margin, cash, reporting, customer, or operating impact.
6. **Confidence** — High, Medium, Low, or Unable to Determine.
7. **Requested resolution** — credit, explanation, recalculation, release, correction, or documentation.
8. **Limitations** — missing files, assumptions, or unresolved conflicts.
9. **Approval** — approver, timestamp, scope, and exact external action authorized.
10. **Audit trail** — submission, responses, follow-ups, recovery, and closure.

Recommended filename:

```text
{case_id}_{platform}_{issue_code}_{YYYY-MM-DD}_{document_type}.{ext}
```

Example:

```text
CASE-2026-0042_amazon_fee_fba_2026-07-27_calculation.csv
```

## 9. Support-message templates

All templates are drafts. Verify current platform instructions and obtain explicit approval before sending.

### 9.1 Initial support request

**Subject:** Review requested for [fee or adjustment] — [account] — [period]

Hello,

We are requesting a review of a [fee/adjustment/reimbursement] affecting [account identifier] during [period].

**Affected records:** [IDs]  
**Amount charged or missing:** [currency and amount]  
**Expected amount or treatment:** [currency and amount or treatment]  
**Calculated variance:** [currency and amount]  
**Evidence basis:** [dated contract, rate card, policy, report, or case reference]

The attached package includes the source records, calculation, and timeline. Please confirm the calculation basis and advise whether a correction, credit, reimbursement, or additional documentation is required.

This request does not assume reimbursement is guaranteed. Please provide the applicable policy or calculation detail if the charge is correct.

Thank you.

### 9.2 Focused follow-up

Hello,

Following up on case [platform case ID], submitted [date], regarding [issue]. The unresolved amount is [currency and amount].

Please confirm:

1. Current case status
2. Missing evidence, if any
3. Applicable calculation or policy basis
4. Expected next review date, if available

This follow-up concerns the same affected records: [IDs].

Thank you.

### 9.3 Escalation request

Hello,

Please escalate case [platform case ID] for a second-level review. The prior response did not address the documented variance between [actual treatment] and [supported expected treatment].

**Unresolved variance:** [currency and amount]  
**Evidence previously supplied:** [references]  
**Specific question requiring review:** [one focused question]

Please provide the calculation detail, policy basis, or correction outcome. We understand that escalation does not guarantee reimbursement.

Thank you.

### 9.4 Closure acknowledgement

Hello,

We confirm receipt of [credit/reimbursement/explanation] for case [platform case ID]. Our records show [amount and date] linked to [credit, settlement, or payout ID].

We will mark the case [resolved/partially resolved] with a remaining unresolved amount of [amount or zero]. Please advise if any additional adjustment is pending.

Thank you.

## 10. Case log schema

| Field | Allowed values or format |
|---|---|
| `case_id` | Unique internal ID |
| `platform_case_id` | Platform-issued ID or `null` |
| `platform` | Canonical platform label |
| `account_id` | Masked or internal identifier |
| `issue_code` | Canonical taxonomy code or approved exception code |
| `affected_record_ids` | Array of normalized transaction IDs |
| `opened_at` | ISO 8601 timestamp or `null` |
| `filing_deadline` | ISO date or `null` when unverified |
| `actual_amount` | Non-negative magnitude |
| `expected_amount` | Non-negative magnitude or `null` |
| `potential_recovery_amount` | Non-negative magnitude or `null` |
| `confirmed_recovery_amount` | Non-negative magnitude |
| `currency` | ISO 4217 |
| `status` | See Section 11 |
| `priority` | `critical`, `high`, `medium`, `low` |
| `confidence` | `high`, `medium`, `low`, `unable_to_determine` |
| `owner` | Human owner |
| `next_action` | Specific next step |
| `follow_up_date` | ISO date or `null` |
| `approval_status` | `not_requested`, `pending`, `approved`, `rejected`, `expired` |
| `review_status` | `unreviewed`, `reviewed`, `approved`, `rejected`, `escalated` |
| `resolution` | Summary or `null` |
| `closed_at` | ISO timestamp or `null` |

## 11. Status definitions

| Status | Meaning |
|---|---|
| `candidate` | Possible issue identified; not fully screened |
| `needs_evidence` | Missing material evidence |
| `ready_for_human_review` | Case package is complete enough for review |
| `approved_to_submit` | Explicit approval recorded for a defined action |
| `submitted` | Platform submission confirmed |
| `awaiting_platform` | Waiting for platform response |
| `additional_information_requested` | Platform requested more evidence |
| `escalated` | Submitted for higher-level review |
| `partially_resolved` | Some recovery or correction confirmed |
| `resolved` | Requested correction, explanation, or recovery completed |
| `denied` | Platform rejected the request |
| `withdrawn` | Authorized user withdrew the case |
| `closed_no_action` | Evidence did not support submission |

## 12. Response deadlines and follow-up

- Never invent a filing deadline or service-level commitment.
- Verify the current deadline from a dated policy, platform interface, support response, or contract.
- Record the source and verification date.
- When no deadline is verified, set `filing_deadline` to `null`.
- Prioritize prompt human review when the deadline is unknown.
- Use the existing platform case ID for follow-ups.
- Do not repeatedly submit identical cases.
- Apply idempotency controls from `action-usage-and-confirmation-policy.md`.

## 13. Reimbursement and recovery tracking

A recovery is confirmed only when linked to a source record such as:

- credit;
- reimbursement transaction;
- balance adjustment;
- settlement line;
- payout;
- bank deposit.

Reconciliation sequence:

1. Link the case to the recovery event.
2. Classify recovery as `REC_REIMBURSEMENT`, `REC_CREDIT`, `LIQ_RESERVE_RELEASE`, or another supported code.
3. Match recovery to settlement or balance activity.
4. Match the resulting payout to bank deposit when applicable.
5. Count one economic recovery.
6. Calculate the remaining unresolved amount.

```text
remaining_unresolved_amount = max(
    0,
    supported_case_amount - confirmed_recovery_amount
)
```

## 14. Evidence retention and privacy

- Store only the minimum evidence required.
- Redact full bank account numbers, card data, tax IDs, credentials, customer PII, employee PII, and unrelated transactions.
- Preserve immutable source copies and hashes when permitted.
- Store derived calculations separately from source evidence.
- Follow the organization’s current retention schedule.
- Do not promise that the GPT controls deletion, storage, or third-party retention.
- Use `privacy-redaction-and-data-handling.md` as the authoritative privacy standard.

## 15. Human approval requirements

Explicit human approval is required before:

- submitting or filing a case;
- sending any support message;
- uploading documents;
- changing an external classification or financial record;
- accepting a settlement or closure statement;
- sharing a report outside the authorized organization;
- escalating a case to a platform, processor, bank, accounting system, or legal team.

Approval must identify:

- action;
- destination;
- affected records;
- attachments;
- amount and currency;
- maximum scope.

## 16. Prohibited claims

Do not state or imply:

- “You will recover this amount.”
- “The platform owes you this money” without authoritative determination.
- “This fee is illegal,” “fraudulent,” or “theft” without qualified legal review.
- “The dispute is guaranteed to succeed.”
- “This is a final accounting or tax adjustment.”
- “Funding approval will improve if this is disputed.”

Use:

- “The evidence supports a potential variance of…”
- “This may justify platform review.”
- “Recovery is not guaranteed.”
- “The platform may request additional evidence.”
- “Human review is required before submission.”

## 17. Fictional worked example

**Business:** Northstar Outfitters LLC (fictional)  
**Platform:** Amazon US  
**Issue:** Potential duplicate FBA fee  
**Period:** 2026-06-01 through 2026-06-30  
**Currency:** USD

Two settlement lines reference the same order item, quantity, fee type, and fulfillment event:

| Transaction ID | Source record ID | Classification | Amount |
|---|---|---|---:|
| `txn_fic_1001` | `src_fic_a91` | `FEE_FBA` | 8.40 |
| `txn_fic_1002` | `src_fic_a92` | `FEE_FBA` | 8.40 |

The evidence supports one expected fee of $8.40.

```text
actual_amount = 16.80
supported_expected_amount = 8.40
potential_leakage_amount = 8.40
```

- **Finding:** The evidence supports a potential duplicate FBA fee of $8.40.
- **Evidence:** Two charged settlement rows tied to one fulfillment event.
- **Impact:** $8.40 potential recovery; low individual materiality but useful control signal if recurring.
- **Confidence:** High for the duplicate calculation; reimbursement outcome unknown.
- **Priority:** Medium.
- **Recommendation:** Human-review the package, verify the filing window, and approve or reject submission.
- **Notice:** Recovery is not guaranteed.

## 18. Final review checklist

- [ ] Affected records are deduplicated.
- [ ] Expected treatment has a dated source.
- [ ] Actual, expected, and variance reconcile.
- [ ] Currency and period are explicit.
- [ ] Evidence is redacted and minimized.
- [ ] Claim language is factual and non-guaranteed.
- [ ] Platform process and deadline are current or marked unverified.
- [ ] Human approval is documented.
- [ ] External action follows idempotency and confirmation policy.
- [ ] Recovery tracking avoids double counting.
