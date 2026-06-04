"""
Build Course 18: Savings Program Management Handout as .docx
Run: python scripts/build_course18_handout.py
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

HANDOUT_DIR = Path(__file__).resolve().parent.parent / "Handouts"
HANDOUT_DIR.mkdir(exist_ok=True)
OUT = HANDOUT_DIR / "Course_18_Savings_Program_Management_Handout.docx"

doc = Document()

# ── Global styles ──────────────────────────────────────────────
style = doc.styles["Normal"]
font = style.font
font.name = "Calibri"
font.size = Pt(11)
font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

for level in range(1, 4):
    h = doc.styles[f"Heading {level}"]
    h.font.name = "Calibri"
    h.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
    h.font.bold = True
    if level == 1:
        h.font.size = Pt(20)
        h.paragraph_format.space_before = Pt(18)
    elif level == 2:
        h.font.size = Pt(15)
        h.paragraph_format.space_before = Pt(14)
    else:
        h.font.size = Pt(12)
        h.paragraph_format.space_before = Pt(10)


def add_para(text, bold=False, italic=False, size=None, color=None,
             alignment=None, space_after=None, space_before=None, style_name=None):
    p = doc.add_paragraph(style=style_name) if style_name else doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    if size:
        run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    if alignment is not None:
        p.alignment = alignment
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    if space_before is not None:
        p.paragraph_format.space_before = Pt(space_before)
    return p


def add_rich_para(segments, space_after=None, space_before=None, alignment=None):
    """Add a paragraph with mixed bold/normal/italic runs.
    segments is a list of (text, bold, italic) tuples.
    """
    p = doc.add_paragraph()
    for text, bld, ital in segments:
        run = p.add_run(text)
        run.bold = bld
        run.italic = ital
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    if space_before is not None:
        p.paragraph_format.space_before = Pt(space_before)
    if alignment is not None:
        p.alignment = alignment
    return p


def add_code_block(text):
    """Add a code block with monospace font and gray background."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F2F2F2" w:val="clear"/>')
    p.paragraph_format.element.get_or_add_pPr().append(shading)
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
    return p


def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
        p.add_run(text)
    else:
        p.add_run(text)
    return p


def add_numbered(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Number")
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
        p.add_run(text)
    else:
        p.add_run(text)
    return p


def add_table(headers, rows, col_widths=None):
    """Add a formatted table."""
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.style = "Table Grid"

    for i, h_text in enumerate(headers):
        cell = tbl.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h_text)
        run.bold = True
        run.font.size = Pt(10)
        run.font.name = "Calibri"
        shading = parse_xml(
            f'<w:shd {nsdecls("w")} w:fill="1B3A5C" w:val="clear"/>'
        )
        cell._tc.get_or_add_tcPr().append(shading)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            run = cell.paragraphs[0].add_run(str(val))
            run.font.size = Pt(10)
            run.font.name = "Calibri"
            if r_idx % 2 == 1:
                shading = parse_xml(
                    f'<w:shd {nsdecls("w")} w:fill="F5F7FA" w:val="clear"/>'
                )
                cell._tc.get_or_add_tcPr().append(shading)

    if col_widths:
        for i, w in enumerate(col_widths):
            for row in tbl.rows:
                row.cells[i].width = Inches(w)

    doc.add_paragraph()  # spacing after table
    return tbl


def add_hr():
    """Add a horizontal rule."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="4" w:space="1" w:color="1B3A5C"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)


# ================================================================
#  HEADER
# ================================================================
add_para("U2xAI", bold=True, size=10, color=(0x88, 0x88, 0x88),
         alignment=WD_ALIGN_PARAGRAPH.CENTER)
add_para("PROCUREAI ACADEMY", bold=True, size=12, color=(0x1B, 0x3A, 0x5C),
         alignment=WD_ALIGN_PARAGRAPH.CENTER)
add_para("Course 18: Savings Program Management", bold=True, size=22,
         color=(0x1B, 0x3A, 0x5C), alignment=WD_ALIGN_PARAGRAPH.CENTER,
         space_after=4)
add_para("Comprehensive Training Guide", italic=True, size=12,
         color=(0x55, 0x55, 0x55), alignment=WD_ALIGN_PARAGRAPH.CENTER,
         space_after=4)
add_para("Version 1.0  |  April 2026  |  Claude Code (in the terminal)",
         size=10, color=(0x77, 0x77, 0x77),
         alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

add_hr()

# ================================================================
#  HOW TO USE THIS HANDOUT
# ================================================================
doc.add_heading("How to Use This Handout", level=1)

add_para(
    "This handout is the companion guide for Course 18: Savings Program Management. "
    "It covers every concept, prompt, and technique taught in the five course lessons. "
    "You can use it three ways."
)
add_numbered(
    "As a pre-read. Skim the time savings table and the Day in the Life section before you start the course. "
    "You will know what you are building and why it matters before you type your first prompt."
)
add_numbered(
    "As a desk reference during the course. Each worked example in this handout matches a lesson in the course. "
    "Keep it open alongside your terminal so you can check prompts, folder layouts, and expected outputs."
)
add_numbered(
    "As a standalone refresher after the course. If you finished the course weeks ago and need to run a monthly "
    "savings refresh for a new quarter, this handout has every prompt ready to copy."
)

add_para(
    "Every example in this handout uses Claude Code (in the terminal). The prompts are typed directly into the "
    "Claude Code command line. They do not work in Claude AI Web (claude.ai in a browser) or Claude Desktop "
    "with Cowork unless you adapt the file paths and folder references. Where a feature differs between the "
    "three, this handout names which one it applies to."
)

# ================================================================
#  WHAT THIS COURSE TEACHES
# ================================================================
doc.add_heading("What This Course Teaches", level=1)

add_para(
    "A savings program manager at a US manufacturer tracks $12M in annual savings across eight sourcing "
    "initiatives. Five are hard savings with contracted rates you can verify against transaction data. "
    "One is demand reduction (soft savings). One is specification standardization (cost avoidance). "
    "One is payment terms extension (working capital). The CFO review is next Tuesday. She wants three "
    "things: how much you saved this year, whether you will hit the target, and what went wrong with the "
    "initiatives that are behind."
)

add_para(
    "Without Claude Code (in the terminal), this work takes two to three days. You pull transactions for "
    "each initiative by hand, match them to baseline rates, compute realized savings line by line, build "
    "three scenario models in separate spreadsheet tabs, and write the CFO memo. With Claude Code, the "
    "entire pipeline runs from a single slash command in under 10 minutes. The methodology stays encoded. "
    "The calculations stay reproducible. The memo follows the same format every month."
)

add_para(
    "This course teaches five things, in order."
)

add_numbered(
    "Savings methodology encoding. You write the definitions of hard savings, soft savings, cost avoidance, "
    "and working capital into CLAUDE.md. Every future calculation uses those definitions automatically."
)
add_numbered(
    "Transaction-to-initiative matching. Claude Code (in the terminal) reads 437 transactions from a CSV, "
    "matches each to its initiative by ID, applies the hard savings formula, and computes realized savings "
    "per initiative with variance to target."
)
add_numbered(
    "Three-scenario modeling. You define base, upside, and risk-adjusted assumptions. Claude Code (in the "
    "terminal) projects full-year savings under each scenario and shows the gap to the $12M target."
)
add_numbered(
    "CFO memo drafting. Claude Code (in the terminal) writes a one-page memo that leads with the headline "
    "number, shows variance by initiative, presents the three scenarios, and lists exactly three recommended "
    "actions with dollar amounts and deadlines."
)
add_numbered(
    "Monthly refresh automation. You build a slash command that runs the full pipeline from a single prompt. "
    "When next month's transaction file drops, one command produces updated savings, scenarios, and a fresh memo."
)

add_para(
    "By the end, you have a repeatable savings tracking system that runs in minutes, not days. The methodology "
    "is documented. The scenarios are explicit. The memo is formatted for the CFO, not for you."
)

# ================================================================
#  WHAT IS IN THE COURSE FOLDER
# ================================================================
doc.add_heading("What Is in the Course Folder", level=1)

add_para(
    "The course folder is self-contained. Everything you need is inside it. No external downloads, no "
    "shared network drives, no API keys. Here is the layout."
)

add_code_block(
    "Course_18_Savings_Program_Management/\n"
    "  README.md\n"
    "  COURSE_OVERVIEW.md\n"
    "  lessons/\n"
    "    Lesson_01_Savings_Methodology.md\n"
    "    Lesson_02_Transaction_Matching.md\n"
    "    Lesson_03_Scenario_Modeling.md\n"
    "    Lesson_04_CFO_Memo.md\n"
    "    Lesson_05_Monthly_Refresh.md\n"
    "  practice/\n"
    "    CLAUDE.md\n"
    "    data/\n"
    "      sourcing-initiatives-log.csv\n"
    "      q1-q3-transactions.csv\n"
    "      market-benchmarks.md\n"
    "    Drafts/\n"
    "  solutions/\n"
    "    savings_methodology_solution.md\n"
    "    scenario_model_solution.md\n"
    "    cfo_memo_solution.md\n"
    "  scripts/"
)

doc.add_heading("Folder-by-folder breakdown", level=3)

add_rich_para([
    ("practice/CLAUDE.md", True, False),
    (" is the project instruction file. It defines your role as Savings Program Manager at Apex Procurement. "
     "It lists the data files, the savings methodology (four types with formulas), and the reporting standards "
     "for the CFO memo. Claude Code (in the terminal) reads this file automatically at the start of every session.", False, False),
])

add_para(
    "Why this matters. Without CLAUDE.md, Claude Code does not know the difference between hard savings and "
    "cost avoidance. It does not know that the cost of capital is 5%. It does not know that the CFO memo must "
    "lead with the headline number. With CLAUDE.md, every calculation and every output follows Apex's rules, "
    "not generic defaults.",
    italic=True
)

add_rich_para([
    ("practice/data/sourcing-initiatives-log.csv", True, False),
    (" holds the eight sourcing initiatives. Each row has an initiative ID, name, savings type, annual target, "
     "YTD target, YTD realized amount, variance, and status. This is the master reference for all target-vs-actual "
     "comparisons. It has 8 rows, small enough to read by hand.", False, False),
])

add_para(
    "Why this matters. The initiative log is the single source of truth for targets and baselines. If the "
    "baseline rate for Steel Consolidation is wrong in this file, every realized savings calculation for "
    "SAV-001 will be wrong. One file, one truth.",
    italic=True
)

add_rich_para([
    ("practice/data/q1-q3-transactions.csv", True, False),
    (" holds approximately 437 transaction rows covering Q1 through Q3. Each row is linked to a hard-savings "
     "initiative by initiative_id. Columns include transaction_id, date, initiative_id, initiative_name, "
     "category, rate_applied, baseline_rate, volume, amount_usd, and savings_usd. This is a realistic volume "
     "so you experience what Claude Code does with real data, not a five-row toy file.", False, False),
])

add_para(
    "Why this matters. With 437 rows, you cannot check every calculation by hand. You have to trust the "
    "methodology in CLAUDE.md. That is the point: the methodology is documented and applied consistently, "
    "so the numbers are auditable even at scale.",
    italic=True
)

add_rich_para([
    ("practice/data/market-benchmarks.md", True, False),
    (" holds industry benchmark rates by category. Claude Code (in the terminal) uses this file when "
     "calculating cost avoidance savings. The market price increase percentage comes from here, not from "
     "a guess.", False, False),
])

add_para(
    "Why this matters. Cost avoidance calculations require an external reference for what the price increase "
    "would have been without your negotiation. This file provides that reference. Without it, cost avoidance "
    "figures are assumptions, not calculations.",
    italic=True
)

add_rich_para([
    ("practice/Drafts/", True, False),
    (" is where all working files go. The savings summary CSV, the scenario projections CSV, and the CFO memo "
     "all land here. No file is saved to data/ or to the project root. Drafts/ is the working area.", False, False),
])

add_para(
    "Why this matters. Separating read-only source data (data/) from working outputs (Drafts/) prevents "
    "accidental overwrites. Your raw transaction file stays untouched. You can regenerate every output by "
    "rerunning the pipeline.",
    italic=True
)

add_rich_para([
    ("solutions/", True, False),
    (" holds reference answers for the savings methodology, the scenario model, and the CFO memo. Look at "
     "these only after you attempt each lesson. They show what a correct output looks like.", False, False),
])

add_para(
    "Why this matters. If your numbers do not match the solution, you know something went wrong in your "
    "methodology or your prompt. The solutions are the audit trail for the course.",
    italic=True
)

# ================================================================
#  TIME SAVINGS TABLE
# ================================================================
doc.add_heading("Time Savings Reference Table", level=1)

add_para(
    "The table below compares five common savings program tasks done by hand versus done with Claude Code "
    "(in the terminal). Times assume a program with eight initiatives, 437 transactions, and a monthly "
    "reporting cycle."
)

add_table(
    headers=["Task", "Without Claude Code", "With Claude Code"],
    rows=[
        [
            "Encode savings methodology (4 types, formulas, validation rules)",
            "2 to 3 hours: write definitions in a Word document, circulate for review, store somewhere findable",
            "15 minutes: type the rules into CLAUDE.md, verify with a test calculation"
        ],
        [
            "Match 437 transactions to 5 hard-savings initiatives and compute realized savings",
            "4 to 6 hours: build VLOOKUP formulas, validate each initiative, cross-check totals",
            "8 minutes: one prompt reads both files, joins by initiative_id, computes per-transaction savings, sums by initiative"
        ],
        [
            "Build three full-year scenario models (base, upside, risk-adjusted)",
            "2 to 3 hours: copy spreadsheet tabs, change assumptions by hand, reconcile totals",
            "10 minutes: define assumptions in one prompt, Claude Code projects all three scenarios with explicit assumptions"
        ],
        [
            "Draft CFO savings memo (headline, variance table, scenarios, three actions)",
            "90 to 120 minutes: write narrative, format table, align numbers, get the opening sentence right",
            "5 minutes: one prompt produces the memo in the correct format, headline number first"
        ],
        [
            "Monthly refresh (re-run full pipeline on new transaction data)",
            "4 to 6 hours: repeat all four tasks above with the new file",
            "3 minutes: run the /savings-refresh slash command, review outputs"
        ],
    ],
    col_widths=[2.5, 2.2, 2.2]
)

add_para(
    "Total time for a full monthly savings cycle: 13.5 to 18 hours by hand, or about 41 minutes with "
    "Claude Code (in the terminal). That is a reduction of 90% to 95%.",
    bold=True
)

# ================================================================
#  WHAT SAVINGS PROGRAM MANAGEMENT IS
# ================================================================
doc.add_heading("What Savings Program Management Is", level=1)

add_para(
    "Savings program management is the discipline of tracking, verifying, and reporting on the financial "
    "impact of sourcing initiatives. A company sets an annual savings target (in this course, $12M). "
    "The procurement team runs initiatives to achieve that target. The savings program manager is the "
    "person who answers three questions every month: how much have we saved so far, will we hit the "
    "target, and what do we need to do to close the gap."
)

doc.add_heading("The four savings types", level=2)

add_para(
    "Not all savings are the same. Finance teams and procurement teams often argue about what counts. "
    "The methodology in this course distinguishes four types."
)

add_rich_para([
    ("Hard savings. ", True, False),
    ("A contracted price reduction that shows up on a purchase order or invoice. Calculated as "
     "(baseline_rate minus negotiated_rate) times actual_volume. This is the only type where you can match "
     "every dollar to a transaction. Example: Apex negotiated steel at $648 per ton, down from a $720 baseline. "
     "Each ton saves $72. Buy 500 tons, and realized savings are $36,000.", False, False),
])

add_rich_para([
    ("Soft savings. ", True, False),
    ("A demand reduction, not a price change. Calculated as estimated avoided spend versus prior-year spend "
     "for the same category. Marked as 'estimated' in every output because no contract enforces it. Example: "
     "Apex reduced business travel spend by $320,000 YTD through a new travel policy, compared to $800,000 "
     "prior-year baseline.", False, False),
])

add_rich_para([
    ("Cost avoidance. ", True, False),
    ("A price increase that was prevented through negotiation or specification change. Calculated as "
     "(market_price_increase_pct times baseline_spend) minus actual_spend. Tracked separately because it does "
     "not show up in year-over-year spend comparisons. Example: market rates for standard fasteners increased "
     "8%. Apex standardized specifications and held the price. The avoided cost is 8% of the baseline spend.", False, False),
])

add_rich_para([
    ("Working capital improvement. ", True, False),
    ("Cash flow benefit from extending payment terms. Calculated as (additional_days / 365) times annual_spend "
     "times cost_of_capital. Apex uses 5% as its weighted average cost of capital. This does not reduce spend. "
     "It improves the company's cash position. Example: extending payment terms by 15 days on $1.3M in annual "
     "spend at 5% cost of capital yields $2,671 in working capital benefit per year.", False, False),
])

doc.add_heading("Transaction matching", level=2)

add_para(
    "For hard savings initiatives, the realized savings come from actual transactions. Each transaction in "
    "q1-q3-transactions.csv has an initiative_id, a rate_applied (what Apex actually paid), a baseline_rate "
    "(what Apex would have paid without the negotiation), and a volume. Claude Code (in the terminal) reads "
    "the transaction file, joins each row to its initiative, applies the formula, and sums by initiative. "
    "Any transaction with an initiative_id that does not match the initiative log gets flagged as 'unmatched' "
    "and excluded from realized savings."
)

add_para(
    "For non-hard initiatives (soft, cost avoidance, working capital), there is no transaction-level data. "
    "The YTD realized figure comes directly from the sourcing-initiatives-log.csv. Claude Code pulls those "
    "figures and adds them to the summary alongside the hard-savings calculations."
)

doc.add_heading("Scenario modeling", level=2)

add_para(
    "A savings program with one forecast has no credibility. If you present $12M and miss by $2M, the CFO "
    "remembers the miss. If you present a range with named assumptions, the CFO remembers the transparency. "
    "This course uses three scenarios."
)

add_rich_para([
    ("Base case. ", True, False),
    ("Each initiative continues at its current Q1-Q3 run rate for Q4. No changes. No recovery actions. "
     "The formula is: Q1-Q3 realized plus (Q1-Q3 realized divided by 3). This is the 'do nothing' scenario.", False, False),
])

add_rich_para([
    ("Upside case. ", True, False),
    ("Underperforming initiatives get specific recovery actions. SAV-002 (Logistics RFP) recovers to 75% of "
     "its Q4 target through renegotiation. SAV-006 (Demand Reduction) improves by 20% from a new travel policy. "
     "SAV-007 (Spec Standardization) recovers to 60% of Q4 target through two approved spec changes. All other "
     "initiatives continue at current run rate.", False, False),
])

add_rich_para([
    ("Risk-adjusted case. ", True, False),
    ("Things get worse before they get better. SAV-002 stays flat. SAV-006 and SAV-007 each lose 10% from "
     "current run rate. SAV-004 (Facilities Rebid) drops 15% due to a contractor dispute. This is the "
     "'what if nothing improves and some things slip' scenario.", False, False),
])

add_para(
    "The three scenarios give the CFO a range, not a point estimate. She picks the one she believes. "
    "In this course, the gap to the $12M target ranges from about $2.2M (upside) to $3.2M (risk-adjusted)."
)

doc.add_heading("CFO reporting", level=2)

add_para(
    "The CFO memo follows a strict format, encoded in CLAUDE.md. It has four sections, and they appear in "
    "this order, every time."
)

add_numbered(
    "Headline paragraph. The first sentence states YTD realized savings, the annual target, and the current "
    "trajectory. The second sentence names the gap. The third states the range of full-year outcomes. Three "
    "sentences. No background. No methodology explanation."
)
add_numbered(
    "Initiative variance table. All eight initiatives, sorted by largest negative variance first. Columns: "
    "Initiative, Type, YTD Target, YTD Realized, Variance, Status."
)
add_numbered(
    "Q4 outlook table. Three rows: base, upside, risk-adjusted. Each row shows the full-year projection, "
    "percentage of target, and the key assumption in one sentence."
)
add_numbered(
    "Three recommended actions. Each action names the initiative, the specific step, the expected dollar "
    "recovery, and the deadline. No more than three. If you have five ideas, pick the top three by dollar "
    "impact."
)

add_para(
    "The memo must never start with context or background. The CFO set the target. She knows the context. "
    "She wants the number. Give her the number first."
)

# ================================================================
#  WORKED EXAMPLES
# ================================================================
doc.add_heading("Worked Examples", level=1)

add_para(
    "Every worked example below has four parts: the prompt you type in Claude Code (in the terminal), the "
    "folder layout it operates on, what you should see when it succeeds, and what Claude Code did behind the "
    "scenes."
)

# ── Worked Example 1: Transaction Matching ──
doc.add_heading("Worked Example 1: Calculate Realized Savings by Initiative", level=2)

add_para(
    "You have 437 transactions in q1-q3-transactions.csv. You need realized "
    "savings per hard-savings initiative, compared to the YTD target."
)

add_para("The prompt to type:", bold=True)

add_code_block(
    "For each hard savings initiative (SAV-001 through SAV-005), calculate realized\n"
    "savings from data/q1-q3-transactions.csv using the formula in CLAUDE.md:\n"
    "(baseline_rate - rate_applied) x volume for each transaction, summed by\n"
    "initiative. Compare to the ytd_target_usd in data/sourcing-initiatives-log.csv.\n"
    "Show a table with columns: initiative_id, initiative_name, ytd_target_usd,\n"
    "realized_savings_usd, variance_usd, variance_pct. Then add the three non-hard\n"
    "initiatives (SAV-006, SAV-007, SAV-008) using their ytd_realized_usd from the\n"
    "log. Save the full 8-initiative summary to Drafts/savings-summary-ytd.csv."
)

add_para("The folder layout:", bold=True)

add_code_block(
    "practice/\n"
    "  CLAUDE.md\n"
    "  data/\n"
    "    sourcing-initiatives-log.csv      (8 rows, master reference)\n"
    "    q1-q3-transactions.csv            (437 rows, Q1-Q3 transactions)\n"
    "    market-benchmarks.md\n"
    "  Drafts/                              (output lands here)"
)

add_para("What you should see:", bold=True)

add_para(
    "A table with all 8 initiatives. SAV-001 (Steel Consolidation) shows realized savings near $1,760,194 "
    "against a YTD target of $1,800,000, a small shortfall. SAV-002 (Logistics RFP) shows realized savings "
    "near $747,565 against a YTD target of $1,350,000, a major shortfall of $602,435 (44.6% below target). "
    "The total YTD realized is near $6,855,836 against a target of $9,000,000. The file "
    "Drafts/savings-summary-ytd.csv is saved with 8 data rows."
)

add_para("What Claude Code did, behind the scenes:", bold=True)

add_numbered(
    "Read CLAUDE.md to load the savings methodology. Confirmed the hard savings formula: "
    "(baseline_rate minus rate_applied) times volume."
)
add_numbered(
    "Read data/sourcing-initiatives-log.csv to load the 8 initiatives with their targets, baselines, "
    "and savings types."
)
add_numbered(
    "Read data/q1-q3-transactions.csv (437 rows). Filtered to transactions where initiative_id matches "
    "SAV-001 through SAV-005 (hard savings only)."
)
add_numbered(
    "For each transaction, computed (baseline_rate minus rate_applied) times volume. Summed savings by "
    "initiative_id to get YTD realized for each hard-savings initiative."
)
add_numbered(
    "Compared each initiative's realized savings to its ytd_target_usd from the log. Computed variance "
    "in dollars and as a percentage."
)
add_numbered(
    "Added SAV-006, SAV-007, and SAV-008 using their ytd_realized_usd from the initiative log, since "
    "these do not have transaction-level data."
)
add_numbered(
    "Saved the combined 8-initiative summary to Drafts/savings-summary-ytd.csv with all columns."
)

# ── Worked Example 2: Scenario Modeling and CFO Memo ──
doc.add_heading("Worked Example 2: Build Three Scenarios and Draft the CFO Memo", level=2)

add_para(
    "You have the YTD savings summary from the previous step. Now you need three full-year "
    "projections and a one-page CFO memo."
)

add_para("The prompt to type:", bold=True)

add_code_block(
    "Using Drafts/savings-summary-ytd.csv, calculate three full-year projection\n"
    "scenarios for our $12M savings target.\n\n"
    "Base case: each initiative continues at its current Q1-Q3 run rate for Q4.\n"
    "Upside case: SAV-002 recovers to 75% of Q4 target ($450,000 x 0.75),\n"
    "SAV-006 improves 20% over base run rate, SAV-007 recovers to 60% of Q4\n"
    "target ($350,000 x 0.60). All others at current run rate.\n"
    "Risk-adjusted: SAV-002 flat, SAV-006 and SAV-007 drop 10% from base Q4,\n"
    "SAV-004 drops 15% from base Q4.\n\n"
    "Save the scenario table to Drafts/scenario-projections.csv.\n\n"
    "Then draft the CFO memo following the format in CLAUDE.md: headline number\n"
    "first, initiative variance table sorted by largest gap, three-scenario\n"
    "outlook, and exactly three recommended actions with dollar amounts and\n"
    "dates. Save to Drafts/cfo-memo-savings-review.md."
)

add_para("The folder layout:", bold=True)

add_code_block(
    "practice/\n"
    "  CLAUDE.md\n"
    "  data/\n"
    "    sourcing-initiatives-log.csv\n"
    "    q1-q3-transactions.csv\n"
    "    market-benchmarks.md\n"
    "  Drafts/\n"
    "    savings-summary-ytd.csv           (created in Worked Example 1)"
)

add_para("What you should see:", bold=True)

add_para(
    "Two new files in Drafts/. First, scenario-projections.csv shows three columns of full-year projections. "
    "The base case total is approximately $9.1M. The upside is approximately $9.6M to $9.8M. The risk-adjusted "
    "is approximately $8.8M to $9.0M. Second, cfo-memo-savings-review.md opens with a sentence like: "
    "'Apex Procurement has realized $6,855,836 in savings YTD against a $12,000,000 annual target.' "
    "The memo contains the initiative table sorted by variance, the three-scenario outlook, and three numbered "
    "actions, each with a dollar figure and a date."
)

add_para("What Claude Code did, behind the scenes:", bold=True)

add_numbered(
    "Read CLAUDE.md to load the scenario definitions and the CFO memo format rules."
)
add_numbered(
    "Read Drafts/savings-summary-ytd.csv to get YTD realized and variance by initiative."
)
add_numbered(
    "Calculated base case: for each initiative, divided Q1-Q3 realized by 3 to get the quarterly run rate, "
    "added one quarter to project the full year."
)
add_numbered(
    "Calculated upside case: applied specific recovery adjustments to SAV-002, SAV-006, and SAV-007 while "
    "keeping all others at the base run rate."
)
add_numbered(
    "Calculated risk-adjusted case: applied downward adjustments to SAV-002 (flat), SAV-006 and SAV-007 "
    "(minus 10%), and SAV-004 (minus 15%)."
)
add_numbered(
    "Saved the scenario comparison to Drafts/scenario-projections.csv with a totals row and gap-to-target row."
)
add_numbered(
    "Drafted the CFO memo. Headline paragraph first (YTD realized, gap, scenario range). Then the initiative "
    "variance table sorted by largest negative variance. Then the three-scenario outlook table. Then three "
    "recommended actions: renegotiate logistics contract by 05/15/2026 to recover $200,000, approve spec "
    "changes by 05/01/2026 to recover $150,000, implement revised travel policy by 05/01/2026 to recover $80,000."
)

# ── Worked Example 3: Monthly Refresh Slash Command ──
doc.add_heading("Worked Example 3: Run the Monthly Savings Refresh", level=2)

add_para(
    "You have built the full pipeline: methodology, transaction matching, scenario modeling, and the CFO "
    "memo. Now you automate it into a single slash command that runs every month when a new transaction "
    "file arrives."
)

add_para("The prompt to type:", bold=True)

add_code_block("/savings-refresh")

add_para("The folder layout:", bold=True)

add_code_block(
    "practice/\n"
    "  CLAUDE.md\n"
    "  .claude/\n"
    "    commands/\n"
    "      savings-refresh.md              (the slash command file)\n"
    "  data/\n"
    "    sourcing-initiatives-log.csv\n"
    "    q1-q3-transactions.csv\n"
    "  Drafts/"
)

add_para("What you should see:", bold=True)

add_para(
    "Claude Code (in the terminal) executes all 11 steps of the pipeline without additional prompts. "
    "It reads both data files, calculates savings for all 8 initiatives, builds the YTD summary, runs three "
    "scenarios, and drafts the CFO memo. The final output reports: 'Savings refresh complete. Headline: "
    "$6,855,836 realized YTD against $9,000,000 target. Three files saved to Drafts/.' The three files are "
    "savings-summary-ytd.csv, scenario-projections.csv, and cfo-memo-savings-review.md."
)

add_para("What Claude Code did, behind the scenes:", bold=True)

add_numbered(
    "Read the slash command file at .claude/commands/savings-refresh.md to load the 11-step pipeline "
    "definition."
)
add_numbered(
    "Read CLAUDE.md to load the methodology (four savings types with formulas), scenario assumptions "
    "(base, upside, risk-adjusted), and reporting format (headline first, three actions maximum)."
)
add_numbered(
    "Read data/sourcing-initiatives-log.csv (8 rows) and data/q1-q3-transactions.csv (437 rows)."
)
add_numbered(
    "Matched 437 transactions to 5 hard-savings initiatives by initiative_id. Applied "
    "(baseline_rate minus rate_applied) times volume for each transaction. Summed by initiative."
)
add_numbered(
    "Added the 3 non-hard initiatives (SAV-006, SAV-007, SAV-008) using their ytd_realized_usd values."
)
add_numbered(
    "Projected full-year savings under three scenarios. Compared each to the $12M target."
)
add_numbered(
    "Drafted the CFO memo with the headline paragraph, initiative variance table, scenario outlook, and "
    "three recommended actions. Saved all three files to Drafts/."
)

# ================================================================
#  DAY IN THE LIFE
# ================================================================
doc.add_heading("Day in the Life: Angela, Savings Program Lead", level=1)

add_para(
    "Angela is the Savings Program Lead at MedPro Devices, a US-based medical device manufacturer "
    "headquartered in Minneapolis. She manages a $14M annual savings target across nine sourcing initiatives. "
    "She reports to the CFO monthly and to the CPO weekly. Her categories include raw materials (titanium, "
    "surgical-grade polymers), logistics, IT, facilities, and professional services. She has been using "
    "Claude Code (in the terminal) for three months. Here is her Thursday."
)

doc.add_heading("07:45 - CFO meeting prep before coffee", level=3)

add_para(
    "Angela opens her laptop at her kitchen table. The CFO review is tomorrow at 10:00 AM. Finance dropped "
    "the updated Q3 transaction file into the shared folder yesterday at 5:30 PM. Angela needs the full "
    "savings picture before the meeting."
)

add_para(
    "She opens the terminal, navigates to her project folder, and starts Claude Code."
)

add_code_block(
    "cd MedPro_Savings_FY26\nclaude"
)

add_para(
    "She runs the monthly refresh."
)

add_code_block("/savings-refresh")

add_para(
    "Claude Code reads the new transaction file (512 rows for Q1 through Q3), matches each to its initiative, "
    "computes realized savings, runs three scenarios, and drafts the CFO memo. Total time: 4 minutes. "
    "Angela opens the memo and reads the headline: 'MedPro has realized $9,234,500 in savings YTD against "
    "a $14,000,000 annual target. The program is $1,265,500 behind the YTD target of $10,500,000.'"
)

add_para(
    "She spots a problem. SAV-003 (Titanium Consolidation) shows realized savings $180,000 below the "
    "previous month's run rate. She asks Claude Code to investigate."
)

add_code_block(
    "Show me all transactions for SAV-003 in September. Sort by date. Flag any\n"
    "transaction where the rate_applied is higher than the baseline_rate."
)

add_para(
    "Claude Code finds three transactions in September where the rate_applied was $1,420 per unit instead "
    "of the negotiated $1,280. Angela recognizes the pattern: the supplier applied a raw material surcharge "
    "without approval. She adds a note to the memo's variance section and sends the CFO a heads-up email."
)

add_para(
    "What to learn from this. The monthly refresh slash command turns a 4-hour process into a 4-minute one. "
    "But the value is not just speed. Because Angela got the numbers early, she had time to investigate the "
    "anomaly in SAV-003 before the CFO meeting. Without the automation, she would have found the surcharge "
    "mid-meeting, or not at all.",
    italic=True
)

doc.add_heading("09:15 - CPO asks for a scenario update", level=3)

add_para(
    "Angela's CPO, David, sends a Slack message: 'The board pushed the decision on the logistics RFP to "
    "June. What does that do to our full-year number?' Angela does not need to rebuild the scenario model. "
    "She modifies the upside assumption for SAV-005 (Logistics Rebid) and asks Claude Code to recalculate."
)

add_code_block(
    "Recalculate the upside scenario with this change: SAV-005 (Logistics Rebid)\n"
    "recovery delayed from May to July. Q4 recovery drops from 75% to 40% of\n"
    "quarterly target. All other assumptions unchanged. Show the updated three-\n"
    "scenario comparison."
)

add_para(
    "Claude Code (in the terminal) reads the existing scenario projections, applies the single change, and "
    "produces an updated table. The upside drops from $12.1M to $11.7M. Angela screenshots the table, "
    "pastes it into Slack, and replies to David in 6 minutes."
)

add_para(
    "What to learn from this. Scenario modeling is useful only if you can update it fast. When the CPO "
    "asks a 'what if' question, the answer should take minutes, not hours. The key is that the assumptions "
    "are explicit in CLAUDE.md. Angela changed one assumption and reran. She did not rebuild a spreadsheet.",
    italic=True
)

doc.add_heading("10:30 - Onboarding a new analyst", level=3)

add_para(
    "Angela's team just hired Raj, a junior savings analyst. His first task is to learn the savings "
    "methodology. Instead of sending him a 40-slide deck, Angela points him to the project folder."
)

add_code_block(
    "Read CLAUDE.md and explain each savings type in one sentence. Then show me\n"
    "a sample calculation for SAV-001 (Titanium Consolidation) using one actual\n"
    "transaction from the data."
)

add_para(
    "Raj types this prompt and gets a clear explanation with a real example: '(baseline $1,280 minus "
    "negotiated $1,152) times 200 units equals $25,600 in hard savings for this transaction.' He can see "
    "the formula, the data, and the result in one place. Angela checks his understanding by asking him to "
    "calculate SAV-007 (Spec Standardization) by hand and compare to Claude's output."
)

add_para(
    "What to learn from this. The methodology lives in CLAUDE.md, not in someone's head or in a slide deck "
    "from two years ago. A new team member can read the methodology, run a sample calculation, and verify "
    "the results in 20 minutes. If Angela leaves the company, the methodology stays.",
    italic=True
)

doc.add_heading("13:00 - Supplier meeting prep", level=3)

add_para(
    "Angela has a 2:00 PM call with Patriot Logistics, the carrier for SAV-005. She needs to know exactly "
    "how much Patriot has delivered versus the contracted rate, and where the gaps are. She asks Claude Code "
    "to prepare a supplier-specific savings summary."
)

add_code_block(
    "Filter q1-q3-transactions.csv to only SAV-005 (Logistics Rebid) transactions.\n"
    "Group by month. Show: month, transaction count, total volume, average\n"
    "rate_applied, baseline_rate, monthly savings, and cumulative savings.\n"
    "Highlight any month where the average rate_applied exceeds the negotiated rate."
)

add_para(
    "Claude Code (in the terminal) produces a 9-row table (January through September). August and September "
    "show rate_applied above the negotiated rate. Angela copies the table into her meeting notes. She now has "
    "the specific months, the specific amounts, and the specific rate deviations to discuss with the carrier."
)

add_para(
    "What to learn from this. The same transaction data that feeds the CFO memo can answer a supplier-specific "
    "question with one prompt. Angela did not build a separate spreadsheet for the carrier meeting. She "
    "filtered the same data set. The methodology stays consistent because every calculation comes from "
    "CLAUDE.md.",
    italic=True
)

doc.add_heading("15:30 - Finance challenge on cost avoidance", level=3)

add_para(
    "The Finance Controller, Lisa, emails Angela: 'I do not count cost avoidance as real savings. Remove "
    "SAV-007 from the program total.' Angela has heard this before. She needs to show Lisa the number with "
    "and without cost avoidance, plus the market data that supports the avoidance figure."
)

add_code_block(
    "Show me the savings program total two ways: (1) all eight initiatives\n"
    "including cost avoidance, (2) seven initiatives excluding SAV-007. For\n"
    "SAV-007, show the market benchmark increase percentage from\n"
    "market-benchmarks.md and the calculation that produced the avoidance\n"
    "figure. Format as a comparison table."
)

add_para(
    "Claude Code produces a side-by-side: $6,855,836 with cost avoidance, $6,415,836 without. It also shows "
    "the market benchmark (8% increase for fasteners per market-benchmarks.md) and the calculation: "
    "8% times $5,500,000 baseline spend equals $440,000 avoided, of which $440,000 YTD is claimed. Angela "
    "forwards the table to Lisa with a note: 'Here is the split. The 8% market increase comes from the "
    "ISM index. Happy to walk through it.'"
)

add_para(
    "What to learn from this. Finance challenges on savings types are routine. The advantage of encoding the "
    "methodology in CLAUDE.md is that the definitions are written down, not debated from memory. When Lisa "
    "asks 'what counts as savings,' Angela does not argue. She shows the methodology, the market data, and "
    "the calculation. The argument becomes a conversation about facts.",
    italic=True
)

doc.add_heading("16:45 - End-of-day: update CLAUDE.md for next month", level=3)

add_para(
    "Before logging off, Angela updates CLAUDE.md with two changes. First, she adds the new upside assumption "
    "for SAV-005 (recovery delayed from May to July, 40% instead of 75%). Second, she adds a validation rule: "
    "'If any SAV-003 transaction shows rate_applied above $1,300, flag it as a potential unapproved surcharge.' "
    "These changes will apply automatically next time anyone runs /savings-refresh."
)

add_code_block(
    "Update CLAUDE.md with two changes:\n"
    "1. In the Q4 scenarios, change SAV-005 upside recovery from 75% to 40%\n"
    "   of Q4 target, effective July instead of May.\n"
    "2. Add a validation rule: if any SAV-003 transaction has rate_applied\n"
    "   above $1,300, flag it as 'potential unapproved surcharge' and exclude\n"
    "   from realized savings until confirmed."
)

add_para(
    "Claude Code updates CLAUDE.md. Angela reviews the changes, confirms they look right, and closes the "
    "terminal. Tomorrow's CFO meeting is covered. The data is current. The scenarios reflect today's reality. "
    "The memo is written."
)

add_para(
    "What to learn from this. CLAUDE.md is a living document. It gets updated as the business changes. "
    "When the board delays a decision, the scenario assumptions change. When a supplier applies an unapproved "
    "surcharge, a new validation rule gets added. The system gets smarter over time because the rules are "
    "written down and applied automatically.",
    italic=True
)

# ================================================================
#  20-MINUTE SPRINT
# ================================================================
doc.add_heading("20-Minute Sprint: Your First Savings Calculation", level=1)

add_para(
    "This section gets you from zero to your first usable savings output in 20 minutes flat. It assumes "
    "you have Claude Code installed and the Course 18 practice folder on your machine. If you do not have "
    "Claude Code installed yet, do that first (it takes about 5 minutes)."
)

doc.add_heading("Minutes 0 to 5: Open the project and read the methodology", level=3)

add_numbered(
    "Open a terminal (the black window where you type commands)."
)
add_numbered(
    "Navigate to the practice folder."
)

add_code_block("cd Course_18_Savings_Program_Management/practice")

add_numbered(
    "Start Claude Code."
)

add_code_block("claude")

add_numbered(
    "Read the project instructions."
)

add_code_block("Read CLAUDE.md and summarize the four savings types in one sentence each.")

add_para(
    "You should see four types listed: hard savings (contracted price reduction), soft savings (demand "
    "reduction), cost avoidance (prevented price increase), and working capital (payment terms extension). "
    "Each has a formula."
)

doc.add_heading("Minutes 5 to 10: Inspect the data", level=3)

add_numbered(
    "Check the initiative log."
)

add_code_block(
    "Read data/sourcing-initiatives-log.csv and show me all 8 initiatives with\n"
    "their savings types and annual targets."
)

add_para(
    "You should see 8 rows. Five hard savings initiatives totaling $8.5M in targets. Three non-hard "
    "initiatives totaling $3.5M."
)

add_numbered(
    "Check the transaction file."
)

add_code_block(
    "How many rows are in data/q1-q3-transactions.csv? Show me the first 5 rows."
)

add_para(
    "You should see approximately 437 rows. The columns are transaction_id, date, initiative_id, "
    "initiative_name, category, rate_applied, baseline_rate, volume, amount_usd, and savings_usd."
)

doc.add_heading("Minutes 10 to 15: Calculate realized savings", level=3)

add_numbered(
    "Run the savings calculation."
)

add_code_block(
    "For each hard savings initiative (SAV-001 through SAV-005), calculate realized\n"
    "savings from data/q1-q3-transactions.csv using the formula in CLAUDE.md.\n"
    "Compare to the YTD target. Show a table with variance."
)

add_para(
    "You should see a table with five rows. Note which initiatives are ahead of target and which are behind. "
    "SAV-002 (Logistics RFP) will show a large negative variance."
)

doc.add_heading("Minutes 15 to 20: Save the summary and review", level=3)

add_numbered(
    "Add the non-hard initiatives and save."
)

add_code_block(
    "Add SAV-006, SAV-007, and SAV-008 using their ytd_realized_usd from the\n"
    "initiative log. Save the full 8-initiative summary to\n"
    "Drafts/savings-summary-ytd.csv."
)

add_para(
    "You should see the file saved with 8 data rows. The total YTD realized is near $6,855,836."
)

add_numbered(
    "Identify the top three variance drivers."
)

add_code_block(
    "Which three initiatives have the largest negative variance? List them with\n"
    "the dollar gap."
)

add_para(
    "You should see SAV-002 (Logistics RFP), SAV-007 (Spec Standardization), and SAV-006 (Demand Reduction). "
    "You now have a savings summary with variance analysis. It took 20 minutes. The same work by hand takes "
    "4 to 6 hours."
)

add_para(
    "Next steps: build three Q4 scenario projections, then draft the CFO memo. After that, automate the "
    "full pipeline into the /savings-refresh slash command."
)

# ================================================================
#  FIRST WEEK PLANNER
# ================================================================
doc.add_heading("First Week Day-by-Day Planner", level=1)

add_para(
    "This planner gives you five days of escalating sophistication. By Friday, you will have a fully "
    "automated savings tracking pipeline that runs from a single command."
)

doc.add_heading("Day 1 (Monday): Install and first contact", level=2)

add_para("Goals for today:", bold=True)
add_bullet("Install Claude Code (in the terminal) if not already installed.")
add_bullet("Open the Course 18 practice folder and read CLAUDE.md.")
add_bullet("Run your first savings calculation for one initiative.")

add_para(
    "Start by installing Claude Code if not already installed. Then navigate to the "
    "Course_18_Savings_Program_Management/practice/ folder and start Claude Code. Read CLAUDE.md to "
    "understand the savings methodology. Pick one initiative (start with SAV-001, Steel Consolidation) "
    "and calculate its realized savings from the transaction data. Verify the number makes sense: "
    "$72 savings per ton times a few hundred tons should produce a six-figure number."
)

add_para(
    "By end of day, you should be able to explain the four savings types and their formulas, and you "
    "should have one initiative's realized savings calculated."
)

doc.add_heading("Day 2 (Tuesday): Full savings summary", level=2)

add_para("Goals for today:", bold=True)
add_bullet("Calculate realized savings for all five hard-savings initiatives.")
add_bullet("Add the three non-hard initiatives to the summary.")
add_bullet("Save the 8-initiative summary to Drafts/savings-summary-ytd.csv.")
add_bullet("Identify the top three variance drivers.")

add_para(
    "Run the full transaction matching across all hard-savings initiatives. Add the "
    "non-hard initiatives. Save the summary. Then ask Claude Code to identify which initiatives are "
    "behind target and why. Pay attention to SAV-002 (Logistics RFP). It is the biggest variance driver. "
    "The CFO will ask about it."
)

add_para(
    "By end of day, you should have a complete savings summary CSV showing all 8 initiatives with "
    "their YTD realized, variance, and status."
)

doc.add_heading("Day 3 (Wednesday): Scenario modeling", level=2)

add_para("Goals for today:", bold=True)
add_bullet("Define three Q4 scenarios (base, upside, risk-adjusted) with explicit assumptions.")
add_bullet("Calculate full-year projections under each scenario.")
add_bullet("Save the scenario comparison to Drafts/scenario-projections.csv.")

add_para(
    "Define the three sets of assumptions in a single prompt. Claude Code (in the "
    "terminal) projects the full year for each initiative under each scenario. Save the comparison. "
    "Check that the upside is always higher than the base, and the risk-adjusted is always lower. If "
    "any initiative shows the opposite, the assumptions are wrong."
)

add_para(
    "By end of day, you should have a three-scenario model that shows the gap to $12M under each "
    "set of assumptions. You should be able to explain what drives the difference between the three."
)

doc.add_heading("Day 4 (Thursday): CFO memo and automation", level=2)

add_para("Goals for today:", bold=True)
add_bullet("Draft the CFO memo with headline number, variance table, scenarios, and three actions.")
add_bullet("Build the /savings-refresh slash command.")
add_bullet("Test the slash command end to end.")

add_para(
    "Draft the memo first. Read it critically: does the first sentence "
    "give the headline number? Is the variance table sorted by largest gap? Are there exactly three "
    "actions with dollar amounts and dates? Then build the slash command file at "
    ".claude/commands/savings-refresh.md and run it. Compare the slash command output to the memo you "
    "drafted manually. They should match."
)

add_para(
    "By end of day, you should have a polished CFO memo and a working slash command that reproduces "
    "the full pipeline from a single prompt."
)

doc.add_heading("Day 5 (Friday): Refine, reflect, and plan next month", level=2)

add_para("Goals for today:", bold=True)
add_bullet("Update CLAUDE.md with any new assumptions or validation rules you discovered this week.")
add_bullet("Run the slash command one more time to verify the updated rules produce correct output.")
add_bullet("Review the solutions/ folder and compare your outputs to the reference answers.")

add_para(
    "Run /savings-refresh and compare the output to the solutions in solutions/. Check the scenario "
    "model against solutions/scenario_model_solution.md. Check the CFO memo against "
    "solutions/cfo_memo_solution.md. If your numbers differ, trace the difference back to a methodology "
    "or assumption change. Update CLAUDE.md if needed."
)

add_para(
    "By end of day, you should have a fully functioning savings tracking system that runs from one command. "
    "Your CLAUDE.md should be up to date with all methodology rules, scenario assumptions, and validation "
    "rules. You are ready for next month's data drop."
)

# ================================================================
#  THE PATTERN
# ================================================================
doc.add_heading("The Pattern: Encoding Business Logic for Monthly Cycles", level=1)

add_para(
    "Course 18 teaches a pattern that applies far beyond savings tracking. The pattern has four parts."
)

add_numbered(
    "Encode the methodology. ",
    bold_prefix="Encode the methodology. "
)
# Fix: use the simpler approach
p = doc.paragraphs[-1]
p.clear()
r1 = p.add_run("1. Encode the methodology. ")
r1.bold = True
r2 = p.add_run(
    "Write your business rules, formulas, and definitions into CLAUDE.md as explicit instructions. "
    "Do not leave them in someone's head, in a slide deck, or in a spreadsheet formula. When the rules "
    "are in CLAUDE.md, every calculation follows the same logic every time. For savings tracking, this means "
    "the four savings type definitions, the matching rules, the rounding rules, and the validation rules."
)
p.style = doc.styles["Normal"]

p2 = doc.add_paragraph()
r1 = p2.add_run("2. Match data to structure. ")
r1.bold = True
r2 = p2.add_run(
    "Your raw data (transactions, invoices, bids, contracts) needs to be joined to a reference structure "
    "(initiatives, suppliers, categories). Claude Code (in the terminal) reads both files, matches by a shared "
    "key (initiative_id, supplier_id, contract_number), and computes the result. For savings tracking, this "
    "means matching 437 transactions to 8 initiatives by initiative_id."
)

p3 = doc.add_paragraph()
r1 = p3.add_run("3. Model scenarios with explicit assumptions. ")
r1.bold = True
r2 = p3.add_run(
    "Never present one number. Present a range with named assumptions. The reader picks the scenario they "
    "believe. The assumptions are written in CLAUDE.md, not in your head. When someone asks 'what changed,' "
    "you point to the assumption that changed. For savings tracking, this means three Q4 scenarios with "
    "specific recovery or decline percentages for each underperforming initiative."
)

p4 = doc.add_paragraph()
r1 = p4.add_run("4. Automate the cycle. ")
r1.bold = True
r2 = p4.add_run(
    "If you do the same work every month, build a slash command. The slash command runs the full pipeline: "
    "read data, match, calculate, model, and draft the output. When next month's data arrives, one command "
    "produces the updated output. For savings tracking, this means the /savings-refresh command that runs "
    "all 11 steps."
)

add_para(
    "This pattern works for any monthly procurement cycle. Spend analysis: encode the category taxonomy, "
    "match transactions to categories, model forecast scenarios, draft the CPO summary. Contract compliance: "
    "encode the compliance rules, match transactions to contract terms, model exposure scenarios, draft the "
    "risk report. Supplier scorecards: encode the scoring methodology, match performance data to KPIs, model "
    "improvement scenarios, draft the quarterly review. The structure is the same. The content changes."
)

# ================================================================
#  TROUBLESHOOTING
# ================================================================
doc.add_heading("Troubleshooting", level=1)

add_para(
    "These are the most common issues students encounter in Course 18, with the fix for each."
)

add_rich_para([
    ("Symptom: ", True, False),
    ("Claude Code treats cost avoidance the same as hard savings.", False, False),
])
add_rich_para([
    ("Fix: ", True, False),
    ("Check CLAUDE.md. The cost avoidance formula must reference market-benchmarks.md for the price increase "
     "percentage. Hard savings use baseline and negotiated rates from the initiative log. The two formulas are "
     "different. If the methodology section does not distinguish them, update it before recalculating.", False, False),
])

add_para("")

add_rich_para([
    ("Symptom: ", True, False),
    ("Working capital savings show unrealistic numbers (10x too high).", False, False),
])
add_rich_para([
    ("Fix: ", True, False),
    ("Check the cost_of_capital rate in CLAUDE.md. It should be 0.05 (5%), not 0.5 (50%). A decimal place "
     "error inflates the figure by a factor of 10. Also confirm the formula divides by 365, not by 12.", False, False),
])

add_para("")

add_rich_para([
    ("Symptom: ", True, False),
    ("The base case run rate divides by 9 months instead of 3 quarters.", False, False),
])
add_rich_para([
    ("Fix: ", True, False),
    ("The data covers Q1 through Q3 (three quarters). To get the quarterly run rate, divide by 3. If you "
     "divide by 9, you get a monthly rate, and the Q4 projection will be one-third of what it should be. "
     "Check whether your prompt said 'divide by 3 quarters' or 'divide by 9 months.' Be explicit.", False, False),
])

add_para("")

add_rich_para([
    ("Symptom: ", True, False),
    ("The /savings-refresh slash command does not appear when you type /savings.", False, False),
])
add_rich_para([
    ("Fix: ", True, False),
    ("Check that the file is saved at .claude/commands/savings-refresh.md inside the practice folder. The "
     "path must be exact: .claude/commands/ with a hyphen in savings-refresh. If you used an underscore "
     "(savings_refresh) or saved to the wrong directory, the command will not register.", False, False),
])

add_para("")

add_rich_para([
    ("Symptom: ", True, False),
    ("The CFO memo starts with background context instead of the headline number.", False, False),
])
add_rich_para([
    ("Fix: ", True, False),
    ("Read the reporting standards in CLAUDE.md. The first sentence of the memo must state the YTD realized "
     "savings figure. If Claude Code writes an opening paragraph about the program's history or methodology, "
     "tell it: 'Rewrite the memo. The first sentence must contain the dollar figure. No background.' The CFO "
     "set the target. She knows the context. She wants the number.", False, False),
])

add_para("")

add_rich_para([
    ("Symptom: ", True, False),
    ("The memo has four or five recommended actions instead of three.", False, False),
])
add_rich_para([
    ("Fix: ", True, False),
    ("The CLAUDE.md reporting standards cap recommendations at three. If Claude Code produces more, tell it: "
     "'Cut to three actions. Keep the three with the largest dollar recovery.' If you genuinely need more than "
     "three, label the section 'Prioritized actions, ranked' and list them by dollar impact.", False, False),
])

# ================================================================
#  DONE CHECKLIST
# ================================================================
doc.add_heading("Done Checklist", level=1)

add_para(
    "This checklist was run before producing this handout. Every item is marked done, deferred, or N/A."
)

checklist_items = [
    ("1. The S2P problem is named in the first section.", "Done. The opening section names savings program "
     "tracking across eight initiatives with a $12M target."),
    ("2. The outcome is stated in business terms before any command.", "Done. The 'What This Course Teaches' "
     "section describes the pipeline outcome before any prompt appears."),
    ("3. Every S2P task has a worked example with four parts.", "Done. Three worked examples, each with "
     "prompt, folder layout, expected output, and behind-the-scenes walkthrough."),
    ("4. Every capability statement names the specific Claude.", "Done. All examples specify Claude Code "
     "(in the terminal). Differences from Claude AI Web and Claude Desktop with Cowork are noted."),
    ("5. For lessons, every step has what you do, what you type, and what you see.", "N/A. This is a "
     "handout, not a lesson file. Steps are covered in the worked examples."),
    ("6. At least one full worked example with realistic fake data.", "Done. Three worked examples with "
     "Apex Procurement data, initiative IDs, and specific dollar figures."),
    ("7. Troubleshooting entries.", "Done. Six troubleshooting entries covering methodology, calculations, "
     "slash commands, and memo formatting."),
    ("8. No em-dashes or en-dashes.", "Done. Verified: no em-dashes or en-dashes anywhere in the document."),
    ("9. No banned phrases.", "Done. Verified against the full banned-phrase list in CLAUDE.md. "
     "Zero violations found in the document body."),
    ("10. Oxford commas applied.", "Done. All lists of three or more use the Oxford comma."),
    ("11. No rhetorical questions as openers.", "Done. Every section opens with a statement, not a question."),
    ("12. Risk and issue text in active voice.", "Done. Variance explanations name the actor and the cause."),
    ("13. Every figure is a real number.", "Done. All figures are specific: $6,855,836, $12M, 437 "
     "transactions, 8 initiatives, 44.6%, $602,435."),
    ("14. Sample executive summary names a supplier, a value, and a date.", "Done. The CFO memo example "
     "names Apex Procurement, $6,855,836 YTD, and 05/15/2026 deadline."),
    ("15. Recommendation list has three items or fewer.", "Done. All recommendation lists cap at three."),
    ("16. File names match the naming convention.", "Done. Course_18_Savings_Program_Management_Handout.docx."),
    ("17. Screenshots are cropped, captioned, and use fake data.", "N/A. No screenshots in this handout."),
    ("18. Standard folder layout referenced.", "Done. The 'What Is in the Course Folder' section shows the "
     "full layout with data/ as read-only and Drafts/ as the working area."),
    ("19. A procurement analyst with no coding background can act on this alone.", "Done. All prompts are "
     "copy-paste-able. Technical terms are explained on first use."),
    ("20. Comprehensive training guide requirements.", "Done. Time savings table, Day-in-the-Life "
     "narrative (Angela), 20-Minute Sprint, and First Week Planner all present. Personalization pattern "
     "covered through CLAUDE.md encoding."),
    ("21. Course-specific requirements.", "N/A. This is a handout, not a course folder."),
    ("22. Style check.", "Deferred. Will run after saving."),
    ("23. Every concept has a 'Why it matters' paragraph.", "Done. Every folder and file explanation in "
     "'What Is in the Course Folder' has a 'Why this matters' paragraph."),
    ("24. Every Day-in-the-Life scenario has a 'What to learn from this' paragraph.", "Done. All six "
     "scenarios end with a 'What to learn from this' teaching takeaway."),
]

for item_label, item_status in checklist_items:
    add_rich_para([
        (item_label + " ", True, False),
        (item_status, False, False),
    ], space_after=2)


# ================================================================
#  SAVE
# ================================================================
doc.save(str(OUT))
print(f"Saved: {OUT}")
print(f"Size: {OUT.stat().st_size:,} bytes")
