<!-- v1.0 2026-04-25 Initial. -->

# /scorecard-refresh

Produce a one-page scorecard summary for a named supplier and quarter.

## Usage

/scorecard-refresh $ARGUMENTS

Parse $ARGUMENTS as: [supplier] [quarter]
- supplier: a supplier_id (e.g., SUP004) or a supplier name (e.g., "Apex Electronics")
- quarter: 2025-Q3, 2025-Q4, 2026-Q1, or 2026-Q2

If supplier is a name, look up the matching supplier_id in supplier-master.csv.

## Inputs

data/scorecard-history.csv
  Filter rows for the named supplier. Pull all available quarters.

data/supplier-master.csv
  Pull tier, risk_rating, category, city, state, contract_id, and status.

data/contract-register.csv
  If the supplier has a contract_id, pull contract end_date and status.

## Process

1. Look up the supplier in supplier-master.csv. Confirm the supplier_id exists.
2. Filter scorecard-history.csv for that supplier_id. Pull all quarters.
3. For the requested quarter, extract quality_score, delivery_score, responsiveness_score, cost_score, innovation_score, and overall_score.
4. Compute trend direction for overall_score across available quarters: improving (each quarter higher than the last), declining (each quarter lower), or stable.
5. Identify the strongest dimension (highest score) and weakest dimension (lowest score) for the requested quarter.
6. If the supplier has a contract, note the contract end_date and days remaining.

## Output format

Save to outputs/scorecard-[supplier_id]-[quarter]-[YYYY-MM-DD].md

Four sections:
1. **Supplier profile** (table): Supplier Name, ID, Category, Tier, Risk, Location, Contract Status.
2. **Scorecard for [quarter]** (table): Dimension, Score, vs Prior Quarter.
3. **Trend** (one paragraph): overall trend direction across quarters, strongest and weakest dimension, one recommendation.
4. **Contract note** (one line): contract end date and days remaining, or "no contract on file".

End with an audit footer.

## Quality criteria

- Scores match scorecard-history.csv exactly. No rounding or estimation.
- Trend direction is computed from actual quarter-over-quarter movement, not assumed.
- The recommendation names the weakest dimension and a specific action.
- If the supplier_id is not found, Claude Code prints an error and does not create a file.
