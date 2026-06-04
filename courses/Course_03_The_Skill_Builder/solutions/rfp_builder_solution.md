# Solution: rfp-builder skill

Reference answer for Lesson 3. Compare to your own only after you have made your own attempt.

## The reference content

Save at `practice/skills/rfp-builder.md`. About 65 lines.

```
<!-- v1.0 2026-04-25 Initial. -->

# rfp-builder

## What this skill does

Builds an RFP package for a sourcing event. Use this skill once at the
start of the event, after the category brief is approved and the supplier
longlist is finalised. Produces a six-section RFP package suitable for
issue to bidders without further editing, except for legal review of
the commercial-terms section.

## Inputs

inputs/category-brief.md
  A markdown brief with sections: Today, Current state, Goal, Scope,
  Stakeholders. Today's date drives the timeline. The Goal section drives
  the executive overview. The Scope section drives Section 2 of the RFP.

inputs/supplier-longlist.csv
  Columns: carrier_id, carrier_name, modes, primary_geography,
  certifications, capacity_tier, financial_health, otd_pct_12m,
  contract_terms_offered, incumbent.

templates/rfp-template.md
  Skeleton with six section headings. Do not modify. Use as the structure
  for the output file.

## Process

1. Read the category brief. Extract: today's date, the savings target,
   the close date, the in-scope modes, the panel ambition.
2. Read the longlist. Group carriers by mode. Note that some carriers
   offer multiple modes (semicolon-separated).
3. Read the RFP template to understand the six-section structure.
4. Section 1 (Executive overview): one page. Open with the headline
   savings target and the close date. Name the panel ambition.
5. Section 2 (Scope of work): list every in-scope mode and every
   in-scope lane category. Pull volume estimates from the brief.
6. Section 3 (Commercial terms): name the term (24 months with one
   12-month extension), payment (Net 45 days from CLAUDE.md folder rules),
   indexation (no indexation in base term, capped at 3% in extension).
7. Section 4 (Evaluation criteria matrix): use Price 40%, Service 25%,
   Capability 20%, Sustainability 10%, Implementation 5% unless the brief
   names different weights.
8. Section 5 (Supplier response template): mirror the shape the
   bid-scorer skill expects. Required fields: Executive summary,
   Capability statement, Pricing table (Lane, Mode, Volume, Unit rate,
   Annual value), Service commitments (OTD, damage rate, IA),
   Contract terms, Three references, Sustainability commitments.
9. Section 6 (Process and timeline): pull dates from the brief.
   Include Q&A window (10 working days), response deadline, evaluation
   period, decision date.

## Output format

Save outputs/rfp-package.md (single file).
Structure: six top-level sections matching templates/rfp-template.md headings.
Length: 4 to 6 pages of equivalent printed text.
Use British English. Oxford commas. No em-dashes. Active voice.
Specific numbers. Cap recommendations and tables at 10 rows.

## Quality criteria

- Every figure cited has a source named in inputs/category-brief.md or
  inputs/supplier-longlist.csv. Trace each figure back to the source.
- No supplier or carrier is named outside the longlist.
- Total length is 4 to 6 pages of equivalent printed text.
- The supplier response template (Section 5) lists the same field names
  the bid-scorer skill expects.
- The timeline in Section 6 has all four dates: Q&A close, response
  deadline, evaluation end, decision.
```

## Why this works

- Five sections. About 65 lines.
- Names input shapes (category brief markdown sections, longlist columns) without naming specific values.
- Process is nine numbered steps in plain English.
- Output format names the path, the structure, the length, and the writing rules.
- Quality criteria are checkable.

## How it differs from a one-off prompt

A prompt would say: "Build the RFP for the logistics consolidation. Spend baseline 11.2m GBP. Close date 2026-06-15. Award 2026-06-30." Those values appear in the category brief, not in the skill. The skill works for any RFP that has a category brief in this shape.
