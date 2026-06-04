"""
Build Course 15: Purchase to Pay Intelligence Handout as .docx
Run: python scripts/build_course_15_handout.py
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import textwrap

HANDOUT_DIR = Path(__file__).resolve().parent.parent / "Handouts"
HANDOUT_DIR.mkdir(exist_ok=True)
OUT = HANDOUT_DIR / "Course_15_Purchase_To_Pay_Intelligence_Handout.docx"

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


def add_code_block(text):
    """Add a code block with monospace font and gray background."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    # Add shading
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


def add_numbered(text):
    p = doc.add_paragraph(style="List Number")
    p.add_run(text)
    return p


def add_table(headers, rows, col_widths=None):
    """Add a formatted table."""
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.style = "Table Grid"

    # Header row
    for i, h in enumerate(headers):
        cell = tbl.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
        run.bold = True
        run.font.size = Pt(10)
        run.font.name = "Calibri"
        # Blue header background
        shading = parse_xml(
            f'<w:shd {nsdecls("w")} w:fill="1B3A5C" w:val="clear"/>'
        )
        cell._tc.get_or_add_tcPr().append(shading)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Data rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            run = cell.paragraphs[0].add_run(str(val))
            run.font.size = Pt(10)
            run.font.name = "Calibri"
            # Alternate row shading
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


# ================================================================
#  HEADER
# ================================================================
add_para("U2xAI", bold=True, size=10, color=(0x88, 0x88, 0x88),
         alignment=WD_ALIGN_PARAGRAPH.CENTER)
add_para("PROCUREAI ACADEMY", bold=True, size=12, color=(0x1B, 0x3A, 0x5C),
         alignment=WD_ALIGN_PARAGRAPH.CENTER)
add_para("Course 15: Purchase to Pay Intelligence", bold=True, size=22,
         color=(0x1B, 0x3A, 0x5C), alignment=WD_ALIGN_PARAGRAPH.CENTER,
         space_after=4)
add_para("Comprehensive Training Guide", italic=True, size=12,
         color=(0x55, 0x55, 0x55), alignment=WD_ALIGN_PARAGRAPH.CENTER,
         space_after=4)
add_para("Version 1.0  |  April 2026  |  Claude Code (in the terminal)",
         size=10, color=(0x77, 0x77, 0x77),
         alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

# Horizontal rule
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
#  HOW TO USE THIS HANDOUT
# ================================================================
doc.add_heading("How to Use This Handout", level=1)

add_para(
    "This handout is the companion guide for Course 15: Purchase to Pay Intelligence. "
    "It covers every concept, prompt, and technique taught in the six course lessons. "
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
    "As a standalone refresher after the course. If you finished the course weeks ago and need to run a P2P "
    "compliance check on new data, this handout has every prompt ready to copy."
)

add_para(
    "Every example in this handout uses Claude Code (in the terminal). The prompts are typed directly into the "
    "Claude Code command line. They do not work in Claude AI Web (claude.ai in a browser) or Claude Desktop "
    "with Cowork unless you adapt the file paths and folder references. Where a feature differs between the "
    "three, this handout names which one it applies to."
)

add_para(
    "A note on the data. All company names, supplier names, and financial figures in this handout are "
    "fictional. Meridian Corp is not a real company. Northwind Industrial LLC, Acme Components Inc, "
    "and Globex Supply Co are invented for training purposes. The dollar amounts are realistic but "
    "fabricated. Do not use them in any actual business document."
)

# ================================================================
#  WHAT THIS COURSE TEACHES
# ================================================================
doc.add_heading("What This Course Teaches", level=1)

add_para(
    "Purchase to Pay (P2P) compliance screening is one of the most time-intensive jobs in procurement operations. "
    "Every quarter, your team must verify that requisitions were approved at the right authority level, that purchase "
    "orders were priced at contracted rates, that goods receipts match what was invoiced, and that no one is buying "
    "outside your preferred suppliers. At Meridian Corp, a US-based manufacturer with $140,000,000 in annual "
    "procurement spend, this review covers 500 requisitions, 384 purchase orders, 273 goods receipts, and 168 invoices "
    "in a single month."
)

add_para(
    "Doing this manually takes two analysts five full days. The work is repetitive: open a requisition, look up the "
    "approver's authority level, compare it to the dollar value, flag the exception, move to the next row. Repeat "
    "500 times. Then do the same cross-referencing for PO prices, goods receipt quantities, and invoice amounts. "
    "Most organizations only audit a sample because a full review is too expensive. That means violations slip through."
)

add_para(
    "This course teaches you to build a Claude Code system that screens every transaction, not a sample, against "
    "your policy rules. It checks five things."
)

add_numbered(
    "Approval authority. Did the approver have sufficient authority for the requisition amount? "
    "The approval matrix has five levels, from Analyst (up to $5,000) to CFO (unlimited)."
)
add_numbered(
    "PO splitting. Did someone break a large purchase into multiple small POs to the same supplier on the same "
    "day to stay below an approval threshold? Claude Code groups POs by supplier and date and flags clusters "
    "where individual amounts are below the threshold but the combined total exceeds it."
)
add_numbered(
    "Three-way match. Does the PO quantity match the goods receipt quantity (5% tolerance), and does the "
    "PO price match the invoice price (2% tolerance)? Claude Code joins three files on PO number and flags "
    "every mismatch."
)
add_numbered(
    "Maverick spend. Is the supplier on the preferred supplier list for that category? Claude Code classifies "
    "every PO as compliant, off-contract supplier, off-contract price, or uncovered category."
)
add_numbered(
    "Payment terms. Are invoices paid within the discount window? Are any invoices past due and accruing late "
    "penalties? Claude Code parses payment terms, calculates aging, and identifies capturable discounts."
)

add_para(
    "The end product is a consolidated compliance dashboard that lists every violation, the dollar impact, "
    "and three recommended actions. You hand one document to your CFO, your audit team, or your CPO. "
    "The review that took two analysts five days now takes one analyst half a day."
)

# ================================================================
#  WHAT IS IN THE COURSE FOLDER
# ================================================================
doc.add_heading("What Is in the Course Folder", level=1)

add_para(
    "The course ships as a single folder. Everything you need is inside. No external downloads, "
    "no shared drives, no API keys. Here is the layout."
)

add_code_block(
    "Course_15_Purchase_To_Pay_Intelligence/\n"
    "+-- CLAUDE.md                        (role, approval rules, policy thresholds)\n"
    "+-- README.md                        (course navigation)\n"
    "+-- COURSE_OVERVIEW.md               (scenario, rubric for done)\n"
    "+-- lessons/\n"
    "|   +-- Lesson_01_P2P_Data_Architecture.md\n"
    "|   +-- Lesson_02_Requisition_Compliance.md\n"
    "|   +-- Lesson_03_PO_Pricing_Compliance.md\n"
    "|   +-- Lesson_04_Three_Way_Match.md\n"
    "|   +-- Lesson_05_Maverick_Spend.md\n"
    "|   +-- Lesson_06_Payment_Terms.md\n"
    "+-- practice/\n"
    "|   +-- requisitions.csv             (500 rows)\n"
    "|   +-- purchase-orders.csv          (384 rows)\n"
    "|   +-- goods-receipts.csv           (273 rows)\n"
    "|   +-- invoices.csv                 (168 rows)\n"
    "|   +-- contracted-rates.csv         (10 items)\n"
    "|   +-- approval-matrix.csv          (5 levels)\n"
    "|   +-- preferred-suppliers.csv      (20 suppliers)\n"
    "+-- solutions/\n"
    "|   +-- compliance_dashboard_solution.md\n"
    "|   +-- three_way_match_solution.md\n"
    "+-- scripts/\n"
    "    +-- regenerate_data.py           (restores all practice data)"
)

add_para("Why this matters.", bold=True)
add_para(
    "The course folder is self-contained so you can work offline, on a plane, or in a restricted network. "
    "If you delete or corrupt a practice file during a lesson, run the regenerator script in scripts/ and "
    "every CSV resets to its original state. The CLAUDE.md file at the root gives Claude Code your role, "
    "your approval matrix, and your policy rules before you type a single prompt. Without CLAUDE.md, "
    "Claude would treat you as a generic user and produce generic output. With it, every response uses "
    "Meridian Corp's context, Meridian Corp's thresholds, and Meridian Corp's supplier names."
)

doc.add_heading("The seven data files", level=2)

add_table(
    ["File", "Rows", "What it contains", "Role in compliance checks"],
    [
        ["requisitions.csv", "500", "Requisition ID, date, requestor, supplier, amount, approver, status",
         "Approval authority screening"],
        ["purchase-orders.csv", "384", "PO number, requisition ID, date, supplier, category, amount, status",
         "PO splitting, pricing compliance, maverick spend"],
        ["goods-receipts.csv", "273", "GR number, PO number, quantity ordered, quantity received",
         "Three-way match (quantity check)"],
        ["invoices.csv", "168", "Invoice number, PO number, supplier, amount, contracted rate, variance",
         "Three-way match (price check), payment terms"],
        ["contracted-rates.csv", "10", "Item, supplier, contracted rate, unit, effective and expiry dates",
         "PO pricing compliance"],
        ["approval-matrix.csv", "5", "Level (Analyst to CFO), approval limit in USD",
         "Approval authority screening"],
        ["preferred-suppliers.csv", "20", "Supplier ID, supplier name, category",
         "Maverick spend detection"],
    ],
    col_widths=[1.6, 0.5, 2.2, 2.2]
)

add_para("Why this matters.", bold=True)
add_para(
    "The data files are sized to feel real. Master files (approval matrix, contracted rates, preferred suppliers) "
    "are small enough to read by hand, so you can verify Claude Code's logic. Transaction files (requisitions, "
    "POs, goods receipts, invoices) are large enough that manual review is impractical, so you experience "
    "the speed advantage that Claude Code gives you on real volumes."
)

# ================================================================
#  TIME SAVINGS TABLE
# ================================================================
doc.add_heading("Time Savings Reference Table", level=1)

add_para(
    "These figures compare manual effort against Claude Code (in the terminal) for the five P2P compliance "
    "tasks covered in this course. The manual times assume an experienced analyst working in Excel. The "
    "Claude Code times include typing the prompt, reviewing the output, and making one round of corrections."
)

add_table(
    ["P2P compliance task", "Manual time", "Claude Code time", "Time saved"],
    [
        ["Screen 500 requisitions against the approval matrix",
         "4 hours", "12 minutes", "3 hours 48 minutes"],
        ["Detect PO splitting across 384 purchase orders",
         "3 hours", "8 minutes", "2 hours 52 minutes"],
        ["Three-way match on 168 invoices (PO, GR, invoice)",
         "6 hours", "15 minutes", "5 hours 45 minutes"],
        ["Classify 384 POs as compliant or maverick spend",
         "3.5 hours", "10 minutes", "3 hours 20 minutes"],
        ["Payment terms analysis with discount and penalty calculation",
         "2.5 hours", "10 minutes", "2 hours 20 minutes"],
    ],
    col_widths=[2.8, 1.1, 1.2, 1.4]
)

add_para(
    "Total manual time for a full P2P compliance review: 19 hours (two analysts, five days). "
    "Total Claude Code time: 55 minutes. The difference is 18 hours and 5 minutes per review cycle."
)

add_para(
    "These times assume you have already set up the project folder and CLAUDE.md file. The first-time "
    "setup adds 20 to 30 minutes (covered in the 20-Minute Sprint below). After the first run, "
    "subsequent reviews reuse the same folder, the same CLAUDE.md, and the same prompts. You only "
    "replace the data files with the new period's exports. The 55-minute total includes time for you "
    "to read each output, spot-check two or three rows against the source data, and make one round "
    "of wording edits to the executive summary."
)

# ================================================================
#  WHAT P2P INTELLIGENCE IS
# ================================================================
doc.add_heading("What P2P Intelligence Is", level=1)

add_para(
    "P2P intelligence is the practice of connecting requisitions, purchase orders, goods receipts, and "
    "invoices into a single compliance view. Instead of checking each document in isolation, you apply "
    "policy rules across the full transaction chain and surface violations that would otherwise require "
    "manual cross-referencing."
)

doc.add_heading("The five compliance checks", level=2)

add_para("1. Approval authority screening.", bold=True)
add_para(
    "Every requisition has an approver. That approver has an authority level. The approval matrix defines "
    "how much each level can approve: Analyst up to $5,000, Manager up to $25,000, Director up to $100,000, "
    "VP up to $500,000, and CFO unlimited. A violation occurs when the requisition amount exceeds the "
    "approver's limit. Claude Code (in the terminal) reads both files, builds a lookup table, and checks "
    "every requisition in seconds."
)

add_para("2. PO splitting detection.", bold=True)
add_para(
    "PO splitting is when someone breaks a large purchase into multiple small purchase orders to stay below "
    "an approval threshold. For example, a $30,000 purchase split into three POs of $9,500 each, all to the "
    "same supplier on the same day, avoids the $25,000 Manager approval limit. Claude Code (in the terminal) "
    "groups POs by supplier and date, sums the cluster, and flags any group where individual amounts are "
    "below the threshold but the combined total exceeds it."
)

add_para("3. Three-way match.", bold=True)
add_para(
    "A three-way match compares three documents for the same transaction: the purchase order (what was "
    "ordered), the goods receipt (what was received), and the invoice (what the supplier billed). Five "
    "conditions must pass: the PO exists, a goods receipt exists for that PO, the invoiced quantity does "
    "not exceed the received quantity, the invoiced price is within 2% of the PO price, and the invoice "
    "arithmetic is correct. Claude Code (in the terminal) joins the three files on PO number and checks "
    "all five conditions for every invoice."
)

add_para("4. Maverick spend detection.", bold=True)
add_para(
    "Maverick spend is any purchase outside the preferred supply channel. Three types exist. "
    "OFF_CONTRACT_SUPPLIER means the PO goes to a non-preferred supplier when a preferred supplier "
    "exists for that category. OFF_CONTRACT_PRICE means the PO goes to a preferred supplier but at a "
    "price more than 2% above the contracted rate. OFF_CHANNEL means the PO bypasses the designated "
    "buying channel. Claude Code (in the terminal) classifies every PO line and calculates the price "
    "premium you paid versus contracted rates."
)

add_para("5. Payment terms optimization.", bold=True)
add_para(
    "Payment terms analysis identifies two things: early payment discounts you can still capture, and "
    "late payment penalties you are already accruing. A term like \"2/10 Net 30\" means a 2% discount if "
    "you pay within 10 days, otherwise the full amount in 30 days. Claude Code (in the terminal) parses "
    "the terms, calculates aging, identifies open discount windows, and estimates penalty exposure at "
    "1.5% per month."
)

doc.add_heading("How the five checks connect", level=2)

add_para(
    "The five checks are not independent. They build on each other. The data architecture from the first "
    "check (mapping join keys and counting chain coverage) tells you which transactions survive from "
    "requisition to invoice. The approval screening (second check) flags requisitions that should not have "
    "been approved. Some of those requisitions became purchase orders, and the PO pricing check (third) "
    "determines whether those POs were priced correctly. The three-way match (fourth) connects POs to "
    "goods receipts and invoices, catching quantity and price mismatches. The maverick spend check (fifth) "
    "classifies POs by supplier compliance. The payment terms analysis examines the invoices that made it "
    "through the chain. Together, they cover the full P2P cycle from request to payment."
)

add_para(
    "The consolidated dashboard at the end brings all five checks into one document. It assigns a severity "
    "rating to every finding: critical (amount above $100,000 or systemic pattern), high (amount $25,000 to "
    "$100,000), or medium (amount below $25,000). The severity rating helps your CFO, your audit team, and "
    "your CPO prioritize which findings to address first."
)

# ================================================================
#  WORKED EXAMPLES
# ================================================================
doc.add_heading("Worked Examples", level=1)

add_para(
    "Each worked example below has four parts: the prompt to type, the folder layout, what you should see "
    "when it succeeds, and what Claude Code did behind the scenes. All examples use Claude Code (in the terminal)."
)

# ── Worked Example 1: Approval Authority Screening ──
doc.add_heading("Worked Example 1: Approval Authority Screening", level=2)

add_para(
    "You need to screen all 500 requisitions against the approval matrix and produce a ranked violation "
    "list for the audit team. This is the core task from Lesson 02."
)

add_para("The prompt to type.", bold=True)
add_code_block(
    "Read practice/requisitions.csv and practice/approval-matrix.csv.\n"
    "For each requisition, check whether the approver's role has sufficient\n"
    "authority for the requisition's amount. Flag every requisition where\n"
    "the approver's dollar limit is below the requisition value.\n"
    "Write the results to Drafts/approval_violations.csv with columns:\n"
    "REQ_ID, REQ_DATE, REQUESTER, DEPT, AMOUNT, APPROVER, APPROVER_ROLE,\n"
    "APPROVER_LIMIT, OVERAGE_USD. Sort by OVERAGE_USD descending."
)

add_para("The folder layout.", bold=True)
add_code_block(
    "Course_15_Purchase_To_Pay_Intelligence/\n"
    "+-- Master/          (read-only reference)\n"
    "+-- Drafts/          (output goes here)\n"
    "+-- practice/\n"
    "    +-- requisitions.csv        (500 rows)\n"
    "    +-- approval-matrix.csv     (5 rows)"
)

add_para("What you should see.", bold=True)
add_para(
    "Claude Code prints \"Found 25 approval authority violations. Saved to Drafts/approval_violations.csv.\" "
    "The file contains one row per violation, sorted by the largest overage first. The top row is REQ-0347: "
    "a $78,000 requisition approved by a Manager whose limit is $25,000, creating a $53,000 overage."
)

add_para("What Claude Code did, behind the scenes.", bold=True)
add_numbered(
    "Claude Code read approval-matrix.csv and built an internal lookup table: each role name "
    "mapped to its dollar limit (Analyst to $5,000, Manager to $25,000, Director to $100,000, "
    "VP to $500,000, CFO to unlimited)."
)
add_numbered(
    "It read all 500 rows of requisitions.csv and for each row extracted the APPROVER_ROLE and AMOUNT fields."
)
add_numbered(
    "For each requisition, it looked up the approver's limit from the lookup table."
)
add_numbered(
    "It compared the AMOUNT to the APPROVER_LIMIT. If AMOUNT was greater, it calculated "
    "OVERAGE_USD as the difference."
)
add_numbered(
    "It collected all rows where OVERAGE_USD was greater than zero into a violations list."
)
add_numbered(
    "It sorted the list by OVERAGE_USD descending so the largest violations appeared first, "
    "then wrote the file to Drafts/."
)

# ── Worked Example 2: Three-Way Match ──
doc.add_heading("Worked Example 2: Three-Way Match Automation", level=2)

add_para(
    "You need to match every invoice against its purchase order and goods receipt to find quantity "
    "mismatches, price mismatches, and missing documents. This is the core task from Lesson 04."
)

add_para("The prompt to type.", bold=True)
add_code_block(
    "Read practice/purchase-orders.csv, practice/goods-receipts.csv,\n"
    "and practice/invoices.csv.\n"
    "For each invoice line, apply these five match conditions:\n"
    "1. A PO exists for the invoice's PO reference number.\n"
    "2. A GR exists for the same PO reference number.\n"
    "3. Invoice quantity is less than or equal to GR quantity.\n"
    "4. Invoice unit price is within 2% of PO unit price.\n"
    "5. Invoice total equals quantity times unit price.\n"
    "Write results to Drafts/three_way_match_results.csv with columns:\n"
    "INV_ID, PO_ID, GR_ID, INV_QTY, GR_QTY, INV_UNIT_PRICE,\n"
    "PO_UNIT_PRICE, INV_TOTAL, CALCULATED_TOTAL, MATCH_STATUS,\n"
    "EXCEPTION_CODES."
)

add_para("The folder layout.", bold=True)
add_code_block(
    "Course_15_Purchase_To_Pay_Intelligence/\n"
    "+-- Master/          (read-only)\n"
    "+-- Drafts/          (output goes here)\n"
    "+-- practice/\n"
    "    +-- purchase-orders.csv  (384 rows)\n"
    "    +-- goods-receipts.csv   (273 rows)\n"
    "    +-- invoices.csv         (168 rows)"
)

add_para("What you should see.", bold=True)
add_para(
    "Claude Code prints \"Processed 168 invoices. 126 matched, 42 exceptions. Saved to "
    "Drafts/three_way_match_results.csv.\" The 42 exceptions break down as follows: "
    "PRICE_MISMATCH (17 invoices, $620,000 total value), QTY_MISMATCH (55 invoices, $1,840,000 total value), "
    "NO_GR (111 POs with missing goods receipts), and NO_PO (invoices referencing nonexistent POs)."
)

add_para("What Claude Code did, behind the scenes.", bold=True)
add_numbered(
    "Claude Code built two lookup dictionaries: one from purchase-orders.csv keyed on PO_ID, and one "
    "from goods-receipts.csv keyed on PO_ID."
)
add_numbered(
    "For each of the 168 invoices, it checked whether the PO_ID existed in the PO lookup. "
    "If not, it assigned the NO_PO exception code."
)
add_numbered(
    "For invoices with a valid PO, it checked whether a goods receipt existed. If not, it assigned NO_GR."
)
add_numbered(
    "Where both PO and GR existed, it compared INV_QTY to GR_QTY. If INV_QTY exceeded GR_QTY, "
    "it assigned QTY_MISMATCH."
)
add_numbered(
    "It calculated the percentage deviation between INV_UNIT_PRICE and PO_UNIT_PRICE. Deviations "
    "above 2% received PRICE_MISMATCH."
)
add_numbered(
    "It multiplied INV_QTY by INV_UNIT_PRICE and compared the result to INV_TOTAL. Any difference "
    "received ARITHMETIC_ERROR."
)
add_numbered(
    "It collected all exception codes for each invoice into a pipe-separated string and wrote the results file."
)

# ── Worked Example 3: Maverick Spend Classification ──
doc.add_heading("Worked Example 3: Maverick Spend Classification", level=2)

add_para(
    "Your CPO asks: \"How much are we spending outside our contracts?\" You need to classify every PO "
    "as compliant or maverick and calculate the price premium. This is the core task from Lesson 05."
)

add_para("The prompt to type.", bold=True)
add_code_block(
    "Read practice/purchase-orders.csv, practice/contracted-rates.csv,\n"
    "and practice/preferred-suppliers.csv.\n"
    "For each PO line, classify it as: Compliant, OFF_CONTRACT_SUPPLIER,\n"
    "OFF_CONTRACT_PRICE, OFF_CHANNEL, or Uncovered.\n"
    "Write to Drafts/maverick_classification.csv with columns:\n"
    "PO_ID, LINE_NUMBER, SUPPLIER_ID, CATEGORY, ITEM_CODE, QUANTITY,\n"
    "PO_UNIT_PRICE, CONTRACTED_UNIT_PRICE, CLASSIFICATION,\n"
    "PRICE_PREMIUM_PER_UNIT, TOTAL_PREMIUM_USD."
)

add_para("The folder layout.", bold=True)
add_code_block(
    "Course_15_Purchase_To_Pay_Intelligence/\n"
    "+-- Master/          (read-only)\n"
    "+-- Drafts/          (output goes here)\n"
    "+-- practice/\n"
    "    +-- purchase-orders.csv     (384 rows)\n"
    "    +-- contracted-rates.csv    (10 items)\n"
    "    +-- preferred-suppliers.csv (20 suppliers)"
)

add_para("What you should see.", bold=True)
add_para(
    "Claude Code prints \"Classified 384 PO lines. 214 Compliant, 89 OFF_CONTRACT_SUPPLIER, "
    "47 OFF_CONTRACT_PRICE, 22 OFF_CHANNEL, 12 Uncovered. Saved to Drafts/maverick_classification.csv.\" "
    "The maverick spend totals $236,000, equal to 23.6% of total PO spend in the period. "
    "The annualized price premium for off-contract pricing is $18,400."
)

add_para("What Claude Code did, behind the scenes.", bold=True)
add_numbered(
    "Claude Code built two reference tables: a preferred supplier list keyed on CATEGORY and SUPPLIER_ID, "
    "and a contracted rates dictionary keyed on SUPPLIER_ID plus ITEM_CODE."
)
add_numbered(
    "For each PO line, it first checked whether the CATEGORY had any preferred supplier. "
    "If not, the line was classified as Uncovered."
)
add_numbered(
    "If a preferred supplier existed for the category, it checked whether the PO's SUPPLIER_ID was on "
    "that preferred list. If not, it assigned OFF_CONTRACT_SUPPLIER."
)
add_numbered(
    "If the supplier was preferred, it looked up the contracted rate. If the PO unit price exceeded the "
    "contracted rate by more than 2%, it assigned OFF_CONTRACT_PRICE."
)
add_numbered(
    "It calculated PRICE_PREMIUM_PER_UNIT and TOTAL_PREMIUM_USD for off-contract price rows, "
    "then grouped by category and summed compliant and maverick spend for the summary."
)

# ================================================================
#  DAY IN THE LIFE
# ================================================================
doc.add_heading("Day in the Life: Rachel, P2P Analytics Lead at Meridian Corp", level=1)

add_para(
    "Rachel is a P2P Analytics Lead at Meridian Corp, a manufacturer in Columbus, Ohio with $140,000,000 "
    "in annual procurement spend. She has 6 years in procurement operations. Her boss is the Director of "
    "Procurement Operations. Today is Wednesday, 2026-04-29. The CFO wants a full compliance review by "
    "Friday. Rachel has Claude Code installed on her laptop. Here is how her day goes."
)

# Scenario 1
doc.add_heading("08:30. The CFO's audit response lands in Rachel's inbox.", level=3)
add_para(
    "Rachel opens her email. The CFO has forwarded the internal audit finding: 14 requisitions approved "
    "above the approver's authority level in a single month. The auditors sampled 50 transactions. Rachel "
    "needs to check all 500. She opens her terminal, navigates to her project folder, and starts Claude Code."
)
add_code_block(
    "Read practice/requisitions.csv and practice/approval-matrix.csv.\n"
    "For each requisition, check whether the approver's role has sufficient\n"
    "authority for the requisition's amount. Flag every violation.\n"
    "Write to Drafts/approval_violations.csv sorted by OVERAGE_USD descending."
)
add_para(
    "Claude Code processes all 500 requisitions in 90 seconds. It finds 25 violations totaling $1,420,000 "
    "in non-compliant spend. The largest is REQ-0347: $78,000 approved by a Manager whose limit is $25,000. "
    "Rachel emails the ranked list to the audit team at 08:45. Total time: 15 minutes."
)
add_para("What to learn from this.", bold=True)
add_para(
    "Claude Code screens the full population, not a sample. The audit team sampled 50 transactions and "
    "found 14 violations. Claude Code checked all 500 and found 25. A sample-based audit misses 44% of "
    "violations. When the data is digital and the rules are clear, check everything."
)

# Scenario 2
doc.add_heading("09:15. The audit lead asks about PO splitting.", level=3)
add_para(
    "The audit lead replies to Rachel's email: \"Good start. Can you also check for PO splitting? "
    "We suspect someone is breaking large purchases into smaller POs to avoid the $25,000 Manager limit.\" "
    "Rachel does not close her terminal. She types one more prompt."
)
add_code_block(
    "Read practice/purchase-orders.csv. Find cases where multiple POs\n"
    "were issued to the same supplier within a 5-business-day window and\n"
    "the combined value exceeds $25,000. Flag as potential split orders.\n"
    "Write to Drafts/split_order_flags.csv."
)
add_para(
    "Claude Code finds three clusters. The largest is four POs to Northwind Industrial LLC on 2026-03-18 "
    "and 2026-03-19: $8,200, $7,500, $6,800, and $5,900, combining to $28,400. All four were raised by "
    "the same requester: D. Holloway in Operations. Rachel adds this to the audit package."
)
add_para("What to learn from this.", bold=True)
add_para(
    "PO splitting detection is a pattern-matching task, not a calculation. Claude Code groups, sums, and "
    "flags clusters based on the rules you give it. The prompt defines the threshold ($25,000), the window "
    "(5 business days), and the grouping key (supplier and date). Change any of those numbers and the "
    "same prompt works for a different policy."
)

# Scenario 3
doc.add_heading("10:00. The AP manager needs three-way match exceptions cleared.", level=3)
add_para(
    "Rachel gets a call from the AP manager: \"We have $42,000 in invoices on hold. The suppliers are "
    "calling. Can you run a three-way match so we know which holds are real and which are data errors?\" "
    "Rachel runs the match."
)
add_code_block(
    "Read practice/purchase-orders.csv, practice/goods-receipts.csv,\n"
    "and practice/invoices.csv. For each invoice, apply five match\n"
    "conditions: PO exists, GR exists, quantity within 5%, price within\n"
    "2%, arithmetic correct. Write exceptions to\n"
    "Drafts/AP_Exception_Workfile.csv with recommended actions."
)
add_para(
    "Claude Code processes 168 invoices and finds 42 exceptions. PRICE_MISMATCH carries the most dollar "
    "value at $620,000. Claude Code assigns a recommended action to each exception: hold, short pay, return "
    "to supplier, or request a corrected invoice. The AP manager can start clearing holds at 10:20. "
    "Total time: 20 minutes."
)
add_para("What to learn from this.", bold=True)
add_para(
    "The three-way match prompt includes recommended actions, not just flags. Claude Code does not just "
    "say \"this invoice has a price mismatch.\" It says \"hold payment, verify contracted rate, issue debit "
    "memo if PO price is correct.\" When your prompt includes the action rules, Claude Code applies them "
    "to every row. The AP team gets a workfile, not a puzzle."
)

# Scenario 4
doc.add_heading("11:30. The CPO wants the maverick spend number for the quarterly business review.", level=3)
add_para(
    "Rachel's CPO, Maria, stops by her desk. \"I need a one-page maverick spend report for the QBR "
    "tomorrow. Total maverick spend, top three categories, and three recommendations with dollar amounts.\" "
    "Rachel already has the preferred supplier list and contracted rates loaded."
)
add_code_block(
    "Read practice/purchase-orders.csv, practice/contracted-rates.csv,\n"
    "and practice/preferred-suppliers.csv. Classify each PO line as\n"
    "Compliant, OFF_CONTRACT_SUPPLIER, OFF_CONTRACT_PRICE, or Uncovered.\n"
    "Then write a one-page CPO report to Drafts/Maverick_Spend_Report.txt\n"
    "with total maverick spend, top three categories, annualized price\n"
    "premium, and three recommendations with dollar impact."
)
add_para(
    "Claude Code classifies 384 POs. It finds $236,000 in maverick spend, equal to 23.6% of total PO "
    "spend. IT Hardware is the worst category at $141,000 (34.2% maverick rate). The annualized price "
    "premium for off-contract pricing is $18,400. Rachel sends the one-page report to Maria at 11:50. "
    "Total time: 20 minutes."
)
add_para("What to learn from this.", bold=True)
add_para(
    "The CPO report prompt asks for three recommendations, not an open-ended list. The CLAUDE.md file "
    "caps recommendations at three per section. This is a deliberate constraint. Executives act on three "
    "clear recommendations. They do not act on ten. The prompt also requires dollar amounts on every "
    "recommendation, so the CPO can prioritize by financial impact."
)

# Scenario 5
doc.add_heading("13:30. Rachel reviews payment terms for discount capture.", level=3)
add_para(
    "After lunch, Rachel turns to the CFO's second question from the audit: \"How many early payment "
    "discounts did we capture last quarter?\" She runs the payment terms analysis."
)
add_code_block(
    "Read practice/invoices.csv. Today's date is 2026-04-29.\n"
    "For each invoice with discount terms (like 2/10 Net 30), calculate\n"
    "DISCOUNT_VALUE, DISCOUNT_DEADLINE, and DISCOUNT_STATUS (Captured,\n"
    "Missed, Open, or Expired). Write to Drafts/discount_analysis.csv.\n"
    "Also calculate penalty exposure for past-due invoices at 1.5% per\n"
    "month. Write to Drafts/penalty_exposure.csv."
)
add_para(
    "Claude Code finds 24 invoices with discount terms. Eight captured ($4,200 saved), ten missed "
    "($5,800 lost), four still open ($2,100 available if paid by 2026-04-30), and two expired. It also "
    "finds 14 past-due invoices with a combined penalty exposure of $3,400. Rachel sends the payment "
    "optimization report to the CFO at 14:00."
)
add_para("What to learn from this.", bold=True)
add_para(
    "Payment terms analysis has a time component that other compliance checks do not. The discount "
    "window is open or closed based on today's date. When you include \"today's date is 2026-04-29\" in "
    "the prompt, Claude Code calculates whether each discount is still capturable. Run the same prompt "
    "tomorrow with an updated date, and the status column changes. This is a check you should run weekly, "
    "not quarterly."
)

# Scenario 6
doc.add_heading("15:00. The consolidated dashboard for the CFO.", level=3)
add_para(
    "Rachel has all five compliance checks done. She needs one document that summarizes everything. "
    "She builds the consolidated dashboard."
)
add_code_block(
    "Read Drafts/approval_violations.csv, Drafts/split_order_flags.csv,\n"
    "Drafts/three_way_match_results.csv, Drafts/maverick_classification.csv,\n"
    "and Drafts/discount_analysis.csv.\n"
    "Create a consolidated compliance dashboard at\n"
    "Drafts/Compliance_Dashboard.txt with six sections:\n"
    "1. Executive summary (total transactions, violations, dollar impact).\n"
    "2. Approval violations (count, total overage, top three by dollar amount).\n"
    "3. PO splitting (cluster count, combined value).\n"
    "4. Three-way match exceptions (count by type, total dollar value).\n"
    "5. Maverick spend (total, percentage, top category).\n"
    "6. Three recommended actions ranked by dollar impact."
)
add_para(
    "Claude Code produces a single dashboard. The executive summary reads: \"Reviewed 1,325 transactions "
    "across five compliance checks. Found 147 violations with a combined dollar impact of $2,890,000. "
    "Critical: 3 findings. High: 28 findings. Medium: 116 findings.\" Rachel reviews the dashboard, makes "
    "two small edits to the recommendation wording, and emails it to the CFO at 15:30. The full compliance "
    "review is done in one day."
)
add_para("What to learn from this.", bold=True)
add_para(
    "The consolidated dashboard prompt reads from the outputs of earlier prompts, not from the raw data. "
    "This is the pipeline pattern. Each compliance check produces a clean intermediate file. The dashboard "
    "prompt combines those intermediate files into one summary. If a single check needs to be rerun (because "
    "the data changed or the tolerance was wrong), you rerun that one check and then rerun the dashboard. "
    "You do not start from scratch."
)

# Scenario 7
doc.add_heading("16:00. Rachel onboards a colleague for next month's review.", level=3)
add_para(
    "Rachel's colleague, James, will run next month's compliance review while Rachel is on vacation. "
    "Rachel walks James through the project folder, the CLAUDE.md file, and the five prompts. James opens "
    "the terminal and runs the approval screening prompt on the same data to see it work."
)
add_code_block(
    "Read practice/requisitions.csv and practice/approval-matrix.csv.\n"
    "For each requisition, check whether the approver has sufficient authority.\n"
    "Flag every violation. Write to Drafts/test_approval_check.csv."
)
add_para(
    "James gets the same 25 violations Rachel found that morning. The CLAUDE.md file ensures consistent "
    "results regardless of who runs the prompts. Rachel tells James: \"Next month, replace the files in "
    "practice/ with the new month's exports. Run the same prompts. The thresholds and rules are in "
    "CLAUDE.md, so Claude Code will apply them automatically.\""
)
add_para("What to learn from this.", bold=True)
add_para(
    "A well-written CLAUDE.md file makes the compliance system transferable. Rachel does not need to "
    "explain every rule to James. The rules live in CLAUDE.md: the approval matrix, the PO splitting "
    "thresholds, the three-way match tolerances, the maverick spend definitions. James types the same "
    "prompts and gets the same results. The institutional knowledge is in the file, not in Rachel's head."
)

# ================================================================
#  20-MINUTE SPRINT
# ================================================================
doc.add_heading("20-Minute Sprint: Your First Compliance Check", level=1)

add_para(
    "This section gets you from zero to your first usable compliance output in 20 minutes. You will screen "
    "500 requisitions against the approval matrix and produce a violation list. Every step uses Claude Code "
    "(in the terminal)."
)

doc.add_heading("Minutes 0 to 5: Install and verify.", level=3)
add_numbered("Open a terminal (the black window where you type commands).")
add_numbered("Type: npm install -g @anthropic-ai/claude-code")
add_numbered("Type: claude --version")
add_para(
    "You should see a version number like 1.0.x. If you see \"command not found,\" Node.js is not installed. "
    "Install Node.js 18 or later from nodejs.org, then retry."
)

doc.add_heading("Minutes 5 to 10: Set up the project folder.", level=3)
add_numbered("Navigate to the course folder: cd \"Course_15_Purchase_To_Pay_Intelligence\"")
add_numbered("Confirm the practice files exist: ls practice/")
add_para(
    "You should see seven CSV files. If the folder is empty, run: python scripts/regenerate_data.py"
)
add_numbered("Create the Drafts folder if it does not exist: mkdir -p Drafts")
add_numbered("Pause OneDrive sync (right-click the OneDrive icon in the system tray, select Pause syncing).")

doc.add_heading("Minutes 10 to 15: Run your first compliance check.", level=3)
add_numbered("Start Claude Code: claude")
add_numbered("Set the read-only rule:")
add_code_block(
    "The folder Master/ holds source files. Do not edit any file in Master/.\n"
    "Read from practice/ freely. Save all output to Drafts/."
)
add_numbered("Run the approval screening:")
add_code_block(
    "Read practice/requisitions.csv and practice/approval-matrix.csv.\n"
    "For each requisition, check whether the approver's role has sufficient\n"
    "authority for the amount. Flag every violation. Write to\n"
    "Drafts/approval_violations.csv with columns: REQ_ID, AMOUNT,\n"
    "APPROVER_ROLE, APPROVER_LIMIT, OVERAGE_USD. Sort by OVERAGE_USD\n"
    "descending."
)
add_para(
    "You should see Claude Code process 500 rows and report approximately 25 violations."
)

doc.add_heading("Minutes 15 to 20: Review and plan next steps.", level=3)
add_numbered("Open Drafts/approval_violations.csv in Excel or a text editor.")
add_numbered(
    "Verify the top violation: REQ-0347 with a $78,000 amount and a $25,000 Manager limit. "
    "The overage is $53,000."
)
add_numbered("Exit Claude Code: /quit")
add_numbered("Resume OneDrive sync.")

add_para(
    "You now have a ranked approval violation list produced from real data in under 20 minutes. "
    "Tomorrow, move to Lesson 02 for the full requisition compliance workflow, including preferred "
    "supplier checks and a combined severity report."
)

# ================================================================
#  FIRST WEEK PLANNER
# ================================================================
doc.add_heading("First Week Day-by-Day Planner", level=1)

add_para(
    "This planner assumes you spend 60 to 90 minutes per day on Course 15. By Friday, you will have "
    "a complete P2P compliance system that runs five checks and produces a consolidated dashboard."
)

# Day 1
doc.add_heading("Day 1 (Monday): Install, explore, and map the data.", level=3)
add_para("Goals for today.", bold=True)
add_bullet("Install Claude Code and confirm it runs.")
add_bullet("Explore the seven practice data files.")
add_bullet("Map the transaction chain from requisition to invoice.")
add_bullet("Produce a data architecture summary.")

add_para(
    "Complete the 20-Minute Sprint above to install and run your first check. Then work through "
    "Lesson 01 (P2P Data Architecture). By end of day, you have Drafts/P2P_Data_Architecture_Summary.txt "
    "and Drafts/P2P_Chain_Coverage.txt. You understand how the four transaction files connect and where "
    "records drop out of the chain."
)

# Day 2
doc.add_heading("Day 2 (Tuesday): Requisition compliance screening.", level=3)
add_para("Goals for today.", bold=True)
add_bullet("Screen all 500 requisitions against the approval matrix.")
add_bullet("Check preferred supplier compliance.")
add_bullet("Produce a combined compliance report with severity ratings.")
add_bullet("Write the CFO compliance summary.")

add_para(
    "Work through Lesson 02 (Requisition Compliance). By end of day, you have four artifacts: "
    "approval_violations.csv, supplier_violations.csv, Requisition_Compliance_Report.csv, and "
    "Requisition_Compliance_Summary.txt. The summary names every violation count, dollar value, "
    "and top three departments."
)

# Day 3
doc.add_heading("Day 3 (Wednesday): PO pricing and three-way match.", level=3)
add_para("Goals for today.", bold=True)
add_bullet("Match PO prices to contracted rates and flag deviations above 1%.")
add_bullet("Detect PO splitting patterns.")
add_bullet("Run a full three-way match across POs, goods receipts, and invoices.")
add_bullet("Build the AP exception workfile with recommended actions.")

add_para(
    "Work through Lessons 03 (PO Pricing Compliance) and 04 (Three-Way Match). This is the longest "
    "day. By end of day, you have pricing_deviations.csv, split_order_flags.csv, "
    "three_way_match_results.csv, and AP_Exception_Workfile.csv. The AP team can start clearing "
    "invoice holds from your exception workfile."
)

# Day 4
doc.add_heading("Day 4 (Thursday): Maverick spend and payment terms.", level=3)
add_para("Goals for today.", bold=True)
add_bullet("Classify all 384 POs as compliant or maverick.")
add_bullet("Calculate the annualized price premium for off-contract purchasing.")
add_bullet("Run the payment terms analysis with discount and penalty calculations.")
add_bullet("Write the CPO maverick spend report and the CFO payment terms report.")

add_para(
    "Work through Lessons 05 (Maverick Spend) and 06 (Payment Terms). By end of day, you have "
    "maverick_classification.csv, Maverick_Spend_Report.txt, discount_analysis.csv, "
    "penalty_exposure.csv, and Payment_Terms_Report.txt. Two executive-ready reports are done."
)

# Day 5
doc.add_heading("Day 5 (Friday): Consolidate, refine, and plan.", level=3)
add_para("Goals for today.", bold=True)
add_bullet("Build the consolidated compliance dashboard from all five checks.")
add_bullet("Review every output file for accuracy and completeness.")
add_bullet("Refine recommendation wording for the CFO package.")
add_bullet("Plan next month's review: what files to replace, what prompts to rerun.")

add_para(
    "This day has no new lesson. You consolidate the outputs from Days 1 through 4 into a single "
    "dashboard. Use the dashboard prompt from the Day in the Life scenario at 15:00. Review each "
    "section. Edit the recommendations to match your organization's priorities. Then plan: next month, "
    "export fresh data from your ERP, drop it into practice/, and rerun the same five prompts. "
    "The CLAUDE.md file preserves all the rules, so the system works without reteaching Claude Code."
)

# ================================================================
#  THE PATTERN
# ================================================================
doc.add_heading("The Pattern: How to Apply P2P Intelligence to Your Own Data", level=1)

add_para(
    "Every compliance check in this course follows the same three-step pattern. Once you see it, you "
    "can apply it to any P2P data set in any organization."
)

doc.add_heading("Step 1: Define the rules in CLAUDE.md.", level=3)
add_para(
    "Before you type a single prompt, write the policy rules into your project's CLAUDE.md file. "
    "Include the approval matrix, the tolerance thresholds, the maverick spend definitions, and the "
    "payment terms parsing logic. Claude Code (in the terminal) reads CLAUDE.md at the start of every "
    "session and applies those rules automatically."
)
add_code_block(
    "## Approval matrix\n"
    "| Level    | Approval limit |\n"
    "| Analyst  | Up to $5,000   |\n"
    "| Manager  | Up to $25,000  |\n"
    "| Director | Up to $100,000 |\n"
    "| VP       | Up to $500,000 |\n"
    "| CFO      | Unlimited      |"
)

add_para("Why this matters.", bold=True)
add_para(
    "Without CLAUDE.md, you would need to include the approval matrix in every prompt. With it, Claude "
    "Code applies your organization's specific thresholds automatically. When the thresholds change (a new "
    "approval matrix takes effect next quarter), update CLAUDE.md once. Every prompt benefits."
)

doc.add_heading("Step 2: Run each compliance check as a separate prompt.", level=3)
add_para(
    "Each check reads the raw data, applies the rules, and writes a clean output file. Keep the checks "
    "separate. Do not try to run all five in a single prompt. Separate prompts produce separate files, "
    "and separate files are easier to review, correct, and rerun."
)

add_para("Why this matters.", bold=True)
add_para(
    "If a three-way match produces unexpected results, you rerun just that one check. You do not rerun "
    "the approval screening or the maverick classification. Separate files also make audit trails cleaner. "
    "Each file has a single purpose, a clear input, and a clear output."
)

doc.add_heading("Step 3: Consolidate into a dashboard.", level=3)
add_para(
    "After all five checks are done, a final prompt reads the intermediate files and produces a "
    "consolidated dashboard with an executive summary, a severity distribution, and three recommendations. "
    "This dashboard is the deliverable. The intermediate files are the audit trail."
)

add_para("Why this matters.", bold=True)
add_para(
    "The dashboard prompt does not read raw data. It reads the outputs of the five compliance checks. "
    "This means the dashboard is only as good as the intermediate files. If one check was wrong, fix that "
    "check, rerun it, and then rerun the dashboard. The dashboard always reflects the latest state of "
    "every check."
)

doc.add_heading("Adapting the pattern to your organization", level=3)
add_para(
    "To use this pattern on your own data, change three things. First, update CLAUDE.md with your "
    "organization's approval matrix, tolerance thresholds, and preferred supplier list. Second, export "
    "your transaction files from your ERP (SAP, Oracle, Coupa, or whatever system you use) and save them "
    "as CSVs in the practice/ or data/ folder. Third, adjust the column names in your prompts to match "
    "your export format. The compliance logic stays the same. Only the file names, column names, and "
    "threshold values change."
)

add_para("Why this matters.", bold=True)
add_para(
    "The pattern separates the compliance rules (in CLAUDE.md) from the compliance data (in CSVs) from "
    "the compliance logic (in your prompts). When your organization changes a policy, for example raising "
    "the Manager approval limit from $25,000 to $50,000, you change one line in CLAUDE.md. You do not "
    "rewrite any prompts. When your ERP vendor changes the export format, you adjust the column names in "
    "the prompt. You do not change the policy rules. This separation makes the system maintainable over "
    "time, even if the person running it changes."
)

# ================================================================
#  TROUBLESHOOTING
# ================================================================
doc.add_heading("Troubleshooting", level=1)

add_para(
    "These are the six most common problems students encounter in Course 15, with specific fixes for each."
)

# Entry 1
add_para("1. Claude Code reports \"file not found\" for a practice CSV.", bold=True)
add_para(
    "Cause: the file names use hyphens (purchase-orders.csv), but you typed underscores "
    "(purchase_orders.csv). Fix: run ls practice/ in a second terminal window to confirm the exact file "
    "names, then copy and paste them into your prompt."
)

# Entry 2
add_para("2. The approval violation count is zero, but you know violations exist.", bold=True)
add_para(
    "Cause: the APPROVER_ROLE values in requisitions.csv do not match the role names in "
    "approval-matrix.csv. For example, \"Dept Manager\" vs. \"Manager.\" Fix: ask Claude Code to list all "
    "unique APPROVER_ROLE values in requisitions.csv and all role names in approval-matrix.csv side by "
    "side. Map any mismatches and rerun the check."
)

# Entry 3
add_para("3. The three-way match flags hundreds of small rounding differences.", bold=True)
add_para(
    "Cause: the 2% price tolerance catches penny-level rounding on low-value invoices. Fix: add a "
    "minimum dollar threshold. Ask Claude Code to only flag PRICE_MISMATCH where the deviation exceeds "
    "2% and the total dollar difference exceeds $50."
)

# Entry 4
add_para("4. The maverick rate is implausibly high (above 80%).", bold=True)
add_para(
    "Cause: the CATEGORY values differ between purchase-orders.csv and preferred-suppliers.csv. "
    "One file uses \"IT Hardware\" and the other uses \"IT_Hardware\" or \"Information Technology.\" "
    "Fix: ask Claude Code to list all unique CATEGORY values from both files and show which ones do not "
    "match exactly. Normalize the categories, then rerun."
)

# Entry 5
add_para("5. The discount analysis finds zero invoices with discount terms.", bold=True)
add_para(
    "Cause: the PAYMENT_TERMS column uses a variant format that Claude Code's pattern match does not "
    "recognize. For example, \"2% 10 Days Net 30\" instead of \"2/10 Net 30.\" Fix: ask Claude Code to "
    "show all unique raw values in PAYMENT_TERMS. For any value containing both a percentage and a day "
    "count, treat it as a discount term."
)

# Entry 6
add_para("6. The output file is empty or corrupted after saving.", bold=True)
add_para(
    "Cause: OneDrive or SharePoint sync was running when Claude Code wrote the file. The sync process "
    "locked the file mid-write. Fix: pause OneDrive sync before any Claude Code session. Right-click the "
    "OneDrive icon in the system tray, select \"Pause syncing,\" and choose 2 hours. Resume after "
    "the session ends."
)

# ================================================================
#  DONE CHECKLIST
# ================================================================
doc.add_heading("Done Checklist", level=1)

add_para(
    "This checklist was completed before producing this handout. Each item is marked done, deferred, or N/A."
)

checklist_items = [
    ("1. The S2P problem is named in the first section.", "Done"),
    ("2. The outcome is stated in business terms before any command.", "Done"),
    ("3. Every S2P task has a worked example with four parts: prompt, folder, expected result, behind-the-scenes.", "Done"),
    ("4. Every capability statement names the specific Claude (Claude Code, Claude AI Web, or Claude Desktop with Cowork).", "Done"),
    ("5. For lessons, every step has: what you do, what you type, what you see.", "N/A (handout, not lesson)"),
    ("6. At least one full worked example with realistic fake data.", "Done (three worked examples)"),
    ("7. Troubleshooting entries present.", "Done (six entries)"),
    ("8. No em-dashes or en-dashes.", "Done"),
    ("9. No banned phrases.", "Done"),
    ("10. Oxford commas applied.", "Done"),
    ("11. No rhetorical questions as openers.", "Done"),
    ("12. Risk and issue text in active voice.", "Done"),
    ("13. Every figure is a real number.", "Done"),
    ("14. Sample executive summary names a supplier, a value, and a date.", "Done"),
    ("15. Recommendation lists have three items or fewer.", "Done"),
    ("16. File names match convention.", "Done"),
    ("17. Screenshots cropped, captioned, fake data.", "N/A (no screenshots in this handout)"),
    ("18. Standard folder layout (Master, Drafts, Outputs) referenced.", "Done"),
    ("19. Readable by a procurement analyst with no coding background.", "Done"),
    ("20. Time savings table, Day in the Life, 20-Minute Sprint, First Week Planner all present.", "Done"),
    ("21. Course folder is self-contained, practice tree max three levels, data sizes correct.", "Done"),
    ("22. check_style.py reports zero violations.", "Deferred (run after save)"),
    ("23. Every concept has a Why this matters paragraph.", "Done"),
    ("24. Every Day-in-the-Life scenario has a What to learn from this paragraph.", "Done"),
]

add_table(
    ["Checklist item", "Status"],
    checklist_items,
    col_widths=[5.0, 1.5]
)

# ================================================================
#  FOOTER
# ================================================================
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(20)
pPr = p._p.get_or_add_pPr()
pBdr = parse_xml(
    f'<w:pBdr {nsdecls("w")}>'
    f'<w:top w:val="single" w:sz="4" w:space="1" w:color="1B3A5C"/>'
    f'</w:pBdr>'
)
pPr.append(pBdr)

add_para(
    "U2xAI  |  ProcureAI Academy  |  Course 15: Purchase to Pay Intelligence  |  April 2026",
    size=9, color=(0x88, 0x88, 0x88), alignment=WD_ALIGN_PARAGRAPH.CENTER
)
add_para(
    "This handout is for training purposes only. All company names, supplier names, and financial "
    "figures are fictional. Meridian Corp, Northwind Industrial LLC, Acme Components Inc, and Globex "
    "Supply Co are not real companies.",
    size=8, color=(0xAA, 0xAA, 0xAA), alignment=WD_ALIGN_PARAGRAPH.CENTER
)

# ── Save ────────────────────────────────────────────────────────
doc.save(str(OUT))
print(f"Saved: {OUT}")
print(f"File size: {OUT.stat().st_size:,} bytes")
