"""
Team notification hook (PostToolUse).
Writes a notification file when a critical risk is detected.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    """Check tool output for critical risk mentions. Write notification if found."""
    input_data = json.loads(sys.stdin.read())

    tool_name = input_data.get("tool_name", "")
    tool_output = input_data.get("tool_output", "")

    if tool_name != "Write":
        return

    # Check for critical risk keywords in written content
    content = input_data.get("tool_input", {}).get("content", "")
    critical_keywords = ["corrective action required", "critical risk", "contract expired", "immediate escalation"]

    found = [kw for kw in critical_keywords if kw.lower() in content.lower()]
    if not found:
        return

    notify_dir = Path("notifications")
    notify_dir.mkdir(exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    notification = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "critical_risk",
        "triggers": found,
        "source_file": input_data.get("tool_input", {}).get("file_path", "unknown"),
        "action_required": "Review the flagged output and escalate to the Procurement Operations Manager.",
    }

    with open(notify_dir / f"notify-{ts}.json", "w", encoding="utf-8") as f:
        json.dump(notification, f, indent=2)


if __name__ == "__main__":
    main()
