# Lesson 5: Security Patterns for MCP Servers

**Time:** 25 minutes.

## Your server works, but it writes too

It is 11:00 on Thursday. A colleague tests your procurement MCP server. They type: "Delete all rows from the spend table where the amount is under $100." Claude calls the tool. The tool runs the SQL. The rows are gone. Your colleague stares at the screen. "I did not mean to actually delete them."

The problem is simple. Your MCP server has full read-write access to the database, and nothing stops Claude from running destructive queries. In production, that is not acceptable. In this lesson, you lock down the server so it can only read, move credentials out of visible files, and make sure secrets never appear in CLAUDE.md.

## What Claude Code is going to do for you

By the end of this lesson, your MCP server will be read-only. Database credentials will live in environment variables, not in source code. And your CLAUDE.md file will contain zero secrets. This is the minimum security posture for any MCP server that touches real procurement data.

## Set up

1. Navigate to the practice folder:

```
cd "Course_09_The_Integration_Architect/practice"
```

2. Start Claude Code:

```
claude
```

3. Confirm your server is still registered:

```
What MCP tools do you have access to?
```

You should see your three procurement tools.

## Step-by-step

### Step 1: Make the database connection read-only

```
Update scripts/procurement_mcp_server.py so the sqlite3 connection opens in read-only mode. Use the URI mode: sqlite3.connect("file:procurement.db?mode=ro", uri=True). Apply this to every function that connects to the database.
```

**What you should see.** Claude modifies each function's `sqlite3.connect()` call to use the read-only URI. If any function tried to write, SQLite would raise an `OperationalError: attempt to write a readonly database`.

### Step 2: Test that writes are blocked

```
Try to insert a row into the suppliers table in procurement.db using the MCP server. What happens?
```

**What you should see.** Claude attempts to call a tool or run a query. The server returns an error: "attempt to write a readonly database." No data is modified. This is exactly the behavior you want.

### Step 3: Move the database path to an environment variable

```
Update scripts/procurement_mcp_server.py so it reads the database path from an environment variable called PROCUREMENT_DB_PATH. If the variable is not set, default to "procurement.db". Use os.environ.get().
```

**What you should see.** Claude adds `import os` at the top and replaces the hardcoded database path with `os.environ.get("PROCUREMENT_DB_PATH", "procurement.db")`.

### Step 4: Set the environment variable in settings.json

Quit Claude:

```
/quit
```

Open `.claude/settings.json` in your text editor. Update the procurement server entry to include an `env` block:

```json
{
  "mcpServers": {
    "procurement": {
      "command": "python",
      "args": ["scripts/procurement_mcp_server.py"],
      "cwd": ".",
      "env": {
        "PROCUREMENT_DB_PATH": "procurement.db"
      }
    }
  }
}
```

Save the file.

**What you should see.** A valid JSON file with the environment variable configured. The database path is now in settings, not in source code.

### Step 5: Verify CLAUDE.md contains no secrets

Start Claude Code again:

```
claude
```

```
Read the CLAUDE.md file in this project. Does it contain any database paths, passwords, API keys, or credentials? List anything that looks like a secret.
```

**What you should see.** Claude confirms that CLAUDE.md contains no secrets. If it finds any, you need to remove them. CLAUDE.md is a context file that Claude reads at startup. Anything in it is visible in the conversation. Secrets do not belong there.

### Step 6: Add a security note to CLAUDE.md

```
Add a section to CLAUDE.md called "Security rules" with three lines: 1) Never write to procurement.db. All database access is read-only. 2) Never log or display database credentials in terminal output. 3) Never store passwords, API keys, or connection strings in this file.
```

**What you should see.** Claude appends the security section to CLAUDE.md. These rules remind Claude (and future users) of the boundaries.

### Step 7: Quit Claude

```
/quit
```

## Worked example: a secure MCP configuration for a real team

**Scenario.** You are deploying this MCP server for three analysts at Nexus Procurement Hub. The database is on a shared network drive. Each analyst has their own machine.

**The prompt you type:**

```
Review scripts/procurement_mcp_server.py and .claude/settings.json for security issues. Check for: hardcoded paths, embedded credentials, write access to the database, and secrets in CLAUDE.md. Give me a pass/fail for each check.
```

**Folder layout:**

```
practice/
├── CLAUDE.md                (no secrets)
├── procurement.db           (read-only access)
├── scripts/
│   └── procurement_mcp_server.py  (reads DB path from env var)
└── .claude/
    └── settings.json        (env var set here)
```

**What you should see:**

A four-line report:
- Hardcoded paths: PASS (database path comes from environment variable).
- Embedded credentials: PASS (no passwords in source code).
- Write access: PASS (connection uses `mode=ro`).
- Secrets in CLAUDE.md: PASS (no credentials found).

**What Claude did behind the scenes:**

1. Claude opened `procurement_mcp_server.py` and searched for hardcoded file paths and credential strings.
2. It checked each `sqlite3.connect()` call for the `mode=ro` flag.
3. It opened `.claude/settings.json` and confirmed the database path is in `env`, not in the script.
4. It opened `CLAUDE.md` and scanned for patterns that look like secrets (API keys, passwords, connection strings).
5. It reported pass or fail for each check.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| "attempt to write a readonly database" on a legitimate read query. | Your SQL may include a `CREATE TEMP TABLE` or `PRAGMA` that requires write access. Rewrite the query to avoid temp tables. Use subqueries instead. |
| Claude prints the database path in its response. | Add a line to CLAUDE.md: "Do not display file paths that contain environment variable values." Claude will follow this instruction. |
| You put the database password in CLAUDE.md for convenience. | Remove it immediately. Use environment variables in `settings.json` instead. CLAUDE.md is readable by anyone who opens the project folder. |
| The environment variable is not picked up by the server. | Check that the `"env"` block is inside the correct server entry in `settings.json`. Restart Claude Code after any settings change. |
| A colleague's machine uses a different path to the database. | Each analyst sets their own `PROCUREMENT_DB_PATH` in their local `.claude/settings.json`. The server script stays the same across all machines. |

## You are done with Lesson 5 when

- Your database connection is read-only (`mode=ro`).
- The database path comes from an environment variable, not a hardcoded string.
- CLAUDE.md contains zero secrets and has a security rules section.
- You tested that a write attempt is blocked.

Move to Lesson 6 when ready.
