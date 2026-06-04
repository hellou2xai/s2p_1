"""PostToolUse hook: append-only audit log for every tool call.

Registered in .claude/settings.json as a PostToolUse hook on all tools.
Claude Code passes tool call result details as JSON on stdin.
This script appends a JSON line to audit/audit.jsonl.

Reference solution for Course 6, Lesson 3.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


AUDIT_DIR = Path(__file__).resolve().parent.parent / "audit"
AUDIT_FILE = AUDIT_DIR / "audit.jsonl"


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = input_data.get("tool_name", "unknown")
    tool_input = input_data.get("tool_input", {})

    # Extract file path if present
    file_path = tool_input.get("file_path", tool_input.get("path", ""))

    # Determine action type
    action_map = {
        "Read": "read",
        "Write": "write",
        "Edit": "edit",
        "Glob": "search",
        "Grep": "search",
        "Bash": "execute",
    }
    action = action_map.get(tool_name, "other")

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool_name,
        "action": action,
        "file_path": str(file_path) if file_path else None,
        "session_id": input_data.get("session_id", "unknown"),
    }

    # Append to audit log (create if needed)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


if __name__ == "__main__":
    main()
