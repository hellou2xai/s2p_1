"""Generate the practice data set for Course 7: The Pipeline Automator.

Scenario: Ironclad Procurement Group, a US-based procurement shared services
center. The nightly spend monitor runs via cron but has no visibility into
results. Students build stop hooks that send tiered notifications on
completion and escalation alerts for critical anomalies.

Produces a flat practice/ folder:
- data/ holds: daily-spend.csv (~2,000 rows of the last 30 days),
  supplier-master.csv (40 suppliers), thresholds.json (alert thresholds),
  three sample daily monitor output files in outputs/daily-monitors/
- hooks/ is empty: the student writes hook scripts here
- notifications/ is empty: notification outputs land here

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


SUPPLIERS = [
    ("SUP001", "Great Lakes Steel", "raw-materials", "strategic", 4200000),
    ("SUP002", "Heartland Polymers", "raw-materials", "strategic", 3800000),
    ("SUP003", "Pacific Aluminum", "raw-materials", "strategic", 3100000),
    ("SUP004", "Apex Electronics", "raw-materials", "preferred", 2400000),
    ("SUP005", "Cascade Fasteners", "raw-materials", "preferred", 1800000),
    ("SUP006", "Summit Metals", "raw-materials", "preferred", 1600000),
    ("SUP007", "Liberty Composites", "raw-materials", "approved", 1200000),
    ("SUP008", "Frontier Plastics", "raw-materials", "approved", 980000),
    ("SUP011", "Continental Freight", "logistics", "strategic", 3600000),
    ("SUP012", "Patriot Logistics", "logistics", "strategic", 2900000),
    ("SUP013", "Eagle Transport", "logistics", "preferred", 2100000),
    ("SUP014", "Horizon Carriers", "logistics", "preferred", 1700000),
    ("SUP015", "Summit Shipping", "logistics", "preferred", 1400000),
    ("SUP016", "Gateway Freight", "logistics", "approved", 1050000),
    ("SUP021", "TechForward Solutions", "it-services", "strategic", 2800000),
    ("SUP022", "CloudBridge Systems", "it-services", "strategic", 2500000),
    ("SUP023", "Nexus IT Services", "it-services", "preferred", 1900000),
    ("SUP024", "Pinnacle Software", "it-services", "preferred", 1500000),
    ("SUP025", "DataVault Analytics", "it-services", "preferred", 1100000),
    ("SUP026", "CyberShield Security", "it-services", "approved", 850000),
    ("SUP031", "National Facilities Group", "facilities", "strategic", 2200000),
    ("SUP032", "Metro Building Services", "facilities", "strategic", 1800000),
    ("SUP033", "Greenfield Maintenance", "facilities", "preferred", 1400000),
    ("SUP034", "Atlas HVAC", "facilities", "preferred", 1100000),
    ("SUP035", "Cornerstone Electric", "facilities", "preferred", 900000),
    ("SUP036", "SafeGuard Fire Systems", "facilities", "approved", 700000),
    ("SUP041", "Whitfield Consulting", "professional-services", "strategic", 2600000),
    ("SUP042", "Sterling Advisory", "professional-services", "strategic", 2100000),
    ("SUP043", "Meridian Legal", "professional-services", "preferred", 1600000),
    ("SUP044", "Crestline Accounting", "professional-services", "preferred", 1200000),
    ("SUP045", "Vanguard Staffing", "professional-services", "preferred", 950000),
    ("SUP046", "Catalyst Training", "professional-services", "approved", 700000),
    ("SUP047", "Blueprint Marketing", "professional-services", "approved", 520000),
    ("SUP048", "Ironside Recruiting", "professional-services", "approved", 380000),
    ("SUP049", "Northstar Audit", "professional-services", "approved", 290000),
    ("SUP050", "Clearpath Compliance", "professional-services", "approved", 220000),
    ("SUP051", "Redstone Cloud", "it-services", "approved", 360000),
    ("SUP052", "Agile Platforms", "it-services", "approved", 480000),
    ("SUP053", "Heritage Painting", "facilities", "approved", 210000),
    ("SUP054", "Precision Plumbing", "facilities", "approved", 380000),
]


def build_supplier_master():
    rows = []
    for sid, name, cat, tier, annual in SUPPLIERS:
        rows.append({
            "supplier_id": sid,
            "supplier_name": name,
            "category": cat,
            "tier": tier,
            "annual_spend_usd": annual,
            "status": "active",
        })
    return rows


def build_daily_spend():
    """~2,000 rows of daily spend transactions over the last 30 days.
    Plant anomalies on specific dates for the exercises."""
    rows = []
    txn_id = 7001

    for day_offset in range(30):
        txn_date = TODAY - timedelta(days=29 - day_offset)
        # Each supplier has 0-3 transactions per day
        for sup in SUPPLIERS:
            sid, name, cat, tier, annual = sup
            daily_base = annual / 365
            n_txns = random.choices([0, 1, 1, 2], weights=[40, 35, 15, 10])[0]
            for _ in range(n_txns):
                amount = round(daily_base * random.uniform(0.5, 1.8), 2)

                # Plant anomalies on day 25 (April 21, 2026)
                if day_offset == 25 and sid in ("SUP004", "SUP013", "SUP047"):
                    amount = round(daily_base * random.uniform(4.0, 7.0), 2)

                # Plant a critical anomaly on day 28 (April 24, 2026)
                if day_offset == 28 and sid == "SUP001":
                    amount = round(daily_base * 12.0, 2)

                rows.append({
                    "transaction_id": f"TXN{txn_id:06d}",
                    "date": txn_date.isoformat(),
                    "supplier_id": sid,
                    "supplier_name": name,
                    "category": cat,
                    "amount_usd": amount,
                    "po_number": f"PO-{random.randint(10000, 99999)}",
                    "cost_center": random.choice(["CC-100", "CC-200", "CC-300", "CC-400"]),
                })
                txn_id += 1

    return rows


def build_thresholds():
    """Alert thresholds for the spend monitor."""
    return {
        "anomaly_multiplier": 3.0,
        "daily_spend_ceiling_usd": 500000,
        "severity_levels": {
            "routine": "Daily spend within normal range, no anomalies detected.",
            "anomaly": "One or more transactions exceed 3x the supplier daily average.",
            "critical": "Total daily spend exceeds $500,000 or a single transaction exceeds 10x supplier daily average."
        },
        "notification_routing": {
            "routine": "log_file",
            "anomaly": "slack_webhook",
            "critical": "email_escalation"
        }
    }


def build_sample_monitors():
    """Three sample daily monitor output files to show the expected format."""
    monitors = []

    # Routine day
    monitors.append({
        "filename": "monitor-2026-04-20.md",
        "content": (
            "# Daily Spend Monitor: 2026-04-20\n\n"
            "**Severity:** Routine\n\n"
            "## Summary\n\n"
            "Total daily spend: $142,380.45 across 38 transactions from 22 suppliers.\n"
            "No anomalies detected. All transactions within normal range.\n\n"
            "## Top 5 Suppliers by Daily Spend\n\n"
            "| Rank | Supplier | Amount | % of Daily Total |\n"
            "|---|---|---|---|\n"
            "| 1 | Great Lakes Steel | $28,450.00 | 20.0% |\n"
            "| 2 | Continental Freight | $22,100.00 | 15.5% |\n"
            "| 3 | Heartland Polymers | $18,900.00 | 13.3% |\n"
            "| 4 | TechForward Solutions | $14,200.00 | 10.0% |\n"
            "| 5 | Whitfield Consulting | $11,800.00 | 8.3% |\n\n"
            "---\n"
            "Generated by Claude Code on 2026-04-20. Data source: daily-spend.csv.\n"
        ),
    })

    # Anomaly day
    monitors.append({
        "filename": "monitor-2026-04-21.md",
        "content": (
            "# Daily Spend Monitor: 2026-04-21\n\n"
            "**Severity:** Anomaly\n\n"
            "## Summary\n\n"
            "Total daily spend: $218,640.32 across 45 transactions from 28 suppliers.\n"
            "3 anomalies detected. Details below.\n\n"
            "## Anomalies\n\n"
            "| Supplier | Transaction | Amount | Daily Avg | Multiple |\n"
            "|---|---|---|---|---|\n"
            "| Apex Electronics | TXN007842 | $42,800.00 | $6,575.34 | 6.5x |\n"
            "| Eagle Transport | TXN007856 | $31,200.00 | $5,753.42 | 5.4x |\n"
            "| Blueprint Marketing | TXN007891 | $8,450.00 | $1,424.66 | 5.9x |\n\n"
            "## Recommended Actions\n\n"
            "1. Review PO-45231 for Apex Electronics. Amount is 6.5x the daily average.\n"
            "2. Confirm Eagle Transport invoice TXN007856 against the rate card.\n"
            "3. Check Blueprint Marketing PO-67892 for proper approval.\n\n"
            "---\n"
            "Generated by Claude Code on 2026-04-21. Data source: daily-spend.csv.\n"
        ),
    })

    # Critical day
    monitors.append({
        "filename": "monitor-2026-04-24.md",
        "content": (
            "# Daily Spend Monitor: 2026-04-24\n\n"
            "**Severity:** Critical\n\n"
            "## Summary\n\n"
            "Total daily spend: $538,200.18 across 52 transactions from 30 suppliers.\n"
            "CRITICAL: Daily spend exceeds $500,000 ceiling. 1 critical anomaly detected.\n\n"
            "## Critical Anomaly\n\n"
            "| Supplier | Transaction | Amount | Daily Avg | Multiple |\n"
            "|---|---|---|---|---|\n"
            "| Great Lakes Steel | TXN008102 | $138,082.19 | $11,506.85 | 12.0x |\n\n"
            "## Recommended Actions\n\n"
            "1. URGENT: Verify Great Lakes Steel TXN008102 ($138,082.19). This is 12x the daily average. Possible duplicate or unauthorized purchase.\n"
            "2. Review total daily spend of $538,200. This exceeds the $500,000 ceiling by $38,200.\n"
            "3. Escalate to VP of Procurement for same-day review.\n\n"
            "---\n"
            "Generated by Claude Code on 2026-04-24. Data source: daily-spend.csv.\n"
        ),
    })

    return monitors


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
    print("Building Course 07 practice data...")
    print()

    data_dir = PRACTICE / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    monitors_dir = PRACTICE / "outputs" / "daily-monitors"
    monitors_dir.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "hooks").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "notifications").mkdir(parents=True, exist_ok=True)

    # Build supplier master
    suppliers = build_supplier_master()
    write_csv(data_dir / "supplier-master.csv", suppliers)

    # Build daily spend
    spend = build_daily_spend()
    spend.sort(key=lambda r: r["date"])
    write_csv(data_dir / "daily-spend.csv", spend)

    # Build thresholds
    thresholds = build_thresholds()
    thresholds_path = data_dir / "thresholds.json"
    with open(thresholds_path, "w", encoding="utf-8") as f:
        json.dump(thresholds, f, indent=2)
    print(f"  thresholds.json: alert thresholds")

    # Build sample monitor outputs
    monitors = build_sample_monitors()
    for m in monitors:
        filepath = monitors_dir / m["filename"]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(m["content"])
    print(f"  daily-monitors/: {len(monitors)} sample output files (routine, anomaly, critical)")

    print()
    print("Done. All files in practice/data/")


if __name__ == "__main__":
    main()
