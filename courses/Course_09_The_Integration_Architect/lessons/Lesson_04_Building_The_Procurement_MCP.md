# Lesson 4: Building the Procurement MCP Server

**Time:** 30 minutes.

## Three questions your VP asks every week

It is 14:00 on a Wednesday. Your VP of Procurement has three standing questions: "What did we spend with each top supplier last quarter?" "What open POs are at risk of being late?" "Is the Globex contract still active?" Right now, answering each one means an ERP export, a pivot table, and a Slack message. In this lesson, you build three MCP tools that answer all three questions in seconds.

## What Claude Code is going to do for you

You will write (with Claude's help) a complete MCP server with three tools: `get_supplier_spend`, `get_open_pos`, and `get_contract_status`. Each tool queries `procurement.db` and returns structured data. Once registered, Claude Code can answer your VP's questions by calling the right tool automatically.

## Set up

1. Navigate to the practice folder:

```
cd "Course_09_The_Integration_Architect/practice"
```

2. Confirm `procurement.db` exists:

```
ls procurement.db
```

You should see the file listed.

3. Start Claude Code:

```
claude
```

**Folder layout:**

```
practice/
├── CLAUDE.md
├── procurement.db
├── supplier-master.csv
├── scripts/
│   └── procurement_mcp_server.py
└── .claude/
    └── settings.json
```

## Step-by-step

### Step 1: Ask Claude to scaffold the server

```
Create a new file called scripts/procurement_mcp_server.py using FastMCP. The server name should be "procurement". It should connect to procurement.db using sqlite3. Add three tool stubs: get_supplier_spend, get_open_pos, and get_contract_status. Each stub should return "Not implemented yet." Include the FastMCP import, the server creation, and the if __name__ block.
```

**What you should see.** Claude creates the file with the FastMCP import, three decorated functions, and a main block. Each function returns a placeholder string.

### Step 2: Build the get_supplier_spend tool

```
Update get_supplier_spend in scripts/procurement_mcp_server.py. It should accept supplier_name (required), start_date (optional), and end_date (optional). Query the spend table in procurement.db for rows matching the supplier name. If dates are provided, filter by transaction_date. Return a JSON string with total_spend, transaction_count, and supplier_name.
```

**What you should see.** Claude rewrites the function with a parameterized SQL query, date filtering, and a `json.dumps()` return.

### Step 3: Build the get_open_pos tool

```
Update get_open_pos in scripts/procurement_mcp_server.py. It should accept supplier_name (optional) and min_amount (optional, default 0). Query the open_pos table for POs where status is "open". If supplier_name is provided, filter by it. If min_amount is provided, filter where amount >= min_amount. Return a JSON string with a list of POs, each having po_number, supplier_name, amount, order_date, and delivery_date.
```

**What you should see.** Claude adds the function with conditional WHERE clauses and returns a JSON list.

### Step 4: Build the get_contract_status tool

```
Update get_contract_status in scripts/procurement_mcp_server.py. It should accept supplier_name (required). Query the contracts table for rows matching the supplier. Return a JSON string with contract_id, supplier_name, annual_value, start_date, end_date, and status.
```

**What you should see.** Claude writes the function with a simple SELECT query and JSON return.

### Step 5: Test the server manually

Quit Claude first:

```
/quit
```

Run the server to check for errors:

```
python scripts/procurement_mcp_server.py
```

**What you should see.** The server starts without errors. Press Ctrl+C to stop it.

### Step 6: Register and test with Claude Code

Start Claude Code again:

```
claude
```

Run a test query:

```
What is the total spend with Northwind Logistics? Also show me any open POs over $10,000. And what is the contract status for Globex SA?
```

**What you should see.** Claude calls all three tools in sequence and returns: a spend total for Northwind, a table of large open POs, and the Globex contract details with status and expiry date.

### Step 7: Quit Claude

```
/quit
```

## Worked example: answering the VP's weekly questions

**Scenario.** It is Friday at 16:00. Your VP sends the weekly check-in Slack: "Top 3 suppliers by spend this quarter, any late POs, and contract renewals due in 90 days."

**The prompt you type:**

```
Answer three questions using the procurement tools: 1) What are the top 3 suppliers by total spend in the last quarter? 2) Are there any open POs past their delivery date? 3) Which contracts expire within the next 90 days?
```

**Folder layout:**

```
practice/
├── procurement.db
├── scripts/
│   └── procurement_mcp_server.py    (3 tools registered)
└── .claude/
    └── settings.json
```

**What you should see:**

Three sections: a ranked table of top suppliers by spend, a list of overdue POs with days late, and a table of contracts expiring soon.

**What Claude did behind the scenes:**

1. Claude parsed your three questions and matched each to a tool.
2. It called `get_supplier_spend` multiple times (or once with broad parameters) to find the top 3.
3. It called `get_open_pos` and filtered for POs where `delivery_date` is before today.
4. It called `get_contract_status` for all suppliers and filtered for expiry within 90 days.
5. It formatted each result set into a readable table.
6. Total time: under 10 seconds. The old way (three ERP exports, three pivot tables) took 45 minutes.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| `SyntaxError` when running the server. | Claude may have left a stray comma or missing colon. Read the error message. It tells you the line number. Open the file and fix that line. |
| Tool returns empty results for a supplier you know exists. | Check the exact spelling. "Northwind Logistics" is not the same as "northwind logistics" in a SQL WHERE clause. Add `.upper()` or use `COLLATE NOCASE` in your query. |
| `json.dumps` fails with "Object of type Row is not JSON serializable." | Convert SQLite Row objects to dictionaries before passing to `json.dumps`. Use `dict(row)` or build the dictionary manually from column names. |
| Claude calls the same tool twice instead of using two different tools. | Your tool descriptions may overlap. Make each docstring specific. "Returns spend totals" and "Returns open purchase orders" are distinct. "Returns procurement data" is too vague for both. |

## You are done with Lesson 4 when

- Your server file has three working tools: `get_supplier_spend`, `get_open_pos`, and `get_contract_status`.
- Each tool queries `procurement.db` and returns a JSON string.
- You tested all three through Claude Code and got real results.

Move to Lesson 5 when ready.
