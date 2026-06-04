# Lesson 03: PO Pricing Compliance: Matching PO Amounts to Contracted Rates and Flagging Overcharges

**Estimated time:** 55 minutes
**Role:** P2P Analytics Lead, Meridian Corp
**Tool:** Claude Code (in the terminal)
**Prerequisite:** Complete Lesson 01. The file layout and folder rules introduced there apply here.

---

## Part 1: The S2P Problem

It is 10:00 Wednesday. Your category manager calls: "I just noticed we are paying $14.20 per unit for cable assemblies on last week's PO. The contract rate is $12.80. When did that change?" It did not change. Someone issued the PO at the wrong price, and the system accepted it without checking. The difference is $1.40 per unit. At 2,000 units per order, that is $2,800 lost on a single transaction. Across 384 purchase orders in the quarter, unchecked pricing drift adds up fast. Meridian Corp has contracted rates for its key suppliers. Checking every PO line against those rates by hand takes two days. Claude Code does it in minutes and produces a ranked overcharge list you can send to suppliers for credit.

---

## Part 2: What Claude Code Is Going to Do for You

Claude Code will read every purchase order line, match it to the contracted rate for that item and supplier, and flag any line where the PO price deviates by more than 1% from the contract. It will separate overcharges (you paid too much) from undercharges (you paid too little), calculate the total dollar impact, and detect PO splitting: multiple small POs to the same supplier in a short window that together exceed an approval threshold. The output is a pricing compliance report with the total overcharge value, ranked so you can tackle the largest recovery first.

---

## Part 3: Set Up

1. Claude Code is installed and you are signed in.
2. The project folder `Course_15_Purchase_To_Pay_Intelligence/` is open in your terminal.
3. These files are in `practice/`:
   - `purchase-orders.csv` (384 rows)
   - `contracted-rates.csv` (10 rows)
4. `Drafts/` exists in the project folder.
5. OneDrive sync is paused.

---

## Part 4: Step-by-Step

**Step 1.** Open your terminal in the project folder and start Claude Code.

```
cd "Course_15_Purchase_To_Pay_Intelligence"
claude
```

You should see the Claude Code prompt with the folder name at the top.

**Step 2.** Set the read-only rule.

```
The folder Master/ holds the source reference files. Do not edit any file in Master/.
Read from practice/ freely. Save all output to Drafts/ unless I tell you otherwise.
```

You should see Claude Code confirm it understands.

**Step 3.** Read the contracted rates file and understand its structure.

```
Read practice/contracted-rates.csv. Tell me: how many rate entries are there,
what columns does it have, how are rates keyed (by supplier, item code, or both),
and do any entries have an effective date range?
```

You should see the rate structure described. The file should have columns like SUPPLIER_ID, ITEM_CODE, CONTRACTED_UNIT_PRICE, EFFECTIVE_FROM, and EFFECTIVE_TO. Each row is one supplier-item combination with a negotiated price.

If the file has fewer columns than expected: ask Claude to "Show me all rows in practice/contracted-rates.csv so I can see the full structure."

**Step 4.** Read the purchase orders file and understand its pricing columns.

```
Read practice/purchase-orders.csv. Tell me: what columns hold the unit price,
quantity, and total line value? What column holds the supplier identifier?
What column holds the item code? Show me three sample rows.
```

You should see the relevant column names confirmed. You need to know these before running the comparison so the match logic uses the right fields.

**Step 5.** Run the pricing comparison across all 384 PO lines.

```
Read practice/purchase-orders.csv and practice/contracted-rates.csv.
For each PO line, find the contracted rate by matching on SUPPLIER_ID and ITEM_CODE.
Compare the PO unit price to the contracted unit price.
Flag any line where the PO unit price deviates from the contracted price by more than 1%.
Write the results to Drafts/pricing_deviations.csv with columns:
PO_ID, LINE_NUMBER, SUPPLIER_ID, ITEM_CODE, PO_UNIT_PRICE, CONTRACTED_UNIT_PRICE,
DEVIATION_PCT, DEVIATION_PER_UNIT, QUANTITY, TOTAL_DEVIATION_USD.
Positive TOTAL_DEVIATION_USD means an overcharge. Negative means an undercharge.
Sort by TOTAL_DEVIATION_USD descending.
```

You should see Claude process all 384 rows and report how many deviations were found. Expect approximately 38 deviations based on the dataset.

If Claude finds zero deviations: check whether the SUPPLIER_ID format matches between the two files. Ask Claude: "Show me the first five SUPPLIER_ID values in purchase-orders.csv and the first five in contracted-rates.csv." A format mismatch (for example, "SUPP-001" vs. "S001") will prevent the join.

**Step 6.** Separate overcharges from undercharges.

```
Read Drafts/pricing_deviations.csv. Split into two groups:
overcharges (TOTAL_DEVIATION_USD greater than zero) and
undercharges (TOTAL_DEVIATION_USD less than zero).
For each group, tell me: count of lines, total dollar deviation,
and the top five lines by TOTAL_DEVIATION_USD.
Save this summary to Drafts/Pricing_Deviation_Summary.txt.
```

You should see a clear split between the two groups in the terminal and the summary saved.

**Step 7.** Check for PO splitting: multiple small POs to the same supplier that together exceed $25,000.

```
Read practice/purchase-orders.csv. Find cases where multiple POs were issued
to the same supplier within any 5-business-day window and the combined PO value
exceeds $25,000. Flag these as potential split orders. A split is more likely
if all POs in the cluster were raised by the same requester.
Write to Drafts/split_order_flags.csv with columns:
SUPPLIER_ID, PO_IDS, PO_DATES, INDIVIDUAL_VALUES, COMBINED_VALUE, SAME_REQUESTER.
```

You should see the file created with any suspected split-order clusters.

If no splits are found: that is a valid result. The dataset may not contain split patterns. Ask Claude to "Confirm the check ran by showing me the date range of POs in practice/purchase-orders.csv and the number of suppliers with more than one PO in the dataset."

**Step 8.** Build the full pricing compliance report.

```
Create Drafts/PO_Pricing_Compliance_Report.csv combining:
1. All rows from Drafts/pricing_deviations.csv with VIOLATION_TYPE = "Price_Deviation".
2. All rows from Drafts/split_order_flags.csv with VIOLATION_TYPE = "PO_Split".
Add a SEVERITY column: "High" if absolute value of TOTAL_DEVIATION_USD or COMBINED_VALUE
exceeds $10,000, "Medium" if $2,500 to $10,000, "Low" if below $2,500.
Sort by SEVERITY (High first), then by absolute dollar value descending.
```

You should see a single ranked report covering both violation types.

**Step 9.** Exit Claude Code.

```
/quit
```

You should see the terminal return to its normal command prompt.

---

## Part 5: Worked Example, End to End

**Starting files:**

```
Course_15_Purchase_To_Pay_Intelligence/
├── Master/          (read-only)
├── Drafts/          (output goes here)
└── practice/
    ├── purchase-orders.csv     (384 rows)
    └── contracted-rates.csv    (10 rows)
```

**Prompt 1:** read-only rule (same as Step 2 above).

**Prompt 2:** the pricing comparison from Step 5.
```
Read practice/purchase-orders.csv and practice/contracted-rates.csv.
For each PO line, find the contracted rate by matching on SUPPLIER_ID and ITEM_CODE.
Compare the PO unit price to the contracted unit price.
Flag any line where the PO unit price deviates from the contracted price by more than 1%.
Write to Drafts/pricing_deviations.csv with columns: PO_ID, LINE_NUMBER, SUPPLIER_ID,
ITEM_CODE, PO_UNIT_PRICE, CONTRACTED_UNIT_PRICE, DEVIATION_PCT, DEVIATION_PER_UNIT,
QUANTITY, TOTAL_DEVIATION_USD. Sort by TOTAL_DEVIATION_USD descending.
```

**What you should see** when this succeeds: "Found 38 pricing deviations. Saved to Drafts/pricing_deviations.csv."

**Sample rows from `Drafts/pricing_deviations.csv`:**

```
PO_ID,    LINE, SUPPLIER_ID, ITEM_CODE,  PO_UNIT, CONTRACT, DEV_PCT, DEV_PER_UNIT, QTY,  TOTAL_DEV_USD
PO-0189,  1,    SUPP-04,     CABL-2201,  14.20,   12.80,    10.9%,   1.40,         2000, 2800.00
PO-0234,  2,    SUPP-07,     FILT-0088,  87.50,   84.00,    4.2%,    3.50,         500,  1750.00
PO-0301,  1,    SUPP-02,     BRKT-1144,  22.00,   23.10,    -4.8%,   -1.10,        300,  -330.00
```

**What Claude Code did, behind the scenes:**

1. Claude Code read `contracted-rates.csv` and built an internal lookup dictionary keyed on SUPPLIER_ID plus ITEM_CODE, with the contracted unit price as the value.
2. It read each of the 384 rows in `purchase-orders.csv` and extracted SUPPLIER_ID, ITEM_CODE, PO_UNIT_PRICE, and QUANTITY.
3. For each row, it searched the lookup dictionary for a matching SUPPLIER_ID and ITEM_CODE combination.
4. Where a match existed, it calculated the percentage deviation: (PO_UNIT_PRICE minus CONTRACTED_UNIT_PRICE) divided by CONTRACTED_UNIT_PRICE, multiplied by 100.
5. It filtered to rows where the absolute deviation exceeded 1%.
6. It calculated TOTAL_DEVIATION_USD as DEVIATION_PER_UNIT multiplied by QUANTITY.
7. It sorted the violations by TOTAL_DEVIATION_USD descending and wrote the output file.
8. For the split-order check, it grouped POs by supplier and sorted by date, then used a sliding window to find clusters within five business days where the combined value exceeded $25,000.

**Finished artifacts:**
- `Drafts/pricing_deviations.csv`: all PO lines with price deviations above 1%, sorted by total overcharge.
- `Drafts/Pricing_Deviation_Summary.txt`: overcharge vs. undercharge totals, top five lines each.
- `Drafts/split_order_flags.csv`: suspected split-order clusters.
- `Drafts/PO_Pricing_Compliance_Report.csv`: combined, ranked report with severity flags.

---

## Part 6: Common Mistakes and How to Recover

- **Symptom:** Claude finds zero pricing deviations even though you can see a price difference in the data. **Fix:** the contracted rate and PO price may use different units of measure. For example, the contracted rate is per box but the PO is per unit. Ask Claude: "Check whether the UNIT_OF_MEASURE field differs between purchase-orders.csv and contracted-rates.csv. If it does, convert to a common unit before comparing."

- **Symptom:** The split-order check flags legitimate consecutive orders for different items. **Fix:** add a filter. Ask Claude: "Only flag split-order clusters where the same ITEM_CODE appears on more than one PO in the cluster. Different items to the same supplier on consecutive days are normal purchasing behavior."

- **Symptom:** Some contracted rates have an EFFECTIVE_TO date in the past, and Claude is still matching against them. **Fix:** ask Claude: "When matching a PO to a contracted rate, only use rate rows where the PO date falls between EFFECTIVE_FROM and EFFECTIVE_TO. Ignore expired rates."

- **Symptom:** The total deviation in the summary does not match the sum of individual rows. **Fix:** ask Claude: "Recalculate the sum of TOTAL_DEVIATION_USD from Drafts/pricing_deviations.csv and show the arithmetic. Compare it to the figure in Drafts/Pricing_Deviation_Summary.txt."

- **Symptom:** POs with no matching contracted rate are missing from the report, but you want to track uncontracted spend too. **Fix:** ask Claude: "Add a third section to Drafts/PO_Pricing_Compliance_Report.csv for PO lines with no matching contracted rate. Set VIOLATION_TYPE to Uncontracted_Purchase. Show SUPPLIER_ID, ITEM_CODE, PO_UNIT_PRICE, QUANTITY, and a column TOTAL_UNCONTRACTED_VALUE."
