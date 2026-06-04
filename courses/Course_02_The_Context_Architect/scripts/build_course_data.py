"""Generate realistic procurement data for Course 2: The Context Architect.

Produces a flat practice/ folder with three category subfolders. Each
category has its own CLAUDE.md plus two CSVs (a master file and an
activity file). No further nesting.

Activity files have thousands of rows so the student gets a real-world
feel for what Claude does over a year of POs, shipments, or invoices.
Master files stay small (50, 20, or 80 entries) so they remain readable.

Deterministic via random.seed(42); regenerating produces identical files.
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
# Starter CLAUDE.md files
# ---------------------------------------------------------------------------

STARTER_GLOBAL = """# My procurement work

I work in procurement.

Help me with sourcing tasks.
"""

STARTER_CATEGORY = "# {name}\n\n(Empty for now. You will fill this in during Lesson 3.)\n"


# ---------------------------------------------------------------------------
# Direct materials master (50 suppliers)
# ---------------------------------------------------------------------------

DIRECT_SUPPLIERS = [
    # supplier_id, name, state, makes, annual_value_usd, contract_end, status
    ("SUP001", "Great Lakes Steel", "Michigan", "steel", 2_400_000, "2026-12-31", "active"),
    ("SUP002", "Pacific Aluminum", "California", "aluminum", 1_800_000, "2026-09-30", "active"),
    ("SUP003", "Lone Star Plastics", "Texas", "plastics", 950_000, "2027-03-31", "active"),
    ("SUP004", "Apex Electronics", "California", "chips", 1_200_000, "2026-05-31", "at_risk"),
    ("SUP005", "Midwest Castings", "Ohio", "castings", 600_000, "2027-01-31", "active"),
    ("SUP006", "Gulf Coast Polymers", "Louisiana", "plastics", 720_000, "2026-08-31", "active"),
    ("SUP007", "Keystone Stamping", "Pennsylvania", "stamped parts", 1_200_000, "2026-05-31", "active"),
    ("SUP008", "Buckeye Tools", "Ohio", "machined parts", 540_000, "2027-01-31", "active"),
    ("SUP009", "Silicon Valley Components", "California", "passive electronics", 870_000, "2026-10-31", "active"),
    ("SUP010", "Cascade Aluminum", "Washington", "aluminum castings", 460_000, "2026-07-31", "active"),
    ("SUP011", "Heartland Steel", "Indiana", "steel", 1_850_000, "2027-04-30", "active"),
    ("SUP012", "Sunbelt Polymers", "Florida", "plastics", 640_000, "2026-06-30", "active"),
    ("SUP013", "Carolina Forge", "North Carolina", "steel forgings", 980_000, "2027-02-28", "active"),
    ("SUP014", "Foundry Row Castings", "Alabama", "iron castings", 410_000, "2026-11-30", "active"),
    ("SUP015", "Boise Chips", "Idaho", "memory chips", 680_000, "2026-09-30", "active"),
    ("SUP016", "Motor City Bearings", "Michigan", "bearings", 380_000, "2027-03-31", "active"),
    ("SUP017", "Jersey Resins", "New Jersey", "plastic resins", 760_000, "2026-12-31", "active"),
    ("SUP018", "New England Castings", "Connecticut", "castings", 290_000, "2027-02-28", "active"),
    ("SUP019", "Desert Metals", "Arizona", "non-ferrous metals", 520_000, "2026-08-31", "active"),
    ("SUP020", "Badger Springs", "Wisconsin", "springs and clips", 340_000, "2027-01-31", "active"),
    ("SUP021", "Rust Belt Press Works", "Pennsylvania", "stamped parts", 720_000, "2026-10-31", "active"),
    ("SUP022", "Magnolia Plastics", "Mississippi", "plastics", 580_000, "2027-04-30", "active"),
    ("SUP023", "Rocky Mountain Composites", "Colorado", "composites", 880_000, "2026-09-30", "active"),
    ("SUP024", "Peach State Aluminum", "Georgia", "aluminum parts", 460_000, "2027-03-31", "active"),
    ("SUP025", "Prairie Vac Forming", "Nebraska", "vacuum-formed parts", 320_000, "2026-11-30", "active"),
    ("SUP026", "Puget Sound Gearworks", "Washington", "gears", 510_000, "2026-12-31", "active"),
    ("SUP027", "Dixie Galvanizing", "Tennessee", "coated steel", 690_000, "2027-02-28", "active"),
    ("SUP028", "Garden State Anodizing", "New Jersey", "surface treatment", 240_000, "2026-08-31", "active"),
    ("SUP029", "Austin Microchip", "Texas", "chips", 1_080_000, "2026-11-30", "active"),
    ("SUP030", "Evergreen Polymers", "Oregon", "plastics", 380_000, "2027-01-31", "active"),
    ("SUP031", "Pittsburgh Steels", "Pennsylvania", "steel", 1_640_000, "2026-12-31", "active"),
    ("SUP032", "Bayou Hardware", "Louisiana", "fasteners", 290_000, "2027-04-30", "active"),
    ("SUP033", "Appalachian Castings", "West Virginia", "castings", 350_000, "2026-09-30", "active"),
    ("SUP034", "Gateway Components", "Missouri", "machined components", 470_000, "2026-10-31", "active"),
    ("SUP035", "Golden State Precision", "California", "precision parts", 1_320_000, "2027-03-31", "active"),
    ("SUP036", "Ozark Wireforms", "Arkansas", "wireforms", 220_000, "2026-08-31", "active"),
    ("SUP037", "Bluegrass Plastics", "Kentucky", "plastics", 380_000, "2027-02-28", "active"),
    ("SUP038", "Research Triangle Electronics", "North Carolina", "PCB assemblies", 920_000, "2026-12-31", "active"),
    ("SUP039", "Granite State Castings", "New Hampshire", "castings", 180_000, "2026-11-30", "active"),
    ("SUP040", "Copper State Light Metals", "Arizona", "aluminum", 420_000, "2027-01-31", "active"),
    ("SUP041", "Chesapeake Composites", "Maryland", "composites", 760_000, "2026-09-30", "active"),
    ("SUP042", "Hoosier Machining", "Indiana", "machined parts", 640_000, "2027-04-30", "active"),
    ("SUP043", "Bay State Moldings", "Massachusetts", "plastic moldings", 540_000, "2026-10-31", "active"),
    ("SUP044", "Allegheny Forge", "Pennsylvania", "forgings", 1_120_000, "2026-12-31", "active"),
    ("SUP045", "Rio Grande Bearings", "New Mexico", "bearings", 290_000, "2027-03-31", "active"),
    ("SUP046", "Empire Diecasting", "New York", "diecasting", 320_000, "2026-08-31", "active"),
    ("SUP047", "Bayou Plastics", "Louisiana", "plastics", 480_000, "2027-02-28", "active"),
    ("SUP048", "Tar Heel Steel", "North Carolina", "steel", 1_280_000, "2026-11-30", "active"),
    ("SUP049", "Centennial Brass", "Colorado", "brass parts", 360_000, "2026-09-30", "active"),
    ("SUP050", "Palmetto Polymers", "South Carolina", "plastics", 410_000, "2027-04-30", "active"),
]

# Item templates per "makes" string. unit_price ranges keep totals plausible.
DIRECT_ITEM_TEMPLATES = {
    "steel": [("steel sheets", 850, 1_200), ("steel coil", 950, 1_400), ("steel plate", 700, 1_100)],
    "aluminum": [("aluminum profile", 60, 120), ("aluminum sheet", 80, 160)],
    "aluminum parts": [("aluminum bracket", 30, 80), ("aluminum housing", 50, 140)],
    "aluminum castings": [("aluminum casting body", 70, 200), ("aluminum gear housing", 100, 280)],
    "non-ferrous metals": [("brass sheet", 90, 180), ("copper bar", 200, 420)],
    "plastics": [("plastic resin", 1.4, 2.6), ("plastic pellets", 1.1, 2.0)],
    "plastic resins": [("polypropylene resin", 1.5, 2.2), ("ABS resin", 1.8, 2.6)],
    "plastic moldings": [("molded part A", 4, 14), ("molded part B", 6, 18)],
    "chips": [("chip A", 7, 11), ("chip B", 9, 14), ("chip C", 12, 22)],
    "memory chips": [("memory chip 8GB", 14, 22)],
    "passive electronics": [("capacitor pack", 0.15, 0.32), ("resistor pack", 0.08, 0.20)],
    "PCB assemblies": [("PCB assembly type A", 80, 180), ("PCB assembly type B", 120, 240)],
    "castings": [("casting body", 140, 220), ("casting bracket", 90, 160)],
    "iron castings": [("iron casting body", 160, 240), ("iron casting bracket", 110, 180)],
    "diecasting": [("diecast housing", 60, 130), ("diecast bracket", 40, 90)],
    "stamped parts": [("stamped bracket", 14, 28), ("stamped clip", 6, 14)],
    "machined parts": [("machined bracket", 28, 60), ("machined housing", 70, 160)],
    "machined components": [("machined component A", 30, 70), ("machined component B", 60, 140)],
    "precision parts": [("precision shaft", 80, 180), ("precision sleeve", 50, 120)],
    "forgings": [("forged hub", 120, 280), ("forged shaft", 90, 220)],
    "steel forgings": [("forged steel hub", 160, 320), ("forged steel arm", 140, 280)],
    "composites": [("composite panel", 220, 480), ("composite tube", 180, 380)],
    "bearings": [("bearing 6204", 8, 18), ("bearing 6206", 12, 26)],
    "vacuum-formed parts": [("vac-formed tray", 14, 32), ("vac-formed housing", 18, 42)],
    "gears": [("gear set A", 80, 180), ("gear set B", 110, 240)],
    "coated steel": [("galvanized steel sheet", 1_050, 1_450), ("powder-coated steel coil", 1_180, 1_600)],
    "surface treatment": [("anodizing service batch", 320, 720)],
    "fasteners": [("M8 bolt pack", 0.4, 0.9), ("M10 nut pack", 0.3, 0.8)],
    "springs and clips": [("compression spring 25mm", 0.6, 1.4), ("circlip 12mm", 0.12, 0.30)],
    "wireforms": [("wireform clip", 0.8, 2.2), ("wireform handle", 1.4, 3.6)],
    "brass parts": [("brass connector", 12, 28), ("brass valve body", 38, 90)],
}


def gen_direct_orders(n: int = 2500):
    rows = []
    days_total = (TODAY - YEAR_AGO).days
    for i in range(n):
        sup = random.choices(
            DIRECT_SUPPLIERS,
            # weight by annual_value_usd so bigger suppliers get more orders
            weights=[s[4] for s in DIRECT_SUPPLIERS],
            k=1,
        )[0]
        sup_id, _, _, makes, _, _, _ = sup
        templates = DIRECT_ITEM_TEMPLATES.get(makes, [("part", 50, 200)])
        item, lo, hi = random.choice(templates)
        units = random.randint(50, 1500)
        unit_price = round(random.uniform(lo, hi), 2)
        total = round(units * unit_price, 2)
        po_date = YEAR_AGO + timedelta(days=random.randint(0, days_total))
        po_num = f"PO-DM-{i + 1:05d}"
        rows.append((po_num, sup_id, item, units, total, po_date.isoformat()))
    rows.sort(key=lambda r: r[5])
    return rows


# ---------------------------------------------------------------------------
# Logistics master (20 carriers)
# ---------------------------------------------------------------------------

LOGISTICS_CARRIERS = [
    ("CAR001", "Interstate Freight", "road", 1_500_000, "2027-01-31", "active"),
    ("CAR002", "Pacific Shipping", "sea", 900_000, "2026-12-31", "active"),
    ("CAR003", "SkyBridge Air", "air", 700_000, "2026-08-31", "active"),
    ("CAR004", "ParcelPlus", "parcel", 350_000, "2026-06-30", "at_risk"),
    ("CAR005", "Heartland Express", "road", 1_200_000, "2026-09-30", "active"),
    ("CAR006", "Atlantic Lines", "sea", 1_650_000, "2027-03-31", "active"),
    ("CAR007", "Eagle Air Freight", "air", 1_080_000, "2026-10-31", "active"),
    ("CAR008", "Glacier Cold Chain", "road", 760_000, "2027-02-28", "active"),
    ("CAR009", "Transpacific Forwarders", "sea", 1_240_000, "2026-12-31", "active"),
    ("CAR010", "Midwest Express Pallets", "road", 360_000, "2026-07-31", "active"),
    ("CAR011", "Gulf Container", "sea", 520_000, "2026-06-30", "active"),
    ("CAR012", "Northern Drayage", "road", 420_000, "2026-11-30", "active"),
    ("CAR013", "Globex Freight", "road", 3_200_000, "2026-12-31", "active"),
    ("CAR014", "Southern Seas Marine", "sea", 680_000, "2027-01-31", "active"),
    ("CAR015", "Continental Air Cargo", "air", 540_000, "2026-09-30", "active"),
    ("CAR016", "Prairie Pallets", "road", 280_000, "2027-04-30", "active"),
    ("CAR017", "Great Lakes Shipping", "sea", 740_000, "2026-08-31", "active"),
    ("CAR018", "QuickShip Parcel", "parcel", 460_000, "2027-02-28", "active"),
    ("CAR019", "Summit Air", "air", 880_000, "2026-11-30", "active"),
    ("CAR020", "CrossCountry Roads", "road", 1_080_000, "2027-03-31", "active"),
]

LOGISTICS_LANES = {
    "road": [
        ("Chicago", "Detroit", 280, (2400, 3400)),
        ("Chicago", "Houston", 1090, (2200, 3200)),
        ("Dallas", "Atlanta", 780, (2100, 3000)),
        ("Los Angeles", "Phoenix", 370, (2800, 3800)),
        ("Seattle", "Portland", 175, (3400, 4400)),
        ("Denver", "Salt Lake City", 525, (3600, 4600)),
        ("Chicago", "Indianapolis", 180, (1800, 2600)),
        ("Chicago", "Milwaukee", 90, (1100, 1800)),
        ("Dallas", "San Antonio", 275, (2000, 2900)),
        ("Detroit", "Cleveland", 170, (300, 600)),
    ],
    "sea": [
        ("Long Beach", "Shanghai", 6500, (3000, 3500)),
        ("Long Beach", "Singapore", 8500, (2800, 3300)),
        ("Savannah", "Rotterdam", 4500, (1300, 1800)),
        ("Long Beach", "Hong Kong", 7200, (3100, 3600)),
        ("Newark", "Hamburg", 3800, (2400, 2900)),
    ],
    "air": [
        ("O'Hare", "Dallas-Fort Worth", 800, (4400, 5200)),
        ("JFK", "Los Angeles", 2500, (6800, 7800)),
        ("JFK", "Singapore", 9500, (8800, 10200)),
        ("JFK", "Dubai", 6800, (5400, 6400)),
    ],
    "parcel": [
        ("Multiple US", "Multiple US", 0, (10000, 16000)),
    ],
}


def gen_logistics_shipments(n: int = 5000):
    rows = []
    days_total = (TODAY - YEAR_AGO).days
    for i in range(n):
        car = random.choices(
            LOGISTICS_CARRIERS,
            weights=[c[3] for c in LOGISTICS_CARRIERS],
            k=1,
        )[0]
        car_id, _, mode, _, _, _ = car
        lane = random.choice(LOGISTICS_LANES[mode])
        origin, dest, _, (lo, hi) = lane
        total = round(random.uniform(lo, hi), 2)
        ship_date = YEAR_AGO + timedelta(days=random.randint(0, days_total))
        ship_id = f"SH-LOG-{i + 1:05d}"
        rows.append((ship_id, car_id, origin, dest, total, ship_date.isoformat()))
    rows.sort(key=lambda r: r[5])
    return rows


# ---------------------------------------------------------------------------
# Indirect master (80 vendors)
# ---------------------------------------------------------------------------

INDIRECT_VENDORS = [
    ("VEN001", "Northwind Office", "office supplies", 240_000, "2026-09-30", "active"),
    ("VEN002", "CodeCraft Software", "software licenses", 320_000, "2026-12-31", "active"),
    ("VEN003", "Vista Marketing", "marketing services", 480_000, "2026-08-31", "active"),
    ("VEN004", "Apex Legal", "legal advisory", 650_000, "2026-11-30", "active"),
    ("VEN005", "Prism Print", "managed print", 140_000, "2026-05-31", "at_risk"),
    ("VEN006", "Helix Consulting", "strategy consulting", 1_200_000, "2026-08-31", "active"),
    ("VEN007", "Patriot MRO", "industrial consumables", 260_000, "2026-10-31", "active"),
    ("VEN008", "Liberty Telecom", "telecoms", 440_000, "2027-01-31", "active"),
    ("VEN009", "Premier Travel", "corporate travel", 380_000, "2026-12-31", "active"),
    ("VEN010", "Aurora Cloud", "cloud hosting", 640_000, "2027-04-30", "active"),
    ("VEN011", "Insight Research", "market research", 180_000, "2026-07-31", "active"),
    ("VEN012", "Steadfast Insurance", "insurance broking", 340_000, "2027-03-31", "active"),
    ("VEN013", "Beacon Audit", "audit and tax", 560_000, "2026-11-30", "active"),
    ("VEN014", "Highline Cleaning", "cleaning services", 160_000, "2026-08-31", "active"),
    ("VEN015", "Eagle Fleet Lease", "fleet lease", 580_000, "2027-06-30", "active"),
    ("VEN016", "Bright Spark Energy", "utilities", 720_000, "2027-02-28", "active"),
    ("VEN017", "Pinnacle Translations", "translation services", 120_000, "2026-09-30", "active"),
    ("VEN018", "Zenith Recruiters", "recruitment", 460_000, "2026-12-31", "active"),
    ("VEN019", "Sentinel Security", "security services", 320_000, "2027-01-31", "active"),
    ("VEN020", "Atlas Catering", "catering", 240_000, "2026-08-31", "active"),
    ("VEN021", "Pinnacle Training", "training services", 220_000, "2026-10-31", "active"),
    ("VEN022", "Vertex Legal", "legal advisory", 380_000, "2027-04-30", "active"),
    ("VEN023", "Arctic IT Support", "IT support", 280_000, "2026-09-30", "active"),
    ("VEN024", "Boreal Marketing", "marketing services", 340_000, "2027-03-31", "active"),
    ("VEN025", "Federal Stationers", "office supplies", 90_000, "2026-07-31", "active"),
    ("VEN026", "TitanWeb Hosting", "cloud hosting", 420_000, "2026-12-31", "active"),
    ("VEN027", "Compass Travel", "corporate travel", 240_000, "2027-02-28", "active"),
    ("VEN028", "Ironside Consultants", "strategy consulting", 580_000, "2027-01-31", "active"),
    ("VEN029", "Phoenix HR Advisory", "HR advisory", 240_000, "2026-08-31", "active"),
    ("VEN030", "Nimbus Cloud", "cloud hosting", 380_000, "2026-10-31", "active"),
    ("VEN031", "Cinder Print", "managed print", 110_000, "2026-09-30", "active"),
    ("VEN032", "Vanguard Software", "software licenses", 540_000, "2027-04-30", "active"),
    ("VEN033", "Alpine Audit", "audit and tax", 320_000, "2026-12-31", "active"),
    ("VEN034", "Sterling Legal", "legal advisory", 410_000, "2027-03-31", "active"),
    ("VEN035", "Velocity Couriers", "couriers", 180_000, "2026-08-31", "active"),
    ("VEN036", "Rampart Security", "security services", 220_000, "2026-11-30", "active"),
    ("VEN037", "Crystal Catering", "catering", 140_000, "2026-09-30", "active"),
    ("VEN038", "Solstice Marketing", "marketing services", 280_000, "2027-02-28", "active"),
    ("VEN039", "Iron Forge Training", "training services", 160_000, "2026-10-31", "active"),
    ("VEN040", "Beacon HR", "HR advisory", 210_000, "2027-04-30", "active"),
    ("VEN041", "Linnet Translations", "translation services", 90_000, "2026-08-31", "active"),
    ("VEN042", "Argyle Audit", "audit and tax", 380_000, "2026-12-31", "active"),
    ("VEN043", "Equinox Energy", "utilities", 420_000, "2026-11-30", "active"),
    ("VEN044", "Pioneer Print", "managed print", 130_000, "2026-09-30", "active"),
    ("VEN045", "Quartz Software", "software licenses", 280_000, "2027-01-31", "active"),
    ("VEN046", "Frontier Legal", "legal advisory", 460_000, "2027-04-30", "active"),
    ("VEN047", "Hartford Insurance", "insurance broking", 240_000, "2026-12-31", "active"),
    ("VEN048", "Polar Cleaning", "cleaning services", 110_000, "2026-08-31", "active"),
    ("VEN049", "Beacon Travel", "corporate travel", 180_000, "2027-02-28", "active"),
    ("VEN050", "Moss MRO", "industrial consumables", 220_000, "2026-10-31", "active"),
    ("VEN051", "Rapid Recruiters", "recruitment", 320_000, "2026-09-30", "active"),
    ("VEN052", "Mariner IT", "IT support", 240_000, "2027-03-31", "active"),
    ("VEN053", "Falcon Couriers", "couriers", 140_000, "2026-08-31", "active"),
    ("VEN054", "Cascade Marketing", "marketing services", 380_000, "2026-12-31", "active"),
    ("VEN055", "Avalon Catering", "catering", 110_000, "2027-01-31", "active"),
    ("VEN056", "Ridgeline Training", "training services", 180_000, "2027-02-28", "active"),
    ("VEN057", "Northern Light Marketing", "marketing services", 240_000, "2026-11-30", "active"),
    ("VEN058", "Turret Security", "security services", 160_000, "2026-08-31", "active"),
    ("VEN059", "Sunset Travel", "corporate travel", 210_000, "2027-04-30", "active"),
    ("VEN060", "Granite Legal", "legal advisory", 380_000, "2026-09-30", "active"),
    ("VEN061", "Ember Software", "software licenses", 240_000, "2026-12-31", "active"),
    ("VEN062", "Birch HR", "HR advisory", 180_000, "2027-01-31", "active"),
    ("VEN063", "Comet Cloud", "cloud hosting", 320_000, "2026-10-31", "active"),
    ("VEN064", "Pelican Print", "managed print", 90_000, "2026-08-31", "active"),
    ("VEN065", "Otter Office Supplies", "office supplies", 110_000, "2027-03-31", "active"),
    ("VEN066", "Dolphin Couriers", "couriers", 130_000, "2026-09-30", "active"),
    ("VEN067", "Forge Insurance", "insurance broking", 200_000, "2026-12-31", "active"),
    ("VEN068", "Kettle MRO", "industrial consumables", 160_000, "2027-04-30", "active"),
    ("VEN069", "Lumen Audit", "audit and tax", 260_000, "2026-11-30", "active"),
    ("VEN070", "Maple Recruiters", "recruitment", 220_000, "2026-08-31", "active"),
    ("VEN071", "Ocean IT", "IT support", 180_000, "2027-02-28", "active"),
    ("VEN072", "Pebble Marketing", "marketing services", 240_000, "2026-12-31", "active"),
    ("VEN073", "Quill Catering", "catering", 90_000, "2026-09-30", "active"),
    ("VEN074", "River Cleaning", "cleaning services", 120_000, "2027-01-31", "active"),
    ("VEN075", "Spruce Training", "training services", 150_000, "2026-08-31", "active"),
    ("VEN076", "Tundra Energy", "utilities", 380_000, "2027-03-31", "active"),
    ("VEN077", "Umber Travel", "corporate travel", 160_000, "2026-10-31", "active"),
    ("VEN078", "Vector Legal", "legal advisory", 320_000, "2026-09-30", "active"),
    ("VEN079", "Willow Software", "software licenses", 280_000, "2027-04-30", "active"),
    ("VEN080", "Yarrow HR", "HR advisory", 140_000, "2026-12-31", "active"),
]

THRESHOLD = 25_000


def gen_indirect_invoices(n: int = 3000):
    rows = []
    days_total = (TODAY - YEAR_AGO).days
    violations_so_far = 0
    target_violations = 18  # ~0.6% of all invoices, realistic
    for i in range(n):
        ven = random.choices(
            INDIRECT_VENDORS,
            weights=[v[3] for v in INDIRECT_VENDORS],
            k=1,
        )[0]
        ven_id, _, what, annual, _, _ = ven
        # rough monthly invoice = annual / 12, varied a bit
        base = annual / 12
        amount = round(random.uniform(base * 0.4, base * 1.3), 2)
        invoice_date = YEAR_AGO + timedelta(days=random.randint(0, days_total))
        invoice_num = f"INV-2026-{i + 1:05d}"
        # decide approval path
        is_violation = False
        if amount >= THRESHOLD and violations_so_far < target_violations and random.random() < 0.04:
            # leave the manager path on a > threshold invoice = violation
            path = "manager_under_25k"
            is_violation = True
            violations_so_far += 1
        elif amount >= THRESHOLD:
            path = "cfo_over_25k"
        else:
            path = "manager_under_25k"
        rows.append((invoice_num, ven_id, what, amount, invoice_date.isoformat(), path))
    rows.sort(key=lambda r: r[4])
    return rows, violations_so_far


# ---------------------------------------------------------------------------
# Write everything
# ---------------------------------------------------------------------------

def write_csv(path: Path, header: list, rows: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    PRACTICE.mkdir(parents=True, exist_ok=True)

    # Global starter
    (PRACTICE / "CLAUDE.md").write_text(STARTER_GLOBAL, encoding="utf-8")

    # Direct materials
    dm = PRACTICE / "direct-materials"
    dm.mkdir(exist_ok=True)
    (dm / "CLAUDE.md").write_text(STARTER_CATEGORY.format(name="Direct materials"), encoding="utf-8")
    write_csv(
        dm / "suppliers.csv",
        ["supplier_id", "supplier_name", "state", "makes",
         "annual_value_usd", "contract_end", "status"],
        DIRECT_SUPPLIERS,
    )
    direct_orders = gen_direct_orders(2500)
    write_csv(
        dm / "orders.csv",
        ["po_number", "supplier_id", "item", "units", "total_usd", "po_date"],
        direct_orders,
    )

    # Logistics
    lg = PRACTICE / "logistics"
    lg.mkdir(exist_ok=True)
    (lg / "CLAUDE.md").write_text(STARTER_CATEGORY.format(name="Logistics"), encoding="utf-8")
    write_csv(
        lg / "carriers.csv",
        ["carrier_id", "carrier_name", "mode",
         "annual_value_usd", "contract_end", "status"],
        LOGISTICS_CARRIERS,
    )
    log_shipments = gen_logistics_shipments(5000)
    write_csv(
        lg / "shipments.csv",
        ["shipment_id", "carrier_id", "from_location", "to_location",
         "total_usd", "ship_date"],
        log_shipments,
    )

    # Indirect
    ind = PRACTICE / "indirect"
    ind.mkdir(exist_ok=True)
    (ind / "CLAUDE.md").write_text(STARTER_CATEGORY.format(name="Indirect"), encoding="utf-8")
    write_csv(
        ind / "vendors.csv",
        ["vendor_id", "vendor_name", "what_they_provide",
         "annual_value_usd", "contract_end", "status"],
        INDIRECT_VENDORS,
    )
    invoices, violations_count = gen_indirect_invoices(3000)
    write_csv(
        ind / "invoices.csv",
        ["invoice_number", "vendor_id", "what_for", "amount_usd",
         "invoice_date", "approval_path"],
        invoices,
    )

    # Report
    print(f"Wrote practice/ folder under {ROOT.name}/")
    print(f"  practice/CLAUDE.md (global starter)")
    print(f"  practice/direct-materials/   "
          f"suppliers.csv ({len(DIRECT_SUPPLIERS)} rows), "
          f"orders.csv ({len(direct_orders)} rows)")
    print(f"  practice/logistics/          "
          f"carriers.csv ({len(LOGISTICS_CARRIERS)} rows), "
          f"shipments.csv ({len(log_shipments)} rows)")
    print(f"  practice/indirect/           "
          f"vendors.csv ({len(INDIRECT_VENDORS)} rows), "
          f"invoices.csv ({len(invoices)} rows, "
          f"{violations_count} violations)")


if __name__ == "__main__":
    main()
