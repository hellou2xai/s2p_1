"""Build the Course 4: The Command Engineer companion handout (.docx).

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

OUTPUT_PATH = _PROJECT_ROOT / "Handouts" / "Course_04_The_Command_Engineer_Handout.docx"


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
    para(doc, "Series 2 (Engineering Track) | Course 4", italic=True)
    doc.add_heading("The Command Engineer", level=0)
    para(
        doc,
        "Repeatable slash commands for monthly procurement reporting, "
        "built once and reused every cycle.",
        italic=True,
        size=14,
    )
    para(
        doc,
        "Four hours. Six lessons. No coding. Real spend data with 50 "
        "suppliers, 2,508 transactions, 45 contracts, and 200 quarterly "
        "scorecard records.",
        italic=True,
    )
    para(
        doc,
        "Use this handout alongside the course folder at "
        "Detailed Course Content/Course_04_The_Command_Engineer/.",
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
        "folder has the data, the starter files, the six lessons, and "
        "the reference answers. You do not need anything else.",
    )
    para(doc, "How to read this guide:")
    numbered(
        doc,
        "Read sections 2 and 3 to understand what the course is and "
        "what you end up with.",
    )
    numbered(
        doc,
        "Read section 4 to see what the course saves you per "
        "reporting cycle.",
    )
    numbered(
        doc,
        "Read section 5 for the mental model of what a slash command "
        "is and how it differs from a prompt or a skill.",
    )
    numbered(doc, "Open the course folder and start Lesson 1.")
    numbered(
        doc,
        "Come back to this handout when you want context (sections "
        "6 to 9 are useful while you work through the lessons).",
    )
    numbered(
        doc,
        "Use section 11 (troubleshooting) if something does not "
        "look right.",
    )
    para(
        doc,
        "The handout does not replace the lessons. It gives you the "
        "bigger picture so you know why each lesson matters before "
        "you start it. It also serves as a quick reference after you "
        "finish the course. When you need to remember how $ARGUMENTS "
        "works or how to troubleshoot a missing command, come back here "
        "instead of re-reading the full lesson.",
    )

    # ===================================================================
    # 2. What this course teaches
    # ===================================================================
    heading(doc, "2. What this course teaches", 1)

    heading(doc, "A first Monday you have lived before", 2)
    para(
        doc,
        "It is 08:30 on the first Monday of the month. Your CPO "
        "messages you: \"Need the monthly spend breakdown by category, "
        "the anomaly report, and the contract expiry list. Same as "
        "last month. By noon.\"",
    )
    para(
        doc,
        "You open Claude Code (in the terminal). You type a long "
        "prompt from memory. You get the spend breakdown, but the "
        "format is different from last month because you worded the "
        "prompt differently. The anomaly report misses the threshold "
        "you used in March because you forgot to mention it. The "
        "contract expiry list uses 60 days instead of 90 because you "
        "copied last month's prompt and changed the wrong number.",
    )
    para(
        doc,
        "Your colleague Priya runs the same analysis for her "
        "categories. Her output looks nothing like yours. Same data, "
        "same intent, different prompts, different results. Your CPO "
        "sees two reports that should match in shape but do not. She "
        "asks you to reconcile them. That takes another 30 minutes.",
    )
    para(
        doc,
        "This happens every month. The prompts are in chat history, "
        "so you scroll back, copy, paste, edit, and hope you caught "
        "every change. Some months you do. Some months you do not.",
    )

    heading(doc, "The fix: a command library", 2)
    para(
        doc,
        "This course fixes that. Instead of typing a different prompt "
        "every month, you build a **command library**: six slash "
        "commands stored in .claude/commands/ that produce standardized "
        "output every time. You type /spend-analyze Q1 "
        "direct-materials, and you get the same shape of report "
        "whether you run it in April or October. Priya types the "
        "same command for her categories and gets the same shape for "
        "hers. No free-text prompts. No variation. One command, one "
        "output shape, every time.",
    )
    para(
        doc,
        "The six commands you will build are: /spend-analyze (monthly "
        "spend breakdown by category and period), /anomaly-detect "
        "(flag transactions above a configurable threshold and "
        "duplicate PO numbers), /scorecard-refresh (supplier trend "
        "summary for quarterly reviews), /contract-sweep (expiring "
        "contracts within a configurable horizon), /rfp-launch "
        "(sourcing brief combining spend and contract data), and "
        "/savings-update (actual-versus-target variance by supplier).",
    )

    heading(doc, "See it in Claude Code (in the terminal)", 2)
    para(doc, "**The prompt you type.**")
    code_block(
        doc,
        "/spend-analyze Q1 direct-materials",
    )
    para(doc, "**The folder layout.**")
    code_block(
        doc,
        "practice/\n"
        "+-  .claude/commands/spend-analyze.md\n"
        "+-  data/spend-transactions.csv\n"
        "+-  data/supplier-master.csv\n"
        "+-  outputs/",
    )
    para(
        doc,
        "**What you should see.** Claude Code (in the terminal) reads "
        "spend-transactions.csv, filters to Q1 2026 and the "
        "direct-materials category, and saves a datestamped spend "
        "analysis to outputs/spend_analysis_Q1_direct-materials_2026-04-25.md. "
        "The report opens with a headline naming the period, category, "
        "total spend, and supplier count. Below is a ranked table.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Claude Code found .claude/commands/spend-analyze.md and "
        "replaced $ARGUMENTS with \"Q1 direct-materials\".",
    )
    numbered(
        doc,
        "The command file told Claude Code to parse the first argument "
        "as the period (Q1) and the second as the category "
        "(direct-materials).",
    )
    numbered(
        doc,
        "Claude Code opened data/spend-transactions.csv (2,508 rows), "
        "filtered to rows where the date fell in Q1 2026 (January "
        "through March) and the category column equaled "
        "direct-materials.",
    )
    numbered(
        doc,
        "It grouped spending by supplier, summed the amount_usd "
        "column, and ranked suppliers by total spend.",
    )
    numbered(
        doc,
        "It compared Q1 totals to Q4 2025 totals and computed the "
        "period-over-period change for each supplier.",
    )
    numbered(
        doc,
        "It saved the output to outputs/ with a datestamp in the "
        "file name and added an audit footer listing the source "
        "files, the date, and the model.",
    )

    # ===================================================================
    # 3. What is in the course folder
    # ===================================================================
    heading(doc, "3. What is in the course folder", 1)
    para(
        doc,
        "Open the course folder before you start. Everything you "
        "need is inside. No external downloads, no separate data "
        "store. The structure is flat (no nesting deeper than three "
        "levels) so you can find any file in seconds.",
    )
    code_block(
        doc,
        "Course_04_The_Command_Engineer/\n"
        "+-  README.md\n"
        "+-  COURSE_OVERVIEW.md\n"
        "+-  lessons/\n"
        "+-  practice/\n"
        "|   +-  CLAUDE.md\n"
        "|   +-  data/\n"
        "|   |   +-  spend-transactions.csv\n"
        "|   |   +-  supplier-master.csv\n"
        "|   |   +-  contract-register.csv\n"
        "|   |   +-  scorecard-history.csv\n"
        "|   +-  .claude/commands/\n"
        "|   +-  outputs/\n"
        "+-  solutions/\n"
        "+-  scripts/build_course_data.py",
    )
    para(doc, "Today's date in the practice data is **2026-04-25**.")
    para(
        doc,
        "Below is what each folder and file does, with an explanation "
        "of why it matters.",
    )

    # README.md
    heading(doc, "README.md", 3)
    para(
        doc,
        "The starting point. It lists what is in the course, what you "
        "need before you start (Course 1 and Course 2 finished, Claude "
        "Code installed), and a step-by-step guide for how to work "
        "through the six lessons.",
    )
    para(
        doc,
        "**Why this matters.** If you skip the README, you may attempt "
        "Lesson 3 before finishing Lesson 1. The README gives the "
        "correct order and names the prerequisites.",
    )

    # COURSE_OVERVIEW.md
    heading(doc, "COURSE_OVERVIEW.md", 3)
    para(
        doc,
        "The scenario. It describes Meridian Manufacturing, the 48m "
        "USD annual spend, the 50 suppliers, the four categories "
        "(direct materials, logistics, indirect, and MRO), the six "
        "commands you will build, and the rubric for \"done\". "
        "Read this before Lesson 1 so you understand the story behind "
        "the exercises.",
    )
    para(
        doc,
        "**Why this matters.** The overview connects every exercise to "
        "a real procurement reporting cycle. Without it, the lessons "
        "feel like disconnected drills instead of steps toward a "
        "working command library.",
    )

    # lessons/
    heading(doc, "lessons/", 3)
    para(
        doc,
        "Six markdown files, one per lesson, numbered in order. Each "
        "lesson opens with a day-to-day scenario (\"It is 09:30 "
        "Tuesday. Your CPO Slacks...\"), then walks you through step "
        "by step: what to type in the terminal, what Claude Code does, "
        "what you should see on screen.",
    )
    para(
        doc,
        "**Why this matters.** The lessons are the core of the course. "
        "Every step has three lines: what to do, the exact command, "
        "and what you should see. You do not need to guess or infer "
        "anything. If a step can fail, the lesson includes a fix.",
    )

    # practice/CLAUDE.md
    heading(doc, "practice/CLAUDE.md", 3)
    para(
        doc,
        "The project context file Claude Code (in the terminal) reads "
        "automatically when you start a session in the practice folder. "
        "It tells Claude Code who you are (Procurement Operations Lead "
        "at Meridian Manufacturing), what the folder layout is, what "
        "the data files contain, and what writing rules to follow "
        "(American English, Oxford commas, active voice, specific "
        "numbers, USD for all currency).",
    )
    para(
        doc,
        "**Why this matters.** Without this file, Claude Code produces "
        "generic output. With it, every output uses Meridian's context, "
        "Meridian's rules, and Meridian's folder structure. You set "
        "this up once and it applies to every session automatically. "
        "When you copy the command library to your real project, you "
        "update the CLAUDE.md to reflect your company's context.",
    )

    # data/
    heading(doc, "practice/data/", 3)
    para(
        doc,
        "Four CSV files that drive every command. These are read-only. "
        "Claude Code reads them but does not modify them.",
    )
    bullet(
        doc,
        "**spend-transactions.csv** (2,508 rows). One row per "
        "transaction over the last 12 months. Columns: transaction_id, "
        "date, supplier_id, supplier_name, category, subcategory, "
        "description, amount_usd, po_number, cost_center, department, "
        "payment_terms, and invoice_status. Contains 15 planted "
        "high-value anomalies and 12 duplicate PO patterns for the "
        "anomaly detection exercises.",
    )
    bullet(
        doc,
        "**supplier-master.csv** (50 rows). One row per supplier. "
        "Columns: supplier_id, supplier_name, category, tier, "
        "contract_id, risk_rating, city, state, payment_terms, "
        "annual_target_usd, and status. Three suppliers (SUP004 "
        "Apex Electronics, SUP019, and SUP048) are flagged as "
        "at_risk.",
    )
    bullet(
        doc,
        "**contract-register.csv** (45 rows). One row per contract. "
        "Columns: contract_id, supplier_id, supplier_name, title, "
        "start_date, end_date, annual_value_usd, total_value_usd, "
        "auto_renew, notice_period_days, and status. Eight contracts "
        "expire within 90 days of 2026-04-25.",
    )
    bullet(
        doc,
        "**scorecard-history.csv** (200 rows). 50 suppliers across "
        "four quarters. Columns: supplier_id, supplier_name, quarter, "
        "quality_score, delivery_score, responsiveness_score, "
        "cost_score, innovation_score, and overall_score. SUP004, "
        "SUP019, and SUP048 show declining trends. SUP007 and SUP011 "
        "show improving trends.",
    )
    para(
        doc,
        "**Why this matters.** The data volumes are realistic. A "
        "5-row CSV does not feel like real procurement work. With "
        "2,508 transaction rows, you experience what Claude Code (in "
        "the terminal) does on real volumes: filtering, grouping, "
        "ranking, and computing variances across thousands of records "
        "in seconds. When you move to your own data, the commands "
        "work the same way on 5,000 or 50,000 rows.",
    )

    # .claude/commands/
    heading(doc, "practice/.claude/commands/", 3)
    para(
        doc,
        "**Starts empty.** This is the folder you fill across Lessons "
        "2 to 5. By the end of the course it holds six command files. "
        "Each file is a markdown document between 30 and 70 lines "
        "that Claude Code (in the terminal) reads when you type the "
        "corresponding slash command.",
    )
    para(
        doc,
        "**Why this matters.** This folder is the command library. "
        "Once populated, any team member who copies this folder into "
        "their project gets the same six commands. No training needed. "
        "No prompt engineering. Type the command, get the output.",
    )

    # outputs/
    heading(doc, "outputs/", 3)
    para(
        doc,
        "Where every command saves its result. File names are "
        "datestamped (for example, "
        "spend_analysis_Q1_direct-materials_2026-04-25.md). This "
        "folder starts with only a README.md placeholder.",
    )
    para(
        doc,
        "**Why this matters.** Datestamped file names prevent "
        "overwriting. When you run /spend-analyze in May and again in "
        "June, both files sit side by side in outputs/. You can "
        "compare months without losing prior work. Your CPO can "
        "open last month's report next to this month's and spot "
        "the differences in 30 seconds.",
    )

    # solutions/
    heading(doc, "solutions/", 3)
    para(
        doc,
        "Reference answers for each command. Six markdown files, one "
        "per command. The lessons tell you: \"Look here only after "
        "attempting the exercise yourself.\"",
    )
    para(
        doc,
        "**Why this matters.** If your command produces unexpected "
        "output, you can compare your command file to the reference "
        "answer line by line and spot the difference. The reference "
        "answers also show best practices for argument parsing and "
        "output formatting.",
    )

    # scripts/
    heading(doc, "scripts/", 3)
    para(
        doc,
        "Contains build_course_data.py, the Python script that "
        "generates all four CSV files deterministically (using "
        "random.seed(42)). If you delete or corrupt the data during "
        "practice, run this script to restore everything to its "
        "original state.",
    )
    para(
        doc,
        "**Why this matters.** Mistakes happen during practice. One "
        "command restores all data to its original state. No need to "
        "re-download anything or ask for a fresh copy.",
    )

    # ===================================================================
    # 4. What the course saves you
    # ===================================================================
    heading(doc, "4. What the course saves you", 1)
    para(
        doc,
        "The table below compares five recurring procurement tasks "
        "done with free-text prompts (typed from memory each time) "
        "and done with pre-built slash commands. Times are based on "
        "a 50-supplier portfolio with 2,500 monthly transactions. "
        "The \"without commands\" column includes the time to write "
        "the prompt, wait for output, check the format, and reformat "
        "if needed. The \"with commands\" column includes the time to "
        "type the command and review the output.",
    )
    fill_table(
        doc,
        ["Task", "Without commands", "With commands"],
        [
            [
                "Monthly spend breakdown by category",
                "25 min (write prompt, review format, reformat)",
                "3 min (type /spend-analyze Q1 direct-materials, review)",
            ],
            [
                "Anomaly detection across 2,500 transactions",
                "40 min (write prompt, set threshold, check duplicates)",
                "4 min (type /anomaly-detect 2.5 Q1, review alerts)",
            ],
            [
                "Supplier scorecard refresh for one supplier",
                "20 min (write prompt, pull history, format trend)",
                "3 min (type /scorecard-refresh SUP004 Q1, review)",
            ],
            [
                "Contract expiry sweep, 90-day horizon",
                "30 min (write prompt, check auto-renew, compile list)",
                "3 min (type /contract-sweep 90, review action list)",
            ],
            [
                "Sourcing event kickoff brief",
                "45 min (pull spend data, pull expiring contracts, draft)",
                "5 min (type /rfp-launch direct-materials 2026-07-31, review)",
            ],
        ],
    )
    para(
        doc,
        "Total for all five tasks: 160 minutes without commands, "
        "18 minutes with commands. That is 142 minutes saved per "
        "reporting cycle. Over 12 monthly cycles, that is 1,704 "
        "minutes, or about 28 hours, returned to higher-value work "
        "like supplier negotiations, strategy development, and "
        "stakeholder meetings.",
    )

    # ===================================================================
    # 5. What a slash command actually is
    # ===================================================================
    heading(doc, "5. What a slash command actually is", 1)

    heading(doc, "The mental model", 2)
    para(
        doc,
        "A custom slash command is a markdown file stored in "
        ".claude/commands/ inside your project folder. When you type "
        "/command-name in Claude Code (in the terminal), Claude Code "
        "finds .claude/commands/command-name.md, reads the "
        "instructions inside, and follows them. Everything after the "
        "command name becomes the value of $ARGUMENTS. So when you "
        "type /spend-analyze Q1 direct-materials, Claude Code replaces "
        "every $ARGUMENTS in the command file with \"Q1 "
        "direct-materials\".",
    )
    para(
        doc,
        "Think of it this way: a prompt is something you type once "
        "and it disappears when the session ends. A command is a "
        "prompt you type once, save as a file, and reuse by name "
        "forever. The arguments are the only thing that changes "
        "between runs.",
    )
    para(
        doc,
        "**Why this matters.** Free-text prompts introduce variation. "
        "You word them differently each time, so the output shape "
        "changes. Commands remove that variation. The instructions "
        "are fixed in the file. Only the arguments change. Two "
        "people running the same command with the same arguments "
        "on the same data get the same output.",
    )

    heading(doc, "How $ARGUMENTS works", 2)
    para(
        doc,
        "$ARGUMENTS is a placeholder in your command file. Claude "
        "Code (in the terminal) replaces it with whatever you type "
        "after the command name. Your command file is responsible "
        "for parsing that string into individual values.",
    )
    para(
        doc,
        "For example, if your command file says \"$ARGUMENTS "
        "contains two values separated by a space: the first is "
        "the period, the second is the category,\" and you type "
        "/spend-analyze Q1 direct-materials, then Claude Code knows "
        "to treat Q1 as the period and direct-materials as the "
        "category. The parsing instructions are plain English, not "
        "code.",
    )

    heading(doc, "The five sections of a command file", 2)
    para(
        doc,
        "Every well-structured command file has five sections. Not "
        "all are required, but the best commands use all five.",
    )
    numbered(
        doc,
        "**Argument parsing.** A short block that tells Claude Code "
        "how to split $ARGUMENTS into named variables (period, "
        "category, threshold, horizon, supplier, or deadline).",
    )
    numbered(
        doc,
        "**Data sources.** A list of the files to read, with column "
        "names and what each file is for.",
    )
    numbered(
        doc,
        "**Analysis steps.** A numbered list of what to compute: "
        "filter, group, sum, compare, rank, or flag.",
    )
    numbered(
        doc,
        "**Output format.** The exact shape of the output: section "
        "headings, table columns, summary paragraph, and audit "
        "footer.",
    )
    numbered(
        doc,
        "**Save location.** Where to save the file, with the "
        "datestamp and naming convention.",
    )

    heading(doc, "A real extract from spend-analyze.md", 2)
    para(
        doc,
        "Below is a shortened extract from the /spend-analyze command "
        "file. It shows how $ARGUMENTS works and how the five sections "
        "appear in practice.",
    )
    code_block(
        doc,
        "# /spend-analyze\n"
        "\n"
        "## Arguments\n"
        "$ARGUMENTS contains two values separated by a space:\n"
        "- First value: the period (Q1, Q2, Q3, Q4, or a month like 2026-01)\n"
        "- Second value: the category (direct-materials, logistics,\n"
        "  indirect, mro, or \"all\")\n"
        "\n"
        "## Data sources\n"
        "- data/spend-transactions.csv (transaction-level spend)\n"
        "- data/supplier-master.csv (supplier metadata and targets)\n"
        "\n"
        "## Steps\n"
        "1. Filter spend-transactions.csv to the requested period.\n"
        "2. If category is not \"all\", filter to that category.\n"
        "3. Group by supplier_id and supplier_name. Sum amount_usd.\n"
        "4. Rank suppliers by total spend, descending.\n"
        "5. Pull the same period from the prior year. Compute change.\n"
        "6. Join supplier-master.csv to add tier and risk_rating.\n"
        "\n"
        "## Output format\n"
        "- Headline: total spend, supplier count, period, category.\n"
        "- Table: Rank, Supplier, Category, Tier, Spend, Prior, Change %.\n"
        "- Summary: top 3 movers (biggest absolute change).\n"
        "- Audit footer: date, source files, model, operator.\n"
        "\n"
        "## Save\n"
        "Save to outputs/spend_analysis_[period]_[category]_[date].md",
    )
    para(
        doc,
        "**Why this matters.** The extract above is 25 lines of plain "
        "English. No code, no scripting language, no syntax to learn. "
        "If you can write a numbered list of steps, you can write a "
        "command file. The five-section structure keeps the file "
        "organized so Claude Code (in the terminal) follows every "
        "instruction in order.",
    )

    heading(doc, "Command vs. skill vs. prompt", 2)
    para(
        doc,
        "Course 3 taught you skills (SKILL.md files). Course 4 teaches "
        "you commands. Here is how they compare.",
    )
    fill_table(
        doc,
        ["", "Prompt", "SKILL.md (Course 3)", "Slash command (Course 4)"],
        [
            [
                "Where it lives",
                "In the chat (gone when the session ends)",
                "In skills/ (persists across sessions)",
                "In .claude/commands/ (persists, invoked by name)",
            ],
            [
                "How you run it",
                "Type the full prompt every time",
                "Type \"Use the skill in skills/name.md\"",
                "Type /command-name [arguments]",
            ],
            [
                "Parameters",
                "You write them into the prompt text",
                "No built-in parameter passing",
                "$ARGUMENTS passes period, category, threshold",
            ],
            [
                "Best for",
                "One-off questions",
                "Multi-step methodologies (RFPs, scorecards)",
                "Recurring reports with changing inputs",
            ],
            [
                "Reuse",
                "Copy-paste from chat history",
                "Re-run with a new prompt naming the skill",
                "Type one line; arguments change each run",
            ],
        ],
    )
    para(
        doc,
        "Skills and commands are complementary. A skill captures "
        "a methodology (how to score bids, how to write an RFP). "
        "A command captures a recurring report (monthly spend "
        "breakdown, quarterly scorecard refresh). Use skills for "
        "project-based work that happens once per sourcing event. "
        "Use commands for cycle-based work that repeats every month "
        "or quarter. In practice, many procurement teams use both: "
        "commands for the monthly reporting cadence, skills for the "
        "ad-hoc sourcing events that arise between cycles.",
    )

    # ===================================================================
    # 6. Worked examples
    # ===================================================================
    heading(doc, "6. Worked examples", 1)
    para(
        doc,
        "Below are two complete examples. Each follows the four-part "
        "pattern: the prompt you type, the folder layout, what you "
        "should see, and what Claude Code (in the terminal) did behind "
        "the scenes.",
    )

    # Example A
    heading(doc, "Example A: /spend-analyze Q1 direct-materials", 2)

    para(doc, "**The prompt you type in Claude Code (in the terminal).**")
    code_block(doc, "/spend-analyze Q1 direct-materials")

    para(doc, "**The folder layout.**")
    code_block(
        doc,
        "practice/\n"
        "+-  .claude/commands/spend-analyze.md\n"
        "+-  data/spend-transactions.csv    (2,508 rows)\n"
        "+-  data/supplier-master.csv       (50 rows)\n"
        "+-  outputs/                       (results land here)",
    )

    para(
        doc,
        "**What you should see.** Claude Code (in the terminal) "
        "produces a file named "
        "outputs/spend_analysis_Q1_direct-materials_2026-04-25.md. "
        "The file opens with a headline: \"Q1 2026 Spend Analysis: "
        "Direct Materials. Total spend: 4,812,340 USD across 12 "
        "suppliers.\" Below the headline is a ranked table of "
        "suppliers by spend, with columns for Rank, Supplier, Tier, "
        "Q1 Spend, Q4 Prior, and Change %. At the bottom, a summary "
        "names the top three movers by absolute change. An audit "
        "footer lists the source files, the run date (2026-04-25), "
        "and the model.",
    )

    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Claude Code read .claude/commands/spend-analyze.md and "
        "replaced $ARGUMENTS with \"Q1 direct-materials\".",
    )
    numbered(
        doc,
        "It parsed the arguments: period = Q1 (meaning January "
        "through March 2026), category = direct-materials.",
    )
    numbered(
        doc,
        "It opened data/spend-transactions.csv, filtered to 312 rows "
        "where the date fell in Q1 2026 and the category equaled "
        "direct-materials.",
    )
    numbered(
        doc,
        "It grouped by supplier_id, summed amount_usd, and ranked "
        "the 12 suppliers by total spend descending.",
    )
    numbered(
        doc,
        "It pulled the same category for Q4 2025, computed the "
        "period-over-period change for each supplier, and flagged "
        "the top three movers by absolute change.",
    )
    numbered(
        doc,
        "It joined supplier-master.csv to add tier and risk_rating "
        "columns to the output table.",
    )
    numbered(
        doc,
        "It saved the output to outputs/ with today's date in the "
        "file name and appended an audit footer naming the source "
        "files and the model.",
    )

    # Example B
    heading(doc, "Example B: /contract-sweep 90", 2)

    para(doc, "**The prompt you type in Claude Code (in the terminal).**")
    code_block(doc, "/contract-sweep 90")

    para(doc, "**The folder layout.**")
    code_block(
        doc,
        "practice/\n"
        "+-  .claude/commands/contract-sweep.md\n"
        "+-  data/contract-register.csv     (45 rows)\n"
        "+-  data/supplier-master.csv       (50 rows)\n"
        "+-  outputs/                       (results land here)",
    )

    para(
        doc,
        "**What you should see.** Claude Code (in the terminal) "
        "produces a file named "
        "outputs/contract_sweep_90d_2026-04-25.md. The file opens "
        "with: \"Contract Expiry Sweep: 90-day horizon from "
        "2026-04-25. Found 8 contracts expiring by 2026-07-24.\" "
        "Below is a table with columns: Contract ID, Supplier, "
        "End Date, Annual Value (USD), Auto-Renew, Notice Window, "
        "and Action Required. Two contracts are flagged because "
        "their notice window has already passed, meaning auto-renew "
        "will trigger unless the team acts immediately. The table is "
        "sorted by end date ascending so the most urgent contracts "
        "appear first.",
    )

    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Claude Code read .claude/commands/contract-sweep.md and "
        "replaced $ARGUMENTS with \"90\".",
    )
    numbered(
        doc,
        "It parsed the argument: horizon = 90 days from today "
        "(2026-04-25), giving a cutoff date of 2026-07-24.",
    )
    numbered(
        doc,
        "It opened data/contract-register.csv (45 rows) and filtered "
        "to 8 contracts where end_date fell on or before 2026-07-24.",
    )
    numbered(
        doc,
        "For each contract, it checked auto_renew and "
        "notice_period_days. If auto_renew was \"yes\" and the notice "
        "deadline had already passed (end_date minus notice_period_days "
        "was before today), it flagged the contract as \"Notice window "
        "passed, auto-renew will trigger.\"",
    )
    numbered(
        doc,
        "It joined supplier-master.csv to add risk_rating and tier "
        "for context.",
    )
    numbered(
        doc,
        "It sorted by end_date ascending, saved the output to "
        "outputs/ with a datestamp, and appended an audit footer.",
    )

    # ===================================================================
    # 7. A day in the life
    # ===================================================================
    heading(doc, "7. A day in the life: Priya, Procurement Operations Analyst", 1)
    para(
        doc,
        "Priya is a Procurement Operations Analyst at a US food "
        "manufacturer. Annual procurement spend is 52m USD across "
        "60 suppliers in five categories. Today is the first Monday "
        "of the month. Priya has Claude Code (in the terminal) open "
        "in her project folder, which has the same command library "
        "you build in this course. She built the commands two months "
        "ago and has used them every reporting cycle since.",
    )

    # 08:30
    heading(doc, "08:30: CPO asks for the monthly spend report", 2)
    para(
        doc,
        "**The situation.** Priya's CPO sends a message at 08:27: "
        "\"Monthly spend breakdown for Q1, direct materials. Need it "
        "before the 10:00 leadership meeting.\" Last month, Priya "
        "typed a 12-line prompt from memory. It took 25 minutes, and "
        "the format was slightly different from February's version. "
        "Her CPO noticed the difference and asked her to reconcile "
        "them. Today she has a command.",
    )
    para(doc, "**The prompt Priya types in Claude Code (in the terminal).**")
    code_block(doc, "/spend-analyze Q1 direct-materials")
    para(
        doc,
        "**What Claude Code produced.** A datestamped spend analysis "
        "in outputs/. Headline: \"Q1 2026 Spend Analysis: Direct "
        "Materials. Total spend: 5,230,000 USD across 14 suppliers.\" "
        "A ranked table with prior-period comparison. The top three "
        "movers flagged at the bottom. Audit footer with source "
        "files and run date. Total time: 3 minutes, including review.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Read spend-analyze.md from .claude/commands/.",
    )
    numbered(
        doc,
        "Replaced $ARGUMENTS with \"Q1 direct-materials\", parsed "
        "period = Q1, category = direct-materials.",
    )
    numbered(
        doc,
        "Filtered spend-transactions.csv to Q1 2026 and "
        "direct-materials. Grouped by supplier, summed, ranked.",
    )
    numbered(
        doc,
        "Compared to Q4 2025. Flagged top movers. Saved to outputs/ "
        "with datestamp and audit footer.",
    )
    para(
        doc,
        "**What to learn from this.** The command removed two sources "
        "of error: prompt wording and format inconsistency. Every "
        "month, the spend report has the same sections, the same "
        "columns, and the same audit footer. Priya's CPO sees the "
        "same shape of report regardless of who runs it or when.",
    )

    # 10:00
    heading(doc, "10:00: CFO flags unusual invoices", 2)
    para(
        doc,
        "**The situation.** During the leadership meeting, the CFO "
        "asks: \"I saw three invoices last quarter that were well "
        "above normal for their category. Can you flag anything "
        "unusual in Q1?\" Priya used to manually scan the "
        "transaction file in Excel, sorting by amount and eyeballing "
        "outliers. That took 40 minutes and missed patterns like "
        "duplicate PO numbers. Today she has a command.",
    )
    para(doc, "**The prompt Priya types in Claude Code (in the terminal).**")
    code_block(doc, "/anomaly-detect 2.5 Q1")
    para(
        doc,
        "**What Claude Code produced.** A structured alert report in "
        "outputs/. Headline: \"Anomaly Detection: Q1 2026, threshold "
        "2.5x category average.\" Section 1: 6 transactions flagged "
        "as high-value outliers (each exceeded 2.5 times its category "
        "average). Section 2: 4 duplicate PO patterns detected (same "
        "PO number appearing on different dates or with different "
        "suppliers). Each alert includes the transaction ID, supplier "
        "name, amount in USD, the category average, and the multiplier. "
        "Total time: 4 minutes.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Read anomaly-detect.md from .claude/commands/.",
    )
    numbered(
        doc,
        "Parsed $ARGUMENTS: threshold = 2.5, period = Q1.",
    )
    numbered(
        doc,
        "Computed the average transaction amount per category for Q1 "
        "2026.",
    )
    numbered(
        doc,
        "Flagged every transaction where amount_usd exceeded 2.5 "
        "times its category average. Listed 6 outliers.",
    )
    numbered(
        doc,
        "Scanned for duplicate PO numbers (same po_number appearing "
        "on different dates or with different suppliers). Found 4 "
        "patterns.",
    )
    numbered(
        doc,
        "Saved the alert report to outputs/ with datestamp and audit "
        "footer.",
    )
    para(
        doc,
        "**What to learn from this.** The threshold is a parameter, "
        "not a hardcoded number. If the CFO says \"show me anything "
        "above 3x average,\" Priya types /anomaly-detect 3.0 Q1. "
        "Same command, different threshold, instant results. The "
        "command also catches duplicate POs, which manual scanning "
        "in Excel almost always misses because you have to sort by "
        "PO number and visually compare rows.",
    )

    # 11:30
    heading(doc, "11:30: Quarterly review prep", 2)
    para(
        doc,
        "**The situation.** Priya has a quarterly business review "
        "with Apex Electronics (SUP004) at 14:00. Apex is flagged "
        "as at_risk in the supplier master. Priya needs to review "
        "their scorecard trend before the meeting so she can speak "
        "to the numbers. Last quarter, pulling the trend took 20 "
        "minutes in Excel: filtering the scorecard history, building "
        "a comparison, and writing a paragraph about the direction. "
        "Today she has a command.",
    )
    para(doc, "**The prompt Priya types in Claude Code (in the terminal).**")
    code_block(doc, "/scorecard-refresh SUP004 Q1")
    para(
        doc,
        "**What Claude Code produced.** A one-page scorecard summary "
        "in outputs/. Headline: \"Scorecard Refresh: Apex Electronics "
        "(SUP004), Q1 2026.\" A table showing all five scoring "
        "dimensions (quality, delivery, responsiveness, cost, and "
        "innovation) across four quarters. A trend line: \"Overall "
        "score declined from 82.1 in Q2 2025 to 71.4 in Q1 2026. "
        "Largest drop: delivery (from 88 to 69).\" A recommendation: "
        "\"Escalate to quarterly improvement plan. Schedule follow-up "
        "review for Q2 2026.\" Total time: 3 minutes.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Read scorecard-refresh.md from .claude/commands/.",
    )
    numbered(
        doc,
        "Parsed $ARGUMENTS: supplier = SUP004, quarter = Q1.",
    )
    numbered(
        doc,
        "Opened scorecard-history.csv, filtered to SUP004 across all "
        "four quarters.",
    )
    numbered(
        doc,
        "Computed trend direction (improving, stable, or declining) "
        "for each dimension and overall.",
    )
    numbered(
        doc,
        "Generated the summary with specific scores and the "
        "recommendation. Saved to outputs/ with datestamp.",
    )
    para(
        doc,
        "**What to learn from this.** The command produces the same "
        "scorecard shape for any supplier. Priya can run "
        "/scorecard-refresh SUP007 Q1 for an improving supplier and "
        "get the same format with different numbers. The consistency "
        "makes quarterly reviews faster to prepare and easier for "
        "stakeholders to read. Every supplier's summary has the same "
        "sections, the same trend terminology, and the same "
        "recommendation structure.",
    )

    # 14:00
    heading(doc, "14:00: Contract expiry alert", 2)
    para(
        doc,
        "**The situation.** After the Apex meeting, Priya's manager "
        "asks: \"Which contracts are coming up for renewal in the "
        "next 90 days? I need the list before I leave at 16:00.\" "
        "In the past, Priya opened the contract register in Excel, "
        "sorted by end date, manually checked auto-renew clauses, "
        "and calculated whether notice windows had passed. That took "
        "30 minutes and she once missed a contract that auto-renewed "
        "because she forgot to check the notice period. Today she has "
        "a command.",
    )
    para(doc, "**The prompt Priya types in Claude Code (in the terminal).**")
    code_block(doc, "/contract-sweep 90")
    para(
        doc,
        "**What Claude Code produced.** A prioritized action list in "
        "outputs/. Headline: \"Contract Expiry Sweep: 90-day horizon "
        "from 2026-04-25. Found 8 contracts expiring by 2026-07-24.\" "
        "A table with Contract ID, Supplier, End Date, Annual Value "
        "(USD), Auto-Renew, Notice Window, and Action Required. Two "
        "contracts flagged as \"Notice window passed\" because their "
        "auto-renew notice deadline was before today. The table is "
        "sorted by urgency, with the passed-notice contracts at the "
        "top. Total time: 3 minutes.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Read contract-sweep.md from .claude/commands/.",
    )
    numbered(
        doc,
        "Parsed $ARGUMENTS: horizon = 90 days, cutoff = 2026-07-24.",
    )
    numbered(
        doc,
        "Filtered contract-register.csv to 8 contracts expiring on "
        "or before the cutoff.",
    )
    numbered(
        doc,
        "Checked auto-renew and notice period for each. Flagged two "
        "contracts where the notice deadline had already passed.",
    )
    numbered(
        doc,
        "Sorted by end_date ascending. Saved to outputs/ with "
        "datestamp and audit footer.",
    )
    para(
        doc,
        "**What to learn from this.** The horizon is a parameter. "
        "Next month, Priya's manager might say \"show me 60 days.\" "
        "Priya types /contract-sweep 60. The command also catches "
        "auto-renew traps that manual scanning misses: contracts "
        "that will silently renew because the notice window already "
        "closed. That one feature alone can save thousands of "
        "dollars in unwanted renewals.",
    )

    # 15:30
    heading(doc, "15:30: New sourcing event kickoff", 2)
    para(
        doc,
        "**The situation.** The CPO calls Priya at 15:20: \"Direct "
        "materials contracts are expiring. Start pulling together a "
        "sourcing brief for the next RFP. Bids should close by "
        "2026-07-31.\" In the past, Priya would open a blank Word "
        "document, pull spend data from one spreadsheet, contract "
        "data from another, and draft the brief over two days. Today "
        "she has a command that combines the spend analysis and "
        "contract sweep into a sourcing brief in one step.",
    )
    para(doc, "**The prompt Priya types in Claude Code (in the terminal).**")
    code_block(doc, "/rfp-launch direct-materials 2026-07-31")
    para(
        doc,
        "**What Claude Code produced.** A sourcing brief in outputs/. "
        "Headline: \"Sourcing Brief: Direct Materials. Baseline "
        "spend: 18,400,000 USD (trailing 12 months). Expiring "
        "contracts: 4 (by 2026-07-31). Bid close: 2026-07-31.\" The "
        "brief includes a spend summary table by supplier, a list of "
        "expiring contracts with annual values, a draft timeline "
        "(RFP issue date, bid close, evaluation period, and award "
        "date), and three recommended actions. Total time: 5 minutes.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Read rfp-launch.md from .claude/commands/.",
    )
    numbered(
        doc,
        "Parsed $ARGUMENTS: category = direct-materials, deadline = "
        "2026-07-31.",
    )
    numbered(
        doc,
        "Ran the same filtering and grouping logic as /spend-analyze "
        "for the trailing 12 months, filtered to direct-materials.",
    )
    numbered(
        doc,
        "Ran the same expiry logic as /contract-sweep, filtering to "
        "contracts in the direct-materials category expiring by "
        "2026-07-31.",
    )
    numbered(
        doc,
        "Combined the spend summary and expiring contracts into a "
        "single sourcing brief. Built a timeline working backward "
        "from the 2026-07-31 deadline. Saved to outputs/ with a "
        "datestamp.",
    )
    para(
        doc,
        "**What to learn from this.** Commands can reuse other "
        "commands' logic. The /rfp-launch command uses the same "
        "filtering and grouping patterns from /spend-analyze and "
        "/contract-sweep. You wrote those patterns once. Now they "
        "appear in a third command without copy-pasting. If you "
        "improve the spend analysis logic later, every command that "
        "reuses it benefits from the improvement.",
    )

    # Summary table
    heading(doc, "Priya's day: the numbers", 2)
    fill_table(
        doc,
        ["Time", "Task", "Command", "Time with commands", "Time without"],
        [
            ["08:30", "Monthly spend report", "/spend-analyze", "3 min", "25 min"],
            ["10:00", "Anomaly detection", "/anomaly-detect", "4 min", "40 min"],
            ["11:30", "Scorecard refresh", "/scorecard-refresh", "3 min", "20 min"],
            ["14:00", "Contract expiry sweep", "/contract-sweep", "3 min", "30 min"],
            ["15:30", "Sourcing brief", "/rfp-launch", "5 min", "45 min"],
            ["", "Total", "", "18 min", "160 min"],
        ],
    )
    para(
        doc,
        "Priya finished five recurring tasks in 18 minutes. Without "
        "commands, those same tasks would have taken 160 minutes. She "
        "used the remaining 142 minutes to prepare for her Apex review, "
        "follow up on the CFO's anomaly questions with supporting "
        "detail, and draft a response to the two auto-renew contracts "
        "that the sweep identified.",
    )
    para(
        doc,
        "Notice what Priya did not do. She did not write a single "
        "free-text prompt. She did not scroll through chat history "
        "to find last month's wording. She did not reformat a single "
        "table. The commands handled all of that. Priya's job shifted "
        "from producing reports to reviewing them, and from typing "
        "prompts to acting on results.",
    )

    # ===================================================================
    # 8. The 20-minute sprint
    # ===================================================================
    heading(doc, "8. The 20-minute sprint", 1)
    para(
        doc,
        "This section is for someone who has never built a slash "
        "command and wants their first working command in 20 minutes. "
        "It assumes Claude Code (in the terminal) is already "
        "installed (Course 1) and you have a CLAUDE.md in your "
        "project folder (Course 2). You do not need to have completed "
        "Course 3.",
    )

    heading(doc, "Minutes 0 to 5: Set up the folder", 2)
    para(doc, "**What to do.** Open your terminal and navigate to your project folder.")
    code_block(doc, "cd your-project-folder")
    para(doc, "Create the commands folder if it does not exist.")
    code_block(doc, "mkdir -p .claude/commands")
    para(doc, "Confirm the folder exists.")
    code_block(doc, "ls .claude/commands/")
    para(
        doc,
        "**What you should see.** An empty directory listing. The "
        "folder exists and is ready for your first command file. If "
        "you see a \"no such file or directory\" error, check that "
        "you ran the mkdir command from your project root, not from "
        "a subfolder.",
    )

    heading(doc, "Minutes 5 to 10: Write your first command", 2)
    para(
        doc,
        "**What to do.** Start Claude Code (in the terminal) and ask "
        "it to create a simple command file. Type the following prompt "
        "exactly as shown.",
    )
    code_block(
        doc,
        "Create a file at .claude/commands/spend-summary.md with this content:\n\n"
        "# /spend-summary\n"
        "## Arguments\n"
        "$ARGUMENTS contains one value: the category to summarize.\n"
        "## Steps\n"
        "1. Read data/spend-transactions.csv.\n"
        "2. Filter to the category in $ARGUMENTS.\n"
        "3. Group by supplier. Sum amount_usd.\n"
        "4. Rank by total spend descending.\n"
        "5. Save to outputs/spend_summary_[category]_[today].md.",
    )
    para(
        doc,
        "**What you should see.** Claude Code creates the file at "
        ".claude/commands/spend-summary.md. You can verify by "
        "running ls .claude/commands/ in your terminal. The file "
        "should appear in the listing.",
    )

    heading(doc, "Minutes 10 to 15: Run the command", 2)
    para(
        doc,
        "**What to do.** Type the slash command in Claude Code (in "
        "the terminal). Make sure you have a data/ folder with a "
        "spend-transactions.csv file (the course practice data works).",
    )
    code_block(doc, "/spend-summary direct-materials")
    para(
        doc,
        "**What you should see.** Claude Code reads the command file, "
        "replaces $ARGUMENTS with \"direct-materials\", opens your "
        "spend data, filters to direct-materials, groups by supplier, "
        "and saves a summary to outputs/. The whole process takes "
        "about 60 seconds. You should see Claude Code working through "
        "the steps in the terminal output.",
    )

    heading(doc, "Minutes 15 to 20: Review and refine", 2)
    para(
        doc,
        "**What to do.** Open the output file in outputs/ and check "
        "three things.",
    )
    numbered(
        doc,
        "Does the headline name the category and the total spend?",
    )
    numbered(
        doc,
        "Does the table rank suppliers by spend descending?",
    )
    numbered(
        doc,
        "Is there an audit footer with the source file, the date, "
        "and the model?",
    )
    para(
        doc,
        "If any of those are missing, open the command file in a text "
        "editor, add the missing instruction (for example, add "
        "\"Include an audit footer with the source file name, today's "
        "date, and the model\" to the Steps section), save the file, "
        "and run the command again. The output should now include the "
        "missing element.",
    )
    para(
        doc,
        "You now have a working slash command. When you are ready to "
        "build the full library of six commands, open the course "
        "folder and start Lesson 2.",
    )

    # ===================================================================
    # 9. Your first week with commands in your real work
    # ===================================================================
    heading(doc, "9. Your first week with commands in your real work", 1)
    para(
        doc,
        "This planner covers five days. Each day has a specific goal "
        "and a concrete deliverable. By the end of the week, you "
        "have a working command library customized for your own "
        "procurement data.",
    )

    heading(doc, "Day 1: Install your first command", 2)
    para(doc, "**Goals:** Set up the .claude/commands/ folder in your real project. Write and run one command.")
    numbered(
        doc,
        "Create .claude/commands/ in your real project folder "
        "(the one with your actual spend data).",
    )
    numbered(
        doc,
        "Copy the spend-analyze.md command file from the course "
        "practice folder into your .claude/commands/.",
    )
    numbered(
        doc,
        "Edit the command file to match your data: update the CSV "
        "file name if yours is named differently, update the column "
        "names if yours use different headers, and update the "
        "category values to match your categories.",
    )
    numbered(
        doc,
        "Run /spend-analyze Q1 [your-category]. Verify the output "
        "looks correct and uses your real supplier names.",
    )
    para(
        doc,
        "**Deliverable:** One spend analysis output file in your "
        "outputs/ folder, generated from your real data.",
    )

    heading(doc, "Day 2: Add anomaly detection", 2)
    para(doc, "**Goals:** Write and run the /anomaly-detect command on your real data. Calibrate the threshold.")
    numbered(
        doc,
        "Copy anomaly-detect.md from the course folder.",
    )
    numbered(
        doc,
        "Edit the threshold logic if your data has different volume "
        "patterns. If your category averages are much higher than "
        "Meridian's, you may want a threshold of 3.0 instead of 2.5.",
    )
    numbered(
        doc,
        "Run /anomaly-detect 2.5 Q1. Review the alerts. Are the "
        "flagged transactions genuinely unusual, or is the threshold "
        "too low? If you get more than 20 alerts, raise the threshold.",
    )
    numbered(
        doc,
        "Adjust the threshold and run again until the alert list "
        "contains only items worth investigating.",
    )
    para(
        doc,
        "**Deliverable:** One anomaly report on your real data, with "
        "a threshold you trust.",
    )

    heading(doc, "Day 3: Add scorecard and contract sweep", 2)
    para(doc, "**Goals:** Write and run two more commands. Build the habit of typing commands instead of free-text prompts.")
    numbered(
        doc,
        "Copy scorecard-refresh.md and contract-sweep.md from the "
        "course folder.",
    )
    numbered(
        doc,
        "Edit both to match your data file names, column names, and "
        "scoring dimensions. If your scorecards use different metrics "
        "(for example, safety instead of innovation), update the "
        "command file.",
    )
    numbered(
        doc,
        "Run /scorecard-refresh [your-supplier] Q1 and "
        "/contract-sweep 90. Verify both outputs against your data.",
    )
    para(
        doc,
        "**Deliverable:** A scorecard summary for one supplier and "
        "a contract expiry list, both from your real data.",
    )

    heading(doc, "Day 4: Build a chained command", 2)
    para(doc, "**Goals:** Write the /rfp-launch command that combines spend and contract data into a sourcing brief.")
    numbered(
        doc,
        "Copy rfp-launch.md from the course folder.",
    )
    numbered(
        doc,
        "Edit it to reference your data files and your category "
        "names.",
    )
    numbered(
        doc,
        "Run /rfp-launch [your-category] [your-deadline]. Review "
        "the sourcing brief.",
    )
    numbered(
        doc,
        "If the timeline section does not match your organization's "
        "process (for example, your evaluations take three weeks, not "
        "two), edit the command file to adjust the milestone sequence.",
    )
    para(
        doc,
        "**Deliverable:** A sourcing brief that pulls from both "
        "spend and contract data in a single command.",
    )

    heading(doc, "Day 5: Review, refine, and share", 2)
    para(doc, "**Goals:** Clean up your command library. Share it with one colleague. Plan next week's improvements.")
    numbered(
        doc,
        "Review all command files in .claude/commands/. Check that "
        "each file names the correct data files, the correct column "
        "names, and the correct output format.",
    )
    numbered(
        doc,
        "Run each command once and compare the output to what you "
        "expected. Fix any discrepancies in the command file.",
    )
    numbered(
        doc,
        "Copy your .claude/commands/ folder to a colleague. Walk "
        "them through running one command on their machine. Verify "
        "their output matches the same shape as yours.",
    )
    numbered(
        doc,
        "Write down three improvements you want to make next week. "
        "Example improvements: \"Add a /savings-update command,\" "
        "\"Lower the anomaly threshold to 2.0 for the indirect "
        "category,\" or \"Add a subcategory parameter to "
        "/spend-analyze.\"",
    )
    para(
        doc,
        "**Deliverable:** A tested command library shared with at "
        "least one colleague. A short list of next-week improvements.",
    )

    # ===================================================================
    # 10. The pattern: one command, any period, any category
    # ===================================================================
    heading(doc, "10. The pattern: one command, any period, any category", 1)
    para(
        doc,
        "Every command you built in this course follows the same "
        "pattern. The command file is static. The arguments change. "
        "The output shape stays the same. Here is the pattern, "
        "spelled out.",
    )
    numbered(
        doc,
        "**The command file names the data sources.** It says "
        "\"read data/spend-transactions.csv\" or \"read "
        "data/contract-register.csv.\" The file paths are fixed. "
        "They do not change between runs.",
    )
    numbered(
        doc,
        "**$ARGUMENTS supplies the changing inputs.** The period, "
        "the category, the supplier ID, the threshold, or the "
        "deadline. These are the only things that differ between "
        "runs.",
    )
    numbered(
        doc,
        "**The analysis steps are numbered and explicit.** Filter, "
        "group, sum, compare, rank, or flag. Claude Code (in the "
        "terminal) follows them in order. No ambiguity.",
    )
    numbered(
        doc,
        "**The output format is pinned.** Same headline structure, "
        "same table columns, same audit footer. Every run produces "
        "the same shape. A reader who saw last month's report "
        "recognizes this month's instantly.",
    )
    numbered(
        doc,
        "**The save location uses a datestamp.** No overwriting. "
        "Every run creates a new file. You can compare this month's "
        "output to last month's by opening two files side by side.",
    )
    para(
        doc,
        "**Why this matters.** This pattern is transferable. You can "
        "apply it to any recurring procurement task: savings tracking, "
        "compliance checks, payment term reviews, category "
        "performance summaries, supplier onboarding checklists, or "
        "weekly PO approval reports. The test is simple: if you do "
        "the same analysis more than once a quarter, it belongs in "
        "a command. Write the command once. Run it by name. Change "
        "only the arguments.",
    )
    para(
        doc,
        "Once you see this pattern, you will start noticing it "
        "everywhere. Every monthly report your team produces by "
        "hand is a candidate for a command. Every quarterly review "
        "that takes an hour to prepare is a candidate. Every "
        "contract check that someone runs in Excel and emails as "
        "a PDF is a candidate. The command library grows over time. "
        "Each new command saves more time than the last because you "
        "already know the five-section structure.",
    )
    para(
        doc,
        "A useful exercise: open your calendar for the last month. "
        "Count the recurring procurement tasks. For each one, ask: "
        "\"Did I type a free-text prompt for this?\" If the answer "
        "is yes, that task is a command candidate. Start with the "
        "task you run most often. Write the command. Run it. Then "
        "move to the next. Within a month, your most frequent tasks "
        "will be one-liners.",
    )

    # ===================================================================
    # 11. Quick reference and troubleshooting
    # ===================================================================
    heading(doc, "11. Quick reference and troubleshooting", 1)

    heading(doc, "Things to remember", 2)
    bullet(
        doc,
        "Command files live in .claude/commands/ inside your project "
        "folder. Claude Code (in the terminal) only looks there.",
    )
    bullet(
        doc,
        "File names must match the command name. The file for "
        "/spend-analyze is spend-analyze.md. Not spend_analyze.md. "
        "Not Spend-Analyze.md.",
    )
    bullet(
        doc,
        "$ARGUMENTS captures everything after the command name. "
        "Your command file must include instructions for parsing "
        "the arguments into individual values.",
    )
    bullet(
        doc,
        "Command files are plain markdown. No special syntax "
        "beyond $ARGUMENTS. If you can write a numbered list, you "
        "can write a command file.",
    )
    bullet(
        doc,
        "Outputs go to outputs/ with a datestamp in the file name. "
        "Never overwrite a prior output.",
    )
    bullet(
        doc,
        "If you share commands with a colleague, share the entire "
        ".claude/commands/ folder. Individual files work only if "
        "the colleague's data file paths match yours.",
    )

    heading(doc, "Troubleshooting", 2)

    # Issue 1
    para(
        doc,
        "**Symptom:** You type /spend-analyze and Claude Code (in "
        "the terminal) says \"Unknown command.\"",
    )
    para(
        doc,
        "**Fix:** Check that the file exists at "
        ".claude/commands/spend-analyze.md (not spend_analyze.md, "
        "not Spend-Analyze.md). The file name must match the command "
        "name exactly, with hyphens, all lowercase. Also confirm you "
        "are running Claude Code from the project root, not from a "
        "subfolder.",
    )

    # Issue 2
    para(
        doc,
        "**Symptom:** The command runs but produces empty output "
        "or says \"no data found.\"",
    )
    para(
        doc,
        "**Fix:** Check that $ARGUMENTS matches values in your "
        "data. If your category column says \"Direct Materials\" "
        "(with capitals and a space) but you type "
        "/spend-analyze Q1 direct-materials, the filter will find "
        "zero rows. Update your command file to handle case "
        "differences, or standardize your data to use lowercase "
        "with hyphens.",
    )

    # Issue 3
    para(
        doc,
        "**Symptom:** Claude Code reads the command file but ignores "
        "some of the instructions.",
    )
    para(
        doc,
        "**Fix:** Long command files (over 80 lines) sometimes "
        "cause Claude Code to skip later sections. Keep each "
        "command file between 30 and 70 lines. If you need more "
        "detail, split the command into two commands and chain them "
        "(like /rfp-launch chains /spend-analyze and /contract-sweep).",
    )

    # Issue 4
    para(
        doc,
        "**Symptom:** The output file overwrites a previous "
        "output with the same name.",
    )
    para(
        doc,
        "**Fix:** Your command file's save section is missing the "
        "datestamp instruction. Add: \"Include today's date "
        "(YYYY-MM-DD) in the file name.\" Example file name: "
        "spend_analysis_Q1_direct-materials_2026-04-25.md.",
    )

    # Issue 5
    para(
        doc,
        "**Symptom:** A colleague runs your command and gets a "
        "\"file not found\" error for the data file.",
    )
    para(
        doc,
        "**Fix:** The command file references a data path that "
        "exists on your machine but not on theirs. Use relative "
        "paths (data/spend-transactions.csv), not absolute paths "
        "(C:/Users/you/project/data/spend-transactions.csv). "
        "Confirm the colleague has the same folder structure and "
        "the same file names.",
    )

    # Issue 6
    para(
        doc,
        "**Symptom:** The command runs but the output format is "
        "different from last month's version.",
    )
    para(
        doc,
        "**Fix:** Your command file's output format section may be "
        "too vague. Instead of \"produce a summary,\" write the "
        "exact section headings and table columns you want. Example: "
        "\"Output a table with columns: Rank, Supplier, Category, "
        "Tier, Spend (USD), Prior Period (USD), Change %.\" Pin "
        "the shape so Claude Code (in the terminal) cannot improvise.",
    )

    # ===================================================================
    # 12. You are done with Course 4 when
    # ===================================================================
    heading(doc, "12. You are done with Course 4 when", 1)
    para(
        doc,
        "Use this checklist to confirm you have completed the "
        "course. All six items must be true before you move on.",
    )
    numbered(
        doc,
        "Your .claude/commands/ folder has six command files "
        "(spend-analyze.md, anomaly-detect.md, scorecard-refresh.md, "
        "contract-sweep.md, rfp-launch.md, and savings-update.md). "
        "Each file is between 30 and 70 lines.",
    )
    numbered(
        doc,
        "You have run /spend-analyze Q1 direct-materials and "
        "produced a datestamped spend analysis in outputs/.",
    )
    numbered(
        doc,
        "You have run /anomaly-detect 2.5 Q1 and it found the "
        "planted high-value transactions and duplicate PO patterns.",
    )
    numbered(
        doc,
        "You have run /contract-sweep 90 and it listed the 8 "
        "contracts expiring within 90 days of 2026-04-25.",
    )
    numbered(
        doc,
        "You have run /rfp-launch direct-materials 2026-07-31 and "
        "it produced a sourcing brief with baseline spend, expiring "
        "contracts, and a timeline.",
    )
    numbered(
        doc,
        "You can copy your .claude/commands/ folder into your real "
        "procurement project and run the same commands on your own "
        "data with only minor edits to file names and column names.",
    )

    # --- Save ---
    doc.save(str(OUTPUT_PATH))
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Size: {OUTPUT_PATH.stat().st_size:,} bytes")


if __name__ == "__main__":
    build()
