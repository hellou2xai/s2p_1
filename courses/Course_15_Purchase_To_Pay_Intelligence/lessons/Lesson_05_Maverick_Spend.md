# Lesson 05: Maverick Spend Detection: Identifying Purchases Outside Preferred Suppliers

**Estimated time:** 50 minutes
**Role:** P2P Analytics Lead, Meridian Corp
**Tool:** Claude Code (in the terminal)
**Prerequisite:** Complete Lessons 01 and 02. The preferred supplier list and category mapping are introduced there.

---

## Part 1: The S2P Problem

It is 09:30 Friday. Your CPO stops by your desk: "I need a number. How much are we spending outside our contracts?" You know Meridian Corp has negotiated rates with 20 preferred suppliers across eight categories. You also know that not every buyer uses them. Some buyers go direct to a local vendor they know. Some go to a catalog site that is not on the approved list. Some raise a PO to a preferred supplier but at the wrong price. After two hours of manual filtering across 384 purchase orders, you might have an estimate. Your CPO wants the exact number, broken down by category, with the cost of the price premium annualized so it is comparable to the savings targets set at the start of the year. Claude Code does this in under 15 minutes and produces a one-page report your CPO can take into the quarterly business review.

---

## Part 2: What Claude Code Is Going to Do for You

Claude Code will classify every purchase order as compliant or maverick. Compliant means: preferred supplier, at or below the contracted rate, through the correct channel. Maverick means: non-preferred supplier when one exists, or preferred supplier at an above-contract price. Claude will calculate the total price premium paid on maverick spend, annualize it based on the period covered by the data, break it down by category, and identify the top ten requesters by maverick spend volume. The CPO gets a one-page report with three recommendations and specific dollar amounts, not a vague savings estimate.

---

## Part 3: Set Up

1. Claude Code is installed and you are signed in.
2. The project folder `Course_15_Purchase_To_Pay_Intelligence/` is open in your terminal.
3. These files are in `practice/`:
   - `purchase-orders.csv` (384 rows)
   - `contracted-rates.csv` (10 rows)
   - `preferred-suppliers.csv` (20 rows)
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

**Step 3.** Establish the maverick spend definitions before running any classification.

```
Save these maverick spend definitions to Drafts/Maverick_Spend_Rules.txt:

Maverick spend is any purchase outside the preferred supply channel.
Three types:

1. OFF_CONTRACT_SUPPLIER: The PO goes to a supplier not on the preferred list
   for that category, when a preferred supplier exists for that category.

2. OFF_CONTRACT_PRICE: The PO goes to a preferred supplier but at a unit price
   more than 2% above the contracted rate.

3. OFF_CHANNEL: The PO bypasses the designated buying channel
   (for example, a catalog item purchased via a manual PO).

Compliant: PO to a preferred supplier, at or below the contracted rate,
through the correct channel.

Not maverick (uncovered category): The purchase is in a category where
no preferred supplier exists. Do not flag these as maverick.
Do count them separately as uncovered spend.

Price premium per line = (PO unit price minus contracted unit price) x quantity.
If no contracted rate exists, the price premium cannot be calculated.

Annualized price premium = total price premium in the data period
multiplied by (12 divided by number of months covered by the data).
```

You should see confirmation that `Drafts/Maverick_Spend_Rules.txt` was created.

**Step 4.** Classify every PO line as compliant, maverick, or uncovered.

```
Read practice/purchase-orders.csv, practice/contracted-rates.csv,
and practice/preferred-suppliers.csv.
Read the classification rules from Drafts/Maverick_Spend_Rules.txt.
For each PO line, classify it as: Compliant, OFF_CONTRACT_SUPPLIER,
OFF_CONTRACT_PRICE, OFF_CHANNEL, or Uncovered.
Write to Drafts/maverick_classification.csv with columns:
PO_ID, LINE_NUMBER, SUPPLIER_ID, CATEGORY, ITEM_CODE, QUANTITY,
PO_UNIT_PRICE, CONTRACTED_UNIT_PRICE, CLASSIFICATION,
PRICE_PREMIUM_PER_UNIT, TOTAL_PREMIUM_USD.
```

You should see Claude process all 384 PO lines and write the classification file. Expect a mix of compliant, maverick, and uncovered rows.

If many rows come back as Uncovered when they should be classified: ask Claude: "Show me the first five values of CATEGORY in purchase-orders.csv and the first five values of CATEGORY in preferred-suppliers.csv. Check whether the category names match exactly or differ in spacing or capitalization."

**Step 5.** Summarize maverick spend by category.

```
Read Drafts/maverick_classification.csv. Group by CATEGORY.
For each category, calculate: total PO value, compliant spend,
maverick spend, maverick percentage, and sum of TOTAL_PREMIUM_USD.
Write to Drafts/Maverick_By_Category.csv. Sort by maverick spend descending.
```

You should see a category table showing which areas have the most maverick activity. The categories at the top are where your CPO will want to focus first.

**Step 6.** Calculate the annualized cost of maverick spend.

```
Read Drafts/maverick_classification.csv. Calculate:
1. Total maverick spend (sum of PO line values classified as maverick).
2. Total price premium (sum of TOTAL_PREMIUM_USD for all maverick rows).
3. Date range of the data: earliest and latest PO_DATE in practice/purchase-orders.csv.
4. Number of months covered (round to one decimal place).
5. Annualized price premium: total price premium multiplied by (12 divided by months covered).
Write these five figures to Drafts/Maverick_Cost_Analysis.txt.
Show the arithmetic for the annualized calculation so I can verify it.
```

You should see specific dollar figures and the annualization arithmetic shown step by step.

**Step 7.** Find the top ten requesters by maverick spend.

```
Read Drafts/maverick_classification.csv and practice/purchase-orders.csv.
Join on PO_ID to get the REQUESTER field from purchase-orders.csv.
Find the top ten requesters by total maverick spend.
For each, show: REQUESTER, DEPT, total maverick POs (count), total maverick value,
and the most common CLASSIFICATION for that requester.
Write to Drafts/Maverick_Top_Requesters.csv.
```

You should see a ranked list. This is the data your CPO needs to have conversations with department heads.

**Step 8.** Write the one-page CPO report.

```
Write Drafts/Maverick_Spend_Report.txt for the CPO.
Use today's date: 2026-04-25.
Include exactly these sections:

1. Headline: Total maverick spend in the period, as a dollar amount and
   a percentage of Meridian Corp's $140M annual procurement spend.
2. Annualized price premium: the extra cost paid per year versus contracted rates.
3. Top three categories by maverick spend with exact dollar amounts.
4. Three recommendations (no more than three):
   each with the expected dollar impact if implemented.

Every figure must be a specific number in USD. No vague language.
Replace any estimate with the exact dollar amount from the data.
If a figure is unknown, write [TBC: figure].
```

You should see a one-page report with four sections and specific numbers throughout.

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
    ├── contracted-rates.csv    (10 rows)
    └── preferred-suppliers.csv (20 rows)
```

**Prompt 1:** read-only rule (same as Step 2 above).

**Prompt 2:** classification rules saved in Step 3.

**Prompt 3:** the classification run from Step 4.
```
Read practice/purchase-orders.csv, practice/contracted-rates.csv,
and practice/preferred-suppliers.csv.
Read the classification rules from Drafts/Maverick_Spend_Rules.txt.
For each PO line, classify it as: Compliant, OFF_CONTRACT_SUPPLIER,
OFF_CONTRACT_PRICE, OFF_CHANNEL, or Uncovered.
Write to Drafts/maverick_classification.csv with columns:
PO_ID, LINE_NUMBER, SUPPLIER_ID, CATEGORY, ITEM_CODE, QUANTITY,
PO_UNIT_PRICE, CONTRACTED_UNIT_PRICE, CLASSIFICATION,
PRICE_PREMIUM_PER_UNIT, TOTAL_PREMIUM_USD.
```

**What you should see** when Prompt 3 succeeds: "Classified 384 PO lines. 214 Compliant, 89 OFF_CONTRACT_SUPPLIER, 47 OFF_CONTRACT_PRICE, 22 OFF_CHANNEL, 12 Uncovered. Saved to Drafts/maverick_classification.csv."

**Sample rows from `Drafts/Maverick_By_Category.csv`:**

```
CATEGORY,         TOTAL_SPEND, COMPLIANT, MAVERICK,  MAVERICK_PCT, PRICE_PREMIUM_USD
IT Hardware,      412000,      271000,    141000,    34.2%,        18400
MRO Supplies,     287000,      207000,    80000,     27.9%,        9600
Office Supplies,  94000,       79000,     15000,     16.0%,        1800
```

**What Claude Code did, behind the scenes:**

1. Claude Code built two reference tables: a preferred supplier list keyed on CATEGORY and SUPPLIER_ID, and a contracted rates dictionary keyed on SUPPLIER_ID plus ITEM_CODE.
2. For each PO line, it first checked whether the CATEGORY had any preferred supplier in the preferred-suppliers table. If not, the line was classified as Uncovered.
3. If a preferred supplier existed for the category, it checked whether the PO's SUPPLIER_ID was in that preferred list. If not, it assigned OFF_CONTRACT_SUPPLIER.
4. If the supplier was preferred, it looked up the contracted rate for the SUPPLIER_ID and ITEM_CODE combination. If the PO unit price exceeded the contracted rate by more than 2%, it assigned OFF_CONTRACT_PRICE.
5. It calculated PRICE_PREMIUM_PER_UNIT as PO_UNIT_PRICE minus CONTRACTED_UNIT_PRICE (only for OFF_CONTRACT_PRICE rows), and TOTAL_PREMIUM_USD as PRICE_PREMIUM_PER_UNIT multiplied by QUANTITY.
6. It grouped by CATEGORY and summed compliant and maverick spend for the category table.
7. For annualization, it found the MIN and MAX of PO_DATE, calculated the number of months, and multiplied the total premium by (12 / months).

**Finished artifacts:**
- `Drafts/Maverick_Spend_Rules.txt`: the classification rules for reference.
- `Drafts/maverick_classification.csv`: every PO line classified and tagged.
- `Drafts/Maverick_By_Category.csv`: category-level summary with maverick percentages.
- `Drafts/Maverick_Cost_Analysis.txt`: total maverick spend, price premium, and annualized cost.
- `Drafts/Maverick_Top_Requesters.csv`: top ten requesters by maverick spend.
- `Drafts/Maverick_Spend_Report.txt`: the one-page CPO briefing note.

---

## Part 6: Common Mistakes and How to Recover

- **Symptom:** Almost every PO is classified as OFF_CONTRACT_SUPPLIER, giving an implausibly high maverick rate. **Fix:** the category names probably differ between files. Ask Claude: "List all unique CATEGORY values in purchase-orders.csv and all unique CATEGORY values in preferred-suppliers.csv side by side. Highlight any that do not match exactly." Fix the category mapping, then rerun the classification.

- **Symptom:** The annualized premium calculation is much higher than expected. **Fix:** confirm the data period is correct. Ask Claude: "What is the earliest PO_DATE and the latest PO_DATE in practice/purchase-orders.csv? How many months does that span?" If the span is less than one month (for example, a single-week extract), the annualization will multiply by a large factor and distort the result.

- **Symptom:** The CPO report uses vague language despite your instruction to use specific numbers. **Fix:** ask Claude: "Review every sentence in Drafts/Maverick_Spend_Report.txt. Replace any sentence using the words 'significant,' 'considerable,' 'material,' or 'substantial' with the exact number from Drafts/Maverick_Cost_Analysis.txt."

- **Symptom:** Uncovered spend (no preferred supplier exists) is counted in the maverick total, inflating the number. **Fix:** ask Claude: "Remove all rows with CLASSIFICATION = Uncovered from the maverick totals. Report uncovered spend as a separate figure. Only OFF_CONTRACT_SUPPLIER, OFF_CONTRACT_PRICE, and OFF_CHANNEL rows should count as maverick."

- **Symptom:** The top requester list shows names but no department, making it hard to know who to approach. **Fix:** ask Claude: "Re-join Drafts/Maverick_Top_Requesters.csv to practice/purchase-orders.csv using PO_ID to add the DEPT column. Include department in the output so the CPO can route the conversation to the right manager."
