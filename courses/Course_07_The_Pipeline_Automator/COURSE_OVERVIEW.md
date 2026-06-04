# Course 7: The Pipeline Automator

## A Monday morning surprise

It is Monday morning, 07:45. You check Slack on your phone while waiting for coffee. No messages from the spend monitor. Good. That probably means the nightly run was clean.

You get to your desk at 08:30. Your VP of Procurement walks over: "Did you see the Great Lakes Steel transaction on Friday? $138,000 on a single PO. That is 12 times their daily average. Why did nobody flag this over the weekend?"

You open your laptop. The nightly spend monitor ran on Friday night as scheduled. It produced a monitor output file with the Critical severity flag. The file is sitting in outputs/daily-monitors/ with the anomaly clearly listed. But nobody saw it. Nobody was notified. The monitor ran, found the problem, wrote the report, and then nothing happened.

This course fixes that. You build a **Stop hook** that fires when a Claude Code session ends, reads the monitor output, determines severity, and routes the result to the right channel: a log file for routine results, a Slack message for anomalies, and an email escalation for critical findings.

## What a Stop hook is

A Stop hook is a script that Claude Code runs automatically when a session ends. Unlike PreToolUse and PostToolUse hooks (which fire during the session, around individual tool calls), a Stop hook fires once, at the very end.

| Hook type | When it fires | Use case |
|---|---|---|
| PreToolUse | Before each tool call | Validation, blocking |
| PostToolUse | After each tool call | Logging, alerts |
| **Stop** | **When the session ends** | **Notifications, summaries, cleanup** |
| Notification | On specific events | Error reactions, progress updates |

Stop hooks are the right choice when:
- You want to send a notification based on what the entire session produced (not a single file write).
- You want to run cleanup or archival logic after all work is done.
- You want to trigger a downstream system (email, Slack, ticketing) based on the session outcome.

## The practice scenario

Ironclad Procurement Group is a US-based procurement shared services center. The team runs a nightly spend monitor that scans the last 24 hours of transactions, detects anomalies, and writes a daily monitor report.

You are the Procurement Analytics Lead. The nightly pipeline works, but it has no notification layer. Results sit in a folder until someone checks manually. Your VP wants three tiers of notification:

1. **Routine**: Daily spend within normal range, no anomalies. Write a one-line log entry. No notification to anyone.
2. **Anomaly**: One or more transactions exceed 3x the supplier daily average. Post a structured summary to the procurement-alerts Slack channel.
3. **Critical**: Total daily spend exceeds $500,000 or a single transaction exceeds 10x the supplier daily average. Send an escalation email to the category manager and the VP distribution list.

Today's date is **2026-04-25**. You have:

- 30 days of spend transactions (851 rows) with planted anomalies.
- 40 suppliers across 5 categories.
- Alert thresholds in thresholds.json.
- Three sample monitor outputs (one per severity) to show the expected format.

The planted anomalies:
- April 21: Three transactions at 5x to 6.5x the daily average (Apex Electronics, Eagle Transport, Blueprint Marketing). Severity: Anomaly.
- April 24: One transaction from Great Lakes Steel at 12x the daily average ($138,082.19). Total daily spend: $538,200. Severity: Critical.

## What you will build

```
hooks/
├── session-complete-hook.sh        ← Stop hook: reads latest monitor, routes by severity
├── slack-notify.py                 ← Formats anomaly summary as Slack block message
└── escalation-email.py             ← Sends structured email for critical findings

notifications/
├── slack-messages/                 ← Slack message payloads (JSON files)
└── email-drafts/                   ← Email drafts for critical escalations
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | Stop hooks: when they fire and what session data is available | 25 min |
| 2 | Notification hooks: event types and payload structure | 35 min |
| 3 | Writing a tiered notification router | 50 min |
| 4 | Slack webhook integration: formatting procurement alerts | 45 min |
| 5 | Building the complete nightly stack: cron to session to notification | 40 min |
| 6 | End-to-end testing: triggering the pipeline and confirming correct routing | 25 min |

Total: about 4 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. Your Stop hook reads the most recent file in outputs/daily-monitors/ and correctly determines the severity.
2. A routine monitor produces a log entry. An anomaly monitor produces a Slack message payload in notifications/slack-messages/. A critical monitor produces an email draft in notifications/email-drafts/.
3. The Slack message includes the anomaly table (supplier, transaction, amount, multiple) formatted as a Slack block.
4. The email draft includes the critical anomaly details, the daily spend total, and three recommended actions.
5. You can describe how to schedule the pipeline with cron and how the Stop hook connects to the session lifecycle.
