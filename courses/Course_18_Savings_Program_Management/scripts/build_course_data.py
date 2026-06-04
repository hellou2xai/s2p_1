"""Generate practice data for Course 18: Savings Program Management.

Scenario: $12M savings target across 8 initiatives at Apex Procurement.
Q3 close, CFO review next Tuesday. Students build savings tracking,
scenario modeling, and CFO memo generation.

Produces three files in practice/data/:
    sourcing-initiatives-log.csv (8 initiatives)
    q1-q3-transactions.csv (~437 rows tied to SAV-001 through SAV-005)
    market-benchmarks.md

The lessons quote specific numbers verbatim:
    SAV-001 (Steel Consolidation) realized = $1,760,193.65
    SAV-002 (Logistics RFP) realized = $747,564.68
    Total YTD realized across 8 initiatives = $6,855,835.67

This script hardcodes those per-initiative YTD values, then generates
transactions for SAV-001 through SAV-005 such that the sum of
(baseline_rate - rate_applied) * volume per initiative equals the
hardcoded YTD realized value, exactly. The lessons' worked examples
will reproduce on first run.

Deterministic via random.seed(42). All currency USD, US geography.
Run: py scripts/build_course_data.py
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"
DATA = PRACTICE / "data"

random.seed(42)
TODAY = date(2026, 4, 25)

# Hardcoded values pinned to the lessons. Do not change these without
# also updating the lessons and the HTML LMS.
INITIATIVES = [
    {
        "initiative_id": "SAV-001",
        "initiative_name": "Steel Consolidation",
        "category": "raw-materials",
        "owner": "Sarah Chen",
        "savings_type": "hard",
        "annual_target_usd": 2400000,
        "ytd_target_usd": 1800000.00,
        "ytd_realized_usd": 1760193.65,
        "variance_usd": -39806.35,
        "variance_pct": -2.2,
        "status": "on_track",
        "baseline_rate": 720,
        "negotiated_rate": 648,
        "unit": "per ton",
        "annual_volume": 14000,
    },
    {
        "initiative_id": "SAV-002",
        "initiative_name": "Logistics RFP",
        "category": "logistics",
        "owner": "Marcus Rivera",
        "savings_type": "hard",
        "annual_target_usd": 1800000,
        "ytd_target_usd": 1350000.00,
        "ytd_realized_usd": 747564.68,
        "variance_usd": -602435.32,
        "variance_pct": -44.6,
        "status": "at_risk",
        "baseline_rate": 3.20,
        "negotiated_rate": 2.72,
        "unit": "per mile",
        "annual_volume": 3750000,
    },
    {
        "initiative_id": "SAV-003",
        "initiative_name": "IT License Rationalization",
        "category": "it-services",
        "owner": "Priya Patel",
        "savings_type": "hard",
        "annual_target_usd": 1500000,
        "ytd_target_usd": 1125000.00,
        "ytd_realized_usd": 1018131.60,
        "variance_usd": -106868.40,
        "variance_pct": -9.5,
        "status": "on_track",
        "baseline_rate": 45,
        "negotiated_rate": 36,
        "unit": "per seat/month",
        "annual_volume": 14000,
    },
    {
        "initiative_id": "SAV-004",
        "initiative_name": "Facilities Rebid",
        "category": "facilities",
        "owner": "James Wright",
        "savings_type": "hard",
        "annual_target_usd": 1200000,
        "ytd_target_usd": 900000.00,
        "ytd_realized_usd": 670177.93,
        "variance_usd": -229822.07,
        "variance_pct": -25.5,
        "status": "on_track",
        "baseline_rate": 2.80,
        "negotiated_rate": 2.38,
        "unit": "per sq ft",
        "annual_volume": 2850000,
    },
    {
        "initiative_id": "SAV-005",
        "initiative_name": "Consulting Rate Card",
        "category": "professional-services",
        "owner": "Sarah Chen",
        "savings_type": "hard",
        "annual_target_usd": 1600000,
        "ytd_target_usd": 1200000.00,
        "ytd_realized_usd": 1196753.09,
        "variance_usd": -3246.91,
        "variance_pct": -0.3,
        "status": "on_track",
        "baseline_rate": 285,
        "negotiated_rate": 245,
        "unit": "per hour",
        "annual_volume": 40000,
    },
    {
        "initiative_id": "SAV-006",
        "initiative_name": "Demand Reduction (Travel)",
        "category": "travel",
        "owner": "Amanda Foster",
        "savings_type": "soft",
        "annual_target_usd": 800000,
        "ytd_target_usd": 600000.00,
        "ytd_realized_usd": 261203.94,
        "variance_usd": -338796.06,
        "variance_pct": -56.5,
        "status": "behind",
        "baseline_rate": 0,
        "negotiated_rate": 0,
        "unit": "annual",
        "annual_volume": 0,
    },
    {
        "initiative_id": "SAV-007",
        "initiative_name": "Spec Standardization",
        "category": "raw-materials",
        "owner": "Tom Baker",
        "savings_type": "cost_avoidance",
        "annual_target_usd": 1400000,
        "ytd_target_usd": 1050000.00,
        "ytd_realized_usd": 502357.71,
        "variance_usd": -547642.29,
        "variance_pct": -52.2,
        "status": "behind",
        "baseline_rate": 0,
        "negotiated_rate": 0,
        "unit": "annual",
        "annual_volume": 0,
    },
    {
        "initiative_id": "SAV-008",
        "initiative_name": "Payment Terms Extension",
        "category": "all",
        "owner": "Elena Rodriguez",
        "savings_type": "working_capital",
        "annual_target_usd": 1300000,
        "ytd_target_usd": 975000.00,
        "ytd_realized_usd": 699453.07,
        "variance_usd": -275546.93,
        "variance_pct": -28.3,
        "status": "on_track",
        "baseline_rate": 0,
        "negotiated_rate": 0,
        "unit": "annual",
        "annual_volume": 0,
    },
]

LOG_FIELDS = [
    "initiative_id",
    "initiative_name",
    "category",
    "owner",
    "savings_type",
    "annual_target_usd",
    "ytd_target_usd",
    "ytd_realized_usd",
    "variance_usd",
    "variance_pct",
    "status",
    "baseline_rate",
    "negotiated_rate",
    "unit",
]

TXN_FIELDS = [
    "transaction_id",
    "date",
    "initiative_id",
    "initiative_name",
    "category",
    "rate_applied",
    "baseline_rate",
    "volume",
    "amount_usd",
    "savings_usd",
]


def build_initiatives_log_rows():
    """Return the 8 initiative rows in LOG_FIELDS order."""
    return [{k: init[k] for k in LOG_FIELDS} for init in INITIATIVES]


def build_transactions_for_initiative(init, target_savings, n_txns, txn_start):
    """Generate n_txns transactions for one hard-savings initiative whose
    per-transaction (baseline - rate_applied) * volume sums to target_savings,
    with rate_applied <= baseline_rate on every row (no negative deltas).

    Strategy:
    - Pick volumes per row from a wide band around the average volume.
    - Generate random raw "savings weights" for every row, where every row
      carries some savings (no compliance-gap zero rows that could push
      rate above baseline).
    - Mix in a small share of "low-savings" rows (5 percent variance) so the
      data still looks like real procurement noise without creating any
      negative deltas.
    - Scale weights so the sum hits target_savings exactly.
    - Compute rate_applied = baseline - (per_row_savings / volume).
    - Adjust the last row to absorb rounding drift and hit the cent.
    """
    baseline = init["baseline_rate"]
    negotiated = init["negotiated_rate"]
    full_delta = baseline - negotiated  # max realistic per-unit savings

    # Date assignment: spread evenly across Q1 through Q3 2026.
    q1_start = date(2026, 1, 1)
    end = date(2026, 9, 30)
    days_range = (end - q1_start).days
    dates = []
    for i in range(n_txns):
        offset = int(days_range * i / max(n_txns - 1, 1))
        # Add a small random jitter for realism (still inside Q1-Q3 2026).
        jitter = random.randint(-3, 3)
        d = q1_start + timedelta(days=max(0, min(days_range, offset + jitter)))
        dates.append(d)

    # Volume per row: pick an average volume that, paired with the negotiated
    # delta band (about 0.95 * full_delta on average), produces the YTD
    # target. This keeps rate_applied inside the realistic 60 to 95 percent
    # of baseline range across all initiatives. We then jitter each row by
    # +/- 30 percent for variety.
    target_per_row = target_savings / n_txns
    avg_vol = target_per_row / (full_delta * 0.95) if full_delta > 0 else 1.0
    volumes = [round(avg_vol * random.uniform(0.7, 1.3), 2) for _ in range(n_txns)]
    volumes = [v if v > 0 else 1.0 for v in volumes]

    # Raw savings weights. Every row carries savings, but with realistic
    # variance: most rows in the negotiated band, a handful "partial wins"
    # at 30 to 60 percent of the negotiated savings (slow rollout, mixed
    # compliance, etc.), and a couple of "stretch wins" slightly above.
    weights = []
    for _ in range(n_txns):
        roll = random.random()
        if roll < 0.15:
            # Partial win: smaller per-unit delta (compliance ramp-up).
            w = random.uniform(0.30, 0.60)
        elif roll < 0.90:
            # Negotiated band.
            w = random.uniform(0.85, 1.10)
        else:
            # Stretch: slightly better than negotiated.
            w = random.uniform(1.10, 1.25)
        weights.append(w)

    # Convert weights to per-row savings totals: weight * volume * full_delta.
    # Then scale the whole vector so the sum equals target_savings.
    raw_savings = [w * v * full_delta for w, v in zip(weights, volumes)]
    raw_sum = sum(raw_savings)
    scale = target_savings / raw_sum
    per_row_savings = [s * scale for s in raw_savings]

    # Build the rows.
    rows = []
    txn_id = txn_start
    for i in range(n_txns):
        volume = volumes[i]
        savings = per_row_savings[i]
        rate = baseline - (savings / volume)

        # Guardrail: rate must stay positive and at or below baseline.
        # By construction it is below baseline (savings > 0). The lower
        # bound just protects against pathological random draws.
        if rate < baseline * 0.5:
            rate = baseline * 0.5
            savings = (baseline - rate) * volume

        savings = round((baseline - rate) * volume, 2)
        rate_rounded = round(rate, 4)

        # Amount-per-unit conventions: per-seat/month is reported daily in
        # this dataset, so divide by 30 for the amount line.
        if init["unit"] == "per seat/month":
            amount = round(rate_rounded * volume / 30, 2)
        else:
            amount = round(rate_rounded * volume, 2)

        rows.append({
            "transaction_id": f"TXN{txn_id:06d}",
            "date": dates[i].isoformat(),
            "initiative_id": init["initiative_id"],
            "initiative_name": init["initiative_name"],
            "category": init["category"],
            "rate_applied": rate_rounded,
            "baseline_rate": baseline,
            "volume": volume,
            "amount_usd": amount,
            "savings_usd": savings,
        })
        txn_id += 1

    # Reconcile to the cent on the last row by solving for volume given
    # a fixed (rounded) rate_applied. We use Decimal arithmetic to avoid
    # float drift on the closure step.
    from decimal import Decimal, ROUND_HALF_UP

    def fsum_decimal(rs):
        total = Decimal("0")
        for r in rs:
            total += (Decimal(str(r["baseline_rate"])) - Decimal(str(r["rate_applied"]))) * Decimal(str(r["volume"]))
        return total

    target_dec = Decimal(str(target_savings))

    # Step 1: adjust last row's rate to roughly close the gap.
    drift = float(target_dec - fsum_decimal(rows))
    if abs(drift) > 0.005:
        last = rows[-1]
        new_delta = (last["baseline_rate"] - last["rate_applied"]) + drift / last["volume"]
        new_rate = round(last["baseline_rate"] - new_delta, 4)
        if new_rate >= last["baseline_rate"]:
            new_rate = last["baseline_rate"] - 0.0001
        if new_rate < last["baseline_rate"] * 0.5:
            new_rate = round(last["baseline_rate"] * 0.5, 4)
        last["rate_applied"] = new_rate

    # Step 2: solve for last-row volume so the Decimal formula sum hits target.
    last = rows[-1]
    baseline_dec = Decimal(str(last["baseline_rate"]))
    rate_dec = Decimal(str(last["rate_applied"]))
    delta_dec = baseline_dec - rate_dec
    if delta_dec > 0:
        sum_others = fsum_decimal(rows[:-1])
        needed = target_dec - sum_others
        # Solve volume to 2 decimal places.
        new_volume_dec = (needed / delta_dec).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if new_volume_dec > 0:
            last["volume"] = float(new_volume_dec)

    # Step 3: with rate at 4dp and volume at 2dp, residual is at most a few
    # millicents. Absorb it into rate_applied at 8dp on the last row so the
    # exact formula sum matches target_savings to the cent.
    last = rows[-1]
    sum_others = fsum_decimal(rows[:-1])
    needed = target_dec - sum_others
    vol_dec = Decimal(str(last["volume"]))
    if vol_dec > 0:
        # rate_applied = baseline - (needed / volume), to 8dp.
        exact_rate = (baseline_dec - needed / vol_dec).quantize(
            Decimal("0.00000001"), rounding=ROUND_HALF_UP
        )
        last["rate_applied"] = float(exact_rate)

    # Recompute savings_usd and amount_usd on the last row for consistency.
    last = rows[-1]
    delta_final = last["baseline_rate"] - last["rate_applied"]
    last["savings_usd"] = round(delta_final * last["volume"], 2)
    if init["unit"] == "per seat/month":
        last["amount_usd"] = round(last["rate_applied"] * last["volume"] / 30, 2)
    else:
        last["amount_usd"] = round(last["rate_applied"] * last["volume"], 2)

    return rows, txn_id


def build_transactions():
    """Return all transactions across SAV-001 through SAV-005, ~437 rows."""
    # Per-initiative transaction counts that total 437.
    counts = {
        "SAV-001": 95,
        "SAV-002": 92,
        "SAV-003": 84,
        "SAV-004": 80,
        "SAV-005": 86,
    }
    all_rows = []
    txn_id = 50001
    for init in INITIATIVES[:5]:
        n = counts[init["initiative_id"]]
        target = init["ytd_realized_usd"]
        rows, txn_id = build_transactions_for_initiative(init, target, n, txn_id)
        all_rows.extend(rows)
    all_rows.sort(key=lambda r: r["date"])
    return all_rows


def build_market_benchmarks():
    return """# Market Benchmarks: Q3 2026

## Steel
- Hot rolled coil: $695-720/ton (down 2% from Q2)
- Cold rolled: $820-860/ton (flat)
- Industry average reduction in 2026 RFPs: 6-9%

## Logistics
- Truckload contract rates: $2.65-3.10/mile (up 4% YoY)
- LTL rates: up 5-7% YoY
- Diesel surcharge: 18-22% of base rate

## IT Services
- Cloud hosting: $32-42/seat/month (down 5% YoY)
- Managed services: flat to +2%
- Cybersecurity: up 10-15%

## Professional Services
- Management consulting: $250-320/hour (Big 4 range)
- Staffing: $55-85/hour (mid-market)
- Legal: $280-450/hour (specialty)

## Facilities
- Janitorial: $2.20-2.80/sq ft (stable)
- HVAC maintenance: $2.50-3.20/sq ft (up 3%)
- Security: $18-25/hour (up 5%)
"""


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.name}: {len(rows)} rows")


def main():
    print("Building Course 18 practice data...")
    print()

    DATA.mkdir(parents=True, exist_ok=True)
    (PRACTICE / "Drafts").mkdir(parents=True, exist_ok=True)

    write_csv(DATA / "sourcing-initiatives-log.csv", build_initiatives_log_rows(), LOG_FIELDS)

    txns = build_transactions()
    write_csv(DATA / "q1-q3-transactions.csv", txns, TXN_FIELDS)

    with open(DATA / "market-benchmarks.md", "w", encoding="utf-8") as f:
        f.write(build_market_benchmarks())
    print("  market-benchmarks.md: benchmark reference")

    # Verify per-initiative formula sums match the log.
    # Lessons compute: sum((baseline_rate - rate_applied) * volume) per initiative.
    print()
    print("Verification: formula sum (baseline_rate - rate_applied) * volume vs lesson target")
    print(f"  {'Initiative':<10} {'Lesson target':>16} {'Formula sum':>16}  Status")
    formula_sums = {}
    neg_rows = 0
    for r in txns:
        delta = r["baseline_rate"] - r["rate_applied"]
        formula_sums[r["initiative_id"]] = formula_sums.get(r["initiative_id"], 0) + delta * r["volume"]
        if delta < 0:
            neg_rows += 1
    formula_total = 0.0
    for init in INITIATIVES:
        target = init["ytd_realized_usd"]
        if init["initiative_id"] in formula_sums:
            actual = round(formula_sums[init["initiative_id"]], 2)
            ok = "OK" if abs(actual - target) < 0.005 else "MISMATCH"
            print(f"  {init['initiative_id']:<10} {target:>16,.2f} {actual:>16,.2f}  [{ok}]")
            formula_total += actual
        else:
            # Soft / cost-avoidance / working-capital initiatives have no
            # transaction rows in this dataset; their YTD realized is taken
            # from the initiatives log directly.
            print(f"  {init['initiative_id']:<10} {target:>16,.2f} {'(log only)':>16}  [N/A]")
            formula_total += target

    print(f"  {'TOTAL':<10} {sum(i['ytd_realized_usd'] for i in INITIATIVES):>16,.2f} {formula_total:>16,.2f}")
    print(f"  Rows with rate_applied > baseline_rate: {neg_rows}")

    print()
    print("Done. All files in practice/data/")


if __name__ == "__main__":
    main()
