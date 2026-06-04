# Skill: Score Bid Response

## Purpose

Read the bid files in `Master/bid-responses/`, score each supplier against the weighted evaluation criteria from `CLAUDE.md`, and write a scorecard to `Drafts/`. This skill works across sourcing events because it names input shapes, not specific values. Swap the data and the weights, and the same skill scores a different event.

## When to use

- After all bids have arrived in `Master/bid-responses/`.
- When you need a consistent, repeatable scoring pass across multiple suppliers.
- When the evaluation weights live in `CLAUDE.md` and may change between events.

## Inputs

1. `Master/bid-responses/`: one pricing CSV (`bid_pricing_<Supplier>.csv`) and one technical CSV (`bid_technical_<Supplier>.csv`) per supplier.
2. `Master/spend-baseline.csv`: baseline pricing per part number, used as the price benchmark.
3. `CLAUDE.md`: evaluation criteria with weights, scoring guidance, and output standards.

## Steps

1. List every file in `Master/bid-responses/`. Group by supplier (each supplier has a pricing CSV and a technical CSV).
2. For each supplier:
   a. Read the pricing CSV. Confirm the columns part_number, description, unit_of_measure, annual_volume, unit_price_usd, total_annual_price, tooling_cost_usd, freight_terms, lead_time_days, minimum_order_quantity are present.
   b. Validate that total_annual_price equals unit_price_usd times annual_volume within $1 tolerance.
   c. Sum total_annual_price across all parts to get the supplier's total annual bid value.
   d. Read the technical CSV. Confirm questions T1 through T10 are answered.
   e. Score price competitiveness: lowest total annual bid value across the set gets 100. Score the others proportionally as `100 x (lowest_bid / this_bid)`.
   f. Score quality and capability (T1 to T4) on a 0 to 100 scale.
   g. Score delivery reliability (T5 to T8) on a 0 to 100 scale.
   h. Score financial stability (T9 to T10) on a 0 to 100 scale.
   i. Compute the weighted total using the weights in `CLAUDE.md`.
3. Write one scorecard per supplier to `Drafts/scorecard-<SUPID>.md`. Name the supplier legal entity, the four sub-scores with a one-sentence justification each, the weighted total, and the total annual bid value.
4. Write a comparison table to `Drafts/scoring-summary.md` ranking all suppliers by weighted total, with columns: rank, supplier, price score, quality score, delivery score, financial score, weighted total, total annual bid value.

## Output

- One file per supplier: `Drafts/scorecard-<SUPID>.md`.
- One comparison file: `Drafts/scoring-summary.md`.

## Rules and guardrails

- Do not modify any file in `Master/`.
- If a bid CSV is missing a required column or value, flag it in the validation step and score that criterion as 0 with a note.
- Apply the same rubric to every supplier. If Supplier A's vague answer scores 45, Supplier B's equally vague answer scores 45.
- Use the weights from `CLAUDE.md` exactly. Do not invent new criteria.
- All currency in USD with commas.
