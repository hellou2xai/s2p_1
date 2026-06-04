"""
Course 10: The Negotiation Intelligence System
Generates practice data for TransGlobal Industries logistics contract negotiation.
Run: python scripts/build_course_data.py
"""

import csv
import json
import os
import random
from pathlib import Path

random.seed(42)

SCRIPT_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = SCRIPT_DIR.parent / "practice"
DATA_DIR = PRACTICE_DIR / "data"
OUTPUTS_DIR = PRACTICE_DIR / "outputs"


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def build_current_contract():
    content = """# Master Services Agreement: Redline Logistics LLC

## Contract ID
CTR-2024-LG-001

## Parties
- **Client**: TransGlobal Industries, Inc., Houston, TX
- **Supplier**: Redline Logistics LLC, Indianapolis, IN

## Term
- **Effective date**: 2024-06-01
- **Expiration date**: 2027-05-31
- **Duration**: 36 months

## Annual value
$9,200,000

## Scope of services

### Warehousing
- Chicago distribution center: 120,000 sq ft, $18.50/sq ft/year
- Dallas distribution center: 95,000 sq ft, $16.75/sq ft/year
- Atlanta distribution center: 85,000 sq ft, $17.25/sq ft/year
- Phoenix distribution center: 70,000 sq ft, $15.00/sq ft/year

### Last-mile delivery
- Eastern US region: 14 states
- Average monthly shipments: 8,400
- Per-shipment rate: $42.00

### Cross-dock operations
- Chicago hub: 2,200 pallets/month at $8.50/pallet
- Atlanta hub: 1,800 pallets/month at $9.00/pallet

## Service level agreements

| KPI | Target | Measurement |
|---|---|---|
| On-time delivery | 96.0% | Monthly, trailing 3 months |
| Damage rate | Below 0.5% | Monthly |
| Invoice accuracy | 99.0% | Monthly |
| Issue response time | Under 4 hours | Per incident |

## Key clauses

### Auto-renewal
Contract auto-renews for successive 12-month periods unless either party provides written notice of non-renewal at least **180 days** before the expiration date.

### Force majeure
Excused events include natural disasters, government actions, pandemics, labor strikes, **supply chain disruptions**, and acts of terrorism. Affected party must notify the other within 5 business days.

### Termination for cause
Either party may terminate with 60 days written notice if the other party materially breaches and fails to cure within 30 days of written notice.

### Termination for convenience
Client may terminate for convenience with 120 days written notice and payment of a termination fee equal to 3 months of the average monthly fee.

### Liability cap
Total liability capped at 12 months of fees paid or payable under the agreement.

### Insurance requirements
- Commercial general liability: $5,000,000
- Auto liability: $2,000,000
- Workers compensation: statutory limits
- Cargo insurance: $1,000,000 per shipment

### Payment terms
Net 45 days from invoice date. 2% early payment discount for payment within 10 days.

### Price adjustment
Annual price adjustment capped at CPI plus 2%, with 90 days advance notice required.
"""
    with open(DATA_DIR / "current-contract.md", "w", encoding="utf-8") as f:
        f.write(content)


def build_proposed_renewal():
    content = """# Proposed Contract Renewal: Redline Logistics LLC

## Submitted by
Redline Logistics LLC, Indianapolis, IN

## Submitted to
TransGlobal Industries, Inc., Houston, TX

## Date submitted
2026-04-22

## Reference contract
CTR-2024-LG-001

## Proposed changes

### 1. Pricing adjustment

Redline proposes a **12% increase** across all service lines, effective at renewal.

| Service | Current rate | Proposed rate | Change |
|---|---|---|---|
| Chicago warehouse | $18.50/sq ft/yr | $20.72/sq ft/yr | +12% |
| Dallas warehouse | $16.75/sq ft/yr | $18.76/sq ft/yr | +12% |
| Atlanta warehouse | $17.25/sq ft/yr | $19.32/sq ft/yr | +12% |
| Phoenix warehouse | $15.00/sq ft/yr | $16.80/sq ft/yr | +12% |
| Last-mile delivery | $42.00/shipment | $47.04/shipment | +12% |
| Chicago cross-dock | $8.50/pallet | $9.52/pallet | +12% |
| Atlanta cross-dock | $9.00/pallet | $10.08/pallet | +12% |

**Proposed annual value**: $10,304,000 (increase of $1,104,000).

**Justification**: Redline cites rising labor costs (8% increase in warehouse wages since 2024), fuel surcharges (diesel up 14% YoY), and insurance premium increases (22% renewal increase in 2025).

### 2. Force majeure clause modification

Redline proposes removing **"supply chain disruptions"** from the list of excused force majeure events.

**Current clause**: "...natural disasters, government actions, pandemics, labor strikes, supply chain disruptions, and acts of terrorism."

**Proposed clause**: "...natural disasters, government actions, pandemics, labor strikes, and acts of terrorism."

**Justification**: Redline states that supply chain disruptions are a normal business risk that logistics providers must manage, not an extraordinary event. They note that including supply chain disruptions creates ambiguity about when performance obligations are suspended.

### 3. Auto-renewal notice period

Redline proposes shortening the non-renewal notice period from **180 days to 90 days**.

**Current clause**: "...unless either party provides written notice of non-renewal at least 180 days before the expiration date."

**Proposed clause**: "...unless either party provides written notice of non-renewal at least 90 days before the expiration date."

**Justification**: Redline argues that 180 days is longer than industry standard (typically 90 to 120 days) and creates unnecessary planning uncertainty for both parties.

## Terms not changed

All other terms remain as stated in CTR-2024-LG-001, including:
- Service scope (no changes to locations, volumes, or service descriptions)
- SLA targets (same KPIs and thresholds)
- Payment terms (Net 45, 2% early pay discount)
- Insurance requirements (unchanged)
- Liability cap (unchanged)
- Termination provisions (unchanged, except as affected by the notice period change above)

## Response requested by
2026-05-07
"""
    with open(DATA_DIR / "proposed-renewal.md", "w", encoding="utf-8") as f:
        f.write(content)


def build_supplier_performance():
    """24 months of monthly KPIs for Redline Logistics."""
    rows = []
    months = []
    for year in [2024, 2025, 2026]:
        for month in range(1, 13):
            if year == 2024 and month < 5:
                continue
            if year == 2026 and month > 4:
                continue
            months.append(f"{year}-{month:02d}")

    # On-time delivery: starts at 96.8%, declines to 93.1% over last 6 months
    otd_base = 96.8
    for i, m in enumerate(months):
        if i >= 18:  # last 6 months
            decline = (i - 17) * 0.62
            otd = round(otd_base - decline + random.uniform(-0.3, 0.3), 1)
        else:
            otd = round(otd_base + random.uniform(-0.5, 0.5), 1)

        damage = round(random.uniform(0.15, 0.45), 2)
        inv_acc = round(random.uniform(98.2, 99.8), 1)
        resp_hrs = round(random.uniform(1.5, 4.5), 1)

        rows.append({
            "month": m,
            "on_time_delivery_pct": min(otd, 99.0),
            "damage_rate_pct": damage,
            "invoice_accuracy_pct": inv_acc,
            "response_time_hours": resp_hrs
        })

    with open(DATA_DIR / "supplier-performance.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def build_market_benchmarks():
    content = """# Logistics Market Benchmarks: Q1 2026

## Warehousing rates (US average, per sq ft per year)

| Market | 2024 avg | 2025 avg | Q1 2026 | YoY change |
|---|---|---|---|---|
| Midwest (Chicago) | $17.00 | $18.20 | $18.90 | +3.8% |
| South Central (Dallas) | $14.50 | $15.60 | $16.40 | +5.1% |
| Southeast (Atlanta) | $15.25 | $16.30 | $17.00 | +4.3% |
| Southwest (Phoenix) | $13.00 | $13.80 | $14.50 | +5.1% |

**Industry average increase**: 4.6% year over year.

## Last-mile delivery rates (per shipment, comparable volume)

| Provider | 2024 rate | 2025 rate | Q1 2026 rate | YoY change |
|---|---|---|---|---|
| Redline Logistics | $42.00 | $42.00 | $42.00 | 0% (contract rate) |
| SwiftLine Freight | $39.50 | $41.00 | $42.50 | +3.7% |
| Horizon Distribution | $41.00 | $42.50 | $43.80 | +3.1% |
| National Carriers Inc | $38.00 | $40.00 | $41.50 | +3.8% |
| Industry average | $39.50 | $41.25 | $42.60 | +3.3% |

## Cross-dock rates (per pallet)

| Market | 2024 avg | 2025 avg | Q1 2026 | YoY change |
|---|---|---|---|---|
| Chicago | $7.80 | $8.20 | $8.60 | +4.9% |
| Atlanta | $8.20 | $8.60 | $9.10 | +5.8% |

## Key market factors

### Labor costs
- Warehouse labor costs increased 8.2% nationally in 2025. Q1 2026 data shows a 3.1% annualized increase, suggesting the pace is slowing.
- Driver wages increased 6.4% in 2025. CDL driver shortage is easing in the Southeast but persists in the Midwest.

### Fuel
- Diesel prices averaged $3.65/gallon in Q1 2026, up 14% from Q1 2025 ($3.20).
- Most carriers apply a fuel surcharge index. Redline's contract includes fuel surcharges in the base rate, not as a separate line item.

### Insurance
- Logistics insurance premiums increased 18% to 22% in 2025 renewals. The increase is driven by cargo theft trends and natural disaster exposure.

### Capacity
- National warehouse vacancy rate: 4.2% (down from 5.1% in 2024). Tight market, but not as tight as 2022 (2.8%).
- Carrier capacity is adequate in most lanes. Southeast to Northeast lane is tight due to seasonal demand.

## Comparable contract benchmarks

Based on three comparable logistics contracts (similar scope, US manufacturer, $7M to $12M annual value):

| Metric | Low | Median | High |
|---|---|---|---|
| Annual price increase | 3.5% | 5.2% | 7.8% |
| Auto-renewal notice | 90 days | 120 days | 180 days |
| Force majeure scope | Narrow (5 events) | Standard (7 events) | Broad (9 events) |
| Payment terms | Net 30 | Net 45 | Net 60 |
| SLA on-time delivery target | 95.0% | 96.0% | 97.5% |

## Summary

A 12% price increase is significantly above market. Comparable contracts renewed at 3.5% to 7.8%. Market data supports an increase of 5% to 6%, reflecting real cost pressures in labor, fuel, and insurance, but not at the level Redline is requesting.
"""
    with open(DATA_DIR / "market-benchmarks.md", "w", encoding="utf-8") as f:
        f.write(content)


def build_negotiation_history():
    """8 past negotiation outcomes."""
    rows = [
        {"negotiation_id": "NEG-2022-01", "supplier": "Redline Logistics LLC", "category": "logistics", "initial_ask_pct": 9.0, "final_outcome_pct": 4.2, "concessions_given": "Extended term from 24 to 36 months", "concessions_received": "Added performance rebate at 97% OTD", "duration_days": 18, "date_closed": "2022-05-15"},
        {"negotiation_id": "NEG-2022-02", "supplier": "SwiftLine Freight", "category": "logistics", "initial_ask_pct": 7.5, "final_outcome_pct": 3.8, "concessions_given": "Increased minimum volume commitment 10%", "concessions_received": "Fuel surcharge cap at 5%", "duration_days": 12, "date_closed": "2022-09-20"},
        {"negotiation_id": "NEG-2023-01", "supplier": "Horizon Distribution", "category": "logistics", "initial_ask_pct": 11.0, "final_outcome_pct": 6.5, "concessions_given": "Accepted 120-day notice period (from 180)", "concessions_received": "Added SLA penalty for below 94% OTD", "duration_days": 22, "date_closed": "2023-02-10"},
        {"negotiation_id": "NEG-2023-02", "supplier": "National Carriers Inc", "category": "logistics", "initial_ask_pct": 6.0, "final_outcome_pct": 3.0, "concessions_given": "Moved payment terms from Net 30 to Net 45", "concessions_received": "Locked rate for 24 months no adjustment", "duration_days": 10, "date_closed": "2023-06-01"},
        {"negotiation_id": "NEG-2023-03", "supplier": "Redline Logistics LLC", "category": "logistics", "initial_ask_pct": 8.0, "final_outcome_pct": 3.5, "concessions_given": "Added Phoenix DC to scope", "concessions_received": "Volume discount tier at $9M+", "duration_days": 15, "date_closed": "2023-11-12"},
        {"negotiation_id": "NEG-2024-01", "supplier": "Apex Warehousing", "category": "warehousing", "initial_ask_pct": 14.0, "final_outcome_pct": 7.0, "concessions_given": "Accepted narrower SLA window", "concessions_received": "Insurance cost pass-through capped at 3%", "duration_days": 25, "date_closed": "2024-03-18"},
        {"negotiation_id": "NEG-2024-02", "supplier": "Redline Logistics LLC", "category": "logistics", "initial_ask_pct": 5.5, "final_outcome_pct": 2.8, "concessions_given": "Accepted auto-renewal clause", "concessions_received": "2% early payment discount added", "duration_days": 8, "date_closed": "2024-05-20"},
        {"negotiation_id": "NEG-2025-01", "supplier": "SwiftLine Freight", "category": "logistics", "initial_ask_pct": 10.0, "final_outcome_pct": 5.5, "concessions_given": "Increased committed volume 15%", "concessions_received": "Added supply chain disruption to force majeure", "duration_days": 20, "date_closed": "2025-08-30"},
    ]

    with open(DATA_DIR / "negotiation-history.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def main():
    ensure_dirs()
    build_current_contract()
    build_proposed_renewal()
    build_supplier_performance()
    build_market_benchmarks()
    build_negotiation_history()
    print("Course 10 data generated.")
    print(f"  Data directory: {DATA_DIR}")
    print(f"  Files: current-contract.md, proposed-renewal.md, supplier-performance.csv,")
    print(f"         market-benchmarks.md, negotiation-history.csv")


if __name__ == "__main__":
    main()
