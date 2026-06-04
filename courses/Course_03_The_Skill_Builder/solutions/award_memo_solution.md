# Solution: award-memo skill

Reference answer for Lesson 5. About 60 lines. The skill that ties the chain together.

## The reference content

Save at `practice/skills/award-memo.md`.

```
<!-- v1.0 2026-04-25 Initial. -->

# award-memo

## What this skill does

Produces a one-page award recommendation memo, drawing on the bid
comparison, the risk profile, and the savings case. Use as the final
step of any sourcing event before the panel meeting. Reads four input
files and synthesises them into a single page the panel can act on.

## Inputs

outputs/bid-comparison.md (from bid-scorer; the score table and commentary).
outputs/risk-profile.md (from risk-profiler; per-bidder risk paragraphs).
outputs/savings-case.md (from savings-calculator; headline, calculation,
sensitivity).
inputs/category-brief.md (the goal, scope, stakeholders, and savings target).
templates/award-memo-template.md (the skeleton structure).

## Process

1. Read all four input files. Build a single mental model of the bid
   landscape, the risks, and the savings.
2. Draft the recommendation. Must name a four-carrier panel: one road FTL,
   one road LTL or pallet, one sea FCL, one air. Use the top-scored bidder
   in each lane category from bid-comparison.md unless risk-profile.md
   names a critical risk that disqualifies them.
3. For each recommended carrier: name the contract value (from
   bid-comparison.md or the source bid response), the key strength
   (one phrase), and the mitigation for the highest risk (from
   risk-profile.md).
4. Pull the bid comparison summary: top 3 by total weighted score.
5. Pull three named risks from risk-profile.md. Name the mitigation
   owner for each.
6. Pull the savings case headline and the sensitivity from
   savings-case.md. Quote the savings figure verbatim (do not recompute).
7. Construct the process and decisions paragraph (80 words) naming the
   evaluators (from category-brief.md stakeholders), the dates, and the
   source documents.
8. Build the audit footer.

## Output format

Save outputs/award-memo.md.

Six sections in order:
- Recommendation (50 to 80 words).
- Bid comparison summary (top 3 bidders, one line each).
- Risks and mitigations (three named risks with mitigation owner).
- Savings case (one paragraph plus a one-row table: Baseline, Proposed,
  Savings, % of target).
- Process and decisions (80 words).
- Audit footer (Generated, Source files, Model, Operator, Output path).

Cap body at 500 words excluding audit footer.

## Quality criteria

- Recommendation names a four-carrier panel covering all four required
  modes (road FTL, road LTL or pallet, sea FCL, air).
- Every recommended carrier has a contract value drawn from
  bid-comparison.md or savings-case.md.
- Three risks named, each with a mitigation owner. No more than three.
- Savings figure quoted matches the headline in savings-case.md (do
  not recompute; quote).
- Audit footer is present with all five lines.
- Total length is 4 to 5 paragraphs of body plus the table plus the
  footer.
```

## Why this works

- The skill produces ONE deliverable (award-memo.md). Other skills produce one deliverable each. Each step is a small contract.
- The recommendation format (four-carrier panel) is fixed in the skill, so the panel structure does not drift between sourcing events.
- "Quote the savings figure, do not recompute" is the rule that keeps the chain consistent. If award-memo recomputed savings, two outputs would say different numbers.

## How it composes with the other skills

Award-memo reads three other skills' outputs. Each one is a stable contract:

- bid-comparison.md has the score table and commentary.
- risk-profile.md has one paragraph per bidder.
- savings-case.md has the headline and sensitivity.

If you change the shape of any of those outputs (e.g., bid-comparison.md drops the commentary section), award-memo breaks. That is why Lesson 6 (versioning) matters: contracts are upheld by discipline.
