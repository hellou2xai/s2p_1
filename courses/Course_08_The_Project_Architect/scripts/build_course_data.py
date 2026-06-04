"""Generate the practice data set for Course 8: The Project Architect.

Scenario: Pinnacle Procurement, a US-based procurement team managing a
$15M annual savings program across eight category initiatives. Students
build a Claude Code project with cross-session memory, state tracking,
and persistent initiative management.

Produces a flat practice/ folder:
- data/ holds: initiatives.csv (8 initiatives), savings-log.csv (~1,200 rows),
  stakeholders.csv (12 stakeholders), milestone-tracker.csv (40 milestones)
- state/ is empty: TodoWrite-maintained status files go here
- outputs/weekly-reviews/ is empty: weekly review outputs land here

Deterministic via random.seed(42).
All currency in USD. All geography US-based.
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


INITIATIVES = [
    {
        "initiative_id": "INIT-001",
        "name": "Direct Materials Consolidation",
        "category": "direct-materials",
        "owner": "Sarah Chen",
        "target_savings_usd": 2800000,
        "stage": "execution",
        "start_date": "2026-01-15",
        "target_completion": "2026-09-30",
        "status": "on_track",
    },
    {
        "initiative_id": "INIT-002",
        "name": "Logistics Network Optimization",
        "category": "logistics",
        "owner": "Marcus Rivera",
        "target_savings_usd": 2200000,
        "stage": "sourcing",
        "start_date": "2026-02-01",
        "target_completion": "2026-10-31",
        "status": "at_risk",
    },
    {
        "initiative_id": "INIT-003",
        "name": "IT Services Rationalization",
        "category": "it-services",
        "owner": "Priya Patel",
        "target_savings_usd": 1900000,
        "stage": "execution",
        "start_date": "2025-11-01",
        "target_completion": "2026-06-30",
        "status": "on_track",
    },
    {
        "initiative_id": "INIT-004",
        "name": "Facilities Management Rebid",
        "category": "facilities",
        "owner": "James Wright",
        "target_savings_usd": 1500000,
        "stage": "planning",
        "start_date": "2026-03-15",
        "target_completion": "2026-12-31",
        "status": "on_track",
    },
    {
        "initiative_id": "INIT-005",
        "name": "Professional Services Rate Card",
        "category": "professional-services",
        "owner": "Sarah Chen",
        "target_savings_usd": 1800000,
        "stage": "negotiation",
        "start_date": "2026-01-01",
        "target_completion": "2026-07-31",
        "status": "on_track",
    },
    {
        "initiative_id": "INIT-006",
        "name": "MRO Catalog Standardization",
        "category": "mro",
        "owner": "David Kim",
        "target_savings_usd": 1200000,
        "stage": "planning",
        "start_date": "2026-04-01",
        "target_completion": "2027-01-31",
        "status": "not_started",
    },
    {
        "initiative_id": "INIT-007",
        "name": "Packaging Material Switch",
        "category": "direct-materials",
        "owner": "Marcus Rivera",
        "target_savings_usd": 1600000,
        "stage": "evaluation",
        "start_date": "2026-02-15",
        "target_completion": "2026-08-31",
        "status": "behind_schedule",
    },
    {
        "initiative_id": "INIT-008",
        "name": "Temp Staffing Consolidation",
        "category": "professional-services",
        "owner": "Priya Patel",
        "target_savings_usd": 1900000,
        "stage": "execution",
        "start_date": "2025-10-01",
        "target_completion": "2026-05-31",
        "status": "on_track",
    },
]

STAGES = ["planning", "sourcing", "evaluation", "negotiation", "execution", "monitoring"]

STAKEHOLDERS = [
    {"name": "Sarah Chen", "role": "Senior Category Manager", "email": "s.chen@pinnacle.com", "initiatives": "INIT-001,INIT-005"},
    {"name": "Marcus Rivera", "role": "Category Manager, Logistics", "email": "m.rivera@pinnacle.com", "initiatives": "INIT-002,INIT-007"},
    {"name": "Priya Patel", "role": "Category Manager, IT and Services", "email": "p.patel@pinnacle.com", "initiatives": "INIT-003,INIT-008"},
    {"name": "James Wright", "role": "Facilities Procurement Lead", "email": "j.wright@pinnacle.com", "initiatives": "INIT-004"},
    {"name": "David Kim", "role": "MRO Procurement Analyst", "email": "d.kim@pinnacle.com", "initiatives": "INIT-006"},
    {"name": "Lisa Torres", "role": "VP of Procurement", "email": "l.torres@pinnacle.com", "initiatives": "all"},
    {"name": "Robert Hayes", "role": "CFO", "email": "r.hayes@pinnacle.com", "initiatives": "all"},
    {"name": "Amanda Foster", "role": "Procurement Operations Manager", "email": "a.foster@pinnacle.com", "initiatives": "all"},
    {"name": "Chris Nguyen", "role": "Savings Program Analyst", "email": "c.nguyen@pinnacle.com", "initiatives": "all"},
    {"name": "Elena Rodriguez", "role": "Contract Manager", "email": "e.rodriguez@pinnacle.com", "initiatives": "INIT-001,INIT-003,INIT-005"},
    {"name": "Tom Baker", "role": "Supply Chain Director", "email": "t.baker@pinnacle.com", "initiatives": "INIT-001,INIT-002"},
    {"name": "Nina Sharma", "role": "Compliance Officer", "email": "n.sharma@pinnacle.com", "initiatives": "all"},
]


def build_savings_log():
    """~1,200 rows of weekly savings tracking entries across all 8 initiatives."""
    rows = []
    entry_id = 1

    for init in INITIATIVES:
        start = date.fromisoformat(init["start_date"])
        # Generate weekly entries from start to today
        current = start
        realized_cumulative = 0
        target_weekly = init["target_savings_usd"] / 52  # simplified weekly target

        while current <= TODAY:
            if init["status"] == "not_started":
                realized = 0
            elif init["status"] == "behind_schedule":
                realized = round(target_weekly * random.uniform(0.3, 0.7), 2)
            elif init["status"] == "at_risk":
                realized = round(target_weekly * random.uniform(0.4, 0.8), 2)
            else:
                realized = round(target_weekly * random.uniform(0.7, 1.3), 2)

            realized_cumulative += realized
            weeks_elapsed = max(1, (current - start).days // 7)
            target_cumulative = round(target_weekly * weeks_elapsed, 2)

            rows.append({
                "entry_id": f"SAV-{entry_id:04d}",
                "initiative_id": init["initiative_id"],
                "initiative_name": init["name"],
                "week_ending": current.isoformat(),
                "realized_savings_usd": round(realized, 2),
                "realized_cumulative_usd": round(realized_cumulative, 2),
                "target_cumulative_usd": round(target_cumulative, 2),
                "variance_usd": round(realized_cumulative - target_cumulative, 2),
                "category": init["category"],
                "stage": init["stage"],
            })
            entry_id += 1
            current += timedelta(days=7)

    return rows


def build_milestones():
    """40 milestones across the 8 initiatives (5 per initiative)."""
    rows = []
    milestone_names = [
        "Scope definition complete",
        "Market analysis complete",
        "RFP issued",
        "Bids evaluated",
        "Recommendation approved",
    ]

    for init in INITIATIVES:
        start = date.fromisoformat(init["start_date"])
        end = date.fromisoformat(init["target_completion"])
        span = (end - start).days
        for i, name in enumerate(milestone_names):
            target = start + timedelta(days=int(span * (i + 1) / 6))
            if target < TODAY:
                if init["status"] in ("behind_schedule", "at_risk") and i >= 2:
                    ms_status = "overdue"
                    actual = None
                else:
                    ms_status = "completed"
                    actual = (target + timedelta(days=random.randint(-3, 5))).isoformat()
            else:
                ms_status = "pending"
                actual = None

            rows.append({
                "initiative_id": init["initiative_id"],
                "milestone": name,
                "target_date": target.isoformat(),
                "actual_date": actual or "",
                "status": ms_status,
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
    print("Building Course 08 practice data...")
    print()

    data_dir = PRACTICE / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "state").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "outputs" / "weekly-reviews").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "initiatives").mkdir(parents=True, exist_ok=True)

    # Write initiatives
    write_csv(data_dir / "initiatives.csv", INITIATIVES)

    # Write stakeholders
    write_csv(data_dir / "stakeholders.csv", STAKEHOLDERS)

    # Build and write savings log
    savings = build_savings_log()
    savings.sort(key=lambda r: (r["week_ending"], r["initiative_id"]))
    write_csv(data_dir / "savings-log.csv", savings)

    # Build and write milestones
    milestones = build_milestones()
    write_csv(data_dir / "milestone-tracker.csv", milestones)

    print()
    print("Done. All files in practice/data/")


if __name__ == "__main__":
    main()
