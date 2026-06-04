# Course 11: The Category Management System

## Six categories, one Monday morning

It is Monday morning, 08:15. You manage six procurement categories at Meridian Corp. Your inbox has 23 unread messages. Three supplier scorecards arrived Friday. Two contracts expire this month. One initiative is behind schedule, and you do not know which one because the tracker is a shared spreadsheet that four people edited over the weekend.

You open six tabs. You cross-reference three dashboards. You build a status summary in a blank Word document, typing the same header format you type every Monday. By 10:30, you have a rough picture. By 11:00, your VP asks for the update and you are still formatting the table.

This course fixes that. You build a Claude Code orchestration system that does the Monday morning scan in under five minutes. One command dispatches six sub-agents (one per category), each reading the relevant data. The orchestrator collects their findings, validates the output, self-corrects any errors, and produces a consolidated briefing. You review it, make two edits, and send it to your VP before 09:00.

## What an orchestration system does

An orchestration system coordinates multiple sub-agents through a single entry point. The orchestrator prompt defines the workflow. Each sub-agent handles one category. The orchestrator collects results, checks for quality, and assembles the final output.

What the system handles:

| Without orchestration | With orchestration |
|---|---|
| Open six spreadsheets manually | One command scans all six categories |
| Copy data between files by hand | Sub-agents read source data directly |
| Spot errors only if you catch them | Feedback loop validates and self-corrects |
| No retry logic; errors stop the process | Retry limits with human escalation |
| Formatting varies by category | Consistent output format across all categories |
| No cost awareness | Token budget tracking prevents runaway costs |

## The practice scenario

Meridian Corp is a US-based manufacturer with $87.4M in annual procurement spend across six categories. You are the Director of Category Management. Your portfolio:

| Category | Annual spend | Suppliers | Active initiatives | Status |
|---|---|---|---|---|
| IT services | $18.2M | 6 | 3 | On track |
| Logistics | $16.8M | 5 | 2 | One initiative at risk |
| Facilities | $14.1M | 4 | 2 | Contract expiring May 2026 |
| Raw materials | $15.6M | 6 | 2 | Price volatility flagged |
| Professional services | $12.4M | 5 | 2 | Supplier consolidation in progress |
| MRO | $10.3M | 4 | 1 | New catalog rollout starting |

Today's date is **2026-04-25**. Your VP wants a consolidated category briefing every Monday by 09:00.

## What you will build

```
category-management-2026/
├── .claude/
│   ├── settings.json                (permissions, hooks)
│   └── commands/
│       ├── monday-briefing.md       (the master Monday command)
│       └── category-deep-dive.md    (single-category analysis)
├── CLAUDE.md                        (portfolio context, category definitions)
├── data/                            (source data files, read-only)
├── state/
│   ├── program-state.json           (updated after each session)
│   └── action-log.md               (actions taken, appended each session)
├── outputs/
│   └── briefings/                   (Monday briefings land here)
└── skills/
    ├── category-scan.md             (reusable category analysis pattern)
    └── initiative-check.md          (initiative status assessment pattern)
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | The multi-category orchestrator: one command, six categories | 50 min |
| 2 | Specialized sub-agents: one agent per category with scoped data access | 55 min |
| 3 | Self-correcting feedback loop: validate outputs and fix errors automatically | 50 min |
| 4 | Retry limits and human escalation: when to stop and ask for help | 45 min |
| 5 | Consolidated briefing: assembling sub-agent outputs into a VP-ready document | 50 min |
| 6 | Performance and cost awareness: tracking token usage and setting budgets | 40 min |

Total: about 5.5 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. You type `/monday-briefing` and Claude Code dispatches six sub-agents, one per category.
2. Each sub-agent reads only its category's data (spend, scorecards, contracts, initiatives) and produces a category summary.
3. The feedback loop catches at least one error (missing supplier name, wrong date format, or incomplete initiative status) and corrects it without your intervention.
4. The retry logic stops after three attempts on any sub-agent and escalates to you with a clear error message.
5. The consolidated briefing names all six categories, lists the top three actions, and includes at least one supplier name, one dollar figure, and one date per category.
6. You can estimate the token cost of a full Monday briefing run and explain how to reduce it.
