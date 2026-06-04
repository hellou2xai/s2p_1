# Portfolio Dashboard and Board Reporting

It is 09:00 Wednesday. The CSO needs a portfolio-level view for the board. Not 15 individual supplier reports. A single dashboard that answers three questions: "Where does our supplier base stand on ESG today? How much Scope 3 carbon do we need to reduce? Are we on track for our SBTi commitment?" You assemble the scored data, the Scope 3 estimates, and the action plan timeline into a single narrative the board can read in five minutes.

## The S2P problem

Boards do not read supplier scorecards. They read dashboards. A dashboard shows distribution (how many suppliers are at each performance level), concentration (where the biggest Scope 3 contributors sit), and trajectory (are we improving or not). Most procurement teams can produce individual supplier reports but struggle to aggregate them into a portfolio view. The aggregation is where the strategic story lives: how many suppliers meet the target, how many need intervention, and what is the total carbon opportunity.

## What Claude Code does for you

Claude Code reads the final ESG scores, the Scope 3 emissions table, and the action plan timeline. It produces a portfolio dashboard with three sections: score distribution (how many suppliers in each category), Scope 3 opportunity (top 5 emitters and the reduction potential), and SBTi progress narrative (where you stand against the commitment). Every number traces to the scored data. The narrative connects the data to the board's question.

## Set up

1. Lessons 1 through 5 completed. All drafts are in the `Drafts/` folder.
2. Claude Code open in `Course_20_ESG_Sustainable_Procurement/practice/`.
3. CLAUDE.md has the ESG framework, scoring rules, and Scope 3 formula.

## Step-by-step

### Step 1. Build the score distribution summary.

```
Read Drafts/supplier-esg-scores-final.csv. Count the number of suppliers in each category: critical, below target, approaching target, meets target. Show a summary table with columns: category, supplier_count, pct_of_total, average_overall_score, combined_annual_spend_usd.
```

You should see a 4-row table. The "meets target" row shows how many suppliers are already at 70 or above. The "critical" row shows how many need immediate action.

### Step 2. Identify the Scope 3 opportunity.

```
Read Drafts/scope3-emissions-by-supplier.csv. Show the top 5 emitters by estimated_tons_co2 with their current ESG overall score and category. For each, estimate the Scope 3 reduction if the supplier improved to the "meets target" category (score 70+). Use this assumption: a 10-point ESG score improvement correlates with a 5% reduction in emission factor. Show the potential tons CO2 reduced for each.
```

You should see a 5-row table showing the top emitters, their current scores, and the estimated carbon reduction if they improve. This is the Scope 3 opportunity the CSO needs.

### Step 3. Calculate the total Scope 3 reduction potential.

```
Sum the potential tons CO2 reduced from Step 2. State the total as a percentage of the current Scope 3 baseline. This is the headline number for the SBTi progress section.
```

You should see a total reduction potential. For example: "Improving the top 5 emitters to target would reduce Scope 3 by approximately 1,200 tons CO2, equal to 8.5% of the current baseline."

### Step 4. Write the SBTi progress narrative.

```
Write a three-paragraph SBTi progress narrative for the board:
- Paragraph 1: Current state. How many suppliers assessed, how many meet target, total Scope 3 baseline in tons CO2.
- Paragraph 2: Gap. How many suppliers are critical or below target, combined spend at risk, Scope 3 reduction needed.
- Paragraph 3: Path forward. Action plans in progress, timeline for completion, expected Scope 3 reduction by end of 12-month period.

Use specific numbers from the data. No vague statements.
```

You should see three paragraphs, each leading with a number. The narrative connects the supplier scores to the Scope 3 target.

### Step 5. Assemble the full dashboard.

```
Combine the score distribution table, the Scope 3 opportunity table, the reduction potential summary, and the SBTi progress narrative into a single board dashboard document. Title: "ESG Portfolio Dashboard, Q2 2026." Add an executive summary at the top with one sentence each for: portfolio health, Scope 3 status, and recommended investment. Save to Drafts/esg-portfolio-dashboard.md.
```

You should see the complete dashboard saved. It should fit on two to three printed pages.

### Step 6. Validate the dashboard.

```
Read Drafts/esg-portfolio-dashboard.md and check:
1. Does the executive summary include at least one supplier name, one value, and one date?
2. Does every paragraph include a specific number?
3. Are there any em-dashes or banned phrases?
4. Does the recommendation section have three items or fewer?
Report pass or fail for each check.
```

You should see pass for all four checks.

## Worked example

**Starting files:**
- `Drafts/supplier-esg-scores-final.csv` (15 suppliers scored).
- `Drafts/scope3-emissions-by-supplier.csv` (15 suppliers with emissions).
- `Drafts/esg-improvement-timeline.csv` (action plan timeline).

**What you type:**

```
Build the ESG portfolio dashboard from all draft files. Include score distribution, Scope 3 opportunity for top 5 emitters, and SBTi progress narrative. Save to Drafts/esg-portfolio-dashboard.md.
```

**What you should see:** A dashboard with three sections and an executive summary. Every sentence includes a specific number. The executive summary names at least one supplier.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the ESG framework and output standards.
2. Read Drafts/supplier-esg-scores-final.csv to count suppliers by category and calculate averages.
3. Read Drafts/scope3-emissions-by-supplier.csv to identify top emitters and total Scope 3 baseline.
4. Calculated the Scope 3 reduction potential for the top 5 emitters using the improvement assumption.
5. Read Drafts/esg-improvement-timeline.csv to summarize the action plan status.
6. Assembled the three sections and wrote the executive summary with supplier name, value, and date.
7. Saved the complete dashboard to Drafts/.

## Common mistakes and how to recover

- **Symptom:** The score distribution percentages do not sum to 100%. **Fix:** Check that all 15 suppliers are categorized. If one supplier is uncategorized (for example, due to missing data), it drops out of the count. Every supplier must be in exactly one category.

- **Symptom:** The Scope 3 reduction estimate is unrealistically large (over 50% of baseline). **Fix:** The 5% reduction per 10-point improvement is an assumption, not a fact. If the assumption produces an unrealistic result, note it as "illustrative" and recommend primary data collection to refine the estimate.

- **Symptom:** The SBTi narrative uses phrases like "making progress" without a number. **Fix:** Replace every qualitative statement with a quantitative one. "Making progress" becomes "6 of 15 suppliers now meet the 70-point target, up from 4 at the start of the assessment period."

- **Symptom:** The dashboard is longer than three pages. **Fix:** Move the detailed supplier-by-supplier data to an appendix. The dashboard shows portfolio-level summaries. Individual supplier details live in the action plans and score files.

- **Symptom:** The executive summary does not name a supplier. **Fix:** Add the highest-emitter or lowest-scorer by name. "Pacific Aluminum (overall score 38, estimated 2,480 tons CO2) requires immediate intervention" gives the board a concrete reference point.
