---
title: "Shopify Payout Reconciliation Guide"
filename: "shopify-payout-reconciliation-guide.md"
version: "1.0.0"
status: "production-ready"
purpose: "Production guide for tracing Shopify orders and Shopify Payments balance activity through payouts, reserves, financing deductions, and bank deposits."
primary_users:
  - "AI Platform Fee Audit Copilot"
  - "Shopify operators"
  - "ecommerce finance operations teams"
  - "human reviewers"
related_files:
  - "ai-platform-fee-audit-copilot-instructions.md"
  - "normalized-platform-fee-taxonomy.yaml"
  - "master-transaction-schema.json"
  - "column-mapping-library.json"
  - "reconciliation-and-calculation-rules.md"
  - "reserve-and-hold-tracker.csv"
  - "monthly-fee-variance-dashboard-schema.json"
last_updated: "2026-07-27"
---

# Shopify Payout Reconciliation Guide

## 1. Purpose and Authority

Use this guide to explain how Shopify order activity becomes Shopify Payments balance activity, a payout, and a bank deposit. It is an operational reconciliation guide, not an accounting, tax, legal, lending, or platform-policy determination. The merchant's live Shopify admin, account notices, contract terms, and current Shopify documentation control when they differ from this guide.

## 2. Reconciliation Objective

The primary objective is to prove, by payout currency and account, that:

```text
starting_shopify_payments_balance
+ balance_change_from_activity
- total_payouts
= ending_shopify_payments_balance
```

Then prove each payout against the bank:

```text
shopify_payout_amount - bank_deposit_amount = payout_to_bank_variance
```

A payout and its matched bank deposit are transfers, not revenue. Use `TRF_PAYOUT` and `TRF_BANK_DEPOSIT`, and eliminate the matched pair from consolidated revenue or contribution-margin views.

## 3. Minimum Files

### Minimum viable payout reconciliation

1. Shopify Payments payout reconciliation report or payout transaction export
2. Specific payout detail, including payout ID, date, currency, status, total, and transfer reference when available
3. Matching bank activity
4. Order or transaction detail for exceptions

### Add for a full fee and margin audit

- Shopify order export with line items
- Refund and dispute detail
- Shopify bill export for third-party transaction fees, subscriptions, apps, and shipping labels not included in Shopify Payments activity
- COGS, fulfillment, carrier, advertising, and other variable-cost files
- Reserve notices and reserve transaction export
- Shopify Capital or Shopify Credit transaction history when applicable

If settlement or payout detail and matching bank evidence are unavailable, produce a **Data Gap Report**. If the core payout chain is available but some cost files are missing, continue as **Preliminary — Partial Reconciliation** and limit the conclusions.

## 4. Shopify Order-to-Payout Flow

```text
Order and payment capture
  -> Shopify Payments balance activity
  -> pending/available payout balance
  -> reserves, holds, refunds, disputes, fees, and adjustments
  -> scheduled payout
  -> bank processing
  -> posted bank deposit
```

Do not assume an order date, capture date, balance-activity date, payout date, and bank-posted date are the same. Preserve each date in the normalized schema.

## 5. Payout Reconciliation Report

The Shopify Payments payout reconciliation report is a balance-movement report, not a revenue statement. At minimum capture:

| Shopify concept | Normalized treatment |
|---|---|
| Starting balance | Opening processor-clearing balance; not current-period revenue |
| Account activity before fees | Source subtotal before Shopify Payments fees |
| Fees | Negative economic value; classify at the most specific supported fee code |
| Net amount | Activity after fees, before payout transfers |
| Total payouts | `TRF_PAYOUT`; transfer out of processor balance |
| Ending balance | Closing processor-clearing balance |

Activity groups may include payments, refunds, disputes, adjustments, reserves and holds, shipping, promotions and credits, payouts, or other activity. Preserve the source group, source label, IDs, and original amount before mapping.

## 6. Required Field Mapping

Use `column-mapping-library.json`, then normalize to `master-transaction-schema.json`.

Recommended fields:

- `source_record_id`
- `source_transaction_type`
- `source_description`
- `transaction_at`
- `available_on`
- `settlement_date`
- `payout_id`
- `payout_trace_id`
- `order_id`
- `transaction_currency`
- `settlement_currency`
- `source_amount`
- `gross_amount`
- `fee_amount`
- `refund_amount`
- `chargeback_amount`
- `reserve_hold_amount`
- `reserve_release_amount`
- `financing_remittance_amount`
- `net_amount`
- `normalized_classification`
- `duplicate_fingerprint`
- `reconciliation_status`

## 7. Transaction Classification Rules

| Shopify activity | Canonical code | Treatment |
|---|---|---|
| Captured merchandise sale | `REV_GROSS_SALES` | Revenue evidence; include once at the approved grain |
| Merchant-funded discount | `REV_DISCOUNT` | Contra-revenue |
| Tax collected | `PASS_TAX` | Pass-through pending human review |
| Shipping charged to customer | `REV_SHIPPING_INCOME` | Revenue component, separate from shipping cost |
| Tip | `REV_TIPS` | Revenue component, not merchandise sales |
| Refund | `REV_REFUND` | Contra-revenue; preserve original order and refund IDs |
| Dispute lifecycle event | `RISK_DISPUTE` | Open risk event; not automatically a final loss |
| Chargeback debit | `RISK_CHARGEBACK` | Cash and margin reduction subject to lifecycle outcome |
| Shopify Payments processing fee | `FEE_PROCESSING` | Variable platform fee |
| Third-party transaction fee | `FEE_MARKETPLACE` | Shopify billing fee; reconcile separately from processor fee |
| Shipping label charge | `FEE_SHIPPING_LABEL` | Variable shipping cost |
| Currency conversion fee | `FEE_FX` | Currency cost; separate from exchange-rate effect |
| Reserve withheld | `LIQ_RESERVE_HOLD` | Liquidity restriction, not permanent expense |
| Reserve released | `LIQ_RESERVE_RELEASE` | Release of previously restricted cash, not revenue |
| Account payout hold | `LIQ_HOLD` | Timing restriction unless evidence supports a permanent deduction |
| Capital/Credit repayment | `FIN_REMITTANCE` | Financing cash outflow; do not classify as platform fee |
| Manual adjustment | `ADJ_MANUAL` | Preserve source description; human review if material |
| Payout | `TRF_PAYOUT` | Transfer from Shopify Payments balance |
| Bank deposit | `TRF_BANK_DEPOSIT` | Transfer into bank cash |

## 8. Processing and Third-Party Transaction Fees

### Shopify Payments processing fees

- Use the actual fee shown in the payout transaction or reconciliation report.
- Do not reconstruct a fee from a public rate when the source fee is available.
- When reconstructing for a reasonableness test, use the merchant's plan, country, payment method, currency, and contract terms as of the transaction date.
- Treat any difference between expected and actual fees as an exception, not automatically as leakage.

### Third-party transaction fees

These may appear on Shopify bills rather than Shopify Payments payouts. They are distinct from the payment processor's fee and can create a double-fee stack. Reconcile them by billing period and order base, not by forcing them into a Shopify Payments payout.

Control:

```text
third_party_fee_base = product_amount_after_discounts + applicable_tax + shipping
expected_third_party_fee = third_party_fee_base × merchant_plan_rate
```

Use this only when the merchant's current plan and applicable fee rules are verified. Refund treatment and exclusions can vary; the live Shopify bill is authoritative.

## 9. Refunds

- Link each refund to the original order, payment, and refund ID.
- Record the refund amount separately from any retained processing fee.
- Do not assume the original processing fee is returned.
- If a refund reduces a later payout, preserve the timing difference between the refund date and payout date.
- If the payout balance is insufficient, classify any resulting negative balance or bank debit separately; do not duplicate the refund.
- Use Acquirer Reference Numbers only as supporting trace evidence, not as a financial amount.

## 10. Disputes and Chargebacks

Track lifecycle records separately:

1. Inquiry or dispute opened
2. Disputed amount debited
3. Dispute fee debited
4. Evidence deadline and response status
5. Won, lost, withdrawn, or unresolved outcome
6. Principal and fee recovery, if any

Never book an open dispute as both a refund and a chargeback. Use `RISK_DISPUTE` for the event and `RISK_CHARGEBACK` for the economic debit. A winning outcome requires a separate recovery record or matched reversal.

## 11. Shipping Labels

- Separate customer shipping income (`REV_SHIPPING_INCOME`) from Shopify label costs (`FEE_SHIPPING_LABEL`).
- Link label costs to orders or fulfillment IDs when possible.
- Treat label refunds or carrier adjustments as separate credits or adjustments.
- Do not infer carrier cost from customer shipping income.

## 12. Taxes, Duties, and Tips

- Preserve tax and duty amounts as pass-through categories until a qualified human confirms treatment.
- Do not include taxes or duties in merchandise revenue or contribution margin unless the approved business model explicitly treats them as revenue.
- Keep tips separate from merchandise revenue and verify whether the merchant bears related processing fees.

## 13. Currency Conversion and Multi-Currency Payouts

Reconcile each payout currency separately.

Record:

- Customer presentment currency
- Store currency
- Shopify Payments settlement/payout currency
- Bank currency
- Source exchange rate when supplied
- Explicit conversion fee

Do not combine native-currency amounts before conversion. Separate:

1. Economic transaction amount
2. Exchange-rate effect
3. Explicit FX fee
4. Timing difference

## 14. Reserves

Shopify Payments reserves can be fixed or percentage-based. Negative reserve transactions place funds into reserve; positive reserve transactions make funds available after release. Reserve adjustments or early releases may not map cleanly to orders.

Maintain a reserve ledger:

```text
opening_reserve_balance
+ reserve_holds
- reserve_releases
- reserve_applications_to_losses
+/- reserve_adjustments
= closing_reserve_balance
```

Controls:

- Reserve holds reduce available cash, not contribution profit.
- Reserve releases increase available cash, not revenue.
- If a reserve is applied to a refund or dispute, classify the underlying loss once and reduce the reserve balance separately.
- Use `reserve-and-hold-tracker.csv` for expected release dates, aging, evidence, and cash impact.

## 15. Account Holds

A payout hold is not the same as a reserve. A hold can stop all payouts during review while the store may continue accepting orders. Track:

- Hold start date
- Notice date and source
- Reason stated by Shopify
- Requested documents
- Submission date
- Expected and actual resolution
- Cash blocked
- Aging days

Do not invent a release date. Use `unable_to_determine` when no reliable date is provided.

## 16. Shopify Capital and Financing Remittances

Financing deductions must remain separate from operating fees and SKU economics unless the user explicitly requests a financing allocation.

For each remittance record:

- Preserve agreement/program name
- Record loan/advance ID when available
- Record daily sales base and remittance percentage when supplied
- Split principal and financing cost only when supported by the agreement or lender statement
- Classify the cash deduction as `FIN_REMITTANCE`
- Do not label principal repayment as an operating expense

**Version-sensitive U.S. rule:** Shopify states that repayments for certain U.S. Shopify Capital loans accepted on or after March 9, 2026 are collected from the Shopify Payments balance and appear in payout Adjustments; older loans may continue through bank debits. Verify the merchant's jurisdiction, acceptance date, and agreement. Do not generalize this rule to other regions or products.

## 17. Payout-to-Bank Matching

Match in this order:

1. Exact transfer reference or trace ID
2. Exact payout ID carried into bank metadata
3. Exact currency and amount within the expected date window
4. Amount plus bank descriptor and account alias
5. Aggregated or split deposit match with documented component IDs

Use these statuses:

- `matched`
- `matched_with_timing_difference`
- `partial`
- `unmatched`
- `data_gap`
- `human_review_required`

Do not force-match two payouts merely because their amounts are equal.

## 18. Common Reconciliation Errors

| Error | Control |
|---|---|
| Treating payouts as sales | Exclude `TRF_PAYOUT` from revenue |
| Counting order total on every line item | Use order/line grain and repeated-total controls |
| Combining Shopify Payments and third-party processor payouts | Reconcile each processor separately |
| Ignoring Shopify bills | Audit transaction fees, app charges, and subscriptions outside payouts |
| Treating reserves as fees | Use liquidity-restriction codes |
| Treating reserve releases as revenue | Link release to reserve ledger |
| Counting refund and chargeback for the same event | Review lifecycle and related IDs |
| Allocating financing principal to SKU margin by default | Keep financing below operating contribution unless explicitly requested |
| Matching on amount alone | Require date, currency, account, and identifier evidence |
| Mixing payout and order periods | Use separate transaction, availability, payout, and bank dates |

## 19. Partial-Payout Scenarios

### Split payout

One Shopify payout can appear as multiple bank credits because of banking or routing behavior. Require the sum of deposits, consistent currency, account, and date window.

### Aggregated bank deposit

A bank may combine multiple processor transfers. Match only when the component payouts are evidenced and sum to the deposit.

### Negative or reduced payout

Investigate refunds, disputes, processing fees, reserves, financing repayments, adjustments, and prior negative balance. Do not treat the gap as fee leakage until classified.

### Failed payout

Track the failed payout and any retry as related lifecycle records, not duplicate transfers. The final successful deposit should link to the original payout or retry chain.

## 20. Troubleshooting Workflow

1. Confirm account, payout currency, audit period, and analysis timezone.
2. Reconcile report starting balance to the prior ending balance.
3. Tie source activity to report activity groups.
4. Isolate unknown adjustments and retained fees.
5. Build the reserve and hold ledger.
6. Confirm financing deductions outside operating fees.
7. Tie total payouts to payout-detail records.
8. Match each payout to bank activity.
9. Run duplicate checks before aggregation.
10. Produce an exception table ranked by amount, confidence, and urgency.

## 21. Fictional Worked Example

**Store:** Northstar Gear Test Store  
**Currency:** USD  
**Period:** 2026-06-01 through 2026-06-07

| Component | Amount |
|---|---:|
| Starting Shopify Payments balance | 500.00 |
| Gross payment activity | 12,000.00 |
| Refunds | (600.00) |
| Processing fees | (390.00) |
| Reserve holds | (1,200.00) |
| Capital remittance | (480.00) |
| Net balance change from activity | 9,330.00 |
| Payouts initiated | (8,900.00) |
| Expected ending balance | 930.00 |
| Reported ending balance | 930.00 |

The payout of 8,900.00 posts to the bank two days later. Classification:

- Gross payments: `REV_GROSS_SALES`
- Refunds: `REV_REFUND`
- Processing fees: `FEE_PROCESSING`
- Reserve holds: `LIQ_RESERVE_HOLD`
- Capital remittance: `FIN_REMITTANCE`
- Payout: `TRF_PAYOUT`
- Bank credit: `TRF_BANK_DEPOSIT`

Conclusion: the payout chain reconciles. The 1,200.00 reserve is a cash-timing restriction, not a permanent fee. The 480.00 financing deduction affects cash available but is not included in operating contribution margin unless the user requests a financing-burden view.

## 22. Human-Review Triggers

Require human review for:

- Material unmatched payout or deposit
- Material unclassified adjustment
- Reserve balance that does not roll forward
- Suspected duplicate fee or bank debit
- Dispute, tax, or duty classification
- Shopify Capital principal/cost split
- Multi-currency mismatch without source exchange-rate evidence
- A proposed platform dispute or support escalation
- Any conclusion used for accounting entries, tax reporting, lending, or underwriting

## 23. Required Output

Every Shopify report must include:

1. Scope and files reviewed
2. Coverage and data gaps
3. Balance roll-forward
4. Payout-to-bank match table
5. Fee and adjustment table
6. Refund and dispute table
7. Reserve/hold ledger
8. Financing-deduction table
9. Exceptions ranked by priority
10. Confidence labels
11. Next actions and human-review items
12. Machine-readable fields compatible with `output-schema.json`

## Official Source References

Verified on `2026-07-27`. Platform fields, fees, eligibility, timing, and policies can change; validate the live account and current documentation before relying on a material conclusion.

- [Shopify Payments payout reconciliation report](https://help.shopify.com/en/manual/payments/shopify-payments/payouts/payout-reconciliation-report)
- [Viewing and exporting payout details](https://help.shopify.com/en/manual/payments/shopify-payments/getting-paid-with-shopify-payments/view-payouts/view-details)
- [Payout timing](https://help.shopify.com/en/manual/payments/shopify-payments/payouts/payout-timing)
- [Lower or missing payouts](https://help.shopify.com/en/manual/payments/shopify-payments/payouts/lower-or-missing-payouts)
- [Shopify Payments refunds](https://help.shopify.com/en/manual/payments/shopify-payments/payouts/refunds)
- [Reserves in Shopify Payments](https://help.shopify.com/en/manual/payments/shopify-payments/payouts/reserves)
- [Shopify Payments account holds](https://help.shopify.com/en/manual/payments/shopify-payments/payouts/account-holds)
- [Third-party transaction fees](https://help.shopify.com/en/manual/your-account/manage-billing/billing-charges/types-of-charges/third-party-charges/third-party-transaction-fees)
- [Shopify Capital loans and repayment — United States](https://help.shopify.com/en/manual/finance/shopify-capital/united-states)
