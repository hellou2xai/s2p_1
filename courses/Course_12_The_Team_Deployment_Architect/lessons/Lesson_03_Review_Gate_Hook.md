# Lesson 3: The Review Gate Hook

**Time:** 25 minutes.

## The analyst sends a brief to the CPO without review

It is 14:00 on Wednesday. Analyst Lisa Chen finishes a contract recommendation and saves it to `Outputs/contract_recommendation.md`. The file is stakeholder-ready. It will go to the CPO. But nobody reviewed it. Lisa's manager, David Park, has not seen the numbers. In your team of eight analysts, this has happened twice in the last month. Both times, the CPO found errors. In this lesson, you build a PreToolUse hook that blocks any file write to the Outputs folder until a reviewer has added a timestamp and their name to the file.

## What Claude Code is going to do for you

You will create a review gate hook that fires before Claude Code writes any file to the `Outputs/` folder. The hook checks whether the file content includes a review block: a reviewer name and a timestamp. If the block is missing, the hook blocks the write and tells the analyst to get a review first. Files in `Drafts/` are not affected. Only `Outputs/` (the stakeholder-ready folder) has the gate.

## Set up

1. Navigate to the practice folder:

```
cd "Course_12_The_Team_Deployment_Architect/practice"
```

2. Start Claude Code:

```
claude
```

3. Confirm the hooks folder has the review gate script:

```
ls hooks/review-gate.py
```

You should see the file listed.

## Step-by-step

### Step 1: Read the review gate script

```
Read hooks/review-gate.py and explain what it does.
```

**What you should see.** Claude explains: the script reads the file content from stdin, checks for a review block (a section containing "Reviewed by:" and a date in YYYY-MM-DD format), and exits with code 1 if the block is missing. It only triggers for files whose path includes `Outputs/`.

### Step 2: Test without the review block

Quit Claude and register the hook first:

```
/quit
```

Open `.claude/settings.json` and add the review gate to PreToolUse. If you already have hooks, add this entry to the existing array:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "write_file",
        "command": "python hooks/review-gate.py"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "write_file",
        "command": "python hooks/audit-log.py"
      }
    ]
  }
}
```

Save the file. Start Claude Code:

```
claude
```

Try to write a file to Outputs without a review block:

```
Write "Contract recommendation: Renew the CleanCorp Services contract at $840,000 for 24 months." to Outputs/contract_recommendation.md.
```

**What you should see.** The review gate hook fires and prints: "BLOCKED: File in Outputs/ is missing a review block. Add a section with 'Reviewed by: [Name]' and 'Review date: YYYY-MM-DD' before saving to Outputs/." The file is not written.

### Step 3: Write to Drafts instead (should pass)

```
Write "Contract recommendation: Renew the CleanCorp Services contract at $840,000 for 24 months." to Drafts/contract_recommendation.md.
```

**What you should see.** The file is written without any block. The review gate only applies to `Outputs/`. Drafts are working files and do not need review.

### Step 4: Add the review block and write to Outputs

```
Write the following to Outputs/contract_recommendation.md:

# Contract Recommendation: CleanCorp Services

Renew the CleanCorp Services facilities contract at $840,000 annually for 24 months. CleanCorp scored 91/100 on the most recent scorecard. The contract expires 2026-05-10.

## Review

Reviewed by: David Park
Review date: 2026-04-25
```

**What you should see.** The review gate hook fires, finds both "Reviewed by:" and a valid date, and allows the write. The file is saved to `Outputs/`.

### Step 5: Verify the file was written

```
Read Outputs/contract_recommendation.md. Does it have the review block at the bottom?
```

**What you should see.** Claude confirms the file exists and contains the review block with David Park's name and the date.

### Step 6: Check the audit log

```
Read governance/audit-log.csv. Does the most recent entry show the Outputs/ file write?
```

**What you should see.** The audit log has an entry for the Outputs write. Both hooks worked in sequence: the review gate checked for the review block (PreToolUse), then the audit hook logged the write (PostToolUse).

### Step 7: Quit Claude

```
/quit
```

## Worked example: the full review flow

**The prompt you type:**

```
Write a contract recommendation for CleanCorp Services to Outputs/contract_recommendation.md. Include a review block with reviewer name and date. The reviewer is David Park. Today's date is 2026-04-25.
```

**Folder layout:**

```
practice/
├── Drafts/
│   └── contract_recommendation.md    (working copy, no gate)
├── Outputs/
│   └── contract_recommendation.md    (stakeholder copy, gate required)
├── hooks/
│   ├── review-gate.py                (PreToolUse: checks for review block)
│   └── audit-log.py                  (PostToolUse: logs the write)
└── governance/
    └── audit-log.csv                  (append-only log)
```

**What you should see:**

The file in Outputs contains the recommendation, the supplier name (CleanCorp Services), the contract value ($840,000), and a review block:

```
Reviewed by: David Park
Review date: 2026-04-25
```

**What Claude did behind the scenes:**

1. Claude drafted the contract recommendation with all required fields.
2. It added the review block at the bottom with the reviewer's name and date.
3. Before writing the file, the PreToolUse hook read the content from stdin.
4. The hook checked for "Reviewed by:" and found "David Park."
5. The hook checked for a date pattern (YYYY-MM-DD) and found "2026-04-25."
6. Both checks passed. The hook exited with code 0.
7. Claude wrote the file to `Outputs/contract_recommendation.md`.
8. The PostToolUse audit hook logged the write to `governance/audit-log.csv`.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| The review gate blocks every file, including Drafts. | The hook must check the file path. Only block writes to `Outputs/`. If the path does not contain `Outputs/`, exit with code 0 immediately. |
| An analyst adds "Reviewed by: TBD" to pass the gate. | Update the hook to reject "TBD," "N/A," or empty names. Check that the reviewer name has at least two words. |
| The date format is wrong (04/25/2026 instead of 2026-04-25). | The hook should require YYYY-MM-DD format. Update the regex to match `\d{4}-\d{2}-\d{2}`. Reject other date formats. |
| The review block is at the top of the file and the CPO asks why. | Convention: put the review block at the bottom so it does not distract from the content. Update the hook to check the last 10 lines of the file, not the entire file. |
| The PreToolUse hook and the PostToolUse hook both fire errors. | PreToolUse fires first. If it blocks, the file is not written, so PostToolUse should not fire. If both fire, check that the PreToolUse hook exits with code 1 (not 0) on failure. |

## You are done with Lesson 3 when

- The review gate blocks writes to `Outputs/` that lack a review block.
- Writes to `Drafts/` are not affected by the gate.
- You wrote a file to `Outputs/` with a valid review block and it passed.
- The audit log recorded the write.

Move to Lesson 4 when ready.
