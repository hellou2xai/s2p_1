# Summit Procurement Group: Shared Context

## Organization

Summit Procurement Group is a US-based procurement team with $124M in annual spend across six categories. Three offices: Chicago (IL), Dallas (TX), and Atlanta (GA). Eight analysts.

## Categories

| Category | Annual spend | Lead analyst | Office |
|---|---|---|---|
| IT services | $22.4M | Sarah Kim | Chicago |
| Raw materials | $24.8M | James Park | Chicago |
| MRO | $12.6M | Lisa Chen | Chicago |
| Logistics | $21.2M | Marcus Davis | Dallas |
| Facilities | $16.8M | Ana Torres | Dallas |
| Professional services | $14.4M | Kevin Wright | Dallas |

Cross-category support: Priya Sharma (supplier risk) and Tom Bradley (reporting), both in Atlanta.

## Output standards

- All currency in USD with commas.
- Dates in YYYY-MM-DD format.
- Short sentences. Active voice.
- No em-dashes or en-dashes.
- Every output that leaves the team must include a `[REVIEWED]` tag.
- Recommendations capped at three.
- Supplier names use legal entity names (e.g., "Great Lakes Steel Corp", not "the steel supplier").

## Scoring standards

Supplier scorecards use a 1 to 5 scale across four dimensions:
- Quality (weight: 30%)
- Delivery (weight: 25%)
- Cost (weight: 25%)
- Responsiveness (weight: 20%)

Overall score = weighted average. Below 3.0 = at risk. Below 2.5 = corrective action required.

## Audit rules

- Every Write and Bash tool call is logged to the audit trail.
- Audit logs are append-only. Never delete entries.
- Every significant output includes an audit reference ID.
