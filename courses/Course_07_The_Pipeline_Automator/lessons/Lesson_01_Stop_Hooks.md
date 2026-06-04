# Lesson 1: Stop Hooks

## The problem

It is 08:30 Monday. You sit down with coffee. Your VP of Procurement walks over: "Did you see the Great Lakes Steel transaction on Friday? $138,000 on a single PO. That is 12 times their daily average. Why did nobody flag this over the weekend?" You open the outputs/daily-monitors/ folder. The monitor file is right there, stamped Friday at 23:15, severity marked Critical. The pipeline ran. It found the problem. It wrote the report. Then nothing happened, because nobody was watching the folder at 11 PM on a Friday night.

The nightly spend monitor at Ironclad Procurement Group produces a daily report, but it has no notification layer. A Routine result, an Anomaly, and a Critical finding all end up in the same folder, waiting for someone to check manually. That gap cost the team a weekend of response time on a $138,000 anomaly.

## What Claude Code does for you

Claude Code has a hook system that runs scripts at specific points in a session. The **Stop hook** fires once, when the session ends. You register a shell script or Python script as a Stop hook, and Claude Code runs it automatically after the last prompt is answered. That means you can read the monitor output, determine severity, and route a notification, all without a human checking the folder.

## Setup

1. Claude Code installed and signed in.
2. The Course 7 practice folder open in your terminal.
3. The three sample monitor files present in outputs/daily-monitors/.
4. The file practice/data/thresholds.json available for reference.

## Step-by-step

**Step 1.** Open the practice folder in your terminal.

```
cd practice
```

You should see the data/, outputs/, and hooks/ subfolders when you run `ls`.

**Step 2.** Review the three hook types that Claude Code supports. Read the table below before moving on.

| Hook type | When it fires | Runs how many times per session | Best use case |
|---|---|---|---|
| PreToolUse | Before each tool call (file read, file write, bash command) | Many times, once per tool call | Blocking a tool call, validation before execution |
| PostToolUse | After each tool call completes | Many times, once per tool call | Logging each file write, style checks on saved files |
| **Stop** | **Once, when the session ends** | **Once** | **End-of-session notifications, summaries, cleanup** |

The key difference: PreToolUse and PostToolUse fire during the session, around individual tool calls. A PostToolUse hook fires every time Claude writes a file. A Stop hook fires once, after the entire session is over. For a notification pipeline, you want the Stop hook. You do not want a Slack message every time Claude writes a temporary file. You want one message at the end, based on the final output.

**Step 3.** Look at where hooks are registered. Open (or create) the file `.claude/settings.json` in the practice folder.

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "command": "bash hooks/session-complete-hook.sh"
      }
    ]
  }
}
```

The `"Stop"` key tells Claude Code to run this command when the session ends. The `"matcher"` field is empty because Stop hooks do not filter by tool name. They always fire at session end.

**Step 4.** Create a minimal Stop hook to confirm the wiring works. Create the file hooks/test-stop-hook.sh.

```bash
#!/usr/bin/env bash
# Minimal Stop hook: writes a timestamped line to a log file.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/../notifications/monitor-log.txt"
mkdir -p "$(dirname "$LOG_FILE")"
echo "$(date -Iseconds) | Session ended. Stop hook fired." >> "$LOG_FILE"
```

You should see the file saved at hooks/test-stop-hook.sh.

**Step 5.** Make the script executable.

```
chmod +x hooks/test-stop-hook.sh
```

No visible output. The file now has execute permission.

**Step 6.** Register the test hook in `.claude/settings.json`.

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "command": "bash hooks/test-stop-hook.sh"
      }
    ]
  }
}
```

Save the file.

**Step 7.** Start a Claude Code session, type any prompt (for example, "List the files in outputs/daily-monitors/"), then exit the session with `/exit`.

```
claude
```

After the session ends, check the log file.

```
cat notifications/monitor-log.txt
```

You should see a line like: `2026-04-25T08:45:00-05:00 | Session ended. Stop hook fired.`

## Worked example

Starting files:

- hooks/test-stop-hook.sh (the minimal script from Step 4).
- .claude/settings.json (the registration from Step 6).

You start a Claude Code session and type:

```
List the files in outputs/daily-monitors/ and tell me which date has the highest severity.
```

Claude responds with the list of three files and identifies monitor-2026-04-24.md as Critical. You type `/exit`. The session ends. Claude Code runs hooks/test-stop-hook.sh. The script appends one line to notifications/monitor-log.txt:

```
2026-04-25T08:47:22-05:00 | Session ended. Stop hook fired.
```

The hook does not yet read the monitor file or route by severity. That comes in Lesson 3. This lesson confirms that the Stop hook fires at the right time.

## Common mistakes and how to recover

- **Symptom:** You expect the Stop hook to fire every time Claude writes a file. **Fix:** That is a PostToolUse hook, not a Stop hook. Stop hooks fire once, at session end. If you need per-file behavior, register a PostToolUse hook instead.
- **Symptom:** The log file is empty after exiting the session. **Fix:** Check that .claude/settings.json is in the practice folder (not a parent folder). Check that the command path in settings.json matches the actual location of the script. Run `bash hooks/test-stop-hook.sh` manually to confirm the script works on its own.
- **Symptom:** Permission denied when the hook tries to run. **Fix:** Run `chmod +x hooks/test-stop-hook.sh` to add execute permission. On Windows with Git Bash, this is usually automatic, but verify with `ls -la hooks/`.
- **Symptom:** The hook runs but the log file lands in the wrong folder. **Fix:** The script uses `SCRIPT_DIR` to find its own location. Confirm the script is in the hooks/ subfolder. If you moved it, update the path calculation.
- **Symptom:** You registered the hook under `"PostToolUse"` instead of `"Stop"`. **Fix:** Open .claude/settings.json and change the key to `"Stop"`. PostToolUse hooks fire on every tool call, which is not what you want for end-of-session notifications.
