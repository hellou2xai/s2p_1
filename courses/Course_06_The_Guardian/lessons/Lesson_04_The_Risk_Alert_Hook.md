# The Risk Alert Hook

It is 13:30 Thursday afternoon. The Legal team's contract analyst sends you a message: "When a contract review comes back High or Critical risk, I need to know immediately. Can you put an alert file somewhere I can check? I do not want to read through every report to find the ones that need attention." You need a PostToolUse hook that watches for newly saved reports, checks the risk level, and writes an alert file when the risk is High or Critical.

## The S2P problem

In a batch of 12 contract reviews, two or three might be flagged High or Critical risk. Those are the ones that need legal attention within 48 hours. If the legal analyst has to open every report to find the high-risk ones, the urgent contracts get buried in the queue. A separate alert file for each high-risk contract gives the legal team a clear, scannable list of what needs attention right now.

## What Claude Code does for you

A PostToolUse hook on the Write tool fires after every successful file save. Your risk alert hook reads the newly written file content, extracts the risk level, and writes an alert file to `alerts/` when the level is High or Critical. Low and Medium risk contracts pass through silently. The legal team checks the `alerts/` folder and sees only what matters.

## Set up

1. Lessons 1 through 3 completed. Both the validation hook and the audit hook are registered.
2. Claude Code open in `Course_06_The_Guardian/practice/`.
3. The `hooks/` directory exists with the two previous hook scripts.

## Step-by-step

### Step 1. Create the alerts directory.

```
mkdir -p alerts
```

You should see the `alerts/` folder appear in your project.

### Step 2. Create the risk alert hook script.

Create the file `hooks/risk-alert-hook.py` with the following content. Copy the entire block.

```python
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

    # Extract contract ID
    contract_match = re.search(r"CTR-\d{4}-\d{3}", content)
    contract_id = (
        contract_match.group(0) if contract_match else "unknown"
    )

    # Extract supplier name
    supplier_match = re.search(
        r"\*\*Parties:\*\*.*?and\s+(.*?)\s*\(Supplier\)", content
    )
    supplier = (
        supplier_match.group(1).strip()
        if supplier_match
        else "unknown"
    )

    # Write alert file
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    alert_filename = (
        f"{today}-{contract_id}-{risk_level.lower()}-risk.txt"
    )
    alert_path = ALERTS_DIR / alert_filename

    alert_content = (
        f"RISK ALERT: {risk_level}\n"
        f"Contract: {contract_id}\n"
        f"Supplier: {supplier}\n"
        f"Date: {today}\n"
        f"File: {file_path}\n"
        f"\n"
        f"Action required: Review this contract and confirm "
        f"risk mitigation.\n"
    )

    with open(alert_path, "w", encoding="utf-8") as f:
        f.write(alert_content)


if __name__ == "__main__":
    main()
```

You should see the file `hooks/risk-alert-hook.py` saved with no errors.

### Step 3. Walk through the script.

The risk alert hook works in five stages:

1. **Read input.** It reads JSON from stdin, same as the other hooks.
2. **Filter by tool and path.** It only processes Write tool calls targeting the `outputs/` folder. All other tool calls are ignored.
3. **Extract risk level.** It uses a regex to find the `**Risk Level:**` field and pulls the value. If the level is not High or Critical, the hook exits silently.
4. **Extract contract details.** It pulls the contract ID (format CTR-YYYY-NNN) and supplier name from the file content.
5. **Write the alert.** It creates a plain-text alert file in `alerts/` with the risk level, contract ID, supplier name, date, and a line stating that review is required.

The alert file name follows the pattern `YYYY-MM-DD-CTR-YYYY-NNN-high-risk.txt` or `YYYY-MM-DD-CTR-YYYY-NNN-critical-risk.txt`. This makes alerts easy to sort by date and risk level.

### Step 4. Register the hook in settings.json.

```
Open .claude/settings.json and add a second PostToolUse hook entry. The matcher should be "Write" and the command should be "python hooks/risk-alert-hook.py".
```

Your `.claude/settings.json` should now look like this:

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

### Step 5. Test with a High or Critical risk contract.

Save a valid contract review that has a High or Critical risk level to outputs/.

```
Read data/contracts/review-CTR-2025-002.md and save it to outputs/review-CTR-2025-002.md exactly as it is. Do not change anything.
```

You should see the file save successfully (it passes validation). Then check the alerts folder:

```
List the files in alerts/ and show me the contents of any alert file.
```

You should see an alert file named something like `2026-04-25-CTR-2025-002-critical-risk.txt` with the content:

```
RISK ALERT: Critical
Contract: CTR-2025-002
Supplier: Heartland Polymers
Date: 2026-04-25
File: outputs/review-CTR-2025-002.md

Action required: Review this contract and confirm risk mitigation.
```

### Step 6. Confirm that Low and Medium risk contracts do not trigger alerts.

```
Read data/contracts/review-CTR-2025-001.md and save it to outputs/review-CTR-2025-001.md exactly as it is.
```

You should see the file save successfully. Check `alerts/` again. No new alert file should appear, because CTR-2025-001 has a Medium risk level.

## Worked example

**Starting files:**
- `data/contracts/review-CTR-2025-002.md`: Valid report, Critical risk, supplier Heartland Polymers.
- `hooks/risk-alert-hook.py`: The alert script from Step 2.
- `.claude/settings.json`: All three hooks registered.

**What you type:**

```
Read data/contracts/review-CTR-2025-002.md and save it to outputs/review-CTR-2025-002.md exactly as written.
```

**What you should see:** The file saves successfully. An alert file appears in `alerts/`.

**What Claude did, behind the scenes:**

1. Claude Code called the Write tool with the file path `outputs/review-CTR-2025-002.md` and the report content.
2. The PreToolUse validation hook ran first and approved the write (all sections present, valid risk level, named supplier).
3. The file was written to disk.
4. The PostToolUse audit hook fired and appended a log entry to `audit/audit.jsonl`.
5. The PostToolUse risk alert hook fired. It found `**Risk Level:** Critical` in the content. It extracted the contract ID (CTR-2025-002) and supplier name (Heartland Polymers).
6. The hook wrote `2026-04-25-CTR-2025-002-critical-risk.txt` to the `alerts/` folder.

## Common mistakes and how to recover

- **Symptom:** Alert files appear for Low and Medium risk contracts too. **Fix:** Check the `HIGH_RISK_LEVELS` set in the script. It should contain only `{"High", "Critical"}`. If you added "Low" or "Medium", remove them.

- **Symptom:** The alert file has "unknown" for the contract ID. **Fix:** The regex `CTR-\d{4}-\d{3}` expects the contract ID in the file content, not in the file name. Check that the report body contains the contract ID in the heading (for example, "Contract Review: CTR-2025-002").

- **Symptom:** The hook crashes because the alerts directory does not exist. **Fix:** The script calls `ALERTS_DIR.mkdir(parents=True, exist_ok=True)` before writing. If you removed that line, add it back.

- **Symptom:** The alert file is empty. **Fix:** Check that the `alert_content` string is built correctly. Make sure the `with open(alert_path, "w") as f: f.write(alert_content)` block is indented inside the `main()` function.

- **Symptom:** Multiple alert files for the same contract appear after re-runs. **Fix:** The file name includes the date and contract ID, so re-running on the same day overwrites the previous alert. If you see duplicates with different dates, that is correct behavior across different days.
