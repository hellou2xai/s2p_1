"""PostToolUse hook: risk alert on High or Critical findings.

Registered in .claude/settings.json as a PostToolUse hook on the Write tool.
After a successful file write to outputs/, reads the file, checks the risk
level, and writes an alert to alerts/ if High or Critical.

Reference solution for Course 6, Lesson 4.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path


ALERTS_DIR = Path(__file__).resolve().parent.parent / "alerts"
HIGH_RISK_LEVELS = {"High", "Critical"}


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only process Write tool calls to outputs/
    if tool_name != "Write":
        return

    file_path = tool_input.get("file_path", "")
    if "outputs/" not in file_path and "outputs\\" not in file_path:
        return

    content = tool_input.get("content", "")

    # Extract risk level
    risk_match = re.search(r"\*\*Risk Level:\*\*\s*(\w+)", content)
    if not risk_match:
        return

    risk_level = risk_match.group(1).strip().rstrip(".")
    if risk_level not in HIGH_RISK_LEVELS:
        return

    # Extract contract ID from the file content or filename
    contract_match = re.search(r"CTR-\d{4}-\d{3}", content)
    contract_id = contract_match.group(0) if contract_match else "unknown"

    # Extract supplier name
    supplier_match = re.search(
        r"\*\*Parties:\*\*.*?and\s+(.*?)\s*\(Supplier\)", content
    )
    supplier = supplier_match.group(1).strip() if supplier_match else "unknown"

    # Write alert
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    alert_path = ALERTS_DIR / f"{today}-{contract_id}-{risk_level.lower()}-risk.txt"

    alert_content = (
        f"RISK ALERT: {risk_level}\n"
        f"Contract: {contract_id}\n"
        f"Supplier: {supplier}\n"
        f"Date: {today}\n"
        f"File: {file_path}\n"
        f"\n"
        f"Action required: Review this contract and confirm risk mitigation.\n"
    )

    with open(alert_path, "w", encoding="utf-8") as f:
        f.write(alert_content)


if __name__ == "__main__":
    main()
