# Lesson 5: Complete Nightly Stack

## The problem

It is 14:30 Tuesday. You have three working pieces: the router script (session-complete-hook.sh), the Slack notification script (slack-notify.py), and the escalation email script (escalation-email.py). Each one works on its own. But nobody is running them. Right now, you start a Claude Code session manually, type a prompt, and exit. The Stop hook fires. That is fine for testing, but it is not a nightly pipeline. The VP wants this running automatically at 23:00 every night, with no human in the loop.

At Ironclad Procurement Group, the nightly spend monitor needs to run on a schedule: cron fires, Claude Code runs headless (no interactive prompt), produces the monitor report, the session ends, and the Stop hook routes the notification. The full stack has four stages, and this lesson connects them.

## What Claude Code does for you

You will map the complete pipeline from cron trigger to notification delivery. You will see how `claude --print` runs a headless session, how the Stop hook connects to the session lifecycle, and how to schedule the whole thing with cron. By the end, you will have a working nightly stack that you could deploy on a Linux server or a scheduled task on Windows.

## Setup

1. Lessons 1 through 4 complete.
2. All three scripts in hooks/ working and tested.
3. The .claude/settings.json file in the practice folder with the Stop hook registered.
4. Access to a terminal with cron (Linux/macOS) or Task Scheduler (Windows).

## Step-by-step

**Step 1.** Review the full pipeline flow. Read this diagram from left to right.

```
[cron: 23:00]
    |
    v
[claude --print "Run the nightly spend monitor for today..."]
    |
    v
[Claude Code reads daily-spend.csv, computes anomalies, writes monitor-YYYY-MM-DD.md]
    |
    v
[Session ends]
    |
    v
[Stop hook fires: session-complete-hook.sh]
    |
    v
[Router reads latest monitor, extracts severity]
    |
    +--> Routine: log entry only
    |
    +--> Anomaly: slack-notify.py --> notifications/slack-messages/
    |
    +--> Critical: slack-notify.py + escalation-email.py --> notifications/slack-messages/ + notifications/email-drafts/
```

Each box is a separate concern. Cron handles scheduling. Claude Code handles analysis. The Stop hook handles notification routing. The Python scripts handle formatting and delivery.

**Step 2.** Understand headless mode. The `claude --print` flag runs Claude Code without an interactive prompt. You pass the full prompt as a string. Claude processes it and exits. The Stop hook fires on exit, just as it would in an interactive session.

```
claude --print "Read data/daily-spend.csv and data/thresholds.json. Analyze today's transactions (2026-04-25). Identify any anomalies where a transaction exceeds 3x the supplier's daily average. If total spend exceeds $500,000 or any transaction exceeds 10x average, mark as Critical. Save the monitor report to outputs/daily-monitors/monitor-2026-04-25.md using the format in the existing monitor files."
```

You should see Claude produce the monitor report and exit. Check outputs/daily-monitors/ for the new file.

**Step 3.** Verify the Stop hook fired after the headless session.

```
cat notifications/monitor-log.txt
```

You should see a new log entry for the session that just ended, with the severity of today's data and the file name.

**Step 4.** Build the cron entry. On Linux or macOS, the crontab line looks like this:

```
0 23 * * * cd /path/to/practice && claude --print "Read data/daily-spend.csv and data/thresholds.json. Analyze today's transactions. Identify anomalies using the 3x multiplier. Mark as Critical if total spend exceeds 500000 or any transaction exceeds 10x average. Save the report to outputs/daily-monitors/monitor-$(date +\%Y-\%m-\%d).md using the existing monitor file format." >> /path/to/practice/logs/cron.log 2>&1
```

This runs at 23:00 every day. It changes to the practice folder first, so all relative paths in the prompt and the Stop hook resolve correctly. Output goes to a cron log for debugging.

On Windows, you would use Task Scheduler with a similar command. The principle is the same: change to the project folder, run `claude --print` with the prompt, and let the Stop hook handle the rest.

**Step 5.** Review the environment requirements. Cron runs in a minimal shell environment. Several things that work in your terminal may not work in cron.

| Requirement | Why it matters | How to set it |
|---|---|---|
| PATH includes claude | Cron does not load your shell profile | Add `PATH=/usr/local/bin:$PATH` at the top of crontab |
| PATH includes python | The Stop hook calls Python scripts | Same PATH line |
| Working directory | Relative paths in prompts and hooks need the right starting point | Use `cd /path/to/practice &&` before the command |
| SLACK_WEBHOOK_URL | The Slack script checks this variable | Add `SLACK_WEBHOOK_URL=https://hooks.slack.com/...` in crontab or an env file |
| Claude API credentials | Claude Code needs authentication | Ensure the API key or session token is available in the cron environment |

**Step 6.** Test the full stack without cron first. Run the headless command from Step 2 manually. After it completes, check three things:

```
ls outputs/daily-monitors/monitor-2026-04-25.md
cat notifications/monitor-log.txt | tail -1
ls notifications/slack-messages/ notifications/email-drafts/
```

You should see: the new monitor file exists, the log has a new entry with the correct severity, and (if the severity was Anomaly or Critical) a Slack payload or email draft exists in the right folder.

## Worked example

You run the full pipeline manually at 15:00 on April 25:

```
claude --print "Read data/daily-spend.csv and data/thresholds.json. Analyze transactions for 2026-04-25. Identify anomalies at the 3x threshold. Mark as Critical if total spend exceeds $500,000 or any single transaction exceeds 10x average. Save the report to outputs/daily-monitors/monitor-2026-04-25.md in the same format as the existing monitor files."
```

Claude reads the CSV, computes daily averages, checks each transaction, and writes the monitor file. The session ends. The Stop hook fires. The router finds monitor-2026-04-25.md (the most recently modified file), extracts the severity, and routes accordingly.

If April 25 data is Routine, the log shows:

```
2026-04-25T15:02:44-05:00 | ROUTINE | monitor-2026-04-25.md | No anomalies.
```

No Slack message. No email. Just a log entry.

If you want to test the Critical path, run the prompt for April 24 instead:

```
claude --print "Read data/daily-spend.csv and data/thresholds.json. Analyze transactions for 2026-04-24. Identify anomalies at the 3x threshold. Mark as Critical if total spend exceeds $500,000 or any single transaction exceeds 10x average. Save the report to outputs/daily-monitors/monitor-2026-04-24.md in the same format as the existing monitor files."
```

The Stop hook detects Critical, calls slack-notify.py and escalation-email.py, and both notification files appear.

## Common mistakes and how to recover

- **Symptom:** Cron runs but Claude is not found. **Fix:** Cron uses a minimal PATH. Add the full path to the claude binary in the crontab, or set PATH at the top of the crontab file. Run `which claude` in your terminal to find the path.
- **Symptom:** The headless session produces no output file. **Fix:** Check that the prompt specifies the output file path explicitly. In headless mode, Claude does not ask clarifying questions. If the prompt is ambiguous about where to save, Claude may print the report to stdout instead of writing a file.
- **Symptom:** The Stop hook does not fire in headless mode. **Fix:** Confirm that .claude/settings.json is in the working directory (the folder you `cd` into before running `claude --print`). The Stop hook registration is project-specific.
- **Symptom:** The cron log shows "permission denied" for the Python scripts. **Fix:** Add execute permission with `chmod +x hooks/*.py`, or call them with `python hooks/slack-notify.py` (using the python command, not executing the script directly).
- **Symptom:** Date substitution in the cron command produces the wrong file name. **Fix:** In crontab, percent signs must be escaped with a backslash: `$(date +\%Y-\%m-\%d)`. Without the backslash, cron treats `%` as a newline character and the command breaks.
