"""
Generate Course 10: The Negotiation Intelligence System Handout (.docx).
Run from repo root: python scripts/build_course_10_handout.py
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

OUTPATH = (
    Path(__file__).resolve().parent.parent
    / "Handouts"
    / "Course_10_The_Negotiation_Intelligence_System_Handout.docx"
)


def set_cell_shading(cell, color_hex):
    """Set background shading on a table cell."""
    shading = cell._element.get_or_add_tcPr()
    shd = shading.makeelement(
        qn("w:shd"),
        {
            qn("w:val"): "clear",
            qn("w:color"): "auto",
            qn("w:fill"): color_hex,
        },
    )
    shading.append(shd)


def style_doc(doc):
    """Configure base styles."""
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    pf = style.paragraph_format
    pf.space_after = Pt(6)
    pf.space_before = Pt(0)

    for level in range(1, 4):
        hs = doc.styles[f"Heading {level}"]
        hf = hs.font
        hf.name = "Calibri"
        hf.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
        hf.bold = True
        if level == 1:
            hf.size = Pt(20)
            hs.paragraph_format.space_before = Pt(18)
            hs.paragraph_format.space_after = Pt(8)
        elif level == 2:
            hf.size = Pt(15)
            hs.paragraph_format.space_before = Pt(14)
            hs.paragraph_format.space_after = Pt(6)
        else:
            hf.size = Pt(12)
            hs.paragraph_format.space_before = Pt(10)
            hs.paragraph_format.space_after = Pt(4)


def add_para(doc, text, style="Normal", bold=False, italic=False, size=None, space_after=None):
    p = doc.add_paragraph(text, style=style)
    if bold or italic or size:
        for run in p.runs:
            if bold:
                run.bold = True
            if italic:
                run.italic = True
            if size:
                run.font.size = Pt(size)
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def add_code_block(doc, text):
    """Add a code-style paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.3)
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    # Light grey background via shading
    shd = p._element.get_or_add_pPr().makeelement(
        qn("w:shd"),
        {qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): "F2F2F2"},
    )
    p._element.get_or_add_pPr().append(shd)
    return p


def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
        p.add_run(text)
    else:
        p.add_run(text)
    return p


def add_table(doc, headers, rows, col_widths=None):
    """Add a formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.style = "Table Grid"
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for par in cell.paragraphs:
            for run in par.runs:
                run.bold = True
                run.font.size = Pt(10)
                run.font.name = "Calibri"
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(cell, "1B3A5C")
    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(10)
                    run.font.name = "Calibri"
            if r_idx % 2 == 1:
                set_cell_shading(cell, "F0F4F8")
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()  # spacer
    return table


def build():
    doc = Document()
    style_doc(doc)

    # Set narrow margins
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # =========================================================================
    # HEADER
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("U2xAI  |  PROCUREAI ACADEMY")
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    r.font.name = "Calibri"
    r.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Course 10: The Negotiation Intelligence System")
    r.font.size = Pt(24)
    r.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
    r.font.name = "Calibri"
    r.bold = True
    p.paragraph_format.space_after = Pt(2)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Comprehensive Handout  |  Claude Code (in the terminal)")
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    r.font.name = "Calibri"
    p.paragraph_format.space_after = Pt(2)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Date: 2026-04-26  |  Version 1.0")
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
    r.font.name = "Calibri"
    p.paragraph_format.space_after = Pt(20)

    # =========================================================================
    # 1. HOW TO USE THIS HANDOUT
    # =========================================================================
    doc.add_heading("How to use this handout", level=1)

    add_para(doc, (
        "This handout is the reference companion for Course 10: The Negotiation Intelligence System. "
        "It covers every concept, prompt, folder layout, and troubleshooting tip from the six course lessons. "
        "Keep it open while you work through the course. Return to it afterwards when you apply the same "
        "patterns to a real supplier negotiation."
    ))
    add_para(doc, (
        "The handout follows a natural workflow progression. It starts with the problem, moves through the "
        "system components, shows worked examples you can copy, walks through a full day of negotiation "
        "preparation, and closes with a week-long adoption plan. Every section includes at least one "
        "Claude Code (in the terminal) example: the prompt you type, the command you run, and the output "
        "you should see."
    ))
    add_para(doc, (
        "All prompts in this handout are written for Claude Code (in the terminal). They do not work "
        "in Claude AI Web (claude.ai in a browser) or Claude Desktop with Cowork unless noted otherwise. "
        "Claude Code reads local files, writes output to local folders, runs sub-agents, and executes "
        "hooks. Those features are terminal-only."
    ))

    # =========================================================================
    # 2. WHAT THIS COURSE TEACHES
    # =========================================================================
    doc.add_heading("What this course teaches", level=1)

    add_para(doc, (
        "A supplier sends a renewal proposal with a 12% price increase, a narrowed force majeure clause, "
        "and a shortened notice period. The contract is worth $9.2M per year. The face-to-face negotiation "
        "is in 12 days. Your VP wants a pre-negotiation brief by Friday. You need to gather market intelligence, "
        "cost every proposed deviation, write the brief, draft a counter-proposal, and capture the outcome "
        "after the negotiation closes. Normally, this takes two analysts a full week."
    ))
    add_para(doc, (
        "This course teaches you to build a composition system in Claude Code (in the terminal) that does the "
        "analyst work. Sub-agents gather intelligence in parallel. A hook costs every deviation automatically. "
        "A slash command generates the pre-negotiation brief. A second command drafts the counter-proposal. "
        "A third command captures the outcome after the deal closes. Total analyst time saved: roughly "
        "35 hours per negotiation cycle."
    ))
    add_para(doc, (
        "The scenario is realistic. TransGlobal Industries ($340M annual procurement spend) is negotiating "
        "the renewal of contract CTR-2024-LG-001 with Redline Logistics LLC, based in Indianapolis, IN. "
        "Redline handles warehousing, last-mile delivery, and cross-dock operations across four US "
        "distribution centers (Chicago, Dallas, Atlanta, and Phoenix). The current annual value is $9.2M. "
        "The renewal deadline is 2026-05-07."
    ))

    add_para(doc, (
        "The course has six parts, each building one component of the system. You start by mapping "
        "the negotiation workflow to Claude Code components. Then you gather intelligence with parallel "
        "sub-agents. Next, you build the PostToolUse hook for deviation costing and the PreToolUse "
        "hook for brief completeness. After that, you create the /counter-proposal slash command and "
        "the /post-close slash command for outcome capture and archiving. Total course time is about "
        "5.5 hours, comfortable in two afternoon sessions."
    ))

    doc.add_heading("What you will have built by the end", level=2)

    add_para(doc, (
        "By the end of the course, your project folder contains a complete, reusable negotiation "
        "intelligence system. The system design map shows each component and how they connect. "
        "Three parallel sub-agents produce an intelligence brief covering market rates, supplier "
        "performance, and contract term analysis. The PostToolUse hook automatically costs every "
        "deviation when Claude Code (in the terminal) writes a deviation analysis. The PreToolUse "
        "hook blocks the pre-negotiation brief from saving until BATNA and walk-away price are "
        "both present. The /counter-proposal command generates the negotiation document from the "
        "approved brief. The /post-close command records the outcome, writes lessons learned, "
        "and archives all working files."
    ))

    # =========================================================================
    # 3. WHAT IS IN THE COURSE FOLDER
    # =========================================================================
    doc.add_heading("What is in the course folder", level=1)

    add_para(doc, (
        "The course folder is self-contained. Everything you need is inside it. No external downloads, "
        "no shared drives, no APIs. Open the folder, start Claude Code (in the terminal), and begin."
    ))

    add_code_block(doc, (
        "Course_10_The_Negotiation_Intelligence_System/\n"
        "  practice/\n"
        "    CLAUDE.md                    (contract context, supplier profile, rules)\n"
        "    data/                        (source files, read-only)\n"
        "      current-contract.md        (active MSA terms)\n"
        "      proposed-renewal.md        (supplier's renewal proposal)\n"
        "      supplier-performance.csv   (24 months of KPIs)\n"
        "      market-benchmarks.md       (US logistics market rates)\n"
        "      negotiation-history.csv    (8 past negotiation outcomes)\n"
        "    Outputs/                     (all generated files go here)\n"
        "    scripts/                     (hook scripts you build)\n"
        "    .claude/\n"
        "      settings.json              (hook registrations)\n"
        "      commands/                  (slash command definitions)\n"
        "  lessons/                       (6 lesson files, in order)\n"
        "  solutions/                     (reference answers)\n"
        "  scripts/                       (data regeneration script)"
    ))

    add_para(doc, (
        'Why this matters. The data/ folder is read-only. Every prompt you type starts with that rule: '
        '"Do not edit any file in data/." This protects your source documents from accidental edits. '
        "All Claude Code (in the terminal) output goes to Outputs/. If something goes wrong, you can delete "
        "Outputs/ and start fresh without touching the source data. If your practice data gets corrupted, "
        "run the regeneration script in scripts/ and everything resets."
    ))

    # Subfolder explanations
    doc.add_heading("Key folders and files", level=2)

    add_para(doc, (
        "CLAUDE.md sits at the practice root. It tells Claude Code (in the terminal) your role (Senior "
        "Category Manager), the supplier name (Redline Logistics LLC), the contract value ($9.2M), "
        "the renewal deadline (2026-05-07), and the output standards (USD, YYYY-MM-DD dates, short "
        "sentences, no dashes, three recommendations max). Every session reads this file automatically."
    ))
    add_para(doc, (
        "Why this matters. Without CLAUDE.md, Claude produces generic output. With it, every output uses "
        "TransGlobal's context, names Redline Logistics LLC, cites the $9.2M value, and follows your "
        "formatting rules. You write CLAUDE.md once. It applies to every prompt in the session."
    ))

    add_para(doc, (
        "data/ holds five source files. The current contract contains the active MSA terms: pricing at "
        "$9.2M/year, a 96% on-time delivery SLA target, a 180-day notice period, and a broad force "
        "majeure clause. The proposed renewal contains Redline's three changes. The performance CSV "
        "covers 24 months of monthly KPIs. The market benchmarks file shows US logistics rate ranges. "
        "The negotiation history CSV records eight past outcomes."
    ))
    add_para(doc, (
        "Why this matters. Real negotiation prep depends on the quality of the source data. Five files "
        "give Claude Code (in the terminal) enough context to produce intelligence that would otherwise "
        "take an analyst two to three days to assemble manually. Without these files, every prompt "
        "would need to include the data inline, which is slow and error-prone."
    ))

    add_para(doc, (
        "Outputs/ is where every generated file lands. By the end of the course, it holds: "
        "system-design.md, intelligence-brief.md, deviation-costs.md, pre-negotiation-brief.md, "
        "counter-proposal.md, post-close-capture.md, negotiation-log.csv, and an archive subfolder."
    ))
    add_para(doc, (
        "Why this matters. A single output folder means you always know where to look. Your VP asks "
        'for the brief? It is in Outputs/. Legal needs the counter-proposal? Outputs/. The next '
        "category manager inherits the negotiation? Point them to the archive subfolder."
    ))

    # =========================================================================
    # 4. TIME SAVINGS TABLE
    # =========================================================================
    doc.add_heading("Time savings reference", level=1)

    add_para(doc, (
        "The table below compares five negotiation preparation tasks with and without Claude Code "
        "(in the terminal). Times are based on the Redline Logistics LLC scenario: a $9.2M contract, "
        "three proposed deviations, five source files, and a 12-day preparation window."
    ))

    add_table(doc,
        ["Task", "Without Claude Code", "With Claude Code", "Time saved"],
        [
            ["Gather market intelligence, supplier performance, and terms risk",
             "12 to 16 hours (manual research, spreadsheet analysis, document review)",
             "25 minutes (three parallel sub-agents, one merge prompt)",
             "14.5 hours"],
            ["Cost every proposed deviation in USD",
             "3 to 4 hours (line-by-line contract comparison, finance consultation)",
             "15 minutes (one prompt plus automatic hook validation)",
             "3.5 hours"],
            ["Write the pre-negotiation brief with BATNA and walk-away price",
             "4 to 6 hours (draft, review cycle, completeness check by hand)",
             "20 minutes (one prompt, automatic completeness gate)",
             "5 hours"],
            ["Draft the counter-proposal document",
             "3 to 4 hours (draft in Word, cross-reference brief and costs)",
             "10 minutes (one slash command, automatic generation)",
             "3.5 hours"],
            ["Capture the negotiation outcome and archive working files",
             "1 to 2 hours (fill template, copy files, update log by hand)",
             "8 minutes (one slash command, automatic log and archive)",
             "1.5 hours"],
        ],
        col_widths=[2.2, 2.0, 2.0, 0.9],
    )

    add_para(doc, (
        "Total: roughly 28 hours of analyst work compressed to about 78 minutes of Claude Code "
        "(in the terminal) interaction. For a team that runs 8 to 12 supplier negotiations per year, "
        "that is 220 to 330 hours returned to strategic work annually."
    ))

    # =========================================================================
    # 5. WHAT A NEGOTIATION INTELLIGENCE SYSTEM IS
    # =========================================================================
    doc.add_heading("What a negotiation intelligence system is", level=1)

    add_para(doc, (
        "A negotiation intelligence system is a set of Claude Code (in the terminal) components wired "
        "together to handle the full lifecycle of a supplier negotiation: from receiving the proposal "
        "to capturing the outcome. Each component has one job. Together, they form a repeatable pipeline "
        "that any category manager on your team can run."
    ))

    add_para(doc, "The system has six components:")

    add_table(doc,
        ["Component", "Type", "What it does"],
        [
            ["System design map", "CLAUDE.md + Outputs/", "Maps each negotiation stage to a Claude Code component, its inputs, and its outputs"],
            ["Intelligence gathering", "Sub-agents (parallel)", "Three sub-agents run at the same time: one analyzes supplier performance, one benchmarks market rates, one assesses contract term risk"],
            ["Deviation costing", "PostToolUse hook", "A Python script fires automatically after every write to deviation-costs.md and checks that every row has a USD cost figure"],
            ["Pre-negotiation brief", "PreToolUse hook", "A Python script fires before every write to pre-negotiation-brief.md and blocks the save if BATNA or walk-away price is missing"],
            ["Counter-proposal", "Slash command", "Typing /counter-proposal generates the full counter-proposal from the approved brief, deviation costs, and negotiation history"],
            ["Post-close capture", "Slash command", "Typing /post-close records the negotiation outcome, writes lessons learned, and archives all working files"],
        ],
        col_widths=[1.5, 1.2, 4.4],
    )

    add_para(doc, (
        "Why this matters. Without a system, negotiation prep is a collection of ad hoc tasks. Each "
        "person does them differently. Some forget the BATNA. Some skip the market benchmarks. Some "
        "never record the outcome. With a system, every negotiation follows the same pipeline. The "
        "hooks enforce quality. The commands enforce completeness. The archive preserves institutional "
        "knowledge for the next negotiation."
    ))

    doc.add_heading("The mental model: pipeline, not checklist", level=2)

    add_para(doc, (
        "Think of the system as a pipeline with five stages. Data flows in one direction: from source "
        "files through intelligence gathering, through deviation costing, through the brief, through "
        "the counter-proposal, and into the post-close archive. Each stage reads the output of the "
        "previous stage. No stage edits the source files."
    ))

    add_code_block(doc, (
        "data/ (read-only)\n"
        "  --> Sub-agents --> Outputs/intelligence-brief.md\n"
        "  --> Hook --> Outputs/deviation-costs.md\n"
        "  --> Hook --> Outputs/pre-negotiation-brief.md\n"
        "  --> Command --> Outputs/counter-proposal.md\n"
        "  --> Command --> Outputs/post-close-capture.md + archive/"
    ))

    add_para(doc, (
        "Why this matters. A pipeline gives you traceability. If the counter-proposal has a wrong figure, "
        "you trace it back through the brief, through the deviation costs, to the source file. You fix "
        "it in one place and regenerate. A checklist gives you no traceability. You fix it everywhere "
        "by hand."
    ))

    doc.add_heading("How the components talk to each other", level=2)

    add_para(doc, (
        "Each component in the system communicates through files in Outputs/. Sub-agents write three "
        "analysis files. The merge prompt reads those three files and writes the intelligence brief. "
        "The deviation costing prompt reads the source contracts and writes the deviation table. The "
        "pre-negotiation brief prompt reads the intelligence brief and the deviation table and writes "
        "the brief. The /counter-proposal command reads the brief, the deviation table, and the "
        "negotiation history and writes the counter-proposal. The /post-close command reads the "
        "counter-proposal and the deviation table and writes the capture document and log row."
    ))
    add_para(doc, (
        "No component modifies the output of a previous component. Each reads and produces. This "
        "makes the system safe to rerun. If the deviation costs change because you updated an "
        "assumption, you rerun the brief prompt and the /counter-proposal command. The pipeline "
        "flows forward. Nothing flows backward."
    ))
    add_para(doc, (
        "Why this matters. In a manual workflow, updating one figure means searching through three "
        "or four documents to find every place it appears. In the pipeline, you update the figure "
        "in the source, rerun the downstream prompts, and every document updates consistently. "
        "This is especially important when your VP changes the walk-away price at the last minute "
        "and you need the counter-proposal updated in ten minutes, not two hours."
    ))

    # =========================================================================
    # 6. WORKED EXAMPLES
    # =========================================================================
    doc.add_heading("Worked examples", level=1)

    # --- Worked Example 1: Intelligence Gathering ---
    doc.add_heading("Worked example 1: Gathering intelligence with parallel sub-agents", level=2)

    add_para(doc, (
        "You need three pieces of intelligence before you can write the negotiation brief: "
        "how Redline Logistics LLC has performed against its SLAs, where their proposed pricing "
        "sits relative to the US logistics market, and what risk the changed contract terms create. "
        "Each piece is independent. Claude Code (in the terminal) can run all three at the same time "
        "using sub-agents."
    ))

    doc.add_heading("The prompt to type", level=3)
    add_code_block(doc, (
        'Run three sub-agents in parallel.\n\n'
        'Sub-agent 1: Read data/supplier-performance.csv and data/current-contract.md.\n'
        'Calculate monthly on-time delivery, damage rate, and SLA compliance for all\n'
        '24 months. Compare the last 6 months to the prior 6 months. Write findings\n'
        'to Outputs/performance-analysis.md with a summary table and a three-sentence\n'
        'conclusion naming Redline Logistics LLC and the 96.0% SLA target.\n\n'
        'Sub-agent 2: Read data/market-benchmarks.md and data/proposed-renewal.md.\n'
        'Compare Redline\'s proposed rates to the US market range for Midwest and\n'
        'Southeast corridors. Write findings to Outputs/market-analysis.md with a\n'
        'comparison table and a three-sentence conclusion.\n\n'
        'Sub-agent 3: Read data/current-contract.md and data/proposed-renewal.md.\n'
        'Assess the risk exposure from each of the three changed terms. Write findings\n'
        'to Outputs/terms-risk-analysis.md with a risk table and a three-sentence\n'
        'conclusion.\n\n'
        'After all three finish, merge the results into Outputs/intelligence-brief.md\n'
        'with an executive summary naming Redline Logistics LLC, $9.2M, and 2026-05-07.'
    ))

    doc.add_heading("The folder layout", level=3)
    add_code_block(doc, (
        "practice/\n"
        "  data/\n"
        "    current-contract.md\n"
        "    proposed-renewal.md\n"
        "    supplier-performance.csv\n"
        "    market-benchmarks.md\n"
        "  Outputs/\n"
        "    system-design.md              (from Lesson 1)"
    ))

    doc.add_heading("What you should see", level=3)
    add_para(doc, (
        "Claude Code (in the terminal) launches three sub-agents. Each reads its assigned files and "
        "writes its output to Outputs/. After all three complete, Claude merges the results into "
        "Outputs/intelligence-brief.md. The executive summary names Redline Logistics LLC, states the "
        "$9.2M contract value, includes the 2026-05-07 deadline, and gives a clear negotiation "
        "recommendation. The whole process takes two to four minutes."
    ))

    doc.add_heading("What Claude did, behind the scenes", level=3)
    add_para(doc, (
        "1. Claude Code (in the terminal) parsed the prompt and identified three independent tasks. "
        "Because none depended on another's output, it launched all three sub-agents in parallel."
    ))
    add_para(doc, (
        "2. Sub-agent 1 loaded supplier-performance.csv, grouped the 24 rows by month, calculated "
        "the on-time delivery rate for each month, identified four months below 95%, and computed "
        "the six-month average decline from 96.8% to 93.1%."
    ))
    add_para(doc, (
        "3. Sub-agent 2 loaded market-benchmarks.md, extracted the rate range for Midwest and "
        "Southeast corridors, loaded proposed-renewal.md, extracted Redline's proposed rates, "
        "and calculated that Redline's proposal sits 8% above the market median."
    ))
    add_para(doc, (
        "4. Sub-agent 3 loaded both contract files, identified the three changed terms, and assessed "
        "each: the force majeure narrowing creates unquantified disruption exposure, the notice period "
        "cut leaves insufficient time to re-source four distribution centers, and the price increase "
        "exceeds market benchmarks."
    ))
    add_para(doc, (
        "5. Each sub-agent saved its output to a separate file in Outputs/, leaving data/ untouched."
    ))
    add_para(doc, (
        "6. Claude Code then read all three output files, identified the key findings, and assembled "
        "them into a single intelligence-brief.md with the executive summary written last."
    ))

    # --- Worked Example 2: Deviation Costing with Hook ---
    doc.add_heading("Worked example 2: Automatic deviation costing with a PostToolUse hook", level=2)

    add_para(doc, (
        "Every proposed contract change has a dollar cost. A deviation table without dollar figures "
        "is useless at the negotiation table. The PostToolUse hook in Claude Code (in the terminal) "
        "enforces this rule automatically. Every time Claude writes to the deviation costs file, the "
        "hook checks that every row has a dollar figure. If any row is blank or says TBD, the hook "
        "prints an error. The table cannot exist on disk with a missing cost."
    ))

    doc.add_heading("The prompt to type", level=3)
    add_code_block(doc, (
        'Read data/current-contract.md and data/proposed-renewal.md. Create a deviation\n'
        'table at Outputs/deviation-costs.md with five columns: Term, Current Value,\n'
        'Proposed Value, Direction, and Annual Cost Impact (in USD). The contract is\n'
        '$9.2M per year. Calculate the annual cost impact for every changed term.\n'
        'Do not leave any cell in the Annual Cost Impact column blank or marked TBD.'
    ))

    doc.add_heading("The folder layout", level=3)
    add_code_block(doc, (
        "practice/\n"
        "  .claude/\n"
        "    settings.json                (PostToolUse hook registered here)\n"
        "  scripts/\n"
        "    check-deviation-costs.py     (the hook script)\n"
        "  data/\n"
        "    current-contract.md\n"
        "    proposed-renewal.md\n"
        "  Outputs/"
    ))

    doc.add_heading("What you should see", level=3)
    add_para(doc, (
        "Claude Code (in the terminal) writes Outputs/deviation-costs.md. Immediately after the write, "
        "the PostToolUse hook fires. The terminal prints: \"Total annual cost impact: $1,378,000.\" "
        "If any row were missing a figure, it would print: \"ERROR: [term name] is missing an annual "
        "cost impact figure.\" and exit with code 1."
    ))

    doc.add_heading("What Claude did, behind the scenes", level=3)
    add_para(doc, (
        "1. Claude Code (in the terminal) read both contract files and compared them term by term, "
        "identifying three changes: price increase, force majeure narrowing, and notice period reduction."
    ))
    add_para(doc, (
        "2. For the price increase, it multiplied $9.2M by 12% to get $1,104,000 in annual impact."
    ))
    add_para(doc, (
        "3. For the force majeure change, it used historical disruption data ($420,000 over 3 years) "
        "to estimate an annualized exposure of $140,000."
    ))
    add_para(doc, (
        "4. For the notice period, it estimated the cost of compressed re-sourcing at $134,000."
    ))
    add_para(doc, (
        "5. It wrote the deviation table to Outputs/deviation-costs.md with dollar figures in every cell."
    ))
    add_para(doc, (
        "6. The PostToolUse hook (scripts/check-deviation-costs.py) fired automatically. It parsed the "
        "markdown table, checked each Annual Cost Impact cell for a dollar sign, summed the values, "
        "and printed the total. Exit code 0 confirmed success."
    ))

    # --- Worked Example 3: Counter-Proposal via Slash Command ---
    doc.add_heading("Worked example 3: Generating the counter-proposal with a slash command", level=2)

    add_para(doc, (
        "The counter-proposal is the document your negotiator takes to the table. It must address "
        "all three proposed changes, stay below the $9.75M walk-away ceiling, cite specific "
        "performance data, and read as a formal external communication. The /counter-proposal slash "
        "command in Claude Code (in the terminal) generates it from the approved brief, the deviation "
        "costs, and the negotiation history."
    ))

    doc.add_heading("The prompt to type", level=3)
    add_code_block(doc, "/counter-proposal")

    doc.add_heading("The folder layout", level=3)
    add_code_block(doc, (
        "practice/\n"
        "  .claude/\n"
        "    commands/\n"
        "      counter-proposal.md        (the command definition)\n"
        "  Outputs/\n"
        "    pre-negotiation-brief.md     (approved brief with BATNA and walk-away)\n"
        "    deviation-costs.md           (costed deviation table)\n"
        "  data/\n"
        "    negotiation-history.csv      (8 past outcomes)"
    ))

    doc.add_heading("What you should see", level=3)
    add_para(doc, (
        "Claude Code (in the terminal) reads the command definition, follows the five steps, and writes "
        "Outputs/counter-proposal.md. The document is addressed to Redline Logistics LLC. It proposes "
        "a 4% price increase ($9.568M total), restoring the original force majeure clause, and keeping "
        "the 180-day notice period. It does not reveal the $9.75M walk-away price. It sets a response "
        "deadline of 2026-05-09."
    ))

    doc.add_heading("What Claude did, behind the scenes", level=3)
    add_para(doc, (
        "1. Claude Code (in the terminal) read the command definition from .claude/commands/counter-proposal.md "
        "and identified five steps to follow."
    ))
    add_para(doc, (
        "2. It read the pre-negotiation brief and extracted the walk-away price ($9.75M), BATNA "
        "(rebid to three carriers, $280,000 transition cost), and three recommendations. It held "
        "these as constraints, not content to copy."
    ))
    add_para(doc, (
        "3. It read the deviation costs and calculated counter-positions: 4% on price (vs. 12%), "
        "full restoration on both legal clauses."
    ))
    add_para(doc, (
        "4. It read the negotiation history and noted the 2024 precedent: Redline proposed 8%, "
        "settled at 4.1%. This confirmed that a 4% counter was realistic."
    ))
    add_para(doc, (
        "5. It verified the total: $9.2M multiplied by 1.04 equals $9.568M, below $9.75M."
    ))
    add_para(doc, (
        "6. It wrote the counter-proposal in formal external language, citing OTD performance data "
        "but never mentioning BATNA, walk-away, or internal deviation terminology."
    ))
    add_para(doc, (
        "7. It set the response deadline to 2026-05-09, 14 days from 2026-04-25."
    ))

    # =========================================================================
    # 7. DAY IN THE LIFE
    # =========================================================================
    doc.add_heading("A day in the life: Maria prepares for the Redline negotiation", level=1)

    add_para(doc, (
        "Maria Ruiz is a Senior Category Manager at TransGlobal Industries, a US-based manufacturer "
        "with $340M in annual procurement spend. She manages the logistics category: $28.4M across "
        "three suppliers. She has been with TransGlobal for six years and has negotiated 14 supplier "
        "contracts in that time. Today is Wednesday, 2026-04-29. The face-to-face negotiation with "
        "Redline Logistics LLC is in eight days."
    ))

    # Scenario 1
    doc.add_heading("08:15. The VP's deadline arrives", level=2)
    add_para(doc, (
        "Maria opens her laptop and finds an email from her VP: \"Need the pre-negotiation brief by "
        "end of day. The CPO wants it before Friday's exec meeting.\" Maria has the source files, but "
        "writing the brief from scratch would take most of the day. She opens her terminal."
    ))
    add_code_block(doc, (
        "cd negotiation-prep\n"
        "claude\n"
        "The folder data/ holds the source files. Do not edit any file in data/. "
        "Save all output to Outputs/."
    ))
    add_para(doc, (
        "She launches three sub-agents in parallel to gather the intelligence she needs."
    ))
    add_code_block(doc, (
        'Run three sub-agents in parallel. Sub-agent 1: analyze supplier performance\n'
        'from data/supplier-performance.csv, write to Outputs/performance-analysis.md.\n'
        'Sub-agent 2: benchmark market rates from data/market-benchmarks.md against\n'
        'data/proposed-renewal.md, write to Outputs/market-analysis.md. Sub-agent 3:\n'
        'assess term risks from data/current-contract.md and data/proposed-renewal.md,\n'
        'write to Outputs/terms-risk-analysis.md. Merge all three into\n'
        'Outputs/intelligence-brief.md with an executive summary naming Redline\n'
        'Logistics LLC, $9.2M, and 2026-05-07.'
    ))
    add_para(doc, (
        "Three minutes later, all three sub-agents finish. Maria reviews the intelligence brief. "
        "Key finding: Redline's on-time delivery dropped from 96.8% to 93.1%, below the 95.0% "
        "SLA target for six consecutive months. Redline's proposed pricing sits 8% above the market "
        "median."
    ))
    add_para(doc, (
        "What to learn from this. Sub-agents cut elapsed time by running independent tasks in parallel. "
        "The critical word is \"independent.\" If task B needs the output of task A, they must run in "
        "sequence. But performance analysis, market benchmarking, and terms risk assessment each read "
        "different source files and produce separate outputs. That makes them ideal for parallel execution."
    ))

    # Scenario 2
    doc.add_heading("08:45. Deviation costing with automatic validation", level=2)
    add_para(doc, (
        "Maria needs to cost every proposed deviation in USD. She types one prompt."
    ))
    add_code_block(doc, (
        'Read data/current-contract.md and data/proposed-renewal.md. Create a deviation\n'
        'table at Outputs/deviation-costs.md with columns: Term, Current Value, Proposed\n'
        'Value, Direction, Annual Cost Impact (USD). The contract is $9.2M/year.\n'
        'Calculate every annual cost impact. No blanks, no TBDs.'
    ))
    add_para(doc, (
        "Claude Code (in the terminal) writes the file. The PostToolUse hook fires automatically. "
        "The terminal prints: \"Total annual cost impact: $1,378,000.\" Maria did not run the check "
        "by hand. The hook ran it for her."
    ))
    add_para(doc, (
        "What to learn from this. A PostToolUse hook runs every time Claude writes a specific file. "
        "You set it up once and forget it. The hook catches missing data, wrong formats, and "
        "incomplete tables without you having to remember to check. For deviation costing, this "
        "prevents the embarrassment of presenting a table with TBD cells to a supplier."
    ))

    # Scenario 3
    doc.add_heading("09:10. Writing the brief with automatic completeness gates", level=2)
    add_para(doc, (
        "Maria writes the pre-negotiation brief. She includes the BATNA (rebid to three qualified "
        "carriers, $280,000 transition cost, 90-day timeline) and the walk-away price ($9.75M)."
    ))
    add_code_block(doc, (
        'Write a complete pre-negotiation brief to Outputs/pre-negotiation-brief.md.\n'
        'Include: Objective, Supplier Background, Performance Summary, Market Position,\n'
        'Deviation Cost Summary, BATNA (rebid to three carriers, $280,000 transition,\n'
        '90-day timeline), Walk-Away Price ($9.75M), and Recommended Strategy (three\n'
        'recommendations max). Name Redline Logistics LLC, $9.2M, and 2026-05-07.'
    ))
    add_para(doc, (
        "The PreToolUse hook fires before the write. It checks the brief content for a BATNA section "
        "and a walk-away price with a dollar figure. Both are present. The terminal prints: \"Brief "
        "completeness check passed.\" The file saves."
    ))
    add_para(doc, (
        "What to learn from this. A PreToolUse hook runs before the write, not after. If the check "
        "fails, the file is never written to disk. This is stronger than a PostToolUse check, which "
        "writes the file first and flags the problem second. Use PreToolUse for hard gates: fields "
        "that must be present before the document can exist."
    ))

    # Scenario 4
    doc.add_heading("09:40. The counter-proposal, one command", level=2)
    add_para(doc, (
        "Maria's VP approved the brief via Slack at 09:35. Maria needs the counter-proposal by noon. "
        "She types one command."
    ))
    add_code_block(doc, "/counter-proposal")
    add_para(doc, (
        "Claude Code (in the terminal) reads the command definition from .claude/commands/counter-proposal.md. "
        "It reads the approved brief for strategy, the deviation costs for figures, and the negotiation "
        "history for precedent. It writes Outputs/counter-proposal.md: a formal letter to Redline "
        "Logistics LLC proposing a 4% price increase ($9.568M total), restoring both the force majeure "
        "clause and the 180-day notice period. Response deadline: 2026-05-09."
    ))
    add_para(doc, (
        "What to learn from this. A slash command encodes multi-step logic into a single trigger. "
        "Maria did not have to remember which files to read, which figures to cite, or which internal "
        "terms to avoid in external documents. The command definition handles all of that. Any "
        "colleague on her team can type /counter-proposal and get the same structured output."
    ))

    # Scenario 5
    doc.add_heading("10:00. Checking the counter-proposal before sending", level=2)
    add_para(doc, (
        "Maria reads the counter-proposal one more time before forwarding it to her VP."
    ))
    add_code_block(doc, (
        'Read Outputs/counter-proposal.md. Is the total annual value below $9.75M?\n'
        'Does it address all three proposed changes? Does it use external language\n'
        'throughout, with no mentions of BATNA, walk-away, or deviation costs?'
    ))
    add_para(doc, (
        "Claude Code (in the terminal) confirms: total is $9.568M (below $9.75M), all three changes "
        "are addressed, and the document uses formal external language throughout. Maria sends it to "
        "her VP. Total time from opening her laptop to sending the counter-proposal: 1 hour 45 minutes."
    ))
    add_para(doc, (
        "What to learn from this. Always verify the output before it leaves your desk. Claude Code "
        "(in the terminal) is a tool, not a decision maker. The hooks catch structural problems "
        "(missing fields, blank costs). Your review catches strategic problems (wrong tone, revealed "
        "walk-away price, inappropriate concessions). Both checks are necessary."
    ))

    # Scenario 6
    doc.add_heading("16:30 (eight days later, 2026-05-07). Post-close capture", level=2)
    add_para(doc, (
        "The negotiation closed at 14:00. Redline accepted the 4% price increase, restored the "
        "force majeure clause, and kept the 180-day notice period. Final agreed value: $9,568,000. "
        "Maria records the outcome before the details fade."
    ))
    add_code_block(doc, "/post-close")
    add_para(doc, (
        "Claude Code (in the terminal) asks Maria for the outcome details. She types them."
    ))
    add_code_block(doc, (
        'Final agreed annual value: $9,568,000. Date signed: 2026-05-07. Concessions\n'
        'TransGlobal gave: performance review clause with 6-month improvement period.\n'
        'Concessions TransGlobal received: 4% price cap, force majeure restored, notice\n'
        'period restored to 180 days.'
    ))
    add_para(doc, (
        "Claude appends a row to Outputs/negotiation-log.csv, writes Outputs/post-close-capture.md "
        "with four sections (Deal Summary, What Worked, What to Watch, Recommendations for Next "
        "Renewal), and copies all working files to Outputs/archive/redline-logistics-llc_2026-05-07/. "
        "The terminal prints: \"Post-close complete. Redline Logistics LLC. Final value: $9,568,000. "
        "Savings vs. opening ask: $1,010,000 (9.5%).\""
    ))
    add_para(doc, (
        "What to learn from this. Post-close capture is the most-skipped step in procurement. People "
        "close the deal, celebrate, and move on. Six months later, nobody remembers why the force "
        "majeure clause mattered or what Redline's opening ask was. The /post-close command captures "
        "everything in one minute. The archive folder means the next category manager who works on "
        "Redline can read the full history, not start from zero."
    ))

    # Scenario 7
    doc.add_heading("16:45. Sharing the system with a colleague", level=2)
    add_para(doc, (
        "Maria's colleague, James, manages the IT services category. He has a $6.8M contract renewal "
        "coming up with Apex Technology Partners. Maria copies the negotiation-prep/ folder structure, "
        "swaps in James's source files, and updates CLAUDE.md with the new supplier name, contract "
        "value, and deadline."
    ))
    add_code_block(doc, (
        "cp -r negotiation-prep/ james-apex-negotiation/\n"
        "# James replaces data/ files with his own\n"
        "# James updates CLAUDE.md with Apex Technology Partners, $6.8M, new deadline\n"
        "# James runs: claude\n"
        "# James types the same prompts. The system works the same way."
    ))
    add_para(doc, (
        "What to learn from this. A composition system is transferable. The prompts, hooks, and commands "
        "are not tied to Redline Logistics LLC. They reference file paths and column names, not specific "
        "supplier values. Change the data files and the CLAUDE.md context, and the same system works for "
        "any supplier negotiation."
    ))

    # =========================================================================
    # 8. 20-MINUTE SPRINT
    # =========================================================================
    doc.add_heading("20-minute sprint: your first negotiation intelligence output", level=1)

    add_para(doc, (
        "This section gets you from zero to a usable intelligence brief in 20 minutes. Follow the "
        "time blocks exactly. Do not stop to explore. Do not customize. Just run the prompts and "
        "see the output. You can customize after you know the system works."
    ))

    doc.add_heading("Minutes 0 to 5: Open the project and start Claude Code", level=2)
    add_para(doc, "Open your terminal. Navigate to the practice folder.")
    add_code_block(doc, (
        'cd "Course_10_The_Negotiation_Intelligence_System/practice"\n'
        'ls data/'
    ))
    add_para(doc, (
        "Confirm you see five files: current-contract.md, proposed-renewal.md, supplier-performance.csv, "
        "market-benchmarks.md, and negotiation-history.csv."
    ))
    add_para(doc, "Start Claude Code (in the terminal).")
    add_code_block(doc, (
        'claude\n'
        'The folder data/ holds the source files. Do not edit any file in data/. '
        'Save all output to Outputs/.'
    ))

    doc.add_heading("Minutes 5 to 10: Launch three sub-agents", level=2)
    add_para(doc, "Launch the intelligence gathering sub-agents.")
    add_code_block(doc, (
        'Run three sub-agents in parallel. Sub-agent 1: analyze performance from\n'
        'data/supplier-performance.csv, write to Outputs/performance-analysis.md.\n'
        'Sub-agent 2: benchmark rates from data/market-benchmarks.md vs.\n'
        'data/proposed-renewal.md, write to Outputs/market-analysis.md. Sub-agent 3:\n'
        'assess term risks from data/current-contract.md and data/proposed-renewal.md,\n'
        'write to Outputs/terms-risk-analysis.md.'
    ))
    add_para(doc, "Wait for all three to complete. This takes two to four minutes.")

    doc.add_heading("Minutes 10 to 15: Merge into the intelligence brief", level=2)
    add_code_block(doc, (
        'Merge Outputs/performance-analysis.md, Outputs/market-analysis.md, and\n'
        'Outputs/terms-risk-analysis.md into Outputs/intelligence-brief.md. Add an\n'
        'executive summary with five bullets: one on OTD trend, one on market position,\n'
        'one on force majeure risk, one on notice period risk, and one overall\n'
        'recommendation. Name Redline Logistics LLC, state $9.2M, include 2026-05-07.'
    ))
    add_para(doc, (
        "Claude Code (in the terminal) merges the three files into one document with an executive summary."
    ))

    doc.add_heading("Minutes 15 to 20: Review and validate", level=2)
    add_code_block(doc, (
        'Read the executive summary in Outputs/intelligence-brief.md. Does it name\n'
        'Redline Logistics LLC, state $9.2M, include 2026-05-07, and give a clear\n'
        'recommendation? List any missing items.'
    ))
    add_para(doc, (
        "Claude confirms all fields are present. Open Outputs/intelligence-brief.md in your text editor "
        "and read the executive summary. You now have a VP-ready intelligence brief. Total time: "
        "about 18 minutes."
    ))
    add_para(doc, (
        "Next step: build the deviation costing hook when you are ready. The intelligence "
        "brief is the input for the deviation analysis and the pre-negotiation brief."
    ))

    # =========================================================================
    # 9. FIRST WEEK PLANNER
    # =========================================================================
    doc.add_heading("First week day-by-day planner", level=1)

    add_para(doc, (
        "This five-day plan takes you from first contact with the system to a complete, repeatable "
        "negotiation workflow. Each day has a specific goal and a time budget."
    ))

    # Day 1
    doc.add_heading("Day 1: Install, orient, and run the 20-minute sprint", level=2)
    add_para(doc, "Goal: Confirm Claude Code (in the terminal) is installed and produce your first intelligence brief.", bold=True)
    add_bullet(doc, "Install Claude Code if not already installed (10 minutes).")
    add_bullet(doc, "Navigate to the course practice folder and confirm five source files in data/ (2 minutes).")
    add_bullet(doc, "Run the 20-minute sprint (20 minutes).")
    add_bullet(doc, "Read the intelligence brief executive summary. Note the OTD decline (96.8% to 93.1%) and the 8% above-market pricing (5 minutes).")
    add_para(doc, "Total: about 37 minutes.")

    # Day 2
    doc.add_heading("Day 2: Build the deviation costing hook", level=2)
    add_para(doc, "Goal: Create the PostToolUse hook that validates every deviation table automatically.", bold=True)
    add_bullet(doc, "Create scripts/check-deviation-costs.py following the course instructions (15 minutes).")
    add_bullet(doc, "Register the hook in .claude/settings.json (5 minutes).")
    add_bullet(doc, "Test the hook by writing a deviation table with a missing cost figure. Confirm the error message (10 minutes).")
    add_bullet(doc, "Write the complete deviation table with all figures populated. Confirm the hook prints the total: $1,378,000 (10 minutes).")
    add_para(doc, "Total: about 40 minutes.")

    # Day 3
    doc.add_heading("Day 3: Build the brief completeness gate and write the brief", level=2)
    add_para(doc, "Goal: Create the PreToolUse hook and produce the VP-ready pre-negotiation brief.", bold=True)
    add_bullet(doc, "Create scripts/check-brief-completeness.py following the course instructions (15 minutes).")
    add_bullet(doc, "Register the PreToolUse hook in .claude/settings.json alongside the existing PostToolUse hook (5 minutes).")
    add_bullet(doc, "Test the gate by writing a brief without BATNA and walk-away. Confirm the block message (10 minutes).")
    add_bullet(doc, "Write the complete brief with BATNA ($280,000 transition cost, 90-day timeline) and walk-away price ($9.75M). Confirm the hook passes (15 minutes).")
    add_para(doc, "Total: about 45 minutes.")

    # Day 4
    doc.add_heading("Day 4: Build the slash commands", level=2)
    add_para(doc, "Goal: Create the /counter-proposal and /post-close commands and run them both.", bold=True)
    add_bullet(doc, "Create .claude/commands/counter-proposal.md with the five-step command definition (10 minutes).")
    add_bullet(doc, "Run /counter-proposal. Review the output: is the total below $9.75M? Are all three changes addressed? Is the language external? (15 minutes).")
    add_bullet(doc, "Create .claude/commands/post-close.md with the eight-step command definition (10 minutes).")
    add_bullet(doc, "Run /post-close with the practice outcome data. Verify the negotiation log, lessons-learned document, and archive folder (15 minutes).")
    add_para(doc, "Total: about 50 minutes.")

    # Day 5
    doc.add_heading("Day 5: Apply the system to a new supplier", level=2)
    add_para(doc, "Goal: Copy the system to a new folder and run it against a different supplier's data.", bold=True)
    add_bullet(doc, "Copy the negotiation-prep/ folder to a new folder for a different supplier (5 minutes).")
    add_bullet(doc, "Replace the five files in data/ with source files for the new supplier (10 minutes).")
    add_bullet(doc, "Update CLAUDE.md with the new supplier name, contract value, and deadline (5 minutes).")
    add_bullet(doc, "Run the full pipeline: sub-agents, deviation costing, brief, counter-proposal (25 minutes).")
    add_bullet(doc, "Compare the output quality to the Redline example. Note any prompts that need adjustment for the new category (10 minutes).")
    add_para(doc, "Total: about 55 minutes.")

    add_para(doc, (
        "By the end of Day 5, you have a negotiation intelligence system that works for two suppliers. "
        "The hooks, commands, and folder structure are proven. From here, every new negotiation is a "
        "copy-and-customize exercise, not a build-from-scratch effort."
    ))

    add_para(doc, (
        "Why this matters. Most procurement tools require weeks of implementation and vendor support "
        "before they produce anything. The negotiation intelligence system produces a usable output "
        "on Day 1 (the intelligence brief) and a complete, repeatable pipeline by Day 4. Day 5 "
        "proves the system transfers to a new supplier. That is five days from zero to a reusable "
        "asset, with no IT department involvement and no software license."
    ))

    # =========================================================================
    # 10. THE PATTERN
    # =========================================================================
    doc.add_heading("The pattern: how to build a composition system for any procurement workflow", level=1)

    add_para(doc, (
        "The negotiation intelligence system follows a pattern you can apply to any multi-stage "
        "procurement workflow: sourcing events, category reviews, risk assessments, or savings "
        "program tracking. The pattern has five steps."
    ))

    add_para(doc, "1. Map the workflow stages.", bold=True)
    add_para(doc, (
        "List every stage from input to output. For each stage, name the input files, the output "
        "file, and whether the stage depends on a previous stage's output. Independent stages can "
        "run in parallel with sub-agents. Dependent stages run in sequence."
    ))

    add_para(doc, "2. Assign components.", bold=True)
    add_para(doc, (
        "Match each stage to a Claude Code (in the terminal) component. Sub-agents for parallel "
        "research. PostToolUse hooks for automatic validation after a file is written. PreToolUse "
        "hooks for hard gates that block the write. Slash commands for multi-step generation "
        "triggered by one command. CLAUDE.md for persistent context that applies to every prompt."
    ))

    add_para(doc, "3. Write the hooks.", bold=True)
    add_para(doc, (
        "Each hook is a Python script in scripts/. It uses only standard library modules. It reads "
        "the file or stdin, checks for specific conditions, and exits with code 0 (pass) or 1 (fail). "
        "Register each hook in .claude/settings.json under PostToolUse or PreToolUse."
    ))

    add_para(doc, "4. Write the commands.", bold=True)
    add_para(doc, (
        "Each command is a markdown file in .claude/commands/. It lists the steps Claude Code "
        "(in the terminal) should follow, the files it should read, the constraints it should enforce, "
        "and the output file it should produce. The command name is the filename without the .md "
        "extension. You run it by typing / followed by the name."
    ))

    add_para(doc, "5. Test, then transfer.", bold=True)
    add_para(doc, (
        "Run the full pipeline against practice data. Fix any prompt that produces the wrong output. "
        "Tighten any hook that passes when it should fail. Then copy the folder to a new supplier, "
        "swap in new data files, update CLAUDE.md, and run again."
    ))

    add_para(doc, (
        "Why this matters. A composition system is not a one-off project. It is a reusable asset. "
        "The time you invest in building the hooks, commands, and folder structure pays off on the "
        "second, third, and tenth negotiation. Without the pattern, every negotiation starts from "
        "scratch. With it, every negotiation starts from a proven pipeline."
    ))

    # =========================================================================
    # 11. CAUTIONS AND TROUBLESHOOTING
    # =========================================================================
    doc.add_heading("Cautions and troubleshooting", level=1)

    add_para(doc, (
        "Every system has failure modes. The six entries below cover the problems you are most likely "
        "to hit when building and running the negotiation intelligence system in Claude Code (in the terminal)."
    ))

    # Entry 1
    doc.add_heading("Sub-agents run in sequence instead of in parallel", level=2)
    add_para(doc, "Symptom:", bold=True)
    add_para(doc, (
        "You ask for three parallel sub-agents. Claude Code (in the terminal) runs them one at a time. "
        "Total time is 8 to 10 minutes instead of 3 to 4."
    ))
    add_para(doc, "Fix:", bold=True)
    add_para(doc, (
        "Tell Claude explicitly: \"These three tasks are independent. Run all three in parallel before "
        "proceeding.\" If it still serializes, check that each sub-agent reads different files. If two "
        "sub-agents read the same file and Claude judges them dependent, it may serialize to avoid "
        "conflicts."
    ))

    # Entry 2
    doc.add_heading("The PostToolUse hook does not fire", level=2)
    add_para(doc, "Symptom:", bold=True)
    add_para(doc, (
        "Claude Code (in the terminal) writes Outputs/deviation-costs.md but the hook never runs. "
        "No total is printed. No errors appear."
    ))
    add_para(doc, "Fix:", bold=True)
    add_para(doc, (
        "Check three things. First, is .claude/settings.json in the practice/ folder (not a parent folder)? "
        "Second, is the JSON valid (no trailing commas, no mismatched brackets)? Third, did you restart "
        "Claude Code after editing settings.json? The hook configuration loads at startup. Changes made "
        "while Claude Code is running do not take effect until the next session."
    ))

    # Entry 3
    doc.add_heading("The PreToolUse hook blocks every file, not just the brief", level=2)
    add_para(doc, "Symptom:", bold=True)
    add_para(doc, (
        "Every file write triggers the brief completeness check, including deviation-costs.md and "
        "counter-proposal.md. Files that should not require BATNA are being blocked."
    ))
    add_para(doc, "Fix:", bold=True)
    add_para(doc, (
        "Add a filename check at the top of scripts/check-brief-completeness.py. Read the target "
        "filename from the CLAUDE_TOOL_INPUT environment variable. If the filename does not contain "
        "\"brief,\" exit with code 0 immediately. This lets non-brief files pass through without "
        "the BATNA check."
    ))

    # Entry 4
    doc.add_heading("The counter-proposal reveals the walk-away price", level=2)
    add_para(doc, "Symptom:", bold=True)
    add_para(doc, (
        "The generated counter-proposal includes the phrase \"$9.75M walk-away\" or similar internal "
        "language. Sending this to Redline Logistics LLC would weaken your negotiating position."
    ))
    add_para(doc, "Fix:", bold=True)
    add_para(doc, (
        "Tell Claude Code (in the terminal): \"Read Outputs/counter-proposal.md. Remove any mention of "
        "$9.75M, BATNA, walk-away, or deviation costs. Replace with external language about reviewing "
        "alternatives for the corridor.\" Then update the command definition in .claude/commands/"
        "counter-proposal.md to add a stronger instruction: \"Never include the walk-away price, "
        "BATNA details, or internal procurement terminology in the output document.\""
    ))

    # Entry 5
    doc.add_heading("The negotiation log has duplicate rows", level=2)
    add_para(doc, "Symptom:", bold=True)
    add_para(doc, (
        "You ran /post-close twice (once by mistake). Outputs/negotiation-log.csv now has two identical "
        "rows for the same negotiation."
    ))
    add_para(doc, "Fix:", bold=True)
    add_para(doc, (
        "Open the CSV in a text editor and delete the duplicate row. Then update .claude/commands/"
        "post-close.md to add a deduplication check: \"Before appending, check whether a row with the "
        "same Contract_ID and Close_Date already exists. If it does, skip the append and print a "
        "message: 'Row already exists. Skipping.'\""
    ))

    # Entry 6
    doc.add_heading("The archive folder copies are missing files", level=2)
    add_para(doc, "Symptom:", bold=True)
    add_para(doc, (
        "The archive subfolder has three files instead of five. The intelligence brief and deviation "
        "costs are missing."
    ))
    add_para(doc, "Fix:", bold=True)
    add_para(doc, (
        "Check that the /post-close command definition says \"Copy all files in Outputs/ (except the "
        "archive/ subfolder)\" and not \"Copy the counter-proposal and brief.\" The command should copy "
        "everything, not a named list. If the command definition is correct but files are still missing, "
        "check that the missing files exist in Outputs/ before running /post-close. The command cannot "
        "copy files that do not exist."
    ))

    # =========================================================================
    # 12. DONE CHECKLIST
    # =========================================================================
    doc.add_heading("Done checklist", level=1)

    add_para(doc, (
        "Run this list before using any output from the negotiation intelligence system in a real "
        "supplier negotiation. Each item must be confirmed before the document leaves your desk."
    ))

    checklist_items = [
        "The intelligence brief names Redline Logistics LLC (or your actual supplier), states the contract value, and includes the negotiation deadline.",
        "The deviation costs table has a dollar figure in every Annual Cost Impact cell. No blanks. No TBDs.",
        "The pre-negotiation brief has a BATNA section and a walk-away price with a dollar figure.",
        "The pre-negotiation brief has three recommendations or fewer.",
        "The counter-proposal total is below the walk-away price.",
        "The counter-proposal addresses all proposed changes (price, force majeure, notice period, or equivalent).",
        "The counter-proposal uses formal external language. No mentions of BATNA, walk-away, deviation costs, or other internal terminology.",
        "The counter-proposal includes a response deadline.",
        "The post-close capture records the final agreed value, date signed, concessions given, and concessions received.",
        "The archive folder contains copies of all working files.",
        "No file in data/ was edited during the process.",
        "All currency figures are in USD. All dates are in YYYY-MM-DD format.",
        "No em-dashes or en-dashes appear anywhere in the output files.",
        "Oxford commas are used in every list of three or more items.",
        "Every executive summary names the supplier (legal entity), a contract value or spend figure, and a date.",
    ]

    for i, item in enumerate(checklist_items, 1):
        add_bullet(doc, f" {item}", bold_prefix=f"{i}.")

    add_para(doc, (
        "If any item fails, fix it before the document goes to your VP, your negotiator, or the supplier. "
        "The hooks catch most structural problems automatically. This checklist catches the rest."
    ))

    # =========================================================================
    # FOOTER
    # =========================================================================
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("U2xAI  |  PROCUREAI ACADEMY  |  Course 10: The Negotiation Intelligence System")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
    r.font.name = "Calibri"

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Confidential. For training use only. Do not distribute outside your organization.")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
    r.font.name = "Calibri"
    r.italic = True

    # Save
    OUTPATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUTPATH))
    print(f"Saved: {OUTPATH}")
    print(f"Size: {OUTPATH.stat().st_size:,} bytes")


if __name__ == "__main__":
    build()
