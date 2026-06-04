# Lesson 06: Payment Terms Optimization: Finding Gaps Between Contracted Terms and Actual Invoice Terms

**Estimated time:** 50 minutes
**Role:** P2P Analytics Lead, Meridian Corp
**Tool:** Claude Code (in the terminal)
**Prerequisite:** Complete Lesson 01. The invoice file structure is established there.

---

## Part 1: The S2P Problem

It is 11:00 Monday. Your CFO asks you two questions: "How many invoices last quarter offered an early payment discount, and how many did we actually capture?" Your AP team processes invoices as they arrive and pays them on a fixed weekly run. Nobody tracks whether a 2/10 Net 30 discount window is open or closed at the time of payment. Last quarter, Meridian Corp had 24 invoices carrying an early payment discount. AP captured 8 of them. The other 16 were paid after the discount window closed, leaving $6,780 on the table. At the same time, 14 invoices are past their due date, and three carry a 1.5% per month late penalty clause. Claude Code reads all 168 invoices, calculates aging for each one, identifies every discount window, and tells you exactly which discounts are still capturable today and which penalties are already accruing.

---

## Part 2: What Claude Code Is Going to Do for You

Claude Code will parse the payment terms on every invoice, calculate how many days each invoice has been outstanding, flag all past-due invoices with their penalty exposure, and identify open discount windows with the dollar value still available to capture. You get three numbers your CFO asked for: discounts captured ($4,200), discounts missed ($5,800), and penalties at risk ($3,400). You also get a priority action list: pay these four invoices by 2026-04-28 to capture $2,100 in discounts before the window closes.

---

## Part 3: Set Up

1. Claude Code is installed and you are signed in.
2. The project folder `Course_15_Purchase_To_Pay_Intelligence/` is open in your terminal.
3. These files are in `practice/`:
   - `invoices.csv` (168 rows, including columns: INV_ID, INV_DATE, DUE_DATE, PAYMENT_DATE, PAYMENT_TERMS, INV_AMOUNT, PO_ID)
   - `purchase-orders.csv` (384 rows, for supplier name lookup)
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

**Step 3.** Profile the payment terms in the invoices file.

```
Read practice/invoices.csv. List all unique values in the PAYMENT_TERMS column
with their row counts. Also tell me:
1. How many invoices have PAYMENT_DATE populated (already paid)?
2. How many have PAYMENT_DATE blank or null (still open and unpaid)?
3. What is the earliest and latest INV_DATE in the file?
```

You should see a breakdown of payment terms, a paid vs. open count, and the date range. Terms like "2/10 Net 30" mean a 2% discount if paid within 10 days, otherwise the full amount is due in 30 days.

If PAYMENT_TERMS values use inconsistent formats (for example, "Net30" vs. "Net 30"): ask Claude to "List all unique raw values in PAYMENT_TERMS so I can see every format variant before we parse them."

**Step 4.** Calculate aging for every invoice.

```
Read practice/invoices.csv. Today's date is 2026-04-25.
For each invoice, calculate:
1. DAYS_OUTSTANDING: today minus INV_DATE.
2. DAYS_UNTIL_DUE: DUE_DATE minus today. Negative means past due.
3. AGING_BUCKET:
   - "Current" if DAYS_UNTIL_DUE is greater than zero.
   - "1 to 30 Past Due" if 1 to 30 days past the due date.
   - "31 to 60 Past Due" if 31 to 60 days past.
   - "61 to 90 Past Due" if 61 to 90 days past.
   - "90 Plus Past Due" if more than 90 days past.
4. For paid invoices (PAYMENT_DATE is populated): DAYS_TO_PAY = PAYMENT_DATE minus INV_DATE.
Write to Drafts/invoice_aging.csv.
```

You should see the file created with every invoice assigned an aging bucket and a DAYS_TO_PAY value where applicable.

If DAYS_UNTIL_DUE is positive for an invoice you know is overdue: check whether the DUE_DATE format in the CSV uses a different date format. Ask Claude: "Show me the raw DUE_DATE value for INV_ID [ID] and confirm how you are parsing it."

**Step 5.** Summarize aging for open (unpaid) invoices.

```
Read Drafts/invoice_aging.csv. Filter to invoices where PAYMENT_DATE is blank.
For each AGING_BUCKET, calculate: count of invoices, total INV_AMOUNT, and
percentage of total open value. Write to Drafts/Aging_Summary.csv.
Also give me the grand total: count and dollar value of all open invoices.
```

You should see a table with five rows (one per bucket) plus a total. Current-bucket invoices are the priority for discount capture. Past-due buckets are the priority for penalty avoidance.

**Step 6.** Identify early payment discount opportunities.

```
Read Drafts/invoice_aging.csv. Filter to invoices where PAYMENT_TERMS contains
a discount (any term with a percentage before a slash, such as "2/10 Net 30").
For each, calculate:
1. DISCOUNT_PCT: the percentage before the slash (2 in "2/10 Net 30").
2. DISCOUNT_WINDOW_DAYS: the number after the slash (10 in "2/10 Net 30").
3. DISCOUNT_VALUE: INV_AMOUNT multiplied by DISCOUNT_PCT divided by 100.
4. DISCOUNT_DEADLINE: INV_DATE plus DISCOUNT_WINDOW_DAYS.
5. DISCOUNT_STATUS:
   - "Captured" if PAYMENT_DATE is on or before DISCOUNT_DEADLINE.
   - "Missed" if PAYMENT_DATE is after DISCOUNT_DEADLINE.
   - "Open" if PAYMENT_DATE is blank and today is on or before DISCOUNT_DEADLINE.
   - "Expired" if PAYMENT_DATE is blank and today is after DISCOUNT_DEADLINE.
Write to Drafts/discount_analysis.csv. Sort by DISCOUNT_DEADLINE ascending.
```

You should see every discount-eligible invoice classified. "Open" invoices are the ones you can still act on today.

**Step 7.** Calculate penalty exposure for past-due invoices.

```
Read Drafts/invoice_aging.csv and practice/purchase-orders.csv.
Filter to open invoices (PAYMENT_DATE blank) where DAYS_UNTIL_DUE is negative.
For each, calculate PENALTY_ESTIMATE using a 1.5% per month late fee:
PENALTY_ESTIMATE = INV_AMOUNT multiplied by 0.015 multiplied by
(absolute value of DAYS_UNTIL_DUE divided by 30).
Join SUPPLIER_NAME from practice/purchase-orders.csv using PO_ID.
Write to Drafts/penalty_exposure.csv with columns:
INV_ID, SUPPLIER_NAME, INV_AMOUNT, DUE_DATE, DAYS_PAST_DUE, PENALTY_ESTIMATE.
Sort by PENALTY_ESTIMATE descending.
Also give me the total PENALTY_ESTIMATE across all past-due invoices.
```

You should see the penalty list with a total at the bottom.

**Step 8.** Write the payment optimization report for the CFO.

```
Write Drafts/Payment_Terms_Report.txt with today's date: 2026-04-25.
Include exactly these four sections:

1. Aging Summary: a table from Drafts/Aging_Summary.csv showing buckets,
   counts, and dollar values.

2. Discount Performance:
   - Discounts captured: [count], $[value] saved.
   - Discounts missed: [count], $[value] lost.
   - Discounts still open: [count], $[value] available. Deadline: [earliest deadline date].

3. Penalty Exposure:
   - Total past-due open invoices: [count], $[value].
   - Total estimated late penalty: $[amount].
   - Top three invoices by penalty amount: INV_ID, supplier, days past due, penalty.

4. Three recommendations (no more than three), each with a specific dollar impact:
   for example, "Pay INV-0042, INV-0088, INV-0103, and INV-0127 by 2026-04-28
   to capture $2,100 in early payment discounts."

Every figure must be in USD. Use exact numbers from the data.
```

You should see the report saved with all four sections completed with real numbers.

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
    ├── invoices.csv         (168 rows)
    └── purchase-orders.csv  (384 rows)
```

**Prompt 1:** read-only rule (same as Step 2 above).

**Prompt 2:** the aging calculation from Step 4.
```
Read practice/invoices.csv. Today's date is 2026-04-25.
For each invoice, calculate: DAYS_OUTSTANDING, DAYS_UNTIL_DUE, AGING_BUCKET,
and DAYS_TO_PAY for paid invoices. Write to Drafts/invoice_aging.csv.
```

**Prompt 3:** the discount analysis from Step 6.
```
Read Drafts/invoice_aging.csv. Filter to invoices where PAYMENT_TERMS contains
a discount. For each, calculate DISCOUNT_PCT, DISCOUNT_WINDOW_DAYS, DISCOUNT_VALUE,
DISCOUNT_DEADLINE, and DISCOUNT_STATUS. Write to Drafts/discount_analysis.csv.
Sort by DISCOUNT_DEADLINE ascending.
```

**What you should see** when Prompt 3 succeeds: "Found 24 invoices with discount terms. 8 Captured, 10 Missed, 4 Open, 2 Expired. Saved to Drafts/discount_analysis.csv."

**Sample rows from `Drafts/discount_analysis.csv`:**

```
INV_ID,   INV_DATE,   PAYMENT_TERMS,  DISCOUNT_PCT, WINDOW_DAYS, DISCOUNT_VALUE, DEADLINE,   STATUS
INV-0042, 2026-04-20, 2/10 Net 30,    2%,           10,          $184,           2026-04-30, Open
INV-0088, 2026-04-18, 2/10 Net 30,    2%,           10,          $310,           2026-04-28, Open
INV-0103, 2026-04-15, 2/10 Net 30,    2%,           10,          $96,            2026-04-25, Open
INV-0127, 2026-04-17, 2/10 Net 30,    2%,           10,          $152,           2026-04-27, Open
```

**What Claude Code did, behind the scenes:**

1. Claude Code read the PAYMENT_TERMS field for each invoice and used a pattern match to detect terms containing a percentage followed by a day count (for example, "2/10 Net 30" parsed as 2% discount, 10-day window, 30-day net).
2. For each discount-eligible invoice, it calculated the DISCOUNT_DEADLINE by adding the discount window days to the INV_DATE.
3. For paid invoices, it compared PAYMENT_DATE to DISCOUNT_DEADLINE. Payment on or before the deadline meant Captured; payment after meant Missed.
4. For unpaid invoices, it compared today's date (2026-04-25) to the DISCOUNT_DEADLINE. On or before meant Open; after meant Expired.
5. For aging, it subtracted INV_DATE from today to get DAYS_OUTSTANDING, and subtracted today from DUE_DATE to get DAYS_UNTIL_DUE. Negative DAYS_UNTIL_DUE values went into past-due buckets.
6. For the penalty estimate, it used the formula: INV_AMOUNT times 0.015 times (days past due divided by 30). This is a monthly rate prorated by days.
7. It joined SUPPLIER_NAME from `purchase-orders.csv` using PO_ID as the link key.

**Finished artifacts:**
- `Drafts/invoice_aging.csv`: all 168 invoices with aging buckets and days outstanding.
- `Drafts/Aging_Summary.csv`: five-bucket summary of open invoice count and value.
- `Drafts/discount_analysis.csv`: all discount-eligible invoices with status and deadline.
- `Drafts/penalty_exposure.csv`: all past-due open invoices with penalty estimates.
- `Drafts/Payment_Terms_Report.txt`: the four-section CFO briefing note with exact figures.

---

## Part 6: Common Mistakes and How to Recover

- **Symptom:** The discount analysis finds zero invoices with discount terms even though you can see "2/10 Net 30" in the file. **Fix:** the payment terms field may use a variant format such as "2% 10 Days Net 30" or "2-10-30". Ask Claude: "Show me all unique raw values in the PAYMENT_TERMS column. For any value that contains both a percentage and a day count, treat it as a discount term and parse accordingly."

- **Symptom:** All open invoices show DISCOUNT_STATUS as "Expired" even for invoices issued this week. **Fix:** Claude may be comparing dates as text strings instead of actual dates, which sorts incorrectly. Ask Claude: "Confirm you are parsing INV_DATE and DISCOUNT_DEADLINE as dates, not as text. Show me the parsed values for INV-0042 so I can verify."

- **Symptom:** The aging bucket totals do not add up to the total open invoice value. **Fix:** one or more invoices may be missing from the bucket assignment. Ask Claude: "Confirm that every open invoice in Drafts/invoice_aging.csv is assigned to exactly one AGING_BUCKET. List any invoice with a blank or null AGING_BUCKET."

- **Symptom:** The penalty calculation seems too high because it assumes 1.5% per month for all suppliers. **Fix:** note the assumption explicitly in the report. Ask Claude: "Add a footnote to Drafts/Payment_Terms_Report.txt: Penalty estimates use a standard rate of 1.5% per month. Actual rates vary by supplier contract. Confirm the rate with each supplier before accruing a liability."

- **Symptom:** The CFO report recommendations are vague, such as "pay invoices sooner." **Fix:** ask Claude: "Replace each recommendation in Drafts/Payment_Terms_Report.txt with a specific action: the invoice ID, the supplier name, the payment amount, the deadline date, and the dollar benefit. For example: Pay INV-0088 to Northwind Industrial LLC ($15,500) by 2026-04-28 to capture a $310 early payment discount."
