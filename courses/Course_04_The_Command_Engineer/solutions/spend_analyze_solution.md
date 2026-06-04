<!-- v1.0 2026-04-25 Initial. -->

# /spend-analyze

Produce a spend breakdown for a given period and category.

## Usage

/spend-analyze $ARGUMENTS

Parse $ARGUMENTS as: [period] [category]
- period: Q1, Q2, Q3, Q4, H1, H2, or YTD (relative to today 2026-04-25)
- category: direct-materials, logistics, indirect, mro, or all

Date ranges:
- Q1 = Jan 1 to Mar 31. Q2 = Apr 1 to Jun 30. Q3 = Jul 1 to Sep 30. Q4 = Oct 1 to Dec 31.
- H1 = Jan 1 to Jun 30. H2 = Jul 1 to Dec 31.
- YTD = Jan 1 of the current year to today.
- Use the most recent completed year for the period (2025 for Q3 and Q4, 2026 for Q1 and Q2).

## Inputs

data/spend-transactions.csv
  Filter rows where `date` falls inside the period.
  If category is not "all", filter rows where `category` matches.

data/supplier-master.csv
  Join on supplier_id to pull tier and risk_rating.

## Process

1. Filter spend-transactions.csv by period and category.
2. Group by supplier_id. Sum amount_usd per supplier. Sort descending.
3. Show top 10 suppliers by spend.
4. Compute total spend for the period.
5. Compute prior-period spend (same length, immediately before). Example: if period is Q1 2026, prior period is Q4 2025.
6. Compute period-over-period change (absolute USD and percentage).
7. Show category-level subtotals if category is "all".
8. Flag any supplier whose spend exceeds 120% of their annual_target_usd prorated to the period length.

## Output format

Save to outputs/spend-analysis-[period]-[category]-[YYYY-MM-DD].md

Three sections:
1. **Summary** (one paragraph): total spend, number of transactions, period-over-period change.
2. **Top 10 suppliers** (table): Rank, Supplier, Category, Tier, Spend (USD), % of Total, vs Prior Period.
3. **Flags** (bullet list): any suppliers exceeding prorated target.

End with an audit footer: date, source files, model, operator.

## Quality criteria

- Every figure traces to spend-transactions.csv. No invented numbers.
- Prior-period comparison uses the same number of days.
- Table has exactly 10 rows (or fewer if fewer suppliers exist in the filter).
- File name includes the period, category, and today's date.
