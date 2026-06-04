# Course 18: Savings Program Management

A short course (about 4 hours) that teaches you to build a **savings tracking and reporting system**: automated calculation of realized vs. projected savings, three-scenario modeling, and CFO-ready memo generation. No coding required.

## What you will end up with

A savings program pipeline that reads transaction data, matches it to initiative targets, computes realized savings, models three scenarios (base, upside, risk-adjusted), and produces a CFO memo. You run `/savings-update Q3` and get a complete savings review ready for Tuesday's meeting.

## What you need before you start

- Courses 1 through 12 finished. You have the full Claude Code engineering stack.
- A laptop with Claude Code installed and signed in.
- About 4 hours, in two sittings.

## What is in this course folder

```
Course_18_Savings_Program_Management/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story)
├── lessons/                        (five lessons, in order)
├── practice/
│   ├── CLAUDE.md                   (Apex Procurement savings context)
│   ├── data/
│   │   ├── sourcing-initiatives-log.csv  (8 initiatives with targets)
│   │   ├── q1-q3-transactions.csv        (~437 transaction rows)
│   │   └── market-benchmarks.md          (market rate reference)
│   └── Drafts/
├── solutions/
└── scripts/build_course_data.py
```

## What is in the practice data

| File | Contents |
|---|---|
| sourcing-initiatives-log.csv (8 rows) | 8 savings initiatives: 5 hard savings, 1 soft, 1 cost avoidance, 1 working capital. Combined target: $12M. 2 at risk or behind schedule. |
| q1-q3-transactions.csv (~437 rows) | Q1-Q3 transactions linked to the 5 hard-savings initiatives. 80% at negotiated rate, 20% at baseline (showing compliance gaps). |
| market-benchmarks.md | Industry benchmark rates for steel, logistics, IT, professional services, facilities. |

Today's date is **2026-04-25**.

## How to work through it

1. Read `COURSE_OVERVIEW.md`.
2. Start with `lessons/Lesson_01_Savings_Methodology.md`.
3. Each lesson builds toward the CFO memo in Lesson 4.
4. Lesson 5 automates the monthly refresh.
