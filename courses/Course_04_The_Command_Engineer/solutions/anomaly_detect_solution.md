<!-- v1.0 2026-04-25 Initial. -->

# /anomaly-detect

Scan spend transactions for statistical outliers and suspicious patterns.

## Usage

/anomaly-detect $ARGUMENTS

Parse $ARGUMENTS as: [threshold] [period]
- threshold: a multiplier (e.g., 2.5 means flag transactions exceeding 2.5x the category average)
- period: Q1, Q2, Q3, Q4, H1, H2, or YTD (same date logic as /spend-analyze)

## Inputs

data/spend-transactions.csv
  Filter rows by period. Compute category-level average amount_usd.

data/supplier-master.csv
  Join on supplier_id for tier, risk_rating, and status.

## Process

1. Filter spend-transactions.csv by period.
2. Compute the average amount_usd per category across all filtered rows.
3. Flag every transaction where amount_usd exceeds (category average x threshold).
4. For each flagged transaction, note the transaction_id, date, supplier_name, category, amount_usd, and the category average.
5. Scan for duplicate PO patterns: group by po_number, flag any PO that appears more than once with different dates or amounts.
6. For each duplicate PO group, list all transactions sharing that PO number.
7. Sort flagged transactions by amount_usd descending.
8. Sort duplicate PO groups by total combined amount descending.

## Output format

Save to outputs/anomaly-report-[period]-[YYYY-MM-DD].md

Four sections:
1. **Summary** (one paragraph): number of high-value flags, number of duplicate PO flags, total USD at risk.
2. **High-value transactions** (table): Transaction ID, Date, Supplier, Category, Amount (USD), Category Avg, Multiple. Capped at 20 rows.
3. **Duplicate PO patterns** (table): PO Number, Count, Transactions (IDs), Combined Amount (USD). Capped at 15 rows.
4. **Recommended actions** (three bullet points): the top three actions the procurement team should take, each naming a specific supplier or PO.

End with an audit footer.

## Quality criteria

- Every flagged transaction has amount_usd > (category average x threshold). No false flags.
- Duplicate PO groups have at least two transactions sharing the same po_number.
- Recommended actions name specific suppliers or PO numbers from the flagged data.
- The summary paragraph includes the exact count and total USD, not approximate language.
