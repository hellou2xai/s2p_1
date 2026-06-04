<!-- v1.0 2026-04-25 Initial. -->

# Orchestrator Prompt (Reference Solution)

The orchestrator prompt the student writes in Lesson 3. This is the full prompt that reads the supplier master, divides into batches, and spawns worker agents.

## The prompt

```
Read data/supplier-master.csv. Group the 50 suppliers by category. There are five categories, each with 10 suppliers.

For each category, launch a background sub-agent with this task:

"You are a supplier scoring worker. Score these 10 suppliers for Q1 2026.

Suppliers to score: [list the 10 supplier_ids and names for this batch]

Read these files in practice/data/:
1. q1-performance.csv - filter to your 10 supplier_ids
2. scorecard-history.csv - filter to your 10 supplier_ids for trend analysis
3. risk-signals.csv - filter to your 10 supplier_ids

Scorecard weights:
- Quality: 25%
- Delivery: 20%
- Responsiveness: 15%
- Cost: 25%
- Innovation: 15%

For each supplier:
1. Compute overall_score = (quality x 0.25) + (delivery x 0.20) + (responsiveness x 0.15) + (cost x 0.25) + (innovation x 0.15). Round to one decimal.
2. Determine trend direction from scorecard-history.csv: improving (each quarter higher), declining (each quarter lower), or stable.
3. Identify strongest dimension (highest score) and weakest dimension (lowest score).
4. Pull risk signals: financial_health_score, on_time_delivery_pct, single_source flag.
5. Flag if: status is at_risk or under_review, overall_score below 65, or trend is declining.

Save two outputs:
1. Individual scorecards: one .md file per supplier in batch-outputs/ named scorecard-[supplier_id].md
2. Batch summary: one JSON file in batch-outputs/ named batch-[category].json with this structure:

{
  \"category\": \"[category name]\",
  \"scored_at\": \"2026-04-25\",
  \"supplier_count\": 10,
  \"category_average\": [number],
  \"suppliers\": [
    {
      \"supplier_id\": \"SUPxxx\",
      \"supplier_name\": \"Name\",
      \"tier\": \"strategic|preferred|approved\",
      \"overall_score\": 85.2,
      \"trend\": \"improving|declining|stable\",
      \"strongest\": \"quality\",
      \"weakest\": \"innovation\",
      \"risk_flag\": true|false,
      \"flag_reasons\": [\"at_risk status\", \"declining trend\"]
    }
  ]
}
"

After all five workers complete, read the five batch-[category].json files from batch-outputs/. Aggregate into a portfolio summary saved to outputs/portfolio-summary-2026-Q1-2026-04-25.md with these sections:

1. Portfolio overview: total suppliers scored, overall portfolio average, count by tier, count flagged.
2. Category averages table: Category, Supplier Count, Average Score, Highest Scorer, Lowest Scorer.
3. Top 10 suppliers by overall score (table): Rank, Supplier, Category, Tier, Score, Trend.
4. Flagged suppliers (table): Supplier, Category, Score, Flag Reasons, Recommended Action.
5. Trend analysis: count improving, declining, stable. Name the three most improved and three most declined.

End with an audit footer.
```

## Quality criteria

- The orchestrator divides by category, not arbitrarily. Each batch is one category.
- Worker prompts include the exact scorecard weights, not a reference to "see CLAUDE.md".
- Workers save to batch-outputs/, not outputs/.
- The orchestrator reads batch JSON files, not individual scorecard files.
- The portfolio summary totals match the sum of individual batch results.
