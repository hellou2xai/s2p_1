"""Generate the practice data set for Course 15: Purchase to Pay Intelligence.

Scenario: Meridian Corp, US-based manufacturer, $140M annual procurement spend.
Students build a P2P intelligence layer to screen requisitions, POs, goods
receipts, and invoices for compliance violations.

Produces seven CSV files at practice/ root (no nested subfolders):
  requisitions.csv         500 rows
  purchase-orders.csv      384 rows
  goods-receipts.csv       273 rows
  invoices.csv             168 rows
  contracted-rates.csv      10 rows
  approval-matrix.csv        5 rows
  preferred-suppliers.csv   20 rows

Field names follow the UPPERCASE convention used throughout the lessons
(REQ_ID, PO_ID, GR_ID, INV_ID, AMOUNT, REQUESTER, DEPT, APPROVER, etc.).
ID formats match the lesson examples: REQ-NNNN, PO-NNNN, GR-NNNN, INV-NNNN.

Deterministic via random.seed(42). All currency USD, US suppliers, US dates.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"

random.seed(42)
TODAY = date(2026, 4, 25)
DATA_START = date(2025, 10, 27)  # ~6 month window ending TODAY


# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

# Categories used across the data set. Capitalized form, since lesson samples
# show "IT Hardware", "MRO Supplies", "Office Supplies" etc.
CATEGORIES = [
    "IT Hardware",
    "MRO Supplies",
    "Office Supplies",
    "Logistics",
    "Professional Services",
    "Facilities",
    "Raw Materials",
    "Components",
]

# 20 preferred suppliers, one to four per category. Names are US business
# entities. SUPP-NN ID format matches the lesson sample (SUPP-04, SUPP-07).
# Supplier names assigned so the LMS Lesson 4 worked example resolves cleanly:
# PO-0189 (SUPP-04) maps to Northwind Industrial LLC, PO-0234 (SUPP-07) maps to
# Acme Components Inc, PO-0301 (SUPP-02) maps to Globex Supply Co. The displaced
# names (Cascade Cable Systems, Pinnacle Filtration LLC) move to other SUPP IDs.
PREFERRED_SUPPLIERS = [
    ("SUPP-01", "Cascade Cable Systems", "IT Hardware"),
    ("SUPP-02", "Globex Supply Co", "Components"),
    ("SUPP-03", "Pinnacle Filtration LLC", "MRO Supplies"),
    ("SUPP-04", "Northwind Industrial LLC", "Components"),
    ("SUPP-05", "Summit Office Solutions", "Office Supplies"),
    ("SUPP-06", "Heartland Logistics Inc", "Logistics"),
    ("SUPP-07", "Acme Components Inc", "MRO Supplies"),
    ("SUPP-08", "Atlantic Steel Co", "Raw Materials"),
    ("SUPP-09", "Beacon Professional Services", "Professional Services"),
    ("SUPP-10", "Cornerstone Facilities Group", "Facilities"),
    ("SUPP-11", "Patriot Freight Lines", "Logistics"),
    ("SUPP-12", "Liberty IT Hardware Corp", "IT Hardware"),
    ("SUPP-13", "Eagle Mechanical Supply", "MRO Supplies"),
    ("SUPP-14", "Redwood Office Products", "Office Supplies"),
    ("SUPP-15", "Magnolia Consulting LLC", "Professional Services"),
    ("SUPP-16", "Apex Polymer Group", "Raw Materials"),
    ("SUPP-17", "Sterling Building Services", "Facilities"),
    ("SUPP-18", "Riverside Electronic Components", "Components"),
    ("SUPP-19", "Crestline Network Hardware", "IT Hardware"),
    ("SUPP-20", "Vanguard Office Supply Co", "Office Supplies"),
]

# Non-preferred (maverick) suppliers used to plant maverick spend patterns.
# These do NOT appear in preferred-suppliers.csv.
NON_PREFERRED_SUPPLIERS = [
    ("SUPP-51", "QuickParts Direct", "MRO Supplies"),
    ("SUPP-52", "FastShip Express LLC", "Logistics"),
    ("SUPP-53", "OfficeMax Local", "Office Supplies"),
    ("SUPP-54", "TempForce Staffing", "Professional Services"),
    ("SUPP-55", "CloudNine Hosting", "IT Hardware"),
    ("SUPP-56", "Ironclad Hardware", "Components"),
    ("SUPP-57", "Bay Area Couriers", "Logistics"),
    ("SUPP-58", "Pioneer Office Direct", "Office Supplies"),
]

ALL_SUPPLIERS = PREFERRED_SUPPLIERS + NON_PREFERRED_SUPPLIERS

# Approval matrix. Lessons reference Role and Approval_Limit_USD columns.
APPROVAL_MATRIX = [
    {"Role": "Analyst", "Approval_Limit_USD": "5000"},
    {"Role": "Manager", "Approval_Limit_USD": "25000"},
    {"Role": "Director", "Approval_Limit_USD": "100000"},
    {"Role": "VP", "Approval_Limit_USD": "500000"},
    {"Role": "CFO", "Approval_Limit_USD": "Unlimited"},
]

ROLE_LIMITS = {
    "Analyst": 5000,
    "Manager": 25000,
    "Director": 100000,
    "VP": 500000,
    "CFO": 10**12,
}

# Departments. Operations, IT, Facilities are referenced in the lesson sample.
DEPARTMENTS = ["Operations", "IT", "Facilities", "Finance", "HR",
               "Engineering", "Procurement", "Sales"]

REQUESTERS = [
    "D. Holloway", "A. Fontaine", "R. Tanaka", "S. Obi", "M. Castillo",
    "T. Renshaw", "J. Whitfield", "K. Marquez", "L. Petersen", "P. Aldridge",
    "B. Sutherland", "E. Calloway", "G. Rasmussen", "H. Okonkwo", "N. Caruso",
    "O. Beaumont", "Q. Strickland", "R. McAllister", "U. Vasquez", "V. Lindgren",
    "W. Espinoza", "X. Chambers", "Y. Halverson", "Z. Donovan",
]

APPROVERS = [
    "T. Renshaw", "S. Obi", "M. Castillo", "P. Aldridge", "K. Marquez",
    "L. Petersen", "G. Rasmussen", "N. Caruso", "Q. Strickland", "U. Vasquez",
    "B. Sutherland", "E. Calloway", "J. Whitfield", "H. Okonkwo",
]

# 10 contracted rate items, one per supplier. ITEM_CODE format matches the
# lesson sample (CABL-2201, FILT-0088, BRKT-1144).
CONTRACTED_ITEMS = [
    ("CABL-2201", "SUPP-04", "Northwind Industrial LLC", 12.80, "Components"),
    ("FILT-0088", "SUPP-07", "Acme Components Inc", 84.00, "MRO Supplies"),
    ("BRKT-1144", "SUPP-02", "Globex Supply Co", 23.10, "Components"),
    ("SVR-3050",  "SUPP-01", "Cascade Cable Systems", 1450.00, "IT Hardware"),
    ("PAPR-0501", "SUPP-05", "Summit Office Solutions", 38.50, "Office Supplies"),
    ("STEEL-T01", "SUPP-08", "Atlantic Steel Co", 720.00, "Raw Materials"),
    ("FRGHT-MIL", "SUPP-06", "Heartland Logistics Inc", 4.85, "Logistics"),
    ("CONS-HR",   "SUPP-09", "Beacon Professional Services", 175.00, "Professional Services"),
    ("CLEAN-SF",  "SUPP-10", "Cornerstone Facilities Group", 1.40, "Facilities"),
    ("WRNCH-022", "SUPP-13", "Eagle Mechanical Supply", 28.75, "MRO Supplies"),
]

CATEGORY_TO_ITEMS = {}
for code, sid, sname, price, cat in CONTRACTED_ITEMS:
    CATEGORY_TO_ITEMS.setdefault(cat, []).append((code, sid, sname, price))

# Items for categories without a contracted rate. These will appear on POs
# (so categories like HR or Engineering have buying activity) but won't have
# a contracted rate for the price-deviation check.
EXTRA_CATEGORY_ITEMS = {
    "IT Hardware": [
        ("LAPTOP-X1", 1180.00),
        ("MNTR-2701", 320.00),
        ("RTR-A55",   485.00),
    ],
    "MRO Supplies": [
        ("LUBE-5G",  62.00),
        ("BELT-V40", 41.50),
    ],
    "Office Supplies": [
        ("TONER-77", 145.00),
        ("CHAIR-EX", 280.00),
    ],
    "Logistics": [
        ("EXPED-HR", 110.00),
    ],
    "Professional Services": [
        ("LEGAL-HR", 295.00),
        ("AUDIT-DAY", 1850.00),
    ],
    "Facilities": [
        ("HVAC-VST", 425.00),
    ],
    "Raw Materials": [
        ("POLY-RES", 9.20),
        ("ALUM-SQF", 14.40),
    ],
    "Components": [
        ("RESI-100", 0.85),
        ("CHIP-A12", 18.40),
    ],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def random_date(start: date, end: date) -> date:
    span = (end - start).days
    return start + timedelta(days=random.randint(0, span))


def required_role(amount: float) -> str:
    """Return the lowest role that can approve this amount."""
    for role, limit in ROLE_LIMITS.items():
        if amount <= limit:
            return role
    return "CFO"


def lower_role(role: str) -> str:
    """Return the role one level below `role`. Analyst stays Analyst."""
    order = ["Analyst", "Manager", "Director", "VP", "CFO"]
    idx = order.index(role)
    return order[max(0, idx - 1)]


def pick_item_for_category(cat: str) -> tuple[str, float]:
    """Pick an item code and contracted unit price for a PO line."""
    options = []
    if cat in CATEGORY_TO_ITEMS:
        options.extend([(code, price) for code, _, _, price in CATEGORY_TO_ITEMS[cat]])
    if cat in EXTRA_CATEGORY_ITEMS:
        options.extend(EXTRA_CATEGORY_ITEMS[cat])
    if not options:
        return ("MISC-0001", round(random.uniform(20, 250), 2))
    return random.choice(options)


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def build_requisitions():
    """500 requisitions, ~5% with approval-authority violations."""
    rows = []
    # Pre-pick which 25 indexes will have approval violations.
    violation_idx = set(random.sample(range(500), 25))

    for i in range(500):
        # 80% preferred, 20% non-preferred (drives maverick spend)
        if random.random() < 0.80:
            sup = random.choice(PREFERRED_SUPPLIERS)
        else:
            sup = random.choice(NON_PREFERRED_SUPPLIERS)
        sid, sname, cat = sup

        req_date = random_date(DATA_START, TODAY)
        # Tiered amounts so we get a realistic spread across approval levels.
        bucket = random.random()
        if bucket < 0.55:
            amount = round(random.uniform(200, 4800), 2)        # Analyst-level
        elif bucket < 0.85:
            amount = round(random.uniform(5500, 24500), 2)      # Manager-level
        elif bucket < 0.97:
            amount = round(random.uniform(28000, 95000), 2)     # Director-level
        else:
            amount = round(random.uniform(110000, 320000), 2)   # VP-level

        needed = required_role(amount)

        if i in violation_idx and needed != "Analyst":
            approver_role = lower_role(needed)
        else:
            approver_role = needed

        # Plant the named example: REQ-0347, $78,000, D. Holloway,
        # Operations, T. Renshaw (Manager).
        if i == 347:
            amount = 78000.00
            approver_role = "Manager"
            requester = "D. Holloway"
            dept = "Operations"
            approver = "T. Renshaw"
            req_date = date(2026, 3, 12)
        # Plant REQ-0219: $62,500, A. Fontaine, IT, S. Obi (Manager).
        elif i == 219:
            amount = 62500.00
            approver_role = "Manager"
            requester = "A. Fontaine"
            dept = "IT"
            approver = "S. Obi"
            req_date = date(2026, 2, 28)
        # Plant REQ-0412: $44,000, R. Tanaka, Facilities, M. Castillo (Manager).
        elif i == 412:
            amount = 44000.00
            approver_role = "Manager"
            requester = "R. Tanaka"
            dept = "Facilities"
            approver = "M. Castillo"
            req_date = date(2026, 4, 1)
        else:
            requester = random.choice(REQUESTERS)
            dept = random.choice(DEPARTMENTS)
            approver = random.choice(APPROVERS)

        rows.append({
            "REQ_ID": f"REQ-{i:04d}",
            "REQ_DATE": req_date.isoformat(),
            "REQUESTER": requester,
            "DEPT": dept,
            "CATEGORY": cat,
            "SUPPLIER_ID": sid,
            "SUPPLIER_NAME": sname,
            "AMOUNT": f"{amount:.2f}",
            "APPROVER": approver,
            "APPROVER_ROLE": approver_role,
            "STATUS": "Approved",
        })
    return rows


def build_purchase_orders(reqs):
    """384 POs. Each PO has at least one line. Sum of line totals = AMOUNT.

    Plant approximately:
      - 38 lines with PRICE_DEVIATION above 1% (overcharges and a few undercharges)
      - 22 OFF_CHANNEL POs (no requisition, preferred supplier)
      - 89 OFF_CONTRACT_SUPPLIER POs (non-preferred supplier where preferred exists)
      - 47 OFF_CONTRACT_PRICE POs (preferred supplier, price > 2% over contract)
    """
    rows = []
    line_rows = []  # the per-line rows we actually write

    # Pick the 384 requisitions whose POs we will issue.
    eligible_reqs = reqs[:]
    random.shuffle(eligible_reqs)
    chosen_reqs = eligible_reqs[:340]  # 340 reqs become POs; rest drop out

    po_counter = 0
    deviation_planted = 0
    target_deviations = 38

    def add_po(po_id, req_id, supplier, amount, po_date, dept, requester, force_dev=None):
        nonlocal deviation_planted
        sid, sname, cat = supplier
        # One line per PO so the row count in purchase-orders.csv matches
        # the canonical 384 figure in the LMS spec.
        allocations = [amount]

        for line_idx, line_total in enumerate(allocations, start=1):
            item_code, contracted_price = pick_item_for_category(cat)
            # Quantity such that qty * contracted_price ~ line_total.
            quantity = max(1, int(round(line_total / max(contracted_price, 0.01))))
            # PO unit price defaults to contracted price.
            po_unit_price = contracted_price
            # Plant pricing deviations.
            plant = False
            if force_dev:
                plant = True
            elif deviation_planted < target_deviations and random.random() < 0.10:
                plant = True
            if plant:
                # 80% overcharge, 20% undercharge
                if random.random() < 0.80:
                    factor = random.uniform(1.04, 1.18)
                else:
                    factor = random.uniform(0.85, 0.96)
                po_unit_price = round(contracted_price * factor, 2)
                deviation_planted += 1
            # Final line total is qty * po unit price.
            actual_line_total = round(quantity * po_unit_price, 2)
            line_rows.append({
                "PO_ID": po_id,
                "LINE_NUMBER": line_idx,
                "REQ_ID": req_id,
                "PO_DATE": po_date.isoformat(),
                "SUPPLIER_ID": sid,
                "SUPPLIER_NAME": sname,
                "CATEGORY": cat,
                "ITEM_CODE": item_code,
                "QUANTITY": quantity,
                "PO_UNIT_PRICE": f"{po_unit_price:.2f}",
                "LINE_TOTAL": f"{actual_line_total:.2f}",
                "DEPT": dept,
                "REQUESTER": requester,
                "STATUS": "Open",
            })

    # 1) POs from chosen requisitions
    for req in chosen_reqs:
        po_id = f"PO-{po_counter:04d}"
        supplier = (req["SUPPLIER_ID"], req["SUPPLIER_NAME"], req["CATEGORY"])
        amount = float(req["AMOUNT"])
        po_date = date.fromisoformat(req["REQ_DATE"]) + timedelta(days=random.randint(1, 7))
        if po_date > TODAY:
            po_date = TODAY
        add_po(po_id, req["REQ_ID"], supplier, amount, po_date,
               req["DEPT"], req["REQUESTER"])
        po_counter += 1

    # Plant the named example PO-0189: SUPP-04 / CABL-2201,
    # PO unit 14.20 vs contract 12.80, qty 2000 (overcharge 2800).
    # Replace the 189-th line block with the planted values.
    target_po = "PO-0189"
    # Find any existing line for that PO_ID and rewrite it as a single line.
    line_rows[:] = [r for r in line_rows if r["PO_ID"] != target_po]
    line_rows.append({
        "PO_ID": "PO-0189",
        "LINE_NUMBER": 1,
        "REQ_ID": "REQ-0347",
        "PO_DATE": "2026-03-15",
        "SUPPLIER_ID": "SUPP-04",
        "SUPPLIER_NAME": "Northwind Industrial LLC",
        "CATEGORY": "Components",
        "ITEM_CODE": "CABL-2201",
        "QUANTITY": 2000,
        "PO_UNIT_PRICE": "14.20",
        "LINE_TOTAL": f"{2000 * 14.20:.2f}",
        "DEPT": "Operations",
        "REQUESTER": "D. Holloway",
        "STATUS": "Open",
    })

    # Plant PO-0234: SUPP-07 / FILT-0088, 87.50 vs 84.00, qty 500 (overcharge 1750).
    line_rows[:] = [r for r in line_rows if r["PO_ID"] != "PO-0234"]
    line_rows.append({
        "PO_ID": "PO-0234",
        "LINE_NUMBER": 2,
        "REQ_ID": "REQ-0219",
        "PO_DATE": "2026-03-02",
        "SUPPLIER_ID": "SUPP-07",
        "SUPPLIER_NAME": "Acme Components Inc",
        "CATEGORY": "MRO Supplies",
        "ITEM_CODE": "FILT-0088",
        "QUANTITY": 500,
        "PO_UNIT_PRICE": "87.50",
        "LINE_TOTAL": f"{500 * 87.50:.2f}",
        "DEPT": "IT",
        "REQUESTER": "A. Fontaine",
        "STATUS": "Open",
    })

    # Plant PO-0301: SUPP-02 / BRKT-1144, 22.00 vs 23.10, qty 300 (undercharge 330).
    line_rows[:] = [r for r in line_rows if r["PO_ID"] != "PO-0301"]
    line_rows.append({
        "PO_ID": "PO-0301",
        "LINE_NUMBER": 1,
        "REQ_ID": "REQ-0412",
        "PO_DATE": "2026-04-04",
        "SUPPLIER_ID": "SUPP-02",
        "SUPPLIER_NAME": "Globex Supply Co",
        "CATEGORY": "Components",
        "ITEM_CODE": "BRKT-1144",
        "QUANTITY": 300,
        "PO_UNIT_PRICE": "22.00",
        "LINE_TOTAL": f"{300 * 22.00:.2f}",
        "DEPT": "Facilities",
        "REQUESTER": "R. Tanaka",
        "STATUS": "Open",
    })

    # Trim/extend to exactly 384 POs.
    distinct_po_ids = sorted({r["PO_ID"] for r in line_rows},
                             key=lambda x: int(x.split("-")[1]))
    if len(distinct_po_ids) > 384:
        keep = set(distinct_po_ids[:384])
        line_rows[:] = [r for r in line_rows if r["PO_ID"] in keep]
    else:
        # Add OFF_CHANNEL POs (no requisition) until we hit 384.
        next_po = max(int(p.split("-")[1]) for p in distinct_po_ids) + 1
        while len({r["PO_ID"] for r in line_rows}) < 384:
            sup = random.choice(PREFERRED_SUPPLIERS)
            sid, sname, cat = sup
            po_date = random_date(DATA_START, TODAY)
            amount = round(random.uniform(800, 18000), 2)
            requester = random.choice(REQUESTERS)
            dept = random.choice(DEPARTMENTS)
            add_po(f"PO-{next_po:04d}", "", sup, amount, po_date, dept, requester)
            next_po += 1

    # Final sort by PO_ID then LINE_NUMBER.
    line_rows.sort(key=lambda r: (r["PO_ID"], r["LINE_NUMBER"]))
    return line_rows


def build_goods_receipts(po_lines):
    """273 goods receipts. One GR row per receipted PO line.

    A GR is created for ~71% of PO lines (273 / 384). Plant ~20% qty mismatches.

    The LMS Lesson 4 worked example expects:
      - PO-0189 has a GR (so INV-0087 fails as PRICE_MISMATCH, not NO_GR).
      - PO-0301 has NO GR (so INV-0141 fails as NO_GR).
    """
    distinct_pos = sorted({r["PO_ID"] for r in po_lines},
                         key=lambda x: int(x.split("-")[1]))
    # Pick 273 received POs, then force PO-0189 in and PO-0301 out.
    received_pos = set(random.sample(distinct_pos, 273))
    received_pos.discard("PO-0301")
    received_pos.add("PO-0189")
    # Hold count at 273 by pruning one other PO if needed.
    while len(received_pos) > 273:
        for pid in distinct_pos:
            if pid in received_pos and pid not in {"PO-0189", "PO-0234"}:
                received_pos.discard(pid)
                break
    while len(received_pos) < 273:
        for pid in distinct_pos:
            if pid not in received_pos and pid != "PO-0301":
                received_pos.add(pid)
                break

    rows = []
    gr_counter = 0
    # For each PO that is received, write one GR row using the first PO line.
    seen = set()
    for line in po_lines:
        if line["PO_ID"] not in received_pos:
            continue
        if line["PO_ID"] in seen:
            continue
        seen.add(line["PO_ID"])

        po_qty = int(line["QUANTITY"])
        # PO-0189 is planted with a clean qty match so INV-0087 fails only
        # as PRICE_MISMATCH (the worked example in Lesson 4 expects this).
        if line["PO_ID"] == "PO-0189":
            gr_qty = po_qty
        elif random.random() < 0.20:
            # 20% of GRs have qty mismatch (gr qty differs from po qty by >5%).
            # Skew under-delivery more than over-delivery.
            if random.random() < 0.75:
                gr_qty = max(1, int(round(po_qty * random.uniform(0.70, 0.93))))
            else:
                gr_qty = int(round(po_qty * random.uniform(1.06, 1.15)))
        else:
            gr_qty = po_qty  # exact match

        po_date = date.fromisoformat(line["PO_DATE"])
        gr_date = po_date + timedelta(days=random.randint(3, 30))
        if gr_date > TODAY:
            gr_date = TODAY
        # Force PO-0189's GR_DATE to a fixed value shortly after the PO_DATE,
        # so the planted row stays stable across regenerations.
        if line["PO_ID"] == "PO-0189":
            gr_date = date(2026, 3, 20)
        rows.append({
            "GR_ID": f"GR-{gr_counter:04d}",
            "PO_ID": line["PO_ID"],
            "GR_DATE": gr_date.isoformat(),
            "SUPPLIER_ID": line["SUPPLIER_ID"],
            "SUPPLIER_NAME": line["SUPPLIER_NAME"],
            "ITEM_CODE": line["ITEM_CODE"],
            "PO_QTY": po_qty,
            "GR_QTY": gr_qty,
            "QUALITY_ACCEPTED": "Yes" if (line["PO_ID"] == "PO-0189" or random.random() < 0.94) else "No",
        })
        gr_counter += 1
    return rows


def build_invoices(po_lines, grs):
    """168 invoices. Plant ~42 three-way-match exceptions (25%).

    Exception mix targets:
      - PRICE_MISMATCH: ~15
      - QTY_MISMATCH:   ~12
      - NO_GR:          ~8
      - NO_PO:          ~4
      - ARITHMETIC_ERROR: ~3
    """
    # Build PO and GR lookups.
    po_first_line = {}
    for line in po_lines:
        if line["PO_ID"] not in po_first_line:
            po_first_line[line["PO_ID"]] = line
    gr_by_po = {g["PO_ID"]: g for g in grs}

    # Invoiced POs are a subset of received POs. 168 invoices total.
    received_po_ids = list(gr_by_po.keys())
    random.shuffle(received_po_ids)
    invoiced_po_ids = received_po_ids[:160]  # 160 invoices come from received POs

    rows = []
    inv_counter = 0
    # Pre-pick exception slots.
    pool = list(range(168))
    random.shuffle(pool)
    no_po_idx = set(pool[:4])                             # 4 NO_PO
    no_gr_idx = set(pool[4:12])                           # 8 NO_GR
    qty_mm_idx = set(pool[12:24])                         # 12 QTY_MISMATCH
    price_mm_idx = set(pool[24:39])                       # 15 PRICE_MISMATCH
    arith_idx = set(pool[39:42])                          # 3 ARITHMETIC_ERROR
    # remaining (42..167) are clean matches

    # Discount terms split: 24 invoices carry "2/10 Net 30".
    discount_idx = set(random.sample(range(168), 24))

    for i in range(168):
        # Choose source PO. NO_PO invoices reference a fake PO that doesn't exist.
        if i in no_po_idx:
            po_id = f"PO-9{i:03d}"  # guaranteed not to exist
            line = None
            gr = None
        elif i in no_gr_idx:
            # Pick a PO that has NO goods receipt.
            unreceipted = [pid for pid in po_first_line.keys() if pid not in gr_by_po]
            if not unreceipted:
                po_id = invoiced_po_ids[i % len(invoiced_po_ids)]
            else:
                po_id = random.choice(unreceipted)
            line = po_first_line.get(po_id)
            gr = None
        else:
            po_id = invoiced_po_ids[i % len(invoiced_po_ids)]
            line = po_first_line.get(po_id)
            gr = gr_by_po.get(po_id)

        # Build invoice fields.
        if line is None:
            # NO_PO: synthetic supplier and amount.
            sup = random.choice(PREFERRED_SUPPLIERS)
            sid, sname, cat = sup
            po_unit_price = round(random.uniform(20, 500), 2)
            inv_qty = random.randint(5, 200)
            inv_unit_price = po_unit_price
            inv_date = random_date(DATA_START, TODAY)
        else:
            sid = line["SUPPLIER_ID"]
            sname = line["SUPPLIER_NAME"]
            cat = line["CATEGORY"]
            po_unit_price = float(line["PO_UNIT_PRICE"])
            po_qty = int(line["QUANTITY"])
            gr_qty = int(gr["GR_QTY"]) if gr else po_qty
            # Default: invoice quantity = received quantity.
            inv_qty = gr_qty
            inv_unit_price = po_unit_price
            inv_date = date.fromisoformat(line["PO_DATE"]) + timedelta(days=random.randint(7, 35))

        # Apply exception planting.
        if i in qty_mm_idx and line is not None:
            # Invoice for MORE than received.
            inv_qty = max(int(inv_qty * 1.10), inv_qty + 5)
        if i in price_mm_idx:
            # Invoice unit price diverges from PO unit price by > 2%.
            inv_unit_price = round(po_unit_price * random.uniform(1.03, 1.12), 2)

        inv_total = round(inv_qty * inv_unit_price, 2)
        # ARITHMETIC_ERROR: write a total that doesn't equal qty * unit price.
        if i in arith_idx:
            inv_total = round(inv_total + random.uniform(50, 250), 2)

        if inv_date > TODAY:
            inv_date = TODAY

        # Payment terms: 24 with discount, rest plain Net N.
        if i in discount_idx:
            payment_terms = "2/10 Net 30"
            net_days = 30
        else:
            payment_terms = random.choice(["Net 30", "Net 45", "Net 60"])
            net_days = int(payment_terms.split()[-1])

        due_date = inv_date + timedelta(days=net_days)

        # Decide whether the invoice has a payment date (paid).
        # Aim: ~24 discount invoices split 8 captured / 10 missed / 4 open / 2 expired.
        # ~14 past-due open invoices (penalty exposure).
        payment_date = ""
        days_since_inv = (TODAY - inv_date).days

        if i in discount_idx:
            # Index within the discount set drives status.
            # Use deterministic ordering by sorting the set.
            ordered = sorted(discount_idx)
            slot = ordered.index(i)
            if slot < 8:
                # Captured: paid within window.
                pay = inv_date + timedelta(days=random.randint(3, 9))
                if pay <= TODAY:
                    payment_date = pay.isoformat()
            elif slot < 18:
                # Missed: paid after the discount window but before today.
                pay = inv_date + timedelta(days=random.randint(15, 28))
                if pay <= TODAY:
                    payment_date = pay.isoformat()
                else:
                    # If payment would be in the future, leave as Open instead.
                    payment_date = ""
            elif slot < 22:
                # Open: discount window still active. Force inv_date close to TODAY.
                inv_date = TODAY - timedelta(days=random.randint(2, 8))
                due_date = inv_date + timedelta(days=net_days)
                payment_date = ""
            else:
                # Expired: discount window passed but unpaid.
                inv_date = TODAY - timedelta(days=random.randint(15, 35))
                due_date = inv_date + timedelta(days=net_days)
                payment_date = ""
        else:
            # ~75% of non-discount invoices are paid.
            if days_since_inv > 7 and random.random() < 0.75:
                pay_offset = random.randint(15, max(net_days + 10, 40))
                pay = inv_date + timedelta(days=pay_offset)
                if pay <= TODAY:
                    payment_date = pay.isoformat()

        rows.append({
            "INV_ID": f"INV-{i:04d}",
            "INV_DATE": inv_date.isoformat(),
            "PO_ID": po_id,
            "SUPPLIER_ID": sid,
            "SUPPLIER_NAME": sname,
            "ITEM_CODE": line["ITEM_CODE"] if line else "MISC-0001",
            "INV_QTY": inv_qty,
            "INV_UNIT_PRICE": f"{inv_unit_price:.2f}",
            "INV_AMOUNT": f"{inv_total:.2f}",
            "DUE_DATE": due_date.isoformat(),
            "PAYMENT_DATE": payment_date,
            "PAYMENT_TERMS": payment_terms,
        })
        inv_counter += 1

    # Plant named samples used in the lessons. The supplier mapping above is
    # arranged so PO-0189 (SUPP-04) joins to Northwind Industrial LLC,
    # PO-0234 (SUPP-07) joins to Acme Components Inc, and PO-0301 (SUPP-02)
    # joins to Globex Supply Co, matching the LMS Lesson 4 worked example.
    if rows:
        # Overwrite by index where we can.
        target_replacements = {
            87: {
                "INV_ID": "INV-0087",
                "INV_DATE": "2026-04-02",
                "PO_ID": "PO-0189",
                "SUPPLIER_ID": "SUPP-04",
                "SUPPLIER_NAME": "Northwind Industrial LLC",
                "ITEM_CODE": "CABL-2201",
                "INV_QTY": 2000,
                "INV_UNIT_PRICE": "21.00",
                "INV_AMOUNT": "42000.00",
                "DUE_DATE": "2026-05-02",
                "PAYMENT_DATE": "",
                "PAYMENT_TERMS": "Net 30",
            },
            103: {
                "INV_ID": "INV-0103",
                "INV_DATE": "2026-04-04",
                "PO_ID": "PO-0234",
                "SUPPLIER_ID": "SUPP-07",
                "SUPPLIER_NAME": "Acme Components Inc",
                "ITEM_CODE": "FILT-0088",
                "INV_QTY": 540,
                "INV_UNIT_PRICE": "46.67",
                "INV_AMOUNT": "25200.00",
                "DUE_DATE": "2026-05-04",
                "PAYMENT_DATE": "",
                "PAYMENT_TERMS": "Net 30",
            },
            141: {
                "INV_ID": "INV-0141",
                "INV_DATE": "2026-03-28",
                "PO_ID": "PO-0301",
                "SUPPLIER_ID": "SUPP-02",
                "SUPPLIER_NAME": "Globex Supply Co",
                "ITEM_CODE": "BRKT-1144",
                "INV_QTY": 841,
                "INV_UNIT_PRICE": "22.00",
                "INV_AMOUNT": "18500.00",
                "DUE_DATE": "2026-04-27",
                "PAYMENT_DATE": "",
                "PAYMENT_TERMS": "Net 30",
            },
            42: {
                "INV_ID": "INV-0042",
                "INV_DATE": "2026-04-20",
                "PAYMENT_DATE": "",
                "PAYMENT_TERMS": "2/10 Net 30",
                "INV_AMOUNT": "9200.00",
            },
            88: {
                "INV_ID": "INV-0088",
                "INV_DATE": "2026-04-18",
                "PAYMENT_DATE": "",
                "PAYMENT_TERMS": "2/10 Net 30",
                "INV_AMOUNT": "15500.00",
            },
            127: {
                "INV_ID": "INV-0127",
                "INV_DATE": "2026-04-17",
                "PAYMENT_DATE": "",
                "PAYMENT_TERMS": "2/10 Net 30",
                "INV_AMOUNT": "7600.00",
            },
        }
        for idx, overrides in target_replacements.items():
            if idx < len(rows):
                rows[idx].update(overrides)
                # Recompute due_date for the discount samples so it stays consistent.
                if "INV_DATE" in overrides and "PAYMENT_TERMS" in overrides:
                    inv_d = date.fromisoformat(overrides["INV_DATE"])
                    if "Net" in overrides["PAYMENT_TERMS"]:
                        net = int(overrides["PAYMENT_TERMS"].split()[-1])
                        rows[idx]["DUE_DATE"] = (inv_d + timedelta(days=net)).isoformat()

    return rows


def build_contracted_rates():
    """10 contracted rate rows."""
    rows = []
    for code, sid, sname, price, cat in CONTRACTED_ITEMS:
        # Effective dates: started 6 to 18 months ago, expire 6 to 18 months out.
        eff_from = TODAY - timedelta(days=random.randint(180, 540))
        eff_to = TODAY + timedelta(days=random.randint(180, 540))
        rows.append({
            "SUPPLIER_ID": sid,
            "SUPPLIER_NAME": sname,
            "ITEM_CODE": code,
            "CATEGORY": cat,
            "CONTRACTED_UNIT_PRICE": f"{price:.2f}",
            "UNIT_OF_MEASURE": "Each",
            "EFFECTIVE_FROM": eff_from.isoformat(),
            "EFFECTIVE_TO": eff_to.isoformat(),
        })
    return rows


def build_preferred_suppliers():
    rows = []
    for sid, sname, cat in PREFERRED_SUPPLIERS:
        rows.append({
            "SUPPLIER_ID": sid,
            "SUPPLIER_NAME": sname,
            "CATEGORY": cat,
            "PREFERRED_FROM": (TODAY - timedelta(days=random.randint(120, 720))).isoformat(),
        })
    return rows


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------

def write_csv(path: Path, rows, fieldnames=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.name}: {len(rows)} rows")


def ensure_workspace_folders():
    """Pre-create Master/, Drafts/, and Outputs/ under practice/ with .gitkeep
    placeholders. Lessons tell students to create these, but having them on
    disk after a fresh clone smooths the setup step.
    """
    for name in ("Master", "Drafts", "Outputs"):
        folder = PRACTICE / name
        folder.mkdir(parents=True, exist_ok=True)
        keep = folder / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    print("  workspace folders ready: Master/, Drafts/, Outputs/")


def main():
    print("Building Course 15 practice data at:", PRACTICE)
    print()
    PRACTICE.mkdir(parents=True, exist_ok=True)

    reqs = build_requisitions()
    write_csv(PRACTICE / "requisitions.csv", reqs)

    po_lines = build_purchase_orders(reqs)
    # Distinct PO count check.
    distinct_po_count = len({r["PO_ID"] for r in po_lines})
    print(f"  (purchase-orders.csv distinct PO_IDs: {distinct_po_count})")
    write_csv(PRACTICE / "purchase-orders.csv", po_lines)

    grs = build_goods_receipts(po_lines)
    write_csv(PRACTICE / "goods-receipts.csv", grs)

    invs = build_invoices(po_lines, grs)
    write_csv(PRACTICE / "invoices.csv", invs)

    write_csv(PRACTICE / "contracted-rates.csv", build_contracted_rates())
    write_csv(PRACTICE / "approval-matrix.csv", APPROVAL_MATRIX)
    write_csv(PRACTICE / "preferred-suppliers.csv", build_preferred_suppliers())

    ensure_workspace_folders()

    print()
    print("Done. All files in practice/")


if __name__ == "__main__":
    main()
