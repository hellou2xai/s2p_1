# Lesson 06: Relationship State Persistence

**Course:** Course 14, Supplier Lifecycle Management
**Role:** Supplier Relationship Manager, Crestview Industries
**Duration:** 50 minutes

---

## Part 1. The S2P Problem

It is 08:30 Monday. Last Friday afternoon you ran a full lifecycle review at Crestview Industries, updated seven supplier stage records, approved two corrective actions, and deferred one decision about Coastal Coatings pending a call with your director on Monday morning. You open Claude Code, start a new session, and type: "Which supplier decision did I defer on Friday?" Claude has no idea. The conversation is gone. The CSV files are still on disk, but they do not record that you deferred a decision, when, or why. Without a persistent state file, every session starts from zero, and decisions made in one session leave no trace for the next.

---

## Part 2. What Claude Code Is Going to Do for You

Claude Code will build and maintain a `Lifecycle_State.json` file that stores the current stage, last action date, decision status, and notes for every supplier. Each new session reads this file first. When you make a decision, Claude writes it back immediately. Deferred decisions survive the session close. When you return on Monday, you ask Claude to show you open deferrals and it reads the state file and answers in seconds.

---

## Part 3. Set Up

1. Claude Code installed and signed in. Project folder `Supplier_Lifecycle_2026/` already set up from Lesson 01.
2. The following files in `Master/`:
   - `supplier-master.csv` (30 rows)
3. `Drafts/Supplier_Segmentation_v4.csv` from Lesson 05 already present.
4. A `State/` subfolder inside `Supplier_Lifecycle_2026/`. Create it now if it does not exist.
5. OneDrive sync paused.

---

## Part 4. Step-by-Step

**Step 1.** Open Claude Code in the project folder.

```
cd "Supplier_Lifecycle_2026"
claude
```

You should see the Claude Code prompt showing `Supplier_Lifecycle_2026` as the working folder.

**Step 2.** State the read-only rule and give Claude the session startup instruction.

```
The folder Master/ holds the source data files. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ or State/ unless I tell you otherwise.
If a file named State/Lifecycle_State.json exists, read it at the start of every session.
That file is the current truth for all supplier stages and open decisions.
```

Claude should confirm. Nothing changes on disk.

**Step 3.** Initialize the state file from the current segmentation data.

```
Read Drafts/Supplier_Segmentation_v4.csv.
Create State/Lifecycle_State.json.
For each supplier, include these fields:
  - Supplier_Name
  - Stage (from the Stage column in the CSV)
  - Last_Action_Date (set to 2026-04-25 for all suppliers on initialization)
  - Decision_Status (set to "Current" for all suppliers on initialization)
  - Notes (set to the Reason column value from the CSV)
  - Decision_Log (an empty array for each supplier)

This file is the persistent state. Every future session will read it first.
Save to State/Lifecycle_State.json.
```

You should see a confirmation that `State/Lifecycle_State.json` was created with 30 records. If the file was not created, check that the `State/` folder exists in the project root.

**Step 4.** Record a new decision and a deferred decision.

```
Update State/Lifecycle_State.json with these two decisions:

1. Apex Electronics: Decision_Status = "CAP Issued". Last_Action_Date = 2026-04-25.
   Notes = "CAP issued 2026-04-25. Root cause due 2026-05-09. Score target 78 by Q2 2026."
   Append to Decision_Log: { "date": "2026-04-25", "action": "CAP Issued", "approved_by": "User", "notes": "CAP sent to supplier." }

2. Coastal Coatings: Decision_Status = "Deferred". Last_Action_Date = 2026-04-25.
   Notes = "Stage change to Under Review deferred. Awaiting director call Monday 2026-04-28."
   Append to Decision_Log: { "date": "2026-04-25", "action": "Stage change deferred", "approved_by": "Deferred", "notes": "Director call Monday 2026-04-28." }

Do not change any other records.
```

You should see a confirmation that two records were updated.

**Step 5.** Verify the state file reflects both decisions.

```
Read State/Lifecycle_State.json.
Show me the full record for Apex Electronics and the full record for Coastal Coatings,
including their Decision_Log arrays.
```

You should see both records with the correct Decision_Status values and a Decision_Log entry each.

**Step 6.** Simulate closing and reopening the session to test persistence.

Close Claude Code by typing:

```
/exit
```

You should see the Claude Code session end and return you to the terminal prompt.

**Step 7.** Start a new session and verify the state survives.

```
cd "Supplier_Lifecycle_2026"
claude
```

You should see a fresh Claude Code session with no prior conversation.

**Step 8.** Ask Claude to read the state file and report open deferrals.

```
Read State/Lifecycle_State.json.
List every supplier where Decision_Status is "Deferred".
For each, show: Supplier_Name, Stage, Last_Action_Date, Notes, and the most recent Decision_Log entry.
```

You should see Coastal Coatings listed with the deferral note from Friday. Claude retrieved this from the state file alone, with no memory of the previous session.

**Step 9.** Resolve the deferred decision.

```
Read State/Lifecycle_State.json.
Update Coastal Coatings as follows:
  - Stage = "Under Review"
  - Decision_Status = "Current"
  - Last_Action_Date = 2026-04-28
  - Notes = "Stage changed to Under Review after director call 2026-04-28."
  - Append to Decision_Log: { "date": "2026-04-28", "action": "Stage set to Under Review", "approved_by": "User", "notes": "Director confirmed on call." }
Do not change any other records.
Save the file.
```

You should see a confirmation that Coastal Coatings was updated and the file was saved.

---

## Part 5. Worked Example, End to End

**Starting files:**

- `Drafts/Supplier_Segmentation_v4.csv`: 30 rows, with Stage and Reason columns for all suppliers including Apex Electronics (At Risk, CAP issued), Coastal Coatings (Under Review, audit pending), and Regional Supply Co (Exit, letter sent).

**Prompts used, in order:**

```
The folder Master/ holds the source data files. Do not edit any file in Master/.
Save all output to Drafts/ or State/.
If State/Lifecycle_State.json exists, read it at the start of every session.
```

```
Read Drafts/Supplier_Segmentation_v4.csv.
Create State/Lifecycle_State.json with fields: Supplier_Name, Stage, Last_Action_Date,
Decision_Status, Notes, Decision_Log (empty array).
Set Last_Action_Date to 2026-04-25 and Decision_Status to "Current" for all records.
```

```
Update State/Lifecycle_State.json for Apex Electronics: Decision_Status "CAP Issued",
Decision_Log entry with action "CAP Issued", approved_by "User".
For Coastal Coatings: Decision_Status "Deferred", Decision_Log entry with action
"Stage change deferred", approved_by "Deferred", notes "Director call Monday 2026-04-28."
```

After restarting the session:

```
Read State/Lifecycle_State.json.
List every supplier where Decision_Status is "Deferred".
Show Supplier_Name, Stage, Last_Action_Date, Notes, and the most recent Decision_Log entry.
```

**Extract of output (State/Lifecycle_State.json, two records):**

```json
[
  {
    "Supplier_Name": "Apex Electronics",
    "Stage": "At Risk",
    "Last_Action_Date": "2026-04-25",
    "Decision_Status": "CAP Issued",
    "Notes": "CAP issued 2026-04-25. Root cause due 2026-05-09. Score target 78 by Q2 2026.",
    "Decision_Log": [
      {
        "date": "2026-04-25",
        "action": "CAP Issued",
        "approved_by": "User",
        "notes": "CAP sent to supplier."
      }
    ]
  },
  {
    "Supplier_Name": "Coastal Coatings",
    "Stage": "Under Review",
    "Last_Action_Date": "2026-04-25",
    "Decision_Status": "Deferred",
    "Notes": "Stage change to Under Review deferred. Awaiting director call Monday 2026-04-28.",
    "Decision_Log": [
      {
        "date": "2026-04-25",
        "action": "Stage change deferred",
        "approved_by": "Deferred",
        "notes": "Director call Monday 2026-04-28."
      }
    ]
  }
]
```

**Finished artifacts:**
- `State/Lifecycle_State.json`: 30-record persistent state file, readable in any future session.

---

## Part 6. Common Mistakes and How to Recover

- **Symptom:** After restarting, Claude does not read State/Lifecycle_State.json automatically. **Fix:** Claude Code reads files only when instructed. You must include the startup instruction (as in Step 2) in your first prompt every session. Consider adding it to a `CLAUDE.md` file at the project root so it loads automatically. Ask Claude: "Read the CLAUDE.md guide at the project root and follow the session startup instructions there."

- **Symptom:** The state file was not created in the State/ folder. **Fix:** The State/ subfolder may not exist. Ask Claude: "Create the folder State/ in the project root if it does not exist, then save Lifecycle_State.json there." On Windows, Claude Code can create folders via file write operations.

- **Symptom:** Claude overwrote an existing Decision_Log entry instead of appending. **Fix:** The state file rules say the log is append-only. Restate: "Append a new entry to the Decision_Log array for Coastal Coatings. Do not modify or delete existing entries." If entries were overwritten, ask Claude to show you the current Decision_Log for that supplier and manually re-add the missing entry.

- **Symptom:** The state file grows very large after many sessions. **Fix:** The Decision_Log is intentionally append-only for audit purposes. Once it exceeds 50 entries per supplier, archive old entries: "Move all Decision_Log entries dated before 2026-01-01 from State/Lifecycle_State.json to State/Decision_Archive_2025.json. Remove them from the active state file. Do not remove any entries dated 2026-01-01 or later."

- **Symptom:** Two people updated the state file at the same time from different machines and one version was overwritten. **Fix:** OneDrive will show a conflict copy. Ask Claude: "Read State/Lifecycle_State.json and State/Lifecycle_State-DESKTOP-AB12.json. For each supplier where the records differ, show me the difference." Manually merge the correct entries and save the resolved version. Then enforce a rule: only one person runs Claude Code against this folder at a time.

- **Symptom:** After resolving a deferral, the Decision_Status is still showing "Deferred". **Fix:** Ask Claude: "Read State/Lifecycle_State.json and show me the full record for Coastal Coatings." If the Decision_Status was not updated, ask Claude to re-read the file and apply the update explicitly: "Set Decision_Status to 'Current' for Coastal Coatings and save the file."
