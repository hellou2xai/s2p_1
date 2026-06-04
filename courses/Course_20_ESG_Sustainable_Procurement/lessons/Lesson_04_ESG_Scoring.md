# ESG Scoring and Red Flag Detection

It is 09:00 Tuesday. You have the raw dimension scores for all 15 suppliers, including benchmark estimates for the 5 partial assessments. Now you need the weighted overall score for each supplier and a clear list of red flags. A red flag is not the same as a low overall score. A supplier can score 72 overall but carry a red flag because one dimension (say Carbon Emissions) is at 35. The board needs both views: the overall ranking and the specific dimension failures.

## The S2P problem

When procurement teams run ESG scoring, they often report only the overall weighted score. A score of 65 looks acceptable until you notice that the supplier scored 28 on Labor Practices. An overall score hides dimension-level failures. The board needs two things: a ranked list of suppliers by overall score, and a separate list of red flags where any single dimension falls below the minimum threshold. These are different questions, and they require different outputs.

## What Claude Code does for you

Claude Code reads the raw scores from Drafts/supplier-esg-scores-raw.csv and the framework from CLAUDE.md. It calculates the weighted overall score for each supplier, checks every dimension against the 40-point minimum threshold, and produces two outputs: a scored supplier ranking and a red flag register. The red flag register lists every instance where a dimension falls below 40, separate from the overall score. A supplier can rank fifth overall and still appear on the red flag list.

## Set up

1. Lessons 1 through 3 completed. `Drafts/supplier-esg-scores-raw.csv` exists with 15 suppliers.
2. Claude Code open in `Course_20_ESG_Sustainable_Procurement/practice/`.
3. CLAUDE.md has the ESG framework with weights, thresholds, and red flag rules.

## Step-by-step

### Step 1. Calculate weighted overall scores.

```
Read Drafts/supplier-esg-scores-raw.csv and CLAUDE.md. For each supplier, calculate the weighted overall ESG score using the formula: (environmental_management x 0.20) + (carbon_emissions x 0.25) + (waste_management x 0.15) + (labor_practices x 0.15) + (diversity_inclusion x 0.10) + (governance_ethics x 0.15). Show a table with columns: supplier_id, supplier_name, overall_score, rank (1 = highest). Sort by overall_score descending.
```

You should see a 15-row table ranked by overall score. Scores will range roughly from 35 to 80.

### Step 2. Identify red flags.

```
For each supplier, check every dimension score against the 40-point minimum threshold. List every instance where a dimension is below 40. Show a table with columns: supplier_id, supplier_name, dimension, score, threshold, gap_below_threshold. Sort by gap descending (worst first).
```

You should see a red flag table. Pacific Aluminum (SUP003) and Eagle Transport (SUP008) likely appear with scores below 40 on one or more dimensions.

### Step 3. Categorize each supplier.

```
Using the scoring categories from CLAUDE.md, assign each supplier to one of four categories:
- Critical (overall below 40 OR any red flag): immediate action required
- Below target (overall 40-59, no red flags): improvement plan needed
- Approaching target (overall 60-69, no red flags): monitor
- Meets target (overall 70+, no red flags): maintain

Show a summary table: category, supplier_count, supplier_names.
```

You should see suppliers distributed across the four categories. The "critical" category includes any supplier with a red flag, even if their overall score is above 40.

### Step 4. Show the distinction between overall score and red flags.

```
Find any supplier whose overall score is above 50 but who has a red flag. Name the supplier, their overall score, and the dimension that triggered the red flag. This demonstrates why red flags must be tracked separately from overall scores.
```

You should see at least one supplier where the overall score looks acceptable but a single dimension failure creates a compliance risk.

### Step 5. Save the scored output.

```
Save the complete scored table to Drafts/supplier-esg-scores-final.csv with columns: supplier_id, supplier_name, environmental_management, carbon_emissions, waste_management, labor_practices, diversity_inclusion, governance_ethics, overall_score, rank, category, red_flag_count, red_flag_dimensions, completeness.
```

You should see the CSV saved with 15 rows, each supplier fully scored and categorized.

### Step 6. Save the red flag register.

```
Save the red flag register as a separate file: Drafts/esg-red-flag-register.csv with columns: supplier_id, supplier_name, dimension, score, threshold, gap, required_action. Set required_action to "immediate improvement plan required" for all red flag entries.
```

You should see the red flag CSV saved with one row per flag instance.

## Worked example

**Starting files:**
- `Drafts/supplier-esg-scores-raw.csv` (15 suppliers, 6 dimension scores each).
- `CLAUDE.md` with ESG framework.

**What you type:**

```
Score all 15 suppliers using the ESG framework in CLAUDE.md. Produce two outputs: a ranked supplier table sorted by overall score, and a red flag register listing every dimension below 40. Save both to Drafts/.
```

**What you should see:** Two files saved. The ranked table shows 15 suppliers from highest to lowest overall score. The red flag register shows specific dimension failures for 2 to 4 suppliers.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the ESG framework: 6 dimensions, weights, and thresholds.
2. Read Drafts/supplier-esg-scores-raw.csv to get all 15 suppliers with their dimension scores.
3. Calculated the weighted overall score for each supplier using the formula.
4. Ranked suppliers by overall score (highest first).
5. Checked every dimension of every supplier against the 40-point threshold.
6. Flagged each below-threshold instance as a red flag entry.
7. Assigned each supplier to a category (critical, below target, approaching, or meets target).

## Common mistakes and how to recover

- **Symptom:** A supplier with a red flag is categorized as "approaching target" instead of "critical." **Fix:** The category logic must check red flags first. Any supplier with a red flag goes to "critical," regardless of overall score. The overall-score bands apply only to suppliers with zero red flags.

- **Symptom:** The red flag register is empty, but you know two suppliers score below 40. **Fix:** Check the threshold comparison. The rule is "below 40," meaning a score of 39 triggers the flag but a score of 40 does not. Verify the operator is strictly less than 40.

- **Symptom:** The overall scores do not match your manual calculation. **Fix:** Check that the weights sum to 1.00. If the weights were entered as percentages (20, 25, 15, 15, 10, 15) instead of decimals (0.20, 0.25, etc.), the formula produces a score 100 times too large.

- **Symptom:** Estimated dimension scores from Lesson 2 are treated the same as actual scores. **Fix:** The completeness column and estimated_dimensions column from the raw file must carry through to the final output. The board needs to know which scores are real and which are benchmark estimates.
