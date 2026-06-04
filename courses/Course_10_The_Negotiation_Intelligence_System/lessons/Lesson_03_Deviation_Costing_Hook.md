# Lesson 3: Deviation Costing with a PostToolUse Hook

**Course:** The Negotiation Intelligence System
**Time:** 50 minutes

---

## Opening scenario

It is 11:00 on Monday. Your intelligence brief is done. Your VP calls. She asks one question: "What does each of Redline's proposed changes actually cost us, in dollars, per year?" You open the deviation table you drafted last month for a different contract. It has four rows with dollar figures and three rows that say "TBD." That table went to a supplier meeting. Nobody caught the TBDs until the supplier's lawyer pointed them out.

That will not happen this time. In this lesson, you build a PostToolUse hook in Claude Code. The hook fires automatically every time Claude writes a deviation analysis file. It checks that every row in the table has a dollar figure. If any row is missing a figure, the hook prints an error and flags the row by name. The deviation table cannot exist on disk with a blank cost cell.

---

## What Claude Code is going to do for you

You will create a Python script that acts as a PostToolUse hook. Every time Claude Code writes to `Outputs/deviation-costs.md`, the hook runs. It reads the file, parses the deviation table, and checks that every row in the "Annual Cost Impact" column starts with a dollar sign. If all rows pass, the hook prints the total annual cost impact. If any row fails, the hook prints an error naming the specific row and exits with a non-zero code, which tells Claude Code the file is not ready. You will test the hook by forcing a failure, then correcting it.

---

## Set up

1. Confirm you completed Lesson 2. Check for the intelligence brief:

```
ls Outputs/intelligence-brief.md
```

You should see the file listed.

2. Navigate to the practice folder if you are not already there:

```
cd "Course_10_The_Negotiation_Intelligence_System/practice"
```

3. Create the `.claude/` folder if it does not already exist:

```
mkdir -p .claude
```

4. Check whether `settings.json` already exists:

```
ls .claude/
```

If `settings.json` exists, you will add the hook to it in Step 4. If it does not exist, you will create it.

5. Start Claude Code:

```
claude
```

6. Restate the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/. Save all output to Outputs/.
```

**Folder layout at the start of this lesson:**

```
practice/
├── CLAUDE.md
├── .claude/
│   └── settings.json          (may not exist yet)
├── data/
│   ├── current-contract.md
│   └── proposed-renewal.md
└── Outputs/
    ├── system-design.md
    └── intelligence-brief.md
```

---

## Step-by-step

### Step 1: Produce a first deviation table, without the hook

Ask Claude Code to compare the two contract documents and produce the deviation table.

```
Read data/current-contract.md and data/proposed-renewal.md. Create a deviation table and save it to Outputs/deviation-costs.md. The table must have five columns: Term, Current Value, Proposed Value, Direction (increase, decrease, or restriction), and Annual Cost Impact (in USD). Include every term that differs between the two documents.
```

You should see Claude Code create `Outputs/deviation-costs.md`. Open it. Some rows will have dollar figures. Others may say "TBD," "N/A," or be blank. That inconsistency is exactly what the hook will catch.

If the file is not created, check that `Outputs/` exists: `mkdir -p Outputs`.

### Step 2: Write the hook script

Ask Claude Code to create the Python hook.

```
Create a Python script at scripts/check-deviation-costs.py. The script must do the following:
1. Read the file Outputs/deviation-costs.md.
2. Find the markdown table in that file.
3. For each row in the table, read the value in the "Annual Cost Impact" column.
4. If a cell in that column does not start with "$" or "-$", print: "ERROR: [term name] is missing an annual cost impact figure." Collect all such errors.
5. If there are any errors, print all of them and exit with code 1.
6. If all cells have dollar figures, sum the values (ignore commas and dollar signs when parsing), print "Total annual cost impact: $[sum]", and exit with code 0.
Use only Python standard library modules. No pip installs required.
```

You should see Claude Code create `scripts/check-deviation-costs.py`. The script uses `re` for parsing and `sys` to set the exit code.

If Claude creates the file outside `scripts/`, ask it to move it: "Move that script to scripts/check-deviation-costs.py."

### Step 3: Test the script manually

Exit Claude Code and test the script directly in your terminal.

```
/quit
```

Run the script against the deviation table you created in Step 1:

```
python scripts/check-deviation-costs.py
```

You should see one of two things. If some rows were missing figures: error messages naming the rows. If all rows had figures: "Total annual cost impact: $[amount]."

If you see a Python error like `FileNotFoundError`, check that you are running the command from the `practice/` folder, not from a parent folder.

### Step 4: Register the hook in settings.json

Open `.claude/settings.json` in a text editor (Notepad, VS Code, or any editor you have). If the file does not exist, create it. Add the following content. If the file already has content, add the `hooks` block inside the existing JSON object:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "python scripts/check-deviation-costs.py"
      }
    ]
  }
}
```

Save the file.

You should have a valid JSON file. If you are not sure the JSON is valid, paste it into `jsonlint.com` and confirm no errors.

### Step 5: Start Claude Code and trigger the hook

Start Claude Code again:

```
claude
```

Now ask Claude to rewrite the deviation table with all costs populated:

```
Read data/current-contract.md and data/proposed-renewal.md. Rewrite Outputs/deviation-costs.md with a complete deviation table. For every row, calculate and fill in the Annual Cost Impact in USD. The contract is $9.2M per year. Do not leave any cell in the Annual Cost Impact column blank or marked TBD.
```

You should see Claude Code write the file. Immediately after the write, the hook runs. If all rows have dollar figures, you will see: "Total annual cost impact: $[amount]" in the terminal output. If any row is missing, you will see an error.

If the hook does not run, check that you saved `settings.json` with the correct JSON structure and restart Claude Code.

### Step 6: Force a failure to confirm the hook works

Test that the hook catches a real problem.

```
Rewrite Outputs/deviation-costs.md. For the "Force majeure" row, put "TBD" in the Annual Cost Impact column instead of a dollar figure. Fill in all other rows with their correct dollar figures.
```

You should see Claude Code write the file, the hook fire, and this message appear: "ERROR: Force majeure is missing an annual cost impact figure." Claude Code will also see this message and know the file is incomplete.

### Step 7: Calculate and fill the missing figure

```
Calculate the annual cost impact of removing supply chain disruption from the force majeure clause. Assume TransGlobal had one supply chain disruption event in the last 3 years that cost $420,000 in unplanned freight premiums. Annualize that risk exposure. Update the force majeure row in Outputs/deviation-costs.md with the result.
```

You should see Claude Code calculate approximately $140,000 per year ($420,000 divided by 3 years) and update the row. The hook fires again. This time it prints the total with no errors.

### Step 8: Exit Claude Code

```
/quit
```

---

## Worked example, end to end

**Starting files:**

- `data/current-contract.md`: CTR-2024-LG-001, active terms including $9.2M/year pricing, 96% OTD SLA, 180-day notice period, and broad force majeure clause.
- `data/proposed-renewal.md`: Redline's three proposed changes: 12% price increase, narrowed force majeure, 90-day notice period.

**The prompts you type, in order:**

```
Read data/current-contract.md and data/proposed-renewal.md. Create a deviation table at Outputs/deviation-costs.md with columns: Term, Current Value, Proposed Value, Direction, Annual Cost Impact.
```

```
Create a PostToolUse hook script at scripts/check-deviation-costs.py that reads Outputs/deviation-costs.md, checks every Annual Cost Impact cell for a dollar figure, and prints either errors or a total.
```

After registering the hook in `.claude/settings.json`:

```
Rewrite Outputs/deviation-costs.md with all Annual Cost Impact cells populated. The contract is $9.2M per year.
```

**What you should see after the hook runs:**

```
Total annual cost impact: $1,378,000
```

Broken down as:

| Term | Current Value | Proposed Value | Direction | Annual Cost Impact |
|---|---|---|---|---|
| Base logistics rate | $9.2M/year | $10.304M/year | Increase | $1,104,000 |
| Force majeure scope | Supply chain disruption covered | Removed | Restriction | $140,000 |
| Auto-renewal notice | 180 days | 90 days | Restriction | $134,000 |

Note: the notice period cost reflects the estimated cost of an accelerated re-sourcing process if TransGlobal must replace Redline with 90 days instead of 180.

**Finished artifact:** `Outputs/deviation-costs.md`, a three-row deviation table with dollar figures in every cell, and `scripts/check-deviation-costs.py`, the hook that validates it automatically.

**What Claude Code did behind the scenes:**

1. Claude Code read both contract files and compared them term by term, identifying the three changed items.
2. For the base rate change, it multiplied the current contract value by 12% to get $1,104,000.
3. For the force majeure change, it used the historical disruption cost ($420,000 over 3 years) to estimate an annualized exposure of $140,000.
4. For the notice period change, it estimated the cost of a compressed re-sourcing timeline based on the contract value and a reasonable market assumption.
5. It wrote the deviation table to `Outputs/deviation-costs.md`.
6. The PostToolUse hook fired, parsed the markdown table, checked each Annual Cost Impact cell, and printed the total.
7. When the hook was tested with a missing cell, it printed the error and exited with code 1, which Claude Code logged as a validation failure.

---

## Common mistakes and how to recover

**Symptom:** The hook does not fire after Claude Code writes the file.
**Fix:** Check that `settings.json` is saved in `.claude/` inside your practice folder, not in a parent folder. Open the file and confirm the JSON is valid. Restart Claude Code after any change to `settings.json`.

**Symptom:** The hook prints a Python error: `ModuleNotFoundError`.
**Fix:** The script should use only standard library modules (`re`, `sys`, `pathlib`). Ask Claude: "Rewrite scripts/check-deviation-costs.py using only Python standard library modules. No third-party packages."

**Symptom:** The hook reports an error for a row that has a figure like "$1,104,000".
**Fix:** The parser may not handle commas in numbers. Ask Claude: "Update the check in scripts/check-deviation-costs.py to strip commas before checking for a dollar sign."

**Symptom:** The total printed by the hook does not match your manual calculation.
**Fix:** Read the individual row values. The force majeure and notice period costs depend on assumptions. Tell Claude the assumptions explicitly: "Use $420,000 over 3 years for force majeure. Use $134,000 for the notice period cost."

**Symptom:** The hook fires on every file write, not just `Outputs/deviation-costs.md`.
**Fix:** Add a filename check inside the script. At the top of the script, read the filename from an environment variable or argument, and exit with code 0 immediately if the file is not `deviation-costs.md`.

---

## You are done with Lesson 3 when

- `Outputs/deviation-costs.md` exists with three rows and a dollar figure in every Annual Cost Impact cell.
- `scripts/check-deviation-costs.py` exists and runs without errors from the terminal.
- The hook is registered in `.claude/settings.json` under `PostToolUse`.
- You tested the hook with a missing figure and confirmed it prints the error.
- The hook prints a total annual cost impact when all rows pass.

Move to Lesson 4 when ready.
