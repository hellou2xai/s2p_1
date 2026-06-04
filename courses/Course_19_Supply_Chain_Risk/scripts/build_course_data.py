"""Generate practice data for Course 19: Supply Chain Risk and Resilience.

Scenario: Board risk review at Fortis Manufacturing. 25-supplier portfolio.
Students build a risk register, scenario models, and a board brief.

Produces (in practice/data/):
  supplier-master.csv     (25 suppliers)
  spend-by-item.csv       (200 line items)
  single-source-items.csv (5 high-exposure items)
  approved-alternates.csv (4 alternates)
  disruption-events.md    (4 historical events)

All values are hardcoded for full determinism. No randomness. Re-running
this script always produces byte-identical files. Today's date: 2026-04-25.
All currency USD. All geography US.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"
DATA = PRACTICE / "data"

# ---------------------------------------------------------------------------
# Suppliers. Order matters: lessons reference SUP003 = Pacific Aluminum,
# SUP004 = Apex Electronics, SUP006 = Continental Freight, etc.
# Tuple shape: (id, name, category, tier, city, state, annual_spend_usd,
#               financial_health_score, geographic_concentration,
#               single_source_items)
# ---------------------------------------------------------------------------
SUPPLIERS = [
    ("SUP001", "Great Lakes Steel",      "raw-materials",          "strategic", "Chicago",       "IL", 4_200_000, 75.2, "medium", 2),
    ("SUP002", "Heartland Polymers",     "raw-materials",          "strategic", "Houston",       "TX", 3_800_000, 80.8, "high",   1),
    ("SUP003", "Pacific Aluminum",       "raw-materials",          "preferred", "Portland",      "OR", 3_100_000, 52.3, "low",    5),
    ("SUP004", "Apex Electronics",       "components",             "preferred", "San Jose",      "CA", 2_400_000, 44.8, "high",   4),
    ("SUP005", "Cascade Fasteners",      "raw-materials",          "approved",  "Seattle",       "WA", 1_800_000, 68.4, "low",    1),
    ("SUP006", "Continental Freight",    "logistics",              "strategic", "Memphis",       "TN", 3_600_000, 41.7, "low",    0),
    ("SUP007", "Patriot Logistics",      "logistics",              "strategic", "Atlanta",       "GA", 2_900_000, 72.0, "low",    1),
    ("SUP008", "Eagle Transport",        "logistics",              "preferred", "Indianapolis",  "IN", 2_100_000, 58.1, "low",    2),
    ("SUP009", "TechForward Solutions",  "it-services",            "strategic", "Austin",        "TX", 2_800_000, 70.9, "high",   2),
    ("SUP010", "CloudBridge Systems",    "it-services",            "strategic", "San Francisco", "CA", 2_500_000, 78.6, "high",   3),
    ("SUP011", "Nexus IT Services",      "it-services",            "preferred", "Raleigh",       "NC", 1_900_000, 62.1, "low",    1),
    ("SUP012", "National Facilities",    "facilities",             "strategic", "Philadelphia",  "PA", 2_200_000, 65.3, "medium", 0),
    ("SUP013", "Metro Building Svcs",    "facilities",             "preferred", "Newark",        "NJ", 1_800_000, 81.7, "low",    1),
    ("SUP014", "Whitfield Consulting",   "professional-services",  "strategic", "New York",      "NY", 2_600_000, 78.4, "low",    0),
    ("SUP015", "Sterling Advisory",      "professional-services",  "strategic", "Chicago",       "IL", 2_100_000, 65.3, "medium", 0),
    ("SUP016", "Summit Metals",          "raw-materials",          "approved",  "Denver",        "CO", 1_600_000, 92.6, "low",    0),
    ("SUP017", "Liberty Composites",     "raw-materials",          "approved",  "Detroit",       "MI", 1_200_000, 66.6, "low",    1),
    ("SUP018", "Frontier Plastics",      "raw-materials",          "approved",  "Dallas",        "TX",   980_000, 56.9, "high",   1),
    ("SUP019", "Horizon Carriers",       "logistics",              "approved",  "Louisville",    "KY", 1_700_000, 60.9, "low",    2),
    ("SUP020", "Pinnacle Software",      "it-services",            "approved",  "Boston",        "MA", 1_500_000, 79.5, "low",    0),
    ("SUP021", "Greenfield Maint.",      "facilities",             "approved",  "Hartford",      "CT", 1_400_000, 64.3, "low",    1),
    ("SUP022", "Meridian Legal",         "professional-services",  "preferred", "Washington",    "DC", 1_600_000, 85.6, "low",    0),
    ("SUP023", "Crestline Accounting",   "professional-services",  "approved",  "Minneapolis",   "MN", 1_200_000, 88.7, "low",    0),
    ("SUP024", "Vanguard Staffing",      "professional-services",  "approved",  "Denver",        "CO",   950_000, 71.8, "low",    1),
    ("SUP025", "SafeGuard Fire",         "facilities",             "approved",  "Albany",        "NY",   700_000, 73.8, "low",    1),
]

# Lookup helpers.
SUPPLIER_BY_ID = {row[0]: row for row in SUPPLIERS}

# ---------------------------------------------------------------------------
# Single-source items. The 5 items the lessons reference verbatim.
# ITEM-0001, ITEM-0013, ITEM-0025, ITEM-0037, ITEM-0049 are the canonical
# single-source items. Their descriptions, supplier ids, supplier names,
# spend, and criticality are quoted directly in lesson 3.
# ---------------------------------------------------------------------------
SINGLE_SOURCE_ITEMS = [
    {"item_id": "ITEM-0001", "item_description": "Steel plate 4mm",     "supplier_id": "SUP001", "supplier_name": "Great Lakes Steel",   "annual_spend_usd": 840_000, "criticality": "high",     "alternate_available": "yes", "qualification_time_weeks": 6},
    {"item_id": "ITEM-0013", "item_description": "Aluminum sheet 2mm",  "supplier_id": "SUP003", "supplier_name": "Pacific Aluminum",    "annual_spend_usd": 620_000, "criticality": "high",     "alternate_available": "yes", "qualification_time_weeks": 4},
    {"item_id": "ITEM-0025", "item_description": "Microcontroller ARM", "supplier_id": "SUP004", "supplier_name": "Apex Electronics",    "annual_spend_usd": 480_000, "criticality": "critical", "alternate_available": "no",  "qualification_time_weeks": 10},
    {"item_id": "ITEM-0037", "item_description": "Cloud hosting",       "supplier_id": "SUP010", "supplier_name": "CloudBridge Systems", "annual_spend_usd": 500_000, "criticality": "high",     "alternate_available": "yes", "qualification_time_weeks": 11},
    {"item_id": "ITEM-0049", "item_description": "Fire inspection",     "supplier_id": "SUP025", "supplier_name": "SafeGuard Fire",      "annual_spend_usd": 140_000, "criticality": "medium",   "alternate_available": "yes", "qualification_time_weeks": 15},
]

SINGLE_SOURCE_BY_ITEM = {row["item_id"]: row for row in SINGLE_SOURCE_ITEMS}

# ---------------------------------------------------------------------------
# Approved alternates. Lesson 3 expects exactly 4 rows. ITEM-0001 has two
# alternates (Summit Metals qualified and Liberty Composites in qualification),
# ITEM-0013 has Summit Metals qualified, ITEM-0037 has Pinnacle Software
# qualified. ITEM-0025 and ITEM-0049 have no alternate row (the "critical
# gap" cases referenced in the lessons).
# ---------------------------------------------------------------------------
APPROVED_ALTERNATES = [
    {"item_id": "ITEM-0001", "item_description": "Steel plate 4mm",    "alternate_supplier_id": "SUP016", "alternate_supplier_name": "Summit Metals",       "qualification_status": "qualified",       "lead_time_weeks": 12},
    {"item_id": "ITEM-0001", "item_description": "Steel plate 4mm",    "alternate_supplier_id": "SUP017", "alternate_supplier_name": "Liberty Composites",  "qualification_status": "in_qualification", "lead_time_weeks": 8},
    {"item_id": "ITEM-0013", "item_description": "Aluminum sheet 2mm", "alternate_supplier_id": "SUP016", "alternate_supplier_name": "Summit Metals",       "qualification_status": "qualified",       "lead_time_weeks": 10},
    {"item_id": "ITEM-0037", "item_description": "Cloud hosting",      "alternate_supplier_id": "SUP020", "alternate_supplier_name": "Pinnacle Software",   "qualification_status": "qualified",       "lead_time_weeks": 4},
]

# ---------------------------------------------------------------------------
# Spend-by-item builder. 200 rows, deterministic, hardcoded item descriptions
# in a 20-item rotation. The 5 single-source ITEM IDs are overwritten with
# the exact supplier and description from SINGLE_SOURCE_ITEMS so the two
# files stay consistent.
# ---------------------------------------------------------------------------
ITEM_DESCRIPTIONS = [
    "Steel plate 4mm", "Steel bar 12mm", "Polymer resin A", "Polymer resin B",
    "Aluminum sheet 2mm", "Aluminum extrusion", "Microcontroller ARM", "Capacitor 100uF",
    "Fastener M6", "Fastener M10", "Freight Chicago-NY", "Freight Houston-LA",
    "Cloud hosting", "Software license", "Janitorial service", "HVAC maintenance",
    "Consulting hours", "Legal review", "Staffing temp", "Fire inspection",
]

# Two deterministic cycles for unit cost and annual volume. Picked once,
# never random. Length 20 so they line up with ITEM_DESCRIPTIONS.
UNIT_COST_CYCLE = [
    387.50, 412.75, 156.20, 188.40, 245.00, 198.30, 32.10, 4.85,
    2.15, 3.40, 1450.00, 1620.00, 0.85, 14500.00, 95.00, 165.00,
    275.00, 380.00, 62.00, 825.00,
]
VOLUME_CYCLE = [
    2200, 1800, 4500, 3600, 1500, 2800, 14000, 88000,
    420000, 280000, 290, 240, 580000, 30, 4800, 2400,
    900, 320, 7200, 170,
]
SPEND_FRACTION_CYCLE = [
    0.20, 0.15, 0.10, 0.08, 0.06, 0.05, 0.05, 0.04,
    0.04, 0.03, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02,
    0.02, 0.01, 0.01, 0.01,
]
CRITICALITY_CYCLE = [
    "high", "high", "medium", "medium", "low",
    "high", "medium", "low", "medium", "medium",
    "high", "medium", "high", "low", "medium",
    "low", "high", "medium", "low", "medium",
]


def build_supplier_master_rows():
    rows = []
    for sid, name, cat, tier, city, state, spend, financial, geo, ssc in SUPPLIERS:
        rows.append({
            "supplier_id": sid,
            "supplier_name": name,
            "category": cat,
            "tier": tier,
            "city": city,
            "state": state,
            "annual_spend_usd": spend,
            "financial_health_score": financial,
            "geographic_concentration": geo,
            "single_source_items": ssc,
        })
    return rows


def build_spend_by_item_rows():
    """200 rows. Rotates suppliers and item descriptions deterministically.

    Single-source ITEM IDs (ITEM-0001, 0013, 0025, 0037, 0049) are forced to
    match SINGLE_SOURCE_ITEMS exactly so the two files stay consistent.
    """
    rows = []
    for i in range(200):
        item_id = f"ITEM-{i + 1:04d}"
        sup = SUPPLIERS[i % len(SUPPLIERS)]
        sid, name, cat = sup[0], sup[1], sup[2]
        desc_idx = i % len(ITEM_DESCRIPTIONS)
        description = ITEM_DESCRIPTIONS[desc_idx]
        # Spend per item is a fixed fraction of the supplier's annual spend
        # divided by how often that supplier appears across 200 rows (8x).
        supplier_spend = sup[6]
        fraction = SPEND_FRACTION_CYCLE[i % len(SPEND_FRACTION_CYCLE)]
        annual_spend = round(supplier_spend * fraction, 2)
        unit_cost = UNIT_COST_CYCLE[desc_idx]
        annual_volume = VOLUME_CYCLE[desc_idx]
        criticality = CRITICALITY_CYCLE[desc_idx]
        single_source = "no"

        # Override the 5 canonical single-source items so they line up with
        # single-source-items.csv exactly.
        if item_id in SINGLE_SOURCE_BY_ITEM:
            ss = SINGLE_SOURCE_BY_ITEM[item_id]
            sid = ss["supplier_id"]
            name = ss["supplier_name"]
            cat = SUPPLIER_BY_ID[sid][2]
            description = ss["item_description"]
            annual_spend = ss["annual_spend_usd"]
            criticality = ss["criticality"]
            single_source = "yes"

        rows.append({
            "item_id": item_id,
            "item_description": description,
            "supplier_id": sid,
            "supplier_name": name,
            "category": cat,
            "annual_spend_usd": annual_spend,
            "unit_cost": unit_cost,
            "annual_volume": annual_volume,
            "single_source": single_source,
            "criticality": criticality,
        })
    return rows


DISRUPTION_EVENTS_MD = """# Disruption Event History

## Event 1: Hurricane Impact (September 2025)
- **Affected supplier:** Heartland Polymers (SUP002), Houston, TX
- **Duration:** 12 days
- **Impact:** Production halted. $420,000 in delayed shipments. 3 customer orders missed.
- **Recovery:** Spot-market premium of 15% above contracted rates. Expedited freight added $42,000.

## Event 2: Supplier Financial Distress (November 2025)
- **Affected supplier:** Apex Electronics (SUP004), San Jose, CA
- **Duration:** Ongoing
- **Impact:** Lead times extended from 14 to 28 days. Quality reject rate increased to 4.2%.
- **Recovery:** Qualification of alternate supplier in progress. ETA: June 2026.

## Event 3: Logistics Capacity Crunch (January 2026)
- **Affected supplier:** Eagle Transport (SUP008), Indianapolis, IN
- **Duration:** 21 days
- **Impact:** Spot rates 35% above contract. $180,000 incremental cost. Expedited freight surcharge $58,000.
- **Recovery:** Temporary capacity from Patriot Logistics (SUP007).

## Event 4: Cybersecurity Incident (March 2026)
- **Affected supplier:** CloudBridge Systems (SUP010), San Francisco, CA
- **Duration:** 5 days
- **Impact:** Systems offline. No data breach confirmed. $95,000 in business interruption (about $19,000 per day).
- **Recovery:** Failover to backup systems. Post-incident review scheduled.
"""


def write_csv(path: Path, rows, fieldnames=None):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.name}: {len(rows)} rows")


def main():
    print("Building Course 19 practice data...")
    print()

    DATA.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "Drafts").mkdir(parents=True, exist_ok=True)

    write_csv(DATA / "supplier-master.csv", build_supplier_master_rows())
    write_csv(DATA / "spend-by-item.csv", build_spend_by_item_rows())
    write_csv(DATA / "single-source-items.csv", SINGLE_SOURCE_ITEMS)
    write_csv(DATA / "approved-alternates.csv", APPROVED_ALTERNATES)

    events_path = DATA / "disruption-events.md"
    events_path.write_text(DISRUPTION_EVENTS_MD, encoding="utf-8")
    print(f"  disruption-events.md: 4 historical events")

    print()
    print("Done. All files in practice/data/.")


if __name__ == "__main__":
    main()
