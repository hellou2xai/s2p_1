<!-- v1.0 2026-04-25 Initial. -->

# MCP Server Registration in settings.json (Reference Solution)

The `.claude/settings.json` file with the procurement MCP server registered.

## The file

```json
{
  "mcpServers": {
    "nexus-procurement": {
      "command": "python",
      "args": ["mcp-server/procurement_server.py"],
      "cwd": "."
    }
  },
  "permissions": {
    "allow": [
      "mcp__nexus-procurement__get_supplier_spend",
      "mcp__nexus-procurement__get_open_pos",
      "mcp__nexus-procurement__get_contract_status"
    ]
  }
}
```

## Key points

- The `mcpServers` key registers the server by name (`nexus-procurement`).
- The `command` is `python` and `args` points to the server script. Claude Code launches this process automatically.
- The `cwd` field sets the working directory. A dot means the project root.
- The `permissions.allow` array pre-approves the three MCP tools. Without this, Claude Code prompts for permission on every call.
- Tool names follow the pattern `mcp__<server-name>__<tool-name>`.
- The server must be running (or launchable) for Claude Code to call the tools. If it fails to start, Claude Code shows a connection error.

## How to verify

After saving this file, restart Claude Code in the project folder. Then type:

```
What MCP servers are connected?
```

Claude Code should list `nexus-procurement` with three tools: `get_supplier_spend`, `get_open_pos`, and `get_contract_status`.
