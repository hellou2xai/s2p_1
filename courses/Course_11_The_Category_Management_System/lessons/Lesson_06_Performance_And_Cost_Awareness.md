# Lesson 6: Performance and Cost Awareness: Tracking Token Usage and Setting Budgets

**Time:** 40 minutes.

## It is 09:05 on Monday. The briefing is sent. Now your IT lead has a question.

The Monday briefing system worked. Your VP read it at 08:58. Six categories, three actions, all supplier names and dollar figures in place. But as you close your laptop, your IT lead, Tom Bradley, sends a Slack: "Nice work. Quick question: how many tokens did that run cost? We're on a consumption-based contract. If you run this every Monday for six months, I need a number for the budget."

You do not have a number. You built the system. You did not track what it consumed. This lesson fixes that. You add cost tracking to the workflow, measure each step, identify the most expensive parts, and redesign at least one to reduce consumption without reducing quality.

## What Claude Code is going to do for you

Claude Code will estimate token consumption for each step in the Monday briefing workflow, identify the step with the highest token cost, redesign that step to pre-filter its inputs, and produce a cost summary file at `Outputs/cost_summary.md`. The summary will show weekly and monthly projections so Tom has a number for the budget.

This capability applies to Claude Code in the terminal. It does not apply to Claude AI Web or Claude Desktop with Cowork.

## Set up

1. Confirm the briefing and all Drafts/ files from Lessons 1 through 5 are present:

```
ls "Course_11_The_Category_Management_System/practice/Drafts/"
ls "Course_11_The_Category_Management_System/practice/Outputs/briefings/"
```

You should see the five Drafts/ files and `briefing-2026-04-25.md` in Outputs/briefings/.

2. Navigate to the practice folder and start Claude Code:

```
cd "Course_11_The_Category_Management_System/practice"
claude
```

3. Restate the read-only rule:

```
The files in data/ are source data. Do not edit any file in data/ or Drafts/.
Save the cost summary to Outputs/cost_summary.md.
```

**Folder layout:**

```
practice/
├── CLAUDE.md
├── data/                           (read-only)
├── Drafts/
│   ├── orchestrator_plan.md
│   ├── savings_tracker.md
│   ├── contract_review.md
│   ├── scorecard_refresh.md
│   └── ps_update.md
└── Outputs/
    ├── briefings/
    │   └── briefing-2026-04-25.md
    └── cost_summary.md             (created in this lesson)
```

## Step-by-step

### Step 1: Understand token consumption basics

Before measuring, make sure you understand the two types of tokens Claude Code uses.

```
Explain the difference between input tokens and output tokens in a Claude Code session.
Give one concrete example from our Monday briefing workflow: which step likely consumed the most input tokens, and which step likely produced the most output tokens?
Keep the explanation to four sentences.
```

You should see a short explanation. Input tokens are the words Claude Code reads (your prompts, the files it opens). Output tokens are the words Claude Code writes (its responses, the files it creates). The step that reads the full `data/category-spend.csv` file (1,452 rows) consumes the most input tokens. The step that writes the full briefing produces the most output tokens.

### Step 2: Measure the size of each input file

```
For each of the following files, count the number of lines and estimate the word count.
Use the file contents to estimate, not a guess.

Files to measure:
- data/program-state.json
- data/category-spend.csv
- data/supplier-scorecards.csv
- data/contract-calendar.csv
- data/initiative-pipeline.csv

Present results as a table: File, Lines, Estimated Words, Estimated Tokens (1 word = 1.3 tokens).
```

You should see a table. The category-spend.csv file will be the largest at 1,452 rows and roughly 7,000 to 9,000 estimated words. The initiative-pipeline.csv will be the smallest at 13 rows.

If Claude Code says it cannot count words in a CSV, tell it: "Estimate word count by multiplying line count by average words per line. For a CSV, average words per line is approximately 8."

### Step 3: Map each workflow step to its input files

```
List every step in the Monday briefing workflow from Lessons 1 through 5.
For each step, list: the step name, the Drafts/ or data/ files it reads, and the Drafts/ or Outputs/ file it writes.
Present as a table with columns: Step, Reads, Writes.
```

You should see a table covering all the major workflow steps: the orchestrator read, the savings tracking sub-agent, the contract review sub-agent, the scorecard sub-agent, the professional services sub-agent, the validation passes, and the consolidated briefing step.

### Step 4: Estimate token consumption per step

```
Using the file sizes from Step 2 and the step-to-file mapping from Step 3, estimate the input tokens and output tokens for each workflow step.

Formula:
- Input tokens: sum of (estimated tokens for each input file) + (estimated tokens for the prompt itself, assume 100 tokens per prompt).
- Output tokens: estimated tokens for the output file written.

Present as a table: Step, Input Tokens, Output Tokens, Total Tokens.
Add a row at the bottom for the grand total.
```

You should see a table with numbers in the range of 2,000 to 8,000 tokens per step. The grand total will be in the range of 25,000 to 45,000 tokens for a full Monday run, depending on how many files each step reads.

### Step 5: Identify the most expensive step

```
From the token table, which step consumes the most total tokens?
What percentage of the grand total does it account for?
What is the primary reason it is expensive?
```

You should see one step identified as the most expensive. It is likely the contract review sub-agent or the consolidated briefing step, because those read the most files. The primary reason will be that the step reads entire CSV files rather than filtered subsets.

### Step 6: Redesign the most expensive step to pre-filter its inputs

```
Rewrite the prompt for the most expensive step to reduce its token consumption.

Redesign rules:
1. Read Drafts/orchestrator_plan.md first. Extract only the supplier names or contract IDs relevant to this step.
2. Then read only the rows matching those names or IDs from the source CSV files. Do not load the entire file.
3. Use that filtered data to complete the analysis.

Write the redesigned prompt as a code block. Then estimate the new input token count.
How much does this reduce token consumption for this step?
```

You should see a redesigned prompt that reads `Drafts/orchestrator_plan.md` first, extracts a short list of identifiers (5 to 10 supplier names or contract IDs), and then fetches only those rows. The estimated token reduction for the step should be 40% to 70%, depending on how many rows were previously loaded unnecessarily.

If Claude Code estimates less than 30% savings, ask it: "What percentage of the rows in the source CSV were actually used by this step? If more than 80% were unused, the savings should be higher."

### Step 7: Test the redesigned step

```
Run the redesigned version of the [most expensive step].
Compare the output to the original output file in Drafts/.
Are the results the same? List any differences.
```

You should see the redesigned step produce the same results. If a supplier or contract is missing from the redesigned output, the pre-filter in Step 6 missed it. Tell Claude Code: "The original output included [supplier name / contract ID]. Recheck the orchestrator plan for that item and add it to the filter list."

### Step 8: Calculate weekly and monthly costs

```
Use the updated token estimates (with the redesigned step from Step 6) to calculate:
1. Total tokens for one full Monday run.
2. Weekly cost at these rates: $3.00 per million input tokens, $15.00 per million output tokens.
3. Monthly cost (4 runs per month).
4. Annual cost (52 runs per year).

Show the calculation for each, not just the final number.
```

You should see explicit calculations. For example, if the total run is 32,000 input tokens and 4,000 output tokens:

- Input cost per run: 32,000 / 1,000,000 x $3.00 = $0.096
- Output cost per run: 4,000 / 1,000,000 x $15.00 = $0.060
- Total per run: $0.156
- Monthly (4 runs): $0.62
- Annual (52 runs): $8.11

These figures are small for the practice data set. In production with 10,000 spend rows and 200 contracts, the numbers scale up proportionally.

### Step 9: Write the cost summary

```
Write a cost summary to Outputs/cost_summary.md with these five sections:

1. Run summary: date of this analysis, total workflow steps, total files read.
2. Token consumption table: one row per step, with input tokens, output tokens, and total.
3. Redesign summary: which step was redesigned, original token count, new token count, percent reduction.
4. Cost projections: per-run cost, monthly cost (4 runs), and annual cost (52 runs) at $3.00 per million input tokens and $15.00 per million output tokens.
5. Next optimization: name one more step that could be redesigned to reduce tokens further. Give a one-sentence description of how.

Use real numbers from Steps 4, 6, and 8. Do not use placeholders.
```

You should see Claude Code create `Outputs/cost_summary.md` with all five sections and real numbers.

If Claude Code uses placeholder text like "[insert token count here]", tell it: "Use the numbers we calculated in this session. Replace every placeholder with the actual figure."

### Step 10: Quit Claude Code

```
/quit
```

## Worked example: the cost audit

**The prompt you type:**

```
Estimate token consumption for every step in the Monday briefing workflow.
Identify the most expensive step.
Redesign it to cut input tokens by at least 30% using pre-filtering from Drafts/orchestrator_plan.md.
Test the redesigned step and confirm the output matches.
Calculate weekly, monthly, and annual costs at $3.00 per million input tokens and $15.00 per million output tokens.
Write the full cost summary to Outputs/cost_summary.md.
Do not edit any file in data/.
```

**Folder layout:**

```
practice/
├── data/
│   ├── category-spend.csv           (large file, measured in Step 2)
│   ├── contract-calendar.csv        (medium file)
│   └── supplier-scorecards.csv      (medium file)
├── Drafts/
│   └── orchestrator_plan.md         (pre-filter source for redesign)
└── Outputs/
    └── cost_summary.md              (output)
```

**What you should see:**

`Outputs/cost_summary.md` has five sections. The cost projection section reads:

```
Cost projections (rates: $3.00 per million input tokens, $15.00 per million output tokens)

Per run:
  Input:  31,200 tokens = $0.094
  Output:  3,800 tokens = $0.057
  Total per run:         $0.151

Monthly (4 runs):        $0.60
Annual (52 runs):        $7.85

After redesign of contract review step:
  Input:  24,600 tokens = $0.074  (21% reduction)
  Output:  3,800 tokens = $0.057
  Total per run:         $0.131

Monthly (4 runs):        $0.52
Annual (52 runs):        $6.81
```

**What Claude Code did behind the scenes:**

1. Claude Code read each data file and counted lines to estimate word counts.
2. It mapped each workflow step to its input and output files, using the session history from Lessons 1 through 5.
3. It applied the 1.3 tokens-per-word multiplier to get per-file token estimates, then summed by step.
4. It identified the contract review sub-agent as the most expensive step because it loaded all 25 contract rows and all 120 scorecard rows even though only 3 to 5 of each were relevant.
5. It redesigned the contract review prompt to read `Drafts/orchestrator_plan.md` first, extract the contract IDs in scope, and then fetch only those rows from each CSV.
6. It re-estimated the token count with the filtered inputs, finding a 21% reduction for that step.
7. It wrote the cost summary with all five required sections to `Outputs/cost_summary.md`.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Token estimates seem much lower than expected. | The 1.3x multiplier is a rough average. CSV files with many numbers run higher, around 1.5x to 2x tokens per word. For data-heavy files, adjust the multiplier: "Recalculate using 1.8 tokens per word for CSV files." |
| The redesigned step produces fewer rows than the original. | The pre-filter missed at least one item. Ask: "Read Drafts/orchestrator_plan.md. Does it list all the contracts or suppliers that the original step processed? If not, which ones are missing?" |
| The cost summary has placeholder text instead of real numbers. | Tell Claude Code: "Replace all placeholder text in Outputs/cost_summary.md with the actual figures from this session. Do not leave any brackets or [TBC] entries." |
| The percent reduction is less than 30% even after pre-filtering. | The step may read a file that is already small. Move on to the next most expensive step and redesign that one instead. Not every step has a large optimization available. |
| Claude Code cannot tell which step was most expensive because the session is new. | Ask Claude Code to re-read the Drafts/ and Outputs/ files to reconstruct the workflow: "Read all files in Drafts/ and Outputs/briefings/. From their contents, reconstruct what each workflow step read and wrote." |

## You are done with Lesson 6 when

- You have a token consumption estimate for every step in the Monday briefing workflow.
- You identified the most expensive step and redesigned it to reduce tokens by at least 30%.
- You tested the redesigned step and confirmed the output matches the original.
- `Outputs/cost_summary.md` has all five sections with real numbers, including a monthly and annual cost projection.
- You can answer Tom Bradley's question: how much does the Monday briefing system cost per month?

This completes Course 11. You built a multi-category orchestration system from scratch. The orchestrator reads the full Meridian Corp portfolio, dispatches specialized sub-agents for each category, validates outputs against defined rules, escalates failures after three retry attempts, assembles a VP-ready consolidated briefing, and tracks its own token cost. Each lesson added one layer. The full system runs in under five minutes and costs less than $1.00 per month at practice data volumes.
