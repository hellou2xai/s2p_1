# Lesson 5: Make vs. Buy Analysis

**Time:** 35 minutes.

## The component your plant manager wants to make in-house

It is 09:00 Friday. Your plant manager at Atlas Manufacturing walks into your office: "We are paying $14.80 per unit for precision bushings. Our CNC shop could make them for $9.00. Why are we buying them?" The answer is not as simple as comparing unit costs. You need to account for tooling investment, machine capacity, quality risk, opportunity cost of CNC time, supplier alternatives, and total cost of ownership over the contract term. Your plant manager sees a $5.80 per unit gap. You need to show the full picture.

## What Claude Code is going to do for you

Claude Code reads the supplier capabilities, current pricing, internal cost estimates, and demand volume to build a structured make-vs-buy comparison. It calculates total cost of ownership for both options, identifies risks, and produces a recommendation with a clear break-even point.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_17_Market_Intelligence/practice/`.
3. `supplier-capabilities.csv` (20 suppliers).
4. `commodity-prices.csv` for raw material costs.
5. `Drafts/demand_specs.json` and `Drafts/sourcing_actions.csv` from earlier lessons.

## Step-by-step

### Define the make-vs-buy framework

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Create the analysis framework in CLAUDE.md.

```
Append to CLAUDE.md a section called "## Make vs Buy Framework" with these cost categories:

Buy Side:
- Unit price from supplier (current or quoted)
- Freight and logistics cost per unit
- Quality inspection cost per unit (incoming inspection labor)
- Risk premium: cost of carrying safety stock for supply disruption
- Total buy cost per unit = sum of above

Make Side:
- Raw material cost per unit (from commodity-prices.csv)
- Direct labor cost per unit (machine operator hours x hourly rate)
- Machine time cost per unit (CNC or equipment depreciation per hour)
- Tooling investment (one-time, amortized over expected volume)
- Quality cost per unit (in-process inspection, scrap rate)
- Opportunity cost: revenue lost from displacing other work on the machine
- Total make cost per unit = sum of above

Decision rule: recommend "Buy" unless total make cost is at least 15% lower than total buy cost AND internal capacity is available without displacing higher-margin work.
```

You should see Claude append the framework.

### Build the comparison for a specific item

**Step 3.** Select an item for analysis.

```
Read Drafts/sourcing_actions.csv. Pick the sourcing action with the highest estimated_value. Show me the item type, combined quantity, and estimated value.
```

You should see the highest-value sourcing action identified.

**Step 4.** Build the buy-side cost model.

```
For the item you just identified, build the buy-side cost model. Use these assumptions: (1) current supplier unit price: read from the most relevant supplier in supplier-capabilities.csv, or use $14.80 if not available. (2) Freight: $0.60 per unit. (3) Quality inspection: $0.25 per unit. (4) Safety stock risk premium: 3% of unit price. Calculate the total buy cost per unit and the total annual buy cost at the combined quantity. Write to Drafts/make_vs_buy_analysis.json under a "buy_side" section.
```

You should see the buy-side costs calculated with specific figures.

**Step 5.** Build the make-side cost model.

```
Add a "make_side" section to Drafts/make_vs_buy_analysis.json. Use these assumptions: (1) Raw material: use the most recent price for the relevant commodity from commodity-prices.csv plus 10% for waste and scrap. (2) Direct labor: 0.15 hours per unit at $32/hour. (3) Machine time: 0.10 hours per unit at $85/hour. (4) Tooling: $28,000 one-time investment, amortized over 24 months of production at the annual quantity. (5) In-process quality: $0.40 per unit. (6) Opportunity cost: $2.00 per unit (estimated revenue margin lost from displacing other CNC work). Calculate total make cost per unit and total annual make cost.
```

You should see the make-side costs calculated. The total make cost per unit should be higher than the plant manager's quick estimate of $9.00 because it includes tooling, opportunity cost, and quality costs.

**Step 6.** Compare and calculate the break-even.

```
Read Drafts/make_vs_buy_analysis.json. Add a "comparison" section with: (1) buy cost per unit, (2) make cost per unit, (3) difference per unit (positive means buy is cheaper), (4) percentage difference, (5) break-even volume: at what annual quantity does the make option become cheaper than buy, considering the fixed tooling cost? (6) recommendation: apply the decision rule from CLAUDE.md. Write the updated file.
```

You should see a clear comparison. If make cost is $12.35 per unit and buy cost is $15.69, the make option is 21% cheaper, which exceeds the 15% threshold.

**Step 7.** Check for alternative suppliers.

```
Read supplier-capabilities.csv. Find all suppliers capable of producing this item type. For each, show: supplier name, location, capability notes, and whether they are currently supplying Atlas. If three or more alternatives exist, note that competitive bidding could reduce the buy-side cost before committing to in-house production.
```

You should see the alternative supplier list. This is important context: if competitive pressure could bring the buy price down 10%, the make case may weaken.

### Generate the recommendation

**Step 8.** Write the make-vs-buy recommendation.

```
Write Drafts/make_vs_buy_recommendation.md with: (1) Executive summary: the item, the current buy cost, the estimated make cost, the percentage difference, and the recommendation. (2) Cost comparison table: all line items from both sides. (3) Break-even analysis: at what volume does in-house production pay off, and is Atlas above or below that volume? (4) Risk factors: three risks of making in-house (capacity constraints, quality learning curve, opportunity cost) and two risks of continuing to buy (price increases, supply disruption). (5) Recommendation: one clear paragraph. Use today's date.
```

You should see a complete recommendation document.

**Step 9.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── supplier-capabilities.csv (20 suppliers)
├── commodity-prices.csv (192 rows)
├── Drafts/
│   ├── demand_specs.json
│   └── sourcing_actions.csv
```

**What you created:**

```
practice/
├── Drafts/
│   ├── make_vs_buy_analysis.json
│   └── make_vs_buy_recommendation.md
├── CLAUDE.md (updated with make vs buy framework)
```

**What Claude did, behind the scenes:**

1. Claude read the highest-value sourcing action to identify the item and volume.
2. It built the buy-side model by looking up the current supplier price and adding freight, inspection, and risk costs.
3. It built the make-side model by reading the raw material price from `commodity-prices.csv`, adding labor, machine time, tooling amortization, quality, and opportunity costs.
4. It calculated the break-even volume by finding the quantity where total make cost (including the one-time tooling cost) equals total buy cost.
5. It applied the decision rule: make only if 15% cheaper and capacity is available.
6. It checked for alternative suppliers who could bring competitive pressure to the buy price.

## Common mistakes and how to recover

- **Symptom:** The make option looks too cheap because tooling cost was not amortized. **Fix:** confirm the tooling cost is divided by the expected total production volume over the amortization period, not treated as a per-unit cost without volume adjustment.

- **Symptom:** Opportunity cost is set to zero because "the CNC shop has idle time." **Fix:** even if idle today, the machine may not be idle next quarter. Use a conservative opportunity cost ($2.00 per unit or the margin on the next-best job the machine could run).

- **Symptom:** The raw material price from commodity-prices.csv is for a different grade or form than what the item requires. **Fix:** add a note: "Raw material cost is estimated from the closest commodity match. Confirm the exact grade and form factor with the plant engineering team before finalizing."

- **Symptom:** The recommendation ignores the learning curve for in-house production. **Fix:** add a risk factor: "First 90 days of in-house production may have a 15-20% higher scrap rate as operators learn the process. Factor this into the make cost for the first year."
