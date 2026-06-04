# Lesson 6: End-to-End Test

## The problem

It is 16:00 Tuesday. You have built every piece of the pipeline: the router, the Slack script, the email script, the Stop hook registration, and the cron entry. But you have not tested the full chain from start to finish in one run. Each script was tested in isolation. The question is whether they work together, in sequence, with no manual steps in between. Your VP will ask tomorrow morning: "Is the pipeline live?" You need to answer yes, with test results to prove it.

At Ironclad Procurement Group, the rule is simple: no pipeline goes to production without a full end-to-end test against known data. You have two test cases: April 24 (Critical) and April 20 (Routine). If both produce the correct outputs and notifications, the pipeline is ready.

## What Claude Code does for you

You will run the full pipeline twice. First against the April 24 data (Critical), then against the April 20 data (Routine). For each run, you will verify that every artifact lands in the right folder: the monitor file, the log entry, the Slack payload, and the email draft. This lesson is a verification exercise, not a building exercise. You are confirming that everything works.

## Setup

1. Lessons 1 through 5 complete.
2. All scripts in hooks/ tested individually.
3. The .claude/settings.json file with the Stop hook registered.
4. The notifications/ folder cleared of previous test outputs (optional, but recommended for a clean test).

## Step-by-step

### Test 1: Critical severity (April 24)

**Step 1.** Clear previous notification artifacts so you can confirm fresh outputs.

```
rm -f notifications/slack-messages/slack-2026-04-24.json
rm -f notifications/email-drafts/escalation-2026-04-24.json
```

No visible output. The files are removed.

**Step 2.** Start a Claude Code session in the practice folder.

```
cd practice
claude
```

You should see the Claude Code prompt.

**Step 3.** Ask Claude to produce a monitor report for April 24.

```
Read data/daily-spend.csv and data/thresholds.json. Analyze all transactions for 2026-04-24. Calculate the daily average for each supplier, then flag any transaction that exceeds 3x the supplier daily average. If total daily spend exceeds $500,000 or any single transaction exceeds 10x the supplier daily average, set severity to Critical. Save the report to outputs/daily-monitors/monitor-2026-04-24.md using the same format as the existing monitor files.
```

You should see Claude confirm the file was saved. The severity should be Critical because of the Great Lakes Steel transaction at 12x ($138,082.19) and the daily total of $538,200.18 exceeding the $500,000 ceiling.

**Step 4.** Exit the session to trigger the Stop hook.

```
/exit
```

The session ends. The Stop hook fires. The router reads monitor-2026-04-24.md, extracts Critical, and calls both slack-notify.py and escalation-email.py.

**Step 5.** Verify the monitor file exists and has the correct severity.

```
head -5 outputs/daily-monitors/monitor-2026-04-24.md
```

You should see: `**Severity:** Critical`

**Step 6.** Verify the log entry.

```
tail -1 notifications/monitor-log.txt
```

You should see a line containing: `CRITICAL | monitor-2026-04-24.md | Routing to email escalation.`

**Step 7.** Verify the Slack payload.

```
cat notifications/slack-messages/slack-2026-04-24.json
```

You should see a JSON file with a header block showing `:rotating_light: Spend Monitor Alert: Critical`, a section block with the date and anomaly count, at least one section block for Great Lakes Steel, a divider, and a context block.

**Step 8.** Verify the email draft.

```
cat notifications/email-drafts/escalation-2026-04-24.json
```

You should see a JSON file with `to` addresses including vp-procurement@ironclad-group.com, a subject line containing `CRITICAL: Spend Monitor Alert for 2026-04-24`, and a body that includes the Great Lakes Steel anomaly, the $538,200 daily total, and three recommended actions.

### Test 2: Routine severity (April 20)

**Step 9.** Note the current line count of the log file so you can confirm a new entry was added.

```
wc -l notifications/monitor-log.txt
```

You should see a number. Remember it.

**Step 10.** Start a new Claude Code session.

```
claude
```

You should see the Claude Code prompt.

**Step 11.** Ask Claude to produce a monitor report for April 20.

```
Read data/daily-spend.csv and data/thresholds.json. Analyze all transactions for 2026-04-20. Calculate the daily average for each supplier, then flag any transaction that exceeds 3x the supplier daily average. If no anomalies are found and total daily spend is under $500,000, set severity to Routine. Save the report to outputs/daily-monitors/monitor-2026-04-20.md using the same format as the existing monitor files.
```

You should see Claude confirm the file was saved. The severity should be Routine because April 20 has no anomalies and total spend of $142,380.45.

**Step 12.** Exit the session.

```
/exit
```

The Stop hook fires. The router reads monitor-2026-04-20.md (now the most recently modified file), extracts Routine, and logs a line. No Slack message. No email.

**Step 13.** Verify the log has one new Routine entry.

```
tail -1 notifications/monitor-log.txt
```

You should see: `ROUTINE | monitor-2026-04-20.md | No anomalies.`

**Step 14.** Confirm that no new Slack or email files were created for April 20.

```
ls notifications/slack-messages/slack-2026-04-20.json 2>/dev/null || echo "No Slack file for April 20. Correct."
ls notifications/email-drafts/escalation-2026-04-20.json 2>/dev/null || echo "No email file for April 20. Correct."
```

You should see "No Slack file for April 20. Correct." and "No email file for April 20. Correct." Routine results produce a log entry only. No notifications to any channel.

### Summary checklist

| Check | Critical (April 24) | Routine (April 20) |
|---|---|---|
| Monitor file in outputs/daily-monitors/ | Yes | Yes |
| Severity correct | Critical | Routine |
| Log entry in notifications/monitor-log.txt | Yes, with CRITICAL | Yes, with ROUTINE |
| Slack payload in notifications/slack-messages/ | Yes | No |
| Email draft in notifications/email-drafts/ | Yes | No |

If all five checks pass for both dates, the pipeline is ready for production.

## Worked example

You run the Critical test first. Claude produces monitor-2026-04-24.md with severity Critical. You exit the session. The Stop hook fires, the router extracts Critical, calls slack-notify.py (which saves slack-2026-04-24.json), and calls escalation-email.py (which saves escalation-2026-04-24.json). The log shows `CRITICAL | monitor-2026-04-24.md | Routing to email escalation.`

You then run the Routine test. Claude produces monitor-2026-04-20.md with severity Routine. You exit the session. The Stop hook fires, the router extracts Routine, and writes a log entry. No Slack file. No email file. The log shows `ROUTINE | monitor-2026-04-20.md | No anomalies.`

Both tests pass. The pipeline routes correctly for the highest and lowest severity levels. To be thorough, you could also test April 21 (Anomaly) and confirm a Slack payload appears but no email draft.

## Common mistakes and how to recover

- **Symptom:** The Stop hook does not fire when you type `/exit`. **Fix:** Confirm that .claude/settings.json is in the practice folder, not a parent or child folder. The Stop hook must be registered in the project where Claude Code is running.
- **Symptom:** The log shows the wrong file name (for example, monitor-2026-04-24.md when you expected monitor-2026-04-20.md). **Fix:** The router picks the most recently modified file in outputs/daily-monitors/. If the April 24 file was modified more recently than the April 20 file, the router picks April 24. Make sure the April 20 monitor is the last file Claude wrote before you exited the session.
- **Symptom:** The Slack payload exists for the Routine test. **Fix:** The router should only call slack-notify.py for Anomaly and Critical. Check the case statement in session-complete-hook.sh. The Routine branch should log only, with no Python calls.
- **Symptom:** The email draft is missing for the Critical test. **Fix:** Check the Critical branch in the router script. It should call both slack-notify.py and escalation-email.py. If only the Slack call is there, add the email call. Also check that hooks/escalation-email.py exists and is not misspelled.
- **Symptom:** The notification files exist but contain empty JSON or errors. **Fix:** Run the Python scripts manually to see error output: `python hooks/slack-notify.py outputs/daily-monitors/monitor-2026-04-24.md`. The error message will tell you whether the issue is in the regex, the file path, or the JSON formatting.
