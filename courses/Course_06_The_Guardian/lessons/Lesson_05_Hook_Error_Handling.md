# Hook Error Handling

It is 14:30 Thursday afternoon. You run a quick batch test of five contract reviews. Halfway through, Claude Code stops with a Python traceback. The audit hook crashed because one tool call returned unexpected JSON. The batch halted. Two reports that passed validation never made it to outputs/. You realize that a hook crash can block the entire pipeline. You need defensive error handling in every hook.

## The S2P problem

In production, hooks run on every tool call. A single unexpected input, a missing field, or a malformed JSON payload can crash a hook script. When a PreToolUse hook crashes, Claude Code cannot get a response, and the tool call may be blocked by default. When a PostToolUse hook crashes, the log entry is lost and downstream actions (like risk alerts) never fire. Either way, the batch is disrupted. Defensive hooks handle errors gracefully so the pipeline keeps moving.

## What Claude Code does for you

Claude Code runs your hook scripts as external processes. If a hook script exits with an error (non-zero exit code) or returns invalid JSON, Claude Code treats the result differently depending on the hook type. For PreToolUse, an unclear result may block the tool call. For PostToolUse, the tool call already happened, but the hook's side effects (logging, alerting) are lost. Adding try/except blocks and default responses to your hooks ensures they fail gracefully instead of crashing the pipeline.

## Set up

1. Lessons 1 through 4 completed. All three hooks are registered and working.
2. Claude Code open in `Course_06_The_Guardian/practice/`.
3. The three hook scripts in `hooks/`.

## Step-by-step

### Step 1. Understand the two failure modes.

There are two ways a hook can fail:

1. **The input is not valid JSON.** Claude Code sends something the hook cannot parse. The `json.loads()` call throws a `json.JSONDecodeError`.
2. **A required field is missing.** The JSON is valid, but a field like `tool_input` or `file_path` is absent. The `.get()` call returns `None`, and a later operation (like string matching) crashes with a `TypeError` or `AttributeError`.

Each hook needs to handle both cases.

### Step 2. Review the existing error handling in the validation hook.

```
Read hooks/validate-report-hook.py and show me the try/except block in the main() function.
```

You should see the existing handler:

```python
try:
    input_data = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    print(json.dumps({"decision": "approve"}))
    return
```

This is the right pattern for a PreToolUse hook. If the input cannot be parsed, the hook approves by default. The reasoning: it is better to let a report through unchecked than to block every write because the hook itself is broken.

### Step 3. Add a top-level try/except to the validation hook.

The existing handler covers bad JSON input. But what if a regex crashes, or a field is an unexpected type? Wrap the entire main function body in a try/except.

```
Open hooks/validate-report-hook.py and wrap the entire body of main() in a try/except block. If any exception occurs, print {"decision": "approve"} and return. Add a comment explaining why: a broken hook should not block production writes. Print the error to stderr for debugging.
```

The updated `main()` function should look like this:

```python
def main():
    try:
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

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
                "Report validation failed. "
                "Fix these issues before saving:\n"
            )
            for i, error in enumerate(errors, 1):
                error_message += f"  {i}. {error}\n"
            print(json.dumps({
                "decision": "block",
                "reason": error_message,
            }))
        else:
            print(json.dumps({"decision": "approve"}))

    except Exception as e:
        # A broken hook should not block production writes.
        # Log the error for debugging, then approve.
        print(f"Hook error: {e}", file=sys.stderr)
        print(json.dumps({"decision": "approve"}))
```

You should see the file updated with the new try/except structure.

### Step 4. Add error handling to the audit hook.

```
Open hooks/audit-log-hook.py and wrap the entire body of main() in a try/except block. If any exception occurs, print the error to stderr and return silently. A PostToolUse hook that crashes should not affect the pipeline. It just means one log entry is lost.
```

The updated `main()` function should look like this:

```python
def main():
    try:
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get("tool_name", "unknown")
        tool_input = input_data.get("tool_input", {})

        file_path = tool_input.get(
            "file_path", tool_input.get("path", "")
        )

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

        AUDIT_DIR.mkdir(parents=True, exist_ok=True)
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    except Exception as e:
        # A missed log entry is acceptable.
        # A crashed hook that blocks the pipeline is not.
        print(f"Audit hook error: {e}", file=sys.stderr)
```

You should see the file updated.

### Step 5. Add error handling to the risk alert hook.

```
Open hooks/risk-alert-hook.py and wrap the entire body of main() in a try/except block. If any exception occurs, print the error to stderr and return silently. A missed alert is a problem, but a crashed hook that stops the batch is worse.
```

The pattern is the same as the audit hook. Wrap everything in `try:`, catch `Exception`, print to stderr, and return.

You should see the file updated with the try/except structure.

### Step 6. Test by feeding invalid input.

```
Run this command to test the validation hook with invalid JSON input:
echo "this is not json" | python hooks/validate-report-hook.py
```

You should see the hook print `{"decision": "approve"}` to stdout. It did not crash. It defaulted to approve because it could not parse the input.

```
Run this command to test the audit hook with invalid JSON input:
echo "this is not json" | python hooks/audit-log-hook.py
```

You should see no output on stdout. The hook exited silently. No log entry was written, but no crash occurred.

## Worked example

**Starting files:**
- `hooks/validate-report-hook.py`: Updated with top-level try/except.
- `hooks/audit-log-hook.py`: Updated with top-level try/except.
- `hooks/risk-alert-hook.py`: Updated with top-level try/except.

**What you type:**

```
echo "this is not json" | python hooks/validate-report-hook.py
```

**What you should see:** The output `{"decision": "approve"}` printed to stdout. No crash. No traceback.

**What Claude did, behind the scenes:**

1. The shell piped the string "this is not json" to the script's stdin.
2. The script tried `json.loads("this is not json")`, which raised a `json.JSONDecodeError`.
3. The outer try/except caught the exception.
4. The script printed the error to stderr for debugging.
5. The script printed `{"decision": "approve"}` to stdout, telling Claude Code to allow the tool call.
6. The script exited cleanly with exit code 0.

## Common mistakes and how to recover

- **Symptom:** The PreToolUse hook blocks all writes after you add error handling, because the except block prints `{"decision": "block"}` instead of `{"decision": "approve"}`. **Fix:** Always default to approve in the except block of a PreToolUse hook. A broken hook should not stop production work.

- **Symptom:** The PostToolUse hook prints output to stdout in the except block. **Fix:** PostToolUse hooks do not need to print anything. If they crash, just log to stderr and return. Printing unexpected output to stdout can confuse Claude Code.

- **Symptom:** You catch only `json.JSONDecodeError` and the hook still crashes on a `KeyError`. **Fix:** Use a broad `except Exception` at the top level. You can keep specific handlers inside for logging, but the outer handler must catch everything.

- **Symptom:** You removed the original `json.JSONDecodeError` handler and now the outer handler catches it differently. **Fix:** You can remove the inner handler if the outer one covers it. The important thing is that every possible exception path ends with either an approve response (PreToolUse) or a silent return (PostToolUse).

- **Symptom:** Errors are silently swallowed and you cannot debug. **Fix:** Always print the exception to stderr with `print(f"Hook error: {e}", file=sys.stderr)`. Stderr output does not interfere with the JSON response on stdout, but it shows up in your terminal for debugging.
