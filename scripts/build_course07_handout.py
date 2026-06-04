"""Build the Course 7: The Pipeline Automator companion handout (.docx).

Style follows CLAUDE.md: no em-dashes, Oxford commas, American English,
no banned phrases, four-part rule on every worked example, active voice.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt


_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent

OUTPUT_PATH = (
    _PROJECT_ROOT / "Handouts" / "Course_07_The_Pipeline_Automator_Handout.docx"
)


def add_runs(paragraph, text):
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            paragraph.add_run(part)


class _NumState:
    counter = 1
    in_block = False


def _end_num_block():
    _NumState.in_block = False


def para(doc, text, *, italic=False, size=None):
    _end_num_block()
    p = doc.add_paragraph()
    add_runs(p, text)
    for run in p.runs:
        if italic:
            run.italic = True
        if size is not None:
            run.font.size = Pt(size)
    return p


def heading(doc, text, level=1):
    _end_num_block()
    return doc.add_heading(text, level=level)


def bullet(doc, text):
    _end_num_block()
    p = doc.add_paragraph(style="List Bullet")
    add_runs(p, text)
    return p


def numbered(doc, text):
    if not _NumState.in_block:
        _NumState.counter = 1
        _NumState.in_block = True
    n = _NumState.counter
    _NumState.counter += 1
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.add_run(f"{n}. ")
    add_runs(p, text)
    return p


def code_block(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(10)
    return p


def fill_table(doc, headers, rows, style="Light Grid Accent 1"):
    _end_num_block()
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = style
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.bold = True
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            table.rows[ri].cells[ci].text = val
    return table


# -----------------------------------------------------------------------
# Main build
# -----------------------------------------------------------------------
def build():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ===================================================================
    # Cover
    # ===================================================================
    para(doc, "U2xAI", italic=True, size=12)
    para(doc, "PROCUREAI ACADEMY", italic=True, size=10)
    para(doc, "Series 2 (Engineering Track) | Course 7", italic=True)
    doc.add_heading("The Pipeline Automator", level=0)
    para(
        doc,
        "Stop hooks and notification routing for automated spend "
        "monitoring, so critical findings reach the right people without "
        "anyone checking a folder at midnight.",
        italic=True,
        size=14,
    )
    para(
        doc,
        "Four hours. Six lessons. No coding background required. "
        "Real spend data with 40 suppliers, 851 transactions, and "
        "planted anomalies across five categories.",
        italic=True,
    )
    para(
        doc,
        "Use this handout alongside the course folder at "
        "Detailed Course Content/Course_07_The_Pipeline_Automator/.",
        italic=True,
    )

    # ===================================================================
    # 1. How to use this handout
    # ===================================================================
    heading(doc, "1. How to use this handout", 1)
    para(
        doc,
        "This handout is your reading companion. The hands-on work "
        "happens in the course folder you received with this guide. The "
        "folder contains the spend data, the sample monitor outputs, the "
        "six lessons, and the reference solutions. You do not need "
        "anything else.",
    )
    para(doc, "How to read this guide:")
    numbered(
        doc,
        "Read sections 2 and 3 to understand what the course covers "
        "and what you will build by the end.",
    )
    numbered(
        doc,
        "Read section 4 to see how much time automated notification "
        "routing saves per monitoring cycle.",
    )
    numbered(
        doc,
        "Read section 5 for the mental model of Stop hooks and "
        "notification routing. This is the concept you need before "
        "you touch the terminal.",
    )
    numbered(
        doc,
        "Work through section 6 for two fully worked examples, each "
        "with the prompt, the folder layout, the expected result, "
        "and the behind-the-scenes walkthrough.",
    )
    numbered(
        doc,
        "Use section 7 (Day in the Life) to see how a procurement "
        "analytics lead uses Stop hooks and notification routing "
        "across a real workday.",
    )
    numbered(
        doc,
        "If you are setting up for the first time, follow section 8 "
        "(20-Minute Sprint) to get your first notification routed in "
        "twenty minutes.",
    )
    numbered(
        doc,
        "Use section 9 (First Week Planner) to build your pipeline "
        "skills day by day.",
    )
    numbered(
        doc,
        "Refer to section 10 (The Pattern) whenever you want to "
        "apply notification routing to a new monitoring task.",
    )
    numbered(
        doc,
        "Keep section 11 (Troubleshooting) open when something "
        "goes wrong.",
    )
    para(
        doc,
        "Every example in this handout uses Claude Code (in the "
        "terminal). The Stop hook and notification routing features "
        "described here are specific to Claude Code. They are not "
        "available in Claude AI Web (claude.ai in a browser) or "
        "Claude Desktop with Cowork.",
    )

    # ===================================================================
    # 2. What this course teaches
    # ===================================================================
    heading(doc, "2. What this course teaches", 1)
    para(
        doc,
        "It is Monday morning, 07:45. You check Slack on your phone "
        "while waiting for coffee. No messages from the spend monitor. "
        "Good. That probably means the nightly run was clean.",
    )
    para(
        doc,
        "You get to your desk at 08:30. Your VP of Procurement walks "
        "over: \"Did you see the Great Lakes Steel transaction on "
        "Friday? $138,000 on a single PO. That is 12 times their daily "
        "average. Why did nobody flag this over the weekend?\"",
    )
    para(
        doc,
        "You open your laptop. The nightly spend monitor ran on Friday "
        "night as scheduled. It produced a monitor output file with the "
        "Critical severity flag. The file is sitting in "
        "outputs/daily-monitors/ with the anomaly clearly listed. But "
        "nobody saw it. Nobody was notified. The monitor ran, found the "
        "problem, wrote the report, and then nothing happened.",
    )
    para(
        doc,
        "This course fixes that gap. You build three things:",
    )
    numbered(
        doc,
        "**A Stop hook** that fires automatically when a Claude Code "
        "session ends. It reads the most recent monitor output file "
        "and determines the severity level: Routine, Anomaly, or "
        "Critical.",
    )
    numbered(
        doc,
        "**A notification router** (a bash script) that branches on "
        "severity. Routine results get a log entry. Anomaly results "
        "trigger a Slack message. Critical findings trigger both a "
        "Slack alert and an email escalation.",
    )
    numbered(
        doc,
        "**Two notification handlers** (Python scripts). One formats "
        "a Slack Block Kit payload for the procurement-alerts channel. "
        "The other builds a structured escalation email for the VP "
        "and the category manager.",
    )
    para(
        doc,
        "By the end, your nightly pipeline produces a monitor report, "
        "classifies it, and routes it to the right audience. No human "
        "checks a folder at midnight. No $138,000 anomaly sits unseen "
        "for an entire weekend.",
    )
    para(
        doc,
        "The practice scenario uses Ironclad Procurement Group, a "
        "US-based procurement shared services center. You are the "
        "Procurement Analytics Lead. The company has 40 suppliers "
        "across five categories, 851 transactions over 30 days, and "
        "planted anomalies on April 21 (three suppliers above 5x daily "
        "average) and April 24 (Great Lakes Steel at 12x, total daily "
        "spend of $538,200 exceeding the $500,000 ceiling).",
    )

    heading(doc, "The six lessons at a glance", 2)
    fill_table(
        doc,
        ["Lesson", "Title", "Time", "What you build"],
        [
            [
                "1",
                "Stop Hooks",
                "25 min",
                "A minimal Stop hook that writes a log entry when a session ends",
            ],
            [
                "2",
                "Notification Hooks",
                "35 min",
                "The severity classification logic: how to extract Routine, Anomaly, or Critical from a monitor file",
            ],
            [
                "3",
                "Tiered Notification Router",
                "50 min",
                "The bash router script (session-complete-hook.sh) that branches by severity",
            ],
            [
                "4",
                "Slack Webhook Integration",
                "45 min",
                "Two Python handlers: slack-notify.py for Slack Block Kit payloads and escalation-email.py for email drafts",
            ],
            [
                "5",
                "Complete Nightly Stack",
                "40 min",
                "The full pipeline from cron trigger to headless session to Stop hook to notification",
            ],
            [
                "6",
                "End-to-End Test",
                "25 min",
                "Two full test runs (Critical and Routine) verifying every artifact lands in the right folder",
            ],
        ],
    )
    para(
        doc,
        "Total time: about four hours. Comfortable in two afternoon "
        "sessions or five daily blocks of 45 to 60 minutes.",
    )

    # ===================================================================
    # 3. What is in the course folder
    # ===================================================================
    heading(doc, "3. What is in the course folder", 1)
    para(
        doc,
        "The course folder is self-contained. Everything you need is "
        "inside. No external downloads, no shared drives, no separate "
        "data store.",
    )
    code_block(
        doc,
        "Course_07_The_Pipeline_Automator/\n"
        "  README.md\n"
        "  COURSE_OVERVIEW.md\n"
        "  lessons/\n"
        "    Lesson_01_Stop_Hooks.md\n"
        "    Lesson_02_Notification_Hooks.md\n"
        "    Lesson_03_Tiered_Notification_Router.md\n"
        "    Lesson_04_Slack_Webhook_Integration.md\n"
        "    Lesson_05_Complete_Nightly_Stack.md\n"
        "    Lesson_06_End_To_End_Test.md\n"
        "  practice/\n"
        "    CLAUDE.md\n"
        "    data/\n"
        "      daily-spend.csv        (851 rows, 30 days)\n"
        "      supplier-master.csv    (40 suppliers)\n"
        "      thresholds.json        (alert thresholds)\n"
        "    outputs/\n"
        "      daily-monitors/        (sample monitor files)\n"
        "    hooks/                    (your scripts go here)\n"
        "    notifications/           (output landing zone)\n"
        "  solutions/\n"
        "    session_complete_hook_solution.sh\n"
        "    slack_notify_solution.py\n"
        "    escalation_email_solution.py\n"
        "  scripts/\n"
        "    build_course_data.py     (regenerator)",
    )
    para(doc, "Here is what each piece does and why it matters.")

    heading(doc, "practice/data/", 2)
    para(
        doc,
        "This folder holds the source data: 851 spend transactions in "
        "daily-spend.csv, 40 suppliers in supplier-master.csv, and the "
        "alert threshold definitions in thresholds.json. All files are "
        "read-only during the course. You analyze them but never edit "
        "them.",
    )
    para(
        doc,
        "**Why this matters.** Without realistic data volumes, the "
        "exercises feel artificial. A 10-row CSV does not reveal the "
        "patterns that 851 rows do. The planted anomalies on April 21 "
        "and April 24 give you known test cases so you can verify your "
        "pipeline routes correctly.",
    )

    heading(doc, "practice/outputs/daily-monitors/", 2)
    para(
        doc,
        "This folder holds three sample monitor output files, one per "
        "severity level. monitor-2026-04-20.md is Routine "
        "($142,380.45 daily spend, zero anomalies). "
        "monitor-2026-04-21.md is Anomaly (three suppliers above 5x). "
        "monitor-2026-04-24.md is Critical (Great Lakes Steel at 12x, "
        "$538,200 total spend).",
    )
    para(
        doc,
        "**Why this matters.** Your Stop hook reads the most recent "
        "file in this folder and routes based on its severity. These "
        "three files let you test all three routing paths without "
        "running the full spend analysis each time. They are your "
        "known-good test fixtures.",
    )

    heading(doc, "practice/hooks/", 2)
    para(
        doc,
        "This is where you build the three scripts that form the "
        "notification layer: session-complete-hook.sh (the router), "
        "slack-notify.py (the Slack formatter), and "
        "escalation-email.py (the email drafter). The folder starts "
        "empty. You create each file during the lessons.",
    )
    para(
        doc,
        "**Why this matters.** Keeping scripts in a dedicated hooks/ "
        "folder separates automation logic from data and outputs. "
        "When your VP asks \"where is the notification code?\", the "
        "answer is one folder, not scattered files across the project.",
    )

    heading(doc, "practice/notifications/", 2)
    para(
        doc,
        "This is the landing zone for notification outputs. It has "
        "three subfolders: monitor-log.txt (a flat log of every "
        "session result), slack-messages/ (Slack Block Kit JSON "
        "payloads), and email-drafts/ (structured escalation emails).",
    )
    para(
        doc,
        "**Why this matters.** Auditors need a trail. The log file "
        "records every nightly run with its severity and routing "
        "decision. The JSON payloads prove what was sent to Slack and "
        "email. If the VP asks \"when did we first flag Great Lakes "
        "Steel?\", the answer is in this folder.",
    )

    heading(doc, "solutions/", 2)
    para(
        doc,
        "Reference answers for all three scripts. Look at them only "
        "after you have attempted each lesson. The solutions match the "
        "exact format, the regex patterns, and the notification "
        "payloads described in the lessons.",
    )
    para(
        doc,
        "**Why this matters.** If your script does not work and you "
        "have spent 15 minutes debugging, the solution file will show "
        "you the exact pattern that works. Comparing your attempt to "
        "the solution is where most of the learning happens.",
    )

    heading(doc, "scripts/build_course_data.py", 2)
    para(
        doc,
        "A deterministic data regenerator. If you delete or corrupt "
        "the practice data, run this script to restore everything. It "
        "uses random.seed(42) so every regeneration produces identical "
        "data.",
    )
    para(
        doc,
        "**Why this matters.** Practice data is expendable. You should "
        "feel free to experiment, break things, and try different "
        "approaches. One command brings the data back to its starting "
        "state.",
    )

    # ===================================================================
    # 4. Time savings reference table
    # ===================================================================
    heading(doc, "4. Time savings reference table", 1)
    para(
        doc,
        "This table compares the time each task takes without "
        "automation versus with a Stop hook and notification routing "
        "built in Claude Code (in the terminal).",
    )
    fill_table(
        doc,
        ["Task", "Without automation", "With Claude Code pipeline"],
        [
            [
                "Check nightly monitor output for anomalies",
                "8 min per morning (manual folder check, open file, read severity)",
                "0 min (Stop hook reads and routes automatically at session end)",
            ],
            [
                "Format a Slack alert for a detected anomaly",
                "12 min (copy data, format Slack blocks, paste into channel)",
                "0 min (slack-notify.py generates and saves the payload in under 2 seconds)",
            ],
            [
                "Draft an escalation email for a critical finding",
                "20 min (write subject, summarize anomaly, list actions, add recipients)",
                "0 min (escalation-email.py generates the draft in under 2 seconds)",
            ],
            [
                "Route a notification to the correct channel based on severity",
                "5 min (read severity, decide channel, switch to correct tool)",
                "0 min (the router script branches automatically by severity)",
            ],
            [
                "End-to-end nightly pipeline: analyze, classify, notify",
                "45 min total (manual analysis, manual notification, manual escalation)",
                "0 min of human time (cron triggers the full pipeline at 23:00)",
            ],
        ],
    )
    para(
        doc,
        "Over a 20-day work month, the manual approach consumes "
        "approximately 15 hours of analyst time on monitoring and "
        "notification alone. The automated pipeline reduces that to "
        "zero hours of daily effort, plus about 4 hours of one-time "
        "setup (this course).",
    )

    # ===================================================================
    # 5. What Stop hooks and notification routing are
    # ===================================================================
    heading(doc, "5. What Stop hooks and notification routing are", 1)

    heading(doc, "The mental model", 2)
    para(
        doc,
        "Think of a Claude Code session as a factory shift. The "
        "session starts, Claude does the work (reads data, runs "
        "analysis, writes output files), and then the session ends. "
        "A Stop hook is the inspector who walks the floor after the "
        "shift ends, checks what was produced, and decides what "
        "happens next.",
    )
    para(
        doc,
        "Claude Code supports three types of hooks. PreToolUse hooks "
        "fire before each tool call (a file read, a file write, a "
        "bash command). PostToolUse hooks fire after each tool call. "
        "Stop hooks fire once, when the entire session ends. For "
        "notification routing, Stop hooks are the right choice. You "
        "do not want a Slack message every time Claude writes a "
        "temporary file. You want one notification at the end, based "
        "on the final output.",
    )
    fill_table(
        doc,
        ["Hook type", "When it fires", "How many times", "Best use case"],
        [
            [
                "PreToolUse",
                "Before each tool call",
                "Many times per session",
                "Blocking a dangerous operation, validation before execution",
            ],
            [
                "PostToolUse",
                "After each tool call completes",
                "Many times per session",
                "Logging each file write, running style checks on saved files",
            ],
            [
                "Stop",
                "When the session ends",
                "Once",
                "End-of-session notifications, summaries, cleanup, downstream triggers",
            ],
        ],
    )

    heading(doc, "How a Stop hook works in practice", 2)
    para(
        doc,
        "You register a Stop hook in the file .claude/settings.json "
        "inside your project folder. The registration looks like this:",
    )
    code_block(
        doc,
        '{\n'
        '  "hooks": {\n'
        '    "Stop": [\n'
        '      {\n'
        '        "matcher": "",\n'
        '        "command": "bash hooks/session-complete-hook.sh"\n'
        '      }\n'
        '    ]\n'
        '  }\n'
        '}',
    )
    para(
        doc,
        "The \"Stop\" key tells Claude Code (in the terminal) to run "
        "this command when the session ends. The \"matcher\" field is "
        "empty because Stop hooks do not filter by tool name. They "
        "always fire at session end, regardless of what tools were "
        "called during the session.",
    )
    para(
        doc,
        "When you type /exit or when a headless session (claude "
        "--print) completes, Claude Code runs every command registered "
        "under the Stop key. Your script can then read output files, "
        "check results, and call downstream systems.",
    )

    heading(doc, "Notification routing: the three-tier model", 2)
    para(
        doc,
        "In the Ironclad Procurement Group scenario, the nightly "
        "spend monitor classifies each day into one of three severity "
        "levels. Each severity maps to a different notification "
        "channel.",
    )
    fill_table(
        doc,
        ["Severity", "Condition", "Notification channel", "Who sees it"],
        [
            [
                "Routine",
                "Daily spend under $500,000, zero transactions above 3x average",
                "Log file entry only",
                "Nobody, unless they check the log",
            ],
            [
                "Anomaly",
                "One or more transactions exceed 3x the supplier daily average",
                "Slack message to procurement-alerts channel",
                "Procurement analytics team",
            ],
            [
                "Critical",
                "Daily spend exceeds $500,000 ceiling, or a single transaction "
                "exceeds 10x average",
                "Email escalation to VP and category manager, plus Slack",
                "Senior leadership",
            ],
        ],
    )
    para(
        doc,
        "The router script reads the severity from the monitor file, "
        "then calls the appropriate handler. Routine gets a log line. "
        "Anomaly gets a Slack payload. Critical gets both a Slack "
        "payload and an email draft. The router uses a bash case "
        "statement, which is the same branching logic you would use in "
        "a spreadsheet IF formula, just written in shell script.",
    )
    para(
        doc,
        "**Why this matters.** Without tiered routing, every result "
        "looks the same until someone opens the file. A $142,000 "
        "routine day and a $538,000 critical day sit in the same "
        "folder with no visual distinction. Tiered routing ensures "
        "that the right people see the right alerts at the right time. "
        "Senior leadership only gets interrupted for critical findings. "
        "The analytics team sees anomalies in their Slack channel. "
        "Routine results produce no noise at all.",
    )

    # ===================================================================
    # 6. Worked examples
    # ===================================================================
    heading(doc, "6. Worked examples", 1)
    para(
        doc,
        "Each example below has four parts: the prompt to type, the "
        "folder layout, what you should see when it succeeds, and "
        "what Claude Code (in the terminal) did behind the scenes.",
    )

    # -- Example 1: Build the notification router --
    heading(doc, "Example 1: Build the notification router", 2)
    para(
        doc,
        "You need a bash script that reads the latest monitor file, "
        "extracts the severity, and calls the right handler. This is "
        "the core of the pipeline.",
    )

    heading(doc, "The prompt to type", 3)
    code_block(
        doc,
        "Create a bash script at hooks/session-complete-hook.sh that does "
        "the following:\n"
        "1. Find the most recent .md file in outputs/daily-monitors/ "
        "(by modification time).\n"
        "2. Extract the severity level from the **Severity:** line.\n"
        "3. If Routine: append a log line to notifications/monitor-log.txt "
        "with the date, severity, and file name.\n"
        "4. If Anomaly: append a log line, then call python "
        "hooks/slack-notify.py with the monitor file path.\n"
        "5. If Critical: append a log line, then call both "
        "hooks/slack-notify.py and hooks/escalation-email.py with "
        "the monitor file path.\n"
        "6. If severity is not recognized: log a warning.\n"
        "Use the script's own directory to build all paths. Do not "
        "hardcode absolute paths. Make the script executable.",
    )

    heading(doc, "The folder layout", 3)
    code_block(
        doc,
        "practice/\n"
        "  hooks/\n"
        "    session-complete-hook.sh   (created by this prompt)\n"
        "  outputs/\n"
        "    daily-monitors/\n"
        "      monitor-2026-04-20.md    (Routine)\n"
        "      monitor-2026-04-21.md    (Anomaly)\n"
        "      monitor-2026-04-24.md    (Critical)\n"
        "  notifications/\n"
        "    monitor-log.txt            (created by the script)\n"
        "  .claude/\n"
        "    settings.json              (Stop hook registration)",
    )

    heading(doc, "What you should see", 3)
    para(
        doc,
        "Claude Code (in the terminal) creates the file "
        "hooks/session-complete-hook.sh. When you run it manually with "
        "\"bash hooks/session-complete-hook.sh\", the script finds "
        "monitor-2026-04-24.md (the most recently modified file), "
        "extracts \"Critical\", and appends a line to "
        "notifications/monitor-log.txt reading: "
        "\"CRITICAL | monitor-2026-04-24.md | Routing to email "
        "escalation.\"",
    )

    heading(doc, "What Claude did, behind the scenes", 3)
    bullet(
        doc,
        "**Step A.** Claude Code (in the terminal) read the prompt "
        "and identified the six requirements: find latest file, "
        "extract severity, handle three severity levels, and handle "
        "unknown severity.",
    )
    bullet(
        doc,
        "**Step B.** It wrote a bash script using SCRIPT_DIR to "
        "locate itself, then built relative paths to the monitors "
        "folder, the notifications folder, and the log file. It used "
        "\"ls -t\" to sort monitor files by modification time and "
        "picked the first result as the latest file.",
    )
    bullet(
        doc,
        "**Step C.** It wrote a grep command with a regex pattern to "
        "extract the word after \"**Severity:**\" from the monitor "
        "file. This single line is the contract between the analysis "
        "step and the router.",
    )
    bullet(
        doc,
        "**Step D.** It created a case statement with four branches: "
        "Routine (log only), Anomaly (log and Slack), Critical (log, "
        "Slack, and email), and a wildcard fallback for unknown "
        "severity. It set the script to executable and saved it to "
        "hooks/session-complete-hook.sh.",
    )

    # -- Example 2: Generate a Slack alert for a critical anomaly --
    heading(doc, "Example 2: Generate a Slack alert for a critical spend anomaly", 2)
    para(
        doc,
        "The April 24 monitor file shows a critical anomaly: Great "
        "Lakes Steel at 12x the daily average ($138,082.19), with "
        "total daily spend of $538,200.18 exceeding the $500,000 "
        "ceiling. You need a Slack Block Kit payload that puts these "
        "numbers in front of the analytics team within seconds of "
        "the session ending.",
    )

    heading(doc, "The prompt to type", 3)
    code_block(
        doc,
        "Create hooks/slack-notify.py that does the following:\n"
        "1. Accept a monitor file path as a command-line argument.\n"
        "2. Read the file and extract the severity level.\n"
        "3. Extract all anomaly rows from the markdown table "
        "(Supplier, Transaction ID, Amount, Daily Avg, Multiple).\n"
        "4. Build a Slack Block Kit payload with a header block "
        "showing severity, a section block with the date and anomaly "
        "count, one section block per anomaly row, and a context "
        "block with the source file name.\n"
        "5. Save the payload as JSON to "
        "notifications/slack-messages/slack-YYYY-MM-DD.json "
        "(date from the file name).\n"
        "6. Use the script's own directory to build paths. "
        "No hardcoded absolute paths.",
    )

    heading(doc, "The folder layout", 3)
    code_block(
        doc,
        "practice/\n"
        "  hooks/\n"
        "    slack-notify.py                      (created by this prompt)\n"
        "  outputs/\n"
        "    daily-monitors/\n"
        "      monitor-2026-04-24.md              (Critical, input file)\n"
        "  notifications/\n"
        "    slack-messages/\n"
        "      slack-2026-04-24.json              (output file)",
    )

    heading(doc, "What you should see", 3)
    para(
        doc,
        "After running \"python hooks/slack-notify.py "
        "outputs/daily-monitors/monitor-2026-04-24.md\", you see: "
        "\"Slack payload saved to "
        "notifications/slack-messages/slack-2026-04-24.json\". "
        "The JSON file contains a header block with "
        "\":rotating_light: Spend Monitor Alert: Critical\", a section "
        "block for Great Lakes Steel showing $138,082.19 at 12.0x "
        "daily average, a divider, and a context block naming the "
        "source file.",
    )

    heading(doc, "What Claude did, behind the scenes", 3)
    bullet(
        doc,
        "**Step A.** Claude Code (in the terminal) read the prompt "
        "and identified three requirements: accept a file path, "
        "parse markdown tables, and produce Slack Block Kit JSON. It "
        "wrote a Python script using only standard library modules "
        "(json, os, re, sys, pathlib, datetime). No pip install "
        "needed.",
    )
    bullet(
        doc,
        "**Step B.** The script uses a regex pattern to match anomaly "
        "rows in the markdown table, pulling supplier name, "
        "transaction ID, amount, daily average, and multiple for each "
        "row. It chooses the Slack emoji based on severity: "
        "\":warning:\" for Anomaly, \":rotating_light:\" for "
        "Critical.",
    )
    bullet(
        doc,
        "**Step C.** It builds the blocks list with a header, a "
        "summary section, one section per anomaly, a divider, and a "
        "context block. Then it saves the payload using json.dump "
        "with indent=2 for readable output.",
    )
    bullet(
        doc,
        "**Step D.** If the SLACK_WEBHOOK_URL environment variable is "
        "set, the script also posts the payload to Slack using "
        "urllib.request. In the course, you save to a file for "
        "inspection instead of posting live.",
    )

    # ===================================================================
    # 7. Day in the Life
    # ===================================================================
    heading(doc, "7. A day in the life: Marcus, Procurement Analytics Lead", 1)
    para(
        doc,
        "Marcus is the Procurement Analytics Lead at Ironclad "
        "Procurement Group. He manages the nightly spend monitoring "
        "pipeline for five indirect spend categories across 40 "
        "suppliers. His VP, Diana Chen, expects anomaly alerts in "
        "the procurement-alerts Slack channel by 07:00, and critical "
        "escalations in her inbox before her 08:30 leadership standup. "
        "Marcus built his pipeline using Claude Code two weeks ago. "
        "Here is a typical Tuesday.",
    )

    # Scenario 1
    heading(doc, "07:15 - Checking the overnight results", 2)
    para(
        doc,
        "Marcus opens Slack on his phone. The procurement-alerts "
        "channel has one message from last night: an Anomaly alert "
        "showing Eagle Transport at 4.8x the daily average "
        "($28,400.00 on TXN009215). The message was posted at 23:04, "
        "four minutes after the nightly cron job ran. Marcus taps the "
        "message, reads the details, and decides it can wait until he "
        "gets to his desk. No fire drill.",
    )
    para(
        doc,
        "**What to learn from this.** The value of automated routing "
        "is not speed. It is confidence. Marcus did not check a folder. "
        "He did not open a file. The system told him exactly what "
        "happened and how severe it was. If the result had been "
        "Routine, he would have seen nothing at all, which is the "
        "correct behavior. Silence means \"no anomalies.\"",
    )

    # Scenario 2
    heading(doc, "08:45 - Investigating the anomaly at his desk", 2)
    para(
        doc,
        "Marcus opens the practice folder in his terminal. He wants "
        "to see the full monitor report for last night.",
    )
    code_block(
        doc,
        "cd practice\n"
        "cat outputs/daily-monitors/monitor-2026-04-22.md",
    )
    para(
        doc,
        "The file shows severity Anomaly, one flagged transaction "
        "(Eagle Transport, TXN009215, $28,400.00, 4.8x daily average), "
        "and three recommended actions. Marcus opens a Claude Code "
        "session to draft a quick Slack reply to his team.",
    )
    code_block(
        doc,
        "claude\n\n"
        "Read outputs/daily-monitors/monitor-2026-04-22.md. Draft a "
        "two-sentence Slack reply for the procurement-alerts channel "
        "that says I reviewed the Eagle Transport anomaly and I am "
        "calling the supplier this morning to verify the PO.",
    )
    para(
        doc,
        "Claude produces: \"Reviewed the Eagle Transport anomaly "
        "(TXN009215, $28,400.00, 4.8x daily avg). Calling the supplier "
        "this morning to verify the PO and will update this thread by "
        "noon.\" Marcus copies it into Slack.",
    )
    para(
        doc,
        "**What to learn from this.** The monitor file is the single "
        "source of truth. Marcus uses it both for the automated Slack "
        "alert and for his own follow-up. He does not retype the "
        "numbers. He asks Claude Code (in the terminal) to read the "
        "file and draft from it. This eliminates transcription errors.",
    )

    # Scenario 3
    heading(doc, "10:30 - VP asks about last week's critical alert", 2)
    para(
        doc,
        "Diana Slacks Marcus: \"Can you pull the details on that "
        "Great Lakes Steel escalation from Thursday? I need the "
        "numbers for the board deck.\" Marcus opens his terminal.",
    )
    code_block(
        doc,
        "cat notifications/email-drafts/escalation-2026-04-24.json",
    )
    para(
        doc,
        "The email draft shows: Great Lakes Steel, TXN008102, "
        "$138,082.19 at 12.0x daily average. Total daily spend: "
        "$538,200.18, exceeding the $500,000 ceiling by $38,200. "
        "Three recommended actions. Marcus copies the summary into "
        "Diana's Slack DM. Total time: 90 seconds.",
    )
    para(
        doc,
        "**What to learn from this.** Notification artifacts are "
        "also retrieval artifacts. The email draft that went out on "
        "Thursday night is a structured JSON file sitting in "
        "notifications/email-drafts/. Marcus does not reconstruct the "
        "data from the CSV. He opens the file the pipeline already "
        "built. Every pipeline output doubles as an audit record.",
    )

    # Scenario 4
    heading(doc, "13:00 - Adding a new threshold rule", 2)
    para(
        doc,
        "Marcus gets a request from the VP of Finance: flag any "
        "single transaction above $75,000, regardless of the supplier "
        "daily average. Marcus opens data/thresholds.json to "
        "review the current rules.",
    )
    code_block(
        doc,
        "claude\n\n"
        "Read data/thresholds.json. Add a new rule called "
        "\"absolute_transaction_ceiling_usd\" set to 75000. Update "
        "the critical severity definition to include: \"or a single "
        "transaction exceeds $75,000.\" Save the file.",
    )
    para(
        doc,
        "Claude Code (in the terminal) reads the JSON, adds the new "
        "field, updates the severity text, and saves. Marcus then "
        "exits the session. The Stop hook fires, but since the "
        "last monitor file is still from April 22 (Anomaly severity), "
        "the hook routes to Slack as expected. The new threshold will "
        "apply to tonight's analysis run.",
    )
    para(
        doc,
        "**What to learn from this.** Threshold changes are data "
        "changes, not code changes. Marcus did not edit the router "
        "script or the notification scripts. He updated "
        "thresholds.json. The analysis prompt reads thresholds.json "
        "every night. Tomorrow's run will use the new $75,000 ceiling "
        "automatically. Separating configuration from logic means "
        "Marcus can adjust rules without touching any script.",
    )

    # Scenario 5
    heading(doc, "15:00 - Running an ad-hoc analysis for a specific date", 2)
    para(
        doc,
        "A colleague asks Marcus to check April 18 because a "
        "supplier complained about a duplicate payment. Marcus runs "
        "a headless session for that date.",
    )
    code_block(
        doc,
        'claude --print "Read data/daily-spend.csv and '
        "data/thresholds.json. Analyze all transactions for "
        "2026-04-18. Identify anomalies at the 3x threshold. "
        "Save the report to "
        'outputs/daily-monitors/monitor-2026-04-18.md."',
    )
    para(
        doc,
        "Claude produces the report. The session ends. The Stop hook "
        "fires. The severity is Routine (no anomalies on April 18). "
        "The log shows: \"ROUTINE | monitor-2026-04-18.md | "
        "No anomalies.\" No Slack message. No email. Marcus opens the "
        "file, confirms no duplicate payment shows up as an anomaly, "
        "and replies to his colleague with the finding.",
    )
    para(
        doc,
        "**What to learn from this.** The pipeline works the same "
        "way for scheduled runs and ad-hoc runs. The Stop hook does "
        "not care whether cron triggered the session or Marcus typed "
        "the command. The routing logic is the same. This means Marcus "
        "can use the pipeline as a research tool during the day, not "
        "just as a nightly batch process.",
    )

    # Scenario 6
    heading(doc, "16:30 - Reviewing the week's notification log", 2)
    para(
        doc,
        "Before leaving for the day, Marcus checks the full "
        "notification log to confirm every night this week ran "
        "correctly.",
    )
    code_block(
        doc,
        "cat notifications/monitor-log.txt",
    )
    para(
        doc,
        "The log shows seven entries (five scheduled runs plus two "
        "ad-hoc runs). Five are ROUTINE, one is ANOMALY (April 22), "
        "and one is CRITICAL (April 24). Every entry has a timestamp, "
        "a severity label, and the file name. Marcus screenshots the "
        "log and drops it into the team's weekly status slide.",
    )
    para(
        doc,
        "**What to learn from this.** A plain text log file is the "
        "simplest and most portable audit trail. It does not require "
        "a database, a dashboard, or a reporting tool. Every line is "
        "one run. Sorting, filtering, and counting entries takes "
        "standard command-line tools. The log is the proof that the "
        "pipeline ran, what it found, and where it sent the result.",
    )

    # Scenario 7
    heading(doc, "17:00 - Onboarding a new analyst", 2)
    para(
        doc,
        "A new analyst, Priya, joins Marcus's team. Marcus walks her "
        "through the pipeline in 10 minutes. He opens the practice "
        "folder, shows her the data/ folder (read-only source), the "
        "outputs/daily-monitors/ folder (analysis results), the "
        "hooks/ folder (automation scripts), and the notifications/ "
        "folder (where alerts land). He runs the router script "
        "manually so she can see the log entry appear.",
    )
    code_block(
        doc,
        "bash hooks/session-complete-hook.sh\n"
        "cat notifications/monitor-log.txt | tail -1",
    )
    para(
        doc,
        "Priya sees the log entry and understands the flow. Marcus "
        "tells her: \"If you ever need to test a specific date, use "
        "claude --print with the date in the prompt. The Stop hook "
        "handles the rest.\"",
    )
    para(
        doc,
        "**What to learn from this.** A well-structured pipeline is "
        "self-documenting. The folder names tell you what each piece "
        "does. The log tells you what happened. A new team member can "
        "understand the system by looking at the folders and running "
        "one command. No training manual needed beyond this handout.",
    )

    # ===================================================================
    # 8. 20-Minute Sprint
    # ===================================================================
    heading(doc, "8. 20-Minute Sprint: your first notification in twenty minutes", 1)
    para(
        doc,
        "This section gets you from zero to your first routed "
        "notification in twenty minutes. Follow the four blocks below "
        "in order.",
    )

    heading(doc, "Minutes 0 to 5: Install and open the course folder", 2)
    para(
        doc,
        "If Claude Code is not yet installed, install it now. Open "
        "your terminal and run:",
    )
    code_block(doc, "npm install -g @anthropic-ai/claude-code")
    para(doc, "Then navigate to the practice folder:")
    code_block(
        doc,
        'cd "Detailed Course Content/Course_07_The_Pipeline_Automator/practice"',
    )
    para(
        doc,
        "Run \"ls\" to confirm you see the data/, outputs/, hooks/, "
        "and notifications/ subfolders. If you see them, you are in "
        "the right place.",
    )

    heading(doc, "Minutes 5 to 10: Review the sample monitor files", 2)
    para(
        doc,
        "Open each of the three sample monitor files to understand "
        "the severity format.",
    )
    code_block(
        doc,
        "cat outputs/daily-monitors/monitor-2026-04-20.md\n"
        "cat outputs/daily-monitors/monitor-2026-04-21.md\n"
        "cat outputs/daily-monitors/monitor-2026-04-24.md",
    )
    para(
        doc,
        "Note the \"**Severity:** Routine\", \"**Severity:** Anomaly\", "
        "and \"**Severity:** Critical\" lines. These are the values "
        "your router script will extract.",
    )
    para(
        doc,
        "Also open data/thresholds.json to see the routing rules: "
        "Routine goes to a log file, Anomaly goes to a Slack webhook, "
        "and Critical goes to email escalation.",
    )

    heading(doc, "Minutes 10 to 15: Create the router and register the Stop hook", 2)
    para(doc, "Start a Claude Code session:")
    code_block(doc, "claude")
    para(doc, "Type this prompt:")
    code_block(
        doc,
        "Create a bash script at hooks/session-complete-hook.sh that "
        "finds the most recent .md file in outputs/daily-monitors/, "
        "extracts the severity from the **Severity:** line, and "
        "branches: Routine logs to notifications/monitor-log.txt, "
        "Anomaly logs and calls python hooks/slack-notify.py, "
        "Critical logs and calls both hooks/slack-notify.py and "
        "hooks/escalation-email.py. Use relative paths based on the "
        "script's own directory. Make it executable.",
    )
    para(
        doc,
        "Claude creates the file. Now register it as a Stop hook. "
        "Type:",
    )
    code_block(
        doc,
        "Create .claude/settings.json with a Stop hook that runs "
        "\"bash hooks/session-complete-hook.sh\" when the session ends.",
    )
    para(doc, "Exit the session with /exit.")

    heading(doc, "Minutes 15 to 20: Test the router and see your first notification", 2)
    para(doc, "Run the router script manually:")
    code_block(
        doc,
        "bash hooks/session-complete-hook.sh\n"
        "cat notifications/monitor-log.txt",
    )
    para(
        doc,
        "You should see a log entry with \"CRITICAL | "
        "monitor-2026-04-24.md | Routing to email escalation.\" The "
        "Python scripts (slack-notify.py and escalation-email.py) do "
        "not exist yet, so those calls will fail. That is expected. "
        "The important result is that the severity extraction and "
        "routing logic work. You built your first automated "
        "notification router in under twenty minutes.",
    )
    para(
        doc,
        "Next step: continue to Lesson 4 in the course to build the "
        "Slack and email handler scripts.",
    )

    # ===================================================================
    # 9. First Week Day-by-Day Planner
    # ===================================================================
    heading(doc, "9. First week day-by-day planner", 1)
    para(
        doc,
        "Five days of escalating capability. Each day has a clear "
        "goal at the top. Spend 45 to 60 minutes per day.",
    )

    heading(doc, "Day 1: Understand hooks and test the wiring", 2)
    para(doc, "**Goals:**")
    bullet(doc, "Understand the three hook types (PreToolUse, PostToolUse, Stop).")
    bullet(doc, "Create a minimal Stop hook that writes to a log file.")
    bullet(doc, "Register the hook in .claude/settings.json.")
    bullet(doc, "Confirm the hook fires when a session ends.")
    para(
        doc,
        "Complete Lesson 1 (Stop Hooks). By the end of Day 1, you "
        "have a working Stop hook that writes a timestamped line to "
        "notifications/monitor-log.txt every time a session ends.",
    )

    heading(doc, "Day 2: Map severity levels and build the router", 2)
    para(doc, "**Goals:**")
    bullet(
        doc,
        "Review the three severity levels (Routine, Anomaly, Critical) "
        "and their conditions.",
    )
    bullet(
        doc,
        "Understand the notification routing table in thresholds.json.",
    )
    bullet(
        doc,
        "Build the tiered notification router "
        "(session-complete-hook.sh).",
    )
    bullet(
        doc,
        "Test the router against all three sample monitor files.",
    )
    para(
        doc,
        "Complete Lessons 2 and 3. By the end of Day 2, the router "
        "correctly identifies Routine, Anomaly, and Critical severity "
        "levels and logs the right routing decision for each.",
    )

    heading(doc, "Day 3: Build the Slack and email handlers", 2)
    para(doc, "**Goals:**")
    bullet(
        doc,
        "Create hooks/slack-notify.py that extracts anomalies and "
        "builds a Slack Block Kit JSON payload.",
    )
    bullet(
        doc,
        "Create hooks/escalation-email.py that extracts the summary "
        "and recommended actions and builds a structured email draft.",
    )
    bullet(
        doc,
        "Test both scripts against the sample monitor files.",
    )
    bullet(
        doc,
        "Verify the Slack payload contains all anomaly rows and the "
        "email draft contains the correct figures.",
    )
    para(
        doc,
        "Complete Lesson 4. By the end of Day 3, the full notification "
        "chain works: router calls Slack script, Slack script produces "
        "a JSON payload. Router calls email script, email script "
        "produces a draft with the VP distribution list.",
    )

    heading(doc, "Day 4: Connect the full pipeline and schedule it", 2)
    para(doc, "**Goals:**")
    bullet(
        doc,
        "Understand headless mode (claude --print) and how the Stop "
        "hook fires after a headless session.",
    )
    bullet(
        doc,
        "Run the full pipeline manually: analysis, monitor output, "
        "Stop hook, notification routing.",
    )
    bullet(
        doc,
        "Write the cron entry (or Windows Task Scheduler task) for "
        "the nightly 23:00 run.",
    )
    bullet(
        doc,
        "Review the environment requirements (PATH, working directory, "
        "API credentials).",
    )
    para(
        doc,
        "Complete Lesson 5. By the end of Day 4, you can run the full "
        "pipeline from the command line and you have a cron entry "
        "ready for deployment.",
    )

    heading(doc, "Day 5: End-to-end test, reflect, and plan next week", 2)
    para(doc, "**Goals:**")
    bullet(
        doc,
        "Run the full end-to-end test: Critical (April 24) and "
        "Routine (April 20).",
    )
    bullet(
        doc,
        "Verify all five checkpoints: monitor file exists, severity "
        "correct, log entry present, Slack payload present (or absent), "
        "email draft present (or absent).",
    )
    bullet(
        doc,
        "Reflect on what you built and identify the next monitoring "
        "task you want to automate.",
    )
    para(
        doc,
        "Complete Lesson 6. By the end of Day 5, your pipeline has "
        "passed two full end-to-end tests. You can answer your VP's "
        "question (\"Is the pipeline live?\") with test results to "
        "prove it.",
    )

    # ===================================================================
    # 10. The Pattern
    # ===================================================================
    heading(doc, "10. The pattern: applying notification routing to any monitoring task", 1)
    para(
        doc,
        "The pipeline you built in this course follows a pattern that "
        "applies to any monitoring task, not just spend anomalies. "
        "Here is the general shape.",
    )
    numbered(
        doc,
        "**Define severity levels and thresholds.** Write them in a "
        "JSON file (thresholds.json or equivalent). Keep them separate "
        "from code so you can change rules without editing scripts.",
    )
    numbered(
        doc,
        "**Build the analysis step.** This is the prompt that reads "
        "your data, applies the thresholds, and writes a structured "
        "output file with a severity line. The severity line is the "
        "contract between the analysis and the router.",
    )
    numbered(
        doc,
        "**Build the router.** A Stop hook script that finds the most "
        "recent output file, extracts the severity, and branches to "
        "the correct handler. Keep the router thin. It should not "
        "contain analysis logic or formatting logic.",
    )
    numbered(
        doc,
        "**Build the handlers.** One script per notification channel. "
        "Each handler takes a file path as input, extracts what it "
        "needs, and produces its output (a Slack payload, an email "
        "draft, a ticket, a dashboard update). Handlers are "
        "independent. Adding a new channel means adding a new handler "
        "and one more line in the router's case statement.",
    )
    numbered(
        doc,
        "**Schedule the pipeline.** Use cron, Task Scheduler, or "
        "another scheduler to trigger claude --print at the desired "
        "time. The Stop hook handles everything after the session ends.",
    )
    para(
        doc,
        "This same pattern works for contract expiry monitoring, "
        "supplier risk score changes, invoice discrepancy detection, "
        "and any other task where you analyze data on a schedule and "
        "need different audiences to see different results.",
    )

    heading(doc, "Example: applying the pattern to contract expiry monitoring", 2)
    para(
        doc,
        "Suppose you manage 200 active contracts. You want a nightly "
        "check that flags contracts expiring within 30, 60, or 90 "
        "days. Here is how you would apply the pattern.",
    )
    numbered(
        doc,
        "**Define severity levels.** Write a thresholds.json: "
        "\"green\" for contracts expiring in 61 to 90 days (log only), "
        "\"amber\" for 31 to 60 days (Slack alert to the category "
        "manager), \"red\" for 30 days or fewer (email escalation to "
        "the VP and the legal team).",
    )
    numbered(
        doc,
        "**Build the analysis prompt.** \"Read contracts.csv. For "
        "each contract, calculate days until expiry. Flag any contract "
        "within 90 days. Save the report to "
        "outputs/expiry-monitors/expiry-YYYY-MM-DD.md with a "
        "Severity line.\"",
    )
    numbered(
        doc,
        "**Reuse the router.** Copy session-complete-hook.sh. Change "
        "the MONITORS_DIR to outputs/expiry-monitors/. Update the "
        "case labels from Routine/Anomaly/Critical to Green/Amber/Red.",
    )
    numbered(
        doc,
        "**Reuse the handlers.** The Slack and email scripts need "
        "minor changes to extract contract data instead of spend "
        "data. The JSON structure stays the same.",
    )
    para(
        doc,
        "The total effort for this second pipeline is about one hour, "
        "because the pattern is already proven. The first pipeline "
        "took four hours. Every subsequent pipeline takes a fraction "
        "of that.",
    )
    para(
        doc,
        "**Why this matters.** The pattern separates four concerns: "
        "scheduling, analysis, classification, and notification. "
        "Each concern lives in its own file. You can change the "
        "schedule without touching the analysis. You can add a new "
        "notification channel without touching the router. You can "
        "adjust thresholds without touching any script. This "
        "separation is what makes the pipeline maintainable by a "
        "team that does not have software engineers.",
    )

    # ===================================================================
    # 11. Troubleshooting
    # ===================================================================
    heading(doc, "11. Troubleshooting", 1)
    para(
        doc,
        "**Cautions and ground rules.** Stop hooks run automatically "
        "after every session, including interactive sessions where you "
        "are just exploring files. If your Stop hook calls an external "
        "system (Slack, email), make sure it only sends when a "
        "genuinely new monitor file exists. The sample router checks "
        "for the latest file by modification time, which means "
        "a file you touched during an unrelated session could trigger "
        "a duplicate notification. For production use, add a check "
        "that compares the file's modification time against the last "
        "log entry timestamp. Also note that Stop hooks run with the "
        "same permissions as the user who started the session. They "
        "can read, write, and execute anything that user can. Review "
        "every script you register as a hook before enabling it.",
    )

    para(
        doc,
        "**Symptom:** The Stop hook does not fire when you type /exit.",
    )
    para(
        doc,
        "**Fix:** Confirm that .claude/settings.json is in the "
        "practice folder (the folder where you started Claude Code), "
        "not in a parent or child folder. The Stop hook registration "
        "is project-specific. Also confirm the key is \"Stop\" "
        "(capital S), not \"stop\" or \"PostToolUse\".",
    )

    para(
        doc,
        "**Symptom:** The router script picks the wrong monitor file.",
    )
    para(
        doc,
        "**Fix:** The script uses \"ls -t\" to sort by modification "
        "time. If you edited an older file, it becomes the \"latest.\" "
        "Use the touch command to reset modification times for "
        "testing, or sort by file name instead if your naming "
        "convention is date-based. Example: "
        "\"touch outputs/daily-monitors/monitor-2026-04-24.md\" makes "
        "that file the most recently modified.",
    )

    para(
        doc,
        "**Symptom:** Severity comes back empty and the router falls "
        "through to the unknown branch.",
    )
    para(
        doc,
        "**Fix:** The grep pattern expects the exact format "
        "\"**Severity:** Critical\" with one space after the colon "
        "and Markdown bold markers (double asterisks). If the monitor "
        "file uses a different format, the pattern will not match. "
        "Test with: grep \"Severity\" "
        "outputs/daily-monitors/monitor-2026-04-24.md",
    )

    para(
        doc,
        "**Symptom:** The Slack payload has zero anomaly rows even "
        "though the monitor file lists three.",
    )
    para(
        doc,
        "**Fix:** The regex in slack-notify.py must match the exact "
        "markdown table format, including pipe characters, dollar "
        "signs, and commas in amounts. Check the anomaly table in the "
        "monitor file. If Claude formatted it differently than "
        "expected, update the regex to match. Run the script manually "
        "and check stderr for error messages.",
    )

    para(
        doc,
        "**Symptom:** The cron job runs but Claude Code is not found.",
    )
    para(
        doc,
        "**Fix:** Cron uses a minimal PATH that does not include your "
        "shell profile. Add the full path to the claude binary in "
        "the crontab, or set PATH at the top of the crontab file. "
        "Run \"which claude\" in your terminal to find the path. "
        "Example: PATH=/usr/local/bin:/usr/bin at the top of crontab.",
    )

    para(
        doc,
        "**Symptom:** The headless session (claude --print) produces "
        "no output file.",
    )
    para(
        doc,
        "**Fix:** In headless mode, Claude Code (in the terminal) "
        "does not ask clarifying questions. If the prompt is ambiguous "
        "about where to save the output, Claude may print the report "
        "to stdout instead of writing a file. Make the output path "
        "explicit in the prompt: \"Save the report to "
        "outputs/daily-monitors/monitor-2026-04-25.md.\"",
    )

    # ===================================================================
    # 12. Done checklist
    # ===================================================================
    heading(doc, "12. Done checklist", 1)
    para(
        doc,
        "Run this list before you consider any pipeline artifact "
        "finished.",
    )
    numbered(
        doc,
        "The Stop hook is registered in .claude/settings.json under "
        "the \"Stop\" key.",
    )
    numbered(
        doc,
        "The router script uses the script's own directory "
        "(SCRIPT_DIR) for all paths. No hardcoded absolute paths.",
    )
    numbered(
        doc,
        "The router correctly routes Routine to log only, Anomaly to "
        "Slack, and Critical to both Slack and email.",
    )
    numbered(
        doc,
        "The Slack payload includes the severity emoji, the date, the "
        "anomaly count, one section block per anomaly, and a context "
        "block naming the source file.",
    )
    numbered(
        doc,
        "The email draft includes the to and cc addresses, the "
        "subject line with the date, the summary paragraph, three "
        "recommended actions, and the four-hour response deadline.",
    )
    numbered(
        doc,
        "The monitor-log.txt file has one entry per session, with "
        "timestamp, severity, and file name.",
    )
    numbered(
        doc,
        "The end-to-end test passes for both Critical (April 24) and "
        "Routine (April 20): correct monitor file, correct severity, "
        "correct log entry, correct presence or absence of Slack "
        "payload and email draft.",
    )
    numbered(
        doc,
        "No em-dashes or en-dashes in any script, any prompt, or any "
        "notification output.",
    )
    numbered(
        doc,
        "Every currency figure uses USD with commas ($138,082.19, "
        "not 138082.19). Every date uses YYYY-MM-DD format.",
    )
    numbered(
        doc,
        "The notification pipeline can run headless (claude --print) "
        "and the Stop hook fires correctly after the headless session "
        "ends.",
    )

    # ===================================================================
    # Save
    # ===================================================================
    # Try primary path; fall back to a temp name if locked
    try:
        doc.save(str(OUTPUT_PATH))
        print(f"Saved: {OUTPUT_PATH}")
    except PermissionError:
        alt = OUTPUT_PATH.with_name(OUTPUT_PATH.stem + "_new.docx")
        doc.save(str(alt))
        print(f"Primary path locked. Saved to: {alt}")
        print("Delete the old file and rename this one.")
    else:
        print(f"File size: {OUTPUT_PATH.stat().st_size:,} bytes")


if __name__ == "__main__":
    build()
