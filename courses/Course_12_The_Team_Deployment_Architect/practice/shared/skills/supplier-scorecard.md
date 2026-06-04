# Supplier Scorecard Skill

Generate a quarterly scorecard for a single supplier.

## Input
- Supplier name or ID
- Path to scorecard data CSV

## Steps
1. Read the scorecard CSV and filter to the specified supplier.
2. Extract scores for the most recent quarter across all four dimensions.
3. Calculate the weighted overall score.
4. Compare to the previous quarter. Note any dimension that changed by more than 0.5 points.
5. Flag if overall score is below 3.0 (at risk) or below 2.5 (corrective action).

## Output format
Save to outputs/ as `scorecard-<supplier_id>.md` with sections:
- Current quarter scores (table)
- Quarter-over-quarter change
- Risk flags
- Recommended actions (if below threshold)
