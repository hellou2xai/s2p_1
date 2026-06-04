# Documentation Completeness Check

It is 09:00 Wednesday. Two compliance checks are done. The third audit area is contract documentation. The audit letter said 15 contracts were missing required documents in the last review. Your data has contract-documentation.csv, which lists the required documents for each contract type: MSA, SOW, NDA, SLA, and amendment. You need to check every contract in the transactions against the documentation requirements and flag gaps.

## The S2P problem

Contract documentation requirements vary by contract type. An MSA requires a signed agreement, scope of work, pricing schedule, insurance certificate, and NDA. An SLA requires a signed SLA, service definition, penalty schedule, and escalation matrix. Checking each contract by hand means opening the contract file, comparing the attached documents to the requirement list, and noting what is missing. With 200 transactions across multiple contract types, this is a full day of clerical work. Missing even one required document is an audit finding.

## What Claude Code does for you

Claude Code reads contract-documentation.csv (which defines required documents per contract type) and transactions.csv (which includes contract_type and documentation status for each transaction). For each transaction, it looks up the contract type, checks which documents are required, and flags any that are missing. The output is a gap register: every missing document, for every contract, with the contract type and the document name.

## Set up

1. Lessons 1 through 3 completed. CLAUDE.md has testable documentation completeness rules.
2. Claude Code open in `Course_21_Compliance_Policy_Audit/practice/`.
3. `data/transactions.csv` (200 transactions) and `data/contract-documentation.csv` (required documents by type) are present.

## Step-by-step

### Step 1. Read the documentation requirements.

```
Read data/contract-documentation.csv and show me all rows. Group by contract_type and list the required documents for each type.
```

You should see 5 contract types: MSA (5 required documents), SOW (3), NDA (1), SLA (4), and amendment (2). Every document is marked as mandatory.

### Step 2. Inspect the transactions for contract type and documentation fields.

```
Read the first 10 rows of data/transactions.csv. Which columns relate to contract type and documentation status? Show the column names and sample values.
```

You should see a contract_type column and possibly columns indicating which documents are present or a violation_type column flagging documentation gaps.

### Step 3. Run the documentation completeness check.

```
Read data/transactions.csv and data/contract-documentation.csv. For each transaction, look up the contract_type and determine which mandatory documents are required. Check the transaction data for documentation gaps. Flag any transaction where one or more mandatory documents are missing. Show a summary: total transactions checked, total with complete documentation, total with gaps, gap rate percentage.
```

You should see the gap count and percentage. The data has planted documentation violations among the 55 total violations.

### Step 4. List the documentation gaps.

```
Show all transactions with documentation gaps in a table with columns: transaction_id, date, supplier_name, contract_type, missing_documents (comma-separated list), severity.
```

You should see a table listing each transaction with incomplete documentation and the specific documents that are missing.

### Step 5. Summarize by contract type.

```
Group the documentation gaps by contract_type. Show a table with columns: contract_type, total_contracts, contracts_with_gaps, gap_rate_pct, most_commonly_missing_document. This tells the audit committee which contract type has the worst documentation discipline.
```

You should see which contract types have the highest gap rates. MSAs with 5 required documents may have more gaps than NDAs with only 1.

### Step 6. Save the documentation compliance report.

```
Save the documentation completeness results to Drafts/documentation-compliance-report.md with three sections:
1. Summary: total checked, total with gaps, gap rate.
2. Gap detail table: all transactions with missing documents.
3. Contract type summary: gap rates by contract type and most commonly missing document.
Save the raw gap data to Drafts/documentation-gaps.csv.
```

You should see both files saved.

## Worked example

**Starting files:**
- `data/transactions.csv` (200 transactions).
- `data/contract-documentation.csv` (required documents by contract type).
- `CLAUDE.md` with documentation completeness rules.

**What you type:**

```
Check all 200 transactions against the documentation requirements in contract-documentation.csv. Flag every transaction missing a mandatory document. Show the total gap count and the most commonly missing document type. Save gaps to Drafts/documentation-gaps.csv.
```

**What you should see:** A summary with the total number of transactions missing documents, the gap rate, and the most frequently missing document (for example, insurance_certificate or pricing_schedule).

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the documentation completeness rule.
2. Read data/contract-documentation.csv to build a lookup: contract type to list of required documents.
3. Read data/transactions.csv to get all 200 transactions with their contract_type.
4. For each transaction, looked up the required documents for its contract type.
5. Compared the required documents to the available documentation fields on the transaction.
6. Flagged missing documents and counted them.
7. Identified the most commonly missing document across all gaps.

## Common mistakes and how to recover

- **Symptom:** No documentation gaps found. **Fix:** The data has planted documentation violations. Check how Claude Code determines whether a document is "present." The transaction data may use a flag column (1 for present, 0 for missing) or a violation_type column. If Claude Code is reading the wrong column, it cannot detect gaps.

- **Symptom:** Every transaction is flagged as having gaps. **Fix:** Check the contract_type matching. If the transaction file uses "MSA" but contract-documentation.csv uses "msa" (lowercase), the lookup fails and Claude Code cannot find any requirements, or it may flag everything. Ensure the case matches.

- **Symptom:** Amendment-type contracts show fewer gaps than MSAs. **Fix:** This is expected. Amendments require only 2 documents (signed amendment and original agreement reference). MSAs require 5. More required documents means more chances for a gap.

- **Symptom:** The gap count includes transactions that are not contracts (for example, spot purchases). **Fix:** Not every transaction has a contract. If a transaction has no contract_type, it should be excluded from the documentation check or flagged separately as "no contract on file."
