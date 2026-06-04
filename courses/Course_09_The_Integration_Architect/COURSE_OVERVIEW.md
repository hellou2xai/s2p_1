# Course 9: The Integration Architect

## The stale data problem

It is Tuesday morning. Your CPO asks: "What is our open PO exposure with Apex Electronics? They just missed a delivery."

You open the spend report you exported last Friday. You scan for Apex Electronics. You find three open POs totaling $184,000. But that was Friday. Since then, AP approved two more requisitions. The real number is $247,000, and you do not know it.

You email the AP team: "Can you send me the latest open PO report for Apex Electronics?" They reply four hours later with a CSV. By then, the CPO has already made a decision based on the stale number.

This happens every week. The data exists in your systems. It sits in databases, ERP tables, and procurement platforms. But Claude Code cannot reach it. You export CSVs, drop them in folders, and hope they are current. They never are.

## What MCP is

The Model Context Protocol (MCP) is a standard that lets Claude Code call external tools and data sources directly. Instead of reading a CSV file, Claude Code sends a structured request to an MCP server. The server queries the database (or API, or file system) and returns the result. Claude Code receives live data, not a stale export.

Think of MCP as a translator. Claude Code speaks one language. Your database speaks another. The MCP server sits between them and handles the translation.

What MCP gives you:

| Without MCP | With MCP |
|---|---|
| Export CSV from ERP, drop in folder, hope it is current | Claude Code queries the database directly |
| Data is hours or days old | Data is current as of the query |
| Manual re-export when data changes | No re-export needed |
| One file per query type | One server handles many query types |
| Format errors in CSV break analysis | Structured data, consistent format |

## The practice scenario

Nexus Procurement Hub is a US-based procurement team managing $46.9M in annual spend across 20 suppliers in five categories: raw materials, logistics, IT services, facilities, and professional services.

Today's date is **2026-04-25**. Your procurement data lives in a SQLite database (`procurement.db`) with four tables:

| Table | Rows | What it holds |
|---|---|---|
| suppliers | 20 | Supplier master: ID, name, category, tier, annual spend, status |
| spend | ~700 | Transaction history: dates, amounts, PO numbers, payment status |
| contracts | 20 | Contract terms: start/end dates, annual value, auto-renewal flag |
| open_pos | 50 | Open purchase orders: amounts, creation dates, delivery dates, status |

You also have a CSV export (`supplier-master.csv`) that was pulled last week. It is already out of date. That is the point.

## What you will build

A FastMCP server in Python that exposes three procurement tools:

1. **get_supplier_spend**: Query spend by supplier, category, or date range.
2. **get_open_pos**: Return open purchase orders, filtered by supplier or status.
3. **get_contract_status**: Check contract terms, expiry dates, and auto-renewal flags.

When you finish, you type a question like "Show me all overdue POs for raw materials suppliers" and Claude Code calls your MCP server, runs the SQL query, and returns the result. No CSV. No export. Live data.

```
practice/
├── CLAUDE.md
├── data/
│   ├── procurement.db
│   └── supplier-master.csv
├── mcp-server/
│   └── procurement_server.py    (you build this)
└── outputs/
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | MCP protocol basics: what it is, how it works, why procurement teams need it | 30 min |
| 2 | Connecting to an existing MCP server: registering in settings.json | 40 min |
| 3 | Anatomy of an MCP server: FastMCP, tools, and type hints | 50 min |
| 4 | Building the procurement data MCP server: three tools against procurement.db | 60 min |
| 5 | Security patterns: read-only access, input validation, and error handling | 40 min |
| 6 | Combining MCP with skill-driven analysis: live data meets reusable prompts | 40 min |

Total: about 5 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. Your MCP server runs and registers in `.claude/settings.json` without errors.
2. You type "What is our total spend with Great Lakes Steel?" and Claude Code calls `get_supplier_spend`, queries the database, and returns the answer.
3. You type "Show me all overdue POs" and Claude Code calls `get_open_pos` with a status filter and returns a table.
4. You type "Which contracts expire in the next 90 days?" and Claude Code calls `get_contract_status` and returns the list.
5. Your server enforces read-only access. No INSERT, UPDATE, or DELETE queries are possible.
6. You combine an MCP tool call with a skill to produce a formatted supplier risk brief from live data.
