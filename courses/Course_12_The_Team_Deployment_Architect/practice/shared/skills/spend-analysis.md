# Spend Analysis Skill

Analyze spend data for a single category.

## Input
- Category name
- Path to spend data CSV

## Steps
1. Read the spend CSV and filter to the specified category.
2. Calculate total spend, transaction count, and average transaction size.
3. Group by supplier. Rank suppliers by total spend.
4. Identify the top 3 suppliers by spend and their percentage of category total.
5. Flag any supplier with fewer than 5 transactions (possible maverick spend).
6. Calculate month-over-month spend trend for the trailing 6 months.

## Output format
Save to outputs/ as `spend-analysis-<category>.md` with sections:
- Summary (total spend, transaction count, supplier count)
- Top suppliers table
- Trend (up, down, stable with percentage)
- Flags (maverick spend, concentration risk)
