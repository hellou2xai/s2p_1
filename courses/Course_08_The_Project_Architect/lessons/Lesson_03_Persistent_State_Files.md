# Lesson 3: Persistent state files

**Time:** 50 minutes.

## Close the session, lose the progress

It is 14:00 Wednesday. You just spent 30 minutes with Claude Code reviewing the savings program. You updated the status of INIT-003 (IT Services Rationalization) from Execution to near-complete. You noted that INIT-002 (Logistics Network Optimization) is $168,269 behind its cumulative savings target. You identified that INIT-007 (Packaging Material Switch) has missed two milestone dates.

Then your laptop battery dies. You plug in, restart Claude Code, and type: "Where did we leave off?"

Claude Code responds: "I don't have any context about a previous session. Could you tell me what you were working on?"

All 30 minutes of analysis are gone. The conversation history does not survive a session restart. CLAUDE.md gives Claude Code the portfolio structure, but it does not capture what changed during the session. You need a file that records current state and gets updated each session.

## What Claude Code is going to do for you

You will create a state file called `state/initiative-tracker.md`. At the start of every session, Claude Code reads it. During the session, you update initiative statuses, flag risks, and note progress. At the end, Claude writes the updated state back to the file. The next session picks up exactly where you left off.

## Set up

1. Lessons 1 and 2 complete (`.claude/settings.json` and updated `CLAUDE.md` exist).
2. The practice data files in `data/`.
3. A terminal open in `Course_08_The_Project_Architect/practice/`.

## Step-by-step

### Create the state directory and initial tracker

**Step 1.** Start Claude Code in the practice folder.

```
cd "Course_08_The_Project_Architect/practice"
claude
```

You should see the Claude Code prompt. Claude loads CLAUDE.md automatically.

**Step 2.** Create the `state/` directory.

```
Create a directory called state/ in the project root.
```

You should see Claude confirm the directory was created.

**Step 3.** Build the initial initiative tracker from the source data.

```
Read data/initiatives.csv, data/savings-log.csv, and data/milestone-tracker.csv. Create a file at state/initiative-tracker.md with this structure:

# Initiative Tracker
Last updated: 2026-04-25

For each of the 8 initiatives, include:
- Initiative ID and name
- Owner
- Stage and status
- Target savings and realized savings to date (sum from savings-log.csv)
- Variance (realized minus target cumulative)
- Next milestone and its target date (from milestone-tracker.csv, pick the earliest pending milestone)
- One-line notes field (leave blank for now)

Use a consistent format: one H2 heading per initiative, then a short table of fields. Keep it scannable.
```

You should see Claude read all three data files, calculate realized savings for each initiative, identify the next pending milestone, and save `state/initiative-tracker.md`.

**Step 4.** Review the tracker.

```
Read state/initiative-tracker.md and show me the contents.
```

You should see eight sections, one per initiative. Each section should show the current stage, realized savings, variance, and next milestone. For example, INIT-001 (Direct Materials Consolidation) should show approximately $746,500 in realized savings and the next milestone as "RFP issued" with a target date of 2026-05-24.

**Step 5.** Verify the numbers against the source data.

```
For INIT-002 (Logistics Network Optimization), compare the realized savings total in the tracker against the sum of realized_savings_usd in data/savings-log.csv for initiative_id INIT-002. Do the numbers match?
```

You should see Claude confirm the numbers match (approximately $297,115 realized for INIT-002). If they differ, ask Claude to fix the tracker.

### Simulate a session update

**Step 6.** Update an initiative status during the session.

```
Update state/initiative-tracker.md with these changes:

1. INIT-003 (IT Services Rationalization): Change status from "on_track" to "on_track". Add note: "Recommendation approval pending. Lisa Torres reviewing. Decision expected by 2026-05-20."

2. INIT-002 (Logistics Network Optimization): Keep status as "at_risk". Add note: "Cumulative variance is -$168,269. Marcus Rivera escalated to Tom Baker on 2026-04-25. Root cause: two carriers declined to bid."

3. Update the "Last updated" timestamp to 2026-04-25.

Save the file. Do not overwrite the entire file. Update only the sections that changed.
```

You should see Claude update the two initiative sections and the timestamp. The other six initiatives remain unchanged.

**Step 7.** Confirm the updates persisted.

```
Read state/initiative-tracker.md and show me only the INIT-002 and INIT-003 sections.
```

You should see the updated notes for both initiatives.

### Test cross-session persistence

**Step 8.** Exit Claude Code.

```
/quit
```

**Step 9.** Restart Claude Code.

```
claude
```

You should see the Claude Code prompt. Claude reads CLAUDE.md and (because CLAUDE.md references state files) knows to check `state/`.

**Step 10.** Ask Claude about the state from the previous session.

```
Read state/initiative-tracker.md. What is the current note on INIT-002?
```

You should see: "Cumulative variance is -$168,269. Marcus Rivera escalated to Tom Baker on 2026-04-25. Root cause: two carriers declined to bid." The state survived the session restart because it is a file on disk, not conversation history.

**Step 11.** Exit Claude Code.

```
/quit
```

## Worked example

**The initiative-tracker.md should look similar to this (showing two of eight sections):**

```markdown
# Initiative Tracker

Last updated: 2026-04-25

## INIT-001: Direct Materials Consolidation

| Field | Value |
|---|---|
| Owner | Sarah Chen |
| Stage | Execution |
| Status | On track |
| Target savings | $2,800,000 |
| Realized to date | $746,500 |
| Variance | -$7,347 |
| Next milestone | RFP issued (2026-05-24) |
| Notes | |

## INIT-002: Logistics Network Optimization

| Field | Value |
|---|---|
| Owner | Marcus Rivera |
| Stage | Sourcing |
| Status | At risk |
| Target savings | $2,200,000 |
| Realized to date | $297,115 |
| Variance | -$168,269 |
| Next milestone | Market analysis complete (2026-05-02) |
| Notes | Cumulative variance is -$168,269. Marcus Rivera escalated to Tom Baker on 2026-04-25. Root cause: two carriers declined to bid. |
```

**What Claude did, behind the scenes:**

1. Claude read `data/initiatives.csv` for the base portfolio data (8 rows).
2. Claude read `data/savings-log.csv` (120 rows) and summed `realized_savings_usd` by `initiative_id` to get realized totals.
3. Claude read `data/milestone-tracker.csv` (40 rows) and filtered for the earliest pending milestone per initiative.
4. Claude combined all three sources into a single structured markdown file.
5. When you asked for updates, Claude edited only the changed sections, preserving the rest of the file.
6. On the next session start, Claude read the tracker file and had the full current state without re-deriving it from the CSVs.

## Common mistakes and how to recover

- **Symptom:** You relied on conversation history instead of writing state to a file. The next session starts blank. **Fix:** always ask Claude to save status updates to `state/initiative-tracker.md` before ending a session. Add a reminder to your CLAUDE.md: "Before ending a session, update state/initiative-tracker.md with any status changes."

- **Symptom:** Claude overwrote the entire tracker file, wiping updates from a previous session. **Fix:** tell Claude to "update only the sections that changed" or "edit the file in place." Do not say "create a new initiative-tracker.md" because that triggers a full overwrite.

- **Symptom:** The tracker has stale data because you forgot to update it for two weeks. **Fix:** re-derive the tracker from the source CSVs. Ask Claude: "Read all four data files and rebuild state/initiative-tracker.md from scratch. Preserve any notes from the existing file."

- **Symptom:** You stored the tracker inside the `data/` folder, and your permissions block writes to `data/`. **Fix:** state files belong in `state/`, not `data/`. The `data/` folder is read-only for source data. Move the file: "Move state files from data/ to state/."

- **Symptom:** The realized savings numbers in the tracker do not match the CSV totals. **Fix:** ask Claude to re-sum the savings from `data/savings-log.csv` and compare against the tracker. Update any mismatches.

## You are done with Lesson 3 when

- You have a file at `state/initiative-tracker.md` with all eight initiatives.
- Each initiative section shows owner, stage, status, target savings, realized savings, variance, next milestone, and notes.
- You closed Claude Code, reopened it, and confirmed the state persisted.
- You can explain why files beat conversation history for cross-session memory.

Move to Lesson 4, where you build a decisions log that records program decisions across sessions without overwriting previous entries.
