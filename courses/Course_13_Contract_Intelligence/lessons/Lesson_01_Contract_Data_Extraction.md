# Lesson 1: Contract Data Extraction

**Time:** 35 minutes.

## The contract pile no one wants to open

It is 08:45 Monday. Your General Counsel just forwarded an email from the board secretary: "Please confirm all active contract values, counterparties, and expiry dates for the Q3 risk review. Deadline: six weeks." You are the contract manager at Vanguard Manufacturing. You inherited 180 contracts from your predecessor, stored in a shared drive with no index, no register, and no summary. Reading each one manually would take 15 to 20 minutes per contract. That is 45 to 60 hours of reading before you can even begin building the register.

## What Claude Code is going to do for you

Claude Code reads each contract file, extracts the key commercial fields (parties, effective date, expiry date, term length, total value, and payment terms), and writes them to a structured output. You get a clean row of data per contract instead of a pile of unread documents.

## Set up

1. Claude Code installed and signed in.
2. A terminal open.
3. The practice folder for this course at `Course_13_Contract_Intelligence/practice/`.
4. Confirm these exist: `contracts/` (20 `.md` files), `contract-register.csv`, `clause-taxonomy.csv`, `intake/`, `processed/`.

## Step-by-step

### Explore the contract files

**Step 1.** Open a terminal and navigate to the practice folder.

```
cd "Course_13_Contract_Intelligence/practice"
```

Your terminal prompt should show `practice`.

**Step 2.** List the contracts directory.

```
ls contracts/
```

You should see 20 contract files with names like `MSA_Northwind_Office_Ltd.md`, `SLA_Apex_Logistics_Inc.md`.

**Step 3.** Look at one contract to understand the format.

```
cat contracts/MSA_Northwind_Office_Ltd.md
```

You should see a full contract with sections for parties, effective date, term, value, payment terms, and obligations.

### Start Claude Code and extract fields

**Step 4.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt. It reads `CLAUDE.md` automatically.

**Step 5.** Ask Claude Code to extract fields from a single contract first.

```
Read contracts/MSA_Northwind_Office_Ltd.md and extract these fields: (1) parties (both sides), (2) effective date, (3) expiry date, (4) term in months, (5) total contract value, (6) payment terms (net days). Return the result as a JSON object.
```

You should see a JSON object like:

```json
{
  "file": "MSA_Northwind_Office_Ltd.md",
  "party_a": "Vanguard Manufacturing Inc.",
  "party_b": "Northwind Office Ltd",
  "effective_date": "2025-07-01",
  "expiry_date": "2027-06-30",
  "term_months": 24,
  "total_value_usd": 284000,
  "payment_terms": "Net 30"
}
```

**Step 6.** Now extract from all 20 contracts and write the results to a file.

```
Read every file in contracts/. For each file, extract: parties, effective date, expiry date, term in months, total contract value in USD, and payment terms. Write the results to Drafts/extraction_results.json as an array of objects. Create the Drafts/ folder if it does not exist.
```

You should see Claude confirm it read all 20 files and wrote `Drafts/extraction_results.json`.

**Step 7.** Verify the output.

```
Read Drafts/extraction_results.json and tell me how many contracts are in the array. List any where the expiry date is before 2026-06-30.
```

You should see the count (20) and a list of contracts expiring within the next 14 months.

### Convert to CSV for the register

**Step 8.** Ask Claude Code to produce a CSV version.

```
Convert Drafts/extraction_results.json to a CSV file at Drafts/extracted_fields.csv. Use these column headers: file_name, party_a, party_b, effective_date, expiry_date, term_months, total_value_usd, payment_terms. Sort by expiry_date ascending.
```

You should see Claude confirm the CSV was written with 20 rows plus a header.

**Step 9.** Spot-check the CSV.

```
Read Drafts/extracted_fields.csv and show me the first 5 rows.
```

You should see five rows sorted by earliest expiry date, with all fields populated.

**Step 10.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── contracts/
│   ├── MSA_Northwind_Office_Ltd.md
│   ├── SLA_Apex_Logistics_Inc.md
│   ├── ... (18 more contract files)
├── contract-register.csv
├── clause-taxonomy.csv
├── intake/
└── processed/
```

**What you created:**

```
practice/
├── Drafts/
│   ├── extraction_results.json
│   └── extracted_fields.csv
```

**What Claude did, behind the scenes:**

1. Claude read `CLAUDE.md` for field definitions and naming conventions.
2. It opened each of the 20 contract files in `contracts/` one at a time.
3. For each file, it scanned for section headers (Parties, Term, Compensation, Payment) and extracted the six target fields.
4. It normalized dates to `YYYY-MM-DD` format and values to plain integers in USD.
5. It assembled all 20 records into a JSON array and wrote `extraction_results.json`.
6. It converted the JSON to CSV with sorted rows and consistent headers.

## Common mistakes and how to recover

- **Symptom:** Claude extracts "N/A" for the total value on some contracts. **Fix:** some contracts state value as monthly or annual amounts. Add to your prompt: "If the contract states a monthly or annual value, calculate the total value over the full term."

- **Symptom:** Date formats are inconsistent (some show MM/DD/YYYY, others YYYY-MM-DD). **Fix:** add "Normalize all dates to YYYY-MM-DD format" to your extraction prompt.

- **Symptom:** Claude misses one or two contracts in the output. **Fix:** ask Claude to "List every file name in contracts/ and confirm each one appears in the JSON array. Report any missing files."

- **Symptom:** The JSON file has a syntax error. **Fix:** ask Claude to "Read Drafts/extraction_results.json, validate the JSON syntax, and fix any errors."

- **Symptom:** Party names are inconsistent across contracts (e.g., "Northwind Office" vs. "Northwind Office Ltd"). **Fix:** this is normal. You will address normalization in Lesson 3 when building the register. For now, extract exactly what the contract says.
