# Lesson 2: Writing a project CLAUDE.md for a multi-initiative program

**Time:** 45 minutes.

## Eight initiatives, zero memory

It is 09:30 Tuesday. Your VP, Lisa Torres, pings you on Slack: "Can you pull together a status snapshot for the savings program? Board deck is due Thursday." You open Claude Code. You know the eight initiatives, their stages, their owners. But Claude Code does not. You start typing: "We have a direct materials consolidation initiative owned by Sarah Chen, targeting $2.8M, currently in execution stage..." You get through three initiatives before you realize you are going to spend 20 minutes just setting context. Again.

The `CLAUDE.md` file you created in Lesson 1 covers the basics: your role, the data file locations, and the stage definitions. But it does not list the eight initiatives, their owners, their targets, or their current status. Every session, you re-explain the program.

## What Claude Code is going to do for you

You will write a `CLAUDE.md` that encodes the full savings program: all eight initiatives with their stages, owners, targets, and status. When Claude Code starts, it reads this file and knows the entire portfolio. You skip straight to the work. Total context-setting time: zero.

## Set up

1. Lesson 1 complete (`.claude/settings.json` exists in the practice folder).
2. The practice data files in `data/` (initiatives.csv, stakeholders.csv, savings-log.csv, milestone-tracker.csv).
3. A terminal open in `Course_08_The_Project_Architect/practice/`.

## Step-by-step

### Decide what goes in CLAUDE.md

The rule is simple: put in what every session needs. Leave out what only some sessions need.

**Put in CLAUDE.md:**

- Your role and the program name.
- The list of all eight initiatives with ID, name, owner, target, stage, and status.
- Stage definitions (what each stage means).
- Key stakeholders and their roles.
- File locations and which folders are read-only.
- Output formatting rules (currency format, date format, voice).

**Leave out of CLAUDE.md:**

- The full contents of data files (Claude can read them when needed).
- Session-specific notes (those go in state files, covered in Lesson 3).
- Decisions made during sessions (those go in the decisions log, covered in Lesson 4).
- Long reference documents or policies.

The goal: CLAUDE.md should be 60 to 120 lines. If it grows past 150 lines, move detail into separate files and reference them from CLAUDE.md.

### Write the CLAUDE.md

**Step 1.** Start Claude Code in the practice folder.

```
cd "Course_08_The_Project_Architect/practice"
claude
```

You should see the Claude Code prompt.

**Step 2.** Ask Claude to read the current CLAUDE.md.

```
Read CLAUDE.md and show me the contents.
```

You should see the existing CLAUDE.md that came with the practice folder. It covers your role, data file locations, stage definitions, and output standards.

**Step 3.** Ask Claude to rewrite CLAUDE.md with the full initiative portfolio.

```
Rewrite CLAUDE.md to include all of the following. Read data/initiatives.csv and data/stakeholders.csv to get the real data. Keep the file under 120 lines.

1. Role: Savings Program Manager at Pinnacle Procurement. $14.9M savings target across 8 initiatives.

2. Initiative portfolio table with columns: ID, Name, Category, Owner, Target (USD), Stage, Status. Pull all 8 rows from initiatives.csv.

3. Key stakeholders table with columns: Name, Role, Initiatives. Pull from stakeholders.csv.

4. Stage definitions table (keep the existing one).

5. Data file locations: all files in data/ are read-only.

6. State file locations: files in state/ are read-write. Read initiative-tracker.md at session start. Update it before session end.

7. Output rules: USD with commas, dates in YYYY-MM-DD, active voice, no em-dashes, Oxford commas.

8. Weekly review output goes to outputs/weekly-reviews/.

Save the result as CLAUDE.md in the project root (overwrite the existing file).
```

You should see Claude read both CSV files, build the tables, and save the updated CLAUDE.md.

**Step 4.** Review the file Claude wrote.

```
Read CLAUDE.md and count the lines.
```

You should see a file between 60 and 120 lines. It should contain a table with all eight initiatives, a stakeholders table, stage definitions, file location rules, and output standards.

**Step 5.** Check that the initiative data matches the source.

```
Compare the initiative table in CLAUDE.md against data/initiatives.csv. Report any differences in names, targets, stages, or status.
```

You should see Claude confirm the data matches, or flag any discrepancies. If there are differences, ask Claude to fix them.

**Step 6.** Test the context by asking a program question.

```
Which initiatives are at risk or behind schedule?
```

You should see Claude respond with two initiatives: Logistics Network Optimization (INIT-002, at risk) and Packaging Material Switch (INIT-007, behind schedule). Claude pulled this from the CLAUDE.md it just wrote, without needing to re-read the CSV.

**Step 7.** Exit Claude Code.

```
/quit
```

### Verify persistence

**Step 8.** Restart Claude Code in the same folder.

```
claude
```

You should see the Claude Code prompt.

**Step 9.** Ask the same question again.

```
Which initiatives are at risk or behind schedule, and who owns them?
```

You should see: INIT-002 Logistics Network Optimization, owned by Marcus Rivera, at risk. INIT-007 Packaging Material Switch, owned by Marcus Rivera, behind schedule. Claude read this from CLAUDE.md on startup. No re-explanation needed.

**Step 10.** Exit Claude Code.

```
/quit
```

## Worked example

**The CLAUDE.md you built should look similar to this (shortened for space):**

```markdown
# Pinnacle Procurement: $14.9M Savings Program

## Role

You are the Savings Program Manager at Pinnacle Procurement. You manage
eight category initiatives with a combined annual savings target of $14.9M.

## Initiative portfolio

| ID | Name | Category | Owner | Target | Stage | Status |
|---|---|---|---|---|---|---|
| INIT-001 | Direct Materials Consolidation | direct-materials | Sarah Chen | $2,800,000 | Execution | On track |
| INIT-002 | Logistics Network Optimization | logistics | Marcus Rivera | $2,200,000 | Sourcing | At risk |
| INIT-003 | IT Services Rationalization | it-services | Priya Patel | $1,900,000 | Execution | On track |
| INIT-004 | Facilities Management Rebid | facilities | James Wright | $1,500,000 | Planning | On track |
| INIT-005 | Professional Services Rate Card | professional-services | Sarah Chen | $1,800,000 | Negotiation | On track |
| INIT-006 | MRO Catalog Standardization | mro | David Kim | $1,200,000 | Planning | Not started |
| INIT-007 | Packaging Material Switch | direct-materials | Marcus Rivera | $1,600,000 | Evaluation | Behind schedule |
| INIT-008 | Temp Staffing Consolidation | professional-services | Priya Patel | $1,900,000 | Execution | On track |

## Key stakeholders

| Name | Role | Initiatives |
|---|---|---|
| Lisa Torres | VP of Procurement | All |
| Robert Hayes | CFO | All |
| Sarah Chen | Senior Category Manager | INIT-001, INIT-005 |
| Marcus Rivera | Category Manager, Logistics | INIT-002, INIT-007 |
| Priya Patel | Category Manager, IT and Services | INIT-003, INIT-008 |
...
```

**What Claude did, behind the scenes:**

1. Claude read the existing CLAUDE.md to understand the current structure.
2. Claude read `data/initiatives.csv` and extracted all 8 rows with their fields.
3. Claude read `data/stakeholders.csv` and extracted all 12 team members.
4. Claude combined the data into markdown tables, formatted targets as USD with commas.
5. Claude preserved the stage definitions and output standards from the original file.
6. Claude saved the result, overwriting the old CLAUDE.md.
7. On the next session start, Claude loaded the new CLAUDE.md and had the full portfolio in context.

## Common mistakes and how to recover

- **Symptom:** CLAUDE.md is 300 lines long because you pasted the full savings-log.csv into it. **Fix:** CLAUDE.md should contain summaries and references, not raw data. Remove the pasted data. Add a line like "Read data/savings-log.csv when savings analysis is needed."

- **Symptom:** CLAUDE.md says "You are a procurement professional" and nothing else. **Fix:** that is too vague. Claude needs the specific program name ($14.9M savings program), the initiative count (8), and the portfolio table to be useful on startup.

- **Symptom:** The initiative table in CLAUDE.md has stale data. INIT-003 moved from Execution to Monitoring last week, but CLAUDE.md still says Execution. **Fix:** update CLAUDE.md when stages change. Or, better: use the initiative-tracker.md pattern from Lesson 3, where current status lives in a state file that gets updated each session.

- **Symptom:** Claude ignores parts of CLAUDE.md. **Fix:** check for formatting problems. Broken markdown tables (misaligned pipes, missing header separators) can cause Claude to misread the data. Ask Claude to "read CLAUDE.md and check for any broken markdown formatting."

## You are done with Lesson 2 when

- Your `CLAUDE.md` lists all eight initiatives with ID, name, category, owner, target, stage, and status.
- You can start a new Claude Code session and ask "which initiatives are behind schedule?" without providing any additional context.
- Your `CLAUDE.md` is between 60 and 120 lines. It references data files by path instead of embedding their contents.

Move to Lesson 3, where you build a state file that tracks initiative status across sessions and survives session restarts.
