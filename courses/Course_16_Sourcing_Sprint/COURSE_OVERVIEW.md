# Course 16: Sourcing Sprint

## Six weeks to award, starting now

It is Monday morning, 08:30. You are the Senior Category Manager at Ironbridge Manufacturing, a US-based industrial company. Your CPO, Lisa Torres, stops by your desk. "The direct materials contracts are up in Q3. I need an award recommendation on my desk by June 20. That is six weeks. The board meets June 25."

You have $22.2M in annual direct materials spend across 10 active suppliers and 2 prospective ones. Steel, polymers, aluminum, electronic components, fasteners, and coatings. The top three suppliers account for 50% of spend. One supplier, Apex Electronics, has declining quality scores. The CPO wants an 8-12% cost reduction, at least one new qualified supplier to reduce single-source risk, and improved payment terms on contracts over $1M.

Normally, a sourcing event this size takes 8 to 10 weeks. You need to compress it to six. The RFP has to go out by May 2. Bids close June 6. Evaluation wraps June 13. Award recommendation due June 20.

This course teaches you to run that sprint with Claude Code. You ingest your category data, generate the RFP package, create supplier response templates, process and score six bids against weighted criteria, and draft the award recommendation memo. Five lessons, five stages, one complete sourcing event.

## What a sourcing sprint system does

A sourcing sprint system moves a competitive sourcing event from category analysis through award recommendation in a structured sequence. Each stage produces a specific deliverable. Claude Code reads your data, applies your criteria, and generates each deliverable for your review.

| Without a sourcing sprint system | With a sourcing sprint system |
|---|---|
| Spend analysis built manually in Excel, 4 to 6 hours | Category context ingested and summarized in 15 minutes |
| RFP drafted from scratch or copied from old events | RFP generated from scope notes with current data and criteria |
| Response template varies by event, inconsistent structure | Standardized template aligned to evaluation criteria |
| Bid scoring done in spreadsheets, prone to weighting errors | Automated scoring against weighted criteria, auditable |
| Award memo drafted from memory after weeks of analysis | Memo generated from scored data with supplier comparisons |

## The practice scenario

Ironbridge Manufacturing is a US-based industrial company with $22.2M in annual direct materials spend. You are the Senior Category Manager, reporting to Tom Baker, Supply Chain Director. Lisa Torres, VP of Procurement, is the approver.

Your sourcing event covers six sub-categories:

| Sub-category | Current annual spend | Incumbent supplier | Key issue |
|---|---|---|---|
| Steel | $4.2M | Great Lakes Steel (SUP001) | Single source, price volatility |
| Polymers | $3.8M | Heartland Polymers (SUP002) | Long lead times |
| Aluminum | $3.4M | Pacific Aluminum (SUP003) | Quality consistent, pricing competitive |
| Electronic components | $2.9M | Apex Electronics (SUP004) | Declining quality scores, at risk |
| Fasteners | $2.1M | Cascade Fasteners (SUP005) | Reliable but above-market pricing |
| Coatings | $1.6M | Various | Fragmented supply base |

Six suppliers submitted bids: Great Lakes Steel, Heartland Polymers, Pacific Aluminum, Cascade Fasteners, Northland Alloys (new), and Bayshore Materials (new).

Evaluation criteria from the scope notes:

| Criterion | Weight |
|---|---|
| Price competitiveness | 40% |
| Quality and capability | 25% |
| Delivery reliability | 20% |
| Financial stability | 15% |

Today's date is **2026-04-25**. RFP issue target: **2026-05-02**. Award recommendation due: **2026-06-20**.

## What you will build

```
sourcing-sprint-2026/
├── .claude/
│   ├── settings.json                (permissions, hooks)
│   └── commands/
│       ├── generate-rfp.md          (create RFP package from scope and spend)
│       ├── score-bids.md            (score all bids against criteria)
│       └── award-memo.md            (generate award recommendation)
├── CLAUDE.md                        (role, evaluation criteria, stakeholders)
├── Master/                          (read-only source files)
│   ├── spend-baseline.csv           (356 rows, $22.2M total)
│   ├── supplier-longlist.csv        (16 suppliers)
│   ├── scope-notes.md               (event scope)
│   └── bid-responses/               (12 CSVs: 6 suppliers x pricing + technical)
├── Drafts/                          (working files during the sprint)
│   ├── RFP_01_Cover_Letter.md       through RFP_06_Terms_And_Conditions.md
│   ├── response_template_pricing.csv
│   ├── response_template_technical.csv
│   ├── bid_validation.json
│   ├── pricing_comparison.json
│   ├── pricing_scores.json
│   ├── technical_scores.json
│   ├── bid_evaluation_matrix.csv
│   ├── award_recommendation.md
│   └── scorecard-SUPNNN.md          (per-supplier scorecards)
├── Outputs/                         (signed-off final deliverables)
├── Reference/                       (supporting reference notes)
└── skills/
    └── score-bid-response.md        (bid scoring pattern)
```

## The five lessons

| # | Title | Time |
|---|---|---|
| 1 | Category context ingestion: building the spend profile and supplier landscape | 55 min |
| 2 | RFP package generation: creating the RFP document from scope notes and spend data | 60 min |
| 3 | Supplier response template: designing a standardized bid format aligned to criteria | 50 min |
| 4 | Bid processing and scoring: reading six bids and scoring them against weighted criteria | 65 min |
| 5 | Award recommendation memo: assembling scores into a VP-ready recommendation | 55 min |

Total: about 5 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. The category context summary identifies the top three suppliers by spend, flags Apex Electronics as at risk, and quantifies the 8-12% savings target in dollars ($1.8M to $2.7M).
2. The RFP package includes scope, timeline, evaluation criteria with weights, submission requirements, and terms and conditions.
3. The response template maps directly to the four evaluation criteria so every bid arrives in a scorable format.
4. Each of the six bid scorecards shows a score for each criterion (0 to 100), the weighted score, and the total. The scoring is consistent: the same pricing gets the same price score across suppliers.
5. The award recommendation memo names the recommended supplier (or suppliers), the total contract value, the expected savings versus baseline, and a decision deadline. It includes no more than three recommendations.
