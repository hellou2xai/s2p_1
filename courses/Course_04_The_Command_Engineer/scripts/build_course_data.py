"""Generate the practice data set for Course 4: The Command Engineer.

Scenario: Meridian Manufacturing, a US-based mid-market manufacturer.
The procurement operations team runs the same monthly analyses from
inconsistent prompts. Students build a slash command library so every
analysis runs from a single command with standardized inputs and outputs.

Produces a flat practice/ folder:
- data/ holds: spend-transactions.csv (~2,500 rows),
  supplier-master.csv (50 suppliers), contract-register.csv (30 contracts),
  scorecard-history.csv (200 rows: 50 suppliers x 4 quarters)
- .claude/commands/ is empty: the student fills it across the lessons
- outputs/ is empty: deliverables land here

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
YEAR_AGO = date(2025, 4, 26)


# ---------------------------------------------------------------------------
# Supplier master (50 suppliers)
# ---------------------------------------------------------------------------

CATEGORIES = {
    "direct-materials": [
        ("SUP001", "Great Lakes Steel", "Chicago", "IL", "strategic", "low", "net_45", 4200000),
        ("SUP002", "Heartland Polymers", "Houston", "TX", "strategic", "low", "net_45", 3800000),
        ("SUP003", "Pacific Aluminum", "Portland", "OR", "strategic", "low", "net_30", 3100000),
        ("SUP004", "Apex Electronics", "San Jose", "CA", "preferred", "high", "net_30", 2400000),
        ("SUP005", "Cascade Fasteners", "Seattle", "WA", "preferred", "low", "net_30", 1800000),
        ("SUP006", "Summit Metals", "Denver", "CO", "preferred", "medium", "net_30", 1600000),
        ("SUP007", "Liberty Composites", "Detroit", "MI", "approved", "low", "net_30", 1200000),
        ("SUP008", "Frontier Plastics", "Dallas", "TX", "approved", "low", "net_30", 980000),
        ("SUP009", "Harbor Wire", "Baltimore", "MD", "approved", "medium", "net_30", 760000),
        ("SUP010", "Keystone Coatings", "Pittsburgh", "PA", "spot", "medium", "net_15", 540000),
        ("SUP011", "Prairie Components", "Omaha", "NE", "approved", "low", "net_30", 680000),
        ("SUP012", "Redwood Rubber", "Sacramento", "CA", "approved", "low", "net_30", 520000),
        ("SUP013", "Pinnacle Alloys", "Cleveland", "OH", "preferred", "low", "net_45", 1400000),
    ],
    "logistics": [
        ("SUP014", "Continental Freight", "Memphis", "TN", "strategic", "low", "net_45", 2800000),
        ("SUP015", "Atlantic Carriers", "Atlanta", "GA", "strategic", "low", "net_45", 2200000),
        ("SUP016", "Midwest Express", "Indianapolis", "IN", "preferred", "low", "net_30", 1600000),
        ("SUP017", "Pacific Logistics", "Los Angeles", "CA", "preferred", "medium", "net_30", 1200000),
        ("SUP018", "Gulf Coast Shipping", "New Orleans", "LA", "approved", "low", "net_30", 880000),
        ("SUP019", "Mountain Transport", "Salt Lake City", "UT", "approved", "high", "net_30", 640000),
        ("SUP020", "Lakeshore Warehousing", "Milwaukee", "WI", "approved", "low", "net_30", 520000),
        ("SUP021", "Patriot Trucking", "Nashville", "TN", "spot", "medium", "net_15", 380000),
        ("SUP022", "Skybridge Air Cargo", "Louisville", "KY", "preferred", "low", "net_30", 960000),
        ("SUP023", "Harbor Drayage", "Newark", "NJ", "approved", "low", "net_30", 440000),
    ],
    "indirect": [
        ("SUP024", "Pinnacle Office Solutions", "New York", "NY", "preferred", "low", "net_30", 1400000),
        ("SUP025", "Bright Spark Energy", "Austin", "TX", "strategic", "low", "net_45", 2600000),
        ("SUP026", "Helix Consulting", "Boston", "MA", "preferred", "low", "net_30", 1800000),
        ("SUP027", "Apex Legal Partners", "Washington", "DC", "preferred", "low", "net_45", 1200000),
        ("SUP028", "Clearview IT Services", "Raleigh", "NC", "strategic", "low", "net_30", 2200000),
        ("SUP029", "Greenfield Facilities", "Charlotte", "NC", "preferred", "low", "net_30", 1600000),
        ("SUP030", "Nova Staffing", "Phoenix", "AZ", "approved", "medium", "net_30", 980000),
        ("SUP031", "Westside Catering", "San Francisco", "CA", "approved", "low", "net_15", 420000),
        ("SUP032", "Metro Print Services", "Philadelphia", "PA", "approved", "low", "net_30", 340000),
        ("SUP033", "Riverview Insurance", "Hartford", "CT", "preferred", "low", "net_45", 1100000),
        ("SUP034", "Cornerstone Training", "Minneapolis", "MN", "approved", "low", "net_30", 580000),
        ("SUP035", "Prism Marketing", "Miami", "FL", "spot", "low", "net_15", 460000),
    ],
    "mro": [
        ("SUP036", "Industrial Supply Co", "St. Louis", "MO", "strategic", "low", "net_30", 1800000),
        ("SUP037", "SafeGuard PPE", "Cincinnati", "OH", "preferred", "low", "net_30", 1200000),
        ("SUP038", "Precision Tools USA", "Grand Rapids", "MI", "preferred", "low", "net_30", 960000),
        ("SUP039", "Voltex Electrical", "Tampa", "FL", "preferred", "low", "net_30", 840000),
        ("SUP040", "AquaPure Filtration", "San Diego", "CA", "approved", "low", "net_30", 620000),
        ("SUP041", "ThermaFlow HVAC", "Kansas City", "MO", "approved", "medium", "net_30", 540000),
        ("SUP042", "BearingPoint Mechanical", "Columbus", "OH", "approved", "low", "net_30", 480000),
        ("SUP043", "FloorMaster Surfaces", "Oklahoma City", "OK", "spot", "low", "net_15", 360000),
        ("SUP044", "LubeMax Industrial", "Tulsa", "OK", "approved", "low", "net_30", 280000),
        ("SUP045", "ProWeld Gases", "Birmingham", "AL", "approved", "low", "net_30", 420000),
        ("SUP046", "Atlas Abrasives", "Buffalo", "NY", "approved", "low", "net_30", 340000),
        ("SUP047", "SignalFire Detection", "Albuquerque", "NM", "approved", "medium", "net_30", 520000),
        ("SUP048", "CoreShield Insulation", "Las Vegas", "NV", "spot", "high", "net_15", 280000),
        ("SUP049", "Ridgeline Hydraulics", "Boise", "ID", "approved", "low", "net_30", 380000),
        ("SUP050", "Beacon Calibration", "Portland", "ME", "approved", "low", "net_30", 320000),
    ],
}


def build_supplier_master():
    """Return flat list of supplier rows and a lookup dict."""
    rows = []
    lookup = {}
    contract_counter = 1
    for category, suppliers in CATEGORIES.items():
        for sup_id, name, city, state, tier, risk, terms, target in suppliers:
            # Most suppliers have a contract; spot suppliers do not
            if tier == "spot":
                contract_id = ""
            else:
                contract_id = f"CTR-{contract_counter:03d}"
                contract_counter += 1
            status = "active"
            if risk == "high":
                status = "at_risk"
            elif risk == "medium" and random.random() < 0.3:
                status = "under_review"
            rows.append((
                sup_id, name, category, tier, contract_id,
                risk, city, state, terms, target, status,
            ))
            lookup[sup_id] = {
                "name": name, "category": category, "tier": tier,
                "target": target, "contract_id": contract_id,
            }
    return rows, lookup


# ---------------------------------------------------------------------------
# Contract register (30 contracts)
# ---------------------------------------------------------------------------

def build_contract_register(supplier_rows):
    """Build contract register from suppliers that have a contract_id."""
    contracts = []
    for row in supplier_rows:
        sup_id, name, category, tier, ctr_id, risk, city, state, terms, target, status = row
        if not ctr_id:
            continue

        # Spread start dates across the last 3 years
        days_back = random.randint(180, 1095)
        start = TODAY - timedelta(days=days_back)

        # Contract lengths: 12, 24, or 36 months
        length_months = random.choice([12, 24, 36])
        end = date(
            start.year + (start.month + length_months - 1) // 12,
            (start.month + length_months - 1) % 12 + 1,
            min(start.day, 28),
        )

        auto_renew = random.choice(["yes", "no"])
        notice_days = random.choice([30, 60, 90])

        # Status based on end date
        if end < TODAY:
            ctr_status = "expired"
        elif end <= TODAY + timedelta(days=90):
            ctr_status = "expiring_soon"
        else:
            ctr_status = "active"

        annual_value = target
        total_value = int(annual_value * length_months / 12)

        title = f"{name} - {category.replace('-', ' ').title()} Agreement"

        contracts.append((
            ctr_id, sup_id, name, title,
            start.isoformat(), end.isoformat(),
            annual_value, total_value,
            auto_renew, notice_days, ctr_status,
        ))

    # Force some specific expiry scenarios for /contract-sweep exercises
    # Make 4 contracts expire within 90 days
    expiring_targets = [c for c in contracts if c[10] != "expiring_soon"]
    for i in range(min(4, len(expiring_targets))):
        c = list(expiring_targets[i])
        days_out = random.randint(10, 85)
        new_end = TODAY + timedelta(days=days_out)
        c[5] = new_end.isoformat()
        c[10] = "expiring_soon"
        idx = contracts.index(expiring_targets[i])
        contracts[idx] = tuple(c)

    # Make 2 contracts already expired but listed
    expired_targets = [c for c in contracts if c[10] == "active"]
    for i in range(min(2, len(expired_targets))):
        c = list(expired_targets[i])
        days_past = random.randint(15, 60)
        new_end = TODAY - timedelta(days=days_past)
        c[5] = new_end.isoformat()
        c[10] = "expired"
        idx = contracts.index(expired_targets[i])
        contracts[idx] = tuple(c)

    return contracts


# ---------------------------------------------------------------------------
# Spend transactions (2,500 rows)
# ---------------------------------------------------------------------------

SUBCATEGORIES = {
    "direct-materials": [
        "raw steel", "polymers", "aluminum sheet", "electronic components",
        "fasteners", "specialty metals", "composite panels", "plastic resin",
        "wire harness", "coatings", "machined parts", "rubber seals",
    ],
    "logistics": [
        "FTL domestic", "LTL domestic", "ocean freight", "air freight",
        "warehousing", "drayage", "last mile", "expedited",
    ],
    "indirect": [
        "office supplies", "energy", "consulting", "legal services",
        "IT services", "facilities maintenance", "temp staffing",
        "catering", "print services", "insurance", "training", "marketing",
    ],
    "mro": [
        "industrial supplies", "PPE", "cutting tools", "electrical",
        "filtration", "HVAC parts", "bearings", "flooring",
        "lubricants", "welding gases", "abrasives", "fire detection",
        "insulation", "hydraulic parts", "calibration services",
    ],
}

COST_CENTERS = ["CC100", "CC200", "CC300", "CC400", "CC500"]
DEPARTMENTS = ["Manufacturing", "Operations", "Engineering", "Quality", "Admin"]


def gen_spend_transactions(supplier_lookup, n=2500):
    """Generate spend transactions with planted anomalies."""
    rows = []
    all_suppliers = list(supplier_lookup.keys())
    days_total = (TODAY - YEAR_AGO).days

    # Build category-level average amounts for anomaly detection
    category_avg = {
        "direct-materials": (8000, 45000),
        "logistics": (3000, 25000),
        "indirect": (1500, 18000),
        "mro": (500, 8000),
    }

    for i in range(n):
        sup_id = random.choice(all_suppliers)
        info = supplier_lookup[sup_id]
        category = info["category"]

        lo, hi = category_avg[category]
        amount = round(random.uniform(lo, hi), 2)

        # Plant anomalies: 15 transactions with amounts >3x category average
        if i < 15:
            amount = round(random.uniform(hi * 2.5, hi * 4.0), 2)

        subcategory = random.choice(SUBCATEGORIES[category])
        txn_date = YEAR_AGO + timedelta(days=random.randint(0, days_total))

        # Create seasonal pattern: Q3 direct-materials gets a 22% bump
        if category == "direct-materials" and 7 <= txn_date.month <= 9:
            amount = round(amount * 1.22, 2)

        po_number = f"PO-{random.randint(100000, 999999)}"
        cost_center = random.choice(COST_CENTERS)
        department = random.choice(DEPARTMENTS)
        terms = "net_30"  # default; overridden below
        for cat_sups in CATEGORIES.values():
            for s in cat_sups:
                if s[0] == sup_id:
                    terms = s[6]
                    break

        invoice_status = random.choices(
            ["paid", "pending", "overdue"],
            weights=[75, 20, 5],
            k=1,
        )[0]

        txn_id = f"TXN-{i + 1:05d}"
        desc = f"{subcategory} - {info['name']}"

        rows.append((
            txn_id, txn_date.isoformat(), sup_id, info["name"],
            category, subcategory, desc, amount,
            po_number, cost_center, department, terms, invoice_status,
        ))

    # Plant 8 duplicate PO patterns (same PO number, different dates)
    for j in range(8):
        src = rows[random.randint(100, n - 1)]
        dup_date = (
            date.fromisoformat(src[1]) + timedelta(days=random.randint(1, 5))
        ).isoformat()
        dup_amount = round(float(src[7]) * random.uniform(0.95, 1.05), 2)
        dup_id = f"TXN-{n + j + 1:05d}"
        dup_row = (
            dup_id, dup_date, src[2], src[3], src[4], src[5],
            src[6], dup_amount, src[8],  # same PO number
            src[9], src[10], src[11], src[12],
        )
        rows.append(dup_row)

    rows.sort(key=lambda r: r[1])
    return rows


# ---------------------------------------------------------------------------
# Scorecard history (50 suppliers x 4 quarters)
# ---------------------------------------------------------------------------

QUARTERS = ["2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2"]


def gen_scorecard_history(supplier_rows):
    """Generate quarterly scorecard data. Plant 3 declining and 2 improving."""
    rows = []
    declining = ["SUP004", "SUP019", "SUP048"]  # at_risk or high-risk suppliers
    improving = ["SUP007", "SUP011"]

    for sup_row in supplier_rows:
        sup_id = sup_row[0]
        name = sup_row[1]

        for qi, quarter in enumerate(QUARTERS):
            base_quality = random.randint(72, 96)
            base_delivery = random.randint(70, 98)
            base_responsive = random.randint(68, 95)
            base_cost = random.randint(65, 94)
            base_innovation = random.randint(60, 90)

            if sup_id in declining:
                # Each quarter drops 4-8 points
                drop = qi * random.randint(4, 8)
                base_quality = max(40, base_quality - drop)
                base_delivery = max(35, base_delivery - drop)
                base_responsive = max(38, base_responsive - drop)
                base_cost = max(42, base_cost - drop)
                base_innovation = max(30, base_innovation - drop)

            if sup_id in improving:
                # Each quarter gains 3-6 points
                gain = qi * random.randint(3, 6)
                base_quality = min(100, base_quality + gain)
                base_delivery = min(100, base_delivery + gain)
                base_responsive = min(100, base_responsive + gain)
                base_cost = min(100, base_cost + gain)
                base_innovation = min(100, base_innovation + gain)

            overall = round(
                base_quality * 0.25
                + base_delivery * 0.25
                + base_responsive * 0.20
                + base_cost * 0.20
                + base_innovation * 0.10,
                1,
            )

            rows.append((
                sup_id, name, quarter,
                base_quality, base_delivery, base_responsive,
                base_cost, base_innovation, overall,
            ))

    return rows


# ---------------------------------------------------------------------------
# Starter CLAUDE.md
# ---------------------------------------------------------------------------

STARTER_CLAUDE_MD = """# Meridian Manufacturing - Procurement Operations

## Who I am

I am a Procurement Operations Lead at Meridian Manufacturing, a US-based
mid-market manufacturer. I manage recurring procurement analyses across four
categories: direct materials, logistics, indirect, and MRO. Annual
procurement spend is approximately 48m USD across 50 active suppliers.

## Folder layout

data/              source data files (read-only, do not modify)
.claude/commands/  custom slash commands (you build these across the lessons)
outputs/           analysis outputs land here, datestamped

## Folder rules

The CSV files in data/ are the source of truth.
Read them when asked. Do not modify them.
Save all outputs to outputs/ with a datestamp in the file name.
The commands in .claude/commands/ are reusable. They work with $ARGUMENTS
so the same command runs for any period, category, or supplier.

## Writing rules

American English. USD for all currency.
Oxford commas. No em-dashes. Active voice.
Specific numbers, never "significant" or "material" for figures.
Cap tables at 15 rows unless the command says otherwise.
Every output ends with an audit footer: date, source files, model, operator.

## Data files

data/spend-transactions.csv
  ~2,500 transaction rows over the last 12 months.
  Columns: transaction_id, date, supplier_id, supplier_name, category,
  subcategory, description, amount_usd, po_number, cost_center,
  department, payment_terms, invoice_status.

data/supplier-master.csv
  50 suppliers across 4 categories.
  Columns: supplier_id, supplier_name, category, tier, contract_id,
  risk_rating, city, state, payment_terms, annual_target_usd, status.

data/contract-register.csv
  30 active contracts.
  Columns: contract_id, supplier_id, supplier_name, title, start_date,
  end_date, annual_value_usd, total_value_usd, auto_renew,
  notice_period_days, status.

data/scorecard-history.csv
  200 rows: 50 suppliers x 4 quarters.
  Columns: supplier_id, supplier_name, quarter, quality_score,
  delivery_score, responsiveness_score, cost_score, innovation_score,
  overall_score.
"""


# ---------------------------------------------------------------------------
# Write helpers
# ---------------------------------------------------------------------------

def write_csv(path: Path, header: list, rows: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    PRACTICE.mkdir(parents=True, exist_ok=True)

    # CLAUDE.md
    (PRACTICE / "CLAUDE.md").write_text(
        STARTER_CLAUDE_MD.strip() + "\n", encoding="utf-8"
    )

    # Supplier master
    supplier_rows, supplier_lookup = build_supplier_master()
    data_dir = PRACTICE / "data"
    data_dir.mkdir(exist_ok=True)
    write_csv(
        data_dir / "supplier-master.csv",
        [
            "supplier_id", "supplier_name", "category", "tier",
            "contract_id", "risk_rating", "city", "state",
            "payment_terms", "annual_target_usd", "status",
        ],
        supplier_rows,
    )

    # Contract register
    contract_rows = build_contract_register(supplier_rows)
    write_csv(
        data_dir / "contract-register.csv",
        [
            "contract_id", "supplier_id", "supplier_name", "title",
            "start_date", "end_date", "annual_value_usd", "total_value_usd",
            "auto_renew", "notice_period_days", "status",
        ],
        contract_rows,
    )

    # Spend transactions
    spend_rows = gen_spend_transactions(supplier_lookup, 2500)
    write_csv(
        data_dir / "spend-transactions.csv",
        [
            "transaction_id", "date", "supplier_id", "supplier_name",
            "category", "subcategory", "description", "amount_usd",
            "po_number", "cost_center", "department", "payment_terms",
            "invoice_status",
        ],
        spend_rows,
    )

    # Scorecard history
    scorecard_rows = gen_scorecard_history(supplier_rows)
    write_csv(
        data_dir / "scorecard-history.csv",
        [
            "supplier_id", "supplier_name", "quarter",
            "quality_score", "delivery_score", "responsiveness_score",
            "cost_score", "innovation_score", "overall_score",
        ],
        scorecard_rows,
    )

    # Commands folder (empty; student fills in)
    commands_dir = PRACTICE / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    (commands_dir / "README.md").write_text(
        "# Your command library\n\n"
        "You will fill this folder across Lessons 1 to 5.\n"
        "Each command is a markdown file with a $ARGUMENTS placeholder.\n\n"
        "By the end of the course you will have:\n"
        "- spend-analyze.md\n"
        "- anomaly-detect.md\n"
        "- scorecard-refresh.md\n"
        "- contract-sweep.md\n"
        "- rfp-launch.md\n"
        "- savings-update.md\n",
        encoding="utf-8",
    )

    # Outputs folder (empty)
    outputs_dir = PRACTICE / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    (outputs_dir / "README.md").write_text(
        "# Outputs\n\n"
        "Analysis files produced by your slash commands land here.\n"
        "Each file is datestamped so you can compare runs over time.\n",
        encoding="utf-8",
    )

    # Print summary
    print("Wrote practice/ folder under Course_04_The_Command_Engineer/")
    print(f"  practice/CLAUDE.md (project context)")
    print(f"  practice/data/")
    print(f"    supplier-master.csv ({len(supplier_rows)} suppliers)")
    print(f"    contract-register.csv ({len(contract_rows)} contracts)")
    print(f"    spend-transactions.csv ({len(spend_rows)} transactions)")
    print(f"    scorecard-history.csv ({len(scorecard_rows)} scorecard rows)")
    print(f"  practice/.claude/commands/ (empty; student fills)")
    print(f"  practice/outputs/ (empty; analysis outputs)")


if __name__ == "__main__":
    main()
