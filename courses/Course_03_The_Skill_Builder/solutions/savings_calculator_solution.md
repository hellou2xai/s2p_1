# Solution: savings-calculator skill

Reference answer for Lesson 5 and Lesson 6. About 50 lines.

## The reference content (v1.0)

Save at `practice/skills/savings-calculator.md`.

```
<!-- v1.0 2026-04-25 Initial. -->

# savings-calculator

## What this skill does

Computes the annualised savings against the baseline if a named bidder
or panel were awarded the contract. Use once you have a recommended
panel from bid-scorer plus baseline data.

## Inputs

inputs/spend-baseline.csv
  Columns: shipment_id, carrier_id, mode, from_location, to_location,
  total_gbp, ship_date. Around 1,500 rows of historical shipments.

outputs/bid-comparison.md (to read each bid's annual value).

inputs/category-brief.md (to read the savings target).

## Process

1. Sum total_gbp from spend-baseline.csv across the last 12 months.
   This is the baseline.
2. Read the bid comparison for each bid's annual value.
3. For the recommended panel (top three from bid-scorer plus the air
   winner if separate), sum their annual values. This is the proposed
   spend.
4. Compute annualised savings = baseline minus proposed spend.
5. Compute saving percentage = savings / baseline.
6. Compare against the savings target named in the category brief.
7. Note any one-off implementation costs from the bids; subtract from
   Year 1 savings to produce risk-adjusted Year 1 savings.

## Output format

Save outputs/savings-case.md. Three sections:

- Headline (one paragraph, 50 words): baseline figure, proposed figure,
  savings figure (GBP and %), comparison against target.
- Calculation (small table: Baseline, Proposed, Savings, Year 1
  implementation, Year 1 risk-adjusted savings, Year 2+ run-rate savings).
- Sensitivity (one paragraph, 80 words): named bidder substitutions and
  the savings impact of each.

Cap at 400 words excluding the table.

## Quality criteria

- Baseline figure is computed from spend-baseline.csv (sum of total_gbp).
  Show row count used.
- Every figure has a source named.
- Savings percentage is computed, not invented.
- Headline names whether the savings target is met, narrowly missed,
  or exceeded.
```

## v1.1 (Lesson 6) - tighter soft-savings rule

After Lesson 6, the skill is updated. Add the version comment at top:

```
<!-- v1.1 2026-06-30 Tightened soft-savings rule per CFO request 2026-06-25.
     Soft savings now go in a supplemental section, not the headline. -->
```

And add a Process step:

```
3a. Soft savings (avoided cost, productivity gains, supplier rebate
projections, etc.) MUST NOT appear in the headline savings figure.
Soft savings appear only in a separate "Soft savings, supplemental"
paragraph at the bottom of the savings case. The headline figure
contains hard savings only (negotiated unit rate reductions against
the baseline spend computed from spend-baseline.csv).
```

Update the Output format section:

```
- Soft savings, supplemental (optional, one paragraph, 100 words max):
  any soft savings claimed, with the methodology stated. Not included
  in headline.
```

And one quality criterion:

```
- Soft savings, if any, appear ONLY in the supplemental paragraph,
  never in the headline figure.
```
