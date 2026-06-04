# Lesson 2: Obligation Mapping

**Time:** 35 minutes.

## The obligations buried in clause 14.3

It is 10:00 Tuesday. Your CFO asks: "Which suppliers require us to provide quarterly business reviews, and what happens if we miss one?" You know the answer is somewhere in the 20 contracts you inherited at Vanguard Manufacturing. But obligations are scattered across different sections: service levels, reporting requirements, termination triggers, insurance minimums. Finding them means reading every contract front to back. Again.

## What Claude Code is going to do for you

Claude Code reads each contract file and extracts every obligation: who is responsible (Vanguard or the supplier), what the obligation is, when it is due, how often it recurs, and what happens if it is missed. The result is a single obligation register you can filter by responsible party, frequency, or consequence.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_13_Contract_Intelligence/practice/`.
3. The `Drafts/extraction_results.json` from Lesson 1 (confirms your environment is working).
4. The `clause-taxonomy.csv` file in the practice root.

## Step-by-step

### Review the clause taxonomy

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt load with context from `CLAUDE.md`.

**Step 2.** Read the clause taxonomy to understand obligation categories.

```
Read clause-taxonomy.csv and list all obligation categories.
```

You should see categories like: Reporting, Insurance, Audit Rights, Confidentiality, Service Levels, Termination Notice, Payment, Indemnification, Business Review, Data Protection.

### Extract obligations from a single contract

**Step 3.** Start with one contract to validate the approach.

```
Read contracts/MSA_Northwind_Office_Ltd.md. For every obligation in the contract, extract: (1) obligation_description (one sentence), (2) responsible_party (Vanguard Manufacturing or Northwind Office Ltd), (3) due_date or trigger, (4) frequency (one-time, monthly, quarterly, annually, ongoing), (5) consequence_of_breach (what happens if missed), (6) clause_reference (section number). Return as a JSON array.
```

You should see a JSON array with 5 to 10 obligations. Example:

```json
{
  "obligation_description": "Provide quarterly business review report",
  "responsible_party": "Northwind Office Ltd",
  "due_date": "15th of Jan, Apr, Jul, Oct",
  "frequency": "quarterly",
  "consequence_of_breach": "Vanguard may withhold 5% of quarterly payment",
  "clause_reference": "Section 8.2"
}
```

**Step 4.** Check if any obligations were missed by asking Claude to re-scan.

```
Re-read contracts/MSA_Northwind_Office_Ltd.md. Are there any obligations in sections covering insurance, indemnification, or data protection that you did not include in the previous list? If yes, add them.
```

You should see Claude confirm the list is complete or add one or two more items.

### Extract obligations from all contracts

**Step 5.** Run the extraction across all 20 contracts.

```
Read every file in contracts/. For each file, extract all obligations using these fields: contract_file, obligation_description, responsible_party, due_date_or_trigger, frequency, consequence_of_breach, clause_reference. Write the full result to Drafts/obligation_register.json as a flat array. Use clause-taxonomy.csv categories to tag each obligation with an obligation_category field.
```

You should see Claude confirm it processed all 20 contracts and wrote the file. Expect 80 to 150 obligations total.

**Step 6.** Get a summary of the results.

```
Read Drafts/obligation_register.json. Tell me: (1) total number of obligations, (2) how many are Vanguard's responsibility vs. supplier responsibility, (3) the top three obligation categories by count.
```

You should see a breakdown like: 112 total obligations, 48 Vanguard, 64 supplier. Top categories: Reporting (24), Service Levels (19), Insurance (15).

### Convert to CSV

**Step 7.** Create a CSV version for sharing.

```
Convert Drafts/obligation_register.json to Drafts/obligation_register.csv. Sort by responsible_party, then by frequency. Include all fields plus the obligation_category.
```

You should see Claude confirm the CSV was written with a header row and all obligation rows.

**Step 8.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── contracts/ (20 files)
├── clause-taxonomy.csv
├── Drafts/
│   └── extraction_results.json (from Lesson 1)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── obligation_register.json
│   └── obligation_register.csv
```

**What Claude did, behind the scenes:**

1. Claude read `clause-taxonomy.csv` to learn the 15 obligation categories.
2. It opened each contract file and scanned every section for language indicating an obligation: "shall", "must", "is required to", "will provide".
3. For each obligation found, it identified the responsible party by checking which entity name appeared as the subject of the obligation clause.
4. It matched each obligation to the closest category from the taxonomy.
5. It compiled all obligations into a single flat JSON array with consistent field names.
6. It converted the JSON to a sorted CSV for easy filtering in Excel.

## Common mistakes and how to recover

- **Symptom:** Claude returns obligations only for one party. **Fix:** some contracts use "the Supplier" or "the Buyer" instead of legal names. Add to your prompt: "Treat 'the Buyer' or 'the Company' as Vanguard Manufacturing. Treat 'the Supplier' or 'the Vendor' as the counterparty named in the Parties section."

- **Symptom:** Consequence field shows "not specified" for many obligations. **Fix:** this is often accurate. Many contracts state obligations without explicit consequences. Flag these for legal review rather than assuming Claude missed something.

- **Symptom:** Duplicate obligations appear because the same requirement is stated in two sections. **Fix:** ask Claude to "Review Drafts/obligation_register.json for duplicate obligations from the same contract. If two entries describe the same requirement, keep the one with the more specific clause reference and remove the other."

- **Symptom:** The obligation count seems too low (under 50 for 20 contracts). **Fix:** ask Claude to "Re-scan the contracts. Look specifically in appendices, schedules, and exhibits. Many obligations live outside the main body."
