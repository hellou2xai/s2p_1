# Lesson 6: One prompt, three briefs

**Time:** 45 minutes. **You need:** Lessons 1 to 5 complete; the test from Lesson 4 passes.

## A typical Friday morning

It is 09:00 Friday. The CPO's deadline is end of day. You have built the file stack across the week. Now you cash in: write **one** Claude prompt, run it from each of three folders, and end up with **three** category briefs that name the right suppliers, the right risks, and the right owners. The briefs come out correctly scoped because of the work you did in Lessons 2 to 5.

## What "correctly scoped" means

After this lesson, you should have three files:

- `direct-materials/category_brief.md` (mentions only direct-materials suppliers)
- `logistics/category_brief.md` (mentions only carriers)
- `indirect/category_brief.md` (mentions only vendors)

All three have the same shape (three sections in the same order), but the content is entirely different. No carrier appears in the direct-materials brief. No vendor appears in the logistics brief.

## The brief format

Each brief has three short sections:

1. **Top three by spend over the last year.** A small table: name, spend, contract status, one-line note.
2. **One specific risk.** A short paragraph naming the supplier or carrier or vendor at risk, the data point that proves it, and which file the data came from.
3. **One recommended action.** Owner, action, deadline. One paragraph.

Plus an audit footer at the bottom (timestamp, source files, model, your name).

Cap the whole brief at 400 words.

## Save the prompt as a file you can reuse

**Step 1.** Open your terminal.

**Step 2.** Move to the practice folder:

```
cd "Course_02_The_Context_Architect/practice"
```

**The folder layout for this lesson.**

```
practice/
├── CLAUDE.md                        (global, from Lesson 2)
├── category_brief_prompt.md         (you create this in Step 3)
├── direct-materials/
│   ├── CLAUDE.md                    (category file, refined in Lesson 5)
│   ├── category_brief.md            (output, created by Claude)
│   ├── orders.csv
│   └── suppliers.csv
├── logistics/
│   ├── CLAUDE.md
│   ├── category_brief.md            (output)
│   ├── carriers.csv
│   └── shipments.csv
└── indirect/
    ├── CLAUDE.md
    ├── category_brief.md            (output)
    ├── invoices.csv
    └── vendors.csv
```

**Step 3.** In your text editor, create a new file at `practice/category_brief_prompt.md`. Paste this content:

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

**Step 4.** Save.

The key word is **"the master file"** and **"the activity file"**. Those phrases let one prompt work in three folders. In direct-materials, "the master file" is suppliers.csv. In logistics, it is carriers.csv. In indirect, it is vendors.csv. Same word, different file.

## Run it three times

**Step 5.** Move to the direct-materials folder:

```
cd direct-materials
```

**Step 6.** Start Claude:

```
claude
```

**Step 7.** Open `practice/category_brief_prompt.md` in your editor. Copy the entire prompt body. Paste into Claude. Press Enter.

Wait. Claude is now reading 50 supplier rows and 2,500 order rows, computing the year's spend by supplier, and writing a 400-word brief. This takes 30 to 60 seconds.

**What you should see.** A 400-word brief at `direct-materials/category_brief.md` with:
- **Top 3 by spend:** the three biggest suppliers by total spend across 2,500 orders. Great Lakes Steel, Heartland Steel, and Pacific Aluminum are likely candidates because they have the highest annual values and most orders.
- **Risk:** SUP004 Apex Electronics flagged at_risk. Contract ends 2026-05-31, which is about 36 days from today.
- **Recommended action:** an engineering owner, a sourcing decision, deadline before 2026-05-25.
- Audit footer at the bottom with timestamp, source files (suppliers.csv, orders.csv), model, your name.

**Step 8.** Open the brief file (`direct-materials/category_brief.md`) in your editor. Read it. Sanity-check one figure: pick the top supplier and check that the spend figure is plausible by glancing at orders.csv (sort by total_usd descending in Excel, eyeball the rows for that supplier).

**Step 9.** Quit Claude (`/quit`). Move to logistics:

```
cd ../logistics
```

**Step 10.** Start Claude. Paste the same prompt.

**What you should see.** A brief at `logistics/category_brief.md`:
- **Top 3 by spend:** Globex Freight (the biggest road carrier by far), Atlantic Lines (sea), and Eagle Air Freight (or another large one), based on summing 5,000 shipments.
- **Risk:** CAR004 ParcelPlus flagged at_risk. Contract ends 2026-06-30.
- **Recommended action:** an operations owner, a corrective action plan, deadline before 2026-05-25.

**Step 11.** Quit. Move to indirect:

```
cd ../indirect
```

**Step 12.** Start Claude. Paste the same prompt.

**What you should see.** A brief at `indirect/category_brief.md`:
- **Top 3 by spend:** Helix Consulting, Bright Spark Energy, Apex Legal, or similar (the largest annual_value vendors will have the most invoices).
- **Risk:** the 18 policy violations in invoices.csv where amount_usd is 25,000 or more but approval_path is manager_under_25k. The brief should name a specific example (one invoice number) and total the violations across the year. Plus VEN005 Prism Print flagged at_risk.
- **Recommended action:** finance owner, investigate the 18 violations, remediation memo, deadline 2026-05-15.

## Compare your three briefs side by side

**Step 13.** Open all three brief files. Confirm:

1. Same shape (three sections in the same order).
2. No entity from one category appears in another category's brief.
3. Each brief mentions a real entity from the right CSV. Nothing invented.
4. Each brief has the audit footer at the bottom.
5. Each brief is under 400 words excluding the footer.

If all five are true, you have just done what would have taken three hours of context-switching and three different prompts. You did it with one prompt and two `cd` commands.

## What Claude did, behind the scenes

Each of the three runs followed the same sequence:

1. Claude loaded the global (practice/CLAUDE.md) and the relevant category file at session start. The global provided writing rules and folder rules. The category file provided the scope, the data file names, and the category-specific rules.
2. Claude resolved the prompt's words "the master file" and "the activity file" to whichever files the category CLAUDE.md named. In direct-materials, that was suppliers.csv and orders.csv. In logistics, carriers.csv and shipments.csv. In indirect, vendors.csv and invoices.csv.
3. Claude read the activity file (thousands of rows), summed the spend column by entity ID, sorted descending, and took the top three for Section 1 of the brief.
4. Claude joined entity IDs back to names from the master file (suppliers.csv, carriers.csv, or vendors.csv).
5. For the risk section, Claude checked the master file for any entity flagged at_risk and computed days until contract_end against today (2026-04-25). In indirect, Claude also scanned invoices.csv for the $25,000 approval violations and found 18.
6. Claude wrote one recommended action with an owner, a verb, and a deadline within 30 days.
7. Claude saved the brief as category_brief.md in the current folder, added the audit footer, and did not modify any source CSV.

The result: one command, three correct outputs, drawn from 10,500 rows of data. The folder you start in does the rest.

## Three things that trip beginners up

- **The direct-materials brief mentions a carrier or vendor.** You forgot to restart Claude after the previous session. Quit, `cd` again, restart.
- **The figures look wrong.** Claude may have summarized rather than fully computed. Re-run the prompt with the constraint added: "Compute by sum across all rows, not by sample." That forces a full pass.
- **Claude invented a supplier name.** The constraint "do not name any entity not in those files" was missing or ignored. Re-paste the prompt with the constraint visible, and quit-and-restart.

## You are done with Course 2 when

- Three brief files exist, one per category folder.
- Each brief has three sections plus the audit footer.
- The direct-materials brief mentions only SUP-prefixed codes; the logistics brief mentions only CAR-prefixed codes; the indirect brief mentions only VEN-prefixed codes.
- All three briefs came from the same prompt run from three different folders.
- You can copy this whole pattern into your real procurement folder and replace the data with your own.

That is the entire course. Well done. Move to Course 3 (The Skill Builder) when you are ready; what you built here is the foundation for every course that follows.
