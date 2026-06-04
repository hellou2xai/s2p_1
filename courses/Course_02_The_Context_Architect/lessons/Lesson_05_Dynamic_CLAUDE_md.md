# Lesson 5: Pointing at data files instead of repeating them

**Time:** 20 minutes. **You need:** Lesson 4 passing.

## A typical Wednesday afternoon

It is 14:30. Your data team Slacks: "We added two new suppliers to direct materials. Updated supplier list is in the same file."

If your direct-materials CLAUDE.md has the supplier list embedded in it (the names typed out, the spend numbers copied across), you now have to edit CLAUDE.md every time the data team updates the CSV. Every Monday. Forever.

There is a better way: keep CLAUDE.md as a **map** to your data files, not a copy of their contents. The CSV is the source of truth. CLAUDE.md just points at it. When the CSV changes, you change nothing.

You will check that your three category files are doing the right thing (pointing at files, not copying them), and you will add one small detail to each: a "last reviewed" date. Twenty minutes.

## The big idea

Your category file's "Files in this folder" section is the **map** to your data. It tells Claude:

- Where the file is (the file name, sitting next to the CLAUDE.md).
- What is in the file (the column headers).
- Roughly how often it changes.

When you ask Claude a question, Claude reads the CSV at runtime and gives you the current answer. You never have to update CLAUDE.md just because a CSV row changed. This is critical: the activity files in this practice (orders.csv, shipments.csv, invoices.csv) have thousands of rows that change all the time.

## Set up

**Step 1.** Open your terminal.

**Step 2.** Move to the direct-materials folder:

```
cd "Course_02_The_Context_Architect/practice/direct-materials"
```

**Step 3.** Open `CLAUDE.md` in your editor.

**The folder layout you are working in.**

```
practice/direct-materials/
├── CLAUDE.md               (you refine this file's "Files" section)
├── orders.csv              (2,500 PO rows, refreshed weekly)
└── suppliers.csv           (50 suppliers, refreshed on changes)
```

## Spot any data that should not be in CLAUDE.md

**Step 4.** Read your "Files in this folder" section. Look for these patterns. If you find any, delete them:

- A list of supplier names typed out ("Great Lakes Steel, Pacific Aluminum, Lone Star Plastics, ...").
- A specific spend number ("Great Lakes Steel was $240,000 last quarter").
- The exact contract end dates of every supplier.

These are all data, not rules. They live in the CSV. If they appear in your CLAUDE.md, every CSV update forces a CLAUDE.md update.

## Add the "last reviewed" detail

**Step 5.** Update your "Files in this folder" section to include three things per file: column headers, refresh note, last-reviewed date. Use this shape:

```
suppliers.csv
- the active supplier list, around 50 rows
- columns: supplier_id, supplier_name, state, makes,
  annual_value_usd, contract_end, status
- refreshed when a new supplier is added or a contract changes;
  last reviewed 2026-04-25

orders.csv
- recent purchase orders, around 2,500 rows over the last year
- columns: po_number, supplier_id, item, units, total_usd, po_date
- refreshed weekly from the orders system; last reviewed 2026-04-25
```

The "last reviewed" line is small but helpful. If you come back in three months and the date is months old, you know the column names in CLAUDE.md may not match the CSV any more, and you should re-check.

**Step 6.** Save.

**Step 7.** Repeat for `logistics/CLAUDE.md` (carriers.csv 20 rows, shipments.csv 5,000 rows) and `indirect/CLAUDE.md` (vendors.csv 80 rows, invoices.csv 3,000 rows). Same shape. Update the column lines from each CSV's actual headers. Set "last reviewed" to today (2026-04-25).

## Test it: confirm Claude reads the file fresh, every time

**Step 8.** Move to the direct-materials folder if you are not there:

```
cd "Course_02_The_Context_Architect/practice/direct-materials"
```

**Step 9.** Start Claude:

```
claude
```

**Step 10.** Try a real Wednesday-afternoon question:

```
Tell me what data files I have here, the columns of each, and how
many rows are in each one. Read the files now to confirm row counts.
```

**What you should see.** A clear two-file summary. For suppliers.csv: 50 rows. For orders.csv: about 2,500 rows. The row counts match what is in the CSVs right now (Claude actually opened them).

**Step 11.** Try another question that proves Claude is reading the data live:

```
Sum total_usd across orders.csv and tell me my top 5 suppliers by
spend over the last year. Group by supplier_id and join supplier_name
from suppliers.csv.
```

**What you should see.** Great Lakes Steel, Heartland Steel, Pacific Aluminum, Pittsburgh Steels, and one or two more should be in the top five (the bigger annual_value suppliers naturally have more orders). Claude pulled the answer from 2,500 rows in this moment, not from anything memorized in CLAUDE.md.

**Step 12.** Try the kind of question that surfaces a problem:

```
Look at orders.csv. Are there any suppliers in the orders file whose
supplier_id does not appear in suppliers.csv? If yes, name them.
```

**What you should see.** Probably zero rogue supplier_ids in the practice data, but the prompt is the kind of data-quality check Claude now does in seconds. If you ran this in your real procurement folder, this question would catch maverick spend immediately.

**Step 13.** Quit Claude (`/quit`).

## What just happened, in plain words

You confirmed your category files are working as a map, not as a copy of the data. Three things are happening when you ask a question:

1. Claude reads the global plus the category file at session start. That is the map.
2. When your prompt asks for data ("sum total_usd", "list suppliers"), Claude opens the CSV named in the map.
3. Claude computes the answer from the live CSV (which may have hundreds or thousands of rows).

The CSV can change tomorrow. The next session reads the new data. CLAUDE.md never has to change.

## Three things that trip beginners up

- **You typed every supplier name into CLAUDE.md "for safety".** Delete it. The CSV is the source of truth. Two sources will drift apart and confuse Claude.
- **Your column line is wrong.** The data team renamed `total_usd` to `total_amount_usd` last week and you did not notice. Open the actual CSV, read the header row, copy it into CLAUDE.md exactly. Update "last reviewed" to today.
- **Claude says the file does not exist.** Run `ls` in your terminal to see the exact file name. Common errors: extra space, wrong capital letter, plural vs singular (suppliers.csv not supplier.csv).

## You are done with Lesson 5 when

- All three category files have a "Files in this folder" section with column headers and a "refreshed / last reviewed" note for each CSV.
- No CLAUDE.md has the actual data typed out (no supplier list, no specific spend figures).
- Claude reads the live CSVs when you ask a data question and gives you a current answer drawn from the thousands of rows.
- You can update a CSV row without editing any CLAUDE.md.

Take a break. Lesson 6 is the finale.
