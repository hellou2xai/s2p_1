# Lesson 04: Disruption Scenario Modeling

## Opening scenario

It is 09:00 Thursday. Your CPO forwards a message from the CFO: "Before the board meeting, I need to know what a supplier failure actually costs us. Not 'significant disruption.' Give me a dollar figure for a realistic worst-case." You have four historical disruption events in the data. Each one recorded what happened, which supplier was hit, how long it lasted, and what it cost. You use those events as a baseline to model two forward-looking scenarios, each with a direct cost, an indirect cost, and a recovery timeline. By the end of this lesson, you have financial impact numbers you can defend in front of the CFO.

## The S2P problem

Most risk registers list risks without quantifying their financial impact. "Supplier X may experience a disruption" tells a board nothing actionable. The board needs a dollar figure broken into two parts: direct cost (spot-market purchases, expedited shipping, overtime labor to work around the gap) and indirect cost (production downtime, customer delivery penalties, lost revenue). Without those numbers, a risk is an opinion. With them, it becomes a budget line item and a decision trigger. Building these models manually from historical event data takes a full day of spreadsheet work and assumption documentation.

## What Claude Code is going to do for you

Claude Code reads `data/disruption-events.md` to extract historical cost patterns, then applies those patterns to current supplier data. For two named scenarios (Pacific Aluminum offline for 60 days, Continental Freight losing capacity for 45 days), Claude Code calculates direct cost, indirect cost, total financial impact, and estimated recovery timeline. Every number ties to a data source or a stated assumption. The output goes to `Drafts/disruption-scenarios.md`, ready to feed into the mitigation plan in Lesson 5. This lesson takes about 50 minutes.

## Set up

1. Lessons 1 through 3 completed. CLAUDE.md has the scoring matrix, data source mapping, and concentration thresholds. `Drafts/single-source-exposure-map.md` is saved.
2. Claude Code open in `Course_19_Supply_Chain_Risk/practice/`. If you closed it, reopen:

```
cd "Course_19_Supply_Chain_Risk/practice"
claude
```

3. Confirm these files are present:
   - `data/disruption-events.md` (4 historical events)
   - `data/supplier-master.csv` (25 suppliers)
   - `data/single-source-items.csv` (5 items)
   - `data/approved-alternates.csv` (4 alternates)

Open the session with the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

## Step-by-step

### Step 1. Read and summarize the disruption events.

Extract the cost patterns from the four historical events before building any model.

```
Read data/disruption-events.md and summarize each event: which supplier was affected,
what type of event it was, how long it lasted in days, and what the total financial
impact was in USD.
```

You should see four events: Hurricane Impact (Heartland Polymers, 12 days, $420,000), Supplier Financial Distress (Apex Electronics, ongoing, lead times doubled and reject rate at 4.2%), Logistics Capacity Crunch (Eagle Transport, 21 days, $180,000 incremental cost), and Cybersecurity Incident (CloudBridge Systems, 5 days, $95,000 business interruption). If any event is missing, ask Claude to re-read the file and list the event headings first.

### Step 2. Extract cost categories and ranges.

Build the assumption set before running scenario numbers.

```
From the 4 disruption events in data/disruption-events.md, extract each cost category
that appears. For each category, state the dollar range observed across events.
Format as a table with columns: cost_category, cost_type (direct or indirect),
observed_range_usd, source_event.
```

You should see categories including: spot-market premiums (direct, from the Heartland Polymers event at 15% above contracted rates), expedited freight (direct, from the Eagle Transport and Heartland Polymers events), production downtime (indirect, from multiple events), and business interruption (indirect, from the CloudBridge event at $95,000 over 5 days, or $19,000 per day). If Claude combines direct and indirect costs into one line, ask it to separate them explicitly.

### Step 3. Model Scenario 1: Pacific Aluminum offline for 60 days.

Apply the historical cost patterns to the first forward-looking scenario.

```
Model this scenario: Pacific Aluminum (SUP003) experiences a facility shutdown for 60 days.
Use these inputs from data/supplier-master.csv and data/single-source-items.csv:
- Pacific Aluminum annual spend: $3,100,000
- Single-source items supplied by SUP003: check data/single-source-items.csv
- Alternate status: check data/approved-alternates.csv

Use these cost assumptions from the historical events:
- Spot-market premium: 30% above contracted rates for any spend during the 60-day window
- Expedited freight surcharge: $150,000 one-time
- Production downtime: $25,000 per day for the first 30 days (after that, alternates ramp up)

Calculate: 60-day spend exposure, direct cost (spot premium plus freight),
indirect cost (downtime), total financial impact, and recovery timeline based
on alternate qualification status.
```

You should see: 60-day spend exposure = $3,100,000 / 365 x 60 = $509,589. Spot premium = $509,589 x 0.30 = $152,877. Plus expedited freight $150,000. Direct cost = $302,877. Indirect cost = $25,000 x 30 = $750,000. Total = $1,052,877. Recovery timeline: Pacific Aluminum's 5 single-source items include ITEM-0013 (Aluminum sheet, Summit Metals qualified at 10 weeks). Other items may have no alternate. If Claude's total differs significantly, ask it to show the calculation line by line.

### Step 4. Model Scenario 2: Continental Freight loses capacity for 45 days.

Run the second scenario with different cost drivers.

```
Model this scenario: Continental Freight (SUP006) loses warehouse capacity for 45 days
due to a fire. Use these inputs:
- Continental Freight annual spend: $3,600,000 from data/supplier-master.csv
- Continental Freight has no single-source items (they are a logistics provider)
- Alternative carriers available at 25% above contracted rates
- Re-routing and expediting cost: $200,000 one-time
- Customer delivery delay penalty: $10,000 per day for 20 affected shipments,
  capped at 30 days

Calculate the same four outputs: direct cost, indirect cost, total financial impact,
and recovery timeline.
```

You should see: 45-day spend exposure = $3,600,000 / 365 x 45 = $443,836. Rate premium at 25% = $110,959. Plus re-routing $200,000. Direct cost = $310,959. Indirect cost (penalties) = $10,000 x 20 x 30 (capped) = wait, the penalty is $10,000 per day total for 20 affected shipments. Clarify: if the $10,000 is per shipment per day, indirect = $10,000 x 30 days = $300,000. Total = $610,959. If Claude interprets the penalty differently, ask it to state its interpretation before calculating.

### Step 5. Compare the two scenarios.

Put both scenarios side by side so the board can see relative severity.

```
Build a comparison table for the two scenarios with columns: scenario_name,
affected_supplier, duration_days, direct_cost_usd, indirect_cost_usd,
total_impact_usd, recovery_timeline, mitigation_available.
Sort by total_impact_usd descending.
```

You should see the Pacific Aluminum scenario ranking first with a higher total impact (approximately $1,052,877 versus $610,959). Recovery timeline for Pacific Aluminum is longer because some single-source items have no qualified alternate. Mitigation available for Continental Freight is "yes" (Patriot Logistics used during the January 2026 event per the historical data). If the two scenarios are nearly identical in cost, review the per-day downtime assumption for Scenario 1.

### Step 6. Save both scenarios with a board takeaway.

Write the full output to Drafts/ with one-sentence summaries for the board.

```
Save both scenario models, the cost assumption table, and the comparison table to
Drafts/disruption-scenarios.md. Add a "Board takeaway" section at the end with one
sentence per scenario that states the financial exposure and the recovery outlook.
Each sentence must start with a dollar figure.
```

You should see `Drafts/disruption-scenarios.md` saved with four sections: assumptions, Scenario 1, Scenario 2, comparison table, and board takeaway. Confirm the board takeaway sentences start with dollar figures. If they start with supplier names instead, ask Claude to rewrite them to lead with the dollar amount.

## Worked example

**Starting files:**
- `data/disruption-events.md` (4 historical events with impact figures).
- `data/supplier-master.csv` (25 suppliers including Pacific Aluminum at $3,100,000).
- `data/single-source-items.csv` (5 items, including ITEM-0013 linked to Pacific Aluminum).
- `data/approved-alternates.csv` (4 alternates, including Summit Metals for ITEM-0013).

**What you type:**

```
Model a 60-day disruption at Pacific Aluminum (SUP003). Annual spend: $3,100,000.
Use historical cost patterns from data/disruption-events.md. Assume spot-market
premium of 30%, expedited freight surcharge of $150,000, and production downtime
of $25,000 per day for 30 days. Show direct cost, indirect cost, and total impact.
```

**What you should see:**

A scenario model with: 60-day spend exposure $509,589, direct cost $302,877 (spot premium $152,877 plus freight $150,000), indirect cost $750,000 (downtime $25,000 x 30 days), total financial impact approximately $1,052,877. Recovery timeline: ITEM-0013 alternate available in 10 weeks. ITEM-0025 has no alternate, extending full recovery to an estimated 6 to 12 months.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the risk scoring framework and output standards (USD with commas, no vague language).
2. Read `data/disruption-events.md` to extract the historical cost patterns: spot premium rates, freight surcharges, and daily downtime costs from the four events.
3. Read `data/supplier-master.csv` to confirm Pacific Aluminum's annual spend of $3,100,000.
4. Calculated 60-day spend exposure: $3,100,000 divided by 365, multiplied by 60.
5. Applied the 30% spot-market premium to the 60-day spend figure.
6. Added the stated expedited freight surcharge of $150,000 to get total direct cost.
7. Multiplied the $25,000 per-day downtime rate by 30 days (the period before alternates ramp) to get indirect cost.
8. Read `data/approved-alternates.csv` to check alternate availability for Pacific Aluminum's items and set the recovery timeline accordingly.

## Common mistakes and how to recover

- **Symptom:** The total financial impact seems unrealistically high (over $5,000,000). **Fix:** Check the per-day downtime cost. $25,000 per day is a reasonable baseline for a mid-size manufacturer. If you accidentally entered $250,000 per day, the indirect cost inflates by 10x. Verify the assumption in the prompt and recalculate.

- **Symptom:** The scenario does not reference alternate suppliers at all. **Fix:** Ask Claude to read `data/approved-alternates.csv` and identify which items affected by the scenario have a qualified alternate. Alternates shorten the recovery window and reduce indirect cost. Without them, the model overstates impact for items that do have backup options.

- **Symptom:** Direct and indirect costs are not separated in the output. **Fix:** The board needs both figures separately. Direct costs are cash outlays (spot purchases, freight surcharges, re-routing fees). Indirect costs are revenue or productivity losses (downtime, customer penalties). Ask Claude to rewrite the output with two clearly labeled rows.

- **Symptom:** The recovery timeline says "unknown." **Fix:** Base the timeline on the alternate qualification status from approved-alternates.csv. A fully qualified alternate means 1 to 2 weeks to switch. An alternate in qualification means 3 to 6 months. No alternate means 6 to 12 months. These ranges are consistent with the historical events in disruption-events.md.

- **Symptom:** Scenario 2 (Continental Freight) shows no indirect cost. **Fix:** Continental Freight has no single-source items, but a 45-day logistics outage still causes customer delivery delays. The customer delivery penalty is the indirect cost. Confirm the prompt includes the $10,000 per day penalty assumption.
