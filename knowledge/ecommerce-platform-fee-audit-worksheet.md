---
title: "Ecommerce Platform Fee Audit Worksheet"
filename: "ecommerce-platform-fee-audit-worksheet.md"
version: "1.0.0"
status: "production-ready"
purpose: "Complete operator workbook for platform-fee audits, reconciliation, SKU margin, reserves, cash timing, and funding readiness."
primary_users:
  - "ecommerce operators"
  - "small-business owners"
  - "finance operations teams"
  - "fractional finance advisors"
related_files:
  - "ai-platform-fee-audit-copilot-instructions.md"
  - "normalized-platform-fee-taxonomy.yaml"
  - "master-transaction-schema.json"
  - "column-mapping-library.json"
  - "reconciliation-and-calculation-rules.md"
  - "sku-contribution-margin-scorecard.csv"
  - "reserve-and-hold-tracker.csv"
last_updated: "2026-07-27"
---

# Ecommerce Platform Fee Audit Worksheet

**Shopify, Amazon, Stripe, and Marketplace Margin Audit Kit**

Prepared for Moonshine Capital

---

## Purpose

This workbook helps ecommerce operators reconcile gross sales, platform deductions, payouts, reserves, refunds, advertising, fulfillment, and bank deposits so they can see what each channel and SKU actually contributes to cash flow.

Use it for:

- Monthly platform-fee audits
- Shopify payout reconciliation
- Amazon settlement analysis
- Stripe fee analysis
- SKU contribution-margin reviews
- Reserve and hold tracking
- Fee-dispute documentation
- Working-capital decisions
- Funding-readiness preparation

> This worksheet supports operational review. It does not replace bookkeeping, accounting, tax, legal, platform-support, lending, or underwriting advice.

---


# Operator Control Sections

## Audit Setup

Complete this section before calculations.

| Field | Required | Entry / definition |
|---|---:|---|
| Audit ID | Yes | Stable identifier, e.g. `AUD-2026-007` |
| Business alias | Yes | Redacted business name if needed |
| Primary objective | Yes | Reconcile payouts, find fee leakage, assess SKU margin, investigate reserves, diagnose cash timing, or prepare funding-readiness summary |
| Period start / end | Yes | Inclusive ISO 8601 dates |
| Analysis timezone | Yes | IANA timezone, e.g. `America/New_York` |
| Currencies | Yes | ISO 4217 codes; reconcile each currency separately |
| Platforms and accounts | Yes | Store, seller, processor, ad, and bank account aliases |
| Materiality threshold | Yes | User-approved threshold and rationale |
| Prepared by / review due | Yes / No | Operator role and human-review deadline |

Recommended materiality when the user has not supplied one:

```text
materiality_threshold = max(10 currency units, 0.1% × absolute gross sales in scope)
```

This is an operational default, not an accounting standard.

## Business and Platform Profile

| Field | Description |
|---|---|
| Platform | Canonical platform name |
| Account alias | Redacted store, seller, processor, advertising, or bank label |
| Account role | Order source, settlement source, payout source, advertising source, cost source, or bank destination |
| Payout schedule | Daily, weekly, scheduled, manual, or unknown |
| Settlement currency | Currency of the platform balance and payout |
| Bank currency | Currency in which deposits post |
| Reserve program | None, rolling, fixed, risk reserve, minimum balance, or unknown |
| Financing program | None or user-provided program name |
| Known changes | Plan, fee, bank, payout schedule, currency, or policy changes during the audit period |

## File Inventory and Coverage Tracker

| File ID | Source system | Export type | Original filename | Period start | Period end | Timezone | Currency | Row count | Control total | Coverage status | Data-quality note |
|---|---|---|---|---|---|---|---|---:|---:|---|---|
| F-001 | Shopify Payments | Payout transactions | `shopify_payout_demo.csv` | 2026-06-01 | 2026-06-30 | -04:00 | USD | 482 | 98425.31 | Complete | Fictional example |
| F-002 | Bank | Posted transactions | `bank_demo_redacted.csv` | 2026-06-01 | 2026-06-30 | America/New_York | USD | 214 | null | Partial | Memo text truncated |

Use coverage status: `complete`, `partial`, `non_overlapping`, `unknown`, or `unusable`.

Control questions:

- Does the export total match the platform UI or statement total for the same basis and period?
- Is the report based on transaction, settlement, payout, available, or posting date?
- Are opening and closing balances required?
- Are amounts signed, unsigned magnitudes, or split into debit and credit columns?
- Are overlapping downloads present?
- Are multiple currencies mixed in one file?

## Evidence and Confidence Labels

Every material conclusion must be labeled as one of:

- **Verified Fact**
- **User-Provided Data**
- **Assumption**
- **Calculation**
- **Inference**
- **Recommendation**

Use confidence: **High**, **Medium**, **Low**, or **Unable to Determine**.

## Data-Gap Checklist

Switch to a **Data Gap Report** and stop affected calculations when any applicable condition is true:

- [ ] Settlement or payout detail is missing.
- [ ] Matching bank activity is missing for bank reconciliation.
- [ ] Order or transaction detail is missing.
- [ ] Date ranges do not materially overlap.
- [ ] Currency cannot be determined.
- [ ] Timezone is unknown and timing is material.
- [ ] Duplicates materially distort totals.
- [ ] Core IDs, dates, or amounts are missing.
- [ ] More than 20% of absolute in-scope value is unclassified.
- [ ] SKU cost data is materially incomplete.
- [ ] Reserve opening balance or movement data is missing.
- [ ] Financing principal and financing cost require a split that evidence does not support.
- [ ] Contradictory source totals remain unresolved.

| Gap ID | Missing item | Affected calculation | Risk | Minimum next document | Owner | Due date | Status |
|---|---|---|---|---|---|---|---|

## Exception Log

| Exception ID | Date found | Platform | Record IDs | Category | Description | Amount at risk | Currency | Evidence | Confidence | Priority | Owner | Next action | Due date | Status | Resolution |
|---|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|

Priority definitions:

- **Critical:** active cash loss, privacy/security issue, missing payout, or material control failure requiring immediate action.
- **High:** material unreconciled amount, repeated unsupported fee, aging reserve, or significant negative-margin exposure.
- **Medium:** nonmaterial variance, mapping ambiguity, or correctable documentation gap.
- **Low:** monitoring or descriptive issue with little financial impact.

## Funding-Readiness Worksheet

This section summarizes evidence and cash timing. It does not make a credit decision or guarantee eligibility.

| Area | Evidence or metric | Status | Risk or limitation | Required next action |
|---|---|---|---|---|
| Revenue consistency | Monthly net revenue and source coverage | | | |
| Payout reconciliation | Matched percentage and unmatched amount | | | |
| Fee burden | Effective fee rate and trend | | | |
| SKU economics | Margin bands and data confidence | | | |
| Reserve exposure | Balance, aging, and expected releases | | | |
| Cash timing | Payout delay and projected cash gap | | | |
| Existing obligations | User-provided financing deductions and liabilities | | | |
| Documentation readiness | Statements, exports, invoices, COGS, and IDs | | | |
| Unresolved discrepancies | Material exceptions and data gaps | | | |

Use compliance-safe language such as “may help,” “can support,” “eligibility varies,” “terms may change,” and “not a guarantee.”

## Final Sign-Off

| Field | Entry |
|---|---|
| Audit ID | |
| Report status | Complete / Preliminary — Partial Reconciliation / Data Gap Report |
| Overall confidence | High / Medium / Low / Unable to Determine |
| Total in-scope value | |
| Reconciled value | |
| Unmatched value | |
| Unclassified value | |
| Material exceptions | |
| Calculations withheld | |
| Human-review items | |
| Prepared by | |
| Reviewed by | |
| Review date | |
| Approval status | Unreviewed / Approved / Approved with exceptions / Rejected |
| Reviewer notes | |

> Sign-off confirms operational review only. It does not certify accounting accuracy, tax treatment, platform-policy eligibility, funding approval, or reimbursement.

---

# Workbook Setup

Create one spreadsheet with these tabs:

1. `00 Instructions`
2. `01 Master Fee Audit`
3. `02 Shopify Reconciliation`
4. `03 Amazon Settlement Analyzer`
5. `04 Stripe Fee Calculator`
6. `05 SKU Margin Scorecard`
7. `06 Reserve and Hold Tracker`
8. `07 Monthly Fee Dashboard`
9. `08 Working Capital Decision`
10. `09 Dispute Log`

Recommended status colors:

- Green: reconciled or healthy
- Yellow: needs review
- Red: material issue
- Blue: reserve, hold, or timing difference
- Gray: manual input
- White: formula

Every deduction should be classified as one of the following:

1. Permanent operating expense
2. Refund or return
3. Temporary reserve or hold
4. Tax or duty
5. Financing remittance
6. Timing difference
7. Unresolved adjustment

Do not leave a material deduction classified as “Other” for more than one monthly close.

---

# 1. Platform-Fee Audit Spreadsheet

## Tab Name

`01 Master Fee Audit`

## Required Columns

| Column | Description |
|---|---|
| Transaction Date | Original transaction date |
| Settlement Date | Date included in settlement |
| Payout Date | Date platform initiated payout |
| Bank Deposit Date | Date cash posted |
| Platform | Shopify, Amazon, Stripe, Etsy, eBay, Walmart, etc. |
| Store / Account | Storefront or merchant account |
| Payout ID | Payout or settlement reference |
| Order ID | Customer order ID |
| Transaction ID | Platform transaction reference |
| SKU | Product SKU |
| Product Name | Product or offer |
| Quantity | Units sold |
| Customer Country | Country |
| Currency | Transaction currency |
| Gross Item Sales | Revenue before discounts |
| Discounts | Discounts and promotions |
| Shipping Collected | Shipping paid by customer |
| Sales Tax Collected | Sales tax collected |
| Duties Collected | Duties collected |
| Refund Amount | Refunded merchandise or shipping |
| Chargeback Amount | Disputed amount |
| Net Merchandise Revenue | Formula |
| Payment Processing Fee | Card, wallet, ACH, or processor fee |
| Marketplace Referral Fee | Marketplace commission |
| Fulfillment Fee | Pick, pack, and fulfill |
| Storage Fee | Monthly or aged-inventory storage |
| Shipping Label Cost | Platform-purchased shipping |
| Return Processing Fee | Return-related charge |
| Dispute Fee | Chargeback-related fee |
| Currency Conversion Fee | International or FX charge |
| Advertising Cost | Attributable ad spend |
| App / Software Cost | Allocated software cost |
| Reserve Hold | New amount withheld |
| Reserve Release | Previously held amount released |
| Financing Remittance | Capital advance or revenue-based remittance |
| Other Adjustment | Unclassified adjustment |
| Other Adjustment Description | Original description |
| Cost of Goods Sold | Product cost |
| Inbound Freight | Allocated freight |
| Packaging Cost | Packaging and inserts |
| Expected Platform Payout | Formula |
| Actual Platform Payout | Platform-reported payout |
| Bank Deposit Amount | Bank-posted deposit |
| Payout Variance | Formula |
| Contribution Profit | Formula |
| Contribution Margin % | Formula |
| Effective Platform Fee % | Formula |
| Review Status | Reconciled, review, disputed, timing, missing data |
| Reviewer Notes | Explanation or action |

## Core Formulas

### Net Merchandise Revenue

```excel
=Gross_Item_Sales-Discounts-Refund_Amount
```

### Total Platform and Payment Fees

```excel
=Payment_Processing_Fee
+Marketplace_Referral_Fee
+Fulfillment_Fee
+Storage_Fee
+Shipping_Label_Cost
+Return_Processing_Fee
+Dispute_Fee
+Currency_Conversion_Fee
+Other_Adjustment
```

### Expected Platform Payout

```excel
=Gross_Item_Sales
-Discounts
+Shipping_Collected
+Sales_Tax_Collected
+Duties_Collected
-Refund_Amount
-Chargeback_Amount
-Payment_Processing_Fee
-Marketplace_Referral_Fee
-Fulfillment_Fee
-Storage_Fee
-Shipping_Label_Cost
-Return_Processing_Fee
-Dispute_Fee
-Currency_Conversion_Fee
-Advertising_Cost_Deducted_From_Settlement
-Financing_Remittance
-Reserve_Hold
+Reserve_Release
-Other_Adjustment
```

### Payout Variance

```excel
=Expected_Platform_Payout-Bank_Deposit_Amount
```

### Contribution Profit

```excel
=Net_Merchandise_Revenue
+Shipping_Collected
-Cost_of_Goods_Sold
-Inbound_Freight
-Packaging_Cost
-Payment_Processing_Fee
-Marketplace_Referral_Fee
-Fulfillment_Fee
-Storage_Fee
-Shipping_Label_Cost
-Return_Processing_Fee
-Dispute_Fee
-Currency_Conversion_Fee
-Advertising_Cost
-App_Software_Cost
```

Do not subtract reserve holds from contribution profit. A reserve affects available cash, not necessarily permanent margin.

### Contribution Margin Percentage

```excel
=IFERROR(Contribution_Profit/Net_Merchandise_Revenue,0)
```

### Effective Platform Fee Percentage

```excel
=IFERROR(Total_Platform_And_Payment_Fees/Net_Merchandise_Revenue,0)
```

## Monthly Summary Metrics

Create a pivot table by platform and month showing:

- Gross sales
- Net merchandise revenue
- Total permanent fees
- Refunds
- Advertising
- Contribution profit
- Contribution margin
- Reserve holds
- Reserve releases
- Net cash deposited
- Unexplained variance
- Effective platform fee rate

---

# 2. Shopify Payout Reconciliation Tab

## Tab Name

`02 Shopify Reconciliation`

## Recommended Data Sources

Collect:

- Shopify orders export
- Shopify Payments payout report
- Transaction report
- Refund report
- Dispute report
- Shipping-label charges
- Financing remittances
- Reserve or hold activity
- Matching bank deposits
- Third-party processor reports, when applicable

## Reconciliation Fields

| Field | Description |
|---|---|
| Payout ID | Shopify payout reference |
| Payout Status | Paid, pending, failed, canceled, in transit |
| Payout Initiated Date | Date Shopify initiated transfer |
| Expected Bank Date | Estimated arrival |
| Actual Bank Date | Date posted |
| Gross Charges | Customer charges |
| Refunds | Refund deductions |
| Disputes | Chargeback activity |
| Processing Fees | Shopify Payments processing |
| Third-Party Transaction Fees | Shopify fee when outside processor is used |
| Shipping Charges | Label or shipping deductions |
| Duties / Taxes | Collected or adjusted |
| Financing Remittance | Shopify Capital or similar |
| New Reserve Hold | Newly withheld amount |
| Reserve Release | Previously held amount released |
| Other Adjustments | Miscellaneous |
| Expected Net Payout | Formula |
| Shopify Reported Payout | Input |
| Bank Deposit | Input |
| Variance | Formula |
| Resolution | Reconciled, timing, missing, dispute, inquiry |

## Shopify Reconciliation Formula

```excel
=Gross_Charges
-Refunds
-Disputes
-Processing_Fees
-Third_Party_Transaction_Fees
-Shipping_Charges
-Financing_Remittance
-New_Reserve_Hold
+Reserve_Release
-Other_Adjustments
```

## Shopify Audit Questions

- Are Shopify Payments fees separated from Shopify plan charges?
- Is an outside payment processor charging separate fees?
- Are Shopify third-party transaction fees also being charged?
- Are refunds reducing revenue while original processing costs remain?
- Are shipping-label charges included in the payout?
- Are duties, taxes, or currency conversion distorting the comparison?
- Are financing remittances reducing deposits?
- Are reserves being confused with expenses?
- Are multiple payouts combined into one bank deposit?
- Did a failed or delayed payout create a timing variance?

## Shopify Review Checklist

- [ ] All payouts imported
- [ ] Bank deposits matched
- [ ] Refunds separated from retained fees
- [ ] Shipping-label charges classified
- [ ] Third-party processor fees imported
- [ ] Shopify transaction fees checked
- [ ] Reserves tracked separately
- [ ] Financing remittances tracked separately
- [ ] Unexplained adjustments documented
- [ ] App subscriptions reviewed separately
- [ ] Contribution margin compared with prior month

---

# 3. Amazon Settlement Analyzer Tab

## Tab Name

`03 Amazon Settlement Analyzer`

## Recommended Data Sources

Collect:

- Amazon settlement reports
- Transaction reports
- FBA fee reports
- Storage and aged-inventory reports
- Advertising reports
- Returns reports
- Inventory reimbursement reports
- Account-level reserve activity
- Bank deposits
- Product cost data

## Settlement Fields

| Field | Description |
|---|---|
| Settlement ID | Amazon settlement reference |
| Settlement Start | Beginning date |
| Settlement End | Ending date |
| Deposit Date | Bank deposit date |
| Product Sales | Gross product sales |
| Shipping Credits | Shipping collected |
| Promotional Rebates | Promotions |
| Sales Tax | Tax activity |
| Refunds | Customer refunds |
| Referral Fees | Marketplace commissions |
| FBA Fulfillment Fees | Fulfillment deductions |
| Storage Fees | Monthly and aged inventory |
| Inbound Placement Fees | Inbound-related charges |
| Returns Processing | Return costs |
| Removal / Disposal Fees | Inventory removal |
| Advertising | Amazon Ads |
| Refund Administration | Refund-related admin charge |
| Shipping Services | Buy Shipping and related |
| Currency Conversion | International settlement or FX |
| Reserve Withheld | New reserve |
| Reserve Released | Prior reserve released |
| Reimbursements | Inventory or service reimbursements |
| Other Adjustments | Miscellaneous |
| Expected Settlement | Formula |
| Amazon Reported Settlement | Input |
| Bank Deposit | Input |
| Variance | Formula |

## Amazon Expected Settlement Formula

```excel
=Product_Sales
+Shipping_Credits
+Promotional_Rebates
+Sales_Tax
-Refunds
-Referral_Fees
-FBA_Fulfillment_Fees
-Storage_Fees
-Inbound_Placement_Fees
-Returns_Processing
-Removal_Disposal_Fees
-Advertising
-Refund_Administration
-Shipping_Services
-Currency_Conversion
-Reserve_Withheld
+Reserve_Released
+Reimbursements
-Other_Adjustments
```

## Amazon Red Flags

Flag when:

- A SKU has positive gross margin but negative contribution margin
- Advertising cost exceeds contribution profit
- Storage cost per unit rises for three consecutive months
- Return rate exceeds the business target
- Reimbursements remain unresolved
- Reserve holds grow without a documented reason
- Settlement-to-bank variance remains unresolved after the next cycle
- A product becomes unprofitable after FBA fees
- Aged inventory creates storage costs and cash lock-up
- Referral fee percentage appears inconsistent with expectations

## Amazon Review Checklist

- [ ] Settlement date range confirmed
- [ ] All transactions imported
- [ ] Advertising imported
- [ ] FBA fees separated by type
- [ ] Storage allocated to SKU
- [ ] Returns and refund administration separated
- [ ] Reimbursements included
- [ ] Reserve activity tracked
- [ ] Deposit matched to bank
- [ ] Fee and margin results compared with prior period
- [ ] Negative-margin SKUs escalated for action

---

# 4. Stripe Fee Calculator Tab

## Tab Name

`04 Stripe Fee Calculator`

## Transaction-Level Fields

| Field | Description |
|---|---|
| Charge Date | Original charge date |
| Charge ID | Stripe charge reference |
| Customer Country | Country |
| Currency | Transaction currency |
| Payment Method | Card, ACH, wallet, etc. |
| Gross Charge | Customer charge |
| Refunded Amount | Amount refunded |
| Disputed Amount | Chargeback amount |
| Base Processing Fee | Standard processing charge |
| International Surcharge | International-card cost |
| Currency Conversion Fee | FX charge |
| Manual Entry Fee | Keyed transaction cost |
| Connect / Billing Fee | Stripe product fee |
| Dispute Fee | Chargeback fee |
| Instant Payout Fee | Expedited payout cost |
| Other Stripe Fee | Other |
| Total Stripe Fees | Formula |
| Net Stripe Proceeds | Formula |
| Effective Stripe Fee % | Formula |
| Contribution Profit | Formula |

## Total Stripe Fees

```excel
=Base_Processing_Fee
+International_Surcharge
+Currency_Conversion_Fee
+Manual_Entry_Fee
+Connect_Billing_Fee
+Dispute_Fee
+Instant_Payout_Fee
+Other_Stripe_Fee
```

## Net Stripe Proceeds

```excel
=Gross_Charge
-Refunded_Amount
-Disputed_Amount
-Total_Stripe_Fees
```

## Effective Stripe Fee Percentage

```excel
=IFERROR(Total_Stripe_Fees/(Gross_Charge-Refunded_Amount),0)
```

## Low-Ticket Order Analysis

| Order Value | Order Count | Revenue | Total Stripe Fees | Effective Fee % | Contribution Profit |
|---|---:|---:|---:|---:|---:|
| Under $10 |  |  |  |  |  |
| $10–$24.99 |  |  |  |  |  |
| $25–$49.99 |  |  |  |  |  |
| $50–$99.99 |  |  |  |  |  |
| $100–$249.99 |  |  |  |  |  |
| $250+ |  |  |  |  |  |

## Stripe Review Questions

- Are low-ticket orders absorbing a high effective fee rate?
- Are international cards creating unexpected cost?
- Is currency conversion avoidable?
- Are manually entered transactions more expensive?
- Are refunds creating retained-cost drag?
- Are instant payouts being used routinely rather than strategically?
- Are disputes concentrated in one product or traffic source?
- Are multiple Stripe products creating stacked fees?
- Does the fee total match the balance transaction export?
- Are payouts split or netted against negative balances?

---

# 5. SKU Contribution-Margin Scorecard

## Tab Name

`05 SKU Margin Scorecard`

## Scorecard Fields

| Field | Description |
|---|---|
| SKU | Product code |
| Product Name | Product name |
| Platform | Sales channel |
| Units Sold | Units sold |
| Gross Sales | Before discounts and refunds |
| Discounts | Promotions |
| Refunds | Refunded revenue |
| Net Merchandise Revenue | Formula |
| Cost of Goods Sold | Product cost |
| Inbound Freight | Allocated freight |
| Packaging | Packaging cost |
| Payment Fees | Processor fees |
| Marketplace Fees | Referral or commission |
| Fulfillment | Fulfillment cost |
| Shipping Subsidy | Shipping not paid by customer |
| Storage | Allocated storage |
| Return Cost | Reverse logistics |
| Advertising | Attributable ad spend |
| App Allocation | Product-related software |
| Contribution Profit | Formula |
| Contribution Margin % | Formula |
| Contribution Profit per Unit | Formula |
| Return Rate | Returned units divided by units sold |
| Ad Cost per Order | Advertising divided by orders |
| Fee Cost per Unit | Fees divided by units |
| Inventory Days | Days of inventory |
| Score | 0–100 |
| Recommended Action | Scale, hold, reprice, bundle, renegotiate, discontinue |

## Contribution Profit per Unit

```excel
=IFERROR(Contribution_Profit/Units_Sold,0)
```

## Rating Model

### Margin Score: 40 Points

| Contribution Margin | Points |
|---|---:|
| 30% or greater | 40 |
| 20%–29.99% | 32 |
| 10%–19.99% | 22 |
| 1%–9.99% | 10 |
| 0% or below | 0 |

### Return Score: 20 Points

| Return Rate | Points |
|---|---:|
| Under 3% | 20 |
| 3%–5.99% | 15 |
| 6%–9.99% | 8 |
| 10% or more | 0 |

### Fee Stability Score: 15 Points

| Fee Trend | Points |
|---|---:|
| Stable or declining | 15 |
| Increase under 5% | 10 |
| Increase of 5%–10% | 5 |
| Increase over 10% | 0 |

### Inventory Efficiency Score: 15 Points

| Inventory Position | Points |
|---|---:|
| Healthy turnover | 15 |
| Slightly slow | 10 |
| Materially slow | 5 |
| Aged or obsolete | 0 |

### Cash-Timing Score: 10 Points

| Cash Timing | Points |
|---|---:|
| Inventory recovers before major obligations | 10 |
| Moderate timing gap | 6 |
| Significant timing gap | 3 |
| Negative cash cycle with weak margin | 0 |

## Score Bands

| Score | Rating | Recommended Action |
|---|---|---|
| 85–100 | Scale candidate | Consider inventory and ad expansion |
| 70–84 | Healthy | Protect margin and monitor |
| 55–69 | Fixable | Reprice, bundle, reduce fees, or renegotiate |
| 40–54 | At risk | Pause scaling and investigate |
| Under 40 | Margin leak | Discontinue, redesign, or radically change economics |

---

# 6. Reserve and Hold Tracker

## Tab Name

`06 Reserve and Hold Tracker`

## Tracker Fields

| Field | Description |
|---|---|
| Platform | Shopify, Amazon, Stripe, etc. |
| Account | Store or merchant account |
| Reserve ID | Reference |
| Hold Start Date | Date hold began |
| Expected Release Date | Expected release |
| Actual Release Date | Actual release |
| Original Amount | Initial reserve |
| Additional Holds | New hold activity |
| Released Amount | Funds released |
| Applied to Refunds | Used for refunds |
| Applied to Disputes | Used for disputes |
| Applied to Negative Balance | Applied elsewhere |
| Ending Reserve Balance | Formula |
| Reason | Platform-provided reason |
| Documentation | Link to notice or support case |
| Status | Active, partial, released, disputed |
| Cash Impact | Amount unavailable |
| Follow-Up Date | Next review |
| Owner | Responsible person |
| Notes | Context |

## Ending Reserve Balance

```excel
=Original_Amount
+Additional_Holds
-Released_Amount
-Applied_to_Refunds
-Applied_to_Disputes
-Applied_to_Negative_Balance
```

## Reserve Aging Table

| Age | Amount | Risk | Action |
|---|---:|---|---|
| 0–14 days |  | Low | Monitor |
| 15–30 days |  | Moderate | Verify expected release |
| 31–60 days |  | Elevated | Contact support |
| 61–90 days |  | High | Escalate |
| Over 90 days |  | Critical | Formal review and cash-plan adjustment |

## Reserve Review Checklist

- [ ] Reserve is not classified as a permanent fee
- [ ] Original platform notice saved
- [ ] Expected release date recorded
- [ ] Actual releases matched
- [ ] Amounts applied to refunds or disputes documented
- [ ] Cash-flow forecast updated
- [ ] Working-capital plan reflects unavailable cash
- [ ] Support case opened when timing is unclear
- [ ] Reserve concentration by platform reviewed
- [ ] Reserve growth compared with sales growth

---

# 7. Monthly Fee-Variance Dashboard

## Tab Name

`07 Monthly Fee Dashboard`

## KPI Cards

Include:

- Gross sales
- Net merchandise revenue
- Platform and payment fees
- Effective platform fee rate
- Refund rate
- Contribution profit
- Contribution margin
- Advertising as a percentage of net revenue
- Reserve balance
- Net cash deposited
- Unexplained payout variance
- Negative-margin SKU count

## Monthly Comparison Table

| Metric | Current Month | Prior Month | Change $ | Change % | Three-Month Average | Status |
|---|---:|---:|---:|---:|---:|---|
| Gross sales |  |  |  |  |  |  |
| Net revenue |  |  |  |  |  |  |
| Payment fees |  |  |  |  |  |  |
| Marketplace fees |  |  |  |  |  |  |
| Fulfillment |  |  |  |  |  |  |
| Storage |  |  |  |  |  |  |
| Advertising |  |  |  |  |  |  |
| Refund costs |  |  |  |  |  |  |
| Contribution profit |  |  |  |  |  |  |
| Contribution margin |  |  |  |  |  |  |
| Reserve balance |  |  |  |  |  |  |
| Payout variance |  |  |  |  |  |  |

## Variance Formula

```excel
=Current_Month_Fee-Prior_Month_Fee
```

## Variance Percentage

```excel
=IFERROR((Current_Month_Fee-Prior_Month_Fee)/Prior_Month_Fee,0)
```

## Suggested Alerts

Flag red when:

- Contribution margin falls by 5 percentage points or more
- Effective fee rate rises by 10% or more against the three-month average
- Refund rate rises by 25% or more
- Advertising exceeds target contribution economics
- Reserve balance exceeds the defined cash threshold
- Unexplained variance exceeds the materiality limit
- Negative-margin SKU count increases
- Storage rises while units sold decline
- Net deposits grow slower than gross sales for two months

Flag yellow when:

- Fee rate rises between 5% and 10%
- Contribution margin falls between 2 and 5 percentage points
- Reserve balance grows but remains manageable
- Other adjustments remain unresolved
- One platform contributes more than 70% of cash receipts

## Recommended Charts

1. Effective platform fee rate by month
2. Contribution margin by platform
3. Gross sales versus net cash deposited
4. Reserve balance by platform
5. Refund rate by SKU
6. Top five fee categories
7. Negative-margin SKUs
8. Advertising spend versus contribution profit

---

# 8. AI Audit Prompt

Use this prompt only with redacted, structured exports.

```text
You are an ecommerce finance-operations analyst conducting an AI platform fee audit.

OBJECTIVE

Reconcile gross sales, platform deductions, settlements, payouts, reserves, refunds, advertising, product costs, and bank deposits. Identify margin leaks across Shopify, Amazon, Stripe, and other marketplaces.

IMPORTANT RULES

1. Do not invent missing transactions, fee rates, costs, platform policies, or explanations.
2. Identify missing fields, incomplete date ranges, duplicate rows, and inconsistent currencies.
3. Separate permanent expenses from temporary reserves and timing differences.
4. Separate refunds from retained processing fees and return-related costs.
5. Do not treat sales tax or duties as merchandise revenue unless the accounting method requires it.
6. Do not treat financing remittances as ordinary platform fees.
7. Detect duplicate transactions before calculating totals.
8. Keep currencies separate unless valid conversion rates are supplied.
9. Flag ambiguous adjustments for human review.
10. State all assumptions.
11. Do not claim a platform made an error unless the supplied evidence supports it.
12. Do not provide tax, legal, accounting, lending, or underwriting conclusions.

DATASETS PROVIDED

- Orders
- Refunds and returns
- Platform settlements
- Payout reports
- Processor balance transactions
- Bank deposits
- Advertising costs
- Product costs
- Fulfillment and shipping costs
- App or subscription costs
- Reserve or hold notices
- Financing remittance records

TASKS

A. Validate each dataset and its date coverage.
B. List missing fields and data-quality problems.
C. Create a normalized fee taxonomy.
D. Match orders to settlements where possible.
E. Reconcile gross customer charges to expected payouts.
F. Reconcile expected payouts to platform-reported payouts.
G. Reconcile platform payouts to bank deposits.
H. Calculate:
   - gross sales
   - net merchandise revenue
   - total platform and payment fees
   - effective platform fee rate
   - contribution profit
   - contribution margin
   - refund drag
   - reserve balance
   - payout variance
   - fee cost per order
   - fee cost per unit
I. Break results down by:
   - platform
   - month
   - SKU
   - product
   - order-size band
   - country
   - currency
   - payment method
J. Flag:
   - unexpected fee increases
   - duplicate charges
   - negative-margin SKUs
   - unusually expensive returns
   - international or currency leakage
   - unexplained payout differences
   - unresolved reserves
   - excessive other adjustments
   - app costs without clear value
   - advertising that exceeds contribution profit
K. Rank findings by:
   - estimated financial impact
   - confidence
   - urgency
   - difficulty to fix
L. Produce a prioritized operator action plan.

OUTPUT FORMAT

1. Executive summary
2. Data-quality report
3. Assumptions
4. Gross-to-net reconciliation table
5. Fee breakdown by category
6. Channel comparison
7. SKU margin scorecard
8. Reserve and hold summary
9. Exception report
10. Top five margin leaks
11. Recommended actions
12. Questions requiring human review
13. Draft platform-support questions
14. Working-capital implications
```

---

# 9. Fee-Dispute Documentation Checklist

## Tab Name

`09 Dispute Log`

## Dispute Log Fields

| Field | Description |
|---|---|
| Case ID | Internal case number |
| Platform | Shopify, Amazon, Stripe, etc. |
| Platform Support Case | Support reference |
| Date Opened | Date submitted |
| Owner | Responsible person |
| Payout / Settlement ID | Relevant payout |
| Order / Transaction ID | Relevant transaction |
| Fee Type | Referral, processing, storage, fulfillment, etc. |
| Disputed Amount | Amount questioned |
| Expected Amount | Calculated amount |
| Actual Amount | Platform charge |
| Difference | Formula |
| Policy or Agreement Reference | Relevant term |
| Supporting Export | File link |
| Screenshot | File link |
| Calculation | Worksheet link |
| Explanation | Plain-English issue |
| Requested Resolution | Refund, correction, explanation, reclassification |
| Platform Response | Response |
| Status | Open, pending, resolved, denied, escalated |
| Resolution Amount | Amount recovered |
| Closed Date | Date closed |
| Notes | Follow-up |

## Documentation Checklist

- [ ] Platform and account identified
- [ ] Payout or settlement ID included
- [ ] Order or transaction IDs included
- [ ] Date range included
- [ ] Fee type identified
- [ ] Expected fee calculated
- [ ] Actual fee documented
- [ ] Difference calculated
- [ ] Raw report attached
- [ ] Relevant screenshot attached
- [ ] Pricing or policy reference saved
- [ ] Account agreement reviewed
- [ ] Currency confirmed
- [ ] Refund, reserve, and timing issues ruled out
- [ ] Duplicate transaction ruled out
- [ ] Requested resolution stated
- [ ] Internal owner assigned
- [ ] Follow-up date scheduled

## Support Message Template

```text
Subject: Request for Review of Fee or Payout Adjustment

Hello,

I am requesting a review of a fee or payout adjustment associated with the following account activity:

Account:
Payout or Settlement ID:
Order or Transaction ID:
Transaction Date:
Fee Type:
Amount Charged:
Expected Amount:
Difference:

Based on the attached settlement report, transaction export, and reconciliation worksheet, the amount appears inconsistent with the fee treatment we expected.

Please review the charge and provide:

1. The calculation used
2. The fee category applied
3. The applicable pricing, policy, or account term
4. Whether the charge should be corrected
5. Any additional documentation needed

Attached:
- Relevant export
- Reconciliation calculation
- Supporting screenshots
- Policy or pricing reference

Thank you.
```

---

# 10. Working-Capital Decision Worksheet

## Tab Name

`08 Working Capital Decision`

## Step 1: Identify the Primary Problem

Select one:

- [ ] Healthy margin, temporary payout delay
- [ ] Healthy margin, inventory purchased before cash returns
- [ ] Healthy product, expensive sales channel
- [ ] High returns
- [ ] High advertising cost
- [ ] Excessive fulfillment or shipping cost
- [ ] Low average order value
- [ ] Platform reserve or hold
- [ ] Slow-moving inventory
- [ ] Negative contribution margin
- [ ] Unexplained deductions or data problem
- [ ] Multiple issues

## Step 2: Calculate the Cash Gap

### Cash Needed Before Next Payout

```excel
=Inventory_Purchases
+Advertising
+Payroll
+Rent
+Shipping
+Taxes_Due
+Other_Critical_Expenses
-Available_Cash
-Confirmed_Receivables
-Confirmed_Payouts
```

### Estimated Working-Capital Gap

```excel
=MAX(0,Cash_Needed_Before_Next_Payout)
```

## Step 3: Use-of-Funds Table

| Use of Funds | Amount | Expected Result | Timing | Confidence |
|---|---:|---|---|---|
| Inventory |  |  |  |  |
| Advertising |  |  |  |  |
| Fulfillment |  |  |  |  |
| Payroll |  |  |  |  |
| Reserve bridge |  |  |  |  |
| Supplier discount |  |  |  |  |
| Other |  |  |  |  |

## Step 4: Contribution Test

Answer:

1. Does the product produce positive contribution profit?
2. Is contribution margin stable?
3. Is demand proven?
4. Is the cash gap primarily caused by timing?
5. Will additional inventory sell within the expected period?
6. Will advertising remain profitable after increased spend?
7. Can the business support repayment from ordinary cash flow?
8. Are reserves expected to release within a documented period?
9. Are taxes and critical expenses accounted for?
10. Is the owner trying to finance losses rather than growth?

## Step 5: Decision Matrix

| Situation | Likely Next Action |
|---|---|
| Positive margin + short timing gap | Consider working capital |
| Positive margin + inventory opportunity | Evaluate inventory funding |
| Positive margin + reserve hold | Build reserve bridge plan |
| Positive product + expensive channel | Improve channel mix |
| High refund rate | Fix product, listing, or fulfillment |
| High ad cost | Improve acquisition economics |
| Negative contribution margin | Do not scale with debt |
| Unresolved data | Reconcile before deciding |
| Slow inventory | Reduce purchasing or liquidate |
| Low order value | Test bundles, thresholds, and pricing |

## Working-Capital Readiness Score

Score each item from 0 to 2.

- 0 = No
- 1 = Partially
- 2 = Yes

| Question | Score |
|---|---:|
| Positive contribution profit |  |
| Stable contribution margin |  |
| Clear use of funds |  |
| Documented cash gap |  |
| Reliable sales history |  |
| Clean payout reconciliation |  |
| Manageable return rate |  |
| Reasonable reserve exposure |  |
| Repayment capacity |  |
| Complete financial documents |  |

### Score Interpretation

| Score | Interpretation |
|---|---|
| 17–20 | Strong operational case for further funding review |
| 13–16 | Potentially viable; fix identified weaknesses |
| 9–12 | Caution; improve economics first |
| 0–8 | Funding may magnify the problem |

This score is an internal planning tool, not a funding approval predictor.

## Final Decision Statement

> The business is considering **$__________** in working capital to fund **__________________**. The primary issue is **__________________**. Current contribution margin is **__________%**. The estimated cash gap lasts **__________ days**. The expected source of repayment is **__________________**. The largest unresolved risk is **__________________**.

---

# Monthly Close Workflow

## Gather

- Export orders
- Export refunds
- Export settlements
- Export payouts
- Export advertising
- Export fulfillment and storage charges
- Export processor transactions
- Download bank activity
- Update product costs
- Update reserve notices
- Update financing remittances

## Normalize

- Standardize dates
- Standardize currencies
- Standardize platform names
- Standardize SKU names
- Remove duplicates
- Map fee categories
- Match payout IDs
- Match bank deposits

## Reconcile

- Reconcile charges to settlements
- Reconcile settlements to payouts
- Reconcile payouts to bank deposits
- Separate fees, reserves, taxes, financing, and timing differences
- Resolve material Other adjustments

## Decide

- Review contribution margin
- Review negative-margin SKUs
- Review reserve exposure
- Review fee variances
- Review refund drag
- Review advertising economics
- Open disputes
- Update working-capital decision
- Assign corrective actions

---

# Data-Quality Rules

## Do Not Combine Currencies Without Conversion Data

Keep currencies separate unless a reliable exchange rate and conversion date are supplied.

## Do Not Double Count Advertising

Choose one authoritative source for each advertising cost and document it.

## Do Not Double Count Refunds

A refund may appear in several reports. Track the economic event once, then use references to reconcile movement.

## Do Not Treat Reserves as Fees

Reserve holds affect available cash. They become expenses only when applied to a real obligation.

## Do Not Treat Taxes as Revenue

Track merchandise revenue separately from taxes and duties collected.

## Do Not Treat Financing Remittances as Platform Fees

Track them as financing cash-flow activity.

## Minimum Data-Quality Checklist

- [ ] Complete date range
- [ ] No duplicate transaction IDs
- [ ] Currency populated
- [ ] Platform populated
- [ ] Payout IDs populated
- [ ] Refunds matched
- [ ] Reserves separated
- [ ] Taxes separated
- [ ] Financing separated
- [ ] Bank deposits matched
- [ ] Product cost updated
- [ ] Advertising source documented
- [ ] Material Other adjustments explained

---

# Final Audit Summary

## What Happened

- Gross sales: $__________
- Net merchandise revenue: $__________
- Total platform and payment fees: $__________
- Effective platform fee rate: __________%
- Contribution profit: $__________
- Contribution margin: __________%
- Reserve balance: $__________
- Unexplained variance: $__________

## Biggest Margin Leaks

1. ______________________________________
2. ______________________________________
3. ______________________________________
4. ______________________________________
5. ______________________________________

## Actions This Month

1. ______________________________________
2. ______________________________________
3. ______________________________________
4. ______________________________________
5. ______________________________________

## Working-Capital Decision

- [ ] No capital needed
- [ ] Reconcile more data first
- [ ] Fix margins before borrowing
- [ ] Consider a short-term timing-gap solution
- [ ] Evaluate inventory funding
- [ ] Review ecommerce funding options
- [ ] Seek professional accounting or finance review

---

# Final Operator Checklist

## Before the Audit

- [ ] Choose the audit period
- [ ] Define materiality threshold
- [ ] Export all required reports
- [ ] Redact sensitive data
- [ ] Confirm currencies
- [ ] Update product costs
- [ ] Identify account owners

## During the Audit

- [ ] Normalize transactions
- [ ] Remove duplicates
- [ ] Classify all fees
- [ ] Separate reserves
- [ ] Separate taxes
- [ ] Separate financing remittances
- [ ] Match payouts
- [ ] Match bank deposits
- [ ] Calculate contribution margin
- [ ] Rank margin leaks
- [ ] Flag unresolved variances

## After the Audit

- [ ] Open support cases
- [ ] Reprice or bundle weak products
- [ ] Review channel mix
- [ ] Cancel unused apps
- [ ] Address return drivers
- [ ] Review fulfillment and storage
- [ ] Update working-capital plan
- [ ] Assign corrective owners
- [ ] Schedule next review
- [ ] Save the completed audit packet

---

## Moonshine Capital

This worksheet is designed to help operators understand cash flow, margin, and funding readiness before making expensive decisions.

Funding is not guaranteed. Eligibility, terms, and available products vary by business profile and provider requirements.
