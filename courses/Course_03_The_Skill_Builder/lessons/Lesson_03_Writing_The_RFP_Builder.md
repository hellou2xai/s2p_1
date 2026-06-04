# Lesson 3: Writing the rfp-builder skill

**Time:** 60 minutes. **You need:** Lessons 1 and 2 complete.

## A typical Wednesday morning

It is 09:30 Wednesday. The Lesson 1 rfp-builder you copied was someone else's. This morning you write your own from a blank file. By 10:30 your `practice/skills/rfp-builder.md` is yours, and you have run it twice on the practice data.

This lesson is the longest in the course because it is where you commit the methodology to the file. Lesson 2 was theory; Lesson 3 is the doing.

## The big idea

Writing a skill is like writing a one-page operating procedure for a new analyst. They will run the procedure many times. You will not be there to answer questions. So the skill must:

- Name the inputs by shape (path, columns, sections), not by specific value.
- Name every step in plain English.
- Name the output by path, structure, and length.
- Name the checks that confirm the run was good.

Five sections, 40 to 80 lines total. No more.

## Set up

**Step 1.** Open your terminal.

**Step 2.** Move to the practice folder:

```
cd "Course_03_The_Skill_Builder/practice"
```

**Step 3.** Delete the rfp-builder skill you copied in Lesson 1. You are starting from scratch:

- Windows PowerShell:
```
Remove-Item skills/rfp-builder.md
```
- Mac or Linux:
```
rm skills/rfp-builder.md
```

**Step 4.** Confirm it is gone:

```
ls skills
```

You should see only `README.md` and `list-incumbents.md` (from Lesson 2).

## Write the rfp-builder skill, one section at a time

**Step 5.** Create a new file at `practice/skills/rfp-builder.md`.

**Step 6.** Type the title and the first section:

```
# rfp-builder

## What this skill does

Builds an RFP package for a sourcing event. Use this skill once at the
start of the event, after the category brief is approved and the supplier
longlist is finalised. The skill produces a six-section RFP package
suitable for issue to bidders without further editing, except for legal
review of the commercial-terms section.
```

Save. Six lines so far.

**Step 7.** Add the inputs section. Type:

```
## Inputs

inputs/category-brief.md
  A markdown brief with sections: Today, Current state, Goal, Scope,
  Stakeholders. Today's date drives the timeline. The Goal section drives
  the executive overview.

inputs/supplier-longlist.csv
  Columns: carrier_id, carrier_name, modes, primary_geography,
  certifications, capacity_tier, financial_health, otd_pct_12m,
  contract_terms_offered, incumbent.

templates/rfp-template.md
  Skeleton with six section headings. Do not modify. Use as the structure
  for the output file.
```

Save. About 18 lines now.

**Step 8.** Add the process section:

```
## Process

1. Read the category brief. Extract: today's date, the goal, the scope,
   the savings target, and the close date.
2. Read the longlist. Group carriers by mode. Note that some carriers
   offer multiple modes (modes are semicolon-separated in the modes column).
3. Read the RFP template to understand the six-section structure required.
4. Write Section 1 (Executive overview): one page. Open with the headline
   savings target and the close date. Name the four-carrier-panel ambition.
5. Write Section 2 (Scope of work): list every in-scope mode and every
   in-scope lane. Pull volume estimates from the brief.
6. Write Section 3 (Commercial terms): name the term (24 months with one
   12-month extension), the payment terms (Net 45 days, derived from the
   global CLAUDE.md folder rules), the indexation rule (no indexation in
   base term, capped at 3% in extension).
7. Write Section 4 (Evaluation criteria matrix): use Price 40%, Service 25%,
   Capability 20%, Sustainability 10%, Implementation 5% unless the brief
   names different weights.
8. Write Section 5 (Supplier response template): mirror the shape the
   bid-scorer skill expects (executive summary, capability statement,
   pricing table with named columns, references, terms). This is critical;
   if the response template diverges from the scorer's input shape,
   bid scoring breaks.
9. Write Section 6 (Process and timeline): pull dates from the brief.
   Include Q&A window (10 working days), response deadline, evaluation
   period, decision date.
```

Save. About 45 lines now.

**Step 9.** Add the output format section:

```
## Output format

Save outputs/rfp-package.md (single file).
Structure: six top-level sections matching templates/rfp-template.md headings.
Length: 4 to 6 pages of equivalent printed text.
Use British English. Oxford commas. No em-dashes. Active voice.
Specific numbers. Cap recommendations and tables at 10 rows.
```

Save. About 53 lines.

**Step 10.** Add the quality criteria section:

```
## Quality criteria

- Every figure cited has a source named in inputs/category-brief.md or
  inputs/supplier-longlist.csv. Trace each figure back to the source on review.
- No supplier or carrier is named outside the longlist. Verify against the
  carrier_id column of supplier-longlist.csv.
- Total length is 4 to 6 pages of equivalent printed text. Section 4
  (Evaluation criteria) is one page; Section 5 (Supplier response template)
  is up to two pages; the rest are half a page each.
- The supplier response template (Section 5) lists the same field names that
  the bid-scorer skill expects. Mismatch means scoring breaks.
- The timeline in Section 6 has all four dates: Q&A close, response deadline,
  evaluation end, decision.
```

Save. Final file should be 60 to 70 lines.

## Test the skill: run it

**Step 11.** Start Claude in the practice folder:

```
claude
```

**Step 12.** Type:

```
Use the rfp-builder skill in skills/rfp-builder.md.
Inputs and templates are in the named folders.
Save the output to outputs/rfp-package.md.
```

Press Enter.

Wait. Claude is reading the category brief, the longlist, the template, then composing the six sections. This takes 60 to 90 seconds.

**What you should see.** A confirmation that `outputs/rfp-package.md` has been written.

**Step 13.** Open `outputs/rfp-package.md`. Read it. The six sections should be:

1. Executive overview that names the 1.6m GBP savings target and the 2026-06-30 award date.
2. Scope of work that lists road FTL, road LTL, sea FCL, and air freight as the in-scope modes.
3. Commercial terms that names a 24-month term plus 12-month extension and Net 45 payment.
4. Evaluation criteria matrix with the 40/25/20/10/5 weights.
5. Supplier response template that lists fields like Executive summary, Capability statement, Pricing table (lane, mode, volume, unit rate, annual value), References, Terms.
6. Process and timeline with Q&A close, response deadline (2026-06-15), evaluation period, decision (2026-06-30).

**Step 14.** Run a quality check on the output. Type a follow-up to Claude:

```
Run the quality criteria from the rfp-builder skill against the file
you just produced. Tell me which criteria pass and which fail.
```

Press Enter.

**What you should see.** Claude opens both the skill file and the output file. Claude tells you which of the five quality criteria pass. If any fail, the message names the gap (for example, "the timeline only has three of the four dates"). Re-run with the gap fixed.

**Step 15.** Quit Claude (`/quit`).

## Compare against the solution

**Step 16.** Open `solutions/rfp_builder_solution.md`. Read it. Compare against your file. The solution is one good answer; yours is one good answer. Borrow ideas where the solution is sharper.

**Step 17.** Optional: re-run the skill with one tweak. Edit your skill to change the evaluation weights to 35/25/20/15/5 (lifting Sustainability, lowering Price). Save. Re-run. The Section 4 weights in the output should now reflect the new percentages. Same skill, different inputs (the weights), different output. This is what reusability means in practice.

## What just happened, in plain words

You wrote a 60-line file that captures the methodology Acme uses to issue an RFP. The next sourcing event you run, you will not write a new RFP. You will run this skill on a new category brief and a new longlist. The skill produces the package.

The skill is now an asset of your team. If three other category leads read your rfp-builder, they can run the same methodology against their categories. The methodology is the same; the inputs differ.

## Three things that trip beginners up

- **You named specific carriers in the skill.** Step back to Step 8. Did your skill say "FastRoad UK" or "11.2m GBP"? If yes, those are inputs, not methodology. Move them out (they are already in the brief and the longlist).
- **You wrote a 200-line skill.** A skill that is too long becomes another chat prompt. Trim back to 60 to 80 lines. If a section is more than 15 lines, you are over-specifying.
- **The output failed the quality criteria check.** That is good news. The skill caught its own gap. Tighten the process steps that produced the gap and re-run.

## You are done with Lesson 3 when

- `practice/skills/rfp-builder.md` is your file (not the copied solution), 50 to 80 lines, with the five sections.
- You ran the skill and produced `practice/outputs/rfp-package.md`.
- You ran the quality check on the output and at least four of the five criteria pass.
- You compared against the solution and borrowed one or two ideas where the solution was sharper.

Take a break. Move to Lesson 4 next, where you write the bid-scorer skill that processes the six bid responses.
