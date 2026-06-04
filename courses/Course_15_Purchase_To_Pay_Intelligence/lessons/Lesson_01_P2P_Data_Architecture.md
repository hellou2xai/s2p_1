# Lesson 01: P2P Data Architecture: Understanding the Four Transaction Files and How They Connect

**Estimated time:** 50 minutes
**Role:** P2P Analytics Lead, Meridian Corp
**Tool:** Claude Code (in the terminal)

---

## Part 1: The S2P Problem

It is 08:15 Monday. Your CFO has just Slacked you: "I need a full P2P compliance review on my desk by 2026-05-02. Start by telling me how the data hangs together." You have four transaction files sitting in your project folder: requisitions, purchase orders, goods receipts, and invoices. Each file was exported from a different system at Meridian Corp. None of them share a common key format, and none of the column names are obvious. Before you can run a single compliance check, you need to know how the files connect, which columns are the join keys, and how many transactions make it all the way from requisition to invoice. Doing this by hand in Excel, across 500 requisitions and 168 invoices, takes three to four hours. With Claude Code, it takes under ten minutes.

---

## Part 2: What Claude Code Is Going to Do for You

Claude Code will read all four transaction files, map the join keys between them, count the rows in each file, identify transactions that drop out at each stage of the chain, and produce a plain-English data architecture summary you can attach to your compliance review kick-off email. You will know, before writing a single compliance rule, exactly how your P2P data is connected and where the gaps are. That summary becomes the foundation for every check in Lessons 02 through 06.

---

## Part 3: Set Up

1. Claude Code is installed and you are signed in. If not, see the Course 15 README.md.
2. The project folder `Course_15_Purchase_To_Pay_Intelligence/` exists with subfolders: `Master/`, `Drafts/`, `Outputs/`, and `practice/`.
3. These files are in `practice/`:
   - `requisitions.csv` (500 rows)
   - `purchase-orders.csv` (384 rows)
   - `goods-receipts.csv` (273 rows)
   - `invoices.csv` (168 rows)
   - `contracted-rates.csv` (10 rows)
   - `approval-matrix.csv` (5 rows)
   - `preferred-suppliers.csv` (20 rows)
4. OneDrive sync is paused. Resume it after the lesson ends.
5. A terminal (the black window where you type commands) is open.

---

## Part 4: Step-by-Step

**Step 1.** Open your terminal and navigate to the course project folder.

```
cd "Course_15_Purchase_To_Pay_Intelligence"
claude
```

You should see the Claude Code prompt appear with the folder name shown at the top of the screen.

If you see "No such file or directory": run `ls` to list what is in your current folder, then navigate step by step using `cd`.

**Step 2.** Set the read-only rule for Master and tell Claude where to save output.

```
The folder Master/ holds the source reference files. Do not edit any file in Master/.
Read from practice/ freely. Save all output to Drafts/ unless I tell you otherwise.
```

You should see Claude Code confirm it understands. Nothing changes on disk at this step.

**Step 3.** Ask Claude Code to read all four transaction files and report basic profile information.

```
Read practice/requisitions.csv, practice/purchase-orders.csv,
practice/goods-receipts.csv, and practice/invoices.csv.
For each file, tell me: the number of rows, the column names,
and which columns look like join keys (IDs that appear in more than one file).
Do not change any file.
```

You should see a summary listing row counts and column names for each file, with the likely join keys called out. Claude Code reads CSV files directly without any extra tools or plugins.

If Claude reports "file not found" for `purchase-orders.csv`: the file name contains a hyphen, not an underscore. Run `ls practice/` in a second terminal to check the exact names on disk, then retry with the exact name.

**Step 4.** Ask Claude Code to trace the full transaction chain and name the linking columns.

```
Using the four files you just read, describe the full transaction chain
from requisition to invoice. Name the exact column in each file that links
to the next file. For example: "requisitions.csv column REQ_ID links to
purchase-orders.csv column REQ_ID." Cover all four links:
requisition to PO, PO to goods receipt, and goods receipt to invoice.
```

You should see a plain-English description of the chain with exact column names. This is the map you will reference in every later lesson.

If Claude gives you a generic answer without naming specific columns: ask it to "Show me five rows from each join key column so I can verify the format."

**Step 5.** Ask Claude Code to count how many transactions survive each stage of the chain.

```
Count how many REQ_IDs from practice/requisitions.csv appear in
practice/purchase-orders.csv. Count how many PO_IDs from
practice/purchase-orders.csv appear in practice/goods-receipts.csv.
Count how many PO_IDs from practice/goods-receipts.csv appear in
practice/invoices.csv. Show the results as a table with columns:
Stage, Records_In, Records_Matched, Records_Unmatched.
Save the table to Drafts/P2P_Chain_Coverage.txt.
```

You should see the table printed in the terminal and a confirmation that `Drafts/P2P_Chain_Coverage.txt` was saved.

If the matched count looks wrong: ask Claude to "Show me the first five values of REQ_ID from requisitions.csv and the first five values of REQ_ID from purchase-orders.csv side by side." Look for leading zeros, spaces, or prefix differences that prevent the join from working.

**Step 6.** Ask Claude Code to write a data architecture summary briefing note.

```
Write a data architecture summary for the Meridian Corp P2P compliance review.
Include: file names, row counts, key columns, the transaction chain with join keys,
and a plain-English description of how many transactions drop out at each stage.
Write it so a CFO who knows procurement but not data systems can follow it.
Save it as Drafts/P2P_Data_Architecture_Summary.txt.
```

You should see a confirmation that `Drafts/P2P_Data_Architecture_Summary.txt` was saved. Open the file to confirm it reads clearly.

**Step 7.** Exit Claude Code.

```
/quit
```

You should see the terminal return to its normal command prompt.

---

## Part 5: Worked Example, End to End

**Starting files:**

```
Course_15_Purchase_To_Pay_Intelligence/
├── Master/          (reference files, read-only)
├── Drafts/          (where output is saved)
├── Outputs/         (final signed-off files)
└── practice/
    ├── requisitions.csv        (500 rows)
    ├── purchase-orders.csv     (384 rows)
    ├── goods-receipts.csv      (273 rows)
    ├── invoices.csv            (168 rows)
    ├── contracted-rates.csv    (10 rows)
    ├── approval-matrix.csv     (5 rows)
    └── preferred-suppliers.csv (20 rows)
```

**Prompts used, in order:**

Prompt 1: setting the read-only rule.
```
The folder Master/ holds the source reference files. Do not edit any file in Master/.
Read from practice/ freely. Save all output to Drafts/ unless I tell you otherwise.
```

Prompt 2: reading and mapping all four files.
```
Read practice/requisitions.csv, practice/purchase-orders.csv,
practice/goods-receipts.csv, and practice/invoices.csv.
For each file, tell me: the number of rows, the column names,
and which columns look like join keys. Do not change any file.
```

Prompt 3: counting chain coverage.
```
Count how many REQ_IDs from practice/requisitions.csv appear in
practice/purchase-orders.csv. Count how many PO_IDs from
practice/purchase-orders.csv appear in practice/goods-receipts.csv.
Count how many PO_IDs from practice/goods-receipts.csv appear in
practice/invoices.csv. Show as a table: Stage, Records_In,
Records_Matched, Records_Unmatched. Save to Drafts/P2P_Chain_Coverage.txt.
```

**What you should see** when Prompt 3 succeeds: a table like the one below printed in the terminal, and a confirmation that `Drafts/P2P_Chain_Coverage.txt` was created.

```
Stage                       Records_In  Records_Matched  Records_Unmatched
Requisition to PO           500         384              116
PO to Goods Receipt         384         273              111
Goods Receipt to Invoice    273         168              105
```

**What Claude Code did, behind the scenes:**

1. Claude Code opened each CSV file and read the header row to get column names, then scanned the first ten data rows to infer data types and ID formats.
2. It identified join keys by looking for columns where values followed an ID pattern (prefixes like REQ-, PO-, GR-) and where those same values appeared in more than one file.
3. It loaded all REQ_ID values from `requisitions.csv` into an internal set, then checked each REQ_ID in `purchase-orders.csv` against that set to count matches and misses.
4. It repeated the join check for PO_ID across `purchase-orders.csv` and `goods-receipts.csv`, then again for `goods-receipts.csv` and `invoices.csv`.
5. It subtracted the matched count from the records-in count to get the unmatched figure for each stage.
6. It formatted the counts as a plain table and wrote the file to `Drafts/`.
7. For the architecture summary, Claude Code replaced column names and ID formats with plain-English descriptions a non-technical reader could follow, and called out the drop-off counts as a signal of where to investigate next.

**Finished artifacts:**
- `Drafts/P2P_Chain_Coverage.txt`: the four-stage coverage table.
- `Drafts/P2P_Data_Architecture_Summary.txt`: a one-page briefing note showing Meridian Corp's P2P data chain, coverage gaps, and key field names, ready to attach to the compliance review kick-off email.

---

## Part 6: Common Mistakes and How to Recover

- **Symptom:** Claude reports "file not found" for `purchase-orders.csv` or `goods-receipts.csv`. **Fix:** these file names use hyphens, not underscores. Run `ls practice/` in a second terminal window to confirm the exact names, then copy and paste them into your prompt.

- **Symptom:** The matched count comes back as zero even though you can see matching IDs by eye. **Fix:** the IDs probably have different formats in the two files. One system might export "REQ-0042" while another exports "42". Ask Claude: "Show me the first five values of REQ_ID in requisitions.csv and the first five values of REQ_ID in purchase-orders.csv." Look for leading zeros, spaces, or prefix differences, then ask Claude to strip and recompare.

- **Symptom:** Claude edited a file in `practice/` instead of writing to `Drafts/`. **Fix:** ask Claude to "undo that change and restore the original file." Then restate the rule: "Do not edit any file in practice/ or Master/. Save all output to Drafts/."

- **Symptom:** The architecture summary uses technical terms your CFO will not understand. **Fix:** ask Claude: "Rewrite Drafts/P2P_Data_Architecture_Summary.txt for a reader who knows procurement but not data systems. Replace every technical term with a plain description of what the data means for the business."

- **Symptom:** `Drafts/P2P_Chain_Coverage.txt` is empty after saving. **Fix:** sync was likely running when the file was written. Pause OneDrive sync, ask Claude to "write the chain coverage table to Drafts/P2P_Chain_Coverage.txt again," then resume sync after the file is confirmed.
