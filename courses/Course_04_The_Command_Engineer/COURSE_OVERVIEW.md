# Course 4: The Command Engineer

## A typical first Monday of the month

It is 08:30 on the first Monday of the month. Your CPO Slacks: "Need the monthly spend breakdown by category, the anomaly report, and the contract expiry list. Same as last month. By noon."

You open Claude Code (in the terminal). You type a long prompt from memory. You get the spend breakdown, but the format is different from last month because you worded the prompt differently. The anomaly report misses the threshold you used in March because you forgot to mention it. The contract expiry list uses 60 days instead of 90 because you copied last month's prompt and forgot to change the horizon.

Your colleague Priya runs the same analysis runs for her categories. Her output looks nothing like yours. Same data, same intent, different prompts, different results.

This course fixes that. Instead of typing a different prompt every month, you build a **command library**: six slash commands that produce standardized output every time. You type `/spend-analyze Q1 direct-materials` and get the same shape of report whether you run it in April or October. Priya types the same command and gets the same shape for her categories.

## What a custom slash command is

A custom slash command is a markdown file in `.claude/commands/` that Claude Code (in the terminal) reads when you type `/command-name`. The file contains instructions, and `$ARGUMENTS` is a placeholder that captures whatever you type after the command name.

When you type `/spend-analyze Q1 direct-materials`, Claude Code finds `.claude/commands/spend-analyze.md`, reads the instructions, and replaces every `$ARGUMENTS` with `Q1 direct-materials`. Your command file parses those arguments and tells Claude Code exactly what to read, what to compute, and where to save.

Compared to a prompt or a skill:

| Prompt | SKILL.md | Slash command |
|---|---|---|
| Written once, used once | Written once, reused on different inputs | Written once, invoked with one line |
| Names specific files and values | Names input shapes | Names data files and uses $ARGUMENTS for parameters |
| Lives in a chat that ends | Lives in skills/ | Lives in .claude/commands/ |
| No parameters | No built-in parameter passing | $ARGUMENTS passes period, category, supplier, threshold |

## The practice scenario

Meridian Manufacturing is a US-based mid-market manufacturer with 48m USD in annual procurement spend across 50 suppliers in four categories: direct materials, logistics, indirect, and MRO.

You are the Procurement Operations Lead. Every month you run the same set of analysis runs: spend breakdowns, anomaly detection, scorecard refreshes, contract expiry sweeps, and savings updates. Until now, every analysis started with a different prompt typed from memory.

Today's date is **2026-04-25**. You have:

- A spend transaction file of 2,508 rows over the last 12 months.
- A supplier master of 50 suppliers with tier, risk, and contract data.
- A contract register of 45 contracts with expiry dates and notice periods.
- Quarterly scorecards for all 50 suppliers across four quarters.
- 15 planted high-value anomalies and 12 duplicate PO patterns for the anomaly exercises.

By the end of Course 4 you will have a library of six slash commands that any team member can run.

## The six commands you will build

1. **`/spend-analyze [period] [category]`** reads spend-transactions.csv, filters by period and category, sums by supplier, compares to the prior period, and saves a datestamped spend analysis.

2. **`/anomaly-detect [threshold] [period]`** scans spend-transactions.csv for transactions exceeding the threshold multiplier above category average, flags duplicate PO patterns, and saves a structured alert report.

3. **`/scorecard-refresh [supplier] [quarter]`** reads scorecard-history.csv, computes trend direction for the named supplier, and saves a one-page scorecard summary.

4. **`/contract-sweep [horizon-days]`** reads contract-register.csv, finds every contract expiring within the horizon, flags auto-renew contracts where the notice window has passed, and saves a prioritized action list.

5. **`/rfp-launch [category] [deadline]`** chains /spend-analyze and /contract-sweep outputs to generate a sourcing brief for the named category with baseline spend, expiring contracts, and a timeline anchored to the deadline.

6. **`/savings-update [period]`** reads spend-transactions.csv and supplier-master.csv, compares actual spend to annual targets, computes variance by supplier, and saves a savings tracker.

## What you will produce by the end of Course 4

Six command files in `.claude/commands/`, each between 30 and 70 lines. Plus a set of datestamped output files in `outputs/` proving each command works.

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | Anatomy of a custom slash command | 25 min |
| 2 | Writing /spend-analyze: period and category parameters | 45 min |
| 3 | Writing /anomaly-detect: configurable threshold and structured alerts | 45 min |
| 4 | Parameterized commands: /scorecard-refresh and /contract-sweep | 50 min |
| 5 | Chaining commands: /rfp-launch and /savings-update | 50 min |
| 6 | Team command distribution: shared storage and consistency governance | 25 min |

Total: about 4 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. Your `.claude/commands/` folder has six command files. Each one is between 30 and 70 lines.
2. You have run `/spend-analyze Q1 direct-materials` and produced a datestamped spend analysis in `outputs/`.
3. You have run `/anomaly-detect 2.5 Q1` and it found the planted high-value transactions and duplicate PO patterns.
4. You have run `/contract-sweep 90` and it listed the 8 contracts expiring within 90 days.
5. You have run `/rfp-launch direct-materials 2026-07-31` and it produced a sourcing brief with baseline spend and expiring contracts.
6. You can copy your `.claude/commands/` folder into your real procurement project and run the same commands on your own data.
