# Lesson 5: Project settings and slash commands

**Time:** 40 minutes.

## Same two prompts, every single Monday

It is 08:45 Monday. You open Claude Code and type the same thing you typed last Monday: "Read state/initiative-tracker.md and data/savings-log.csv. Give me a status update on the direct materials consolidation initiative." Then, ten minutes later: "Now read all the data files and build me a consolidated weekly review across all eight initiatives."

These two prompts are identical every week. The wording never changes. Only the data changes. You are typing 50 words each time to trigger the same workflow. That is what slash commands fix. You type `/initiative-status` or `/weekly-review`, and Claude runs the full workflow.

## What Claude Code is going to do for you

You will create two slash commands that live in your project's `.claude/commands/` folder. These commands persist across sessions because they are files on disk. You will also configure `.claude/settings.json` with project-level tool permissions. When any team member clones this project, the commands and permissions come with it.

## Set up

1. Lessons 1 through 4 complete (`.claude/settings.json`, `CLAUDE.md`, `state/initiative-tracker.md`, and `state/decisions-log.md` all exist).
2. A terminal open in `Course_08_The_Project_Architect/practice/`.

## Step-by-step

### Create the commands directory

**Step 1.** Start Claude Code in the practice folder.

```
cd "Course_08_The_Project_Architect/practice"
claude
```

You should see the Claude Code prompt.

**Step 2.** Create the `.claude/commands/` directory.

```
Create a directory at .claude/commands/ if it does not already exist.
```

You should see Claude confirm the directory exists or was created.

### Build the initiative-status command

**Step 3.** Create the initiative-status slash command.

```
Create a file at .claude/commands/initiative-status.md with this content:

# Initiative Status Check

Read state/initiative-tracker.md for the current status of initiative "$ARGUMENTS".

Then read data/savings-log.csv and filter for the matching initiative_id. Calculate:
- Total realized savings to date
- Cumulative target savings to date
- Variance (realized minus target)
- Week-over-week trend (last 4 weeks)

Then read data/milestone-tracker.csv and filter for the matching initiative_id. List:
- Completed milestones with actual dates
- Pending milestones with target dates
- Any overdue milestones (target date before 2026-04-25 and no actual date)

Output a concise status update. Include the initiative name, owner, stage, status, savings summary, milestone summary, and any notes from the tracker. Use USD with commas. Dates in YYYY-MM-DD format.
```

You should see Claude create the file at `.claude/commands/initiative-status.md`.

**Step 4.** Test the command. Exit and restart Claude Code so it picks up the new command.

```
/quit
```

Then:

```
claude
```

You should see the Claude Code prompt.

**Step 5.** Run the initiative-status command.

```
/initiative-status INIT-001
```

You should see a status update for Direct Materials Consolidation: owner Sarah Chen, stage Execution, status on track, approximately $746,500 realized savings, and the next milestone (RFP issued, target 2026-05-24). If Claude does not recognize the command, confirm the file is at `.claude/commands/initiative-status.md` with `ls .claude/commands/`.

**Step 6.** Test with a different initiative.

```
/initiative-status INIT-002
```

You should see a status update for Logistics Network Optimization showing at-risk status, approximately $297,115 realized, a negative variance of about -$168,269, and the next milestone (Market analysis complete, target 2026-05-02).

### Build the weekly-review command

**Step 7.** Create the weekly-review slash command.

```
Create a file at .claude/commands/weekly-review.md with this content:

# Weekly Review

Read state/initiative-tracker.md for the current state of all 8 initiatives.
Read state/decisions-log.md for any decisions made since the last review.
Read data/savings-log.csv and data/milestone-tracker.csv for the latest data.

Produce a weekly review document with these sections:

1. Executive summary: one paragraph naming the total program savings target ($14.9M), total realized to date, overall variance, and the count of initiatives on track, at risk, and behind schedule.

2. Initiative-by-initiative status: a table with columns ID, Name, Stage, Status, Realized, Target, Variance.

3. Key risks and actions: list any initiative with status "at_risk" or "behind_schedule". Name the owner and the specific issue.

4. Decisions made this week: pull from state/decisions-log.md. List only entries from the past 7 days.

5. Next week priorities: list the next pending milestone for each initiative, sorted by target date.

Save the output to outputs/weekly-reviews/weekly-review-2026-04-25.md.

After saving, update the "Last updated" timestamp in state/initiative-tracker.md to today's date.
```

You should see Claude create the file at `.claude/commands/weekly-review.md`.

**Step 8.** Exit and restart Claude Code.

```
/quit
```

Then:

```
claude
```

**Step 9.** Run the weekly-review command.

```
/weekly-review
```

You should see Claude read all the data and state files, produce a weekly review, and save it to `outputs/weekly-reviews/weekly-review-2026-04-25.md`. The review should name the $14.9M target, list all eight initiatives, flag INIT-002 and INIT-007 as risks, and include the three decisions from Lesson 4.

If you see an error about the `outputs/weekly-reviews/` directory not existing, ask Claude to create it and run the command again.

**Step 10.** Review the output.

```
Read outputs/weekly-reviews/weekly-review-2026-04-25.md and show me the executive summary.
```

You should see a summary paragraph with the program total, realized savings, and risk count.

**Step 11.** Exit Claude Code.

```
/quit
```

## Worked example

**Project structure after this lesson:**

```
practice/
├── .claude/
│   ├── settings.json
│   └── commands/
│       ├── initiative-status.md
│       └── weekly-review.md
├── CLAUDE.md
├── state/
│   ├── initiative-tracker.md
│   └── decisions-log.md
├── data/
│   ├── initiatives.csv
│   ├── savings-log.csv
│   ├── stakeholders.csv
│   └── milestone-tracker.csv
└── outputs/
    └── weekly-reviews/
        └── weekly-review-2026-04-25.md
```

**What Claude did, behind the scenes:**

1. Claude read the slash command file (for example, `initiative-status.md`) when you typed `/initiative-status`.
2. The `$ARGUMENTS` placeholder in the command file was replaced with the text you typed after the command name (for example, `INIT-001`).
3. Claude followed the instructions in the command file: read the tracker, read the CSVs, filter, calculate, and format the output.
4. For the weekly review, Claude read four files (tracker, decisions log, savings log, milestones), combined the data, and saved the output to a dated file.
5. The commands persist across sessions because they are files in `.claude/commands/`, not conversation history.

## Common mistakes and how to recover

- **Symptom:** You type `/initiative-status` and Claude says "unknown command." **Fix:** the command file must be at `.claude/commands/initiative-status.md` (not `.claude/initiative-status.md` or `commands/initiative-status.md`). Check the path with `ls .claude/commands/`.

- **Symptom:** You registered a hook in the global `~/.claude/settings.json` instead of the project `settings.json`. Now the hook runs in every project, not just this one. **Fix:** move project-specific settings to `.claude/settings.json` inside the project folder. Global settings should contain only machine-wide defaults.

- **Symptom:** The weekly review output is empty or missing sections. **Fix:** the command file may reference files that do not exist yet (for example, `outputs/weekly-reviews/`). Create the directory first. Ask Claude: "Create the directory outputs/weekly-reviews/ if it does not exist."

- **Symptom:** The `$ARGUMENTS` placeholder does not expand. Claude treats "INIT-001" as literal text in the command file. **Fix:** make sure the placeholder is written as `$ARGUMENTS` (all caps, with the dollar sign). Claude Code replaces this with whatever you type after the slash command name.

## You are done with Lesson 5 when

- You have two slash command files in `.claude/commands/`: `initiative-status.md` and `weekly-review.md`.
- You can type `/initiative-status INIT-001` and get a scoped status update.
- You can type `/weekly-review` and get a full program review saved to `outputs/weekly-reviews/`.
- You understand that project settings in `.claude/settings.json` apply only to this project folder, while global settings apply everywhere.

Move to Lesson 6, where you share this project with a teammate using git.
