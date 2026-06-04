# Course 5: The Orchestrator

## A typical quarter-end scoring week

It is Monday morning, the first week after Q1 close. Your VP of Procurement sends a Teams message: "Need all 50 supplier scorecards refreshed by Wednesday COB. Board wants the portfolio risk summary Thursday."

You open Claude Code. You start scoring suppliers one at a time. Supplier 1: read the master, read Q1 performance, read the history, compute the weighted score, write the scorecard. Twenty minutes later, you have one scorecard. Forty-nine to go.

By supplier 12, Claude Code's context window is full of scorecard data from the first 11 suppliers. The scores start drifting. Supplier 12's "quality" commentary references Supplier 8's reject rate. You catch it, but how many did you miss?

By supplier 20, you are two hours in and less than halfway done. The Wednesday deadline looks tight. You consider splitting the work with a colleague, but they would need the same CLAUDE.md, the same scoring weights, the same output format. Setting them up takes an hour you do not have.

This course fixes that. Instead of scoring 50 suppliers sequentially in one long session, you build an **orchestrator** that reads the supplier master, divides it into batches, spawns five parallel worker agents (one per batch of 10), and aggregates their outputs into a portfolio summary. The whole run takes minutes, not hours. No context contamination. Every scorecard uses the same weights and format.

## What a sub-agent is

A sub-agent is a separate Claude Code session that the main session (the orchestrator) launches using the **Agent tool**. Each sub-agent gets its own context window, its own conversation, and its own set of tools. It does not see what other sub-agents are doing. It does not inherit the orchestrator's conversation history.

What the orchestrator controls:
- **What each sub-agent works on.** The orchestrator decides which suppliers go to which worker.
- **What each sub-agent knows.** The orchestrator writes the task prompt that tells the worker what files to read, what weights to use, and where to save.
- **What each sub-agent produces.** The orchestrator specifies the output format (a JSON summary file) so it can aggregate results without re-reading individual scorecards.

What the orchestrator does not control:
- **How the sub-agent reasons.** Each worker has its own context and makes its own decisions within its task scope.
- **When the sub-agent finishes.** Background agents run independently. The orchestrator checks for completion.

## The practice scenario

Atlas Procurement Services is a US-based shared services center managing procurement for three business units. The team scores 50 strategic suppliers every quarter across five categories: raw materials, logistics, IT services, facilities, and professional services.

You are the Portfolio Scoring Lead. Every quarter you produce:
1. Individual scorecards for all 50 suppliers.
2. A batch summary per category group.
3. A portfolio summary ranking all 50 by overall score, flagging at-risk and declining suppliers.

Today's date is **2026-04-25**. You have:

- A supplier master of 50 suppliers with tier, category, and annual spend data.
- Current quarter (2026-Q1) performance scores across six dimensions for all 50 suppliers.
- Historical scorecard data for three prior quarters (2025-Q2 through 2025-Q4).
- Monthly spend data (1,816 rows) for 12-month trend context.
- Risk signals for all 50 suppliers: financial health, on-time delivery, quality reject rate, single-source flags.
- Scorecard weights: quality 25%, delivery 20%, responsiveness 15%, cost 25%, innovation 15%.

Three suppliers (SUP004 Apex Electronics, SUP019 Lakeshore Drayage, SUP048 Ironside Recruiting) show declining performance trends. Three suppliers (SUP007 Liberty Composites, SUP028 Agile Platforms, SUP035 Cornerstone Electric) show improving trends. Three suppliers are at_risk status. Two are under_review.

## The multi-agent architecture you will build

```
Orchestrator prompt
├── reads supplier-master.csv (50 suppliers)
├── divides into 5 batches of 10 by category
├── spawns Worker A (raw-materials: SUP001-SUP010)
├── spawns Worker B (logistics: SUP011-SUP020)
├── spawns Worker C (it-services: SUP021-SUP030)
├── spawns Worker D (facilities: SUP031-SUP040)
├── spawns Worker E (professional-services: SUP041-SUP050)
└── aggregates 5 batch summaries → portfolio-summary.md

Each Worker agent
├── reads its batch from supplier-master.csv (10 rows)
├── reads q1-performance.csv for its 10 suppliers
├── reads scorecard-history.csv for trend analysis
├── reads risk-signals.csv for risk context
├── applies scorecard weights from its task prompt
├── writes individual scorecard .md files to batch-outputs/
└── writes batch-summary.json for the orchestrator
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | When sub-agents are the right design | 25 min |
| 2 | The Task tool: context inheritance and what sub-agents receive | 40 min |
| 3 | Designing the orchestrator: decomposition and worker invocation | 50 min |
| 4 | Designing the worker: narrow scope and structured JSON output | 50 min |
| 5 | State handoff: JSON outputs that aggregate without re-reading | 45 min |
| 6 | Failure handling: detecting malformed output and recovering | 40 min |

Total: about 4.5 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. You have an orchestrator prompt that reads supplier-master.csv, divides 50 suppliers into five batches, and spawns five worker agents.
2. Each worker agent scores its 10 suppliers using the weighted scorecard formula and writes a batch-summary.json to batch-outputs/.
3. The orchestrator reads all five batch-summary.json files and produces a portfolio-summary.md in outputs/.
4. The portfolio summary ranks all 50 suppliers by overall score, flags at-risk and declining suppliers, and includes category-level averages.
5. You can explain why a sequential single-session approach fails at this scale and how the orchestrator pattern prevents context contamination.
6. You can adapt the orchestrator pattern to a different portfolio task (contract reviews, spend analysis runs, or risk assessments).
