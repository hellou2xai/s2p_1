#!/usr/bin/env bash
# Stop hook: reads the most recent daily monitor output and routes by severity.
# Reference solution for Course 7, Lesson 3.
#
# Registered in .claude/settings.json as a Stop hook.
# Claude Code runs this script when the session ends.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRACTICE_DIR="$(dirname "$SCRIPT_DIR")"
MONITORS_DIR="$PRACTICE_DIR/outputs/daily-monitors"
NOTIFICATIONS_DIR="$PRACTICE_DIR/notifications"
LOG_FILE="$NOTIFICATIONS_DIR/monitor-log.txt"

# Find the most recent monitor file
LATEST=$(ls -t "$MONITORS_DIR"/monitor-*.md 2>/dev/null | head -1)

if [ -z "$LATEST" ]; then
    echo "$(date -Iseconds) | No monitor output found. Nothing to route." >> "$LOG_FILE"
    exit 0
fi

# Extract severity from the file
SEVERITY=$(grep -oP '(?<=\*\*Severity:\*\* )\w+' "$LATEST" | head -1)

case "$SEVERITY" in
    Routine)
        echo "$(date -Iseconds) | ROUTINE | $(basename "$LATEST") | No anomalies." >> "$LOG_FILE"
        ;;
    Anomaly)
        echo "$(date -Iseconds) | ANOMALY | $(basename "$LATEST") | Routing to Slack." >> "$LOG_FILE"
        python "$SCRIPT_DIR/../hooks/slack-notify.py" "$LATEST"
        ;;
    Critical)
        echo "$(date -Iseconds) | CRITICAL | $(basename "$LATEST") | Routing to email escalation." >> "$LOG_FILE"
        python "$SCRIPT_DIR/../hooks/slack-notify.py" "$LATEST"
        python "$SCRIPT_DIR/../hooks/escalation-email.py" "$LATEST"
        ;;
    *)
        echo "$(date -Iseconds) | UNKNOWN | $(basename "$LATEST") | Severity not recognized: $SEVERITY" >> "$LOG_FILE"
        ;;
esac
