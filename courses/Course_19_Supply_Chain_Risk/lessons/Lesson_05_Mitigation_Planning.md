# Lesson 05: Mitigation Planning

## Opening scenario

It is 14:00 Thursday. You have the risk scores, the concentration map, the single-source exposure, and two disruption scenarios with dollar figures attached. Your CPO calls again: "Good work. Now the board is going to ask: what are we doing about it? I need a list of actions, not a brainstorm. Ranked, costed, and with a timeline. And cap it at five. I'm not taking a fifteen-item wish list to a board meeting." You turn to Claude Code. The draft files from Lessons 2 through 4 are all in `Drafts/`. Everything you need to build the mitigation plan is already written down.

## The S2P problem

Most risk mitigation plans are long lists of good ideas with no prioritization. "Qualify an alternate supplier" sits next to "improve supplier communication" with no indication of which action matters more or what either one costs. Without a ranking method, the board cannot decide where to spend money first. The plan needs to connect each action to a specific risk, state a dollar cost, and estimate how much exposure it reduces. That turns a wish list into an investment case. Three to five actions, ranked by bang for dollar. That's what boards approve.

## What Claude Code is going to do for you

Claude Code reads the three risk analysis drafts from `Drafts/` (concentration risk summary, single-source exposure map, and disruption scenarios). For each critical or high risk, it generates one specific mitigation action with a cost estimate, a timeline, and a calculated risk reduction ratio (exposure reduced per dollar spent). It ranks the actions by that ratio, selects the top five, builds a timeline table with owner roles and milestones, and adds an investment case summary at the top. The finished file goes to `Drafts/mitigation-plan.md`. This lesson takes about 40 minutes.

## Set up

1. Lessons 1 through 4 completed. All three draft files are saved in `Drafts/`.
2. Claude Code open in `Course_19_Supply_Chain_Risk/practice/`. If you closed it, reopen:

```
cd "Course_19_Supply_Chain_Risk/practice"
claude
```

3. Confirm these draft files exist:
   - `Drafts/concentration-risk-summary.md`
   - `Drafts/single-source-exposure-map.md`
   - `Drafts/disruption-scenarios.md`
4. CLAUDE.md has the scoring matrix and the output standard: board recommendation lists capped at three items.

Open the session with the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

## Step-by-step

### Step 1. Extract all identified risks from the three draft files.

Build a consolidated risk list before generating any mitigation actions.

```
Read Drafts/concentration-risk-summary.md, Drafts/single-source-exposure-map.md,
and Drafts/disruption-scenarios.md. Extract every identified risk. For each risk list:
risk_id (assign R-01, R-02, etc.), description, affected_supplier,
annual_exposure_usd, current_risk_level (critical/high/medium/low).
Sort by annual_exposure_usd descending.
```

You should see a consolidated list of risks drawn from all three documents. Risks from single-source exposure (Microcontroller ARM with no alternate, $480,000, Apex Electronics already in financial distress) and disruption scenarios (Pacific Aluminum 60-day failure at $1,052,877 total impact) should appear at the top. If Claude lists fewer than 6 risks, ask it to re-read all three files and confirm it extracted risks from each one.

### Step 2. Generate one specific mitigation action per critical or high risk.

Every action must name a supplier, an item, and a measurable outcome. No generic suggestions.

```
For each critical or high risk from the list, generate one specific mitigation action.
Each action must include:
- action_id (A-01, A-02, etc.)
- action_description (specific: name the supplier, item, and outcome)
- target_risk_id
- estimated_cost_usd
- estimated_timeline_months
- risk_reduction_description (what exposure this removes, in dollars)

Do not suggest generic actions like "improve supplier relationships" or
"monitor supplier performance." Every action must be specific.
Example of a specific action: "Accelerate qualification of Summit Metals (SUP016)
as alternate for ITEM-0025 (Microcontroller ARM), currently sole-sourced from
Apex Electronics (SUP004) at $480,000 per year. Estimated qualification cost:
$45,000 over 4 months. Removes $480,000 in unprotected single-source exposure."
```

You should see a list of specific actions. Each names a supplier by name, references an item by ID or description, states a cost, and states a timeline. If any action says "consider improving" or "explore options," ask Claude to rewrite it with a specific action verb and a named supplier.

### Step 3. Calculate the risk reduction ratio for each action.

Rank actions by how much exposure they remove per dollar spent.

```
For each mitigation action, calculate the risk reduction ratio:
annual_exposure_reduced_usd divided by estimated_cost_usd.
Build a table with columns: action_id, action_description, target_risk,
exposure_reduced_usd, cost_usd, risk_reduction_ratio, timeline_months.
Sort by risk_reduction_ratio descending.
```

You should see actions ranked from highest to lowest ratio. A ratio of 10.0 means every $1 spent removes $10 of annual exposure. Actions that address large exposures at low cost rank highest. If the top-ranked action has a ratio below 1.0, the cost estimate may be inflated. Ask Claude to review the cost assumption for that action.

### Step 4. Select the top five actions.

Pick the five highest-ratio actions and write a one-sentence justification for each.

```
Select the top 5 mitigation actions by risk reduction ratio. For each one, write a
one-sentence justification that names the risk, the supplier, and the expected outcome.
Format as a numbered list. Use specific numbers.
```

You should see five numbered actions, each with a justification sentence that contains a dollar figure and a supplier name. For example: "1. Accelerate Summit Metals qualification for ITEM-0025: removes $480,000 in critical single-source exposure at a cost of $45,000, a 10.7x reduction ratio." If a justification sentence lacks a number, ask Claude to add the exposure or cost figure.

### Step 5. Build the mitigation timeline.

Assign dates, owners, and milestones to each of the five actions.

```
Create a timeline table for the 5 selected mitigation actions with columns:
action_id, action_description, owner (use a role title: Category Manager Raw Materials,
Category Manager Logistics, IT Procurement Manager, etc.), start_date (use 2026-05-01),
end_date, milestone_at_midpoint, status (all "planned").
Save the table to Drafts/mitigation-plan.md.
```

You should see a 5-row timeline. Actions with a 3-month timeline end on 2026-07-31. Actions with a 6-month timeline end on 2026-10-31. Each row has a midpoint milestone (for example, "Alternate supplier sample parts approved"). If all end dates are identical, ask Claude to vary them based on the estimated_timeline_months from Step 3.

### Step 6. Add the investment case to the top of the plan.

Summarize the total cost, total exposure reduced, and payback ratio in one section.

```
Add an "Investment case" section at the top of Drafts/mitigation-plan.md.
Include:
- Total mitigation investment: sum of all 5 action costs.
- Total annual exposure reduced: sum of all 5 exposure reductions.
- Payback ratio: total exposure reduced divided by total investment.
- One paragraph recommending the three highest-priority actions.
  The paragraph must name each action, state its deadline, and state the exposure it removes.
  Three actions maximum. Specific dollar figures required. Save the updated file.
```

You should see the investment case section at the top of the file. The payback ratio should be a specific number like 12.4x. The recommendation paragraph names three actions with deadlines and dollar figures. If the paragraph lists more than three actions, ask Claude to trim to three, keeping the highest-ratio actions.

## Worked example

**Starting files:**
- `Drafts/concentration-risk-summary.md` (three concentration views with dollar figures).
- `Drafts/single-source-exposure-map.md` (5 items, 2 with no alternate).
- `Drafts/disruption-scenarios.md` (2 scenarios, total impacts $1,052,877 and $610,959).

**What you type:**

```
Build a risk-ranked mitigation plan from the three draft files in Drafts/. For each
critical or high risk, generate one specific action with a cost and timeline. Rank by
risk reduction ratio (exposure reduced divided by cost). Select the top 5. Build a
timeline starting 2026-05-01. Add an investment case at the top. Save to
Drafts/mitigation-plan.md.
```

**What you should see:**

A mitigation plan saved to `Drafts/mitigation-plan.md` with an investment case section at the top, followed by 5 ranked actions, each with a target risk, cost, timeline, and reduction ratio. The investment case shows total cost, total exposure reduced, and a payback ratio expressed as a specific multiple (for example, 9.8x). The recommendation paragraph names three actions with deadlines.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the output standards: board recommendations capped at three, all currency in USD with commas, no vague language.
2. Read the three draft files and extracted all risks with their associated exposure amounts.
3. Generated one specific mitigation action per critical or high risk, naming the supplier, item, and measurable outcome for each.
4. Calculated the risk reduction ratio for each action: annual exposure reduced divided by estimated cost.
5. Ranked all actions by ratio and selected the top five.
6. Assigned start dates of 2026-05-01, calculated end dates from the timeline estimates, and added midpoint milestones.
7. Summed total cost and total exposure reduction across the five actions.
8. Wrote the investment case paragraph naming the three highest-priority actions with deadlines.

## Common mistakes and how to recover

- **Symptom:** The mitigation actions are generic ("enhance supplier monitoring," "conduct supplier reviews"). **Fix:** Reject any action without a named supplier, a named item or category, and a measurable outcome. Ask Claude to rewrite each generic action. A valid action reads: "Negotiate 60-day safety stock agreement with Great Lakes Steel for hot-rolled coil (ITEM-0001), covering $840,000 in annual spend. Estimated cost: $18,000 to fund the safety stock buffer. Reduces lead-time exposure from 6 weeks to 2 weeks."

- **Symptom:** The risk reduction ratio is below 1.0 for several actions. **Fix:** A ratio below 1.0 means the mitigation costs more than the annual exposure it reduces. This sometimes applies to actions that protect against low-probability, high-severity events. Ask Claude to check the cost estimate. If the cost is correct, note in the justification that the action is justified by severity, not ratio, and include it only if no higher-ratio alternative exists.

- **Symptom:** All five actions have the same end date. **Fix:** Action timelines vary by type. Qualifying a new supplier takes 4 to 6 months. Negotiating a safety stock clause takes 4 to 6 weeks. Building inventory buffer takes 2 to 4 weeks. Ask Claude to assign distinct end dates based on the estimated_timeline_months value for each action.

- **Symptom:** The investment case recommendation lists more than three actions. **Fix:** CLAUDE.md caps recommendation lists at three. Ask Claude to keep the three with the highest risk reduction ratio and move the other two to a footnote labeled "Additional actions, ranked."

- **Symptom:** Drafts/mitigation-plan.md saves but the investment case section is at the bottom, not the top. **Fix:** Ask Claude to rewrite the file with the investment case section first, followed by the timeline table, then the ranked action list. Structure matters: the board reads the first section and may not reach the bottom.
