# Lesson 3: Self-Correcting Feedback Loop: Validate Outputs and Fix Errors Automatically

**Time:** 50 minutes.

## It is 08:30 on Monday. The sub-agents finished. Something is wrong with one of the outputs.

You run your Monday briefing system for the third week. Four sub-agents completed. You open `Drafts/contract_review.md` to spot-check. The Facilities contract row shows no supplier name in the Supplier column. It reads "N/A." The savings tracker has a percent complete figure of 147% for LOG-002, which is mathematically possible but was not flagged as unusual. The scorecard file has a trend column that says "unknown" for three suppliers.

These are the kinds of errors that slip through when you are moving fast. They are small, but they destroy VP credibility. If your 09:00 briefing says "Supplier: N/A" or "147% complete," your VP loses confidence in the whole system.

This lesson teaches you to build a validation step that catches these errors automatically and asks Claude Code to fix them before the output leaves `Drafts/`.

## What Claude Code is going to do for you

Claude Code will run a validator after each sub-agent completes. The validator checks the output file against a set of quality rules: no missing supplier names, no percent values above 110%, no "unknown" trend values, and no dates in the wrong format. When the validator finds a violation, it writes a correction instruction and runs a fix pass on the same file. You do not have to open the file, find the error, and correct it manually. The feedback loop handles it.

This is Claude Code in action. The capability described in this lesson applies to Claude Code in the terminal. It does not apply to Claude AI Web or Claude Desktop with Cowork.

## Set up

1. Confirm Lessons 1 and 2 are complete and all four output files exist:

```
ls "Course_11_The_Category_Management_System/practice/Drafts/"
```

You should see: `orchestrator_plan.md`, `savings_tracker.md`, `contract_review.md`, `scorecard_refresh.md`, `ps_update.md`.

If any file is missing, complete Lesson 2 first.

2. Navigate to the practice folder and start Claude Code:

```
cd "Course_11_The_Category_Management_System/practice"
claude
```

3. Restate the read-only rule:

```
The files in data/ are source data. Do not edit any file in data/.
Save all corrected output to Drafts/. Do not create files outside Drafts/ or Outputs/.
```

**Folder layout:**

```
practice/
├── CLAUDE.md
├── data/                          (read-only)
├── Drafts/
│   ├── orchestrator_plan.md
│   ├── savings_tracker.md
│   ├── contract_review.md
│   ├── scorecard_refresh.md
│   └── ps_update.md
└── Outputs/
```

## Step-by-step

### Step 1: Define the validation rules

Before running the validator, give Claude Code the rules it will check against.

```
I am going to describe five validation rules for the sub-agent output files.
Confirm you understand each one before we run the validator.

Rule 1: No supplier name cell in any Drafts/ output file may be empty, "N/A", "Unknown", or "None".
Rule 2: No percent complete value may exceed 110%. Values above 110% indicate a data error.
Rule 3: No trend value in scorecard files may be "unknown". Valid values are: up, down, flat.
Rule 4: All dates must be in YYYY-MM-DD format. Any date in MM/DD/YYYY or spelled-out format is an error.
Rule 5: Every file in Drafts/ must have at least one data row below the header. Empty tables are errors.

Confirm you have these five rules.
```

You should see Claude Code list all five rules back to you and confirm. If it paraphrases a rule incorrectly, correct it before moving on.

### Step 2: Validate the savings tracker

Run Claude Code against `Drafts/savings_tracker.md` using the rules you defined.

```
Validate Drafts/savings_tracker.md against the five rules.
For each violation found, write a one-line description: which rule was violated, which row, and the current value.
If no violations are found, say "PASS: savings_tracker.md".
```

You should see a result like "PASS: savings_tracker.md" or a short list of violations. A common issue is a percent complete value above 110% if the realized savings exceeded the target.

### Step 3: Validate the contract review

```
Validate Drafts/contract_review.md against the five rules.
For each violation, write: rule number, row identifier (use Contract ID), and the bad value.
If the Supplier column has any empty or "N/A" value, that is a Rule 1 violation.
```

You should see either "PASS" or a list of violations with contract IDs. If the Facilities contract row is missing a supplier name, you will see: "Rule 1 violation: CTR-010, Supplier column is empty."

### Step 4: Fix violations automatically

If violations were found in Step 3, run the fix pass now.

```
Fix all violations found in Drafts/contract_review.md.
For Rule 1 violations: read data/contract-calendar.csv and look up the supplier name for each contract ID. Fill in the correct name.
For Rule 4 violations: convert any dates to YYYY-MM-DD format.
Overwrite Drafts/contract_review.md with the corrected version.
After saving, re-validate against the five rules and confirm the file now passes.
```

You should see Claude Code read the source data, apply the corrections, write the file, and then run validation again. The final message should be "PASS: contract_review.md."

If Claude Code cannot find the supplier name in `data/contract-calendar.csv`, it will say so. Tell it: "The supplier column is `supplier` and the contract ID column is `contract_id`. Match on contract_id."

### Step 5: Validate the scorecard file

```
Validate Drafts/scorecard_refresh.md against the five rules.
Pay special attention to Rule 3: check every value in the trend column.
List any supplier names where trend is "unknown" or blank.
```

You should see either "PASS" or a list of supplier names with missing trend values. Three to five suppliers from the Logistics and Raw materials categories may show "unknown" if there was only one quarter of data available for comparison.

### Step 6: Fix unknown trend values

```
Fix Rule 3 violations in Drafts/scorecard_refresh.md.
For each supplier where trend is "unknown" or blank:
- Read data/supplier-scorecards.csv.
- Find all rows for that supplier.
- If only one quarter of data exists, set trend to "insufficient data" rather than "unknown".
- If two or more quarters exist, calculate the trend: compare the most recent quarter's average score to the previous quarter's average score. If higher, set "up". If lower, set "down". If within 0.1 points, set "flat".
Overwrite Drafts/scorecard_refresh.md with corrections.
Re-validate and confirm it passes.
```

You should see Claude Code work through the supplier list, find the quarter data, and apply the trend logic. The file will be rewritten with no "unknown" values.

### Step 7: Validate the professional services update

```
Validate Drafts/ps_update.md against the five rules.
Also check: does the file include at least one supplier name? Does it include at least one dollar figure? Does it include at least one date?
These are additional quality checks for briefing-ready output.
```

You should see either a clean pass or a list of findings. If the file lacks supplier names, Claude Code will flag it.

### Step 8: Run a final validation pass across all files

```
Run a final validation pass on all five files in Drafts/:
orchestrator_plan.md, savings_tracker.md, contract_review.md, scorecard_refresh.md, ps_update.md.
For each file, report: PASS or FAIL. If FAIL, list the rule numbers violated.
```

You should see five lines, each starting with PASS or FAIL. All five should pass after the corrections in Steps 4 and 6.

If any file still fails, run a targeted fix for that file using the same approach as Steps 4 and 6.

### Step 9: Quit Claude Code

```
/quit
```

## Worked example: fixing a missing supplier name

**The prompt you type:**

```
Validate Drafts/contract_review.md. Rule 1: no supplier name may be empty or "N/A".
If you find a violation, look up the correct supplier name in data/contract-calendar.csv using the contract_id.
Fix the violation, overwrite the file, and re-validate.
```

**Folder layout:**

```
practice/
├── data/
│   └── contract-calendar.csv     (input: source of supplier names)
└── Drafts/
    └── contract_review.md        (input and output: fixed in place)
```

**What you should see:**

Claude Code reports the violation, for example: "Rule 1 violation: CTR-007, Supplier is blank." It then reads `data/contract-calendar.csv`, finds the row where `contract_id` is CTR-007, extracts the supplier name "Horizon Distribution," writes the corrected row to the file, and confirms: "PASS: contract_review.md. One correction applied (CTR-007, Supplier: Horizon Distribution)."

**What Claude Code did behind the scenes:**

1. Claude Code read `Drafts/contract_review.md` line by line and checked the Supplier column for empty strings, "N/A," "Unknown," or "None."
2. It found one violation: CTR-007 had a blank Supplier field.
3. It opened `data/contract-calendar.csv` and searched for the row where `contract_id` equals CTR-007.
4. It extracted the `supplier` value from that row: "Horizon Distribution."
5. It wrote the corrected row back into the table in `Drafts/contract_review.md`.
6. It re-read the file and checked all five rules again, finding no further violations.
7. It reported "PASS" with a one-line summary of the correction applied.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Claude Code validates the file but finds no violations, even when you can see an empty cell. | The validation prompt must be specific. Add: "Treat a cell that contains only whitespace as empty. Treat a cell that reads 'N/A', 'None', 'Unknown', or 'n/a' (any case) as a Rule 1 violation." |
| The fix pass changes the wrong row. | Claude Code may have matched on a partial name. Add to the fix prompt: "Match contract_id exactly. Do not match partial strings." |
| After re-validation, the file fails a different rule than before. | The fix introduced a new issue. Ask: "What change did you make in the last fix pass? Show me the diff." Then correct the new issue. |
| The trend calculation produces inconsistent results across suppliers. | Specify the formula explicitly: "Average the four score columns (quality, delivery, cost, responsiveness) for each quarter. Compare the most recent quarter average to the previous quarter average. Difference greater than 0.1 = up or down. Within 0.1 = flat." |
| Claude Code reports PASS but the file still has an error you can see. | Read the file yourself: "Read Drafts/contract_review.md and show me the full content." Visual inspection beats trusting the validator alone for critical output. |

## You are done with Lesson 3 when

- You can define five validation rules and apply them to a Drafts/ output file.
- Claude Code has found and fixed at least one violation automatically.
- All five files in Drafts/ report PASS on a final validation run.

Move to Lesson 4 when ready.
