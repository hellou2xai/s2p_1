# Lesson 2: Writing /spend-analyze

**Time:** 45 minutes

## The problem

It is 10:00 Tuesday. Your CPO Slacks you: "Need a Q1 vs Q4 spend comparison for direct materials. Also break out logistics separately. Two reports, same format, by 11:30."

In Lesson 1, you ran `/spend-analyze` using a pre-built solution you copied from the solutions folder. It worked. But you do not own that command yet. You did not write it. If you need to change the output format, add a column, or adjust how prior-period comparison works, you would be editing someone else's instructions without understanding why each line is there.

This lesson fixes that. You will delete the copied solution and write `spend-analyze.md` from scratch, section by section. By the end, you will have a command you understand completely, because you wrote every line.

## What Claude Code is going to do for you

You will build a reusable slash command that any team member can run from one line in the terminal. Type `/spend-analyze Q1 direct-materials`, and Claude Code reads the data, filters by period and category, computes totals and comparisons, and saves a datestamped report to `outputs/`. The same command works for any period (Q1, Q2, H1, YTD) and any category (direct-materials, logistics, indirect, mro, or all). Two reports for the CPO in under five minutes, not ninety.

## Set up

1. You have completed Lesson 1. You know what a slash command is and you have seen one run.
2. Your terminal is open and you are inside the `practice/` folder.
3. The file `.claude/commands/spend-analyze.md` exists from Lesson 1 (the copied solution).
4. The `data/` folder has `spend-transactions.csv` and `supplier-master.csv`.
5. The `outputs/` folder exists.

## Step-by-step

### Step 1. Navigate to the practice folder.

```
cd "Course_04_The_Command_Engineer/practice"
```

You should see the practice folder path in your terminal prompt.

### Step 2. Delete the copied solution.

You are going to write this command from scratch. Remove the copy you made in Lesson 1:

```
rm .claude/commands/spend-analyze.md
```

You should see no output (silent deletion means success).

If you see "No such file or directory," the file was already removed. That is fine. Continue.

### Step 3. Confirm the commands folder is empty.

```
ls .claude/commands/
```

You should see only `README.md`. The `spend-analyze.md` file is gone.

### Step 4. Open the command file in your editor.

Create a new file called `spend-analyze.md` in `.claude/commands/`. Use whichever text editor you prefer. VS Code, Notepad, or any plain-text editor works:

```
code .claude/commands/spend-analyze.md
```

You should see a blank file open in your editor. If you do not have VS Code, use `notepad .claude/commands/spend-analyze.md` on Windows, or `nano .claude/commands/spend-analyze.md` on macOS or Linux.

### Step 5. Write Section 1: Usage.

The Usage section tells Claude how to parse the arguments. Type the following into your file:

```markdown
# /spend-analyze

Produce a spend breakdown for a given period and category.

## Usage

/spend-analyze $ARGUMENTS

Parse $ARGUMENTS as: [period] [category]
- period: Q1, Q2, Q3, Q4, H1, H2, or YTD (relative to today 2026-04-25)
- category: direct-materials, logistics, indirect, mro, or all

Date ranges:
- Q1 = Jan 1 to Mar 31. Q2 = Apr 1 to Jun 30. Q3 = Jul 1 to Sep 30. Q4 = Oct 1 to Dec 31.
- H1 = Jan 1 to Jun 30. H2 = Jul 1 to Dec 31.
- YTD = Jan 1 of the current year to today.
- Use the most recent completed year for the period (2025 for Q3 and Q4, 2026 for Q1 and Q2).
```

You should see the Usage section in your editor. Save the file but keep it open.

**Why this matters:** The `$ARGUMENTS` placeholder is how Claude Code passes parameters into your command. When you type `/spend-analyze Q1 direct-materials`, Claude replaces every `$ARGUMENTS` in the file with the literal text `Q1 direct-materials`. The parsing instructions ("Parse $ARGUMENTS as: [period] [category]") tell Claude how to split that text into two named values. Without explicit parsing rules, Claude might guess wrong about which word is the period and which is the category.

### Step 6. Write Section 2: Inputs.

Below the Usage section, add the Inputs section. This tells Claude which files to open and how to filter them:

```markdown
## Inputs

data/spend-transactions.csv
  Filter rows where `date` falls inside the period.
  If category is not "all", filter rows where `category` matches.

data/supplier-master.csv
  Join on supplier_id to pull tier and risk_rating.
```

You should see both the Usage and Inputs sections in your file. Save.

**Why this matters:** Claude Code can read any file in the project folder. If you do not name the exact files, Claude might read the wrong CSV, or skip the supplier master entirely. Naming the files and the join key removes ambiguity.

### Step 7. Write Section 3: Process.

The Process section is the numbered recipe. Claude follows these steps in order:

```markdown
## Process

1. Filter spend-transactions.csv by period and category.
2. Group by supplier_id. Sum amount_usd per supplier. Sort descending.
3. Show top 10 suppliers by spend.
4. Compute total spend for the period.
5. Compute prior-period spend (same length, immediately before). Example: if period is Q1 2026, prior period is Q4 2025.
6. Compute period-over-period change (absolute USD and percentage).
7. Show category-level subtotals if category is "all".
8. Flag any supplier whose spend exceeds 120% of their annual_target_usd prorated to the period length.
```

You should see the Process section with eight numbered steps. Save.

**Why this matters:** Without numbered steps, Claude picks its own order. Sometimes it computes the prior period before filtering the current period, which leads to mismatched date ranges. Numbered steps force a predictable sequence. Step 5 is especially important: it defines "prior period" explicitly (same length, immediately before) so Claude does not compare Q1 2026 to Q1 2025 by default.

### Step 8. Write Section 4: Output format.

This section controls what the saved file looks like:

```markdown
## Output format

Save to outputs/spend-analysis-[period]-[category]-[YYYY-MM-DD].md

Three sections:
1. **Summary** (one paragraph): total spend, number of transactions, period-over-period change.
2. **Top 10 suppliers** (table): Rank, Supplier, Category, Tier, Spend (USD), % of Total, vs Prior Period.
3. **Flags** (bullet list): any suppliers exceeding prorated target.

End with an audit footer: date, source files, model, operator.
```

You should see the Output format section with the file name pattern and three-section layout. Save.

**Why this matters:** The file name pattern (`[period]-[category]-[YYYY-MM-DD]`) means every run creates a uniquely named file. You can compare April's Q1 analysis to May's Q1 analysis side by side. The three-section layout gives you a consistent shape: summary for the CPO, table for the detail, flags for the follow-up actions.

### Step 9. Write Section 5: Quality criteria.

The last section tells Claude to check its own work:

```markdown
## Quality criteria

- Every figure traces to spend-transactions.csv. No invented numbers.
- Prior-period comparison uses the same number of days.
- Table has exactly 10 rows (or fewer if fewer suppliers exist in the filter).
- File name includes the period, category, and today's date.
```

You should see all five sections complete. Save and close the file.

**Why this matters:** Quality criteria act as a self-check. Claude reads these before finishing and corrects mistakes that would otherwise slip through. "No invented numbers" prevents Claude from estimating or rounding. "Same number of days" catches the common error where Q1 (90 days) gets compared to a full year.

### Step 10. Review your complete command file.

Read the file you just wrote to confirm all five sections are present:

```
cat .claude/commands/spend-analyze.md
```

You should see the full file: a title line, then Usage, Inputs, Process, Output format, and Quality criteria. Five sections, about 40 to 50 lines total.

If any section is missing, open the file and add it before continuing.

### Step 11. Start Claude Code and test with Q1 direct-materials.

```
claude
```

At the Claude Code prompt, type:

```
/spend-analyze Q1 direct-materials
```

Claude should read your command file, parse the arguments, filter `spend-transactions.csv` to Q1 2026 and direct-materials, and produce a spend analysis. You should see the Summary, Top 10 table, and Flags sections. Claude saves the file to `outputs/`.

If Claude says it cannot find the command, check that the file is named `spend-analyze.md` (hyphen, not underscore) and sits inside `.claude/commands/`.

If the output is missing a section, open your command file and check that the Output format section lists all three sections.

### Step 12. Test with Q1 all.

Run the command again with a different category:

```
/spend-analyze Q1 all
```

This time Claude should include category-level subtotals because you passed `all` instead of a specific category. The Top 10 table should show suppliers from all four categories. The output file is named `outputs/spend-analysis-Q1-all-2026-04-25.md`.

If category subtotals are missing, check Step 7 of the Process section. It should say "Show category-level subtotals if category is 'all'."

### Step 13. Test with YTD logistics.

Run the command a third time:

```
/spend-analyze YTD logistics
```

Claude filters to January 1 through today (2026-04-25) and the logistics category only. The prior period should be the same number of days ending December 31, 2025.

You should see a smaller data set (logistics has fewer suppliers than direct-materials) and the Top 10 table may have fewer than 10 rows. That is correct. The Quality criteria section says "or fewer if fewer suppliers exist in the filter."

### Step 14. Compare your outputs.

List the output files Claude created:

```
ls outputs/
```

You should see three new markdown files, plus the original `README.md`:

- `spend-analysis-Q1-direct-materials-2026-04-25.md`
- `spend-analysis-Q1-all-2026-04-25.md`
- `spend-analysis-YTD-logistics-2026-04-25.md`

Each file has the same three-section structure. Same shape, different data. That is the point of a slash command.

### Step 15. Exit Claude Code.

```
/exit
```

You are back at the terminal prompt.

## Worked example, end to end

**Starting files:**
- `data/spend-transactions.csv` (2,508 rows of spend data across 12 months)
- `data/supplier-master.csv` (50 suppliers with tier, risk, and annual target data)
- `.claude/commands/spend-analyze.md` (the command file you wrote in Steps 5 through 9)

**Prompt typed:**

```
/spend-analyze Q1 direct-materials
```

**What Claude produced (extract):**

> **Summary.** Meridian Manufacturing spent $5,842,319 across 127 transactions on direct materials in Q1 2026 (January 1 to March 31). This represents a 6.3% increase from Q4 2025 ($5,496,210 across 118 transactions).
>
> **Top 10 suppliers**
>
> | Rank | Supplier | Category | Tier | Spend (USD) | % of Total | vs Prior Period |
> |---|---|---|---|---|---|---|
> | 1 | Great Lakes Steel | direct-materials | strategic | $1,045,200 | 17.9% | +4.2% |
> | 2 | Heartland Polymers | direct-materials | strategic | $923,400 | 15.8% | +8.1% |
> | 3 | Pacific Aluminum | direct-materials | strategic | $812,600 | 13.9% | -2.1% |
> | ... | ... | ... | ... | ... | ... | ... |
>
> **Flags**
> - Apex Electronics: Q1 spend of $648,200 exceeds 120% of prorated annual target ($600,000 quarterly).

**Output file:** `outputs/spend-analysis-Q1-direct-materials-2026-04-25.md`

**What Claude did, behind the scenes:**

1. Found `spend-analyze.md` in `.claude/commands/` and replaced `$ARGUMENTS` with `Q1 direct-materials`.
2. Parsed `Q1` into the date range January 1 to March 31, 2026. Parsed `direct-materials` as the category filter.
3. Opened `data/spend-transactions.csv` and filtered to rows where `date` fell in Q1 2026 and `category` equaled `direct-materials`. This produced 127 matching rows.
4. Grouped those rows by `supplier_id`, summed `amount_usd` per supplier, and sorted descending.
5. Opened `data/supplier-master.csv` and joined on `supplier_id` to add `tier` and `risk_rating` columns.
6. Repeated the filter for Q4 2025 (the prior period) to get a comparison baseline. Computed absolute and percentage change per supplier.
7. Checked each supplier's Q1 spend against 120% of their `annual_target_usd` divided by 4 (prorated quarterly). Flagged Apex Electronics because its $648,200 exceeded the $600,000 threshold.
8. Saved the three-section report to `outputs/spend-analysis-Q1-direct-materials-2026-04-25.md` with an audit footer.

## What you learned

You now know how to write a slash command from scratch. The five sections work together:

- **Usage** defines the interface: what the user types and how Claude parses it.
- **Inputs** points Claude to the right files and tells it how to filter.
- **Process** gives Claude a numbered recipe so the steps run in order.
- **Output format** controls the file name and the report structure.
- **Quality criteria** makes Claude check its own work before saving.

This same five-section pattern applies to every command you will build in Lessons 3 through 5.

## Common mistakes and how to recover

**Symptom:** Claude invents numbers that do not match the CSV.
**Fix:** Check the Quality criteria section. It should include "Every figure traces to spend-transactions.csv. No invented numbers." If it does, and Claude still invents data, add a stronger line: "Do not estimate, interpolate, or round. Use only values directly computed from the CSV rows." Then run the command again.

**Symptom:** The prior-period comparison shows a different time span (for example, comparing 90 days of Q1 to 365 days of the prior year).
**Fix:** Check Process step 5. It must say "same length, immediately before." If it says "prior year" or "year-over-year," Claude compares to the same quarter last year instead of the immediately preceding period. Change the wording and rerun.

**Symptom:** The command works for `Q1 direct-materials` but fails for `YTD logistics` with a parsing error.
**Fix:** Check the Usage section. The period list must include `YTD`, and the category list must include `logistics`. If you typed `Logistics` (capital L) in the Usage section but the CSV uses `logistics` (lowercase), Claude may not match. Use the exact values from the CSV.

**Symptom:** Claude produces output in the terminal but does not save a file.
**Fix:** Check the Output format section. It must start with "Save to outputs/..." in an explicit instruction. If it says "Display the following" or "Output the following" without a save instruction, Claude shows the result but does not write a file. Add the save line and rerun.

**Symptom:** You edit the command file, rerun the command, but Claude uses the old version.
**Fix:** If Claude Code is already running, it reads the command file fresh each time you invoke it. But if you edited the file outside of the Claude Code session and the file system has not synced (common with OneDrive), the old version may be cached. Exit Claude Code with `/exit`, confirm the file is saved in your editor, then restart with `claude` and rerun the command.

**Symptom:** The file saves with the wrong date in the file name (for example, yesterday's date).
**Fix:** The Quality criteria section should say "File name includes today's date." If Claude uses the wrong date, add an explicit line to the Output format section: "Use today's date (2026-04-25) in the file name, not the data's date range." After the course, update this to "Use today's actual date" so it stays current.

---

**Next:** In Lesson 3, you will write `/anomaly-detect`, a command that scans spend data for transactions above a configurable threshold and flags duplicate PO patterns. You will learn to handle numeric arguments and structured alert output.
