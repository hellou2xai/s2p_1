"""Generate the practice data set for Course 9: The Integration Architect.

Scenario: Nexus Procurement Hub, a US-based procurement team connecting
Claude Code to live data sources via MCP servers. Students build a simple
MCP server that exposes procurement data as callable tools.

Produces:
- data/ holds: procurement.db (SQLite database with suppliers, spend, contracts, POs)
- The SQLite DB simulates a "live" data source that refreshes nightly.

Deterministic via random.seed(42).
All currency in USD. All geography US-based.
"""

from __future__ import annotations

import csv
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRACTICE = ROOT / "practice"

random.seed(42)

TODAY = date(2026, 4, 25)

SUPPLIERS = [
    ("SUP001", "Great Lakes Steel", "raw-materials", "strategic", 4200000, "active"),
    ("SUP002", "Heartland Polymers", "raw-materials", "strategic", 3800000, "active"),
    ("SUP003", "Pacific Aluminum", "raw-materials", "strategic", 3100000, "active"),
    ("SUP004", "Apex Electronics", "raw-materials", "preferred", 2400000, "at_risk"),
    ("SUP005", "Cascade Fasteners", "raw-materials", "preferred", 1800000, "active"),
    ("SUP011", "Continental Freight", "logistics", "strategic", 3600000, "active"),
    ("SUP012", "Patriot Logistics", "logistics", "strategic", 2900000, "active"),
    ("SUP013", "Eagle Transport", "logistics", "preferred", 2100000, "active"),
    ("SUP021", "TechForward Solutions", "it-services", "strategic", 2800000, "active"),
    ("SUP022", "CloudBridge Systems", "it-services", "strategic", 2500000, "active"),
    ("SUP023", "Nexus IT Services", "it-services", "preferred", 1900000, "under_review"),
    ("SUP031", "National Facilities Group", "facilities", "strategic", 2200000, "active"),
    ("SUP032", "Metro Building Services", "facilities", "strategic", 1800000, "active"),
    ("SUP041", "Whitfield Consulting", "professional-services", "strategic", 2600000, "active"),
    ("SUP042", "Sterling Advisory", "professional-services", "strategic", 2100000, "active"),
    ("SUP043", "Meridian Legal", "professional-services", "preferred", 1600000, "active"),
    ("SUP044", "Crestline Accounting", "professional-services", "preferred", 1200000, "active"),
    ("SUP045", "Vanguard Staffing", "professional-services", "preferred", 950000, "active"),
    ("SUP046", "Catalyst Training", "professional-services", "approved", 700000, "active"),
    ("SUP047", "Blueprint Marketing", "professional-services", "approved", 520000, "active"),
]


def build_sqlite_db():
    db_path = PRACTICE / "data" / "procurement.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()

    # Suppliers table
    c.execute("""CREATE TABLE suppliers (
        supplier_id TEXT PRIMARY KEY,
        supplier_name TEXT,
        category TEXT,
        tier TEXT,
        annual_spend_usd INTEGER,
        status TEXT
    )""")
    for s in SUPPLIERS:
        c.execute("INSERT INTO suppliers VALUES (?,?,?,?,?,?)", s)

    # Spend transactions table
    c.execute("""CREATE TABLE spend (
        transaction_id TEXT PRIMARY KEY,
        date TEXT,
        supplier_id TEXT,
        supplier_name TEXT,
        category TEXT,
        amount_usd REAL,
        po_number TEXT,
        status TEXT
    )""")

    txn_id = 9001
    for s in SUPPLIERS:
        sid, name, cat, _, annual, _ = s
        monthly = annual / 12
        for m in range(12):
            txn_date = (TODAY - timedelta(days=365)) + timedelta(days=30 * m + random.randint(0, 28))
            if txn_date > TODAY:
                continue
            for _ in range(random.randint(2, 5)):
                amount = round(monthly / 3 * random.uniform(0.5, 1.5), 2)
                po = f"PO-{random.randint(10000, 99999)}"
                status = random.choice(["paid", "paid", "paid", "pending", "approved"])
                c.execute("INSERT INTO spend VALUES (?,?,?,?,?,?,?,?)",
                          (f"TXN{txn_id:06d}", txn_date.isoformat(), sid, name, cat, amount, po, status))
                txn_id += 1

    # Contracts table
    c.execute("""CREATE TABLE contracts (
        contract_id TEXT PRIMARY KEY,
        supplier_id TEXT,
        supplier_name TEXT,
        contract_type TEXT,
        start_date TEXT,
        end_date TEXT,
        annual_value_usd INTEGER,
        status TEXT,
        auto_renew TEXT
    )""")

    for i, s in enumerate(SUPPLIERS):
        sid, name, _, _, annual, _ = s
        cid = f"CTR-2025-{i+1:03d}"
        start = TODAY - timedelta(days=random.randint(180, 730))
        end = start + timedelta(days=random.choice([365, 730]))
        status = "expired" if end < TODAY else ("expiring_soon" if (end - TODAY).days <= 90 else "active")
        c.execute("INSERT INTO contracts VALUES (?,?,?,?,?,?,?,?,?)",
                  (cid, sid, name, random.choice(["MSA", "SOW"]), start.isoformat(), end.isoformat(),
                   annual, status, random.choice(["yes", "no"])))

    # Open POs table
    c.execute("""CREATE TABLE open_pos (
        po_number TEXT PRIMARY KEY,
        supplier_id TEXT,
        supplier_name TEXT,
        category TEXT,
        amount_usd REAL,
        date_created TEXT,
        status TEXT,
        delivery_date TEXT
    )""")

    for i in range(50):
        s = random.choice(SUPPLIERS)
        sid, name, cat, _, annual, _ = s
        po = f"PO-{80000 + i}"
        amount = round(annual / 12 * random.uniform(0.3, 1.0), 2)
        created = TODAY - timedelta(days=random.randint(1, 60))
        delivery = created + timedelta(days=random.randint(14, 90))
        status = random.choice(["open", "open", "partially_received", "overdue"])
        c.execute("INSERT INTO open_pos VALUES (?,?,?,?,?,?,?,?)",
                  (po, sid, name, cat, amount, created.isoformat(), status, delivery.isoformat()))

    conn.commit()
    conn.close()
    print(f"  procurement.db: SQLite database with 4 tables")


def build_csv_exports():
    """Also write CSV versions for reference."""
    data_dir = PRACTICE / "data"

    rows = [{"supplier_id": s[0], "supplier_name": s[1], "category": s[2],
             "tier": s[3], "annual_spend_usd": s[4], "status": s[5]} for s in SUPPLIERS]
    with open(data_dir / "supplier-master.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"  supplier-master.csv: {len(rows)} rows (CSV reference)")


def main():
    print("Building Course 09 practice data...")
    print()

    (PRACTICE / "data").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "outputs").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "mcp-server").mkdir(parents=True, exist_ok=True)

    build_sqlite_db()
    build_csv_exports()

    print()
    print("Done. All files in practice/data/")


if __name__ == "__main__":
    main()
