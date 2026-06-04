# The Four Hook Types

It is 09:15 on a Thursday. Your team lead just reviewed the 12 contract review reports your pipeline produced this morning. In five minutes she found three problems: CTR-2025-003 has no risk assessment section, CTR-2025-006 uses a risk level of "Extreme" that is not in your taxonomy, and CTR-2025-011 is flagged Critical but has no recommendation. She sends a message: "These reports cannot go to Legal in this state. We need a quality gate."

## The S2P problem

Contract review reports leave the pipeline unchecked. A report with a missing section, an invalid risk level, or no recommendation can reach the legal team and cause delays, rework, or missed risk. Manual review of every report before filing takes 10 to 15 minutes per document. At 12 documents per batch, that is two to three hours of checking that a script could handle in seconds.

## What Claude Code does for you

Claude Code supports hooks: scripts that run automatically before or after every tool call. You register a hook once. From that point on, Claude Code calls your script every time the matching tool fires. No manual checking. No missed reports. The quality gate runs itself.

## Set up

1. Claude Code installed and signed in.
2. The course folder `Course_06_The_Guardian/practice/` open in your terminal.
3. The practice data files in `data/` (contract register, clause taxonomy, 12 contract reviews).

## Step-by-step

### Step 1. Open Claude Code in the practice folder.

```
cd Course_06_The_Guardian/practice
claude
```

You should see the Claude Code prompt with the folder path at the top.

### Step 2. Ask Claude Code where hooks are registered.

```
Where do I register hooks in Claude Code? Show me the file path and format.
```

Claude should explain that hooks are registered in `.claude/settings.json` at the project root. It will describe the JSON structure with `PreToolUse` and `PostToolUse` arrays.

### Step 3. Look at the four hook types.

Claude Code has four hook types. Each one fires at a different moment and can do different things.

| Hook type | When it fires | What it can do | Use it for |
|---|---|---|---|
| PreToolUse | Before a tool call executes | Approve, block, or modify the call | Validation gates. Stop a bad file from saving. |
| PostToolUse | After a tool call completes | Read the result, log it, trigger actions | Audit logs, alerts, notifications. |
| Stop | When a Claude Code session ends | Run cleanup, write summaries | Session reports, cleanup scripts. |
| Notification | When Claude Code emits an event | React to events like errors | Error monitoring, status updates. |

In this course you build one PreToolUse hook and two PostToolUse hooks. The Stop and Notification types are covered in Course 7.

### Step 4. Open the settings.json file to see the hook registration format.

```
Read the file .claude/settings.json if it exists. If it does not exist, show me an empty settings.json with the hooks structure.
```

Claude should show you a JSON structure like this:

```json
{
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": []
  }
}
```

### Step 5. Understand the matcher and command fields.

Each hook entry has two key fields:

- **matcher**: which tool triggers the hook. Use `"Write"` to fire only on file writes. Use `"*"` to fire on every tool call.
- **command**: the shell command Claude Code runs. For example, `"python hooks/validate-report-hook.py"`.

A PreToolUse hook on the Write tool looks like this:

```json
{
  "matcher": "Write",
  "hooks": [
    {
      "type": "command",
      "command": "python hooks/validate-report-hook.py"
    }
  ]
}
```

Claude Code runs the command, passes tool call details as JSON on stdin, and reads the hook's JSON response from stdout.

## Worked example

**Starting state:** An empty `.claude/settings.json` file.

**What you type:**

```
Create the file .claude/settings.json with an empty hooks structure. Include both PreToolUse and PostToolUse as empty arrays. Do not add any hook entries yet.
```

**What you should see:** Claude creates `.claude/settings.json` with the structure shown in Step 4. The file is valid JSON. Both arrays are empty.

**What Claude did, behind the scenes:**

1. Checked whether `.claude/settings.json` already existed.
2. Created the `.claude/` directory if it did not exist.
3. Wrote a JSON file with a `hooks` object containing two empty arrays: `PreToolUse` and `PostToolUse`.
4. Saved the file to disk. No hooks are active yet because both arrays are empty.

## Common mistakes and how to recover

- **Symptom:** You register a PreToolUse hook but it never fires. **Fix:** Check the matcher field. If you wrote `"matcher": "write"` (lowercase), change it to `"matcher": "Write"` (capital W). Tool names are case-sensitive.

- **Symptom:** You put the settings.json file in the project root instead of `.claude/settings.json`. **Fix:** Move the file into the `.claude/` directory. Claude Code only reads settings from `.claude/settings.json`.

- **Symptom:** You register a hook globally in your home directory's `.claude/settings.json` instead of the project settings. **Fix:** Use the project-level `.claude/settings.json` inside the practice folder. Global hooks apply to every project, which is rarely what you want.

- **Symptom:** You confuse PreToolUse and PostToolUse. **Fix:** Remember the rule: Pre fires before and can block. Post fires after and can only react. If you need to stop a bad file from saving, that is PreToolUse. If you need to log what happened, that is PostToolUse.

- **Symptom:** JSON syntax error in settings.json. **Fix:** Run `python -m json.tool .claude/settings.json` in your terminal. It will print the exact line and character where the syntax breaks.
