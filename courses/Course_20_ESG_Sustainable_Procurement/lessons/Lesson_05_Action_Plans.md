# Supplier Action Plans

It is 14:00 Tuesday. You have the scores and the red flags. The CSO's next question: "What do we do about the suppliers who are behind?" A score without an action plan is just a grade. The board wants to see a specific improvement roadmap for each underperforming supplier. Three actions per supplier, prioritized by the largest gap to target, with a 12-month timeline. Not ten actions. Not a generic "improve sustainability." Three specific, measurable steps.

## The S2P problem

ESG improvement plans fail when they are too broad. "Reduce carbon emissions" is not an action. "Install energy monitoring on the primary production line by Q3 2026 to measure baseline consumption" is an action. Most teams produce vague improvement recommendations because they do not connect the score gap to a specific intervention. The larger the gap between the current score and the target, the more urgent the action. Prioritizing by gap size ensures the biggest improvements get addressed first.

## What Claude Code does for you

Claude Code reads the final ESG scores, identifies each supplier's three largest gaps to the 70-point target, and generates a specific action for each gap. Each action names the dimension, the current score, the target, the recommended intervention, and the deadline. The actions are ranked by gap size so the most impactful improvement comes first. The output is one action plan per supplier, formatted for a supplier meeting.

## Set up

1. Lesson 4 completed. `Drafts/supplier-esg-scores-final.csv` and `Drafts/esg-red-flag-register.csv` exist.
2. Claude Code open in `Course_20_ESG_Sustainable_Procurement/practice/`.
3. CLAUDE.md has the ESG framework with target scores of 70 per dimension.

## Step-by-step

### Step 1. Identify the suppliers that need action plans.

```
Read Drafts/supplier-esg-scores-final.csv. List all suppliers in the "critical" or "below target" categories. Show supplier_id, supplier_name, overall_score, and category.
```

You should see a list of suppliers below the target. Suppliers with red flags and suppliers with overall scores below 70 both appear.

### Step 2. Calculate the gap-to-target for each dimension of one supplier.

```
For SUP003 (Pacific Aluminum), show the gap between each dimension score and the 70-point target. Format as a table with columns: dimension, current_score, target, gap. Sort by gap descending (largest gap first).
```

You should see 6 rows. The dimensions with the largest gaps are the priorities for the action plan.

### Step 3. Generate three actions for one supplier.

```
For SUP003 (Pacific Aluminum), generate three improvement actions based on the three largest dimension gaps. Each action must include:
- dimension: the ESG dimension being addressed
- current_score: the supplier's current score
- target_score: 70
- action: a specific, measurable intervention (not "improve performance")
- deadline: a date within the next 12 months (start from 2026-05-01)
- expected_improvement: the estimated score increase (be realistic, 10-20 points per action)

Format as a numbered list.
```

You should see three specific actions. For example: "1. Carbon Emissions (current: 32, target: 70). Action: Submit a verified carbon footprint report for Scope 1 and 2 emissions by 2026-08-01. Expected improvement: 15 points."

### Step 4. Generate action plans for all underperforming suppliers.

```
For every supplier in the "critical" or "below target" category, generate three improvement actions following the same format as Step 3. Group actions by supplier. Save the complete set to Drafts/supplier-action-plans.md.
```

You should see action plans grouped by supplier, each with three prioritized actions. The file may cover 5 to 8 suppliers.

### Step 5. Build the 12-month timeline view.

```
From Drafts/supplier-action-plans.md, extract all actions and arrange them in a timeline table with columns: month (2026-05 through 2027-04), supplier_name, action_summary, dimension. This shows the CSO what is due each month.
```

You should see a timeline with actions distributed across the 12 months. Early months focus on the most critical gaps (red flag dimensions). Later months handle lower-priority improvements.

### Step 6. Save the timeline.

```
Save the timeline table to Drafts/esg-improvement-timeline.csv with columns: deadline_month, supplier_id, supplier_name, dimension, action_summary, current_score, target_score.
```

You should see the CSV saved with one row per action, sorted by deadline.

## Worked example

**Starting files:**
- `Drafts/supplier-esg-scores-final.csv` (15 suppliers with scores and categories).
- `CLAUDE.md` with ESG framework and target of 70.

**What you type:**

```
Generate the action plan for Eagle Transport (SUP008). Their scores are: Environmental Management 42, Carbon Emissions 35, Waste Management 55, Labor Practices 60, Diversity and Inclusion 38, Governance and Ethics 65. Show the three largest gaps and the recommended action for each.
```

**What you should see:** Three actions: (1) Carbon Emissions gap of 35 points, action: implement emissions tracking and set a 10% reduction target by 2026-09-01. (2) Diversity and Inclusion gap of 32 points, action: publish a diversity report and set hiring targets by 2026-11-01. (3) Environmental Management gap of 28 points, action: obtain ISO 14001 certification or equivalent by 2027-02-01.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the ESG framework with the 70-point target for each dimension.
2. Calculated the gap for each of Eagle Transport's 6 dimensions: 70 minus current score.
3. Sorted the gaps descending: Carbon (35), Diversity (32), Environmental (28), Governance (5), Labor (10), Waste (15).
4. Selected the top 3 gaps as priority actions.
5. Generated a specific, measurable intervention for each gap dimension.
6. Assigned deadlines spread across the next 12 months, with the largest gap getting the earliest deadline.

## Common mistakes and how to recover

- **Symptom:** The action plan has generic actions like "improve carbon performance." **Fix:** Every action must be specific and measurable. "Improve carbon performance" becomes "Submit a verified Scope 1 and 2 emissions inventory with a 10% reduction target by 2026-09-01." If the action cannot be verified as done or not done, it is not specific enough.

- **Symptom:** A supplier with a red flag dimension does not have that dimension in its top 3 gaps. **Fix:** Red flag dimensions (below 40) should always be included in the action plan, even if other dimensions have a larger numeric gap. Override the gap-sort to prioritize red flag dimensions first.

- **Symptom:** All actions have the same deadline. **Fix:** Spread deadlines across the 12-month window. The first action should be due within 3 months. The second within 6 months. The third within 9 to 12 months. Bunching deadlines reduces the chance of completion.

- **Symptom:** Expected improvement exceeds 30 points per action. **Fix:** A 30-point improvement in a single action is unrealistic. Use 10 to 20 points as the expected range. Larger improvements require multiple actions over multiple periods.
