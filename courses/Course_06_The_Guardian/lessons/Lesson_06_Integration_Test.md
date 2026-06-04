# Integration Test

It is 15:30 Thursday afternoon. All three hooks are registered: the validation gate, the audit log, and the risk alert. Time to run the full batch of 12 contract reviews through the pipeline and confirm that everything works together. Six reports should save successfully. Six should be blocked by the validation hook. The audit log should capture every tool call. Alert files should appear for High and Critical risk contracts that pass validation.

## The S2P problem

A batch contract review pipeline is only as reliable as its end-to-end test. Individual hooks may pass unit tests but fail when they run together. The validation hook might approve a file, but the audit hook might crash on the same input. The risk alert hook might fire for a blocked write that never actually saved. Running all 12 reviews through the full pipeline in one session proves that the hooks work together, in sequence, without conflicts.

## What Claude Code does for you

Claude Code runs all registered hooks automatically on every tool call. You do not need to call each hook by hand. When you ask Claude Code to save a file, the PreToolUse validation hook fires first. If it approves, the file saves, and then both PostToolUse hooks fire (audit log first, risk alert second). If it blocks, the file does not save, and the PostToolUse hooks still fire for the attempted write (recording the blocked action in the audit log). You just ask Claude Code to process the files. The hooks handle the rest.

## Set up

1. Lessons 1 through 5 completed. All three hooks are registered with error handling.
2. Claude Code open in `Course_06_The_Guardian/practice/`.
3. The `outputs/`, `audit/`, and `alerts/` directories exist.
4. Clear any previous test files:

```
Delete all files in outputs/, audit/, and alerts/ so we start clean.
```

You should see empty `outputs/`, `audit/`, and `alerts/` directories.

## Step-by-step

### Step 1. Confirm all three hooks are registered.

```
Read .claude/settings.json and show me the registered hooks.
```

You should see three hook entries:
- PreToolUse: `validate-report-hook.py` on matcher `"Write"`.
- PostToolUse: `audit-log-hook.py` on matcher `"*"`.
- PostToolUse: `risk-alert-hook.py` on matcher `"Write"`.

If any hook is missing, go back to the lesson where you registered it and add it.

### Step 2. Process all 12 contract reviews.

Ask Claude Code to read each contract review from `data/contracts/` and save it to `outputs/`.

```
Read each of the 12 contract review files in data/contracts/. For each one, save it to outputs/ with the same filename. Do not modify the file contents. Save them one at a time and report what happens with each file.
```

You should see Claude Code attempt to save each file. Some will succeed. Some will be blocked by the validation hook with specific error messages.

### Step 3. Check the results: which files were blocked.

The six flawed files should be blocked with these specific errors:

| File | Expected error |
|---|---|
| review-CTR-2025-003.md | Missing required section: Risk Assessment |
| review-CTR-2025-006.md | Invalid risk level: 'Extreme' |
| review-CTR-2025-008.md | Supplier name is missing or empty in Parties section |
| review-CTR-2025-010.md | Missing required section: Key Clauses |
| review-CTR-2025-011.md | Missing required section: Recommendation (Critical risk with no recommendation) |
| review-CTR-2025-012.md | Key Clauses section is empty or contains no clause references |

```
List the files in outputs/. Tell me which of the 12 were saved and which were blocked.
```

You should see six files in `outputs/`:
- review-CTR-2025-001.md
- review-CTR-2025-002.md
- review-CTR-2025-004.md
- review-CTR-2025-005.md
- review-CTR-2025-007.md
- review-CTR-2025-009.md

The other six were blocked. If you see more or fewer than six, check the validation hook's regex patterns against the flawed files.

### Step 4. Check the audit log.

```
Read audit/audit.jsonl and count the entries. Show me the first three and last three lines.
```

You should see multiple log entries. Every tool call Claude Code made during the batch (reads, writes, searches) should have a corresponding entry. Each entry has a timestamp, tool name, action type, and file path.

The log should include entries for both successful writes and blocked write attempts. The blocked attempts still generate audit entries because the PostToolUse hook fires for the tool call regardless of the PreToolUse outcome.

### Step 5. Check the risk alerts.

```
List the files in alerts/ and show me the contents of each alert file.
```

You should see alert files only for contracts that both passed validation and had a High or Critical risk level. Based on the practice data, expect alerts for contracts like CTR-2025-002 (Critical risk, Heartland Polymers).

Contracts that were blocked by the validation hook should not have alert files, because the file was never written to outputs/. Contracts that passed validation but have Low or Medium risk should not have alert files either.

### Step 6. Verify the end-to-end summary.

```
Give me a summary table: for each of the 12 contract review files, show the contract ID, supplier name, risk level, whether it was saved or blocked, the block reason (if blocked), and whether an alert was generated.
```

You should see a table with 12 rows. Six rows show "saved" with no block reason. Six rows show "blocked" with the specific validation error. Alert files appear only for saved contracts with High or Critical risk.

## Worked example

**Starting state:**
- 12 contract review files in `data/contracts/`.
- Three hooks registered in `.claude/settings.json`.
- Empty `outputs/`, `audit/`, and `alerts/` directories.

**What you type:**

```
Read each of the 12 contract review files in data/contracts/. For each one, save it to outputs/ with the same filename. Do not modify the contents. Process them one at a time.
```

**What you should see:** Claude Code processes each file and reports the result. Six files save successfully. Six are blocked. For each blocked file, Claude shows the validation error.

**What Claude did, behind the scenes:**

1. Claude Code read each contract review file from `data/contracts/`.
2. For each file, Claude Code attempted a Write tool call to `outputs/`.
3. Before each write, the PreToolUse validation hook ran. It checked the content for required sections, valid risk level, named supplier, non-empty key clauses, and recommendation for high-risk contracts.
4. For the six valid files, the hook returned `{"decision": "approve"}`. The file was written.
5. For the six flawed files, the hook returned `{"decision": "block", "reason": "..."}`. The file was not written. Claude Code displayed the error.
6. After each tool call (successful or blocked), the PostToolUse audit hook appended a log entry to `audit/audit.jsonl`.
7. After each successful write, the PostToolUse risk alert hook checked the risk level. For High or Critical risk contracts, it wrote an alert file to `alerts/`.

## Common mistakes and how to recover

- **Symptom:** All 12 files are blocked, including the valid ones. **Fix:** The validation hook may have a regex error that flags every file. Test the hook manually: `cat data/contracts/review-CTR-2025-001.md | python -c "import json,sys; print(json.dumps({'tool_name':'Write','tool_input':{'file_path':'outputs/test.md','content':sys.stdin.read()}}))" | python hooks/validate-report-hook.py`. If it blocks a valid file, check each regex pattern in `REQUIRED_SECTIONS`.

- **Symptom:** The audit log is empty after the batch run. **Fix:** Check that the audit hook matcher is `"*"` (not `"Write"`). Also check that `audit/audit.jsonl` is the correct path. Run `cat audit/audit.jsonl` to see if entries exist outside Claude Code.

- **Symptom:** Alert files appear for contracts that were blocked by validation. **Fix:** This should not happen if the hooks are ordered correctly. The risk alert hook only fires on successful writes. If a PreToolUse hook blocks the write, the file is never saved, and the PostToolUse Write hooks should not fire for that file. Check that your risk alert hook filters on `tool_name == "Write"`.

- **Symptom:** Only three hooks registered but you expected three entries in settings.json. **Fix:** Read `.claude/settings.json` carefully. The PreToolUse array should have one entry (validation). The PostToolUse array should have two entries (audit and risk alert). If any are missing, add them following the format from the earlier lessons.

- **Symptom:** The batch takes a long time because hooks run sequentially. **Fix:** This is expected. Each write triggers up to three hook scripts (one PreToolUse, two PostToolUse). For 12 files, that is up to 36 hook executions. On a typical machine this should complete in under a minute. If it takes longer, check for infinite loops or blocking input reads in your hook scripts.
