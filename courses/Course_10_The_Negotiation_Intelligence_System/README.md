# Course 10: The Negotiation Intelligence System

A short course (about 5.5 hours) that teaches you to build a full Claude Code composition system for contract negotiation. You combine sub-agents, hooks, skills, and commands into a single workflow that gathers intelligence, costs deviations, builds a pre-negotiation brief, generates counter-proposals, and captures outcomes. No coding required beyond copy-paste prompts.

## What you will end up with

A negotiation preparation system for a $9.2M logistics contract renewal. You type one command and Claude Code dispatches sub-agents to analyze the current contract, score supplier performance, benchmark market rates, and cost every proposed deviation. It produces a pre-negotiation brief your VP can read in five minutes and a counter-proposal document ready for the negotiation table.

After Course 10, you can prepare for a high-value negotiation in hours instead of days.

## What you need before you start

- Courses 1 through 9 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, projects, and MCP.
- A laptop with Claude Code installed and signed in.
- About 5.5 hours, in two or three sittings.

## What is in this course folder

```
Course_10_The_Negotiation_Intelligence_System/
├── README.md                              (this file)
├── COURSE_OVERVIEW.md                     (the story behind the course)
├── lessons/                               (six lessons, do them in order)
├── practice/                              (your hands-on workspace)
│   ├── CLAUDE.md                          (project context for TransGlobal Industries)
│   ├── data/
│   │   ├── current-contract.md            (current contract terms with Redline Logistics)
│   │   ├── proposed-renewal.md            (supplier's proposed renewal terms)
│   │   ├── supplier-performance.csv       (24 months of monthly KPIs)
│   │   ├── market-benchmarks.md           (market rate data for logistics services)
│   │   └── negotiation-history.csv        (past negotiation outcomes)
│   └── outputs/                           (negotiation deliverables land here)
├── solutions/                             (reference answers; look only after attempting)
│   ├── intelligence_brief_solution.md     (reference intelligence gathering output)
│   ├── deviation_cost_solution.md         (reference deviation costing output)
│   ├── pre_negotiation_brief_solution.md  (reference pre-negotiation brief)
│   ├── counter_proposal_solution.md       (reference counter-proposal)
│   └── post_close_capture_solution.md     (reference post-close capture template)
└── scripts/build_course_data.py           (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| data/ | current-contract.md | Current 36-month MSA with Redline Logistics LLC. $9.2M annual value. Key terms: pricing, SLAs, force majeure, termination, auto-renewal. |
| data/ | proposed-renewal.md | Supplier's proposed renewal: 12% price increase, narrowed force majeure, shortened auto-renewal notice from 180 to 90 days. |
| data/ | supplier-performance.csv | 24 months of monthly KPIs: on-time delivery, damage rate, invoice accuracy, response time. 24 rows. |
| data/ | market-benchmarks.md | Market rate data for comparable logistics services from three benchmark sources. |
| data/ | negotiation-history.csv | 8 past negotiation outcomes with this and similar suppliers: opening positions, final terms, concessions. |
| outputs/ | (empty) | Negotiation deliverables land here. |

Today's date in the data is **2026-04-25**. Contract renewal deadline: **2026-05-07** (12 days).

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_System_Design_Mapping.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order. Each lesson builds on the previous one.
5. When stuck, check `solutions/`.
6. Lesson 6 captures post-negotiation outcomes so the system learns from every deal.
