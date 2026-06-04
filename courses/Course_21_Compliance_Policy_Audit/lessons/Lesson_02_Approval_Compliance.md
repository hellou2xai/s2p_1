# Approval Authority Compliance

It is 10:00 Tuesday. The policy rules are encoded. Now you run the first compliance check: approval authority. Every transaction in the data set needs to be checked against the approval matrix. Does the approver have sufficient authority for the transaction amount? Is any transaction self-approved? The audit letter said they found 12 approval breaches in the last review. Your data has 200 transactions. You need to find every breach and categorize it by severity.

## The S2P problem

Checking 200 transactions against an approval matrix by hand means 200 lookups. For each transaction, you find the amount, look up the required approval level, check the actual approver, and decide pass or fail. At two minutes per transaction, that is nearly seven hours. And manual checking misses patterns. A manager who approves three $24,000 transactions in a week is technically within their authority each time, but the pattern raises questions. Automated checking catches both individual breaches and suspicious patterns.

## What Claude Code does for you

Claude Code reads transactions.csv and approval-matrix.csv together. For each transaction, it checks the amount against the approval tiers, compares the actual approver to the required level, and flags breaches. It also checks for self-approvals (where the approver is the same as the requester). The output is a compliance report showing every breach with the transaction ID, amount, required approver, actual approver, and severity.

## Set up

1. Lesson 1 completed. CLAUDE.md has testable approval authority rules.
2. Claude Code open in `Course_21_Compliance_Policy_Audit/practice/`.
3. `data/transactions.csv` (200 transactions) and `data/approval-matrix.csv` (5 levels) are present.

## Step-by-step

### Step 1. Inspect the transaction data.

```
Read the first 10 rows of data/transactions.csv and show me all columns.
```

You should see columns including transaction_id, date, amount_usd, supplier_id, supplier_name, requester, approver_title, approver_name, contract_type, and violation_type.

### Step 2. Run the approval authority check on all 200 transactions.

```
Read data/transactions.csv and data/approval-matrix.csv. For each transaction, determine the required approver level based on amount_usd. Compare to the actual approver_title. Flag any transaction where:
1. The actual approver_title is below the required level, OR
2. The approver_name equals the requester (self-approval).

Show a summary first: total transactions checked, total breaches found, breach rate percentage.
```

You should see the total breach count. The data has planted approval violations among the 55 total violations.

### Step 3. List the approval breaches.

```
Show all approval authority breaches in a table with columns: transaction_id, date, amount_usd, required_approver, actual_approver, approver_name, breach_type (under-approved or self-approved), severity.
```

You should see a table listing each breach. Under-approved means the approver's level was too low for the amount. Self-approved means the approver and requester are the same person.

### Step 4. Categorize breaches by severity.

```
Group the approval breaches by severity and amount range. Show a summary table with columns: amount_range, breach_count, total_breach_amount_usd. Use these ranges: $0-5,000, $5,001-25,000, $25,001-100,000, $100,001-500,000, $500,001+.
```

You should see the distribution of breaches across amount ranges. Breaches in higher amount ranges are more serious to the audit committee.

### Step 5. Identify repeat offenders.

```
From the approval breaches, identify any approver who appears in more than one breach. Show a table with columns: approver_name, approver_title, breach_count, total_breach_amount_usd. Sort by breach_count descending.
```

You should see whether any single approver has multiple breaches. Repeat offenders suggest a systemic issue, not a one-time mistake.

### Step 6. Save the approval compliance report.

```
Save the full approval compliance results to Drafts/approval-compliance-report.md with three sections:
1. Summary: total checked, total breaches, breach rate.
2. Breach detail table: all breaches with transaction details.
3. Risk findings: repeat offenders and highest-amount breaches.
Save the raw breach data to Drafts/approval-breaches.csv.
```

You should see both files saved. The markdown report is for the audit committee. The CSV is the supporting evidence.

## Worked example

**Starting files:**
- `data/transactions.csv` (200 transactions).
- `data/approval-matrix.csv` (5 authority levels).
- `CLAUDE.md` with approval authority rules.

**What you type:**

```
Check all 200 transactions in data/transactions.csv against the approval matrix. Flag every approval authority breach (under-approved or self-approved). Show the breach count and save the detail to Drafts/approval-breaches.csv.
```

**What you should see:** A summary showing the total number of approval breaches found (a subset of the 55 total violations), and confirmation that the breach detail CSV is saved.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the approval authority rule with pass/fail conditions.
2. Read data/approval-matrix.csv to build a lookup: amount range to required approver level.
3. Read data/transactions.csv to get all 200 transactions.
4. For each transaction, looked up the required approver based on amount_usd.
5. Compared the required approver to the actual approver_title. Flagged mismatches.
6. Checked whether approver_name equals requester. Flagged self-approvals.
7. Counted total breaches and saved the detail to CSV.

## Common mistakes and how to recover

- **Symptom:** Zero breaches found in 200 transactions. **Fix:** The data has planted violations. Check that the comparison logic is correct. A transaction of $28,000 with a Manager approval should fail because the $25,001-$100,000 range requires a VP. If the logic treats Manager as sufficient for any amount, the tiers are not being applied.

- **Symptom:** Every transaction is flagged as a breach. **Fix:** Check the approval level hierarchy. Manager is lower than Director, Director is lower than VP, VP is lower than CFO, CFO is lower than Board. If the hierarchy is inverted, every transaction fails. Verify the tier boundaries match approval-matrix.csv.

- **Symptom:** Self-approvals are not detected. **Fix:** The self-approval check compares approver_name to requester, not approver_title to requester. Two different people can have the same title. The check must use names.

- **Symptom:** Transactions at exact tier boundaries (for example, exactly $5,000 or $25,000) are flagged incorrectly. **Fix:** Check the boundary logic. The approval matrix uses ranges: $0-$5,000 requires Manager, $5,001-$25,000 requires Director. A transaction at exactly $5,000 falls in the Manager tier. A transaction at $5,001 falls in the Director tier.

- **Symptom:** The breach count includes duplicates. **Fix:** Each transaction should produce one compliance result. If a transaction is both under-approved and self-approved, count it once but list both breach types.
