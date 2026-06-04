# Writing the Audit Hook

It is 11:00 Thursday morning. Your VP of Procurement stops by your desk. "I need to know exactly what Claude Code does during these batch runs. Every file it reads, every file it writes, every search it runs. If something goes wrong, I want a log I can hand to the auditors." You need a PostToolUse hook that records every tool call to a JSON log file.

## The S2P problem

When an automated pipeline processes contracts, the legal and compliance teams want a record of what happened. Which files were read? Which files were written? In what order? Without an audit trail, you cannot answer these questions after the fact. Building audit logs by hand after each run is slow and error-prone. Missing a single entry undermines the entire trail.

## What Claude Code does for you

A PostToolUse hook fires after every tool call completes. By registering an audit hook with the matcher `"*"` (all tools), you capture every action Claude Code takes. The hook appends one JSON line per tool call to `audit/audit.jsonl`. The log is append-only, so previous entries are never modified. After any batch run, you can open the log and see the complete sequence of events.

## Set up

1. Lessons 1 and 2 completed. The validation hook is registered and working.
2. Claude Code open in `Course_06_The_Guardian/practice/`.
3. The `hooks/` directory exists from Lesson 2.

## Step-by-step

### Step 1. Create the audit directory.

```
mkdir -p audit
```

You should see the `audit/` folder appear in your project.

### Step 2. Create the audit hook script.

Create the file `hooks/audit-log-hook.py` with the following content. Copy the entire block.

```python
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
    file_path = tool_input.get(
        "file_path", tool_input.get("path", "")
    )

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

    # Create audit directory if needed, then append
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


if __name__ == "__main__":
    main()
```

You should see the file `hooks/audit-log-hook.py` saved with no errors.

### Step 3. Walk through the script.

The audit hook works in three stages:

1. **Read input.** It reads JSON from stdin. Claude Code sends the tool name, tool input (including file paths), and session details.
2. **Build the log entry.** It creates a dictionary with five fields: timestamp (UTC ISO format), tool name, action type (mapped from tool name), file path (if any), and session ID.
3. **Append to log.** It opens `audit/audit.jsonl` in append mode and writes one JSON line. If the audit directory does not exist, it creates it first.

The action map translates tool names into human-readable categories. Read becomes "read". Write becomes "write". Glob and Grep both become "search". Bash becomes "execute". Anything else becomes "other".

### Step 4. Register the hook in settings.json.

```
Open .claude/settings.json and add a PostToolUse hook entry. The matcher should be "*" (all tools) and the command should be "python hooks/audit-log-hook.py".
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
      }
    ]
  }
}
```

### Step 5. Generate some audit entries.

Run a few commands so the hook has something to log.

```
List the files in data/contracts/.
```

You should see the list of 12 contract review files. The audit hook should have fired and appended a line to `audit/audit.jsonl`.

### Step 6. Read the audit log.

```
Read the file audit/audit.jsonl and show me its contents.
```

You should see one or more JSON lines. Each line has a timestamp, tool name, action, file path, and session ID. For example:

```json
{"timestamp": "2026-04-25T15:30:00.000000+00:00", "tool": "Glob", "action": "search", "file_path": "data/contracts/", "session_id": "abc123"}
```

## Worked example

**Starting files:**
- `hooks/audit-log-hook.py`: The audit script from Step 2.
- `.claude/settings.json`: Both hooks registered (validation and audit).

**What you type:**

```
Read data/contracts/review-CTR-2025-001.md and tell me the supplier name.
```

**What you should see:** Claude reads the file and tells you the supplier is Great Lakes Steel. After the command completes, a new line appears in `audit/audit.jsonl`.

**What Claude did, behind the scenes:**

1. Claude Code called the Read tool on `data/contracts/review-CTR-2025-001.md`.
2. After the Read completed, Claude Code ran the PostToolUse hook `hooks/audit-log-hook.py`.
3. The hook received the tool call details as JSON on stdin.
4. The hook built a log entry with the timestamp, tool name "Read", action "read", and the file path.
5. The hook appended the JSON line to `audit/audit.jsonl`.
6. Claude Code continued and displayed the supplier name.

## Common mistakes and how to recover

- **Symptom:** The audit log file overwrites itself on each entry, keeping only the last line. **Fix:** Check the file open mode. It must be `"a"` (append), not `"w"` (write). Using `"w"` truncates the file each time.

- **Symptom:** The hook crashes with a "FileNotFoundError" for the audit directory. **Fix:** Add `AUDIT_DIR.mkdir(parents=True, exist_ok=True)` before opening the file. The script should create the directory if it does not exist.

- **Symptom:** The audit log contains sensitive file content, not just metadata. **Fix:** Only log the tool name, action type, file path, and timestamp. Never log the full `content` field from the tool input. Audit logs should record what happened, not what was in the file.

- **Symptom:** The matcher is set to `"Write"` instead of `"*"`. **Fix:** Change the matcher to `"*"` so the hook fires on every tool call, not just writes. An audit log that only captures writes misses reads, searches, and command executions.

- **Symptom:** The log file grows very large during long sessions. **Fix:** For this course, the log file stays small. In production, rotate the log daily or set a size limit. That is outside the scope of this lesson.
