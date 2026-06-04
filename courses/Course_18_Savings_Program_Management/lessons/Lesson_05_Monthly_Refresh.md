# Monthly Savings Refresh

It is 08:30 on the last Monday of the month. Finance just dropped the updated transaction file into the shared folder. You need to rerun the savings analysis, update the variance table, refresh the scenario projections, and produce a new CFO memo. Last month this took you four hours. This month you want it done in ten minutes. You build a slash command that runs the entire pipeline from a single prompt.

## The S2P problem

Savings tracking is a monthly cycle. Every month, a new transaction file arrives. Every month, you repeat the same steps: match transactions to initiatives, compute realized savings, update the variance, recalculate projections, and rewrite the memo. The work is identical each month. The only thing that changes is the data. Doing this by hand every month is a guaranteed source of errors, because one skipped step or one wrong cell reference produces a number the CFO will question.

## What Claude Code does for you

You create a Claude Code slash command called `/savings-refresh` that runs the full pipeline: read the transaction file, match to initiatives, calculate realized savings, run three scenarios, and draft the CFO memo. When next month's transaction file drops, you run one command. The output is a fresh memo with updated numbers. The methodology, scenario assumptions, and memo format all come from CLAUDE.md, so nothing drifts between months.

## Set up

1. Lessons 1 through 4 completed. CLAUDE.md has the methodology, scenarios, and reporting standards.
2. Claude Code open in `Course_18_Savings_Program_Management/practice/`.
3. The `.claude/commands/` directory exists (or you will create it).

## Step-by-step

### Step 1. Create the commands directory.

```
mkdir -p .claude/commands
```

You should see the `.claude/commands/` directory created inside the practice folder.

### Step 2. Write the slash command file.

Create the slash command that automates the full savings refresh pipeline.

```
Create a file at .claude/commands/savings-refresh.md with this content:

Run the monthly savings refresh pipeline. Follow these steps in order:

1. Read data/sourcing-initiatives-log.csv to load the 8 initiatives with targets and baselines.
2. Read data/q1-q3-transactions.csv to load all transactions.
3. For each hard savings initiative (SAV-001 through SAV-005), calculate realized savings using the formula in CLAUDE.md: (baseline_rate - rate_applied) x volume, summed by initiative.
4. For non-hard initiatives (SAV-006, SAV-007, SAV-008), use the ytd_realized_usd from the initiatives log.
5. Build the initiative summary table with columns: initiative_id, initiative_name, savings_type, ytd_target_usd, realized_savings_usd, variance_usd, variance_pct, status.
6. Save the summary to Drafts/savings-summary-ytd.csv.
7. Calculate three Q4 scenarios (base, upside, risk-adjusted) using the assumptions in CLAUDE.md.
8. Save the scenario comparison to Drafts/scenario-projections.csv.
9. Draft the CFO memo following the format in CLAUDE.md: headline number first, initiative variance table sorted by largest gap, three-scenario outlook, and exactly three recommended actions with dollar amounts and dates.
10. Save the memo to Drafts/cfo-memo-savings-review.md.
11. Report what you produced and the headline savings number.
```

You should see the file saved at `.claude/commands/savings-refresh.md`.

### Step 3. Test the slash command.

```
/savings-refresh
```

You should see Claude Code execute all 11 steps. It reads the data files, calculates savings, builds the summary, runs scenarios, and drafts the memo. At the end, it reports the headline number and lists the three files it produced.

### Step 4. Verify the outputs.

```
Read Drafts/savings-summary-ytd.csv and show me the totals row.
```

You should see the total YTD realized savings matching the figure from Lesson 2 (approximately $6,855,836).

### Step 5. Verify the memo.

```
Read Drafts/cfo-memo-savings-review.md and show me the first paragraph.
```

You should see the headline number in the first sentence, the gap in the second, and the scenario range in the third.

## Worked example

**Starting files:**
- `data/sourcing-initiatives-log.csv` (8 initiatives).
- `data/q1-q3-transactions.csv` (437 transactions).
- `CLAUDE.md` with methodology, scenarios, and reporting standards.
- `.claude/commands/savings-refresh.md` (the slash command).

**What you type:**

```
/savings-refresh
```

**What you should see:** Claude Code processes all 11 steps and produces three files: `Drafts/savings-summary-ytd.csv`, `Drafts/scenario-projections.csv`, and `Drafts/cfo-memo-savings-review.md`. The final output reports: "Savings refresh complete. Headline: $6,855,836 realized YTD against $9,000,000 target. Three files saved to Drafts/."

**What Claude did, behind the scenes:**

1. Read the slash command file to load the 11-step pipeline.
2. Read CLAUDE.md to load the methodology, scenario assumptions, and reporting format.
3. Read both data files and matched 437 transactions to 5 hard-savings initiatives.
4. Calculated per-transaction savings and summed by initiative.
5. Added the three non-hard initiatives using their log figures.
6. Ran three Q4 projections using the scenario assumptions from CLAUDE.md.
7. Drafted the CFO memo following the headline-first format.

## Common mistakes and how to recover

- **Symptom:** The slash command does not appear when you type `/savings`. **Fix:** Check that the file is saved at `.claude/commands/savings-refresh.md`, not `.claude/commands/savings_refresh.md` or another location. The file name must match exactly.

- **Symptom:** The command runs but produces different numbers from Lesson 2. **Fix:** Check whether CLAUDE.md was modified between lessons. The slash command reads CLAUDE.md each time. If someone changed the methodology or scenario assumptions, the numbers will change.

- **Symptom:** The memo is missing the scenario section. **Fix:** The slash command instructions list the scenario step (step 7) and the memo step (step 9). If either step is missing from the command file, Claude Code skips it. Read the command file and confirm all 11 steps are present.

- **Symptom:** The Drafts folder does not exist and the save fails. **Fix:** Create the Drafts folder first: `mkdir -p Drafts`. The slash command assumes the folder exists. You can add a `mkdir -p Drafts` step at the top of the command file to prevent this.
