# Lesson 6: MCP Plus Skills for Live Spend Analysis

**Time:** 30 minutes.

## The data arrives, but the analysis does not

It is 15:00 on Friday. Your MCP server pulls live spend data in seconds. But your VP does not want raw numbers. She wants a spend variance analysis: this quarter versus last quarter, by category, with a flag on anything that moved more than 10%. Right now, you get the data from MCP, then manually write the analysis prompt every time. You repeat the same analytical steps each Friday. That is a skill waiting to be saved.

## What Claude Code is going to do for you

In this lesson, you combine MCP (live data retrieval) with a saved skill (consistent analytical steps). The skill tells Claude how to analyze the data. The MCP tools fetch the data. Together, they produce a repeatable spend variance report without you writing the analysis prompt from scratch each time.

## Set up

1. Navigate to the practice folder:

```
cd "Course_09_The_Integration_Architect/practice"
```

2. Confirm you have a `.claude/skills` directory. If not, create it:

```
mkdir -p .claude/skills
```

3. Start Claude Code:

```
claude
```

4. Verify MCP tools are still connected:

```
What MCP tools do you have access to?
```

You should see your three procurement tools.

**Folder layout:**

```
practice/
├── CLAUDE.md
├── procurement.db
├── .claude/
│   ├── settings.json
│   └── skills/
└── scripts/
    └── procurement_mcp_server.py
```

## Step-by-step

### Step 1: Define the analysis steps in a skill

```
Create a skill file at .claude/skills/spend-variance-analysis.md with this content: "When asked for a spend variance analysis: 1) Use get_supplier_spend to pull current quarter spend for each supplier in the supplier-master.csv. 2) Use get_supplier_spend again with the previous quarter date range. 3) Calculate the dollar and percentage change for each supplier. 4) Flag any supplier where the absolute percentage change exceeds 10%. 5) Sort by absolute dollar change, descending. 6) Output a markdown table with columns: Supplier, Prior Quarter, Current Quarter, Dollar Change, Percent Change, Flag."
```

**What you should see.** Claude creates the file `.claude/skills/spend-variance-analysis.md` with the six-step analysis process.

### Step 2: Run the skill with live data

```
Run a spend variance analysis for Q1 2026 versus Q4 2025.
```

**What you should see.** Claude reads the skill file, then calls `get_supplier_spend` for each supplier in two date ranges. It calculates variances and outputs a markdown table. Suppliers with changes over 10% are flagged with "YES" in the Flag column.

### Step 3: Verify the numbers

```
Show me the raw spend data you pulled for Northwind Logistics in Q1 2026 and Q4 2025, before the variance calculation.
```

**What you should see.** Claude shows the two dollar amounts it got from the MCP tool. You can compare them to the variance row in the table above to confirm the math is correct.

### Step 4: Add a narrative summary skill

```
Create a second skill file at .claude/skills/variance-narrative.md with this content: "After producing a spend variance table, write a three-sentence executive summary. Name the supplier with the largest dollar increase, the supplier with the largest dollar decrease, and the total number of flagged suppliers. Use active voice. Never use vague qualifiers like 'large savings' or 'notable reduction'. Always state the exact dollar figure and percentage."
```

**What you should see.** Claude creates the second skill file.

### Step 5: Run both skills together

```
Run a spend variance analysis for Q1 2026 versus Q4 2025. Then write the executive narrative summary.
```

**What you should see.** First, the variance table appears. Then Claude writes three sentences: "Acme Industrial saw the largest spend increase at $42,300 (14.2%). Northwind Logistics had the largest decrease at $28,100 (9.8%). Four of twelve suppliers are flagged for changes exceeding 10%."

### Step 6: Save the output to a file

```
Save the variance table and the narrative summary to Drafts/spend_variance_Q1_2026.md.
```

**What you should see.** Claude creates the file in the Drafts folder. The file contains both the table and the narrative.

### Step 7: Quit Claude

```
/quit
```

## Worked example: the Friday spend report

**Scenario.** Every Friday at 15:30, you produce a spend variance report for the VP. Before today, this took 40 minutes: export from ERP, build a pivot table, write the narrative, email it. Now it takes under 2 minutes.

**The prompt you type:**

```
Run a spend variance analysis for Q1 2026 versus Q4 2025. Include the executive narrative. Save to Drafts/spend_variance_Q1_2026.md.
```

**Folder layout:**

```
practice/
├── CLAUDE.md
├── procurement.db
├── supplier-master.csv
├── Drafts/
│   └── spend_variance_Q1_2026.md    (output goes here)
├── .claude/
│   ├── settings.json
│   └── skills/
│       ├── spend-variance-analysis.md
│       └── variance-narrative.md
└── scripts/
    └── procurement_mcp_server.py
```

**What you should see:**

A file at `Drafts/spend_variance_Q1_2026.md` containing a markdown table with 12 supplier rows and a three-sentence summary naming specific suppliers, dollar figures, and flag counts.

**What Claude did behind the scenes:**

1. Claude loaded the two skill files at session start.
2. Your prompt triggered the spend-variance-analysis skill.
3. Claude read `supplier-master.csv` to get the list of supplier names.
4. It called `get_supplier_spend` 24 times (12 suppliers, 2 quarters each).
5. It calculated dollar and percentage changes, flagging any over 10%.
6. It sorted by absolute dollar change and built the markdown table.
7. It then triggered the variance-narrative skill and wrote three sentences using the exact figures from the table.
8. It saved the combined output to `Drafts/spend_variance_Q1_2026.md`.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Claude does not find the skill files. | Check that the files are in `.claude/skills/`, not in a different folder. Skill files must be in that exact directory for Claude Code to load them. |
| The variance table has blank cells. | The MCP tool returned no data for that supplier and quarter. Check whether the supplier name in `supplier-master.csv` matches the `spend` table exactly. |
| Claude writes a vague phrase instead of a dollar figure. | Your narrative skill file needs to be explicit: "Always state the exact dollar figure and percentage. Never use vague qualifiers." Add that line if it is missing. |
| The skill runs but ignores the date range you specified. | Your skill file may not reference the date parameters. Update the skill to say: "Use the date range specified in the user's prompt for current quarter, and the three months before it for prior quarter." |
| Claude calls the MCP tool 50 times and the response is slow. | Twelve suppliers with two calls each is 24 calls. If you have more suppliers, consider modifying the MCP tool to accept a list of supplier names in one call. That reduces the round trips. |

## You are done with Lesson 6 when

- You have two skill files: one for the analysis steps, one for the narrative summary.
- You ran a spend variance analysis that pulled live data through MCP and applied the skills.
- The output includes a table with real numbers and a narrative with named suppliers and dollar figures.
- The output is saved to a file in the Drafts folder.

This completes Course 9. You now know how to connect Claude Code to external data through MCP, build tools, secure them, and combine them with skills for repeatable analysis.
