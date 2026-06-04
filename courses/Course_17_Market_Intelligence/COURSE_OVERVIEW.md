# Course 17: Market Intelligence and Demand Management

## Sourcing in the dark

It is Thursday morning, 08:15. You are the Market Intelligence Analyst at Atlas Manufacturing, a US-based industrial company with $58M in annual procurement spend. Your Director of Strategic Sourcing, Karen Webb, drops a question at the morning stand-up: "Steel prices moved 12% in the last quarter. Should we lock in pricing now or wait? And three departments submitted overlapping requests for polymer resin this month. Are we consolidating or buying three times?"

You do not have a good answer to either question. The commodity price data sits in a spreadsheet that someone updates monthly when they remember. Market reports arrive as PDFs from industry associations and land in a shared folder nobody checks. Stakeholder requirements arrive by email, and nobody cross-references them across departments.

Your sourcing decisions are disconnected from market reality. You buy based on last year's contracts, not this quarter's conditions. You miss volume aggregation opportunities because each department submits requirements independently. You cannot tell your Director whether steel is trending up or down without opening three browser tabs and a spreadsheet.

This course fixes that. You build a Claude Code system that ingests commodity price data, reads market reports, tracks trends, processes stakeholder requirements, consolidates overlapping demand, and connects market conditions to sourcing recommendations. When your Director asks about steel prices, you run one command and get a brief with 24 months of price history, the current trend, and a recommendation tied to supply conditions.

## What a market intelligence system does

A market intelligence system connects external market data to internal sourcing decisions. It tracks commodity prices over time, summarizes market reports, identifies demand overlap across departments, and produces sourcing briefs that cite specific data points.

| Without market intelligence | With market intelligence |
|---|---|
| Commodity prices checked ad hoc, no trend tracking | 24 months of price history with trend analysis on demand |
| Market reports filed in shared folders, rarely read | Reports ingested and summarized, key findings extracted |
| Stakeholder requirements processed one at a time | Requirements consolidated across departments, overlaps identified |
| Volume aggregation opportunities missed | Demand grouped by commodity, total volume calculated |
| Make-versus-buy decisions based on intuition | Analysis grounded in supplier capabilities and market pricing |
| Sourcing briefs cite "market conditions" with no data | Briefs cite specific price movements, percentages, and dates |

## The practice scenario

Atlas Manufacturing is a US-based industrial company with $58M in annual procurement spend across raw materials, IT services, logistics, and facilities. You are the Market Intelligence Analyst, reporting to Karen Webb, Director of Strategic Sourcing.

Your data covers 8 commodities tracked monthly for 24 months:

| Commodity | Unit | 24-month trend | Current price |
|---|---|---|---|
| Steel (hot rolled) | USD/ton | Volatile, up 7% YoY | ~$720/ton |
| Steel (cold rolled) | USD/ton | Stable, up 3% YoY | ~$880/ton |
| Polymer resin | USD/kg | Rising, up 11% YoY | ~$1.85/kg |
| Aluminum sheet | USD/sq ft | Down 4% YoY | ~$3.10/sq ft |
| Copper wire | USD/lb | Up 15% YoY | ~$4.50/lb |
| Electronic components | USD/each | Stable | ~$12.00/each |
| Natural gas | USD/MMBtu | Seasonal, down 6% YoY | ~$2.80/MMBtu |
| Diesel fuel | USD/gal | Volatile | ~$3.65/gal |

Six stakeholder requirements arrived this month from five departments. Two involve polymer resin, creating a consolidation opportunity.

Four quarterly market reports cover steel, polymers, logistics, and IT services.

Today's date is **2026-04-25**. Karen wants a consolidated market brief and demand analysis by **2026-05-02**.

## What you will build

```
market-intelligence-2026/
├── .claude/
│   ├── settings.json                (permissions, hooks)
│   └── commands/
│       ├── market-brief.md          (consolidated market intelligence summary)
│       ├── commodity-tracker.md     (price trend analysis for a commodity)
│       └── demand-consolidation.md  (cross-department demand analysis)
├── CLAUDE.md                        (role, category definitions, consolidation rules)
├── data/
│   ├── commodity-prices.csv         (192 rows, read-only)
│   ├── supplier-capabilities.csv    (20 suppliers, read-only)
│   ├── demand-intake/               (6 requirement files, read-only)
│   └── market-intelligence/         (4 market reports, read-only)
├── outputs/
│   ├── market-brief.md              (consolidated market intelligence)
│   ├── commodity-trackers/          (per-commodity trend reports)
│   ├── demand-consolidation.md      (cross-department demand summary)
│   ├── make-vs-buy-analysis.md      (make-versus-buy recommendation)
│   └── sourcing-brief.md            (market-linked sourcing recommendations)
└── skills/
    ├── analyze-commodity-trend.md   (commodity price analysis pattern)
    └── consolidate-demand.md        (demand consolidation pattern)
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | Market intelligence ingestion: reading market reports and extracting key findings | 55 min |
| 2 | Commodity tracker: building price trend analysis from 24 months of data | 60 min |
| 3 | Stakeholder requirements processing: reading and structuring demand from six departments | 50 min |
| 4 | Demand consolidation: identifying overlaps and calculating aggregated volumes | 55 min |
| 5 | Make-versus-buy analysis: comparing internal capability to market options | 55 min |
| 6 | Connecting market intelligence to sourcing: producing a sourcing brief grounded in data | 55 min |

Total: about 6 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. The market intelligence summary covers all four market reports and extracts at least three key findings from each (supply condition, price outlook, and one risk factor).
2. The commodity tracker for steel shows 24 months of price history, identifies the trend direction, calculates year-over-year change, and flags months with price swings above 5%.
3. All six stakeholder requirements are structured into a consistent format with department, requestor, commodity, quantity, specification, and timeline.
4. The demand consolidation report identifies at least one overlap (polymer resin across two departments), calculates the combined volume, and estimates the volume discount opportunity.
5. The make-versus-buy analysis for at least one commodity compares internal capability (from supplier-capabilities.csv) against market pricing (from commodity-prices.csv) and recommends buy, make, or hybrid with specific figures.
6. The sourcing brief ties at least two recommendations to specific market data points (e.g., "Lock in polymer resin pricing now. Prices rose 11% year over year and the Q1 2026 market report forecasts continued tightening through Q3 2026.").
