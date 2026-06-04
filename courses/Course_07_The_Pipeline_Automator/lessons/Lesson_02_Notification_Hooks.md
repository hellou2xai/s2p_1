# Lesson 2: Notification Hooks

## The problem

It is 09:15 Tuesday. Your VP has asked for a tiered notification system: routine results go to a log file, anomalies go to Slack, and critical findings go to email. Right now, every result sits in the same folder with no routing. A $142,000 routine day and a $538,000 critical day look the same until someone opens each file and reads it. The team needs different channels for different severity levels, so the right people see the right alerts at the right time.

At Ironclad Procurement Group, the nightly spend monitor already classifies each day as Routine, Anomaly, or Critical. The severity line is right there in the monitor file. What is missing is a layer that reads that severity and sends the result to the correct channel.

## What Claude Code does for you

You will read the three sample monitor files, identify the severity in each one, and map each severity to its notification channel. This gives you the classification logic you need before writing the router script in Lesson 3. By the end of this lesson, you will know exactly what each severity level means, where it is defined, and how to extract it from a monitor file.

## Setup

1. Lessons 1 complete (Stop hook concept understood).
2. The three sample monitor files in outputs/daily-monitors/.
3. The file data/thresholds.json available for reference.

## Step-by-step

**Step 1.** Open thresholds.json and review the severity definitions.

```
cat data/thresholds.json
```

You should see three severity levels with their conditions and notification routes:

```json
{
  "anomaly_multiplier": 3.0,
  "daily_spend_ceiling_usd": 500000,
  "severity_levels": {
    "routine": "Daily spend within normal range, no anomalies detected.",
    "anomaly": "One or more transactions exceed 3x the supplier daily average.",
    "critical": "Total daily spend exceeds $500,000 or a single transaction exceeds 10x supplier daily average."
  },
  "notification_routing": {
    "routine": "log_file",
    "anomaly": "slack_webhook",
    "critical": "email_escalation"
  }
}
```

**Step 2.** Review the severity routing table. This is the decision tree your router will follow.

| Severity | Condition | Notification channel | Who sees it |
|---|---|---|---|
| Routine | Daily spend under $500,000, no transactions above 3x average | Log file entry | Nobody, unless they check the log |
| Anomaly | One or more transactions exceed 3x the supplier daily average | Slack message to procurement-alerts | Procurement analytics team |
| Critical | Daily spend exceeds $500,000 ceiling, or a single transaction exceeds 10x average | Email escalation to category manager and VP | Senior leadership |

Critical alerts also get a Slack message. The router sends both.

**Step 3.** Open the Routine monitor file and find the severity line.

```
cat outputs/daily-monitors/monitor-2026-04-20.md
```

You should see `**Severity:** Routine` near the top of the file. Total daily spend: $142,380.45. No anomalies detected.

**Step 4.** Open the Anomaly monitor file.

```
cat outputs/daily-monitors/monitor-2026-04-21.md
```

You should see `**Severity:** Anomaly`. Three anomalies listed: Apex Electronics at 6.5x, Eagle Transport at 5.4x, and Blueprint Marketing at 5.9x.

**Step 5.** Open the Critical monitor file.

```
cat outputs/daily-monitors/monitor-2026-04-24.md
```

You should see `**Severity:** Critical`. Great Lakes Steel at 12.0x ($138,082.19). Total daily spend: $538,200.18, which exceeds the $500,000 ceiling.

**Step 6.** Start a Claude Code session and ask Claude to classify each file.

```
claude
```

Type this prompt:

```
Read the three files in outputs/daily-monitors/. For each file, extract the severity level and tell me which notification channel it should route to, based on the rules in data/thresholds.json. Present the results as a table with columns: Date, Severity, Channel.
```

You should see a table like this:

| Date | Severity | Channel |
|---|---|---|
| 2026-04-20 | Routine | Log file only |
| 2026-04-21 | Anomaly | Slack webhook |
| 2026-04-24 | Critical | Email escalation (and Slack) |

**Step 7.** Confirm the extraction pattern. The severity line in every monitor file follows this format:

```
**Severity:** Routine
```

The word after `**Severity:**` is the severity level. Your router script will use a grep or regex pattern to extract this value. In bash, that looks like:

```bash
SEVERITY=$(grep -oP '(?<=\*\*Severity:\*\* )\w+' "$MONITOR_FILE" | head -1)
```

This returns one word: `Routine`, `Anomaly`, or `Critical`.

## Worked example

Starting files:

- outputs/daily-monitors/monitor-2026-04-20.md (Routine).
- outputs/daily-monitors/monitor-2026-04-21.md (Anomaly).
- outputs/daily-monitors/monitor-2026-04-24.md (Critical).
- data/thresholds.json (severity definitions and routing rules).

You ask Claude Code:

```
Read all three monitor files in outputs/daily-monitors/. For each one, extract the severity level, the total daily spend, and the number of anomalies. Then map each severity to its notification channel using the routing rules in data/thresholds.json.
```

Claude reads each file, finds the severity line, and produces:

```
monitor-2026-04-20.md: Routine, $142,380.45, 0 anomalies → log file only
monitor-2026-04-21.md: Anomaly, $218,640.32, 3 anomalies → Slack webhook
monitor-2026-04-24.md: Critical, $538,200.18, 1 critical anomaly → email escalation + Slack
```

Behind the scenes, Claude opened each file in modification-date order, searched for the `**Severity:**` line, pulled the severity word, then looked up the matching channel in thresholds.json. No code was needed for this step. The classification logic is straightforward pattern matching.

## Common mistakes and how to recover

- **Symptom:** You hardcode severity in your router script instead of reading it from the file. **Fix:** Always extract severity from the monitor file at runtime. The whole point of the tiered system is that severity changes day to day. A hardcoded value defeats the purpose.
- **Symptom:** You route all severities to the same channel (for example, always sending a Slack message). **Fix:** Review the routing table in thresholds.json. Routine results go to the log only. Anomalies go to Slack. Critical findings go to email and Slack. Each channel serves a different audience.
- **Symptom:** The grep pattern does not find the severity line. **Fix:** Check the exact format. The line is `**Severity:** Routine` with Markdown bold markers. The regex must account for the double asterisks. Test with `grep "Severity" outputs/daily-monitors/monitor-2026-04-20.md` first to confirm the line exists.
- **Symptom:** You confuse the anomaly multiplier (3x) with the critical multiplier (10x). **Fix:** Read thresholds.json again. The anomaly_multiplier (3.0) triggers Anomaly severity. A single transaction at 10x or more triggers Critical. These are separate thresholds.
- **Symptom:** You forget that Critical also gets a Slack message. **Fix:** Critical sends both Slack and email. The router must call both handlers for Critical severity.
