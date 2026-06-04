"""Generate the practice data set for Course 5: The Orchestrator.

Scenario: Atlas Procurement Services, a US-based shared services center.
The team scores 50 strategic suppliers quarterly. A single sequential
session risks context contamination and takes too long. Students build
a multi-agent orchestrator that decomposes the portfolio, spawns parallel
worker sub-agents per batch, and aggregates results into a portfolio summary.

Produces a flat practice/ folder:
- data/ holds: supplier-master.csv (50 suppliers),
  q3-performance.csv (50 rows: one per supplier with 6 KPI columns),
  spend-by-supplier.csv (~1,800 rows of monthly spend over 12 months),
  risk-signals.csv (50 rows: financial and operational risk indicators)
- batch-outputs/ is empty: worker agents write here
- outputs/ is empty: orchestrator summary lands here

Deterministic via random.seed(42).
All currency in USD. All geography US-based.
"""

from __future__ import annotations

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRACTICE = ROOT / "practice"

random.seed(42)

TODAY = date(2026, 4, 25)
YEAR_AGO = date(2025, 4, 26)


# ---------------------------------------------------------------------------
# Supplier master (50 suppliers across 5 categories)
# ---------------------------------------------------------------------------

CATEGORIES = {
    "raw-materials": [
        ("SUP001", "Great Lakes Steel", "Chicago", "IL", "strategic", 4200000),
        ("SUP002", "Heartland Polymers", "Houston", "TX", "strategic", 3800000),
        ("SUP003", "Pacific Aluminum", "Portland", "OR", "strategic", 3100000),
        ("SUP004", "Apex Electronics", "San Jose", "CA", "preferred", 2400000),
        ("SUP005", "Cascade Fasteners", "Seattle", "WA", "preferred", 1800000),
        ("SUP006", "Summit Metals", "Denver", "CO", "preferred", 1600000),
        ("SUP007", "Liberty Composites", "Detroit", "MI", "approved", 1200000),
        ("SUP008", "Frontier Plastics", "Dallas", "TX", "approved", 980000),
        ("SUP009", "Harbor Wire", "Baltimore", "MD", "approved", 760000),
        ("SUP010", "Keystone Coatings", "Pittsburgh", "PA", "approved", 540000),
    ],
    "logistics": [
        ("SUP011", "Continental Freight", "Memphis", "TN", "strategic", 3600000),
        ("SUP012", "Patriot Logistics", "Atlanta", "GA", "strategic", 2900000),
        ("SUP013", "Eagle Transport", "Indianapolis", "IN", "preferred", 2100000),
        ("SUP014", "Horizon Carriers", "Louisville", "KY", "preferred", 1700000),
        ("SUP015", "Summit Shipping", "Nashville", "TN", "preferred", 1400000),
        ("SUP016", "Gateway Freight", "St. Louis", "MO", "approved", 1050000),
        ("SUP017", "Prairie Express", "Kansas City", "KS", "approved", 820000),
        ("SUP018", "Valley Haulage", "Omaha", "NE", "approved", 610000),
        ("SUP019", "Lakeshore Drayage", "Milwaukee", "WI", "approved", 480000),
        ("SUP020", "Bridgewater Cold Chain", "Columbus", "OH", "approved", 350000),
    ],
    "it-services": [
        ("SUP021", "TechForward Solutions", "Austin", "TX", "strategic", 2800000),
        ("SUP022", "CloudBridge Systems", "San Francisco", "CA", "strategic", 2500000),
        ("SUP023", "Nexus IT Services", "Raleigh", "NC", "preferred", 1900000),
        ("SUP024", "Pinnacle Software", "Boston", "MA", "preferred", 1500000),
        ("SUP025", "DataVault Analytics", "Charlotte", "NC", "preferred", 1100000),
        ("SUP026", "CyberShield Security", "Washington", "DC", "approved", 850000),
        ("SUP027", "Quantum Hosting", "Phoenix", "AZ", "approved", 620000),
        ("SUP028", "Agile Platforms", "Salt Lake City", "UT", "approved", 480000),
        ("SUP029", "Redstone Cloud", "Richmond", "VA", "approved", 360000),
        ("SUP030", "Beacon Consulting", "Tampa", "FL", "approved", 280000),
    ],
    "facilities": [
        ("SUP031", "National Facilities Group", "Philadelphia", "PA", "strategic", 2200000),
        ("SUP032", "Metro Building Services", "Newark", "NJ", "strategic", 1800000),
        ("SUP033", "Greenfield Maintenance", "Hartford", "CT", "preferred", 1400000),
        ("SUP034", "Atlas HVAC", "Providence", "RI", "preferred", 1100000),
        ("SUP035", "Cornerstone Electric", "Buffalo", "NY", "preferred", 900000),
        ("SUP036", "SafeGuard Fire Systems", "Albany", "NY", "approved", 700000),
        ("SUP037", "ClearView Janitorial", "Trenton", "NJ", "approved", 520000),
        ("SUP038", "Precision Plumbing", "Scranton", "PA", "approved", 380000),
        ("SUP039", "Eastside Landscaping", "Syracuse", "NY", "approved", 290000),
        ("SUP040", "Heritage Painting", "New Haven", "CT", "approved", 210000),
    ],
    "professional-services": [
        ("SUP041", "Whitfield Consulting", "New York", "NY", "strategic", 2600000),
        ("SUP042", "Sterling Advisory", "Chicago", "IL", "strategic", 2100000),
        ("SUP043", "Meridian Legal", "Washington", "DC", "preferred", 1600000),
        ("SUP044", "Crestline Accounting", "Minneapolis", "MN", "preferred", 1200000),
        ("SUP045", "Vanguard Staffing", "Denver", "CO", "preferred", 950000),
        ("SUP046", "Catalyst Training", "Portland", "OR", "approved", 700000),
        ("SUP047", "Blueprint Marketing", "Miami", "FL", "approved", 520000),
        ("SUP048", "Ironside Recruiting", "Detroit", "MI", "approved", 380000),
        ("SUP049", "Northstar Audit", "Milwaukee", "WI", "approved", 290000),
        ("SUP050", "Clearpath Compliance", "San Diego", "CA", "approved", 220000),
    ],
}

# Scorecard weights (encoded in CLAUDE.md for the student)
WEIGHTS = {
    "quality": 0.25,
    "delivery": 0.20,
    "responsiveness": 0.15,
    "cost": 0.25,
    "innovation": 0.15,
}

# Suppliers with planted performance patterns
DECLINING = {"SUP004", "SUP019", "SUP048"}  # declining overall
IMPROVING = {"SUP007", "SUP028", "SUP035"}  # improving overall
AT_RISK = {"SUP004", "SUP019", "SUP040"}  # at_risk status
UNDER_REVIEW = {"SUP009", "SUP048"}  # under_review status


def build_supplier_master():
    """50 suppliers with tier, category, location, annual spend, status."""
    rows = []
    for cat, suppliers in CATEGORIES.items():
        for sid, name, city, state, tier, annual_spend in suppliers:
            if sid in AT_RISK:
                status = "at_risk"
                risk = "high"
            elif sid in UNDER_REVIEW:
                status = "under_review"
                risk = "medium"
            else:
                status = "active"
                risk = random.choice(["low", "low", "low", "medium"])
            rows.append({
                "supplier_id": sid,
                "supplier_name": name,
                "category": cat,
                "tier": tier,
                "city": city,
                "state": state,
                "annual_spend_usd": annual_spend,
                "risk_rating": risk,
                "status": status,
            })
    return rows


def build_q3_performance(suppliers):
    """One row per supplier with six KPI scores for 2026-Q1 (the quarter to score)."""
    rows = []
    for s in suppliers:
        sid = s["supplier_id"]
        tier = s["tier"]

        # Base scores by tier
        if tier == "strategic":
            base = random.uniform(78, 95)
        elif tier == "preferred":
            base = random.uniform(70, 90)
        else:
            base = random.uniform(60, 85)

        # Generate individual dimension scores
        quality = round(min(100, max(0, base + random.uniform(-8, 8))), 1)
        delivery = round(min(100, max(0, base + random.uniform(-10, 6))), 1)
        responsiveness = round(min(100, max(0, base + random.uniform(-6, 10))), 1)
        cost = round(min(100, max(0, base + random.uniform(-8, 8))), 1)
        innovation = round(min(100, max(0, base + random.uniform(-12, 12))), 1)

        # Declining suppliers: low scores in Q1
        if sid in DECLINING:
            quality = round(max(0, quality - random.uniform(15, 25)), 1)
            delivery = round(max(0, delivery - random.uniform(10, 20)), 1)

        # Improving suppliers: high scores in Q1
        if sid in IMPROVING:
            quality = round(min(100, quality + random.uniform(5, 12)), 1)
            delivery = round(min(100, delivery + random.uniform(5, 10)), 1)

        overall = round(
            quality * WEIGHTS["quality"]
            + delivery * WEIGHTS["delivery"]
            + responsiveness * WEIGHTS["responsiveness"]
            + cost * WEIGHTS["cost"]
            + innovation * WEIGHTS["innovation"],
            1,
        )

        rows.append({
            "supplier_id": sid,
            "supplier_name": s["supplier_name"],
            "quarter": "2026-Q1",
            "quality_score": quality,
            "delivery_score": delivery,
            "responsiveness_score": responsiveness,
            "cost_score": cost,
            "innovation_score": innovation,
            "overall_score": overall,
        })
    return rows


def build_prior_quarters(suppliers):
    """Historical scores for Q3-2025, Q4-2025, and Q1-2026 to show trends."""
    all_rows = []
    quarters = ["2025-Q2", "2025-Q3", "2025-Q4"]

    for s in suppliers:
        sid = s["supplier_id"]
        tier = s["tier"]

        if tier == "strategic":
            base = random.uniform(80, 92)
        elif tier == "preferred":
            base = random.uniform(72, 88)
        else:
            base = random.uniform(62, 82)

        for qi, q in enumerate(quarters):
            # Declining: start high, drop each quarter
            if sid in DECLINING:
                adj = -qi * random.uniform(3, 6)
            elif sid in IMPROVING:
                adj = qi * random.uniform(2, 5)
            else:
                adj = random.uniform(-3, 3)

            quality = round(min(100, max(0, base + adj + random.uniform(-5, 5))), 1)
            delivery = round(min(100, max(0, base + adj + random.uniform(-6, 4))), 1)
            responsiveness = round(min(100, max(0, base + adj + random.uniform(-4, 6))), 1)
            cost = round(min(100, max(0, base + adj + random.uniform(-5, 5))), 1)
            innovation = round(min(100, max(0, base + adj + random.uniform(-8, 8))), 1)

            overall = round(
                quality * WEIGHTS["quality"]
                + delivery * WEIGHTS["delivery"]
                + responsiveness * WEIGHTS["responsiveness"]
                + cost * WEIGHTS["cost"]
                + innovation * WEIGHTS["innovation"],
                1,
            )

            all_rows.append({
                "supplier_id": sid,
                "supplier_name": s["supplier_name"],
                "quarter": q,
                "quality_score": quality,
                "delivery_score": delivery,
                "responsiveness_score": responsiveness,
                "cost_score": cost,
                "innovation_score": innovation,
                "overall_score": overall,
            })
    return all_rows


def build_spend_by_supplier(suppliers):
    """Monthly spend per supplier over 12 months (~1,800 rows total).
    36 months x 50 suppliers would be 600, but we do 12 months x ~3 entries
    per supplier per month to get volume."""
    rows = []
    txn_id = 5001
    for s in suppliers:
        sid = s["supplier_id"]
        monthly_base = s["annual_spend_usd"] / 12

        for m in range(12):
            month_date = YEAR_AGO + timedelta(days=30 * m)
            # 3 transactions per supplier per month on average
            n_txns = random.randint(2, 4)
            for _ in range(n_txns):
                day_offset = random.randint(0, 28)
                txn_date = month_date + timedelta(days=day_offset)
                if txn_date > TODAY:
                    continue
                amount = round(monthly_base / n_txns * random.uniform(0.7, 1.3), 2)
                rows.append({
                    "transaction_id": f"TXN{txn_id:06d}",
                    "date": txn_date.isoformat(),
                    "supplier_id": sid,
                    "supplier_name": s["supplier_name"],
                    "category": s["category"],
                    "amount_usd": amount,
                    "cost_center": random.choice([
                        "CC-100", "CC-200", "CC-300", "CC-400", "CC-500",
                    ]),
                })
                txn_id += 1
    return rows


def build_risk_signals(suppliers):
    """One row per supplier with financial and operational risk indicators."""
    rows = []
    for s in suppliers:
        sid = s["supplier_id"]
        # Financial health score (0-100)
        if sid in AT_RISK:
            financial_health = round(random.uniform(25, 45), 1)
            on_time_delivery_pct = round(random.uniform(65, 78), 1)
            quality_reject_rate = round(random.uniform(4.5, 8.2), 2)
        elif sid in UNDER_REVIEW:
            financial_health = round(random.uniform(45, 60), 1)
            on_time_delivery_pct = round(random.uniform(72, 82), 1)
            quality_reject_rate = round(random.uniform(3.0, 5.5), 2)
        else:
            financial_health = round(random.uniform(60, 95), 1)
            on_time_delivery_pct = round(random.uniform(82, 99), 1)
            quality_reject_rate = round(random.uniform(0.2, 3.0), 2)

        # Concentration risk
        single_source = "yes" if sid in {"SUP001", "SUP011", "SUP021", "SUP031"} else "no"

        rows.append({
            "supplier_id": sid,
            "supplier_name": s["supplier_name"],
            "financial_health_score": financial_health,
            "on_time_delivery_pct": on_time_delivery_pct,
            "quality_reject_rate_pct": quality_reject_rate,
            "single_source": single_source,
            "geographic_risk": random.choice(["low", "low", "low", "medium", "medium", "high"]),
            "cyber_risk_rating": random.choice(["low", "low", "medium", "medium", "high"]),
            "last_audit_date": (TODAY - timedelta(days=random.randint(30, 365))).isoformat(),
        })
    return rows


def write_csv(path, rows, fieldnames=None):
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
    print("Building Course 05 practice data...")
    print()

    # Create directories
    data_dir = PRACTICE / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "outputs").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "batch-outputs").mkdir(parents=True, exist_ok=True)

    # Build supplier master
    suppliers = build_supplier_master()
    write_csv(data_dir / "supplier-master.csv", suppliers)

    # Build Q1 2026 performance (current quarter to score)
    q1_scores = build_q3_performance(suppliers)
    write_csv(data_dir / "q1-performance.csv", q1_scores)

    # Build prior quarter history
    prior = build_prior_quarters(suppliers)
    all_scores = prior + q1_scores
    all_scores.sort(key=lambda r: (r["supplier_id"], r["quarter"]))
    write_csv(data_dir / "scorecard-history.csv", all_scores)

    # Build spend data
    spend = build_spend_by_supplier(suppliers)
    spend.sort(key=lambda r: r["date"])
    write_csv(data_dir / "spend-by-supplier.csv", spend)

    # Build risk signals
    risk = build_risk_signals(suppliers)
    write_csv(data_dir / "risk-signals.csv", risk)

    # Write scorecard weights JSON for reference
    weights_path = data_dir / "scorecard-weights.json"
    with open(weights_path, "w", encoding="utf-8") as f:
        json.dump(WEIGHTS, f, indent=2)
    print(f"  scorecard-weights.json: weights file")

    print()
    print("Done. All files in practice/data/")


if __name__ == "__main__":
    main()
