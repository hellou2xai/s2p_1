"""
Audit log hook (PostToolUse).
Appends a JSONL entry to audit/audit.jsonl after every Write or Bash tool call.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    """Read tool result from stdin and append audit entry."""
    input_data = json.loads(sys.stdin.read())

    tool_name = input_data.get("tool_name", "unknown")
    tool_input = input_data.get("tool_input", {})

    # Only log Write and Bash calls
    if tool_name not in ("Write", "Bash"):
        return

    audit_dir = Path("audit")
    audit_dir.mkdir(exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool_name,
        "file_path": tool_input.get("file_path", tool_input.get("command", "n/a")),
        "analyst": "ANALYST_NAME_PLACEHOLDER",
        "session_id": "SESSION_PLACEHOLDER",
    }

    with open(audit_dir / "audit.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    main()
