# Lesson 2: RFP Package

**Time:** 40 minutes.

## The RFP that took three weeks to write

It is 09:00 Tuesday, day two of your six-week sourcing sprint at Ironbridge Manufacturing. Your CPO needs an RFP out to the supplier longlist by end of week one. Last time you ran a sourcing event, the RFP took three weeks to write: scope section from the engineer, pricing template from finance, quality requirements from the quality manager, terms and conditions from legal. Four authors, four rounds of review, and a document that still had inconsistencies on page 12. This time, you want one chained session that produces all RFP sections from the context already in `CLAUDE.md`.

## What Claude Code is going to do for you

Claude Code reads the sourcing event context, spend baseline, and supplier longlist from `CLAUDE.md` and the data files, then generates every section of the RFP in a single session: cover letter, scope of work, technical requirements, pricing template structure, evaluation criteria, submission instructions, and terms and conditions. One session, one consistent document.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_16_Sourcing_Sprint/practice/`.
3. `CLAUDE.md` with the Sourcing Event Context from Lesson 1.
4. `spend-baseline.csv` and `supplier-longlist.csv`.

## Step-by-step

### Generate the RFP sections in sequence

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt with the full sourcing context loaded.

**Step 2.** Generate the cover letter.

```
Write the RFP cover letter to Drafts/RFP_01_Cover_Letter.md. Include: (1) Ironbridge Manufacturing Inc. as the issuing entity, (2) the sourcing event title: "RFP-2026-04: Precision-Machined Steel Brackets," (3) a one-paragraph scope summary, (4) the submission deadline (two weeks from today: 2026-05-09), (5) the single point of contact for questions. Keep it to one page.
```

You should see a professional cover letter with all five elements.

**Step 3.** Generate the scope of work.

```
Write the scope of work to Drafts/RFP_02_Scope_Of_Work.md. Include: (1) description of the parts (use the part numbers and specifications from spend-baseline.csv), (2) estimated annual volumes per part number, (3) delivery locations (Detroit assembly plant), (4) contract term (24 months with one 12-month renewal option), (5) quality requirements (defect rate below 0.3%, ISO 9001 certification required).
```

You should see a detailed scope section referencing actual part numbers and volumes from the spend data.

**Step 4.** Generate the pricing template structure.

```
Write the pricing template instructions to Drafts/RFP_03_Pricing_Template.md. Define the columns suppliers must complete: part_number, description, unit_of_measure, annual_volume, unit_price_usd, total_annual_price, tooling_cost (one-time), freight_terms (FOB origin or delivered). Include a note that prices must be held firm for 90 days from submission. Add a sample row using one part number from spend-baseline.csv.
```

You should see a clear pricing template with a sample row.

**Step 5.** Generate the evaluation criteria section.

```
Write the evaluation criteria to Drafts/RFP_04_Evaluation_Criteria.md. Use the weights from CLAUDE.md: price 40%, quality capability 25%, delivery reliability 20%, financial stability 15%. For each criterion, list 2-3 specific items the evaluators will assess. Example for price: unit pricing competitiveness, total cost of ownership including tooling and freight, volume discount structure.
```

You should see four criteria sections with specific assessment items and weights.

**Step 6.** Generate submission instructions.

```
Write submission instructions to Drafts/RFP_05_Submission_Instructions.md. Include: (1) deadline: 2026-05-09 at 17:00 ET, (2) format: all pricing in the template format from Section 3, technical responses in a separate document, (3) questions deadline: 2026-05-02, questions sent to the point of contact, (4) late submissions will not be accepted, (5) Ironbridge reserves the right to award to one or multiple suppliers.
```

You should see clear, specific submission instructions.

**Step 7.** Generate the terms and conditions summary.

```
Write a terms and conditions summary to Drafts/RFP_06_Terms_And_Conditions.md. Include standard clauses: payment terms (Net 45), warranty (12 months from delivery), liability cap (2x annual contract value), intellectual property (Ironbridge retains all rights to custom tooling), confidentiality (mutual NDA required), and termination (90 days written notice). Mark each as "subject to negotiation" or "non-negotiable."
```

You should see six clause summaries, each with a negotiability label.

### Assemble the complete RFP

**Step 8.** Combine all sections into one document.

```
Read Drafts/RFP_01 through RFP_06. Combine them into a single document at Drafts/RFP_2026_04_Steel_Brackets_Complete.md with a table of contents at the top. Number the sections 1 through 6. Verify that all cross-references are consistent (e.g., "see Section 3 for pricing template" actually points to the pricing section).
```

You should see the complete RFP with a table of contents and consistent cross-references.

**Step 9.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── spend-baseline.csv
├── supplier-longlist.csv
├── CLAUDE.md (with sourcing context)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── RFP_01_Cover_Letter.md
│   ├── RFP_02_Scope_Of_Work.md
│   ├── RFP_03_Pricing_Template.md
│   ├── RFP_04_Evaluation_Criteria.md
│   ├── RFP_05_Submission_Instructions.md
│   ├── RFP_06_Terms_And_Conditions.md
│   └── RFP_2026_04_Steel_Brackets_Complete.md
```

**What Claude did, behind the scenes:**

1. Claude read the sourcing context from `CLAUDE.md` for the category, objectives, and evaluation weights.
2. It read `spend-baseline.csv` to extract actual part numbers, volumes, and current pricing for the scope and pricing sections.
3. It generated each section in sequence, carrying forward consistent details (same deadline, same contact, same part numbers).
4. It applied the evaluation weights from `CLAUDE.md` and expanded each into specific assessment items.
5. It assembled the final document by reading all six sections and adding a numbered table of contents.
6. It checked cross-references between sections to ensure consistency.

## Common mistakes and how to recover

- **Symptom:** Part numbers in the scope section do not match the pricing template. **Fix:** both sections should pull from the same source (`spend-baseline.csv`). Ask Claude to "Read spend-baseline.csv and list the unique part numbers. Verify these same part numbers appear in both Section 2 and Section 3."

- **Symptom:** The evaluation weights in Section 4 do not match `CLAUDE.md`. **Fix:** ask Claude to "Read the evaluation criteria weights from CLAUDE.md and confirm Section 4 uses the exact same percentages."

- **Symptom:** The RFP uses vague language like "competitive pricing expected." **Fix:** the RFP should state what it needs (prices per part, held for 90 days) without telling suppliers what to bid. Remove subjective adjectives.

- **Symptom:** The combined document has duplicate headers or broken section numbering. **Fix:** ask Claude to "Re-number all sections sequentially from 1.0 and ensure no heading appears twice."
