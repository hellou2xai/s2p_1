# Lesson 6: Market to Sourcing Brief

**Time:** 35 minutes.

## The RFP that ignored the market

It is 10:00 Monday of the following week at Atlas Manufacturing. Your category manager is about to issue an RFP for industrial gaskets. The evaluation weights are the same ones used last year: price 50%, quality 25%, delivery 15%, service 10%. But the market has changed. Steel prices are up 14%. Two suppliers from the Midwest are dealing with logistics disruptions. A new tariff on imported gasket materials takes effect in 90 days. If the RFP goes out with last year's weights, it will optimize for price in a rising-price environment and ignore supply security when disruptions are active. You need the market intelligence to adjust the sourcing strategy before the RFP ships.

## What Claude Code is going to do for you

Claude Code reads the market signals, commodity tracker, and supplier capabilities from earlier lessons, then adjusts the evaluation criteria weights in the RFP. It produces a market-informed sourcing brief that explains why each weight was adjusted, what risk each signal introduces, and what the adjusted RFP evaluation should look like.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_17_Market_Intelligence/practice/`.
3. `Drafts/market_signals.json` from Lesson 1.
4. `Drafts/commodity_tracker.json` from Lesson 2.
5. `supplier-capabilities.csv` (20 suppliers).

## Step-by-step

### Review the current evaluation weights

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Establish the baseline evaluation criteria.

```
The current RFP evaluation weights for Atlas Manufacturing sourcing events are: price 50%, quality 25%, delivery 15%, service 10%. Save these as the baseline in Drafts/evaluation_baseline.json with fields: criterion, baseline_weight_pct, and a notes field set to "Standard weights, no market adjustment."
```

You should see Claude create the baseline file with four criteria.

### Map market signals to evaluation criteria

**Step 3.** Identify which signals affect which criteria.

```
Read Drafts/market_signals.json and Drafts/commodity_tracker.json. For each active market signal, determine which evaluation criterion it affects. Use these mapping rules:

- Price movement signals (rising prices) reduce the importance of price weight because the market is inflating and all bids will be higher. Shift weight toward supply security.
- Supply disruption signals increase the importance of delivery weight because reliable delivery is at risk.
- Regulatory change signals (tariffs, new requirements) increase the importance of quality and compliance checks.
- Capability update signals do not directly change weights but may add a new criterion (innovation or capability breadth).

Write to Drafts/signal_weight_impact.json with fields: signal_id, signal_type, affected_criterion, recommended_adjustment (e.g., "increase delivery weight by 5%"), rationale (one sentence).
```

You should see each signal mapped to a criterion with a specific adjustment recommendation.

**Step 4.** Calculate the adjusted weights.

```
Read Drafts/evaluation_baseline.json and Drafts/signal_weight_impact.json. Apply all recommended adjustments. Rules: (1) Weights must still sum to 100%. (2) No single criterion can exceed 40% or fall below 5%. (3) If adjustments push a criterion outside these bounds, cap it and redistribute the excess proportionally. Write the adjusted weights to Drafts/evaluation_adjusted.json with fields: criterion, baseline_weight_pct, adjusted_weight_pct, change_pct, and justification (citing the specific signals that drove the change).
```

You should see the adjusted weights. Example: price drops from 50% to 35%, delivery increases from 15% to 25%, quality stays at 25%, service adjusts to 15%.

### Build the sourcing brief

**Step 5.** Generate the market-informed sourcing brief.

```
Write Drafts/market_sourcing_brief.md with these sections:

1. Purpose: explain that this brief adjusts the standard sourcing evaluation weights based on current market conditions.

2. Market Context: a table of active market signals with signal_id, type, magnitude, and time horizon. Three to five signals maximum.

3. Weight Adjustments: a table comparing baseline and adjusted weights with the justification for each change.

4. Supplier Landscape: read supplier-capabilities.csv and list the suppliers most affected by the active signals (e.g., Midwest suppliers affected by the disruption alert). Note which suppliers gain or lose competitive advantage under the adjusted weights.

5. Recommended Sourcing Approach: based on the adjusted weights and market context, recommend the sourcing approach (competitive bid with adjusted criteria, negotiated sole source if supply is constrained, or split award to manage risk).

6. Validity: note that this brief is valid for 90 days from today. After that, market conditions should be reassessed and weights recalibrated.

Use today's date (2026-04-25).
```

You should see a complete sourcing brief with all six sections.

**Step 6.** Create the adjusted evaluation scorecard template.

```
Write Drafts/adjusted_scorecard_template.csv with columns: supplier_name (blank, to be filled during evaluation), price_score (0-100), quality_score (0-100), delivery_score (0-100), service_score (0-100), weighted_total. Include a header row and a formula description row showing: weighted_total = (price_score x adjusted_price_weight) + (quality_score x adjusted_quality_weight) + (delivery_score x adjusted_delivery_weight) + (service_score x adjusted_service_weight). Use the adjusted weights from Drafts/evaluation_adjusted.json.
```

You should see a scorecard template ready for the evaluation team.

**Step 7.** Verify the brief is complete.

```
Read Drafts/market_sourcing_brief.md. Confirm: (1) every weight adjustment cites a specific signal_id, (2) all four weights sum to 100%, (3) no weight exceeds 40% or falls below 5%, (4) the supplier landscape names at least three specific suppliers. Report any issues.
```

You should see Claude confirm completeness or flag issues.

**Step 8.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── supplier-capabilities.csv (20 suppliers)
├── Drafts/
│   ├── market_signals.json (8-12 signals)
│   └── commodity_tracker.json
```

**What you created:**

```
practice/
├── Drafts/
│   ├── evaluation_baseline.json
│   ├── signal_weight_impact.json
│   ├── evaluation_adjusted.json
│   ├── market_sourcing_brief.md
│   └── adjusted_scorecard_template.csv
```

**What Claude did, behind the scenes:**

1. Claude read the market signals and commodity tracker to identify active conditions affecting sourcing.
2. It mapped each signal to the evaluation criterion it most directly affects using the mapping rules.
3. It calculated percentage adjustments for each criterion and checked that the total remained at 100%.
4. It applied caps (40% max, 5% min) and redistributed any excess proportionally.
5. It cross-referenced the supplier capabilities list to identify which suppliers are most affected by disruptions or tariffs.
6. It generated the sourcing brief by combining market context, weight adjustments, and supplier analysis into a single document.
7. It created a scorecard template pre-loaded with the adjusted weights for use during bid evaluation.

## Common mistakes and how to recover

- **Symptom:** The adjusted weights do not sum to 100%. **Fix:** this is a rounding error. Ask Claude to "Adjust the final criterion by the rounding difference so all four weights sum to exactly 100.0%."

- **Symptom:** All weight shifts go to one criterion (e.g., delivery gets 40% of the weight because three signals affect it). **Fix:** the cap of 40% should prevent this. If not applied, ask Claude to "Re-read the cap rule from the prompt. No criterion can exceed 40%. Redistribute the excess to the next most affected criterion."

- **Symptom:** The sourcing brief recommends sole source when three capable suppliers exist. **Fix:** sole source is only appropriate when supply is severely constrained (one or two capable suppliers). If three or more exist, the recommendation should be competitive bid with adjusted criteria.

- **Symptom:** The brief is valid for 90 days, but a signal has a 30-day time horizon. **Fix:** adjust the validity period to match the shortest signal horizon. Add: "Reassess if any signal changes within its stated time horizon, even if the 90-day validity has not expired."
