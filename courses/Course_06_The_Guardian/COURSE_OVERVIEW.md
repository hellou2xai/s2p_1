# Course 6: The Guardian

## A contract review gone wrong

It is Thursday afternoon. Your team lead reviews the 12 contract review reports your automated pipeline produced this morning. She finds three problems in the first five minutes:

1. Contract CTR-2025-003 has no risk assessment section at all. The report reads as if the contract has no risk, but it is a $2.4M raw materials agreement with a single-source supplier.
2. Contract CTR-2025-006 lists a risk level of "Extreme," which is not in your risk taxonomy. Your taxonomy uses Low, Medium, High, and Critical. The report passed through Claude Code without any check.
3. Contract CTR-2025-011 is flagged Critical risk, but the report has no recommendation section. A Critical-risk contract with no recommended action is worse than no report at all.

She sends you a Teams message: "These reports cannot go to the legal team in this state. We need a quality gate. No report should save to outputs/ unless it passes validation. And I want a log of everything Claude Code does so we can audit it."

This course builds that quality gate. You write three hook scripts that intercept Claude Code's actions, validate report structure before saving, log every tool call, and trigger alerts for high-risk findings.

## What a hook is

A hook is a script that Claude Code runs automatically before or after a tool call. You register hooks in `.claude/settings.json`. Claude Code checks the registry before every tool call (PreToolUse) and after every tool call (PostToolUse).

There are four hook types in Claude Code:

| Hook type | When it fires | What it can do |
|---|---|---|
| PreToolUse | Before a tool call executes | Approve, block, or modify the call. Use this for validation gates. |
| PostToolUse | After a tool call completes | Read the result, log it, trigger downstream actions. Use this for audit and alerts. |
| Stop | When a Claude Code session ends | Run cleanup, send notifications, write session summaries. |
| Notification | When Claude Code emits an event | React to specific events like errors or completions. |

In this course you build one PreToolUse hook and two PostToolUse hooks. Course 7 covers Stop and Notification hooks.

## How hooks work in practice

When Claude Code is about to write a file (using the Write or Edit tool):

1. Claude Code checks `.claude/settings.json` for any PreToolUse hooks registered for the Write tool.
2. If a hook is registered, Claude Code runs the hook script and passes the tool call details (file path, content) as JSON on stdin.
3. The hook script reads the JSON, runs its validation checks, and prints a JSON response to stdout.
4. If the response says "approve," the write proceeds. If it says "block," the write is stopped and Claude Code receives the error message from the hook.
5. After the write completes (if approved), Claude Code checks for PostToolUse hooks and runs them with the result details.

The hook script is a plain Python file. It reads JSON from stdin, does its checks, and prints JSON to stdout. No special library needed.

## The practice scenario

Sentinel Contract Services is a US-based contract management firm. The procurement team uses Claude Code to review supplier agreements and produce structured review reports. The pipeline processes 12 contracts in a batch.

You are the Contract Operations Lead. Your job is to ensure every review report meets quality standards before it reaches the legal review queue.

Today's date is **2026-04-25**. You have:

- A contract register of 30 contracts with dates, values, and risk levels.
- A clause taxonomy of 12 standard clause types with risk weights.
- 12 contract review files in data/contracts/. Six are valid. Six have planted flaws that your hook should catch.

The six planted flaws are:
1. Missing risk assessment section.
2. Invalid risk level value ("Extreme" instead of Low/Medium/High/Critical).
3. Missing supplier name in the parties section.
4. Missing key clauses section entirely.
5. Critical risk with no recommendation section.
6. Empty clause references (section exists but has no content).

## The three hooks you will build

1. **validate-report-hook.py** (PreToolUse on Write): Intercepts every file write to outputs/. Checks for required sections (parties, term, value, risk assessment, key clauses, recommendation). Validates risk level values. Checks supplier name format. Blocks the write if any check fails and returns the specific error.

2. **audit-log-hook.py** (PostToolUse on all tools): Runs after every tool call. Appends a JSON line to audit/audit.jsonl with timestamp, tool name, file path, and action type. Append-only. Never modifies previous entries.

3. **risk-alert-hook.py** (PostToolUse on Write): Runs after every successful file write. Reads the written file. If the risk level is High or Critical, writes an alert file to alerts/ with the contract ID, risk level, and key findings.

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | The four hook types: when each fires and what it can do | 25 min |
| 2 | Writing the PreToolUse validation hook | 50 min |
| 3 | Writing the PostToolUse audit hook | 40 min |
| 4 | The risk alert hook: reading new files and triggering alerts | 40 min |
| 5 | Hook error handling: defensive writing for production reliability | 35 min |
| 6 | Integration test: running the full contract batch through all hooks | 30 min |

Total: about 4 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. Your `.claude/settings.json` has three hooks registered: validate-report (PreToolUse), audit-log (PostToolUse), and risk-alert (PostToolUse).
2. You ask Claude Code to save one of the flawed contract reviews to outputs/. The PreToolUse hook blocks the write and returns the specific error (for example, "Missing risk assessment section").
3. You ask Claude Code to save a valid contract review. The write succeeds. The audit log has an entry. If the risk level is High or Critical, an alert file appears in alerts/.
4. You run the full batch of 12 contract reviews. Six are blocked (the flawed ones). Six are saved. The audit log has entries for every tool call. Alert files exist for the high-risk contracts.
5. You can explain the difference between PreToolUse and PostToolUse and when to use each.
