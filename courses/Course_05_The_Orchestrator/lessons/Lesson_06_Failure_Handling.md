# Failure Handling: Detecting Malformed Output and Recovering

It is Thursday at 09:00. You ran the full orchestrator last night. Four workers completed correctly. The fifth, logistics, returned a JSON file that is missing its closing bracket. The orchestrator tried to aggregate, read the broken file, and produced a portfolio summary with only 40 suppliers. Your VP is reviewing the summary right now. She will notice that Continental Freight and Patriot Logistics are missing from the top 10. You need a way to catch this before it reaches her inbox.

## The S2P problem

When you run five parallel workers, any one of them can fail. A worker might produce invalid JSON, miss a supplier, miscalculate a weighted score, or not finish at all. If the orchestrator blindly aggregates whatever it finds in `batch-outputs/`, garbage goes into the portfolio summary. A single malformed batch file can make the entire quarterly report wrong. The fix is validation before aggregation.

## What Claude Code does for you

You add validation checks to the orchestrator prompt. After all workers complete, the orchestrator inspects each batch-summary JSON file before using it. If a file fails validation, the orchestrator re-launches the worker for that specific category with the exact error message. If two retries fail, the orchestrator saves an error log and continues with the categories that passed. The portfolio summary notes which categories are missing.

## Set up

1. You have completed Lessons 4 and 5. All five workers have run at least once.
2. The `batch-outputs/` folder contains five JSON files and 50 scorecard files.
3. You will intentionally corrupt one file to test the validation logic.

## Step by step

### Step 1. Write the validation checks

Add this block to your orchestrator prompt, after the "wait for all workers" instruction and before the aggregation step.

```
## Validation (run before aggregation)

For each category in [raw-materials, logistics, it-services, facilities, professional-services]:

1. File exists: check that batch-[category].json is present in batch-outputs/. If missing, the worker did not complete.

2. Valid JSON: parse the file. If parsing fails, the file is malformed.

3. Supplier count: the "supplier_count" field must equal 10, and the "suppliers" array must contain exactly 10 objects.

4. Score ranges: every overall_score, quality_score, delivery_score, responsiveness_score, cost_score, and innovation_score must be between 0 and 100.

5. Weighted score consistency: for each supplier, recompute overall_score from (quality x 0.25) + (delivery x 0.20) + (responsiveness x 0.15) + (cost x 0.25) + (innovation x 0.15). If the recomputed value differs from the stated overall_score by more than 0.5, flag a calculation error.

6. Trend validity: the "trend" field must be one of "improving", "declining", or "stable".

7. Flag consistency: if risk_flag is true, flag_reasons must be a non-empty array. If risk_flag is false, flag_reasons must be an empty array.

If all seven checks pass, mark this category as validated.
If any check fails, log the specific error and the category name.
```

You should see seven numbered checks. Each check tests one specific thing. The orchestrator can report exactly which check failed and for which category.

### Step 2. Write the retry pattern

Tell the orchestrator what to do when a validation check fails.

```
## Recovery

If a category fails validation:

1. Re-launch the worker for that category. Include the specific error in the re-launch prompt.
   Example: "Your previous output for logistics failed validation. Error: supplier_count is 9, expected 10. SUP017 Prairie Express is missing. Re-score all 10 logistics suppliers and produce a corrected batch-logistics.json."

2. After the retry worker completes, run all seven validation checks again on the new file.

3. Maximum retries per category: 2. If a category still fails after 2 retries, save the error details to outputs/scoring-errors-2026-Q1.md and continue with the remaining validated categories.

4. Never re-launch a worker with a generic "try again" instruction. Always include the specific error: which check failed, what value was found, what value was expected.
```

You should see a three-step pattern: re-launch with error details, validate again, and stop after two retries. The key rule is specificity. A generic "try again" gives the worker no information about what went wrong.

### Step 3. Write the partial-portfolio logic

Tell the orchestrator how to handle a portfolio summary when one or more categories failed all retries.

```
## Partial portfolio handling

If one or more categories failed validation after 2 retries:
- Aggregate only the validated categories.
- In the portfolio overview section, state: "This summary covers [N] of 50 suppliers. [Category name] failed validation and is excluded. See outputs/scoring-errors-2026-Q1.md for details."
- Adjust all counts and averages to reflect only the included suppliers.
- Do not leave a gap in the top 10 table. Rank only the suppliers you have.
```

You should see explicit instructions for partial output. The orchestrator does not silently drop a category. It names the missing category and points to the error log.

### Step 4. Simulate a failure

Open `batch-outputs/batch-logistics.json` in a text editor. Delete the last closing bracket `}` so the JSON is invalid. Save the file.

```
Open batch-outputs/batch-logistics.json. Delete the final closing brace so the file ends with ] instead of ]}.
```

You should see a file that ends abruptly without the closing `}`. This is a common failure mode: truncated output from a worker that ran out of context or was interrupted.

### Step 5. Run the orchestrator with validation

Run the orchestrator prompt that includes the validation block from Step 1 and the recovery block from Step 2.

```
Read the five batch-summary JSON files from batch-outputs/. Before aggregating, run the seven validation checks on each file. If any file fails, re-launch the worker for that category with the specific error. Maximum 2 retries. Then aggregate validated files and save the portfolio summary to outputs/portfolio-summary-2026-Q1-2026-04-25.md.
```

You should see the orchestrator report that `batch-logistics.json` failed the "Valid JSON" check. It should re-launch the logistics worker with a message like "Your previous output was not valid JSON. The file is missing its closing brace. Re-score all 10 logistics suppliers and produce a corrected batch-logistics.json." After the retry, the orchestrator validates the new file, passes all checks, and proceeds to aggregation.

## Worked example: the full failure and recovery cycle

Here is what the orchestrator output looks like when it catches a malformed file.

```
Validation results:
- raw-materials: PASSED (7/7 checks)
- logistics: FAILED (check 2: invalid JSON, unexpected end of input)
- it-services: PASSED (7/7 checks)
- facilities: PASSED (7/7 checks)
- professional-services: PASSED (7/7 checks)

Re-launching logistics worker (attempt 1 of 2)...
Task: "Your previous output for logistics failed validation. Error: invalid JSON. The file is missing its closing brace. Re-score all 10 logistics suppliers (SUP011 through SUP020) and produce a corrected batch-logistics.json in batch-outputs/."

Logistics worker completed. Re-validating...
- logistics: PASSED (7/7 checks)

All 5 categories validated. Proceeding to aggregation.
```

After aggregation, open `outputs/portfolio-summary-2026-Q1-2026-04-25.md`. Confirm all 50 suppliers are present, the logistics category average is included, and the trend counts sum to 50. Then restore the original `batch-logistics.json` by re-running the logistics worker or using the regeneration script.

## Common mistakes and how to recover

**No validation at all.** If the orchestrator skips validation and goes straight to aggregation, a malformed JSON file causes a parse error or, worse, silently produces wrong numbers. Symptom: the portfolio summary has fewer than 50 suppliers, or a category average is `null`. Fix: add the seven validation checks from Step 1 to your orchestrator prompt.

**Generic "try again" re-launches.** If the retry prompt says "the logistics batch failed, please try again," the worker has no idea what went wrong. It might produce the same error. Symptom: the retry fails with the same issue. Fix: include the specific check that failed, the value that was found, and the value that was expected.

**No retry limit.** If the orchestrator keeps retrying forever, a persistent error creates an infinite loop of sub-agent launches. Each launch consumes tokens and time. Symptom: the orchestrator runs for 20 minutes and produces dozens of failed attempts. Fix: cap retries at 2 per category. After 2 failures, log the error and move on.

**Silently dropping failed categories.** If the orchestrator skips a failed category without noting it in the portfolio summary, the VP sees a report for 40 suppliers and assumes it covers all 50. Symptom: the portfolio overview says "50 suppliers scored" but only 40 appear in the tables. Fix: use the partial-portfolio logic from Step 3. State which categories are excluded and why.

**Not checking weighted score consistency.** A worker might state an overall score of 85.2 but the dimension scores do not add up to 85.2 when weighted. This is a calculation error, not a format error. It passes the JSON and count checks but produces wrong rankings. Fix: include check 5 (recompute the weighted score and compare). A tolerance of 0.5 accounts for rounding.
