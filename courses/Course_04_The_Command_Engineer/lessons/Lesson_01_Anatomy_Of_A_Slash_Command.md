# Lesson 1: Anatomy of a Custom Slash Command

**Time:** 25 minutes

## The problem

It is 08:45 on the first Monday of the month. Your CPO Slacks you: "Need the monthly spend breakdown for direct materials. Same as last month. By noon."

You open Claude Code in the terminal. You start typing a prompt from memory. Halfway through, you stop. What threshold did you use last month? Was it top 10 or top 15 suppliers? Did you compare to Q4 or to the same quarter last year? You scroll through your chat history looking for last month's prompt. You find it, but it was slightly different from the month before that. Your output format keeps drifting.

Your colleague Priya runs the same analysis for her categories. Her output looks nothing like yours. Same data, same intent, different prompts, different results.

This lesson introduces the fix: a **custom slash command**. One markdown file, saved once, reused every month by every analyst on the team.

## What Claude Code is going to do for you

By the end of this lesson, you will run a single line in Claude Code (in the terminal) and produce a standardized spend analysis for any period and category. The command reads the same data files, applies the same logic, and saves a datestamped output file every time. No prompt from memory. No format drift.

## Set up

Before you begin, confirm these four things:

1. Claude Code is installed and signed in. You can type `claude` in your terminal and see the Claude Code prompt.
2. You have the Course 4 practice folder on your machine. The path ends with `Course_04_The_Command_Engineer/practice/`.
3. Inside that folder you can see `data/`, `.claude/commands/`, and `outputs/`.
4. The `data/` folder holds four CSV files: `spend-transactions.csv`, `supplier-master.csv`, `contract-register.csv`, and `scorecard-history.csv`.

If any of those are missing, run the regenerator script in `scripts/build_course_data.py` from the course root before continuing.

## Step-by-step

### Step 1. Open your terminal and navigate to the practice folder.

```
cd "Course_04_The_Command_Engineer/practice"
```

You should see the practice folder path in your terminal prompt.

If you see "No such file or directory," check your starting location. You need to be inside the course root, or use the full path to the practice folder on your machine.

### Step 2. Check that the commands folder exists.

```
ls .claude/commands/
```

You should see `README.md` and nothing else. The folder is empty because you have not built any commands yet.

If you see "No such file or directory," create the path:

```
mkdir -p .claude/commands
```

### Step 3. Look at the solution file for spend-analyze.

Before you write your own command, look at what a finished command looks like. Open the solution file in your editor or read it in the terminal:

```
cat ../solutions/spend_analyze_solution.md
```

You should see a markdown file with five sections: Usage, Inputs, Process, Output format, and Quality criteria. This is the anatomy of a slash command. Every command you build in this course follows this same five-section structure.

### Step 4. Copy the solution into your commands folder.

For this first lesson, you will use the pre-built solution so you can see a command in action before writing one yourself. Copy the solution file into `.claude/commands/` with the correct name:

```
cp ../solutions/spend_analyze_solution.md .claude/commands/spend-analyze.md
```

You should see no output (a silent copy means success).

If you see "Permission denied," check that you are inside the `practice/` folder, not the course root.

### Step 5. Confirm the command file is in place.

```
ls .claude/commands/
```

You should see two files: `README.md` and `spend-analyze.md`.

### Step 6. Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt. The working directory shown at the top should be the `practice/` folder.

If Claude Code does not start, confirm it is installed with `claude --version`. If that fails, revisit Course 1, Lesson 1 for installation steps.

### Step 7. Run the spend-analyze command.

Type the following at the Claude Code prompt:

```
/spend-analyze Q1 direct-materials
```

Claude Code finds `.claude/commands/spend-analyze.md`, reads the instructions, and replaces every `$ARGUMENTS` with `Q1 direct-materials`. It then reads `data/spend-transactions.csv`, filters to Q1 2026 and the direct-materials category, groups by supplier, computes totals and period-over-period changes, and saves a datestamped file to `outputs/`.

You should see Claude produce a spend analysis with three sections: a Summary paragraph, a Top 10 suppliers table, and a Flags section. Claude will also confirm the output file name, something like `outputs/spend-analysis-Q1-direct-materials-2026-04-25.md`.

If Claude asks "Which command do you mean?" or shows no results, check that the file is named exactly `spend-analyze.md` (with a hyphen, not an underscore) and that it lives in `.claude/commands/`, not in `.claude/` or the project root.

### Step 8. Check the output file.

Open the output file Claude just created:

```
Read outputs/spend-analysis-Q1-direct-materials-2026-04-25.md
```

You should see a markdown file with the Summary, Top 10, and Flags sections. Every figure traces back to `spend-transactions.csv`. The file ends with an audit footer listing the date, source files, model, and operator.

### Step 9. Run the command again with different arguments.

Try a different period and category:

```
/spend-analyze Q4 all
```

Claude reads the same command file but this time replaces `$ARGUMENTS` with `Q4 all`. It filters to Q4 2025 across all categories and produces a new output file.

You should see a second spend analysis with category-level subtotals (because you passed `all`). The output file is named something like `outputs/spend-analysis-Q4-all-2026-04-25.md`.

### Step 10. Exit Claude Code.

```
/exit
```

You are back at the terminal prompt.

## How a slash command works, behind the scenes

Here is what happened when you typed `/spend-analyze Q1 direct-materials`:

1. Claude Code looked inside `.claude/commands/` for a file named `spend-analyze.md`.
2. It read the entire file as a prompt. Every instance of `$ARGUMENTS` was replaced with `Q1 direct-materials`.
3. The Usage section told Claude how to parse `Q1 direct-materials` into two parameters: period = Q1, category = direct-materials.
4. The Inputs section told Claude which CSV files to read and how to filter them.
5. The Process section gave Claude the exact steps: filter, group, sum, sort, compare to prior period, flag outliers.
6. The Output format section told Claude the file name pattern and the three-section layout.
7. The Quality criteria section told Claude to check its own work: every figure must trace to the CSV, the table must have exactly 10 rows, the file name must include the date.

The command file is just a prompt. But because it is saved as a file, it runs the same way every time. No memory required. No drift.

## The five sections of a command file

Every command file in this course follows the same structure:

| Section | What it does |
|---|---|
| **Usage** | Shows the command name, `$ARGUMENTS` placeholder, and how to parse the arguments into named parameters. |
| **Inputs** | Lists the data files to read and how to filter them. |
| **Process** | Numbered steps Claude follows: filter, group, compute, compare, flag. |
| **Output format** | The file name pattern, the section layout, and the audit footer. |
| **Quality criteria** | Self-check rules so Claude validates its own output before saving. |

You will write all five sections yourself in Lesson 2.

## Worked example, end to end

**Starting files:**
- `data/spend-transactions.csv` (2,508 transaction rows, 12 months of spend data)
- `data/supplier-master.csv` (50 suppliers with tier and risk data)
- `.claude/commands/spend-analyze.md` (the command file you copied from solutions)

**Prompt typed:**

```
/spend-analyze Q1 direct-materials
```

**What Claude produced (extract):**

> **Summary.** Meridian Manufacturing spent $5,842,319 across 127 transactions on direct materials in Q1 2026. This is a 6.3% increase from Q4 2025 ($5,496,210 across 118 transactions).
>
> | Rank | Supplier | Category | Tier | Spend (USD) | % of Total | vs Prior |
> |---|---|---|---|---|---|---|
> | 1 | Great Lakes Steel | direct-materials | strategic | $1,045,200 | 17.9% | +4.2% |
> | 2 | Heartland Polymers | direct-materials | strategic | $923,400 | 15.8% | +8.1% |
> | ... | ... | ... | ... | ... | ... | ... |

**Output file:** `outputs/spend-analysis-Q1-direct-materials-2026-04-25.md`

**What Claude did, behind the scenes:**

1. Found `spend-analyze.md` in `.claude/commands/` and replaced `$ARGUMENTS` with `Q1 direct-materials`.
2. Parsed `Q1` as January 1 to March 31, 2026. Parsed `direct-materials` as the category filter.
3. Opened `data/spend-transactions.csv` and filtered to rows where the date fell in Q1 2026 and the category was `direct-materials`.
4. Grouped the filtered rows by `supplier_id`, summed `amount_usd`, and sorted descending.
5. Opened `data/supplier-master.csv` and joined on `supplier_id` to pull `tier` and `risk_rating` for each supplier.
6. Computed the prior period (Q4 2025), filtered the same CSV for that period, and calculated period-over-period change for each supplier.
7. Saved the result to `outputs/spend-analysis-Q1-direct-materials-2026-04-25.md` with the Summary, Top 10, and Flags sections, plus an audit footer.

## Common mistakes and how to recover

**Symptom:** You type `/spend-analyze` and Claude says it cannot find the command.
**Fix:** Check that the file is named `spend-analyze.md` (hyphen, not underscore) and sits inside `.claude/commands/`, not `.claude/` or the project root. The file name before `.md` must match what you type after the slash.

**Symptom:** Claude produces output but the numbers look wrong or the table is empty.
**Fix:** Check the period argument. `Q1` maps to January through March of the current year (2026). If your data does not cover that range, try `Q4` (which maps to Q4 2025) or `YTD`. Open `data/spend-transactions.csv` and confirm there are rows in the date range you requested.

**Symptom:** Claude asks you to confirm which file to save to, instead of saving automatically.
**Fix:** The Output format section in the command file should specify the exact file name pattern. Open `.claude/commands/spend-analyze.md` and confirm the Output format section includes `Save to outputs/spend-analysis-[period]-[category]-[YYYY-MM-DD].md`.

**Symptom:** The output file appears in the project root instead of in `outputs/`.
**Fix:** Make sure the command file says `outputs/` in the file path, and confirm the `outputs/` folder exists. If it does not exist, create it with `mkdir outputs` and run the command again.

**Symptom:** You see two commands with similar names and Claude picks the wrong one.
**Fix:** Each command file must have a unique name. Check `.claude/commands/` for duplicates. Remove any file you did not intend to keep. File names are case-sensitive on macOS and Linux but not on Windows, so avoid names that differ only in case.

---

**Next:** In Lesson 2, you will delete the copied solution and write `spend-analyze.md` from scratch. You will learn to write each of the five sections and test the command with multiple argument combinations.
