# Solution: the category intelligence brief prompt

Reference answer for Lesson 6. This is the single prompt that produces three correctly scoped briefs when run from each of the three category folders.

## Where to save it

For convenience, save as a Markdown file at the practice root so you can copy-paste from it any time:

```
practice/category_brief_prompt.md
```

For Claude Code (terminal or Desktop) users with slash commands, save as:

```
.claude/commands/category-brief.md       (in your project root)
```

## The prompt

```
Build a category intelligence brief for this category.

Inputs (use the data files my CLAUDE.md points at):
- the master file (suppliers, carriers, or vendors),
- the activity file (orders, shipments, or invoices).

Action:

1. Top three by total spend over the last year. Sum the spend column
in the activity file, group by the master file's id column, sort
descending, take the top three.

2. One specific risk visible in the data. Pick the most concrete one:
- a supplier or carrier or vendor flagged at_risk in the master file,
- a contract ending within 90 days of today (2026-04-25),
- a row in the activity file that breaks a stated rule (in indirect,
  any invoice with amount_usd 25000 or above using manager_under_25k
  is a violation).

3. One recommended action. Name the owner, the action, the deadline.
Deadline must be within the next 30 days from today.

Output:

Save as category_brief.md in this folder.

Format:
- Title: Category brief - <category name>.
- Section 1: Top 3 by spend over the last year (a table with name,
  spend over the year, contract status, one-line note).
- Section 2: Risk (one paragraph naming the entity, the data point,
  which file).
- Section 3: Recommended action (one paragraph: owner, action, deadline).

Cap at 400 words excluding audit footer.

Add an audit footer at the bottom (separated from the body by a row
of three dashes) with these five lines:
- Generated: today's date and time.
- Source files: every file you actually read, by name.
- Model: the Claude model you are running.
- Operator: my name.
- Output: the path of the file you just saved.

Constraints:
- Use only files my CLAUDE.md points at.
- Do not name any entity not in those files. Do not invent figures.
  If a number is not in the source, write "not in source".
- Do not modify any data file.
```

## How to invoke it

From each category folder in turn:

```
cd practice/direct-materials
claude
```

Paste the prompt body. Wait 30 to 60 seconds while Claude aggregates 2,500 order rows. Read the output. Quit (`/quit`).

```
cd ../logistics
claude
```

Paste again. This time Claude aggregates 5,000 shipment rows. Quit.

```
cd ../indirect
claude
```

Paste once more. Claude aggregates 3,000 invoice rows AND finds the 18 violations.

Three runs. Three briefs. Same prompt.

## Why one prompt produces three different briefs

The prompt uses words like "the master file" and "the activity file" rather than naming a specific file. Claude resolves "the master file" to whichever file is named in the current folder's CLAUDE.md. In direct-materials, that is `suppliers.csv`. In logistics, `carriers.csv`. In indirect, `vendors.csv`. Same word, different file.

Same for "the activity file" (`orders.csv` vs `shipments.csv` vs `invoices.csv`).

This is the entire point of the CLAUDE.md hierarchy: one prompt, one command pattern, three correct outputs, with no manual switching. The folder you start in does the rest.

## What you should see in each brief

| Category | Top 3 by spend (likely) | Risk | Recommended action (likely) |
|---|---|---|---|
| Direct materials | Great Lakes Steel, Heartland Steel, Pacific Aluminum (or similar; the highest annual_value suppliers will dominate) | SUP004 Apex Electronics, contract ends 2026-05-31, 36 days from today | Engineering owner: complete supplier audit and qualify alternates by 2026-05-25 |
| Logistics | Globex Freight, Atlantic Lines, Eagle Air Freight (or similar; biggest road carriers dominate) | CAR004 ParcelPlus flagged at_risk, contract ends 2026-06-30 | Operations owner: corrective action plan with ParcelPlus by 2026-05-22 |
| Indirect | Helix Consulting, Bright Spark Energy, Apex Legal (or similar; biggest annual_value vendors) | 18 invoices over $25,000 that used manager_under_25k instead of cfo_over_25k. Plus VEN005 Prism Print at_risk. | Finance owner: investigate the 18 violations, remediation memo, by 2026-05-15 |
