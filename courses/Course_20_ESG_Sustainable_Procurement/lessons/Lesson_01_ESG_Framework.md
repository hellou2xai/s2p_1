# ESG Framework Design

It is 08:00 Monday morning. Your CPO forwards an email from the Chief Sustainability Officer: the organization committed to Science Based Targets last quarter. You need ESG assessments from your top suppliers, and the board deadline is eight weeks away. Before you can score a single supplier, you need a framework. What dimensions are you scoring? What weight does each one carry? What is the minimum acceptable score? You encode all of this in CLAUDE.md so every assessment uses the same yardstick.

## The S2P problem

ESG scoring without a written framework is opinion, not measurement. One analyst weights carbon emissions at 50%. Another weights governance at 40%. The resulting scores are not comparable. When the board asks "how many suppliers are below our standard," the answer depends on which analyst did the scoring. A framework with defined dimensions, weights, scoring scales, and minimum thresholds turns subjective judgment into consistent measurement.

## What Claude Code does for you

You define the ESG framework in CLAUDE.md: six dimensions, each with a percentage weight, a 0-to-100 scoring scale, a minimum threshold of 40, and a target score of 70. Claude Code reads this framework every time it processes an assessment. The weighted score formula, the red-flag threshold, and the target are all fixed. Every supplier gets scored against the same standard.

## Set up

1. Claude Code open in `Course_20_ESG_Sustainable_Procurement/practice/`.
2. The existing `CLAUDE.md` has the role definition, data file list, and scoring weights.
3. `data/esg-framework.csv` is present with 6 dimensions.

## Step-by-step

### Step 1. Read the framework CSV.

```
Read data/esg-framework.csv and show me all rows.
```

You should see 6 dimensions: Environmental Management (20%), Carbon Emissions and Reduction (25%), Waste Management and Circular Economy (15%), Labor Practices and Human Rights (15%), Diversity and Inclusion (10%), and Governance and Ethics (15%). Each has a minimum threshold of 40 and a target of 70.

### Step 2. Review the existing CLAUDE.md.

```
Read CLAUDE.md and show me the ESG scoring weights section and the rules section.
```

You should see the weights table and rules for overall scoring, red flags, incomplete assessments, and Scope 3 estimation.

### Step 3. Add the scoring scale and interpretation rules.

```
Add a "Scoring scale and interpretation" section to CLAUDE.md with these rules:

1. Each dimension is scored 0 to 100. Scores come from supplier assessment responses.
2. Overall ESG score = sum of (dimension_score x weight) for all 6 dimensions.
3. Red flag rule: if ANY single dimension scores below 40, the supplier gets a red flag, regardless of the overall score. A supplier can score 75 overall but still have a red flag if one dimension is at 35.
4. Target rule: a supplier meets the SBTi readiness standard if ALL dimensions score 70 or above AND the overall score is 70 or above.
5. Below-threshold categories:
   - 0-39: critical (red flag, immediate action required)
   - 40-59: below target (improvement plan needed)
   - 60-69: approaching target (monitor)
   - 70-100: meets target (maintain)
6. For incomplete assessments: use the industry benchmark average from esg-benchmarks.md for missing dimensions. Mark the score as "estimated" in all outputs.
```

You should see CLAUDE.md updated with the full scoring scale section.

### Step 4. Test the framework with a sample calculation.

```
A supplier scores: Environmental Management 65, Carbon Emissions 45, Waste Management 72, Labor Practices 80, Diversity and Inclusion 60, Governance and Ethics 75. Calculate the weighted overall score and determine: does this supplier have a red flag? Does it meet the SBTi readiness standard?
```

You should see: overall score equals (65 x 0.20) + (45 x 0.25) + (72 x 0.15) + (80 x 0.15) + (60 x 0.10) + (75 x 0.15) = 13.00 + 11.25 + 10.80 + 12.00 + 6.00 + 11.25 = 64.30. No red flag (no dimension below 40). Does not meet SBTi readiness (Carbon at 45 and Diversity at 60 are below 70).

### Step 5. Test the red flag rule.

```
A different supplier scores: Environmental Management 72, Carbon Emissions 38, Waste Management 65, Labor Practices 70, Diversity and Inclusion 55, Governance and Ethics 80. Does this supplier have a red flag?
```

You should see: yes, Carbon Emissions at 38 is below the 40 minimum threshold. Red flag triggered. The overall score is 62.85, but the red flag applies regardless because one dimension is below 40.

### Step 6. Verify the framework is complete.

```
Read CLAUDE.md and confirm these five things are present:
1. Six dimensions with weights summing to 100%.
2. The 0-100 scoring scale.
3. The weighted overall score formula.
4. The red flag rule (any dimension below 40).
5. The SBTi readiness standard (all dimensions at 70 or above).
Report pass or fail for each.
```

You should see pass for all five checks.

## Worked example

**Starting files:**
- `data/esg-framework.csv` (6 dimensions).
- `CLAUDE.md` with existing weights and rules.

**What you type:**

```
Using the ESG framework in CLAUDE.md, score a supplier with these dimension scores: Environmental Management 55, Carbon Emissions 62, Waste Management 48, Labor Practices 71, Diversity and Inclusion 45, Governance and Ethics 68. Show the weighted score calculation, red flag check, and SBTi readiness check.
```

**What you should see:** Weighted score: (55 x 0.20) + (62 x 0.25) + (48 x 0.15) + (71 x 0.15) + (45 x 0.10) + (68 x 0.15) = 11.00 + 15.50 + 7.20 + 10.65 + 4.50 + 10.20 = 59.05. No red flag (no dimension below 40). Does not meet SBTi readiness (only Labor Practices is at 70 or above).

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the ESG framework: 6 dimensions, weights, thresholds.
2. Multiplied each dimension score by its weight.
3. Summed the six weighted values to get the overall score of 59.05.
4. Checked each dimension against the 40 minimum threshold. None below 40, so no red flag.
5. Checked each dimension against the 70 target. Five of six are below 70, so SBTi readiness is not met.
6. Categorized the supplier as "below target" (overall 40-59 range) with an improvement plan needed.

## Common mistakes and how to recover

- **Symptom:** The overall score exceeds 100. **Fix:** Check that the weights sum to 1.00 (or 100%). If a weight is entered as 25 instead of 0.25, the formula multiplies by 25 instead of 0.25, inflating the score by 100x.

- **Symptom:** A supplier with all dimensions above 40 still gets a red flag. **Fix:** The red flag threshold is "below 40," not "at or below 40." A score of exactly 40 passes. A score of 39 triggers the flag. Check the comparison operator.

- **Symptom:** Estimated scores from benchmarks are not labeled. **Fix:** CLAUDE.md requires the "estimated" label on any score derived from industry benchmarks. Every output row must show whether the score is "actual" or "estimated."

- **Symptom:** The weights in CLAUDE.md do not match esg-framework.csv. **Fix:** The CSV is the source of truth. If CLAUDE.md has different weights, update CLAUDE.md to match the CSV. The framework CSV should be the single source for dimension definitions.
