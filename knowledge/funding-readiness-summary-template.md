---
title: "Funding Readiness Summary Template"
filename: "funding-readiness-summary-template.md"
version: "1.0.0"
status: "production-ready"
purpose: "Compliance-safe template for summarizing reconciled cash timing, unit economics, reserve exposure, working-capital need, documentation readiness, and unresolved risk."
primary_users:
  - "ecommerce operators"
  - "small-business owners"
  - "finance operations teams"
  - "funding advisors"
related_files:
  - "ecommerce-platform-fee-audit-worksheet.md"
  - "reconciliation-and-calculation-rules.md"
  - "sku-contribution-margin-scorecard.csv"
  - "reserve-and-hold-tracker.csv"
  - "monthly-fee-variance-dashboard-schema.json"
  - "output-schema.json"
  - "privacy-redaction-and-data-handling.md"
last_updated: "2026-07-27"
---

# Funding Readiness Summary Template

## How to use this template

Use this document only after completing the available payout reconciliation and data-quality review. Replace bracketed fields with evidence-supported values. Delete sections that are not applicable, but do not remove limitations, confidence, human-review, or disclaimer sections.

This is an operational readiness document. It may help organize information for a funding conversation, but it is not a credit decision, underwriting determination, accounting opinion, tax opinion, legal opinion, or guarantee of eligibility, approval, pricing, terms, or funding speed.

### Required evidence labels

- **Verified Fact** — supported by a source record or reconciled source total.
- **User-Provided Data** — stated by the user but not independently reconciled.
- **Assumption** — explicit operating assumption.
- **Calculation** — derived using documented formulas.
- **Inference** — interpretation supported by evidence but not directly observed.
- **Recommendation** — suggested next action, not a guarantee.

Use only these confidence labels:

- **High**
- **Medium**
- **Low**
- **Unable to Determine**

---

# [Business Name] — Funding Readiness Summary

**Report ID:** [report_id]  
**Prepared on:** [ISO 8601 timestamp]  
**Audit period:** [period_start] through [period_end]  
**Analysis timezone:** [IANA timezone]  
**Reporting currency:** [ISO 4217 currency]  
**Platforms reviewed:** [platforms]  
**Overall confidence:** [High / Medium / Low / Unable to Determine]  
**Reconciliation status:** [matched / matched_with_timing_difference / partial / unmatched / data_gap / human_review_required]

> **Important:** This summary is based on the documents and authorized data available for the stated period. Eligibility varies, terms may change, and funding is not guaranteed. Any lender, funder, bank, investor, or platform will apply its own eligibility, verification, underwriting, and compliance standards.

## 1. Executive summary

### Direct answer

[Write a 40–60 word evidence-based answer explaining whether the business appears operationally prepared to begin a funding conversation, what the primary cash or margin constraint is, and which unresolved issue matters most. Do not state that the business qualifies or will be approved.]

### At-a-glance

| Dimension | Status | Evidence-supported result | Confidence |
|---|---|---|---|
| Payout reconciliation | [status] | [result] | [confidence] |
| Revenue consistency | [status] | [result] | [confidence] |
| Fee burden | [status] | [result] | [confidence] |
| SKU economics | [status] | [result] | [confidence] |
| Reserve exposure | [status] | [result] | [confidence] |
| Cash conversion timing | [status] | [result] | [confidence] |
| Working-capital gap | [status] | [result] | [confidence] |
| Documentation readiness | [status] | [result] | [confidence] |
| Unresolved risk | [status] | [result] | [confidence] |

### Primary conclusion

- **Finding:** [Most important evidence-supported finding]
- **Evidence:** [Source totals, reconciliations, and date range]
- **Business impact:** [Cash, margin, timing, documentation, or operating impact]
- **Confidence:** [level]
- **Priority:** [Critical / High / Medium / Low]
- **Recommended next action:** [one concrete action]

## 2. Data coverage and quality

### Files reviewed

| File or source | Platform/account | Period covered | Status | Notes |
|---|---|---|---|---|
| [source] | [account] | [dates] | [usable/partial/unusable] | [notes] |

### Coverage summary

- **Requested period:** [dates]
- **Covered period:** [dates]
- **Date overlap:** [complete / partial / none]
- **Currencies:** [currencies]
- **Source records reviewed:** [count]
- **Absolute in-scope value:** [currency and amount]
- **Reconciled share:** [percentage]
- **Unclassified share:** [percentage]
- **Duplicate records excluded:** [count and amount]
- **Materiality threshold:** [currency and amount]

Use the operating default only when the user has not approved another threshold:

```text
materiality_threshold = max(
    10 currency units,
    0.1% × absolute gross sales in scope
)
```

This is an operational default, not an accounting standard.

### Missing or unresolved data

| Missing item | Affected conclusion | Impact | Required next document | Priority |
|---|---|---|---|---|
| [item] | [conclusion] | [impact] | [document] | [priority] |

When minimum evidence is unavailable:

- label the affected conclusion **Unable to Determine**;
- state which calculation is withheld;
- request the minimum next document;
- do not estimate missing financial values.

## 3. Revenue profile

| Metric | Current period | Comparison period | Change | Evidence label |
|---|---:|---:|---:|---|
| Gross sales | [amount] | [amount] | [amount / %] | [label] |
| Discounts | [amount] | [amount] | [amount / %] | [label] |
| Refunds | [amount] | [amount] | [amount / %] | [label] |
| Net product revenue | [amount] | [amount] | [amount / %] | [label] |
| Shipping income | [amount] | [amount] | [amount / %] | [label] |
| Reimbursements and credits | [amount] | [amount] | [amount / %] | [label] |

### Revenue observations

- [Describe concentration, volatility, seasonality, refunds, channel mix, or data limitations.]
- [Do not classify pass-through tax, loan proceeds, payouts, transfers, or reserve releases as revenue.]

## 4. Net payout profile

### Reconciliation bridge

| Component | Amount |
|---|---:|
| Opening platform balance | [amount] |
| Gross sales and supported revenue | [amount] |
| Discounts and refunds | ([amount]) |
| Permanent platform and processing fees | ([amount]) |
| Advertising deducted by platform | ([amount]) |
| Financing remittances | ([amount]) |
| New reserve or hold | ([amount]) |
| Reserve or hold release | [amount] |
| Reimbursements and credits | [amount] |
| Taxes, duties, and withholding | [amount with treatment noted] |
| Other supported adjustments | [amount] |
| Expected payout | [amount] |
| Reported payout | [amount] |
| Unexplained variance | [amount] |

### Payout-to-bank summary

| Payout ID | Initiated | Expected arrival | Bank posted | Payout amount | Deposit amount | Variance | Status |
|---|---|---|---|---:|---:|---:|---|
| [ID] | [date] | [date] | [date] | [amount] | [amount] | [amount] | [status] |

State whether unmatched items are:

- permanent deductions;
- valid timing differences;
- missing source data;
- unresolved exceptions;
- unsupported classifications.

## 5. Fee burden

| Fee category | Amount | Rate basis | Effective rate | Period variance | Finding |
|---|---:|---|---:|---:|---|
| Processing | [amount] | [denominator] | [rate] | [variance] | [finding] |
| Marketplace/referral | [amount] | [denominator] | [rate] | [variance] | [finding] |
| Fulfillment/storage | [amount] | [denominator] | [rate] | [variance] | [finding] |
| Advertising | [amount] | [denominator] | [rate] | [variance] | [finding] |
| FX/international | [amount] | [denominator] | [rate] | [variance] | [finding] |
| Instant payout | [amount] | [denominator] | [rate] | [variance] | [finding] |
| Other | [amount] | [denominator] | [rate] | [variance] | [finding] |

```text
platform_fee_rate =
    permanent_platform_fees
    / applicable_net_revenue
```

```text
effective_fee_rate = (
    permanent_platform_fees
    + payment_fees
    + variable_fulfillment_fees
) / applicable_net_revenue
```

- **Potential fee leakage:** [amount or Unable to Determine]
- **Supported dispute candidates:** [count and amount]
- **Recurring control issue:** [yes/no and explanation]

Do not call a normal contracted fee “leakage.” A dispute candidate requires a dated expected-fee source.

## 6. Refund, return, dispute, and chargeback exposure

| Metric | Result | Trend | Operational impact | Confidence |
|---|---:|---|---|---|
| Refund rate by value | [rate] | [trend] | [impact] | [confidence] |
| Return rate by units | [rate] | [trend] | [impact] | [confidence] |
| Chargeback rate by value | [rate] | [trend] | [impact] | [confidence] |
| Open dispute amount | [amount] | [trend] | [impact] | [confidence] |

Clearly separate:

- refunded principal;
- returned units;
- dispute principal;
- chargeback fee;
- return-processing cost;
- recovered amount.

## 7. Reserve and hold exposure

| Platform/account | Reserve type | Current balance | Expected release | Aging days | Documentation | Cash impact | Priority |
|---|---|---:|---|---:|---|---|---|
| [account] | [type] | [amount] | [date or unknown] | [days] | [status] | [impact] | [priority] |

```text
reserve_exposure_ratio =
    ending_reserve_balance
    / applicable_net_revenue
```

- **Total current reserve and hold exposure:** [amount]
- **Verified expected releases within forecast horizon:** [amount]
- **Unverified or disputed release amount:** [amount]
- **Key documentation gap:** [gap]

Reserve holds affect available cash but are not automatically permanent expenses.

## 8. Financing deductions and existing obligations

| Obligation | Provider | Original amount | Current balance | Period remittance | Payment basis | Data status |
|---|---|---:|---:|---:|---|---|
| [obligation] | [provider] | [amount] | [amount] | [amount] | [fixed/%/other] | [verified/user-provided/unknown] |

Separate:

- financing principal;
- financing cost or fee;
- current remittance;
- reserve or hold activity;
- new funding proceeds;
- transfers between accounts.

Do not treat financing principal as a product-level variable cost by default. A supported variable financing cost may be shown separately.

## 9. SKU economics

Use `sku-contribution-margin-scorecard.csv` as the canonical structure.

### Portfolio summary

| Score band | SKU count | Net product revenue | Contribution profit | Primary action |
|---|---:|---:|---:|---|
| Strong | [count] | [amount] | [amount] | [action] |
| Watch | [count] | [amount] | [amount] | [action] |
| Weak | [count] | [amount] | [amount] | [action] |
| Negative | [count] | [amount] | [amount] | [action] |
| Unable to determine | [count] | [amount] | [amount/null] | [action] |

### Material SKU findings

| SKU | Net revenue | Contribution profit | Margin % | Refund rate | Ad ratio | Score | Confidence | Action |
|---|---:|---:|---:|---:|---:|---:|---|---|
| [SKU] | [amount] | [amount] | [rate] | [rate] | [rate] | [score] | [confidence] | [action] |

Do not claim a SKU is profitable when COGS, fulfillment, shipping, advertising, or another material variable cost is missing.

## 10. Cash conversion timing

| Stage | Median days | Range | Evidence coverage | Finding |
|---|---:|---|---|---|
| Transaction to available | [days] | [range] | [coverage] | [finding] |
| Available to payout | [days] | [range] | [coverage] | [finding] |
| Payout to bank | [days] | [range] | [coverage] | [finding] |
| Total cash conversion | [days] | [range] | [coverage] | [finding] |

Classify the dominant issue:

- [ ] Margin problem
- [ ] Timing problem
- [ ] Combined margin and timing problem
- [ ] Unable to determine

Explain the evidence supporting the classification.

## 11. Working-capital gap

Use a daily or weekly cash schedule.

```text
ending_unrestricted_cash_t =
    opening_unrestricted_cash_t
    + verified_expected_inflows_t
    - verified_expected_outflows_t
```

```text
cash_buffer_shortfall_t = max(
    0,
    required_minimum_cash_buffer_t
    - ending_unrestricted_cash_t
)
```

```text
working_capital_gap =
    max(cash_buffer_shortfall_t over forecast horizon)
```

| Scenario | Forecast horizon | Minimum cash point | Required buffer | Estimated gap | Confidence |
|---|---|---:|---:|---:|---|
| Base | [dates] | [amount/date] | [amount] | [amount] | [confidence] |
| Downside | [dates] | [amount/date] | [amount] | [amount] | [confidence] |
| Upside | [dates] | [amount/date] | [amount] | [amount] | [confidence] |

Rules:

- Do not count uncertain future funding as a verified inflow.
- Show possible funding or recovery only as a separate scenario.
- Do not hide a negative-margin problem inside a cash-timing explanation.
- Identify whether inventory, advertising, reserves, payout delays, financing remittances, or operating costs drive the gap.

## 12. Documentation readiness

| Document category | Status | Period | Quality issue | Next action |
|---|---|---|---|---|
| Platform statements | [status] | [period] | [issue] | [action] |
| Bank statements | [status] | [period] | [issue] | [action] |
| Processor statements | [status] | [period] | [issue] | [action] |
| Financial statements | [status] | [period] | [issue] | [action] |
| Debt or financing schedules | [status] | [period] | [issue] | [action] |
| Entity and ownership documents | [status] | [period] | [issue] | [action] |
| Tax documentation | [status] | [period] | [issue] | [action] |
| Inventory and SKU cost support | [status] | [period] | [issue] | [action] |

Do not request or store unnecessary sensitive data. Use redacted copies when possible.

## 13. Potential funding-use scenarios

These are operating scenarios, not product recommendations, approvals, or eligibility predictions.

| Scenario | Evidence-supported use | Estimated amount | Timing need | Repayment source | Key risk |
|---|---|---:|---|---|---|
| Inventory timing | [use] | [amount] | [date] | [source] | [risk] |
| Advertising bridge | [use] | [amount] | [date] | [source] | [risk] |
| Reserve bridge | [use] | [amount] | [date] | [source] | [risk] |
| Payout-delay bridge | [use] | [amount] | [date] | [source] | [risk] |
| Consolidation/refinance review | [use] | [amount] | [date] | [source] | [risk] |

For each scenario, state:

- whether the need is temporary or recurring;
- whether contribution margin conceptually supports repayment;
- which assumptions require verification;
- that eligibility and terms vary;
- that a qualified provider must perform its own review.

## 14. Unresolved discrepancies and risks

| Issue | Amount at risk | Evidence | Confidence | Priority | Required resolution |
|---|---:|---|---|---|---|
| [issue] | [amount] | [evidence] | [confidence] | [priority] | [action] |

Mandatory human-review topics include:

- material unexplained reconciliation differences;
- tax, duty, withholding, or accounting classification;
- disputed fees or chargebacks;
- material financing deductions;
- multi-currency conflicts;
- incomplete COGS or SKU cost allocation;
- ambiguous reserve treatment;
- funding or credit decisions.

## 15. Required next actions

### Before a funding conversation

1. [Highest-impact documentation or reconciliation action]
2. [Cash-flow or margin action]
3. [Reserve, dispute, or payout action]
4. [Document organization action]
5. [Qualified human review, if required]

### Optional operational improvements

- [Process improvement]
- [Dashboard or alert]
- [SKU action]
- [Payout monitoring action]

## 16. Human-review notice

Human review is required before this report is:

- submitted to a lender, funder, bank, investor, accountant, tax professional, attorney, or platform;
- used to update accounting or financial records;
- used to file a dispute or make a certification;
- shared externally;
- relied upon for a funding, credit, legal, tax, or accounting decision.

## 17. Disclaimer

This summary is designed to support finance-operations organization and funding readiness. It does not constitute legal, tax, accounting, investment, lending, brokerage, underwriting, or credit advice. It does not guarantee reimbursement, approval, eligibility, rates, terms, revenue, margin improvement, or funding speed. Platform policies and funding terms may change. Independent verification and qualified human review may be required.

---

# Fictional completed excerpt

**Business:** Northstar Outfitters LLC (fictional)  
**Audit period:** 2026-04-01 through 2026-06-30  
**Overall confidence:** Medium  
**Reconciliation status:** `partial`

**Direct answer:** Northstar appears prepared to begin an exploratory funding conversation, but the analysis does not establish eligibility. Payouts are substantially reconciled, while a $24,000 temporary reserve and incomplete SKU freight allocation reduce confidence. The primary need appears to be a timing gap rather than a proven company-wide margin failure.

- **Verified Fact:** 92% of absolute in-scope value is reconciled.
- **Calculation:** Base-case working-capital gap is $31,500 over the next eight weeks.
- **Inference:** The dominant constraint appears to be reserve and inventory timing.
- **Limitation:** Inbound freight is missing for 18% of SKU revenue.
- **Recommendation:** Complete SKU cost support and verify reserve release timing before selecting a funding product.
- **Notice:** Eligibility varies, terms may change, and approval is not guaranteed.
