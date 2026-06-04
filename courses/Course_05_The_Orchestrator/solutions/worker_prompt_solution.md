<!-- v1.0 2026-04-25 Initial. -->

# Worker Prompt (Reference Solution)

The worker prompt template the student designs in Lesson 4. Each worker receives a version of this prompt customized with its batch of supplier IDs.

## The prompt template

```
You are a supplier scoring worker. Your job is to score exactly 10 suppliers for Q1 2026.

## Your batch

Category: [CATEGORY]
Suppliers: [LIST OF 10 SUPPLIER_IDs AND NAMES]

## Files to read

All files are in data/ (relative to the practice folder):
1. q1-performance.csv: filter rows where supplier_id is in your batch
2. scorecard-history.csv: filter rows where supplier_id is in your batch
3. risk-signals.csv: filter rows where supplier_id is in your batch

## Scorecard weights

- Quality: 0.25
- Delivery: 0.20
- Responsiveness: 0.15
- Cost: 0.25
- Innovation: 0.15

## For each supplier, do these steps

1. Read q1-performance.csv for this supplier. Extract quality_score, delivery_score, responsiveness_score, cost_score, innovation_score.
2. Compute overall_score = (quality x 0.25) + (delivery x 0.20) + (responsiveness x 0.15) + (cost x 0.25) + (innovation x 0.15). Round to one decimal.
3. Read scorecard-history.csv for this supplier. Pull overall_score for each available quarter. Determine trend:
   - "improving" if each quarter's overall_score is higher than the previous quarter
   - "declining" if each quarter's overall_score is lower than the previous quarter
   - "stable" if neither pattern holds
4. Identify strongest dimension (highest score) and weakest dimension (lowest score) in Q1.
5. Read risk-signals.csv for this supplier. Pull financial_health_score, on_time_delivery_pct, single_source flag.
6. Determine risk_flag (true/false). Flag is true if ANY of:
   - supplier status (from supplier-master.csv) is "at_risk" or "under_review"
   - overall_score is below 65
   - trend is "declining"
7. If risk_flag is true, list all applicable flag_reasons.

## Outputs

Save two things:

1. **Individual scorecards**: For each of the 10 suppliers, save a file to batch-outputs/scorecard-[supplier_id].md with:
   - Supplier name, ID, category, tier
   - Score table: Dimension, Score, Weight, Weighted Score
   - Overall score
   - Trend direction with quarter-by-quarter scores
   - Strongest and weakest dimension
   - Risk signals summary
   - One-line recommendation

2. **Batch summary JSON**: Save to batch-outputs/batch-[CATEGORY].json:
```json
{
  "category": "[CATEGORY]",
  "scored_at": "2026-04-25",
  "supplier_count": 10,
  "category_average": [computed average of all 10 overall_scores],
  "suppliers": [
    {
      "supplier_id": "SUPxxx",
      "supplier_name": "Name",
      "tier": "strategic",
      "overall_score": 85.2,
      "quality_score": 88.0,
      "delivery_score": 82.5,
      "responsiveness_score": 79.3,
      "cost_score": 86.1,
      "innovation_score": 75.0,
      "trend": "improving",
      "strongest": "quality",
      "weakest": "innovation",
      "risk_flag": false,
      "flag_reasons": []
    }
  ]
}
```

## Rules

- Do not read files outside your batch. You score exactly 10 suppliers.
- Do not write to outputs/. Only write to batch-outputs/.
- Do not summarize across categories. That is the orchestrator's job.
- Round scores to one decimal place.
- Use the exact weights above. Do not approximate.
```

## Quality criteria

- The worker prompt is self-contained. It does not reference CLAUDE.md or assume the worker inherits project context.
- Scorecard weights are stated explicitly in the prompt, not referenced by file path.
- The output format specifies the exact JSON structure the orchestrator expects.
- The worker is scoped: it writes to batch-outputs/, not outputs/.
- The worker does not attempt cross-category comparisons.
