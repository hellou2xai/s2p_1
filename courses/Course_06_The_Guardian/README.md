# Course 6: The Guardian

A short course (about 4 hours) that teaches you to build **PreToolUse and PostToolUse hooks**: Python scripts that intercept Claude Code's tool calls to validate output before it saves, log every action to an audit trail, and trigger alerts when risk conditions are detected. No prior Python experience required.

## What you will end up with

Three hook scripts that run automatically during every Claude Code session in this project:
1. A **PreToolUse validation hook** that checks every file write for required sections, valid risk levels, and complete supplier references. If the report is malformed, the hook blocks the write and tells Claude Code what to fix.
2. A **PostToolUse audit hook** that logs every tool call (reads, writes, edits) to an append-only audit.jsonl file with timestamps and session metadata.
3. A **PostToolUse risk alert hook** that reads every newly written file, checks for High or Critical risk findings, and writes an alert file to alerts/.

After Course 6, no malformed report reaches your outputs/ folder, every action is auditable, and high-risk findings trigger automatic alerts.

## What you need before you start

- Courses 1 through 5 finished. You know CLAUDE.md, skills, slash commands, and sub-agents.
- A laptop with Claude Code installed and signed in.
- Python 3.10 or later installed (for running hook scripts). No Python coding experience needed. You will copy and modify templates.
- About 4 hours, in two or three sittings.

## What is in this course folder

```
Course_06_The_Guardian/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story behind the course)
├── lessons/                        (six lessons, do them in order)
├── practice/                       (your hands-on workspace)
│   ├── CLAUDE.md                   (project context for Sentinel Contract Services)
│   ├── data/
│   │   ├── contract-register.csv   (30 contracts)
│   │   ├── clause-taxonomy.csv     (12 standard clause categories)
│   │   └── contracts/              (12 contract review files, 6 with planted flaws)
│   ├── hooks/                      (you write hook scripts here)
│   ├── alerts/                     (risk alert hook writes here)
│   ├── audit/                      (audit log hook writes here)
│   └── outputs/                    (validated reports land here)
├── solutions/                      (reference answers; look only after attempting)
└── scripts/build_course_data.py    (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Folder | Files | Contents |
|---|---|---|
| data/ | contract-register.csv (30 contracts) | Contract metadata: parties, dates, values, risk levels, auto-renew status. |
| data/ | clause-taxonomy.csv (12 clause types) | Standard clause categories with risk weights and required-in rules. |
| data/contracts/ | 12 contract review .md files | Six valid reviews and six with planted flaws: missing risk assessment, invalid risk level, missing supplier name, missing key clauses, high risk with no recommendation, empty clause references. |
| hooks/ | (empty) | You write three Python hook scripts here. |
| alerts/ | (empty) | The risk alert hook writes alert files here. |
| audit/ | (empty) | The audit hook writes audit.jsonl here. |
| outputs/ | (empty) | Validated contract review reports land here. |

Today's date in the data is **2026-04-25**.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_The_Four_Hook_Types.md`. Follow along on your laptop.
3. Each lesson tells you exactly which folder to start Claude Code in, exactly what to type, and what you should see.
4. Do each lesson in order. Lessons 2 through 4 each build one hook script.
5. When stuck, look at the matching reference in `solutions/`. Compare against your work. Adjust.
6. Lesson 6 is the integration test. You run the full contract batch through all three hooks.
