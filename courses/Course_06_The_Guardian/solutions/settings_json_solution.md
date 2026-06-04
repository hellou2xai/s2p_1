<!-- v1.0 2026-04-25 Initial. -->

# settings.json Hook Registration (Reference Solution)

The .claude/settings.json file with all three hooks registered.

## The file

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python hooks/validate-report-hook.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python hooks/audit-log-hook.py"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python hooks/risk-alert-hook.py"
          }
        ]
      }
    ]
  }
}
```

## Key points

- The validation hook uses `"matcher": "Write"` so it only fires on Write tool calls.
- The audit hook uses `"matcher": "*"` so it fires on every tool call.
- The risk alert hook uses `"matcher": "Write"` because it only needs to check newly written files.
- Hook commands use relative paths. Claude Code runs them from the project root.
- The order matters: within the same event type, hooks run in the order listed.
