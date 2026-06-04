# Lesson 6: Contract Drafting from Term Sheets

**Time:** 35 minutes.

## The blank page problem

It is 13:00 Monday of week three at Vanguard Manufacturing. Your sourcing team just finished negotiations with a new supplier, Cascade Fasteners Inc. They hand you a one-page term sheet: parties, scope, value ($348,000 over 36 months), payment terms (Net 45), insurance minimums, termination notice period, and three performance KPIs. They need a first-draft Master Services Agreement by Wednesday. Starting from a blank Word document and writing 15 to 20 clauses by hand would take you a full day. Your clause library in `clause-taxonomy.csv` has 15 standard clause types, but assembling them into a coherent draft is still slow.

## What Claude Code is going to do for you

Claude Code reads the term sheet, maps each commercial term to the appropriate clause type from your clause taxonomy, and generates a complete first-draft agreement. The draft uses your standard clause structures, fills in the negotiated values, and flags any terms the term sheet does not cover so you know where gaps remain.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_13_Contract_Intelligence/practice/`.
3. `clause-taxonomy.csv` in the practice root.
4. At least two completed contracts in `contracts/` to use as style references.

## Step-by-step

### Create the term sheet

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Create a term sheet for the new contract.

```
Write a file at Drafts/term_sheet_cascade_fasteners.md with these negotiated terms: Parties: Vanguard Manufacturing Inc. and Cascade Fasteners Inc. Scope: Supply of Grade 8 hex bolts, lock nuts, and flat washers for the Greenville assembly plant. Effective date: 2026-06-01. Term: 36 months. Total value: $348,000. Payment terms: Net 45. Insurance: $2,000,000 general liability, $1,000,000 product liability. Termination: 90 days written notice by either party. KPIs: on-time delivery >= 97%, defect rate <= 0.5%, order fill rate >= 99%. Governing law: State of Ohio.
```

You should see Claude create the term sheet file.

### Map terms to clause types

**Step 3.** Ask Claude to map the term sheet to the clause taxonomy.

```
Read Drafts/term_sheet_cascade_fasteners.md and clause-taxonomy.csv. For each term in the term sheet, identify which clause category from the taxonomy it maps to. List any clause categories from the taxonomy that have no corresponding term in the term sheet. These are gaps I need to address.
```

You should see a mapping like: Parties maps to "Parties and Recitals", Payment terms maps to "Payment", Insurance maps to "Insurance." You should also see gaps like "Confidentiality: not covered in term sheet", "Indemnification: not covered", "Data Protection: not covered."

### Generate the first draft

**Step 4.** Use existing contracts as style references.

```
Read contracts/MSA_Northwind_Office_Ltd.md and contracts/MSA_Apex_Logistics_Inc.md. Note the clause structure, section numbering, and language style. These are your reference contracts for drafting.
```

You should see Claude confirm it read both reference contracts.

**Step 5.** Generate the draft agreement.

```
Using the term sheet at Drafts/term_sheet_cascade_fasteners.md, the clause taxonomy, and the style of the two reference contracts you just read, draft a complete Master Services Agreement. Rules: (1) Use the section numbering style from the reference contracts. (2) Fill in all negotiated values from the term sheet. (3) For clause categories that appear in the taxonomy but not the term sheet, include the clause with placeholder text marked [TO BE NEGOTIATED]. (4) Add a "Schedule A: Service Level Agreement" section using the three KPIs from the term sheet. (5) Write to Drafts/MSA_Draft_Cascade_Fasteners.md.
```

You should see Claude write a full draft agreement with all sections populated.

**Step 6.** Review the draft for completeness.

```
Read Drafts/MSA_Draft_Cascade_Fasteners.md. List: (1) every section that has [TO BE NEGOTIATED] placeholders, (2) every section that references a specific dollar amount or date (verify these match the term sheet), (3) the total number of sections.
```

You should see a review listing the gaps (likely Confidentiality, Indemnification, Data Protection, Force Majeure) and confirmation that all dollar amounts and dates match the term sheet.

### Create a gap analysis for legal review

**Step 7.** Generate a cover memo for your legal team.

```
Write a one-page memo to Drafts/cascade_legal_review_memo.md addressed to "Legal Review Team." Include: (1) a summary of the contract (parties, value, term), (2) a table of sections with [TO BE NEGOTIATED] placeholders and a suggested priority (high, medium, low) for each, (3) any risk notes based on what the term sheet omits. Use today's date.
```

You should see Claude write a concise memo with a prioritized gap table.

**Step 8.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── contracts/ (20 files, used as style references)
├── clause-taxonomy.csv (15 clause types)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── term_sheet_cascade_fasteners.md
│   ├── MSA_Draft_Cascade_Fasteners.md
│   └── cascade_legal_review_memo.md
```

**What Claude did, behind the scenes:**

1. Claude read the term sheet and parsed each negotiated term into a structured list.
2. It read the clause taxonomy and matched each term to a clause category, identifying four unmapped categories.
3. It read two reference contracts to learn the section numbering style (1.0, 1.1, 1.2) and language patterns (formal but readable, no archaic legalese).
4. It generated each section of the MSA by combining the reference style with the term sheet values.
5. For unmapped categories, it inserted the clause structure with `[TO BE NEGOTIATED]` markers.
6. It built the SLA schedule using the three KPIs and standard measurement language from the reference contracts.
7. It wrote the legal review memo with a prioritized gap table.

## Common mistakes and how to recover

- **Symptom:** The draft uses legalese that does not match your reference contracts ("hereinafter referred to as"). **Fix:** add to your prompt: "Match the language register of the reference contracts. If the references use plain English, the draft should too. Do not add formal legal language that does not appear in the references."

- **Symptom:** Dollar amounts in the draft do not match the term sheet. **Fix:** always include the verification step (Step 6). Ask Claude to cross-check every figure against the source term sheet.

- **Symptom:** The draft is missing the SLA schedule entirely. **Fix:** Claude may have included KPIs in the main body instead of a separate schedule. Ask: "Move the KPI requirements to a separate Schedule A section at the end of the agreement, formatted as a table with KPI name, target, measurement frequency, and consequence of breach."

- **Symptom:** Claude generates clauses that contradict each other (e.g., two different termination notice periods). **Fix:** ask Claude to "Scan the entire draft for contradictions. Check that every reference to termination notice, payment terms, and insurance amounts is consistent throughout the document."

- **Symptom:** The [TO BE NEGOTIATED] sections are empty with no structure. **Fix:** ask Claude to "For each [TO BE NEGOTIATED] section, include the standard clause structure from the reference contracts with blank values. The legal team needs the framework, not just a placeholder label."
