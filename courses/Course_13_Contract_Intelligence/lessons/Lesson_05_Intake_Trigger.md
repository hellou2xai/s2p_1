# Lesson 5: Intake Trigger

**Time:** 35 minutes.

## The contract that sat in the inbox for three weeks

It is 11:00 Friday. Your legal team at Vanguard Manufacturing emails you a signed contract with a new supplier, Ridgeline Components Inc. The email says "FYI, fully executed, please file." You save it to the shared drive and plan to extract the data on Monday. Monday becomes Wednesday. Wednesday becomes next week. Three weeks later, the contract is still unprocessed, and Ridgeline's first delivery arrives with no matching record in your register. You need a system where dropping a file into a folder triggers extraction automatically.

## What Claude Code is going to do for you

Claude Code uses a file-watcher hook that monitors the `intake/` folder. When a new contract file appears, the hook triggers an extraction pipeline: read the contract, extract the standard fields, add the record to the register, move the processed file to `processed/`, and log the action. No manual intervention required after the file lands.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_13_Contract_Intelligence/practice/`.
3. `Drafts/contract_register.json` from Lesson 3.
4. The `intake/` and `processed/` folders in the practice root (both should be empty or nearly empty).

## Step-by-step

### Design the intake pipeline

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Define the pipeline steps in CLAUDE.md.

```
Append to CLAUDE.md a section called "## Intake Pipeline" with these rules: (1) New contract files are placed in intake/. (2) When processing a file from intake/, extract all standard fields (parties, effective_date, expiry_date, term_months, total_value_usd, payment_terms). (3) Validate that all required fields are present. If any field is missing, write a note to intake/errors.log with the file name and missing fields. Do not add to the register. (4) If validation passes, add the record to Drafts/contract_register.json with status calculated from today's date and obligation_count set to 0. (5) Move the processed file from intake/ to processed/. (6) Append a line to Drafts/intake_log.csv with timestamp, file_name, status (success or error), and notes.
```

You should see Claude confirm it appended the intake pipeline rules to `CLAUDE.md`.

### Create the processing prompt

**Step 3.** Write a reusable processing command.

```
Write a file at scripts/process_intake.md that contains the exact prompt I should paste into Claude Code to process all files in intake/. The prompt should follow the Intake Pipeline rules in CLAUDE.md. Include the instruction to read each file, extract fields, validate, update the register, move to processed/, and log.
```

You should see Claude create the file with a complete, copy-paste-ready prompt.

### Test the pipeline manually

**Step 4.** Copy a contract into the intake folder to simulate a new arrival.

```
Copy contracts/MSA_Northwind_Office_Ltd.md to intake/MSA_Ridgeline_Components_Inc.md but change the party name to "Ridgeline Components Inc", the effective date to 2026-04-01, the expiry date to 2028-03-31, and the value to $192,000.
```

You should see Claude confirm it created the test file in `intake/`.

**Step 5.** Run the intake pipeline.

```
Process all files in intake/ following the Intake Pipeline rules in CLAUDE.md.
```

You should see Claude: (1) read the file, (2) extract all six fields, (3) validate them, (4) add the record to the register, (5) move the file to `processed/`, and (6) log the action.

**Step 6.** Verify each step.

```
Confirm: (1) Is intake/ empty now? (2) Does processed/ contain MSA_Ridgeline_Components_Inc.md? (3) Does Drafts/contract_register.json contain a record for Ridgeline Components Inc? (4) Does Drafts/intake_log.csv exist and contain a success entry?
```

You should see four confirmations.

### Test the error path

**Step 7.** Create a contract file with missing data.

```
Write a file to intake/MSA_Incomplete_Vendor.md that contains only a parties section naming "Incomplete Vendor LLC" and "Vanguard Manufacturing Inc" but no dates, no term, no value, and no payment terms.
```

You should see Claude create the intentionally incomplete file.

**Step 8.** Run the pipeline again.

```
Process all files in intake/ following the Intake Pipeline rules in CLAUDE.md.
```

You should see Claude report that the file failed validation. It should not add the record to the register. It should log the error to `intake/errors.log` and to `Drafts/intake_log.csv` with status "error."

**Step 9.** Verify the error handling.

```
Read intake/errors.log and Drafts/intake_log.csv. Confirm the error was logged correctly with the file name and missing fields listed.
```

You should see the error log entry naming the missing fields (effective_date, expiry_date, term_months, total_value_usd, payment_terms).

**Step 10.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── intake/ (empty)
├── processed/ (empty)
├── Drafts/
│   └── contract_register.json (21 records)
```

**What you created:**

```
practice/
├── intake/
│   └── errors.log (1 error entry)
├── processed/
│   └── MSA_Ridgeline_Components_Inc.md
├── Drafts/
│   ├── contract_register.json (22 records)
│   └── intake_log.csv (2 entries: 1 success, 1 error)
├── scripts/
│   └── process_intake.md
├── CLAUDE.md (updated with Intake Pipeline section)
```

**What Claude did, behind the scenes:**

1. Claude read the Intake Pipeline rules from `CLAUDE.md` to know the process.
2. For the valid file, it extracted all six fields, confirmed none were missing, added the record to the register with a calculated status, moved the file to `processed/`, and logged the success.
3. For the incomplete file, it attempted extraction, detected five missing fields, wrote the error to `errors.log`, logged the failure to `intake_log.csv`, and left the file in `intake/` (or moved it, depending on your error handling preference).
4. It never modified the register for the failed file.

## Common mistakes and how to recover

- **Symptom:** The file stays in `intake/` after processing. **Fix:** Claude may not have file-move permissions. Check `.claude/settings.json` and add `Write(processed/*)` and `Write(intake/*)` to the allow list.

- **Symptom:** The register gains a duplicate because you re-ran the pipeline on an already-processed contract. **Fix:** add a deduplication check to the Intake Pipeline rules: "Before adding a record, check if party_b and effective_date already exist in the register. If they do, skip and log as 'duplicate, not added.'"

- **Symptom:** The error log does not exist after the error test. **Fix:** Claude may have skipped the logging step. Re-run with an explicit instruction: "Write the error to intake/errors.log. Create the file if it does not exist."

- **Symptom:** The intake_log.csv has inconsistent date formats. **Fix:** add "Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS) for all timestamps in intake_log.csv" to the pipeline rules.
