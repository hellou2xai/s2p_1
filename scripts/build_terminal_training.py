"""Build the Claude Code (terminal) training guide for S2P professionals.

Written in the same shape as the Cowork and Code Desktop training docs:
cover, exec summary with time-savings table, install, distinctive features,
permission modes, slash commands, hooks, day in the life, five use cases,
first-week planner, twenty-minute sprint, team deployment, troubleshooting.

All five comprehensive-training-guide rules from CLAUDE.md applied.
Style follows CLAUDE.md: no em-dashes, Oxford commas, British English,
no banned phrases, every worked example has the four parts (prompt,
folder layout, what you should see, behind-the-scenes walkthrough).
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


OUTPUT_PATH = Path(
    r"C:\Users\sambi\OneDrive - U2xAI\Claude Code Projects"
    r"\S2p Training\Course List\Claude Code Foundation for S2P"
    r"\Handouts\Claude_Code_Terminal_S2P_Training.docx"
)


# ---------------- helpers (with auto-restart numbering) ---------------------

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


# ---------------- content ---------------------------------------------------

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

    # ---------------- Cover ----------------
    para(doc, "U2xAI", italic=True, size=12)
    para(doc, "PROCUREMENT AI EXCELLENCE SERIES", italic=True, size=10)
    doc.add_heading("Claude Code in the Terminal", level=0)
    para(doc, "Complete Training Guide for S2P Professionals", italic=True, size=14)
    para(doc, "CLI | Hooks | Slash Commands | MCP | Headless Mode | Audit Trail", italic=True)
    para(doc, "Step-by-step | Daily use scenarios | Full worked examples", italic=True)
    para(doc, "Prepared by U2xAI | u2xai.com", italic=True, size=10)

    # ---------------- 1. How to use this guide ----------------
    heading(doc, "1. How to use this guide", 1)
    para(
        doc,
        "This guide is for procurement professionals who want full control "
        "of their Claude workflows: scripted, repeatable, auditable, and "
        "automatable. The terminal version of Claude Code is the CLI "
        "sibling of Claude Code Desktop. It does the same work, on the "
        "same files, using the same models. The difference is that "
        "everything happens in a black command-line window, with the "
        "scrollback as your audit log.",
    )
    para(
        doc,
        "You do not need to be a developer. You need three skills: open a "
        "terminal, type one command at a time, and read what comes back. "
        "Everything in this guide is shown end to end with the exact "
        "commands and what you should see on screen.",
    )
    para(
        doc,
        "Recommended path for a first-time reader: read sections 2 and 3 "
        "for context. Follow section 4 to install. Follow section 5 to "
        "build your project folder. Jump to section 11 (the 20-minute "
        "sprint) for your first real task. Then read the remaining "
        "sections as your needs grow.",
    )

    # ---------------- 2. Executive summary ----------------
    heading(doc, "2. Executive summary", 1)
    para(
        doc,
        "Claude Code in the terminal is Anthropic's CLI agent. Installed "
        "via npm, it runs inside any terminal (Mac Terminal, Windows "
        "PowerShell, the Linux shell on a corporate jumpbox over SSH). "
        "It opens the folder you start it in, reads any CLAUDE.md it "
        "finds, and works on your files exactly the way Claude Code "
        "Desktop does, but without a GUI.",
    )
    para(
        doc,
        "The CLI form has three advantages for S2P professionals.",
    )
    bullet(doc, "**The scrollback is your audit log.** Every prompt, every file change, every clarifying question is on screen and saveable as plain text. Critical for any output that lands with a CFO, a board, or an external auditor.")
    bullet(doc, "**Everything is hookable.** Hooks (small commands that fire on tool use, on Claude finishing, on a notification) let you enforce house style, run a linter, or stop dangerous operations without trusting yourself to remember.")
    bullet(doc, "**It runs anywhere a terminal runs.** SSH into a corporate jumpbox to read Oracle exports that live behind your firewall. Run from CI to fire a monthly variance memo. Schedule from cron. None of this needs a GUI.")

    heading(doc, "Time savings reference table", 2)
    para(doc, "Source: U2xAI practitioner benchmarks across procurement automation work.")
    fill_table(
        doc,
        ["Procurement task", "Without Claude Code", "With Claude Code in the terminal"],
        [
            ("Bulk NDA review across 24 supplier contracts", "2 to 3 days of manual reading", "30 to 45 minutes (one prompt, full audit log in scrollback)"),
            ("Monthly variance memo, repeated cadence", "3 to 4 hours every month", "Saved as a slash command, replayable in 8 minutes"),
            ("House style enforcement on every output", "Random, depends on reviewer attention", "Automated by a PostToolUse hook on every save"),
            ("Audit trail for a CFO-bound analysis", "Reconstruct from chat history, 1 to 2 hours", "Terminal scrollback saved as plain text, 30 seconds"),
            ("Live Oracle PO anomaly detection", "Export CSV nightly, 15 minutes", "MCP server, real-time, zero seconds"),
            ("Refresh quarterly RFP across 4 categories", "1 day per category", "20 to 30 minutes per category, in parallel using sub-agents"),
        ],
    )

    # ---------------- 3. Understanding Claude Code (terminal) ----------------
    heading(doc, "3. Understanding Claude Code (terminal)", 1)
    para(
        doc,
        "Claude Code in the terminal is one binary, installed once per "
        "machine. You start it inside any folder by typing `claude`. The "
        "tool prints a prompt, you type your task, Claude reads, plans, "
        "and acts. When you are done you type `/quit` and the session "
        "ends. The full record of the session stays in your terminal "
        "scrollback until you close the window.",
    )

    heading(doc, "Claude Code in the terminal vs Claude Code Desktop", 2)
    fill_table(
        doc,
        ["Dimension", "Terminal (this guide)", "Desktop (separate guide)"],
        [
            ("Where it lives", "Any terminal: Mac Terminal, PowerShell, Linux shell, SSH", "The Code tab in the Claude desktop app"),
            ("Visual diff viewer", "No. Diffs print as text in scrollback.", "Yes. Side-by-side diff before each save."),
            ("Multi-session sidebar", "No. One session per terminal window. Open a second terminal for a second session.", "Yes. Sidebar with up to five parallel sessions."),
            ("Hooks", "Yes. PostToolUse, PreToolUse, Stop, Notification, others. Configured in .claude/settings.json.", "Yes, via the same mechanism."),
            ("Slash commands", "Yes. Built-in (/help, /quit) and custom (any .md file in .claude/commands/).", "Yes. Same mechanism."),
            ("Headless mode", "Yes. claude -p \"do X\" runs one shot, exits. Use in cron, CI, or a Slack-triggered script.", "Limited. Routines cover the scheduled case."),
            ("MCP servers", "Yes. Configured in .mcp.json or via /mcp slash command.", "Yes. Same mechanism."),
            ("Best for procurement", "Audit-bound work, scripted automation, SSH access to corporate data, headless CI runs.", "Visual review of changes, parallel category analyses, scheduled Routines, fastest first-day experience."),
        ],
    )

    heading(doc, "When to choose the terminal version", 2)
    bullet(doc, "Your data lives behind a firewall and you reach it via SSH.")
    bullet(doc, "Your team needs an audit trail for every output that goes to a CFO or a board.")
    bullet(doc, "You want to enforce writing rules with a hook so no analyst can forget.")
    bullet(doc, "You want to fire one-shot analyses from a cron schedule, a Slack command, or a CI pipeline.")
    bullet(doc, "You want to commit your CLAUDE.md, your hooks, and your slash commands to Git so the team works from one source of truth.")

    heading(doc, "When to use the Desktop version instead", 2)
    bullet(doc, "Your first day on Claude. The Desktop app is friendlier.")
    bullet(doc, "You need a side-by-side visual diff before each save.")
    bullet(doc, "You want to run three category analyses in parallel without opening three terminals.")
    bullet(doc, "Your work is mostly visual: PowerPoint decks, redlined Word documents, RAG-coloured Excel files.")

    # ---------------- 4. Complete installation guide ----------------
    heading(doc, "4. Complete installation guide", 1)
    para(
        doc,
        "Total time: 10 minutes if Node.js is already installed, 20 "
        "minutes if it is not. You only do this once per machine.",
    )

    heading(doc, "Part A: Install Node.js (one-off prerequisite)", 2)
    para(doc, "Claude Code in the terminal is distributed via npm, the Node.js package manager. If you already have Node.js, skip to Part B. Otherwise:")
    numbered(doc, "Open https://nodejs.org in a browser.")
    numbered(doc, "Click the green button labelled \"LTS\" (long-term support). Do not pick \"Current\".")
    numbered(doc, "The installer downloads to your Downloads folder.")
    numbered(doc, "Run the installer. Click through with default settings.")
    numbered(doc, "Open a new terminal window after the install completes. New terminal so it picks up the updated PATH.")
    numbered(doc, "Verify with the command:")
    code_block(doc, "node --version")
    para(doc, "What you should see: a version number like `v22.10.0`. If you see \"command not found\", reopen the terminal or restart your computer.")

    heading(doc, "Part B: Install Claude Code", 2)
    numbered(doc, "Open a terminal (Mac Terminal, Windows PowerShell, Linux shell).")
    numbered(doc, "Type the install command:")
    code_block(doc, "npm install -g @anthropic-ai/claude-code")
    numbered(doc, "Wait. The install takes 30 to 60 seconds.")
    numbered(doc, "Verify with:")
    code_block(doc, "claude --version")
    para(doc, "What you should see: a version string. If you see \"command not found\", restart the terminal once more, or check that npm's global bin folder is on your PATH.")

    heading(doc, "Part C: Sign in", 2)
    numbered(doc, "From any folder, start Claude:")
    code_block(doc, "claude")
    numbered(doc, "On first run, Claude prints a sign-in URL.")
    numbered(doc, "Open the URL in a browser. Sign in with your Anthropic account (the same one you use for claude.ai).")
    numbered(doc, "Approve the CLI to access your account.")
    numbered(doc, "Return to the terminal. The Claude prompt appears.")
    numbered(doc, 'Type "/quit" to exit. Your sign-in is saved. You will not have to sign in again.')

    heading(doc, "Part D: Build your procurement project folder", 2)
    para(doc, "Claude Code in the terminal opens whatever folder you start it in. Build the folder once with the standard layout (this matches the Folder_Structure rule for the course).")
    numbered(doc, "Choose a parent folder, for example `~/Documents/Procurement` on Mac or `C:\\Users\\<you>\\Documents\\Procurement` on Windows.")
    numbered(doc, "Inside it, create a project folder. Use a date-prefixed name for time-bounded work, or a category name for ongoing work.")
    code_block(doc, 'mkdir -p ~/Documents/Procurement/2026-Q2_Office_Supplies_RFP\ncd ~/Documents/Procurement/2026-Q2_Office_Supplies_RFP')
    numbered(doc, "Create the standard subfolders:")
    code_block(doc, "mkdir Master Drafts Outputs Reference Archive")
    numbered(doc, "Move your source files into Master/. Master/ is read-only by convention; Claude must not write here.")

    heading(doc, "Part E: Create your CLAUDE.md", 2)
    para(doc, "CLAUDE.md is the instructions file Claude reads at the start of every session. Without one, Claude has no procurement context and your prompts have to repeat the same setup every time. With one, your CLAUDE.md is the single source of truth for your team's standards.")
    para(doc, "Save the file at the project folder root with this template. Replace every value in angle brackets.")
    code_block(
        doc,
        "# Procurement Analytics standing instructions\n\n"
        "## Who I am\n"
        "Role: <Senior Category Manager, Office Supplies>\n"
        "Company: <Acme Plc>\n"
        "Categories: <office supplies, packaging>\n\n"
        "## What I am working on\n"
        "Year priority: <consolidate office-supplies suppliers from 14 to 4>\n"
        "Annual savings target: <420,000 GBP>\n\n"
        "## Folder rules\n"
        "Master/ is READ-ONLY. Never modify any file in Master/.\n"
        "Save all output to Drafts/ unless I tell you otherwise.\n"
        "Promote files to Outputs/ only when I confirm they are final.\n\n"
        "## Writing rules\n"
        "British English by default. Oxford commas. No em-dashes.\n"
        "No vague figures: write 1.4m savings, not 'significant savings'.\n"
        "Active voice. Specific suppliers and dates by name.\n\n"
        "## Standards\n"
        "Supplier scoring: price 40%, delivery 25%, quality 20%, "
        "compliance 15%.\n"
        "RAG bands for delivery: red below 90%, amber 90 to 95%, "
        "green 95% and up.\n"
        "Payment terms: net 60 unless contract states otherwise."
    )
    para(doc, "What you should see: a CLAUDE.md file at the project root. Next time you start `claude` in this folder, the prompt shows a small \"CLAUDE.md loaded\" indicator.")

    # ---------------- 5. Permission modes ----------------
    heading(doc, "5. Permission modes (the safety control)", 1)
    para(
        doc,
        "Claude Code in the terminal uses the same five permission modes "
        "as Claude Code Desktop. The wrong default either drowns you in "
        "approval prompts or, in production data, lets Claude rewrite a "
        "master contract without asking. Lesson 01 in the course covers "
        "this in full; the short version follows.",
    )
    fill_table(
        doc,
        ["Mode", "Behaviour", "When to pick it"],
        [
            ("Plan", "Read-only. Produces a numbered plan. No file changes.", "Any new task. Use this first, every time."),
            ("Ask permissions", "Stops on every file edit. Shows a diff. Asks yes or no.", "Lessons in production data the first time."),
            ("Auto accept edits", "Edits files automatically. Asks before terminal commands.", "A pattern you have run ten times before."),
            ("Auto", "Executes everything with background safety verification.", "Headless and scheduled runs only."),
            ("Bypass permissions", "No prompts at all.", "Sandboxed test environments. Never on real supplier data."),
        ],
    )
    para(doc, "Switch modes inside a session with the slash command:")
    code_block(doc, "/permission")
    para(doc, "Or set the mode at launch:")
    code_block(doc, "claude --permission-mode plan")

    # ---------------- 6. Slash commands ----------------
    heading(doc, "6. Slash commands: turning prompts into commands", 1)
    para(
        doc,
        "A slash command is a saved prompt you invoke by name. Built-in "
        "commands cover housekeeping (`/help`, `/quit`, `/memory`, "
        "`/permission`). Custom commands are any Markdown file you save "
        "in `.claude/commands/` at your project root or in `~/.claude/"
        "commands/` for personal commands across all projects. The file "
        "name (without the .md) becomes the command name.",
    )

    heading(doc, "Step-by-step: build a custom /scorecard command", 2)
    numbered(doc, "Create the commands folder if it does not exist:")
    code_block(doc, "mkdir -p .claude/commands")
    numbered(doc, "Create the file `.claude/commands/scorecard.md` with the prompt body:")
    code_block(
        doc,
        "Build a Q3 supplier scorecard pack.\n\n"
        "Read Master/q3_kpi_export.csv. Columns: Supplier, "
        "On_Time_Delivery_Pct, Defect_Rate_Pct, Spend_GBP, Open_Issues.\n"
        "Take the top 10 suppliers by Spend_GBP.\n"
        "Use Master/scorecard_template.xlsx as the layout.\n"
        "Apply the RAG bands from CLAUDE.md.\n"
        "Save outputs to Drafts/scorecards/, one .xlsx per supplier.\n"
        "Master/ is read-only."
    )
    numbered(doc, "Save the file. Quit and restart Claude (or run /memory reload).")
    numbered(doc, "Inside any new Claude session in this folder, run:")
    code_block(doc, "/scorecard")
    numbered(doc, "Claude reads the saved prompt and runs it. The next time you need a scorecard pack, type two characters, not 200.")

    heading(doc, "Six slash commands every procurement team should have", 2)
    bullet(doc, "**/variance-memo** for monthly spend variance memos.")
    bullet(doc, "**/contract-deviation** for contract clause review against your standard MSA.")
    bullet(doc, "**/savings-case** for CFO savings cases from a planned-savings register.")
    bullet(doc, "**/risk-brief** for on-demand supplier risk briefs.")
    bullet(doc, "**/onboarding-pack** for supplier onboarding pack assembly.")
    bullet(doc, "**/audit-trail** to save the current session scrollback to Outputs/audit/.")

    # ---------------- 7. Hooks ----------------
    heading(doc, "7. Hooks: enforcing standards automatically", 1)
    para(
        doc,
        "A hook is a small command that fires automatically when something "
        "happens in Claude Code. Procurement-relevant hook events:",
    )
    bullet(doc, "**PostToolUse**: fires after a file write, edit, or terminal command. The standard place to run a quality check.")
    bullet(doc, "**PreToolUse**: fires before a destructive action. Use it to block writes to Master/ or to Outputs/ unless approved.")
    bullet(doc, "**Stop**: fires when Claude finishes its turn. Use it to write a session summary to the audit log.")
    bullet(doc, "**Notification**: fires when Claude wants attention. Route to Slack or email so a long run finishing does not need you watching the terminal.")

    heading(doc, "Step-by-step: add a writing-style linter hook", 2)
    para(doc, "This is the same pattern the course itself uses: every time Claude saves a Markdown or Word file, a Python linter runs against it and blocks the session if banned phrases or em-dashes appear.")
    numbered(doc, "Create the settings folder if it does not exist:")
    code_block(doc, "mkdir -p .claude")
    numbered(doc, "Save the following to `.claude/settings.json`:")
    code_block(
        doc,
        '{\n'
        '  "hooks": {\n'
        '    "PostToolUse": [\n'
        '      {\n'
        '        "matcher": "Write|Edit|MultiEdit",\n'
        '        "hooks": [\n'
        '          {\n'
        '            "type": "command",\n'
        '            "command": "python scripts/check_style.py --hook"\n'
        '          }\n'
        '        ]\n'
        '      }\n'
        '    ]\n'
        '  }\n'
        '}'
    )
    numbered(doc, "Save the linter script at `scripts/check_style.py`. (The course ships one; reuse it.)")
    numbered(doc, "Restart Claude in this folder. From now on, every Write or Edit by Claude triggers the linter. If the linter exits 2, Claude reports the violations to you and waits.")
    numbered(doc, "Refine the rules in the linter as your team's standards evolve. The hook fires regardless of who is running Claude in the project.")

    # ---------------- 8. Headless mode and MCP ----------------
    heading(doc, "8. Headless mode and MCP servers", 1)

    heading(doc, "Headless mode (one-shot from the command line)", 2)
    para(doc, "For runs that do not need a conversation, fire Claude in headless mode. It runs the prompt, saves outputs, exits.")
    code_block(doc, "claude -p \"Run /variance-memo for April 2026\"")
    para(doc, "Use cases: scheduled cron jobs, CI pipelines, a Slack slash command that shells out, an Excel macro that ends with a Claude call.")

    heading(doc, "MCP servers (live ERP integration)", 2)
    para(doc, "MCP (Model Context Protocol) lets Claude call tools that reach into Oracle, SAP, or any other system. Lesson 06 covers procurement-specific MCP work in full. The terminal version configures MCP servers via a `.mcp.json` file at the project root or via the `/mcp` slash command.")
    code_block(
        doc,
        '{\n'
        '  "mcpServers": {\n'
        '    "oracle-fusion": {\n'
        '      "transport": "http",\n'
        '      "url": "https://mcp.u2xai.com/oracle/<tenant>",\n'
        '      "headers": {\n'
        '        "Authorization": "Bearer <token-from-IT>"\n'
        '      }\n'
        '    }\n'
        '  }\n'
        '}'
    )
    para(doc, "Once configured, ask Claude \"list the Oracle MCP tools\" to confirm the connection.")

    # ---------------- 9. A day in the life ----------------
    heading(doc, "9. A day in the life: Claude Code (terminal) in a real procurement workday", 1)
    para(
        doc,
        "This section follows Marcus, Procurement Operations Lead at a "
        "manufacturing company in the Midlands. Marcus has the install "
        "and folder layout from sections 4 and 5 already in place. He "
        "uses the terminal version because his Oracle data lives behind "
        "a corporate jumpbox and he reaches it over SSH.",
    )

    heading(doc, "07:00. Reviewing the overnight headless run", 2)
    para(
        doc,
        "Last night at 02:00, a cron job on the jumpbox fired "
        "`claude -p \"/nightly-anomaly-scan\"`. Marcus opens his laptop, "
        "SSHes into the jumpbox, and reads the saved scrollback from "
        "/var/log/procurement/nightly-2026-04-25.log. There are seven "
        "PO anomalies above the 50,000 GBP threshold. He picks the two "
        "largest for follow-up.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/                (on the jumpbox)\n"
        "├── .claude/\n"
        "│   └── commands/\n"
        "│       └── nightly-anomaly-scan.md\n"
        "├── Master/\n"
        "│   └── oracle_exports/po_anomalies_latest.csv\n"
        "└── Outputs/\n"
        "    └── nightly_briefs/\n"
        "        └── 2026-04-25.md\n"
        "/var/log/procurement/\n"
        "└── nightly-2026-04-25.log    (full scrollback for audit)"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Cron called `claude -p \"/nightly-anomaly-scan\"` at 02:00.")
    numbered(doc, "Claude loaded the project's CLAUDE.md, read the slash command body, and executed it.")
    numbered(doc, "Read `Master/oracle_exports/po_anomalies_latest.csv` (refreshed at 01:45 by another job).")
    numbered(doc, "Filtered for POs above the 50,000 GBP threshold and unusual against the seven-day rolling baseline.")
    numbered(doc, "Wrote the brief to `Outputs/nightly_briefs/2026-04-25.md`.")
    numbered(doc, "Sent a one-line Slack notification via the configured Notification hook.")
    numbered(doc, "Exited cleanly. The full scrollback was redirected to the cron log file for audit.")

    heading(doc, "09:30. Bulk contract review using a custom slash command", 2)
    para(
        doc,
        "Legal sent twelve supplier MSAs that need procurement's review "
        "before the quarterly executive signature batch. Marcus drops "
        "the PDFs into `Master/contracts_april/`. He opens a terminal in "
        "the project folder and runs a saved command:",
    )
    code_block(doc, "claude\n/contract-deviation contracts_april/")
    para(
        doc,
        "Claude reads each contract, compares against the standard MSA "
        "in `standards/our_standard_msa.docx`, flags every deviation, and "
        "writes one summary file per contract to `Drafts/contract_reviews/`. "
        "Total elapsed time: 12 minutes for twelve contracts.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/commands/\n"
        "│   └── contract-deviation.md\n"
        "├── Master/\n"
        "│   └── contracts_april/   (12 supplier MSAs)\n"
        "├── standards/\n"
        "│   └── our_standard_msa.docx\n"
        "└── Drafts/\n"
        "    └── contract_reviews/\n"
        "        └── (12 review files, one per contract)"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Loaded CLAUDE.md and the saved contract-deviation slash command.")
    numbered(doc, "Listed every PDF in `Master/contracts_april/`. Counted twelve.")
    numbered(doc, "Read `standards/our_standard_msa.docx` once and held the baseline clauses in working memory.")
    numbered(doc, "For each PDF in turn, parsed the text, walked clause by clause, compared against the baseline.")
    numbered(doc, "Wrote one Markdown summary per contract to `Drafts/contract_reviews/<supplier>-review.md`.")
    numbered(doc, "Where a clause was missing or unreadable, recorded \"not present\" or \"OCR uncertain\" rather than guessing.")
    numbered(doc, "Did not modify Master/ or standards/. The PostToolUse hook ran the linter on every saved file; all twelve passed.")

    heading(doc, "11:00. Headless one-shot from a Slack command", 2)
    para(
        doc,
        "Marcus's CFO Slacks: \"Quick supplier risk read on Globex, "
        "please. We have a meeting in 45 minutes.\" Marcus does not "
        "open the terminal; instead he uses a Slack workflow that fires:",
    )
    code_block(doc, "claude -p \"/risk-brief Globex SA\"")
    para(
        doc,
        "Forty seconds later the Slack workflow posts back a one-page "
        "risk brief written to `Outputs/risk_briefs/globex-2026-04-25.md` "
        "and a summary in the Slack thread. Marcus reads it, makes one "
        "edit, and forwards to the CFO with two minutes to spare.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/commands/\n"
        "│   └── risk-brief.md\n"
        "├── data/\n"
        "│   └── supplier_master.csv\n"
        "└── Outputs/\n"
        "    └── risk_briefs/\n"
        "        └── globex-2026-04-25.md"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "The Slack workflow shelled out to `claude -p \"/risk-brief Globex SA\"`.")
    numbered(doc, "Claude loaded CLAUDE.md, read the risk-brief slash command, and substituted \"Globex SA\" into the prompt body.")
    numbered(doc, "Looked up Globex SA in `data/supplier_master.csv` for spend, contract value, and primary contact.")
    numbered(doc, "Pulled the most recent news on Globex via the connected web-search tool.")
    numbered(doc, "Drafted a one-page risk brief in CFO voice: lead with the headline, three risk points, three recommended actions.")
    numbered(doc, "Saved to `Outputs/risk_briefs/globex-2026-04-25.md`.")
    numbered(doc, "Returned a JSON summary which the Slack workflow rendered as a thread reply.")

    heading(doc, "14:00. Audit trail capture for a CFO-bound output", 2)
    para(
        doc,
        "Marcus has just produced a savings case worth 1.42m GBP for the "
        "consolidation initiative. The CFO will want to know exactly "
        "what data went into the analysis. Inside the same Claude "
        "session he runs:",
    )
    code_block(doc, "/audit-trail")
    para(
        doc,
        "Claude saves the entire session scrollback (every prompt he "
        "typed, every file Claude opened, every output Claude produced) "
        "to `Outputs/audit/2026-04-25_logistics_savings.txt`. Marcus "
        "attaches the audit file to the savings case before forwarding.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/commands/\n"
        "│   └── audit-trail.md\n"
        "└── Outputs/\n"
        "    ├── savings_cases/\n"
        "    │   └── logistics_consolidation_2026-04-25.md\n"
        "    └── audit/\n"
        "        └── 2026-04-25_logistics_savings.txt"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Read the saved /audit-trail slash command body.")
    numbered(doc, "Captured the session transcript: every user prompt, every Claude response, every file read, every file write.")
    numbered(doc, "Stamped the file with the date, the model used, and the CLAUDE.md version active for the session.")
    numbered(doc, "Saved to `Outputs/audit/`. The PostToolUse hook ran on the audit file too, confirming clean output.")
    numbered(doc, "Did not redact anything. The savings case has one source of truth, end to end, in plain text.")

    heading(doc, "16:30. Adding a new hook to enforce a fresh rule", 2)
    para(
        doc,
        "In a meeting today the CPO asked that every output naming a "
        "supplier must also include the supplier's number from the "
        "Oracle supplier master. Marcus does not want to remember; he "
        "wants the rule enforced. He opens `.claude/settings.json` and "
        "adds a second PostToolUse hook that runs a small validation "
        "script.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/\n"
        "│   └── settings.json    (edited: second hook added)\n"
        "└── scripts/\n"
        "    ├── check_style.py             (existing linter)\n"
        "    └── check_supplier_numbers.py  (newly added)"
    )
    para(doc, "**The hook command added to settings.json:**")
    code_block(doc, "python scripts/check_supplier_numbers.py --hook")
    para(
        doc,
        "From the next session onwards, any output that names a supplier "
        "without the Oracle number is flagged on save and Marcus or his "
        "team must fix it before the file ships. The rule does not depend "
        "on memory.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Marcus added a second hook entry to the PostToolUse array in .claude/settings.json.")
    numbered(doc, "On the next Write or Edit by Claude in this project, Claude Code Desktop runs both hooks in order: the writing-style linter, then the supplier-number validator.")
    numbered(doc, "If either exits non-zero, the violation is reported and Claude waits for the fix before continuing.")
    numbered(doc, "The settings.json file is committed to Git, so every team member on the project gets the same hook automatically.")

    # ---------------- 10. Use cases ----------------
    heading(doc, "10. Complete use case walkthroughs", 1)

    heading(doc, "Use Case 1: Bulk NDA review across 24 supplier contracts", 2)
    para(doc, "When to use this: legal sends a quarterly batch of NDAs and you need a procurement review against your standard before they go to signature.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/commands/nda-review.md\n"
        "├── Master/\n"
        "│   └── nda_batch_april/   (24 supplier NDAs as PDF)\n"
        "├── standards/\n"
        "│   └── our_standard_nda.docx\n"
        "└── Drafts/\n"
        "    └── NDA_Summary.xlsx"
    )
    para(doc, "**The prompt to type (or save as a slash command):**")
    code_block(
        doc,
        "Master/ is read-only. Save all output to Drafts/.\n"
        "For every PDF in Master/nda_batch_april/, extract:\n"
        "  - supplier name,\n"
        "  - NDA effective date,\n"
        "  - term in months,\n"
        "  - governing law,\n"
        "  - mutual or one-way,\n"
        "  - presence of arbitration clause.\n"
        "Compare each NDA against standards/our_standard_nda.docx.\n"
        "Save the result as Drafts/NDA_Summary.xlsx with one row per file.\n"
        "Flag any NDA where: term > 36 months, governing law is not\n"
        '"England and Wales", or arbitration is missing where required.\n'
        "Cross-check three rows manually before sending."
    )
    para(doc, "**What you should see.** A 24-row Excel in Drafts/. The terminal scrollback shows every clause Claude considered for each NDA, ready to save as the audit log.")
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Listed every file in Master/nda_batch_april/. Counted 24.")
    numbered(doc, "Loaded standards/our_standard_nda.docx as the comparison baseline.")
    numbered(doc, "For each PDF, parsed the text, OCR'd any scans.")
    numbered(doc, "Searched each NDA for the six known fields by language pattern (e.g., 'governed by the laws of', 'shall remain in effect for', 'arbitration').")
    numbered(doc, "Wrote one row per NDA into Drafts/NDA_Summary.xlsx with the six fields and the flag column.")
    numbered(doc, "Where a field could not be found, left the cell blank and added 'not detected' to the flag column rather than guessing.")
    numbered(doc, "PostToolUse hook ran the linter on the saved Excel, confirmed clean.")

    heading(doc, "Use Case 2: Build a supplier onboarding pack from templates", 2)
    para(doc, "When to use this: a new supplier passes due diligence. Procurement Operations needs to send the NDA, code of conduct, bank details form, and tax form, all pre-filled with the supplier's details, as a single PDF pack.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/commands/onboarding-pack.md\n"
        "├── Master/\n"
        "│   ├── NDA_Template.docx\n"
        "│   ├── Code_of_Conduct.docx\n"
        "│   ├── Bank_Details_Form.docx\n"
        "│   └── W8_W9_Form.pdf\n"
        "├── data/\n"
        "│   └── globex_profile.txt\n"
        "└── Drafts/\n"
        "    └── Onboarding_Pack_Globex.pdf"
    )
    para(doc, "**The prompt to type:**")
    code_block(
        doc,
        "Master/ is read-only.\n"
        "Read data/globex_profile.txt for supplier details (legal name,\n"
        "address, primary contact, signing authority).\n"
        "Use the four files in Master/ as templates.\n"
        "Substitute placeholders {SupplierName}, {Address}, {ContactName},\n"
        "{Date} using the profile. Today is 2026-04-25.\n"
        "Combine the four filled documents into one PDF:\n"
        "Drafts/Onboarding_Pack_Globex.pdf in this order: NDA, Code of\n"
        "Conduct, Bank Details, W-8/W-9.\n"
        "Leave Master/ untouched."
    )
    para(doc, "**What you should see.** One PDF in Drafts/, four sub-documents filled, ready to email to the supplier.")
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Read data/globex_profile.txt and parsed it into key-value pairs.")
    numbered(doc, "Opened each Master/ template in turn and scanned for placeholder tokens.")
    numbered(doc, "Substituted each placeholder with the matching profile value, or today's date for {Date}.")
    numbered(doc, "Saved each filled document into Drafts/ as an interim file (so Legal can review the four individually if asked).")
    numbered(doc, "Combined them into one PDF in the requested order using the standard merge tool.")
    numbered(doc, "Saved the combined pack to Drafts/Onboarding_Pack_Globex.pdf. Master/ untouched.")

    heading(doc, "Use Case 3: Spend variance analysis from an Oracle CSV export", 2)
    para(doc, "When to use this: monthly variance memo for the CFO. Replaces 4 hours of manual Oracle work with a 12-minute Claude run.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/commands/variance-memo.md\n"
        "├── Master/\n"
        "│   └── oracle_exports/\n"
        "│       ├── purchasing_apr.csv\n"
        "│       └── apr_budget.xlsx\n"
        "└── Drafts/\n"
        "    └── variance_memo_apr.md"
    )
    para(doc, "**The prompt (saved as `.claude/commands/variance-memo.md`):**")
    code_block(
        doc,
        "Read Master/oracle_exports/purchasing_apr.csv (Oracle Purchasing\n"
        "export). Read Master/oracle_exports/apr_budget.xlsx (the approved\n"
        "April budget).\n"
        "Build a CFO-style variance narrative.\n"
        "- Headline: April actual vs budget, total and percentage.\n"
        "- Top three commodities by absolute over-budget variance, with figures.\n"
        "- Top three suppliers responsible for the over-budget commodities.\n"
        "- Three recommended management actions, each tied to a specific overrun.\n"
        "Cap the narrative at 600 words.\n"
        "Save to Drafts/variance_memo_apr.md.\n"
        "Master/ is read-only."
    )
    para(doc, "**What you should see.** A 580-word memo with named commodities, named suppliers, and concrete GBP figures. No vague phrases.")
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Read both source files and detected the column headers.")
    numbered(doc, "Joined the actuals against the budget on commodity_code.")
    numbered(doc, "Computed the variance per commodity and ranked by absolute over-budget.")
    numbered(doc, "Picked the top three over-budget commodities, then traced each back to the suppliers driving the overrun.")
    numbered(doc, "Wrote the narrative in CFO voice: headline, three worst commodities, three actions.")
    numbered(doc, "Held the output to 580 words because the prompt capped at 600.")
    numbered(doc, "Did not modify the source files. The PostToolUse hook ran the linter and confirmed the memo passed.")

    heading(doc, "Use Case 4: Headless CI run for a monthly variance memo", 2)
    para(doc, "When to use this: you want the variance memo to fire on the first business day of every month, with the output emailed to leadership, with no manual click. The CSV is refreshed nightly by a separate job.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/\n"
        "│   ├── commands/variance-memo.md\n"
        "│   └── settings.json   (PostToolUse linter hook)\n"
        "├── Master/oracle_exports/\n"
        "│   └── purchasing_<month>.csv  (refreshed nightly)\n"
        "├── scripts/\n"
        "│   └── monthly_runner.sh\n"
        "└── Outputs/\n"
        "    └── variance_memos/\n"
        "        └── 2026-04.md"
    )
    para(doc, "**The shell script saved at `scripts/monthly_runner.sh`:**")
    code_block(
        doc,
        '#!/usr/bin/env bash\n'
        'set -euo pipefail\n'
        'cd "$(dirname "$0")/.."\n'
        'MONTH=$(date -d "yesterday" +%Y-%m)\n'
        'OUT=Outputs/variance_memos/${MONTH}.md\n'
        'claude -p "/variance-memo for ${MONTH}, save to ${OUT}" \\\n'
        '       --permission-mode auto-accept-edits\n'
        'mail -s "Variance memo ${MONTH}" leadership@acme.com < "${OUT}"\n'
    )
    para(doc, "**What you should see.** On the first business day of each month, an email lands with the memo attached. The output file is saved to Outputs/variance_memos/. The terminal log is captured by cron for audit.")
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Cron triggered the shell script at 06:00 on the first business day.")
    numbered(doc, "The script set the working directory to the project folder, computed the month string, and called `claude -p` in headless mode.")
    numbered(doc, "Claude loaded the project's CLAUDE.md and the variance-memo slash command.")
    numbered(doc, "Read the latest Master/oracle_exports/purchasing_<month>.csv (refreshed by the nightly job).")
    numbered(doc, "Built the memo following the slash command body and saved to the named output path.")
    numbered(doc, "Exited cleanly with status 0. The shell script then mailed the file to leadership.")
    numbered(doc, "The full transcript was redirected by cron to /var/log/procurement/variance-<month>.log for audit.")

    heading(doc, "Use Case 5: Live PO anomaly detection via Oracle MCP", 2)
    para(doc, "When to use this: real-time intra-day monitoring. CSV exports are stale by lunchtime; MCP queries the live Oracle tenant whenever Claude needs to.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Analytics/\n"
        "├── .claude/commands/po-anomaly-now.md\n"
        "├── .mcp.json                  (Oracle MCP server config)\n"
        "└── Outputs/\n"
        "    └── live_alerts/\n"
        "        └── 2026-04-25_1432.md"
    )
    para(doc, "**The prompt (saved as a slash command):**")
    code_block(
        doc,
        "Use the Oracle MCP tools to find every open PO over 500,000 GBP\n"
        "that has been 'Pending Receipt' for more than 30 days as of right now.\n"
        "For each one, also pull the supplier's last three on-time delivery\n"
        "percentages from the Supplier Performance module.\n"
        "Output: a table with PO number, supplier, value, days pending,\n"
        "last three OTD percentages, and a one-line risk note.\n"
        "Cap at 20 rows.\n"
        "Save to Outputs/live_alerts/<date>_<time>.md."
    )
    para(doc, "**What you should see.** Within 30 seconds, a table of up to 20 rows reflecting Oracle right now. Useful for the 14:00 risk meeting.")
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Loaded .mcp.json and discovered the Oracle MCP tools.")
    numbered(doc, "Called oracle.purchasing.query with filters: status = 'Pending Receipt', value > 500000, age > 30 days.")
    numbered(doc, "For each returned PO, called oracle.suppliers.performance to get the last three OTD percentages.")
    numbered(doc, "Joined the two result sets and wrote a one-line risk note per row based on the OTD trend.")
    numbered(doc, "Capped output at 20 rows because the prompt asked for it.")
    numbered(doc, "Saved to Outputs/live_alerts/ with a date-and-time stamp in the filename.")
    numbered(doc, "Wrote nothing to Oracle. The MCP credentials are read-only.")

    # ---------------- 11. First week ----------------
    heading(doc, "11. Your first week with Claude Code in the terminal", 1)

    heading(doc, "Day 1 (Monday): install and first contact", 2)
    bullet(doc, "Goals: Node.js installed, Claude Code installed, signed in, first session opened and closed cleanly.")
    bullet(doc, "Tasks: complete section 4 of this guide. Open `claude` in your home folder. Type a one-line question. Quit with /quit.")
    bullet(doc, "Time budget: 30 minutes.")

    heading(doc, "Day 2 (Tuesday): first real procurement task in Plan mode", 2)
    bullet(doc, "Goals: project folder built, CLAUDE.md saved, first analysis run end to end in Plan mode then Ask permissions.")
    bullet(doc, "Tasks: build `Procurement_Analytics/` with Master/, Drafts/, Outputs/. Save a real KPI export to Master/. Run the supplier scorecard from section 10, Use Case 1.")
    bullet(doc, "Time budget: 60 minutes.")

    heading(doc, "Day 3 (Wednesday): your first slash command", 2)
    bullet(doc, "Goals: a custom slash command saved at .claude/commands/, invocable across sessions.")
    bullet(doc, "Tasks: take the prompt that worked yesterday. Save it as `.claude/commands/scorecard.md`. Run it with /scorecard. Confirm it produces the same output.")
    bullet(doc, "Time budget: 30 minutes.")

    heading(doc, "Day 4 (Thursday): your first hook", 2)
    bullet(doc, "Goals: a PostToolUse hook that runs a writing-style linter on every file Claude saves.")
    bullet(doc, "Tasks: copy the course's `scripts/check_style.py` into your project. Save the .claude/settings.json from section 7. Restart Claude. Trigger a save and confirm the hook fires.")
    bullet(doc, "Time budget: 45 minutes.")

    heading(doc, "Day 5 (Friday): your first headless run", 2)
    bullet(doc, "Goals: a one-shot run from outside Claude. Saved to disk. Captured in a log.")
    bullet(doc, "Tasks: open a terminal in the project folder. Run `claude -p \"/scorecard\"`. Redirect output to a log file. Verify the output is saved correctly. If you have admin access on a server, schedule the same command in cron.")
    bullet(doc, "Time budget: 45 minutes.")

    para(doc, "End-of-week reflection: keep a `Prompts_That_Worked.md` file at your project root. Every prompt that earns its keep, paste it in with the result. After two weeks you will have a personal slash-command library worth more than any course.")

    # ---------------- 12. 20-Minute Sprint ----------------
    heading(doc, "12. The 20-minute procurement onboarding sprint", 1)
    para(
        doc,
        "Use this when you have already installed Claude Code (Day 1 in "
        "section 11) and you want a first real win in twenty minutes flat.",
    )

    heading(doc, "Minutes 0 to 5: the project folder", 2)
    numbered(doc, "Open a terminal.")
    numbered(doc, "Create the project folder and standard subfolders.")
    code_block(
        doc,
        "mkdir -p ~/Documents/Procurement/Sprint_Test/{Master,Drafts,Outputs,Reference,Archive}\n"
        "cd ~/Documents/Procurement/Sprint_Test"
    )
    numbered(doc, "Drop one real file into Master/. Anything you would actually analyse: a recent PO export, a contract PDF, a KPI CSV.")

    heading(doc, "Minutes 5 to 10: the CLAUDE.md", 2)
    numbered(doc, "Save a CLAUDE.md at the project root using the template in section 4, Part E.")
    numbered(doc, "Replace every value in angle brackets with your actual role, your category, and your standards.")
    numbered(doc, "Keep it under 50 lines for the first pass; you can refine later.")

    heading(doc, "Minutes 10 to 13: open Claude in Plan mode", 2)
    numbered(doc, "Start Claude:")
    code_block(doc, "claude --permission-mode plan")
    numbered(doc, "Verify the prompt shows \"Plan mode\" and \"CLAUDE.md loaded\".")

    heading(doc, "Minutes 13 to 18: the first real task", 2)
    numbered(doc, "Type a real procurement prompt naming the file you saved to Master/. Example for a KPI export:")
    code_block(
        doc,
        "Read Master/<your-file>.csv. Tell me what columns you found and\n"
        "what kinds of analysis would be useful for a procurement team.\n"
        "Cap at 5 suggestions. Do not modify Master/."
    )
    numbered(doc, "Read the plan Claude prints. If it looks right, switch to Ask permissions and approve. If not, refine the prompt and re-run.")

    heading(doc, "Minutes 18 to 20: review and save what worked", 2)
    numbered(doc, "Read the output. If useful, copy the prompt into a new file at .claude/commands/.")
    numbered(doc, "Save the session scrollback for your records. (On Mac: Cmd+S in Terminal. On Windows PowerShell: Ctrl+M to mark, Enter to copy, paste into a file.)")
    numbered(doc, "Quit cleanly with /quit. The first usable output is in Drafts/. The reusable prompt is in .claude/commands/.")

    # ---------------- 13. Team deployment ----------------
    heading(doc, "13. Deploying Claude Code in the terminal across a team", 1)
    para(
        doc,
        "The terminal version makes team deployment straightforward "
        "because every standard the team agrees on is a file in the "
        "project. Commit the project folder to Git and every analyst "
        "starts from the same baseline on day one.",
    )

    heading(doc, "What to commit to Git", 2)
    bullet(doc, "**CLAUDE.md** at the project root. The team's standing instructions, scoring weights, RAG bands, and writing rules.")
    bullet(doc, "**.claude/settings.json**. The team's hooks. Linter, supplier-number validator, audit-log writer.")
    bullet(doc, "**.claude/commands/*.md**. The team's slash commands. /variance-memo, /risk-brief, /onboarding-pack, /audit-trail.")
    bullet(doc, "**.mcp.json**. The team's MCP server connections (without secrets; pass tokens via environment variables).")
    bullet(doc, "**scripts/**. The hook scripts (linter, validators) and any shared headless runners.")
    bullet(doc, "**standards/**. Your standard MSA, NDA, RFP boilerplate, code of conduct.")

    heading(doc, "What NOT to commit to Git", 2)
    bullet(doc, "Real supplier data in Master/. Use a separate data store (SharePoint, OneDrive, or a database).")
    bullet(doc, "Drafts/ and Outputs/. These are per-analyst working files.")
    bullet(doc, "API tokens. Use environment variables or your secret manager.")
    bullet(doc, "Personal CLAUDE.md additions. The shared CLAUDE.md is for team rules; personal context goes in `~/.claude/CLAUDE.md` (the user-level file).")

    heading(doc, "Role-based first tasks", 2)
    fill_table(
        doc,
        ["Role", "First task", "Right slash command"],
        [
            ("Sourcing manager", "RFP refresh from a master template", "/rfp-refresh"),
            ("Category manager", "Quarterly scorecard pack", "/scorecard"),
            ("Contract manager", "Bulk NDA review against your standard", "/nda-review"),
            ("AP lead", "Reconcile a folder of invoice exceptions, draft chase emails", "/ap-reconcile"),
            ("Supplier risk manager", "On-demand risk brief from a Slack trigger", "/risk-brief"),
            ("Procurement analyst", "Monthly variance memo, headless from cron", "/variance-memo"),
            ("Procurement operations", "Supplier onboarding pack assembly", "/onboarding-pack"),
        ],
    )

    heading(doc, "Governance: three rules, no exceptions", 2)
    bullet(doc, "**Data classification before paste.** Public-OK, Internal-OK on Pro/Max, restricted goes only to the enterprise instance. Lesson 07 of the course covers this in full.")
    bullet(doc, "**Audit-ready outputs.** Every CFO- or board-bound file includes a footer with timestamp, source files, and Claude model used. The /audit-trail slash command produces it automatically.")
    bullet(doc, "**Three recommendations max** in any output that lands with a CFO or a board. Anything more, prune before sending.")

    # ---------------- 14. Quick reference and troubleshooting ----------------
    heading(doc, "14. Quick reference and troubleshooting", 1)

    heading(doc, "Built-in slash commands", 2)
    fill_table(
        doc,
        ["Command", "What it does"],
        [
            ("/help", "Lists the built-in commands and any custom slash commands the project has."),
            ("/quit", "Exits the session cleanly. The scrollback stays in your terminal until you close the window."),
            ("/memory", "Reloads CLAUDE.md without restarting the session. Useful after editing CLAUDE.md mid-session."),
            ("/permission", "Switches the permission mode (Plan, Ask, Auto-accept, Auto, Bypass)."),
            ("/mcp", "Lists or configures connected MCP servers."),
            ("/clear", "Clears the visible session history. Does NOT clear the scrollback or saved files."),
            ("/audit-trail", "Custom command. Saves the session transcript to Outputs/audit/ with a timestamp."),
        ],
    )

    heading(doc, "Common terminal errors and how to fix them", 2)
    bullet(doc, "**Symptom:** `command not found: claude`. **Fix:** restart your terminal so it picks up npm's global bin folder. If that fails, run `npm config get prefix` and add `/bin` to your PATH.")
    bullet(doc, "**Symptom:** `EACCES: permission denied` during npm install. **Fix:** use a Node.js installer that does not require sudo (the LTS installer from nodejs.org), or change npm's global folder to a user-owned path.")
    bullet(doc, "**Symptom:** Claude says \"CLAUDE.md not loaded\". **Fix:** check the file is at the project root (the folder you ran `claude` in), spelt exactly `CLAUDE.md` (case-sensitive on Linux and Mac).")
    bullet(doc, "**Symptom:** Hook reports a violation but the file looks fine. **Fix:** the hook output is in stderr. Read the full message; it names the rule that fired and the line number.")
    bullet(doc, "**Symptom:** `claude -p` runs but produces no output file. **Fix:** in headless mode, prompts must explicitly say where to save. \"Save to Outputs/...\" not \"save the result\".")
    bullet(doc, "**Symptom:** SSH session times out during a long Claude run. **Fix:** wrap the run in `tmux` or `screen` so it survives disconnect. Re-attach when you reconnect.")
    bullet(doc, "**Symptom:** MCP tool call returns 401. **Fix:** the access token in .mcp.json is wrong or expired. Update the token. If the token is via env var, check the var is exported in the shell that runs Claude.")
    bullet(doc, "**Symptom:** Slash command not found, but the .md file exists. **Fix:** restart Claude or run /memory. Slash commands are loaded at session start.")

    heading(doc, "Essential resources", 2)
    bullet(doc, "**Official docs.** docs.claude.com (look for \"Claude Code\").")
    bullet(doc, "**Community.** Anthropic Discord, the #claude-code channel.")
    bullet(doc, "**Course CLAUDE.md.** The writing rules and procurement-specific anti-AI rules referenced throughout this guide. Live in the project root.")
    bullet(doc, "**Course lessons 01 to 07.** Permission modes, token efficiency, Routines, parallel sessions, voice input, Oracle integration, team deployment.")

    doc.save(str(OUTPUT_PATH))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
