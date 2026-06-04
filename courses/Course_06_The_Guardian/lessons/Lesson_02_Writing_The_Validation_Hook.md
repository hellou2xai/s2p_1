# Writing the Validation Hook

It is 10:00 Thursday morning. Your team lead's message is still on your screen: "No report should save to outputs/ unless it passes validation." You need a PreToolUse hook that intercepts every file write, checks the report structure, and blocks the save if anything is wrong. The hook must catch the six flaw types your team found: missing risk assessment, invalid risk level, missing supplier name, missing key clauses, high risk with no recommendation, and empty clause references.

## The S2P problem

Contract review reports follow a standard structure: parties, term, value, risk assessment, key clauses, and recommendation. When any of these sections is missing, incomplete, or uses an invalid value, the report fails legal review. Catching these problems after the report is filed costs rework time and delays the contract pipeline. Catching them before the file saves costs nothing.

## What Claude Code does for you

A PreToolUse hook on the Write tool runs your validation script automatically every time Claude Code tries to save a file. If the file fails validation, the hook blocks the write and tells Claude Code exactly what is wrong. Claude Code sees the error and can fix the report before trying again. No manual review needed.

## Set up

1. Lesson 1 completed. `.claude/settings.json` exists with the empty hooks structure.
2. Claude Code open in `Course_06_The_Guardian/practice/`.
3. The `hooks/` directory created (you will create it in Step 1 if it does not exist).

## Step-by-step

### Step 1. Create the hooks directory.

```
mkdir -p hooks
```

You should see the `hooks/` folder appear in your project.

### Step 2. Create the validation hook script.

Create the file `hooks/validate-report-hook.py` with the following content. Copy the entire block.

```python
import json
import re
import sys


VALID_RISK_LEVELS = {"Low", "Medium", "High", "Critical"}

REQUIRED_SECTIONS = [
    ("Parties", r"\*\*Parties:\*\*"),
    ("Term", r"\*\*Term:\*\*"),
    ("Value", r"\*\*(Annual )?Value:\*\*"),
    ("Risk Assessment", r"\*\*Risk Level:\*\*"),
    ("Key Clauses", r"\*\*Key Clauses:\*\*"),
    ("Recommendation", r"\*\*Recommendation:\*\*"),
]


def validate_report(content):
    errors = []

    # Check required sections
    for section_name, pattern in REQUIRED_SECTIONS:
        if not re.search(pattern, content):
            errors.append(f"Missing required section: {section_name}")

    # Check risk level value
    risk_match = re.search(r"\*\*Risk Level:\*\*\s*(\w+)", content)
    if risk_match:
        risk_value = risk_match.group(1).strip().rstrip(".")
        if risk_value not in VALID_RISK_LEVELS:
            errors.append(
                f"Invalid risk level: '{risk_value}'. "
                f"Must be one of: {', '.join(sorted(VALID_RISK_LEVELS))}"
            )

    # Check supplier name in parties section
    parties_match = re.search(
        r"\*\*Parties:\*\*.*?and\s+(.*?)\s*\(Supplier\)", content
    )
    if parties_match:
        supplier_name = parties_match.group(1).strip()
        if not supplier_name or len(supplier_name) < 2:
            errors.append(
                "Supplier name is missing or empty in Parties section"
            )

    # Check key clauses are not empty
    clauses_match = re.search(
        r"\*\*Key Clauses:\*\*\s*\n(.*?)(?=\n\*\*|\Z)", content, re.DOTALL
    )
    if clauses_match:
        clauses_content = clauses_match.group(1).strip()
        if not clauses_content or clauses_content == "(none reviewed)":
            errors.append(
                "Key Clauses section is empty or contains no clause references"
            )

    # Check high/critical risk has recommendation
    if risk_match:
        risk_value = risk_match.group(1).strip().rstrip(".")
        if risk_value in {"High", "Critical"}:
            if not re.search(r"\*\*Recommendation:\*\*", content):
                errors.append(
                    f"Risk level is {risk_value} but no Recommendation "
                    f"section found. High and Critical risk contracts "
                    f"require a specific recommendation."
                )

    return errors


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print(json.dumps({"decision": "approve"}))
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only validate Write tool calls to outputs/
    if tool_name != "Write":
        print(json.dumps({"decision": "approve"}))
        return

    file_path = tool_input.get("file_path", "")
    if "outputs/" not in file_path and "outputs\\" not in file_path:
        print(json.dumps({"decision": "approve"}))
        return

    content = tool_input.get("content", "")
    errors = validate_report(content)

    if errors:
        error_message = (
            "Report validation failed. Fix these issues before saving:\n"
        )
        for i, error in enumerate(errors, 1):
            error_message += f"  {i}. {error}\n"
        print(json.dumps({"decision": "block", "reason": error_message}))
    else:
        print(json.dumps({"decision": "approve"}))


if __name__ == "__main__":
    main()
```

You should see the file `hooks/validate-report-hook.py` saved with no errors.

### Step 3. Walk through what the script does.

The script works in four stages:

1. **Read input.** It reads JSON from stdin. Claude Code sends the tool name, the file path, and the file content.
2. **Filter.** It checks whether the tool is `Write` and the path contains `outputs/`. If not, it approves immediately. This means the hook only validates reports headed for the outputs folder.
3. **Validate.** It runs five checks: required sections present, valid risk level, supplier name not empty, key clauses not empty, and high/critical risk has a recommendation.
4. **Respond.** If any check fails, it prints `{"decision": "block", "reason": "..."}`. If all checks pass, it prints `{"decision": "approve"}`.

### Step 4. Register the hook in settings.json.

```
Open .claude/settings.json and add a PreToolUse hook entry. The matcher should be "Write" and the command should be "python hooks/validate-report-hook.py".
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
    "PostToolUse": []
  }
}
```

### Step 5. Test with a flawed report.

Ask Claude Code to save one of the flawed contract reviews to outputs/.

```
Read data/contracts/review-CTR-2025-003.md and save it to outputs/review-CTR-2025-003.md exactly as it is. Do not change anything in the file.
```

You should see the hook block the write with an error message like: "Report validation failed. Fix these issues before saving: 1. Missing required section: Risk Assessment."

### Step 6. Test with a valid report.

```
Read data/contracts/review-CTR-2025-001.md and save it to outputs/review-CTR-2025-001.md exactly as it is. Do not change anything.
```

You should see the file save successfully. The hook approved it because CTR-2025-001 has all required sections, a valid risk level, a named supplier, and a recommendation.

## Worked example

**Starting files:**
- `data/contracts/review-CTR-2025-006.md`: Has risk level "Extreme" (invalid).
- `hooks/validate-report-hook.py`: The validation script from Step 2.
- `.claude/settings.json`: The hook registered from Step 4.

**What you type:**

```
Read data/contracts/review-CTR-2025-006.md and save it to outputs/review-CTR-2025-006.md exactly as written.
```

**What you should see:** Claude Code reports that the write was blocked. The error message reads: "Invalid risk level: 'Extreme'. Must be one of: Critical, High, Low, Medium."

**What Claude did, behind the scenes:**

1. Read the contents of `data/contracts/review-CTR-2025-006.md`.
2. Attempted to write the content to `outputs/review-CTR-2025-006.md`.
3. Before the write executed, Claude Code ran `hooks/validate-report-hook.py` and passed the file path and content as JSON on stdin.
4. The hook found the risk level "Extreme" and checked it against the set `{Low, Medium, High, Critical}`. It did not match.
5. The hook returned `{"decision": "block", "reason": "Invalid risk level: 'Extreme'..."}`.
6. Claude Code received the block response and did not write the file. It showed you the error message instead.

## Common mistakes and how to recover

- **Symptom:** The hook never fires. Claude saves the file without any validation. **Fix:** Check that the matcher in settings.json is `"Write"` with a capital W. Also check that the command path `"python hooks/validate-report-hook.py"` is correct relative to your project root.

- **Symptom:** The hook blocks every file, even valid ones. **Fix:** Check the `outputs/` path filter in the script. If the condition checks for a different path string, the filter may not match. Print the file_path to stderr for debugging: `print(file_path, file=sys.stderr)`.

- **Symptom:** The hook crashes with "json.decoder.JSONDecodeError". **Fix:** The script must read from `sys.stdin`, not from a file. Check that the `main()` function starts with `input_data = json.loads(sys.stdin.read())`.

- **Symptom:** Claude Code says the hook returned an invalid response. **Fix:** The response must be valid JSON with a `"decision"` field set to either `"approve"` or `"block"`. If blocking, include a `"reason"` field. Nothing else should be printed to stdout.

- **Symptom:** The hook approves a file that writes to a path like `./outputs/review.md` (with a leading `./`). **Fix:** The path filter checks for `"outputs/"` in the string. The `./` prefix still contains `outputs/`, so this should work. If it does not, normalize the path with `os.path.normpath()` before checking.

- **Symptom:** The hook does not catch files written outside outputs/. **Fix:** That is correct behavior. The hook is designed to validate only files going to outputs/. Files written to drafts/ or other folders pass through without validation.
