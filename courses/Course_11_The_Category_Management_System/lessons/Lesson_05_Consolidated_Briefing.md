# Lesson 5: Consolidated Briefing: Assembling Sub-Agent Outputs into a VP-Ready Document

**Time:** 50 minutes.

## It is 08:50 on Monday. Five files in Drafts/ are validated. Your VP is expecting something in ten minutes.

You have the building blocks. `Drafts/savings_tracker.md` has the at-risk initiatives. `Drafts/contract_review.md` has the expiring contracts. `Drafts/scorecard_refresh.md` has the Logistics and Raw materials supplier scores. `Drafts/ps_update.md` has the professional services status. Each file is clean and validated.

What your VP wants is one document, not five. A briefing that covers all six categories, names the top three actions for this week, and fits on two pages. You are ten minutes away. Writing it by hand, pulling figures from five files, takes 20 minutes on a good day.

This lesson assembles the sub-agent outputs into a single VP-ready briefing using Claude Code.

## What Claude Code is going to do for you

Claude Code will read all five validated output files from `Drafts/`, cross-reference them with `data/program-state.json`, and write a consolidated briefing to `Outputs/briefings/briefing-2026-04-25.md`. The briefing covers all six categories, names suppliers, cites dollar figures, and caps the overall action list at three items. You review it, make two edits, and send it before 09:00.

This capability applies to Claude Code in the terminal. It does not apply to Claude AI Web or Claude Desktop with Cowork.

## Set up

1. Confirm all five Drafts/ files are present and validated:

```
ls "Course_11_The_Category_Management_System/practice/Drafts/"
```

You should see: `orchestrator_plan.md`, `savings_tracker.md`, `contract_review.md`, `scorecard_refresh.md`, `ps_update.md`. Any escalation files are also fine to have present.

2. Confirm the output folder exists:

```
ls "Course_11_The_Category_Management_System/practice/Outputs/"
```

You should see `Outputs/`. If there is no `briefings/` subfolder inside it, Claude Code will create it in Step 2.

3. Navigate to the practice folder and start Claude Code:

```
cd "Course_11_The_Category_Management_System/practice"
claude
```

4. Restate the read-only rule and name the output location:

```
The files in data/ are source data. Do not edit any file in data/ or Drafts/.
Save the consolidated briefing to Outputs/briefings/briefing-2026-04-25.md.
Create the Outputs/briefings/ folder if it does not exist.
```

Claude Code will confirm. The folder will be created on the first write if it does not exist.

**Folder layout:**

```
practice/
├── CLAUDE.md
├── data/                          (read-only)
├── Drafts/
│   ├── orchestrator_plan.md
│   ├── savings_tracker.md
│   ├── contract_review.md
│   ├── scorecard_refresh.md
│   └── ps_update.md
└── Outputs/
    └── briefings/                 (created in this lesson)
```

## Step-by-step

### Step 1: Confirm the briefing standards

Before assembling the briefing, remind Claude Code of the output requirements from `CLAUDE.md`.

```
Read CLAUDE.md. Confirm the following output standards for Monday briefings:
1. Save to Outputs/briefings/ with filename briefing-YYYY-MM-DD.md.
2. Name all six categories.
3. Every category section includes at least one supplier name, one dollar figure, and one date.
4. Recommendations capped at three per category and three overall.
5. All currency in USD with commas.
6. Dates in YYYY-MM-DD format.
7. No em-dashes or en-dashes.
Confirm all seven standards before we start.
```

You should see Claude Code list all seven standards and confirm it has read `CLAUDE.md`. If it lists fewer than seven, ask it to re-read and try again.

### Step 2: Read all five Drafts/ files

Ask Claude Code to read and summarize the validated outputs.

```
Read these five files:
Drafts/orchestrator_plan.md
Drafts/savings_tracker.md
Drafts/contract_review.md
Drafts/scorecard_refresh.md
Drafts/ps_update.md

For each file, give me a one-line summary: the number of data rows, the categories covered, and any items flagged as at-risk, behind schedule, or requiring action.
```

You should see five one-line summaries. The savings tracker summary should flag LOG-002 and RM-002. The contract review summary should list the number of contracts with "Review" or "Rebid" recommendations.

If Claude Code reports that a file is empty, re-run the relevant lesson to regenerate it.

### Step 3: Read the portfolio state for the two categories not in Drafts/

The Drafts/ files cover Logistics, Raw materials, Facilities, and Professional services. IT services and MRO are not yet in any draft file. Read the source data for those two.

```
Read data/program-state.json. Give me a status summary for:
- IT services: initiatives, risk flags, and any items due this week.
- MRO: initiatives, risk flags, and any items due this week.
Use data from data/initiative-pipeline.csv to add savings figures for IT and MRO initiatives.
```

You should see summaries for both categories. IT services: three initiatives on track, total target savings $910,000, no risk flags. MRO: one initiative not started (MRO-001, catalog rollout, $310,000 target, starts 2026-05-01).

### Step 4: Identify the top three overall actions

```
From everything you have read, identify the top three actions that require my attention this week.
Base the ranking on: (1) hard deadlines in the next 7 days, (2) dollar impact, (3) risk level.
Each action must name: the category, the supplier or initiative, the dollar amount, the deadline or risk flag, and a one-sentence recommended action.
No more than three items.
```

You should see three ranked actions. They will likely be:

1. Professional services: PS-001 consulting rate card negotiation, $340,000 realized of $380,000 target, delivery deadline 2026-04-30. Confirm delivery with Kevin Wright by 2026-04-28.
2. Logistics: LOG-002 carrier consolidation, $540,000 target at risk due to Southeast carrier capacity. Schedule a call with Redline Logistics LLC to assess capacity by 2026-04-27.
3. Facilities: Contract expiring 2026-05-31, renewal not started, contract value approximately $3.1M. Start renewal process this week with Ana Torres.

### Step 5: Draft the consolidated briefing

```
Write the Monday category briefing to Outputs/briefings/briefing-2026-04-25.md.

Structure:
1. Header: "Meridian Corp: Weekly Category Briefing" and the date 2026-04-25.
2. Top 3 actions this week (from Step 4).
3. One section per category in this order: IT services, Logistics, Raw materials, Facilities, Professional services, MRO.
4. Each category section must include:
   - Current annual spend.
   - Active initiative count and combined savings target.
   - Any risk flags or at-risk items.
   - At least one supplier name.
   - At least one dollar figure.
   - At least one date.
   - One recommended action (or "No action required this week" if clean).
5. Close with: "Prepared by: Category Management System. Review and edit before sending."

Follow all seven output standards from Step 1.
```

You should see Claude Code create `Outputs/briefings/briefing-2026-04-25.md`. The terminal will confirm the file path.

If Claude Code tries to save to `Drafts/` instead of `Outputs/briefings/`, remind it: "Save to Outputs/briefings/briefing-2026-04-25.md, not to Drafts/."

### Step 6: Review the briefing

```
Read Outputs/briefings/briefing-2026-04-25.md.
Count: how many category sections are present? Does each section have a supplier name, a dollar figure, and a date?
List any section that is missing one of the three.
```

You should see six sections confirmed. If any section is missing a required element, Claude Code will name it.

### Step 7: Fix any missing required elements

If Step 6 found missing elements, run this fix:

```
The [category name] section is missing [supplier name / dollar figure / date].
Read [the relevant Drafts/ file or data/program-state.json] to find the missing element.
Update the [category name] section in Outputs/briefings/briefing-2026-04-25.md.
Do not change any other section.
```

You should see the targeted section updated. Re-read the section after the fix to confirm.

### Step 8: Final quality check

```
Read Outputs/briefings/briefing-2026-04-25.md.
Check for:
1. Any em-dashes (the symbol between words, like "word -- word"). Report line numbers.
2. Any dates not in YYYY-MM-DD format. Report them.
3. Any currency figure without a dollar sign or without commas. Report them.
4. Any more than three items in any recommendation list. Report the section.
```

You should see "No issues found" or a short list of specific line numbers to fix. Fix each one before moving to Lesson 6.

### Step 9: Quit Claude Code

```
/quit
```

## Worked example: building the full briefing

**The prompt you type:**

```
Read Drafts/savings_tracker.md, Drafts/contract_review.md, Drafts/scorecard_refresh.md, Drafts/ps_update.md, and data/program-state.json.
Identify the top 3 actions this week, ranked by deadline and dollar impact.
Write the Monday briefing to Outputs/briefings/briefing-2026-04-25.md.
Cover all six categories. Each section needs a supplier name, a dollar figure, and a date.
Cap recommendations at 3 per category and 3 overall.
Do not edit any file in data/.
```

**Folder layout:**

```
practice/
├── data/
│   └── program-state.json              (input: IT services and MRO data)
├── Drafts/
│   ├── savings_tracker.md              (input: at-risk initiatives)
│   ├── contract_review.md              (input: expiring contracts)
│   ├── scorecard_refresh.md            (input: supplier scores)
│   └── ps_update.md                    (input: PS-001 status)
└── Outputs/
    └── briefings/
        └── briefing-2026-04-25.md      (output)
```

**What you should see:**

`Outputs/briefings/briefing-2026-04-25.md` opens with:

```
# Meridian Corp: Weekly Category Briefing
Date: 2026-04-25

## Top 3 Actions This Week

1. Professional services: Confirm PS-001 rate card delivery with Kevin Wright. Target: $380,000 savings. Delivery deadline: 2026-04-30. $340,000 already realized.
2. Logistics: Assess Redline Logistics LLC carrier capacity. LOG-002 at risk. Savings target: $540,000. Owner: Marcus Davis.
3. Facilities: Start renewal for contract expiring 2026-05-31. Estimated annual value: $3,143,626. Owner: Ana Torres.
```

Each of the six category sections follows, with spend figures, initiative summaries, at least one supplier name, and one recommended action.

**What Claude Code did behind the scenes:**

1. Claude Code read all four Drafts/ files and extracted the at-risk and action-required items from each.
2. It read `data/program-state.json` to fill in IT services and MRO, which had no dedicated Drafts/ file.
3. It merged all findings, then ranked by deadline (items with deadlines in the next 7 days first) and dollar impact (descending).
4. It selected the top three actions and wrote them as a numbered list.
5. It wrote one section per category in the specified order, pulling supplier names, dollar figures, and dates from the source files.
6. It capped each category's recommendation at one item and the overall list at three.
7. It saved the file to `Outputs/briefings/briefing-2026-04-25.md`.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| The briefing has fewer than six category sections. | Ask Claude Code: "Which categories are missing from the briefing?" Then: "Add a section for [category name] using data from data/program-state.json." |
| A category section has no supplier name. | Ask Claude Code: "Read data/supplier-scorecards.csv. Find one supplier in the [category name] category and add their name and most recent overall score to the [category name] section of the briefing." |
| The top three actions list has four or more items. | Tell Claude Code: "The top actions list must have exactly three items. Remove the lowest-priority item and rewrite the list." |
| The briefing file was saved to the wrong location. | Run: "Move the briefing file to Outputs/briefings/briefing-2026-04-25.md." If the briefings/ subfolder does not exist, Claude Code will create it. |
| Currency figures appear without commas (e.g., "$3143626" instead of "$3,143,626"). | Ask Claude Code: "Reformat all currency figures in the briefing to use commas as thousand separators. Do not change any other text." |

## You are done with Lesson 5 when

- `Outputs/briefings/briefing-2026-04-25.md` exists and is readable.
- The briefing has six category sections.
- Each section names at least one supplier, one dollar figure, and one date.
- The overall top three actions list has exactly three items.
- The final quality check returns no issues.

Move to Lesson 6 when ready.
