# Course 10: The Negotiation Intelligence System

## Twelve days and a bad proposal

It is Wednesday morning. Your inbox has a renewal proposal from Redline Logistics LLC, your largest logistics provider. The current contract is $9.2M per year, covering warehousing, last-mile delivery, and cross-dock operations across four US distribution centers.

The proposal asks for three things:

1. A 12% price increase ($1.1M more per year).
2. A narrowed force majeure clause that removes "supply chain disruption" as a covered event.
3. A shortened auto-renewal notice period, from 180 days to 90 days.

Your VP wants a pre-negotiation brief by Friday. The face-to-face negotiation is in 12 days (2026-05-07). You need to understand the market, cost every deviation, and build a counter-proposal. Normally, this takes your team two weeks of analyst time. You have 12 days and no spare analyst.

This course teaches you to build a Claude Code composition system that does the analyst work. Sub-agents gather intelligence in parallel. A hook costs every deviation automatically. A command generates the pre-negotiation brief. Another command drafts the counter-proposal. After the negotiation closes, a capture template records the outcome so the system gets smarter over time.

## What a composition system is

A composition system combines multiple Claude Code features into a single coordinated workflow. Instead of running one prompt at a time, you orchestrate sub-agents, hooks, skills, and commands so they work together.

The components:

| Component | Role in this system |
|---|---|
| Sub-agents | Gather intelligence in parallel: market rates, supplier performance, contract terms |
| PostToolUse hook | Automatically cost every deviation when Claude writes a deviation analysis |
| PreToolUse block | Validate that the pre-negotiation brief meets completeness standards before saving |
| Slash command | `/negotiation-brief` generates the full pre-negotiation brief |
| Slash command | `/counter-proposal` drafts the counter-proposal document |
| Skill | Reusable negotiation analysis patterns |

## The practice scenario

TransGlobal Industries is a US-based manufacturer with $340M in annual procurement spend. You are a Senior Category Manager responsible for the logistics category ($28.4M across three suppliers).

Your largest logistics supplier is Redline Logistics LLC, based in Indianapolis, IN. They handle:

- Warehousing at four distribution centers (Chicago, Dallas, Atlanta, Phoenix)
- Last-mile delivery for the eastern US region
- Cross-dock operations at Chicago and Atlanta

The current contract (CTR-2024-LG-001) runs from 2024-06-01 to 2027-05-31. Annual value: $9.2M. The contract has performed well overall, but on-time delivery has slipped from 96.8% to 93.1% in the last six months.

Today's date is **2026-04-25**. Renewal decision deadline: **2026-05-07**.

## What you will build

```
negotiation-prep/
├── .claude/
│   ├── settings.json              (hooks for deviation costing and brief validation)
│   └── commands/
│       ├── negotiation-brief.md   (generates the pre-negotiation brief)
│       └── counter-proposal.md    (drafts the counter-proposal)
├── CLAUDE.md                      (contract context, supplier profile, negotiation rules)
├── data/                          (source files, read-only)
├── outputs/
│   ├── intelligence-brief.md      (sub-agent intelligence output)
│   ├── deviation-costs.md         (hook-generated deviation costing)
│   ├── pre-negotiation-brief.md   (VP-ready brief)
│   ├── counter-proposal.md        (negotiation-table-ready document)
│   └── post-close-capture.md      (outcome record after negotiation)
└── skills/
    └── negotiation-analysis.md    (reusable analysis pattern)
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | System design mapping: breaking the negotiation workflow into components | 40 min |
| 2 | Intelligence gathering with sub-agents: parallel research on market, performance, and terms | 55 min |
| 3 | Deviation costing with a PostToolUse hook: auto-pricing every contract change | 50 min |
| 4 | Pre-negotiation brief with a PreToolUse block: completeness validation before save | 50 min |
| 5 | Counter-proposal generation: building the document your negotiator takes to the table | 55 min |
| 6 | Post-close capture: recording outcomes so the system improves over time | 40 min |

Total: about 5.5 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. Your system design map shows each component (sub-agents, hooks, commands, skills) and how they connect.
2. Sub-agents run in parallel and produce an intelligence brief covering market rates, supplier performance, and contract term analysis.
3. The PostToolUse hook automatically costs every deviation when Claude writes a deviation analysis. The total annual cost impact of the proposed changes is quantified in USD.
4. The pre-negotiation brief passes a completeness check: it names Redline Logistics LLC, states the $9.2M annual value, lists the 2026-05-07 deadline, and includes three or fewer recommendations.
5. The counter-proposal document is ready for the negotiation table with specific positions on price, force majeure, and notice period.
6. A post-close capture template records the negotiation outcome with fields for final terms, concessions given, concessions received, and lessons learned.
