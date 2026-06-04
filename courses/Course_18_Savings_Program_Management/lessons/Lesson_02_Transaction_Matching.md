# Transaction-to-Initiative Matching

It is 14:00 Thursday. You have your savings methodology locked down in CLAUDE.md. Now you need actual numbers. The CFO does not want definitions on Tuesday. She wants realized savings by initiative, with the variance to target. You have 437 transactions in q1-q3-transactions.csv, each tagged with an initiative_id. You need to match every transaction to its initiative, compute realized savings per transaction, and roll up the totals.

## The S2P problem

Matching transactions to savings initiatives by hand is the most time-consuming part of a savings review. Each transaction needs its baseline rate, negotiated rate, and volume. You multiply, sum, and compare to the YTD target. With 437 transactions across five hard-savings initiatives, that is 437 lookups and calculations. One wrong VLOOKUP and your CFO number is off. One missed transaction and the variance explanation falls apart.

## What Claude Code does for you

Claude Code reads the transaction file and the initiative log in a single pass. It joins each transaction to its initiative by initiative_id, applies the hard savings formula from CLAUDE.md, computes realized savings per transaction, sums by initiative, and compares to the YTD target. You get a variance table in under a minute. Every calculation follows the methodology you encoded in Lesson 1.

## Set up

1. Lesson 1 completed. CLAUDE.md has the savings methodology with all four savings types and the validation rule.
2. Claude Code open in `Course_18_Savings_Program_Management/practice/`.
3. Both `data/sourcing-initiatives-log.csv` and `data/q1-q3-transactions.csv` are present.

## Step-by-step

### Step 1. Inspect the transaction file structure.

```
Read the first 10 rows of data/q1-q3-transactions.csv and describe the columns.
```

You should see columns: transaction_id, date, initiative_id, initiative_name, category, rate_applied, baseline_rate, volume, amount_usd, savings_usd.

### Step 2. Check for unmatched transactions.

```
Read data/q1-q3-transactions.csv and data/sourcing-initiatives-log.csv. List any transactions where the initiative_id does not match a row in the initiatives log.
```

You should see either zero unmatched transactions (the data is clean) or a short list of mismatches. Per your CLAUDE.md rules, unmatched transactions get flagged and excluded.

### Step 3. Calculate realized savings by initiative using the methodology.

```
For each hard savings initiative (SAV-001 through SAV-005), calculate realized savings from q1-q3-transactions.csv using the formula in CLAUDE.md: (baseline_rate - rate_applied) x volume for each transaction, summed by initiative. Compare to the ytd_target_usd in sourcing-initiatives-log.csv. Show a table with columns: initiative_id, initiative_name, ytd_target_usd, realized_savings_usd, variance_usd, variance_pct.
```

You should see a table with five rows. SAV-001 (Steel Consolidation) shows realized savings near $1,760,194 against a YTD target of $1,800,000. SAV-002 (Logistics RFP) shows realized savings near $747,565 against $1,350,000, a significant shortfall.

### Step 4. Add the non-hard savings initiatives.

```
Now add the three non-hard-savings initiatives (SAV-006, SAV-007, SAV-008) to the table. Use the ytd_realized_usd values from sourcing-initiatives-log.csv for these, since they do not have transaction-level data. Mark them with their savings type (soft, cost_avoidance, working_capital). Show the full 8-initiative table.
```

You should see the complete table with all 8 initiatives. The total YTD realized should be near $6,855,836 against a YTD target of $9,000,000.

### Step 5. Save the summary to Drafts.

```
Save this initiative savings summary as a CSV file to Drafts/savings-summary-ytd.csv with the columns: initiative_id, initiative_name, savings_type, ytd_target_usd, realized_savings_usd, variance_usd, variance_pct, status.
```

You should see the file saved with 8 data rows plus a header.

### Step 6. Identify the biggest variance drivers.

```
From the savings summary, which three initiatives have the largest negative variance in dollar terms? List them with the dollar gap and a one-sentence explanation of why each is behind.
```

You should see SAV-002 (Logistics RFP), SAV-007 (Spec Standardization), and SAV-006 (Demand Reduction) as the top three variance drivers.

## Worked example

**Starting files:**
- `data/q1-q3-transactions.csv` (437 rows).
- `data/sourcing-initiatives-log.csv` (8 initiatives).
- `CLAUDE.md` with savings methodology.

**What you type:**

```
Calculate the realized savings for SAV-002 (Logistics RFP) from q1-q3-transactions.csv. The baseline_rate is $3.20 per mile and the negotiated_rate is $2.72 per mile. Sum all savings for SAV-002 transactions and compare to the YTD target of $1,350,000.
```

**What you should see:** Claude Code shows SAV-002 realized savings of approximately $747,565, a variance of negative $602,435, or 44.6% below target.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to confirm the hard savings formula: (baseline minus negotiated) times volume.
2. Read q1-q3-transactions.csv and filtered to rows where initiative_id equals SAV-002.
3. For each SAV-002 transaction, computed (baseline_rate minus rate_applied) times volume.
4. Summed all per-transaction savings to get the YTD realized figure.
5. Compared to the YTD target of $1,350,000 from sourcing-initiatives-log.csv.
6. Calculated variance: $747,565 minus $1,350,000 equals negative $602,435 (negative 44.6%).

## Common mistakes and how to recover

- **Symptom:** Realized savings total does not match the sourcing-initiatives-log.csv figure. **Fix:** Check whether Claude Code used rate_applied or negotiated_rate from the initiative log. The transaction file has the actual rate_applied per transaction, which may differ slightly from the negotiated_rate due to surcharges or volume tiers.

- **Symptom:** The variance percentage shows a positive number when the initiative is behind. **Fix:** Confirm the formula is (realized minus target) divided by target. A negative result means behind. A positive result means ahead.

- **Symptom:** Claude Code includes soft savings initiatives in the transaction-level calculation. **Fix:** Only SAV-001 through SAV-005 are hard savings with transaction data. SAV-006, SAV-007, and SAV-008 use the ytd_realized_usd from the initiative log directly.

- **Symptom:** The CSV output has inconsistent decimal places. **Fix:** Check the rounding rule in CLAUDE.md. All USD figures should be rounded to two decimal places.

- **Symptom:** One initiative shows zero realized savings. **Fix:** Check whether any transactions exist for that initiative_id in the transaction file. If the filter returns no rows, the initiative may use a different ID format.
