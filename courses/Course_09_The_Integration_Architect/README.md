# Course 9: The Integration Architect

A short course (about 5 hours) that teaches you to connect Claude Code to live procurement data using the Model Context Protocol (MCP). You build a Python server that exposes procurement queries as callable tools. No prior Python experience required.

## What you will end up with

An MCP server that connects Claude Code directly to a SQLite procurement database. You type a natural-language question ("What is our total spend with Great Lakes Steel this quarter?"), and Claude Code calls your server, queries the database, and returns the answer. No CSV exports. No stale spreadsheets. Live data, every time.

After Course 9, Claude Code stops reading flat files and starts querying structured data on demand.

## What you need before you start

- Courses 1 through 8 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, and projects.
- A laptop with Claude Code installed and signed in.
- Python 3.10 or later installed (type `python --version` in a terminal to check).
- About 5 hours, in two or three sittings.

## What is in this course folder

```
Course_09_The_Integration_Architect/
├── README.md                         (this file)
├── COURSE_OVERVIEW.md                (the story behind the course)
├── lessons/                          (six lessons, do them in order)
├── practice/                         (your hands-on workspace)
│   ├── CLAUDE.md                     (project context for Nexus Procurement Hub)
│   ├── data/
│   │   ├── procurement.db            (SQLite: suppliers, spend, contracts, open_pos)
│   │   └── supplier-master.csv       (20 suppliers, CSV reference)
│   ├── mcp-server/                   (empty: you build the server here)
│   └── outputs/                      (analysis outputs land here)
├── solutions/                        (reference answers; look only after attempting)
│   ├── mcp_server_solution.py        (complete FastMCP server with three tools)
│   └── settings_json_solution.md     (MCP registration in settings.json)
└── scripts/build_course_data.py      (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| data/ | procurement.db | SQLite database with 4 tables: suppliers (20 rows), spend (~700 transactions), contracts (20 contracts), open_pos (50 open purchase orders). |
| data/ | supplier-master.csv | 20 suppliers across 5 categories (raw-materials, logistics, it-services, facilities, professional-services). CSV reference copy. |
| mcp-server/ | (empty) | You build your FastMCP server here during Lessons 3 and 4. |
| outputs/ | (empty) | Query results and analysis outputs land here. |

Today's date in the data is **2026-04-25**. Total annual spend across 20 suppliers: approximately $46.9M.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_MCP_Protocol_Basics.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order.
5. When stuck, check `solutions/`.
6. Lesson 6 combines your MCP server with skill-driven analysis. That is the payoff.
