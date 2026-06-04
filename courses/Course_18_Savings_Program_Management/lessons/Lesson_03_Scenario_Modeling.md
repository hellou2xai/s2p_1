# Three-Scenario Modeling

It is 09:00 Friday. You have YTD realized savings by initiative. The CFO will ask one question on Tuesday: "Will we hit $12M?" You cannot answer with a single number. The Logistics RFP is at risk, Demand Reduction is behind, and Spec Standardization is underperforming. You need three projections: a base case (current run rate), an upside case (recovery actions land), and a risk-adjusted case (things get worse before they get better). Three numbers, not one. The CFO picks the one she believes.

## The S2P problem

A savings program with one forecast is a savings program with no credibility. If you present $12M and miss by $2M, the CFO remembers the miss. If you present a range with named assumptions, the CFO remembers the transparency. Most teams model scenarios by copying a spreadsheet three times and changing cells by hand. The assumptions live in someone's head, not on the page. When the CPO asks "what changed since last month," nobody can answer precisely.

## What Claude Code does for you

Claude Code reads the YTD savings summary, applies three sets of assumptions (base, upside, risk-adjusted), and projects full-year savings for each initiative under each scenario. The assumptions are explicit: base case uses the current Q1-Q3 run rate, upside adds specific recovery actions, and risk-adjusted discounts underperforming initiatives. Every number traces back to a stated assumption.

## Set up

1. Lessons 1 and 2 completed. `Drafts/savings-summary-ytd.csv` exists with 8 initiatives.
2. Claude Code open in `Course_18_Savings_Program_Management/practice/`.
3. `data/market-benchmarks.md` is present for upside assumptions.

## Step-by-step

### Step 1. Define the three scenarios in plain language.

```
I need three full-year projection scenarios for our $12M savings target. Here are the assumptions:

Base case: Each initiative continues at its current Q1-Q3 run rate for Q4. No changes.

Upside case: SAV-002 (Logistics RFP) recovers to 75% of its Q4 target through renegotiation. SAV-006 (Demand Reduction) improves by 20% in Q4 from a new travel policy. SAV-007 (Spec Standardization) recovers to 60% of Q4 target through two approved spec changes. All other initiatives continue at current run rate.

Risk-adjusted case: SAV-002 stays flat at current run rate. SAV-006 and SAV-007 each lose 10% from current run rate due to business travel increase and spec delays. SAV-004 (Facilities Rebid) drops 15% in Q4 due to a contractor dispute.

Add these scenario definitions to CLAUDE.md under a new section called "Q4 Projection Scenarios."
```

You should see CLAUDE.md updated with the three scenarios and their specific assumptions.

### Step 2. Calculate the base case projection.

```
Using Drafts/savings-summary-ytd.csv, calculate the base case full-year projection. For each initiative, take the Q1-Q3 realized savings, divide by 3 to get the quarterly run rate, and add one quarter to project the full year. Show a table with: initiative_id, initiative_name, q1_q3_realized, q4_projected, full_year_projected.
```

You should see a table where the full-year total is approximately $9.1M, well short of the $12M target.

### Step 3. Calculate the upside case.

```
Now calculate the upside case. Start from the base case Q4 projections, then apply the upside adjustments: SAV-002 Q4 at 75% of its quarterly target ($450,000 x 0.75), SAV-006 Q4 improved by 20% over base run rate, SAV-007 Q4 at 60% of its quarterly target ($350,000 x 0.60). Show the same table format with a "scenario" column showing "upside."
```

You should see the upside full-year total near $9.6M to $9.8M.

### Step 4. Calculate the risk-adjusted case.

```
Now calculate the risk-adjusted case. Start from the base case Q4 projections, then apply the risk adjustments: SAV-002 stays at base run rate (no change), SAV-006 drops 10% from base Q4, SAV-007 drops 10% from base Q4, SAV-004 drops 15% from base Q4. Show the table with scenario column "risk_adjusted."
```

You should see the risk-adjusted full-year total near $8.8M to $9.0M.

### Step 5. Build the scenario comparison table.

```
Combine all three scenarios into a single comparison table. Columns: initiative_id, initiative_name, annual_target, base_case, upside_case, risk_adjusted. Include a totals row. Add a "gap_to_target" row showing the difference between each scenario total and $12M.
```

You should see a clean comparison. The gap to target ranges from approximately $2.2M (risk-adjusted) to $2.4M (upside) to $2.9M (base).

### Step 6. Save the scenario model.

```
Save the scenario comparison table as Drafts/scenario-projections.csv. Include all columns and the totals row.
```

You should see the CSV saved with 8 initiative rows plus the totals row.

## Worked example

**Starting files:**
- `Drafts/savings-summary-ytd.csv` (8 initiatives with YTD realized savings).
- `CLAUDE.md` with savings methodology and scenario definitions.

**What you type:**

```
For SAV-002 (Logistics RFP), the Q1-Q3 realized savings are $747,565. Calculate the Q4 projection under all three scenarios: base (current run rate), upside (75% of Q4 target of $450,000), and risk-adjusted (same as base). Show the full-year total for each.
```

**What you should see:** Base case Q4 is approximately $249,188 (one-third of YTD), full year $996,753. Upside Q4 is $337,500 (75% of $450,000), full year $1,085,065. Risk-adjusted Q4 is $249,188 (same as base), full year $996,753.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the scenario definitions and assumptions.
2. Read Drafts/savings-summary-ytd.csv to get SAV-002 YTD realized of $747,565.
3. Calculated base Q4: $747,565 divided by 3 equals $249,188.
4. Calculated upside Q4: 75% of $450,000 equals $337,500.
5. Calculated risk-adjusted Q4: same as base, $249,188.
6. Added each Q4 figure to the YTD to get three full-year projections.

## Common mistakes and how to recover

- **Symptom:** The base case run rate divides by 9 months instead of 3 quarters. **Fix:** The data covers Q1 through Q3 (three quarters). Divide by 3 to get the quarterly run rate. If you divide by 9, you get a monthly rate, and the Q4 projection will be one-third of what it should be.

- **Symptom:** Upside case shows a lower number than base case for an initiative. **Fix:** Check the upside assumptions. The upside should never be below the base for any initiative. If it is, the assumption is wrong. Review the scenario definitions in CLAUDE.md.

- **Symptom:** The gap to target is a positive number when the program is behind. **Fix:** The gap should be negative: scenario total minus $12M target. A positive gap means you exceeded the target, which is not the case here.

- **Symptom:** All three scenarios show the same number for an initiative that has a scenario adjustment. **Fix:** Check that Claude Code applied the scenario-specific adjustments. Read back the CLAUDE.md scenario section to confirm the adjustments are defined correctly.
