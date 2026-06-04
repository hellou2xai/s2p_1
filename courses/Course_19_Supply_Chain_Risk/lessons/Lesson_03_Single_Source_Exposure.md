# Lesson 03: Single-Source Exposure Mapping

## Opening scenario

It is 14:00 Wednesday. The concentration risk summary is saved. Your procurement director stops by your desk: "Before the board meeting, I need to know exactly which items we can only get from one supplier and what our backup plan is for each one. If Apex Electronics goes under tomorrow, what stops?" You have five single-source items spread across three suppliers. Some have qualified alternates. Some have alternates still in qualification. One has no alternate at all. The board needs a map that shows the full picture in one table, not three separate spreadsheets.

## The S2P problem

Single-source items carry the highest supply chain risk in any manufacturing operation. When you rely on one supplier for a critical component, any disruption to that supplier stops your production line. Most procurement teams know they have single-source items. Fewer can say exactly how many there are, which items, how much annual spend is at risk, and whether a qualified backup exists. Building this map manually requires cross-referencing the item file, the supplier master, and the alternates register. Three files, hundreds of rows, and hours of manual lookups with no guarantee of accuracy.

## What Claude Code is going to do for you

Claude Code reads `data/single-source-items.csv`, `data/supplier-master.csv`, and `data/approved-alternates.csv` in one pass. It joins the files on item_id, adds alternate status for each item, and sorts by spend descending so the highest-exposure items appear first. Items with no approved alternate get flagged as critical gaps. The result is a structured table with every number the board needs, saved to `Drafts/single-source-exposure-map.md`. This lesson takes about 45 minutes.

## Set up

1. Lessons 1 and 2 completed. CLAUDE.md has the scoring matrix, data source mapping, and concentration risk thresholds.
2. Claude Code open in `Course_19_Supply_Chain_Risk/practice/`. If you closed it, reopen:

```
cd "Course_19_Supply_Chain_Risk/practice"
claude
```

3. Confirm the following files are present:
   - `data/single-source-items.csv` (5 items)
   - `data/approved-alternates.csv` (4 alternates)
   - `data/supplier-master.csv` (25 suppliers)
4. Confirm `Drafts/concentration-risk-summary.md` was saved in Lesson 2.

Open the session with the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

## Step-by-step

### Step 1. Read the single-source items file.

Confirm the five items and their key columns before joining.

```
Read data/single-source-items.csv and show me all rows.
```

You should see 5 rows with columns: item_id, item_description, supplier_id, supplier_name, annual_spend_usd, criticality, alternate_available, and qualification_time_weeks. The five items include ITEM-0001 (Steel plate 4mm, $840,000), ITEM-0013 (Aluminum sheet 2mm, $620,000), ITEM-0025 (Microcontroller ARM, $480,000), ITEM-0037 (Cloud hosting, $500,000), and ITEM-0049 (Fire inspection, $140,000). If you see fewer rows, ask Claude to confirm the row count in the file.

### Step 2. Read the approved alternates file.

Check which items have approved backup suppliers.

```
Read data/approved-alternates.csv and show me all rows.
```

You should see 4 rows. The file covers ITEM-0001 twice (two alternates: Summit Metals qualified, Liberty Composites in qualification), ITEM-0013 (Summit Metals qualified), and ITEM-0037 (Pinnacle Software qualified). ITEM-0025 and ITEM-0049 have no rows in this file. That means the Microcontroller ARM and Fire inspection items have no approved alternate recorded. If you see only 3 rows, ask Claude to recount. There are 4 rows in the source file.

### Step 3. Build the exposure map.

Join the two files and add alternate status to each single-source item.

```
Join data/single-source-items.csv with data/approved-alternates.csv on item_id.
Use a left join so all 5 single-source items appear even if they have no alternate.
For each item show: item_id, item_description, supplier_name, annual_spend_usd,
criticality, alternate_supplier_name (or "NONE" if none exists),
alternate_status (qualified, in_qualification, or "NO ALTERNATE").
Sort by annual_spend_usd descending.
```

You should see a 5-row table. ITEM-0001 appears once with its primary alternate (Summit Metals, qualified). ITEM-0013 shows Summit Metals qualified. ITEM-0037 shows Pinnacle Software qualified. ITEM-0025 shows "NONE" and "NO ALTERNATE." ITEM-0049 shows "NONE" and "NO ALTERNATE." If the join produces more than 5 rows, Claude Code performed an inner join or a many-to-many join. Ask it to deduplicate by keeping the highest-priority alternate (qualified over in_qualification) per item.

### Step 4. Quantify the exposure by alternate status.

Break the $2,580,000 total single-source spend into three buckets.

```
From the exposure map, calculate:
1. Total single-source spend across all 5 items.
2. Spend covered by a qualified alternate.
3. Spend covered by an alternate in qualification only.
4. Spend with no alternate at all.
Show each bucket as a dollar amount and as a percentage of total single-source spend.
```

You should see: total single-source spend $2,580,000. Qualified alternate: ITEM-0001 ($840,000) plus ITEM-0013 ($620,000) plus ITEM-0037 ($500,000) = $1,960,000 (75.97%). In qualification only: $0 (Liberty Composites covers ITEM-0001 as a secondary alternate, but Summit Metals is already qualified). No alternate: ITEM-0025 ($480,000) plus ITEM-0049 ($140,000) = $620,000 (24.03%). If your totals differ, ask Claude to show the item-by-item calculation before summing.

### Step 5. Flag the highest-risk item.

Identify the item the board needs to see first.

```
Which single-source item carries the highest combined risk based on: annual spend,
criticality rating, and no qualified alternate? Name the item, its current supplier,
the annual spend, the criticality rating, and why it ranks as the top risk.
```

You should see ITEM-0025 (Microcontroller ARM, Apex Electronics, $480,000, criticality: critical) identified as the top risk. It is the only item rated "critical" with no alternate in place or in qualification. If Claude names ITEM-0049 instead, point out that ITEM-0025 has a higher criticality rating even though ITEM-0049 also lacks an alternate.

### Step 6. Save the exposure map.

Write the complete output to Drafts/ with a summary and a critical gaps section.

```
Save the complete single-source exposure map to Drafts/single-source-exposure-map.md.
Include: the 5-row item table, the spend-by-status summary (qualified, in qualification,
no alternate), and a "Critical gaps" section that lists items with no alternate,
names the supplier, and states the annual spend and criticality for each.
```

You should see the file saved. Open it and confirm it has three sections: the item table, the spend summary, and the critical gaps list. If the file saves as empty, check that Drafts/ exists and that you have write permission in that folder.

## Worked example

**Starting files:**
- `data/single-source-items.csv` (5 items with spend, criticality, and supplier columns).
- `data/approved-alternates.csv` (4 rows covering 3 of the 5 items).
- `data/supplier-master.csv` (25 suppliers with financial health scores).

**What you type:**

```
Build the single-source exposure map by joining data/single-source-items.csv with
data/approved-alternates.csv on item_id. Use a left join. Show each item with its
current supplier, annual spend, criticality, and alternate status. Flag items with
no alternate as "CRITICAL GAP." Then save to Drafts/single-source-exposure-map.md.
```

**What you should see:**

A 5-row table with current supplier, spend, and alternate status for each item. ITEM-0025 (Microcontroller ARM) and ITEM-0049 (Fire inspection) show "CRITICAL GAP" in the alternate column. The file saves successfully to `Drafts/single-source-exposure-map.md`.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the risk scoring rules for single-source exposure and the output standards.
2. Read `data/single-source-items.csv` to get all 5 items with supplier_id, annual_spend_usd, and criticality.
3. Read `data/approved-alternates.csv` to get the 4 alternate rows with qualification_status.
4. Performed a left join on item_id, keeping all 5 single-source items regardless of whether a matching alternate row existed.
5. For items with no match in approved-alternates.csv (ITEM-0025 and ITEM-0049), set alternate_supplier_name to "NONE" and alternate_status to "CRITICAL GAP."
6. For ITEM-0001, which has two alternate rows, kept the qualified alternate (Summit Metals) as the primary and noted Liberty Composites as a secondary.
7. Sorted by annual_spend_usd descending so the highest-exposure items appear first in the table.
8. Wrote the three-section output file to Drafts/.

## Common mistakes and how to recover

- **Symptom:** The joined table has more than 5 rows. **Fix:** ITEM-0001 has two alternates in approved-alternates.csv. A standard left join produces 6 rows. Ask Claude to deduplicate by keeping the "qualified" alternate over the "in_qualification" one. The goal is one row per item showing the best available alternate.

- **Symptom:** An item shows "NO ALTERNATE" but you know an alternate exists. **Fix:** Check whether the item_id values match exactly across both files. "ITEM-0001" and "ITEM-001" do not match. Ask Claude: "Show me the item_id values from both files side by side." Find and fix the mismatch in your prompt by specifying the exact ID.

- **Symptom:** The spend figures in the exposure map differ from those in supplier-master.csv. **Fix:** This is expected. Single-source-items.csv holds item-level spend ($840,000 for Steel plate 4mm). Supplier-master.csv holds total supplier spend ($4,200,000 for Great Lakes Steel across all items). Both numbers are correct for their purpose. Use item-level spend in the exposure map.

- **Symptom:** All items show "in_qualification" and none show "qualified." **Fix:** Read approved-alternates.csv directly and check the qualification_status column. If Summit Metals shows "qualified," the join is working correctly and the status is coming through. If it still shows "in_qualification," Claude may have read an old cached version. Ask it to re-read the file.

- **Symptom:** The critical gaps section in the saved file is empty. **Fix:** The critical gaps section should list ITEM-0025 and ITEM-0049. Ask Claude: "Which items in the exposure map have alternate_status equal to NO ALTERNATE or CRITICAL GAP?" If it names both items, ask it to rewrite the critical gaps section and save again.
