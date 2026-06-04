"""Generate practice data for Course 21: Compliance, Policy, and Audit Readiness.

Scenario: Internal audit flagged three compliance concerns at Meridian Corp.
Students build policy encoding, compliance checking, and audit trail generation.

Produces:
  practice/data/transactions.csv          (200 rows, 55 planted violations)
  practice/data/approval-matrix.csv       (5 authority levels)
  practice/data/preferred-suppliers.csv   (10 preferred suppliers)
  practice/data/contract-documentation.csv (required documents per contract type)
  practice/data/policy-rules.json         (testable compliance rules)

Deterministic via random.seed(42). All currency USD, US geography.

Schema notes:
  transactions.csv columns match Lesson 2 / Lesson 4 references:
    transaction_id, date, amount_usd, supplier_id, supplier_name, category,
    requester, requester_id, requester_title, approver_title, approver_name,
    contract_type, signed_agreement, scope_of_work, pricing_schedule,
    insurance_certificate, nda_document, signed_sow, delivery_schedule,
    signed_nda, signed_sla, service_definition, penalty_schedule,
    escalation_matrix, signed_amendment, original_agreement_reference,
    exception_approved, violation_type, cost_center.

The per-document flag columns (signed_agreement, scope_of_work, etc.) hold
"present" or "missing" so Lesson 4 can detect gaps by reading the columns
named in contract-documentation.csv.
"""

from __future__ import annotations

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"
DATA_DIR = PRACTICE / "data"
random.seed(42)
TODAY = date(2026, 4, 25)
START_DATE = date(2026, 1, 1)
END_DATE = date(2026, 4, 24)

APPROVAL_MATRIX = [
    {"level": "Analyst", "min_usd": 0, "max_usd": 5000, "approver_title": "Manager"},
    {"level": "Manager", "min_usd": 5001, "max_usd": 25000, "approver_title": "Director"},
    {"level": "Director", "min_usd": 25001, "max_usd": 100000, "approver_title": "VP"},
    {"level": "VP", "min_usd": 100001, "max_usd": 500000, "approver_title": "CFO"},
    {"level": "CFO", "min_usd": 500001, "max_usd": 9999999, "approver_title": "Board"},
]

# Approval level rank, lowest to highest. Used to compare titles.
RANK = {"Manager": 1, "Director": 2, "VP": 3, "CFO": 4, "Board": 5}

PREFERRED_SUPPLIERS = [
    ("SUP001", "Great Lakes Steel", "raw-materials"),
    ("SUP002", "Heartland Polymers", "raw-materials"),
    ("SUP003", "Pacific Aluminum", "raw-materials"),
    ("SUP004", "Continental Freight", "logistics"),
    ("SUP005", "TechForward Solutions", "it-services"),
    ("SUP006", "National Facilities", "facilities"),
    ("SUP007", "Whitfield Consulting", "professional-services"),
    ("SUP008", "Cascade Fasteners", "raw-materials"),
    ("SUP009", "Patriot Logistics", "logistics"),
    ("SUP010", "CloudBridge Systems", "it-services"),
]

NON_PREFERRED_SUPPLIERS = [
    ("SUP051", "QuickParts Inc", "raw-materials"),
    ("SUP052", "FastShip Express", "logistics"),
    ("SUP053", "OfficeMax Direct", "office-supplies"),
    ("SUP054", "TempForce Staffing", "professional-services"),
    ("SUP055", "CloudNine Hosting", "it-services"),
]

# Requesters: (id, name, title). Title sets the requester's own authority level.
REQUESTERS = [
    ("EMP001", "Aaron Johnson", "Analyst"),
    ("EMP002", "Beth Smith", "Manager"),
    ("EMP003", "Carlos Williams", "Director"),
    ("EMP004", "Dana Brown", "Analyst"),
    ("EMP005", "Evan Davis", "Manager"),
    ("EMP006", "Faith Miller", "VP"),
    ("EMP007", "Gabe Wilson", "Analyst"),
    ("EMP008", "Hannah Moore", "Director"),
]

# Approvers: (name, title). Used as the named approver on each transaction.
APPROVERS = {
    "Manager": [("Beth Smith", "Manager"), ("Evan Davis", "Manager"), ("Marcus Lee", "Manager")],
    "Director": [("Carlos Williams", "Director"), ("Hannah Moore", "Director"), ("Tara Nguyen", "Director")],
    "VP": [("Faith Miller", "VP"), ("Owen Reed", "VP")],
    "CFO": [("Priya Shah", "CFO")],
    "Board": [("Board of Directors", "Board")],
}

CONTRACT_TYPES = ["MSA", "SOW", "NDA", "SLA", "amendment"]

CONTRACT_DOCS = {
    "MSA": ["signed_agreement", "scope_of_work", "pricing_schedule", "insurance_certificate", "nda_document"],
    "SOW": ["signed_sow", "pricing_schedule", "delivery_schedule"],
    "NDA": ["signed_nda"],
    "SLA": ["signed_sla", "service_definition", "penalty_schedule", "escalation_matrix"],
    "amendment": ["signed_amendment", "original_agreement_reference"],
}

ALL_DOC_COLUMNS = sorted({d for docs in CONTRACT_DOCS.values() for d in docs})

COST_CENTERS = ["CC-100", "CC-200", "CC-300", "CC-400"]


def required_approver_title(amount):
    for tier in APPROVAL_MATRIX:
        if tier["min_usd"] <= amount <= tier["max_usd"]:
            return tier["approver_title"]
    return "Board"


def pick_approver(title):
    return random.choice(APPROVERS[title])


def lower_approver_title(required_title):
    """Pick a title strictly below the required title."""
    required_rank = RANK[required_title]
    candidates = [t for t, r in RANK.items() if r < required_rank]
    if not candidates:
        return "Manager"
    return random.choice(candidates)


def random_business_date():
    while True:
        days_back = random.randint(0, (END_DATE - START_DATE).days)
        d = START_DATE + timedelta(days=days_back)
        if d.weekday() < 5:
            return d


def blank_doc_flags():
    return {col: "n/a" for col in ALL_DOC_COLUMNS}


def fill_complete_docs(contract_type):
    flags = blank_doc_flags()
    for doc in CONTRACT_DOCS[contract_type]:
        flags[doc] = "present"
    return flags


def fill_with_gap(contract_type):
    """Mark required docs present, then drop one to create a gap."""
    flags = blank_doc_flags()
    required = list(CONTRACT_DOCS[contract_type])
    for doc in required:
        flags[doc] = "present"
    # Remove one mandatory doc.
    missing = random.choice(required)
    flags[missing] = "missing"
    return flags, missing


def build_transactions():
    """Build 200 transactions. Plant 55 violations, distributed across four types.

    Plan: 18 approval breaches, 14 non-preferred, 16 documentation gaps,
          7 split-order pairs (counted as 7 violations on the second leg).
    Total: 55 violations across 4 types.
    """
    rows = []
    txn_idx = 0

    def new_id():
        nonlocal txn_idx
        txn_id = f"TXN-{60000 + txn_idx:05d}"
        txn_idx += 1
        return txn_id

    def base_compliant():
        """Return a transaction dict with no violations."""
        amount = round(random.uniform(200, 480000), 2)
        supplier = random.choice(PREFERRED_SUPPLIERS)
        requester = random.choice(REQUESTERS)
        contract_type = random.choice(CONTRACT_TYPES)
        required_title = required_approver_title(amount)
        # Approver must be different person from requester for compliance.
        for _ in range(10):
            approver = pick_approver(required_title)
            if approver[0] != requester[1]:
                break
        flags = fill_complete_docs(contract_type)
        row = {
            "transaction_id": new_id(),
            "date": random_business_date().isoformat(),
            "amount_usd": amount,
            "supplier_id": supplier[0],
            "supplier_name": supplier[1],
            "category": supplier[2],
            "requester": requester[1],
            "requester_id": requester[0],
            "requester_title": requester[2],
            "approver_title": approver[1],
            "approver_name": approver[0],
            "contract_type": contract_type,
            "exception_approved": "no",
            "violation_type": "none",
            "cost_center": random.choice(COST_CENTERS),
        }
        row.update(flags)
        return row

    # ----- 1. Approval authority breaches (18) -----
    # Mix of under-approved (12) and self-approved (6).
    for _ in range(12):
        row = base_compliant()
        # Force amount into a higher tier than the title we will pick.
        amount = round(random.uniform(5500, 95000), 2)
        row["amount_usd"] = amount
        required = required_approver_title(amount)
        wrong = lower_approver_title(required)
        approver = pick_approver(wrong)
        # Ensure approver is not the same person as requester.
        for _ in range(10):
            if approver[0] != row["requester"]:
                break
            approver = pick_approver(wrong)
        row["approver_title"] = approver[1]
        row["approver_name"] = approver[0]
        row["violation_type"] = "approval_authority_breach"
        rows.append(row)

    for _ in range(6):
        row = base_compliant()
        # Self-approved: approver name equals requester.
        amount = round(random.uniform(2000, 80000), 2)
        row["amount_usd"] = amount
        required = required_approver_title(amount)
        row["approver_title"] = required
        row["approver_name"] = row["requester"]
        row["violation_type"] = "approval_authority_breach"
        rows.append(row)

    # ----- 2. Non-preferred supplier (14) -----
    for _ in range(14):
        row = base_compliant()
        supplier = random.choice(NON_PREFERRED_SUPPLIERS)
        row["supplier_id"] = supplier[0]
        row["supplier_name"] = supplier[1]
        row["category"] = supplier[2]
        row["exception_approved"] = "no"
        row["violation_type"] = "non_preferred_supplier"
        rows.append(row)

    # ----- 3. Documentation gaps (16) -----
    for _ in range(16):
        row = base_compliant()
        flags, missing_doc = fill_with_gap(row["contract_type"])
        for col in ALL_DOC_COLUMNS:
            row[col] = flags[col]
        row["violation_type"] = "incomplete_documentation"
        rows.append(row)

    # ----- 4. Suspected split orders (7 pairs => 14 transactions, 7 flagged) -----
    # Each pair: same supplier, two amounts under $5,000, dates within 5 business days.
    # We flag the second transaction in the pair as the violation.
    split_pairs_count = 7
    used_split_suppliers = []
    for _ in range(split_pairs_count):
        supplier = random.choice(PREFERRED_SUPPLIERS)
        used_split_suppliers.append(supplier)
        first_date = random_business_date()
        # Second date 1 to 4 business days later.
        second_date = first_date
        added = 0
        while added < random.randint(1, 4):
            second_date = second_date + timedelta(days=1)
            if second_date.weekday() < 5:
                added += 1
        a1 = round(random.uniform(2500, 4900), 2)
        a2 = round(random.uniform(2500, 4900), 2)
        # First leg: compliant looking.
        leg1 = base_compliant()
        leg1["date"] = first_date.isoformat()
        leg1["amount_usd"] = a1
        leg1["supplier_id"] = supplier[0]
        leg1["supplier_name"] = supplier[1]
        leg1["category"] = supplier[2]
        leg1["approver_title"] = "Manager"
        leg1["approver_name"] = pick_approver("Manager")[0]
        # Make sure approver is not requester.
        if leg1["approver_name"] == leg1["requester"]:
            leg1["approver_name"] = "Marcus Lee"
        leg1["violation_type"] = "none"
        rows.append(leg1)

        leg2 = base_compliant()
        leg2["date"] = second_date.isoformat()
        leg2["amount_usd"] = a2
        leg2["supplier_id"] = supplier[0]
        leg2["supplier_name"] = supplier[1]
        leg2["category"] = supplier[2]
        leg2["approver_title"] = "Manager"
        leg2["approver_name"] = pick_approver("Manager")[0]
        if leg2["approver_name"] == leg2["requester"]:
            leg2["approver_name"] = "Marcus Lee"
        leg2["violation_type"] = "suspected_split_order"
        rows.append(leg2)

    # ----- 5. Fill the rest with compliant transactions to reach 200 total -----
    while len(rows) < 200:
        rows.append(base_compliant())

    # Sort by date for readability.
    rows.sort(key=lambda r: (r["date"], r["transaction_id"]))

    # Renumber transaction_ids in date order so TXN-60000 is the earliest.
    for i, row in enumerate(rows):
        row["transaction_id"] = f"TXN-{60000 + i:05d}"

    return rows


def build_contract_documentation():
    rows = []
    for ctype in CONTRACT_TYPES:
        for doc in CONTRACT_DOCS[ctype]:
            rows.append({
                "contract_type": ctype,
                "required_document": doc,
                "mandatory": "yes",
            })
    return rows


def build_policy_rules():
    return {
        "approval_authority": {
            "description": "Every transaction must be approved by the correct authority level based on amount.",
            "thresholds": [
                {"min_usd": 0, "max_usd": 5000, "required_approver": "Manager"},
                {"min_usd": 5001, "max_usd": 25000, "required_approver": "Director"},
                {"min_usd": 25001, "max_usd": 100000, "required_approver": "VP"},
                {"min_usd": 100001, "max_usd": 500000, "required_approver": "CFO"},
                {"min_usd": 500001, "max_usd": 9999999, "required_approver": "Board"},
            ],
            "self_approval_check": "approver_name must not equal requester",
            "severity_if_breached": "high",
        },
        "preferred_supplier": {
            "description": "All purchases must use a preferred supplier unless an approved exception exists.",
            "exception_required_fields": ["rationale", "approval_chain", "expiry_date"],
            "severity_if_breached": "medium",
        },
        "documentation": {
            "description": "Every transaction must have complete documentation per the contract type.",
            "required_documents_lookup": "contract-documentation.csv",
            "severity_if_breached": "medium",
        },
        "split_order_detection": {
            "description": "Flag transactions from the same supplier within 5 business days that individually fall below a threshold but combined exceed it.",
            "detection_window_days": 5,
            "threshold_usd": 5000,
            "severity_if_breached": "high",
        },
        "breach_escalation": {
            "description": "If total breach count exceeds 15 in a single compliance run, escalate to VP of Procurement.",
            "escalation_threshold": 15,
            "escalation_recipient": "VP of Procurement",
        },
    }


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
    print("Building Course 21 practice data...")
    print()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Fixed column order so the CSV header is stable.
    transaction_columns = [
        "transaction_id", "date", "amount_usd",
        "supplier_id", "supplier_name", "category",
        "requester", "requester_id", "requester_title",
        "approver_title", "approver_name",
        "contract_type",
    ] + ALL_DOC_COLUMNS + [
        "exception_approved", "violation_type", "cost_center",
    ]

    txns = build_transactions()
    write_csv(DATA_DIR / "transactions.csv", txns, fieldnames=transaction_columns)

    violations = sum(1 for t in txns if t["violation_type"] != "none")
    print(f"    ({violations} planted violations)")

    write_csv(DATA_DIR / "approval-matrix.csv", APPROVAL_MATRIX)

    write_csv(
        DATA_DIR / "preferred-suppliers.csv",
        [{"supplier_id": s[0], "supplier_name": s[1], "category": s[2]} for s in PREFERRED_SUPPLIERS],
    )

    write_csv(DATA_DIR / "contract-documentation.csv", build_contract_documentation())

    policy = build_policy_rules()
    with open(DATA_DIR / "policy-rules.json", "w", encoding="utf-8") as f:
        json.dump(policy, f, indent=2)
    print(f"  policy-rules.json: 5 testable rules")

    print()
    print("Done. All files in practice/data/.")


if __name__ == "__main__":
    main()
