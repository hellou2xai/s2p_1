# Lesson 3: Tiered Notification Router

## The problem

It is 10:00 Tuesday. You understand the severity levels and the routing rules from Lesson 2. Now you need to build the actual router: a bash script that runs as a Stop hook, finds the most recent monitor file, reads its severity, and calls the right handler. Without this script, the Stop hook from Lesson 1 just writes "session ended" to a log. It does not read the monitor output or do anything useful with it.

At Ironclad Procurement Group, the VP wants this script running by the end of the week. Every night, after the spend monitor session finishes, the router must determine whether the result is Routine, Anomaly, or Critical, then send the notification to the right channel. No manual checking. No forgotten alerts.

## What Claude Code does for you

You will create hooks/session-complete-hook.sh, the bash script that ties the pipeline together. It finds the latest monitor file, extracts the severity, and branches to the correct handler. You will register it as a Stop hook and test it against the April 24 Critical monitor file.

## Setup

1. Lessons 1 and 2 complete.
2. The three sample monitor files in outputs/daily-monitors/.
3. The hooks/ subfolder exists in the practice folder.
4. The notifications/ subfolder exists (or will be created by the script).

## Step-by-step

**Step 1.** Start a Claude Code session in the practice folder.

```
cd practice
claude
```

You should see the Claude Code prompt.

**Step 2.** Ask Claude to create the router script.

```
Create a bash script at hooks/session-complete-hook.sh that does the following:
1. Find the most recent .md file in outputs/daily-monitors/ (by modification time).
2. Extract the severity level from the **Severity:** line.
3. If Routine: append a log line to notifications/monitor-log.txt with the date, severity, and file name.
4. If Anomaly: append a log line, then call python hooks/slack-notify.py with the monitor file path.
5. If Critical: append a log line, then call both hooks/slack-notify.py and hooks/escalation-email.py with the monitor file path.
6. If severity is not recognized: log a warning.
Use the script's own directory to build all paths. Do not hardcode absolute paths. Make the script executable.
```

You should see Claude create the file hooks/session-complete-hook.sh.

**Step 3.** Read the script Claude created and confirm it has these five sections.

```
Read hooks/session-complete-hook.sh and walk me through each section.
```

You should see Claude explain:

1. **Path setup.** The script finds its own directory with `SCRIPT_DIR`, then builds paths to the monitors folder, notifications folder, and log file relative to that location.
2. **Find latest file.** It uses `ls -t` to sort monitor files by modification time and picks the first one.
3. **Extract severity.** It uses grep with a regex pattern to pull the word after `**Severity:**`.
4. **Case statement.** It branches on the severity value: Routine logs only, Anomaly logs and calls Slack, Critical logs and calls both Slack and email.
5. **Fallback.** If severity is not Routine, Anomaly, or Critical, it logs an unknown severity warning.

The script should look similar to this:

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRACTICE_DIR="$(dirname "$SCRIPT_DIR")"
MONITORS_DIR="$PRACTICE_DIR/outputs/daily-monitors"
NOTIFICATIONS_DIR="$PRACTICE_DIR/notifications"
LOG_FILE="$NOTIFICATIONS_DIR/monitor-log.txt"

mkdir -p "$NOTIFICATIONS_DIR"

LATEST=$(ls -t "$MONITORS_DIR"/monitor-*.md 2>/dev/null | head -1)

if [ -z "$LATEST" ]; then
    echo "$(date -Iseconds) | No monitor output found." >> "$LOG_FILE"
    exit 0
fi

SEVERITY=$(grep -oP '(?<=\*\*Severity:\*\* )\w+' "$LATEST" | head -1)

case "$SEVERITY" in
    Routine)
        echo "$(date -Iseconds) | ROUTINE | $(basename "$LATEST") | No anomalies." >> "$LOG_FILE"
        ;;
    Anomaly)
        echo "$(date -Iseconds) | ANOMALY | $(basename "$LATEST") | Routing to Slack." >> "$LOG_FILE"
        python "$SCRIPT_DIR/slack-notify.py" "$LATEST"
        ;;
    Critical)
        echo "$(date -Iseconds) | CRITICAL | $(basename "$LATEST") | Routing to email escalation." >> "$LOG_FILE"
        python "$SCRIPT_DIR/slack-notify.py" "$LATEST"
        python "$SCRIPT_DIR/escalation-email.py" "$LATEST"
        ;;
    *)
        echo "$(date -Iseconds) | UNKNOWN | $(basename "$LATEST") | Severity not recognized: $SEVERITY" >> "$LOG_FILE"
        ;;
esac
```

**Step 4.** Register the script as a Stop hook. Update .claude/settings.json in the practice folder.

```
Update .claude/settings.json to register hooks/session-complete-hook.sh as a Stop hook. The command should be: bash hooks/session-complete-hook.sh
```

You should see the file updated with:

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

**Step 5.** Test the script manually against the Critical monitor file before relying on the Stop hook.

```
bash hooks/session-complete-hook.sh
```

You should see a log entry appended to notifications/monitor-log.txt. Since monitor-2026-04-24.md is the most recently modified file, the severity should be Critical. The script will try to call slack-notify.py and escalation-email.py. Those scripts do not exist yet (they come in Lesson 4), so you may see a "file not found" error for the Python calls. That is expected. The important thing is that the severity extraction and branching work correctly.

**Step 6.** Check the log file to confirm the router chose the right path.

```
cat notifications/monitor-log.txt
```

You should see a line containing `CRITICAL | monitor-2026-04-24.md | Routing to email escalation.`

## Worked example

Starting files:

- outputs/daily-monitors/monitor-2026-04-20.md (Routine).
- outputs/daily-monitors/monitor-2026-04-21.md (Anomaly).
- outputs/daily-monitors/monitor-2026-04-24.md (Critical, most recent by modification time).

You start a Claude Code session and ask Claude to create the router script. Claude writes hooks/session-complete-hook.sh with path setup, file discovery, severity extraction, and a case statement. You register it as a Stop hook in .claude/settings.json.

You run the script manually:

```
bash hooks/session-complete-hook.sh
```

The script finds monitor-2026-04-24.md (the most recently modified file), extracts `Critical`, and logs:

```
2026-04-25T10:22:14-05:00 | CRITICAL | monitor-2026-04-24.md | Routing to email escalation.
```

It also attempts to call slack-notify.py and escalation-email.py. Those scripts are not built yet, so the calls fail. The routing logic itself is correct.

To test the Routine path, touch the April 20 file to make it the newest:

```
touch outputs/daily-monitors/monitor-2026-04-20.md
bash hooks/session-complete-hook.sh
cat notifications/monitor-log.txt
```

The last line should read: `ROUTINE | monitor-2026-04-20.md | No anomalies.`

## Common mistakes and how to recover

- **Symptom:** The script picks the wrong monitor file. **Fix:** `ls -t` sorts by modification time. If you edited an older file, it becomes the "latest." Use `touch` to reset modification times for testing, or sort by file name instead if your naming convention is date-based.
- **Symptom:** The script reports "No monitor output found." **Fix:** Check that the MONITORS_DIR path is correct. The script builds it relative to its own location. If you moved the script out of hooks/, the path calculation breaks. Run `ls outputs/daily-monitors/` to confirm the files exist.
- **Symptom:** Severity comes back empty. **Fix:** The grep pattern expects the exact format `**Severity:** Routine` with one space after the colon. If the monitor file uses a different format (for example, no space, or lowercase), the pattern will not match. Check the file with `head -5 outputs/daily-monitors/monitor-2026-04-24.md`.
- **Symptom:** The case statement falls through to the wildcard `*` branch. **Fix:** Severity matching is case-sensitive. The monitor files use `Routine`, `Anomaly`, and `Critical` with an uppercase first letter. If your grep returns `routine` (lowercase), the case statement will not match. Adjust the grep or the case labels to be consistent.
- **Symptom:** The script runs but the Python scripts fail with "No such file." **Fix:** That is expected at this stage. The Python notification scripts are built in Lesson 4. The router logic is correct even if the downstream handlers do not exist yet.
- **Symptom:** The notifications/ folder does not exist and the log file is not created. **Fix:** Add `mkdir -p "$NOTIFICATIONS_DIR"` before the first `echo` that writes to the log file. The script should create the folder if it is missing.
