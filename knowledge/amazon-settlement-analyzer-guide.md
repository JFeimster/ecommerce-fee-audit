---
title: "Amazon Settlement Analyzer Guide"
filename: "amazon-settlement-analyzer-guide.md"
version: "1.0.0"
status: "production-ready"
purpose: "Production guide for tracing Amazon settlement and financial-event activity through fees, reserves, reimbursements, advertising charges, and bank disbursements."
primary_users:
  - "AI Platform Fee Audit Copilot"
  - "Amazon sellers"
  - "FBA operators"
  - "ecommerce finance operations teams"
  - "human reviewers"
related_files:
  - "ai-platform-fee-audit-copilot-instructions.md"
  - "normalized-platform-fee-taxonomy.yaml"
  - "master-transaction-schema.json"
  - "column-mapping-library.json"
  - "reconciliation-and-calculation-rules.md"
  - "sku-contribution-margin-scorecard.csv"
  - "reserve-and-hold-tracker.csv"
  - "monthly-fee-variance-dashboard-schema.json"
last_updated: "2026-07-27"
---

# Amazon Settlement Analyzer Guide

## 1. Purpose and Authority

Use this guide to reconcile Amazon orders, financial events, settlement groups, reserves, fees, reimbursements, and disbursements to bank deposits. It supports operational analysis and does not replace Amazon policy, accounting, tax, legal, or lending judgment.

## 2. Required Reconciliation Chain

```text
order and inventory events
  -> Amazon financial events / settlement rows
  -> financial event group or settlement ID
  -> closed disbursement amount
  -> bank deposit
```

Reconcile each marketplace, seller account, settlement group, and currency separately before consolidation.

## 3. Source Priority and Version Control

Preferred evidence hierarchy:

1. Amazon settlement report or Finances API financial events tied to a financial event group
2. Seller Central transaction or payment detail
3. FBA reimbursement, returns, inventory ledger, storage-fee, and removal reports
4. Amazon Ads billing or transaction export
5. Matching bank activity
6. Merchant-provided cost and inventory records

Amazon announced that legacy XML and Flat File settlement reports are scheduled for removal on **November 11, 2026**, with `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` as the replacement. Record the exact report type and generation date. The V2 report uses fields such as `amount-type`, `amount-description`, and `amount`, and may format numbers using marketplace-local conventions.

Do not hardcode a report layout without validating the current headers.

## 4. Minimum Files

### Minimum viable settlement reconciliation

- Flat File V2 settlement report or complete financial events for the event group
- Settlement/financial event group ID and status
- Original total/disbursement amount and currency
- Matching bank statement or transaction export

### Full audit additions

- Order and shipment detail
- Returns report
- FBA reimbursement report
- Inventory ledger detail
- Storage and aged-inventory fee reports
- Removal/disposal detail
- Amazon Ads invoice or transaction detail
- SKU COGS and inbound/fulfillment costs

If a financial event group is not closed or the settlement report is incomplete, do not describe the disbursement as final.

## 5. Settlement Header and Control Totals

Capture when available:

- Settlement or financial event group ID
- Marketplace and seller account
- Start and end dates
- Deposit date or transfer date
- Processing status
- Beginning balance
- Original total/disbursement amount
- Currency
- Bank destination alias

For API-based reviews, use the closed financial event group and `OriginalTotal` as the disbursement control. For report-based reviews, tie all detail rows to the report's settlement control total.

## 6. Flat File V2 Parsing Rules

Validate:

- Delimiter and encoding
- Header names and report version
- `posted-date-time` timezone, which may be UTC
- Marketplace-local decimal and thousands separators
- `amount-type`
- `amount-description`
- `amount`
- `transaction-type`
- `quantity-purchased`
- Order, shipment, adjustment, and settlement IDs

One business event can occupy multiple rows. Group rows by stable order, shipment, adjustment, reimbursement, and settlement identifiers before calculating totals. Do not deduplicate legitimate component rows that share the same amount.

## 7. Core Classification Map

| Amazon event | Canonical code | Notes |
|---|---|---|
| Product sales | `REV_GROSS_SALES` | Include once at order-item grain |
| Promotions/discounts | `REV_DISCOUNT` | Separate merchant- and Amazon-funded credits where evidence supports it |
| Shipping credit | `REV_SHIPPING_INCOME` | Separate from carrier or FBA cost |
| Sales tax / VAT collected or withheld | `PASS_TAX` or `PASS_WITHHOLDING` | Human review required |
| Customer refund | `REV_REFUND` | Link to original order and item |
| Return event | `OPS_RETURN` | Operational event; not automatically equal to refund amount |
| Chargeback | `RISK_CHARGEBACK` | Track lifecycle and recovery separately |
| Referral fee | `FEE_REFERRAL` | Marketplace fee |
| FBA fulfillment fee | `FEE_FBA` | Per-unit fulfillment cost |
| Storage or aged-inventory fee | `FEE_STORAGE` | Period cost; allocate to SKU only with documented method |
| Other marketplace fee | `FEE_MARKETPLACE` | Preserve amount description |
| Advertising charge | `FEE_ADVERTISING` | Tie to Ads evidence and period |
| Reserve/withheld balance | `LIQ_RESERVE_HOLD` or `PASS_WITHHOLDING` | Use evidence; do not assume expense |
| Reserve release | `LIQ_RESERVE_RELEASE` | Not revenue |
| FBA reimbursement | `REC_REIMBURSEMENT` | Recovery; link to case/reimbursement and inventory event |
| Promotional or account credit | `REC_CREDIT` | Do not net against unrelated fees without evidence |
| Removal or disposal fee | `FEE_FBA` or `FEE_MARKETPLACE` | Preserve source subtype |
| Settlement transfer | `TRF_PAYOUT` | Not revenue |
| Bank deposit | `TRF_BANK_DEPOSIT` | Not revenue |
| Unknown settlement row | `UNCLASSIFIED` | Human review if material |

## 8. Orders and Revenue

- Use order-item or shipment-item grain when the report provides line-level amounts.
- Do not count the same sales amount from both order reports and settlement reports.
- Settlement rows prove cash movement; order reports support revenue and SKU analysis.
- Separate principal sales, shipping credits, gift wrap, tax, discounts, and reimbursements.
- Pending orders or unshipped authorizations are not settled revenue.

## 9. Referral Fees

Use the actual amount in the settlement row. A reasonableness test may compare:

```text
observed_referral_fee_rate = abs(referral_fees) / eligible_referral_fee_base
```

The eligible base and rate depend on category, marketplace, and current fee schedule. A deviation is an exception for investigation, not proof of overcharge.

## 10. FBA Fulfillment Fees

- Use actual settled FBA fees for historical audit.
- Use the FBA Fee Preview report only as an estimate or benchmark, not as proof of the historical fee.
- Tie fulfillment fees to SKU, ASIN, quantity, fulfillment channel, and shipment when possible.
- Flag quantity or size-tier discrepancies for human review.
- Do not mix inbound placement, removal, disposal, storage, and per-unit fulfillment fees under one generic cost when detail exists.

## 11. Storage and Aged-Inventory Fees

Storage charges may be period-level or ASIN-level. Record:

- Charge month
- ASIN/FNSKU/SKU
- Quantity and volume basis
- Storage rate
- Estimated versus settled status
- Currency

Allocation to SKU contribution margin must be documented. Preferred hierarchy:

1. Direct ASIN/SKU charge
2. Volume or cubic-foot basis
3. Average units on hand
4. Revenue or units sold only as a low-confidence fallback

## 12. Returns and Refund Administration

Separate:

- Customer refund principal
- Return event and disposition
- Refund administration or retained fee
- Restocking or recovery amount
- Inventory returned to sellable stock
- Inventory returned damaged/unsellable

A return does not automatically equal a cash refund, and a refund does not prove that inventory was physically returned. Use `OPS_RETURN` for the inventory/operating event and `REV_REFUND` for the financial refund.

## 13. Reimbursements

Use the FBA Reimbursements Report when available. Preserve:

- Reimbursement ID
- Case ID
- Approval date
- Original reimbursement ID/type
- Order ID
- SKU/FNSKU/ASIN
- Reason
- Cash and inventory quantities
- Amount per unit and total

Classify the recovery as `REC_REIMBURSEMENT`. Do not treat a reimbursement as new product revenue. Match any reversal or correction to the original reimbursement chain.

## 14. Advertising Charges

Amazon advertising charges can appear outside the settlement or as deductions within payment activity depending on account configuration and market. Reconcile Ads evidence separately, then link to settlement rows by date, invoice, account, amount, and description.

Avoid double counting when:

- The advertising export records spend
- An Amazon settlement also deducts that spend
- A bank or card statement records the payment

Choose one economic-cost record and treat settlement/card/bank movement as payment evidence.

## 15. Account-Level Reserves and Withheld Balances

Treat an account-level reserve as a liquidity restriction unless evidence shows a permanent charge.

Reserve roll-forward:

```text
opening_reserve
+ new_withholding
- released_amount
- applied_to_losses
+/- adjustments
= closing_reserve
```

Track the reserve in `reserve-and-hold-tracker.csv`. Do not infer a release date. If Amazon provides a statement-level beginning balance or reserve amount, preserve it separately from current-period operating activity.

## 16. Shipping Charges and Credits

Keep separate:

- Customer shipping credit: `REV_SHIPPING_INCOME`
- FBA or Amazon shipping/fulfillment fee: `FEE_FBA`
- Merchant-purchased carrier cost: `shipping_cost_amount`
- Shipping adjustment or reimbursement: `ADJ_MANUAL`, `REC_CREDIT`, or `REC_REIMBURSEMENT` based on evidence

Do not assume the customer shipping credit covers actual shipping cost.

## 17. Inventory Adjustments, Removals, and Disposal

Inventory movement needs quantity reconciliation in addition to cash reconciliation. Use inventory ledger and removal reports to track:

- Lost, found, damaged, returned, removed, disposed, or transferred units
- Reference ID
- Reconciled and unreconciled quantity
- Related fee
- Related reimbursement

A fee and an inventory write-off are separate economic components. Do not combine them unless the user has supplied the approved cost basis and accounting treatment.

## 18. Tax-Related Entries and Withholding

Tax, VAT, duties, and marketplace withholding rules vary by jurisdiction and transaction. Preserve Amazon labels and amounts. Use `PASS_TAX`, `PASS_DUTY`, or `PASS_WITHHOLDING` only when evidence supports the classification. Require qualified human review before accounting or tax use.

## 19. Multi-Marketplace and Multi-Currency Controls

- Reconcile each marketplace and currency independently.
- Preserve marketplace ID and local currency.
- Parse local decimal formats before normalization.
- Do not use a single exchange rate across a period unless explicitly approved.
- Separate explicit FX fees from exchange-rate effects.
- Never net a positive balance in one marketplace against a negative balance in another without evidence that Amazon did so in the same event group.

## 20. Settlement-to-Bank Matching

Match hierarchy:

1. Financial event group or settlement ID in bank metadata
2. Transfer reference
3. Exact amount and currency within expected date range
4. Descriptor and bank-account alias
5. Documented aggregation or split transfer

For API data, confirm the event group's `ProcessingStatus` is `Closed` before calling the disbursement final. Preserve pending/open groups as partial.

## 21. Duplicate Prevention

Do not deduplicate by amount alone. Use a fingerprint containing the most stable available fields:

```text
source_system + seller_account + marketplace + settlement_id
+ source_record_id + order_id + amount_type + amount_description
+ amount + currency + posted_timestamp
```

Legitimate rows can share order ID, amount, or description because one event may contain principal, fee, tax, and promotion components.

## 22. Common Data Gaps

- Missing settlement control total
- Report truncated or not fully paginated
- Legacy and V2 reports mixed
- Local numeric format misread
- Missing marketplace ID or currency
- Advertising cost recorded without invoice/payment evidence
- Reimbursement report missing
- Return status missing
- Storage fee is estimated, not settled
- Reserve beginning balance missing
- Bank deposit is aggregated with other platforms

If more than 20% of transaction value remains unclassified, stop definitive conclusions and issue a Data Gap Report.

## 23. Fictional Worked Example

**Seller:** Atlas Home Test Seller  
**Marketplace:** US  
**Settlement:** `SET-FIC-0626-01`  
**Currency:** USD

| Component | Amount |
|---|---:|
| Product and shipping revenue | 48,500.00 |
| Promotions and refunds | (4,250.00) |
| Referral fees | (7,050.00) |
| FBA fulfillment fees | (8,200.00) |
| Storage and removal fees | (1,150.00) |
| Advertising deduction | (3,400.00) |
| Reimbursement | 620.00 |
| Account-level reserve withheld | (2,000.00) |
| Other supported adjustments | (70.00) |
| Expected disbursement | 23,000.00 |
| Closed event-group original total | 23,000.00 |
| Bank deposit two days later | 23,000.00 |

The settlement and bank deposit match. The 2,000.00 reserve is reported as restricted cash, not fee expense. The 620.00 reimbursement is a recovery linked to its case, not revenue. SKU margin remains preliminary until COGS and advertising allocation are complete.

## 24. Escalation Conditions

Require human review for:

- Settlement or bank variance above materiality
- Open event group presented as final
- Material reserve without beginning balance or release terms
- Reimbursement without case or inventory linkage
- Tax/VAT/duty classification
- Material local-number-format ambiguity
- Duplicate or missing settlement rows
- Advertising cost that appears in both Ads and settlement data
- Inventory loss with no cost basis or reimbursement evidence
- Proposed Amazon support dispute or reimbursement claim

## 25. Required Output

1. Scope and report versions
2. Settlement roll-forward
3. Settlement-to-bank match table
4. Fee table by category and SKU where supported
5. Refund/return table
6. Reserve and withholding table
7. Reimbursement table
8. Advertising reconciliation
9. Inventory adjustment and removal exceptions
10. Data gaps and confidence labels
11. Prioritized next actions
12. Machine-readable output compatible with `output-schema.json`

## Official Source References

Verified on `2026-07-27`. Platform fields, fees, eligibility, timing, and policies can change; validate the live account and current documentation before relying on a material conclusion.

- [Flat File V2 settlement report migration notice](https://developer-docs.amazon.com/sp-api/changelog/update-removal-of-xml-settlement-report-and-flat-file-settlement-report-date-changed-to-november-11-2026)
- [Retrieve financial events in a financial event group](https://developer-docs.amazon.com/sp-api/docs/retrieve-financial-events-in-group)
- [Retrieve amount and status of a payment](https://developer-docs.amazon.com/sp-api/docs/retrieve-amount-status-payment)
- [FBA reports and report fields](https://developer-docs.amazon.com/sp-api/lang-en_EN/docs/report-type-values-fba)
