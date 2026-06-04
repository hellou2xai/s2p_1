# Course 3: The Skill Builder

A short course (about 4 hours) that teaches you to write **SKILL.md files**: reusable methodologies that turn every future sourcing event into a configuration job rather than a creation job. No coding required.

## What you will end up with

A library of five reusable SKILL.md files (`rfp-builder`, `bid-scorer`, `award-memo`, `risk-profiler`, `savings-calculator`) plus a complete sourcing event package (RFP, bid comparison, award memo) produced by chaining those skills against real bid data.

After Course 3, the next sourcing event you run uses the same skill library. You configure inputs; Claude does the work.

## What you need before you start

- Course 1 (Terminal Foundation) and Course 2 (The Context Architect) finished. You know how to write a CLAUDE.md, start `claude` in a folder, and read the practice data.
- A laptop with Claude Code installed and signed in.
- About 4 hours, in two or three sittings.

## What is in this course folder

```
Course_03_The_Skill_Builder/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story behind the course)
├── lessons/                        (six lessons, do them in order)
├── practice/                       (your hands-on workspace)
│   ├── CLAUDE.md                   (project context for the practice scenario)
│   ├── inputs/                     (the source documents)
│   ├── bid-responses/              (six bid responses from shortlisted carriers)
│   ├── templates/                  (skeleton templates for RFP, scorecard, memo)
│   ├── skills/                     (you fill this folder across Lessons 3 to 5)
│   └── outputs/                    (deliverables Claude produces)
├── solutions/                      (reference answers; look only after attempting)
└── scripts/build_course_data.py    (regenerates the practice data if you delete it)
```

The practice scenario is a logistics consolidation RFP at Acme Plc. The
data is realistic: 25 candidate carriers, 1,500 historical shipments to
establish baseline, and six full bid responses from shortlisted bidders.

## What is in the practice data (data rigour)

| Folder | Files | Contents |
|---|---|---|
| inputs/ | category-brief.md (one-page sourcing brief), supplier-longlist.csv (25 carriers with capability data), spend-baseline.csv (~1,500 shipment rows over the last year) | The starting context for the sourcing event |
| bid-responses/ | 6 markdown files, one per shortlisted bidder, each ~2.5 KB with executive summary, capability statement, pricing table, references, terms | Real-shaped bid responses |
| templates/ | rfp-template.md, scorecard-template.md, award-memo-template.md | Skeleton documents the skills will populate |
| skills/ | (empty) | You fill this with five SKILL.md files across Lessons 3 to 5 |
| outputs/ | (empty) | Deliverables produced by your skills land here |

Today's date in the data is **2026-04-25**.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_What_A_Skill_Is.md`. Follow along on your laptop.
3. Each lesson tells you exactly which folder to start Claude in, exactly which command to type, and exactly what you should see.
4. Do each lesson in order. Each one builds on the last.
5. When you finish a lesson, take a five-minute break.
6. When stuck, look at the matching reference SKILL.md in `solutions/`. Compare against your work. Adjust. Carry on.
7. Lesson 5 is the finale. You produce a complete sourcing event package using the five skills.
