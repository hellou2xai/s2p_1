# Solution: risk-profiler skill

Reference answer for Lesson 5. About 45 lines.

## The reference content

Save at `practice/skills/risk-profiler.md`.

```
<!-- v1.0 2026-04-25 Initial. -->

# risk-profiler

## What this skill does

Produces a risk profile per bidder, drawing on the longlist data and the
bid response. Use after bid-scorer has run; the output feeds into the
award memo as the risks section.

## Inputs

bid-responses/*.md
  Each file's contract terms section drives commercial risk. Implementation
  cost drives operational risk start-up exposure.

inputs/supplier-longlist.csv
  Columns: carrier_id, carrier_name, modes, primary_geography,
  certifications, capacity_tier, financial_health, otd_pct_12m,
  contract_terms_offered, incumbent. The financial_health column drives
  financial risk. The capacity_tier column adjusts operational risk.

outputs/bid-comparison.md (from bid-scorer).

## Process

1. List bidders in bid-responses/.
2. For each bidder, look up financial_health, capacity_tier, incumbent
   from the longlist (keyed by carrier_id from filename).
3. Score Financial risk 1-5 (5 = highest):
   - financial_health = strong: 1.
   - financial_health = stable: 2-3 (closer to 3 if non-incumbent).
   - financial_health = weak: 4-5.
4. Score Operational risk 1-5:
   - capacity_tier = tier_1 + incumbent: 1.
   - capacity_tier = tier_1 not incumbent: 2.
   - capacity_tier = tier_2: 3.
   - capacity_tier = tier_3: 4-5.
5. Score Commercial risk 1-5:
   - Term + extension covers contract life: 1-2.
   - Term shorter than scope requires: 3.
   - Indexation tied to fuel or HGV index: +1.
   - Implementation cost over 2% of annual: +1.
6. Total = sum (3-15).
7. One paragraph per bidder (60-100 words):
   - Name the highest-risk dimension.
   - Name a specific mitigation tied to that dimension (e.g., performance-based fee, parallel awarding).

## Output format

Save outputs/risk-profile.md.

One section per bidder:
- Title: Bidder name. Total risk: N/15. Key risk: <dimension>.
- One paragraph (60-100 words).

Cap file at 800 words.

## Quality criteria

- Every bidder in bid-responses/ has a section.
- Every total risk score is 3-15 (sum of three 1-5 scores).
- Each section names a specific mitigation, not a generic phrase.
- No invented data; every claim traces to longlist or bid response.
```

## Why this works

- Three risk dimensions (financial, operational, commercial) are stable across categories. Direct materials would use the same three with different inputs.
- Numeric scoring (1-5) keeps scores comparable.
- Mitigation must be specific (named in the bid or sourceable from the longlist), not generic.
