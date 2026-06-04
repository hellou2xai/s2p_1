# Lesson 02: Audit Hook for Teams

**Course:** The Team Deployment Architect
**Time:** 50 minutes
**Prerequisites:** Lesson 01 complete. Claude Code installed and signed in. Practice folder open.

---

## Part 1: The S2P problem

It is 09:15 Tuesday. Your CPO sends you a message: "The CFO wants to know which outputs our procurement team sent to Northwind Office Ltd last quarter. How quickly can you pull that?" Without an audit trail, the answer is: not quickly. You would have to ask each of eight analysts to search their email sent folders, check their SharePoint outputs, and report back. That takes most of a day, the results are incomplete, and you have no way to verify that every file is accounted for. With a team audit hook running on every analyst workspace, the answer is: about three minutes. Every Write and Bash action is logged automatically to a timestamped JSONL file. You filter by date range and file path, and the CFO has a complete list.

---

## Part 2: What Claude Code is going to do for you

Claude Code will run `hooks/audit-log.py` automatically after every Write or Bash tool call in any analyst workspace. Each log entry captures the timestamp, the tool name, the file path or command, and a placeholder for the analyst name. By the end of this lesson, you will have a working audit hook, a tested audit trail file at `audit/audit.jsonl`, and a working query prompt that filters the trail by analyst or date. The CFO question above will take three minutes, not three hours.

---

## Part 3: Set up

1. Claude Code is installed and you are signed in.
2. The course practice folder is open: `Course_12_The_Team_Deployment_Architect/practice/`.
3. `hooks/audit-log.py` exists and is readable.
4. The analyst workspace template exists at `practice/analyst-workspace-template/`.
5. `analyst-workspace-template/.claude/settings.json` exists with the PostToolUse hook configured.
6. Python 3.10 or later is installed. Confirm with: `python --version`.
7. OneDrive sync is paused. Resume when finished.

Open Claude Code in the practice folder:

```
cd "Course_12_The_Team_Deployment_Architect/practice"
claude
```

Set the read-only rule:

```
The folders shared/, hooks/, and governance/ are read-only. Do not edit any file in those folders.
Read from them freely. Save all output to workspaces/ or to a file I specify.
```

---

## Part 4: Step-by-step

**Step 1.** Open Claude Code in the practice folder.

```
cd "Course_12_The_Team_Deployment_Architect/practice"
claude
```

You should see the Claude Code prompt with `practice` in the path at the top.

**Step 2.** State the read-only rule.

```
The folders shared/, hooks/, and governance/ are read-only. Do not edit any file in those folders.
Read from them freely. Save all output to workspaces/ or to a file I specify.
```

Claude should confirm it understands. Nothing changes on disk.

**Step 3.** Ask Claude to read the audit hook and explain what it logs.

```
Read hooks/audit-log.py.
List: (1) which tool calls it logs, (2) what fields each log entry contains, (3) where it writes the log file.
Do not change the file.
```

You should see three numbered items: Write and Bash calls; timestamp, tool, file_path, analyst, session_id; `audit/audit.jsonl` in the current working directory.

If Claude says the file does not exist, confirm that `hooks/audit-log.py` is present by running `ls hooks/` in a separate terminal.

**Step 4.** Read the workspace settings to confirm the hook is wired correctly.

```
Read analyst-workspace-template/.claude/settings.json.
Confirm that audit-log.py is registered as a PostToolUse hook for Write and Bash calls.
Show me the exact JSON block that registers it.
```

You should see the PostToolUse section with `"matcher": "Write|Bash"` and `"command": "python hooks/audit-log.py"`.

If the hook is missing, open the settings file and add the block shown in the worked example below.

**Step 5.** Create a test analyst workspace and run a write action to generate an audit entry.

```
Create the folder workspaces/test_analyst/audit/.
Then write a test file: workspaces/test_analyst/outputs/test-output.txt
Content: "Test output. This line triggers the audit hook. [REVIEWED]"
```

You should see confirmation that `workspaces/test_analyst/outputs/test-output.txt` was saved.

Note: the audit hook runs automatically from `.claude/settings.json`. In this practice scenario, you can also trigger it manually by running the hook script directly (Step 6 shows how).

**Step 6.** Manually test the audit hook against a sample input to verify it writes a log entry.

```
Run this command in the terminal:
echo '{"tool_name": "Write", "tool_input": {"file_path": "workspaces/test_analyst/outputs/test-output.txt", "content": "Test."}}' | python hooks/audit-log.py
```

You should see no output on screen (the script is silent). Confirm the log was written:

```
cat audit/audit.jsonl
```

You should see one JSONL line with timestamp, tool "Write", and the file path. If the file is empty, check that Python 3.10 or later is installed and that the `audit/` directory exists in the current working directory.

**Step 7.** Ask Claude to read the audit trail and answer a simulated CFO question.

```
Read audit/audit.jsonl.
List every Write action logged, showing the timestamp and file path.
Format the output as a table with columns: timestamp, file path.
```

You should see a table with at least one row from Step 6. If the table is empty, confirm that `audit/audit.jsonl` exists and has at least one line.

**Step 8.** Update the audit hook placeholder so it logs a real analyst name instead of `ANALYST_NAME_PLACEHOLDER`.

```
Read hooks/audit-log.py.
The entry currently uses the string "ANALYST_NAME_PLACEHOLDER" for the analyst field.
In a new file at workspaces/test_analyst/hooks/audit-log.py,
replace that placeholder with the string "test_analyst".
Keep every other line identical.
```

You should see confirmation that `workspaces/test_analyst/hooks/audit-log.py` was created with the analyst name filled in.

---

## Part 5: Worked example, end to end

**Scenario.** Marcus Davis in Dallas writes a spend analysis output for the Logistics category. The CFO asks the next morning which files Marcus sent out on 2026-04-25.

**Starting files:**

- `hooks/audit-log.py`: canonical audit hook.
- `analyst-workspace-template/.claude/settings.json`: hook wired to PostToolUse.
- `workspaces/marcus_davis/`: Marcus's workspace, set up by the onboarding script.

**Prompts, in order:**

**Prompt 1.** Set context and read-only rule.

```
The folders shared/, hooks/, and governance/ are read-only. Do not edit any file in those folders.
I am working in workspaces/marcus_davis/.
```

**Prompt 2.** Generate a logistics spend output (this triggers the audit hook automatically).

```
Write a short spend summary to workspaces/marcus_davis/outputs/logistics-spend-2026-04-25.md.
Content: "Logistics category spend for Q1 2026: $5.3M total. Top supplier: Apex Freight Solutions at $2.1M (39.6% of category). [REVIEWED]"
```

Expected output: Confirmation that the file was saved. The PostToolUse hook logs the action to `audit/audit.jsonl`.

**Prompt 3.** Answer the CFO question.

```
Read audit/audit.jsonl.
Show every Write action where the analyst field is "marcus_davis" and the timestamp starts with "2026-04-25".
Format as a table: timestamp, file path.
```

Expected output:

| timestamp | file path |
|---|---|
| 2026-04-25T14:32:11Z | workspaces/marcus_davis/outputs/logistics-spend-2026-04-25.md |

**Short extract from `audit/audit.jsonl`:**

```json
{"timestamp": "2026-04-25T14:32:11+00:00", "tool": "Write", "file_path": "workspaces/marcus_davis/outputs/logistics-spend-2026-04-25.md", "analyst": "marcus_davis", "session_id": "SESSION_PLACEHOLDER"}
```

**Finished artifact:** `audit/audit.jsonl`. A growing append-only log of every Write and Bash action across all analyst workspaces.

---

## Part 6: Common mistakes and how to recover

- **Symptom:** The audit hook runs but the log is empty. **Fix:** Check that the `audit/` directory exists in the same folder where Claude Code is running. The script creates it with `mkdir(exist_ok=True)`, but only if it has write permission. Run `mkdir -p audit` by hand if needed.

- **Symptom:** Python throws `ModuleNotFoundError` when the hook runs. **Fix:** The hook uses only the standard library (json, sys, datetime, pathlib). If this error appears, the wrong Python is running. Confirm with `which python` and `python --version`. The hook needs Python 3.6 or later.

- **Symptom:** The analyst name in every log entry is `ANALYST_NAME_PLACEHOLDER`. **Fix:** The onboarding script should replace this placeholder for each analyst workspace. Run Step 8 for each workspace that was not updated. A future onboarding script improvement is to replace the placeholder automatically during `onboard-analyst.sh`.

- **Symptom:** The audit log grows very large because it logs every Bash command including minor ones. **Fix:** Add a filter list to the hook: skip commands shorter than 20 characters (usually short diagnostic commands). Do this in each analyst's personal copy of the hook, not in the canonical `hooks/audit-log.py`.

- **Symptom:** A manager accidentally deletes `audit/audit.jsonl`. **Fix:** The file is append-only by policy, but the OS does not enforce this. Keep a daily copy to a network share. Add a note to the governance documents: "audit.jsonl is append-only. Deletion requires Operations Manager approval and a log entry."
