# /trigger-exit

Initiate the exit workflow for a supplier flagged for off-boarding.

## Inputs

- The supplier name (passed as an argument).
- `Master/supplier-master.csv`
- `Master/open-orders.csv`

## Steps

1. Find the supplier row in `Master/supplier-master.csv`. Confirm Lifecycle_Stage is `exit`.
2. Find every row in `Master/open-orders.csv` for the supplier where Status is not Closed or Cancelled. Sum the Amount_USD.
3. Build a seven-milestone transition timeline starting from today's date.
4. Draft a formal supplier exit notification letter listing every open PO and the deadlines.
5. Save the timeline and letter to `Outputs/exit-plans/<supplier-name>-exit-plan.md`.
6. Append a Decision_Log entry to `state/lifecycle-state.json` for that supplier.

## Output format

A markdown file with the supplier name, transition timeline table, exit letter, and a list of open POs with values and dates.
