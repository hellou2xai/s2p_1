# Lesson 3: Anatomy of an MCP Server

**Time:** 25 minutes.

## You connected a server, but you did not build it

It is 10:45. Your MCP server works. You ask Claude a question, it calls a tool, and you get an answer. But you have no idea what is inside that server script. If a tool returns the wrong data, you cannot debug it. If your team needs a new tool, you cannot add one. In this lesson, you open the server file, read every line, and understand how FastMCP turns a Python function into a tool that Claude can call.

## What Claude Code is going to do for you

By the end of this lesson, you will be able to read any MCP server file and identify three things: where tools are defined, what inputs each tool accepts, and what each tool returns. You will not need to write Python from scratch. You will need to read it well enough to modify a description or change a return field.

## Set up

1. Navigate to the practice folder:

```
cd "Course_09_The_Integration_Architect/practice"
```

2. Open the server script in your editor or read it with Claude:

```
claude
```

3. Confirm you can see the server file:

```
Read the file scripts/procurement_mcp_server.py and show me its full contents.
```

**What you should see.** Claude prints the entire Python file. It should be about 60 to 80 lines long.

## Step-by-step

### Step 1: Identify the FastMCP import and server creation

Ask Claude:

```
In scripts/procurement_mcp_server.py, find the line where the MCP server object is created. What is the server's name?
```

**What you should see.** Claude points to a line like `mcp = FastMCP("procurement")`. The string "procurement" is the server name. This is the name Claude Code uses to identify the server.

### Step 2: Find the first tool definition

```
Find the first function decorated with @mcp.tool() in the server file. Show me the function name, the decorator, the parameters, and the return statement.
```

**What you should see.** Claude shows something like:

```python
@mcp.tool()
def get_supplier_spend(supplier_name: str, start_date: str = None, end_date: str = None) -> str:
    """Returns total spend in USD for a named supplier over a date range."""
    # ... SQL query ...
    return json.dumps(result)
```

Claude explains that the `@mcp.tool()` decorator registers this function as a tool. The function name becomes the tool name. The type hints (`str`) become the input schema. The docstring becomes the tool description.

### Step 3: Understand input schemas from type hints

```
How does FastMCP know which inputs are required and which are optional for get_supplier_spend?
```

**What you should see.** Claude explains that `supplier_name: str` has no default value, so it is required. `start_date: str = None` has a default of `None`, so it is optional. FastMCP reads these type hints and defaults to build the JSON schema automatically.

### Step 4: Trace the database query

```
In get_supplier_spend, show me the SQL query that runs against procurement.db. What table does it read from? What column does it filter on?
```

**What you should see.** Claude shows a SQL query like `SELECT SUM(amount) FROM spend WHERE supplier_name = ?`. It reads from the `spend` table and filters on the `supplier_name` column.

### Step 5: Check the return format

```
What format does get_supplier_spend return its results in? Why does it use json.dumps?
```

**What you should see.** Claude explains that MCP tools return strings. The function uses `json.dumps()` to convert the Python dictionary into a JSON string. Claude Code then parses this JSON to format the answer.

### Step 6: Count all tools in the file

```
How many tools are defined in this server file? List each tool name and its one-line description.
```

**What you should see.** Claude lists three tools:
- `get_supplier_spend`: Returns total spend for a named supplier.
- `get_open_pos`: Returns open purchase orders filtered by supplier or amount.
- `get_contract_status`: Returns contract details for a named supplier.

### Step 7: Quit Claude

```
/quit
```

## Worked example: reading a new tool you have never seen

**Scenario.** A colleague sends you a new MCP server file with a tool called `get_invoice_aging`. You need to understand it before adding it to your settings.

**The prompt you type:**

```
Read scripts/procurement_mcp_server.py and explain the get_supplier_spend tool. Tell me: what inputs it takes, which are required, what SQL it runs, and what it returns.
```

**Folder layout:**

```
practice/
├── scripts/
│   └── procurement_mcp_server.py
└── procurement.db
```

**What you should see:**

Claude gives a structured breakdown: one required input (`supplier_name`), two optional inputs (`start_date`, `end_date`), a SQL query against the `spend` table, and a JSON string with total spend and row count.

**What Claude did behind the scenes:**

1. Claude opened `scripts/procurement_mcp_server.py` and read the full file.
2. It found the `@mcp.tool()` decorator on `get_supplier_spend`.
3. It read the function signature to identify parameters and their types.
4. It checked which parameters have default values (optional) versus which do not (required).
5. It traced the SQL query inside the function body.
6. It identified the return type as a JSON-serialized dictionary.
7. It formatted all of this into a clear summary.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Claude says the server file has no tools. | Check that each tool function has the `@mcp.tool()` decorator. A plain function without the decorator is invisible to MCP. |
| The docstring is empty and Claude cannot describe the tool. | Add a one-line docstring to the function. FastMCP uses the docstring as the tool description. Without it, Claude has no context for when to call the tool. |
| You see `sqlite3.OperationalError: no such table`. | The SQL references a table that does not exist in `procurement.db`. Run `python scripts/regenerate_data.py` to rebuild the database. |
| Claude shows different parameter names than expected. | Parameter names in the function signature become the input field names in the schema. If the function says `supplier` but you expected `supplier_name`, rename the parameter in the Python file. |

## You are done with Lesson 3 when

- You can point to the decorator, the function name, the type hints, and the docstring in any MCP tool.
- You understand that required inputs have no default value, and optional inputs have one.
- You know that MCP tools return strings, usually as JSON.

Move to Lesson 4 when ready.
