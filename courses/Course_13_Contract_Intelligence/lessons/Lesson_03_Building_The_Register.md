# Lesson 3: Building the Contract Register

**Time:** 35 minutes.

## The spreadsheet that should have existed all along

It is 14:00 Wednesday. Your CPO stops by your desk at Vanguard Manufacturing and asks: "Can you send me a list of every contract over $200,000 that expires in the next 12 months? I need it for the board pack by Friday." You have the extraction data from Lessons 1 and 2. But it sits in two separate JSON files with no single source of truth. The existing `contract-register.csv` in the practice folder has only 8 of the 20 contracts, and three of those have outdated values. You need one clean, structured register that you can update incrementally as new contracts arrive.

## What Claude Code is going to do for you

Claude Code merges your extraction data into a single contract register in JSON format. It reconciles duplicates, fills gaps, validates fields, and writes a register you can query and update without rebuilding from scratch each time.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_13_Contract_Intelligence/practice/`.
3. `Drafts/extraction_results.json` and `Drafts/obligation_register.json` from Lessons 1 and 2.
4. The existing `contract-register.csv` in the practice root.

## Step-by-step

### Audit the existing register

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Compare the existing register against your extraction data.

```
Read contract-register.csv and Drafts/extraction_results.json. Tell me: (1) how many contracts are in the CSV, (2) how many are in the JSON, (3) which contracts appear in the JSON but not the CSV, and (4) which contracts have different values between the two sources.
```

You should see that the CSV has 8 contracts, the JSON has 20, and Claude lists the 12 missing contracts and any value discrepancies.

### Build the master register

**Step 3.** Create the consolidated register.

```
Build a contract register by merging contract-register.csv and Drafts/extraction_results.json. Rules: (1) Use extraction_results.json as the primary source because it comes directly from the contract text. (2) For the 8 contracts that appear in both, keep the JSON values but flag any fields where the CSV had a different value. (3) Add an obligation_count field by counting obligations per contract from Drafts/obligation_register.json. (4) Add a status field: "active" if expiry_date is after today, "expired" if before today, "expiring_soon" if within 180 days. Write the result to Drafts/contract_register.json.
```

You should see Claude confirm it wrote `Drafts/contract_register.json` with 20 records, each containing all commercial fields plus `obligation_count` and `status`.

**Step 4.** Validate the register.

```
Read Drafts/contract_register.json and run these checks: (1) Every record has all required fields populated (no nulls or blanks). (2) Every total_value_usd is a positive number. (3) Every expiry_date is after the effective_date. (4) Every payment_terms field matches a known pattern (Net 15, Net 30, Net 45, Net 60, Net 90). Report any failures.
```

You should see a validation report. If any records fail, Claude lists them with the specific issue.

**Step 5.** Fix any validation issues.

```
Fix the validation failures you just identified in Drafts/contract_register.json. For each fix, tell me what the old value was and what you changed it to.
```

You should see Claude confirm each fix with before and after values.

### Add incremental update capability

**Step 6.** Create an update instruction in CLAUDE.md so future sessions know how to add contracts.

```
Append to CLAUDE.md a section called "## Contract Register Update Rules" with these instructions: (1) New contracts go through extraction first (same fields as extraction_results.json). (2) The register at Drafts/contract_register.json is the single source of truth. (3) When adding a new contract, check for duplicates by matching party_b and effective_date. (4) Recalculate the status field on every update. (5) Never overwrite the register. Read it, append the new record, and write the updated version.
```

You should see Claude confirm it appended the section to `CLAUDE.md`.

**Step 7.** Test incremental addition by simulating a new contract.

```
A new contract has arrived: MSA with Summit Supplies LLC, effective 2026-03-01, expiry 2028-02-28, term 24 months, value $156,000, payment terms Net 30. Add it to Drafts/contract_register.json following the update rules you just wrote. Set obligation_count to 0 (we have not extracted obligations yet).
```

You should see Claude confirm the register now has 21 records. The new record should have `status: "active"`.

**Step 8.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── contract-register.csv (8 records, partially outdated)
├── Drafts/
│   ├── extraction_results.json (20 records)
│   └── obligation_register.json (112 obligations)
```

**What you created:**

```
practice/
├── Drafts/
│   └── contract_register.json (21 records, validated)
├── CLAUDE.md (updated with register update rules)
```

**What Claude did, behind the scenes:**

1. Claude read both the CSV and the JSON extraction file and built a lookup table keyed on file name.
2. It compared every matching record field by field, keeping the JSON value as primary and noting discrepancies.
3. It counted obligations per contract from the obligation register and added the count to each record.
4. It calculated the status field by comparing each expiry date to today's date (2026-04-25).
5. It ran four validation checks and reported failures before fixing them.
6. It appended update rules to `CLAUDE.md` so future sessions follow the same process.
7. It added the simulated new contract as record 21, following the rules it just wrote.

## Common mistakes and how to recover

- **Symptom:** The register has duplicate entries for the same contract. **Fix:** ask Claude to "Find any records in Drafts/contract_register.json where party_b and effective_date are identical. Keep the record with more populated fields and remove the duplicate."

- **Symptom:** The status field does not update when you re-run the process next month. **Fix:** the status calculation uses today's date. Add to your prompt: "Recalculate the status field for every record using today's date before writing the file."

- **Symptom:** Obligation counts do not match after you extract obligations for the new contract. **Fix:** re-run the count: "Re-count obligations per contract from Drafts/obligation_register.json and update the obligation_count field in the register."

- **Symptom:** The JSON file grows too large to read in one pass. **Fix:** for production use with 180+ contracts, ask Claude to "Read Drafts/contract_register.json in batches of 50 records and validate each batch separately."
