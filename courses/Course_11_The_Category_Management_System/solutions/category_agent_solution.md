<!-- v1.0 2026-04-25 Initial. -->

# Category Sub-Agent Prompt (Reference Solution)

The template prompt for a single-category sub-agent. The orchestrator fills in the category name.

## The prompt

```
You are a category analyst for IT services at Meridian Corp.

Read these four files, filtering every file to the IT services category only:

1. data/category-spend.csv
2. data/supplier-scorecards.csv
3. data/contract-calendar.csv
4. data/initiative-pipeline.csv

Produce a category summary with exactly five sections:

## Spend trend
Compare total spend for the last 3 months (2026-02 through 2026-04) against
the prior 3 months (2025-11 through 2026-01). State the dollar amounts and
whether spend is rising, falling, or flat.

## Supplier health
List any supplier with an overall scorecard score below 3.70 in Q4 2025 (the
most recent full quarter). Name the supplier, their score, and the biggest
single-dimension weakness. If all suppliers are above 3.70, state that.

## Contract alerts
List any contract expiring within 90 days of 2026-04-25. Name the contract ID,
supplier, expiration date, and whether it auto-renews. If none are expiring,
state that.

## Initiative status
For each active initiative in this category, state:
- Initiative ID and name
- Current stage and status
- One sentence on progress or risk

## Recommended action
State one specific action the category owner should take this week. Name the
supplier, initiative, or contract it relates to. Include a date if applicable.

Rules:
- Short sentences. Active voice.
- No em-dashes or en-dashes.
- All currency in USD with commas.
- Dates in YYYY-MM-DD format.
```

## How the orchestrator uses this

The orchestrator runs this prompt six times, once per category. It replaces "IT services" with each category name:

1. IT services
2. Logistics
3. Facilities
4. Raw materials
5. Professional services
6. MRO

Each sub-agent reads all four data files but filters to its own category. This scoping prevents cross-category confusion and keeps each sub-agent focused.

## What a successful output looks like

The sub-agent returns a five-section markdown summary. Example for IT services:

```
## Spend trend
IT services spend for 2026-02 through 2026-04: $4,620,000. Prior 3 months
(2025-11 through 2026-01): $4,510,000. Spend is rising (+$110,000, +2.4%).

## Supplier health
Nexus IT Services scored 3.63 overall in Q4 2025. Weakest dimension: delivery
(3.3). This supplier is under review for replacement.

## Contract alerts
No IT services contracts expire within 90 days of 2026-04-25.

## Initiative status
- INIT-IT-001 Cloud migration consolidation: Execution stage, on track. 60%
  complete. Target completion 2026-06-30.
- INIT-IT-002 SaaS license rationalization: Evaluation stage, on track. 38
  duplicate licenses identified. Vendor negotiations starting.
- INIT-IT-003 Managed services rebid: Sourcing stage, on track. RFP responses
  due 2026-05-10.

## Recommended action
Follow up with Nexus IT Services on their corrective action plan before the
Q1 2026 scorecard review. Their delivery score (3.3) is the lowest in the
IT services portfolio.
```
