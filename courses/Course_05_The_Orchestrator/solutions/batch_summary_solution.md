<!-- v1.0 2026-04-25 Initial. -->

# Batch Summary JSON (Reference Solution)

The JSON structure each worker produces. The orchestrator reads these five files to build the portfolio summary.

## Example: batch-raw-materials.json

```json
{
  "category": "raw-materials",
  "scored_at": "2026-04-25",
  "supplier_count": 10,
  "category_average": 78.4,
  "suppliers": [
    {
      "supplier_id": "SUP001",
      "supplier_name": "Great Lakes Steel",
      "tier": "strategic",
      "overall_score": 86.2,
      "quality_score": 88.5,
      "delivery_score": 84.0,
      "responsiveness_score": 82.3,
      "cost_score": 87.1,
      "innovation_score": 79.8,
      "trend": "stable",
      "strongest": "quality",
      "weakest": "innovation",
      "risk_flag": false,
      "flag_reasons": []
    },
    {
      "supplier_id": "SUP004",
      "supplier_name": "Apex Electronics",
      "tier": "preferred",
      "overall_score": 58.7,
      "quality_score": 52.3,
      "delivery_score": 55.1,
      "responsiveness_score": 68.4,
      "cost_score": 62.0,
      "innovation_score": 60.5,
      "trend": "declining",
      "strongest": "responsiveness",
      "weakest": "quality",
      "risk_flag": true,
      "flag_reasons": ["at_risk status", "declining trend", "overall_score below 65"]
    }
  ]
}
```

## Design decisions

- **category_average at the top**: The orchestrator needs category averages for the summary table. Putting it at the top level saves the orchestrator from recalculating.
- **Individual scores included**: The orchestrator might need to identify the portfolio-wide highest and lowest scorers per dimension. Including all six dimension scores prevents re-reading individual scorecard files.
- **flag_reasons as an array**: Multiple reasons can apply. The orchestrator lists them in the flagged suppliers table.
- **Flat structure**: No nesting beyond the suppliers array. The orchestrator can parse this with a simple loop.

## Quality criteria

- category_average matches the mean of all 10 supplier overall_scores.
- Every supplier has exactly six dimension scores plus one overall_score.
- trend is computed from scorecard-history.csv, not assumed.
- flag_reasons is empty when risk_flag is false.
- The JSON is valid and parseable.
