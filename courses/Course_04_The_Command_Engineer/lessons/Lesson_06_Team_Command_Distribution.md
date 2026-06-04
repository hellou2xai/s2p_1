# Lesson 6: Team Command Distribution

**Time:** 25 minutes

---

## The S2P problem

It is 16:00 Friday. Your colleague Priya Slacks you: "I saw your spend breakdown this morning. The format was clean and consistent. Can I use your commands for my categories? I manage logistics and MRO, and every month I write the same prompts from scratch. Different wording every time, different output shapes every time."

This is the moment every procurement operations team hits. One person builds useful prompts, and the rest of the team wants them. But sharing prompts by copying text into Slack messages does not work. The wording drifts. Someone changes a column name. Another person forgets the threshold. Within two months, the "standard" report looks different depending on who ran it.

This lesson solves that problem. You will not write any new commands. Instead, you will version the six commands you have, organize them for sharing, and set up a pattern so the whole team uses the same library.

## What Claude Code is going to do for you

By the end of this lesson, your six command files will have version headers, a changelog, and a clear sharing path. Priya will be able to copy your `.claude/commands/` folder into her project, run `/spend-analyze Q1 logistics`, and get a report with the exact same structure as yours. No prompt drift. No format inconsistency.

## Set up

Confirm these before starting.

1. Claude Code installed and signed in.
2. Your terminal open in the `practice/` folder inside Course 04.
3. All six command files in `.claude/commands/`: `spend-analyze.md`, `anomaly-detect.md`, `scorecard-refresh.md`, `contract-sweep.md`, `rfp-launch.md`, and `savings-update.md`.
4. At least one output file in `outputs/` from each of the previous lessons.

---

## Part A: Project-level vs. user-level commands (5 minutes)

### Where commands live

Claude Code (in the terminal) looks for commands in two places:

| Location | Scope | Who sees them |
|---|---|---|
| `.claude/commands/` inside the project folder | Project-level | Anyone who opens this project folder in Claude Code |
| `~/.claude/commands/` in your home directory | User-level | Only you, across all your projects |

**Project-level commands** travel with the project. If you share the project folder (through Git, a shared drive, or a zip file), the commands come along. This is what you want for team standardization.

**User-level commands** are personal shortcuts. They stay on your machine. Use them for commands that only you need, like personal formatting preferences or shortcuts for tasks outside procurement.

### Step 1: Confirm your commands are project-level

Check that your commands are in the project folder, not in your home directory.

```
List all files in .claude/commands/ and confirm the path is relative to the practice/ folder, not my home directory
```

You should see six `.md` files listed under `.claude/commands/` inside the `practice/` folder. If Claude Code shows a path starting with `~/.claude/commands/` or your home directory, your commands are user-level. Move them to the project folder.

If you see the commands in your home directory instead of the project folder, copy them to the project.

```
Copy all .md files from ~/.claude/commands/ to .claude/commands/ in this project folder
```

You should see six files copied. Then delete the originals from the home directory if you do not need them there.

---

## Part B: Versioning your commands (10 minutes)

### Why version comments matter

When Priya uses your `/spend-analyze` command next month and gets an unexpected result, the first question is: "Which version of the command is she running?" Without a version marker, there is no way to know. A version comment at the top of each file answers that question in one line.

### Step 2: Check existing version comments

Your command files should already have a version comment from the solutions. Verify.

```
For each .md file in .claude/commands/ (excluding README.md), show me the first line only
```

You should see a line like `<!-- v1.0 2026-04-25 Initial. -->` at the top of each file. If any file is missing this line, add it in the next step.

### Step 3: Add or update version comments

If any command file is missing a version comment, add one now. The format is:

```
<!-- v1.0 YYYY-MM-DD Description of this version. -->
```

For any file that needs a version comment, ask Claude Code to add it.

```
For any command file in .claude/commands/ that does not start with a version comment, add this as the first line: <!-- v1.0 2026-04-25 Initial command for Course 04. -->
```

You should see Claude Code confirm it updated the files (or that all files already have version comments).

### Step 4: Create a changelog

A changelog tracks what changed across versions. This is the same pattern as skill versioning from Course 03. Create a changelog file in the commands folder.

```
Create .claude/commands/CHANGELOG.md with this content:

# Command Library Changelog

## 2026-04-25

- v1.0 spend-analyze.md: Initial. Spend breakdown by period and category.
- v1.0 anomaly-detect.md: Initial. Threshold-based anomaly detection with duplicate PO scan.
- v1.0 scorecard-refresh.md: Initial. Single-supplier scorecard summary with trend.
- v1.0 contract-sweep.md: Initial. Contract expiry sweep with urgency classification.
- v1.0 rfp-launch.md: Initial. Sourcing brief combining spend and contract data.
- v1.0 savings-update.md: Initial. Savings variance tracker with prorated targets.
```

You should see Claude Code create `CHANGELOG.md` in `.claude/commands/`.

### The version bump pattern

When you update a command in the future, follow these three steps:

1. Change the version comment at the top of the file. Bump the minor number for small changes (`v1.0` to `v1.1`) and the major number for breaking changes (`v1.1` to `v2.0`). A breaking change is anything that changes the output structure, renames a column, or changes the argument format.
2. Add a line to `CHANGELOG.md` with the date, the version, the file name, and a one-line description.
3. Tell the team. A Slack message or email with the version number and what changed.

Example: if you add a "subcategory breakdown" section to `/spend-analyze`, you would change the version comment to `<!-- v1.1 2026-05-10 Added subcategory breakdown table. -->` and add a changelog entry.

---

## Part C: Sharing the command library (5 minutes)

### Three ways to share

| Method | Best for | How it works |
|---|---|---|
| Git repository | Teams already using Git | Commit `.claude/commands/` to the repo. Team members pull updates. |
| Shared network folder | Teams using a shared drive or SharePoint | Copy `.claude/commands/` to the shared location. Team members copy into their project. |
| Zip file or email | One-time sharing with a colleague | Zip the `.claude/commands/` folder and send it. |

For Meridian Manufacturing, assume you are using a shared network folder. The pattern works the same regardless of method.

### Step 5: Package the commands for sharing

Create a summary of what the command library contains, so Priya knows what she is getting.

```
Read all six command files in .claude/commands/. For each one, list: the command name, the arguments it takes, a one-sentence description, and the output file name pattern. Format as a table.
```

You should see a table like this:

| Command | Arguments | Description | Output pattern |
|---|---|---|---|
| /spend-analyze | [period] [category] | Spend breakdown by supplier for a period and category. | spend-analysis-[period]-[category]-[date].md |
| /anomaly-detect | [threshold] [period] | Flags transactions above a threshold multiple and duplicate POs. | anomaly-report-[period]-[date].md |
| /scorecard-refresh | [supplier] [quarter] | One-page scorecard summary with trend for a single supplier. | scorecard-[supplier_id]-[quarter]-[date].md |
| /contract-sweep | [horizon-days] | Lists contracts expiring within the horizon with urgency tiers. | contract-sweep-[horizon]-days-[date].md |
| /rfp-launch | [category] [deadline] | Sourcing brief with spend, contracts, risk, and timeline. | rfp-brief-[category]-[date].md |
| /savings-update | [period] | Savings variance tracker comparing actuals to prorated targets. | savings-tracker-[period]-[date].md |

### Step 6: Test as Priya would

Simulate what happens when Priya runs your commands for her category. She manages logistics.

```
/spend-analyze Q1 logistics
```

You should see a spend analysis for the logistics category, with the same section structure as your direct-materials run from Lesson 2. The top suppliers will be different (logistics suppliers instead of direct-materials suppliers), but the format is identical. That is the point: same command, same shape, different data.

If the output is empty or shows zero spend, check that `logistics` (lowercase) matches the category values in `spend-transactions.csv`. It should.

### Step 7: Verify format consistency

Compare Priya's output to yours.

```
Compare the structure of the most recent spend-analysis file for logistics to the most recent spend-analysis file for direct-materials. Do they have the same sections, the same table columns, and the same audit footer format?
```

You should see that both files have: a Summary paragraph, a Top 10 suppliers table with the same columns (Rank, Supplier, Category, Tier, Spend, % of Total, vs Prior Period), a Flags section, and an audit footer. The numbers differ because the categories differ. The structure is identical.

This is what standardization looks like. Priya's report and your report sit side by side in the board deck. The CPO does not have to re-read a different format for each category.

---

## Part D: Governance ground rules (5 minutes)

### Step 8: Review the six rules for team command governance

These are not Claude Code features. They are team practices that keep the command library useful over time.

1. **One owner per command.** Each command file has one person responsible for updates. Put the owner's name in the version comment if your team is larger than three people. Example: `<!-- v1.0 2026-04-25 Initial. Owner: Jordan. -->`.

2. **No silent edits.** If you change a command, bump the version and update the changelog. If you do not, Priya's output will change without warning and she will not know why.

3. **Test before you share.** Run the command with at least two different argument sets before distributing an update. For `/spend-analyze`, that means testing with at least two categories and two periods.

4. **Keep arguments stable.** If `/spend-analyze` takes `[period] [category]`, do not change the order to `[category] [period]` in a future version. That breaks every team member's muscle memory. If you must change the argument order, bump the major version and send a migration note.

5. **Review quarterly.** Once per quarter, review the command library with the team. Remove commands nobody uses. Update thresholds that have drifted. Add new commands the team has requested.

6. **Document the data contract.** Each command lists its input files and the columns it reads. If someone changes the column names in `spend-transactions.csv` (for example, renaming `amount_usd` to `spend_usd`), every command that reads that column will break. The changelog should note data schema changes too.

---

## Worked example: Priya's first run

Here is the sequence Priya would follow to start using your command library.

**Step 1: Copy the commands into her project.**

Priya has her own project folder for logistics analysis. She copies your `.claude/commands/` folder into her project root.

```
cp -r /path/to/your/project/.claude/commands/ /path/to/priyas/project/.claude/commands/
```

**Folder layout after copy:**

```
priyas-logistics-project/
  data/
    spend-transactions.csv
    supplier-master.csv
    contract-register.csv
    scorecard-history.csv
  .claude/commands/
    spend-analyze.md
    anomaly-detect.md
    scorecard-refresh.md
    contract-sweep.md
    rfp-launch.md
    savings-update.md
    CHANGELOG.md
  outputs/
```

**What Priya should see:** The `.claude/commands/` folder in her project now contains six command files and a changelog.

**What happened, behind the scenes:**

1. Priya copied the entire `.claude/commands/` directory from the shared location into her project root.
2. Claude Code (in the terminal) automatically discovers command files in `.claude/commands/` when she opens her project folder.
3. No configuration is needed. Claude Code reads the directory on startup.
4. The commands reference relative paths (`data/spend-transactions.csv`), so they work in any project that has the same folder structure.

**Step 2: Priya runs her first command.**

```
/spend-analyze Q1 logistics
```

**What Priya should see:** A spend analysis saved to `outputs/spend-analysis-Q1-logistics-2026-04-25.md` with the same three sections (Summary, Top 10 suppliers, Flags) as every other spend analysis in the team.

**What Claude did, behind the scenes:**

1. Claude Code found `.claude/commands/spend-analyze.md` in Priya's project folder and replaced `$ARGUMENTS` with `Q1 logistics`.
2. It parsed the arguments: period = Q1 (2026-01-01 to 2026-03-31), category = logistics.
3. It read `data/spend-transactions.csv` from Priya's project folder and filtered to logistics transactions in Q1.
4. It joined with `data/supplier-master.csv` for tier and risk data.
5. It grouped by supplier, sorted by spend descending, and built the standard three-section output.
6. It saved the file with a datestamp and audit footer.

**The critical point:** Priya's data files have the same column names as yours. That is why the command works. If her `spend-transactions.csv` used different column headers, the command would fail. This is the "data contract" from rule 6 above.

---

## You are done with Course 4 when

Run through this checklist. Every item should be true.

1. Your `.claude/commands/` folder has six command files: `spend-analyze.md`, `anomaly-detect.md`, `scorecard-refresh.md`, `contract-sweep.md`, `rfp-launch.md`, and `savings-update.md`.
2. Each command file is between 30 and 70 lines.
3. Each command file starts with a version comment in the format `<!-- v1.0 YYYY-MM-DD Description. -->`.
4. A `CHANGELOG.md` file exists in `.claude/commands/` with an entry for each command.
5. You have run `/spend-analyze Q1 direct-materials` and produced a datestamped spend analysis in `outputs/`.
6. You have run `/anomaly-detect 2.5 Q1` and it found high-value transactions and duplicate PO patterns.
7. You have run `/scorecard-refresh SUP004 2026-Q1` and produced a scorecard summary.
8. You have run `/contract-sweep 90` and it listed contracts expiring within 90 days.
9. You have run `/rfp-launch direct-materials 2026-07-31` and produced a sourcing brief with baseline spend, expiring contracts, and a timeline.
10. You have run `/savings-update Q1` and produced a savings tracker with variance figures.
11. You can explain the difference between project-level commands (`.claude/commands/` in the project) and user-level commands (`~/.claude/commands/` in your home directory).
12. You can copy your `.claude/commands/` folder into a different project with the same data structure and run the same commands.

If all twelve are true, you have finished Course 4: The Command Engineer. You now have a reusable command library that any team member can run for any category, period, or supplier.

---

## Common mistakes and how to recover

**Symptom:** Priya copies the commands but gets "command not found" when she types `/spend-analyze`.
**Fix:** The commands folder must be at `.claude/commands/` relative to the project root where she opens Claude Code. If she placed the files in `commands/` without the `.claude/` parent, Claude Code will not find them. The correct path is `.claude/commands/spend-analyze.md`.

**Symptom:** Priya's output has different column names or missing sections compared to yours.
**Fix:** Check that both of you are running the same version of the command file. Compare the version comment at the top. If the versions differ, one of you has an older copy. Update from the shared source.

**Symptom:** The CHANGELOG.md file gets out of sync with the actual command versions.
**Fix:** This happens when someone edits a command and forgets to update the changelog. Add a team rule: every pull request or shared-folder update must include both the changed command file and a changelog entry. Review during your quarterly command library check.

**Symptom:** A command works in your project but fails in Priya's project with "file not found."
**Fix:** The command references a relative path like `data/spend-transactions.csv`. Priya's project must have the same folder structure: a `data/` folder at the project root with the same file names. If her data lives in a different location (for example, `raw-data/spend.csv`), she needs to either rename her folders to match or update the command file paths. Renaming folders is simpler and keeps the team on one standard.

**Symptom:** Two team members edit the same command file and overwrite each other's changes.
**Fix:** This is a merge conflict. If you use Git, Git handles it. If you use a shared folder, adopt the "one owner per command" rule from Part D. Only the owner edits the command file. Others submit change requests to the owner.
