# Preferred Supplier Compliance

It is 14:00 Tuesday. The approval check is done. Now you run the second compliance area: preferred supplier usage. The audit letter flagged 8% of purchases going to suppliers not on the preferred list. Your data has 200 transactions and 10 preferred suppliers. Every transaction must use a preferred supplier unless an approved exception exists. You need the full list of off-contract purchases, the dollar amount, and the percentage of total spend that went off-contract.

## The S2P problem

Preferred supplier agreements exist for a reason. Negotiated rates, quality standards, and contractual protections all depend on purchasing from approved suppliers. When buyers go off-contract, the organization loses negotiated savings, takes on unvetted supplier risk, and weakens the contract position with preferred suppliers. Quantifying off-contract spend is essential. "Some purchases went off-contract" is not an audit finding. "$247,000 in off-contract spend, equal to 6.3% of total purchases, went to 4 non-preferred suppliers" is an audit finding.

## What Claude Code does for you

Claude Code reads transactions.csv and preferred-suppliers.csv. It checks each transaction's supplier_id against the preferred list. Transactions from non-preferred suppliers are flagged. The output shows each off-contract transaction, the non-preferred supplier name, the amount, and whether an approved exception exists. It also calculates the total off-contract spend as a dollar amount and percentage.

## Set up

1. Lessons 1 and 2 completed. CLAUDE.md has testable preferred supplier rules.
2. Claude Code open in `Course_21_Compliance_Policy_Audit/practice/`.
3. `data/transactions.csv` (200 transactions) and `data/preferred-suppliers.csv` (10 suppliers) are present.

## Step-by-step

### Step 1. Read the preferred supplier list.

```
Read data/preferred-suppliers.csv and show me all 10 suppliers with their supplier_id, supplier_name, and category.
```

You should see 10 rows: Great Lakes Steel, Heartland Polymers, Pacific Aluminum, Continental Freight, TechForward Solutions, National Facilities, Whitfield Consulting, Cascade Fasteners, Patriot Logistics, and CloudBridge Systems.

### Step 2. Run the preferred supplier check.

```
Read data/transactions.csv and data/preferred-suppliers.csv. For each transaction, check if the supplier_id exists in the preferred supplier list. Flag transactions where the supplier is NOT on the preferred list. Show a summary: total transactions, on-contract count, off-contract count, off-contract percentage.
```

You should see the off-contract count and percentage. The data has planted preferred-supplier violations among the 55 total violations.

### Step 3. List the off-contract transactions.

```
Show all off-contract transactions in a table with columns: transaction_id, date, supplier_id, supplier_name, amount_usd, category. Sort by amount_usd descending.
```

You should see a table of transactions that used non-preferred suppliers. The largest off-contract purchases are at the top.

### Step 4. Quantify by non-preferred supplier.

```
Group the off-contract transactions by supplier. Show a table with columns: supplier_name, transaction_count, total_off_contract_usd, pct_of_total_spend. Sort by total_off_contract_usd descending.
```

You should see which non-preferred suppliers received the most off-contract spend. This tells the audit committee where the leakage is concentrated.

### Step 5. Check for approved exceptions.

```
From the off-contract transactions, check the transactions.csv data for any exception or justification field. List transactions that have an approved exception documented versus those that do not. Show a summary: off-contract with exception, off-contract without exception.
```

You should see that most off-contract transactions lack an approved exception. Transactions without exceptions are the compliance findings. Transactions with valid exceptions are compliant despite being off-contract.

### Step 6. Save the preferred supplier compliance report.

```
Save the preferred supplier compliance results to Drafts/preferred-supplier-report.md with three sections:
1. Summary: total on-contract, total off-contract, off-contract spend amount and percentage.
2. Off-contract detail table: all off-contract transactions.
3. Non-preferred supplier summary: aggregated spend by non-preferred supplier.
Save the raw off-contract data to Drafts/off-contract-transactions.csv.
```

You should see both files saved.

## Worked example

**Starting files:**
- `data/transactions.csv` (200 transactions).
- `data/preferred-suppliers.csv` (10 suppliers).
- `CLAUDE.md` with preferred supplier rules.

**What you type:**

```
Check all 200 transactions against the preferred supplier list. Calculate total off-contract spend in dollars and as a percentage. Save the off-contract transactions to Drafts/off-contract-transactions.csv.
```

**What you should see:** A summary showing the number of off-contract transactions, the total off-contract dollar amount, and the percentage. Confirmation that the CSV is saved.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the preferred supplier compliance rule.
2. Read data/preferred-suppliers.csv to build a set of 10 approved supplier_ids.
3. Read data/transactions.csv to get all 200 transactions.
4. For each transaction, checked whether supplier_id exists in the preferred set.
5. Flagged non-matches as off-contract.
6. Summed the amount_usd for all off-contract transactions.
7. Calculated the percentage: off-contract total divided by total spend times 100.

## Common mistakes and how to recover

- **Symptom:** Zero off-contract transactions found. **Fix:** Check that the supplier_id format matches between transactions.csv and preferred-suppliers.csv. If one file uses "SUP001" and the other uses "SUP-001," the lookup fails and every transaction appears off-contract. Or if the matching logic is inverted, every transaction appears on-contract.

- **Symptom:** The off-contract percentage is over 50%. **Fix:** The preferred list has 10 suppliers. If the transactions file uses 15 or 20 different suppliers, many will be off-contract. Check whether the matching logic is correct. Also verify that the preferred-suppliers.csv file has all 10 expected entries.

- **Symptom:** Off-contract transactions with valid exceptions are counted as violations. **Fix:** The rule says: off-contract is a violation ONLY if no approved exception exists. Transactions with documented exceptions should pass. Separate them in the report.

- **Symptom:** The report does not include dollar amounts. **Fix:** Every off-contract finding must state the dollar amount. "SUP-012 is not on the preferred list" is not a finding. "3 transactions totaling $18,400 went to SUP-012 (not on preferred list), with no approved exception" is a finding.
