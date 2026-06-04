# Course 14: Supplier Lifecycle Management

A short course (about 6 hours) that teaches you to build a Claude Code system for managing suppliers from onboarding to exit. You work with 30 suppliers at different lifecycle stages and build automated workflows for segmentation, onboarding, development, risk response, and offboarding. No coding required beyond copy-paste prompts.

## What you will end up with

A supplier lifecycle system. You open Claude Code, run a single command, and see every supplier's current stage, what actions are due, who needs a development review, who is at risk, and who is heading for exit. When a supplier's performance drops, the system detects it and triggers a corrective action workflow. When a new supplier arrives, the onboarding checklist runs automatically.

After Course 14, you manage 30 suppliers proactively instead of reacting to problems after they escalate.

## What you need before you start

- Courses 1 through 13 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, pipelines, projects, MCP, composition, category management, supplier risk, and contract intelligence.
- A laptop with Claude Code installed and signed in.
- About 6 hours, in two or three sittings.

## What is in this course folder

```
Course_14_Supplier_Lifecycle_Management/
├── README.md                            (this file)
├── COURSE_OVERVIEW.md                   (the story behind the course)
├── lessons/                             (six lessons, do them in order)
├── practice/                            (your hands-on workspace)
│   ├── CLAUDE.md                        (project context for Crestview Industries)
│   ├── .claude/
│   │   ├── settings.json                (permissions)
│   │   └── commands/
│   │       ├── lifecycle-status.md
│   │       ├── onboard-supplier.md
│   │       └── trigger-exit.md
│   ├── Master/                          (read-only source data and templates)
│   │   ├── supplier-master.csv          (30 suppliers at various lifecycle stages)
│   │   ├── performance-history.csv      (120 rows, 4 quarters of scores)
│   │   ├── compliance-status.csv        (30 rows, one per supplier)
│   │   ├── development-plans.csv        (10 active development plans)
│   │   ├── open-orders.csv              (active POs for exit planning)
│   │   ├── Onboarding_Checklist_Template.docx
│   │   ├── Heartland_Polymers_Dev_Plan.docx
│   │   └── CAP_Template.docx
│   ├── Drafts/                          (empty; working files land here)
│   ├── Outputs/                         (empty; signed-off final files land here)
│   ├── state/                           (empty; lifecycle-state.json lands here)
│   ├── skills/
│   │   ├── assess-lifecycle-stage.md
│   │   └── detect-risk-triggers.md
├── solutions/                           (reference answers; look only after attempting)
└── scripts/build_course_data.py         (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| Master/ | supplier-master.csv | 30 suppliers across raw materials, components, IT, facilities, logistics, packaging, MRO, and professional services. Columns: Supplier_ID, Supplier_Name, Category, Tier, Lifecycle_Stage, Annual_Spend_USD, Onboarded_Date, Last_Review_Date, Risk_Tier, Region. Stages: 3 onboarding, 15 active, 3 strategic, 3 at_risk, 2 corrective_action, 2 exit, 2 under_review. |
| Master/ | performance-history.csv | 120 rows. 30 suppliers scored across 4 quarters (Q2 2025 through Q1 2026). Score columns: Quality_Score, Delivery_Score, Responsiveness_Score, Cost_Score, Overall_Score. Scale: 0 to 100. |
| Master/ | compliance-status.csv | 30 rows, one per supplier. Columns: Supplier_ID, Supplier_Name, W9, COI, ACH_Banking_Form, Code_of_Conduct, Quality_Agreement, Last_Review_Date. Each document column holds Received, Pending, Expired, or blank. |
| Master/ | development-plans.csv | 10 active plans. Columns: Supplier_ID, Supplier_Name, Plan_Type, Target, Status, Plan_Start_Date, Review_Date. |
| Master/ | open-orders.csv | 16 purchase orders, including three open POs for Regional Supply Co totaling $48,000. Used in Lesson 5. |
| Master/ | Onboarding_Checklist_Template.docx | Crestview's 12-item onboarding checklist. Used in Lesson 2. |
| Master/ | Heartland_Polymers_Dev_Plan.docx | Heartland Polymers strategic development plan. Used in Lesson 3. |
| Master/ | CAP_Template.docx | Crestview's standard corrective action plan template. Used in Lesson 4. |
| Drafts/ | (empty) | Working files (segmentation drafts, checklists, draft emails, draft CAPs) land here. |
| Outputs/ | (empty) | Signed-off final files land here. |
| state/ | (empty) | Lesson 6 generates lifecycle-state.json at runtime. |
| skills/ | 2 .md files | Reusable patterns for stage assessment and at-risk detection. |
| .claude/ | settings.json + 3 commands | Permissions plus the /lifecycle-status, /onboard-supplier, and /trigger-exit slash commands. |

Today's date in the data is **2026-04-25**. Total annual spend across 30 suppliers: approximately $38.6M.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_Supplier_Segmentation.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order. Each lesson adds a new capability to the system.
5. When stuck, check `solutions/`.
6. Lesson 6 teaches you to persist lifecycle state between sessions so the system remembers where each supplier stands.
