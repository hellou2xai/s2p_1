# Lesson 5: Chaining Commands: /rfp-launch and /savings-update

**Time:** 50 minutes

---

## The S2P problem

It is 09:00 Friday. Your CPO Slacks you: "We need to start a sourcing event for direct materials. Several contracts are expiring. Get me a brief with baseline spend, contract status, and a timeline. Also, I need the quarterly savings tracker before the board call at 15:00."

Two deliverables, both due today. You already have commands that pull spend data (`/spend-analyze`) and scan contracts (`/contract-sweep`). But those produce separate outputs. The CPO does not want two files. She wants a single sourcing brief that combines spend and contract data, plus a savings tracker that compares actuals to targets. Building each from scratch means writing a long prompt, pulling the right columns, formatting the output, and hoping you did not miss a step.

This lesson solves that. You will build two commands that read the same source data your earlier commands use, but produce combined deliverables. The key idea: design command outputs so they feed naturally into other commands.

## What Claude Code is going to do for you

By the end of this lesson you will have two new slash commands in Claude Code (in the terminal). `/rfp-launch direct-materials 2026-07-31` produces a one-page sourcing brief with baseline spend, expiring contracts, supplier risk flags, and a timeline. `/savings-update Q1` produces a variance tracker comparing actual spend to prorated annual targets. Both commands run in under 60 seconds and save datestamped files to `outputs/`.

## Set up

You should already have these in place from Lessons 1 through 4. Confirm each one before continuing.

1. Claude Code installed and signed in.
2. Your terminal open in the `practice/` folder inside Course 04.
3. Four command files in `.claude/commands/`: `spend-analyze.md`, `anomaly-detect.md`, `scorecard-refresh.md`, and `contract-sweep.md`.
4. The `data/` folder with all four CSV files: `spend-transactions.csv`, `supplier-master.csv`, `contract-register.csv`, and `scorecard-history.csv`.
5. The `outputs/` folder exists and contains at least one output from a previous lesson.

If any of these is missing, go back to the relevant lesson and complete it first.

---

## Part A: Building /rfp-launch (30 minutes)

### Why this command matters

A sourcing brief is the document that kicks off an RFP. It tells the sourcing team: here is how much we spend in this category, here are the contracts about to expire, here are the risky suppliers, and here is the timeline. Without it, the RFP starts with guesswork.

Today you would open the spend analysis, copy the top suppliers, open the contract sweep, copy the expiring contracts, paste both into a Word doc, add a timeline by hand, and write a summary paragraph. That takes 45 to 90 minutes. The `/rfp-launch` command does all of it in one step.

### The chaining concept

Look at what `/rfp-launch` needs:

| Data needed | Where it comes from | Which existing command uses it |
|---|---|---|
| 12-month spend by supplier | spend-transactions.csv | /spend-analyze |
| Supplier tier, risk, status | supplier-master.csv | /spend-analyze |
| Contract expiry dates | contract-register.csv | /contract-sweep |
| Auto-renew notice windows | contract-register.csv | /contract-sweep |

The `/rfp-launch` command reads the same CSV files that `/spend-analyze` and `/contract-sweep` read. It does not call those commands. It reads the same sources and combines the results into a single brief. This is what "chaining" means in practice: designing commands so they share input files and output structures.

### Step 1: Study the solution template

Read the solution file so you understand what the finished command looks like.

```
Read solutions/rfp_launch_solution.md and summarize the six output sections.
```

You should see a summary listing: Category overview, Top 5 suppliers by spend, Contract status, Risk flags, Proposed timeline, and Recommendation.

### Step 2: Create the command file

Create the `/rfp-launch` command file.

```
Create the file .claude/commands/rfp-launch.md with the content from solutions/rfp_launch_solution.md
```

You should see Claude Code confirm it created `.claude/commands/rfp-launch.md`.

If you see "permission denied" or "path not found", check that your terminal is in the `practice/` folder. Run `pwd` to confirm.

### Step 3: Verify the command file exists

Confirm the file landed in the right place.

```
List all files in .claude/commands/ and show me the first 10 lines of rfp-launch.md
```

You should see six files in `.claude/commands/` (the four from earlier lessons, plus `rfp-launch.md` and the README). The first lines should show the version comment and the `# /rfp-launch` heading.

### Step 4: Test with direct-materials

Run the command with the direct-materials category and a July 31 deadline.

```
/rfp-launch direct-materials 2026-07-31
```

You should see Claude Code read `spend-transactions.csv`, `supplier-master.csv`, and `contract-register.csv`. It will filter to the direct-materials category, compute spend totals, identify expiring contracts, build a timeline from today (2026-04-25) to the deadline (2026-07-31), and save the brief to `outputs/`.

The output file should be named something like `outputs/rfp-brief-direct-materials-2026-04-25.md`.

If you see an error about missing columns or no data, check that the category argument matches the values in the CSV. The valid categories are: `direct-materials`, `logistics`, `indirect`, and `mro`. Capitalization matters.

### Step 5: Verify the output

Read the output file and check it against the quality criteria.

```
Read the rfp-brief file in outputs/ and answer these questions: 1. Does the Category overview name total 12-month spend and number of active suppliers? 2. Does the Top 5 table have exactly 5 rows with spend figures? 3. Does the Contract status paragraph count active, expiring, and expired contracts? 4. Do the Risk flags name specific suppliers? 5. Does the Proposed timeline use dates computed from 2026-07-31? 6. Does the Recommendation name at least one supplier and one dollar figure?
```

You should see "yes" to all six questions. If any answer is "no", open the command file and check the relevant section of the Process instructions.

### Step 6: Compare to a standalone spend-analyze run

This step shows you the chaining relationship. Run `/spend-analyze` for the same category and compare.

```
/spend-analyze YTD direct-materials
```

You should see a spend analysis output in `outputs/`. Now compare the two files.

```
Compare the top suppliers in the rfp-brief file to the top suppliers in the spend-analysis file. Are the spend figures consistent?
```

You should see that the top suppliers and their spend figures match between the two outputs. The rfp-brief pulls from the same source data. This consistency is why chaining works: same source, same numbers, different deliverable.

---

## Part B: Building /savings-update (15 minutes)

### Why this command matters

Before every board call, the CPO needs to know: are we on track to hit our savings targets? The savings tracker compares actual spend per supplier to their annual target (prorated to the period), flags overspends, and recommends actions. Without it, the CPO walks into the board meeting with "we think we are on track" instead of "we are $142,000 under target across 38 suppliers, with 3 flagged for overspend."

### Step 7: Create the savings-update command

Create the command file from the solution.

```
Create the file .claude/commands/savings-update.md with the content from solutions/savings_update_solution.md
```

You should see Claude Code confirm it created `.claude/commands/savings-update.md`.

### Step 8: Verify all six commands exist

Check that your command library is complete.

```
List all .md files in .claude/commands/ (excluding the README) and show the first line of each
```

You should see six files: `spend-analyze.md`, `anomaly-detect.md`, `scorecard-refresh.md`, `contract-sweep.md`, `rfp-launch.md`, and `savings-update.md`. Each should start with a version comment like `<!-- v1.0 2026-04-25 Initial. -->`.

### Step 9: Test with Q1

Run the savings tracker for Q1.

```
/savings-update Q1
```

You should see Claude Code read `spend-transactions.csv` and `supplier-master.csv`. It will filter spend to Q1 (2026-01-01 to 2026-03-31), compute prorated targets for each supplier, calculate variance, and save to `outputs/`.

The output file should be named something like `outputs/savings-tracker-Q1-2026-04-25.md`.

If you see all zeros in the variance column, check that the command is prorating the annual target correctly. The proration formula is: `annual_target_usd x (days_in_period / 365)`. For Q1, that is 90 days out of 365.

### Step 10: Verify the output

Check the savings tracker against the quality criteria.

```
Read the savings-tracker file in outputs/ and answer these questions: 1. Does the Portfolio summary show total actual spend, total prorated target, and total variance in USD and percentage? 2. Does the Supplier variance table include columns for Actual, Prorated Target, Variance, and Flag? 3. Are suppliers with variance above +10% flagged as overspend? 4. Are suppliers with variance below -15% flagged as demand shortfall? 5. Does the Recommended actions section have exactly three bullet points, each naming a specific supplier?
```

You should see "yes" to all five questions.

---

## Part C: Understanding the chaining pattern (5 minutes)

### Step 11: Map the data flow across all six commands

This is the conceptual step that ties the course together. Ask Claude Code to map how data flows through your command library.

```
Read all six command files in .claude/commands/. For each command, list: (1) which CSV files it reads, (2) what parameters it takes, and (3) what output file it produces. Then draw a table showing which commands share the same input files.
```

You should see a table like this:

| CSV File | Used by |
|---|---|
| spend-transactions.csv | /spend-analyze, /anomaly-detect, /rfp-launch, /savings-update |
| supplier-master.csv | /spend-analyze, /anomaly-detect, /scorecard-refresh, /contract-sweep, /rfp-launch, /savings-update |
| contract-register.csv | /contract-sweep, /scorecard-refresh, /rfp-launch |
| scorecard-history.csv | /scorecard-refresh |

This shared-input pattern is what makes the command library consistent. Every command that reports supplier spend pulls from the same `spend-transactions.csv`. If the data changes, all commands reflect the change.

### The design principle

When you build new commands in the future, follow this pattern:

1. **Same source, different deliverable.** Commands that need similar data should read the same CSV files, not duplicate data into intermediate files.
2. **Consistent column names.** Every command that groups by `supplier_id` uses the same column name. No aliases, no renaming.
3. **Datestamped outputs.** Every output file includes the date, so you can compare Monday's run to Friday's run.
4. **Audit footers.** Every output ends with a footer that names the source files, so the reader can trace any number back to the data.

---

## Worked example: the full Friday morning

Here is the complete sequence for the CPO's request. You would type these two commands in Claude Code (in the terminal), one after the other.

**Command 1: Generate the sourcing brief**

```
/rfp-launch direct-materials 2026-07-31
```

**Folder layout:**

```
practice/
  data/
    spend-transactions.csv
    supplier-master.csv
    contract-register.csv
  .claude/commands/
    rfp-launch.md
  outputs/
    rfp-brief-direct-materials-2026-04-25.md   <-- new
```

**What you should see:** A sourcing brief with six sections: category overview showing total direct-materials spend, top 5 suppliers table, contract status summary, risk flags naming specific suppliers, a timeline from 2026-05-02 (RFP issue) to 2026-08-14 (award), and a recommendation paragraph.

**What Claude did, behind the scenes:**

1. Claude Code found `.claude/commands/rfp-launch.md` and replaced `$ARGUMENTS` with `direct-materials 2026-07-31`.
2. It parsed the two arguments: category = `direct-materials`, deadline = `2026-07-31`.
3. It read `spend-transactions.csv` (2,508 rows), filtered to `direct-materials` transactions from the last 12 months, and summed `amount_usd` by `supplier_id`.
4. It read `supplier-master.csv`, filtered to `direct-materials` suppliers, and pulled tier, risk_rating, and status for each.
5. It read `contract-register.csv`, found contracts linked to direct-materials suppliers, and flagged any with `end_date` before 2026-07-31 or status `expired`.
6. It computed timeline milestones: RFP issue = today + 7 days, Q&A close = deadline minus 14 days, bid close = deadline, evaluation = deadline + 7, award = deadline + 14.
7. It assembled all six sections into a markdown file and saved it to `outputs/rfp-brief-direct-materials-2026-04-25.md` with an audit footer.

**Command 2: Generate the savings tracker**

```
/savings-update Q1
```

**Folder layout:**

```
practice/
  data/
    spend-transactions.csv
    supplier-master.csv
  .claude/commands/
    savings-update.md
  outputs/
    savings-tracker-Q1-2026-04-25.md   <-- new
```

**What you should see:** A savings tracker with four sections: a portfolio summary paragraph with total actual spend, total prorated target, and total variance in USD and percentage. A supplier variance table showing each supplier's actual versus target. A flags section listing suppliers over +10% or below -15%. Three recommended actions, each naming a specific supplier.

**What Claude did, behind the scenes:**

1. Claude Code found `.claude/commands/savings-update.md` and replaced `$ARGUMENTS` with `Q1`.
2. It parsed the period: Q1 = 2026-01-01 to 2026-03-31 (90 days).
3. It read `spend-transactions.csv`, filtered to rows with dates in Q1 2026, and summed `amount_usd` per `supplier_id`.
4. It read `supplier-master.csv` and, for each supplier with `annual_target_usd` greater than zero, computed `prorated_target = annual_target_usd x (90 / 365)`.
5. It computed variance (actual minus prorated target) and variance percentage for each supplier, then sorted by variance descending.
6. It flagged suppliers with variance above +10% as overspend and below -15% as demand shortfall.
7. It wrote the four sections plus an audit footer and saved to `outputs/savings-tracker-Q1-2026-04-25.md`.

---

## Common mistakes and how to recover

**Symptom:** The `/rfp-launch` command runs but the Top 5 table is empty.
**Fix:** The category argument did not match any rows in `spend-transactions.csv`. Check your spelling. The valid values are `direct-materials`, `logistics`, `indirect`, and `mro` (all lowercase, with a hyphen in direct-materials). Run `/rfp-launch direct-materials 2026-07-31` exactly as shown.

**Symptom:** The timeline shows wrong dates or negative day counts.
**Fix:** The deadline argument must be a future date in YYYY-MM-DD format. If you typed `07/31/2026` or `July 31`, Claude Code may misparse it. Use `2026-07-31`.

**Symptom:** The savings tracker shows all variances as negative (under target).
**Fix:** Check the variance formula in the command file. Variance should be `actual_spend minus prorated_target`. If the command computes `prorated_target minus actual_spend`, the signs are flipped. Open `.claude/commands/savings-update.md` and confirm the formula matches the solution.

**Symptom:** The savings tracker shows zero for prorated target on some suppliers.
**Fix:** Those suppliers have `annual_target_usd` set to zero or blank in `supplier-master.csv`. The command should skip suppliers without a target. Check that the Process section says "for each supplier with an annual_target_usd > 0".

**Symptom:** The rfp-brief file has a generic recommendation like "proceed with the RFP" without naming a supplier or dollar figure.
**Fix:** The Quality criteria section in the command file requires the recommendation paragraph to name at least one supplier and one dollar figure. If Claude Code skipped that, re-run the command. If it still produces a generic recommendation, add a line to the command file: "The recommendation paragraph MUST name at least one supplier from the Top 5 table and one dollar figure from the spend data."

**Symptom:** You see "command not found" when you type `/rfp-launch`.
**Fix:** The file is not in the right location. It must be at `.claude/commands/rfp-launch.md` relative to your working directory. Run `ls .claude/commands/` to check. If the file is missing, go back to Step 2 and create it.
