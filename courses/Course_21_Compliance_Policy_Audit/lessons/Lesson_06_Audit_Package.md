# Audit Package Assembly

It is 09:00 Thursday. You have the compliance ledger, the breach reports, and the supporting transaction data. Internal Audit arrives in 85 days. They will ask for an evidence package: a defined scope, the compliance checks you ran, the results, and the supporting documents. You need to assemble all of this into a structured package that an auditor can walk through without calling you for context. The package tells the story from scope to findings to evidence.

## The S2P problem

Audit readiness fails at the assembly stage. The checks are done. The data exists. But it lives in six different files with no index. The auditor opens a folder, sees 12 files, and asks: "Where do I start? Which file supports which finding?" Without a structured package, the auditor spends half their time understanding your file organization. A proper evidence package has a cover page (scope and summary), an index (which file contains what), findings (each tied to a rule, a transaction, and a supporting document), and a ledger (the chronological audit trail). That structure is what turns a folder of files into an auditable record.

## What Claude Code does for you

Claude Code reads the compliance ledger, the three breach reports, and the raw transaction data. It assembles an audit evidence package with four sections: scope definition, findings summary, evidence index, and the ledger itself. Each finding links to a specific rule, a specific transaction, and a specific supporting file. The auditor can trace any finding from the summary to the ledger to the raw data in three steps.

## Set up

1. Lessons 1 through 5 completed. The compliance ledger exists at `outputs/compliance-ledger.jsonl`.
2. Breach reports are in `Drafts/`: approval-compliance-report.md, preferred-supplier-report.md, documentation-compliance-report.md.
3. Raw breach data CSVs are in `Drafts/`: approval-breaches.csv, off-contract-transactions.csv, documentation-gaps.csv.
4. Claude Code open in `Course_21_Compliance_Policy_Audit/practice/`.

## Step-by-step

### Step 1. Define the audit scope.

```
Write the audit scope section for the evidence package. Include:
- Audit title: Procurement Compliance Review, H1 2026
- Period: 2026-01-01 through 2026-06-30
- Compliance areas: approval authority, preferred supplier usage, contract documentation completeness
- Data: 200 transactions from transactions.csv
- Rules applied: 5 rules from policy-rules.json (approval authority, preferred supplier, documentation, split orders, breach escalation)
- Prepared by: Procurement Compliance Lead, Meridian Corp
- Date prepared: 2026-04-25

Save to outputs/audit-packages/scope.md.
```

You should see the scope document saved with all seven elements.

### Step 2. Build the findings summary.

```
Read Drafts/approval-compliance-report.md, Drafts/preferred-supplier-report.md, and Drafts/documentation-compliance-report.md. Create a findings summary with one row per compliance area. Columns: compliance_area, transactions_checked, violations_found, violation_rate_pct, severity, total_violation_amount_usd. Add a totals row. Save to outputs/audit-packages/findings-summary.md.
```

You should see a table with three compliance area rows plus a totals row. The total violations should be close to 55 (the number of planted violations in the data).

### Step 3. Build the evidence index.

```
Create an evidence index that maps each finding to its supporting files. Format as a table with columns: finding_id (F-001 through F-xxx), compliance_area, description, supporting_file_1 (the report), supporting_file_2 (the raw CSV), ledger_reference (the compliance-ledger.jsonl entry timestamp range). Save to outputs/audit-packages/evidence-index.md.
```

You should see an index where each finding points to two supporting files and a ledger reference. The auditor can follow any row from the index to the evidence.

### Step 4. Extract the relevant ledger entries.

```
Read outputs/compliance-ledger.jsonl. Filter to entries related to the three compliance areas. Show the entries in a table with columns: timestamp, action, file_written, content_length. Save the filtered ledger to outputs/audit-packages/ledger-extract.jsonl.
```

You should see the ledger entries that correspond to the compliance reports written in Lessons 2 through 4.

### Step 5. Assemble the cover page.

```
Write a cover page for the audit evidence package. Include:
- Title: Procurement Compliance Evidence Package, H1 2026
- Prepared for: Internal Audit, Meridian Corp
- Prepared by: Procurement Compliance Lead
- Date: 2026-04-25
- Summary: 200 transactions checked against 5 policy rules. [X] violations found across 3 compliance areas. All findings documented with supporting evidence and chronological ledger.
- Package contents: scope.md, findings-summary.md, evidence-index.md, ledger-extract.jsonl, plus references to the 6 supporting files in Drafts/.

Save to outputs/audit-packages/cover-page.md.
```

You should see the cover page saved with the violation count filled in from the findings summary.

### Step 6. Validate the package.

```
Read all files in outputs/audit-packages/. Check that:
1. The cover page lists all files in the package.
2. Every finding in findings-summary.md has at least one matching entry in evidence-index.md.
3. Every file referenced in evidence-index.md exists in Drafts/ or outputs/.
4. The ledger extract is non-empty.
5. No file contains em-dashes or banned phrases.
Report pass or fail for each check.
```

You should see pass for all five checks. If any fail, fix the specific file before shipping the package.

## Worked example

**Starting files:**
- `outputs/compliance-ledger.jsonl` (ledger entries from Lesson 5).
- `Drafts/approval-compliance-report.md`, `Drafts/preferred-supplier-report.md`, `Drafts/documentation-compliance-report.md` (three compliance reports).
- `Drafts/approval-breaches.csv`, `Drafts/off-contract-transactions.csv`, `Drafts/documentation-gaps.csv` (three raw data files).

**What you type:**

```
Assemble the full audit evidence package from the compliance reports, raw data files, and compliance ledger. Create outputs/audit-packages/ with: cover-page.md, scope.md, findings-summary.md, evidence-index.md, and ledger-extract.jsonl. Every finding must link to its supporting file and ledger entry.
```

**What you should see:** Five files saved in `outputs/audit-packages/`. The cover page lists all components. The findings summary shows violations by compliance area. The evidence index maps each finding to its supporting files. The ledger extract contains the relevant JSONL entries.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the compliance rules and output standards.
2. Read the three compliance reports from Drafts/ to extract findings and violation counts.
3. Read the three raw CSV files to confirm the supporting evidence exists.
4. Read outputs/compliance-ledger.jsonl to get the chronological audit trail.
5. Created the scope document with audit period, data sources, and rules applied.
6. Built the findings summary table from the three compliance area reports.
7. Created the evidence index linking each finding to its supporting files and ledger entries.

## Common mistakes and how to recover

- **Symptom:** The evidence index references a file that does not exist. **Fix:** Check the file paths in the index against the actual files in Drafts/ and outputs/. A typo in the file name (for example, "approval-breach.csv" instead of "approval-breaches.csv") breaks the reference. Fix the file name in the index.

- **Symptom:** The findings summary total does not match the sum of individual compliance areas. **Fix:** The totals row must sum the violations from all three areas. If the total says 50 but the three areas add up to 55, one area count is wrong. Recheck each compliance report.

- **Symptom:** The ledger extract is empty. **Fix:** The ledger only records writes to files with compliance keywords in their paths. If the compliance reports were saved without keywords like "compliance," "breach," or "violation" in the file name, the hook did not fire. Check the file names used in Lessons 2 through 4.

- **Symptom:** The cover page does not have the violation count filled in. **Fix:** The cover page must read the findings summary to get the total. If Claude Code wrote the cover page before the findings summary, the count is missing. Save the findings summary first, then write the cover page.

- **Symptom:** The auditor cannot trace a finding from the index to the ledger. **Fix:** Each evidence index row needs a ledger reference (a timestamp or timestamp range). If the ledger entries do not have timestamps that match the compliance report write times, the trace breaks. Check that the hook script uses UTC ISO timestamps.
