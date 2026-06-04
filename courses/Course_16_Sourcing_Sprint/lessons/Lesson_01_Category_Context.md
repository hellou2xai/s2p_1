# Lesson 01: Category Context Ingestion
## Building the Spend Profile and Supplier Landscape

**Course:** Course 16, Sourcing Sprint
**Estimated time:** 55 minutes
**Role:** Senior Category Manager, Ironbridge Manufacturing

---

## Part 1: The S2P Problem

It is 08:15 Monday, April 25. Tom Baker, your Supply Chain Director, has confirmed the kick-off
call for the direct materials sourcing sprint is at 10:00. You have a spend export from the ERP
(356 rows, six sub-categories), a supplier longlist CSV with 12 names, and a set of scope notes.
Before you can write an RFP or brief a single supplier, you need to know where the spend is
concentrated, which positions are single-source risks, and which sub-categories offer the most
cost reduction opportunity. Building that picture manually, pivoting the CSV, cross-referencing
supplier data, and drafting a briefing note, normally takes three to four hours.

---

## Part 2: What Claude Code Is Going to Do for You

Claude Code will read your spend CSV and supplier longlist, calculate totals by sub-category and
by supplier, flag concentration and single-source risks, compare the longlist against active
suppliers to surface new entrants, and write a category context summary you can share with Tom
and Lisa Torres (VP Procurement) before the 10:00 call. You review the numbers, confirm they
match your knowledge, and you are ready to brief the room. Total time: about 25 minutes.

---

## Part 3: Set Up

Complete these steps before you open Claude Code.

1. Confirm Claude Code is installed and you are signed in. If not, complete Course 01 first.
2. Create the project folder `Sourcing_Sprint_2026/` with four subfolders inside:
   `Master/`, `Drafts/`, `Outputs/`, and `Reference/`.
3. Save `spend-baseline.csv` (356 rows) to `Master/`.
4. Save `supplier-longlist.csv` (12 suppliers) to `Master/`.
5. Save `scope-notes.md` to `Master/`.
6. Pause OneDrive sync before you start. Right-click the OneDrive tray icon and choose
   "Pause syncing". Resume when you finish the lesson.
7. Open a terminal (the black window where you type commands).

---

## Part 4: Step-by-Step

**Step 1.** Navigate to the project folder.

```
cd "Sourcing_Sprint_2026"
```

You should see the terminal prompt update to show `Sourcing_Sprint_2026` in the path.

If you see "No such file or directory": confirm you created the folder with this exact name.
If the folder name has spaces, quote the full path:
`cd "C:/Users/YourName/Documents/Sourcing Sprint 2026"`.

**Step 2.** Start Claude Code.

```
claude
```

You should see the Claude Code welcome prompt, with the current folder shown at the top.

If Claude Code does not start: run `claude --version` to confirm it is installed.
If no version appears, return to Course 01 and complete the install steps.

**Step 3.** State the read-only rule for `Master/`.

```
The folder Master/ holds the source files for this sourcing sprint. Do not edit any file in Master/. Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

Claude Code should confirm it understands. No files change on disk at this point.

**Step 4.** Ask Claude Code to read the spend file and produce a sub-category summary.

```
Read Master/spend-baseline.csv. Calculate total spend by sub-category and by supplier. For each sub-category, show: the sub-category name, total USD spend, share of total spend, and the name and spend of the top supplier within that sub-category. Sort from highest to lowest sub-category spend. Do not edit Master/spend-baseline.csv.
```

You should see a table with six rows, one per sub-category, showing spend totals, percentage
shares, and top-supplier names.

If Claude Code reports "file not found": confirm `spend-baseline.csv` is in `Master/`, not
in the project root. The exact filename, including the hyphen, must match the file on disk.

**Step 5.** Ask Claude Code to flag concentration and single-source risks.

```
Using the same spend data, identify any sub-category where a single supplier holds 80% or more of spend. Also identify any sub-category where only one supplier appears in the data. Label each finding as "Concentration risk" or "Single source" as appropriate.
```

You should see a short list of risk flags, each showing the sub-category name, the supplier
name, the percentage, and the risk label.

**Step 6.** Ask Claude Code to identify new entrants from the supplier longlist.

```
Read Master/supplier-longlist.csv. Compare supplier names against the spend data you already read. List every supplier that appears in the longlist but not in the spend data. These are potential new entrants.
```

You should see a list of supplier names from the longlist that have no spend history
at Ironbridge.

If the list is empty and you know Northland Alloys is on the longlist: the names may not
match exactly between the two files. Ask: "Show me the exact supplier names in
`Master/supplier-longlist.csv` and the distinct supplier names in `Master/spend-baseline.csv`
side by side." Find spelling differences and ask Claude to normalize the match.

**Step 7.** Ask Claude Code to summarize the scope notes.

```
Read Master/scope-notes.md and summarize the key requirements: what is in scope, what is out of scope, and any constraints mentioned such as lead time, quality standards, or delivery terms.
```

You should see a short bullet list drawn from your scope notes.

**Step 8.** Ask Claude Code to write the category context summary.

```
Using the spend analysis, risk flags, new entrant list, and scope summary you have produced, write a one-page category context summary for Ironbridge Manufacturing's direct materials sourcing sprint. Include: a spend table by sub-category with USD totals and share of the $22.2M total, concentration and single-source risk findings, a list of potential new entrants from the supplier longlist, and three observations about where cost reduction potential is highest. Address it to Tom Baker (Supply Chain Director) and Lisa Torres (VP Procurement). Date it 2026-04-25. Save it as Drafts/Category_Context_v1.md.
```

You should see confirmation that `Drafts/Category_Context_v1.md` has been saved.

If the file appears in the project root instead of `Drafts/`: ask Claude Code:
"Move `Category_Context_v1.md` into `Drafts/` and confirm."

**Step 9.** Open `Drafts/Category_Context_v1.md` and verify three things: the six sub-category
spend totals sum to roughly $22.2M, the Steel sub-category is flagged as single source, and at
least two supplier names from the longlist appear in the new entrant list.

---

## Part 5: Worked Example, End to End

**Starting files:**

- `Master/spend-baseline.csv`: 356 rows of direct materials purchase orders, six sub-categories,
  covering 2025-04-01 to 2026-03-31.
- `Master/supplier-longlist.csv`: 12 suppliers including two new entrants, Northland Alloys and
  Bayshore Materials, not active in current spend.
- `Master/scope-notes.md`: Scope notes covering in-scope sub-categories, exclusions, lead-time
  requirements, and quality standards.

**Prompts used, in order:**

```
The folder Master/ holds the source files for this sourcing sprint. Do not edit any file in Master/. Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

```
Read Master/spend-baseline.csv. Calculate total spend by sub-category and by supplier. For each sub-category, show: the sub-category name, total USD spend, share of total spend, and the name and spend of the top supplier within that sub-category. Sort from highest to lowest sub-category spend.
```

```
Using the same spend data, identify any sub-category where a single supplier holds 80% or more of spend. Also identify any sub-category where only one supplier appears. Label each finding as "Concentration risk" or "Single source" as appropriate.
```

```
Read Master/supplier-longlist.csv. Compare supplier names against the spend data. List every supplier in the longlist that does not appear in the spend data. These are potential new entrants.
```

```
Read Master/scope-notes.md and summarize the key requirements: in scope, out of scope, and constraints.
```

```
Write a one-page category context summary. Include the spend table, risk flags, new entrant list, and three cost reduction observations. Address it to Tom Baker and Lisa Torres. Date 2026-04-25. Save as Drafts/Category_Context_v1.md.
```

**Extract from the output (Drafts/Category_Context_v1.md):**

```
Direct Materials Sourcing Sprint: Category Context Summary
To: Tom Baker (Supply Chain Director), Lisa Torres (VP Procurement)
Date: 2026-04-25

Sub-Category Spend Summary (FY2025-26, total $22.2M):

Sub-Category     | Total Spend  | Share  | Top Supplier          | Top Supplier Spend
Steel            | $4,200,000   | 18.9%  | Great Lakes Steel     | $4,200,000 (100%)
Polymers         | $3,800,000   | 17.1%  | Heartland Polymers    | $3,572,000 (94%)
Aluminum         | $3,400,000   | 15.3%  | Pacific Aluminum      | $2,958,000 (87%)
Electronics      | $2,900,000   | 13.1%  | Apex Electronics      | $2,610,000 (90%)
Fasteners        | $2,100,000   |  9.5%  | Cascade Fasteners     | $1,890,000 (90%)
Coatings         | $1,600,000   |  7.2%  | (fragmented)          | n/a

Risk Flags:
- Steel: Single source. Great Lakes Steel holds 100% of sub-category spend ($4.2M).
- Polymers: Concentration risk. Heartland Polymers holds 94% of sub-category spend.
- Electronics: Concentration risk. Apex Electronics holds 90%. Quality declining per ops team.

Potential New Entrants:
- Northland Alloys (Steel and Aluminum capability)
- Bayshore Materials (Polymers and Coatings capability)
```

**Finished artifact:** `Drafts/Category_Context_v1.md`. A one-page brief covering spend by
sub-category, risk flags, new entrant opportunities, and three cost reduction observations.
Ready to share with Tom Baker and Lisa Torres before the 10:00 kick-off call.

**What Claude Code did, behind the scenes:**

1. Opened `spend-baseline.csv` and parsed all 356 rows, reading the sub-category column,
   the supplier name column, and the spend amount column.
2. Grouped rows by sub-category, summed spend per group, and calculated each group's
   share of the $22.2M total.
3. Within each sub-category group, found the supplier with the highest individual spend
   and computed their share of that sub-category total. Flagged groups where one supplier
   held 80% or more, or where only one supplier appeared.
4. Opened `supplier-longlist.csv`, extracted all 12 supplier names, and compared them
   against the distinct supplier names found in the spend data. Names with no match
   became the new entrant list.
5. Opened `scope-notes.md` as plain text and identified lines or bullet points associated
   with in-scope items, out-of-scope items, and stated constraints.
6. Combined all five outputs into a business-memo format with addressee, date, labeled
   sections, and three synthesized cost reduction observations, then saved to `Drafts/`.

---

## Part 6: Common Mistakes and How to Recover

- **Symptom:** Claude Code reports "file not found" for `spend-baseline.csv`. **Fix:** confirm
  the file is in `Master/`, not the project root. The name must match exactly: `spend-baseline.csv`
  with a hyphen, not `spend_baseline.csv` with an underscore.

- **Symptom:** Sub-category totals do not sum to $22.2M. **Fix:** ask Claude Code: "Check whether
  any rows in `Master/spend-baseline.csv` have a blank or null value in the sub-category column
  and count them." Those rows may have been excluded. Ask Claude to add them to an "Uncategorized"
  line so the full total is represented.

- **Symptom:** The new entrant list is empty even though Northland Alloys is on the longlist.
  **Fix:** supplier names in the two files likely differ by spelling or punctuation. Ask: "Show me
  the exact supplier names in `Master/supplier-longlist.csv` and the distinct supplier names in
  `Master/spend-baseline.csv`." Then ask Claude to match on a lower-case, punctuation-stripped
  version of each name.

- **Symptom:** Claude Code saved `Category_Context_v1.md` in the project root, not in `Drafts/`.
  **Fix:** ask Claude Code: "Move `Category_Context_v1.md` to `Drafts/Category_Context_v1.md`
  and confirm." Re-state the save-location rule at the start of your next session.

- **Symptom:** The summary states a cost reduction observation without a dollar figure, for example
  "Steel offers room for improvement." **Fix:** ask Claude Code: "Rewrite the three cost reduction
  observations. Each one must name the sub-category, state the current annual spend in USD, and give
  a percentage range for potential reduction. For example: Steel, $4.2M spend, 8-12% reduction
  target equals $336,000-$504,000. Remove any observation that does not include a specific number."

- **Symptom:** OneDrive shows a sync conflict on the saved draft. **Fix:** another app had the file
  open during the session. Pause sync, move the conflict copy to `Archive/`, keep the main file,
  and resume sync.
