<!-- v1.0 2026-04-25 Initial. -->

# Self-Correcting Feedback Loop (Reference Solution)

The validation pattern that checks sub-agent outputs and re-runs them if they fail quality checks.

## The validation logic

Add this to the orchestrator prompt after each sub-agent returns:

```
After each sub-agent returns its category summary, validate it against these
three checks:

1. SUPPLIER CHECK: Does the summary name at least one real supplier from the
   data? Search for any supplier name that appears in supplier-scorecards.csv.
   If no supplier is named, the check fails.

2. DOLLAR CHECK: Does the summary include at least one dollar figure? Search
   for a "$" character followed by digits. If no dollar figure appears, the
   check fails.

3. DATE CHECK: Does the summary include at least one date in YYYY-MM-DD
   format? Search for a pattern like "2026-" followed by digits. If no date
   appears, the check fails.

If any check fails:
- Log which check failed and for which category.
- Re-run the sub-agent with an additional instruction: "Your previous output
  was missing [supplier name / dollar figure / date]. Include it this time."
- Validate the new output against the same three checks.

If the sub-agent fails the same check three times in a row:
- Stop retrying.
- Include this line in the category section of the final briefing:
  "[CATEGORY] summary incomplete. Manual review needed. Missing: [list of
  failed checks]."

Track the retry count per sub-agent. Report total retries at the end of the
briefing in a "System notes" section.
```

## What the feedback loop catches

Common sub-agent failures and how the loop corrects them:

| Failure | Detection | Correction |
|---|---|---|
| Summary says "the supplier" without naming it | Supplier check fails | Re-run with "name the specific supplier" |
| Summary says "spend increased significantly" without a number | Dollar check fails | Re-run with "include the dollar amount" |
| Summary says "contract expires next month" without a date | Date check fails | Re-run with "include the exact expiration date" |
| Summary is empty or malformed | All three checks fail | Re-run with full original instructions |

## System notes example

At the end of the consolidated briefing:

```
## System notes

- Total sub-agents dispatched: 6
- Sub-agents that passed on first attempt: 5
- Sub-agents that required retries: 1 (Logistics, retry 1: missing date)
- Total retries: 1
- Escalations to manual review: 0
```

This section gives you visibility into system reliability. If retries increase over time, the sub-agent prompts may need refinement.
