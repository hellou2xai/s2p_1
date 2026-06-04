# Lesson 2: Commodity Tracker

**Time:** 35 minutes.

## The price move you heard about too late

It is 09:30 Tuesday. Your category manager at Atlas Manufacturing calls you: "Hot-rolled steel is up 14% since January. Did you know?" You did not. The commodity-prices.csv file in your shared drive has 192 rows of monthly price data across six commodities. Nobody has looked at it since last quarter's category review. You need a tracker that shows trend direction, percentage movement, and forward-looking commentary for every commodity Atlas buys. Updated monthly. Visible in two minutes.

## What Claude Code is going to do for you

Claude Code reads the commodity price history, calculates period-over-period changes, identifies trend direction (rising, falling, stable), and generates forward-looking commentary based on recent momentum and the market signals from Lesson 1. The output is a commodity dashboard you can share with your sourcing team every month.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_17_Market_Intelligence/practice/`.
3. `commodity-prices.csv` (192 rows).
4. `Drafts/market_signals.json` from Lesson 1 (for forward-looking context).

## Step-by-step

### Profile the price data

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Understand the commodity price data.

```
Read commodity-prices.csv. Tell me: (1) how many rows, (2) column names, (3) which commodities are tracked, (4) the date range, and (5) the price unit for each commodity.
```

You should see: 192 rows, columns like date, commodity, unit_price, unit_of_measure, source. Six commodities tracked (e.g., hot-rolled steel, cold-rolled steel, aluminum, copper, polypropylene, natural rubber). Date range covering 24 to 36 months.

### Calculate price movements

**Step 3.** Compute month-over-month and year-over-year changes.

```
Read commodity-prices.csv. For each commodity, calculate: (1) the most recent price, (2) the price one month ago, (3) month-over-month change in USD and percentage, (4) the price 12 months ago, (5) year-over-year change in USD and percentage, (6) trend direction based on the last three months: "rising" if all three months increased, "falling" if all three decreased, "volatile" if direction changed, "stable" if movement is within 2%. Write to Drafts/commodity_tracker.json.
```

You should see Claude create the tracker with all six fields per commodity.

**Step 4.** Review the tracker.

```
Read Drafts/commodity_tracker.json. Show me a table with columns: commodity, current_price, mom_change_pct, yoy_change_pct, trend_direction. Sort by absolute yoy_change_pct descending.
```

You should see the commodities ranked by annual price movement. Example: hot-rolled steel +14.2% YoY, copper -6.8% YoY.

### Add forward-looking commentary

**Step 5.** Combine price data with market signals.

```
Read Drafts/commodity_tracker.json and Drafts/market_signals.json. For each commodity in the tracker, check if any market signal relates to it. If yes, add a forward_outlook field with a one-sentence comment combining the price trend and the signal. If no signal exists, write "No forward intelligence available. Monitor next month." Write the updated tracker to Drafts/commodity_tracker.json.
```

You should see Claude update the tracker. Example: hot-rolled steel forward_outlook = "Rising trend (+14.2% YoY) supported by SIG-001 forecasting 8-12% further increase through Q3 2026."

**Step 6.** Generate the monthly dashboard.

```
Write Drafts/commodity_dashboard.md with: (1) report date (2026-04-25), (2) a summary table of all commodities with current price, MoM change, YoY change, trend, and forward outlook, (3) a "Watch List" section highlighting any commodity with a YoY change exceeding 10% in either direction, (4) one recommended action per watch list commodity. Keep it to one page.
```

You should see a clean dashboard document.

**Step 7.** Create a reusable update prompt.

```
Write scripts/update_commodity_tracker.md with the exact prompt to paste into Claude Code next month to regenerate the tracker. The prompt should: (1) read the latest commodity-prices.csv (assuming new rows have been appended), (2) recalculate all movements, (3) re-check market signals, and (4) regenerate the dashboard.
```

You should see Claude create the reusable prompt file.

**Step 8.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── commodity-prices.csv (192 rows)
├── Drafts/
│   └── market_signals.json (from Lesson 1)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── commodity_tracker.json
│   └── commodity_dashboard.md
├── scripts/
│   └── update_commodity_tracker.md
```

**What Claude did, behind the scenes:**

1. Claude read all 192 rows of price data and grouped them by commodity.
2. For each commodity, it sorted by date and identified the most recent, one-month-prior, and 12-month-prior prices.
3. It calculated percentage changes: (current minus prior) divided by prior, multiplied by 100.
4. It evaluated the last three consecutive monthly changes to determine trend direction.
5. It cross-referenced each commodity against the market signals array, matching on commodity_or_topic.
6. It generated forward-looking commentary by combining the historical trend with the signal's forecast.

## Common mistakes and how to recover

- **Symptom:** Month-over-month change is zero for every commodity. **Fix:** check if the date column has the right format. Ask Claude to "Show me the five most recent dates in commodity-prices.csv for hot-rolled steel. Are they in consecutive months?"

- **Symptom:** Year-over-year change cannot be calculated because the data covers less than 12 months. **Fix:** reduce to the available period. Ask Claude to "Calculate the change over the full available period instead. State the period length in the output so the reader knows it is not a full year."

- **Symptom:** The forward outlook just repeats the signal without adding the trend context. **Fix:** ask Claude to "Combine the historical trend and the signal into one sentence. Start with the trend, then add the signal forecast. Example: 'Rising trend (+14.2% YoY). Forward signal indicates a further 8-12% increase through Q3 2026.'"

- **Symptom:** The dashboard has more than one page because every commodity has a long commentary. **Fix:** limit the forward_outlook to one sentence maximum. Ask Claude to "Keep each forward outlook to 25 words or fewer."
