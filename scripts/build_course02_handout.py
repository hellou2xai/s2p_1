"""Build the Course 2: The Context Architect e-learning handout (v2).

Revised version with scenario-led section 2, folder explanations with
examples in section 3, Claude Code terminal examples throughout every
section, a real-workday Day in the Life (not a course walkthrough),
and behind-the-scenes walkthroughs on every worked example.

Style follows CLAUDE.md: no em-dashes, Oxford commas, American English,
no banned phrases, four-part rule on every worked example.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt


_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
OUTPUT_PATH = _PROJECT_ROOT / "Handouts" / "Course_02_The_Context_Architect_Handout.docx"


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
    para(doc, "Series 2 (Engineering Track) | Course 2", italic=True)
    doc.add_heading("The Context Architect", level=0)
    para(
        doc,
        "How to give Claude the right background for procurement work.",
        italic=True,
        size=14,
    )
    para(
        doc,
        "Three hours. Six lessons. No coding. Real procurement data "
        "(10,500 rows).",
        italic=True,
    )
    para(
        doc,
        "Use this handout alongside the course folder at "
        "Detailed Course Content/Course_02_The_Context_Architect/.",
        italic=True,
    )

    # ===================================================================
    # 1. How to use this handout
    # ===================================================================
    heading(doc, "1. How to use this handout", 1)
    para(
        doc,
        "This handout is your reading companion. The hands-on work "
        "happens in the course folder you got with this guide. The "
        "folder has the data (10,500 rows in CSVs), the starter files, "
        "the six lessons, and the reference answers. Everything is in "
        "one place. No external downloads.",
    )
    para(doc, "How to read this guide:")
    numbered(
        doc,
        "Read sections 2 and 3 to understand what the course is and "
        "what you end up with.",
    )
    numbered(
        doc,
        "Read section 4 to see how much time the course saves you "
        "per week, once you have done it.",
    )
    numbered(
        doc,
        "Read section 5 for the simple mental model of how Claude "
        "reads files.",
    )
    numbered(doc, "Open the course folder and start Lesson 1.")
    numbered(
        doc,
        "Come back to this handout when you want context (sections 6 "
        "to 8 are useful while you work).",
    )
    numbered(
        doc,
        "Use section 11 (troubleshooting) if something does not look "
        "right.",
    )

    # ===================================================================
    # 2. What this course teaches  (scenario-led)
    # ===================================================================
    heading(doc, "2. What this course teaches", 1)

    heading(doc, "A Tuesday morning you have lived before", 2)
    para(
        doc,
        "It is 09:30 Tuesday. Your CPO Slacks: \"Need three short "
        "briefs by Friday. One on materials, one on logistics, one on "
        "indirect. Top suppliers, anything risky, what we should do "
        "about it.\"",
    )
    para(
        doc,
        "You open Claude Code (in the terminal). You type: \"Help me "
        "write a category brief.\" Claude writes something. The grammar "
        "is right. The shape is right. The content is wrong. The "
        "materials brief talks about preferred-vendor compliance (an "
        "indirect rule). The logistics brief asks about chip suppliers "
        "(those are materials). The indirect brief talks about transit "
        "times (those are logistics).",
    )
    para(
        doc,
        "You spend Tuesday afternoon rewriting brief one. By Wednesday "
        "morning, you have not started briefs two and three.",
    )

    heading(doc, "The fix: a stack of small files", 2)
    para(
        doc,
        "The problem is that Claude has no background. Your CLAUDE.md "
        "file says \"I work in procurement\" and nothing else. Claude "
        "cannot tell direct materials from indirect.",
    )
    para(
        doc,
        "This course teaches you to build a small stack of CLAUDE.md "
        "files:",
    )
    bullet(
        doc,
        "**One global file at the top of your project.** It says who "
        "you are, your folder rules, and your writing rules. Three "
        "short sections.",
    )
    bullet(
        doc,
        "**One small file in each category folder.** It says what is "
        "special about that category: which suppliers, which rules, "
        "which data files.",
    )
    para(
        doc,
        "When you start Claude Code (in the terminal) in a category "
        "folder, Claude reads BOTH files automatically. You do not "
        "type anything different. The folder you start in is the "
        "difference.",
    )

    heading(doc, "See it in Claude Code", 2)
    para(doc, "**The prompt you type in the terminal after setting up the stack:**")
    code_block(
        doc,
        "cd practice/direct-materials\n"
        "claude\n\n"
        "> Build a category intelligence brief for this category.\n"
        "> Inputs: use the data files my CLAUDE.md points at.\n"
        "> Save as category_brief.md in this folder.",
    )
    para(
        doc,
        "**What you should see.** A 400-word brief naming only "
        "direct-materials suppliers (Great Lakes Steel, Heartland "
        "Steel, Pacific Aluminum), the at-risk flag on SUP004 Apex "
        "Electronics, and one recommended action. No carrier or "
        "vendor appears.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Loaded two CLAUDE.md files at session start: the global "
        "(practice/CLAUDE.md) and the category file "
        "(direct-materials/CLAUDE.md).",
    )
    numbered(
        doc,
        "Resolved \"the data files my CLAUDE.md points at\" to "
        "suppliers.csv and orders.csv (named in the category file).",
    )
    numbered(
        doc,
        "Read orders.csv (2,500 rows), summed total_usd by "
        "supplier_id, joined to supplier_name in suppliers.csv, "
        "sorted descending.",
    )
    numbered(
        doc,
        "Checked suppliers.csv for at_risk status. Found SUP004 "
        "Apex Electronics, contract_end 2026-05-31.",
    )
    numbered(
        doc,
        "Wrote a 400-word brief with three sections and an audit "
        "footer, saved to direct-materials/category_brief.md.",
    )
    para(
        doc,
        "Run the same prompt from logistics/ and you get a "
        "logistics brief (carriers only). Run from indirect/ and "
        "you get an indirect brief (vendors, plus the 18 approval "
        "violations). Same prompt, three different correct outputs.",
    )

    # ===================================================================
    # 3. What is in the course folder
    # ===================================================================
    heading(doc, "3. What is in the course folder", 1)
    para(
        doc,
        "Open the course folder before you start. Everything is "
        "inside, in a flat structure with no nested data folders. "
        "The CSV files sit alongside the CLAUDE.md in each category "
        "folder.",
    )
    code_block(
        doc,
        "Course_02_The_Context_Architect/\n"
        "├── README.md                       (start here, course navigation)\n"
        "├── COURSE_OVERVIEW.md              (the story behind the course)\n"
        "├── lessons/                        (six lessons, follow them in order)\n"
        "│   ├── Lesson_01_How_Claude_Reads_CLAUDE_md.md\n"
        "│   ├── Lesson_02_Writing_The_Global_CLAUDE_md.md\n"
        "│   ├── Lesson_03_Writing_Folder_Level_CLAUDE_md.md\n"
        "│   ├── Lesson_04_Testing_The_Hierarchy.md\n"
        "│   ├── Lesson_05_Dynamic_CLAUDE_md.md\n"
        "│   └── Lesson_06_Category_Intelligence_Brief.md\n"
        "├── practice/                       (the hands-on workspace)\n"
        "│   ├── CLAUDE.md                   (starter, deliberately weak)\n"
        "│   ├── direct-materials/\n"
        "│   │   ├── CLAUDE.md               (stub)\n"
        "│   │   ├── suppliers.csv           (50 suppliers)\n"
        "│   │   └── orders.csv              (2,500 PO rows over the year)\n"
        "│   ├── logistics/\n"
        "│   │   ├── CLAUDE.md               (stub)\n"
        "│   │   ├── carriers.csv            (20 carriers)\n"
        "│   │   └── shipments.csv           (5,000 shipment rows)\n"
        "│   └── indirect/\n"
        "│       ├── CLAUDE.md               (stub)\n"
        "│       ├── vendors.csv             (80 vendors)\n"
        "│       └── invoices.csv            (3,000 invoice rows, 18 violations)\n"
        "├── solutions/                      (reference answers)\n"
        "└── scripts/build_course_data.py    (regenerates the data if you delete it)",
    )
    para(
        doc,
        "Today's date in the data is 2026-04-25. Every PO, every "
        "shipment, every invoice is dated within the last year so "
        "the exercises feel like real recent work.",
    )
    para(
        doc,
        "About 10,500 rows of data total. You will not read every "
        "row. Claude will, when you ask. That is the point: Claude "
        "becomes the analyst who reads the data while you direct "
        "the work.",
    )

    # ===================================================================
    # 4. Time savings
    # ===================================================================
    heading(doc, "4. What the course saves you", 1)
    para(
        doc,
        "Three hours of course time, once. The savings come every "
        "week after.",
    )
    fill_table(
        doc,
        ["Task you do every week", "Time without the stack",
         "Time with the stack"],
        [
            (
                "Three category briefs (one per category)",
                "3 to 4 hours: write three different prompts, "
                "manage context by hand",
                "20 to 30 minutes: one prompt, three folders, "
                "three correct briefs",
            ),
            (
                "Aggregate spend across thousands of order or "
                "invoice rows",
                "30 to 60 minutes per category in Excel",
                "30 seconds: Claude reads the CSV and sums it",
            ),
            (
                "Find policy violations across thousands of invoices",
                "Sample audit only; full audit takes a day",
                "60 seconds: Claude scans every row by the stated "
                "rule",
            ),
            (
                "Update a supplier or vendor master, then re-run "
                "a brief",
                "Edit CLAUDE.md and re-paste data into the chat. "
                "30 minutes.",
                "Update the CSV. The next session reads it. "
                "2 minutes.",
            ),
            (
                "Onboard a colleague to your workflow",
                "Walk them through prompts and rules. Half a day.",
                "Share the project folder. They get the same "
                "setup. 30 minutes.",
            ),
            (
                "Confirm the right context loaded before a "
                "critical brief",
                "Read the prompt and hope.",
                "Run the five-question test in 5 minutes. Always "
                "confirms what loaded.",
            ),
        ],
    )
    para(doc, "**See the savings in Claude Code.**")
    para(
        doc,
        "The spend aggregation row in the table above takes 30 to "
        "60 minutes in Excel. In Claude Code (in the terminal), "
        "you type one prompt:",
    )
    code_block(
        doc,
        "cd practice/direct-materials\n"
        "claude\n\n"
        "> Sum total_usd across all orders for the last year,\n"
        "> grouped by supplier. Show the top 5 by spend.",
    )
    para(
        doc,
        "**What you should see.** Five rows: Great Lakes Steel at "
        "the top, followed by Heartland Steel, Pacific Aluminum, "
        "and two more. Claude reads 2,500 order rows, joins to "
        "suppliers.csv, and returns the answer in 30 seconds.",
    )

    # ===================================================================
    # 5. The simple mental model
    # ===================================================================
    heading(doc, "5. The simple mental model: a stack of files", 1)
    para(
        doc,
        "Claude Code (in the terminal) reads CLAUDE.md files in a "
        "specific order, every time you start a session. The order "
        "is the same on Mac, Windows, and Linux:",
    )
    numbered(
        doc,
        "Claude looks in the folder you started in. If there is a "
        "CLAUDE.md, it reads it.",
    )
    numbered(
        doc,
        "Claude looks in the folder above. If there is a CLAUDE.md, "
        "it reads it too.",
    )
    numbered(
        doc,
        "Claude keeps walking up until it gets to your project root.",
    )
    numbered(
        doc,
        "Every CLAUDE.md it finds is stacked together as Claude's "
        "background for this session.",
    )
    para(
        doc,
        "So if your project has two files (one global at the top, "
        "one in each category folder), Claude reads BOTH when you "
        "start in a category folder. The global gives Claude the "
        "universal context, the category file gives Claude the "
        "specifics.",
    )
    para(doc, "Three layers, one map:")
    fill_table(
        doc,
        ["Layer", "Where it lives", "What it holds"],
        [
            (
                "Global",
                "practice/CLAUDE.md",
                "Who you are. Folder rules. Writing rules. "
                "About 25 to 40 lines.",
            ),
            (
                "Category file",
                "<category>/CLAUDE.md (one per category)",
                "What this folder is. Files in this folder. "
                "Rules specific to this category. About 20 to "
                "35 lines.",
            ),
            (
                "Data files",
                "<category>/<file>.csv",
                "The actual data. Master files small (20 to 80 "
                "rows). Activity files large (2,500 to 5,000 "
                "rows). Read at runtime.",
            ),
        ],
    )

    heading(doc, "Prove it yourself in Claude Code", 2)
    para(
        doc,
        "This is the test from Lesson 1. You add a marker to the "
        "global and to one category file, then watch Claude obey "
        "both at once.",
    )
    para(doc, "**The prompt you type in the terminal:**")
    code_block(
        doc,
        "cd practice/direct-materials\n"
        "claude\n\n"
        "> Hello, what files are in this folder?",
    )
    para(
        doc,
        "**What you should see.** If you added the test markers "
        "from Lesson 1, Claude's reply opens with \"GLOBAL FILE "
        "LOADED\" and \"MATERIALS FILE LOADED\", then lists "
        "suppliers.csv and orders.csv. Both CLAUDE.md files were "
        "loaded because you started in direct-materials/ (which is "
        "below practice/).",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Looked in direct-materials/ for a CLAUDE.md. Found it. "
        "Read it.",
    )
    numbered(
        doc,
        "Looked in practice/ (one level up). Found the global. "
        "Read it too.",
    )
    numbered(
        doc,
        "Stacked both into one background document: global on "
        "top, category file underneath.",
    )
    numbered(
        doc,
        "Answered the prompt using the combined context. Listed "
        "the three files in the current folder.",
    )
    para(
        doc,
        "Move to logistics/ and repeat. Only the global marker "
        "appears. The materials marker is gone because "
        "direct-materials/CLAUDE.md is in a sibling folder, not on "
        "the path up. That is the entire mechanism.",
    )

    # ===================================================================
    # 6. Worked example: the indirect brief
    # ===================================================================
    heading(doc, "6. Worked example: the indirect brief", 1)
    para(
        doc,
        "This is what the deliverable of Lesson 6 looks like for "
        "the indirect category. Same shape works for direct "
        "materials and logistics, just with different content and "
        "different files.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Course_02_The_Context_Architect/practice/\n"
        "├── CLAUDE.md                        (global, after Lesson 2)\n"
        "└── indirect/\n"
        "    ├── CLAUDE.md                    (category file, after "
        "Lessons 3 and 5)\n"
        "    ├── category_brief.md            (this is the output)\n"
        "    ├── vendors.csv                  (80 rows)\n"
        "    └── invoices.csv                 (3,000 rows, 18 violations)",
    )
    para(
        doc,
        "**The exact prompt to type after starting Claude Code in "
        "`indirect/`:**",
    )
    code_block(
        doc,
        "Build a category intelligence brief for this category.\n\n"
        "Inputs (use the data files my CLAUDE.md points at):\n"
        "- the master file (vendors.csv),\n"
        "- the activity file (invoices.csv).\n\n"
        "Action:\n"
        "1. Top 3 vendors by sum of amount_usd over the last year.\n"
        "2. One specific risk: an at-risk vendor, a contract ending "
        "in 90\n"
        "   days, or invoices that break the $25,000 approval rule.\n"
        "3. One concrete action with owner, action, and deadline.\n\n"
        "Output:\n"
        "Save as category_brief.md in this folder. Three sections:\n"
        "Top 3 (table), Risk (paragraph), Action (paragraph).\n"
        "Cap at 400 words plus an audit footer at the bottom.\n\n"
        "Constraints:\n"
        "- Use only files my CLAUDE.md points at.\n"
        "- Do not invent any vendor or figure.\n"
        "- Do not modify any data file.",
    )
    para(
        doc,
        "**What you should see (after about 60 seconds).** A "
        "400-word file at `indirect/category_brief.md`. Top 3 will "
        "be the largest vendors by total invoiced spend across 3,000 "
        "invoices: candidates include Helix Consulting, Bright Spark "
        "Energy, Apex Legal. Risk section will name the 18 invoices "
        "that broke the $25,000 approval rule (with one or two "
        "example invoice numbers) and VEN005 Prism Print as the "
        "at-risk vendor. Action: investigate the 18 violations, "
        "remediation memo by 2026-05-15. Audit footer at the bottom "
        "with timestamp, source files, model, your name.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the global from practice/CLAUDE.md and the category "
        "file from indirect/CLAUDE.md.",
    )
    numbered(
        doc,
        "Resolved 'the master file' to vendors.csv (per the category "
        "file) and 'the activity file' to invoices.csv.",
    )
    numbered(
        doc,
        "Read invoices.csv (all 3,000 rows). Summed amount_usd by "
        "vendor_id. Sorted descending. Took top 3.",
    )
    numbered(
        doc,
        "Joined vendor_ids back to vendor_name in vendors.csv.",
    )
    numbered(
        doc,
        "Filtered invoices.csv for the policy violation: amount_usd "
        ">= 25000 AND approval_path = 'manager_under_25k'. Found "
        "18 rows.",
    )
    numbered(
        doc,
        "Read vendors.csv. Found VEN005 flagged at_risk. Computed "
        "days-until-contract-end as 36 against today (2026-04-25).",
    )
    numbered(
        doc,
        "Wrote three sections, capped at 400 words, with audit "
        "footer below a horizontal rule.",
    )
    numbered(
        doc,
        "Saved only category_brief.md to the current folder. Did "
        "not modify the source CSVs.",
    )

    # ===================================================================
    # 7. A day in the life  (REAL WORKDAY, NOT course walkthrough)
    # ===================================================================
    heading(doc, "7. A day in the life: Anwar's Tuesday", 1)
    para(
        doc,
        "Anwar is a Senior Category Manager at a US manufacturing "
        "company. He manages direct materials, logistics, and "
        "indirect. He finished Course 2 last week and set up the "
        "CLAUDE.md stack for his real procurement portfolio. This "
        "is what an ordinary Tuesday looks like now.",
    )

    # 08:45
    heading(doc, "08:45. CPO deadline lands", 2)
    para(
        doc,
        "Anwar's CPO Slacks: \"Board pack goes to print Thursday. I "
        "need a one-page brief on each of your three categories by "
        "end of day Wednesday. Top suppliers by spend, any risks, "
        "and one action per category.\"",
    )
    para(
        doc,
        "Before the stack, this was a three-hour job per brief. "
        "Anwar opens his terminal.",
    )
    para(doc, "**The prompt Anwar types in Claude Code:**")
    code_block(
        doc,
        "cd ~/procurement/direct-materials\n"
        "claude\n\n"
        "> Build a category intelligence brief for this category.\n"
        "> Inputs: use the data files my CLAUDE.md points at.\n"
        "> Top 3 by spend, one risk, one action.\n"
        "> Save as category_brief.md. Cap at 400 words plus audit footer.",
    )
    para(
        doc,
        "**What Anwar sees.** In 60 seconds, Claude reads 2,500 "
        "order rows, aggregates by supplier, finds SUP004 Apex "
        "Electronics at risk (contract ends 2026-05-31), and saves "
        "a 400-word brief with audit footer. Anwar opens the file, "
        "changes one sentence in the action paragraph, and moves on.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the global (portfolio-level rules) and the "
        "direct-materials category file (scope, data file paths, "
        "at-risk flag).",
    )
    numbered(
        doc,
        "Read suppliers.csv (50 rows) and orders.csv (2,500 rows).",
    )
    numbered(
        doc,
        "Summed total_usd by supplier_id, joined to supplier_name, "
        "returned the top 3.",
    )
    numbered(
        doc,
        "Found SUP004 flagged at_risk with contract_end 36 days "
        "from today. Wrote the risk paragraph.",
    )
    numbered(
        doc,
        "Saved category_brief.md. Did not touch any CSV.",
    )
    para(
        doc,
        "Anwar repeats from logistics/ (Claude reads 5,000 "
        "shipments, finds CAR004 ParcelPlus at risk) and from "
        "indirect/ (Claude finds 18 approval violations across "
        "3,000 invoices). Three briefs in 20 minutes. Anwar "
        "spends 10 minutes reviewing, makes two small edits, "
        "and emails all three to the CPO before 09:30.",
    )
    para(
        doc,
        "**Time: 30 minutes.** Without the stack: 9 to 12 hours "
        "across three days.",
    )

    # 10:15
    heading(doc, "10:15. Data team updates the supplier list", 2)
    para(
        doc,
        "The data team Slacks: \"We added three new suppliers to "
        "direct materials. Updated CSV is in the shared folder.\"",
    )
    para(
        doc,
        "Anwar copies the new suppliers.csv into his "
        "direct-materials/ folder. He does not edit CLAUDE.md. The "
        "category file points at suppliers.csv by name, not by "
        "content. The next time Claude reads it, the new suppliers "
        "will be there.",
    )
    para(
        doc,
        "He runs a quick check to confirm:",
    )
    para(doc, "**The prompt Anwar types in Claude Code:**")
    code_block(
        doc,
        "cd ~/procurement/direct-materials\n"
        "claude\n\n"
        "> How many suppliers are in suppliers.csv now? List any new\n"
        "> ones added since the last reviewed date in my CLAUDE.md.",
    )
    para(
        doc,
        "**What Anwar sees.** Claude reports the updated row count "
        "and names the three new suppliers. The CLAUDE.md still "
        "says \"around 50 rows\", so Anwar updates that one number "
        "and the \"last reviewed\" date. Two minutes.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the category file. Noted the last reviewed date.",
    )
    numbered(
        doc,
        "Read suppliers.csv. Counted rows. Compared to the "
        "\"around 50 rows\" note in CLAUDE.md.",
    )
    numbered(
        doc,
        "Identified the new rows by checking which supplier_ids "
        "were not in the previously-expected range.",
    )

    # 11:00
    heading(doc, "11:00. CFO changes the approval threshold", 2)
    para(
        doc,
        "The CFO announces: \"Effective immediately, the approval "
        "threshold for indirect invoices drops from $25,000 to "
        "$15,000. Anything at $15,000 or above must use "
        "cfo_over_15k.\"",
    )
    para(
        doc,
        "Anwar opens indirect/CLAUDE.md in his editor. He changes "
        "the approval rule from $25,000 to $15,000 and updates "
        "\"cfo_over_25k\" to \"cfo_over_15k\". He saves. Four lines "
        "changed. One minute.",
    )
    para(
        doc,
        "He restarts Claude in indirect/ and runs the violation "
        "check:",
    )
    para(doc, "**The prompt Anwar types in Claude Code:**")
    code_block(
        doc,
        "cd ~/procurement/indirect\n"
        "claude\n\n"
        "> Find every invoice in invoices.csv that breaks the\n"
        "> approval rule stated in my CLAUDE.md. Show invoice\n"
        "> number, vendor, amount, and approval path. Cap at 30 rows.",
    )
    para(
        doc,
        "**What Anwar sees.** More violations now, because the "
        "threshold dropped. Claude finds every invoice at $15,000 "
        "or above that used the wrong approval path. Anwar sends "
        "the list to the CFO's office.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the updated indirect/CLAUDE.md. Parsed the new "
        "$15,000 threshold.",
    )
    numbered(
        doc,
        "Read all 3,000 invoice rows. Filtered for amount_usd "
        ">= 15000 AND approval_path != 'cfo_over_15k'.",
    )
    numbered(
        doc,
        "Joined vendor_ids to vendor names. Returned the violations "
        "sorted by amount descending.",
    )

    # 14:00
    heading(doc, "14:00. Onboarding a new colleague", 2)
    para(
        doc,
        "A new analyst joins the team. Instead of walking her "
        "through prompts for half a day, Anwar shares the project "
        "folder. It contains the global, the three category files, "
        "and the saved prompt template.",
    )
    para(
        doc,
        "He tells her: \"cd into any category folder, start Claude, "
        "and paste the brief prompt. The right context loads "
        "automatically.\" She runs the five-question test (from "
        "Lesson 4) in each folder and confirms the stack works.",
    )
    para(doc, "**The prompt the new analyst types in Claude Code:**")
    code_block(
        doc,
        "cd ~/procurement/direct-materials\n"
        "claude\n\n"
        "> Answer these five questions using only the CLAUDE.md\n"
        "> context loaded in this session. Do not read any data file.\n"
        "> 1. What is my role at the portfolio level?\n"
        "> 2. What is the scope of this folder?\n"
        "> 3. What data files live in this folder?\n"
        "> 4. What at-risk entity is in this category?\n"
        "> 5. What rules apply only in this category?",
    )
    para(
        doc,
        "**What she sees.** The same answers Anwar would get. The "
        "stack is portable. Onboarding: 30 minutes instead of "
        "half a day.",
    )

    # 16:00
    heading(doc, "16:00. Preparing for a supplier meeting", 2)
    para(
        doc,
        "Anwar has a call with Great Lakes Steel tomorrow at 10:00. "
        "He needs a one-page supplier profile: annual spend, order "
        "volume, contract status, and any open risks.",
    )
    para(doc, "**The prompt Anwar types in Claude Code:**")
    code_block(
        doc,
        "cd ~/procurement/direct-materials\n"
        "claude\n\n"
        "> Write a one-page supplier profile for Great Lakes Steel.\n"
        "> Include: annual spend from orders.csv, number of POs,\n"
        "> contract status from suppliers.csv, and any risk flags.\n"
        "> Save as great_lakes_steel_profile.md.",
    )
    para(
        doc,
        "**What Anwar sees.** A one-page profile. Annual spend: "
        "$2,400,000 across 127 POs. Contract status: active, ends "
        "2027-01-31. No risk flags. Anwar reviews it in two "
        "minutes and saves it for the meeting.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the global and direct-materials category file.",
    )
    numbered(
        doc,
        "Read suppliers.csv. Found Great Lakes Steel (SUP001). "
        "Extracted contract_end and status.",
    )
    numbered(
        doc,
        "Read orders.csv (2,500 rows). Filtered for supplier_id = "
        "SUP001. Summed total_usd. Counted POs.",
    )
    numbered(
        doc,
        "Wrote a one-page profile with the figures. Saved to the "
        "current folder.",
    )
    para(
        doc,
        "**End of Anwar's Tuesday.** Five procurement tasks "
        "completed, all powered by the same CLAUDE.md stack. Total "
        "active time with Claude: about 50 minutes. Without the "
        "stack, this workload would have filled two days.",
    )

    # ===================================================================
    # 8. The 20-minute sprint
    # ===================================================================
    heading(doc, "8. The 20-minute sprint: a quick taste", 1)
    para(
        doc,
        "If you only have 20 minutes today, do this. You will not "
        "finish the course but you will see the stacking work end "
        "to end with one category. Pick direct materials.",
    )

    heading(doc, "Minutes 0 to 5: see the starter state", 2)
    numbered(doc, "Open the course folder.")
    numbered(
        doc,
        "Open `practice/CLAUDE.md`. Read it. Three weak generic "
        "lines.",
    )
    numbered(
        doc,
        "Open `practice/direct-materials/CLAUDE.md`. A stub.",
    )
    numbered(
        doc,
        "Open `practice/direct-materials/suppliers.csv` (in Excel "
        "or any editor). Skim the columns. 50 suppliers.",
    )

    heading(doc, "Minutes 5 to 10: write a quick global and a quick category file", 2)
    numbered(
        doc,
        "Open `solutions/global_CLAUDE_md.md`. Copy the writing "
        "rules block. Paste into your global. That alone is enough "
        "for the sprint.",
    )
    numbered(
        doc,
        "Open `solutions/direct_materials_CLAUDE_md.md`. Copy the "
        "Files section. Paste into your "
        "direct-materials/CLAUDE.md.",
    )
    numbered(doc, "Save both.")

    heading(doc, "Minutes 10 to 15: run a real spend prompt", 2)
    numbered(doc, "Open your terminal. Type:")
    code_block(
        doc,
        'cd "Course_02_The_Context_Architect/practice/direct-materials"\n'
        "claude",
    )
    numbered(doc, "Once Claude starts, type the prompt:")
    code_block(
        doc,
        "List my top 10 suppliers by total spend across all orders. Sum\n"
        "total_usd from orders.csv, group by supplier_id, join supplier_name\n"
        "from suppliers.csv. Show the figure for each.",
    )
    numbered(
        doc,
        "Wait 30 seconds while Claude reads 2,500 order rows. You "
        "should see ten rows with Great Lakes Steel, Heartland "
        "Steel, and Pacific Aluminum near the top.",
    )

    heading(doc, "Minutes 15 to 20: prove the stacking works", 2)
    numbered(
        doc,
        "Quit Claude (`/quit`). Move to logistics:",
    )
    code_block(doc, "cd ../logistics\nclaude")
    numbered(doc, "Run the same kind of prompt:")
    code_block(
        doc,
        "List my top 10 carriers by total spend across all shipments.\n"
        "Sum total_usd from shipments.csv, group by carrier_id, join\n"
        "carrier_name from carriers.csv.",
    )
    numbered(
        doc,
        "Now you see carrier names: Globex Freight, Atlantic Lines, "
        "etc. Same prompt shape, completely different output, "
        "because Claude read a different CLAUDE.md (which pointed "
        "at different CSVs) when you started in this folder.",
    )

    para(
        doc,
        "After this sprint, you have proven the stacking works on "
        "real data with thousands of rows. The remaining lessons are "
        "about doing it properly: complete CLAUDE.md files, the "
        "test, and the three-brief deliverable.",
    )

    # ===================================================================
    # 9. Your first week (with terminal examples)
    # ===================================================================
    heading(doc, "9. Your first week with the stack in your real work", 1)
    para(
        doc,
        "After Course 2, you take the pattern into your own real "
        "procurement folder.",
    )

    heading(doc, "Day 1 (Monday): build your real global", 2)
    bullet(doc, "**Goal:** a global CLAUDE.md for your real portfolio.")
    bullet(
        doc,
        "**Tasks:** create a project folder for your portfolio. Add "
        "three subfolders (one per category you manage). Write a "
        "global CLAUDE.md at the root with three sections: Who I am, "
        "Folder rules, Writing rules. Keep it under 40 lines.",
    )
    bullet(doc, "**Time:** 30 minutes.")
    para(doc, "**Example: the command to create the folder structure.**")
    code_block(
        doc,
        "mkdir -p ~/procurement/{direct-materials,logistics,indirect}\n"
        "# Then create CLAUDE.md at ~/procurement/ in your editor.",
    )

    heading(doc, "Day 2 (Tuesday): one real category file", 2)
    bullet(
        doc,
        "**Goal:** the category file for your highest-volume category.",
    )
    bullet(
        doc,
        "**Tasks:** pick one category folder. Copy your real CSVs "
        "into it. Write the category CLAUDE.md with three sections "
        "(scope, files, rules). Use the course solution as a model.",
    )
    bullet(doc, "**Time:** 60 minutes.")
    para(doc, "**Example: testing the file after you write it.**")
    code_block(
        doc,
        "cd ~/procurement/direct-materials\n"
        "claude\n\n"
        "> What data files do I have here? Read each one and tell me\n"
        "> the row count and column headers.",
    )
    para(
        doc,
        "If Claude names the right files and the right columns, "
        "your category file is working.",
    )

    heading(doc, "Day 3 (Wednesday): the rest of the category files", 2)
    bullet(
        doc,
        "**Goal:** category files for the rest of your categories.",
    )
    bullet(
        doc,
        "**Tasks:** repeat Tuesday for each. Each one takes 30 to "
        "45 minutes once you have the pattern.",
    )
    bullet(doc, "**Time:** 90 minutes.")

    heading(doc, "Day 4 (Thursday): the test and the file references", 2)
    bullet(doc, "**Goal:** hierarchy test passes everywhere.")
    bullet(
        doc,
        "**Tasks:** save your five-question test prompt at the "
        "project root. Run it from each category. Add 'last "
        "reviewed' lines to every category file.",
    )
    bullet(doc, "**Time:** 60 minutes.")
    para(doc, "**Example: running the test from each folder.**")
    code_block(
        doc,
        "cd ~/procurement/direct-materials\n"
        "claude\n\n"
        "> Answer these five questions using only the CLAUDE.md\n"
        "> context loaded in this session:\n"
        "> 1. What is my role?\n"
        "> 2. What is the scope of this folder?\n"
        "> 3. What data files live here?\n"
        "> 4. What at-risk entity is in this category?\n"
        "> 5. What rules apply only here?",
    )
    para(
        doc,
        "Repeat from logistics/ and indirect/. Question 1 should "
        "match everywhere. Questions 2 to 5 should differ.",
    )

    heading(doc, "Day 5 (Friday): your first real brief", 2)
    bullet(
        doc,
        "**Goal:** a real category brief from the saved prompt.",
    )
    bullet(
        doc,
        "**Tasks:** save the brief prompt as a Markdown file. Run "
        "it from each category. Three real briefs land. Send the "
        "most important to your CPO.",
    )
    bullet(doc, "**Time:** 90 minutes.")
    para(doc, "**Example: generating three briefs in sequence.**")
    code_block(
        doc,
        "cd ~/procurement/direct-materials\n"
        "claude\n"
        "# Paste the brief prompt. Wait 60 seconds. /quit\n\n"
        "cd ../logistics\n"
        "claude\n"
        "# Same prompt. /quit\n\n"
        "cd ../indirect\n"
        "claude\n"
        "# Same prompt. /quit",
    )
    para(
        doc,
        "Three brief files appear, one per folder. Same shape, "
        "completely different content. Send the most urgent to "
        "your CPO and keep the others for the board pack.",
    )

    # ===================================================================
    # 10. Personalization pattern (with terminal examples)
    # ===================================================================
    heading(doc, "10. The pattern: short shared files, not one big one", 1)
    para(
        doc,
        "What you build in this course is the procurement equivalent "
        "of the Cowork ABOUT ME pattern from the foundation course. "
        "Where Cowork splits context into four files (about-me, "
        "anti-ai-writing-style, my-company, procurement-standards), "
        "Claude Code (in the terminal) in a multi-category project "
        "splits it into one global plus one file per category folder.",
    )
    para(doc, "What goes where, in plain words:")
    bullet(
        doc,
        "**Global CLAUDE.md** at the project root. Universal stuff. "
        "About 25 to 40 lines.",
    )
    bullet(
        doc,
        "**Category CLAUDE.md** in each subfolder. "
        "Category-specific. About 20 to 35 lines.",
    )
    bullet(
        doc,
        "**Personal CLAUDE.md** at `~/.claude/CLAUDE.md` (optional). "
        "Your own preferences across every project.",
    )

    heading(doc, "Checking the stack in Claude Code", 2)
    para(
        doc,
        "After you set up the stack, you can ask Claude Code to "
        "confirm what it loaded:",
    )
    para(doc, "**The prompt you type in the terminal:**")
    code_block(
        doc,
        "cd ~/procurement/direct-materials\n"
        "claude\n\n"
        "> List every CLAUDE.md file you loaded for this session,\n"
        "> in order. For each one, summarize what it tells you\n"
        "> in one sentence.",
    )
    para(
        doc,
        "**What you should see.** Claude lists the global first "
        "(\"Senior Category Lead at Acme Inc, three categories, "
        "$5.4m cost reduction program\") and then the category "
        "file (\"Direct materials: 50 suppliers, SUP004 at risk, "
        "points at suppliers.csv and orders.csv\").",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(
        doc,
        "Walked up from direct-materials/ to the project root, "
        "collecting every CLAUDE.md on the path.",
    )
    numbered(
        doc,
        "Listed them in load order (global first, category second).",
    )
    numbered(
        doc,
        "Summarized each from the actual content loaded into the "
        "session.",
    )
    para(
        doc,
        "When you ship the project to a colleague, they get the "
        "global and the category files automatically. They run the "
        "same prompt, they get the same kind of output. Their "
        "personal preferences come from their own user-level file.",
    )

    # ===================================================================
    # 11. Quick reference and troubleshooting
    # ===================================================================
    heading(doc, "11. Quick reference and troubleshooting", 1)

    heading(doc, "Things to remember", 2)
    bullet(
        doc,
        "Start Claude in the specific category folder, not the "
        "project root, when you want category context.",
    )
    bullet(
        doc,
        "CLAUDE.md is loaded once at session start. Edits during "
        "a session do not apply until you restart with `/quit` and "
        "`claude`.",
    )
    bullet(
        doc,
        "The global stays under 40 lines. Each category file stays "
        "under 35.",
    )
    bullet(
        doc,
        "Run the five-question test (Lesson 4) any time you change "
        "a CLAUDE.md.",
    )
    bullet(
        doc,
        "One prompt, three folders, three correctly scoped briefs. "
        "That is the deliverable.",
    )

    heading(doc, "Common problems and the matching fix", 2)
    bullet(
        doc,
        "**Symptom:** the brief mentions a vendor when you are in "
        "direct materials. **Fix:** restart Claude. The previous "
        "session is leaking.",
    )
    bullet(
        doc,
        "**Symptom:** Claude cannot find a CSV. **Fix:** check the "
        "path in your category file. Paths inside a category "
        "CLAUDE.md are relative to that folder. Just `suppliers.csv`, "
        "not `direct-materials/suppliers.csv` and not "
        "`data/suppliers.csv` (there is no data subfolder).",
    )
    bullet(
        doc,
        "**Symptom:** Claude is slow on every reply. **Fix:** the "
        "global is too long. Trim back to 25 to 40 lines.",
    )
    bullet(
        doc,
        "**Symptom:** the test passes but the brief still mixes "
        "content. **Fix:** the issue is the prompt, not the stack. "
        "Use the prompt from "
        "`solutions/category_intelligence_brief_command.md`.",
    )
    bullet(
        doc,
        "**Symptom:** Claude invented a supplier name. **Fix:** "
        "the constraint 'do not name any entity not in the master "
        "file' was missing. Re-paste with it visible.",
    )
    bullet(
        doc,
        "**Symptom:** Claude says the CSV has a different number "
        "of rows than CLAUDE.md says. **Fix:** the CSV grew or "
        "shrank since you last reviewed. Update the column line "
        "and the 'last reviewed' date.",
    )

    # ===================================================================
    # 12. Done
    # ===================================================================
    heading(doc, "12. You are done with Course 2 when", 1)
    numbered(
        doc,
        "Your global CLAUDE.md is between 25 and 40 lines and "
        "holds only universal context.",
    )
    numbered(
        doc,
        "Each of your three category files is 20 to 35 lines and "
        "has the three sections.",
    )
    numbered(
        doc,
        "The five-question test passes from every category folder.",
    )
    numbered(
        doc,
        "One prompt run from each category folder produces three "
        "correctly scoped briefs.",
    )
    numbered(
        doc,
        "Three brief files exist: direct-materials/category_brief.md, "
        "logistics/category_brief.md, indirect/category_brief.md.",
    )
    numbered(
        doc,
        "You can explain in two sentences how Claude reads CLAUDE.md "
        "and why a stack of files beats one big file.",
    )
    para(
        doc,
        "When all six are true, move to Course 3 (The Skill Builder). "
        "The stack you built in Course 2 is the foundation for every "
        "later course.",
    )

    doc.save(str(OUTPUT_PATH))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
