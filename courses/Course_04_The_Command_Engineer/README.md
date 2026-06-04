# Course 4: The Command Engineer

A short course (about 4 hours) that teaches you to build **custom slash commands**: reusable, parameterized analysis commands you run from a single line in the terminal. No coding required.

## What you will end up with

A library of six slash commands (`/spend-analyze`, `/anomaly-detect`, `/scorecard-refresh`, `/contract-sweep`, `/rfp-launch`, `/savings-update`) that produce standardized, datestamped output files from your procurement data. Every analyst on your team runs the same command and gets the same shape of output.

After Course 4, every monthly analysis starts with a slash command, not a blank prompt.

## What you need before you start

- Course 1 (Terminal Foundation), Course 2 (The Context Architect), and Course 3 (The Skill Builder) finished. You know how to write a CLAUDE.md, use skills, and start `claude` in a folder.
- A laptop with Claude Code installed and signed in.
- About 4 hours, in two or three sittings.

## What is in this course folder

```
Course_04_The_Command_Engineer/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story behind the course)
├── lessons/                        (six lessons, do them in order)
├── practice/                       (your hands-on workspace)
│   ├── CLAUDE.md                   (project context for Meridian Manufacturing)
│   ├── data/                       (four CSV files, read-only)
│   │   ├── spend-transactions.csv  (~2,500 transaction rows)
│   │   ├── supplier-master.csv     (50 suppliers)
│   │   ├── contract-register.csv   (45 contracts)
│   │   └── scorecard-history.csv   (200 rows: 50 suppliers x 4 quarters)
│   ├── .claude/commands/           (you fill this folder across the lessons)
│   └── outputs/                    (analysis outputs land here)
├── solutions/                      (reference answers; look only after attempting)
└── scripts/build_course_data.py    (regenerates the practice data if you delete it)
```

The practice scenario is a procurement operations role at Meridian Manufacturing, a US mid-market manufacturer. The data is realistic: 50 suppliers, 45 contracts, 2,508 spend transactions over the last year, and quarterly scorecards.

## What is in the practice data (data quality)

| Folder | Files | Contents |
|---|---|---|
| data/ | spend-transactions.csv (~2,508 rows over 12 months) | Every purchase transaction: supplier, category, amount, PO number, cost center. 15 high-value anomalies and 12 duplicate PO patterns are planted for the /anomaly-detect exercises. |
| data/ | supplier-master.csv (50 suppliers across 4 categories) | Supplier profiles: tier, risk rating, contract link, annual target, status. 3 suppliers flagged at_risk. |
| data/ | contract-register.csv (45 contracts) | Contract details: start, end, annual value, auto-renew, notice period. 8 contracts expiring within 90 days. 21 already expired. |
| data/ | scorecard-history.csv (200 rows: 50 suppliers x 4 quarters) | Quarterly performance scores: quality, delivery, responsiveness, cost, innovation. 3 suppliers show declining trends; 2 show improving trends. |
| .claude/commands/ | (empty) | You fill this with six command files across the lessons. |
| outputs/ | (empty) | Analysis files produced by your commands land here. |

Today's date in the data is **2026-04-25**.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_Anatomy_Of_A_Slash_Command.md`. Follow along on your laptop.
3. Each lesson tells you exactly which folder to start Claude Code in, exactly which command to type, and exactly what you should see.
4. Do each lesson in order. Each one builds on the last.
5. When you finish a lesson, take a five-minute break.
6. When stuck, look at the matching reference command in `solutions/`. Compare against your work. Adjust. Carry on.
7. Lesson 5 is the composition lesson. You chain commands together.
