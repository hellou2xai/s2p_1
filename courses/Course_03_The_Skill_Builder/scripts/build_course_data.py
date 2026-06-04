"""Generate the practice data set for Course 3: The Skill Builder.

Scenario: a logistics consolidation RFP. The student is sourcing carriers
to consolidate down from 14 incumbents to 4 strategic partners across road,
sea, and air lanes. Annual logistics spend baseline is around 11.2m GBP.

Produces a flat practice/ folder:
- inputs/ holds: category-brief.md, supplier-longlist.csv (25 carriers),
  spend-baseline.csv (~1,500 historical shipments)
- bid-responses/ holds 6 bid response markdown files (one per shortlisted bidder)
- templates/ holds skeleton templates for RFP, scorecard, award memo
- skills/ is empty: the student fills it across the lessons

Deterministic via random.seed(42).
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRACTICE = ROOT / "practice"

random.seed(42)

TODAY = date(2026, 4, 25)
YEAR_AGO = date(2025, 4, 26)


# ---------------------------------------------------------------------------
# Starter CLAUDE.md for the practice folder
# ---------------------------------------------------------------------------

STARTER_CLAUDE_MD = """# Practice project for Course 3 - The Skill Builder

## Who I am

I am a Strategic Sourcing Lead at Acme Plc, running a logistics consolidation
RFP that aims to consolidate 14 incumbent carriers down to 4 strategic
partners across road, sea, and air lanes. Annual baseline spend is roughly
11.2m GBP. The savings target is 1.6m GBP, around 14% off baseline.

## Folder layout

inputs/         the source documents I work from (category brief, longlist, baseline)
bid-responses/  the bid responses from shortlisted carriers
templates/      skeleton templates for RFP, scorecard, and award memo
skills/         my SKILL.md library (you, the student, fill these in across the lessons)
outputs/        deliverables Claude produces using the skills

## Folder rules

The CSVs and markdown files in inputs/ and bid-responses/ are the source of truth.
Read them when I ask. Do not modify them.
Save any new files (drafts, scorecards, memos) to outputs/.
The skills in skills/ are methodologies, not one-off prompts. They get reused
across every sourcing event.

## Writing rules

Use British English. Use organise, summarise, behaviour, colour.
Use Oxford commas. No em-dashes. Active voice.
Specific numbers, never "significant" or "material" for figures.
Cap recommendations at 3. Cap tables at 10 rows unless I name a different cap.
Every output bound for a CFO ends with an audit footer listing source files,
date, and the model used.
"""


# ---------------------------------------------------------------------------
# Category brief (input)
# ---------------------------------------------------------------------------

CATEGORY_BRIEF = """# Logistics consolidation - category brief

## Today

Today is 2026-04-25. The RFP must close by 2026-06-15 with award by 2026-06-30.

## Current state

We currently use 14 carriers across road FTL (8), road LTL (3), sea FCL (2),
and air freight (1). Annual logistics spend is 11.2m GBP. Coverage is uneven:
some lanes have three carriers competing, others rely on a single carrier.

The biggest annual spend is with FastRoad UK (1.8m), Globex Freight (1.5m),
and Atlantic Lines (1.4m). These three together cover 42% of total spend.
The remaining 11 carriers each cover under 5% of spend.

Service quality is also uneven. Two carriers (CAR014, CAR023) have on-time
delivery below 90% on critical lanes. One carrier (CAR018) has filed late
invoices on six of the last twelve months.

## Goal

Consolidate to 4 strategic carriers (1 road FTL, 1 road LTL plus parcel,
1 sea FCL, 1 air). Award contracts of 24 months with one 12-month extension.
Target a 14% saving against baseline (1.6m GBP annualised) plus measurable
service-level improvements (on-time over 95% across all critical lanes).

## Scope of the RFP

In scope: all UK domestic and UK-EU lanes, plus UK-Asia sea, plus UK-USA air.
Out of scope: parcel courier (managed under indirect category), drayage at
ports (managed under inbound logistics), and last-mile customer delivery
(managed by the customer fulfilment team).

## Stakeholders

Sponsor: Director of Operations.
Decision authority: CFO (over 1.0m GBP annualised commitment).
Reviewers: Head of Customer Fulfilment, Head of Procurement.

## Inputs you have

- supplier-longlist.csv: 25 candidate carriers we have shortlisted to bid.
- spend-baseline.csv: roughly 1,500 historical shipments over the last
  12 months that establish the baseline spend by lane.
- bid-responses/: six bid responses from shortlisted carriers.
- templates/: skeletons for the RFP, the scorecard, and the award memo.

## Inputs you do not have yet

- Final award memo (you produce it in Lesson 5).
- Pre-negotiation brief (Lesson 6 covers skill versioning, not negotiations).
"""


# ---------------------------------------------------------------------------
# Supplier longlist (25 carriers)
# ---------------------------------------------------------------------------

LONGLIST = [
    # carrier_id, name, modes, primary_geography, certifications,
    # capacity_tier, financial_health, otd_pct_12m, contract_terms_offered,
    # incumbent
    ("CAR001", "FastRoad UK", "road_ftl;road_ltl", "UK_and_EU",
     "ISO_9001+CarbonNeutral", "tier_1", "strong", 96.4, "Net_45;24m+12m", "yes"),
    ("CAR002", "TransEuro Express", "road_ltl;road_ftl", "EU",
     "ISO_9001", "tier_1", "strong", 93.2, "Net_45;24m+12m", "yes"),
    ("CAR003", "OceanLine", "sea_fcl", "UK_to_Asia",
     "ISO_9001+ISO_14001", "tier_1", "strong", 90.5, "Net_60;36m", "yes"),
    ("CAR004", "AirSwift", "air", "Global",
     "IATA", "tier_2", "strong", 99.1, "Net_45;24m", "yes"),
    ("CAR005", "Iberian Container", "sea_lcl;sea_fcl", "UK_to_Med",
     "ISO_9001", "tier_2", "stable", 87.8, "Net_60;24m", "yes"),
    ("CAR006", "Northern Drayage", "road_ftl", "UK_ports",
     "ISO_9001", "tier_2", "stable", 91.4, "Net_45;12m+12m", "no"),
    ("CAR007", "Polaris Cold Chain", "road_temp_controlled", "UK_and_EU",
     "ISO_9001+HACCP", "tier_2", "strong", 97.2, "Net_45;24m+12m", "yes"),
    ("CAR008", "Pacific Forwarders", "sea_fcl;air", "Asia_to_UK",
     "ISO_9001", "tier_1", "strong", 92.6, "Net_60;36m", "no"),
    ("CAR009", "UK Express Pallets", "road_pallet_network", "UK",
     "ISO_9001", "tier_3", "stable", 97.6, "Net_30;24m", "yes"),
    ("CAR010", "Globex Freight", "road_ftl", "UK_and_EU",
     "ISO_9001+CarbonNeutral", "tier_1", "strong", 96.0, "Net_45;36m+12m", "yes"),
    ("CAR011", "Mediterranean Marine", "sea_fcl", "UK_to_Med",
     "ISO_9001+ISO_14001", "tier_2", "stable", 89.1, "Net_60;24m", "no"),
    ("CAR012", "Helios Air Freight", "air", "Global",
     "IATA+ISO_9001", "tier_1", "strong", 98.6, "Net_45;36m+12m", "yes"),
    ("CAR013", "Britannia Pallets", "road_pallet_network", "UK",
     "ISO_9001", "tier_3", "stable", 96.0, "Net_30;24m", "no"),
    ("CAR014", "Atlantic Lines", "sea_fcl", "UK_to_Americas",
     "ISO_9001", "tier_1", "stable", 88.4, "Net_60;36m+12m", "yes"),
    ("CAR015", "Skyline Air", "air", "EU_and_Americas",
     "IATA", "tier_2", "stable", 97.4, "Net_45;24m", "no"),
    ("CAR016", "Channel Shipping", "sea_lcl", "UK_to_EU",
     "ISO_9001", "tier_3", "stable", 90.8, "Net_60;24m", "no"),
    ("CAR017", "Continental Roads", "road_ftl;road_ltl", "EU",
     "ISO_9001+CarbonNeutral", "tier_1", "strong", 95.2, "Net_45;24m+12m", "no"),
    ("CAR018", "ParcelFast UK", "parcel", "UK",
     "ISO_9001", "tier_3", "weak", 96.6, "Net_30;12m", "yes"),
    ("CAR019", "Euro Air Cargo", "air", "EU",
     "IATA", "tier_2", "stable", 96.8, "Net_45;24m", "no"),
    ("CAR020", "Adriatic Drayage", "road_drayage", "UK_ports",
     "ISO_9001", "tier_3", "stable", 90.2, "Net_45;12m", "no"),
    ("CAR021", "Nordic Freight", "road_ftl", "UK_and_Nordic",
     "ISO_9001+CarbonNeutral", "tier_2", "strong", 95.8, "Net_45;24m+12m", "no"),
    ("CAR022", "Iberia Express", "road_ltl", "UK_to_Iberia",
     "ISO_9001", "tier_3", "stable", 92.4, "Net_45;24m", "no"),
    ("CAR023", "Cardiff Maritime", "sea_lcl", "UK_to_Med",
     "ISO_9001", "tier_3", "weak", 86.8, "Net_60;24m", "yes"),
    ("CAR024", "Hibernia Roads", "road_ftl;road_ltl", "Ireland_and_UK",
     "ISO_9001", "tier_2", "stable", 94.6, "Net_45;24m+12m", "no"),
    ("CAR025", "AlpineAir Cargo", "air", "EU_and_Americas",
     "IATA+ISO_9001", "tier_2", "strong", 98.2, "Net_45;24m+12m", "no"),
]


# ---------------------------------------------------------------------------
# Spend baseline (1,500 historical shipments over the last year)
# ---------------------------------------------------------------------------

LANE_PROFILES = {
    "road_ftl": {
        "lanes": [
            ("Birmingham", "Munich", 1480, (2400, 3400)),
            ("Birmingham", "Hamburg", 1240, (2200, 3200)),
            ("Birmingham", "Lyon", 1180, (2100, 3000)),
            ("Birmingham", "Antwerp", 860, (1800, 2600)),
            ("Birmingham", "Glasgow", 720, (1100, 1800)),
            ("Coventry", "Madrid", 1680, (2800, 3800)),
            ("Coventry", "Lyon", 1180, (2000, 2900)),
            ("Manchester", "Hamburg", 1280, (2200, 3200)),
        ],
    },
    "road_ltl": {
        "lanes": [
            ("Coventry", "Madrid", 1680, (1100, 1700)),
            ("Birmingham", "Lyon", 1180, (840, 1300)),
            ("Coventry", "Lyon", 1180, (820, 1280)),
            ("Manchester", "Hamburg", 1280, (920, 1480)),
            ("Birmingham", "Munich", 1480, (1080, 1680)),
            ("Birmingham", "Glasgow", 720, (480, 780)),
        ],
    },
    "road_temp_controlled": {
        "lanes": [
            ("Manchester", "Stockholm", 2080, (3400, 4400)),
            ("Manchester", "Oslo", 2200, (3600, 4600)),
            ("Manchester", "Hamburg", 1280, (2400, 3200)),
        ],
    },
    "road_pallet_network": {
        "lanes": [
            ("Birmingham", "Glasgow", 720, (1100, 1700)),
            ("Birmingham", "Manchester", 140, (340, 620)),
            ("Birmingham", "Newcastle", 380, (640, 980)),
        ],
    },
    "sea_fcl": {
        "lanes": [
            ("Felixstowe", "Shanghai", 19800, (3000, 3500)),
            ("Felixstowe", "Singapore", 16400, (2800, 3300)),
            ("Felixstowe", "Hong Kong", 18400, (3100, 3600)),
            ("Liverpool", "New York", 5500, (2400, 2900)),
        ],
    },
    "sea_lcl": {
        "lanes": [
            ("Cardiff", "Genoa", 2100, (1300, 1800)),
            ("Felixstowe", "Antwerp", 320, (480, 740)),
            ("Cardiff", "Naples", 2300, (1400, 1900)),
        ],
    },
    "air": {
        "lanes": [
            ("Heathrow", "Frankfurt", 650, (4400, 5200)),
            ("Heathrow", "JFK New York", 5500, (6800, 7800)),
            ("Heathrow", "Singapore", 16400, (8800, 10200)),
            ("Heathrow", "Dubai", 5500, (5400, 6400)),
        ],
    },
    "parcel": {
        "lanes": [
            ("Multiple UK", "Multiple UK", 0, (10000, 16000)),
        ],
    },
    "road_drayage": {
        "lanes": [
            ("Felixstowe", "Birmingham", 260, (640, 880)),
            ("Liverpool", "Manchester", 60, (320, 480)),
        ],
    },
}


def gen_spend_baseline(n: int = 1500):
    rows = []
    days_total = (TODAY - YEAR_AGO).days
    incumbents = [c for c in LONGLIST if c[9] == "yes"]
    for i in range(n):
        # bias spend to incumbents (we have a year of history with them)
        carrier = random.choices(
            incumbents,
            weights=[1.0] * len(incumbents),
            k=1,
        )[0]
        car_id, _, modes, _, _, _, _, _, _, _ = carrier
        # pick a mode this carrier offers
        mode = random.choice(modes.split(";"))
        if mode not in LANE_PROFILES:
            mode = list(LANE_PROFILES.keys())[0]
        lane = random.choice(LANE_PROFILES[mode]["lanes"])
        origin, dest, _, (lo, hi) = lane
        total = round(random.uniform(lo, hi), 2)
        ship_date = YEAR_AGO + timedelta(days=random.randint(0, days_total))
        ship_id = f"SH-{i + 1:05d}"
        rows.append((ship_id, car_id, mode, origin, dest, total, ship_date.isoformat()))
    rows.sort(key=lambda r: r[6])
    return rows


# ---------------------------------------------------------------------------
# Bid responses (six suppliers shortlisted to bid)
# ---------------------------------------------------------------------------

BID_TEMPLATE = """# Bid response: {name}

**Bidder:** {name} ({carrier_id})
**RFP:** Acme Plc Logistics Consolidation 2026
**Submitted:** {submitted}
**Validity:** until 2026-08-31

## Executive summary

{exec_summary}

## Capability statement

{capability}

## Pricing table

| Lane | Mode | Volume per year (estimated) | Unit rate (GBP per shipment) | Annual value (GBP) |
|---|---|---|---|---|
{pricing_rows}

**Total annual price (GBP):** {total_annual}

**Implementation cost (one-off, GBP):** {implementation}

## Service commitments

- On-time delivery: {otd}% across all in-scope lanes, measured monthly.
- Damage rate: below {damage}% across all shipments.
- Invoice accuracy: {ia}% across all monthly invoice batches.
- Reporting: monthly KPI pack to Acme procurement, plus quarterly review.

## Contract terms

- Term: {term}.
- Payment terms: {payment}.
- Indexation: {indexation}.
- Exit: 90 days notice on either side after Year 1, with no exit fee.

## Three references

- **{ref1_name}** ({ref1_industry}). Annual spend: {ref1_spend} GBP. Contact: {ref1_contact}.
- **{ref2_name}** ({ref2_industry}). Annual spend: {ref2_spend} GBP. Contact: {ref2_contact}.
- **{ref3_name}** ({ref3_industry}). Annual spend: {ref3_spend} GBP. Contact: {ref3_contact}.

## Sustainability commitments

{sustainability}

## Closing

{closing}
"""


def gen_bid(carrier, profile):
    name = carrier[1]
    car_id = carrier[0]
    pricing_rows = "\n".join(
        f"| {lane} | {mode} | {vol} | {rate} | {ann} |"
        for lane, mode, vol, rate, ann in profile["pricing"]
    )
    return BID_TEMPLATE.format(
        name=name,
        carrier_id=car_id,
        submitted=profile["submitted"],
        exec_summary=profile["exec_summary"],
        capability=profile["capability"],
        pricing_rows=pricing_rows,
        total_annual=profile["total_annual"],
        implementation=profile["implementation"],
        otd=profile["otd"],
        damage=profile["damage"],
        ia=profile["ia"],
        term=profile["term"],
        payment=profile["payment"],
        indexation=profile["indexation"],
        sustainability=profile["sustainability"],
        closing=profile["closing"],
        ref1_name=profile["refs"][0][0], ref1_industry=profile["refs"][0][1],
        ref1_spend=profile["refs"][0][2], ref1_contact=profile["refs"][0][3],
        ref2_name=profile["refs"][1][0], ref2_industry=profile["refs"][1][1],
        ref2_spend=profile["refs"][1][2], ref2_contact=profile["refs"][1][3],
        ref3_name=profile["refs"][2][0], ref3_industry=profile["refs"][2][1],
        ref3_spend=profile["refs"][2][2], ref3_contact=profile["refs"][2][3],
    )


# Six shortlisted bidders
SHORTLIST_BIDS = [
    # (carrier_index, profile)
    (0, {  # CAR001 FastRoad UK (incumbent)
        "submitted": "2026-06-10",
        "exec_summary": "FastRoad UK is your incumbent road FTL and LTL provider. We propose a 24-month strategic partnership with one 12-month extension at flat unit rates. Our committed annual price is 5.2% below your current spend on equivalent lanes, plus a service-level improvement of 200 basis points on on-time delivery (target 96.5% from current 94.5% on critical lanes).",
        "capability": "We operate 480 tractor units across 11 UK depots, including dedicated cold-chain and oversize fleets. Our network covers all current Acme road lanes with no gaps. Year on year we have grown European LTL coverage by 18% and now offer overnight LTL into 14 EU countries.",
        "pricing": [
            ("Birmingham-Munich", "road_ftl", 180, 2750, 495000),
            ("Birmingham-Hamburg", "road_ftl", 144, 2580, 371520),
            ("Birmingham-Antwerp", "road_ftl", 96, 2240, 215040),
            ("Birmingham-Lyon", "road_ftl", 72, 2640, 190080),
            ("Coventry-Madrid", "road_ltl", 60, 1240, 74400),
            ("Birmingham-Munich", "road_ltl", 48, 1380, 66240),
        ],
        "total_annual": "1,412,280",
        "implementation": "0",
        "otd": "96.5",
        "damage": "0.7",
        "ia": "99.4",
        "term": "24 months with one 12-month extension at flat unit rates (year 4 indexed if extension exercised)",
        "payment": "Net 45 days from invoice date",
        "indexation": "No indexation in base term. CPI capped at 3% per year if extension exercised.",
        "sustainability": "Carbon neutral fleet certification verified by Carbon Trust. Quarterly carbon reporting per shipment included at no extra cost. SBT-aligned reduction plan to 2030.",
        "closing": "FastRoad UK welcomes the opportunity to deepen our partnership with Acme through this consolidation. Our pricing reflects committed volumes; should awarded volumes vary materially we are open to a structured volume-rate review at month 12.",
        "refs": [
            ("Brunton Industrial", "Manufacturing", "2,100,000", "K Patel, Director of Logistics"),
            ("Westwood Foods", "FMCG", "1,400,000", "M Cardew, Head of Supply Chain"),
            ("Lyle Engineering", "Engineering", "780,000", "S Holroyd, Operations Manager"),
        ],
    }),
    (9, {  # CAR010 Globex Freight (incumbent, biggest road competitor)
        "submitted": "2026-06-12",
        "exec_summary": "Globex Freight has serviced Acme road FTL since 2019. Our bid offers a 7.4% reduction against your current Globex unit rates plus a network-wide guarantee of 96% on-time delivery, with service credits where missed. We propose a 36-month term plus 12-month extension to amortise our planned investment in three new EU hubs.",
        "capability": "We operate 720 tractor units across 14 depots in the UK and EU. Our 2025 European Carbon Emissions Reduction programme cut average tonne-km emissions by 11% across the year. We are SBT-certified and carbon-neutral on UK domestic since 2024.",
        "pricing": [
            ("Birmingham-Munich", "road_ftl", 180, 2680, 482400),
            ("Birmingham-Hamburg", "road_ftl", 144, 2510, 361440),
            ("Birmingham-Antwerp", "road_ftl", 96, 2180, 209280),
            ("Birmingham-Lyon", "road_ftl", 72, 2570, 185040),
            ("Coventry-Madrid", "road_ftl", 36, 3100, 111600),
            ("Manchester-Hamburg", "road_ftl", 48, 2520, 120960),
        ],
        "total_annual": "1,470,720",
        "implementation": "32,000",
        "otd": "96.0",
        "damage": "0.7",
        "ia": "99.3",
        "term": "36 months with one 12-month extension. Year 1 to 3 at fixed rates. Year 4 to 5 indexed against UK HGV operating cost index, capped at 3.5% per year.",
        "payment": "Net 45 days",
        "indexation": "Year 1 to 3 fixed. Year 4 onwards UK HGV cost index, capped at 3.5%.",
        "sustainability": "Carbon-neutral on all UK lanes. SBT 1.5C scope 1 and 2 reduction plan with 2030 milestones. Quarterly carbon reporting included.",
        "closing": "Globex Freight is committed to a long-term partnership and prepared to invest 18m GBP into our European network across the contract term, including three new hubs that will benefit Acme's central European volume.",
        "refs": [
            ("Marlborough Manufacturing", "Industrial", "3,200,000", "D Heath, CPO"),
            ("Severnside Pharma", "Pharma", "1,800,000", "L Quinn, Director of Procurement"),
            ("Atlas Components", "Automotive", "2,400,000", "T Pasternak, Logistics Director"),
        ],
    }),
    (16, {  # CAR017 Continental Roads (challenger, not incumbent)
        "submitted": "2026-06-13",
        "exec_summary": "Continental Roads has not previously served Acme. We are bidding aggressively to win a place on your strategic carrier panel. Our proposed annual price is 11.8% below the FastRoad and Globex blended rate on equivalent lanes. We commit to onboarding within 30 days at our cost.",
        "capability": "We are a tier-1 European challenger with 360 tractor units across 8 depots. Our European LTL network is operated through partner carriers under a single SLA framework and a unified TMS. Our 2025 average on-time delivery across the UK-EU corridor was 95.2%.",
        "pricing": [
            ("Birmingham-Munich", "road_ftl", 180, 2420, 435600),
            ("Birmingham-Hamburg", "road_ftl", 144, 2280, 328320),
            ("Birmingham-Antwerp", "road_ftl", 96, 2050, 196800),
            ("Birmingham-Lyon", "road_ftl", 72, 2380, 171360),
            ("Coventry-Madrid", "road_ltl", 60, 1090, 65400),
            ("Birmingham-Lyon", "road_ltl", 48, 1180, 56640),
        ],
        "total_annual": "1,254,120",
        "implementation": "0",
        "otd": "95.0",
        "damage": "0.9",
        "ia": "98.4",
        "term": "24 months with one 12-month extension at flat rates",
        "payment": "Net 45 days",
        "indexation": "No indexation in base term. CPI capped at 3% if extension exercised.",
        "sustainability": "Carbon-neutral on UK lanes from 2026, EU lanes by 2028. SBT certification process started.",
        "closing": "Continental Roads is offering a partnership-grade entry price specifically to build a track record with Acme. We are willing to put 4% of annual fees at risk against on-time delivery and damage-rate KPIs across Year 1.",
        "refs": [
            ("Pennine Drinks", "FMCG", "1,200,000", "R Singh, Logistics Lead"),
            ("Eider Aerospace", "Aerospace", "880,000", "B Lockhart, VP Supply Chain"),
            ("Coastal Foods", "FMCG", "640,000", "F Aldridge, Procurement Lead"),
        ],
    }),
    (2, {  # CAR003 OceanLine (incumbent)
        "submitted": "2026-06-09",
        "exec_summary": "OceanLine is your incumbent UK-Asia sea FCL provider. We propose a 36-month flat-rate agreement with no BAF surcharge in Year 1, an 8% reduction against your current 2025 average, and priority space allocation on our weekly UK-Shanghai service.",
        "capability": "Our UK-Asia service operates with 14 vessels across two strings, with weekly direct sailings from Felixstowe to Shanghai, Singapore, and Hong Kong. Our 2025 schedule reliability on these strings averaged 90.5%, the best in our segment per Drewry's Q4 2025 ranking.",
        "pricing": [
            ("Felixstowe-Shanghai", "sea_fcl", 96, 3050, 292800),
            ("Felixstowe-Singapore", "sea_fcl", 60, 2920, 175200),
            ("Felixstowe-Hong Kong", "sea_fcl", 48, 3120, 149760),
        ],
        "total_annual": "617,760",
        "implementation": "0",
        "otd": "90.5",
        "damage": "0.4",
        "ia": "99.0",
        "term": "36 months at flat rates",
        "payment": "Net 60 days",
        "indexation": "BAF surcharge waived in Year 1. From Year 2, BAF tied to public bunker index with quarterly reset.",
        "sustainability": "All UK-Shanghai sailings on dual-fuel LNG ready vessels. SBT-aligned reduction plan submitted to CDP.",
        "closing": "OceanLine values the partnership with Acme and is willing to put schedule-reliability KPIs on a published quarterly scorecard with rebates against missed targets.",
        "refs": [
            ("Riverbend Tech", "Electronics", "1,400,000", "Y Sato, Director of Trade"),
            ("Heathfield Imports", "Retail", "2,200,000", "M Okafor, Logistics Lead"),
            ("Kingston Components", "Industrial", "780,000", "P Vasquez, Procurement Lead"),
        ],
    }),
    (7, {  # CAR008 Pacific Forwarders (challenger, sea FCL alternative)
        "submitted": "2026-06-13",
        "exec_summary": "Pacific Forwarders is a tier-1 challenger to OceanLine on the UK-Asia FCL corridor. Our 2025 schedule reliability hit 92.6% across the same trade lanes, the highest of the bidders. We bid 6.2% below the OceanLine 2025 spot average.",
        "capability": "Our UK-Asia service is operated jointly with three regional partners under a single SLA. We have invested 280m EUR into UK-Asia capacity expansion since 2023.",
        "pricing": [
            ("Felixstowe-Shanghai", "sea_fcl", 96, 2870, 275520),
            ("Felixstowe-Singapore", "sea_fcl", 60, 2750, 165000),
            ("Felixstowe-Hong Kong", "sea_fcl", 48, 2980, 143040),
        ],
        "total_annual": "583,560",
        "implementation": "18,000",
        "otd": "92.6",
        "damage": "0.5",
        "ia": "98.8",
        "term": "36 months",
        "payment": "Net 60 days",
        "indexation": "BAF tied to public bunker index, quarterly reset, capped at 4% per quarter.",
        "sustainability": "All major sailings on Tier III emission vessels. Carbon offset programme covering 100% of customer container-km from 2027.",
        "closing": "Pacific Forwarders is offering a strategic discount to break into the Acme partnership. We are willing to commit weekly capacity reservations and a published service-reliability scorecard.",
        "refs": [
            ("Marston Tech", "Electronics", "920,000", "K Yamaguchi, Director of Trade"),
            ("Westcoast Foods", "FMCG", "1,640,000", "M Lindh, Logistics Director"),
            ("Anchor Industries", "Industrial", "1,180,000", "T Adeyemo, Supply Chain Lead"),
        ],
    }),
    (11, {  # CAR012 Helios Air Freight (incumbent)
        "submitted": "2026-06-11",
        "exec_summary": "Helios Air Freight is your incumbent global air provider. We propose a 36-month flat-rate agreement with capacity guarantees on Heathrow-JFK and Heathrow-Singapore. Our annual price is 4.6% below your 2025 spot average across the same lanes plus a 100bps improvement on on-time delivery.",
        "capability": "We operate 22 wide-body freighters across our global network, plus block-space agreements with three airline partners. Our 2025 average on-time delivery was 98.6% across all lanes.",
        "pricing": [
            ("Heathrow-Frankfurt", "air", 84, 4720, 396480),
            ("Heathrow-JFK", "air", 60, 7200, 432000),
            ("Heathrow-Singapore", "air", 36, 9400, 338400),
            ("Heathrow-Dubai", "air", 24, 5800, 139200),
        ],
        "total_annual": "1,306,080",
        "implementation": "0",
        "otd": "98.6",
        "damage": "0.2",
        "ia": "99.7",
        "term": "36 months at flat rates",
        "payment": "Net 45 days",
        "indexation": "Fuel surcharge tied to public jet-fuel index, monthly reset, capped at 6% per month.",
        "sustainability": "SAF (sustainable aviation fuel) blending of 8% in 2026, rising to 25% by 2030. Carbon offset programme covers all customer freight-km.",
        "closing": "Helios values the long-term relationship with Acme and is willing to put our scorecard performance on a published quarterly basis with rebates for missed lanes.",
        "refs": [
            ("Quartermaster Components", "Industrial", "1,420,000", "K Esposito, Director of Trade"),
            ("Stratford Pharma", "Pharma", "780,000", "Y Jain, Logistics Lead"),
            ("Northridge Aerospace", "Aerospace", "2,100,000", "C Albrecht, VP Logistics"),
        ],
    }),
]


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

RFP_TEMPLATE = """# RFP package skeleton

The skill `rfp-builder` will fill this skeleton. Do not edit this file directly
during practice; the skill produces a new draft each time.

## Section 1: Executive overview

(One page. The sourcing event in business terms. Audience: bidder commercial lead.)

## Section 2: Scope of work

(In-scope lanes by mode. Out-of-scope items. Volume estimate by lane.)

## Section 3: Commercial terms

(Contract structure: term, indexation, exit, payment, indemnities. Derived from CLAUDE.md and category brief.)

## Section 4: Evaluation criteria matrix

(Weighted criteria with definitions. Pulled from `procurement-standards.md` if present, else use these defaults: Price 40%, Service 25%, Capability 20%, Sustainability 10%, Implementation 5%.)

## Section 5: Supplier response template

(The structure the bidder must fill. Mirrors how `bid-scorer` reads bids.)

## Section 6: Process and timeline

(Q&A window, response deadline, evaluation period, decision date.)
"""

SCORECARD_TEMPLATE = """# Scorecard skeleton

The skill `bid-scorer` will fill this skeleton. The output is one row per
bidder, with weighted scores per criterion and a total.

| Bidder | Price (40%) | Service (25%) | Capability (20%) | Sustainability (10%) | Implementation (5%) | Total | Recommended? |
|---|---|---|---|---|---|---|---|
"""

AWARD_MEMO_TEMPLATE = """# Award memo skeleton

The skill `award-memo` will fill this skeleton.

## Recommendation (one paragraph, 50 to 80 words)

State the recommended awardee(s), the contract value, the term, and the key reason.

## Bid comparison summary

(Top 3 bidders by weighted score, with a one-line note for each.)

## Risks and mitigations

(Three named risks, each with a mitigation owner and date.)

## Savings case

(Annual savings against baseline, with the calculation visible inline.)

## Process and decisions

(One paragraph. Names the evaluators, the dates, and the source documents.)

## Audit footer

(Generated date, source files, model used, operator, output path.)
"""


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------

def write_csv(path: Path, header: list, rows: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    PRACTICE.mkdir(parents=True, exist_ok=True)

    # Practice CLAUDE.md
    (PRACTICE / "CLAUDE.md").write_text(STARTER_CLAUDE_MD, encoding="utf-8")

    # Inputs
    inputs = PRACTICE / "inputs"
    inputs.mkdir(exist_ok=True)
    (inputs / "category-brief.md").write_text(CATEGORY_BRIEF, encoding="utf-8")
    write_csv(
        inputs / "supplier-longlist.csv",
        ["carrier_id", "carrier_name", "modes", "primary_geography",
         "certifications", "capacity_tier", "financial_health",
         "otd_pct_12m", "contract_terms_offered", "incumbent"],
        LONGLIST,
    )
    spend_rows = gen_spend_baseline(1500)
    write_csv(
        inputs / "spend-baseline.csv",
        ["shipment_id", "carrier_id", "mode", "from_location",
         "to_location", "total_gbp", "ship_date"],
        spend_rows,
    )

    # Bid responses
    bid_dir = PRACTICE / "bid-responses"
    bid_dir.mkdir(exist_ok=True)
    bid_count = 0
    for idx, profile in SHORTLIST_BIDS:
        carrier = LONGLIST[idx]
        text = gen_bid(carrier, profile)
        # filename uses carrier id and short name
        safe_name = carrier[1].replace(" ", "_")
        filename = f"BID_{carrier[0]}_{safe_name}.md"
        (bid_dir / filename).write_text(text, encoding="utf-8")
        bid_count += 1

    # Templates
    templates = PRACTICE / "templates"
    templates.mkdir(exist_ok=True)
    (templates / "rfp-template.md").write_text(RFP_TEMPLATE, encoding="utf-8")
    (templates / "scorecard-template.md").write_text(SCORECARD_TEMPLATE, encoding="utf-8")
    (templates / "award-memo-template.md").write_text(AWARD_MEMO_TEMPLATE, encoding="utf-8")

    # Skills folder (empty; student fills in)
    skills = PRACTICE / "skills"
    skills.mkdir(exist_ok=True)
    (skills / "README.md").write_text(
        "# Your skill library\n\n"
        "You will fill this folder across Lessons 3, 4, and 5.\n"
        "Each skill is a markdown file describing a methodology Claude can reuse.\n\n"
        "Lessons 3 to 5 walk you through writing:\n"
        "- rfp-builder.md\n"
        "- bid-scorer.md\n"
        "- award-memo.md\n"
        "- risk-profiler.md\n"
        "- savings-calculator.md\n",
        encoding="utf-8",
    )

    # Outputs folder (empty; deliverables land here)
    outputs = PRACTICE / "outputs"
    outputs.mkdir(exist_ok=True)
    (outputs / "README.md").write_text(
        "# Outputs\n\n"
        "Files Claude produces using your skills land here. After Lesson 5\n"
        "you will have:\n"
        "- rfp-package.md (or several files)\n"
        "- bid-comparison.md\n"
        "- award-memo.md\n",
        encoding="utf-8",
    )

    print(f"Wrote practice/ folder under Course_03_The_Skill_Builder/")
    print(f"  practice/CLAUDE.md (project context)")
    print(f"  practice/inputs/")
    print(f"    category-brief.md")
    print(f"    supplier-longlist.csv ({len(LONGLIST)} carriers)")
    print(f"    spend-baseline.csv ({len(spend_rows)} historical shipments)")
    print(f"  practice/bid-responses/")
    print(f"    {bid_count} bid response files")
    print(f"  practice/templates/")
    print(f"    rfp-template.md, scorecard-template.md, award-memo-template.md")
    print(f"  practice/skills/ (empty; student fills across Lessons 3 to 5)")
    print(f"  practice/outputs/ (empty; deliverables land here)")


if __name__ == "__main__":
    main()
