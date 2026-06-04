# Course 11: The Category Management System

A short course (about 5.5 hours) that teaches you to build a Claude Code orchestration system that monitors six procurement categories simultaneously. One Monday morning command scans all six categories, surfaces what needs attention, drafts active initiative work, and updates program state. No coding required beyond copy-paste prompts.

## What you will end up with

A multi-category monitoring system. You open Claude Code on Monday morning, type one command, and get a consolidated briefing: which categories are on track, which need attention, which initiatives are stalled, and which contracts are expiring. Claude Code dispatches specialized sub-agents for each category, collects their findings, self-corrects errors, and produces a VP-ready briefing in under five minutes.

After Course 11, you manage six categories from a single terminal session instead of six separate spreadsheets.

## What you need before you start

- Courses 1 through 10 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, projects, MCP, and composition systems.
- A laptop with Claude Code installed and signed in.
- About 5.5 hours, in two or three sittings.

## What is in this course folder

```
Course_11_The_Category_Management_System/
├── README.md                            (this file)
├── COURSE_OVERVIEW.md                   (the story behind the course)
├── lessons/                             (six lessons, do them in order)
├── practice/                            (your hands-on workspace)
│   ├── CLAUDE.md                        (project context for Meridian Corp)
│   ├── data/
│   │   ├── program-state.json           (6 categories with current status)
│   │   ├── category-spend.csv           (~1,500 rows across 6 categories)
│   │   ├── supplier-scorecards.csv      (30 suppliers x 4 quarters)
│   │   ├── contract-calendar.csv        (25 contracts with key dates)
│   │   └── initiative-pipeline.csv      (12 active initiatives)
│   └── outputs/                         (briefings and reports land here)
├── solutions/                           (reference answers; look only after attempting)
│   ├── orchestrator_prompt_solution.md  (the master orchestrator prompt)
│   ├── category_agent_solution.md       (specialized category sub-agent prompt)
│   ├── feedback_loop_solution.md        (self-correcting validation pattern)
│   ├── consolidated_briefing_solution.md (reference Monday briefing output)
│   └── cost_awareness_solution.md       (token budget tracking pattern)
└── scripts/build_course_data.py         (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| data/ | program-state.json | 6 categories: IT services, logistics, facilities, raw materials, professional services, MRO. Each has status, owner, active initiatives, and risk flags. |
| data/ | category-spend.csv | ~1,500 spend transactions across 6 categories over 12 months. |
| data/ | supplier-scorecards.csv | 30 suppliers scored across 4 quarters on quality, delivery, cost, and responsiveness. 120 rows. |
| data/ | contract-calendar.csv | 25 contracts with start dates, end dates, renewal windows, and auto-renewal flags. |
| data/ | initiative-pipeline.csv | 12 active initiatives across 6 categories with targets, stages, and owners. |
| outputs/ | (empty) | Monday briefings and category reports land here. |

Today's date in the data is **2026-04-25**. Total annual spend across 6 categories: $87.4M.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_Multi_Category_Orchestrator.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order. Each lesson adds a new capability to the system.
5. When stuck, check `solutions/`.
6. Lesson 6 teaches you to track token costs so the system stays within budget.
