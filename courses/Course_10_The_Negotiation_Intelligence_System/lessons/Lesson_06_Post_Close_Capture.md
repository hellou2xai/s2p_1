# Lesson 6: Post-Close Capture

**Course:** The Negotiation Intelligence System
**Time:** 40 minutes

---

## Opening scenario

It is 16:45 on Thursday, 2026-05-07. The face-to-face negotiation with Redline Logistics LLC ended two hours ago. Redline accepted a 4% price increase, restored the original force majeure language, and agreed to keep the 180-day notice period. Final agreed value: $9.568M per year. Your VP is pleased.

You send the signed term sheet to Legal. You close your laptop. And right there, the institutional knowledge starts to dissolve. In six months, when a colleague prepares for the next supplier negotiation, they will have no record of why the force majeure clause mattered, what Redline's opening ask was, or that a 4% counter worked when Redline proposed 12%. That knowledge lives in your head, nowhere else.

This lesson builds the final piece of the system: a slash command called `/post-close` that captures everything. It records the outcome in a permanent log, generates a lessons-learned document, and archives all working files. One command. Nothing forgotten.

---

## What Claude Code is going to do for you

You will create a file at `.claude/commands/post-close.md` that defines a slash command. When you type `/post-close`, Claude Code reads the command, prompts you for the final negotiation outcome (agreed value, key concessions, date signed), and then does three things. First, it appends a row to `Outputs/negotiation-log.csv` with the outcome data. Second, it writes a lessons-learned document to `Outputs/post-close-capture.md`. Third, it copies all working files from `Outputs/` to an archive subfolder named after the supplier and the close date. The full negotiation record sits in one place, ready for the next person who works on this supplier.

---

## Set up

1. Confirm you completed Lesson 5. Check for the counter-proposal:

```
ls Outputs/counter-proposal.md
```

You should see the file listed.

2. Navigate to the practice folder if you are not already there:

```
cd "Course_10_The_Negotiation_Intelligence_System/practice"
```

3. Create the archive folder:

```
mkdir -p Outputs/archive
```

4. Start Claude Code:

```
claude
```

5. Restate the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/. Save all output to Outputs/.
```

**Folder layout at the start of this lesson:**

```
practice/
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   └── commands/
│       └── counter-proposal.md
├── data/
├── scripts/
│   ├── check-deviation-costs.py
│   └── check-brief-completeness.py
└── Outputs/
    ├── system-design.md
    ├── intelligence-brief.md
    ├── deviation-costs.md
    ├── pre-negotiation-brief.md
    ├── counter-proposal.md
    └── archive/
```

---

## Step-by-step

### Step 1: Create the negotiation log

Before building the command, set up the log file so there is a record to append to.

```
Create a file at Outputs/negotiation-log.csv with these column headers: Close_Date, Supplier, Contract_ID, Supplier_Opening_Ask_USD, Final_Agreed_Value_USD, Savings_vs_Opening_Ask_USD, Savings_Pct, Key_Concessions_Given, Key_Concessions_Received, Negotiator.
```

You should see Claude Code create `Outputs/negotiation-log.csv` with one header row and no data rows.

### Step 2: Create the post-close command file

```
Create a file at .claude/commands/post-close.md with the following content:

This command captures the outcome of a completed negotiation and archives the working files.

Steps:
1. Ask me for the following outcome details: final agreed annual value (USD), date signed (YYYY-MM-DD), key concessions TransGlobal gave, key concessions TransGlobal received.
2. Read Outputs/counter-proposal.md to identify the supplier name, contract ID, and TransGlobal's opening counter-position.
3. Read Outputs/deviation-costs.md to get the supplier's original opening ask (current value plus total deviation cost).
4. Calculate savings vs. the supplier's opening ask (opening ask minus final agreed value). Calculate savings percentage.
5. Append one row to Outputs/negotiation-log.csv with all the outcome fields. If the file does not exist, create it with headers first.
6. Write a lessons-learned document to Outputs/post-close-capture.md with these sections:
   a. Deal Summary: supplier name, contract ID, opening ask, final value, savings, date signed.
   b. What Worked: three bullets describing which counter-positions were accepted and what data supported them.
   c. What to Watch: two bullets describing risks or gaps in the data that should be addressed before the next renewal.
   d. Recommendations for Next Renewal: two recommendations for the team that will prepare the next negotiation.
7. Copy all files in Outputs/ (except the archive/ subfolder) to Outputs/archive/[supplier-name-lowercase-hyphens]_[close-date]/.
8. Print a summary line: "Post-close complete. [Supplier name]. Final value: $[amount]. Savings vs. opening ask: $[amount] ([pct]%). Archive: Outputs/archive/[folder-name]/."
```

You should see Claude Code create `.claude/commands/post-close.md`.

### Step 3: Run the command

Type the slash command:

```
/post-close
```

You should see Claude Code read the command and ask you for the outcome details. Provide them:

```
Final agreed annual value: $9,568,000. Date signed: 2026-05-07. Concessions TransGlobal gave: agreed to a performance review clause allowing Redline a 6-month improvement period before any penalty applies. Concessions TransGlobal received: price increase capped at 4%, force majeure clause restored in full, notice period restored to 180 days.
```

You should see Claude Code work through the eight steps. It will ask no further questions and should complete in one to two minutes.

If Claude says "Unknown command," check that the file is at `.claude/commands/post-close.md` and restart Claude Code.

### Step 4: Verify the negotiation log

```
Read Outputs/negotiation-log.csv. How many rows are there (excluding headers)? What is the final agreed value in the data row?
```

You should see one data row. The final agreed value should be $9,568,000. If the row is missing, ask Claude: "Append the negotiation outcome row to Outputs/negotiation-log.csv using the values I gave in the previous step."

### Step 5: Verify the lessons-learned document

```
Read Outputs/post-close-capture.md. Does it have all four sections: Deal Summary, What Worked, What to Watch, and Recommendations for Next Renewal? Does the Deal Summary name Redline Logistics LLC and state the $9,568,000 final value and 2026-05-07 close date?
```

You should see Claude Code confirm all four sections are present with the correct figures.

### Step 6: Verify the archive

```
List all files in Outputs/archive/, including all subfolders.
```

You should see a subfolder named `redline-logistics-llc_2026-05-07` (or similar) containing copies of the five working files: `system-design.md`, `intelligence-brief.md`, `deviation-costs.md`, `pre-negotiation-brief.md`, and `counter-proposal.md`.

If the subfolder name contains spaces, tell Claude: "Rename the archive subfolder so it uses hyphens instead of spaces."

### Step 7: Confirm Outputs/ still has the originals

```
List all files directly in Outputs/ (not the archive subfolder).
```

You should see the originals still in place. The archive is a copy, not a move.

### Step 8: Exit Claude Code

```
/quit
```

---

## Worked example, end to end

**Starting files:**

- `Outputs/counter-proposal.md`: TransGlobal's counter-proposal addressed to Redline Logistics LLC, proposing $9.568M.
- `Outputs/deviation-costs.md`: Supplier opening ask implied at $9.2M plus $1,378,000 in proposed changes equals $10.578M.

**The prompts you type, in order:**

```
Create Outputs/negotiation-log.csv with headers: Close_Date, Supplier, Contract_ID, Supplier_Opening_Ask_USD, Final_Agreed_Value_USD, Savings_vs_Opening_Ask_USD, Savings_Pct, Key_Concessions_Given, Key_Concessions_Received, Negotiator.
```

```
Create .claude/commands/post-close.md with the eight-step command definition.
```

```
/post-close
```

When prompted:

```
Final agreed annual value: $9,568,000. Date signed: 2026-05-07. Concessions TransGlobal gave: performance review clause with 6-month improvement period. Concessions TransGlobal received: 4% price cap, force majeure restored, notice period restored to 180 days.
```

**Summary line printed by the command:**

```
Post-close complete. Redline Logistics LLC. Final value: $9,568,000.
Savings vs. opening ask: $1,010,000 (9.5%). Archive: Outputs/archive/redline-logistics-llc_2026-05-07/.
```

**Extract from the lessons-learned document:**

```
## What Worked

- Citing the OTD decline from 96.8% to 93.1% gave the price counter-position a specific,
  data-backed justification. Redline did not contest the performance figures.
- Framing the force majeure restoration as a market-standard position (not a TransGlobal
  preference) reduced friction. Redline accepted it without counter-argument.
- Referencing alternatives for the corridor without naming specific carriers created
  credible pressure without revealing the rebid timeline or cost.
```

**Finished artifacts:**

- `Outputs/negotiation-log.csv`: one data row recording the outcome of the CTR-2024-LG-001 renewal.
- `Outputs/post-close-capture.md`: four-section lessons-learned document with the $9,568,000 final value and 2026-05-07 close date.
- `Outputs/archive/redline-logistics-llc_2026-05-07/`: copies of all five working files.

**What Claude Code did behind the scenes:**

1. Claude Code read the command definition from `.claude/commands/post-close.md`.
2. It prompted for the outcome details and waited for the response.
3. It read `Outputs/counter-proposal.md` to confirm the supplier name (Redline Logistics LLC) and contract ID (CTR-2024-LG-001).
4. It read `Outputs/deviation-costs.md` to calculate the supplier's effective opening ask: $9.2M current value plus $1,378,000 in proposed changes equals $10.578M.
5. It calculated savings: $10.578M minus $9.568M equals $1,010,000, which is 9.5% of the opening ask.
6. It appended the data row to `Outputs/negotiation-log.csv`, preserving the headers.
7. It wrote the lessons-learned document, drawing specific language from the performance and market analysis files to populate the "What Worked" section.
8. It created the archive subfolder, named it with lowercase hyphens, and copied the five working files into it without deleting the originals.
9. It printed the summary line.

---

## Common mistakes and how to recover

**Symptom:** The `/post-close` command is not recognized.
**Fix:** Check that the file is at `.claude/commands/post-close.md`. The command name matches the filename without `.md`. Restart Claude Code after creating any new command file.

**Symptom:** The negotiation log has duplicate rows after running the command twice.
**Fix:** Add a deduplication check to the command instructions: "Before appending, check whether a row with the same Contract_ID and Close_Date already exists. If it does, skip the append and print a message."

**Symptom:** The archive subfolder name contains spaces.
**Fix:** Tell Claude: "Rename the archive subfolder to use lowercase letters and hyphens only. Replace spaces with hyphens. For example, 'Redline Logistics LLC' becomes 'redline-logistics-llc'."

**Symptom:** The lessons-learned document is generic and does not reference specific figures from the negotiation.
**Fix:** Update the command instructions: "For every bullet in What Worked and What to Watch, include at least one specific figure, date, or clause name from the negotiation files. Generic advice is not acceptable."

**Symptom:** The archive copy deleted the originals from Outputs/.
**Fix:** Run `python scripts/build_course_data.py` to regenerate the practice data. Update the command instructions to say "Copy files to the archive folder. Do not delete or move the originals."

---

## You are done with Lesson 6 when

- `.claude/commands/post-close.md` exists with the eight-step command definition.
- `Outputs/negotiation-log.csv` has one data row with the $9,568,000 final value, 2026-05-07 close date, $1,010,000 savings, and 9.5% savings percentage.
- `Outputs/post-close-capture.md` has all four sections, names Redline Logistics LLC, and includes specific figures from the negotiation.
- `Outputs/archive/redline-logistics-llc_2026-05-07/` contains copies of all five working files.
- The originals in `Outputs/` are unchanged.

---

## Course complete

You have built a full negotiation intelligence system in Claude Code:

- A system design document that maps each negotiation stage to a Claude Code component.
- Three parallel sub-agents that gather performance, market, and terms intelligence in minutes rather than hours.
- A PostToolUse hook that automatically checks every deviation analysis for missing cost figures.
- A PreToolUse hook that blocks the pre-negotiation brief from being saved until BATNA and walk-away price are both present.
- A `/counter-proposal` slash command that generates the negotiation document from the approved brief.
- A `/post-close` slash command that records the outcome, writes the lessons-learned document, and archives all working files.

The next time a supplier sends a renewal proposal, you open a terminal, navigate to your negotiation folder, and type. The system does the analyst work. You do the negotiating.
