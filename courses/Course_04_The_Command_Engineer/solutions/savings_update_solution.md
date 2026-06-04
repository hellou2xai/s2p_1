<!-- v1.0 2026-04-25 Initial. -->

# /savings-update

Compare actual spend to annual targets and produce a savings tracker.

## Usage

/savings-update $ARGUMENTS

Parse $ARGUMENTS as: [period]
- period: Q1, Q2, Q3, Q4, H1, H2, or YTD (same date logic as /spend-analyze)

## Inputs

data/spend-transactions.csv
  Filter rows by period. Sum amount_usd per supplier.

data/supplier-master.csv
  Pull annual_target_usd per supplier. Prorate to the period length.

## Process

1. Filter spend-transactions.csv by period. Sum amount_usd per supplier_id.
2. Read supplier-master.csv. For each supplier with an annual_target_usd > 0, compute prorated_target = annual_target_usd x (period_days / 365).
3. Compute variance = actual_spend minus prorated_target. Positive means over target. Negative means under target (a saving).
4. Compute variance_pct = (variance / prorated_target) x 100.
5. Sort by variance descending (biggest overspend at top).
6. Compute portfolio totals: total actual, total prorated target, total variance, total variance percentage.
7. Flag any supplier where variance_pct exceeds +10% (overspend) or is below -15% (possible underdelivery or demand shortfall).

## Output format

Save to outputs/savings-tracker-[period]-[YYYY-MM-DD].md

Four sections:
1. **Portfolio summary** (one paragraph): total actual spend, total prorated target, total variance (USD and %), number of suppliers over target, number under target.
2. **Supplier variance table** (table): Supplier, Category, Tier, Actual (USD), Prorated Target (USD), Variance (USD), Variance (%), Flag. Show all suppliers with a target. Cap at 20 rows.
3. **Flags** (bullet list): suppliers flagged for overspend (>+10%) or demand shortfall (<-15%), each with the variance figure and a one-line note.
4. **Recommended actions** (three bullet points): the top three actions, each naming a supplier and a specific action.

End with an audit footer.

## Quality criteria

- Prorated target uses the exact number of days in the period, not a fixed fraction.
- Variance is computed as actual minus target, not the other way around.
- Flags use the exact thresholds (+10% and -15%).
- The portfolio total matches the sum of individual supplier rows.
