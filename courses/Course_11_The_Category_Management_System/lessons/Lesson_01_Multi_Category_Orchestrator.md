# Lesson 1: The Multi-Category Orchestrator

**Time:** 50 minutes.

## It is 07:45 on Monday. Your VP wants a briefing by 09:00.

You manage six procurement categories at Meridian Corp: IT services ($18.2M), Logistics ($16.8M), Raw materials ($15.6M), Facilities ($14.1M), Professional services ($12.4M), and MRO ($10.3M). Your phone has two Slack messages from Marcus Davis about a logistics carrier issue, a voicemail from the Facilities team about an expiring contract, and an email from James Park flagging steel price movement. It is not yet 08:00.

You need a picture of the full portfolio before you walk into the 09:00 call. Checking each category manually, opening the right spreadsheet, finding the right tab, and writing the summary takes 15 minutes per category. Six categories, 90 minutes. You have 75.

The orchestrator you build in this lesson reads the state of all six categories in one command and tells you what needs attention this week.

## What Claude Code is going to do for you

Claude Code will read `data/program-state.json`, identify every active risk, initiative, and expiring contract, and produce a prioritized task list ranked by urgency and dollar impact. You will have a clear picture of all six categories in under five minutes. The orchestrator does not do the category analysis itself. It reads the state, decides what is urgent, and writes a plan that Lesson 2's sub-agents will execute.

## Set up

1. Open your terminal. Navigate to the practice folder:

```
cd "Course_11_The_Category_Management_System/practice"
```

2. Confirm the practice data files are present:

```
ls data/
```

You should see: `program-state.json`, `category-spend.csv`, `supplier-scorecards.csv`, `contract-calendar.csv`, `initiative-pipeline.csv`.

If you see "No such file or directory", run `python ../scripts/build_course_data.py` from the course root first, then repeat the `ls` command.

3. Confirm the output folders exist:

```
ls
```

You should see a `Drafts/` folder and an `Outputs/` folder alongside the data files and `CLAUDE.md`.

4. Start Claude Code in the practice folder:

```
claude
```

You should see the Claude Code prompt with the folder path shown.

5. Pause OneDrive sync before you begin. Resume it after the lesson.

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
└── Outputs/
```

## Step-by-step

### Step 1: Set the read-only rule

Tell Claude Code which files are source data and must not be changed.

```
The files in data/ are source data. Do not edit, overwrite, or delete any file in data/.
Read from data/ freely. Save all output to Drafts/ unless I say otherwise.
```

You should see Claude Code confirm the rule. Nothing on disk changes.

### Step 2: Read the portfolio state

Ask Claude Code to parse the program state and give you a category snapshot.

```
Read data/program-state.json. For each of the six categories, tell me:
- The category name and annual spend.
- The number of active initiatives and their combined savings target.
- Any risk flags listed in the file.
- The owner name for each initiative.
```

You should see a six-section summary. Logistics will show one risk flag: "Initiative LOG-002 at risk: carrier capacity constraint in Southeast." Facilities will show a contract expiry warning. Raw materials will show a steel price volatility flag.

If Claude Code says the file is empty or returns no categories, type `/quit`, run `python ../scripts/build_course_data.py`, then restart Claude Code and repeat this step.

### Step 3: Identify what needs action this week

Ask Claude Code to filter for items requiring attention in the next seven days.

```
From data/program-state.json, list only the risk flags and initiatives with a status of "at_risk" or "behind_schedule".
For each item, tell me: the category, the initiative ID, the owner, the savings target, and the current status.
Sort by savings target descending.
```

You should see a short list. LOG-002 (carrier consolidation, $540,000 target, Marcus Davis) and RM-002 (polymer specification standardization, $290,000 target, James Park) should appear. Facilities should appear for the contract expiry.

### Step 4: Cross-reference the contract calendar

Ask Claude Code to add contract data to the picture.

```
Read data/contract-calendar.csv. Find all contracts with an end_date on or before 2026-05-31.
For each contract, list: contract_id, supplier, category, end_date, annual_value_usd, and notice_period_days.
Cross-reference with the Facilities risk flag you found in program-state.json.
```

You should see a table of near-term contract deadlines. The Facilities contract for ProClean Services or the contract flagged in program-state.json should appear. Annual values will be in the range of $3M to $4.2M.

If Claude Code cannot parse the CSV, check that the file is in `data/` and not in the course root. Path: `data/contract-calendar.csv`.

### Step 5: Prioritize and rank

Ask Claude Code to combine the risk flags, at-risk initiatives, and contract deadlines into a ranked action list.

```
Combine the at-risk initiatives and the near-term contract expirations into one prioritized action list.
Rank by: (1) items with a hard deadline in the next 7 days first, (2) then by dollar impact descending.
Show: Rank, Category, Item, Owner, Dollar Impact, Deadline, Recommended Action (one short sentence).
Limit to the top 8 items.
```

You should see a numbered table. The top item will likely be the Facilities contract expiry or LOG-002. Dollar impacts will be $175,000 to $680,000 for initiatives and $3M to $4.2M for contracts.

### Step 6: Plan the sub-agent work

Ask Claude Code to assign each item to a sub-agent work type for Lesson 2.

```
For each of the top 8 items, specify:
- The work type: sourcing analysis, contract review, scorecard check, or savings tracking.
- The specific data file(s) the sub-agent will need.
- The output file the sub-agent should write to in Drafts/.
Do not do the analysis yet. Just write the plan.
```

You should see each item matched to a work type and file set. For example: "LOG-002: savings tracking. Files needed: data/initiative-pipeline.csv, data/supplier-scorecards.csv. Output: Drafts/savings_tracker.md."

### Step 7: Save the orchestrator plan

Ask Claude Code to write the plan to a file.

```
Save the following to Drafts/orchestrator_plan.md:
1. Today's date: 2026-04-25.
2. The six-category snapshot from Step 2.
3. The top 8 prioritized items from Step 5.
4. The sub-agent assignments from Step 6.
Use plain markdown. Do not use em-dashes.
```

You should see Claude Code confirm that `Drafts/orchestrator_plan.md` has been created.

### Step 8: Confirm the file

```
Read the first 20 lines of Drafts/orchestrator_plan.md.
```

You should see the date, the six-category snapshot header, and the first rows of the priority table.

### Step 9: Quit Claude Code

```
/quit
```

## Worked example: the Monday morning read

**The prompt you type:**

```
Read data/program-state.json. Identify risk flags and at-risk or behind-schedule initiatives.
Read data/contract-calendar.csv. Find contracts expiring by 2026-05-31.
Combine into a ranked action list of top 8 items. Assign each to a sub-agent work type.
Save to Drafts/orchestrator_plan.md. Do not edit any file in data/.
```

**Folder layout:**

```
practice/
├── data/
│   ├── program-state.json     (input: portfolio state)
│   └── contract-calendar.csv  (input: contract deadlines)
└── Drafts/
    └── orchestrator_plan.md   (output)
```

**What you should see:**

`Drafts/orchestrator_plan.md` contains a date header (2026-04-25), a six-category snapshot table, and a ranked priority table. The top three rows read:

- Rank 1: Logistics, LOG-002 Carrier consolidation, Marcus Davis, $540,000 savings target, at risk, savings tracking.
- Rank 2: Facilities, Contract FAC-CTR-003 expiry, Ana Torres, $3.1M annual value, expires 2026-05-31, contract review.
- Rank 3: Raw materials, RM-002 Polymer standardization, James Park, $290,000 savings target, behind schedule, savings tracking.

**What Claude Code did behind the scenes:**

1. Claude Code opened `data/program-state.json` and parsed the six category objects, reading the `risk_flags` array and `active_initiatives` array for each.
2. It filtered for initiatives with `status` equal to `at_risk` or `behind_schedule`, capturing LOG-002 and RM-002.
3. It opened `data/contract-calendar.csv` and filtered rows where `end_date` is on or before 2026-05-31.
4. It merged the two filtered sets, then sorted: hard deadlines in the next 7 days first, then by dollar impact descending.
5. It assigned each item a work type by matching the item type (initiative, contract) to the four sub-agent categories.
6. It wrote the full plan to `Drafts/orchestrator_plan.md` in markdown format, with today's date at the top.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Claude Code returns no risk flags or no at-risk initiatives. | The dates in `program-state.json` may be stale. Run `python ../scripts/build_course_data.py` from the course root to regenerate current data. |
| The priority table shows no dollar values. | Dollar amounts for initiatives come from `initiative-pipeline.csv`, not `program-state.json`. Add: "Also read data/initiative-pipeline.csv and use the savings_target_usd column for initiative dollar values." |
| Claude Code edits a file in data/. | Stop immediately. Type `/quit`. The file may be damaged. Run the regenerator: `python ../scripts/build_course_data.py`. Then restart and restate the read-only rule at the beginning of the session. |
| The orchestrator plan mixes the analysis with the planning. | Be explicit: "Write the plan only. Do not produce sourcing analysis, scorecard updates, or contract recommendations in this file. Leave those for sub-agents." |
| Drafts/orchestrator_plan.md is missing the six-category snapshot. | Ask Claude Code: "Prepend a six-category snapshot table to Drafts/orchestrator_plan.md. Include: category name, annual spend, active initiative count, and any risk flags." |

## You are done with Lesson 1 when

- You can read `data/program-state.json` and summarize all six categories.
- You have a ranked action list of the top 8 items across the portfolio.
- You have sub-agent assignments for each item.
- The plan is saved in `Drafts/orchestrator_plan.md`.

Move to Lesson 2 when ready.
