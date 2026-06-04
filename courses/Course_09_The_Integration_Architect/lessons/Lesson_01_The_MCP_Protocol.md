# Lesson 1: The MCP Protocol

**Time:** 25 minutes.

## A Tuesday morning without live data

It is 09:15. Your VP of Procurement asks: "What is our open PO exposure with Northwind Logistics right now?" You open Claude Code. You paste in a CSV from last week's ERP export. Claude answers, but the numbers are seven days old. The VP frowns. "I need current data."

The gap is clear. Claude Code can read files on your laptop, but it cannot reach into a database, an API, or an ERP on its own. It has no built-in connector to your procurement systems. Every time you want current data, you export, save, and paste. That loop costs you 10 to 15 minutes per query, and the answer is always stale by the time you read it.

## What Claude Code is going to do for you

The Model Context Protocol (MCP) closes that gap. MCP is an open standard that lets Claude Code discover and call external tools at runtime. A tool might query a database, call an API, or read from a live dashboard. Claude Code does not need to know the details in advance. It discovers what tools are available, reads their descriptions, and calls the right one when your prompt matches.

By the end of this lesson, you will understand how MCP works, what a tool schema looks like, and how Claude Code decides which tool to call.

## Set up

1. Open a terminal and navigate to the course folder:

```
cd "Course_09_The_Integration_Architect/practice"
```

2. Confirm the practice folder contents:

```
ls
```

You should see `procurement.db`, `supplier-master.csv`, and a `CLAUDE.md` file.

3. Start Claude Code:

```
claude
```

You should see the Claude Code prompt appear.

**Folder layout:**

```
Course_09_The_Integration_Architect/
├── practice/
│   ├── CLAUDE.md
│   ├── procurement.db
│   └── supplier-master.csv
├── lessons/
├── solutions/
└── scripts/
```

## Step-by-step

### Step 1: Ask Claude what MCP is

Type this prompt:

```
Explain in three sentences what the Model Context Protocol is and why a procurement team would use it.
```

**What you should see.** Claude explains that MCP is a standard for exposing external tools to AI assistants. It lets Claude call functions (like database queries) without you exporting data first. A procurement team uses it to get live answers from supplier databases, contract systems, or spend cubes.

### Step 2: Ask Claude what tools it can see right now

Type:

```
What MCP tools do you currently have access to?
```

**What you should see.** Claude lists whatever tools are registered in your settings. If you have not connected any MCP server yet, Claude says it has no MCP tools available. That is expected. You will connect one in Lesson 2.

### Step 3: Understand a tool schema

A tool schema tells Claude three things: the tool's name, what it does, and what inputs it expects. Here is an example schema for a procurement tool:

```json
{
  "name": "get_supplier_spend",
  "description": "Returns total spend for a given supplier over a date range.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "supplier_name": {
        "type": "string",
        "description": "Legal name of the supplier."
      },
      "start_date": {
        "type": "string",
        "description": "Start date in YYYY-MM-DD format."
      },
      "end_date": {
        "type": "string",
        "description": "End date in YYYY-MM-DD format."
      }
    },
    "required": ["supplier_name"]
  }
}
```

Type this prompt to Claude:

```
I am going to paste a JSON tool schema. Tell me: what is the tool's name, what does it do, and which input is required? Here is the schema: {"name": "get_supplier_spend", "description": "Returns total spend for a given supplier over a date range.", "inputSchema": {"type": "object", "properties": {"supplier_name": {"type": "string"}, "start_date": {"type": "string"}, "end_date": {"type": "string"}}, "required": ["supplier_name"]}}
```

**What you should see.** Claude responds that the tool is called `get_supplier_spend`, it returns spend for a supplier over a date range, and only `supplier_name` is required. The date fields are optional.

### Step 4: How Claude decides which tool to call

Type:

```
If you had two tools available, get_supplier_spend and get_open_pos, and I asked "How much have we spent with Northwind this quarter?", which tool would you call and why?
```

**What you should see.** Claude says it would call `get_supplier_spend` because the question is about spend, not open purchase orders. It matches the user's intent to the tool description.

### Step 5: Quit Claude

```
/quit
```

## Worked example: mapping a procurement question to a tool

**Scenario.** You are a category manager at Nexus Procurement Hub. Your VP asks: "Do we have any open POs with Globex SA that are overdue?"

**The prompt you would type (once MCP tools are connected):**

```
Check for any open POs with Globex SA that are past their delivery date.
```

**What Claude does behind the scenes:**

1. Claude reads the list of available MCP tools.
2. It finds `get_open_pos`, whose description says "Returns open purchase orders filtered by supplier and status."
3. It calls `get_open_pos` with `supplier_name: "Globex SA"`.
4. The MCP server queries `procurement.db`, filters the `open_pos` table for Globex SA, and returns 3 rows where `delivery_date < today`.
5. Claude formats the result as a table with PO number, line item, amount, and days overdue.
6. You see the answer in your terminal. No CSV export. No stale data.

**What you should see:**

A table showing 3 overdue POs for Globex SA, with amounts totaling $47,200 and the oldest being 12 days past due.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Claude says "I have no MCP tools available." | You have not registered an MCP server yet. That is normal for Lesson 1. You will do this in Lesson 2. |
| Claude calls the wrong tool for your question. | The tool descriptions may be vague. Write clearer descriptions in the tool schema. A description like "Returns spend data" is weaker than "Returns total spend in USD for a named supplier over a date range." |
| Claude invents a tool that does not exist. | Claude may hallucinate tool names if none are registered. Always verify tool availability with "What MCP tools do you have?" before relying on a response. |
| You see a JSON parsing error when pasting the schema. | Make sure the JSON is on one line with no trailing commas. Copy the exact block from this lesson. |

## You are done with Lesson 1 when

- You can explain MCP in one sentence: "MCP lets Claude Code discover and call external tools like database queries at runtime."
- You can read a tool schema and name the required inputs.
- You understand that Claude matches your question to a tool by reading the tool's description.

Move to Lesson 2 when ready.
