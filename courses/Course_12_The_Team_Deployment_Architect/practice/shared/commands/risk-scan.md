# Risk Scan

Scan all suppliers for risk indicators.

## What this command does
1. Read supplier scorecards. Flag any supplier with overall score below 3.0.
2. Read contract calendar. Flag any contract expiring within 60 days without a renewal plan.
3. Read initiative pipeline. Flag any initiative behind schedule with more than $200,000 at risk.
4. Produce a risk summary sorted by severity (critical, high, medium).

## Output
Save to outputs/ as `risk-scan-YYYY-MM-DD.md`.
