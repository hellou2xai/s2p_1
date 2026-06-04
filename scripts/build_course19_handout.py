"""
Build Course 19: Supply Chain Risk Handout as .docx
Run: python scripts/build_course19_handout.py
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
OUT = HANDOUT_DIR / "Course_19_Supply_Chain_Risk_Handout.docx"

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

    for i, h in enumerate(headers):
        cell = tbl.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
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
add_para("Course 19: Supply Chain Risk and Resilience", bold=True, size=22,
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
    "This handout is the companion guide for Course 19: Supply Chain Risk and Resilience. "
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
    "As a standalone refresher after the course. If you finished the course weeks ago and need to run a "
    "supply chain risk assessment on new data, this handout has every prompt ready to copy."
)

add_para(
    "Every example in this handout uses Claude Code (in the terminal). The prompts are typed directly "
    "into the Claude Code command line. They do not work in Claude AI Web (claude.ai in a browser) or "
    "Claude Desktop with Cowork unless you adapt the file paths and folder references. Where a feature "
    "differs between the three, this handout names which one it applies to."
)

add_para(
    "A note on the data. All company names, supplier names, and financial figures in this handout are "
    "fictional. Fortis Manufacturing is not a real company. Apex Electronics, Great Lakes Steel, Pacific "
    "Aluminum, Continental Freight, and Heartland Polymers are invented for training purposes. The dollar "
    "amounts are realistic but fabricated. Do not use them in any actual business document."
)

# ================================================================
#  WHAT THIS COURSE TEACHES
# ================================================================
doc.add_heading("What This Course Teaches", level=1)

add_para(
    "Supply chain risk assessment is one of the most consequential tasks in procurement. "
    "When a critical supplier fails, production stops, customers lose confidence, and revenue drops. "
    "Most organizations assess supply chain risk once a year, if at all. "
    "The assessment usually takes three analysts two to three weeks. "
    "They build spreadsheets, cross-reference supplier files, model scenarios by hand, "
    "and write a narrative in a shared document. The result is often 20 or more pages. "
    "The board reads the first two."
)

add_para(
    "This course teaches you to build a repeatable supply chain risk pipeline using Claude Code "
    "(in the terminal). You start with raw data: supplier financials, spend by item, single-source "
    "flags, disruption events, and approved alternates. You end with a three-page board resilience "
    "brief that names specific suppliers, states specific dollar exposures, and recommends specific "
    "actions with deadlines. The entire pipeline runs in about 4.5 hours across six lessons."
)

add_para(
    "The course covers four core capabilities."
)

add_numbered(
    "Risk scoring. You encode a five-factor risk matrix into CLAUDE.md so Claude Code (in the "
    "terminal) applies the same scoring logic to every supplier, every session. Financial health, "
    "geographic concentration, single-source exposure, disruption history, and alternate availability "
    "each carry a specific weight. The result is a weighted score from 1.00 to 3.00, with defined "
    "bands for critical, high, medium, and low risk."
)
add_numbered(
    "Single-source exposure mapping. You join three data files (single-source items, supplier master, "
    "and approved alternates) in one pass. Claude Code (in the terminal) builds a table that shows "
    "each single-source item, its current supplier, annual spend, criticality, and alternate status. "
    "Items with no approved alternate are flagged as critical gaps. At Fortis Manufacturing, 5 items "
    "carry $2,580,000 in single-source spend, and $620,000 of that has no backup supplier."
)
add_numbered(
    "Disruption scenario modeling. You model two forward-looking scenarios (a 60-day supplier facility "
    "shutdown and a 45-day logistics capacity loss) with financial impact broken into direct cost "
    "(spot-market premiums, expedited freight) and indirect cost (production downtime, customer "
    "penalties). Claude Code (in the terminal) calculates each scenario using cost assumptions drawn "
    "from four historical disruption events. The Pacific Aluminum scenario produces a $1,052,877 total "
    "impact. The Continental Freight scenario produces $610,959."
)
add_numbered(
    "Board resilience brief. You assemble the full pipeline output into a three-section brief: three "
    "key findings (each starting with a number), a top-five risk table, and an investment case with "
    "a payback ratio. Claude Code (in the terminal) writes the brief in one pass from four draft "
    "files, applying output standards from CLAUDE.md. The $340,000 mitigation investment reduces "
    "$4,200,000 in annual exposure, a 12.4x payback."
)

# ================================================================
#  WHAT IS IN THE COURSE FOLDER
# ================================================================
doc.add_heading("What Is in the Course Folder", level=1)

add_para(
    "The course folder is self-contained. Everything you need is inside it. No external downloads, "
    "no shared drives, no separate data stores. The folder structure follows the standard layout "
    "from the course framework."
)

add_code_block(
    "Course_19_Supply_Chain_Risk/\n"
    "  README.md\n"
    "  COURSE_OVERVIEW.md\n"
    "  lessons/\n"
    "    Lesson_01_Risk_Signal_Architecture.md\n"
    "    Lesson_02_Concentration_Risk.md\n"
    "    Lesson_03_Single_Source_Exposure.md\n"
    "    Lesson_04_Disruption_Scenario_Modeling.md\n"
    "    Lesson_05_Mitigation_Planning.md\n"
    "    Lesson_06_Board_Resilience_Brief.md\n"
    "  practice/\n"
    "    CLAUDE.md\n"
    "    data/\n"
    "      supplier-master.csv\n"
    "      spend-by-item.csv\n"
    "      single-source-items.csv\n"
    "      approved-alternates.csv\n"
    "      disruption-events.md\n"
    "    Drafts/\n"
    "  solutions/\n"
    "    risk_register_solution.md\n"
    "    board_brief_solution.md\n"
    "  scripts/\n"
    "    build_course_data.py"
)

doc.add_heading("Folder-by-folder breakdown", level=3)

add_para(
    "lessons/ holds the six lesson files in order. Each lesson follows the standard six-part "
    "structure: the S2P problem, what Claude Code does for you, set up, step-by-step instructions, "
    "a worked example, and common mistakes. Work through them in sequence.",
    bold=False
)
add_para(
    "Why this matters. The lesson sequence mirrors the real workflow: define the scoring method, "
    "find concentration risk, map single-source exposure, model disruptions, plan mitigations, and "
    "assemble the board brief. Skipping a lesson means a later lesson references a draft file that "
    "does not exist yet.",
    italic=True
)

add_para(
    "practice/ is your working directory. You start Claude Code here. It holds CLAUDE.md (the role "
    "definition and risk scoring matrix), a data/ subfolder with five read-only source files, and an "
    "empty Drafts/ folder where all outputs land."
)
add_para(
    "Why this matters. CLAUDE.md in practice/ tells Claude Code your role (Supply Chain Risk Manager "
    "at Fortis Manufacturing), the five risk factors with their weights and scoring bands, and the "
    "output standards (USD with commas, three-page board brief, no vague language). Without this "
    "file, Claude Code produces generic output. With it, every output uses Fortis's context, "
    "Fortis's scoring logic, and Fortis's supplier names.",
    italic=True
)

add_para(
    "data/ holds five source files. supplier-master.csv has 25 suppliers with financial health "
    "scores, geographic concentration levels, and single-source item counts. spend-by-item.csv has "
    "200 line items with annual spend, unit cost, single-source flags, and criticality ratings. "
    "single-source-items.csv has 5 high-exposure items with alternate availability and qualification "
    "times. approved-alternates.csv has 4 qualified or in-qualification alternate suppliers. "
    "disruption-events.md has 4 historical events with impact and recovery details."
)
add_para(
    "Why this matters. These files simulate a real supply chain risk data set at realistic volumes. "
    "25 suppliers is a manageable portfolio you can inspect by hand. 200 line items give Claude Code "
    "enough data to find real concentration patterns. The data is deterministic: running "
    "scripts/build_course_data.py with seed 42 regenerates everything if a file gets corrupted.",
    italic=True
)

add_para(
    "solutions/ holds two reference answers: risk_register_solution.md (the scored risk register "
    "with the top 10 risks) and board_brief_solution.md (the finished board resilience brief with "
    "three key findings, top five risks, and the $340,000 investment case). Compare your outputs "
    "against these after completing the course."
)
add_para(
    "Why this matters. Solutions give you a benchmark. If your risk register scores Midwest Precision "
    "as the top risk but the solution scores them third, you know to investigate the scoring bands "
    "in your CLAUDE.md. Without a reference answer, you cannot tell whether a difference is a "
    "mistake or a valid alternative.",
    italic=True
)

add_para(
    "scripts/ holds build_course_data.py. Run it with python scripts/build_course_data.py to "
    "regenerate all data files from scratch. The script uses random.seed(42) so the output is "
    "identical every time."
)
add_para(
    "Why this matters. If you delete a file during practice, one command restores it. You never "
    "have to re-download anything or ask an instructor for a fresh copy.",
    italic=True
)

# ================================================================
#  TIME SAVINGS TABLE
# ================================================================
doc.add_heading("Time Savings Reference Table", level=1)

add_para(
    "The table below compares five supply chain risk tasks done manually versus done with "
    "Claude Code (in the terminal). The time estimates assume a 25-supplier portfolio with 200 "
    "line items, which is the scale used in this course."
)

add_table(
    ["Task", "Without Claude Code", "With Claude Code", "Time saved"],
    [
        [
            "Score 25 suppliers against a five-factor\nrisk matrix",
            "4 hours (manual spreadsheet,\nlookup each factor per supplier)",
            "12 minutes (one prompt per factor,\nClaude applies the matrix to all 25)",
            "3 hours 48 minutes"
        ],
        [
            "Map single-source exposure across\n5 items with alternate status",
            "2 hours (cross-reference three files,\nbuild a joined table by hand)",
            "8 minutes (one prompt joins three\nCSVs and flags critical gaps)",
            "1 hour 52 minutes"
        ],
        [
            "Model 2 disruption scenarios with\nfinancial impact and recovery timeline",
            "6 hours (build spreadsheet model,\ndocument assumptions, calculate\ndirect and indirect costs)",
            "20 minutes (two prompts, one\nper scenario, with stated assumptions)",
            "5 hours 40 minutes"
        ],
        [
            "Build a risk-ranked mitigation plan\nwith cost estimates and payback ratio",
            "3 hours (extract risks from multiple\ndocuments, generate actions, calculate\nratios, rank and select top 5)",
            "15 minutes (one prompt reads three\ndraft files, generates and ranks actions)",
            "2 hours 45 minutes"
        ],
        [
            "Assemble a three-page board\nresilience brief from four draft files",
            "5 hours (write narrative, build tables,\nformat, review, cut to three pages)",
            "10 minutes (one prompt assembles\nbrief, validates against output standards)",
            "4 hours 50 minutes"
        ],
    ],
    col_widths=[2.2, 2.0, 2.0, 1.3]
)

add_para(
    "Total across all five tasks: 20 hours manually versus 65 minutes with Claude Code (in the "
    "terminal). That is a reduction from two and a half analyst-days to just over one hour. The "
    "analyst's time shifts from data assembly and formatting to reviewing outputs, validating "
    "assumptions, and presenting findings to the board.",
    bold=True
)

# ================================================================
#  WHAT SUPPLY CHAIN RISK INTELLIGENCE IS
# ================================================================
doc.add_heading("What Supply Chain Risk Intelligence Is", level=1)

add_para(
    "Supply chain risk intelligence is the practice of turning raw supplier data into actionable "
    "risk assessments that support board-level decisions. It answers three questions: which suppliers "
    "pose the greatest risk, what would happen if a specific supplier failed, and what should we "
    "spend to reduce that exposure."
)

doc.add_heading("Risk signals", level=2)

add_para(
    "A risk signal is any data point that indicates a supplier may be unable to deliver as "
    "contracted. This course uses five signals, each weighted differently."
)

add_bullet(
    " (25% weight). A supplier's Dun and Bradstreet score or equivalent, on a 0 to 100 scale. "
    "Below 50 is high risk. Between 50 and 69 is medium. Above 70 is low.",
    bold_prefix="Financial health"
)
add_bullet(
    " (15% weight). How many of your suppliers are located in the same state. Three or more "
    "suppliers in one state means a single regional event (hurricane, power grid failure, flood) "
    "can take multiple suppliers offline simultaneously.",
    bold_prefix="Geographic concentration"
)
add_bullet(
    " (25% weight). How many items you can only get from one supplier. Three or more single-source "
    "items from one supplier is critical. One or two is elevated. Zero is acceptable.",
    bold_prefix="Single-source exposure"
)
add_bullet(
    " (20% weight). Whether the supplier has experienced a disruption in the past 12 months. Any "
    "documented event scores elevated. No events score acceptable.",
    bold_prefix="Disruption history"
)
add_bullet(
    " (15% weight). Whether a qualified backup supplier exists for single-source items. No "
    "alternate is critical. An alternate in qualification is moderate. A fully qualified alternate "
    "is acceptable.",
    bold_prefix="Alternate availability"
)

add_para(
    "Why this matters. Without a written scoring matrix, two analysts will score the same supplier "
    "differently. One calls a financial health score of 55 acceptable. Another flags it as medium "
    "risk. The board loses confidence in the entire assessment because the numbers are inconsistent. "
    "Encoding the matrix in CLAUDE.md means Claude Code (in the terminal) applies the same logic "
    "every time, and the logic is visible and auditable.",
    italic=True
)

doc.add_heading("Concentration risk", level=2)

add_para(
    "Concentration risk is the exposure created when too much spend or too many suppliers cluster "
    "around a single point of failure. This course measures three types."
)

add_bullet(
    " Any supplier holding more than 10% of total portfolio spend is a concentration risk. "
    "At Fortis, total portfolio spend is approximately $52,050,000. A supplier above $5,205,000 "
    "would breach the threshold.",
    bold_prefix="Share of wallet."
)
add_bullet(
    " Any US state with three or more suppliers, or with more than 20% of total spend, is a "
    "geographic concentration risk. Texas has three Fortis suppliers (Heartland Polymers, "
    "TechForward Solutions, and Frontier Plastics).",
    bold_prefix="Geographic clustering."
)
add_bullet(
    " Any supplier holding more than 50% of spend in a single category is a category "
    "concentration risk.",
    bold_prefix="Category dominance."
)

add_para(
    "Why this matters. A category manager knows their top supplier. They do not always know that "
    "the same supplier also appears in two other categories, making total exposure three times what "
    "any single category shows. Claude Code (in the terminal) reads supplier-master.csv and "
    "spend-by-item.csv together and calculates all three concentration views in one prompt.",
    italic=True
)

doc.add_heading("Disruption scenario modeling", level=2)

add_para(
    "A disruption scenario is a forward-looking model that answers: if supplier X goes offline for "
    "Y days, what does it cost us? The model has two cost components."
)

add_bullet(
    " Cash outlays during the disruption: spot-market premiums (buying the same material at "
    "30% above contracted rates), expedited freight surcharges, and re-routing fees.",
    bold_prefix="Direct cost."
)
add_bullet(
    " Revenue and productivity losses: production downtime (at $25,000 per day for the first "
    "30 days), customer delivery penalties, and lost orders.",
    bold_prefix="Indirect cost."
)

add_para(
    "The assumptions come from historical disruption events. Fortis has four documented events in "
    "the past year: Hurricane Impact on Heartland Polymers (12 days, $420,000), Supplier Financial "
    "Distress at Apex Electronics (ongoing, lead times doubled), Logistics Capacity Crunch at Eagle "
    "Transport (21 days, $180,000), and a Cybersecurity Incident at CloudBridge Systems (5 days, "
    "$95,000). These events provide the cost rates used in forward-looking models."
)

add_para(
    "Why this matters. Most risk registers list risks without quantifying their financial impact. "
    "\"Supplier X may experience a disruption\" tells a board nothing actionable. The board needs a "
    "dollar figure broken into direct and indirect cost. With those numbers, a risk becomes a "
    "budget line item and a decision trigger, not an opinion.",
    italic=True
)

# ================================================================
#  WORKED EXAMPLE 1: Risk Scoring
# ================================================================
doc.add_heading("Worked Examples", level=1)

doc.add_heading("Worked example 1: Score a supplier against the risk matrix", level=2)

add_para(
    "This example shows how Claude Code (in the terminal) scores a single supplier against all "
    "five risk factors."
)

add_para("The prompt to type:", bold=True)
add_code_block(
    "Using the risk scoring matrix in CLAUDE.md, score supplier SUP004\n"
    "(Apex Electronics) from data/supplier-master.csv. Show the score for\n"
    "each of the five factors and the weighted overall score. Check\n"
    "data/disruption-events.md for disruption history and\n"
    "data/approved-alternates.csv for alternate availability."
)

add_para("The folder layout:", bold=True)
add_code_block(
    "Course_19_Supply_Chain_Risk/practice/\n"
    "  CLAUDE.md                        (risk scoring matrix)\n"
    "  data/\n"
    "    supplier-master.csv            (25 suppliers, read-only)\n"
    "    disruption-events.md           (4 events, read-only)\n"
    "    approved-alternates.csv        (4 alternates, read-only)\n"
    "  Drafts/                          (output goes here)"
)

add_para("What you should see:", bold=True)
add_para(
    "Apex Electronics scored: financial health 44.8 is below 50, so factor score 3 (high risk). "
    "Geographic concentration \"high,\" so factor score 3. Single-source items count is 4, which is "
    "3 or more, so factor score 3. Disruption history: Apex Electronics appears in Event 2 of "
    "disruption-events.md, so factor score 3. Alternate availability: check approved-alternates.csv "
    "for items linked to SUP004. Overall weighted score is in the critical range (2.50 to 3.00)."
)

add_para("What Claude did, behind the scenes:", bold=True)
add_numbered(
    "Read CLAUDE.md to load the five-factor scoring matrix with weights and scoring bands."
)
add_numbered(
    "Read data/supplier-master.csv to find SUP004 (Apex Electronics): financial_health_score 44.8, "
    "geographic_concentration \"high,\" single_source_items 4."
)
add_numbered(
    "Applied the financial health band: 44.8 falls in the 0 to 49 range, so score 3."
)
add_numbered(
    "Applied the geographic concentration band: \"high\" maps to score 3."
)
add_numbered(
    "Applied the single-source exposure band: 4 items is 3 or more, so score 3."
)
add_numbered(
    "Searched data/disruption-events.md for any event naming \"Apex Electronics.\" Found Event 2 "
    "(Supplier Financial Distress), so disruption history scores 3."
)
add_numbered(
    "Calculated the weighted sum: (3 x 0.25) + (3 x 0.15) + (3 x 0.25) + (3 x 0.20) + "
    "(result x 0.15). Matched the total to the overall risk band (critical, high, medium, or low)."
)

doc.add_heading("Worked example 2: Build a single-source exposure map", level=2)

add_para(
    "This example shows how Claude Code (in the terminal) joins three data files in one prompt "
    "to produce a complete exposure map."
)

add_para("The prompt to type:", bold=True)
add_code_block(
    "Build the single-source exposure map by joining\n"
    "data/single-source-items.csv with data/approved-alternates.csv on\n"
    "item_id. Use a left join so all 5 single-source items appear even if\n"
    "they have no alternate. Show each item with its current supplier,\n"
    "annual spend, criticality, and alternate status. Flag items with no\n"
    "alternate as \"CRITICAL GAP.\" Then save to\n"
    "Drafts/single-source-exposure-map.md."
)

add_para("The folder layout:", bold=True)
add_code_block(
    "Course_19_Supply_Chain_Risk/practice/\n"
    "  CLAUDE.md\n"
    "  data/\n"
    "    single-source-items.csv        (5 items, read-only)\n"
    "    approved-alternates.csv        (4 alternates, read-only)\n"
    "    supplier-master.csv            (25 suppliers, read-only)\n"
    "  Drafts/\n"
    "    single-source-exposure-map.md  (output created here)"
)

add_para("What you should see:", bold=True)
add_para(
    "A 5-row table saved to Drafts/single-source-exposure-map.md. ITEM-0001 (Steel plate 4mm, "
    "Great Lakes Steel, $840,000, qualified alternate: Summit Metals). ITEM-0013 (Aluminum sheet "
    "2mm, Pacific Aluminum, $620,000, qualified alternate: Summit Metals). ITEM-0025 "
    "(Microcontroller ARM, Apex Electronics, $480,000, CRITICAL GAP). ITEM-0037 (Cloud hosting, "
    "CloudBridge Systems, $500,000, qualified alternate: Pinnacle Software). ITEM-0049 (Fire "
    "inspection, SafeGuard Inc, $140,000, CRITICAL GAP). Total single-source spend: $2,580,000. "
    "Spend with no alternate: $620,000 (24.03%)."
)

add_para("What Claude did, behind the scenes:", bold=True)
add_numbered(
    "Read CLAUDE.md to load the output standards: USD with commas, no vague language, name "
    "specific suppliers and dollar figures."
)
add_numbered(
    "Read data/single-source-items.csv to get all 5 items with supplier_id, annual_spend_usd, "
    "and criticality ratings."
)
add_numbered(
    "Read data/approved-alternates.csv to get the 4 alternate rows with qualification_status."
)
add_numbered(
    "Performed a left join on item_id, keeping all 5 single-source items even when no matching "
    "alternate row existed."
)
add_numbered(
    "For items with no match (ITEM-0025 and ITEM-0049), set alternate_supplier_name to \"NONE\" "
    "and alternate_status to \"CRITICAL GAP.\""
)
add_numbered(
    "For ITEM-0001, which has two alternate rows, kept the qualified alternate (Summit Metals) "
    "as the primary and noted Liberty Composites as a secondary."
)
add_numbered(
    "Sorted by annual_spend_usd descending and wrote the three-section output file to Drafts/."
)

doc.add_heading("Worked example 3: Model a disruption scenario", level=2)

add_para(
    "This example shows how Claude Code (in the terminal) models a forward-looking supplier "
    "disruption with quantified financial impact."
)

add_para("The prompt to type:", bold=True)
add_code_block(
    "Model a 60-day disruption at Pacific Aluminum (SUP003). Annual spend:\n"
    "$3,100,000. Use historical cost patterns from data/disruption-events.md.\n"
    "Assume spot-market premium of 30%, expedited freight surcharge of\n"
    "$150,000, and production downtime of $25,000 per day for 30 days.\n"
    "Show direct cost, indirect cost, and total impact. Check\n"
    "data/approved-alternates.csv for recovery timeline."
)

add_para("The folder layout:", bold=True)
add_code_block(
    "Course_19_Supply_Chain_Risk/practice/\n"
    "  CLAUDE.md\n"
    "  data/\n"
    "    disruption-events.md           (4 events, read-only)\n"
    "    supplier-master.csv            (25 suppliers, read-only)\n"
    "    single-source-items.csv        (5 items, read-only)\n"
    "    approved-alternates.csv        (4 alternates, read-only)\n"
    "  Drafts/\n"
    "    disruption-scenarios.md        (output created here)"
)

add_para("What you should see:", bold=True)
add_para(
    "A scenario model with: 60-day spend exposure $509,589 (calculated as $3,100,000 divided by "
    "365, multiplied by 60). Direct cost: spot premium $152,877 (30% of $509,589) plus expedited "
    "freight $150,000, totaling $302,877. Indirect cost: production downtime $25,000 per day for "
    "30 days, totaling $750,000. Total financial impact: approximately $1,052,877. Recovery "
    "timeline: ITEM-0013 alternate (Summit Metals) available in 10 weeks. ITEM-0025 has no "
    "alternate, extending full recovery to 6 to 12 months."
)

add_para("What Claude did, behind the scenes:", bold=True)
add_numbered(
    "Read CLAUDE.md to load the output standards (USD with commas, no vague language)."
)
add_numbered(
    "Read data/disruption-events.md to extract historical cost patterns: spot premium rates, "
    "freight surcharges, and daily downtime costs from the four events."
)
add_numbered(
    "Read data/supplier-master.csv to confirm Pacific Aluminum's annual spend of $3,100,000."
)
add_numbered(
    "Calculated 60-day spend exposure: $3,100,000 divided by 365, multiplied by 60."
)
add_numbered(
    "Applied the 30% spot-market premium to the 60-day spend figure and added the $150,000 "
    "expedited freight surcharge to get total direct cost."
)
add_numbered(
    "Multiplied $25,000 per-day downtime by 30 days (the period before alternates ramp up) "
    "to get indirect cost."
)
add_numbered(
    "Read data/approved-alternates.csv to check alternate availability for Pacific Aluminum's "
    "items and set the recovery timeline accordingly."
)

# ================================================================
#  DAY IN THE LIFE
# ================================================================
doc.add_heading("Day in the Life: James, Supply Chain Risk Manager", level=1)

add_para(
    "James is a Supply Chain Risk Manager at Fortis Manufacturing, a mid-size US manufacturer "
    "with 25 suppliers across five categories. He reports to the CPO and prepares the quarterly "
    "board risk brief. His company uses Claude Code (in the terminal) for risk analysis. Below is "
    "a typical Thursday when the board meeting has been moved up and the CPO needs the resilience "
    "brief by Monday."
)

doc.add_heading("07:45. The CPO calls from the airport", level=3)

add_para(
    "James checks his phone before coffee. The CPO's message: \"Board meeting moved to next "
    "Thursday. I need the risk posture and resilience plan. Full brief, three pages. Don't give "
    "me the 28-page report.\" James opens his laptop, navigates to the practice folder, and starts "
    "Claude Code."
)

add_code_block(
    "cd Course_19_Supply_Chain_Risk/practice\n"
    "claude\n"
    "The folder data/ holds the source files. Do not edit any file in data/.\n"
    "Read from it freely. Save all output to Drafts/."
)

add_para(
    "He checks that CLAUDE.md has the current scoring matrix. It does. The five-factor weights "
    "and scoring bands are there from last quarter. He moves on."
)

add_para(
    "What to learn from this. James did not start from scratch. The scoring matrix lives in "
    "CLAUDE.md, so every new session picks it up automatically. A risk manager who encodes their "
    "method once reuses it every quarter without re-explaining the rules.",
    italic=True
)

doc.add_heading("08:15. Score the portfolio", level=3)

add_para(
    "James needs all 25 suppliers scored before he can pick the top risks for the board. He types "
    "one prompt."
)

add_code_block(
    "Score all 25 suppliers in data/supplier-master.csv against the risk\n"
    "scoring matrix in CLAUDE.md. For each supplier, show the five factor\n"
    "scores and the weighted overall score. Sort by overall score descending.\n"
    "Flag any supplier in the critical (2.50-3.00) or high (2.00-2.49)\n"
    "range. Save to Drafts/risk-register.md."
)

add_para(
    "Claude Code reads all 25 rows, applies the matrix, and saves the register. Three suppliers "
    "land in the critical range: Apex Electronics (2.85), Midwest Precision (2.70), and Eagle "
    "Transport (2.55). James reviews the scores for 5 minutes, confirms the top three match his "
    "intuition, and moves on. Total time: 12 minutes."
)

add_para(
    "What to learn from this. One prompt scored 25 suppliers. Manually, this takes 4 hours because "
    "each supplier requires lookups across three files. Claude Code reads all three files in "
    "parallel and applies the matrix consistently. The output is a sorted table, not a "
    "color-coded spreadsheet that only the person who built it can read.",
    italic=True
)

doc.add_heading("09:00. Map single-source exposure", level=3)

add_para(
    "The CPO specifically asked about backup plans. James needs to know which items have no "
    "alternate supplier."
)

add_code_block(
    "Build the single-source exposure map by joining\n"
    "data/single-source-items.csv with data/approved-alternates.csv on\n"
    "item_id. Use a left join. Flag items with no alternate as CRITICAL GAP.\n"
    "Show spend totals by alternate status. Save to\n"
    "Drafts/single-source-exposure-map.md."
)

add_para(
    "The output shows 5 single-source items totaling $2,580,000. Two items ($620,000 combined) "
    "have no alternate. James highlights ITEM-0025 (Microcontroller ARM, $480,000, Apex "
    "Electronics, criticality: critical) as the top gap. This is the item the board needs to see "
    "first. Total time: 8 minutes."
)

add_para(
    "What to learn from this. Claude Code joined three CSV files in one prompt. A left join "
    "ensures that items with no alternate still appear in the output, flagged as critical gaps. "
    "Without the left join, those items would silently disappear, and the board would think every "
    "item has a backup.",
    italic=True
)

doc.add_heading("09:30. Model two disruption scenarios", level=3)

add_para(
    "The CFO wants dollar figures for a worst-case. James models the two most expensive scenarios: "
    "Pacific Aluminum offline for 60 days and Continental Freight losing capacity for 45 days."
)

add_code_block(
    "Model this scenario: Pacific Aluminum (SUP003) experiences a facility\n"
    "shutdown for 60 days. Annual spend: $3,100,000. Spot-market premium:\n"
    "30%. Expedited freight: $150,000. Production downtime: $25,000/day for\n"
    "30 days. Calculate direct cost, indirect cost, total impact, and\n"
    "recovery timeline. Save to Drafts/disruption-scenarios.md."
)

add_para(
    "Pacific Aluminum: $1,052,877 total impact. James runs the second scenario for Continental "
    "Freight ($610,959 total impact) and saves both to the same file. He adds a comparison table "
    "with one more prompt. Total time for both scenarios: 20 minutes."
)

add_para(
    "What to learn from this. Each scenario uses a prompt that states all assumptions explicitly: "
    "the premium rate, the freight surcharge, and the daily downtime cost. Those assumptions came "
    "from historical events in disruption-events.md. Stating them in the prompt means the board "
    "can challenge any number, and James can re-run the model with a different assumption in "
    "under two minutes.",
    italic=True
)

doc.add_heading("10:15. Build the mitigation plan", level=3)

add_para(
    "James now has three draft files. He needs to turn them into a ranked action plan with costs "
    "and a payback ratio."
)

add_code_block(
    "Build a risk-ranked mitigation plan from the three draft files in\n"
    "Drafts/. For each critical or high risk, generate one specific action\n"
    "with a cost and timeline. Rank by risk reduction ratio (exposure\n"
    "reduced divided by cost). Select the top 5. Add an investment case at\n"
    "the top. Save to Drafts/mitigation-plan.md."
)

add_para(
    "Claude Code extracts risks from all three files, generates specific actions (not generic "
    "suggestions), calculates the reduction ratio for each, and selects the top five. The "
    "investment case shows: $340,000 total cost, $4,200,000 exposure reduced, 12.4x payback. "
    "The recommendation paragraph names three actions with deadlines. Total time: 15 minutes."
)

add_para(
    "What to learn from this. Claude Code read three separate draft files and synthesized them "
    "into one plan. The risk reduction ratio (exposure reduced divided by cost) is the ranking "
    "mechanism that makes the plan an investment case, not a wish list. Any procurement "
    "professional can apply this ratio to any set of risks and actions.",
    italic=True
)

doc.add_heading("11:00. Assemble the board brief", level=3)

add_para(
    "Four draft files are ready. James assembles the three-page brief in one prompt."
)

add_code_block(
    "Assemble the board resilience brief from the four draft files in\n"
    "Drafts/. Structure: executive summary (one sentence), three key\n"
    "findings (number first, supplier named), top 5 risks table (by\n"
    "annual_exposure_usd), investment case (cost, exposure reduced, payback\n"
    "ratio, three-action recommendation). Title: \"Supply Chain Risk and\n"
    "Resilience Brief, Q2 2026 - Fortis Manufacturing.\" Date: 2026-04-25.\n"
    "Save to Drafts/board-resilience-brief.md."
)

add_para(
    "The brief saves in under a minute. James reads it, confirms the executive summary names "
    "a supplier (Apex Electronics), a value ($620,000 unprotected exposure), and a date "
    "(2026-05-15 investment deadline). Each finding starts with a number. The risk table has "
    "exactly five rows. The recommendation names three actions. He makes two minor edits "
    "(tightens a sentence, corrects a rounding) and emails the brief to the CPO by 11:30."
)

add_para(
    "What to learn from this. The entire pipeline, from raw data to board brief, took James about "
    "65 minutes of active work. Last quarter, three analysts spent two weeks. The difference is "
    "not that Claude Code is faster at typing. It is that the scoring matrix, the data files, and "
    "the output standards are all encoded so Claude Code can read and apply them in one pass. "
    "The analyst's job shifts from data assembly to judgment: reviewing the scores, validating "
    "the assumptions, and editing the brief.",
    italic=True
)

doc.add_heading("11:30. Peer review", level=3)

add_para(
    "James asks a colleague, Maria, to review the brief. She opens Claude Code in the same folder "
    "and runs a validation prompt."
)

add_code_block(
    "Read Drafts/board-resilience-brief.md and check it against these rules:\n"
    "1. Does the executive summary name a supplier, a dollar value, and a date?\n"
    "2. Does each key finding start with a number written as a figure?\n"
    "3. Does the risk table have exactly 5 rows?\n"
    "4. Does the recommendation paragraph name 3 actions or fewer?\n"
    "5. Are all currency figures in USD with commas?\n"
    "6. Are there any em-dashes, en-dashes, or banned phrases?\n"
    "Report pass or fail for each rule."
)

add_para(
    "Six passes. Maria spots one sentence that could be tighter and edits it by hand. The brief "
    "is ready for the CPO by noon."
)

add_para(
    "What to learn from this. A second person can validate the brief using the same CLAUDE.md "
    "output standards. The validation prompt is reusable. Every board brief this team produces "
    "goes through the same six-point check. The standards are written down, not in someone's head.",
    italic=True
)

# ================================================================
#  20-MINUTE SPRINT
# ================================================================
doc.add_heading("20-Minute Sprint: Your First Risk Score", level=1)

add_para(
    "This section gets you from zero to your first scored supplier in 20 minutes. "
    "Follow the four blocks in order. Do not skip steps."
)

doc.add_heading("Minutes 0 to 5: Install and open Claude Code", level=3)

add_numbered(
    "Open a terminal window. On Windows, press Win+R, type cmd, and press Enter. "
    "On Mac, open Terminal from Applications."
)
add_numbered(
    "If Claude Code is not installed, run: npm install -g @anthropic-ai/claude-code"
)
add_numbered(
    "Navigate to the course folder:"
)
add_code_block(
    "cd Course_19_Supply_Chain_Risk/practice"
)
add_numbered(
    "Start Claude Code:"
)
add_code_block(
    "claude"
)
add_numbered(
    "You should see the Claude Code prompt with the folder name at the top."
)

doc.add_heading("Minutes 5 to 10: Set the ground rules and read the data", level=3)

add_numbered(
    "Type the read-only rule:"
)
add_code_block(
    "The folder data/ holds the source files. Do not edit any file in data/.\n"
    "Read from it freely. Save all output to Drafts/."
)
add_numbered(
    "Confirm the scoring matrix is loaded:"
)
add_code_block(
    "Read CLAUDE.md and show me the risk scoring matrix section."
)
add_numbered(
    "You should see a table with five risk factors, their weights, and their scoring bands. If "
    "you see an empty file, confirm you are in the practice/ folder."
)
add_numbered(
    "Check the supplier data:"
)
add_code_block(
    "Read data/supplier-master.csv and show me the first 5 rows."
)
add_numbered(
    "You should see columns including supplier_id, supplier_name, financial_health_score, "
    "geographic_concentration, and single_source_items."
)

doc.add_heading("Minutes 10 to 15: Score your first supplier", level=3)

add_numbered(
    "Pick a supplier and score it:"
)
add_code_block(
    "Using the risk scoring matrix in CLAUDE.md, score supplier SUP004\n"
    "(Apex Electronics) from data/supplier-master.csv. Show the score for\n"
    "each factor and the weighted overall score."
)
add_numbered(
    "You should see Apex Electronics with a critical-range score (2.50 to 3.00). Financial "
    "health 44.8 scores 3. Geographic concentration \"high\" scores 3. Single-source items 4 "
    "scores 3."
)
add_numbered(
    "If the score looks wrong, ask Claude Code to show the calculation step by step."
)

doc.add_heading("Minutes 15 to 20: Score the full portfolio and review", level=3)

add_numbered(
    "Score all 25 suppliers in one prompt:"
)
add_code_block(
    "Score all 25 suppliers in data/supplier-master.csv against the risk\n"
    "scoring matrix in CLAUDE.md. Sort by overall score descending. Save to\n"
    "Drafts/risk-register.md."
)
add_numbered(
    "Open Drafts/risk-register.md and review the top 5. Do the critical-range suppliers match "
    "your expectations? If Apex Electronics, Midwest Precision, and Eagle Transport are in the "
    "top three, the matrix is working correctly."
)
add_numbered(
    "You now have a scored risk register for 25 suppliers. Next step: concentration "
    "risk analysis."
)

# ================================================================
#  FIRST WEEK PLANNER
# ================================================================
doc.add_heading("First Week Day-by-Day Planner", level=1)

add_para(
    "This planner assumes you spend 60 to 90 minutes per day on the course. By Friday, you will "
    "have a complete board resilience brief built from your practice data."
)

doc.add_heading("Day 1 (Monday): Install, set up, and score the portfolio", level=3)

add_para("Goals:", bold=True)
add_bullet("Install Claude Code and confirm it runs.")
add_bullet("Navigate to the practice folder and verify all five data files are present.")
add_bullet("Encode the scoring matrix in CLAUDE.md and score all 25 suppliers.")
add_bullet(
    "Deliverable: Drafts/risk-register.md with 25 suppliers scored and sorted by weighted "
    "risk score."
)

doc.add_heading("Day 2 (Tuesday): Concentration risk and single-source exposure", level=3)

add_para("Goals:", bold=True)
add_bullet(
    "Calculate share of wallet, geographic clustering, and category dominance. "
    "Save Drafts/concentration-risk-summary.md."
)
add_bullet(
    "Build the single-source exposure map by joining three data files. "
    "Save Drafts/single-source-exposure-map.md."
)
add_bullet(
    "Deliverable: two draft files showing where Fortis Manufacturing's supply chain is most "
    "concentrated and which items have no backup supplier."
)

doc.add_heading("Day 3 (Wednesday): Disruption scenario modeling", level=3)

add_para("Goals:", bold=True)
add_bullet(
    "Model two disruption scenarios (Pacific Aluminum 60 days, Continental "
    "Freight 45 days) with financial impact. Save Drafts/disruption-scenarios.md."
)
add_bullet(
    "Review the cost assumptions. Challenge at least one assumption (for example, change the "
    "spot premium from 30% to 40%) and re-run the model to see the impact."
)
add_bullet(
    "Deliverable: Drafts/disruption-scenarios.md with two scenarios, a comparison table, and "
    "board takeaway sentences."
)

doc.add_heading("Day 4 (Thursday): Mitigation planning", level=3)

add_para("Goals:", bold=True)
add_bullet(
    "Extract risks from three draft files, generate specific mitigation "
    "actions, calculate risk reduction ratios, rank and select the top five. Save "
    "Drafts/mitigation-plan.md."
)
add_bullet(
    "Add the investment case section at the top: total cost, total exposure reduced, payback "
    "ratio, three-action recommendation paragraph."
)
add_bullet(
    "Deliverable: Drafts/mitigation-plan.md with a $340,000 investment case and 12.4x payback."
)

doc.add_heading("Day 5 (Friday): Board brief and review", level=3)

add_para("Goals:", bold=True)
add_bullet(
    "Assemble the board resilience brief from four draft files. Save "
    "Drafts/board-resilience-brief.md."
)
add_bullet(
    "Run the six-point validation check against the output standards."
)
add_bullet(
    "Compare your outputs against the reference answers in solutions/."
)
add_bullet(
    "Deliverable: a three-page board brief with three key findings, a top-five risk table, "
    "and an investment case. The full pipeline runs from raw data to board brief."
)

add_para(
    "By Friday afternoon, you have a repeatable risk assessment pipeline. Next quarter, updating "
    "the data files and re-running the pipeline takes under 90 minutes, not two weeks."
)

# ================================================================
#  THE PATTERN
# ================================================================
doc.add_heading("The Pattern: From Data to Board Brief in One System", level=1)

add_para(
    "Every supply chain risk assessment follows the same shape, regardless of the number of "
    "suppliers, the industry, or the board's specific questions. The pattern has five stages."
)

add_numbered(
    "Encode the scoring method. Write the risk factors, weights, and scoring bands into CLAUDE.md "
    "so Claude Code (in the terminal) applies them consistently. This is a one-time setup that "
    "carries forward to every future session."
)
add_numbered(
    "Find concentration. Read the supplier master and spend files together. Identify share of "
    "wallet, geographic clustering, and category dominance. Save the findings with specific "
    "supplier names, dollar amounts, and percentages."
)
add_numbered(
    "Map exposure. Join the single-source items with the approved alternates. Flag every item "
    "with no backup. Quantify the unprotected spend."
)
add_numbered(
    "Model scenarios. Pick the two or three most consequential supplier failures. Calculate "
    "direct cost, indirect cost, and recovery timeline using assumptions drawn from historical "
    "events. State every assumption explicitly."
)
add_numbered(
    "Assemble the brief. Pull from all draft files into a three-section document: findings, "
    "risk table, and investment case. Cap recommendations at three. Start every finding with "
    "a number. Name a supplier, a value, and a date in the executive summary."
)

add_para(
    "Why this matters. The pattern is transferable. If your organization has 50 suppliers instead "
    "of 25, the prompts do not change. You update the data files and re-run. If your board wants "
    "ESG risk instead of financial health, you add an ESG factor to CLAUDE.md and re-score. The "
    "pattern separates the method (encoded in CLAUDE.md) from the data (in data/) from the output "
    "(in Drafts/). Changing one does not require rebuilding the other two.",
    italic=True
)

add_para(
    "The personalization approach. CLAUDE.md in the practice folder is a single-purpose instruction "
    "file. It holds the role definition, the scoring matrix, and the output standards. For a real "
    "engagement, you might split this into multiple files at the project root: one for role and "
    "context, one for scoring logic, one for output formatting rules. Claude Code (in the terminal) "
    "reads all CLAUDE.md files in the folder hierarchy and combines them."
)

# ================================================================
#  TROUBLESHOOTING
# ================================================================
doc.add_heading("Troubleshooting", level=1)

add_para(
    "Below are the six most common problems you will encounter during this course, with "
    "specific fixes for each."
)

doc.add_heading("1. All 25 suppliers receive the same overall score", level=3)
add_para(
    "Cause: the scoring bands in CLAUDE.md are too broad, or the data column names in the prompt "
    "do not match the CSV headers."
)
add_para(
    "Fix: read CLAUDE.md and confirm the bands have distinct thresholds (0 to 49, 50 to 69, "
    "70 to 100 for financial health). Then ask Claude Code (in the terminal) to show the column "
    "headers from data/supplier-master.csv. If the CSV says \"fin_health_score\" but CLAUDE.md "
    "says \"financial_health_score,\" the lookup fails silently and every supplier defaults to "
    "the same score."
)

doc.add_heading("2. The weighted score exceeds 3.00", level=3)
add_para(
    "Cause: the five weights in CLAUDE.md do not sum to 1.00. A typo in one weight (0.30 instead "
    "of 0.25) inflates the total."
)
add_para(
    "Fix: ask Claude Code (in the terminal) to read CLAUDE.md and sum the five weights. The sum "
    "must equal 1.00: 0.25 + 0.15 + 0.25 + 0.20 + 0.15 = 1.00. If it does not, correct the "
    "weight that is off and re-score."
)

doc.add_heading("3. Geographic analysis shows every state with only one supplier", level=3)
add_para(
    "Cause: the state column in supplier-master.csv uses inconsistent formats. \"TX\" and \"Texas\" "
    "do not group together."
)
add_para(
    "Fix: ask Claude Code (in the terminal) to show the unique values in the state column. If "
    "you see both abbreviations and full names, ask Claude to normalize to two-letter state codes "
    "before grouping."
)

doc.add_heading("4. The joined table has more than 5 rows in the exposure map", level=3)
add_para(
    "Cause: ITEM-0001 has two alternates in approved-alternates.csv (Summit Metals and Liberty "
    "Composites). A standard left join produces 6 rows."
)
add_para(
    "Fix: ask Claude Code (in the terminal) to deduplicate by keeping the qualified alternate "
    "over the in-qualification one. The goal is one row per item showing the best available "
    "alternate. You should end up with exactly 5 rows."
)

doc.add_heading("5. Disruption scenario shows unrealistically high impact (above $5,000,000)", level=3)
add_para(
    "Cause: the per-day downtime cost was entered as $250,000 instead of $25,000, inflating "
    "indirect cost by 10x."
)
add_para(
    "Fix: review the assumptions in the prompt. Production downtime at $25,000 per day for 30 "
    "days is $750,000. At $250,000 per day, it becomes $7,500,000. Correct the assumption and "
    "re-run the model. Always state assumptions explicitly in the prompt so they are auditable."
)

doc.add_heading("6. The board brief recommendation lists more than three actions", level=3)
add_para(
    "Cause: CLAUDE.md caps recommendation lists at three, but Claude Code sometimes includes "
    "four or five if the prompt does not repeat the cap."
)
add_para(
    "Fix: add \"Three actions maximum\" to the prompt when asking for the investment case "
    "section. If the output still has more than three, ask Claude Code (in the terminal) to "
    "keep the three actions with the highest risk reduction ratio and move the rest to a note "
    "labeled \"Additional actions, ranked.\""
)

# ================================================================
#  CAUTIONS AND GROUND RULES
# ================================================================
doc.add_heading("Cautions and Ground Rules", level=1)

add_bullet(
    " Claude Code (in the terminal) reads your data files and applies your scoring logic. It "
    "does not access external databases, credit agencies, or real-time supplier data. If your "
    "supplier-master.csv is six months old, the scores reflect six-month-old data.",
    bold_prefix="Data freshness."
)
add_bullet(
    " Every disruption scenario depends on stated assumptions: the spot premium rate, the "
    "daily downtime cost, the recovery timeline. If an assumption is wrong, the model output "
    "is wrong. State every assumption in the prompt. Challenge at least one before presenting "
    "to the board.",
    bold_prefix="Assumption validation."
)
add_bullet(
    " Claude Code (in the terminal) can read and process CSV, markdown, and text files directly. "
    "For Excel (.xlsx) files, save them as CSV first or use a conversion step. For PDF supplier "
    "reports, Claude Code reads them directly but may miss tables embedded as images.",
    bold_prefix="File format limits."
)
add_bullet(
    " The practice data (25 suppliers, 200 line items) runs fast. A production portfolio with "
    "500 suppliers and 10,000 line items will take longer per prompt. Break large portfolios "
    "into category-level batches if prompts time out.",
    bold_prefix="Scale limits."
)
add_bullet(
    " Do not paste confidential supplier financials, pricing data, or contract terms into Claude "
    "Code unless your organization's data policy permits it. Use anonymized or masked data for "
    "training. This course uses fictional data for exactly this reason.",
    bold_prefix="Confidentiality."
)
add_bullet(
    " The scoring matrix, the assumptions, and the output standards are all visible in CLAUDE.md "
    "and in the prompts. Any reviewer can trace every number back to a data source and a rule. "
    "This is the standard a board expects. If a number cannot be traced, do not include it.",
    bold_prefix="Auditability."
)

# ================================================================
#  DONE CHECKLIST
# ================================================================
doc.add_heading("Done Checklist", level=1)

add_para(
    "This checklist was run before saving this handout. Each item is marked done, deferred, "
    "or N/A."
)

checklist = [
    ("1. S2P problem named in the opening section.", "Done"),
    ("2. Outcome stated in business terms before any command.", "Done"),
    ("3. Every S2P task has a worked example with four parts: prompt, folder layout, "
     "what you see, behind-the-scenes walkthrough.", "Done"),
    ("4. Every capability statement names the specific Claude: Claude Code (in the terminal).", "Done"),
    ("5. For lessons, every step has: what you do, what you type, what you see.", "N/A (handout, not lesson)"),
    ("6. At least one full worked example with realistic fake data.", "Done (three worked examples)"),
    ("7. Troubleshooting entries.", "Done (six entries)"),
    ("8. No em-dashes or en-dashes.", "Done"),
    ("9. No banned phrases.", "Done"),
    ("10. Oxford commas applied.", "Done"),
    ("11. No rhetorical questions as openers.", "Done"),
    ("12. Risk text in active voice, actor named.", "Done"),
    ("13. Every figure is a real number, not vague.", "Done"),
    ("14. Sample executive summary names a supplier, a value, and a date.", "Done"),
    ("15. Recommendation list has three items or fewer.", "Done"),
    ("16. File name matches convention.", "Done"),
    ("17. Screenshots cropped, captioned, fake data.", "N/A (no screenshots in this handout)"),
    ("18. Standard folder layout referenced.", "Done"),
    ("19. Readable by a procurement analyst with no coding background.", "Done"),
    ("20. Comprehensive training guide elements: time savings table, Day in the Life, "
     "20-Minute Sprint, First Week Planner, personalization pattern.", "Done"),
    ("21. Course-specific rules.", "N/A (handout, not course folder)"),
    ("22. Style check reports zero violations.", "Deferred (run after save)"),
    ("23. Every concept/folder/file has a Why it matters paragraph.", "Done"),
    ("24. Every Day-in-the-Life scenario has a What to learn from this paragraph.", "Done"),
]

add_table(
    ["Item", "Status"],
    [[item, status] for item, status in checklist],
    col_widths=[5.5, 1.8]
)

# ================================================================
#  SAVE
# ================================================================
doc.save(str(OUT))
print(f"Saved: {OUT}")
print(f"Size: {OUT.stat().st_size:,} bytes")
