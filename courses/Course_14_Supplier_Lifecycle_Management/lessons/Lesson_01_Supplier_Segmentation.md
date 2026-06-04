# Lesson 01: Supplier Segmentation and Lifecycle Stages

**Course:** Course 14, Supplier Lifecycle Management
**Role:** Supplier Relationship Manager, Crestview Industries
**Duration:** 55 minutes

---

## Part 1. The S2P Problem

It is 08:15 Monday. Your director has asked for a lifecycle status report on all 30 Crestview Industries suppliers by Friday. The data lives in three separate CSV files: supplier-master.csv, performance-history.csv, and compliance-status.csv. Cross-referencing them by hand and sorting 30 rows into seven stages (Onboarding, Active, Strategic, At Risk, Corrective Action, Exit, Under Review) would take the better part of a day. Some suppliers have missing fields. Others have stage labels that no one has updated in six months. The directory will not wait.

---

## Part 2. What Claude Code Is Going to Do for You

Claude Code will read all three data files, cross-reference them, classify each supplier into a lifecycle stage, flag data gaps, and produce a clean segmentation summary saved to your Drafts folder. You review the output, confirm the classifications, and hand the summary to your director. Total time: about 20 minutes, including your review.

---

## Part 3. Set Up

1. Claude Code installed and signed in on your machine. See Lesson 00 if not yet done.
2. The project folder `Supplier_Lifecycle_2026/` created, with `Master/`, `Drafts/`, and `Outputs/` subfolders inside it.
3. The following files saved in `Master/`:
   - `supplier-master.csv` (30 rows, one per supplier)
   - `performance-history.csv` (120 rows, performance scores by quarter)
   - `compliance-status.csv` (30 rows, compliance fields per supplier)
4. OneDrive sync paused before you start. Resume when the session ends.
5. A terminal window open at the project root.

---

## Part 4. Step-by-Step

**Step 1.** Open Claude Code in the project folder.

```
cd "Supplier_Lifecycle_2026"
claude
```

You should see the Claude Code prompt with `Supplier_Lifecycle_2026` shown as the working directory.

**Step 2.** State the read-only rule for Master/ and set the working rules for this session.

```
The folder Master/ holds the source data files. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

Claude should confirm it understands. Nothing changes on disk at this step.

**Step 3.** Ask Claude to read the three source files and report what it finds.

```
Read Master/supplier-master.csv, Master/performance-history.csv, and Master/compliance-status.csv.
List the column headers for each file. Tell me how many rows each file has.
Do not change any file.
```

You should see three numbered lists of column headers, one per file, with row counts. If Claude reports a file not found, check that the file name in your prompt matches the file name in Master/ exactly, including hyphens and lowercase letters.

**Step 4.** Ask Claude to classify each supplier into a lifecycle stage.

```
Using the three files in Master/, classify each of the 30 suppliers into one of these seven lifecycle stages:
- Onboarding: supplier activated within the last 90 days or missing compliance items
- Active: performing supplier, all compliance current, no open issues
- Strategic: top-tier supplier with a development plan on file
- At Risk: performance score dropped 10 or more points in the last two quarters
- Corrective Action: supplier with an open corrective action plan
- Exit: supplier flagged for off-boarding
- Under Review: supplier with a pending audit or unresolved dispute

List each supplier name, their current stage, and a one-line reason for the classification.
Save the result as Drafts/Supplier_Segmentation_v1.csv with columns: Supplier_Name, Stage, Reason.
```

You should see Claude working through the files and then confirming that `Drafts/Supplier_Segmentation_v1.csv` has been created. If Claude says it cannot determine stage for some suppliers, that is expected: it will flag them as data gaps.

**Step 5.** Ask Claude to summarize the distribution.

```
Read Drafts/Supplier_Segmentation_v1.csv and give me a count of suppliers in each stage.
Also list any suppliers where the stage could not be determined, with the missing data field.
```

You should see a table showing counts per stage and a short list of data gaps. Take note of any supplier where stage is unclear: you will need to fill those fields manually before the Friday report.

**Step 6.** Save a formatted summary to Drafts.

```
Using Drafts/Supplier_Segmentation_v1.csv, write a plain-text lifecycle summary table
with columns: Stage, Count, Supplier Names (comma-separated).
Save it as Drafts/Lifecycle_Summary_v1.txt.
```

You should see confirmation that `Drafts/Lifecycle_Summary_v1.txt` has been saved.

---

## Part 5. Worked Example, End to End

**Starting files:**

- `Master/supplier-master.csv`: 30 suppliers, including Summit Electrical (onboarding, missing two compliance fields), Great Lakes Steel (active, stable performance), Heartland Polymers (strategic, development plan on file), Apex Electronics (performance score dropped from 84 to 66 over two quarters), Frontier Machining (open corrective action, 30 days remaining), Regional Supply Co (flagged for exit, orders still active), and Coastal Coatings (pending audit).
- `Master/performance-history.csv`: 120 rows, quarterly scores for each supplier over the last year.
- `Master/compliance-status.csv`: 30 rows, fields for insurance certificate, W-9, NDA, and onboarding checklist completion.

**Prompts used, in order:**

```
The folder Master/ holds the source data files. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

```
Read Master/supplier-master.csv, Master/performance-history.csv, and Master/compliance-status.csv.
List the column headers for each file. Tell me how many rows each file has.
```

```
Using the three files in Master/, classify each of the 30 suppliers into one of these seven
lifecycle stages: Onboarding, Active, Strategic, At Risk, Corrective Action, Exit, Under Review.
Use these rules:
- Onboarding: activated within 90 days or missing compliance items
- Active: all compliance current, stable performance, no open issues
- Strategic: top-tier, development plan on file
- At Risk: performance score dropped 10 or more points in last two quarters
- Corrective Action: open corrective action plan
- Exit: flagged for off-boarding
- Under Review: pending audit or unresolved dispute
Save as Drafts/Supplier_Segmentation_v1.csv with columns: Supplier_Name, Stage, Reason.
```

**Extract of output (Drafts/Supplier_Segmentation_v1.csv):**

```
Supplier_Name,Stage,Reason
Summit Electrical,Onboarding,Insurance certificate and W-9 not yet received
Great Lakes Steel,Active,All compliance current, score 79 stable over 4 quarters
Heartland Polymers,Strategic,Development plan on file, score 91 consistent
Apex Electronics,At Risk,Score dropped from 84 to 66 over Q3 and Q4 2025
Frontier Machining,Corrective Action,Open CAP issued 2026-03-26, 30 days remaining
Regional Supply Co,Exit,Off-boarding flag set 2026-02-14, active orders still open
Coastal Coatings,Under Review,Audit pending since 2026-03-01, unresolved
```

**Finished artifact:** `Drafts/Supplier_Segmentation_v1.csv` with 30 rows and `Drafts/Lifecycle_Summary_v1.txt` with stage counts and data gap notes.

---

## Part 6. Common Mistakes and How to Recover

- **Symptom:** Claude reports "file not found" for supplier-master.csv. **Fix:** Check the exact file name in Master/, including hyphens. The file must be named `supplier-master.csv`, not `Supplier_Master.csv`. Names are case-sensitive in the terminal on Mac and Linux. On Windows, a typo still breaks the path.

- **Symptom:** Claude classifies most suppliers as Active even though you know several are at risk. **Fix:** Check that performance-history.csv has a date column Claude can sort by. If the column is named `Quarter` not `Date`, add that to your prompt: "The date column is called Quarter, in format Q1-2025."

- **Symptom:** The output CSV has 29 rows, not 30. **Fix:** Ask Claude: "How many unique supplier names appear in Master/supplier-master.csv?" One row may have a blank supplier name or a duplicate that got collapsed. Fix the source file in Master/ (after removing the read-only rule), then rerun.

- **Symptom:** Claude put a supplier in the wrong stage. **Fix:** Ask Claude to show its reasoning for that specific supplier: "Why did you classify Apex Electronics as Active? Show me the raw rows from performance-history.csv that you used." Correct the logic in your prompt and rerun.

- **Symptom:** Drafts/Supplier_Segmentation_v1.csv was saved but will not open in Excel. **Fix:** The file may have been saved with inconsistent line endings or extra quotes. Ask Claude: "Re-save Drafts/Supplier_Segmentation_v1.csv as a clean UTF-8 CSV compatible with Excel. Use commas as the delimiter and wrap fields with commas in double quotes."

- **Symptom:** OneDrive shows a sync conflict on the CSV file. **Fix:** You likely had sync running during the write. Pause sync, delete the conflict copy, keep the one named without a device suffix, then resume sync.
