---
title: "Stripe Fee Calculation Guide"
filename: "stripe-fee-calculation-guide.md"
version: "1.0.0"
status: "production-ready"
purpose: "Production guide for analyzing Stripe balance transactions, fees, refunds, disputes, reserves, payouts, Instant Payouts, and multi-currency activity."
primary_users:
  - "AI Platform Fee Audit Copilot"
  - "Stripe operators"
  - "platform and marketplace finance teams"
  - "ecommerce finance operations teams"
  - "human reviewers"
related_files:
  - "ai-platform-fee-audit-copilot-builder-instructions.md"
  - "normalized-platform-fee-taxonomy.yaml"
  - "master-transaction-schema.json"
  - "column-mapping-library.json"
  - "reconciliation-and-calculation-rules.md"
  - "reserve-and-hold-tracker.csv"
  - "monthly-fee-variance-dashboard-schema.json"
last_updated: "2026-07-27"
---

# Stripe Fee Calculation Guide

## 1. Purpose and Authority

Use this guide to trace Stripe payment activity through the Stripe balance, fees, refunds, disputes, reserves, payouts, and bank deposits. It supports operational review and does not replace Stripe pricing, contract terms, accounting, tax, legal, or lending judgment.

## 2. Source Hierarchy

1. Balance Transaction objects or itemized balance reports
2. Payout reconciliation or payout reports
3. PaymentIntent, Charge, Refund, Dispute, Transfer, Application Fee, and Payout objects
4. Stripe Dashboard evidence
5. Matching bank activity
6. Merchant order, COGS, advertising, and fulfillment records

Use balance transactions as the canonical ledger of Stripe-balance movement. Expand or link the source object when business context is required.

## 3. Unit and Sign Controls

Stripe API monetary amounts commonly use the currency's smallest unit, while many report exports use major units. Record the unit before normalization.

For a Stripe balance transaction:

```text
net = amount - fee
```

API semantics:

- `amount`: signed gross impact
- `fee`: non-negative fee magnitude when assessed
- `net`: signed net impact to the Stripe balance
- `available_on`: date the net funds become available
- `status`: pending or available
- `reporting_category`: preferred reporting classification context
- `type`: event-specific transaction type

Do not divide zero-decimal currencies by 100. Use the currency exponent defined for the specific currency and source.

## 4. Minimum Files

### Minimum viable payout reconciliation

- Itemized balance transactions for the audit period
- Payout list and payout detail
- Matching bank activity

### Add for complete analysis

- Charge or PaymentIntent detail
- Refund and dispute detail
- Connect transfers and application fees
- Instant Payout and advance-funding detail
- Reserve or minimum-balance activity
- Contract/pricing evidence for fee reasonableness
- Order, COGS, fulfillment, shipping, and advertising data for margin analysis

## 5. Required Fields

Map to `master-transaction-schema.json`:

- `source_record_id` = balance transaction ID when available
- `transaction_reference_id` = related Stripe source object ID
- `payout_id`
- `payout_trace_id`
- `transaction_at`
- `available_on`
- `payout_initiated_date`
- `bank_posted_date`
- `transaction_currency`
- `source_amount`
- `gross_amount`
- `fee_amount`
- `refund_amount`
- `chargeback_amount`
- `reserve_hold_amount`
- `reserve_release_amount`
- `net_amount`
- `exchange_rate`
- `normalized_classification`
- `duplicate_fingerprint`
- `reconciliation_status`

Preserve `type`, `reporting_category`, `balance_type`, status, source ID, description, and fee detail components in source metadata or notes when no dedicated normalized field exists.

## 6. Classification Map

| Stripe activity | Canonical code | Treatment |
|---|---|---|
| Charge/payment gross | `REV_GROSS_SALES` | Revenue evidence only when linked to underlying sale |
| Stripe processing fee | `FEE_PROCESSING` | Fee magnitude from balance transaction |
| Stripe FX fee | `FEE_FX` | Separate from exchange-rate effect |
| International card fee | `FEE_INTERNATIONAL` | Use fee detail or verified pricing evidence |
| Application fee charged to connected account | `FEE_MARKETPLACE` or `FEE_PROCESSING` | Preserve Connect context and beneficiary |
| Instant Payout fee | `FEE_INSTANT_PAYOUT` | Separate payout-access cost |
| Refund | `REV_REFUND` | Contra-revenue when linked to original sale |
| Dispute opened | `RISK_DISPUTE` | Lifecycle event |
| Disputed amount debit | `RISK_CHARGEBACK` | Economic debit subject to outcome |
| Reserve hold | `LIQ_RESERVE_HOLD` | Restricted cash, not expense |
| Reserve release | `LIQ_RESERVE_RELEASE` | Release of restricted cash, not revenue |
| Minimum-balance hold | `LIQ_HOLD` | Liquidity restriction |
| Payout | `TRF_PAYOUT` | Transfer out of Stripe balance |
| Bank credit | `TRF_BANK_DEPOSIT` | Transfer into bank cash |
| Advance/advance funding | `ADJ_MANUAL` or documented liquidity subtype | Do not treat as revenue or fee |
| Transfer to connected account | `TRF_PAYOUT` or internal transfer subtype | Avoid revenue duplication |
| Unsupported transaction | `UNCLASSIFIED` | Preserve type and require review if material |

## 7. Charges and PaymentIntents

- Use PaymentIntent or Charge for customer/payment context.
- Use the related Balance Transaction for actual Stripe-balance amount, fee, net, currency, and availability.
- One PaymentIntent can have multiple charges or attempts; select the successful captured lifecycle.
- Do not count authorization-only or failed payments as settled revenue.
- Keep platform Connect transfers and application fees separate from gross customer payment.

## 8. Processing Fee Analysis

Historical fee:

```text
observed_processing_fee = balance_transaction.fee
observed_effective_fee_rate = fee / eligible_gross_amount
```

For multi-component fee details:

```text
total_fee = stripe_fee + application_fee + tax_fee + passthrough_fee + other_supported_fee
```

Use actual source values. Compare to contract or current pricing only as a reasonableness test. Pricing varies by country, product, payment method, volume, and contract. A mismatch is not automatically leakage.

## 9. International and Currency-Conversion Fees

Separate:

- Customer transaction currency
- Charge or PaymentIntent currency
- Stripe balance/settlement currency
- Bank payout currency
- `exchange_rate`
- Explicit `stripe_fx_fee`
- International-card fee detail

If Stripe provides an exchange rate, preserve its quote direction. Do not reconstruct the rate when fees or multiple conversions make the relationship ambiguous.

## 10. Refunds

- Link the Refund to the original PaymentIntent/Charge and both balance transactions.
- Record refunded principal separately from any fee retained or newly assessed.
- Stripe states refunds use the available balance; a card refund can remain pending when available funds are insufficient.
- Fee treatment may depend on region, product, pricing, and contract. Use actual balance transactions and verified pricing rather than assuming a universal refund-fee rule.
- A failed refund and a later successful refund are lifecycle records, not duplicate losses.

## 11. Disputes and Chargebacks

Track:

1. Dispute ID and reason
2. Original payment and charge IDs
3. Disputed amount
4. Dispute received fee
5. Countered fee, if applicable
6. Evidence deadline
7. Status and response
8. Won/lost/withdrawn outcome
9. Principal and fee recovery balance transactions

At opening, Stripe generally debits the disputed amount and applicable fee from the balance. The issuing bank decides the outcome. Do not promise recovery or classify an open dispute as permanently lost.

## 12. Connect and Application Fees

For Connect, establish the charge model:

- Direct charge
- Destination charge
- Separate charge and transfer

Then identify which account bears:

- Processing fee
- Application fee
- Refund
- Dispute
- Transfer reversal
- Payout fee

Do not count the same customer charge as revenue for both platform and connected account. Use account IDs, charge IDs, transfer IDs, and application-fee IDs to maintain the economic owner and transfer chain.

## 13. Instant Payouts

Instant Payouts can move eligible funds to a supported debit card or bank account, including outside normal banking hours, and Stripe states funds usually appear within about 30 minutes. Eligibility, supported institutions, limits, and fees vary.

Audit controls:

- Identify standard versus instant payout
- Capture payout amount, payout fee, destination, initiation time, and bank-posted time
- Classify the payout fee as `FEE_INSTANT_PAYOUT`
- Classify the payout as `TRF_PAYOUT`
- Avoid treating earlier access to pending funds as revenue

## 14. Instant Payouts With Advance Funding

When an Instant Payout exceeds currently available funds, Stripe can create `advance` and `advance_funding` balance transactions that move value between pending and available balances. These are liquidity-state changes, not new sales.

Control:

```text
advance_funding_increase_to_available
= corresponding_reduction_to_pending_balance
```

Link all advance-funding records to the payout and underlying availability dates. Do not classify the temporary internal balance movement as fee leakage.

## 15. Reserves and Minimum Balances

Stripe may maintain separate reserve or minimum-balance activity. Track by balance type and transaction type, including:

- `reserve_hold`
- `reserve_release`
- `reserved_funds`
- `payment_network_reserve_hold`
- `payment_network_reserve_release`
- `payout_minimum_balance_hold`
- `payout_minimum_balance_release`

Reserve treatment:

- Hold: `LIQ_RESERVE_HOLD` or `LIQ_HOLD`
- Release: `LIQ_RESERVE_RELEASE`
- Application to refund/dispute: classify the underlying economic loss once and update reserve balance separately
- Do not treat a reserve release as revenue

## 16. Payout Reconciliation

For automatic payouts, Stripe's balance-transaction listing can be filtered by payout ID to retrieve transactions included in a payout.

Payout control:

```text
sum(net of included balance transactions)
+/- payout-specific adjustments
= payout amount
```

Then:

```text
payout amount - bank deposit amount = payout_to_bank_variance
```

Match by:

1. Payout ID and trace ID
2. Currency and exact amount
3. Expected arrival date and bank-posted date
4. Bank descriptor and destination alias
5. Documented split/aggregate deposit

## 17. Balance Availability and Timing

Do not confuse:

- Payment created/captured
- Balance transaction created
- Funds available-on date
- Payout initiated
- Payout expected arrival
- Bank posted

Cash-timing diagnosis should report each delay separately:

```text
settlement_delay_days = available_on - transaction_at
payout_queue_days = payout_initiated_date - available_on
bank_delay_days = bank_posted_date - payout_initiated_date
end_to_end_days = bank_posted_date - transaction_at
```

## 18. Multi-Currency Handling

- Reconcile one Stripe balance currency at a time.
- Confirm whether the account has separate balances by currency.
- Preserve minor-unit exponent.
- Use source exchange rate and explicit FX fee when available.
- Do not net balances across currencies before conversion.
- Present native-currency and consolidated views separately.

## 19. Duplicate Prevention

Recommended fingerprint:

```text
stripe_account_id + balance_transaction_id + type + reporting_category
+ source_id + amount + fee + net + currency + created_timestamp
```

Related balance transactions for a charge, refund, dispute, transfer, payout, or reserve are not duplicates merely because they share a source object or amount.

## 20. Common Errors

| Error | Control |
|---|---|
| Treating API cents as dollars | Apply currency exponent before normalization |
| Using Charge fee instead of Balance Transaction fee | Use the balance transaction as fee source |
| Counting charge and payout as revenue | Payout is a transfer |
| Counting refund and dispute for same event | Review lifecycle and IDs |
| Treating reserve hold as expense | Use liquidity restriction |
| Treating reserve release as revenue | Link to reserve ledger |
| Ignoring Connect account ownership | Preserve account and transfer chain |
| Treating advance funding as sales | It is an internal availability movement |
| Hardcoding Stripe pricing | Verify contract and actual transaction evidence |
| Matching deposits by amount alone | Require identifiers, currency, destination, and timing |

## 21. Fictional Worked Example

**Account:** `acct_fictional_northstar`  
**Currency:** USD  
**Payout:** `po_fictional_0720`

| Balance activity | Gross/amount | Fee | Net |
|---|---:|---:|---:|
| Card payments | 20,000.00 | 610.00 | 19,390.00 |
| Refunds | (1,250.00) | 0.00 | (1,250.00) |
| Dispute debit | (450.00) | 15.00 | (465.00) |
| Reserve hold | (1,000.00) | 0.00 | (1,000.00) |
| Instant Payout fee | 0.00 | 90.00 | (90.00) |
| Expected payout |  |  | 16,585.00 |

The bank posts 16,585.00 on the same day. The payout reconciles. The 1,000.00 reserve is restricted cash; the 90.00 Instant Payout fee is a payout-access cost; the open dispute remains provisional until outcome evidence is available.

## 22. Human-Review Triggers

- Material payout or bank variance
- Currency exponent uncertainty
- Connect ownership ambiguity
- Open or conflicting dispute lifecycle
- Reserve balance that does not roll forward
- Material `UNCLASSIFIED` balance transaction
- Contract fee comparison without verified pricing evidence
- Proposed dispute submission or financial-record update
- Any output used for accounting, tax, legal, lending, or underwriting decisions

## 23. Required Output

1. Scope, Stripe account, currency, and period
2. Source files and units
3. Balance activity roll-forward
4. Fee-detail table
5. Refund and dispute lifecycle table
6. Reserve/minimum-balance ledger
7. Payout-to-bank match table
8. Timing analysis
9. Connect transfer chain where relevant
10. Exceptions and confidence labels
11. Prioritized next actions
12. Machine-readable fields compatible with `output-schema.json`

## Official Source References

Verified on `2026-07-27`. Platform fields, fees, eligibility, timing, and policies can change; validate the live account and current documentation before relying on a material conclusion.

- [Balance Transaction object](https://docs.stripe.com/api/balance_transactions/object)
- [Balance report types](https://docs.stripe.com/reports/report-types/balance)
- [Receive payouts and Instant Payouts](https://docs.stripe.com/payouts)
- [Balances and settlement time](https://docs.stripe.com/payments/balances)
- [Refund payments](https://docs.stripe.com/refunds)
- [How disputes work](https://docs.stripe.com/disputes/how-disputes-work)
- [Respond to disputes](https://docs.stripe.com/disputes/responding)
- [Instant Payouts with advance funding](https://docs.stripe.com/payouts/instant-payouts-with-advance-funding)
