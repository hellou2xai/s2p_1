# Lesson 1: Market Intelligence Ingestion

**Time:** 35 minutes.

## The market report nobody reads

It is 08:00 Monday. You are the strategic sourcing analyst at Atlas Manufacturing. Your category manager forwards you four market intelligence reports: a steel price outlook from a commodity service, a regulatory update on tariff changes, a supply chain disruption alert for the Midwest, and a supplier capability assessment from a trade show. All four are different formats. All four sit in your inbox until someone has time to read them. By the time someone does, the steel price has already moved, and the tariff took effect two weeks ago. You need a system that turns unstructured market information into structured, actionable signals.

## What Claude Code is going to do for you

Claude Code reads each market report, extracts structured signals (commodity, direction, magnitude, time horizon, source, and recommended action), and writes them to a consistent format. Instead of four unread reports, you get a single signals file you can scan in two minutes.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_17_Market_Intelligence/practice/`.
3. Confirm these files exist: `commodity-prices.csv` (192 rows), `supplier-capabilities.csv` (20 suppliers), `demand-intake/` (8 requirement files), `market-intelligence/` (4 report files).

## Step-by-step

### Explore the market intelligence files

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt with context from `CLAUDE.md`.

**Step 2.** List the market intelligence reports.

```
List all files in market-intelligence/. For each file, show the file name and a one-line description of its contents (read the first 10 lines to determine the topic).
```

You should see four files covering topics like: steel price forecast, tariff regulatory update, supply chain disruption alert, and supplier capability benchmarking.

**Step 3.** Read the first report in detail.

```
Read the first file in market-intelligence/. Summarize: (1) the commodity or topic covered, (2) the key finding or forecast, (3) the time horizon, (4) the source or publisher, and (5) any recommended action.
```

You should see a structured summary of the report.

### Define the signal format

**Step 4.** Create a signal extraction template in CLAUDE.md.

```
Append to CLAUDE.md a section called "## Market Signal Format" with this structure:

Every market intelligence report produces one or more signals. Each signal has these fields:
- signal_id: auto-incrementing (SIG-001, SIG-002, etc.)
- source_file: the file name of the report
- date_extracted: today's date
- commodity_or_topic: the subject (e.g., "hot-rolled steel", "tariff policy", "logistics disruption")
- signal_type: one of "price_movement", "regulatory_change", "supply_disruption", "capability_update"
- direction: "up", "down", "stable", "new_requirement", or "new_capability"
- magnitude: a specific number or range (e.g., "8-12% increase", "15% tariff", "$2.40/lb")
- time_horizon: when the signal takes effect (e.g., "Q3 2026", "effective 2026-07-01", "next 90 days")
- confidence: "high" (data-backed forecast), "medium" (expert opinion), "low" (speculation)
- recommended_action: one sentence describing what procurement should do
```

You should see Claude confirm it appended the format.

### Extract signals from all reports

**Step 5.** Process all four reports into signals.

```
Read every file in market-intelligence/. For each file, extract one or more market signals using the Market Signal Format from CLAUDE.md. Write all signals to Drafts/market_signals.json as a flat array. Assign signal_ids starting at SIG-001.
```

You should see Claude process all four reports and write the signals file. Expect 6 to 12 signals total (some reports contain multiple signals).

**Step 6.** Review the signals.

```
Read Drafts/market_signals.json. Show me all signals in a table with columns: signal_id, commodity_or_topic, signal_type, direction, magnitude, time_horizon. Sort by time_horizon ascending (most urgent first).
```

You should see a table showing all signals ranked by urgency. The nearest-term signals appear first.

**Step 7.** Create a summary for your category manager.

```
Write Drafts/market_signals_summary.md with: (1) the number of signals extracted, (2) a breakdown by signal_type (count per type), (3) the three most urgent signals (nearest time horizon) with their recommended actions, (4) any signals that directly affect current Atlas Manufacturing sourcing categories. Use today's date.
```

You should see a one-page summary with specific signal counts and actions.

**Step 8.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── market-intelligence/
│   ├── steel_price_outlook.md
│   ├── tariff_regulatory_update.md
│   ├── midwest_disruption_alert.md
│   └── supplier_capability_benchmark.md
├── commodity-prices.csv
├── supplier-capabilities.csv
```

**What you created:**

```
practice/
├── Drafts/
│   ├── market_signals.json (8-12 signals)
│   └── market_signals_summary.md
├── CLAUDE.md (updated with Market Signal Format)
```

**What Claude did, behind the scenes:**

1. Claude read each report file and identified distinct pieces of market intelligence within them.
2. It classified each piece using the signal_type categories: price movements, regulatory changes, supply disruptions, and capability updates.
3. It extracted specific numbers (percentages, dollar amounts, dates) for the magnitude and time_horizon fields.
4. It assigned a confidence level based on whether the source used data, expert opinion, or speculation.
5. It generated a recommended action for each signal by considering how the signal would affect a manufacturing company's procurement decisions.
6. It sorted signals by time horizon to surface the most urgent items first.

## Common mistakes and how to recover

- **Symptom:** Claude extracts only one signal per report, but a report contains multiple distinct findings. **Fix:** add to your prompt: "A single report may contain multiple signals. Extract every distinct finding as a separate signal. A steel price report that mentions both hot-rolled and cold-rolled prices should produce two signals."

- **Symptom:** The magnitude field says "increase expected" instead of a specific number. **Fix:** require specific numbers: "If the report states a percentage or dollar figure, use it. If the report gives a range, use the range (e.g., '8-12%'). If no number is available, write '[TBC: figure]' and set confidence to 'low.'"

- **Symptom:** All signals show the same date_extracted. **Fix:** this is correct. The extraction date is today, not the report's publication date. If you want the report date too, add a "report_date" field to the signal format.

- **Symptom:** Signals from the capability benchmark do not have a clear "direction." **Fix:** for capability updates, use "new_capability" as the direction. This indicates a supplier has a capability that Atlas did not previously know about.
