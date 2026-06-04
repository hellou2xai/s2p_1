# Lesson 6: Team project sharing

**Time:** 35 minutes.

## Priya needs the same setup

It is 10:00 Thursday. Priya Patel manages INIT-003 (IT Services Rationalization) and INIT-008 (Temp Staffing Consolidation). She sees you running initiative status checks and weekly reviews in seconds. She wants the same setup for her two initiatives. She asks: "Can you send me your Claude Code project folder?"

You could zip the folder and email it. But that creates two copies with no way to keep them in sync. When you update the CLAUDE.md to reflect a stage change, Priya's copy falls behind. When Priya records a decision, your log does not have it.

The answer is a shared git repository. You commit the project files, Priya clones the repo, and both of you work from the same source of truth. CLAUDE.md updates go through pull requests. State files follow a naming convention so you do not overwrite each other's notes.

## What Claude Code is going to do for you

You will initialize a git repository in your project folder, commit the project structure (CLAUDE.md, settings, commands, state files), and document the conventions a teammate needs to start working. You will also establish rules for what gets committed and what stays local.

## Set up

1. Lessons 1 through 5 complete (full project structure in place).
2. Git installed on your machine. Check by running `git --version` in your terminal.
3. A terminal open in `Course_08_The_Project_Architect/practice/`.

## Step-by-step

### Define what gets committed

Not everything in the project belongs in the repository. Here is the split:

| Commit to git | Do not commit |
|---|---|
| `CLAUDE.md` | Personal preference files |
| `.claude/settings.json` | API keys or tokens |
| `.claude/commands/*.md` | Large data exports |
| `state/initiative-tracker.md` | Temporary analysis files |
| `state/decisions-log.md` | Session logs |
| `data/*.csv` (source data) | `.claude/credentials` |

The rule: commit anything the team needs to share context. Do not commit anything personal or sensitive.

### Initialize the repository

**Step 1.** Start Claude Code in the practice folder.

```
cd "Course_08_The_Project_Architect/practice"
claude
```

You should see the Claude Code prompt.

**Step 2.** Create a `.gitignore` file.

```
Create a file at .gitignore with this content:

# Personal Claude settings
.claude/credentials
.claude/*.local.*

# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak

# Session-specific outputs (commit only finalized weekly reviews)
outputs/drafts/
```

You should see Claude create the `.gitignore` file.

**Step 3.** Exit Claude Code.

```
/quit
```

**Step 4.** Initialize the git repository.

```
git init
```

You should see: "Initialized empty Git repository in .../practice/.git/"

**Step 5.** Stage the project files.

```
git add CLAUDE.md .claude/settings.json .claude/commands/ state/ data/ .gitignore
```

You should see no errors. Git stages the files silently.

**Step 6.** Verify what is staged.

```
git status
```

You should see a list of new files to be committed: CLAUDE.md, .claude/settings.json, the two command files, the two state files, the four CSV files, and .gitignore.

**Step 7.** Create the first commit.

```
git commit -m "Initial project setup: CLAUDE.md, settings, commands, state files, and source data"
```

You should see a commit confirmation with the count of files added.

### Document the onboarding steps

**Step 8.** Start Claude Code again.

```
claude
```

**Step 9.** Create a brief contributor guide.

```
Create a file at CONTRIBUTING.md with this content:

# Contributing to the Savings Program Project

## Getting started

1. Clone the repository.
2. Open a terminal in the project root.
3. Run `claude` to start Claude Code. It reads CLAUDE.md and .claude/settings.json automatically.
4. Read state/initiative-tracker.md to see the current status of all 8 initiatives.
5. Run /initiative-status INIT-XXX to check a specific initiative.
6. Run /weekly-review to generate the weekly review.

## State file conventions

- **initiative-tracker.md**: Current status. Updated in place. Only one person should update a given initiative section at a time. Coordinate via Slack before editing.
- **decisions-log.md**: Append only. Never delete or edit previous entries. Add your decision at the bottom.

## Making changes to CLAUDE.md

CLAUDE.md defines the shared context for the entire team. Changes to CLAUDE.md go through a pull request. Do not edit CLAUDE.md directly on the main branch.

Examples of CLAUDE.md changes that need a PR:
- An initiative moves to a new stage.
- A new initiative is added to the program.
- A stakeholder changes role or leaves the team.
- Output formatting rules change.

## What not to commit

- Personal settings or preferences.
- API keys, tokens, or credentials.
- Draft outputs that are not finalized.
- Session-specific analysis files.

## Updating the initiative tracker

When you update an initiative during a session:
1. Tell Claude to update only the section for your initiative in state/initiative-tracker.md.
2. Update the "Last updated" timestamp.
3. Commit the change with a message that names the initiative. Example: "Update INIT-003 status to monitoring."
4. Push to the shared repository.
```

You should see Claude create `CONTRIBUTING.md`.

**Step 10.** Exit Claude Code.

```
/quit
```

**Step 11.** Stage and commit the contributor guide.

```
git add CONTRIBUTING.md
git commit -m "Add contributor guide for team onboarding"
```

You should see a commit confirmation.

### Simulate what Priya would do

**Step 12.** Verify the project works from a clean start. Start Claude Code.

```
claude
```

**Step 13.** Run the initiative-status command for one of Priya's initiatives.

```
/initiative-status INIT-003
```

You should see a status update for IT Services Rationalization: owner Priya Patel, stage Execution, on track, approximately $932,859 realized savings, and the next milestone (Recommendation approved, target 2026-05-20).

**Step 14.** Record a decision as Priya would.

```
Append a new entry to state/decisions-log.md:

Date: 2026-04-25
Initiative: INIT-003 (IT Services Rationalization)
Decision: Recommend Acme IT Solutions as preferred supplier at $1.72M over 36 months.
Context: Acme scored highest on technical evaluation (92/100) and offered the lowest total cost of ownership. Two other finalists scored 85 and 78.
Approved by: Pending (Lisa Torres review by 2026-05-20)
Recorded by: Priya Patel
```

You should see Claude append the fourth decision entry to the log.

**Step 15.** Exit Claude Code.

```
/quit
```

**Step 16.** Commit the state update.

```
git add state/decisions-log.md
git commit -m "INIT-003: Record supplier recommendation decision"
```

You should see a commit confirmation.

## Worked example

**Final project structure:**

```
practice/
├── .claude/
│   ├── settings.json
│   └── commands/
│       ├── initiative-status.md
│       └── weekly-review.md
├── .git/
├── .gitignore
├── CLAUDE.md
├── CONTRIBUTING.md
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

1. Claude created the `.gitignore` to exclude personal files and temporary outputs.
2. Git initialized a repository and tracked the shared project files.
3. Claude created a contributor guide that documents the state file conventions and the PR workflow for CLAUDE.md changes.
4. When simulating Priya's workflow, Claude read the same CLAUDE.md and state files, ran the same slash commands, and appended to the same decisions log.
5. The git commit history shows who changed what and when, providing the audit trail procurement teams need.

## Common mistakes and how to recover

- **Symptom:** You committed your personal `.claude/credentials` file to git. **Fix:** remove it from tracking with `git rm --cached .claude/credentials`. Add `.claude/credentials` to `.gitignore`. Rotate any exposed credentials immediately.

- **Symptom:** Two people edit `state/initiative-tracker.md` at the same time. Git reports a merge conflict. **Fix:** coordinate updates via Slack or a shared calendar. Each person owns specific initiative sections. Pull before editing, push after committing. If a conflict occurs, open the file and manually resolve the conflicting sections.

- **Symptom:** CLAUDE.md on the main branch is outdated. Someone edited it directly without a PR. **Fix:** revert the direct edit with `git revert`. Re-apply the change through a pull request so the team reviews it. Add branch protection rules if your repository host supports them.

- **Symptom:** A teammate cloned the repo but the slash commands do not work. **Fix:** confirm the commands are at `.claude/commands/initiative-status.md` and `.claude/commands/weekly-review.md`. The teammate may need to restart Claude Code after cloning so it picks up the new command files.

## You are done with Lesson 6 when

- Your project folder is a git repository with at least two commits.
- You have a `.gitignore` that excludes personal and sensitive files.
- You have a `CONTRIBUTING.md` that documents the state file conventions and the CLAUDE.md update workflow.
- You recorded a decision as a teammate would and committed it with a descriptive message.
- You can explain why CLAUDE.md changes should go through pull requests.

## You are done with the course when

You have completed all six lessons and your project meets these criteria:

1. A `.claude/` directory with `settings.json` and two slash commands.
2. A `CLAUDE.md` with all eight initiatives, stages, owners, and stakeholders.
3. A `state/initiative-tracker.md` with current status for all eight initiatives.
4. A `state/decisions-log.md` with at least four dated, attributed entries.
5. You can close Claude Code, reopen it, and pick up where you left off without re-explaining the program.
6. A teammate can clone the repository and start working with the same context, commands, and conventions.

The project you built is a pattern. Apply it to any multi-initiative program, any category portfolio, or any long-running procurement engagement. The structure stays the same. The content changes.
