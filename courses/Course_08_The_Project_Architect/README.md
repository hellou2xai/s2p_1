# Course 8: The Project Architect

A short course (about 4.5 hours) that teaches you to build a **Claude Code project** with cross-session memory: a persistent workspace where initiative status, decisions, and program state survive between sessions. No coding required.

## What you will end up with

A savings program project that remembers where you left off. You open a new session on Monday, run `/initiative-status direct-materials`, and Claude Code reads the initiative tracker, pulls the latest savings data, and gives you a scoped update. You run `/weekly-review` and get a consolidated program summary. When you close the session and open a new one next week, the state is still there.

After Course 8, your work accumulates across sessions instead of starting from scratch each time.

## What you need before you start

- Courses 1 through 7 finished. You know CLAUDE.md, skills, slash commands, sub-agents, and hooks.
- A laptop with Claude Code installed and signed in.
- About 4.5 hours, in two or three sittings.

## What is in this course folder

```
Course_08_The_Project_Architect/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story behind the course)
├── lessons/                        (six lessons, do them in order)
├── practice/                       (your hands-on workspace)
│   ├── CLAUDE.md                   (project context for Pinnacle Procurement)
│   ├── data/
│   │   ├── initiatives.csv         (8 savings initiatives)
│   │   ├── savings-log.csv         (120 weekly tracking entries)
│   │   ├── stakeholders.csv        (12 stakeholders)
│   │   └── milestone-tracker.csv   (40 milestones across 8 initiatives)
│   ├── state/                      (persistent state files maintained across sessions)
│   ├── initiatives/                (initiative-specific working files)
│   └── outputs/weekly-reviews/     (weekly review outputs land here)
├── solutions/                      (reference answers; look only after attempting)
└── scripts/build_course_data.py    (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Folder | Files | Contents |
|---|---|---|
| data/ | initiatives.csv (8 initiatives) | Savings program initiatives with targets, stages, owners, and status. 1 at_risk, 1 behind_schedule, 1 not_started, 5 on_track. |
| data/ | savings-log.csv (120 rows) | Weekly realized savings vs. target for each initiative. Shows cumulative variance. |
| data/ | stakeholders.csv (12 stakeholders) | Team members with roles, emails, and initiative assignments. |
| data/ | milestone-tracker.csv (40 milestones) | 5 milestones per initiative: completed, pending, or overdue. |
| state/ | (empty) | You build persistent state files here (initiative-tracker.md, decisions-log.md). |
| outputs/weekly-reviews/ | (empty) | Weekly review summaries land here. |

Today's date in the data is **2026-04-25**. Total savings target: $14.9M across 8 initiatives.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_What_A_Project_Is.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order.
5. When stuck, check `solutions/`.
6. Lesson 6 tests cross-session persistence: close and reopen Claude Code to confirm state survives.
