# Lesson 03: Strategic Development Plans

**Course:** Course 14, Supplier Lifecycle Management
**Role:** Supplier Relationship Manager, Crestview Industries
**Duration:** 55 minutes

---

## Part 1. The S2P Problem

It is 10:30 Wednesday. Your CPO stops by your desk to ask when the Heartland Polymers development plan review is due. You know it is coming up soon, but the plan lives in a Word file buried in a reference folder. You also have development-plans.csv tracking targets and review dates for 10 strategic suppliers. Pulling the dates, summarizing progress against targets, and building a review pack for the meeting takes about two hours. The CPO wants an update by end of day.

---

## Part 2. What Claude Code Is Going to Do for You

Claude Code will read development-plans.csv and the Word plan for Heartland Polymers, extract every target and its current status, identify the next review date, flag targets that are behind schedule, and produce a one-page status summary ready for the CPO meeting. You spend 10 minutes reviewing and editing. Claude does the rest.

---

## Part 3. Set Up

1. Claude Code installed and signed in. Project folder `Supplier_Lifecycle_2026/` already set up from Lesson 01.
2. The following files in `Master/`:
   - `development-plans.csv` (10 rows, one per strategic supplier, columns for supplier name, plan start date, review date, targets, and status)
   - `Heartland_Polymers_Dev_Plan.docx` (the current Word version of the Heartland Polymers development plan, including performance targets and agreed milestones)
   - `performance-history.csv` (from Lesson 01)
3. OneDrive sync paused.

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

**Step 3.** Check which strategic supplier reviews are coming up.

```
Read Master/development-plans.csv.
List every supplier where the Review_Date is within the next 60 days from today, 2026-04-25.
Show: Supplier_Name, Review_Date, and days until review.
Sort by Review_Date ascending.
```

You should see a short list of upcoming reviews with days-until counts. If the column is not named Review_Date, Claude will tell you. Restate with the correct column name.

**Step 4.** Pull the full detail for Heartland Polymers from the CSV.

```
Read Master/development-plans.csv.
Show me all columns for the row where Supplier_Name is Heartland Polymers.
```

You should see every field for that supplier printed in the terminal.

**Step 5.** Read the Word plan and extract targets and milestones.

```
Read Master/Heartland_Polymers_Dev_Plan.docx.
List every improvement target mentioned in the document.
For each target, show: the target description, the numeric goal, and the deadline date.
Also note any milestones listed as complete.
```

You should see a numbered list of targets and milestones. If the document has tables, Claude will read them. If Claude returns a partial list, ask: "Were there any tables in that document? If so, list the rows in each table separately."

**Step 6.** Cross-reference targets against recent performance.

```
Read Master/performance-history.csv.
Find all rows for Heartland Polymers.
For each improvement target from the development plan, tell me whether the most recent performance data
shows the supplier is On Track, Behind, or Met for that target.
Use the last two quarters of data (Q3 and Q4 2025).
```

You should see a status line for each target. If data is insufficient to assess a target, Claude will say so.

**Step 7.** Write the status summary for the CPO.

```
Using the target list and performance data for Heartland Polymers, write a one-page status summary.
The summary must include:
- Supplier name and review date
- Total targets: how many On Track, how many Behind, how many Met
- A three-row table: Target, Goal, Current Status
- One recommendation (three sentences maximum) for the review meeting
Save as Drafts/Heartland_Polymers_Review_Summary_v1.txt.
```

You should see the summary in the terminal and confirmation the file was saved. Read it before sharing with your CPO.

---

## Part 5. Worked Example, End to End

**Starting files:**

- `Master/development-plans.csv`: 10 rows. Heartland Polymers row shows Review_Date of 2026-05-08, three targets: delivery on-time rate from 87% to 94%, defect rate from 2.1% to below 1.0%, and supplier portal adoption from 40% to 100%.
- `Master/Heartland_Polymers_Dev_Plan.docx`: eight-page Word document with narrative, milestone table, and quarterly check-in notes.
- `Master/performance-history.csv`: Heartland Polymers rows show Q3 2025 delivery rate 91%, Q4 2025 delivery rate 93%. Defect rate Q4 2025 at 1.4%. Portal adoption Q4 2025 at 72%.

**Prompts used, in order:**

```
Read Master/development-plans.csv.
List every supplier where Review_Date is within the next 60 days from 2026-04-25.
Show Supplier_Name, Review_Date, and days until review. Sort ascending.
```

```
Read Master/Heartland_Polymers_Dev_Plan.docx.
List every improvement target with the numeric goal and deadline date.
Note any milestones listed as complete.
```

```
Read Master/performance-history.csv. Find all rows for Heartland Polymers.
For each target from the development plan, tell me whether recent data shows On Track, Behind, or Met.
Use Q3 and Q4 2025.
```

```
Write a one-page status summary for Heartland Polymers including:
- Review date (2026-05-08)
- Target counts by status
- A three-row table: Target, Goal, Current Status
- One recommendation for the review meeting
Save as Drafts/Heartland_Polymers_Review_Summary_v1.txt.
```

**Extract of output (summary):**

```
Heartland Polymers: Development Plan Review Summary
Review Date: 2026-05-08 (13 days)

Targets: 1 Met, 1 On Track, 1 Behind

Target                    Goal      Current Status
Delivery on-time rate     94%       93% (Q4 2025) - On Track
Defect rate               < 1.0%    1.4% (Q4 2025) - Behind
Supplier portal adoption  100%      72% (Q4 2025) - Behind

Recommendation: Confirm the delivery target as effectively met at 93% and agree on a final push
plan for defect reduction and portal adoption before the contract review in Q3 2026.
The defect rate needs a root-cause discussion: the trend is improving from 2.1% but is
not close enough to 1.0% to close without a formal action.
```

**Finished artifact:** `Drafts/Heartland_Polymers_Review_Summary_v1.txt`.

---

## Part 6. Common Mistakes and How to Recover

- **Symptom:** Claude cannot find the Review_Date column and lists no upcoming reviews. **Fix:** Ask Claude to list the exact column names in development-plans.csv. Then restate your prompt with the correct column name.

- **Symptom:** The Word plan reads as mostly blank or returns garbled text. **Fix:** The file may be in an older .doc format. Open it in Word, save as .docx, replace the file in Master/, and rerun.

- **Symptom:** Claude marks a target as Behind when you believe it is Met. **Fix:** Show Claude the exact rows it used: "Show me the raw rows from performance-history.csv for Heartland Polymers, Q3 and Q4 2025 only." If the data column name or the quarter label does not match what Claude expected, adjust the prompt.

- **Symptom:** The summary recommendation has more than three sentences. **Fix:** Ask Claude to revise: "Rewrite the recommendation section so it is three sentences or fewer. Keep the same factual content."

- **Symptom:** The output file is missing the target table and only shows narrative text. **Fix:** Claude may have produced the table in terminal output but not written it to the file. Ask: "Re-save Drafts/Heartland_Polymers_Review_Summary_v1.txt and include the three-row target table in the file. Do not omit it."
