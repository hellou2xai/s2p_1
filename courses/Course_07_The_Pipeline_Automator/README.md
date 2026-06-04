# Course 7: The Pipeline Automator

A short course (about 4 hours) that teaches you to build **Stop hooks and notification hooks**: scripts that trigger automatically when a Claude Code session ends, routing results to the right channel based on what the session found. No prior Python experience required.

## What you will end up with

A fully automated nightly spend monitoring pipeline:
1. A **Stop hook** that reads the most recent monitor output, determines severity (routine, anomaly, or critical), and routes the result to the appropriate notification channel.
2. A **Slack notification script** that formats anomaly summaries as structured messages and posts them to a webhook URL.
3. An **escalation email script** that sends a structured email with the anomaly table and recommended actions for critical findings.

After Course 7, your nightly spend monitor runs unattended and tells the right people what it found, without anyone logging in to check.

## What you need before you start

- Courses 1 through 6 finished. You know CLAUDE.md, skills, slash commands, sub-agents, and PreToolUse/PostToolUse hooks.
- A laptop with Claude Code installed and signed in.
- Python 3.10 or later installed.
- About 4 hours, in two or three sittings.
- Optional: a Slack webhook URL for testing. The course works without one (the script writes to a local file instead).

## What is in this course folder

```
Course_07_The_Pipeline_Automator/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story behind the course)
├── lessons/                        (six lessons, do them in order)
├── practice/                       (your hands-on workspace)
│   ├── CLAUDE.md                   (project context for Ironclad Procurement Group)
│   ├── data/
│   │   ├── daily-spend.csv         (~851 rows, last 30 days)
│   │   ├── supplier-master.csv     (40 suppliers)
│   │   └── thresholds.json         (alert thresholds and severity definitions)
│   ├── outputs/daily-monitors/     (3 sample monitor outputs: routine, anomaly, critical)
│   ├── hooks/                      (you write hook scripts here)
│   └── notifications/              (notification outputs land here)
├── solutions/                      (reference answers; look only after attempting)
└── scripts/build_course_data.py    (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Folder | Files | Contents |
|---|---|---|
| data/ | daily-spend.csv (~851 rows over 30 days) | Daily spend transactions with planted anomalies on April 21 (3 anomalies) and April 24 (1 critical: $138K single transaction at 12x average). |
| data/ | supplier-master.csv (40 suppliers) | Supplier profiles across 5 categories with tier and annual spend. |
| data/ | thresholds.json | Anomaly multiplier (3x), daily spend ceiling ($500,000), severity definitions, notification routing rules. |
| outputs/daily-monitors/ | 3 sample monitor outputs | One routine (April 20), one anomaly (April 21), one critical (April 24). These show the expected output format. |
| hooks/ | (empty) | You write the stop hook and notification scripts here. |
| notifications/ | (empty) | Notification outputs (Slack messages, email drafts) land here. |

Today's date in the data is **2026-04-25**.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_Stop_Hooks.md`. Follow along.
3. Each lesson tells you exactly which folder to start Claude Code in, what to type, and what you should see.
4. Do each lesson in order.
5. When stuck, check `solutions/`.
6. Lesson 5 builds the complete pipeline. Lesson 6 tests it end to end.
