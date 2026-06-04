# /lifecycle-status

Produce a full portfolio status report covering every supplier in `Master/supplier-master.csv`.

## Steps

1. Read `state/lifecycle-state.json` if it exists. That is the current truth for stages and decisions.
2. Read `Master/supplier-master.csv`, `Master/performance-history.csv`, `Master/compliance-status.csv`, and `Master/development-plans.csv`.
3. Apply the rules in `skills/assess-lifecycle-stage.md` to confirm or correct the stage on every supplier.
4. Group suppliers by stage. Report a count per stage.
5. List every supplier with a Decision_Status of `Deferred` or `CAP Issued` from the state file.
6. Save the full report to `Outputs/segmentation-report.md`.

## Output format

A markdown report with these sections:
- Header: today's date, total suppliers, total annual spend.
- Stage distribution table: Stage, Count, Total Spend.
- Per-stage supplier lists.
- Open decisions section (Deferred and CAP Issued).
- Recommendations: at most three.
