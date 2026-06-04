# Daily Check

Run a quick status check across all categories.

## What this command does
1. Read program-state.json for current risk flags.
2. Check contract-calendar.csv for contracts expiring within 30 days.
3. Check initiative-pipeline.csv for initiatives with status "at_risk" or "behind_schedule".
4. Produce a one-page summary with three sections: risk flags, expiring contracts, and troubled initiatives.

## Output
Save to outputs/ as `daily-check-YYYY-MM-DD.md`.
