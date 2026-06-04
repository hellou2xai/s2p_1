# Designing the Orchestrator

It is 10:30 Monday morning. You know how the Agent tool works. You know sub-agents get their own context and can read files from disk. Now you need the master plan. The VP wants 50 scorecards by Wednesday, and you are not going to type 5 separate sub-agent prompts by hand. You need an orchestrator: one prompt that reads the supplier list, divides it into 5 batches by category, writes the task prompt for each worker, and launches all 5. This lesson teaches you how to design that orchestrator.

## What Claude Code does for you

You will write a single orchestrator prompt that reads `data/supplier-master.csv`, groups the 50 suppliers into 5 category batches of 10, and spawns 5 worker sub-agents. Each worker scores its 10 suppliers using the same weights and format. The orchestrator handles decomposition and delegation so you do not have to manage each batch by hand. Total effort from you: one prompt.

## Set up

1. Claude Code installed and signed in.
2. Your terminal open in the `practice/` folder inside `Course_05_The_Orchestrator/`.
3. The `data/` folder contains all six data files.
4. The `batch-outputs/` subfolder exists (created in Lesson 2).
5. The `outputs/` subfolder exists. If not, create it.

**Step 1.** Confirm the outputs folder exists.

```
mkdir -p outputs
```

You should see no output. The folder now exists.

**Step 2.** Open Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

## The orchestrator pattern

Every orchestrator follows four stages:

1. **Read.** Load the data that defines the work. In this case, supplier-master.csv.
2. **Decompose.** Split the work into independent batches. Here, group by category.
3. **Invoke workers.** Launch one sub-agent per batch, passing it a complete, self-contained task prompt.
4. **Aggregate.** After workers finish, read their outputs and combine into a portfolio summary.

This lesson covers stages 1 through 3. Aggregation comes in a later lesson.

## Step by step

### Step 3. Set the project rules.

```
The folder data/ holds all source files. Do not edit any file in data/. Save worker outputs to batch-outputs/. Save the final portfolio summary to outputs/.
```

Claude confirms the constraints.

### Step 4. Understand why the orchestrator passes weights explicitly.

The practice folder has a CLAUDE.md that defines scorecard weights. You might be tempted to tell workers to "use the weights in CLAUDE.md" instead of repeating them. That will not work reliably.

Sub-agents may not inherit the project's CLAUDE.md. When the Agent tool launches a sub-agent, that sub-agent starts a fresh session. It may not load the parent folder's CLAUDE.md automatically. If the worker does not see the weights, it will guess or ask, and either outcome wastes time.

The fix is simple. Include the weights directly in every worker's task prompt. Copy the five weights into the prompt text. It adds two lines and eliminates ambiguity.

### Step 5. Type the orchestrator prompt.

This is the full prompt. Copy it and paste it into your Claude Code session.

```
Read data/supplier-master.csv. Group the 50 suppliers by category. There are five categories, each with exactly 10 suppliers:
- raw-materials (SUP001 through SUP010)
- logistics (SUP011 through SUP020)
- it-services (SUP021 through SUP030)
- facilities (SUP031 through SUP040)
- professional-services (SUP041 through SUP050)

For each category, launch a sub-agent using the Agent tool with this task prompt:

"You are a supplier scoring worker for Q1 2026. Score exactly these 10 suppliers: [list the supplier_ids and names for this category].

Read these files from data/:
1. q1-performance.csv. Filter to your 10 supplier_ids only.
2. scorecard-history.csv. Filter to your 10 supplier_ids for trend analysis.
3. risk-signals.csv. Filter to your 10 supplier_ids.

Scorecard weights (use these exactly):
- Quality: 0.25
- Delivery: 0.20
- Responsiveness: 0.15
- Cost: 0.25
- Innovation: 0.15

For each supplier:
1. Compute overall_score = (quality_score x 0.25) + (delivery_score x 0.20) + (responsiveness_score x 0.15) + (cost_score x 0.25) + (innovation_score x 0.15). Round to one decimal.
2. From scorecard-history.csv, determine trend: improving (each quarter higher than prior), declining (each quarter lower), or stable.
3. Identify strongest dimension (highest score) and weakest dimension (lowest score).
4. Pull risk signals: financial_health_score, on_time_delivery_pct, single_source flag.
5. Flag the supplier if status is at_risk or under_review, overall_score is below 65, or trend is declining.

Save two outputs:
1. One scorecard per supplier as batch-outputs/scorecard-[supplier_id].md
2. One batch summary as batch-outputs/batch-[category].json with this structure:
{
  'category': '[category]',
  'scored_at': '2026-04-25',
  'supplier_count': 10,
  'category_average': [average of 10 overall_scores],
  'suppliers': [array of objects with supplier_id, supplier_name, tier, overall_score, trend, strongest, weakest, risk_flag, flag_reasons]
}

Do not modify any file in data/. Do not write to outputs/. Only write to batch-outputs/."

Launch all five workers. After they complete, confirm that batch-outputs/ contains five batch-[category].json files and 50 scorecard-[supplier_id].md files.
```

You should see Claude read supplier-master.csv, parse the 50 rows, group them into 5 categories, and begin launching sub-agents. Each sub-agent appears as a separate task in the Claude Code output. You will see five workers start, each processing its batch of 10 suppliers.

### Step 6. Watch the workers run.

As each worker runs, Claude Code shows its progress. You should see output like:

- "Launching sub-agent for raw-materials (SUP001 through SUP010)..."
- "Launching sub-agent for logistics (SUP011 through SUP020)..."
- "Launching sub-agent for it-services (SUP021 through SUP030)..."
- "Launching sub-agent for facilities (SUP031 through SUP040)..."
- "Launching sub-agent for professional-services (SUP041 through SUP050)..."

Each worker reads its filtered data, computes scores, and writes files to batch-outputs/. The workers operate independently. Worker C (it-services) does not wait for Worker A (raw-materials) to finish.

### Step 7. Verify the outputs.

After all workers complete, check that the batch-outputs folder has the expected files.

```
List all files in batch-outputs/ and count them. I expect 5 JSON files and 50 markdown scorecard files, for a total of 55 files.
```

You should see 55 files: `batch-raw-materials.json`, `batch-logistics.json`, `batch-it-services.json`, `batch-facilities.json`, `batch-professional-services.json`, and 50 `scorecard-SUPxxx.md` files.

### Step 8. Spot-check one batch summary.

```
Read batch-outputs/batch-raw-materials.json. Confirm it has 10 suppliers and that the category_average is calculated correctly.
```

Claude reads the JSON and confirms 10 suppliers in the raw-materials category. It verifies the category_average matches the average of the 10 individual overall_scores. For example, Great Lakes Steel at 93.7, Apex Electronics at 69.6, and so on.

## Worked example

**Starting files:** `data/supplier-master.csv` (50 rows), `data/q1-performance.csv` (50 rows), `data/scorecard-history.csv` (200 rows), `data/risk-signals.csv` (50 rows), `data/scorecard-weights.json`.

**Prompt typed:** The orchestrator prompt from Step 5.

**What you saw:** Claude launched 5 sub-agents. Each scored 10 suppliers. The batch-outputs folder ended up with 55 files: 5 batch JSON summaries and 50 individual scorecards.

**What Claude did, behind the scenes:**

1. The orchestrator read `data/supplier-master.csv` and parsed all 50 rows.
2. It grouped suppliers by the `category` column, producing 5 lists of 10 supplier IDs each.
3. For each category, it constructed a task prompt by inserting the 10 supplier IDs and names into the worker template.
4. It launched each task prompt as a sub-agent using the Agent tool. Each sub-agent received the full worker instructions, including the explicit scorecard weights.
5. Each sub-agent independently read the CSV files, filtered to its 10 suppliers, computed weighted scores, determined trends, and identified risk flags.
6. Each sub-agent wrote 10 individual scorecard files and 1 batch summary JSON to batch-outputs/.
7. The orchestrator confirmed all 55 files were present in batch-outputs/.

## Common mistakes and how to recover

- **Symptom:** A worker produces scorecards for all 50 suppliers instead of just 10. **Fix:** The orchestrator's task prompt did not specify which supplier IDs belong to this worker. Always list the exact supplier IDs: "Score exactly these 10 suppliers: SUP001 Great Lakes Steel, SUP002 Heartland Polymers..." The word "exactly" matters.

- **Symptom:** A worker says it cannot find the scorecard weights. **Fix:** You referenced "see CLAUDE.md" or "see scorecard-weights.json" instead of pasting the weights into the task prompt. Sub-agents may not load CLAUDE.md. Include the five weights as plain text in every worker prompt.

- **Symptom:** Workers write output files to the wrong location, like the project root or outputs/. **Fix:** The task prompt did not specify the output path, or it used a vague instruction like "save the results." Always include the exact path: "Save to batch-outputs/scorecard-SUP001.md."

- **Symptom:** The orchestrator says "batch-outputs/ contains 45 files" instead of 55. One worker failed. **Fix:** Check which category's batch JSON is missing. Re-launch a single sub-agent for that category using the same task prompt. The other four batches do not need to re-run. This is one advantage of the sub-agent pattern: failures are isolated.

- **Symptom:** You assign batches by supplier ID range (1 through 10, 11 through 20) instead of by category, and two categories end up mixed in one batch. **Fix:** In this data set, supplier IDs happen to align with categories. But in real data, they may not. Always group by the actual category column, not by ID range. Read the data first, then batch.

- **Symptom:** The orchestrator prompt is vague: "score some suppliers and save the results somewhere." **Fix:** Vague prompts produce vague outputs. Specify the exact file names, the exact weights, the exact output format (including the JSON structure), and the exact save location. The more precise the worker prompt, the more consistent the results across all five batches.
