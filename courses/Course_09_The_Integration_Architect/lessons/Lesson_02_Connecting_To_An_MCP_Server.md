# Lesson 2: Connecting to an MCP Server

**Time:** 25 minutes.

## The data is one room away

It is 10:00. You just learned what MCP is, but Claude Code still cannot reach your procurement database. The database is right there, sitting in `procurement.db` in your practice folder. The problem is not access. The problem is that nobody told Claude where to find the server that speaks to the database. In this lesson, you register an MCP server in Claude Code's settings, verify the connection, and run your first live query.

## What Claude Code is going to do for you

After this lesson, Claude Code will know about your procurement MCP server. When you ask a procurement question, Claude will call the server, the server will query the database, and the answer will appear in your terminal. No exports. No copy-paste. No stale spreadsheets.

## Set up

1. Make sure you are in the practice folder:

```
cd "Course_09_The_Integration_Architect/practice"
```

2. Confirm the MCP server script is present:

```
ls scripts/
```

You should see `procurement_mcp_server.py`.

3. Confirm Python is installed:

```
python --version
```

You should see Python 3.10 or later. If not, install Python before continuing.

4. Install the FastMCP library:

```
pip install fastmcp
```

You should see "Successfully installed fastmcp" or "Requirement already satisfied."

**Folder layout:**

```
practice/
├── CLAUDE.md
├── procurement.db
├── supplier-master.csv
└── scripts/
    └── procurement_mcp_server.py
```

## Step-by-step

### Step 1: Test the server manually

Run the server to confirm it starts without errors:

```
python scripts/procurement_mcp_server.py
```

**What you should see.** The server prints "Procurement MCP server running on stdio" or a similar startup message. Press Ctrl+C to stop it.

### Step 2: Register the server in Claude Code settings

Open your project-level Claude Code settings file. If it does not exist, create it:

```
cat .claude/settings.json
```

If the file does not exist, you will see an error. That is fine. Create the directory and file:

```
mkdir -p .claude
```

Now open `.claude/settings.json` in your text editor and add this content:

```json
{
  "mcpServers": {
    "procurement": {
      "command": "python",
      "args": ["scripts/procurement_mcp_server.py"],
      "cwd": "."
    }
  }
}
```

Save the file.

**What you should see.** A valid JSON file at `.claude/settings.json` with the procurement server registered.

### Step 3: Start Claude Code and verify the connection

```
claude
```

**What you should see.** Claude Code starts and loads the MCP server. You may see a brief message like "Connected to MCP server: procurement" or a tool count.

### Step 4: Ask Claude what tools are available

```
What MCP tools do you have access to right now? List each tool name and what it does.
```

**What you should see.** Claude lists the tools exposed by your procurement server. At minimum, you should see tools like `get_supplier_spend`, `get_open_pos`, and `get_contract_status`. Each tool has a description.

### Step 5: Run your first live query

```
What is the total spend with Northwind Logistics in the last 12 months?
```

**What you should see.** Claude calls the `get_supplier_spend` tool, passes "Northwind Logistics" as the supplier name, and returns a dollar figure. The number comes from `procurement.db`, not from a CSV you exported.

### Step 6: Run a second query to confirm

```
Show me all open POs over $5,000.
```

**What you should see.** Claude calls `get_open_pos` with a minimum amount filter and returns a table of POs with supplier names, amounts, and dates.

### Step 7: Quit Claude

```
/quit
```

## Worked example: verifying a connection end to end

**Scenario.** You are the procurement operations lead at Nexus Procurement Hub. You just set up MCP for the first time. Your manager asks: "Can Claude pull contract data now?"

**The prompt you type:**

```
What is the contract status for Globex SA? Include the contract value and expiry date.
```

**Folder layout:**

```
practice/
├── .claude/
│   └── settings.json       (MCP server registered here)
├── procurement.db           (contains contracts table)
└── scripts/
    └── procurement_mcp_server.py
```

**What you should see:**

Claude responds with: "Globex SA has an active contract valued at $1,240,000, expiring 2026-09-30."

**What Claude did behind the scenes:**

1. Claude read `settings.json` at startup and connected to the `procurement` MCP server.
2. Your prompt mentioned "contract status," so Claude matched it to the `get_contract_status` tool.
3. Claude called `get_contract_status` with `supplier_name: "Globex SA"`.
4. The MCP server queried the `contracts` table in `procurement.db` for rows matching Globex SA.
5. The server returned the contract value, status, and expiry date as JSON.
6. Claude formatted the JSON into a readable sentence.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Claude starts but says "No MCP tools found." | Your `settings.json` path or command is wrong. Check that `"command": "python"` works in your terminal. Try `"command": "python3"` on Mac or Linux. |
| "ModuleNotFoundError: No module named 'fastmcp'" | You installed FastMCP in a different Python environment. Run `pip install fastmcp` again in the same terminal where Claude runs. |
| Claude says "MCP server failed to start." | Run `python scripts/procurement_mcp_server.py` manually to see the error. Common causes: wrong file path, missing `procurement.db`, or a syntax error in the server script. |
| The spend figure looks wrong. | The MCP server queries `procurement.db` as-is. If the data was regenerated with different seeds, the numbers will differ. Run `python scripts/regenerate_data.py` to reset. |
| You edited `settings.json` but Claude does not see the change. | Claude reads settings at startup. Quit (`/quit`) and restart `claude`. |

## You are done with Lesson 2 when

- Your `settings.json` file registers the procurement MCP server.
- Claude Code starts and lists at least three procurement tools.
- You ran a live query and got a result from `procurement.db`.

Move to Lesson 3 when ready.
