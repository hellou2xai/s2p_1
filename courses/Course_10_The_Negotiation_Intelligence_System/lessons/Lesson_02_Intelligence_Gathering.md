# Lesson 2: Intelligence Gathering with Sub-Agents

**Course:** The Negotiation Intelligence System
**Time:** 55 minutes

---

## Opening scenario

It is 09:15 on Monday. Your system design is done. Now you need the intelligence. Before you can write a single word of a negotiation brief, you need three things: how Redline Logistics LLC has actually performed against the contract SLAs, where Redline's proposed pricing sits relative to the US logistics market, and how the proposed contract terms compare to industry-standard clauses. Each of those is a separate research task. Working through them one at a time would take most of the day. You have until 2:00 PM before the strategy call.

Claude Code can run multiple sub-agents at the same time. Each sub-agent works on its own task, in parallel. You launch three, wait a few minutes, and merge the results into a single intelligence brief. That brief goes to your VP. This lesson shows you exactly how to do it.

---

## What Claude Code is going to do for you

You will launch three sub-agents in parallel using Claude Code. Sub-agent 1 reads `supplier-performance.csv` and produces a performance analysis covering the last 24 months. Sub-agent 2 reads `market-benchmarks.md` and compares Redline's proposed pricing to the market. Sub-agent 3 reads `current-contract.md` and `proposed-renewal.md` and summarizes the risk exposure in the changed terms. All three write their outputs to `Outputs/`. You then ask Claude Code to merge those three outputs into a single `Outputs/intelligence-brief.md` with an executive summary. The brief names Redline Logistics LLC, states the $9.2M contract value, and lists the 2026-05-07 deadline.

---

## Set up

1. Confirm you completed Lesson 1. The file `Outputs/system-design.md` should exist:

```
ls Outputs/
```

You should see `system-design.md`.

2. Navigate to the practice folder if you are not already there:

```
cd "Course_10_The_Negotiation_Intelligence_System/practice"
```

3. Start Claude Code:

```
claude
```

4. Restate the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/. Save all output to Outputs/.
```

Claude should confirm. Nothing changes on disk.

**Folder layout at the start of this lesson:**

```
practice/
├── CLAUDE.md
├── data/
│   ├── current-contract.md
│   ├── proposed-renewal.md
│   ├── supplier-performance.csv
│   ├── market-benchmarks.md
│   └── negotiation-history.csv
└── Outputs/
    └── system-design.md
```

---

## Step-by-step

### Step 1: Launch the performance analysis sub-agent

Launch the first sub-agent. Its job is Redline's delivery and service level performance over the last 24 months.

```
Run a sub-agent with this task: "Read data/supplier-performance.csv. Calculate Redline Logistics LLC's monthly on-time delivery rate, damage rate, and SLA compliance rate for every month in the file. Identify any month where on-time delivery fell below 95%. Calculate the average OTD rate for the most recent 6 months and compare it to the average for the 6 months before that. Write the findings to Outputs/performance-analysis.md. Include a summary table and a three-sentence conclusion naming Redline Logistics LLC, the contract SLA target from data/current-contract.md, and the trend direction."
```

You should see Claude Code launch a sub-agent. It will acknowledge the task and begin processing. The terminal may show the sub-agent reading the CSV file.

If you see "Sub-agent failed to start," check that the file path `data/supplier-performance.csv` is correct with `ls data/`.

### Step 2: Launch the market benchmarks sub-agent

Without waiting for Step 1 to finish, launch the second sub-agent.

```
Run a second sub-agent with this task: "Read data/market-benchmarks.md. Extract the current US market rate range for full-truckload logistics on Midwest and Southeast corridors. Read data/proposed-renewal.md and extract Redline's proposed rates. Compare Redline's proposed rates to the market range. Identify whether Redline is pricing above, at, or below market. Write the findings to Outputs/market-analysis.md. Include a comparison table and a three-sentence conclusion naming Redline Logistics LLC, the proposed annual cost increase in dollars, and how the proposed rates rank against the market range."
```

You should see a second sub-agent launch. Both agents are now running. Claude Code may show progress messages for each.

### Step 3: Launch the terms risk sub-agent

Launch the third sub-agent.

```
Run a third sub-agent with this task: "Read data/current-contract.md and data/proposed-renewal.md. Identify the three terms that have changed and assess the risk exposure each change creates for TransGlobal Industries. For the narrowed force majeure clause: estimate the financial exposure if a supply chain disruption event occurs and is no longer covered. For the shortened notice period: calculate how many fewer days TransGlobal would have to find an alternative supplier. For the price increase: calculate the total dollar increase over the remaining contract term. Write the findings to Outputs/terms-risk-analysis.md. Include a risk table and a three-sentence conclusion naming the highest-risk change and a recommended counter-position."
```

You should see a third sub-agent launch. All three agents are now running in parallel.

### Step 4: Confirm all three output files were created

Wait for all three sub-agents to complete, then check for the output files.

```
List all files in Outputs/. How many markdown files are there?
```

You should see four files: `system-design.md`, `performance-analysis.md`, `market-analysis.md`, and `terms-risk-analysis.md`.

If one of the three new files is missing, ask Claude: "The sub-agent for [missing task] did not produce its output file. Please re-run that analysis now and save to Outputs/[filename]."

### Step 5: Read a quick summary from each file

Before merging, confirm each output is usable.

```
Read Outputs/performance-analysis.md, Outputs/market-analysis.md, and Outputs/terms-risk-analysis.md. For each file, give me the three-sentence conclusion and flag any missing data or unsupported claims.
```

You should see three conclusions. For example:
- Performance: "Redline's OTD rate averaged 93.1% over the last 6 months, down from 96.8% in the prior 6 months. The contract SLA target is 96.0%. OTD has fallen below SLA in four of the last six months."
- Market: "Redline's proposed rate of $X.XX per mile is 8% above the market median for comparable corridors. The $1.1M proposed increase represents the top quartile of the benchmarked rate range. Three of the five benchmark carriers priced below Redline's proposed renewal rate."
- Terms: "The narrowed force majeure clause removes supply chain disruption as a covered event, exposing TransGlobal to unplanned cost absorption in a disruption scenario. The shortened notice period reduces TransGlobal's transition window from 180 days to 90 days, which is insufficient to re-source all four distribution centers."

If any conclusion is missing a dollar figure, use `[TBC: figure]` as a placeholder and note it for correction.

### Step 6: Merge into the intelligence brief

Combine all three outputs into a single document.

```
Read Outputs/performance-analysis.md, Outputs/market-analysis.md, and Outputs/terms-risk-analysis.md. Merge them into a single file at Outputs/intelligence-brief.md. Structure the file as follows: 1) Executive Summary (five bullets: one on OTD trend, one on market rate position, one on force majeure risk, one on notice period risk, and one on the overall negotiation recommendation). 2) Supplier Performance section (paste the performance analysis). 3) Market Position section (paste the market analysis). 4) Contract Terms Risk section (paste the terms risk analysis). The executive summary must name Redline Logistics LLC, state the $9.2M current contract value, and include the 2026-05-07 negotiation deadline.
```

You should see a confirmation that `Outputs/intelligence-brief.md` was created. It should have four sections.

If the file is created but the executive summary is missing the deadline, tell Claude: "Add the 2026-05-07 deadline to the executive summary in Outputs/intelligence-brief.md."

### Step 7: Check the executive summary for required fields

```
Read the executive summary in Outputs/intelligence-brief.md. Does it contain: Redline Logistics LLC by name, the $9.2M value, the 2026-05-07 deadline, and a clear negotiation recommendation? List any missing items.
```

You should see Claude confirm all four fields are present, or add the missing ones.

### Step 8: Exit Claude Code

```
/quit
```

---

## Worked example, end to end

**Starting files:**

- `data/supplier-performance.csv`: 24 months of monthly OTD rate, damage rate, and SLA compliance for Redline Logistics LLC.
- `data/market-benchmarks.md`: Market rate ranges for full-truckload logistics, sourced from three industry indexes covering the Midwest and Southeast.
- `data/current-contract.md`: Active terms of CTR-2024-LG-001, including SLA targets (96% OTD), pricing, and legal clauses.
- `data/proposed-renewal.md`: Redline's renewal proposal: 12% price increase, narrowed force majeure, notice period cut from 180 to 90 days.

**The prompts you type, in order:**

```
Run a sub-agent: Read data/supplier-performance.csv and data/current-contract.md. Analyze OTD performance over 24 months. Write to Outputs/performance-analysis.md with a summary table and a three-sentence conclusion.
```

```
Run a second sub-agent: Read data/market-benchmarks.md and data/proposed-renewal.md. Compare proposed rates to market. Write to Outputs/market-analysis.md with a comparison table and a three-sentence conclusion.
```

```
Run a third sub-agent: Read data/current-contract.md and data/proposed-renewal.md. Assess risk from the three changed terms. Write to Outputs/terms-risk-analysis.md with a risk table and a three-sentence conclusion.
```

```
Merge Outputs/performance-analysis.md, Outputs/market-analysis.md, and Outputs/terms-risk-analysis.md into Outputs/intelligence-brief.md. Add an executive summary naming Redline Logistics LLC, $9.2M, and 2026-05-07.
```

**Extract from the output (executive summary):**

```
## Executive Summary

- On-time delivery for Redline Logistics LLC averaged 93.1% over the last 6 months,
  below the 96.0% SLA target and down from 96.8% in the prior 6-month period.
- Redline's proposed rate sits 8% above the market median for comparable US Midwest
  and Southeast corridors.
- The narrowed force majeure clause removes supply chain disruption coverage, creating
  unquantified but material exposure in the event of another logistics network disruption.
- The shortened notice period (90 days vs. the current 180 days) is insufficient to
  re-source four distribution centers if negotiations fail.
- Recommendation: TransGlobal negotiates from a strong position. Counter with a price increase
  cap of 4% ($368,000) and restore both the force majeure clause and the 180-day
  notice period. Deadline: 2026-05-07.
```

**Finished artifact:** `Outputs/intelligence-brief.md`, a four-section document covering performance, market position, and terms risk, with an executive summary.

**What Claude Code did behind the scenes:**

1. Claude Code parsed each sub-agent task and identified that all three were independent of each other, so it launched them in parallel.
2. Sub-agent 1 loaded `supplier-performance.csv`, grouped rows by month, calculated OTD and damage rates, compared the last 6 months to the prior 6 months, and identified the four months where OTD fell below 95%.
3. Sub-agent 2 loaded `market-benchmarks.md`, extracted rate ranges, loaded `proposed-renewal.md`, extracted Redline's proposed rates, and calculated the percentage difference from the market median.
4. Sub-agent 3 loaded both contract files, identified the three changed terms, assessed the risk exposure for each, and wrote counter-position recommendations.
5. Each sub-agent saved its output to a separate file in `Outputs/`, leaving `data/` untouched.
6. Claude Code then read all three output files, identified the shared structure (summary tables and conclusions), and assembled them into a single document.
7. It wrote the executive summary last, pulling the key figures (93.1% OTD, 8% above market, 2026-05-07) from the three sections.

---

## Common mistakes and how to recover

**Symptom:** Only one sub-agent runs. The other two are skipped.
**Fix:** Claude Code may serialize tasks if it judges them dependent. Tell it explicitly: "These three tasks are independent. Run all three in parallel before proceeding."

**Symptom:** The performance analysis covers only 6 months of data, not 24.
**Fix:** Specify the date range: "Calculate metrics for all 24 months in the file. The file runs from 2024-04 to 2026-03."

**Symptom:** The market analysis has no dollar figures, only percentages.
**Fix:** Prompt the sub-agent: "Convert the percentage difference to an annualized dollar impact. Redline's current contract value is $9.2M. An 8% rate premium on $9.2M equals $736,000 per year."

**Symptom:** The intelligence brief executive summary is missing the 2026-05-07 deadline.
**Fix:** Tell Claude: "Add '2026-05-07 negotiation deadline' to the executive summary in Outputs/intelligence-brief.md."

**Symptom:** The terms risk analysis recommends accepting the narrowed force majeure clause.
**Fix:** Push back: "Do not recommend accepting the force majeure narrowing. State the risk TransGlobal faces if a supply chain disruption occurs and the clause no longer covers it. The recommendation should be to restore the original clause."

**Symptom:** Two output files have conflicting dollar figures for the same proposed change.
**Fix:** Tell Claude: "Read all three sub-agent output files. Identify any figure that appears in more than one file with a different value. For each conflict, use the figure from Outputs/market-analysis.md as the source of truth."

---

## You are done with Lesson 2 when

- You have three analysis files in `Outputs/`: `performance-analysis.md`, `market-analysis.md`, and `terms-risk-analysis.md`.
- You have a merged `Outputs/intelligence-brief.md` with four sections and an executive summary.
- The executive summary names Redline Logistics LLC, states $9.2M, and includes the 2026-05-07 deadline.
- You understand how parallel sub-agents reduce elapsed time compared to sequential prompting.

Move to Lesson 3 when ready.
