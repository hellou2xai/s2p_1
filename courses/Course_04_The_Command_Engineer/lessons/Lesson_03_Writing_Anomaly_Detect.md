# Lesson 3: Writing /anomaly-detect

**Time:** 45 minutes

## The problem

It is 11:00 Wednesday. The CFO emails: "AP flagged some unusual invoices last week. Can you scan the last quarter for anything above normal?" You need a repeatable way to scan for outliers. Today you open a spreadsheet, sort by amount, squint at the top rows, and decide what looks "unusual." Tomorrow you forget the threshold you used. Next month, Priya runs her own scan with a different cutoff and gets a different count. Nobody agrees on what "anomaly" means because nobody wrote it down.

This lesson fixes that. You will write a slash command that defines "anomaly" once, accepts a configurable threshold, and produces a structured alert report every time.

## What Claude Code is going to do for you

By the end of this lesson, you will type `/anomaly-detect 2.5 Q1` in Claude Code (in the terminal) and get a report listing every transaction that exceeds 2.5 times the category average, plus every duplicate PO pattern. The threshold and period are parameters. Change them and the results change with them. The report format stays the same.

## Set up

Before you begin, confirm these three things:

1. You are in the `practice/` folder and Claude Code is installed.
2. You already have `.claude/commands/spend-analyze.md` from Lesson 2. If not, copy the solution: `cp ../solutions/spend_analyze_solution.md .claude/commands/spend-analyze.md`.
3. The `outputs/` folder exists.

## Step-by-step

### Step 1. Review what the command needs to do.

Open the solution file to see the finished product. Read it before you write your own:

```
cat ../solutions/anomaly_detect_solution.md
```

You should see a markdown file with five sections: Usage, Inputs, Process, Output format, and Quality criteria. Two detection types: high-value transactions (above threshold times category average) and duplicate PO patterns.

### Step 2. Create the command file.

Open a new file in your editor:

```
code .claude/commands/anomaly-detect.md
```

You should see a blank file in VS Code (or your default editor). If you prefer the terminal, you can use `nano .claude/commands/anomaly-detect.md` instead.

If you see "command not found" for `code`, open the file manually from your file explorer. The path is `.claude/commands/anomaly-detect.md` inside the `practice/` folder.

### Step 3. Write the Usage section.

Type the following into the file:

```markdown
# /anomaly-detect

Scan spend transactions for statistical outliers and suspicious patterns.

## Usage

/anomaly-detect $ARGUMENTS

Parse $ARGUMENTS as: [threshold] [period]
- threshold: a multiplier (e.g., 2.5 means flag transactions exceeding 2.5x the category average)
- period: Q1, Q2, Q3, Q4, H1, H2, or YTD (same date logic as /spend-analyze)
```

You should see eight lines in the file so far.

This is different from `/spend-analyze` in one important way. The first argument is a number, not a keyword. Claude Code needs to know that `2.5` is a threshold multiplier and `Q1` is a period. The description after each argument tells Claude how to interpret the value.

### Step 4. Write the Inputs section.

Add the following below the Usage section:

```markdown
## Inputs

data/spend-transactions.csv
  Filter rows by period. Compute category-level average amount_usd.

data/supplier-master.csv
  Join on supplier_id for tier, risk_rating, and status.
```

You should see two data files listed, each with a one-line description of what to do with it.

### Step 5. Write the Process section.

This is the core of the command. Add the following:

```markdown
## Process

1. Filter spend-transactions.csv by period.
2. Compute the average amount_usd per category across all filtered rows.
3. Flag every transaction where amount_usd exceeds (category average x threshold).
4. For each flagged transaction, note the transaction_id, date, supplier_name, category, amount_usd, and the category average.
5. Scan for duplicate PO patterns: group by po_number, flag any PO that appears more than once with different dates or amounts.
6. For each duplicate PO group, list all transactions sharing that PO number.
7. Sort flagged transactions by amount_usd descending.
8. Sort duplicate PO groups by total combined amount descending.
```

You should see eight numbered steps. Notice two separate detection methods: steps 2 through 4 handle high-value outliers, and steps 5 through 6 handle duplicate POs. These are the two most common AP fraud patterns in procurement.

### Step 6. Write the Output format section.

Add the following:

```markdown
## Output format

Save to outputs/anomaly-report-[period]-[YYYY-MM-DD].md

Four sections:
1. **Summary** (one paragraph): number of high-value flags, number of duplicate PO flags, total USD at risk.
2. **High-value transactions** (table): Transaction ID, Date, Supplier, Category, Amount (USD), Category Avg, Multiple. Capped at 20 rows.
3. **Duplicate PO patterns** (table): PO Number, Count, Transactions (IDs), Combined Amount (USD). Capped at 15 rows.
4. **Recommended actions** (three bullet points): the top three actions the procurement team should take, each naming a specific supplier or PO.

End with an audit footer.
```

You should see four output sections defined, plus an audit footer requirement.

Two things to notice. First, the "Multiple" column in the high-value table shows how many times above average each transaction is. This helps the reader prioritize: a 4.2x outlier is more urgent than a 2.6x outlier. Second, the recommended actions must name specific suppliers or PO numbers. Generic advice ("review large transactions") is not useful.

### Step 7. Write the Quality criteria section.

Add the following:

```markdown
## Quality criteria

- Every flagged transaction has amount_usd > (category average x threshold). No false flags.
- Duplicate PO groups have at least two transactions sharing the same po_number.
- Recommended actions name specific suppliers or PO numbers from the flagged data.
- The summary paragraph includes the exact count and total USD, not approximate language.
```

You should have a complete command file with five sections. Save the file.

### Step 8. Start Claude Code and test the command.

```
claude
```

You should see the Claude Code prompt with the `practice/` folder as the working directory.

### Step 9. Run the command with a broad scope first.

Start with YTD so you see the full set of planted anomalies across all categories:

```
/anomaly-detect 2.5 YTD
```

Claude Code reads `.claude/commands/anomaly-detect.md`, replaces `$ARGUMENTS` with `2.5 YTD`, filters spend-transactions.csv to all rows from January 1 through today, computes category averages, and flags outliers.

You should see a report with about 15 high-value flags and 12 duplicate PO groups. The total USD at risk will be in the hundreds of thousands. Claude saves the file to something like `outputs/anomaly-report-YTD-2026-04-25.md`.

If Claude finds zero flags, check two things. First, confirm the threshold is `2.5`, not `25`. Second, open the command file and make sure step 3 says "exceeds (category average x threshold)", not "exceeds threshold".

### Step 10. Now narrow the scope to Q1.

```
/anomaly-detect 2.5 Q1
```

You should see fewer results. Q1 2026 contains a subset of the planted anomalies. The report will show 2 high-value flags in the logistics category and a smaller set of duplicate PO groups. This is expected. The planted outliers are spread across the full year, so a single-quarter scan catches only the ones that fall in that period.

### Step 11. Change the threshold to see how it affects results.

```
/anomaly-detect 3.0 YTD
```

You should see the same 15 high-value flags or close to it. In this data set, the planted anomalies are well above the 3.0x threshold too, so the count stays similar. The point is that the threshold is now a parameter you can adjust without editing the command file.

If you set the threshold lower, say `1.5`, you would see many more flags, including legitimate transactions that happen to be above average. That is why 2.0 to 3.0 is the typical range for procurement anomaly detection.

### Step 12. Verify the output file.

Open the YTD report:

```
Read outputs/anomaly-report-YTD-2026-04-25.md
```

You should see four sections: Summary, High-value transactions table, Duplicate PO patterns table, and Recommended actions. Every flagged transaction should have an amount above 2.5 times its category average. Every duplicate PO group should have at least two transactions sharing the same PO number.

### Step 13. Exit Claude Code.

```
/exit
```

You are back at the terminal prompt.

## Worked example, end to end

**Starting files:**
- `data/spend-transactions.csv` (2,508 transaction rows, 12 months of spend data)
- `data/supplier-master.csv` (50 suppliers with tier, risk, and status data)
- `.claude/commands/anomaly-detect.md` (the command file you just wrote)

**Prompt typed:**

```
/anomaly-detect 2.5 YTD
```

**What Claude produced (extract):**

> **Summary.** Anomaly scan of YTD spend (2,508 transactions) at a 2.5x threshold flagged 15 high-value transactions totaling $1,282,749 and 12 duplicate PO patterns totaling $196,450. Total USD at risk: $1,479,199.
>
> | Transaction ID | Date | Supplier | Category | Amount (USD) | Category Avg | Multiple |
> |---|---|---|---|---|---|---|
> | TXN-00003 | 2025-06-01 | Great Lakes Steel | direct-materials | $173,616 | $29,145 | 5.96x |
> | TXN-00011 | 2025-10-03 | Apex Electronics | direct-materials | $149,098 | $29,145 | 5.12x |
> | ... | ... | ... | ... | ... | ... | ... |
>
> **Duplicate PO patterns:**
>
> | PO Number | Count | Transactions | Combined Amount (USD) |
> |---|---|---|---|
> | PO-774442 | 2 | TXN-01968, TXN-02506 | $46,784 |
> | ... | ... | ... | ... |

**Output file:** `outputs/anomaly-report-YTD-2026-04-25.md`

**What Claude did, behind the scenes:**

1. Found `anomaly-detect.md` in `.claude/commands/` and replaced `$ARGUMENTS` with `2.5 YTD`.
2. Parsed `2.5` as the threshold multiplier and `YTD` as January 1, 2026 through today (April 25, 2026).
3. Opened `data/spend-transactions.csv` and kept all rows in the YTD date range. Grouped those rows by `category` and computed the average `amount_usd` per category.
4. Scanned every row and flagged any transaction where `amount_usd` exceeded 2.5 times the category average. Recorded the transaction ID, date, supplier, category, amount, category average, and the multiple.
5. Grouped all rows by `po_number` and flagged any PO number appearing more than once with different dates or amounts.
6. Joined flagged suppliers to `data/supplier-master.csv` for tier and risk context.
7. Saved the result to `outputs/anomaly-report-YTD-2026-04-25.md` with four sections (Summary, High-value transactions, Duplicate PO patterns, and Recommended actions) plus an audit footer.

## Common mistakes and how to recover

**Symptom:** Claude flags hundreds of transactions, not 15.
**Fix:** Your threshold is too low or the Process section computes the average incorrectly. Open the command file and confirm step 3 says "amount_usd exceeds (category average x threshold)". A threshold of `2.5` means only transactions above 2.5 times the average get flagged. If you wrote "exceeds threshold" without the multiplication, Claude flags everything above $2.50.

**Symptom:** Claude finds zero duplicate PO patterns.
**Fix:** Check step 5 in the Process section. It should say "group by po_number, flag any PO that appears more than once." If you wrote "flag any PO with the same amount," Claude misses duplicates where the amount varies slightly (which is the common real-world pattern).

**Symptom:** The recommended actions are generic ("review flagged transactions").
**Fix:** Add wording to step 4 of the Output format: "each naming a specific supplier or PO." Claude follows explicit instructions. If you do not require specifics, it defaults to general advice.

**Symptom:** Claude asks which period format you mean.
**Fix:** Check the Usage section. Make sure it lists Q1, Q2, Q3, Q4, H1, H2, and YTD as valid periods. If you wrote "any period," Claude has to guess the format and may ask for clarification.

**Symptom:** The output file name has the wrong date or period.
**Fix:** Check the Output format section. The file name pattern should be `outputs/anomaly-report-[period]-[YYYY-MM-DD].md`. If `[period]` is missing, Claude uses its own naming convention, which may not match your other output files.

---

**Next:** In Lesson 4, you will write two commands in one session: `/scorecard-refresh` for supplier performance summaries and `/contract-sweep` for contract expiry alerts. You will learn how to parse multiple parameters from `$ARGUMENTS` and handle supplier name versus ID lookup.
