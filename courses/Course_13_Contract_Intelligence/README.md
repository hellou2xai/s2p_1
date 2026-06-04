# Course 13: Contract Intelligence

A short course (about 6 hours) that teaches you to build a Claude Code system for extracting, tracking, and managing supplier contracts. You start with 20 inherited agreements and build an extraction pipeline, an obligation tracker, a renewal calendar, and a contract drafting workflow. No coding required beyond copy-paste prompts.

## What you will end up with

A contract intelligence system. You point Claude Code at a folder of supplier agreements and it extracts key terms, maps obligations, flags upcoming renewals, and maintains a structured contract register. When a new contract arrives, an intake trigger processes it automatically. When you need a new agreement, Claude Code drafts one from templates using your standards.

After Course 13, you manage contracts from a single terminal session instead of hunting through shared drives and spreadsheets.

## What you need before you start

- Courses 1 through 12 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, pipelines, projects, MCP, composition, category management, and supplier risk.
- A laptop with Claude Code installed and signed in.
- About 6 hours, in two or three sittings.

## What is in this course folder

```
Course_13_Contract_Intelligence/
├── README.md                            (this file)
├── COURSE_OVERVIEW.md                   (the story behind the course)
├── lessons/                             (six lessons, do them in order)
├── practice/                            (your hands-on workspace)
│   ├── CLAUDE.md                        (project context for Vanguard Manufacturing)
│   ├── contract-register.csv            (20 contracts with key metadata)
│   ├── clause-taxonomy.csv              (15 clause types with risk weights)
│   ├── contracts/                       (20 contract .md files)
│   ├── intake/                          (empty; new contracts land here)
│   └── processed/                       (empty; processed contracts move here)
├── solutions/                           (reference answers; look only after attempting)
└── scripts/build_course_data.py         (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| practice/ | contract-register.csv | Starter register with 8 of 20 contracts; three rows carry outdated values that get reconciled in Lesson 3. Fields: contract ID, supplier, category, type, dates, annual value, notice period, auto-renew flag, status, risk level. |
| practice/ | clause-taxonomy.csv | 15 clause types (term and renewal, payment terms, liability, termination, IP, confidentiality, and others). Each has a risk weight: high, medium, or low. |
| practice/contracts/ | 20 contract .md files | Full contract text for each of the 20 agreements. Filenames follow the pattern `<TYPE>_<Supplier_Name>.md`, for example `MSA_Northwind_Office_Ltd.md`, `MSA_Apex_Logistics_Inc.md`, `SOW_Whitfield_Consulting.md`. |
| practice/intake/ | (empty) | New contracts arriving for processing land here. |
| practice/processed/ | (empty) | Contracts that have been extracted and registered move here. |

Today's date in the data is **2026-04-25**. Total annual contract value across 20 agreements: approximately $9.8M.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_Contract_Data_Extraction.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order. Each lesson adds a new capability to the system.
5. When stuck, check `solutions/`.
6. Lesson 6 teaches you to draft new contracts from templates so the system covers the full contract lifecycle.
