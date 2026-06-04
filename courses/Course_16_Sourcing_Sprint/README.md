# Course 16: Sourcing Sprint

A short course (about 5 hours) that teaches you to run a competitive sourcing event end to end with Claude Code. You start with spend data and a supplier longlist, generate an RFP package, process six bid responses, score them against weighted criteria, and produce an award recommendation memo. No coding required beyond copy-paste prompts.

## What you will end up with

A sourcing event system. You feed Claude Code your category spend, scope notes, and supplier longlist. It generates an RFP document, creates a response template for suppliers, processes incoming bids, scores each response against your evaluation criteria, and drafts an award recommendation memo for your VP. The entire sourcing sprint, from category analysis to award recommendation, runs through five structured prompts.

After Course 16, you compress a 4-week sourcing cycle into a 2-week sprint with consistent scoring and auditable decisions.

## What you need before you start

- Courses 1 through 15 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, pipelines, projects, MCP, composition, category management, supplier risk, contract intelligence, supplier lifecycle, and P2P compliance.
- A laptop with Claude Code installed and signed in.
- About 5 hours, in two sittings.

## What is in this course folder

```
Course_16_Sourcing_Sprint/
├── README.md                            (this file)
├── COURSE_OVERVIEW.md                   (the story behind the course)
├── lessons/                             (five lessons, do them in order)
├── practice/                            (your hands-on workspace)
│   ├── CLAUDE.md                        (project context for Ironbridge Mfg)
│   ├── Master/                          (read-only source files)
│   │   ├── spend-baseline.csv           (356 rows of historical spend, $22.2M total)
│   │   ├── supplier-longlist.csv        (16 suppliers with capabilities)
│   │   ├── scope-notes.md               (sourcing event scope and objectives)
│   │   └── bid-responses/               (12 CSV files: 6 suppliers x pricing + technical)
│   ├── Drafts/                          (working files saved during the lessons)
│   ├── Outputs/                         (final, signed-off deliverables)
│   ├── Reference/                       (supporting reference notes)
│   └── skills/
│       └── score-bid-response.md        (reusable bid scoring pattern)
├── solutions/                           (reference answers; look only after attempting)
└── scripts/build_course_data.py         (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| Master/ | spend-baseline.csv | 356 rows of historical spend across direct materials (steel, polymers, aluminum, electronics, fasteners, coatings, plus a small "Other" residual). Fields: transaction_id, date, supplier_id, supplier_name, sub_category, part_number, description, unit_of_measure, quantity, unit_price_usd, amount_usd. Covers 12 months and totals $22.2M. |
| Master/ | supplier-longlist.csv | 16 suppliers: 10 active, 2 prospective new entrants (Northland Alloys, Bayshore Materials), and 4 additional approved names referenced in lesson narrative (Titan Precision LLC, Cascade Metals, Summit Steel, Atlas Metalworks). Fields: supplier_id, supplier_name, city, state, tier, annual_spend_usd, status, capability_match, capabilities, risk_rating. |
| Master/ | scope-notes.md | Sourcing event scope: category definition, current state, objectives (8-12% cost reduction, new supplier qualification, payment terms improvement), timeline, evaluation criteria with weights, and stakeholder list. |
| Master/bid-responses/ | 12 CSV files | Six supplier bids. Each bidder has a pricing CSV (`bid_pricing_<Supplier>.csv` with part_number, description, unit_of_measure, annual_volume, unit_price_usd, total_annual_price, tooling_cost_usd, freight_terms, lead_time_days, minimum_order_quantity) and a technical CSV (`bid_technical_<Supplier>.csv` with question_id, question, response, covering T1 through T10). Bidders: Great Lakes Steel, Heartland Polymers, Pacific Aluminum, Cascade Fasteners, Northland Alloys, Bayshore Materials. |
| Drafts/ | (empty) | Working files saved during the lessons land here. |
| Outputs/ | (empty) | Final, signed-off deliverables. |
| Reference/ | (empty) | Supporting reference notes added during the lessons. |
| skills/ | score-bid-response.md | Reusable bid scoring pattern. Reads every file in Master/bid-responses/, applies the weights from CLAUDE.md, and writes scorecards to Drafts/. |

Today's date in the data is **2026-04-25**. Annual category spend: $22.2M. CPO deadline for award recommendation: **2026-06-20**.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_Category_Context_Ingestion.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order. Each lesson moves the sourcing event forward one stage.
5. When stuck, check `solutions/`.
6. Lesson 5 produces the award recommendation memo that goes to your VP for approval.
