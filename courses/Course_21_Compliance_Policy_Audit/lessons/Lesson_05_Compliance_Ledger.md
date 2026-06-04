# The Compliance Ledger

It is 14:00 Wednesday. You have three compliance reports: approval authority, preferred supplier, and documentation completeness. Each report lives in a separate file. The auditors want a single, chronological trail of every compliance check you ran, what rule was tested, what the result was, and when. You build an append-only JSONL ledger using a PostToolUse hook. Every time Claude Code writes a compliance finding, the hook appends a line to the ledger. The ledger cannot be edited after the fact. That is the audit trail.

## The S2P problem

Compliance evidence scattered across multiple files is hard to audit. The auditor asks: "Show me every compliance check you ran on February 15." If your checks live in three separate reports with different formats, you search three files, reconcile timestamps, and hope nothing was missed. An append-only ledger in JSONL format (one JSON object per line) gives the auditor a single file. Each line has a timestamp, the rule tested, the transaction checked, the result (pass or fail), and the severity. No line is ever deleted or modified. The ledger is the evidence.

## What Claude Code does for you

You create a PostToolUse hook that fires after every Write operation. When Claude Code writes a compliance finding to any output file, the hook appends a structured entry to `outputs/compliance-ledger.jsonl`. Each entry records the timestamp, the rule name, the transaction_id, the result, the severity, and the output file that was written. The ledger grows with every compliance check. It cannot shrink.

## Set up

1. Lessons 1 through 4 completed. Compliance reports are in `Drafts/`.
2. Claude Code open in `Course_21_Compliance_Policy_Audit/practice/`.
3. The `.claude/` directory exists (or you will create it).

## Step-by-step

### Step 1. Create the outputs directory and the hooks directory.

```
mkdir -p outputs hooks .claude
```

You should see three directories created: `outputs/`, `hooks/`, and `.claude/`.

### Step 2. Create the compliance ledger hook script.

Create the file `hooks/compliance-ledger-hook.py` with the following content.

```python
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LEDGER_DIR = Path(__file__).resolve().parent.parent / "outputs"
LEDGER_FILE = LEDGER_DIR / "compliance-ledger.jsonl"


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = input_data.get("tool_name", "unknown")
    if tool_name != "Write":
        return

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")

    # Only log writes to compliance-related files
    compliance_keywords = [
        "compliance", "breach", "violation",
        "gap", "exception", "finding", "audit"
    ]
    file_lower = str(file_path).lower()
    if not any(kw in file_lower for kw in compliance_keywords):
        return

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "compliance_write",
        "file_written": str(file_path),
        "content_length": len(content),
        "session_id": input_data.get("session_id", "unknown"),
    }

    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    main()
```

You should see the file saved at `hooks/compliance-ledger-hook.py`.

### Step 3. Walk through the hook logic.

The hook works in four stages:

1. **Read input.** It reads JSON from stdin. Claude Code sends the tool name and tool input after each tool call.
2. **Filter.** It checks whether the tool is "Write" and whether the file path contains a compliance keyword. This prevents the hook from logging every file write. Only compliance-related writes get recorded.
3. **Build the entry.** It creates a JSON object with the timestamp, file path, content length, and session ID.
4. **Append to ledger.** It opens `outputs/compliance-ledger.jsonl` in append mode ("a") and writes one JSON line. Append mode means existing entries are never overwritten.

### Step 4. Register the hook in settings.json.

```
Create the file .claude/settings.json with this content:

{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python hooks/compliance-ledger-hook.py"
          }
        ]
      }
    ]
  }
}
```

You should see `.claude/settings.json` saved with the PostToolUse hook registered.

### Step 5. Test the hook by writing a compliance file.

```
Write a test file to outputs/test-compliance-finding.md with this content: "Test finding: TXN-001 failed approval authority check. Amount $28,000, approved by Manager, required VP."
```

You should see the test file saved. After the write, the hook fires and appends a line to `outputs/compliance-ledger.jsonl`.

### Step 6. Verify the ledger.

```
Read outputs/compliance-ledger.jsonl and show me its contents.
```

You should see one JSON line recording the write to `outputs/test-compliance-finding.md` with a UTC timestamp, the file path, and the content length.

## Worked example

**Starting files:**
- `hooks/compliance-ledger-hook.py` (the ledger hook).
- `.claude/settings.json` (hook registration).

**What you type:**

```
Write a compliance finding to outputs/approval-breach-summary.md: "12 approval authority breaches found across 200 transactions. Total breach amount: $342,000. Highest single breach: TXN-087 at $95,000 approved by a Manager instead of a VP."
```

**What you should see:** The file saved to outputs/. A new line appended to `outputs/compliance-ledger.jsonl` recording the write.

**What Claude did, behind the scenes:**

1. Claude Code called the Write tool to save `outputs/approval-breach-summary.md`.
2. After the Write completed, Claude Code ran the PostToolUse hook.
3. The hook read the tool input from stdin: tool name "Write," file path containing "breach."
4. The hook checked the file path for compliance keywords. "breach" matched.
5. The hook built a ledger entry with timestamp, file path, content length, and session ID.
6. The hook appended the entry to `outputs/compliance-ledger.jsonl` in append mode.

## Common mistakes and how to recover

- **Symptom:** The ledger file is empty after writing a compliance file. **Fix:** Check that the hook is registered in `.claude/settings.json` with the matcher set to "Write." If the matcher says "write" (lowercase) or "All," it may not match. The matcher is case-sensitive for tool names.

- **Symptom:** The hook logs every file write, not just compliance files. **Fix:** Check the keyword filter in the hook script. The `compliance_keywords` list must match the file names you use. If your compliance files do not contain any of those keywords in their paths, the filter never triggers. Add the relevant keyword to the file name or to the keyword list.

- **Symptom:** The ledger file overwrites itself with each entry. **Fix:** The file must be opened in append mode ("a"), not write mode ("w"). Check the `open()` call in the hook script.

- **Symptom:** The hook crashes with a permissions error. **Fix:** Check that the `outputs/` directory exists and is writable. The hook creates it with `mkdir(parents=True, exist_ok=True)`, but if the parent directory has restricted permissions, the creation may fail.

- **Symptom:** The ledger entries do not have timestamps. **Fix:** Check the `datetime.now(timezone.utc).isoformat()` call. If the import for `timezone` is missing, the timestamp field will be empty or cause an error. Both `datetime` and `timezone` must be imported from the `datetime` module.
