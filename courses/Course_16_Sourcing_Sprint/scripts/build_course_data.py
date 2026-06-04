"""Generate practice data for Course 16: Sourcing Sprint.

Scenario: end-to-end sourcing event for direct materials at Ironbridge
Manufacturing. The course folder is self-contained; this script regenerates
all practice files deterministically.

Output layout matches the lesson contract:

    practice/
      CLAUDE.md
      Master/                  read-only source files
        spend-baseline.csv     356 rows, 12 months direct materials, $22.2M
        supplier-longlist.csv  16 suppliers (10 active, 2 prospective bidders, 4 narrative)
        scope-notes.md         event scope, objectives, timeline, weights
        bid-responses/         6 bidders, each with pricing CSV and technical CSV
      Drafts/                  working files saved here during the lessons
      Outputs/                 final, signed-off deliverables
      Reference/               supporting reference notes
      skills/
        score-bid-response.md  reusable bid scoring pattern

Run with: python scripts/build_course_data.py

Deterministic via random.seed(42). All currency USD, US geography.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"
random.seed(42)
TODAY = date(2026, 4, 25)

# ---------------------------------------------------------------------------
# Sub-categories and target spend per the Lesson 1 worked example.
# ---------------------------------------------------------------------------

SUBCATEGORIES = {
    "Steel": {
        "target_spend": 4_200_000,
        "incumbent": ("SUP001", "Great Lakes Steel"),
        "incumbent_share": 1.00,
        "fillers": [],
        "parts": [
            ("ST-1001", "Hot-rolled steel plate, 12 mm", "ton", 1200, 720.00),
            ("ST-1002", "Cold-rolled steel coil, 4 mm", "ton", 800, 845.00),
            ("ST-1003", "Steel bracket blank, 6 mm", "each", 24000, 18.50),
            ("ST-1004", "Precision-machined steel bracket A", "each", 18000, 42.00),
        ],
    },
    "Polymers": {
        "target_spend": 3_800_000,
        "incumbent": ("SUP002", "Heartland Polymers"),
        "incumbent_share": 0.94,
        "fillers": [("SUP008", "Frontier Plastics")],
        "parts": [
            ("PM-2001", "ABS resin, automotive grade", "kg", 220000, 4.20),
            ("PM-2002", "Polycarbonate sheet, 3 mm", "sheet", 12000, 38.00),
            ("PM-2003", "Polymer gasket compound", "kg", 60000, 9.80),
        ],
    },
    "Aluminum": {
        "target_spend": 3_400_000,
        "incumbent": ("SUP003", "Pacific Aluminum"),
        "incumbent_share": 0.87,
        "fillers": [("SUP007", "Liberty Composites")],
        "parts": [
            ("AL-3001", "6061-T6 aluminum bar, 25 mm", "ft", 18000, 22.50),
            ("AL-3002", "Aluminum sheet, 1.5 mm", "sheet", 9000, 96.00),
            ("AL-3003", "Aluminum extrusion, custom profile", "ft", 14000, 18.00),
        ],
    },
    "Electronics": {
        "target_spend": 2_900_000,
        "incumbent": ("SUP004", "Apex Electronics"),
        "incumbent_share": 0.90,
        "fillers": [("SUP009", "Harbor Wire")],
        "parts": [
            ("EC-4001", "Sensor module, 24 V", "each", 6000, 78.00),
            ("EC-4002", "Connector harness, 8-pin", "each", 22000, 32.50),
            ("EC-4003", "Control board, 4-channel", "each", 1800, 285.00),
        ],
    },
    "Fasteners": {
        "target_spend": 2_100_000,
        "incumbent": ("SUP005", "Cascade Fasteners"),
        "incumbent_share": 0.90,
        "fillers": [("SUP006", "Summit Metals")],
        "parts": [
            ("FS-5001", "M8 hex bolt, zinc plated", "each", 480000, 0.42),
            ("FS-5002", "M10 lock nut, stainless", "each", 320000, 0.85),
            ("FS-5003", "Thread-forming screw kit", "kit", 9000, 32.00),
        ],
    },
    "Coatings": {
        "target_spend": 1_600_000,
        "incumbent": ("SUP010", "Keystone Coatings"),
        "incumbent_share": 0.40,  # fragmented per worked example
        "fillers": [("SUP006", "Summit Metals"), ("SUP007", "Liberty Composites")],
        "parts": [
            ("CT-6001", "Epoxy primer, gray", "gal", 4800, 96.00),
            ("CT-6002", "Powder coat, black", "lb", 18000, 11.50),
            ("CT-6003", "Anti-corrosion topcoat", "gal", 2400, 142.00),
        ],
    },
}

# Total target: $18.0M base across the six sub-categories. Lessons quote
# $22.2M total. Add an "Other" residual (legitimate trailing direct-materials
# MRO and packaging spend) so the baseline sums to $22.2M.
RESIDUAL_TARGET = 22_200_000 - sum(s["target_spend"] for s in SUBCATEGORIES.values())

# Supplier longlist:
# - 10 active (have spend in the baseline)
# - 2 prospective new entrants (Northland Alloys, Bayshore Materials)
# - 4 narrative names referenced in the lessons (Titan Precision, Cascade
#   Metals, Summit Steel, Atlas Metalworks). These appear in the longlist
#   as approved or prospective suppliers so the lesson narrative ties back
#   to a real row, but they are not among the six bidders.
SUPPLIERS = [
    # supplier_id, name, city, state, tier, annual_spend_usd, status, capability_match, risk_rating
    ("SUP001", "Great Lakes Steel",  "Chicago",     "IL", "strategic",  4_200_000, "active",      "high",   "high"),
    ("SUP002", "Heartland Polymers", "Houston",     "TX", "strategic",  3_572_000, "active",      "high",   "medium"),
    ("SUP003", "Pacific Aluminum",   "Portland",    "OR", "preferred",  2_958_000, "active",      "high",   "low"),
    ("SUP004", "Apex Electronics",   "San Jose",    "CA", "preferred",  2_610_000, "at_risk",     "medium", "high"),
    ("SUP005", "Cascade Fasteners",  "Seattle",     "WA", "preferred",  1_890_000, "active",      "high",   "low"),
    ("SUP006", "Summit Metals",      "Denver",      "CO", "approved",   1_200_000, "active",      "medium", "low"),
    ("SUP007", "Liberty Composites", "Detroit",     "MI", "approved",     980_000, "active",      "medium", "medium"),
    ("SUP008", "Frontier Plastics",  "Dallas",      "TX", "approved",     228_000, "active",      "medium", "medium"),
    ("SUP009", "Harbor Wire",        "Baltimore",   "MD", "approved",     290_000, "active",      "medium", "medium"),
    ("SUP010", "Keystone Coatings",  "Pittsburgh",  "PA", "spot",          640_000, "active",      "low",    "medium"),
    ("SUP011", "Northland Alloys",   "Minneapolis", "MN", "new",                 0, "prospective", "high",   "low"),
    ("SUP012", "Bayshore Materials", "Tampa",       "FL", "new",                 0, "prospective", "high",   "low"),
    # Narrative-example suppliers from the lessons. Approved on the longlist,
    # not active in current spend.
    ("SUP013", "Titan Precision LLC", "Cleveland",  "OH", "approved",            0, "prospective", "high",   "low"),
    ("SUP014", "Cascade Metals",      "Tacoma",     "WA", "approved",            0, "prospective", "high",   "low"),
    ("SUP015", "Summit Steel",        "Birmingham", "AL", "approved",            0, "prospective", "high",   "medium"),
    ("SUP016", "Atlas Metalworks",    "Cincinnati", "OH", "approved",            0, "prospective", "medium", "medium"),
]

CAPABILITY_NOTES = {
    "SUP001": "Steel",
    "SUP002": "Polymers",
    "SUP003": "Aluminum",
    "SUP004": "Electronics",
    "SUP005": "Fasteners",
    "SUP006": "Fasteners, Coatings",
    "SUP007": "Aluminum, Coatings",
    "SUP008": "Polymers",
    "SUP009": "Electronics",
    "SUP010": "Coatings",
    "SUP011": "Steel, Aluminum",
    "SUP012": "Polymers, Coatings",
    "SUP013": "Steel, Precision Machining",
    "SUP014": "Steel, Aluminum",
    "SUP015": "Steel",
    "SUP016": "Steel, Fasteners",
}


def _date_in_year(rng: random.Random) -> date:
    """Return a random date within the last 12 months from TODAY."""
    days_back = rng.randint(0, 365)
    return TODAY - timedelta(days=days_back)


def build_spend_baseline() -> list[dict]:
    """Build exactly 356 transaction rows summing to roughly $22.2M."""
    rng = random.Random(42)
    rows: list[dict] = []
    txn = 1001

    # Phase 1: 320 sub-category rows, distributed by target spend.
    target_rows = 320
    total_target = sum(s["target_spend"] for s in SUBCATEGORIES.values())
    for subcat, info in SUBCATEGORIES.items():
        share = info["target_spend"] / total_target
        n_rows = max(8, round(target_rows * share))
        incumbent_id, incumbent_name = info["incumbent"]
        for _ in range(n_rows):
            r = rng.random()
            if r < info["incumbent_share"] or not info["fillers"]:
                sid, sname = incumbent_id, incumbent_name
            else:
                sid, sname = rng.choice(info["fillers"])
            part = rng.choice(info["parts"])
            part_number, description, uom, annual_vol, unit_price = part
            qty = max(1, round(annual_vol / n_rows * rng.uniform(0.5, 1.6)))
            jitter = rng.uniform(0.94, 1.06)
            unit = round(unit_price * jitter, 2)
            amount = round(qty * unit, 2)
            rows.append({
                "transaction_id": f"TXN{txn:05d}",
                "date": _date_in_year(rng).isoformat(),
                "supplier_id": sid,
                "supplier_name": sname,
                "sub_category": subcat,
                "part_number": part_number,
                "description": description,
                "unit_of_measure": uom,
                "quantity": qty,
                "unit_price_usd": unit,
                "amount_usd": amount,
            })
            txn += 1

        # Scale this sub-category so the sub-category total hits target.
        current_subtotal = sum(r["amount_usd"] for r in rows if r["sub_category"] == subcat)
        scale = info["target_spend"] / current_subtotal if current_subtotal else 1.0
        for r in rows:
            if r["sub_category"] == subcat:
                r["amount_usd"] = round(r["amount_usd"] * scale, 2)
                r["unit_price_usd"] = round(r["unit_price_usd"] * scale, 2)

    # Phase 2: residual rows ("Other" category) so the 12-month total
    # matches the $22.2M baseline figure.
    residual_rows_n = 356 - len(rows)
    if residual_rows_n > 0 and RESIDUAL_TARGET > 0:
        per_row = RESIDUAL_TARGET / residual_rows_n
        other_suppliers = [
            ("SUP006", "Summit Metals"),
            ("SUP007", "Liberty Composites"),
            ("SUP008", "Frontier Plastics"),
            ("SUP009", "Harbor Wire"),
            ("SUP010", "Keystone Coatings"),
        ]
        other_items = [
            ("MR-7001", "MRO consumables, mixed", "lot", 12.00),
            ("MR-7002", "Tooling spares, replacement", "kit", 240.00),
            ("MR-7003", "Pallet and packaging", "lot", 38.00),
        ]
        for _ in range(residual_rows_n):
            sid, sname = rng.choice(other_suppliers)
            part_number, description, uom, _ = rng.choice(other_items)
            amount = round(per_row * rng.uniform(0.7, 1.3), 2)
            qty = max(1, rng.randint(1, 50))
            unit = round(amount / qty, 2)
            rows.append({
                "transaction_id": f"TXN{txn:05d}",
                "date": _date_in_year(rng).isoformat(),
                "supplier_id": sid,
                "supplier_name": sname,
                "sub_category": "Other",
                "part_number": part_number,
                "description": description,
                "unit_of_measure": uom,
                "quantity": qty,
                "unit_price_usd": unit,
                "amount_usd": amount,
            })
            txn += 1

    # Final scaling pass: pull the grand total to exactly $22.2M.
    grand = sum(r["amount_usd"] for r in rows)
    final_scale = 22_200_000 / grand
    for r in rows:
        r["amount_usd"] = round(r["amount_usd"] * final_scale, 2)
    rows.sort(key=lambda r: (r["sub_category"], r["supplier_id"], r["date"]))
    for i, r in enumerate(rows, start=1001):
        r["transaction_id"] = f"TXN{i:05d}"
    return rows


def build_supplier_longlist() -> list[dict]:
    rows = []
    for s in SUPPLIERS:
        sid, name, city, state, tier, spend, status, capability, risk = s
        rows.append({
            "supplier_id": sid,
            "supplier_name": name,
            "city": city,
            "state": state,
            "tier": tier,
            "annual_spend_usd": spend,
            "status": status,
            "capability_match": capability,
            "capabilities": CAPABILITY_NOTES[sid],
            "risk_rating": risk,
        })
    return rows


def build_scope_notes() -> str:
    return """# Direct Materials Sourcing Event: Scope Notes

## Category
Direct materials: steel, polymers, aluminum, electronic components, fasteners, and coatings.

## Current state
- 10 active suppliers, 2 prospective new entrants, 4 additional approved suppliers on the longlist.
- Annual spend: $22.2M across the category.
- Top 3 suppliers account for roughly 50% of spend.
- Apex Electronics (SUP004) is at_risk with declining quality scores.
- Steel is single source (Great Lakes Steel, 100% of sub-category).

## Objectives
1. Reduce unit costs by 8 to 12% through volume consolidation and competitive bidding.
2. Qualify at least one new supplier to reduce single-source risk on steel.
3. Improve payment terms from net-30 to net-45 on contracts above $1M.

## In scope
- Steel, polymers, aluminum, electronic components, fasteners, and coatings.
- Annual contract volume across all six sub-categories.
- Delivery to the Detroit assembly plant.

## Out of scope
- Indirect spend (office supplies, MRO, professional services).
- Capital equipment purchases.
- Service contracts.

## Constraints
- Lead time: production orders must ship within 21 business days.
- Quality: ISO 9001 certification required; defect rate target below 0.3%.
- Delivery terms: FOB destination preferred; FOB origin acceptable with freight quote.
- Contract term: 24 months with one 12-month renewal option.

## Timeline
- RFP issue target: 2026-05-02
- Q&A close: 2026-05-23
- Bid deadline: 2026-06-06
- Evaluation complete: 2026-06-13
- Award recommendation: 2026-06-20
- Board meeting: 2026-06-25

## Evaluation criteria
| Criterion | Weight |
|---|---|
| Price competitiveness | 40% |
| Quality and capability | 25% |
| Delivery reliability | 20% |
| Financial stability | 15% |

## Stakeholders
- Sarah Chen, Senior Category Manager (lead)
- Tom Baker, Supply Chain Director (sponsor)
- Lisa Torres, VP of Procurement (approver)
"""


def build_claude_md() -> str:
    return """# Ironbridge Manufacturing: Sourcing Sprint System

## Role

You are the Senior Category Manager at Ironbridge Manufacturing, a US-based industrial company with $22.2M in annual direct materials spend. You report to Tom Baker, Supply Chain Director. Lisa Torres, VP of Procurement, is the approver for award decisions. The CPO deadline for the award recommendation is 2026-06-20.

## Folder layout

The practice folder uses four working areas:

- **Master/**: read-only source files. Do not edit anything here.
- **Drafts/**: working files saved during the lessons.
- **Outputs/**: final, signed-off deliverables.
- **Reference/**: supporting notes the lessons may add to.

When a lesson prompt names a file without a folder prefix (for example, `spend-baseline.csv` or `bid-responses/`), look for it in `Master/`.

## Source files (read-only, in Master/)

- **spend-baseline.csv**: 356 rows of historical spend across direct materials. Fields: transaction_id, date, supplier_id, supplier_name, sub_category, part_number, description, unit_of_measure, quantity, unit_price_usd, amount_usd. Covers 12 months and totals $22.2M.
- **supplier-longlist.csv**: 16 suppliers (10 active, 2 prospective new entrants, 4 additional approved suppliers). Fields: supplier_id, supplier_name, city, state, tier, annual_spend_usd, status, capability_match, capabilities, risk_rating.
- **scope-notes.md**: sourcing event scope, objectives, timeline, evaluation criteria with weights, and stakeholder list.
- **bid-responses/**: 6 supplier bids. Each bidder has two CSV files: `bid_pricing_<Supplier>.csv` and `bid_technical_<Supplier>.csv`. Pricing files use the columns part_number, description, unit_of_measure, annual_volume, unit_price_usd, total_annual_price, tooling_cost_usd, freight_terms, lead_time_days, minimum_order_quantity. Technical files use question_id, question, response.

## Stakeholders

| Name | Title | Role in event |
|---|---|---|
| Sarah Chen | Senior Category Manager | Lead (you) |
| Tom Baker | Supply Chain Director | Sponsor |
| Lisa Torres | VP of Procurement | Approver |

## Evaluation criteria

| Criterion | Weight | Scoring guidance |
|---|---|---|
| Price competitiveness | 40% | Lowest total annual bid value gets 100. Others scored proportionally. |
| Quality and capability | 25% | ISO certifications, defect rates, quality references. Score 0 to 100. |
| Delivery reliability | 20% | Lead time, on-time delivery rate, geographic proximity. Score 0 to 100. |
| Financial stability | 15% | Revenue, years in business, credit rating, references. Score 0 to 100. |

## Sourcing event timeline

| Milestone | Date |
|---|---|
| RFP issue | 2026-05-02 |
| Q&A close | 2026-05-23 |
| Bid deadline | 2026-06-06 |
| Evaluation complete | 2026-06-13 |
| Award recommendation | 2026-06-20 |
| Board meeting | 2026-06-25 |

## Savings target

The CPO target is 8 to 12% cost reduction on $22.2M baseline spend. That translates to $1.8M to $2.7M in annual savings.

## Output standards

- All currency in USD with commas (for example, $4,200,000).
- Dates in YYYY-MM-DD format.
- Working files save to Drafts/.
- Final, signed-off deliverables save to Outputs/.
- Bid scorecards save to Drafts/ with filename pattern `scorecard-SUPNNN.md`.
- The award memo saves to Drafts/award_recommendation.md, then promoted to Outputs/ when finalized.
- Short sentences. Active voice.
- No em-dashes or en-dashes.
- Every scorecard names the supplier legal entity, the total weighted score, and the total bid value.
- The award memo names the recommended supplier, the contract value, the savings versus baseline, and the decision deadline.
- Recommendations capped at three.
"""


def build_skill_score_bid_response() -> str:
    return """# Skill: Score Bid Response

## Purpose

Read the bid files in `Master/bid-responses/`, score each supplier against the weighted evaluation criteria from `CLAUDE.md`, and write a scorecard to `Drafts/`. This skill works across sourcing events because it names input shapes, not specific values. Swap the data and the weights, and the same skill scores a different event.

## When to use

- After all bids have arrived in `Master/bid-responses/`.
- When you need a consistent, repeatable scoring pass across multiple suppliers.
- When the evaluation weights live in `CLAUDE.md` and may change between events.

## Inputs

1. `Master/bid-responses/`: one pricing CSV (`bid_pricing_<Supplier>.csv`) and one technical CSV (`bid_technical_<Supplier>.csv`) per supplier.
2. `Master/spend-baseline.csv`: baseline pricing per part number, used as the price benchmark.
3. `CLAUDE.md`: evaluation criteria with weights, scoring guidance, and output standards.

## Steps

1. List every file in `Master/bid-responses/`. Group by supplier (each supplier has a pricing CSV and a technical CSV).
2. For each supplier:
   a. Read the pricing CSV. Confirm the columns part_number, description, unit_of_measure, annual_volume, unit_price_usd, total_annual_price, tooling_cost_usd, freight_terms, lead_time_days, minimum_order_quantity are present.
   b. Validate that total_annual_price equals unit_price_usd times annual_volume within $1 tolerance.
   c. Sum total_annual_price across all parts to get the supplier's total annual bid value.
   d. Read the technical CSV. Confirm questions T1 through T10 are answered.
   e. Score price competitiveness: lowest total annual bid value across the set gets 100. Score the others proportionally as `100 x (lowest_bid / this_bid)`.
   f. Score quality and capability (T1 to T4) on a 0 to 100 scale.
   g. Score delivery reliability (T5 to T8) on a 0 to 100 scale.
   h. Score financial stability (T9 to T10) on a 0 to 100 scale.
   i. Compute the weighted total using the weights in `CLAUDE.md`.
3. Write one scorecard per supplier to `Drafts/scorecard-<SUPID>.md`. Name the supplier legal entity, the four sub-scores with a one-sentence justification each, the weighted total, and the total annual bid value.
4. Write a comparison table to `Drafts/scoring-summary.md` ranking all suppliers by weighted total, with columns: rank, supplier, price score, quality score, delivery score, financial score, weighted total, total annual bid value.

## Output

- One file per supplier: `Drafts/scorecard-<SUPID>.md`.
- One comparison file: `Drafts/scoring-summary.md`.

## Rules and guardrails

- Do not modify any file in `Master/`.
- If a bid CSV is missing a required column or value, flag it in the validation step and score that criterion as 0 with a note.
- Apply the same rubric to every supplier. If Supplier A's vague answer scores 45, Supplier B's equally vague answer scores 45.
- Use the weights from `CLAUDE.md` exactly. Do not invent new criteria.
- All currency in USD with commas.
"""


# ---------------------------------------------------------------------------
# Bid response data: 6 bidders, each with a pricing CSV and a technical CSV.
# ---------------------------------------------------------------------------

# Each bidder's part scope and proposed prices. The price is set as a
# percentage of the baseline unit price for that part to make the bids
# differentiable but realistic.
BIDDERS = [
    # (supplier_id, supplier_name, sub_categories_in_scope, price_factor,
    #  payment_terms, lead_time_days, on_time_pct, defect_pct, iso_status,
    #  revenue_m, years, dnb, references_count)
    ("SUP001", "Great_Lakes_Steel",  ["Steel"],                  0.955, 45, 12,  98, 0.4, "ISO 9001:2015 certificate GLS-9001-2024, expires 2027-08-31",  298, 25, "12-345-6789",  3),
    ("SUP002", "Heartland_Polymers", ["Polymers"],               0.929, 45, 14,  96, 0.6, "ISO 9001:2015 certificate HP-22148, expires 2026-11-30",      185, 22, "23-456-7890", 3),
    ("SUP003", "Pacific_Aluminum",   ["Aluminum"],               0.918, 45, 10,  99, 0.3, "ISO 9001:2015 and IATF 16949 certified, expires 2027-04-15",  412, 31, "34-567-8901", 3),
    ("SUP005", "Cascade_Fasteners",  ["Fasteners"],              0.910, 45, 11,  97, 0.7, "ISO 9001:2015 certificate CF-887, expires 2026-09-30",         98, 18, "45-678-9012", 3),
    ("SUP011", "Northland_Alloys",   ["Steel", "Aluminum"],      0.900, 60, 16,  92, 0.5, "ISO 9001:2015 certificate NA-2024-118, expires 2027-02-28",    74, 12, "56-789-0123", 2),
    ("SUP012", "Bayshore_Materials", ["Polymers", "Coatings"],   0.900, 60, 18,  90, 0.9, "ISO 9001 certification in progress, audit scheduled 2026-09",  52,  8, "67-890-1234", 2),
]


def _baseline_unit_price(part_number: str) -> tuple[float, int, str, str]:
    """Return baseline (unit_price, annual_volume, description, uom) for a part."""
    for info in SUBCATEGORIES.values():
        for pn, desc, uom, vol, price in info["parts"]:
            if pn == part_number:
                return price, vol, desc, uom
    raise KeyError(part_number)


def _parts_for_subcategories(subcats: list[str]) -> list[tuple]:
    """Return the part list (part_number, description, uom, annual_volume, baseline_price)
    for the given sub-categories."""
    parts = []
    for sub in subcats:
        for pn, desc, uom, vol, price in SUBCATEGORIES[sub]["parts"]:
            parts.append((pn, desc, uom, vol, price))
    return parts


def build_bid_pricing(sid: str, sname: str, subcats: list[str], factor: float) -> list[dict]:
    """Build the pricing CSV rows for one supplier."""
    rng = random.Random(hash(sid) & 0xFFFFFFFF)
    rows = []
    for pn, desc, uom, vol, baseline in _parts_for_subcategories(subcats):
        # Each part-line price is the supplier's factor times baseline,
        # plus a small per-part jitter to avoid uniform discounts.
        jitter = rng.uniform(0.97, 1.03)
        unit_price = round(baseline * factor * jitter, 2)
        total = round(unit_price * vol, 2)
        tooling = round(rng.uniform(2_000, 18_000), 2) if pn.startswith(("ST-1004", "AL-3003", "CT-")) else 0.0
        freight = "FOB destination" if rng.random() < 0.7 else "FOB origin"
        lead_time = rng.randint(8, 18)
        moq = max(1, vol // rng.randint(20, 60))
        rows.append({
            "part_number": pn,
            "description": desc,
            "unit_of_measure": uom,
            "annual_volume": vol,
            "unit_price_usd": unit_price,
            "total_annual_price": total,
            "tooling_cost_usd": tooling,
            "freight_terms": freight,
            "lead_time_days": lead_time,
            "minimum_order_quantity": moq,
        })
    return rows


def build_bid_technical(
    sid: str,
    sname: str,
    iso_status: str,
    defect_pct: float,
    lead_time_days: int,
    on_time_pct: int,
    revenue_m: int,
    years: int,
    dnb: str,
    references_count: int,
) -> list[dict]:
    """Build the technical CSV rows (10 questions, 10 answers) for one supplier."""
    name_pretty = sname.replace("_", " ")
    qa = [
        ("T1",
         "Describe your ISO 9001 or equivalent quality certification (include certificate number and expiry date).",
         iso_status),
        ("T2",
         "What is your current defect rate (PPM) for precision-machined steel parts?",
         f"Current defect rate: {defect_pct:.2f}%, equivalent to {int(defect_pct * 10000)} PPM. Measured against PPAP-approved control plans across the last 12 months."),
        ("T3",
         "List your three largest customers for similar parts, with annual volumes.",
         (f"Customer A: industrial OEM, $14.2M annual; Customer B: heavy equipment manufacturer, $9.8M annual; Customer C: tier-1 automotive supplier, $6.5M annual."
          if references_count >= 3
          else f"Customer A: industrial OEM, $7.4M annual; Customer B: agricultural equipment, $4.1M annual. References available on request.")),
        ("T4",
         "Describe your inspection process for machined tolerances.",
         "First-article inspection on every new part, AQL 1.0 sampling on production runs, CMM measurement on all critical dimensions, full SPC tracking on key features."),
        ("T5",
         "What is your standard lead time for first article and production orders?",
         f"First article: {lead_time_days + 5} business days. Production orders: {lead_time_days} business days from PO release."),
        ("T6",
         "Describe your capacity for this category (current utilization percentage and maximum monthly units).",
         f"Current utilization: {65 + (hash(sid) % 20)}%. Maximum monthly capacity: {revenue_m * 1500} units across our primary line. Surge capacity available on 30-day notice."),
        ("T7",
         "Do you have secondary or backup production capability? If yes, describe.",
         ("Yes. We operate two facilities in different states with mirrored equipment. Production can be transferred within 5 business days."
          if years >= 15
          else "Partial backup capability through a qualified subcontractor. Transfer time approximately 10 business days.")),
        ("T8",
         "Describe your freight and logistics capabilities to Detroit, MI.",
         f"Direct truckload service to Detroit assembly plant. On-time delivery: {on_time_pct}% over the last 12 months. FOB destination available; FOB origin with negotiated freight rates also offered."),
        ("T9",
         "Provide your Dun and Bradstreet number and most recent credit rating.",
         f"D&B number: {dnb}. Annual revenue: ${revenue_m}M. Years in operation: {years}. Most recent D&B PAYDEX score: {72 + (hash(sid) % 18)}."),
        ("T10",
         "Describe any value-add services (kitting, consignment, VMI) you offer.",
         "Kitting and consignment available on line items above 10,000 units annual. VMI program optional. Engineering support for design-for-manufacturability reviews included at no charge."),
    ]
    # Bayshore Materials (the smallest, prospective bidder) gives a vague
    # answer on T7 to mirror the lesson's "5 valid, 1 with missing answer
    # on T7" expectation.
    if sid == "SUP012":
        qa[6] = ("T7",
                 "Do you have secondary or backup production capability? If yes, describe.",
                 "")
    return [{"question_id": q, "question": question, "response": answer} for (q, question, answer) in qa]


def build_bid_responses(bids_dir: Path) -> int:
    """Write one pricing CSV and one technical CSV per bidder. Returns total file count."""
    file_count = 0
    for (sid, sname, subcats, factor, payterm, lead, on_time, defect, iso,
         revenue, years, dnb, refs) in BIDDERS:
        pricing_rows = build_bid_pricing(sid, sname, subcats, factor)
        technical_rows = build_bid_technical(sid, sname, iso, defect, lead, on_time, revenue, years, dnb, refs)

        pricing_path = bids_dir / f"bid_pricing_{sname}.csv"
        write_csv(pricing_path, pricing_rows, fieldnames=[
            "part_number", "description", "unit_of_measure", "annual_volume",
            "unit_price_usd", "total_annual_price", "tooling_cost_usd",
            "freight_terms", "lead_time_days", "minimum_order_quantity",
        ])
        file_count += 1

        technical_path = bids_dir / f"bid_technical_{sname}.csv"
        write_csv(technical_path, technical_rows, fieldnames=["question_id", "question", "response"])
        file_count += 1

    return file_count


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.relative_to(ROOT)}: {len(rows)} rows")


def main() -> None:
    print("Building Course 16 practice data...")
    print()

    master_dir = PRACTICE / "Master"
    bids_dir = master_dir / "bid-responses"
    drafts_dir = PRACTICE / "Drafts"
    outputs_dir = PRACTICE / "Outputs"
    reference_dir = PRACTICE / "Reference"
    skills_dir = PRACTICE / "skills"

    for d in (master_dir, bids_dir, drafts_dir, outputs_dir, reference_dir, skills_dir):
        d.mkdir(parents=True, exist_ok=True)

    # CLAUDE.md sits at practice/ root.
    claude_md_path = PRACTICE / "CLAUDE.md"
    with open(claude_md_path, "w", encoding="utf-8") as f:
        f.write(build_claude_md())
    print(f"  {claude_md_path.relative_to(ROOT)}: project context")

    # Master/ source files.
    write_csv(master_dir / "spend-baseline.csv", build_spend_baseline())
    write_csv(master_dir / "supplier-longlist.csv", build_supplier_longlist())

    scope_path = master_dir / "scope-notes.md"
    with open(scope_path, "w", encoding="utf-8") as f:
        f.write(build_scope_notes())
    print(f"  {scope_path.relative_to(ROOT)}: sourcing scope document")

    bid_count = build_bid_responses(bids_dir)
    print(f"  {bids_dir.relative_to(ROOT)}/: {bid_count} bid CSV files (6 suppliers x 2 files)")

    # Skill file.
    skill_path = skills_dir / "score-bid-response.md"
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(build_skill_score_bid_response())
    print(f"  {skill_path.relative_to(ROOT)}: reusable bid scoring pattern")

    # Keep Drafts/, Outputs/, Reference/ empty with a .gitkeep marker.
    for d in (drafts_dir, outputs_dir, reference_dir):
        placeholder = d / ".gitkeep"
        placeholder.write_text("", encoding="utf-8")
        print(f"  {d.relative_to(ROOT)}/: ready (.gitkeep)")

    print()
    print("Done. Practice tree built under practice/.")


if __name__ == "__main__":
    main()
