<!-- v1.0 2026-04-25 Initial. -->

# /contract-sweep

Find every contract expiring within a given horizon and produce an action list.

## Usage

/contract-sweep $ARGUMENTS

Parse $ARGUMENTS as: [horizon-days]
- horizon-days: an integer (e.g., 90 means find contracts expiring within 90 days of today)

## Inputs

data/contract-register.csv
  All contracts. Compute days remaining from today (2026-04-25) to end_date.

data/supplier-master.csv
  Join on supplier_id for tier, risk_rating, and category.

## Process

1. Read contract-register.csv. Parse end_date for every row.
2. Compute days_remaining = end_date minus today. Negative means already expired.
3. Filter for contracts where days_remaining <= horizon-days.
4. For each contract, check auto_renew. If auto_renew is "yes" and today is past the notice window (end_date minus notice_period_days), flag as "auto-renew notice window passed".
5. Sort results: expired contracts first (by days_remaining ascending), then expiring_soon (by days_remaining ascending).
6. Join to supplier-master.csv for tier, risk_rating, and category.
7. Classify urgency: "Expired" (days_remaining < 0), "Critical" (days_remaining <= 30), "Action needed" (days_remaining <= 60), "Monitor" (days_remaining <= horizon-days).

## Output format

Save to outputs/contract-sweep-[horizon]-days-[YYYY-MM-DD].md

Three sections:
1. **Summary** (one paragraph): total contracts found, breakdown by urgency tier, total annual value at risk.
2. **Contract action list** (table): Contract ID, Supplier, Category, Tier, End Date, Days Left, Annual Value (USD), Auto-Renew, Notice Window, Urgency, Recommended Action.
3. **Top three actions** (numbered list): the three highest-priority actions, each naming the contract, the supplier, and a specific deadline.

End with an audit footer.

## Quality criteria

- Days remaining is computed from today (2026-04-25), not estimated.
- Auto-renew notice window logic is correct: if auto_renew is "yes" and today > (end_date - notice_period_days), the notice window has passed.
- Urgency classification uses the exact thresholds above.
- Top three actions are ordered by urgency, then by annual_value_usd descending.
