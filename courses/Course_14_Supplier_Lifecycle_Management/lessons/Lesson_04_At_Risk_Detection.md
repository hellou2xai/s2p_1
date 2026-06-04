# Lesson 04: At-Risk Detection and Corrective Action

**Course:** Course 14, Supplier Lifecycle Management
**Role:** Supplier Relationship Manager, Crestview Industries
**Duration:** 60 minutes

---

## Part 1. The S2P Problem

It is 14:00 Thursday. A production line supervisor emails you: parts from Apex Electronics are failing incoming inspection at a higher rate than last quarter. You check your notes and recall that Apex's quality score dropped 18 points over the last two quarters, from 84 to 66. That is a significant decline for a supplier delivering $1.2M of components annually. Identifying the drop, documenting it formally, and drafting a corrective action plan (CAP) by hand would take three to four hours. Frontier Machining already has an open CAP with 30 days remaining as of today, and you need to track that too.

---

## Part 2. What Claude Code Is Going to Do for You

Claude Code will scan performance-history.csv for all suppliers whose scores have dropped 10 or more points in the last two quarters, flag them as at risk, generate a formatted at-risk report with spend context, and draft a corrective action plan for Apex Electronics. For Frontier Machining, it will calculate the days remaining on the open CAP and tell you whether the deadline is today, overdue, or still open. You review the output and decide on next steps. Total time: about 20 minutes.

---

## Part 3. Set Up

1. Claude Code installed and signed in. Project folder `Supplier_Lifecycle_2026/` already set up from Lesson 01.
2. The following files in `Master/`:
   - `performance-history.csv` (120 rows, quarterly scores for all 30 suppliers)
   - `supplier-master.csv` (30 rows, includes annual spend per supplier)
   - `CAP_Template.docx` (the standard Crestview corrective action plan template)
3. `Drafts/Supplier_Segmentation_v2.csv` from Lesson 02 already present.
4. OneDrive sync paused.

---

## Part 4. Step-by-Step

**Step 1.** Open Claude Code in the project folder.

```
cd "Supplier_Lifecycle_2026"
claude
```

You should see the Claude Code prompt showing `Supplier_Lifecycle_2026` as the working folder.

**Step 2.** State the read-only rule.

```
The folder Master/ holds the source data files and templates. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

Claude should confirm. Nothing changes on disk.

**Step 3.** Scan for at-risk suppliers.

```
Read Master/performance-history.csv.
Find all suppliers where the performance score dropped 10 or more points between Q3 2025 and Q4 2025.
Show: Supplier_Name, Q3 score, Q4 score, and the point drop.
Sort by point drop descending.
```

You should see a ranked list of declining suppliers. If Claude returns no results, ask: "What are the unique values in the quarter column of Master/performance-history.csv?" The quarter labels may differ from what you expect. Restate the prompt using the exact labels Claude reports.

**Step 4.** Add annual spend context for each at-risk supplier.

```
Read Master/supplier-master.csv.
For each supplier in the at-risk list you just produced, look up their annual spend.
Re-sort the list by annual spend descending.
Save the result as Drafts/At_Risk_Report_v1.csv with columns:
Supplier_Name, Q3_Score, Q4_Score, Point_Drop, Annual_Spend_USD.
```

You should see the updated list and a confirmation that `Drafts/At_Risk_Report_v1.csv` was saved.

**Step 5.** Draft a corrective action plan for Apex Electronics.

```
Read Master/CAP_Template.docx.
Using that template, draft a corrective action plan for Apex Electronics with these facts:
- Quality score: Q3 2025 was 84, Q4 2025 was 66. Drop of 18 points.
- Annual spend at Crestview: $1,200,000
- Root cause: to be determined by supplier. Use [Root Cause TBC] as a placeholder.
- Required actions:
  1. Submit root cause analysis by 2026-05-09
  2. Submit corrective action response by 2026-05-23
  3. Achieve quality score of 78 or above by Q2 2026
- Plan issued by: Supplier Relationship Manager, Crestview Industries
- Issue date: 2026-04-25
Save as Drafts/Apex_Electronics_CAP_v1.docx.
```

You should see a confirmation that `Drafts/Apex_Electronics_CAP_v1.docx` was saved. Open the file and check every placeholder field before sending to Apex.

**Step 6.** Check the status of Frontier Machining's open CAP.

```
The CAP for Frontier Machining was issued on 2026-03-26 with a 30-day deadline.
Today is 2026-04-25.
Calculate: how many days remain as of today?
Is the supplier past the deadline, on time, or within 5 days of the deadline?
Print a one-line status: "Frontier Machining CAP: [X] days remaining as of 2026-04-25. Status: [On Time / Due Today / Overdue]."
```

You should see the one-line status. The CAP was issued 30 days ago, so today is the due date. Claude should report 0 days remaining and flag it as Due Today.

**Step 7.** Update the segmentation file with current at-risk and CAP notes.

```
Read Drafts/Supplier_Segmentation_v2.csv.
Update the Reason field for Apex Electronics to:
"Q4 2025 score: 66. Dropped 18 pts from Q3. CAP issued 2026-04-25. Root cause due 2026-05-09."
Update the Reason field for Frontier Machining to:
"CAP issued 2026-03-26. Due date reached 2026-04-25. Awaiting closure confirmation."
Save as Drafts/Supplier_Segmentation_v3.csv. Do not change any other rows.
```

You should see confirmation that v3 was saved. Open it and verify that only the two named rows changed.

---

## Part 5. Worked Example, End to End

**Starting files:**

- `Master/performance-history.csv`: Apex Electronics shows Q3 2025 score 84, Q4 2025 score 66. Frontier Machining shows Q3 2025 score 71, Q4 2025 score 69 (small drop, but CAP is already open from a prior period).
- `Master/supplier-master.csv`: Apex Electronics annual spend $1,200,000. Frontier Machining annual spend $480,000.
- `Master/CAP_Template.docx`: Crestview standard CAP with sections for supplier details, incident summary, required actions, deadlines, and sign-off.

**Prompts used, in order:**

```
Read Master/performance-history.csv.
Find all suppliers where the performance score dropped 10 or more points between Q3 2025 and Q4 2025.
Show Supplier_Name, Q3 score, Q4 score, point drop. Sort descending.
```

```
Read Master/supplier-master.csv.
For each at-risk supplier, add their annual spend. Re-sort by spend descending.
Save as Drafts/At_Risk_Report_v1.csv.
```

```
Read Master/CAP_Template.docx.
Draft a CAP for Apex Electronics: Q3 score 84, Q4 score 66, spend $1,200,000.
Required actions: root cause by 2026-05-09, response by 2026-05-23, score 78 or above by Q2 2026.
Issue date 2026-04-25. Save as Drafts/Apex_Electronics_CAP_v1.docx.
```

**Extract of output (Drafts/At_Risk_Report_v1.csv):**

```
Supplier_Name,Q3_Score,Q4_Score,Point_Drop,Annual_Spend_USD
Apex Electronics,84,66,18,1200000
Midland Packaging,77,64,13,320000
```

**Finished artifacts:**
- `Drafts/At_Risk_Report_v1.csv`: ranked list of at-risk suppliers with spend context.
- `Drafts/Apex_Electronics_CAP_v1.docx`: corrective action plan ready for review and issue.
- `Drafts/Supplier_Segmentation_v3.csv`: updated reason fields for Apex and Frontier.

---

## Part 6. Common Mistakes and How to Recover

- **Symptom:** Claude finds no at-risk suppliers even though you know Apex dropped. **Fix:** Ask Claude: "What are the unique values in the quarter column of Master/performance-history.csv?" The labels may be "2025-Q3" or "Q3-25" instead of "Q3 2025". Restate the prompt with the exact format Claude reports.

- **Symptom:** The annual spend column in the at-risk report is blank for some suppliers. **Fix:** The supplier name in performance-history.csv may not match the name in supplier-master.csv exactly. Ask Claude: "List the Supplier_Name values from Drafts/At_Risk_Report_v1.csv that do not appear in Master/supplier-master.csv." Fix the spelling in the draft file, not in Master/, and rerun.

- **Symptom:** The CAP Word file was saved but opens blank. **Fix:** Claude may not have been able to populate a protected template. Ask: "Read Master/CAP_Template.docx and list every section heading." If the template uses Word form controls, those cannot be filled by Claude Code. Export the template as a plain .docx first (File, Save As, .docx, uncheck "Add password" and form protection), replace the file in Master/, and rerun.

- **Symptom:** Claude calculates the wrong number of days remaining for Frontier Machining. **Fix:** Confirm today's date in the prompt: "Today is 2026-04-25. The CAP was issued on 2026-03-26 with a 30-day deadline. How many days remain?" If still wrong, ask Claude to show its arithmetic step by step.

- **Symptom:** Saving Supplier_Segmentation_v3.csv overwrote v2. **Fix:** Ask Claude: "List all files in Drafts/ starting with Supplier_Segmentation." If v2 was overwritten, restore from your original and rerun the update step, specifying the output file name explicitly as Drafts/Supplier_Segmentation_v3.csv.

- **Symptom:** The CAP shows the wrong issue date. **Fix:** The prompt may not have included today's date, and Claude defaulted to a different value. Ask: "In Drafts/Apex_Electronics_CAP_v1.docx, find any date shown as the issue date and replace it with 2026-04-25. Save the file."
