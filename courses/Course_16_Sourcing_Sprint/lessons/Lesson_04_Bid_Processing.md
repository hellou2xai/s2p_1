# Lesson 4: Bid Processing

**Time:** 40 minutes.

## Six bids, six hours of data entry

It is 09:00 Monday of week three at Ironbridge Manufacturing. The RFP deadline has passed. Six suppliers submitted their bid responses in the template format you defined in Lesson 3. Each bid has a pricing CSV and a technical CSV. Normally, you would open each file, copy the pricing into a comparison spreadsheet, read each technical response, score it by hand, and build a weighted evaluation. For six bids with 18 part numbers and 10 technical questions each, that is at least six hours of manual work. Your CPO wants the evaluation by Wednesday.

## What Claude Code is going to do for you

Claude Code reads all six bid files in a loop, validates each one against the template rules, scores the pricing against the baseline and the technical responses against the evaluation criteria, and produces a ranked comparison. One prompt processes all six bids. The output is a scored evaluation matrix ready for your review.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_16_Sourcing_Sprint/practice/`.
3. `CLAUDE.md` with the Sourcing Event Context and Bid Response Processing Rules from Lessons 1 and 3.
4. `bid-responses/` folder containing 6 bid files.
5. `spend-baseline.csv` for baseline pricing comparison.

## Step-by-step

### Validate all bid files

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt with the full sourcing context.

**Step 2.** List the bid files.

```
List all files in bid-responses/. For each file, show the file name and size.
```

You should see 6 bid files (or 12 if pricing and technical are separate files per supplier).

**Step 3.** Validate every bid against the template rules.

```
Read every file in bid-responses/. For each bid, apply the Bid Response Processing Rules from CLAUDE.md: (1) check all required columns are present, (2) check no blank unit_price_usd values, (3) verify total_annual_price equals unit_price_usd x annual_volume within $1 tolerance, (4) check all 10 technical questions answered. Write the validation results to Drafts/bid_validation.json with fields: supplier_name, file_name, valid (true/false), issues (array of specific problems).
```

You should see Claude validate all bids. Example: 5 valid, 1 with a missing answer on question T7.

### Score the pricing

**Step 4.** Compare bid pricing to the baseline.

```
Read spend-baseline.csv to get the current average unit price per part number. Read the pricing from each validated bid in bid-responses/. For each supplier, calculate: (1) total annual bid value (sum of unit_price x annual_volume across all parts), (2) percentage difference from the baseline total, (3) per-part comparison showing which parts are above and below baseline. Write to Drafts/pricing_comparison.json.
```

You should see a comparison showing each supplier's total bid and percentage difference from the $2.4M baseline.

**Step 5.** Assign pricing scores.

```
Read Drafts/pricing_comparison.json. Assign a pricing score (0 to 100) to each supplier. The lowest total bid gets 100. Other bids are scored proportionally: score = 100 x (lowest_bid / this_bid). Write the scores to Drafts/pricing_scores.json.
```

You should see scores like: Titan Precision 100, Cascade Metals 94, Summit Steel 88, etc.

### Score the technical responses

**Step 6.** Evaluate technical responses against criteria.

```
Read the technical responses from each bid in bid-responses/. Score each supplier on a 0 to 100 scale for each of the three non-price criteria: quality_capability (questions T1-T4), delivery_reliability (questions T5-T8), financial_stability (questions T9-T10). Use these scoring rules: specific certifications and data = 80-100, general statements with some evidence = 50-79, vague or missing answers = 0-49. Write to Drafts/technical_scores.json with supplier_name, quality_score, delivery_score, financial_score, and a one-sentence justification for each score.
```

You should see scored technical evaluations for all six suppliers with justifications.

### Calculate weighted totals

**Step 7.** Apply the evaluation weights and rank the suppliers.

```
Read Drafts/pricing_scores.json and Drafts/technical_scores.json. Apply the evaluation weights from CLAUDE.md: price 40%, quality 25%, delivery 20%, financial stability 15%. Calculate the weighted total score for each supplier. Write to Drafts/bid_evaluation_matrix.csv with columns: rank, supplier_name, pricing_score, quality_score, delivery_score, financial_score, weighted_total. Sort by weighted_total descending.
```

You should see a ranked evaluation matrix. The supplier with the highest weighted total is the leading candidate.

**Step 8.** Verify the scores.

```
Read Drafts/bid_evaluation_matrix.csv. For the top-ranked supplier, show me: their total bid value, their percentage below baseline, and their scores across all four criteria with justifications. For the second-ranked supplier, show the same.
```

You should see a detailed comparison of the top two candidates.

**Step 9.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── spend-baseline.csv (356 rows)
├── bid-responses/ (6 supplier bids)
├── CLAUDE.md (with evaluation criteria and processing rules)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── bid_validation.json
│   ├── pricing_comparison.json
│   ├── pricing_scores.json
│   ├── technical_scores.json
│   └── bid_evaluation_matrix.csv
```

**What Claude did, behind the scenes:**

1. Claude read each bid file and checked it against the template column structure.
2. It validated arithmetic (unit price times volume equals total) for every pricing line.
3. It loaded the baseline average prices from `spend-baseline.csv` and calculated each supplier's total bid.
4. It applied proportional scoring: the lowest bidder gets 100, others get proportionally lower scores.
5. It read technical responses and scored them based on specificity of evidence (certifications, data, and named references score higher than vague statements).
6. It applied the four evaluation weights and calculated a weighted total for ranking.

## Common mistakes and how to recover

- **Symptom:** Pricing scores are all very close (within 2 points) because bids are similar. **Fix:** this is normal in competitive categories. The technical scores will differentiate. Check the weighted totals, not just the pricing scores.

- **Symptom:** Claude gives inconsistent technical scores (one supplier's vague answer scores 70, another's scores 45). **Fix:** ask Claude to "Re-score all technical responses using the same rubric. Show the scoring criteria you applied to each answer. Ensure consistent treatment: if Supplier A's vague answer on T3 scores 45, Supplier B's equally vague answer on T3 should score the same."

- **Symptom:** A bid file fails validation because it uses a slightly different column name. **Fix:** ask Claude to "Show me the column headers from the failing bid file and the expected headers. Map any close matches (e.g., 'UnitPrice' vs 'unit_price_usd') and process accordingly."

- **Symptom:** The weighted totals do not add up to 100 for any supplier. **Fix:** weighted totals are not expected to reach 100 unless a supplier scores 100 on every criterion. Verify by checking: (pricing_score x 0.40) + (quality_score x 0.25) + (delivery_score x 0.20) + (financial_score x 0.15).
