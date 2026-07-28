---
title: "Reconciliation and Calculation Rules"
filename: "reconciliation-and-calculation-rules.md"
version: "1.0.0"
status: "production-ready"
purpose: "Authoritative formulas, reconciliation sequence, duplicate controls, thresholds, and confidence rules for platform-fee audits."
primary_users:
  - "AI Platform Fee Audit Copilot"
  - "ecommerce finance operations teams"
  - "operators and human reviewers"
related_files:
  - "ai-platform-fee-audit-copilot-builder-instructions.md"
  - "ecommerce-platform-fee-audit-worksheet.md"
  - "normalized-platform-fee-taxonomy.yaml"
  - "master-transaction-schema.json"
  - "column-mapping-library.json"
last_updated: "2026-07-27"
---

# Reconciliation and Calculation Rules

## 1. Authority and Scope

These are the canonical operational rules for the AI Platform Fee Audit Copilot. They support ecommerce finance operations and do not determine accounting, tax, legal, platform-policy, underwriting, lending, or reimbursement treatment. Material conclusions require human review.

## 2. Required Calculation Order

Always work in this order:

1. Validate file coverage, dates, timezone, currency, source totals, and data grain.
2. Normalize source fields without overwriting source evidence.
3. Detect and resolve duplicates before aggregation.
4. Classify transactions using `normalized-platform-fee-taxonomy.yaml`.
5. Reconcile transactions to settlements.
6. Reconcile settlements to payouts.
7. Reconcile payouts to bank deposits.
8. Analyze fee leakage and period variance.
9. Calculate order- and SKU-level contribution margin only when required costs are sufficiently complete.
10. Diagnose margin pressure, timing pressure, or both.
11. Calculate working-capital gap only from evidence-supported inflows and outflows.

Do not calculate definitive margin or leakage conclusions from materially unreconciled data. Label limited results **Preliminary — Partial Reconciliation** and lower confidence.

---

# 3. Sign, Date, Currency, and Null Conventions

## 3.1 Signed amount convention

- `source_amount` preserves the original source sign.
- `normalized_amount` is positive when merchant economic value or cash increases.
- `normalized_amount` is negative when merchant economic value or cash decreases.
- Dedicated component fields such as `fee_amount`, `refund_amount`, `reserve_hold_amount`, and `cogs_amount` store non-negative magnitudes.
- Formulas explicitly add or subtract component magnitudes.

## 3.2 Transfer convention

A payout transfers value out of a platform or processor clearing balance. A bank deposit transfers that value into bank cash. Neither is revenue. In a consolidated cash view, the matched pair has zero economic impact.

## 3.3 Date convention

Use ISO 8601. Preserve source timestamp and timezone or offset. Do not treat these as interchangeable:

- Transaction date
- Available-on date
- Settlement date
- Payout initiation date
- Expected bank-arrival date
- Bank-posted date

Period analysis must use an explicitly approved analysis timezone.

## 3.4 Currency convention

Reconcile each currency separately before consolidation. Record:

- Transaction currency
- Settlement currency
- Bank currency
- Exchange rate
- Quote direction, such as `USD_per_EUR`
- Rate source
- Conversion date or timestamp
- Explicit FX fee, if any

Do not infer a conversion rate from two amounts when fees, reserves, or timing differences may also explain the variance unless clearly labeled as an inference and reviewed.

## 3.5 Null and zero

- `null` means unknown, unavailable, or not applicable.
- `0` means a confirmed numeric zero.
- Never replace null with zero to make a formula complete.
- If a required amount is missing, withhold the affected calculation or issue a Data Gap Report.

## 3.6 Precision and rounding

- Preserve source precision.
- Use decimal arithmetic in production.
- Retain at least four decimal places or platform-native precision in intermediate calculations.
- Round only presentation values using the currency's customary minor unit.
- Record material rounding residuals separately; do not plug them into fees or adjustments.

---

# 4. Data Grain and Control Totals

Determine each file's grain before aggregation:

- Order
- Order line
- Payment transaction
- Fee component
- Settlement line
- Payout
- Bank transaction
- Daily or campaign advertising aggregate
- Reserve movement
- Reserve balance snapshot

An order export may repeat order totals on multiple line-item rows. A settlement row may contain one component rather than one complete transaction. An advertising export may aggregate by day, campaign, ad group, ad, product, or attribution event.

For every source file, record:

- File ID
- Source system
- Export type/version
- Coverage period
- Timezone
- Currency
- Row count
- Available source control total
- Grain
- Known limitations

Never sum a field until its grain and duplicate behavior are documented.

---

# 5. Duplicate Detection

Run duplicate detection before any financial totals.

## 5.1 Exact duplicate fingerprint

Recommended deterministic fingerprint input:

```text
source_system | source_account_id | source_record_id | transaction_at |
transaction_currency | source_amount | source_transaction_type |
order_id | settlement_id | payout_id
```

Normalize surrounding whitespace and descriptive-field case, while preserving identifier characters and numeric precision. Hash with SHA-256 in production.

## 5.2 Probable duplicate rules

Flag probable duplicates when:

- The same account, currency, amount, and transaction type occur within a narrow time window.
- The same order or charge appears in overlapping exports.
- The same payout appears in payout summary and itemized transaction files.
- The same advertising spend appears in an ad export, marketplace settlement, invoice, and bank activity.
- A reserve balance snapshot is treated as a new reserve movement.
- A reimbursement and a related adjustment credit appear to represent the same recovery.

Do not automatically delete probable duplicates. Group them, identify the authoritative economic record, and retain lineage.

## 5.3 Related records are not duplicates

A sale, fee, payout, and bank deposit may share an identifier or amount but represent different lifecycle stages. Mark them `related_not_duplicate` when evidence supports separate events.

---

# 6. Gross-to-Net Revenue Rules

## 6.1 Net merchandise revenue

```text
net_merchandise_revenue = gross_item_sales
                         - discounts
                         - refunded_merchandise_revenue
```

## 6.2 Economic revenue for contribution analysis

```text
economic_revenue = net_merchandise_revenue
                 + shipping_income_retained
                 + tips_retained
```

Exclude from product revenue:

- Taxes and duties
- Payouts and bank deposits
- Reserve releases
- Reimbursements unless the underlying treatment specifically requires revenue restoration
- Financing proceeds
- Loan proceeds
- Transfers between internal accounts

---

# 7. Settlement Reconciliation

## 7.1 Signed-record method

When normalized signed records are complete:

```text
expected_settlement = opening_platform_balance
                    + sum(normalized_amount for in-scope settlement activity)
                    - closing_balance_carried_forward
```

## 7.2 Component method

When separate component magnitudes are used:

```text
expected_settlement = gross_sales
                    + shipping_income
                    + tips
                    + tax_collected
                    + duties_collected
                    - discounts
                    - refunds
                    - chargeback_principal
                    - permanent_platform_fees
                    - advertising_deducted_in_settlement
                    - tax_or_regulatory_withholding
                    - financing_remittances
                    - reserve_holds
                    + reserve_releases
                    + reimbursements
                    + credits
                    +/- supported_adjustments
                    + opening_balance
                    - closing_balance_carried_forward
```

```text
settlement_variance = reported_settlement - expected_settlement
```

Do not use an unexplained adjustment to force the bridge to zero.

## 7.3 Settlement status

- `matched`: unexplained variance is within approved materiality and no material classification remains unresolved.
- `matched_with_timing_difference`: variance is supported by a dated, expected resolving event.
- `partial`: limited calculations are reliable but required data remains missing.
- `unmatched`: material unexplained variance remains.
- `data_gap`: minimum evidence is unavailable.
- `human_review_required`: treatment is materially ambiguous or outside operational scope.

---

# 8. Payout Reconciliation

A settlement may create one payout, multiple payouts, a payout plus reserve, or no immediate payout.

```text
expected_payout = reported_settlement_available_for_payout
                - payout_level_fees
                - payout_level_holds
                + payout_level_releases
```

```text
payout_variance = reported_payout - expected_payout
```

Preferred match order:

1. Exact payout ID
2. Exact platform trace/reference
3. Currency, amount, account, and date
4. One-to-many match
5. Many-to-one match
6. FX-adjusted match
7. Manual match with documented evidence

Failed, canceled, withdrawn, reversed, or minimum-balance payouts remain unresolved until subsequent evidence closes the lifecycle.

---

# 9. Bank-Deposit Matching

## 9.1 Match hierarchy

1. Exact bank trace/reference ID
2. Exact payout ID in bank memo or reference
3. Exact currency and amount within the approved arrival window
4. One payout to multiple deposits
5. Multiple payouts to one deposit
6. FX-adjusted match with supported rate and fee
7. Manual match with retained evidence

## 9.2 Formulas

```text
amount_variance = bank_amount_converted_to_payout_currency - payout_amount

date_variance_days = bank_posted_date - payout_initiated_date

payout_to_bank_days = bank_posted_date - payout_initiated_date

total_cash_conversion_days = bank_posted_date - transaction_capture_date
```

Report calendar days unless business-day logic, holidays, and jurisdiction are explicitly configured.

A platform status such as “deposited” may mean the platform sent funds; it does not prove the bank posted them. Bank activity is required for final bank matching.

---

# 10. Refund Treatment

Refunded principal is contra-revenue. Refund-related fees are separate costs.

Do not:

- Subtract the same refund in both order and settlement layers as two economic losses.
- Treat refund principal as a processing fee.
- Assume processing fees are returned or retained without evidence.
- Treat a failed refund as a completed cash outflow.

Cross-period refunds should:

- Remain in the settlement period for cash reconciliation.
- Link to the original order or charge when possible.
- Be disclosed separately for cohort, SKU, and period-margin analysis.

---

# 11. Chargeback and Dispute Treatment

Track separately:

- Disputed principal
- Dispute or chargeback fee
- Provisional hold
- Reserve impact
- Final outcome
- Recovery or reversal

A dispute opening is not automatically a permanent loss. Use the current and final lifecycle status. Lower confidence when outcome or recovery evidence is missing.

---

# 12. Reserve and Hold Treatment

## 12.1 Reserve ledger

```text
ending_reserve = opening_reserve
               + new_reserve_holds
               - reserve_releases
               - reserve_applied_to_confirmed_losses
               +/- supported_reserve_adjustments
```

## 12.2 Cash and margin treatment

- New reserve hold: reduces available cash.
- Reserve release: increases available cash.
- Hold and release: no contribution-margin impact by default.
- Amount applied to a confirmed loss: classify the underlying loss separately.

Do not treat a reserve balance snapshot as a new hold.

## 12.3 Reserve metrics

```text
reserve_exposure_ratio = ending_reserve_balance / applicable_net_revenue

reserve_aging_days = analysis_date - hold_start_date
```

If applicable net revenue is zero or null, reserve exposure ratio is null.

Expected release dates are estimates, not guarantees. Flag overdue items for review, not automatic dispute.

---

# 13. Reimbursements, Credits, and Adjustments

A reimbursement restores value related to an underlying loss or error. A credit offsets a charge. A reserve release returns restricted funds. Keep them distinct.

Apply a recovery to the same economic category as the underlying loss only when evidence supports that treatment. Otherwise keep it separate and require human accounting review.

Generic adjustments must preserve source description. Material unresolved adjustments reduce confidence.

---

# 14. Financing-Remittance Treatment

Financing deductions reduce payout cash but are not platform fees.

```text
financing_remittance = principal_repayment
                     + financing_cost
                     + other_supported_component
```

- Exclude principal from contribution margin.
- Include financing cost only in a clearly labeled financing-cost or fully loaded view when documents support the split.
- If the split is unavailable, retain the full deduction as `financing_remittance_unallocated`.
- Require human review for allocation.
- Do not double-count a platform deduction and a matching bank payment.

Funding-readiness outputs may summarize obligations and cash impact but may not make a credit decision or guarantee eligibility.

---

# 15. Tax, Duty, and Withholding Treatment

Taxes and duties are pass-through by default for operational margin analysis. Track collection, withholding, remittance, and reversal separately.

Tax, duty, VAT/GST, nexus, marketplace-facilitator, and accounting treatment always require qualified human review. Do not infer tax liability from settlement labels alone.

---

# 16. Shipping Income and Cost Treatment

Track separately:

- Customer shipping income
- Shipping label cost
- Carrier cost
- Fulfillment fee
- Return shipping
- Shipping refund

```text
shipping_contribution = shipping_income_retained
                      - outbound_shipping_cost
                      - shipping_label_cost
                      - return_shipping_cost
```

Do not subtract both a bundled fulfillment fee and an embedded shipping component unless the source separates them.

---

# 17. Advertising Attribution

## 17.1 Preferred allocation hierarchy

1. Direct order or SKU attribution supported by IDs
2. Campaign-to-product mapping
3. Revenue-share allocation
4. Unit-share allocation
5. Contribution-weighted allocation
6. Platform-level only, with no SKU allocation

Document:

- Attribution window
- Reporting latency
- Account timezone
- Conversion date logic
- Currency
- Credits and taxes
- Allocation method
- Allocation confidence

## 17.2 Formula

```text
advertising_to_sales_ratio = attributable_advertising_cost / applicable_net_revenue
```

## 17.3 Double-counting control

The same spend may appear in:

- Advertising platform export
- Marketplace settlement deduction
- Platform invoice
- Card or bank payment

Select one authoritative expense record. Use the other records only for settlement, liability, and payment reconciliation.

---

# 18. Multi-Currency Reconciliation

Reconcile native currency before consolidation.

```text
converted_amount = source_amount × exchange_rate
```

The exchange-rate quote must state units, such as `USD_per_EUR`.

Separate:

- Economic transaction amount
- Explicit FX fee
- International fee
- Exchange-rate difference
- Timing difference

Do not combine currencies in gross sales, fee rates, unmatched totals, or margin without conversion. Present both native and consolidated values.

---

# 19. Contribution-Margin Rules

## 19.1 SKU-level contribution profit

```text
net_product_revenue = gross_product_sales
                    - discounts
                    - product_refunds
```

```text
sku_contribution_profit = net_product_revenue
                        + allocated_shipping_income
                        + retained_tips_if_applicable
                        - cogs
                        - inbound_freight_allocated
                        - packaging
                        - fulfillment
                        - outbound_shipping
                        - processing_fees
                        - marketplace_fees
                        - storage_allocated
                        - advertising_allocated
                        - return_processing_and_shipping
                        - chargeback_cost
                        - supported_variable_financing_cost
                        - other_supported_variable_cost
```

```text
sku_contribution_margin_pct = sku_contribution_profit / net_product_revenue
```

If net product revenue is zero or null, contribution-margin percentage is null.

Exclude from contribution margin by default:

- Taxes and duties
- Financing principal
- Reserve holds and releases
- Payouts and bank deposits
- Loan proceeds
- Fixed overhead unless a separate fully loaded view is requested

## 19.2 Order-level contribution profit

Use the same logic at order grain. Allocate shared discounts, fees, and shipping with a documented method. Do not duplicate order totals across line items.

## 19.3 Platform-level contribution profit

Either:

- Aggregate deduplicated SKU or order results; or
- Calculate from reconciled platform totals.

Do not do both and add them together.

---

# 20. Fee and Risk Metrics

```text
platform_fee_rate = permanent_platform_fees / applicable_net_revenue

effective_fee_rate = (permanent_platform_fees
                    + payment_fees
                    + variable_fulfillment_fees)
                    / applicable_net_revenue

refund_rate_value = refunded_merchandise_value / gross_merchandise_sales

refund_rate_units = refunded_or_returned_units / units_sold

chargeback_rate_value = chargeback_principal / gross_payment_volume

chargeback_rate_count = chargeback_count / successful_charge_count

reserve_exposure_ratio = ending_reserve_balance / applicable_net_revenue

unmatched_rate = absolute_unmatched_value / absolute_in_scope_value

unclassified_rate = absolute_unclassified_value / absolute_in_scope_value
```

Always state numerator, denominator, period, currency, and whether a rate is value-based or count-based.

---

# 21. Fee-Leakage Rules

A fee is a leakage candidate only when evidence indicates one or more of:

- Duplicate charge
- Unsupported fee label or amount
- Contract or documented-rate mismatch
- Incorrect category, geography, card, weight, dimension, or fulfillment basis
- Fee retained contrary to documented refund treatment
- Missing reimbursement after an approved event
- Fee rate changed without an identified plan or policy change
- Repeated unexplained adjustment

Do not label normal contracted fees as leakage.

```text
potential_leakage_amount = actual_fee - supported_expected_fee
```

The expected fee must have a dated evidence source. If the expected rule is unavailable, report **Unable to Determine**, not zero.

---

# 22. Payout Delay and Cash-Timing Rules

```text
transaction_to_available_days = available_on - transaction_capture_date

available_to_payout_days = payout_initiated_date - available_on

payout_to_bank_days = bank_posted_date - payout_initiated_date

total_cash_conversion_days = bank_posted_date - transaction_capture_date
```

A timing problem exists when economically profitable activity creates a temporary cash deficit because of payout delays, reserves, inventory lead times, receivable terms, advertising timing, or financing deductions.

A margin problem exists when contribution profit is persistently weak or negative after sufficient cost allocation.

A combined problem exists when both conditions are present.

---

# 23. Working-Capital Gap

Use a daily or weekly cash schedule.

```text
ending_unrestricted_cash_t = opening_unrestricted_cash_t
                           + verified_expected_inflows_t
                           - verified_expected_outflows_t
```

```text
cash_buffer_shortfall_t = max(
    0,
    required_minimum_cash_buffer_t - ending_unrestricted_cash_t
)
```

```text
working_capital_gap = max(cash_buffer_shortfall_t over forecast horizon)
```

Do not include uncertain future funding proceeds as verified inflows. Show them only as separately labeled scenarios.

Scenario labels:

- **Base:** Evidence-supported timing and amounts
- **Downside:** Clearly labeled adverse timing or cost assumptions
- **Upside:** Supported improvement scenario, not a guarantee

---

# 24. Double-Counting Control Matrix

| Economic event | Common duplicate records | Required control |
|---|---|---|
| Sale | Order export, payment transaction, settlement line | Recognize revenue once; use other records for lifecycle matching |
| Refund | Order refunded amount, refund transaction, settlement line | Recognize contra-revenue once; use settlement record for cash reconciliation |
| Processing fee | Fee detail, combined net, invoice, bank payment | Use itemized fee once; net validates the bridge |
| Advertising | Ad export, marketplace deduction, invoice, card/bank payment | Select one expense record; use others as liability/payment records |
| Reserve | Hold transaction, reserve balance snapshot | Count movement once; use snapshot to validate ledger |
| Reserve release | Release transaction, higher payout | Record release once; payout is a transfer |
| Financing | Platform remittance, bank payment | Determine whether they are separate obligations or duplicate representations |
| Payout | Platform payout, bank deposit | Transfer pair; never two inflows |
| Reimbursement | Recovery event, adjustment credit | Link lifecycle and count one recovery |

---

# 25. Missing-Data Rules

Proceed with **Preliminary — Partial Reconciliation** only when available evidence supports reliable limited conclusions. List:

- Files reviewed
- Files missing
- Coverage periods
- Assumptions
- Exclusions
- Calculations completed
- Calculations withheld
- Unresolved items
- Confidence
- Required next documents

Issue a **Data Gap Report** and stop affected calculations when:

- Settlement or payout detail is missing.
- Matching bank activity is missing for bank reconciliation.
- Date ranges do not materially overlap.
- Currency cannot be determined.
- Duplicates materially distort totals.
- Core IDs, dates, or amounts are missing.
- More than 20% of absolute in-scope value is unclassified.
- SKU cost data is materially incomplete.
- Reserve movement cannot be reconstructed.
- A conclusion requires invented values.

Never estimate missing financial values merely to complete a report.

---

# 26. Materiality

Use a user-approved threshold. If absent, recommend:

```text
materiality_threshold = max(
    10 currency units,
    0.1% × absolute gross sales in scope
)
```

This is an operational default, not an accounting standard. A lower-value item may still require review when recurring, privacy-related, policy-sensitive, or evidence of control failure.

A reconciliation is `matched` only when unexplained variance is within approved materiality and no material unresolved classification remains.

---

# 27. Confidence Rules

Apply confidence to each material finding.

## High

- Required files and periods are complete or near-complete.
- At least 95% of absolute in-scope value is reconciled.
- No more than 1% of value is unclassified.
- IDs, currency, signs, and source totals are supported.
- No material contradiction remains.

## Medium

- Most required data is present.
- At least 80% of absolute in-scope value is reconciled.
- No more than 5% is unclassified.
- Limited assumptions or timing items remain.

## Low

Use Low when any applies:

- Less than 80% is reconciled.
- More than 5% is unclassified.
- Material mappings, cost data, periods, or identifiers are incomplete.
- Findings rely heavily on allocation or inference.

Low-confidence findings are directional only.

## Unable to Determine

Use when the minimum evidence needed for the specific conclusion is missing or contradictory.

A report may have Medium overall confidence while a specific payout match is High and a SKU-margin conclusion is Low.

---

# 28. Worked Fictional Example — Settlement to Bank

Fictional June activity for Northstar Outfitters, USD:

| Component | Amount |
|---|---:|
| Gross sales | 10,000.00 |
| Discounts | (300.00) |
| Shipping income | 400.00 |
| Tax collected | 650.00 |
| Refunds | (500.00) |
| Processing fees | (320.00) |
| Marketplace fees | (700.00) |
| Advertising deducted in settlement | (600.00) |
| Financing remittance | (450.00) |
| New reserve hold | (800.00) |
| Reserve release | 200.00 |
| Reimbursement | 75.00 |

```text
expected_settlement = 10,000 - 300 + 400 + 650 - 500 - 320 - 700
                    - 600 - 450 - 800 + 200 + 75
                    = 7,655
```

Platform-reported payout: $7,655.00  
Bank deposit two days later: $7,655.00

Results:

- Settlement variance: $0.00
- Bank amount variance: $0.00
- Payout-to-bank delay: 2 calendar days
- Financing remittance affects cash, not product contribution margin by default.
- Reserve hold reduces available cash by $800 but is not a permanent expense.
- Tax collected is excluded from product revenue and margin.

---

# 29. Worked Fictional Example — SKU Margin

Fictional SKU `NS-MUG-BLK`:

| Component | Amount |
|---|---:|
| Gross product sales | 6,000.00 |
| Discounts | (200.00) |
| Refunds | (300.00) |
| Shipping income allocated | 240.00 |
| COGS | (1,900.00) |
| Fulfillment | (750.00) |
| Shipping cost | (420.00) |
| Processing fees | (180.00) |
| Marketplace fees | (360.00) |
| Advertising allocated | (900.00) |
| Return cost | (110.00) |

```text
net_product_revenue = 6,000 - 200 - 300 = 5,500
```

```text
contribution_profit = 5,500 + 240 - 1,900 - 750 - 420
                    - 180 - 360 - 900 - 110
                    = 1,120
```

```text
contribution_margin_pct = 1,120 / 5,500 = 20.36%
```

Advisor-style finding:

- **Finding:** The SKU is profitable but has a thin-to-watch margin under the default directional bands.
- **Evidence:** $1,120 contribution profit on $5,500 net product revenue.
- **Impact:** Advertising and fulfillment consume 30% of net product revenue combined.
- **Confidence:** Medium if advertising allocation is modeled rather than directly attributed.
- **Priority:** Medium.
- **Next action:** Validate advertising allocation, refund causes, and fulfillment alternatives before changing price or spend.

---

# 30. Human-Review Triggers

Require human review for:

- Any material unmatched settlement, payout, or bank deposit
- Tax, duty, withholding, VAT/GST, nexus, or accounting treatment
- Financing principal and cost allocation
- Reserve converted to permanent loss
- Dispute eligibility, evidence, or submission
- Contract or rate interpretation
- Material unclassified or low-confidence mapping
- Multi-currency conflict or unsupported exchange rate
- Negative SKU margin based on allocated costs
- Funding use, eligibility, or repayment conclusions
- Any write action to a platform, accounting system, bank, CRM, support case, or external repository

---

# 31. Required Disclosure

> This operational analysis is based on the documents and authorized data provided. Platform exports, labels, fees, policies, and timing may change. Findings may help identify reconciliation gaps, cost pressure, or documentation needs, but they are not accounting, tax, legal, lending, underwriting, or reimbursement determinations. Material conclusions require human review, and outcomes are not guaranteed.
