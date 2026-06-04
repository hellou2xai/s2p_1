# Contract Review Skill

Review a contract for completeness and upcoming deadlines.

## Input
- Contract ID
- Path to contract calendar CSV

## Steps
1. Read the contract calendar and find the specified contract.
2. Check if the contract expires within 90 days.
3. If auto-renewal is "yes", check if the notice period deadline has passed.
4. Calculate days until expiry and days until notice deadline.
5. Flag contracts expiring within 60 days without a renewal plan.

## Output format
Save to outputs/ as `contract-review-<contract_id>.md` with sections:
- Contract summary (supplier, category, dates, value)
- Timeline (days to expiry, days to notice deadline)
- Risk level (green, amber, red)
- Recommended action
