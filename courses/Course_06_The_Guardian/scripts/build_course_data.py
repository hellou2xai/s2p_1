"""Generate the practice data set for Course 6: The Guardian.

Scenario: Sentinel Contract Services, a US-based contract management firm.
The automated contract review pipeline produces reports with missing clauses
and incorrect risk levels. Students build PreToolUse and PostToolUse hooks
to validate report structure before saving and log every tool call.

Produces a flat practice/ folder:
- data/ holds: contracts/ (12 contract review .md files, mix of valid and
  intentionally flawed), contract-register.csv (30 contracts),
  clause-taxonomy.csv (standard clause categories)
- hooks/ is empty: the student writes hook scripts here
- alerts/ is empty: risk alert hook writes here
- audit/ is empty: audit log hook writes here
- outputs/ is empty: validated reports land here

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


# ---------------------------------------------------------------------------
# Contract register (30 contracts)
# ---------------------------------------------------------------------------

SUPPLIERS = [
    ("SUP001", "Great Lakes Steel", "raw-materials", "strategic"),
    ("SUP002", "Heartland Polymers", "raw-materials", "strategic"),
    ("SUP003", "Pacific Aluminum", "raw-materials", "strategic"),
    ("SUP004", "Apex Electronics", "raw-materials", "preferred"),
    ("SUP005", "Cascade Fasteners", "raw-materials", "preferred"),
    ("SUP011", "Continental Freight", "logistics", "strategic"),
    ("SUP012", "Patriot Logistics", "logistics", "strategic"),
    ("SUP013", "Eagle Transport", "logistics", "preferred"),
    ("SUP014", "Horizon Carriers", "logistics", "preferred"),
    ("SUP021", "TechForward Solutions", "it-services", "strategic"),
    ("SUP022", "CloudBridge Systems", "it-services", "strategic"),
    ("SUP023", "Nexus IT Services", "it-services", "preferred"),
    ("SUP031", "National Facilities Group", "facilities", "strategic"),
    ("SUP032", "Metro Building Services", "facilities", "strategic"),
    ("SUP041", "Whitfield Consulting", "professional-services", "strategic"),
    ("SUP042", "Sterling Advisory", "professional-services", "strategic"),
]

RISK_LEVELS = ["Low", "Medium", "High", "Critical"]

CLAUSE_TYPES = [
    "term_and_renewal",
    "payment_terms",
    "liability_cap",
    "indemnification",
    "termination_for_convenience",
    "termination_for_cause",
    "force_majeure",
    "confidentiality",
    "intellectual_property",
    "insurance_requirements",
    "service_level_agreement",
    "dispute_resolution",
]


def build_contract_register():
    """30 contracts with varying statuses and dates."""
    rows = []
    for i in range(30):
        sup = SUPPLIERS[i % len(SUPPLIERS)]
        cid = f"CTR-2025-{i + 1:03d}"
        start = TODAY - timedelta(days=random.randint(180, 730))
        end = start + timedelta(days=random.choice([365, 730, 1095]))
        annual_value = random.randint(50, 500) * 10000

        if end < TODAY:
            status = "expired"
        elif (end - TODAY).days <= 90:
            status = "expiring_soon"
        else:
            status = "active"

        rows.append({
            "contract_id": cid,
            "supplier_id": sup[0],
            "supplier_name": sup[1],
            "category": sup[2],
            "tier": sup[3],
            "contract_type": random.choice(["MSA", "SOW", "NDA", "SLA", "amendment"]),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "annual_value_usd": annual_value,
            "status": status,
            "auto_renew": random.choice(["yes", "no"]),
            "risk_level": random.choice(RISK_LEVELS),
        })
    return rows


def build_clause_taxonomy():
    """Standard clause categories with required fields."""
    rows = []
    for clause in CLAUSE_TYPES:
        rows.append({
            "clause_type": clause,
            "display_name": clause.replace("_", " ").title(),
            "required_in": "MSA,SOW,SLA" if clause in [
                "term_and_renewal", "payment_terms", "liability_cap",
                "termination_for_convenience", "termination_for_cause",
            ] else "MSA",
            "risk_weight": random.choice(["high", "medium", "low"]),
        })
    return rows


def build_contract_reviews(contracts):
    """12 contract review reports. Some are valid, some have intentional flaws
    that the PreToolUse hook should catch."""
    reviews = []
    selected = contracts[:12]

    for i, c in enumerate(selected):
        cid = c["contract_id"]
        supplier = c["supplier_name"]
        risk = c["risk_level"]

        # Required sections for a valid report
        sections = {
            "parties": f"**Parties:** Sentinel Contract Services (Buyer) and {supplier} (Supplier).",
            "term": f"**Term:** {c['start_date']} to {c['end_date']}. Auto-renew: {c['auto_renew']}.",
            "value": f"**Annual Value:** ${c['annual_value_usd']:,}.",
            "risk_assessment": f"**Risk Level:** {risk}.",
            "key_clauses": "**Key Clauses:**\n" + "\n".join(
                [f"- {ct.replace('_', ' ').title()}: Present and standard."
                 for ct in random.sample(CLAUSE_TYPES, random.randint(6, 10))]
            ),
            "missing_clauses": "**Missing Clauses:** None identified.",
            "recommendation": f"**Recommendation:** Renew with standard terms. Next review by {(TODAY + timedelta(days=90)).isoformat()}.",
        }

        # Introduce flaws in specific reports
        flaws = []
        if i == 2:
            # Missing risk assessment section
            del sections["risk_assessment"]
            flaws.append("missing_risk_assessment")
        if i == 5:
            # Invalid risk level value
            sections["risk_assessment"] = "**Risk Level:** Extreme."
            flaws.append("invalid_risk_level")
        if i == 7:
            # Missing supplier name (empty parties)
            sections["parties"] = "**Parties:** Sentinel Contract Services (Buyer) and (Supplier)."
            flaws.append("missing_supplier_name")
        if i == 9:
            # Missing key clauses section
            del sections["key_clauses"]
            flaws.append("missing_key_clauses")
        if i == 10:
            # High risk but no recommendation
            sections["risk_assessment"] = "**Risk Level:** Critical."
            del sections["recommendation"]
            flaws.append("high_risk_no_recommendation")
        if i == 11:
            # Empty clause references
            sections["key_clauses"] = "**Key Clauses:**\n(none reviewed)"
            flaws.append("empty_clause_references")

        content = f"# Contract Review: {cid}\n\n"
        content += f"**Reviewed:** {TODAY.isoformat()}\n\n"
        for section_content in sections.values():
            content += section_content + "\n\n"

        reviews.append({
            "filename": f"review-{cid}.md",
            "content": content,
            "contract_id": cid,
            "has_flaws": len(flaws) > 0,
            "flaws": flaws,
        })

    return reviews


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
    print("Building Course 06 practice data...")
    print()

    # Create directories
    data_dir = PRACTICE / "data"
    contracts_dir = data_dir / "contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "outputs").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "hooks").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "alerts").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "audit").mkdir(parents=True, exist_ok=True)

    # Build contract register
    contracts = build_contract_register()
    write_csv(data_dir / "contract-register.csv", contracts)

    # Build clause taxonomy
    taxonomy = build_clause_taxonomy()
    write_csv(data_dir / "clause-taxonomy.csv", taxonomy)

    # Build contract review files (12 files, some with intentional flaws)
    reviews = build_contract_reviews(contracts)
    for r in reviews:
        filepath = contracts_dir / r["filename"]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(r["content"])
    print(f"  contracts/: {len(reviews)} review files ({sum(1 for r in reviews if r['has_flaws'])} with planted flaws)")

    # Write a manifest of which files have flaws (for the solutions folder)
    manifest_path = ROOT / "solutions" / "flaw-manifest.md"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("# Planted Flaws in Contract Reviews\n\n")
        f.write("This file lists which contract reviews have intentional flaws.\n")
        f.write("The PreToolUse validation hook should catch all of these.\n\n")
        f.write("| File | Flaws |\n")
        f.write("|---|---|\n")
        for r in reviews:
            if r["has_flaws"]:
                f.write(f"| {r['filename']} | {', '.join(r['flaws'])} |\n")
    print(f"  solutions/flaw-manifest.md: flaw reference")

    print()
    print("Done. All files in practice/data/")


if __name__ == "__main__":
    main()
