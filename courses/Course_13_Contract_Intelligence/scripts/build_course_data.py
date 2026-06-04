"""Generate the practice data set for Course 13: Contract Intelligence.

Scenario: Vanguard Manufacturing, US-based industrial company, $42M annual
procurement spend. The Contract Intelligence Lead inherits 180 active
agreements. The student works with a representative sample of 20.

Practice data:
  - 20 contract markdown files (descriptive filenames keyed to supplier and type)
  - contract-register.csv: starter register, 8 of 20 with 3 carrying outdated values
  - clause-taxonomy.csv: 17 clause types with risk weights

Today's date: 2026-04-25. All currency USD, US geography.

The shape of the data matches the HTML LMS handout for this course
(Course_13_Contract_Intelligence_LMS.html). The supplier names, contract
filenames, and field set are the ones the lessons reference verbatim.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"
TODAY = date(2026, 4, 25)

# ----------------------------------------------------------------------------
# Clause taxonomy
# ----------------------------------------------------------------------------

CLAUSE_TYPES = [
    ("term_and_renewal", "Term and Renewal", "high"),
    ("payment", "Payment", "high"),
    ("liability_cap", "Liability Cap", "high"),
    ("indemnification", "Indemnification", "high"),
    ("termination_notice", "Termination Notice", "high"),
    ("force_majeure", "Force Majeure", "medium"),
    ("confidentiality", "Confidentiality", "medium"),
    ("ip_rights", "IP Rights", "high"),
    ("insurance", "Insurance", "medium"),
    ("service_levels", "Service Levels", "high"),
    ("dispute_resolution", "Dispute Resolution", "low"),
    ("assignment", "Assignment and Subcontracting", "medium"),
    ("compliance", "Regulatory Compliance", "high"),
    ("audit_rights", "Audit Rights", "medium"),
    ("reporting", "Reporting", "medium"),
    ("business_review", "Business Review", "medium"),
    ("data_protection", "Data Protection", "high"),
]

# ----------------------------------------------------------------------------
# 20 contracts. Hardcoded for deterministic regeneration. Distribution:
#   Raw materials (5)        $3.2M annual
#   IT services (4)          $2.4M annual
#   Facilities (4)           $1.8M annual
#   Logistics (4)            $1.6M annual
#   Professional services (3) $0.8M annual
# Renewal escalation (today 2026-04-25):
#   2 red    (<= 30 days to expiry)
#   3 amber  (31 to 60 days)
#   4 yellow (61 to 90 days)
#   11 green (> 90 days)
# ----------------------------------------------------------------------------

CONTRACTS = [
    # Raw materials (5)
    {
        "id": "CTR-2025-001", "sup_id": "SUP001",
        "supplier": "Great Lakes Steel", "category": "raw-materials",
        "type": "MSA", "effective": "2024-09-15", "expiry": "2027-09-15",
        "term_months": 36, "annual_value": 700000,
        "payment_terms": "Net 45", "auto_renewal": True, "notice_days": 90,
        "liability_cap": "$2,000,000", "governing_law": "Ohio",
        "scope": "Supply of hot-rolled and cold-rolled steel coil, plate, and structural shapes for the Vanguard Greenville assembly plant.",
    },
    {
        "id": "CTR-2025-002", "sup_id": "SUP002",
        "supplier": "Heartland Polymers", "category": "raw-materials",
        "type": "MSA", "effective": "2025-05-22", "expiry": "2026-05-22",
        "term_months": 12, "annual_value": 650000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 30,
        "liability_cap": "Twelve months of fees paid", "governing_law": "Indiana",
        "scope": "Supply of injection-grade polypropylene and ABS resin for component molding.",
    },
    {
        "id": "CTR-2025-003", "sup_id": "SUP003",
        "supplier": "Pacific Aluminum", "category": "raw-materials",
        "type": "MSA", "effective": "2026-01-10", "expiry": "2028-01-09",
        "term_months": 24, "annual_value": 600000,
        "payment_terms": "Net 30", "auto_renewal": False, "notice_days": 60,
        "liability_cap": "$1,500,000", "governing_law": "California",
        "scope": "Supply of 6061 and 7075 aluminum extrusions and sheet for the chassis line.",
    },
    {
        "id": "CTR-2025-004", "sup_id": "SUP004",
        "supplier": "Apex Electronics", "category": "raw-materials",
        "type": "SOW", "effective": "2025-04-01", "expiry": "2028-03-31",
        "term_months": 36, "annual_value": 700000,
        "payment_terms": "Net 60", "auto_renewal": False, "notice_days": 90,
        "liability_cap": "$3,000,000", "governing_law": "Texas",
        "scope": "Supply of printed circuit boards, sensors, and motor controllers for assembled product lines.",
    },
    {
        "id": "CTR-2025-005", "sup_id": "SUP005",
        "supplier": "Summit Metals", "category": "raw-materials",
        "type": "MSA", "effective": "2025-08-15", "expiry": "2027-08-15",
        "term_months": 24, "annual_value": 550000,
        "payment_terms": "Net 45", "auto_renewal": True, "notice_days": 60,
        "liability_cap": "$1,200,000", "governing_law": "Pennsylvania",
        "scope": "Supply of stainless steel fasteners, washers, and specialty hardware.",
    },
    # IT services (4)
    {
        "id": "CTR-2025-006", "sup_id": "SUP006",
        "supplier": "Northwind Office Ltd", "category": "it-services",
        "type": "MSA", "effective": "2025-07-01", "expiry": "2027-06-30",
        "term_months": 24, "annual_value": 142000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 90,
        "liability_cap": "Twelve months of fees paid", "governing_law": "Ohio",
        "scope": "Managed IT services covering helpdesk, endpoint management, and Microsoft 365 administration for Vanguard's office locations.",
    },
    {
        "id": "CTR-2025-007", "sup_id": "SUP007",
        "supplier": "TechForward Solutions", "category": "it-services",
        "type": "SLA", "effective": "2025-02-01", "expiry": "2028-01-31",
        "term_months": 36, "annual_value": 850000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 60,
        "liability_cap": "$2,500,000", "governing_law": "Ohio",
        "scope": "Hosting, monitoring, and 24x7 support for Vanguard's customer-facing web platform and order portal.",
    },
    {
        "id": "CTR-2025-008", "sup_id": "SUP008",
        "supplier": "CloudBridge Systems", "category": "it-services",
        "type": "SLA", "effective": "2025-12-01", "expiry": "2027-11-30",
        "term_months": 24, "annual_value": 750000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 90,
        "liability_cap": "$2,000,000", "governing_law": "Washington",
        "scope": "Cloud infrastructure, backup, and disaster recovery services for production ERP and MES systems.",
    },
    {
        "id": "CTR-2025-009", "sup_id": "SUP009",
        "supplier": "Pinnacle Software", "category": "it-services",
        "type": "MSA", "effective": "2024-06-10", "expiry": "2026-06-10",
        "term_months": 24, "annual_value": 658000,
        "payment_terms": "Net 30", "auto_renewal": False, "notice_days": 60,
        "liability_cap": "$1,500,000", "governing_law": "Massachusetts",
        "scope": "Enterprise license for plant scheduling and quality management software, including upgrades and patches.",
    },
    # Facilities (4)
    {
        "id": "CTR-2025-010", "sup_id": "SUP010",
        "supplier": "National Facilities Group", "category": "facilities",
        "type": "SOW", "effective": "2023-06-15", "expiry": "2026-06-15",
        "term_months": 36, "annual_value": 550000,
        "payment_terms": "Net 30", "auto_renewal": False, "notice_days": 90,
        "liability_cap": "$1,000,000", "governing_law": "Ohio",
        "scope": "Janitorial, landscaping, and HVAC preventive maintenance across three Vanguard sites in Ohio and Pennsylvania.",
    },
    {
        "id": "CTR-2025-011", "sup_id": "SUP011",
        "supplier": "Metro Building Services", "category": "facilities",
        "type": "MSA", "effective": "2025-07-10", "expiry": "2026-07-10",
        "term_months": 12, "annual_value": 500000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 30,
        "liability_cap": "$750,000", "governing_law": "Indiana",
        "scope": "Security guarding, access control monitoring, and visitor management at the Greenville plant.",
    },
    {
        "id": "CTR-2025-012", "sup_id": "SUP012",
        "supplier": "SafeGuard Fire Systems", "category": "facilities",
        "type": "SOW", "effective": "2023-07-22", "expiry": "2026-07-22",
        "term_months": 36, "annual_value": 450000,
        "payment_terms": "Net 45", "auto_renewal": False, "notice_days": 60,
        "liability_cap": "$1,500,000", "governing_law": "Ohio",
        "scope": "Inspection, testing, and maintenance of fire suppression and life safety systems across all Vanguard facilities.",
    },
    {
        "id": "CTR-2025-013", "sup_id": "SUP013",
        "supplier": "Beacon Property Management", "category": "facilities",
        "type": "MSA", "effective": "2024-11-01", "expiry": "2027-10-31",
        "term_months": 36, "annual_value": 300000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 90,
        "liability_cap": "$500,000", "governing_law": "Ohio",
        "scope": "Property management and tenant coordination for the leased corporate headquarters in Columbus, Ohio.",
    },
    # Logistics (4)
    {
        "id": "CTR-2025-014", "sup_id": "SUP014",
        "supplier": "Apex Logistics Inc", "category": "logistics",
        "type": "MSA", "effective": "2024-05-15", "expiry": "2026-05-15",
        "term_months": 24, "annual_value": 500000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 60,
        "liability_cap": "$1,000,000", "governing_law": "Illinois",
        "scope": "Inbound and outbound truckload freight across the Midwest manufacturing footprint, including expedited shipments.",
    },
    {
        "id": "CTR-2025-015", "sup_id": "SUP015",
        "supplier": "Continental Freight", "category": "logistics",
        "type": "MSA", "effective": "2025-06-20", "expiry": "2026-06-20",
        "term_months": 12, "annual_value": 450000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 30,
        "liability_cap": "$750,000", "governing_law": "Illinois",
        "scope": "Less-than-truckload and parcel consolidation services for the aftermarket distribution centers.",
    },
    {
        "id": "CTR-2025-016", "sup_id": "SUP016",
        "supplier": "Patriot Logistics", "category": "logistics",
        "type": "MSA", "effective": "2024-07-15", "expiry": "2026-07-15",
        "term_months": 24, "annual_value": 400000,
        "payment_terms": "Net 30", "auto_renewal": False, "notice_days": 60,
        "liability_cap": "$1,000,000", "governing_law": "Texas",
        "scope": "Dedicated dry van capacity for Gulf Coast routes and customs brokerage for cross-border shipments.",
    },
    {
        "id": "CTR-2025-017", "sup_id": "SUP017",
        "supplier": "Eagle Transport", "category": "logistics",
        "type": "MSA", "effective": "2025-10-01", "expiry": "2027-09-30",
        "term_months": 24, "annual_value": 250000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 60,
        "liability_cap": "$500,000", "governing_law": "Indiana",
        "scope": "Intra-plant yard moves, drayage, and short-haul shuttle service between the Greenville plant and the local distribution center.",
    },
    # Professional services (3)
    {
        "id": "CTR-2025-018", "sup_id": "SUP018",
        "supplier": "Whitfield Consulting", "category": "professional-services",
        "type": "SOW", "effective": "2024-07-01", "expiry": "2026-07-01",
        "term_months": 24, "annual_value": 350000,
        "payment_terms": "Net 30", "auto_renewal": False, "notice_days": 30,
        "liability_cap": "Twelve months of fees paid", "governing_law": "New York",
        "scope": "Strategy and operations consulting on the multi-year supply chain modernization program.",
    },
    {
        "id": "CTR-2025-019", "sup_id": "SUP019",
        "supplier": "Sterling Advisory", "category": "professional-services",
        "type": "SOW", "effective": "2025-09-01", "expiry": "2027-08-31",
        "term_months": 24, "annual_value": 250000,
        "payment_terms": "Net 30", "auto_renewal": False, "notice_days": 30,
        "liability_cap": "Twelve months of fees paid", "governing_law": "New York",
        "scope": "Tax advisory, transfer pricing review, and indirect tax compliance support.",
    },
    {
        "id": "CTR-2025-020", "sup_id": "SUP020",
        "supplier": "Crestline Accounting", "category": "professional-services",
        "type": "SOW", "effective": "2026-05-01", "expiry": "2028-04-30",
        "term_months": 24, "annual_value": 200000,
        "payment_terms": "Net 30", "auto_renewal": True, "notice_days": 60,
        "liability_cap": "Twelve months of fees paid", "governing_law": "Ohio",
        "scope": "External audit support, internal controls testing, and Sarbanes-Oxley remediation work.",
    },
]

# ----------------------------------------------------------------------------
# Obligations are pulled by category. Each contract gets four to seven.
# ----------------------------------------------------------------------------

OBLIGATIONS_BY_CATEGORY = {
    "raw-materials": [
        "Maintain ISO 9001 certification throughout the contract term",
        "Submit a Certificate of Analysis with every shipment",
        "Provide 90-day advance notice of any price change",
        "Hold a minimum of 30 days of safety stock at the supplier site",
        "Deliver a monthly on-time-in-full performance report by the fifth business day",
        "Notify Vanguard within 24 hours of any disruption to source materials",
    ],
    "it-services": [
        "Maintain SOC 2 Type II attestation throughout the contract term",
        "Report security incidents within 24 hours of detection",
        "Provide a quarterly business review presentation",
        "Maintain monthly system uptime of 99.5% or higher",
        "Submit a monthly service level report by the third business day",
        "Complete an annual penetration test and share remediation plan",
    ],
    "facilities": [
        "Maintain general liability insurance with Vanguard named as additional insured",
        "Submit monthly inspection reports for all serviced equipment",
        "Provide 48-hour advance notice for any planned site shutdown work",
        "Complete an annual safety audit by an independent third party",
        "Maintain OSHA compliance documentation on file",
        "Respond to emergency service requests within four hours",
    ],
    "logistics": [
        "Maintain motor carrier liability insurance of at least $1,000,000",
        "Provide real-time shipment tracking through the carrier portal",
        "Submit a monthly carrier scorecard covering on-time delivery and damage rates",
        "Notify Vanguard within two hours of any delivery exception",
        "Complete an annual rate review and benchmark submission",
        "Maintain valid DOT and FMCSA registrations throughout the term",
    ],
    "professional-services": [
        "Submit monthly time and expense reports by the fifth business day",
        "Provide quarterly status reviews to the Vanguard sponsor",
        "Maintain professional liability insurance of at least $2,000,000",
        "Complete annual conflict-of-interest disclosure",
        "Notify Vanguard of any change in lead consultant within five business days",
        "Provide updated firm financial statements annually",
    ],
}

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def filename_for(c) -> str:
    safe = c["supplier"].replace(" ", "_").replace(",", "").replace(".", "")
    return f"{c['type']}_{safe}.md"


def total_value(c) -> int:
    return int(c["annual_value"] * c["term_months"] / 12)


def status_for(c) -> str:
    expiry = date.fromisoformat(c["expiry"])
    if expiry < TODAY:
        return "expired"
    if (expiry - TODAY).days <= 90:
        return "expiring_soon"
    return "active"


def risk_for(c) -> str:
    days = (date.fromisoformat(c["expiry"]) - TODAY).days
    if days <= 60:
        return "High"
    if days <= 365:
        return "Medium"
    return "Low"


def fmt_money(n: int) -> str:
    return f"${n:,}"


# ----------------------------------------------------------------------------
# Contract markdown
# ----------------------------------------------------------------------------

def build_contract_markdown(c) -> str:
    annual = c["annual_value"]
    total = total_value(c)
    parts = []
    parts.append(f"# {c['type']}: {c['supplier']}")
    parts.append("")
    parts.append("## Parties")
    parts.append("")
    parts.append(
        f"This Agreement is entered into between Vanguard Manufacturing Inc. "
        f"(\"Buyer\") and {c['supplier']} (\"Supplier\")."
    )
    parts.append("")
    parts.append("## Recitals")
    parts.append("")
    parts.append(c["scope"])
    parts.append("")
    parts.append("## Term")
    parts.append("")
    parts.append(
        f"Effective date: {c['effective']}. Expiry date: {c['expiry']}. "
        f"Term: {c['term_months']} months. "
        f"Auto-renewal: {'yes' if c['auto_renewal'] else 'no'}. "
        f"Notice period: {c['notice_days']} days."
    )
    parts.append("")
    parts.append("## Compensation")
    parts.append("")
    parts.append(
        f"Annual contract value: {fmt_money(annual)}. "
        f"Total contract value over the {c['term_months']}-month term: {fmt_money(total)}."
    )
    parts.append("")
    parts.append("## Payment")
    parts.append("")
    parts.append(
        f"Payment terms: {c['payment_terms']} from receipt of an undisputed invoice. "
        f"Invoices may be submitted monthly in arrears."
    )
    parts.append("")
    parts.append("## Service Levels")
    parts.append("")
    parts.append(
        "Supplier shall meet the service levels set out in Schedule A. Failure to "
        "meet a target for two consecutive measurement periods entitles Buyer to "
        "service credits as defined in Schedule A."
    )
    parts.append("")
    parts.append("## Termination")
    parts.append("")
    parts.append(
        f"Either party may terminate for convenience on {c['notice_days']} days' "
        "written notice. Either party may terminate for material breach if the "
        "breach is not cured within 30 days of written notice."
    )
    parts.append("")
    parts.append("## Confidentiality")
    parts.append("")
    parts.append(
        "Each party shall hold the other party's Confidential Information in "
        "confidence for a period of five years following expiry or termination."
    )
    parts.append("")
    parts.append("## Intellectual Property Rights")
    parts.append("")
    parts.append(
        "All deliverables and work product created specifically for Buyer under "
        "this Agreement are the property of Buyer. Supplier retains its pre-existing "
        "intellectual property."
    )
    parts.append("")
    parts.append("## Insurance Requirements")
    parts.append("")
    parts.append(
        "Supplier shall maintain commercial general liability insurance of at least "
        "$2,000,000 per occurrence and shall name Buyer as an additional insured."
    )
    parts.append("")
    parts.append("## Liability Cap")
    parts.append("")
    parts.append(
        f"Supplier's aggregate liability under this Agreement is capped at "
        f"{c['liability_cap']}, except for breaches of confidentiality, "
        "indemnification obligations, and gross negligence or willful misconduct."
    )
    parts.append("")
    parts.append("## Indemnification")
    parts.append("")
    parts.append(
        "Supplier shall indemnify and hold Buyer harmless from any third-party "
        "claims arising out of Supplier's negligence, willful misconduct, or "
        "infringement of third-party intellectual property rights."
    )
    parts.append("")
    parts.append("## Force Majeure")
    parts.append("")
    parts.append(
        "Neither party shall be liable for delays or failures caused by events "
        "beyond reasonable control, including natural disasters, governmental "
        "actions, or labor disruptions, provided the affected party gives prompt "
        "written notice."
    )
    parts.append("")
    parts.append("## Audit Rights")
    parts.append("")
    parts.append(
        "Buyer may audit Supplier's records relating to this Agreement on 14 days' "
        "written notice, no more than once per calendar year."
    )
    parts.append("")
    parts.append("## Governing Law")
    parts.append("")
    parts.append(
        f"This Agreement is governed by the laws of the State of {c['governing_law']}, "
        "without regard to conflict-of-law principles."
    )
    parts.append("")
    parts.append("## Obligations")
    parts.append("")
    obligations = OBLIGATIONS_BY_CATEGORY[c["category"]]
    pick_count = 4 + (sum(ord(ch) for ch in c["id"]) % 4)  # 4..7, deterministic
    for ob in obligations[:pick_count]:
        parts.append(f"- {ob}")
    parts.append("")
    parts.append("## Signatures")
    parts.append("")
    parts.append(f"Executed on {c['effective']}.")
    parts.append("")
    return "\n".join(parts)


# ----------------------------------------------------------------------------
# Starter contract-register.csv: 8 of 20 contracts, 3 with intentionally
# outdated values. The lesson teaches the student to reconcile the messy
# inherited register against the source contracts.
# ----------------------------------------------------------------------------

STARTER_REGISTER_IDS = [
    "CTR-2025-001",  # Great Lakes Steel        (outdated annual value)
    "CTR-2025-002",  # Heartland Polymers       (correct)
    "CTR-2025-006",  # Northwind Office Ltd     (correct)
    "CTR-2025-007",  # TechForward Solutions    (outdated end_date)
    "CTR-2025-009",  # Pinnacle Software        (correct)
    "CTR-2025-010",  # National Facilities Grp  (outdated annual value)
    "CTR-2025-014",  # Apex Logistics Inc       (correct)
    "CTR-2025-018",  # Whitfield Consulting     (correct)
]

REGISTER_OUTDATED_OVERRIDES = {
    "CTR-2025-001": {"annual_value_usd": 625000},          # was 700,000
    "CTR-2025-007": {"end_date": "2027-12-31"},            # actual is 2028-01-31
    "CTR-2025-010": {"annual_value_usd": 480000},          # was 550,000
}


def build_register_rows() -> list[dict]:
    rows = []
    for c in CONTRACTS:
        if c["id"] not in STARTER_REGISTER_IDS:
            continue
        row = {
            "contract_id": c["id"],
            "supplier_id": c["sup_id"],
            "supplier_name": c["supplier"],
            "category": c["category"],
            "contract_type": c["type"],
            "start_date": c["effective"],
            "end_date": c["expiry"],
            "annual_value_usd": c["annual_value"],
            "notice_period_days": c["notice_days"],
            "auto_renew": "yes" if c["auto_renewal"] else "no",
            "status": status_for(c),
            "risk_level": risk_for(c),
        }
        overrides = REGISTER_OUTDATED_OVERRIDES.get(c["id"])
        if overrides:
            row.update(overrides)
        rows.append(row)
    return rows


# ----------------------------------------------------------------------------
# Writers
# ----------------------------------------------------------------------------

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {path.relative_to(PRACTICE)}: {len(rows)} rows")


def main() -> None:
    print("Building Course 13 practice data...")
    print()

    contracts_dir = PRACTICE / "contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "intake").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "processed").mkdir(parents=True, exist_ok=True)

    # Clear any prior contract files so a rerun does not leave stale ones behind.
    for old in contracts_dir.glob("*.md"):
        old.unlink()

    register_rows = build_register_rows()
    write_csv(PRACTICE / "contract-register.csv", register_rows)

    taxonomy = [
        {"clause_type": c[0], "display_name": c[1], "risk_weight": c[2]}
        for c in CLAUSE_TYPES
    ]
    write_csv(PRACTICE / "clause-taxonomy.csv", taxonomy)

    for c in CONTRACTS:
        path = contracts_dir / filename_for(c)
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_contract_markdown(c))
    print(f"  contracts/: {len(CONTRACTS)} contract documents")

    print()
    print(f"Done. All files in {PRACTICE}")


if __name__ == "__main__":
    main()
