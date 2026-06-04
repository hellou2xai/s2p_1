# Course 19: Supply Chain Risk and Resilience

A short course (about 4.5 hours) that teaches you to build a **supply chain risk assessment system**: concentration risk scoring, single-source exposure mapping, disruption scenario modeling, and board-level reporting. No coding required.

## What you will end up with

A complete board risk brief covering a 25-supplier portfolio: risk register, two disruption scenario models, prioritized mitigation plan, and a three-page board narrative. Produced through the full agentic pipeline without manual analysis.

## What is in this course folder

```
Course_19_Supply_Chain_Risk/
├── README.md                       (this file)
├── COURSE_OVERVIEW.md              (the story)
├── lessons/                        (six lessons, in order)
├── practice/
│   ├── CLAUDE.md                   (Fortis Manufacturing risk context)
│   ├── data/
│   │   ├── supplier-master.csv     (25 suppliers with financial health)
│   │   ├── spend-by-item.csv       (200 line items)
│   │   ├── single-source-items.csv (5 single-source items)
│   │   ├── approved-alternates.csv (4 qualified alternates)
│   │   └── disruption-events.md    (4 historical events)
│   └── Drafts/                     (your saved outputs land here)
├── solutions/
└── scripts/build_course_data.py
```

## What is in the practice data

| File | Contents |
|---|---|
| supplier-master.csv (25 suppliers) | Supplier profiles with financial health scores (3 weak), geographic concentration, single-source item counts. |
| spend-by-item.csv (200 items) | Line items across 25 suppliers. 17 are single-source. Criticality ratings included. |
| single-source-items.csv (5 items) | High-exposure single-source items with qualification time and alternate availability. |
| approved-alternates.csv (4 rows) | Qualified or in-qualification alternates for single-source items. |
| disruption-events.md | 4 historical disruption events: hurricane, financial distress, capacity crunch, cyber incident. |

Today's date is **2026-04-25**.
