# Course 5: The Orchestrator

A short course (about 4.5 hours) that teaches you to design **multi-agent workflows**: an orchestrator that decomposes a large portfolio task, spawns parallel worker sub-agents, and aggregates their results into a single deliverable. No coding required.

## What you will end up with

A working multi-agent system that scores 50 suppliers in parallel batches. You run one command. The orchestrator reads the supplier master, divides it into five batches of 10, spawns five worker agents, collects their outputs, and produces a ranked portfolio summary. The same pattern works for any large-scale procurement task.

After Course 5, portfolio-scale work runs in parallel instead of one supplier at a time.

## What you need before you start

- Courses 1 through 4 finished. You know how to write a CLAUDE.md, use skills, build slash commands, and start `claude` in a folder.
- A laptop with Claude Code installed and signed in.
- About 4.5 hours, in two or three sittings.

## What is in this course folder

```
Course_05_The_Orchestrator/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story behind the course)
├── lessons/                        (six lessons, do them in order)
├── practice/                       (your hands-on workspace)
│   ├── CLAUDE.md                   (project context for Atlas Procurement Services)
│   ├── data/                       (five data files, read-only)
│   │   ├── supplier-master.csv     (50 suppliers across 5 categories)
│   │   ├── q1-performance.csv      (50 rows: current quarter KPIs)
│   │   ├── scorecard-history.csv   (200 rows: 50 suppliers x 4 quarters)
│   │   ├── spend-by-supplier.csv   (~1,800 monthly spend rows)
│   │   ├── risk-signals.csv        (50 rows: financial and operational risk)
│   │   └── scorecard-weights.json  (dimension weights for scoring)
│   ├── batch-outputs/              (worker agents write batch results here)
│   └── outputs/                    (orchestrator summary lands here)
├── solutions/                      (reference answers; look only after attempting)
└── scripts/build_course_data.py    (regenerates the practice data if you delete it)
```

The practice scenario is a shared services procurement role at Atlas Procurement Services, a US-based shared services center. The data is realistic: 50 suppliers across five categories, quarterly scorecards, monthly spend, and risk signals.

## What is in the practice data (data quality)

| Folder | Files | Contents |
|---|---|---|
| data/ | supplier-master.csv (50 suppliers across 5 categories) | Supplier profiles: tier, risk rating, annual spend, status. 3 suppliers flagged at_risk, 2 under_review. |
| data/ | q1-performance.csv (50 rows) | Current quarter (2026-Q1) KPIs: quality, delivery, responsiveness, cost, innovation scores per supplier. |
| data/ | scorecard-history.csv (200 rows: 50 suppliers x 4 quarters) | Historical scores for 2025-Q2 through 2026-Q1. 3 suppliers show declining trends; 3 show improving trends. |
| data/ | spend-by-supplier.csv (~1,816 rows over 12 months) | Monthly spend transactions per supplier for trend context. |
| data/ | risk-signals.csv (50 rows) | Financial health, on-time delivery, quality reject rate, single-source flag, geographic risk, cyber risk. |
| data/ | scorecard-weights.json | Dimension weights: quality 25%, delivery 20%, responsiveness 15%, cost 25%, innovation 15%. |
| batch-outputs/ | (empty) | Worker agents write batch-summary JSON files here. |
| outputs/ | (empty) | The orchestrator writes the portfolio summary here. |

Today's date in the data is **2026-04-25**.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_When_Sub_Agents_Are_The_Right_Design.md`. Follow along on your laptop.
3. Each lesson tells you exactly which folder to start Claude Code in, exactly which command to type, and exactly what you should see.
4. Do each lesson in order. Each one builds on the last.
5. When you finish a lesson, take a five-minute break.
6. When stuck, look at the matching reference in `solutions/`. Compare against your work. Adjust. Carry on.
7. Lesson 5 is the aggregation lesson. You combine batch outputs into the portfolio summary.
