# Designing the Worker: Narrow Scope and Structured JSON Output

It is 10:15 on a Tuesday morning. Your orchestrator prompt is ready. It reads the supplier master, groups 50 suppliers into five batches of 10 by category, and launches a sub-agent for each batch. But when you run it, the workers produce inconsistent output. One writes a paragraph of commentary. Another dumps a raw table. A third tries to build the entire portfolio summary on its own. The problem is not the orchestrator. The problem is that you never told each worker exactly what to produce, in what format, or where to save it. That is what you fix now.

## The S2P problem

Quarterly supplier scoring at Atlas Procurement Services requires each category batch to produce two things: 10 individual scorecards and one batch summary. If the batch summary is a free-text paragraph, the orchestrator cannot reliably parse it. If the worker decides on its own what fields to include, the five batch files will not match. The orchestrator needs machine-readable, predictable output from every worker.

## What Claude Code does for you

You write a single worker prompt template. The orchestrator fills in the category name and supplier list for each batch, then passes the template to each sub-agent. Every worker follows the same instructions, uses the same weights, produces the same JSON structure, and saves to the same folder. The orchestrator can then read five identical-format files without guessing what each one contains.

## Set up

1. You have completed Lesson 3. Your orchestrator prompt divides the 50 suppliers into five batches.
2. The `batch-outputs/` folder exists in your practice directory. If not, create it now.
3. All data files are in `practice/data/`.

## Step by step

### Step 1. Write the worker prompt header

Define the worker's identity and scope in the first three lines. A worker does one thing: score its batch. Nothing else.

Open a new file or a scratch section in your orchestrator prompt. Add the worker prompt header.

```
You are a supplier scoring worker. Your job is to score exactly 10 suppliers for Q1 2026.
Do not summarize across categories. Do not write to outputs/. Do not read suppliers outside your batch.
```

You should see the three boundary rules stated up front: batch scope only, no cross-category work, no writing to the final output folder.

### Step 2. Specify the batch

The orchestrator fills in the category and supplier list for each worker. Write the placeholder section.

```
## Your batch

Category: raw-materials
Suppliers: SUP001 Great Lakes Steel, SUP002 Heartland Polymers, SUP003 Pacific Aluminum, SUP004 Apex Electronics, SUP005 Cascade Fasteners, SUP006 Summit Metals, SUP007 Liberty Composites, SUP008 Frontier Plastics, SUP009 Harbor Wire, SUP010 Keystone Coatings
```

You should see the category name and all 10 supplier IDs with names listed explicitly. The worker does not need to look up which suppliers belong to its batch. The orchestrator already did that.

### Step 3. Embed the scorecard weights directly

Do not tell the worker to read `scorecard-weights.json`. Do not tell it to check `CLAUDE.md`. Sub-agents do not inherit the orchestrator's project context. Embed the weights in the prompt itself.

```
## Scorecard weights

- Quality: 0.25
- Delivery: 0.20
- Responsiveness: 0.15
- Cost: 0.25
- Innovation: 0.15

overall_score = (quality x 0.25) + (delivery x 0.20) + (responsiveness x 0.15) + (cost x 0.25) + (innovation x 0.15). Round to one decimal.
```

You should see five weights that sum to 1.00 and the exact formula. No ambiguity.

### Step 4. Define the scoring steps

Tell the worker what to do for each supplier, in order.

```
## For each supplier

1. Read q1-performance.csv, filter to this supplier_id. Extract quality_score, delivery_score, responsiveness_score, cost_score, innovation_score.
2. Compute overall_score using the weights above.
3. Read scorecard-history.csv, filter to this supplier_id. Pull overall_score for each quarter. Determine trend: "improving" if each quarter is higher than the previous, "declining" if each quarter is lower, "stable" otherwise.
4. Identify strongest dimension (highest score) and weakest dimension (lowest score) in Q1.
5. Read risk-signals.csv, filter to this supplier_id. Pull financial_health_score, on_time_delivery_pct, single_source flag.
6. Set risk_flag to true if ANY of: status is "at_risk" or "under_review", overall_score below 65, or trend is "declining". List all applicable reasons in flag_reasons.
```

You should see six numbered steps. Each step names the file, the filter, and the output.

### Step 5. Specify the output format

This is the most important part. Define the exact JSON structure for the batch summary. The orchestrator will read this file, so the keys must be identical across all five workers.

```
## Outputs

1. Individual scorecards: save one file per supplier to batch-outputs/scorecard-[supplier_id].md.
2. Batch summary: save to batch-outputs/batch-[category].json with this exact structure:

{
  "category": "raw-materials",
  "scored_at": "2026-04-25",
  "supplier_count": 10,
  "category_average": 81.3,
  "suppliers": [
    {
      "supplier_id": "SUP001",
      "supplier_name": "Great Lakes Steel",
      "tier": "strategic",
      "overall_score": 93.7,
      "quality_score": 93.6,
      "delivery_score": 95.0,
      "responsiveness_score": 96.9,
      "cost_score": 95.1,
      "innovation_score": 86.4,
      "trend": "stable",
      "strongest": "responsiveness",
      "weakest": "innovation",
      "risk_flag": false,
      "flag_reasons": []
    }
  ]
}
```

You should see `category_average` at the top level (so the orchestrator does not have to recalculate it) and all six dimension scores per supplier (so the orchestrator can identify portfolio-wide highs and lows without re-reading individual scorecards).

**Why JSON, not markdown?** The orchestrator needs to sort, filter, and compute across all 50 suppliers. JSON is machine-readable. Markdown is not. The orchestrator would have to parse tables, guess column positions, and handle formatting variations. JSON gives consistent keys every time.

**Why `category_average` at the top level?** The portfolio summary needs a category averages table. If `category_average` is buried inside the suppliers array, the orchestrator has to loop and compute. Putting it at the top saves a step and reduces the chance of a rounding mismatch.

## Worked example: run the raw-materials worker

Assemble the full worker prompt from the pieces above. Then launch it as a sub-agent from Claude Code.

```
Use the subagent tool to run this task:

"You are a supplier scoring worker. Your job is to score exactly 10 suppliers for Q1 2026.
Do not summarize across categories. Do not write to outputs/. Do not read suppliers outside your batch.

Your batch - Category: raw-materials
Suppliers: SUP001 Great Lakes Steel, SUP002 Heartland Polymers, SUP003 Pacific Aluminum, SUP004 Apex Electronics, SUP005 Cascade Fasteners, SUP006 Summit Metals, SUP007 Liberty Composites, SUP008 Frontier Plastics, SUP009 Harbor Wire, SUP010 Keystone Coatings

[rest of worker prompt with weights, scoring steps, and output format as written above]"
```

You should see the worker create 10 scorecard files in `batch-outputs/` (scorecard-SUP001.md through scorecard-SUP010.md) and one `batch-outputs/batch-raw-materials.json` file. Open the JSON file and check three things:

1. `supplier_count` is 10.
2. `category_average` is close to the mean of the 10 `overall_score` values.
3. SUP004 (Apex Electronics) has `risk_flag: true` with reasons including "at_risk status" and "declining trend".

## Common mistakes and how to recover

**Giving the worker too much scope.** If your worker prompt says "score all suppliers and build the portfolio summary," the worker will try to do the orchestrator's job. Symptom: the worker writes to `outputs/` or references suppliers outside its batch. Fix: add the three boundary rules at the top of the worker prompt. One batch. One folder. No cross-category work.

**Omitting the output format spec.** If you do not show the exact JSON structure, each worker invents its own. One uses `weighted_score`, another uses `overall_score`, a third nests scores inside a `dimensions` object. The orchestrator cannot parse inconsistent keys. Fix: paste the full JSON example into every worker prompt.

**Referencing CLAUDE.md instead of embedding weights.** Sub-agents launched with the Task tool do not inherit the orchestrator's CLAUDE.md. If the worker prompt says "use the weights in CLAUDE.md," the worker may guess the weights or use equal weights. Fix: paste the five weights and the formula directly into the worker prompt.

**Letting the worker write to outputs/.** The `outputs/` folder is for the orchestrator's final portfolio summary. If workers write there too, you get a mix of batch files and final files in one folder. Fix: the worker prompt must say `batch-outputs/` for all worker output. Only the orchestrator writes to `outputs/`.

**Not listing suppliers by ID.** If the worker prompt says "score the raw-materials category" without listing the 10 IDs, the worker has to read the supplier master and filter. That is the orchestrator's job. The worker should receive a pre-filtered list. Fix: the orchestrator reads supplier-master.csv, groups by category, and passes the explicit list of IDs and names to each worker.
