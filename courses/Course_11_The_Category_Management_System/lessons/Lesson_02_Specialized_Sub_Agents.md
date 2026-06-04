# Lesson 2: Specialized Sub-Agents: One Agent Per Category with Scoped Data Access

**Time:** 55 minutes.

## It is 08:10 on Monday. The orchestrator plan is ready. Now someone has to do the work.

You have `Drafts/orchestrator_plan.md` from Lesson 1. It lists eight priority items across five categories: a logistics initiative at risk, a facilities contract expiring, a raw materials initiative behind schedule, a professional services rate card due for delivery, and a handful of supplier scorecards flagged for review.

One general-purpose agent reading all six categories at once produces mediocre output. It skims. It misses the contract notice period. It conflates the steel spend trend with the polymer initiative. You have seen this happen before with a shared analyst who covered too many categories.

The right approach is specialization. Each sub-agent gets one job, one data scope, and one output file. This lesson builds and runs those agents.

## What Claude Code is going to do for you

Claude Code will run four specialized sub-agents in sequence. The sourcing agent scans the spend data and scorecard data for its category. The contract agent reads the contract calendar and recommends action for each expiring contract. The scorecard agent calculates current supplier scores. The savings tracking agent checks initiative progress against targets. Each agent writes its output to a separate file in `Drafts/`. You end the lesson with four clean files ready to be assembled in Lesson 5.

## Set up

1. Confirm Lesson 1 is complete and the plan file exists:

```
ls "Course_11_The_Category_Management_System/practice/Drafts/orchestrator_plan.md"
```

You should see the file listed. If you do not, complete Lesson 1 first.

2. Navigate to the practice folder and start Claude Code:

```
cd "Course_11_The_Category_Management_System/practice"
claude
```

You should see the Claude Code prompt.

3. Restate the read-only rule at the start of every session:

```
The files in data/ are source data. Do not edit any file in data/.
Read from data/ freely. Save all output to Drafts/ unless I say otherwise.
```

Claude Code will confirm. Nothing on disk changes.

**Folder layout:**

```
practice/
├── CLAUDE.md
├── data/
│   ├── program-state.json
│   ├── category-spend.csv
│   ├── supplier-scorecards.csv
│   ├── contract-calendar.csv
│   └── initiative-pipeline.csv
├── Drafts/
│   └── orchestrator_plan.md   (from Lesson 1)
└── Outputs/
```

## Step-by-step

### Step 1: Launch the savings tracking sub-agent for Logistics

The most urgent item is LOG-002. Start there.

```
Run a sub-agent with this task:
"Read data/initiative-pipeline.csv. Find the row where initiative_id is LOG-002.
Report: initiative name, owner, savings_target_usd, realized_savings_usd, percent complete (calculated as realized divided by target, as a percentage), status, and target_completion.
Also read data/supplier-scorecards.csv. Find all suppliers in the Logistics category. List their most recent overall score (average of quality, delivery, cost, responsiveness on a 1-to-5 scale).
Write the results to Drafts/savings_tracker.md. Include a header: 'Savings Tracker: Week of 2026-04-25'."
```

You should see Claude Code launch the sub-agent, read both files, and confirm that `Drafts/savings_tracker.md` has been created.

If the agent reports that `LOG-002` is not found, check the CSV header names by asking: "Read the first two lines of data/initiative-pipeline.csv and list the column names."

### Step 2: Add the Raw materials initiative to the savings tracker

```
Run a sub-agent with this task:
"Read data/initiative-pipeline.csv. Find the row where initiative_id is RM-002.
Report: initiative name, owner, savings_target_usd, realized_savings_usd, percent complete, status, and target_completion.
Append this row to Drafts/savings_tracker.md. Do not overwrite the existing content. Add it below the LOG-002 entry."
```

You should see the sub-agent append to the existing file. The file should now have two initiative rows.

If Claude Code creates a new file instead of appending, check the output. Then tell it: "The file already has a LOG-002 row. Read Drafts/savings_tracker.md, then append the RM-002 row at the end. Do not erase existing content."

### Step 3: Launch the contract review sub-agent

```
Run a sub-agent with this task:
"Read data/contract-calendar.csv. Find all rows where end_date is on or before 2026-06-30.
For each contract found, list: contract_id, supplier, category, end_date, annual_value_usd, notice_period_days, auto_renewal.
Then read data/supplier-scorecards.csv and look up the most recent overall score for each supplier.
Based on the score, recommend an action:
- Score 4.0 or above: Renew.
- Score 3.0 to 3.9: Review before renewing.
- Score below 3.0: Rebid.
Write to Drafts/contract_review.md with a table: Contract ID, Supplier, Category, End Date, Annual Value, Score, Recommended Action."
```

You should see Claude Code create `Drafts/contract_review.md` with a table. The Facilities contract should appear with a recommendation.

### Step 4: Verify the contract review output

```
Read Drafts/contract_review.md. Count the rows. Tell me: how many contracts are listed, the total annual value of all listed contracts, and the breakdown of actions (Renew, Review, Rebid).
```

You should see three or more contracts. The total annual value will be above $3M. At least one contract should show "Review" or "Rebid."

If Claude Code lists zero contracts, the date filter may be wrong. Ask: "Read data/contract-calendar.csv. What is the earliest end_date in the file? What is the latest?" Adjust the filter date if needed.

### Step 5: Launch the scorecard sub-agent for flagged suppliers

```
Run a sub-agent with this task:
"Read data/supplier-scorecards.csv. Find all rows where category is 'Logistics' or category is 'Raw materials'.
For each supplier in those categories, calculate the average score across all four dimensions: quality, delivery, cost, responsiveness. Use all available quarters.
List each supplier with: supplier name, category, average quality, average delivery, average cost, average responsiveness, overall average, and trend (compare the most recent quarter to the previous quarter: up, down, or flat).
Write to Drafts/scorecard_refresh.md with a header: 'Scorecard Refresh: Logistics and Raw Materials, 2026-04-25'."
```

You should see Claude Code create `Drafts/scorecard_refresh.md`. Logistics suppliers (4 to 5 rows) and raw materials suppliers (5 to 6 rows) will appear with scores on a 1-to-5 scale.

### Step 6: Launch the professional services rate card check

```
Run a sub-agent with this task:
"Read data/initiative-pipeline.csv. Find initiative PS-001 (Consulting rate card negotiation).
Report: savings_target_usd, realized_savings_usd, percent complete, status, and target_completion.
Read data/contract-calendar.csv. Find contracts in the Professional services category. List each contract with its end_date and annual_value_usd.
Write findings to Drafts/ps_update.md with a header: 'Professional Services Update: 2026-04-25'."
```

You should see `Drafts/ps_update.md` created with initiative progress and contract details for the professional services category. PS-001 target completion is 2026-04-30, so the agent should flag it as a near-term item.

### Step 7: Confirm all four output files

```
List all files in Drafts/. Read the first 5 lines of each of these files:
Drafts/savings_tracker.md, Drafts/contract_review.md, Drafts/scorecard_refresh.md, Drafts/ps_update.md.
```

You should see all four files listed. Each should have a header line and at least one data row.

If a file is missing, re-run the relevant step above. If a file exists but has no data rows, ask: "Read Drafts/[filename]. What data is present? Did the sub-agent find matching rows?"

### Step 8: Quit Claude Code

```
/quit
```

## Worked example: the contract review sub-agent

**The prompt you type:**

```
Run a sub-agent with this task:
"Read data/contract-calendar.csv. Find contracts expiring by 2026-06-30.
Look up each supplier in data/supplier-scorecards.csv to get their average overall score.
Score above 4.0: Renew. Score 3.0 to 3.9: Review. Score below 3.0: Rebid.
Write to Drafts/contract_review.md."
```

**Folder layout:**

```
practice/
├── data/
│   ├── contract-calendar.csv      (input: expiry dates and values)
│   └── supplier-scorecards.csv    (input: supplier scores)
└── Drafts/
    └── contract_review.md         (output)
```

**What you should see:**

| Contract ID | Supplier | Category | End Date | Annual Value | Score | Action |
|---|---|---|---|---|---|---|
| CTR-003 | NetSecure Corp | IT services | 2026-05-28 | $3,141,225 | 4.1 | Renew |
| CTR-010 | ProClean Services | Facilities | 2027-03-28 | $3,143,626 | 3.6 | Review |
| CTR-007 | Horizon Distribution | Logistics | 2025-05-28 | $3,855,060 | 2.9 | Rebid |

**What Claude Code did behind the scenes:**

1. The sub-agent read `data/contract-calendar.csv` and filtered for rows where `end_date` is on or before 2026-06-30.
2. For each matching contract, it extracted the `supplier` field and searched `data/supplier-scorecards.csv` for all rows with that supplier name.
3. It averaged the four score columns (quality, delivery, cost, responsiveness) across all available quarters to get an overall score.
4. It applied the three-tier decision rule (above 4.0, 3.0 to 3.9, below 3.0) and assigned a recommended action.
5. It wrote the results as a markdown table to `Drafts/contract_review.md`.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| A sub-agent reads the wrong file. | Name the file explicitly in the task: "Read data/contract-calendar.csv (not data/category-spend.csv)." Exact file names prevent confusion. |
| The scorecard agent produces identical scores for every supplier. | The agent may have averaged incorrectly. Ask it: "Show me the raw score columns for one supplier before averaging. Use data/supplier-scorecards.csv." |
| Two sub-agents overwrite the same output file. | Each agent must write to a different file. If two agents both write to `Drafts/savings_tracker.md`, one will erase the other's output. Assign distinct file names in every task. |
| A sub-agent produces no rows for the Logistics category. | The category value in the CSV may be "Logistics" with a capital L, or it may be stored differently. Ask: "What are the unique values in the category column of data/initiative-pipeline.csv?" |
| The professional services rate card shows 0% complete even though realized savings are $340,000. | The percent complete calculation requires dividing realized by target. Specify in your prompt: "Calculate percent complete as realized_savings_usd divided by savings_target_usd, multiplied by 100, rounded to one decimal place." |
| Claude Code tries to run all four agents at once and the outputs are incomplete. | Run one agent at a time and verify each output before launching the next. Complex parallel tasks can produce partial writes. |

## You are done with Lesson 2 when

- `Drafts/savings_tracker.md` has rows for LOG-002 and RM-002.
- `Drafts/contract_review.md` has at least three contracts with recommended actions.
- `Drafts/scorecard_refresh.md` has Logistics and Raw materials suppliers with scores and trends.
- `Drafts/ps_update.md` has the PS-001 initiative status and professional services contract details.

Move to Lesson 3 when ready.
