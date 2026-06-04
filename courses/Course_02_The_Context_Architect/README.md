# Course 2: The Context Architect

A short course (about 3 hours) that teaches you how to give Claude the right background for the procurement work in front of you. No coding. The hardest thing you do is type a few commands into a terminal.

## What you will end up with

By the end of this course, you can produce three real procurement briefs (one for direct materials, one for logistics, one for indirect) by typing **the same prompt** in **three different folders**. Claude reads a small instructions file in each folder, so each brief talks about the right suppliers and the right rules.

## What you need before you start

- Course 1 (Terminal Foundation) finished. You know how to open a terminal and type `claude`.
- A laptop with Claude Code installed and signed in.
- About 3 hours, in two or three sittings.

## What is in this course folder (the simple version)

```
Course_02_The_Context_Architect/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story behind the course)
├── lessons/                        (six lessons, do them in order)
├── practice/                       (your hands-on workspace)
│   ├── CLAUDE.md                   (starter, weak on purpose, you fix it in Lesson 2)
│   ├── direct-materials/           (one folder per category)
│   ├── logistics/
│   └── indirect/
├── solutions/                      (reference answers; look only after you try)
└── scripts/build_course_data.py    (regenerates the data if you delete it)
```

Inside each category folder you have just three files: a CLAUDE.md (starter, you fill it in Lesson 3), a master CSV, and an activity CSV. No further nesting.

## What is in the practice data

Realistic procurement volumes. Today's date in the data is **2026-04-25**.

| Category | Master file | Activity file |
|---|---|---|
| direct-materials/ | suppliers.csv (50 suppliers across Michigan, California, Texas, Ohio, and other US states) | orders.csv (2,500 purchase orders across the last year) |
| logistics/ | carriers.csv (20 carriers covering road, sea, air, parcel) | shipments.csv (5,000 shipments across the last year) |
| indirect/ | vendors.csv (80 vendors: office, software, marketing, legal, audit, MRO, telecoms, fleet, facilities) | invoices.csv (3,000 invoices, 18 of them break the $25,000 approval rule) |

Total: about 10,500 rows of data. You will not read every row by hand. Claude will, when you ask. That is the point.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_How_Claude_Reads_CLAUDE_md.md`. Follow along on your laptop.
3. Each lesson tells you exactly which folder to start Claude in, exactly which command to type, and exactly what you should see back.
4. Do each lesson in order. Each one builds on the last.
5. When you finish a lesson, take a five-minute break.
6. When stuck, look at the matching file in `solutions/`. Compare. Adjust. Carry on.

## A note on style

Every instruction is in plain English. If something feels jargon-heavy, that is a bug. The course follows the project writing rules: short sentences, real numbers, named suppliers, no marketing fluff.
