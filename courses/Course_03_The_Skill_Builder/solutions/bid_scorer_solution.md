# Solution: bid-scorer skill

Reference answer for Lesson 4. About 80 lines.

## The reference content

Save at `practice/skills/bid-scorer.md`.

```
<!-- v1.0 2026-04-25 Initial. -->

# bid-scorer

## What this skill does

Scores every bid response in a folder using a fixed weighted criteria set,
then ranks them. Use this skill once after all bids are received and the
bid-responses folder is complete. Produces a single comparison table with
weighted scores plus a one-paragraph commentary per bid.

## Inputs

bid-responses/*.md
  Multiple bid response files, one per bidder. Each follows the same
  six-section structure: Executive summary, Capability statement,
  Pricing table, Service commitments, Contract terms, References.
  The pricing table has columns: Lane, Mode, Volume per year, Unit rate
  (GBP per shipment), Annual value (GBP).

inputs/supplier-longlist.csv
  Used to look up the carrier_id from the bid filename and pull
  background data: capacity_tier, financial_health, otd_pct_12m,
  incumbent. Columns: carrier_id, carrier_name, modes, primary_geography,
  certifications, capacity_tier, financial_health, otd_pct_12m,
  contract_terms_offered, incumbent.

templates/scorecard-template.md
  Skeleton with eight columns. Use as the structure for the output table.

## Process

1. List every file in bid-responses/. Extract carrier_id from filename
   (BID_CARxxx prefix).

2. For each bid, score five criteria 0-100 before weighting:

3. Price (40%):
   - Sum Annual value (GBP) from the pricing table.
   - Lowest total = 100. Highest total = 60. Linear interpolation.
   - Subtract (implementation/total) percentage points, capped at 10.

4. Service (25%):
   - On-time delivery 95%+ = 90-100. 92-95% = 75-89. <92% = 60-74.
   - Subtract 5 per 1% damage rate above 1%.
   - Subtract 3 per 1% invoice accuracy below 99%.

5. Capability (20%):
   - In-scope modes 4+ = 90-100. 2-3 = 75-89. 1 = 60-74.
   - capacity_tier: tier_1 +5, tier_2 0, tier_3 -5.
   - financial_health: strong +5, stable 0, weak -10.

6. Sustainability (10%):
   - SBT-aligned + carbon-neutral verified = 90-100.
   - Carbon-neutral committed only = 75-89.
   - No specific commitments = 60-74.

7. Implementation (5%):
   - Implementation cost 0 = 90-100.
   - Up to 1% of annual = 75-89.
   - Over 1% = 60-74.

8. Total = (Price*0.40) + (Service*0.25) + (Capability*0.20)
   + (Sus*0.10) + (Impl*0.05).

9. Sort descending by Total. Top three Recommended = "Yes". Rest "No".

10. One-paragraph commentary per bidder (50-80 words): strongest
    score, weakest score, decision-relevant trade-off.

## Output format

Save outputs/bid-comparison.md.

Structure:
- Title: Bid comparison - <category name from category-brief.md>.
- Section 1: Comparison table. Eight columns matching scorecard-template.md.
  Sorted descending by Total.
- Section 2: Commentary. One paragraph per bidder, in score order.
- Section 3: Top three summary. Three bullet points.

Cap at 600 words excluding the table.

Audit footer: Generated, Source files, Model, Operator, Output path.

## Quality criteria

- Every bidder in bid-responses/ appears as a row.
- Every score is between 60 and 100.
- Weighted total = (P*0.40 + S*0.25 + C*0.20 + Sus*0.10 + I*0.05),
  rounded to 1 decimal.
- Top three are flagged Recommended = "Yes".
- Each commentary names the strongest and weakest score.
- Audit footer present with all five lines.
```

## Why this works

- The scoring bands are numeric and explicit. Two analysts running the same skill on the same bids get the same rank order.
- The capability score uses the longlist data, so it accounts for context the bid response itself does not contain (incumbent status, financial health).
- The quality criteria include "every bidder appears", which prevents silent drops.
