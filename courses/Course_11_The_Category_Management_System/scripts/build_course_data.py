"""
Course 11: The Category Management System
Generates practice data for Meridian Corp multi-category management.
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
OUTPUTS_DIR = PRACTICE_DIR / "outputs" / "briefings"
STATE_DIR = PRACTICE_DIR / "state"

CATEGORIES = [
    {"name": "IT services", "annual_spend": 18200000, "suppliers": 6},
    {"name": "Logistics", "annual_spend": 16800000, "suppliers": 5},
    {"name": "Facilities", "annual_spend": 14100000, "suppliers": 4},
    {"name": "Raw materials", "annual_spend": 15600000, "suppliers": 6},
    {"name": "Professional services", "annual_spend": 12400000, "suppliers": 5},
    {"name": "MRO", "annual_spend": 10300000, "suppliers": 4},
]

SUPPLIER_NAMES = {
    "IT services": ["CloudStack Solutions", "DataVault Inc", "NetSecure Corp", "Pinnacle IT Group", "RapidDeploy LLC", "TechBridge Systems"],
    "Logistics": ["Redline Logistics LLC", "SwiftLine Freight", "Horizon Distribution", "National Carriers Inc", "Coastal Transport Co"],
    "Facilities": ["ProClean Services", "Meridian Maintenance Group", "SafeGuard Security", "GreenSpace Facilities"],
    "Raw materials": ["Great Lakes Steel", "Heartland Polymers", "Pacific Aluminum", "Apex Electronics", "Cascade Fasteners", "Bayshore Materials"],
    "Professional services": ["Sterling Consulting", "Whitfield Advisory", "Keystone Legal", "Broadview Analytics", "Nexus Staffing"],
    "MRO": ["Industrial Supply Co", "FastParts Direct", "ToolWorks Inc", "Grainger West"],
}


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def build_program_state():
    state = {
        "as_of": "2026-04-25",
        "total_annual_spend": 87400000,
        "categories": []
    }
    risk_flags = {
        "IT services": [],
        "Logistics": ["Initiative LOG-002 at risk: carrier capacity constraint in Southeast"],
        "Facilities": ["Contract FAC-CTR-003 expires 2026-05-31, renewal not started"],
        "Raw materials": ["Steel price volatility: 12% increase in Q1 2026"],
        "Professional services": ["Supplier consolidation: reducing from 5 to 3 vendors by Q3"],
        "MRO": ["New catalog rollout: phase 1 starting 2026-05-01"],
    }
    initiatives_by_cat = {
        "IT services": [
            {"id": "IT-001", "name": "Cloud migration savings", "target": 450000, "status": "on_track", "stage": "execution", "owner": "Sarah Kim"},
            {"id": "IT-002", "name": "License rationalization", "target": 280000, "status": "on_track", "stage": "execution", "owner": "Sarah Kim"},
            {"id": "IT-003", "name": "Security vendor consolidation", "target": 180000, "status": "on_track", "stage": "planning", "owner": "Sarah Kim"},
        ],
        "Logistics": [
            {"id": "LOG-001", "name": "Route optimization", "target": 320000, "status": "on_track", "stage": "execution", "owner": "Marcus Davis"},
            {"id": "LOG-002", "name": "Carrier consolidation", "target": 540000, "status": "at_risk", "stage": "execution", "owner": "Marcus Davis"},
        ],
        "Facilities": [
            {"id": "FAC-001", "name": "Energy efficiency program", "target": 210000, "status": "on_track", "stage": "monitoring", "owner": "Ana Torres"},
            {"id": "FAC-002", "name": "Cleaning services rebid", "target": 175000, "status": "on_track", "stage": "planning", "owner": "Ana Torres"},
        ],
        "Raw materials": [
            {"id": "RM-001", "name": "Steel volume aggregation", "target": 680000, "status": "on_track", "stage": "execution", "owner": "James Park"},
            {"id": "RM-002", "name": "Polymer specification standardization", "target": 290000, "status": "behind_schedule", "stage": "execution", "owner": "James Park"},
        ],
        "Professional services": [
            {"id": "PS-001", "name": "Consulting rate card negotiation", "target": 380000, "status": "on_track", "stage": "execution", "owner": "Kevin Wright"},
            {"id": "PS-002", "name": "Vendor consolidation 5 to 3", "target": 260000, "status": "on_track", "stage": "planning", "owner": "Kevin Wright"},
        ],
        "MRO": [
            {"id": "MRO-001", "name": "Catalog rollout and spend redirect", "target": 310000, "status": "not_started", "stage": "planning", "owner": "Lisa Chen"},
        ],
    }

    for cat in CATEGORIES:
        cat_name = cat["name"]
        state["categories"].append({
            "name": cat_name,
            "annual_spend": cat["annual_spend"],
            "supplier_count": cat["suppliers"],
            "risk_flags": risk_flags.get(cat_name, []),
            "active_initiatives": initiatives_by_cat.get(cat_name, []),
        })

    with open(DATA_DIR / "program-state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def build_category_spend():
    """~1500 spend transactions across 6 categories over 12 months."""
    rows = []
    txn_id = 1000
    months = [f"2025-{m:02d}" for m in range(5, 13)] + [f"2026-{m:02d}" for m in range(1, 5)]

    for cat in CATEGORIES:
        cat_name = cat["name"]
        suppliers = SUPPLIER_NAMES[cat_name]
        monthly_target = cat["annual_spend"] / 12
        txns_per_month = random.randint(18, 25)

        for month in months:
            month_total = 0
            for j in range(txns_per_month):
                txn_id += 1
                supplier = random.choice(suppliers)
                amount = round(monthly_target / txns_per_month * random.uniform(0.5, 1.5), 2)
                day = random.randint(1, 28)
                rows.append({
                    "transaction_id": f"TXN-{txn_id}",
                    "date": f"{month}-{day:02d}",
                    "category": cat_name,
                    "supplier": supplier,
                    "description": f"{cat_name} services",
                    "amount_usd": amount,
                    "po_number": f"PO-{txn_id}",
                    "cost_center": f"CC-{random.randint(100, 999)}",
                })

    random.shuffle(rows)

    with open(DATA_DIR / "category-spend.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print(f"  category-spend.csv: {len(rows)} rows")


def build_supplier_scorecards():
    """30 suppliers scored across 4 quarters. 120 rows total."""
    rows = []
    quarters = ["2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1"]
    all_suppliers = []
    sup_id = 0

    for cat_name, suppliers in SUPPLIER_NAMES.items():
        for name in suppliers:
            sup_id += 1
            all_suppliers.append({
                "supplier_id": f"SUP{sup_id:03d}",
                "supplier_name": name,
                "category": cat_name,
            })

    # Declining suppliers
    declining = {"Apex Electronics", "Horizon Distribution"}
    # Improving suppliers
    improving = {"Pacific Aluminum", "Nexus Staffing"}

    for sup in all_suppliers:
        base_quality = random.uniform(3.2, 4.8)
        base_delivery = random.uniform(3.0, 4.7)
        base_cost = random.uniform(3.0, 4.5)
        base_resp = random.uniform(3.2, 4.6)

        for qi, q in enumerate(quarters):
            drift = 0
            if sup["supplier_name"] in declining:
                drift = -0.25 * qi
            elif sup["supplier_name"] in improving:
                drift = 0.15 * qi

            quality = round(min(5.0, max(1.0, base_quality + drift + random.uniform(-0.2, 0.2))), 1)
            delivery = round(min(5.0, max(1.0, base_delivery + drift + random.uniform(-0.2, 0.2))), 1)
            cost = round(min(5.0, max(1.0, base_cost + random.uniform(-0.15, 0.15))), 1)
            responsiveness = round(min(5.0, max(1.0, base_resp + random.uniform(-0.2, 0.2))), 1)
            overall = round((quality + delivery + cost + responsiveness) / 4, 1)

            rows.append({
                "supplier_id": sup["supplier_id"],
                "supplier_name": sup["supplier_name"],
                "category": sup["category"],
                "quarter": q,
                "quality_score": quality,
                "delivery_score": delivery,
                "cost_score": cost,
                "responsiveness_score": responsiveness,
                "overall_score": overall,
            })

    with open(DATA_DIR / "supplier-scorecards.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def build_contract_calendar():
    """25 contracts with expiry dates, renewal windows, and auto-renewal flags."""
    rows = []
    contract_id = 0

    for cat in CATEGORIES:
        cat_name = cat["name"]
        suppliers = SUPPLIER_NAMES[cat_name]
        contracts_per_cat = min(len(suppliers), random.randint(3, 5))

        for i in range(contracts_per_cat):
            contract_id += 1
            supplier = suppliers[i % len(suppliers)]
            start_year = random.choice([2023, 2024, 2025])
            start_month = random.randint(1, 12)
            duration_months = random.choice([12, 24, 36])

            end_year = start_year + (start_month + duration_months - 1) // 12
            end_month = (start_month + duration_months - 1) % 12 + 1

            notice_days = random.choice([90, 120, 180])
            auto_renew = random.choice(["yes", "yes", "no"])
            annual_value = round(cat["annual_spend"] / len(suppliers) * random.uniform(0.7, 1.3), 0)

            rows.append({
                "contract_id": f"CTR-{contract_id:03d}",
                "supplier": supplier,
                "category": cat_name,
                "start_date": f"{start_year}-{start_month:02d}-01",
                "end_date": f"{end_year}-{end_month:02d}-{28}",
                "duration_months": duration_months,
                "annual_value_usd": int(annual_value),
                "notice_period_days": notice_days,
                "auto_renewal": auto_renew,
                "status": "active",
            })

    with open(DATA_DIR / "contract-calendar.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def build_initiative_pipeline():
    """12 active initiatives across 6 categories."""
    rows = [
        {"initiative_id": "IT-001", "category": "IT services", "name": "Cloud migration savings", "owner": "Sarah Kim", "savings_target_usd": 450000, "stage": "execution", "status": "on_track", "start_date": "2026-01-15", "target_completion": "2026-06-30", "realized_savings_usd": 185000},
        {"initiative_id": "IT-002", "category": "IT services", "name": "License rationalization", "owner": "Sarah Kim", "savings_target_usd": 280000, "stage": "execution", "status": "on_track", "start_date": "2026-02-01", "target_completion": "2026-07-31", "realized_savings_usd": 92000},
        {"initiative_id": "IT-003", "category": "IT services", "name": "Security vendor consolidation", "owner": "Sarah Kim", "savings_target_usd": 180000, "stage": "planning", "status": "on_track", "start_date": "2026-04-01", "target_completion": "2026-09-30", "realized_savings_usd": 0},
        {"initiative_id": "LOG-001", "category": "Logistics", "name": "Route optimization", "owner": "Marcus Davis", "savings_target_usd": 320000, "stage": "execution", "status": "on_track", "start_date": "2025-11-01", "target_completion": "2026-05-31", "realized_savings_usd": 210000},
        {"initiative_id": "LOG-002", "category": "Logistics", "name": "Carrier consolidation", "owner": "Marcus Davis", "savings_target_usd": 540000, "stage": "execution", "status": "at_risk", "start_date": "2026-01-10", "target_completion": "2026-08-31", "realized_savings_usd": 125000},
        {"initiative_id": "FAC-001", "category": "Facilities", "name": "Energy efficiency program", "owner": "Ana Torres", "savings_target_usd": 210000, "stage": "monitoring", "status": "on_track", "start_date": "2025-07-01", "target_completion": "2026-06-30", "realized_savings_usd": 178000},
        {"initiative_id": "FAC-002", "category": "Facilities", "name": "Cleaning services rebid", "owner": "Ana Torres", "savings_target_usd": 175000, "stage": "planning", "status": "on_track", "start_date": "2026-03-15", "target_completion": "2026-09-30", "realized_savings_usd": 0},
        {"initiative_id": "RM-001", "category": "Raw materials", "name": "Steel volume aggregation", "owner": "James Park", "savings_target_usd": 680000, "stage": "execution", "status": "on_track", "start_date": "2025-10-01", "target_completion": "2026-06-30", "realized_savings_usd": 420000},
        {"initiative_id": "RM-002", "category": "Raw materials", "name": "Polymer specification standardization", "owner": "James Park", "savings_target_usd": 290000, "stage": "execution", "status": "behind_schedule", "start_date": "2026-01-15", "target_completion": "2026-07-31", "realized_savings_usd": 45000},
        {"initiative_id": "PS-001", "category": "Professional services", "name": "Consulting rate card negotiation", "owner": "Kevin Wright", "savings_target_usd": 380000, "stage": "execution", "status": "on_track", "start_date": "2025-09-01", "target_completion": "2026-04-30", "realized_savings_usd": 340000},
        {"initiative_id": "PS-002", "category": "Professional services", "name": "Vendor consolidation 5 to 3", "owner": "Kevin Wright", "savings_target_usd": 260000, "stage": "planning", "status": "on_track", "start_date": "2026-04-01", "target_completion": "2026-10-31", "realized_savings_usd": 0},
        {"initiative_id": "MRO-001", "category": "MRO", "name": "Catalog rollout and spend redirect", "owner": "Lisa Chen", "savings_target_usd": 310000, "stage": "planning", "status": "not_started", "start_date": "2026-05-01", "target_completion": "2026-11-30", "realized_savings_usd": 0},
    ]

    with open(DATA_DIR / "initiative-pipeline.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def build_state_files():
    action_log = """# Action Log

## 2026-04-25

No actions recorded yet. This file is updated after each Monday briefing.
"""
    with open(STATE_DIR / "action-log.md", "w", encoding="utf-8") as f:
        f.write(action_log)


def main():
    ensure_dirs()
    build_program_state()
    build_category_spend()
    build_supplier_scorecards()
    build_contract_calendar()
    build_initiative_pipeline()
    build_state_files()
    print("Course 11 data generated.")
    print(f"  Data directory: {DATA_DIR}")


if __name__ == "__main__":
    main()
