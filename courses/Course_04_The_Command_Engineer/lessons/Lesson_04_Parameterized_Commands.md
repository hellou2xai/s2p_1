# Lesson 4: Parameterized Commands: /scorecard-refresh and /contract-sweep

**Time:** 50 minutes

## The problem

It is 14:00 Thursday. You have a quarterly business review with Apex Electronics (SUP004) tomorrow at 10:00. You need a fresh scorecard showing their performance trend across the last four quarters. You also got a Slack from the CPO: "Get me the list of contracts expiring in the next 90 days. I want it before end of day."

Two tasks, two different data files, two different parameter shapes. The scorecard command needs a supplier ID and a quarter. The contract sweep needs a number of days. Until now, you would type two long prompts from memory, rewording each one slightly every time. Today you write two commands that handle the parameters for you.

This lesson also introduces a new skill: parsing more than one argument from `$ARGUMENTS` when the arguments have different types (a supplier ID, a quarter label, an integer).

## What Claude Code is going to do for you

By the end of this lesson, you will type `/scorecard-refresh SUP004 2026-Q2` and get a one-page scorecard summary showing Apex Electronics' declining performance trend. You will type `/contract-sweep 90` and get a prioritized list of 8 contracts expiring within 90 days, with urgency tiers and recommended actions. Both commands read from the practice data files and save datestamped outputs.

## Set up

Before you begin, confirm these three things:

1. You are in the `practice/` folder with Claude Code installed.
2. You have `.claude/commands/spend-analyze.md` and `.claude/commands/anomaly-detect.md` from Lessons 2 and 3.
3. The `outputs/` folder exists and the four CSV files are in `data/`.

## Step-by-step

### Part A: Writing /scorecard-refresh (25 minutes)

### Step 1. Review the scorecard data.

Before writing the command, look at the data you will work with:

```
head -5 data/scorecard-history.csv
```

You should see columns: supplier_id, supplier_name, quarter, quality_score, delivery_score, responsiveness_score, cost_score, innovation_score, overall_score. Each supplier has four rows, one per quarter (2025-Q3 through 2026-Q2).

### Step 2. Check the Apex Electronics data.

Look at what you expect the command to find:

```
grep SUP004 data/scorecard-history.csv
```

You should see four rows for Apex Electronics. Notice the overall_score drops from 84.4 in 2025-Q3 to 57.9 in 2026-Q2. That is a declining trend, and the command needs to detect it.

### Step 3. Create the command file.

```
code .claude/commands/scorecard-refresh.md
```

You should see a blank file. If `code` is not available, use `nano` or open the file from your file explorer.

### Step 4. Write the Usage section.

Type the following into the file:

```markdown
# /scorecard-refresh

Produce a one-page scorecard summary for a named supplier and quarter.

## Usage

/scorecard-refresh $ARGUMENTS

Parse $ARGUMENTS as: [supplier] [quarter]
- supplier: a supplier_id (e.g., SUP004) or a supplier name (e.g., "Apex Electronics")
- quarter: 2025-Q3, 2025-Q4, 2026-Q1, or 2026-Q2

If supplier is a name, look up the matching supplier_id in supplier-master.csv.
```

You should see nine lines.

This introduces a new pattern: the first argument can be either an ID or a name. The instruction "If supplier is a name, look up the matching supplier_id" tells Claude to handle both cases. This saves the user from memorizing supplier IDs.

### Step 5. Write the Inputs section.

```markdown
## Inputs

data/scorecard-history.csv
  Filter rows for the named supplier. Pull all available quarters.

data/supplier-master.csv
  Pull tier, risk_rating, category, city, state, contract_id, and status.

data/contract-register.csv
  If the supplier has a contract_id, pull contract end_date and status.
```

You should see three data files listed. This command reads from three files, not two. The contract register provides context about the supplier's contract status, which matters for a business review.

### Step 6. Write the Process section.

```markdown
## Process

1. Look up the supplier in supplier-master.csv. Confirm the supplier_id exists.
2. Filter scorecard-history.csv for that supplier_id. Pull all quarters.
3. For the requested quarter, extract quality_score, delivery_score, responsiveness_score, cost_score, innovation_score, and overall_score.
4. Compute trend direction for overall_score across available quarters: improving (each quarter higher than the last), declining (each quarter lower), or stable.
5. Identify the strongest dimension (highest score) and weakest dimension (lowest score) for the requested quarter.
6. If the supplier has a contract, note the contract end_date and days remaining.
```

You should see six numbered steps. Step 4 is the trend computation. It compares quarter over quarter, not just the requested quarter to one prior quarter.

### Step 7. Write the Output format section.

```markdown
## Output format

Save to outputs/scorecard-[supplier_id]-[quarter]-[YYYY-MM-DD].md

Four sections:
1. **Supplier profile** (table): Supplier Name, ID, Category, Tier, Risk, Location, Contract Status.
2. **Scorecard for [quarter]** (table): Dimension, Score, vs Prior Quarter.
3. **Trend** (one paragraph): overall trend direction across quarters, strongest and weakest dimension, one recommendation.
4. **Contract note** (one line): contract end date and days remaining, or "no contract on file".

End with an audit footer.
```

You should see four output sections defined.

### Step 8. Write the Quality criteria section.

```markdown
## Quality criteria

- Scores match scorecard-history.csv exactly. No rounding or estimation.
- Trend direction is computed from actual quarter-over-quarter movement, not assumed.
- The recommendation names the weakest dimension and a specific action.
- If the supplier_id is not found, Claude Code prints an error and does not create a file.
```

You should have a complete command file. Save it.

### Step 9. Start Claude Code and test the command.

```
claude
```

You should see the Claude Code prompt.

### Step 10. Run the scorecard command for Apex Electronics.

```
/scorecard-refresh SUP004 2026-Q2
```

Claude Code reads the command file, replaces `$ARGUMENTS` with `SUP004 2026-Q2`, looks up SUP004 in the supplier master, pulls all four quarters of scorecard data, and computes the trend.

You should see a scorecard showing Apex Electronics with an overall score of 57.9 for 2026-Q2, a declining trend (84.4 to 75.2 to 62.5 to 57.9), and a recommendation targeting the weakest dimension. The output file saves to something like `outputs/scorecard-SUP004-2026-Q2-2026-04-25.md`.

If Claude says it cannot find the supplier, check that you typed `SUP004` (capital S, capital U, capital P, zero-padded to three digits).

### Step 11. Test with a supplier name instead of an ID.

```
/scorecard-refresh "Apex Electronics" 2026-Q2
```

You should see the same scorecard. The command file's Usage section tells Claude to look up the name in supplier-master.csv, so both `SUP004` and `"Apex Electronics"` work.

If Claude creates a second file instead of recognizing it as the same supplier, check that the Usage section includes the line "If supplier is a name, look up the matching supplier_id."

### Step 12. Exit Claude Code.

```
/exit
```

You are back at the terminal prompt.

---

### Part B: Writing /contract-sweep (25 minutes)

### Step 13. Review the contract data.

```
head -5 data/contract-register.csv
```

You should see columns: contract_id, supplier_id, supplier_name, title, start_date, end_date, annual_value_usd, total_value_usd, auto_renew, notice_period_days, status.

### Step 14. Count what the command should find.

Before writing the command, check how many contracts expire within 90 days of today (2026-04-25):

```
grep "expiring_soon" data/contract-register.csv
```

You should see several contracts with the status "expiring_soon." The command will compute exact days remaining and classify urgency, so it is more precise than the status field alone. There are 8 contracts with end dates between today and 90 days from now.

### Step 15. Create the command file.

```
code .claude/commands/contract-sweep.md
```

You should see a blank file.

### Step 16. Write the Usage section.

```markdown
# /contract-sweep

Find every contract expiring within a given horizon and produce an action list.

## Usage

/contract-sweep $ARGUMENTS

Parse $ARGUMENTS as: [horizon-days]
- horizon-days: an integer (e.g., 90 means find contracts expiring within 90 days of today)
```

You should see seven lines.

This command has only one argument: an integer. Simpler than `/scorecard-refresh`, but the processing logic is more complex because it involves date arithmetic and urgency classification.

### Step 17. Write the Inputs section.

```markdown
## Inputs

data/contract-register.csv
  All contracts. Compute days remaining from today (2026-04-25) to end_date.

data/supplier-master.csv
  Join on supplier_id for tier, risk_rating, and category.
```

You should see two data files.

### Step 18. Write the Process section.

```markdown
## Process

1. Read contract-register.csv. Parse end_date for every row.
2. Compute days_remaining = end_date minus today. Negative means already expired.
3. Filter for contracts where days_remaining <= horizon-days.
4. For each contract, check auto_renew. If auto_renew is "yes" and today is past the notice window (end_date minus notice_period_days), flag as "auto-renew notice window passed".
5. Sort results: expired contracts first (by days_remaining ascending), then expiring_soon (by days_remaining ascending).
6. Join to supplier-master.csv for tier, risk_rating, and category.
7. Classify urgency: "Expired" (days_remaining < 0), "Critical" (days_remaining <= 30), "Action needed" (days_remaining <= 60), "Monitor" (days_remaining <= horizon-days).
```

You should see seven steps. Steps 3 and 4 are the key logic. Step 3 filters by the horizon. Step 4 checks auto-renew contracts where the notice window has already passed, meaning they will renew automatically unless someone acts.

### Step 19. Write the Output format section.

```markdown
## Output format

Save to outputs/contract-sweep-[horizon]-days-[YYYY-MM-DD].md

Three sections:
1. **Summary** (one paragraph): total contracts found, breakdown by urgency tier, total annual value at risk.
2. **Contract action list** (table): Contract ID, Supplier, Category, Tier, End Date, Days Left, Annual Value (USD), Auto-Renew, Notice Window, Urgency, Recommended Action.
3. **Top three actions** (numbered list): the three highest-priority actions, each naming the contract, the supplier, and a specific deadline.

End with an audit footer.
```

You should see three output sections. The table includes an "Urgency" column and a "Recommended Action" column, so each row tells the reader exactly what to do.

### Step 20. Write the Quality criteria section.

```markdown
## Quality criteria

- Days remaining is computed from today (2026-04-25), not estimated.
- Auto-renew notice window logic is correct: if auto_renew is "yes" and today > (end_date - notice_period_days), the notice window has passed.
- Urgency classification uses the exact thresholds above.
- Top three actions are ordered by urgency, then by annual_value_usd descending.
```

Save the file. You now have two new command files.

### Step 21. Start Claude Code and test the contract sweep.

```
claude
```

You should see the Claude Code prompt.

### Step 22. Run the contract sweep with a 90-day horizon.

```
/contract-sweep 90
```

Claude Code reads the command file, replaces `$ARGUMENTS` with `90`, reads contract-register.csv, computes days remaining for every contract, and filters to those expiring within 90 days.

You should see 8 contracts in the action list. The urgency breakdown will include a mix of "Critical" (expiring within 30 days), "Action needed" (within 60 days), and "Monitor" (within 90 days). The total annual value at risk will be in the millions. The output file saves to something like `outputs/contract-sweep-90-days-2026-04-25.md`.

If Claude returns more than 8 contracts, it may be including already-expired contracts in the count. Check step 3 in your Process section. The filter should use "days_remaining <= horizon-days" but should only count contracts with positive days remaining (end_date is in the future). You can also adjust the filter to "0 < days_remaining <= horizon-days" if you want to exclude expired contracts from the main count.

### Step 23. Try a shorter horizon.

```
/contract-sweep 30
```

You should see fewer contracts. Only those expiring within 30 days appear. This is the "Critical" tier from the urgency classification. The narrower horizon helps you focus on the most urgent renewals.

### Step 24. Verify the output.

```
Read outputs/contract-sweep-90-days-2026-04-25.md
```

You should see the Summary, Contract action list, and Top three actions. Check that the days-remaining figures are consistent with today's date (2026-04-25) and each contract's end_date.

### Step 25. Exit Claude Code.

```
/exit
```

You are back at the terminal prompt.

## Worked example: /scorecard-refresh

**Starting files:**
- `data/scorecard-history.csv` (200 rows, 50 suppliers across 4 quarters)
- `data/supplier-master.csv` (50 suppliers)
- `data/contract-register.csv` (45 contracts)
- `.claude/commands/scorecard-refresh.md` (the command file you just wrote)

**Prompt typed:**

```
/scorecard-refresh SUP004 2026-Q2
```

**What Claude produced (extract):**

> **Supplier profile:**
>
> | Field | Value |
> |---|---|
> | Supplier Name | Apex Electronics |
> | ID | SUP004 |
> | Category | direct-materials |
> | Tier | preferred |
> | Risk | high |
> | Location | San Jose, CA |
> | Contract Status | CTR-004, expiring 2026-07-13 (79 days remaining) |
>
> **Scorecard for 2026-Q2:**
>
> | Dimension | Score | vs Prior Quarter |
> |---|---|---|
> | Quality | 58 | 0 |
> | Delivery | 59 | -15 |
> | Responsiveness | 55 | -6 |
> | Cost | 57 | +1 |
> | Innovation | 62 | +1 |
> | **Overall** | **57.9** | **-4.6** |
>
> **Trend.** Apex Electronics shows a declining trend across all four quarters: 84.4 (2025-Q3), 75.2 (2025-Q4), 62.5 (2026-Q1), 57.9 (2026-Q2). The overall score dropped 26.5 points over four quarters. The weakest dimension for 2026-Q2 is Responsiveness at 55. Recommendation: escalate to a corrective action plan focused on responsiveness, with a 60-day review checkpoint before the contract expiry on 2026-07-13.

**Output file:** `outputs/scorecard-SUP004-2026-Q2-2026-04-25.md`

**What Claude did, behind the scenes:**

1. Found `scorecard-refresh.md` in `.claude/commands/` and replaced `$ARGUMENTS` with `SUP004 2026-Q2`.
2. Parsed `SUP004` as the supplier ID and `2026-Q2` as the requested quarter.
3. Opened `data/supplier-master.csv` and found SUP004 (Apex Electronics, preferred tier, high risk, San Jose, CA).
4. Opened `data/scorecard-history.csv` and filtered to the four rows for SUP004. Extracted scores for 2026-Q2 and all prior quarters.
5. Compared overall_score across quarters (84.4, 75.2, 62.5, 57.9) and classified the trend as "declining" because each quarter was lower than the previous one.
6. Identified the weakest dimension (Responsiveness at 55) and the strongest (Innovation at 62).
7. Opened `data/contract-register.csv`, found CTR-004, and computed 79 days remaining to the 2026-07-13 end date.
8. Saved the result to `outputs/scorecard-SUP004-2026-Q2-2026-04-25.md` with four sections plus an audit footer.

## Worked example: /contract-sweep

**Starting files:**
- `data/contract-register.csv` (45 contracts with end dates, auto-renew flags, and notice periods)
- `data/supplier-master.csv` (50 suppliers)
- `.claude/commands/contract-sweep.md` (the command file you just wrote)

**Prompt typed:**

```
/contract-sweep 90
```

**What Claude produced (extract):**

> **Summary.** Contract sweep with a 90-day horizon from 2026-04-25 found 8 contracts expiring by 2026-07-24. Breakdown: 2 Critical (within 30 days), 2 Action needed (within 60 days), 4 Monitor (within 90 days). Total annual value at risk: $17,720,000.
>
> | Contract ID | Supplier | Category | Tier | End Date | Days Left | Annual Value (USD) | Auto-Renew | Notice Window | Urgency | Recommended Action |
> |---|---|---|---|---|---|---|---|---|---|---|
> | CTR-033 | Industrial Supply Co | mro | strategic | 2026-05-05 | 10 | $1,800,000 | no | N/A | Critical | Begin sourcing alternatives by 2026-04-30 |
> | CTR-036 | Voltex Electrical | mro | preferred | 2026-05-15 | 20 | $840,000 | no | N/A | Critical | Issue renewal terms or RFP by 2026-05-01 |
> | CTR-003 | Pacific Aluminum | direct-materials | strategic | 2026-06-01 | 37 | $3,100,000 | no | N/A | Action needed | Start renewal negotiation by 2026-05-15 |
> | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
>
> **Top three actions:**
> 1. CTR-033 Industrial Supply Co: contract expires 2026-05-05 (10 days). Begin sourcing alternatives or issue emergency renewal by 2026-04-30.
> 2. CTR-036 Voltex Electrical: contract expires 2026-05-15 (20 days). Issue renewal terms or launch a competitive bid by 2026-05-01.
> 3. CTR-003 Pacific Aluminum: contract expires 2026-06-01 (37 days), annual value $3,100,000. Start renewal negotiation by 2026-05-15 to avoid supply disruption.

**Output file:** `outputs/contract-sweep-90-days-2026-04-25.md`

**What Claude did, behind the scenes:**

1. Found `contract-sweep.md` in `.claude/commands/` and replaced `$ARGUMENTS` with `90`.
2. Parsed `90` as the horizon in days.
3. Opened `data/contract-register.csv` and computed `days_remaining = end_date - 2026-04-25` for every row.
4. Filtered to contracts where days_remaining was between 0 and 90 (inclusive). Found 8 contracts.
5. Checked auto_renew for each contract. For any contract where `auto_renew` was "yes" and today was past the notice window (end_date minus notice_period_days), flagged the notice window as passed.
6. Classified each contract by urgency: "Critical" for 0 to 30 days, "Action needed" for 31 to 60 days, "Monitor" for 61 to 90 days.
7. Joined to `data/supplier-master.csv` for tier, risk_rating, and category.
8. Saved the result to `outputs/contract-sweep-90-days-2026-04-25.md` with three sections (Summary, Contract action list, Top three actions) plus an audit footer.

## Key teaching: parsing multiple parameters from $ARGUMENTS

In `/spend-analyze`, `$ARGUMENTS` held two string values: `Q1 direct-materials`. In `/anomaly-detect`, it held a number and a string: `2.5 Q1`. In `/scorecard-refresh`, it holds an ID (or a quoted name) and a quarter label: `SUP004 2026-Q2`. In `/contract-sweep`, it holds a single integer: `90`.

The pattern is the same every time:

1. Write `$ARGUMENTS` in the Usage section.
2. Below it, list each argument by position with its name, type, and an example.
3. If an argument can be two types (ID or name), say so and tell Claude how to resolve it.

Claude Code does not parse `$ARGUMENTS` automatically. It reads your Usage section and follows the parsing instructions you wrote. If you forget to describe an argument, Claude guesses. If you describe it clearly, Claude handles it correctly every time.

## Common mistakes and how to recover

**Symptom:** Claude cannot find the supplier when you pass a name like "Apex Electronics."
**Fix:** Check the Usage section. It must include the line "If supplier is a name, look up the matching supplier_id in supplier-master.csv." Without that instruction, Claude treats the name as a supplier_id and fails the lookup.

**Symptom:** The scorecard trend says "stable" when Apex Electronics is clearly declining.
**Fix:** Check step 4 of the Process section. The trend logic must compare quarter-over-quarter values across all available quarters, not just the requested quarter versus the one before it. If you wrote "compare to prior quarter," Claude might check only two quarters instead of all four.

**Symptom:** /contract-sweep returns 29 contracts instead of 8.
**Fix:** Your filter likely includes already-expired contracts (those with negative days remaining). If you want only future expirations, adjust step 3 in the Process section to filter for "0 < days_remaining <= horizon-days" instead of "days_remaining <= horizon-days." The 29 includes contracts that expired months ago.

**Symptom:** The auto-renew notice window flag does not appear on any contract.
**Fix:** Check step 4 in the Process section. The comparison should be "today > (end_date minus notice_period_days)." If you wrote "today > end_date," it only fires on expired contracts, not on upcoming ones where the notice window has already closed.

**Symptom:** The contract sweep output has no "Recommended Action" column.
**Fix:** Check the table definition in the Output format section. Each column must be listed explicitly. If you left out "Recommended Action" from the column list, Claude skips it.

**Symptom:** Claude creates the output file but the file name has the supplier name instead of the supplier ID.
**Fix:** Check the Output format section in `scorecard-refresh.md`. The file name pattern should be `outputs/scorecard-[supplier_id]-[quarter]-[YYYY-MM-DD].md`, not `[supplier_name]`. Using the ID keeps file names short and consistent.

---

**Next:** In Lesson 5, you will chain two commands together. `/rfp-launch` will call the outputs of `/spend-analyze` and `/contract-sweep` to produce a sourcing brief. `/savings-update` will compare actual spend against annual targets across all suppliers.
