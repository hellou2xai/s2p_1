<!-- v1.0 2026-04-25 Initial. -->

# Failure Handling (Reference Solution)

The validation and recovery logic the orchestrator uses when a worker returns malformed or incomplete output.

## Validation checks on each batch-summary JSON

1. **File exists.** If batch-[category].json is missing from batch-outputs/, the worker did not complete. Re-invoke the worker for that category.

2. **Valid JSON.** If the file is not valid JSON, the worker produced malformed output. Re-invoke with explicit instruction: "Your previous output was not valid JSON. Write valid JSON only."

3. **Correct supplier count.** supplier_count must equal 10. If fewer, the worker missed suppliers. Re-invoke with the missing supplier_ids listed explicitly.

4. **Score range.** Every overall_score, quality_score, delivery_score, responsiveness_score, cost_score, and innovation_score must be between 0 and 100. If any score is outside this range, flag the supplier for re-scoring.

5. **Weighted score consistency.** Recompute overall_score from the six dimension scores and weights. If the recomputed value differs from the stated overall_score by more than 0.5, the worker made a calculation error. Re-invoke for that supplier only.

6. **Trend validity.** trend must be one of "improving", "declining", or "stable". Any other value is malformed.

7. **Flag consistency.** If risk_flag is true, flag_reasons must be non-empty. If risk_flag is false, flag_reasons must be empty.

## Recovery pattern

```
After all workers complete:

1. For each category in [raw-materials, logistics, it-services, facilities, professional-services]:
   a. Check if batch-[category].json exists in batch-outputs/.
   b. If missing: re-launch the worker for that category. Wait for completion.
   c. If present: parse the JSON.
      - If parse fails: re-launch the worker with "output valid JSON" instruction.
      - If parse succeeds: validate supplier_count, score ranges, weighted consistency, trend values, and flag consistency.
      - If any validation fails: log the specific error. Re-launch the worker for that category with the error details.
   d. Maximum retries per category: 2. After 2 failed retries, write the category to outputs/scoring-errors.md with the error details and continue with the remaining categories.

2. Aggregate only the validated batch summaries.
3. In the portfolio summary, note any categories that failed validation in a "Data quality notes" section.
```

## Quality criteria

- The orchestrator never proceeds with unvalidated data.
- Re-invocation prompts include the specific error, not a generic "try again".
- Maximum retry count prevents infinite loops.
- Failed categories are documented, not silently dropped.
- The portfolio summary accurately reflects which categories were included.
