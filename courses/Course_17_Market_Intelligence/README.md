# Course 17: Market Intelligence and Demand Management

A short course (about 6 hours) that teaches you to build a Claude Code system for connecting market data to sourcing decisions. You work with commodity price histories, supplier capabilities, stakeholder requirements, and market reports to build a market intelligence layer, consolidate demand, and run make-versus-buy analysis. No coding required beyond copy-paste prompts.

## What you will end up with

A market intelligence and demand management system. You point Claude Code at commodity price data and market reports. It tracks price trends, flags inflection points, and summarizes supply conditions. When stakeholder requirements arrive, the system consolidates overlapping demand across departments, identifies volume aggregation opportunities, and connects consolidated demand to current market conditions. One command produces a sourcing brief grounded in real market data instead of guesswork.

After Course 17, your sourcing recommendations cite specific price movements, supply trends, and consolidated volumes instead of anecdotal market knowledge.

## What you need before you start

- Courses 1 through 16 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, pipelines, projects, MCP, composition, category management, supplier risk, contract intelligence, supplier lifecycle, P2P compliance, and sourcing sprints.
- A laptop with Claude Code installed and signed in.
- About 6 hours, in two or three sittings.

## What is in this course folder

```
Course_17_Market_Intelligence/
├── README.md                            (this file)
├── COURSE_OVERVIEW.md                   (the story behind the course)
├── lessons/                             (six lessons, do them in order)
│   ├── Lesson_01_Market_Intelligence_Ingestion.md
│   ├── Lesson_02_Commodity_Tracker.md
│   ├── Lesson_03_Requirements_Processing.md
│   ├── Lesson_04_Demand_Consolidation.md
│   ├── Lesson_05_Make_Vs_Buy.md
│   └── Lesson_06_Sourcing_Brief.md
├── practice/                            (your hands-on workspace)
│   ├── CLAUDE.md                        (project context for Atlas Manufacturing)
│   ├── commodity-prices.csv             (192 rows, 6 commodities, 32 months)
│   ├── supplier-capabilities.csv        (20 suppliers with capability data)
│   ├── demand-intake/                   (8 stakeholder requirement files)
│   ├── market-intelligence/             (4 market report files)
│   └── Drafts/                          (your working files go here)
├── solutions/                           (reference answers; look only after attempting)
└── scripts/build_course_data.py         (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| practice/ | commodity-prices.csv | 192 rows. 6 commodities tracked monthly for 32 months (2023-08 through 2026-03). Fields: commodity_id, commodity_name, unit, date, price, change_pct, trend. Commodities: hot-rolled steel, cold-rolled steel, aluminum, copper, polypropylene, natural rubber. |
| practice/ | supplier-capabilities.csv | 20 suppliers. Fields: supplier_id, supplier_name, location, capability_description, lead_time_days, capacity_available_pct, capability_score, certifications, make_capability, currently_supplying_atlas. |
| practice/demand-intake/ | 8 requirement files | Stakeholder requirements in mixed formats (structured forms, emails, memos, voicemail transcripts). Departments include Engineering, Manufacturing (Plants 1 and 2), Logistics, IT, and Facilities. Industrial gaskets appear across three specs. Hydraulic fittings appear across two specs, creating consolidation opportunities. |
| practice/market-intelligence/ | 4 report files | Steel price outlook, Section 301 tariff regulatory update, Midwest supply chain disruption alert, and supplier capability benchmark from a spring trade show. Each report covers a different signal_type: price_movement, regulatory_change, supply_disruption, and capability_update. |
| practice/Drafts/ | (empty) | Your working files land here. Market signals, commodity trackers, demand specs, consolidation reports, and sourcing briefs all save to Drafts/. |

Today's date in the data is **2026-04-25**. Atlas Manufacturing has $58M in annual procurement spend.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_Market_Intelligence_Ingestion.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order. Each lesson adds a new capability to the system.
5. When stuck, check `solutions/`.
6. Lesson 6 connects market intelligence to sourcing decisions so your recommendations are grounded in data, not assumptions.

## If you delete or corrupt the practice data

Run the regenerator from the course root:

```
python scripts/build_course_data.py
```

It rewrites `commodity-prices.csv`, `supplier-capabilities.csv`, the eight demand-intake files, and the four market-intelligence reports back to their original state. The script is deterministic (`random.seed(42)`), so you get the same data every time.
