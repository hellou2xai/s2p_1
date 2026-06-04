<!-- v1.0 2026-04-25 Initial. -->

# /rfp-launch

Generate a sourcing brief for a named category by chaining spend and contract data.

## Usage

/rfp-launch $ARGUMENTS

Parse $ARGUMENTS as: [category] [deadline]
- category: direct-materials, logistics, indirect, or mro
- deadline: a date in YYYY-MM-DD format (the RFP close date)

## Inputs

data/spend-transactions.csv
  Filter to the named category. Sum by supplier for the last 12 months.

data/supplier-master.csv
  Filter to the named category. Pull tier, risk_rating, and status.

data/contract-register.csv
  Filter to contracts linked to suppliers in the named category.
  Identify expiring and expired contracts.

## Process

1. Read spend-transactions.csv. Filter to the named category over the last 12 months.
2. Sum total category spend. Group by supplier, sorted descending.
3. Read supplier-master.csv. Filter to the named category. Count suppliers by tier.
4. Read contract-register.csv. Find contracts linked to category suppliers. Flag expired and expiring_soon.
5. Compute a timeline: today to deadline, minus standard milestones (RFP issue = today + 7 days, Q&A close = deadline minus 14 days, bid close = deadline, evaluation = deadline + 7 days, award = deadline + 14 days).
6. Identify the top 5 suppliers by spend as the likely incumbent panel.
7. Identify any at_risk or under_review suppliers as risk flags.
8. Draft a one-page sourcing brief with all sections below.

## Output format

Save to outputs/rfp-brief-[category]-[YYYY-MM-DD].md

Six sections:
1. **Category overview** (one paragraph): category name, total 12-month spend, number of active suppliers, tier distribution.
2. **Top 5 suppliers by spend** (table): Rank, Supplier, Tier, 12-Month Spend (USD), % of Category, Contract Status.
3. **Contract status** (one paragraph): how many contracts are active, expiring, or expired in this category.
4. **Risk flags** (bullet list): suppliers with at_risk or under_review status, declining scorecard trends, or expired contracts.
5. **Proposed timeline** (table): Milestone, Date.
6. **Recommendation** (one paragraph): whether to proceed with the RFP, suggested scope, and one key risk to address.

End with an audit footer.

## Quality criteria

- All spend figures trace to spend-transactions.csv for the last 12 months only.
- Timeline milestones are computed from the deadline argument, not hardcoded.
- Risk flags name specific suppliers and specific reasons.
- The recommendation paragraph names at least one supplier and one dollar figure.
