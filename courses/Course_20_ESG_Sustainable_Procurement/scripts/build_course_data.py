"""Generate practice data for Course 20: ESG and Sustainable Procurement.

Scenario: Fortis Manufacturing committed to Science Based Targets last quarter.
Sustainable Procurement Lead has 15 supplier ESG assessments. Ten complete,
five partial. Two suppliers (SUP003, SUP008) have red-flag scores below 40 on
one or more dimensions. Two suppliers (SUP006, SUP009) inflated their
self-scores to 90+ on dimensions where the industry benchmark is in the 50s.

Produces:
  practice/data/spend-by-supplier.csv     (15 suppliers)
  practice/data/esg-framework.csv         (6 dimensions)
  practice/data/esg-benchmarks.md         (industry averages, emission factors)
  practice/data/supplier-assessments/     (15 questionnaire .md files)

Deterministic: random.seed(42). All currency USD, US geography. Today is
2026-04-25. Lesson references in lessons/ are the contract; this script is
authored to match those references verbatim. Do not change supplier IDs,
names, spend, or emission factors without checking every lesson first.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"
DATA = PRACTICE / "data"
ASSESSMENTS = DATA / "supplier-assessments"

random.seed(42)
TODAY = date(2026, 4, 25)

# Supplier roster. Aligned with lesson references:
#  - SUP001 Great Lakes Steel: $4,200,000 (highest spender), raw materials.
#  - SUP003 Pacific Aluminum: red flag supplier (low scores).
#  - SUP008 Eagle Transport: red flag supplier (low scores), $520,000
#    (lowest spender per HTML overview).
#  - SUP006, SUP009: inflated self-score suppliers (90+ on benchmark-50s
#    dimensions).
# Categories: raw-materials, logistics, it-services, facilities,
# professional-services, components.
# Emission factor ranges per HTML LMS spec for Lesson 3:
#   raw-materials 0.7 to 1.0, logistics 1.0 to 1.5, components 0.6 to 0.9,
#   it-services 0.2 to 0.4, facilities 0.3 to 0.5, professional-services
#   0.1 to 0.3. SUP001 Great Lakes Steel is pinned at 0.8 because Lesson 3
#   step 5 uses it as the worked example. The HTML is the spec; the data
#   matches the spec verbatim. Do not editorialize toward "more realistic"
#   values without first checking every lesson reference.
SUPPLIERS = [
    ("SUP001", "Great Lakes Steel",      "raw-materials",         4_200_000, 0.8),
    ("SUP002", "Heartland Polymers",     "raw-materials",         3_800_000, 0.9),
    ("SUP003", "Pacific Aluminum",       "raw-materials",         3_100_000, 1.0),
    ("SUP004", "Continental Freight",    "logistics",             3_600_000, 1.2),
    ("SUP005", "Patriot Logistics",      "logistics",             2_900_000, 1.3),
    ("SUP006", "Summit Components",      "components",            2_400_000, 0.8),
    ("SUP007", "TechForward Solutions",  "it-services",           2_800_000, 0.3),
    ("SUP008", "Eagle Transport",        "logistics",               520_000, 1.4),
    ("SUP009", "National Facilities",    "facilities",            2_200_000, 0.4),
    ("SUP010", "Metro Building Svcs",    "facilities",            1_800_000, 0.4),
    ("SUP011", "Whitfield Consulting",   "professional-services", 2_600_000, 0.2),
    ("SUP012", "Cascade Fasteners",      "components",            1_800_000, 0.7),
    ("SUP013", "Summit Metals",          "raw-materials",         1_600_000, 0.9),
    ("SUP014", "Greenfield Maintenance", "facilities",            1_400_000, 0.3),
    ("SUP015", "SafeGuard Fire",         "facilities",              900_000, 0.5),
]

# Six ESG dimensions. Names match esg-framework.csv and CLAUDE.md weights.
ESG_DIMENSIONS = [
    ("environmental_management", "Environmental Management System",       20),
    ("carbon_emissions",         "Carbon Emissions and Reduction",        25),
    ("waste_management",         "Waste Management and Circular Economy", 15),
    ("labor_practices",          "Labor Practices and Human Rights",      15),
    ("diversity_inclusion",      "Diversity and Inclusion",               10),
    ("governance_ethics",        "Governance and Ethics",                 15),
]

# Industry benchmark scores per dimension. Lesson 2 step 3 says:
# "Carbon Emissions industry average might be 52, Environmental Management
# might be 58." We pin all six.
BENCHMARK_SCORES = {
    "environmental_management": 58,
    "carbon_emissions":         52,
    "waste_management":         54,
    "labor_practices":          61,
    "diversity_inclusion":      45,
    "governance_ethics":        57,
}

# Hardcoded scores per supplier for determinism. The lesson references are
# the contract for SUP003 (red flag), SUP008 Eagle Transport (Lesson 5 worked
# example uses ENV 42, Carbon 35, Waste 55, Labor 60, D&I 38, Gov 65), and
# SUP006/SUP009 (inflated self-scores at 90+).
# Five suppliers are partial (SUP011 to SUP015): one or more dimensions left
# blank to force benchmark substitution.

# None means the supplier did not answer that dimension (partial assessment).
SUPPLIER_SCORES = {
    "SUP001": {  # Great Lakes Steel: complete, mid-tier overall.
        "environmental_management": 65,
        "carbon_emissions":         58,
        "waste_management":         62,
        "labor_practices":          70,
        "diversity_inclusion":      55,
        "governance_ethics":        68,
    },
    "SUP002": {  # Heartland Polymers: complete, near-target.
        "environmental_management": 72,
        "carbon_emissions":         65,
        "waste_management":         70,
        "labor_practices":          75,
        "diversity_inclusion":      60,
        "governance_ethics":        72,
    },
    "SUP003": {  # Pacific Aluminum: red flag. Multiple dimensions below 40.
        "environmental_management": 38,
        "carbon_emissions":         32,
        "waste_management":         41,
        "labor_practices":          48,
        "diversity_inclusion":      35,
        "governance_ethics":        45,
    },
    "SUP004": {  # Continental Freight: complete, meets target.
        "environmental_management": 70,
        "carbon_emissions":         68,
        "waste_management":         72,
        "labor_practices":          74,
        "diversity_inclusion":      62,
        "governance_ethics":        71,
    },
    "SUP005": {  # Patriot Logistics: complete, approaching target.
        "environmental_management": 62,
        "carbon_emissions":         60,
        "waste_management":         65,
        "labor_practices":          68,
        "diversity_inclusion":      58,
        "governance_ethics":        66,
    },
    "SUP006": {  # Summit Components: inflated self-scores at 90+ on
                 # carbon and environmental dimensions where benchmarks are
                 # 52 and 58. Triggers the +30 inflated flag.
        "environmental_management": 92,
        "carbon_emissions":         95,
        "waste_management":         60,
        "labor_practices":          68,
        "diversity_inclusion":      55,
        "governance_ethics":        70,
    },
    "SUP007": {  # TechForward Solutions: complete, meets target overall.
        "environmental_management": 68,
        "carbon_emissions":         72,
        "waste_management":         70,
        "labor_practices":          78,
        "diversity_inclusion":      72,
        "governance_ethics":        75,
    },
    "SUP008": {  # Eagle Transport: red flag. Lesson 5 worked example pins
                 # these exact scores.
        "environmental_management": 42,
        "carbon_emissions":         35,
        "waste_management":         55,
        "labor_practices":          60,
        "diversity_inclusion":      38,
        "governance_ethics":        65,
    },
    "SUP009": {  # National Facilities: inflated self-scores at 90+ on
                 # diversity (benchmark 45) and waste (benchmark 54).
        "environmental_management": 65,
        "carbon_emissions":         58,
        "waste_management":         92,
        "labor_practices":          70,
        "diversity_inclusion":      90,
        "governance_ethics":        68,
    },
    "SUP010": {  # Metro Building Svcs: complete, approaching.
        "environmental_management": 60,
        "carbon_emissions":         55,
        "waste_management":         62,
        "labor_practices":          68,
        "diversity_inclusion":      52,
        "governance_ethics":        64,
    },
    "SUP011": {  # Whitfield Consulting: PARTIAL. Three dimensions blank.
        "environmental_management": None,
        "carbon_emissions":         None,
        "waste_management":         70,
        "labor_practices":          72,
        "diversity_inclusion":      None,
        "governance_ethics":        78,
    },
    "SUP012": {  # Cascade Fasteners: PARTIAL. Two dimensions blank.
        "environmental_management": 55,
        "carbon_emissions":         48,
        "waste_management":         None,
        "labor_practices":          62,
        "diversity_inclusion":      None,
        "governance_ethics":        60,
    },
    "SUP013": {  # Summit Metals: PARTIAL. One dimension blank.
        "environmental_management": 50,
        "carbon_emissions":         45,
        "waste_management":         52,
        "labor_practices":          None,
        "diversity_inclusion":      48,
        "governance_ethics":        55,
    },
    "SUP014": {  # Greenfield Maintenance: PARTIAL. Two dimensions blank.
        "environmental_management": 62,
        "carbon_emissions":         None,
        "waste_management":         58,
        "labor_practices":          65,
        "diversity_inclusion":      None,
        "governance_ethics":        67,
    },
    "SUP015": {  # SafeGuard Fire: PARTIAL. One dimension blank.
        "environmental_management": 58,
        "carbon_emissions":         50,
        "waste_management":         None,
        "labor_practices":          70,
        "diversity_inclusion":      48,
        "governance_ethics":        62,
    },
}

# Stable submission dates so regeneration produces the same files.
SUBMISSION_DATES = {
    "SUP001": date(2026, 3,  9),
    "SUP002": date(2026, 3, 15),
    "SUP003": date(2026, 3, 23),
    "SUP004": date(2026, 3, 28),
    "SUP005": date(2026, 4,  2),
    "SUP006": date(2026, 4,  4),
    "SUP007": date(2026, 4,  6),
    "SUP008": date(2026, 4,  8),
    "SUP009": date(2026, 4, 10),
    "SUP010": date(2026, 4, 12),
    "SUP011": date(2026, 4, 14),
    "SUP012": date(2026, 4, 16),
    "SUP013": date(2026, 4, 18),
    "SUP014": date(2026, 4, 20),
    "SUP015": date(2026, 4, 22),
}


def detail_lines(dim_id: str, score: int, sid: str) -> str:
    """Return a few narrative bullets that match the dimension and score."""
    rng = random.Random(hash((sid, dim_id)) & 0xFFFFFFFF)

    if dim_id == "environmental_management":
        return (
            f"- ISO 14001 certified: {'Yes' if score >= 60 else 'No'}\n"
            f"- Environmental policy published: {'Yes' if score >= 40 else 'No'}\n"
            f"- Annual environmental report: {'Yes' if score >= 70 else 'No'}\n\n"
        )
    if dim_id == "carbon_emissions":
        out = (
            f"- Scope 1 emissions reported: {'Yes' if score >= 50 else 'No'}\n"
            f"- Scope 2 emissions reported: {'Yes' if score >= 50 else 'No'}\n"
            f"- Reduction target set: {'Yes' if score >= 60 else 'No'}\n"
        )
        if score >= 60:
            out += f"- Reduction target: {rng.randint(10, 30)}% by 2030\n"
        return out + "\n"
    if dim_id == "waste_management":
        return (
            f"- Waste diversion rate: {rng.randint(20, 80)}%\n"
            f"- Circular economy commitments: {'Yes' if score >= 60 else 'No'}\n"
            f"- Hazardous waste tracking: {'Yes' if score >= 50 else 'No'}\n\n"
        )
    if dim_id == "labor_practices":
        return (
            f"- Living wage commitment: {'Yes' if score >= 60 else 'No'}\n"
            f"- Safety incident rate: {round(rng.uniform(0.5, 5.0), 1)} per 100 workers\n"
            f"- Modern slavery statement: {'Published' if score >= 50 else 'Not published'}\n\n"
        )
    if dim_id == "diversity_inclusion":
        return (
            f"- Diversity reporting: {'Annual' if score >= 60 else 'Not published'}\n"
            f"- Hiring targets set: {'Yes' if score >= 55 else 'No'}\n"
            f"- Pay equity audit: {'Yes' if score >= 65 else 'No'}\n\n"
        )
    if dim_id == "governance_ethics":
        return (
            f"- Anti-bribery policy: {'Yes' if score >= 40 else 'No'}\n"
            f"- Whistleblower mechanism: {'Yes' if score >= 55 else 'No'}\n"
            f"- Board ESG oversight: {'Yes' if score >= 70 else 'No'}\n\n"
        )
    return "Details provided in supplementary documentation.\n\n"


def build_assessment(sid: str, name: str, category: str, spend: int) -> str:
    submitted = SUBMISSION_DATES[sid].isoformat()
    out = f"# ESG Assessment: {name} ({sid})\n\n"
    out += f"**Submitted:** {submitted}\n"
    out += f"**Category:** {category}\n"
    out += f"**Annual Spend:** ${spend:,}\n\n"

    scores = SUPPLIER_SCORES[sid]
    for dim_id, dim_name, _ in ESG_DIMENSIONS:
        out += f"## {dim_name}\n\n"
        score = scores[dim_id]
        if score is None:
            out += "**Score:** Not provided\n\n"
            out += "*This section was not completed by the supplier.*\n\n"
        else:
            out += f"**Score:** {score}/100\n\n"
            out += detail_lines(dim_id, score, sid)
    return out


def build_spend_rows():
    rows = []
    for sid, name, cat, spend, ef in SUPPLIERS:
        rows.append({
            "supplier_id": sid,
            "supplier_name": name,
            "category": cat,
            "annual_spend_usd": spend,
            "emission_factor_kg_co2_per_usd": ef,
            "estimated_scope3_tons": round(spend * ef / 1000, 1),
        })
    return rows


def build_framework_rows():
    rows = []
    for dim_id, dim_name, weight in ESG_DIMENSIONS:
        rows.append({
            "dimension_id": dim_id,
            "dimension_name": dim_name,
            "weight_pct": weight,
            "minimum_threshold": 40,
            "target_score": 70,
        })
    return rows


def benchmarks_md() -> str:
    return """# ESG Benchmarks: Manufacturing Sector 2026

Source for Scope 3 emission factors: EPA Environmentally-Extended Input-Output
(EEIO) v1.1, scaled to 2026 USD. Source for industry score averages: Fortis
Manufacturing peer benchmarking study, Q4 2025 (n=84 US manufacturers).

## Industry average ESG scores by dimension

| Dimension | Industry average score |
|---|---|
| Environmental Management | 58 |
| Carbon Emissions and Reduction | 52 |
| Waste Management and Circular Economy | 54 |
| Labor Practices and Human Rights | 61 |
| Diversity and Inclusion | 45 |
| Governance and Ethics | 57 |

Use these averages to fill missing dimensions in partial assessments. Mark
any substituted score as "estimated" in every output.

Inflated self-score rule: any supplier-reported score more than 30 points
above the dimension benchmark is flagged for review.

## Environmental indicators

- Average ISO 14001 certification rate: 62 percent (up from 55 percent in 2024)
- Average Scope 1+2 emissions reduction target: 25 percent by 2030
- Top quartile carbon intensity: below 0.5 kg CO2 per USD spend

## Social indicators

- Industry average safety incident rate: 2.8 per 100 workers
- Living wage adoption rate: 45 percent of major suppliers
- Diversity reporting rate: 38 percent of manufacturing suppliers

## Governance indicators

- Anti-bribery policy adoption: 78 percent of suppliers over $1M annual spend
- Whistleblower mechanism: 55 percent of suppliers
- Board ESG oversight: 32 percent of suppliers

## Scope 3 emission factors (spend-based method)

Source: EPA EEIO v1.1, USD 2026.

| Category | Emission factor (kg CO2 per USD) |
|---|---|
| Raw materials | 0.7 to 1.0 |
| Logistics | 1.0 to 1.5 |
| Components | 0.6 to 0.9 |
| IT services | 0.2 to 0.4 |
| Facilities management | 0.3 to 0.5 |
| Professional services | 0.1 to 0.3 |

## Science Based Targets Initiative (SBTi)

- 1.5C pathway requires 4.2 percent annual Scope 3 reduction.
- Current supplier portfolio baseline: establish in Year 1.
- First reduction targets due: end of Year 2.
"""


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.relative_to(ROOT)}: {len(rows)} rows")


def clear_assessments():
    if ASSESSMENTS.exists():
        for old in ASSESSMENTS.glob("*.md"):
            old.unlink()


def main():
    print("Building Course 20 practice data...")
    print()

    DATA.mkdir(parents=True, exist_ok=True)
    ASSESSMENTS.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "Drafts").mkdir(parents=True, exist_ok=True)
    (PRACTICE / "Outputs").mkdir(parents=True, exist_ok=True)

    write_csv(DATA / "spend-by-supplier.csv", build_spend_rows())
    write_csv(DATA / "esg-framework.csv", build_framework_rows())

    with open(DATA / "esg-benchmarks.md", "w", encoding="utf-8") as f:
        f.write(benchmarks_md())
    print(f"  practice/data/esg-benchmarks.md")

    clear_assessments()
    complete_count = 0
    partial_count = 0
    for sid, name, cat, spend, _ in SUPPLIERS:
        content = build_assessment(sid, name, cat, spend)
        out_path = ASSESSMENTS / f"assessment-{sid}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        if any(v is None for v in SUPPLIER_SCORES[sid].values()):
            partial_count += 1
        else:
            complete_count += 1
    print(
        f"  practice/data/supplier-assessments/: 15 files "
        f"({complete_count} complete, {partial_count} partial)"
    )

    print()
    print(f"Done. Today: {TODAY.isoformat()}.")


if __name__ == "__main__":
    main()
