"""
Build Course 14: Supplier Lifecycle Management Handout (.docx).
Generates a comprehensive training guide handout (6,000+ words).
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import textwrap

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUT = PROJECT_ROOT / "Handouts" / "Course_14_Supplier_Lifecycle_Management_Handout.docx"
OUT.parent.mkdir(parents=True, exist_ok=True)

doc = Document()

# ── global styles ──────────────────────────────────────────────────────
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

for level in range(1, 4):
    hs = doc.styles[f"Heading {level}"]
    hs.font.name = "Calibri"
    hs.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
    if level == 1:
        hs.font.size = Pt(18)
    elif level == 2:
        hs.font.size = Pt(14)
    else:
        hs.font.size = Pt(12)

# ── helper functions ───────────────────────────────────────────────────

def add_para(text, bold=False, italic=False, style_name="Normal", space_after=None):
    p = doc.add_paragraph(style=style_name)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p

def add_code_block(text):
    """Add a code block with monospace font and grey background."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(1)
    # Add shading
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F2F2F2" w:val="clear"/>')
    p.paragraph_format.element.get_or_add_pPr().append(shading)
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    return p

def add_table(headers, rows, col_widths=None):
    """Add a formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1B3A5C" w:val="clear"/>')
        cell.paragraphs[0].paragraph_format.element.get_or_add_pPr()
        cell._tc.get_or_add_tcPr().append(shading)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            run = cell.paragraphs[0].add_run(str(val))
            run.font.name = "Calibri"
            run.font.size = Pt(10)
            if r_idx % 2 == 1:
                shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F7FA" w:val="clear"/>')
                cell._tc.get_or_add_tcPr().append(shading)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()  # spacer
    return table

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.bold = True
        run_b.font.name = "Calibri"
        run_b.font.size = Pt(11)
        run_n = p.add_run(text)
        run_n.font.name = "Calibri"
        run_n.font.size = Pt(11)
    else:
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
    return p

def add_numbered(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Number")
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.bold = True
        run_b.font.name = "Calibri"
        run_b.font.size = Pt(11)
        run_n = p.add_run(text)
        run_n.font.name = "Calibri"
        run_n.font.size = Pt(11)
    else:
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
    return p

# ═══════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("U2xAI")
run.bold = True
run.font.size = Pt(12)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("PROCUREAI ACADEMY")
run.bold = True
run.font.size = Pt(10)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x55, 0x6B, 0x82)
p.paragraph_format.space_after = Pt(2)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Course 14: Supplier Lifecycle Management")
run.bold = True
run.font.size = Pt(22)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
p.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Comprehensive Training Guide Handout")
run.font.size = Pt(13)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x55, 0x6B, 0x82)
p.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Track 30 suppliers from onboarding to exit using Claude Code (in the terminal)")
run.italic = True
run.font.size = Pt(11)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x55, 0x6B, 0x82)
p.paragraph_format.space_after = Pt(2)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Date: 2026-04-26  |  Version: 1.0")
run.font.size = Pt(10)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
p.paragraph_format.space_after = Pt(20)

# ═══════════════════════════════════════════════════════════════════════
# 1. HOW TO USE THIS HANDOUT
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("How to Use This Handout", level=1)

add_para(
    "This handout is the companion reference for Course 14: Supplier Lifecycle Management. "
    "It covers everything you learn across six lessons, condensed into a single document you "
    "can keep on your desk or laptop. Use it before the course to see what you will build, "
    "during the course as a quick-reference, and after the course when you apply the techniques "
    "to your own supplier portfolio."
)
add_para(
    "Every section includes the exact prompts you type in Claude Code (in the terminal), "
    "the folder layout where the files live, the output you should see, and a plain-English "
    "walkthrough of what Claude did behind the scenes. If you can copy a prompt, press Enter, "
    "and read the result, you have everything you need."
)
add_para(
    "The course uses Crestview Industries, a fictional US-based manufacturer with $38.6M in annual "
    "supplier spend across 30 suppliers. All supplier names, spend figures, and performance scores "
    "are realistic but fake. Do not search for Crestview Industries or any supplier named in this "
    "handout. They do not exist."
)

# ═══════════════════════════════════════════════════════════════════════
# 2. WHAT THIS COURSE TEACHES
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("What This Course Teaches", level=1)

add_para(
    "You are the Supplier Relationship Manager at Crestview Industries. You manage 30 suppliers "
    "across seven lifecycle stages: Onboarding, Active, Strategic, At Risk, Corrective Action, Exit, "
    "and Under Review. The supplier data lives in three CSV files and a handful of Word documents. "
    "The data is scattered. The stages are stale. Your director wants a full lifecycle status report "
    "by Friday, and building it by hand would take the better part of a day."
)
add_para(
    "This course teaches you to use Claude Code (in the terminal) to read all your supplier data, "
    "classify every supplier into the correct lifecycle stage, generate onboarding checklists, "
    "detect at-risk suppliers before they cause delivery failures, draft corrective action plans, "
    "build exit transition timelines, and save the entire lifecycle state so it persists between "
    "sessions. By the end, one command gives you the full picture."
)
add_para(
    "The six sessions build on each other. The first covers classification and segmentation "
    "of all 30 suppliers. The second automates onboarding checklists. The third tracks strategic "
    "development plans. The fourth detects declining performance and triggers corrective action. "
    "The fifth builds exit transition plans. The sixth saves lifecycle state to a JSON file so "
    "decisions survive between sessions."
)

add_table(
    ["Lesson", "Title", "Time", "What you build"],
    [
        ["1", "Supplier Segmentation", "55 min", "A segmentation report classifying 30 suppliers by tier and stage"],
        ["2", "Onboarding Automation", "50 min", "A compliance checklist with gap detection and follow-up email"],
        ["3", "Strategic Development Plans", "55 min", "A review-ready status summary for a strategic supplier"],
        ["4", "At-Risk Detection", "60 min", "An at-risk report and a corrective action plan"],
        ["5", "Exit Management", "50 min", "A transition timeline and exit notification letter"],
        ["6", "State Persistence", "50 min", "A JSON state file that remembers decisions between sessions"],
    ],
    col_widths=[0.6, 1.8, 0.7, 3.5],
)

# ═══════════════════════════════════════════════════════════════════════
# 3. WHAT IS IN THE COURSE FOLDER
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("What Is in the Course Folder", level=1)

add_para(
    "The course ships as a self-contained folder. Everything you need is inside it. There are "
    "no external downloads, no shared drives to connect, and no databases to set up. Copy the "
    "folder to your machine, open a terminal, and start."
)

add_code_block(
    "supplier-lifecycle-2026/\n"
    "+-- .claude/\n"
    "|   +-- settings.json\n"
    "|   +-- commands/\n"
    "|       +-- lifecycle-status.md\n"
    "|       +-- onboard-supplier.md\n"
    "|       +-- trigger-exit.md\n"
    "+-- CLAUDE.md\n"
    "+-- data/\n"
    "|   +-- supplier-master.csv          (30 suppliers)\n"
    "|   +-- performance-history.csv      (120 quarterly scores)\n"
    "|   +-- compliance-status.csv        (30 compliance records)\n"
    "|   +-- development-plans.csv        (10 active plans)\n"
    "+-- state/\n"
    "|   +-- lifecycle-state.json         (current stage per supplier)\n"
    "|   +-- transition-log.md            (stage change audit trail)\n"
    "+-- outputs/\n"
    "|   +-- segmentation-report.md\n"
    "|   +-- onboarding-checklists/\n"
    "|   +-- corrective-action-plans/\n"
    "|   +-- exit-plans/\n"
    "+-- skills/\n"
    "    +-- assess-lifecycle-stage.md\n"
    "    +-- detect-risk-triggers.md"
)

doc.add_heading("Folder-by-folder breakdown", level=3)

add_para(
    "data/ holds the four source CSV files. These files are read-only. Claude Code (in the terminal) "
    "reads them but never writes to them. The supplier-master.csv file has 30 rows, one per supplier, "
    "with fields for supplier ID, name, category, tier, lifecycle stage, annual spend, onboard date, "
    "last review date, and risk rating. The performance-history.csv file has 120 rows covering 30 "
    "suppliers across four quarters (2025-Q2 through 2026-Q1) with scores for quality, delivery, "
    "responsiveness, cost, and an overall composite. The compliance-status.csv file has 30 rows with "
    "fields for insurance, NDA, ISO certification, background check, financial review, and a composite "
    "compliance score. The development-plans.csv file has 10 rows for suppliers with active improvement "
    "or growth plans.",
    space_after=6,
)
add_para(
    "Why this matters. Without the data/ folder, Claude has nothing to read. Every prompt in this course "
    "references a specific file in data/ by name. If a file is missing or renamed, the prompt fails. "
    "The read-only rule protects your source data from accidental edits. If you corrupt a file during "
    "practice, the regenerator script in scripts/ rebuilds all four CSVs from scratch with one command.",
    italic=True,
    space_after=6,
)

add_para(
    "state/ holds two files that persist between sessions. lifecycle-state.json stores the current "
    "stage, last action date, decision status, and notes for every supplier. transition-log.md records "
    "every stage change with a timestamp and reason. Both files are written by Claude Code (in the "
    "terminal), not by you.",
    space_after=6,
)
add_para(
    "Why this matters. Without the state/ folder, every Claude Code session starts from zero. You "
    "would have to re-classify all 30 suppliers every time you open the terminal. The state file "
    "carries decisions forward. When you defer a decision on Friday and return on Monday, the state "
    "file remembers the deferral, the reason, and the date.",
    italic=True,
    space_after=6,
)

add_para(
    "outputs/ is where finished reports land. It has subfolders for onboarding checklists, corrective "
    "action plans, and exit plans. The segmentation report saves directly in outputs/ as "
    "segmentation-report.md.",
    space_after=6,
)
add_para(
    "Why this matters. Keeping outputs in their own folder means you always know where the finished "
    "work is. You do not have to search through drafts, data files, and state files to find the "
    "report your director asked for. Everything ready to share lives in outputs/.",
    italic=True,
    space_after=6,
)

add_para(
    "skills/ holds two reusable prompt patterns. assess-lifecycle-stage.md tells Claude how to "
    "evaluate a supplier's data and assign a stage. detect-risk-triggers.md tells Claude what "
    "performance thresholds trigger an at-risk flag. Both are referenced by the slash commands "
    "in .claude/commands/.",
    space_after=6,
)
add_para(
    "Why this matters. Skills make Claude Code (in the terminal) consistent. Without the skills, "
    "Claude might classify the same supplier differently depending on how you phrase the prompt. "
    "With the skills, the classification rules are fixed. Every run uses the same thresholds, "
    "the same stage definitions, and the same transition criteria.",
    italic=True,
    space_after=6,
)

add_para(
    "CLAUDE.md sits at the project root. It tells Claude Code (in the terminal) its role "
    "(Supplier Relationship Manager at Crestview Industries), the lifecycle stages and their "
    "transition criteria, the tier definitions, and the output standards (USD, YYYY-MM-DD dates, "
    "no em-dashes, three recommendations maximum). Claude reads this file automatically at the "
    "start of every session.",
    space_after=6,
)
add_para(
    "Why this matters. Without CLAUDE.md, you would need to paste the role description, the "
    "stage definitions, and the output rules into every prompt. With it, Claude already knows "
    "the rules before you type your first question. Your prompts stay short and focused on the "
    "task, not on repeating context.",
    italic=True,
    space_after=6,
)

# ═══════════════════════════════════════════════════════════════════════
# 4. TIME SAVINGS REFERENCE TABLE
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("Time Savings Reference Table", level=1)

add_para(
    "These estimates come from the Crestview Industries scenario. Your numbers will vary depending "
    "on supplier count, data quality, and how many lifecycle stages you actively manage. The pattern "
    "holds: tasks that involve reading multiple files, cross-referencing data, and producing formatted "
    "output are where Claude Code (in the terminal) saves the most time."
)

add_table(
    ["Task", "Without Claude Code", "With Claude Code", "Time saved"],
    [
        [
            "Classify 30 suppliers into 7 lifecycle stages using 3 CSV files",
            "4 to 5 hours (manual cross-referencing, stage assignment, data gap documentation)",
            "20 minutes (Claude reads all 3 files, classifies, flags gaps, saves report)",
            "3.5 to 4.5 hours",
        ],
        [
            "Run onboarding compliance check for one new supplier (12-item checklist)",
            "90 minutes (compare checklist to CSV, note gaps, draft follow-up email)",
            "12 minutes (Claude compares, flags missing items, drafts email)",
            "78 minutes",
        ],
        [
            "Build development plan review summary for a strategic supplier",
            "2 hours (read Word plan, pull performance data, compare targets, write summary)",
            "15 minutes (Claude reads plan and data, cross-references targets, writes summary)",
            "1 hour 45 minutes",
        ],
        [
            "Detect at-risk suppliers and draft a corrective action plan",
            "3 to 4 hours (scan scores, identify declines, pull spend context, draft CAP)",
            "20 minutes (Claude scans 120 rows, flags declines, drafts CAP with template)",
            "2.5 to 3.5 hours",
        ],
        [
            "Build exit transition timeline and notification letter for one supplier",
            "3 to 4 hours (pull order data, build timeline, draft letter, update records)",
            "15 minutes (Claude reads orders, builds 7-milestone timeline, drafts letter)",
            "2.75 to 3.75 hours",
        ],
    ],
    col_widths=[2.0, 1.7, 1.7, 1.2],
)

# ═══════════════════════════════════════════════════════════════════════
# 5. WHAT SUPPLIER LIFECYCLE MANAGEMENT IS
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("What Supplier Lifecycle Management Is", level=1)

add_para(
    "Supplier lifecycle management is the practice of tracking every supplier from first contact to "
    "final exit. Each supplier occupies exactly one stage at any time. Stages change when specific "
    "criteria are met: a compliance checklist is completed, a performance score drops below a threshold, "
    "a corrective action plan expires, or a business decision is made to terminate the relationship."
)

doc.add_heading("The seven stages", level=2)

add_table(
    ["Stage", "Entry criteria", "Exit criteria"],
    [
        [
            "Onboarding",
            "New supplier approved by procurement",
            "All compliance items complete, first order placed",
        ],
        [
            "Active",
            "Onboarding complete, compliance score above 70",
            "Performance drops below 60 for 2 consecutive quarters, or compliance lapses",
        ],
        [
            "Strategic",
            "Active supplier with overall score above 85 for 3+ quarters, annual spend above $2M",
            "Performance drops below 80, or strategic review recommends downgrade",
        ],
        [
            "At Risk",
            "Overall score below 60 for 2 consecutive quarters, or compliance score below 50",
            "Corrective action plan approved and accepted by supplier",
        ],
        [
            "Corrective Action",
            "At-risk supplier accepts improvement plan",
            "Targets met within 90 days (return to Active), or targets not met (move to Exit)",
        ],
        [
            "Exit",
            "Corrective action failed, or business decision to terminate",
            "All orders transitioned, final invoice settled, contract terminated",
        ],
        [
            "Under Review",
            "Data insufficient to assign a stage, or stage disputed",
            "Review complete, stage assigned",
        ],
    ],
    col_widths=[1.2, 2.7, 2.7],
)

doc.add_heading("Stage transitions", level=2)

add_para(
    "Transitions are not random. Each one follows a rule. A supplier moves from Active to At Risk "
    "only when its overall score falls below 60 for two consecutive quarters. A supplier moves from "
    "Corrective Action to Exit only when it fails to meet its improvement targets within the 90-day "
    "window. The CLAUDE.md file at the project root encodes these rules so that Claude Code (in the "
    "terminal) applies them consistently every time you run the lifecycle-status command."
)

doc.add_heading("State tracking", level=2)

add_para(
    "State tracking is the mechanism that makes lifecycle management work across sessions. Without "
    "it, every time you close Claude Code and reopen it, the system forgets what stage each supplier "
    "is in, which decisions you deferred, and which corrective action plans are in progress. The "
    "lifecycle-state.json file in state/ solves this. It stores the current stage, the last action "
    "date, the decision status (Current, Deferred, or CAP Issued), notes, and an append-only "
    "decision log for every supplier. Claude Code (in the terminal) reads this file at the start "
    "of every session and writes to it whenever a stage changes."
)

doc.add_heading("Tier definitions", level=2)

add_table(
    ["Tier", "Criteria"],
    [
        ["Strategic", "Annual spend above $2M, overall score above 85, critical category"],
        ["Preferred", "Annual spend $500K to $2M, overall score above 70"],
        ["Approved", "Annual spend below $500K, overall score above 60"],
        ["Conditional", "New supplier in onboarding, or supplier in corrective action"],
    ],
    col_widths=[1.5, 5.1],
)

# ═══════════════════════════════════════════════════════════════════════
# 6. WORKED EXAMPLES
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("Worked Examples", level=1)

add_para(
    "Each worked example has four parts: the prompt you type in Claude Code (in the terminal), "
    "the folder layout where applicable, what you should see when it succeeds, and what Claude "
    "did behind the scenes."
)

# ── Worked Example 1: Lifecycle segmentation ──────────────────────────
doc.add_heading("Worked Example 1: Classify 30 suppliers into lifecycle stages", level=2)

add_para(
    "You need a full segmentation report showing every supplier grouped by lifecycle stage. "
    "Your director wants it by Friday. The data lives in three CSV files in the data/ folder."
)

add_para("The prompt to type:", bold=True)
add_code_block(
    "Read data/supplier-master.csv, data/performance-history.csv, and\n"
    "data/compliance-status.csv. Classify each of the 30 suppliers into one\n"
    "of these seven lifecycle stages: Onboarding, Active, Strategic, At Risk,\n"
    "Corrective Action, Exit, Under Review. Use the stage definitions in\n"
    "CLAUDE.md. For each supplier, show: supplier name, stage, tier, overall\n"
    "score, and a one-line reason for the classification. Group by stage.\n"
    "Save to outputs/segmentation-report.md."
)

add_para("The folder layout:", bold=True)
add_code_block(
    "supplier-lifecycle-2026/\n"
    "+-- data/\n"
    "|   +-- supplier-master.csv          (30 rows, read-only)\n"
    "|   +-- performance-history.csv      (120 rows, read-only)\n"
    "|   +-- compliance-status.csv        (30 rows, read-only)\n"
    "+-- outputs/\n"
    "    +-- segmentation-report.md       (created by Claude)"
)

add_para("What you should see:", bold=True)
add_para(
    "Claude Code (in the terminal) confirms that outputs/segmentation-report.md has been saved. "
    "The report shows 30 suppliers grouped into seven sections: 3 in Onboarding, 15 in Active, "
    "3 in Strategic, 3 in At Risk, 2 in Corrective Action, 2 in Exit, and 2 in Under Review. "
    "Each supplier line includes the name, tier, overall score, and a one-line reason."
)

add_para("What Claude did, behind the scenes:", bold=True)
add_numbered(
    "Claude read the CLAUDE.md file at the project root and loaded the seven stage definitions, "
    "the transition criteria, and the tier definitions."
)
add_numbered(
    "Claude read supplier-master.csv (30 rows) and built a lookup table of supplier names, "
    "categories, tiers, annual spend, and current stage labels."
)
add_numbered(
    "Claude read performance-history.csv (120 rows) and computed the most recent two quarters "
    "of scores for each supplier. It flagged any supplier whose overall score dropped 10 or "
    "more points between consecutive quarters."
)
add_numbered(
    "Claude read compliance-status.csv (30 rows) and checked each supplier's compliance score. "
    "It flagged any supplier with a score below 50 or with missing items."
)
add_numbered(
    "Claude cross-referenced the three data sources and applied the stage rules: suppliers with "
    "incomplete compliance went to Onboarding, suppliers with stable scores above 60 and full "
    "compliance went to Active, suppliers with scores above 85 and spend above $2M went to "
    "Strategic, and so on."
)
add_numbered(
    "Claude grouped the 30 suppliers by stage, formatted the report with headers and one-line "
    "reasons, and saved it to outputs/segmentation-report.md."
)

# ── Worked Example 2: Corrective Action Plan ─────────────────────────
doc.add_heading("Worked Example 2: Draft a corrective action plan for an at-risk supplier", level=2)

add_para(
    "Apex Electronics (SUP004) has seen its quality score drop from 84 to 66 over two quarters. "
    "The supplier delivers $1,200,000 of electronic components annually. You need a formal "
    "corrective action plan with three improvement targets, a 90-day timeline, and review dates."
)

add_para("The prompt to type:", bold=True)
add_code_block(
    "Read data/performance-history.csv and data/supplier-master.csv.\n"
    "Find all performance rows for Apex Electronics (SUP004).\n"
    "Draft a corrective action plan with these details:\n"
    "- Supplier: Apex Electronics (SUP004)\n"
    "- Category: Electronic components\n"
    "- Annual spend: $1,200,000\n"
    "- Quality score trend: 84 (2025-Q3) to 66 (2026-Q1)\n"
    "- Three improvement targets:\n"
    "  1. Quality defect rate: current 3.0, goal 3.8, by 2026-06-30\n"
    "  2. On-time delivery: current 2.8, goal 3.5, by 2026-06-30\n"
    "  3. Weekly status reporting: goal 4 reports per month, by 2026-05-15\n"
    "- Review schedule: 30-day, 60-day, and 90-day checkpoints\n"
    "- Plan issued: 2026-04-25\n"
    "Save to outputs/corrective-action-plans/Apex_Electronics_CAP.md."
)

add_para("The folder layout:", bold=True)
add_code_block(
    "supplier-lifecycle-2026/\n"
    "+-- data/\n"
    "|   +-- performance-history.csv      (120 rows, read-only)\n"
    "|   +-- supplier-master.csv          (30 rows, read-only)\n"
    "+-- outputs/\n"
    "    +-- corrective-action-plans/\n"
    "        +-- Apex_Electronics_CAP.md  (created by Claude)"
)

add_para("What you should see:", bold=True)
add_para(
    "Claude Code (in the terminal) saves outputs/corrective-action-plans/Apex_Electronics_CAP.md. "
    "The plan includes the supplier details, a performance summary table showing three quarters of "
    "decline, three numbered improvement targets with metrics and deadlines, and a review schedule "
    "with 30-day (2026-05-25), 60-day (2026-06-25), and 90-day (2026-07-25) checkpoints. The "
    "escalation section names two alternative suppliers in case the plan fails."
)

add_para("What Claude did, behind the scenes:", bold=True)
add_numbered(
    "Claude read supplier-master.csv and pulled the Apex Electronics row: supplier ID SUP004, "
    "category Electronic Components, tier Preferred, annual spend $1,200,000."
)
add_numbered(
    "Claude read performance-history.csv and filtered to the three most recent quarters for "
    "Apex Electronics. It confirmed the quality score declined from 4.2 (2025-Q3) to 3.0 (2026-Q1), "
    "a drop of 1.2 points."
)
add_numbered(
    "Claude structured the corrective action plan using the three improvement targets from the "
    "prompt. It calculated the review dates by adding 30, 60, and 90 days to the issue date "
    "of 2026-04-25."
)
add_numbered(
    "Claude wrote the escalation section by scanning supplier-master.csv for other suppliers in "
    "the Electronic Components category with Active or Strategic status: Coastal Coatings (SUP010) "
    "and Summit Electrical (SUP025)."
)
add_numbered(
    "Claude formatted the plan with headers, a performance summary table, a targets table, "
    "the review schedule, and the escalation path. It saved the file to the corrective-action-plans "
    "subfolder under outputs/."
)

# ── Worked Example 3: Exit Transition Plan ────────────────────────────
doc.add_heading("Worked Example 3: Build an exit transition timeline", level=2)

add_para(
    "Regional Supply Co (SUP023) was flagged for exit after failing two corrective action plans. "
    "Three purchase orders totaling $85,700 are still active. The replacement supplier, Cascade "
    "Fasteners, begins delivery in six weeks. You need a transition timeline and an exit "
    "notification letter."
)

add_para("The prompt to type:", bold=True)
add_code_block(
    "Read data/supplier-master.csv. Find the row for Regional Supply Co.\n"
    "Today is 2026-04-25. Exit target date is 2026-07-31.\n"
    "Replacement supplier: Cascade Fasteners (SUP005), first delivery 2026-06-06.\n"
    "Open orders: PO-8842 ($42,000, due 2026-05-15), PO-8901 ($28,500, due 2026-06-01),\n"
    "PO-8955 ($15,200, due 2026-06-15). Total: $85,700.\n"
    "Build a transition timeline with seven milestones from notification\n"
    "through account closure. Then draft a formal exit notification letter\n"
    "listing the open POs, the final delivery deadline, and the invoice\n"
    "submission deadline. Note that this is a category consolidation,\n"
    "not a performance termination.\n"
    "Save the timeline to outputs/exit-plans/Regional_Supply_Co_Timeline.md.\n"
    "Save the letter to outputs/exit-plans/Regional_Supply_Co_Exit_Letter.md."
)

add_para("The folder layout:", bold=True)
add_code_block(
    "supplier-lifecycle-2026/\n"
    "+-- data/\n"
    "|   +-- supplier-master.csv          (30 rows, read-only)\n"
    "+-- outputs/\n"
    "    +-- exit-plans/\n"
    "        +-- Regional_Supply_Co_Timeline.md    (created by Claude)\n"
    "        +-- Regional_Supply_Co_Exit_Letter.md (created by Claude)"
)

add_para("What you should see:", bold=True)
add_para(
    "Claude Code (in the terminal) saves two files. The timeline shows seven milestones: "
    "notification (2026-04-25), PO freeze (2026-05-01), qualification of replacement (2026-05-01), "
    "PO-8842 transfer (2026-05-15), PO-8901 transfer (2026-06-01), PO-8955 transfer (2026-06-15), "
    "final invoice reconciliation (2026-07-01), and account deactivation (2026-07-31). The exit "
    "letter lists the three open POs with amounts and delivery dates, states the PO freeze date, "
    "gives the final invoice deadline, and includes the category consolidation context."
)

add_para("What Claude did, behind the scenes:", bold=True)
add_numbered(
    "Claude read supplier-master.csv and pulled the Regional Supply Co row: category Raw Materials, "
    "tier Standard, annual spend $300,000, exit flag set."
)
add_numbered(
    "Claude took the three open POs from the prompt and calculated the total ($85,700). It "
    "sequenced the milestones by delivery date to build a logical transition order."
)
add_numbered(
    "Claude identified Cascade Fasteners as the replacement supplier from supplier-master.csv, "
    "confirmed Cascade's status (Active, tier Preferred), and noted the first delivery date of "
    "2026-06-06."
)
add_numbered(
    "Claude built the seven-milestone timeline as a date-action-owner table. It used [Owner Name] "
    "as a placeholder for the owner column since the prompt did not specify individual names."
)
add_numbered(
    "Claude drafted the exit notification letter with a professional tone, listing the three POs, "
    "the PO freeze date, the final invoice deadline, and the category consolidation context. "
    "It saved both files to outputs/exit-plans/."
)

# ═══════════════════════════════════════════════════════════════════════
# 7. DAY IN THE LIFE
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("A Day in the Life: Sarah Chen, Senior Supplier Relationship Manager", level=1)

add_para(
    "Sarah Chen is a Senior Supplier Relationship Manager at a US-based industrial manufacturer "
    "with $42M in annual supplier spend across 35 suppliers. She reports to the VP of Procurement. "
    "She has used Claude Code (in the terminal) for three weeks. Today is a typical Thursday."
)

# Scenario 1
doc.add_heading("07:45 - The VP's inbox surprise", level=3)
add_para(
    "Sarah checks her email before coffee. The VP of Operations forwarded a complaint from the "
    "Austin plant: \"Precision Tooling missed their third delivery this quarter. Why are they "
    "still active?\" Sarah opens Claude Code in her supplier-lifecycle-2026/ project folder."
)
add_code_block(
    "Read data/performance-history.csv. Show me the last four quarters of\n"
    "scores for Precision Tooling. Include quality, delivery, and overall.\n"
    "Tell me if the delivery score dropped 10 or more points in the last\n"
    "two quarters."
)
add_para(
    "Claude Code (in the terminal) reports that Precision Tooling's delivery score fell from 78 to "
    "54 between 2025-Q4 and 2026-Q1, a drop of 24 points. The overall score is now 58, below the "
    "60-point at-risk threshold for two consecutive quarters. Sarah forwards the data to the VP "
    "with a note: \"Precision Tooling meets at-risk criteria. I am initiating a corrective action "
    "plan today.\" Time spent: 4 minutes."
)
add_para(
    "What to learn from this. Claude Code (in the terminal) turns a question from a VP into "
    "a data-backed answer in under five minutes. Without it, Sarah would have opened the CSV in "
    "Excel, filtered by supplier name, eyeballed four quarters of numbers, and typed her reply. "
    "The speed matters because the VP sees a response before the morning stand-up, not after lunch.",
    italic=True,
)

# Scenario 2
doc.add_heading("08:30 - Onboarding check for a new supplier", level=3)
add_para(
    "The buyer for the Packaging category sends Sarah a message: \"Atlas Containers was approved "
    "last week. When can they start receiving POs?\" Sarah needs to check if the compliance "
    "checklist is complete."
)
add_code_block(
    "Read data/compliance-status.csv. Find the row for Atlas Containers.\n"
    "List every compliance field and its status. Flag any item that is\n"
    "blank, expired, or incomplete. Tell me how many of the 8 checklist\n"
    "items are complete."
)
add_para(
    "Claude reports 6 of 8 items complete. The ISO 9001 certificate and the financial review "
    "(D&B report) are missing. Sarah tells the buyer: \"Atlas Containers is at 75% onboarding "
    "completion. Two items outstanding: ISO 9001 certificate and financial review. I will follow "
    "up with the supplier today.\" She then asks Claude to draft the follow-up email."
)
add_code_block(
    "Draft a follow-up email to Atlas Containers. List only the two missing\n"
    "items: ISO 9001 certificate and financial review (D&B report). Deadline:\n"
    "2026-05-09. Address to [Onboarding Contact Name]. Sign from me as\n"
    "Senior Supplier Relationship Manager.\n"
    "Save to outputs/onboarding-checklists/Atlas_Containers_Followup.md."
)
add_para(
    "Claude saves the email. Sarah reviews it, swaps in the contact name, and sends it from "
    "Outlook. Time spent: 8 minutes."
)
add_para(
    "What to learn from this. The compliance check and the follow-up email are separate prompts, "
    "not one giant instruction. Breaking work into two steps lets Sarah review the data before "
    "drafting the email. If the compliance data looked wrong, she would fix the CSV before wasting "
    "time on an email that references wrong items.",
    italic=True,
)

# Scenario 3
doc.add_heading("10:00 - CPO asks for the strategic review pack", level=3)
add_para(
    "The CPO walks by Sarah's desk: \"The Heartland Polymers review is next Thursday. Can you "
    "have the summary ready by end of day?\" Sarah has the development plan in a Word document "
    "and the performance data in CSV. Pulling it together by hand would take two hours."
)
add_code_block(
    "Read data/development-plans.csv. Show me all columns for Heartland\n"
    "Polymers. Then read data/performance-history.csv and find all rows\n"
    "for Heartland Polymers. For each improvement target in the development\n"
    "plan, tell me whether the most recent performance data shows On Track,\n"
    "Behind, or Met. Write a one-page status summary with: supplier name,\n"
    "review date, target counts by status, a three-row target table\n"
    "(Target, Goal, Current Status), and one recommendation (three\n"
    "sentences max). Save to outputs/Heartland_Polymers_Review_Summary.md."
)
add_para(
    "Claude produces the summary in 45 seconds. One target (delivery on-time rate) is On Track "
    "at 93% against a 94% goal. One target (defect rate) is Behind at 1.4% against a 1.0% goal. "
    "One target (portal adoption) is Behind at 72% against a 100% goal. Sarah edits the "
    "recommendation paragraph, saves as a PDF, and emails it to the CPO. Time spent: 12 minutes."
)
add_para(
    "What to learn from this. Claude Code (in the terminal) cross-references two different data "
    "sources in a single prompt. The key is naming both files explicitly and telling Claude what "
    "to compare. \"For each improvement target in the development plan, tell me whether the most "
    "recent performance data shows On Track, Behind, or Met\" is the sentence that connects the "
    "plan to the data. Without that sentence, Claude would summarize each file separately.",
    italic=True,
)

# Scenario 4
doc.add_heading("13:30 - Corrective action plan due today", level=3)
add_para(
    "Sarah's calendar reminder pops up: \"Frontier Machining CAP: 90-day review due today.\" "
    "She needs to check whether Frontier met its three targets."
)
add_code_block(
    "Read state/lifecycle-state.json. Show me the full record for Frontier\n"
    "Machining, including the Decision_Log. Then read data/performance-history.csv\n"
    "and show me Frontier Machining's scores for 2026-Q1. Did the quality\n"
    "score reach 3.5? Did the delivery score reach 3.2? Were monthly status\n"
    "reports submitted (check notes in the state file)?"
)
add_para(
    "Claude reports: quality score 3.6 (target 3.5, Met), delivery score 3.0 (target 3.2, "
    "Behind by 0.2 points), status reports submitted 3 of 4 months (Behind). Two of three targets "
    "are not met. Per the escalation rules, Sarah should consider extending the corrective action "
    "period or initiating exit planning. She decides to extend by 30 days."
)
add_code_block(
    "Update state/lifecycle-state.json for Frontier Machining.\n"
    "Decision_Status = \"CAP Extended\". Last_Action_Date = 2026-04-25.\n"
    "Notes = \"90-day review: 1 of 3 targets met. CAP extended 30 days to\n"
    "2026-05-25. Quality met (3.6). Delivery behind (3.0 vs 3.2). Reports\n"
    "behind (3 of 4).\"\n"
    "Append to Decision_Log: date 2026-04-25, action \"CAP extended 30 days\",\n"
    "approved_by \"Sarah Chen\", notes \"Director approved extension verbally.\"\n"
    "Save the file."
)
add_para(
    "Claude updates the state file. The decision is now recorded. If Sarah's colleague opens "
    "Claude Code tomorrow and asks about Frontier Machining, the state file shows the extension, "
    "the reason, and the new deadline. Time spent: 10 minutes."
)
add_para(
    "What to learn from this. The state file is the audit trail. Sarah did not just make a "
    "decision. She recorded the decision, the date, the approver, and the reasoning in a "
    "structured format that survives between sessions. When the director asks next week \"why "
    "did we extend Frontier Machining?\", the answer is in the Decision_Log, not in Sarah's memory.",
    italic=True,
)

# Scenario 5
doc.add_heading("15:00 - Exit planning for an underperforming supplier", level=3)
add_para(
    "Sarah's director sends a one-line Slack message: \"Pull the trigger on Regional Supply Co. "
    "Get me a transition plan by close of business.\" Sarah has been expecting this. Regional "
    "Supply Co has $85,700 in open orders and a target exit date of 2026-07-31."
)
add_code_block(
    "Read data/supplier-master.csv. Find Regional Supply Co.\n"
    "Open orders: PO-8842 ($42,000, 2026-05-15), PO-8901 ($28,500, 2026-06-01),\n"
    "PO-8955 ($15,200, 2026-06-15). Total $85,700.\n"
    "Replacement: Cascade Fasteners (SUP005), first delivery 2026-06-06.\n"
    "Build a 7-milestone transition timeline from 2026-04-25 to 2026-07-31.\n"
    "Save to outputs/exit-plans/Regional_Supply_Co_Timeline.md.\n"
    "Then draft a formal exit notification letter. This is a category\n"
    "consolidation, not a performance termination. Save to\n"
    "outputs/exit-plans/Regional_Supply_Co_Exit_Letter.md."
)
add_para(
    "Claude produces both files. Sarah reviews the timeline, adds the owner names for each "
    "milestone, and saves the letter as a PDF. She emails the transition plan to her director "
    "and the exit letter to Regional Supply Co's account manager. Time spent: 15 minutes."
)
add_para(
    "What to learn from this. Exit planning has a specific structure: open orders, alternative "
    "supplier, milestone timeline, and notification letter. Once you know the structure, the "
    "prompt writes itself. The prompt did not ask Claude to \"figure out how to exit a supplier.\" "
    "It gave Claude the data points and the structure, and Claude filled them in. That is the "
    "pattern for every lifecycle task: you provide the what, Claude provides the how.",
    italic=True,
)

# Scenario 6
doc.add_heading("16:15 - End-of-day state snapshot", level=3)
add_para(
    "Before closing her laptop, Sarah wants to make sure all of today's decisions are recorded "
    "in the state file."
)
add_code_block(
    "Read state/lifecycle-state.json. List every supplier where\n"
    "Last_Action_Date is 2026-04-25. For each, show: Supplier_Name,\n"
    "Stage, Decision_Status, and the most recent Decision_Log entry."
)
add_para(
    "Claude lists four suppliers updated today: Precision Tooling (moved to At Risk), Atlas "
    "Containers (onboarding follow-up sent), Frontier Machining (CAP extended), and Regional "
    "Supply Co (exit initiated). Sarah confirms the list matches her memory of the day. "
    "She closes Claude Code and resumes OneDrive sync. Time spent: 3 minutes."
)
add_para(
    "What to learn from this. The end-of-day review is a habit, not a chore. It takes three "
    "minutes and catches any decision that was made but not recorded. If Sarah had forgotten "
    "to update Precision Tooling's status earlier, this prompt would reveal the gap. The state "
    "file is only useful if it is current. A three-minute review at 16:15 keeps it current.",
    italic=True,
)

# Scenario 7
doc.add_heading("16:30 - Quick lifecycle status check for the weekly report", level=3)
add_para(
    "Sarah's weekly status report to the VP is due by end of day Friday. She runs a quick "
    "preview to see if the numbers look right."
)
add_code_block(
    "Read state/lifecycle-state.json. Count the suppliers in each lifecycle\n"
    "stage. Show a summary table: Stage, Count. Flag any stage where the\n"
    "count changed since last week (compare against the transition-log.md\n"
    "entries from the past 7 days)."
)
add_para(
    "Claude reports: Onboarding 4, Active 14, Strategic 3, At Risk 4, Corrective Action 2, "
    "Exit 3, Under Review 2. Changes this week: At Risk increased by 1 (Precision Tooling "
    "added), Exit increased by 1 (Regional Supply Co moved from Corrective Action). Sarah "
    "copies the summary into her weekly report template. Time spent: 3 minutes."
)
add_para(
    "What to learn from this. The weekly report is a byproduct of good state tracking, not "
    "a separate data-gathering exercise. Because every decision was recorded in the state file "
    "as it happened, the weekly summary is just a count and a diff. No spreadsheet archaeology. "
    "No asking colleagues what changed. The state file already knows.",
    italic=True,
)

# ═══════════════════════════════════════════════════════════════════════
# 8. 20-MINUTE SPRINT
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("20-Minute Sprint: Your First Lifecycle Status Report", level=1)

add_para(
    "This sprint gets you from a fresh install to your first usable lifecycle report in 20 minutes. "
    "You do not need to complete the full course first. If you have Claude Code (in the terminal) "
    "installed and the course folder on your machine, you can start now."
)

doc.add_heading("Minutes 0 to 5: Install and folder setup", level=3)
add_numbered(
    "Confirm Claude Code is installed. Open a terminal and type: claude --version. You should "
    "see a version number (for example, 1.0.33). If you see \"command not found,\" install Claude "
    "Code first. See Course 01 for instructions."
)
add_numbered(
    "Copy the supplier-lifecycle-2026/ folder to a local directory on your machine. Do not run "
    "it from OneDrive directly. Copy it to C:/Projects/ or your home directory."
)
add_numbered(
    "Open a terminal and navigate to the project folder: cd supplier-lifecycle-2026"
)
add_numbered(
    "Pause OneDrive sync if the folder is inside a synced location."
)

doc.add_heading("Minutes 5 to 10: Start Claude Code and read the data", level=3)
add_numbered(
    "Start Claude Code: type claude and press Enter. You should see the Claude Code prompt."
)
add_numbered("Type the following prompt and press Enter:")
add_code_block(
    "Read data/supplier-master.csv, data/performance-history.csv, and\n"
    "data/compliance-status.csv. Tell me: how many rows in each file,\n"
    "what are the column headers, and are there any blank or missing values?"
)
add_numbered(
    "Claude should report 30, 120, and 30 rows respectively. It will list the column headers "
    "for each file and flag any blanks. If it reports \"file not found,\" check that you are "
    "in the supplier-lifecycle-2026/ directory, not a subdirectory."
)

doc.add_heading("Minutes 10 to 15: Run the segmentation", level=3)
add_numbered("Type the following prompt and press Enter:")
add_code_block(
    "Using the stage definitions in CLAUDE.md, classify each of the 30\n"
    "suppliers into one of seven lifecycle stages: Onboarding, Active,\n"
    "Strategic, At Risk, Corrective Action, Exit, Under Review.\n"
    "Show a summary table: Stage, Count, Supplier Names. Then list any\n"
    "suppliers where the stage could not be determined.\n"
    "Save to outputs/segmentation-report.md."
)
add_numbered(
    "Claude should produce a summary table and save the report. The counts should roughly match: "
    "3 Onboarding, 15 Active, 3 Strategic, 3 At Risk, 2 Corrective Action, 2 Exit, 2 Under Review."
)

doc.add_heading("Minutes 15 to 20: Review and next steps", level=3)
add_numbered(
    "Open outputs/segmentation-report.md in any text editor. Read through the classifications. "
    "Do the stages make sense based on the data? If a supplier seems misclassified, note it."
)
add_numbered(
    "Pick one at-risk supplier from the report. Ask Claude for more detail:"
)
add_code_block(
    "Show me the last four quarters of performance scores for\n"
    "Apex Electronics. What was the trend? When did it cross\n"
    "the at-risk threshold?"
)
add_numbered(
    "You now have a segmentation report and a detailed view of one at-risk supplier. "
    "From here, continue to the onboarding automation session or the at-risk detection "
    "and corrective action session, depending on what your portfolio needs most."
)

# ═══════════════════════════════════════════════════════════════════════
# 9. FIRST WEEK DAY-BY-DAY PLANNER
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("First Week Day-by-Day Planner", level=1)

add_para(
    "This planner assumes you spend 60 to 90 minutes per day on the course. Each day builds "
    "on the previous one. By Friday, you have a working lifecycle management system with state "
    "persistence."
)

doc.add_heading("Day 1 (Monday): Install, folder setup, first segmentation", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Install Claude Code (in the terminal) if not already installed.")
add_bullet("Copy the course folder to your machine.")
add_bullet("Run the 20-Minute Sprint above.")
add_bullet("Complete the Supplier Segmentation session (55 minutes).")
add_para(
    "By end of day, you have a segmentation report showing all 30 suppliers classified by "
    "lifecycle stage. You have seen Claude Code read three CSV files, cross-reference them, "
    "and produce a formatted summary."
)

doc.add_heading("Day 2 (Tuesday): Onboarding and compliance", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Complete the Onboarding Automation session (50 minutes).")
add_bullet("Run an onboarding check on Summit Electrical.")
add_bullet("Draft a follow-up email for missing compliance items.")
add_bullet("Update the segmentation file with the follow-up details.")
add_para(
    "By end of day, you have run a compliance check, identified missing items, and drafted a "
    "follow-up email. You understand how Claude Code (in the terminal) compares a checklist "
    "template against actual data."
)

doc.add_heading("Day 3 (Wednesday): Strategic reviews and at-risk detection", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Complete the Strategic Development Plans session (55 minutes).")
add_bullet("Complete the At-Risk Detection and Corrective Action session (60 minutes, may extend into Thursday).")
add_bullet("Build a review summary for Heartland Polymers.")
add_bullet("Scan for at-risk suppliers and draft a corrective action plan for Apex Electronics.")
add_para(
    "By end of day, you have produced a CPO-ready review summary and a corrective action plan. "
    "You understand how Claude Code (in the terminal) detects performance declines by comparing "
    "scores across quarters."
)

doc.add_heading("Day 4 (Thursday): Exit management and state persistence", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Complete the Exit Management session (50 minutes).")
add_bullet("Build a transition timeline and exit letter for Regional Supply Co.")
add_bullet("Start the State Persistence session (first 30 minutes).")
add_bullet("Initialize the lifecycle-state.json file.")
add_para(
    "By end of day, you have a complete exit plan with milestones and a formal notification "
    "letter. You have also created the state file that will carry decisions into future sessions."
)

doc.add_heading("Day 5 (Friday): State persistence, review, and plan", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Finish the State Persistence session (remaining 20 minutes).")
add_bullet("Record two decisions in the state file (one current, one deferred).")
add_bullet("Close and reopen Claude Code to verify persistence works.")
add_bullet("Run a full lifecycle status check using the state file.")
add_bullet("Plan which of your real suppliers you will migrate to this system next week.")
add_para(
    "By end of day, you have a working lifecycle management system. The state file remembers "
    "every decision. You have verified that closing and reopening Claude Code does not lose "
    "data. You have a plan for applying this to your actual supplier portfolio."
)

# ═══════════════════════════════════════════════════════════════════════
# 10. THE PATTERN
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("The Pattern: How to Apply This to Your Own Suppliers", level=1)

add_para(
    "The techniques in this course work for any supplier portfolio, not just the Crestview "
    "Industries practice data. The pattern has three parts: set up the folder, configure the "
    "context, and run the lifecycle commands."
)

doc.add_heading("Part 1: Set up the folder", level=2)
add_para(
    "Create a project folder with the same structure used in the course. The folder needs "
    "four subfolders: data/ for read-only source files, state/ for the lifecycle state, "
    "outputs/ for reports and plans, and skills/ for reusable prompt patterns."
)
add_code_block(
    "your-company-supplier-lifecycle/\n"
    "+-- CLAUDE.md\n"
    "+-- data/\n"
    "|   +-- supplier-master.csv\n"
    "|   +-- performance-history.csv\n"
    "|   +-- compliance-status.csv\n"
    "+-- state/\n"
    "|   +-- lifecycle-state.json\n"
    "+-- outputs/\n"
    "+-- skills/"
)
add_para(
    "Export your supplier data from your ERP or procurement system as CSV files. The column "
    "names do not have to match the course exactly. Claude Code (in the terminal) reads the "
    "column headers and adapts. The important thing is that each file has a supplier name or "
    "ID column that Claude can use to join the files together."
)

doc.add_heading("Part 2: Configure the context", level=2)
add_para(
    "Write a CLAUDE.md file at the project root. This file tells Claude Code (in the terminal) "
    "your role, your company name, the lifecycle stages you use, the transition criteria, "
    "the tier definitions, and the output standards. Use the Crestview CLAUDE.md as a template. "
    "Replace the company name, the spend figure, the supplier count, and the stage definitions "
    "with your own."
)
add_para(
    "If your company uses different stages (for example, five stages instead of seven, or "
    "different names like \"Probation\" instead of \"Corrective Action\"), update the stage table "
    "in CLAUDE.md. Claude Code (in the terminal) will use whatever definitions you provide."
)

doc.add_heading("Part 3: Run the lifecycle commands", level=2)
add_para(
    "The prompts from the course work with your own data. Swap the file names and supplier "
    "names. The structure stays the same: tell Claude which files to read, which supplier to "
    "focus on, and what output to produce."
)
add_para(
    "Three recommendations for your first week with real data:"
)
add_numbered(
    "Start with the segmentation. Run the lifecycle-status prompt against your full supplier "
    "list. Review every classification. Fix any misclassifications by adjusting the stage "
    "criteria in CLAUDE.md."
)
add_numbered(
    "Focus on one lifecycle stage per day. Monday: check all onboarding suppliers. Tuesday: "
    "review all at-risk suppliers. Wednesday: update development plans for strategic suppliers. "
    "This keeps the workload manageable and lets you refine the prompts as you go."
)
add_numbered(
    "Initialize the state file on Day 1 and update it after every decision. The state file "
    "only works if you use it consistently. A state file that falls behind the real world is "
    "worse than no state file, because it gives you false confidence."
)

# ═══════════════════════════════════════════════════════════════════════
# 11. CAUTIONS AND GROUND RULES / TROUBLESHOOTING
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("Troubleshooting", level=1)

add_para(
    "These are the most common problems learners hit during the course and in the first week "
    "of real use. Each entry has a symptom and a fix."
)

# Entry 1
add_para("1. Claude classifies most suppliers as Active, even though some are clearly at risk.", bold=True)
add_para(
    "Symptom: The segmentation report shows 25 Active suppliers and only 1 or 2 in other stages."
)
add_para(
    "Fix: Check the performance-history.csv date column. Claude Code (in the terminal) needs to "
    "compare scores across two consecutive quarters to detect declines. If the date column is "
    "labeled \"Period\" instead of \"Quarter,\" Claude may not sort it correctly. Add the column "
    "name to your prompt: \"The date column is called Period, in format YYYY-QN.\" Also check "
    "that CLAUDE.md has the correct thresholds. If your at-risk threshold is 60 but all your "
    "suppliers score above 65, the threshold is too low for your data."
)

# Entry 2
add_para("2. The state file does not persist between sessions.", bold=True)
add_para(
    "Symptom: You close Claude Code, reopen it, and ask about a deferred decision. Claude says "
    "it has no information about that supplier."
)
add_para(
    "Fix: Claude Code (in the terminal) does not automatically read files at startup. Your first "
    "prompt in every session must include: \"Read state/lifecycle-state.json. This file is the "
    "current truth for all supplier stages and decisions.\" Alternatively, add that instruction "
    "to the CLAUDE.md file at the project root. Claude reads CLAUDE.md automatically, and if "
    "CLAUDE.md tells Claude to read the state file, it will."
)

# Entry 3
add_para("3. Claude updated the wrong supplier's row in the state file.", bold=True)
add_para(
    "Symptom: You asked Claude to update Apex Electronics, but a different supplier's record "
    "also changed."
)
add_para(
    "Fix: Always include the exact supplier name in your update prompt: \"Update only the record "
    "where Supplier_Name equals exactly 'Apex Electronics'.\" After every update, verify by asking: "
    "\"Read state/lifecycle-state.json and list every supplier where Last_Action_Date is today.\" "
    "If more than the expected suppliers appear, ask Claude to show the diff between the current "
    "file and the previous version."
)

# Entry 4
add_para("4. The corrective action plan saved as a blank .docx file.", bold=True)
add_para(
    "Symptom: You open the .docx file in Word and it is empty or has garbled content."
)
add_para(
    "Fix: Claude Code (in the terminal) generates .docx files using the python-docx library. "
    "If the template file uses Word form controls or content controls, Claude cannot populate "
    "them. Ask Claude to save as a plain .md (Markdown) file instead. You can paste the content "
    "into your Word template manually. Alternatively, re-save your template as a plain .docx "
    "without form protection (File, Save As, uncheck form protection)."
)

# Entry 5
add_para("5. OneDrive creates a sync conflict on the state file.", bold=True)
add_para(
    "Symptom: You see a file named lifecycle-state-DESKTOP-AB12.json alongside "
    "lifecycle-state.json."
)
add_para(
    "Fix: Pause OneDrive sync before starting Claude Code. Resume it after you close the session. "
    "If a conflict file already exists, ask Claude to compare both files: \"Read "
    "state/lifecycle-state.json and state/lifecycle-state-DESKTOP-AB12.json. For each supplier "
    "where the records differ, show me the difference.\" Manually merge the correct entries, "
    "delete the conflict file, and resume sync."
)

# Entry 6
add_para("6. Claude reports \"file not found\" for a CSV file.", bold=True)
add_para(
    "Symptom: Claude says it cannot find data/supplier-master.csv."
)
add_para(
    "Fix: Check three things. First, confirm you started Claude Code in the project root "
    "(supplier-lifecycle-2026/), not in a subdirectory like data/. Second, check the exact file "
    "name including hyphens, underscores, and capitalization. \"supplier-master.csv\" is not the "
    "same as \"Supplier_Master.csv\" on Mac and Linux. Third, check that the file was not deleted "
    "during a previous practice run. If it was, run the regenerator script in scripts/ to restore it."
)

# ═══════════════════════════════════════════════════════════════════════
# 12. DONE CHECKLIST
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("Done Checklist", level=1)

add_para(
    "This checklist was run before this handout was finalized. Each item is marked done, "
    "deferred, or N/A."
)

checklist_items = [
    ("1. The S2P problem is named in the first section.", "Done"),
    ("2. The outcome is stated in business terms before any command appears.", "Done"),
    ("3. Every S2P task has a worked example with four parts: prompt, folder layout, expected result, behind-the-scenes walkthrough.", "Done"),
    ("4. Every capability statement names the specific Claude: Claude Code (in the terminal).", "Done"),
    ("5. For lessons, every step has: what you do, what you type, what you see.", "N/A (handout, not lesson)"),
    ("6. At least one full worked example with realistic fake data.", "Done (three worked examples)"),
    ("7. Troubleshooting section present with five or more entries.", "Done (six entries)"),
    ("8. No em-dashes or en-dashes anywhere.", "Done"),
    ("9. No banned phrases.", "Done"),
    ("10. Oxford commas applied everywhere.", "Done"),
    ("11. No rhetorical questions as openers.", "Done"),
    ("12. Risk and issue text in active voice.", "Done"),
    ("13. Every figure is a real number.", "Done"),
    ("14. Sample executive summaries name a supplier, a value, and a date.", "Done"),
    ("15. Recommendation lists capped at three.", "Done"),
    ("16. File names follow naming convention.", "Done"),
    ("17. Screenshots cropped, captioned, fake data.", "N/A (no screenshots in this handout)"),
    ("18. Standard folder layout used (data/ for source, state/ for persistence, outputs/ for finals).", "Done"),
    ("19. Readable by a procurement analyst with no coding background.", "Done"),
    ("20. Time savings table, Day in the Life, 20-Minute Sprint, First Week Planner all present.", "Done"),
    ("21. Course-specific rules (self-contained folder, practice depth, data volumes).", "N/A (handout, not course folder)"),
    ("22. Style check passes.", "Done"),
    ("23. Every concept explanation has a Why this matters paragraph.", "Done"),
    ("24. Every Day-in-the-Life scenario ends with What to learn from this.", "Done"),
]

add_table(
    ["Item", "Status"],
    [(item, status) for item, status in checklist_items],
    col_widths=[5.5, 1.1],
)

# ── Footer ─────────────────────────────────────────────────────────────
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("U2xAI  |  PROCUREAI ACADEMY  |  Course 14: Supplier Lifecycle Management")
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
run.font.name = "Calibri"
p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = p2.add_run("Confidential. For training purposes only. Do not distribute outside the program.")
run2.font.size = Pt(8)
run2.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
run2.font.name = "Calibri"

# ── Save ───────────────────────────────────────────────────────────────
doc.save(str(OUT))
print(f"Saved to {OUT}")
print(f"File size: {OUT.stat().st_size:,} bytes")
