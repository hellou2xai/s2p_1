"""Generate practice data for Course 17: Market Intelligence and Demand Management.

Scenario: Atlas Manufacturing, US-based industrial company, $58M annual procurement
spend. Today's date in the data: 2026-04-25.

Produces, written directly to practice/:
  commodity-prices.csv         192 rows. 6 commodities, 32 months (2023-08 through 2026-03).
  supplier-capabilities.csv    20 suppliers.
  demand-intake/               8 stakeholder requirement files in mixed formats
                               (structured form, email, memo, voicemail transcript).
  market-intelligence/         4 reports per Lesson 1: steel_price_outlook.md,
                               tariff_regulatory_update.md, midwest_disruption_alert.md,
                               supplier_capability_benchmark.md.

Deterministic via random.seed(42). All currency USD, US geography.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"

random.seed(42)

# Commodity list comes from Lesson 2: "Six commodities tracked
# (e.g., hot-rolled steel, cold-rolled steel, aluminum, copper,
# polypropylene, natural rubber)." 192 rows over 6 commodities = 32 months.
COMMODITIES = [
    ("HRS", "Hot-Rolled Steel", "USD/ton", 660.00),
    ("CRS", "Cold-Rolled Steel", "USD/ton", 820.00),
    ("ALU", "Aluminum", "USD/lb", 1.05),
    ("CU",  "Copper", "USD/lb", 4.80),
    ("PP",  "Polypropylene", "USD/lb", 0.78),
    ("RUB", "Natural Rubber", "USD/lb", 0.92),
]

MONTHS = 32  # 32 months x 6 commodities = 192 rows
END_YEAR, END_MONTH = 2026, 3  # last month covered (March 2026)


def month_iter():
    """Yield (year, month) tuples for the 32 months ending 2026-03."""
    pairs = []
    y, m = END_YEAR, END_MONTH
    for _ in range(MONTHS):
        pairs.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return list(reversed(pairs))


def build_commodity_prices():
    rows = []
    pairs = month_iter()
    for cid, name, unit, base in COMMODITIES:
        price = base
        # Walk forward in time. Bias each commodity slightly differently so
        # the YoY headlines in the lessons make sense.
        if cid == "HRS":
            drift = 0.012
        elif cid == "CRS":
            drift = 0.004
        elif cid == "ALU":
            drift = -0.003
        elif cid == "CU":
            drift = -0.005
        elif cid == "PP":
            drift = 0.009
        else:  # RUB
            drift = 0.006
        for (y, m) in pairs:
            shock = random.uniform(-0.04, 0.05)
            change = drift + shock
            new_price = round(price * (1 + change), 4)
            change_pct = round(((new_price - price) / price) * 100, 2)
            if change_pct > 1:
                trend = "up"
            elif change_pct < -1:
                trend = "down"
            else:
                trend = "flat"
            rows.append({
                "commodity_id": cid,
                "commodity_name": name,
                "unit": unit,
                "date": f"{y:04d}-{m:02d}",
                "price": f"{new_price:.4f}" if unit.endswith("/lb") else f"{new_price:.2f}",
                "change_pct": f"{change_pct:.2f}",
                "trend": trend,
            })
            price = new_price
    return rows


# Lesson 4 calls out "industrial gaskets" appearing across three specs and
# "hydraulic fittings" appearing twice, so the 8 requirements include those
# overlaps. Mixed formats per Lesson 3: structured_form, email, memo, transcript.
DEMAND_FILES = [
    {
        "filename": "engineering_request_042.md",
        "format": "structured_form",
        "content": (
            "# Procurement Request Form\n\n"
            "**Form ID:** ENG-REQ-042\n"
            "**Submitted:** 2026-04-21\n"
            "**Department:** Engineering\n"
            "**Requester:** Mike Johnson, Senior Mechanical Engineer\n"
            "**Cost center:** ENG-310\n"
            "**Project code:** PRJ-2026-014\n\n"
            "## Item details\n\n"
            "- Item description: Industrial gasket, EPDM, 4 inch outer diameter, 2.5 inch inner diameter, 0.125 inch thick\n"
            "- Quantity: 600\n"
            "- Unit of measure: each\n"
            "- Required delivery date: 2026-06-10\n"
            "- Technical specifications: ASTM D2000 compliant, durometer 70A, temperature range -40F to 250F, "
            "compatible with hot water and steam service\n"
            "- Budget reference: PRJ-2026-014, $4,800 allocated\n"
            "- Priority: medium\n"
        ),
    },
    {
        "filename": "plant_manager_email.md",
        "format": "email",
        "content": (
            "From: David Reyes <dreyes@atlasmfg.com>\n"
            "To: Procurement Team <procurement@atlasmfg.com>\n"
            "Date: 2026-04-22 16:42\n"
            "Subject: Need more of those blue gaskets\n\n"
            "Hi team,\n\n"
            "We need more of those blue gaskets, the ones from last year, but bigger. "
            "About 800 of them. Probably 5 inch outer diameter this time, similar material to before. "
            "Plant 2 shutdown risk if we do not have them by mid June. Cost center is MFG-220.\n\n"
            "Same supplier as last time would be ideal but we are open. "
            "Let me know what you need from me.\n\n"
            "Thanks,\n"
            "David Reyes\n"
            "Plant Manager, Plant 2\n"
        ),
    },
    {
        "filename": "voicemail_transcript_apr15.md",
        "format": "transcript",
        "content": (
            "# Voicemail transcript\n\n"
            "**Caller:** unidentified, sounds like Karen from Maintenance\n"
            "**Received:** 2026-04-15 11:08\n"
            "**Transcribed by:** auto-transcription service\n\n"
            "---\n\n"
            "Hi this is Karen from maintenance, uh, we need a couple hundred of the "
            "hydraulic fittings, the half inch ones I think, the ones we used on the "
            "press lines last year. Pretty soon, uh, before the end of the month would be great. "
            "I do not have the part number in front of me but you guys should have it on file. "
            "Call me back at extension 4471. Thanks.\n"
        ),
    },
    {
        "filename": "facilities_memo.md",
        "format": "memo",
        "content": (
            "# Memo\n\n"
            "**To:** Procurement\n"
            "**From:** James Wright, Facilities Manager\n"
            "**Date:** 2026-04-18\n"
            "**Subject:** HVAC gasket replacement, Building C\n\n"
            "Building C rooftop unit servicing in Q2 requires replacement gaskets for the four "
            "main air handlers. We need 12 industrial gaskets, 6 inch outer diameter, 4 inch inner "
            "diameter, neoprene, 0.25 inch thick. ASHRAE 62.1 compliance required.\n\n"
            "Required on site by 2026-05-30 to align with the maintenance window. Cost center FAC-110, "
            "approximately $480 budget. Standard freight is fine.\n\n"
            "If a vendor-managed inventory program exists for this part, please consider it.\n"
        ),
    },
    {
        "filename": "logistics_request.md",
        "format": "structured_form",
        "content": (
            "# Procurement Request Form\n\n"
            "**Form ID:** LOG-REQ-118\n"
            "**Submitted:** 2026-04-19\n"
            "**Department:** Logistics\n"
            "**Requester:** Lisa Torres, Logistics Operations Lead\n"
            "**Cost center:** LOG-410\n\n"
            "## Item details\n\n"
            "- Item description: Hydraulic fitting, 1/2 inch NPT, brass body, 3000 psi rating\n"
            "- Quantity: 240\n"
            "- Unit of measure: each\n"
            "- Required delivery date: 2026-05-20\n"
            "- Technical specifications: SAE J514 compliant, working pressure 3,000 psi minimum, "
            "compatible with hydraulic fluid ISO 32\n"
            "- Budget reference: LOG-410, $1,920 allocated\n"
            "- Priority: high (forklift fleet repair backlog)\n"
        ),
    },
    {
        "filename": "it_email_patel.md",
        "format": "email",
        "content": (
            "From: Priya Patel <ppatel@atlasmfg.com>\n"
            "To: procurement@atlasmfg.com\n"
            "Date: 2026-04-23 09:14\n"
            "Subject: Urgent. Cloud hosting renewal\n\n"
            "Hello,\n\n"
            "Our cloud hosting contract for the production ERP environment expires on 2026-06-30. "
            "We need a renewal or replacement proposal by 2026-06-01.\n\n"
            "Requirements:\n"
            "- 12 production workloads, total 480 vCPU and 1.8 TB RAM\n"
            "- 99.95 percent uptime SLA\n"
            "- US-region data residency only\n"
            "- SOC 2 Type II report on file\n\n"
            "Cost center IT-510. Annual budget approved: $640,000. Please initiate competitive "
            "bidding. Three vendors minimum.\n\n"
            "Priya\n"
        ),
    },
    {
        "filename": "manufacturing_chen_request.md",
        "format": "structured_form",
        "content": (
            "# Procurement Request Form\n\n"
            "**Form ID:** MFG-REQ-205\n"
            "**Submitted:** 2026-04-20\n"
            "**Department:** Manufacturing\n"
            "**Requester:** Sarah Chen, Production Engineer, Plant 1\n"
            "**Cost center:** MFG-150\n\n"
            "## Item details\n\n"
            "- Item description: Industrial gasket, FKM (Viton), 3 inch outer diameter, 1.75 inch inner diameter, 0.0625 inch thick\n"
            "- Quantity: 350\n"
            "- Unit of measure: each\n"
            "- Required delivery date: 2026-06-05\n"
            "- Technical specifications: chemical resistant for use with mineral oils and synthetic lubricants, "
            "operating temperature up to 400F, ASTM D2000 grade specified\n"
            "- Budget reference: MFG-150, $2,100 allocated\n"
            "- Priority: medium\n"
        ),
    },
    {
        "filename": "facilities_voicemail_wright.md",
        "format": "transcript",
        "content": (
            "# Voicemail transcript\n\n"
            "**Caller:** James Wright, Facilities\n"
            "**Received:** 2026-04-22 08:55\n"
            "**Transcribed by:** auto-transcription service\n\n"
            "---\n\n"
            "Hey it is James from facilities, follow up on the gasket order from my memo last week. "
            "I also need maybe 50 or so of the smaller hydraulic fittings, like the quarter inch ones, "
            "for the press shop. They asked me to add it on. Same urgency as the gaskets. "
            "I think I sent the cost center already, FAC-110. Call back if you need more details.\n"
        ),
    },
]


# Per Lesson 1 worked example: four reports.
# steel_price_outlook.md, tariff_regulatory_update.md, midwest_disruption_alert.md,
# supplier_capability_benchmark.md.
MARKET_REPORTS = [
    {
        "filename": "steel_price_outlook.md",
        "content": (
            "# Steel Price Outlook, Q2 2026\n\n"
            "**Publisher:** SteelMarketWatch (commodity research service)\n"
            "**Published:** 2026-04-12\n"
            "**Coverage:** US flat-rolled steel\n\n"
            "## Headline\n\n"
            "Hot-rolled coil prices are forecast to rise 8 to 12 percent through Q3 2026, "
            "driven by infrastructure spending and constrained Midwest mill capacity. "
            "Cold-rolled is expected to follow at a 4 to 6 percent increase.\n\n"
            "## Price drivers\n\n"
            "- Federal infrastructure outlays releasing $14.2B in awarded projects between April and August 2026.\n"
            "- US Steel and Nucor have planned maintenance shutdowns in June, removing roughly 320,000 tons of monthly capacity.\n"
            "- Chinese export quotas reduced by 8 percent for H2 2026, tightening global supply.\n\n"
            "## Forecast\n\n"
            "- Q2 2026 hot-rolled: $720 to $760 per ton (currently $702).\n"
            "- Q3 2026 hot-rolled: $740 to $790 per ton.\n"
            "- Q4 2026 hot-rolled: flat to slightly down if housing starts soften.\n\n"
            "## Recommended action\n\n"
            "Forward-buy 60 to 90 days of hot-rolled coverage at current contract pricing before "
            "the Q2 mill maintenance window. Reassess in late June.\n"
        ),
    },
    {
        "filename": "tariff_regulatory_update.md",
        "content": (
            "# Regulatory Update: Section 301 Tariff Adjustments\n\n"
            "**Publisher:** US Trade Policy Bulletin\n"
            "**Published:** 2026-04-08\n"
            "**Effective:** 2026-07-01\n\n"
            "## Summary\n\n"
            "A 15 percent additional tariff applies to imported industrial gasket materials and "
            "select polymer compounds (HTS 4016.93 and 3920.99) starting 2026-07-01. The tariff "
            "covers EPDM, FKM, and select fluoropolymer formulations sourced from Asia.\n\n"
            "## Scope\n\n"
            "- Affected categories: industrial gaskets, sealing rings, polymer sheet stock for fabricated parts.\n"
            "- Country coverage: China, Vietnam, Malaysia.\n"
            "- Estimated landed cost increase for affected SKUs: 11 to 17 percent.\n\n"
            "## Recommended action\n\n"
            "Review supplier base for affected SKUs. Identify domestic or Mexico-based alternatives "
            "for any line where the imported share exceeds 40 percent of annual volume. "
            "Pre-buy a 90-day inventory buffer before the 2026-07-01 effective date if a domestic "
            "switch cannot be completed in time.\n"
        ),
    },
    {
        "filename": "midwest_disruption_alert.md",
        "content": (
            "# Supply Chain Disruption Alert: Midwest Logistics, Spring 2026\n\n"
            "**Publisher:** SCM Risk Daily\n"
            "**Published:** 2026-04-19\n"
            "**Time horizon:** next 60 to 90 days\n\n"
            "## Summary\n\n"
            "Severe spring flooding across the Mississippi River basin (Iowa, Missouri, southern "
            "Illinois) has closed three rail interchange points and caused a 25 to 35 percent "
            "extension in Midwest truckload transit times. Conditions are expected to persist "
            "through mid-June.\n\n"
            "## Impacted lanes\n\n"
            "- Chicago to St. Louis: average transit up from 18 to 28 hours.\n"
            "- Kansas City to Memphis: average transit up from 24 to 36 hours.\n"
            "- Indianapolis to Cleveland: rail-truck handoff delayed by 36 to 48 hours.\n\n"
            "## Affected suppliers\n\n"
            "- Heartland Polymer (Davenport, Iowa): shipping delays of 4 to 6 days reported.\n"
            "- Midstate Steel Service (Peoria, Illinois): customer shipments delayed an average of 3 days.\n"
            "- Cardinal Industrial Supply (Cape Girardeau, Missouri): plant operations curtailed.\n\n"
            "## Recommended action\n\n"
            "Notify any sourcing event using a Midwest supplier of the increased delivery risk. "
            "For events closing within the 60-day window, raise the delivery weight in the "
            "evaluation criteria and require documented contingency routing from each bidder.\n"
        ),
    },
    {
        "filename": "supplier_capability_benchmark.md",
        "content": (
            "# Supplier Capability Benchmark, Spring 2026 Trade Show\n\n"
            "**Publisher:** Atlas Manufacturing Sourcing team (internal)\n"
            "**Source event:** Industrial Sealing and Hose Expo, Cleveland, 2026-04-09 to 2026-04-11\n"
            "**Published:** 2026-04-16\n\n"
            "## Summary\n\n"
            "Three suppliers demonstrated new capabilities relevant to Atlas Manufacturing's "
            "industrial gasket and hydraulic fitting categories.\n\n"
            "## Supplier observations\n\n"
            "1. **Crescent Sealing Co. (Akron, Ohio).** Launched a domestic FKM compounding line "
            "with 1,200 tons annual capacity. Lead time 14 to 21 days. ISO 9001 and AS9100 certified. "
            "Currently not on Atlas approved supplier list.\n\n"
            "2. **Northland Hydraulics (Minneapolis, Minnesota).** Announced vendor-managed "
            "inventory program for hydraulic fittings, minimum order $25,000 per quarter. "
            "Eight Atlas plants are within their service radius.\n\n"
            "3. **PolyForm Industries (Houston, Texas).** Expanded EPDM gasket production by 40 "
            "percent. Now offers six-week lead time on custom dimensions versus 10 to 12 weeks "
            "industry standard.\n\n"
            "## Recommended action\n\n"
            "Add Crescent Sealing Co. and PolyForm Industries to the approved supplier list "
            "before the Q3 RFP cycle. Pilot the Northland Hydraulics VMI program at one plant for "
            "90 days before broader rollout.\n"
        ),
    },
]


# 20 named suppliers, US locations, with item-type capability text the
# Lesson 4 prompts can match on (industrial gasket, hydraulic fitting, etc.).
SUPPLIERS = [
    ("SUP-001", "Crescent Sealing Co.",      "Akron, OH",          "industrial gaskets; FKM and EPDM compounds", "no",  "ISO 9001, AS9100",  21, 35, 88.0),
    ("SUP-002", "PolyForm Industries",       "Houston, TX",        "industrial gaskets; EPDM custom dimensions", "no",  "ISO 9001",          28, 40, 84.5),
    ("SUP-003", "Northland Hydraulics",      "Minneapolis, MN",    "hydraulic fittings; VMI program",            "no",  "ISO 9001",          14, 30, 86.2),
    ("SUP-004", "Cardinal Industrial Supply","Cape Girardeau, MO", "industrial gaskets; hydraulic fittings",     "yes", "ISO 9001",          18, 22, 79.5),
    ("SUP-005", "Heartland Polymer",         "Davenport, IA",      "polypropylene resin; polymer compounds",     "no",  "ISO 9001, ISO 14001", 21, 28, 82.0),
    ("SUP-006", "Midstate Steel Service",    "Peoria, IL",         "hot-rolled steel; cold-rolled steel",        "no",  "ISO 9001",          14, 25, 81.0),
    ("SUP-007", "Lakefront Aluminum",        "Toledo, OH",         "aluminum sheet; aluminum extrusion",         "no",  "ISO 9001, ISO 14001", 21, 33, 85.0),
    ("SUP-008", "Copperline Wire Works",     "Carrollton, GA",     "copper wire; copper cathode",                "yes", "ISO 9001",          25, 18, 76.5),
    ("SUP-009", "Gulf Coast Polymers",       "Lake Charles, LA",   "polypropylene; polyethylene resin",          "no",  "ISO 9001",          24, 45, 87.0),
    ("SUP-010", "Allegheny Rubber",          "Pittsburgh, PA",     "natural rubber; rubber compounds",           "no",  "ISO 9001",          20, 32, 80.5),
    ("SUP-011", "Great Plains Trucking",     "Omaha, NE",          "logistics; dedicated fleet",                 "no",  "None",              7,  20, 74.0),
    ("SUP-012", "Eastern Freight Lines",     "Baltimore, MD",      "logistics; intermodal",                      "no",  "None",              5,  15, 71.5),
    ("SUP-013", "Apex Cloud Services",       "Reston, VA",         "cloud hosting; managed services",            "no",  "SOC 2 Type II",     10, 38, 90.0),
    ("SUP-014", "Summit Cybersecurity",      "Austin, TX",         "IT services; cybersecurity consulting",      "no",  "SOC 2 Type II",     14, 28, 88.5),
    ("SUP-015", "Pacific Facilities Group",  "Sacramento, CA",     "facilities maintenance; HVAC",               "no",  "None",              30, 25, 72.0),
    ("SUP-016", "Northeast Building Services","Newark, NJ",        "facilities maintenance; cleaning",           "no",  "None",              21, 30, 70.5),
    ("SUP-017", "Capital Fastener Supply",   "Columbus, OH",       "fasteners; vendor-managed inventory",        "yes", "ISO 9001",          14, 35, 83.0),
    ("SUP-018", "Riverbend Electronics",     "Phoenix, AZ",        "electronic components; microcontrollers",    "no",  "ISO 9001, AS9100",  35, 24, 86.5),
    ("SUP-019", "Southern Energy Partners",  "Birmingham, AL",     "natural gas; industrial fuel",               "no",  "None",              5,  40, 75.0),
    ("SUP-020", "Liberty Diesel Distribution","Charlotte, NC",     "diesel fuel; bulk fuel delivery",            "no",  "None",              3,  42, 73.0),
]


def build_supplier_capabilities():
    rows = []
    for sid, name, location, cap_desc, make_cap, certs, lead, capacity_pct, score in SUPPLIERS:
        rows.append({
            "supplier_id": sid,
            "supplier_name": name,
            "location": location,
            "capability_description": cap_desc,
            "lead_time_days": lead,
            "capacity_available_pct": capacity_pct,
            "capability_score": score,
            "certifications": certs,
            "make_capability": make_cap,
            "currently_supplying_atlas": "yes" if sid in {"SUP-004", "SUP-005", "SUP-006", "SUP-007", "SUP-009", "SUP-010", "SUP-013", "SUP-017", "SUP-019", "SUP-020"} else "no",
        })
    return rows


def write_csv(path, rows, fieldnames=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.relative_to(ROOT)}: {len(rows)} rows")


def main():
    print("Building Course 17 practice data.")
    print()

    PRACTICE.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "demand-intake").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "market-intelligence").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "Drafts").mkdir(parents=True, exist_ok=True)

    write_csv(PRACTICE / "commodity-prices.csv", build_commodity_prices())
    write_csv(PRACTICE / "supplier-capabilities.csv", build_supplier_capabilities())

    for f in DEMAND_FILES:
        path = PRACTICE / "demand-intake" / f["filename"]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f["content"])
    print(f"  practice/demand-intake/: {len(DEMAND_FILES)} requirement files")

    for r in MARKET_REPORTS:
        path = PRACTICE / "market-intelligence" / r["filename"]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(r["content"])
    print(f"  practice/market-intelligence/: {len(MARKET_REPORTS)} report files")

    # A .gitkeep so Drafts/ shows up in version control even when empty.
    keep = PRACTICE / "Drafts" / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")
    print("  practice/Drafts/: created (empty workspace for student output)")

    print()
    print("Done. All files in practice/.")


if __name__ == "__main__":
    main()
