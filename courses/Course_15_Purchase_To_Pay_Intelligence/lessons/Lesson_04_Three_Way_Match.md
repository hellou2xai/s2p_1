# Lesson 04: Three-Way Match Automation: Connecting POs, Goods Receipts, and Invoices to Find Mismatches

**Estimated time:** 60 minutes
**Role:** P2P Analytics Lead, Meridian Corp
**Tool:** Claude Code (in the terminal)
**Prerequisite:** Complete Lessons 01 and 03. The join keys and column names are established in those lessons.

---

## Part 1: The S2P Problem

It is 14:00 Thursday. Accounts payable at Meridian Corp has put a $42,000 invoice on hold. The supplier says they shipped everything. The warehouse says they received everything. But the numbers do not agree: the PO says 500 units at $84.00, the goods receipt shows 480 units received, and the invoice claims 500 units at $87.50. Three documents, three different stories. Your AP team spends 40 minutes per exception reconciling these mismatches by hand. With 168 invoices in the quarter and a 25% exception rate, that is 42 exceptions at 40 minutes each, or 28 hours per month of manual work. Claude Code automates the full three-way match across all 168 invoices and delivers a structured exception file AP can work from the same afternoon.

---

## Part 2: What Claude Code Is Going to Do for You

Claude Code will perform a three-way match across every invoice. For each invoice line, it checks: does the PO exist, is there a goods receipt for that PO, does the invoiced quantity match what was received, and does the invoiced unit price match the PO price? Any invoice that fails one or more of those checks is flagged as an exception, with the specific mismatch type and the dollar difference. The output is a ranked exception report with recommended actions, so AP can clear holds faster and stop overpaying.

---

## Part 3: Set Up

1. Claude Code is installed and you are signed in.
2. The project folder `Course_15_Purchase_To_Pay_Intelligence/` is open in your terminal.
3. These files are in `practice/`:
   - `purchase-orders.csv` (384 rows)
   - `goods-receipts.csv` (273 rows)
   - `invoices.csv` (168 rows)
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

**Step 3.** Confirm the join keys between all three files before running the match.

```
Read practice/purchase-orders.csv, practice/goods-receipts.csv, and practice/invoices.csv.
Tell me: what column in goods-receipts.csv links to purchase-orders.csv,
and what column in invoices.csv links to goods-receipts.csv or purchase-orders.csv?
Show me three sample values from each join key column so I can confirm the format matches.
```

You should see the join keys confirmed with sample values. This step prevents the match from silently failing because of a key format mismatch.

If the key formats differ between files: ask Claude to "Note the format difference and normalize the keys before running the match. For example, strip leading zeros or add a prefix to make the formats consistent."

**Step 4.** Define the three-way match rules so Claude applies them consistently.

```
Save these three-way match rules to Drafts/Three_Way_Match_Rules.txt:

A three-way match compares three documents for the same transaction.

Document 1: Purchase Order (PO). The authorized order. Contains agreed quantity and price.
Document 2: Goods Receipt (GR). Confirms what was physically received.
Document 3: Invoice (INV). The supplier's payment request.

All five conditions must pass for a match:
1. A PO exists for the invoice's PO reference number.
2. A GR exists for the same PO reference number.
3. Invoice quantity is less than or equal to GR quantity. You cannot invoice for more than received.
4. Invoice unit price is within 2% of PO unit price.
5. Invoice total equals invoice quantity multiplied by invoice unit price (arithmetic check).

Exception codes:
- NO_PO: Invoice references a PO that does not exist.
- NO_GR: PO exists but no goods receipt is recorded.
- QTY_MISMATCH: Invoice quantity exceeds GR quantity.
- PRICE_MISMATCH: Invoice unit price deviates more than 2% from PO unit price.
- ARITHMETIC_ERROR: Invoice total does not equal quantity multiplied by unit price.
```

You should see confirmation that `Drafts/Three_Way_Match_Rules.txt` was created.

**Step 5.** Run the three-way match across all 168 invoices.

```
Read practice/purchase-orders.csv, practice/goods-receipts.csv, and practice/invoices.csv.
Read the match rules from Drafts/Three_Way_Match_Rules.txt.
For each invoice line, apply all five match conditions.
Write results to Drafts/three_way_match_results.csv with columns:
INV_ID, PO_ID, GR_ID, INV_QTY, GR_QTY, INV_UNIT_PRICE, PO_UNIT_PRICE,
INV_TOTAL, CALCULATED_TOTAL, MATCH_STATUS (Matched or Exception),
EXCEPTION_CODES (pipe-separated if more than one).
```

You should see Claude process all 168 invoices. Expect approximately 42 exceptions (25% of 168).

If the exception count is much higher than expected: ask Claude to "Show me five example matched invoices so I can confirm the match logic is working correctly before reviewing exceptions."

**Step 6.** Get the exception breakdown by type.

```
Read Drafts/three_way_match_results.csv. Give me:
1. Total invoices: [count].
2. Matched: [count] ([percentage]%).
3. Exception: [count] ([percentage]%).
4. For each exception code (NO_PO, NO_GR, QTY_MISMATCH, PRICE_MISMATCH, ARITHMETIC_ERROR),
   give the count and total dollar value of invoices carrying that code.
Which exception type has the highest total dollar value?
```

You should see a breakdown table. PRICE_MISMATCH and QTY_MISMATCH typically carry the most dollar value.

**Step 7.** Build the AP exception workfile with recommended actions.

```
Read Drafts/three_way_match_results.csv and practice/purchase-orders.csv.
Filter to exception rows only.
Create Drafts/AP_Exception_Workfile.csv with columns:
INV_ID, PO_ID, SUPPLIER_NAME (join from purchase-orders.csv on PO_ID),
EXCEPTION_CODES, INV_AMOUNT, PO_AMOUNT, DIFFERENCE_USD,
RECOMMENDED_ACTION.

Use these action rules:
NO_PO: Return to supplier. Request valid PO reference before any payment.
NO_GR: Hold payment. Confirm receipt with warehouse before releasing.
QTY_MISMATCH: Short pay to GR quantity. Notify supplier of the shortfall.
PRICE_MISMATCH: Hold. Verify contracted rate. Issue debit memo if PO price is correct.
ARITHMETIC_ERROR: Return to supplier for a corrected invoice.

Sort by absolute value of DIFFERENCE_USD descending.
```

You should see the exception workfile created with every exception given a clear action and a dollar impact.

**Step 8.** Calculate the financial and time impact of the exception rate.

```
Read Drafts/AP_Exception_Workfile.csv. Calculate and write to
Drafts/Three_Way_Match_Impact.txt:
1. Total value of invoices on hold (sum of INV_AMOUNT for all exceptions).
2. Total overcharge amount (sum of positive DIFFERENCE_USD where invoice exceeds PO).
3. Total undercharge amount (sum of negative DIFFERENCE_USD).
4. Estimated monthly AP labor hours saved if the exception rate drops from 25% to 5%,
   assuming 40 minutes per exception to resolve manually.
   Show the arithmetic: current exceptions per month minus target exceptions per month,
   multiplied by 40 minutes, divided by 60 to get hours.
```

You should see specific dollar and time figures. This is the business case for fixing the root causes.

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
    ├── purchase-orders.csv  (384 rows)
    ├── goods-receipts.csv   (273 rows)
    └── invoices.csv         (168 rows)
```

**Prompt 1:** read-only rule (same as Step 2 above).

**Prompt 2:** the match rules definition from Step 4.

**Prompt 3:** the three-way match from Step 5.
```
Read practice/purchase-orders.csv, practice/goods-receipts.csv, and practice/invoices.csv.
Read the match rules from Drafts/Three_Way_Match_Rules.txt.
For each invoice line, apply all five match conditions.
Write results to Drafts/three_way_match_results.csv with columns:
INV_ID, PO_ID, GR_ID, INV_QTY, GR_QTY, INV_UNIT_PRICE, PO_UNIT_PRICE,
INV_TOTAL, CALCULATED_TOTAL, MATCH_STATUS, EXCEPTION_CODES.
```

**What you should see** when Prompt 3 succeeds: "Processed 168 invoices. 126 matched, 42 exceptions. Saved to Drafts/three_way_match_results.csv."

**Sample rows from `Drafts/AP_Exception_Workfile.csv`:**

```
INV_ID,   PO_ID,   SUPPLIER_NAME,           EXCEPTION_CODES,             INV_AMOUNT, PO_AMOUNT, DIFF_USD, RECOMMENDED_ACTION
INV-0087, PO-0189, Northwind Industrial LLC, PRICE_MISMATCH,              42000,      40000,     2000,     Hold. Verify contracted rate. Issue debit memo if PO price is correct.
INV-0103, PO-0234, Acme Components Inc,      QTY_MISMATCH,                25200,      24000,     1200,     Short pay to GR quantity. Notify supplier of the shortfall.
INV-0141, PO-0301, Globex Supply Co,         NO_GR,                       18500,      18500,     0,        Hold payment. Confirm receipt with warehouse before releasing.
```

**What Claude Code did, behind the scenes:**

1. Claude Code built two lookup dictionaries: one from `purchase-orders.csv` (keyed on PO_ID), and one from `goods-receipts.csv` (keyed on PO_ID).
2. For each of the 168 invoices, it checked whether the PO_ID existed in the PO lookup. If not, it assigned NO_PO.
3. For invoices with a valid PO_ID, it checked whether the PO_ID existed in the GR lookup. If not, it assigned NO_GR.
4. Where both PO and GR existed, it compared INV_QTY to GR_QTY. If INV_QTY exceeded GR_QTY, it assigned QTY_MISMATCH.
5. It calculated the percentage deviation between INV_UNIT_PRICE and PO_UNIT_PRICE. Deviations above 2% received PRICE_MISMATCH.
6. It multiplied INV_QTY by INV_UNIT_PRICE and compared the result to INV_TOTAL. Differences received ARITHMETIC_ERROR.
7. It collected all exception codes for each invoice into a pipe-separated string and wrote the results file.
8. For the workfile, it joined SUPPLIER_NAME from `purchase-orders.csv` using PO_ID, then applied the action rules to each exception code.

**Finished artifacts:**
- `Drafts/Three_Way_Match_Rules.txt`: the match logic saved for reference.
- `Drafts/three_way_match_results.csv`: all 168 invoices with match status and exception codes.
- `Drafts/AP_Exception_Workfile.csv`: 42 exceptions with supplier names, dollar impact, and recommended actions.
- `Drafts/Three_Way_Match_Impact.txt`: total value on hold, overcharge exposure, and labor hours saved.

---

## Part 6: Common Mistakes and How to Recover

- **Symptom:** Every invoice shows NO_GR, but you can see goods receipts in the data. **Fix:** the join key between `goods-receipts.csv` and `invoices.csv` may use different column names. Ask Claude: "Show me the column names in goods-receipts.csv and invoices.csv that should link the two files. If the names differ, use the column with matching ID values as the join key."

- **Symptom:** The 2% price tolerance flags hundreds of small rounding differences on low-value lines. **Fix:** add a minimum dollar threshold. Ask Claude: "Only flag PRICE_MISMATCH where the price deviation exceeds 2% AND the total dollar difference (DIFFERENCE_USD) exceeds $50."

- **Symptom:** One invoice has multiple exception codes but only the first appears in the CSV. **Fix:** ask Claude: "Store all exception codes for each invoice as a pipe-separated value in one cell, for example: PRICE_MISMATCH|QTY_MISMATCH. Do not drop additional codes."

- **Symptom:** Invoices with a blank PO reference are silently excluded from the results. **Fix:** ask Claude: "Include invoices with a blank or null PO_ID in the results. Classify them as NO_PO exceptions, since we cannot verify what they were issued against."

- **Symptom:** DIFFERENCE_USD is always zero for QTY_MISMATCH rows. **Fix:** for quantity mismatches, the dollar difference should be calculated as (INV_QTY minus GR_QTY) multiplied by PO_UNIT_PRICE. Ask Claude to "Recalculate DIFFERENCE_USD for QTY_MISMATCH rows using that formula."
