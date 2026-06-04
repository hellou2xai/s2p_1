"""
Build Course 17: Market Intelligence Handout as .docx
Run: python scripts/build_course17_handout.py
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

OUTPUT = Path(__file__).resolve().parent.parent / "Handouts" / "Course_17_Market_Intelligence_Handout.docx"

doc = Document()

# ── Styles ──────────────────────────────────────────────────────────────────
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

for level in range(1, 4):
    hs = doc.styles[f"Heading {level}"]
    hs.font.name = "Calibri"
    hs.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
    if level == 1:
        hs.font.size = Pt(18)
        hs.font.bold = True
    elif level == 2:
        hs.font.size = Pt(14)
        hs.font.bold = True
    else:
        hs.font.size = Pt(12)
        hs.font.bold = True

# helpers
def add_para(text, bold=False, italic=False, style_name="Normal", alignment=None, space_after=None):
    p = doc.add_paragraph(style=style_name)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    if alignment is not None:
        p.alignment = alignment
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p

def add_code_block(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.3)
    # Set paragraph shading
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F2F2F2" w:val="clear"/>')
    p.paragraph_format.element.get_or_add_pPr().append(shading)
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
    return p

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r2 = p.add_run(text)
        r2.font.name = "Calibri"
        r2.font.size = Pt(11)
    else:
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(11)
    return p

def add_numbered(text):
    p = doc.add_paragraph(style="List Number")
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    return p

def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    # header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        # header shading
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1B3A5C" w:val="clear"/>')
        cell._element.get_or_add_tcPr().append(shading)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    # data rows
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.name = "Calibri"
            run.font.size = Pt(10)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()  # spacing
    return table

# ============================================================================
# HEADER
# ============================================================================
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
run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
p.paragraph_format.space_after = Pt(2)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Course 17: Market Intelligence and Demand Management")
run.bold = True
run.font.size = Pt(20)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
p.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Comprehensive Training Guide")
run.font.size = Pt(12)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
p.paragraph_format.space_after = Pt(2)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Date: 2026-04-26  |  Version 1.0  |  Platform: Claude Code (in the terminal)")
run.font.size = Pt(10)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

doc.add_page_break()

# ============================================================================
# 1. HOW TO USE THIS HANDOUT
# ============================================================================
doc.add_heading("How to Use This Handout", level=1)

add_para(
    "This handout is your companion for Course 17: Market Intelligence and Demand Management. "
    "It covers the full workflow: ingesting market reports, tracking commodity prices, consolidating "
    "stakeholder demand across departments, analyzing make-versus-buy decisions, and producing "
    "sourcing briefs grounded in real market data. Everything runs through Claude Code (in the terminal)."
)

add_para(
    "The handout follows a natural workflow progression. You start by reading and structuring market "
    "data. Then you track commodity price trends. Next you process stakeholder requirements and "
    "consolidate overlapping demand. Finally you connect market intelligence to sourcing decisions. "
    "Each section includes prompts you can copy and paste, folder layouts, expected outputs, and "
    "a behind-the-scenes walkthrough explaining what Claude Code did."
)

add_para(
    "If you are opening this handout for the first time, skip to the 20-Minute Sprint on page 10 "
    "to get your first usable output in twenty minutes. Then come back and work through the full "
    "sections at your own pace."
)

add_para(
    "Every prompt in this handout is written for Claude Code (in the terminal). These prompts will "
    "not work in Claude AI Web (claude.ai in a browser) or Claude Desktop with Cowork because those "
    "interfaces cannot read local files on your machine. Claude Code is the only Claude product that "
    "reads your project folder, processes CSVs, and writes output files directly."
)

# ============================================================================
# 2. WHAT THIS COURSE TEACHES
# ============================================================================
doc.add_heading("What This Course Teaches", level=1)

add_para(
    "Most procurement teams source in the dark. Commodity price data sits in a spreadsheet that "
    "someone updates when they remember. Market reports arrive as PDFs and land in a shared folder "
    "nobody checks. Stakeholder requirements arrive by email, and nobody cross-references them "
    "across departments. The result: sourcing decisions based on last year's contracts, not this "
    "quarter's conditions. Volume aggregation opportunities missed because each department buys "
    "independently. No clear answer when the Director asks whether steel prices are trending up or down."
)

add_para(
    "This course fixes that. You build a Claude Code (in the terminal) system that does three things:"
)

add_numbered(
    "Commodity tracking. Claude Code reads 24 months of price history from a CSV, calculates "
    "month-over-month and year-over-year changes, identifies trend direction (rising, falling, "
    "stable, volatile), and flags inflection points where the trend reversed."
)
add_numbered(
    "Demand consolidation. Claude Code reads stakeholder requirement submissions from multiple "
    "departments, structures them into a consistent format, groups overlapping requests by commodity, "
    "calculates combined volumes, and estimates volume discount opportunities."
)
add_numbered(
    "Market-linked sourcing recommendations. Claude Code combines commodity trends, market report "
    "signals, supplier capabilities, and demand data to produce a sourcing brief that adjusts "
    "RFP evaluation weights based on current market conditions."
)

add_para(
    "By the end of the course, when your Director asks about steel prices, you run one command and "
    "get a brief with 24 months of price history, the current trend, a year-over-year percentage, "
    "and a recommendation tied to supply conditions. Total time: about two minutes."
)

# ============================================================================
# 3. WHAT IS IN THE COURSE FOLDER
# ============================================================================
doc.add_heading("What Is in the Course Folder", level=1)

add_para(
    "The course folder is self-contained. Everything you need is inside. No external downloads, "
    "no shared drives, no separate data stores. Here is the structure:"
)

add_code_block(
    "Course_17_Market_Intelligence/\n"
    "  README.md                      (start here)\n"
    "  COURSE_OVERVIEW.md             (scenario, rubric, what 'done' looks like)\n"
    "  lessons/                       (6 numbered lesson files)\n"
    "    Lesson_01_Market_Intelligence_Ingestion.md\n"
    "    Lesson_02_Commodity_Tracker.md\n"
    "    Lesson_03_Requirements_Processing.md\n"
    "    Lesson_04_Demand_Consolidation.md\n"
    "    Lesson_05_Make_Vs_Buy.md\n"
    "    Lesson_06_Sourcing_Brief.md\n"
    "  practice/                      (your hands-on workspace)\n"
    "    CLAUDE.md                    (role, rules, output standards)\n"
    "    commodity-prices.csv         (192 rows, 8 commodities, 24 months)\n"
    "    supplier-capabilities.csv    (20 suppliers)\n"
    "    demand-intake/               (6 requirement files)\n"
    "    market-intelligence/         (4 quarterly market reports)\n"
    "    Drafts/                      (your working files go here)\n"
    "  solutions/                     (reference answers, look after attempting)\n"
    "  scripts/                       (data regeneration script)"
)

add_para(
    "Why this matters. The folder layout enforces the rule that source data stays untouched and "
    "outputs go to a separate location. If you delete or corrupt a practice file, the regeneration "
    "script in scripts/ rebuilds everything with one command. Without this structure, you risk "
    "editing source data by accident and losing the ability to restart a lesson cleanly.",
    italic=True
)

doc.add_heading("Key files explained", level=2)

add_para("CLAUDE.md (in the practice/ folder)", bold=True)
add_para(
    "This file tells Claude Code (in the terminal) who you are, what data files exist, and what "
    "rules to follow. It defines your role as Market Intelligence Analyst at Atlas Manufacturing. "
    "It lists the commodity tracking rules (3-month moving average for trend, 5% volatility "
    "threshold), the demand consolidation rules (match by commodity, check specification "
    "compatibility, 3% discount per volume doubling), and the make-versus-buy decision rules "
    "(recommend make only if 15% cheaper and capacity is available)."
)
add_para(
    "Why this matters. Without CLAUDE.md, Claude Code produces generic analysis. With it, every "
    "output uses Atlas Manufacturing's context, Atlas's rules, and Atlas's folder structure. "
    "The CLAUDE.md file is what turns a general-purpose AI tool into a procurement-specific system.",
    italic=True
)

add_para("commodity-prices.csv", bold=True)
add_para(
    "This file holds 192 rows of monthly price data for 8 commodities over 24 months (April 2024 "
    "through March 2026). Columns include commodity_id, commodity_name, unit, date, price, "
    "change_pct, and trend. This is your primary market data source."
)
add_para(
    "Why this matters. Without price history, commodity tracking is impossible. Claude Code reads "
    "this CSV to calculate trends, flag volatility, and ground sourcing recommendations in real numbers "
    "instead of opinions.",
    italic=True
)

add_para("demand-intake/ (6 files)", bold=True)
add_para(
    "Six stakeholder requirement files from five departments. Formats vary: some are structured forms, "
    "others are emails or memos. Two of them request polymer resin, creating a consolidation opportunity. "
    "The requirements cover steel, polymer resin, natural gas, electronic components, and diesel fuel."
)
add_para(
    "Why this matters. In real procurement, requirements arrive in inconsistent formats. This folder "
    "simulates that reality. Claude Code reads each file, extracts structured fields, and flags "
    "missing information so you can follow up before sourcing begins.",
    italic=True
)

add_para("market-intelligence/ (4 reports)", bold=True)
add_para(
    "Four quarterly market reports covering steel, polymers, logistics, and IT services. Each report "
    "includes supply conditions, price outlooks, and risk factors. These are the external market signals "
    "that inform your sourcing decisions."
)
add_para(
    "Why this matters. Market reports are useless sitting in a shared folder unread. Claude Code "
    "extracts structured signals from each report and connects them to your commodity tracking and "
    "sourcing recommendations. A market report about steel prices rising 8-12% becomes a signal "
    "that adjusts your RFP evaluation weights.",
    italic=True
)

# ============================================================================
# 4. TIME SAVINGS REFERENCE TABLE
# ============================================================================
doc.add_heading("Time Savings Reference Table", level=1)

add_para(
    "These estimates compare a procurement analyst doing each task manually (spreadsheets, reading "
    "reports, cross-referencing emails) against the same task with Claude Code (in the terminal). "
    "Times assume a comfortable working pace. Advanced users may be faster."
)

add_table(
    ["Task", "Without Claude Code", "With Claude Code", "Time saved"],
    [
        ["Read 4 market reports and extract key findings, price outlooks, and risk factors into a structured summary",
         "3 hours (read each report, take notes, compile findings manually)", "12 minutes (one prompt to read all 4 reports and write a signals file)", "2 hours 48 minutes"],
        ["Build a commodity price tracker for 8 commodities over 24 months with trend analysis and volatility flags",
         "4 hours (download data, build pivot tables, write formulas, format charts)", "15 minutes (one prompt to read the CSV, calculate all metrics, and write the dashboard)", "3 hours 45 minutes"],
        ["Process 6 stakeholder requirement submissions into a standardized format and flag missing fields",
         "2 hours (read each email or form, re-type into a template, check for gaps)", "10 minutes (one prompt to read all 6 files and write structured specs)", "1 hour 50 minutes"],
        ["Consolidate overlapping demand across departments and estimate volume discount opportunities",
         "1.5 hours (cross-reference spec sheets, compare items, sum quantities, look up discount tiers)",
         "8 minutes (one prompt to group specs, calculate combined volumes, and estimate savings)", "1 hour 22 minutes"],
        ["Produce a make-versus-buy analysis with total cost of ownership for both options and a break-even calculation",
         "3 hours (gather cost data, build cost model in Excel, calculate break-even, write recommendation)",
         "18 minutes (two prompts: one to build the cost model, one to write the recommendation)", "2 hours 42 minutes"],
    ]
)

add_para(
    "Across these five tasks, the manual approach takes about 13.5 hours. With Claude Code (in the "
    "terminal), the same work takes about 63 minutes. That is a reduction of roughly 12.4 hours per cycle."
)

# ============================================================================
# 5. WHAT MARKET INTELLIGENCE IS
# ============================================================================
doc.add_heading("What Market Intelligence Means for Procurement", level=1)

add_para(
    "Market intelligence in procurement is not a dashboard or a subscription service. It is the "
    "practice of connecting external market data to internal sourcing decisions. Three activities "
    "make up the core of market intelligence work."
)

doc.add_heading("Commodity tracking", level=2)

add_para(
    "Commodity tracking means monitoring the price of raw materials, energy, and services that your "
    "organization buys. At Atlas Manufacturing, that means tracking steel (hot rolled and cold rolled), "
    "polymer resin, aluminum sheet, copper wire, electronic components, natural gas, and diesel fuel. "
    "Each commodity has a unit (USD/ton, USD/kg, USD/lb, USD/each, USD/MMBtu, USD/gal) and a 24-month "
    "price history."
)

add_para(
    "Good commodity tracking answers four questions. First, is the price going up, down, or sideways? "
    "The CLAUDE.md file defines this using a 3-month moving average: if the current 3-month average "
    "is above the prior 3-month average, the trend is up. Second, how much has the price changed over "
    "the last year? Year-over-year change expressed as a percentage. Third, is the price volatile? "
    "If any month in the trailing 6 months shows a swing above 5%, the commodity is flagged as volatile. "
    "Fourth, where did the trend change direction? These inflection points are decision points for "
    "locking in pricing or switching suppliers."
)

add_para(
    "In Claude Code (in the terminal), you run a single prompt against commodity-prices.csv and get "
    "a tracker file with all four answers for every commodity. That tracker becomes the foundation for "
    "sourcing briefs and supplier negotiations."
)

doc.add_heading("Demand consolidation", level=2)

add_para(
    "Demand consolidation means grouping purchase requests from different departments that cover the "
    "same material. At Atlas Manufacturing, two departments submitted requests for polymer resin "
    "this month: Manufacturing needs 450 metric tons and R&D needs 120 metric tons. Both require "
    "industrial grade, pellet form. If sourced separately, each gets retail pricing. If consolidated "
    "into a single 570-metric-ton order, the combined volume qualifies for a volume discount."
)

add_para(
    "The consolidation rules in CLAUDE.md define four checks. Match by commodity (group requests for "
    "the same material). Match by specification (only consolidate if grades and forms are compatible). "
    "Calculate combined volume (sum quantities and apply the 3% per doubling discount rule). Flag "
    "timeline conflicts (if delivery dates are more than 90 days apart, note it but consider a "
    "blanket order)."
)

add_para(
    "Claude Code (in the terminal) reads all requirement files, groups them, calculates combined "
    "volumes, and writes a consolidation report with estimated savings. For the polymer resin "
    "example, the estimated savings are $15,818 on a combined spend of $1,054,500."
)

doc.add_heading("Make-versus-buy analysis", level=2)

add_para(
    "Make-versus-buy analysis compares the total cost of producing an item internally against the "
    "total cost of purchasing it from a supplier. The comparison is never as simple as unit price "
    "versus unit price. The buy side includes freight ($0.60/unit), quality inspection ($0.25/unit), "
    "and a safety stock risk premium (3% of unit price). The make side includes raw material cost, "
    "direct labor (0.15 hours at $32/hour), machine time (0.10 hours at $85/hour), tooling "
    "amortization ($28,000 over 24 months), in-process quality ($0.40/unit), and opportunity cost "
    "($2.00/unit for displaced CNC work)."
)

add_para(
    "The decision rule in CLAUDE.md says: recommend buy unless the total make cost is at least 15% "
    "lower than the total buy cost and internal capacity is available without displacing higher-margin "
    "work. This prevents the common mistake of switching to in-house production based on a unit-cost "
    "comparison that ignores overhead."
)

# ============================================================================
# 6. WORKED EXAMPLES
# ============================================================================
doc.add_heading("Worked Examples", level=1)

add_para(
    "Each worked example has four parts: the prompt you type in Claude Code (in the terminal), "
    "the folder layout, what you should see when it succeeds, and a behind-the-scenes walkthrough "
    "of what Claude Code did."
)

# ── Worked Example 1: Commodity Tracker ──
doc.add_heading("Worked Example 1: Building a Commodity Price Tracker for Steel", level=2)

add_para(
    "Your Director of Strategic Sourcing, Karen Webb, asks: \"Steel prices moved 12% in the last "
    "quarter. Should we lock in pricing now or wait?\" You need a tracker that shows 24 months of "
    "price history, the trend direction, year-over-year change, and a recommendation."
)

add_para("The prompt to type", bold=True)
add_code_block(
    "Read commodity-prices.csv. Filter to hot-rolled steel only. Calculate:\n"
    "1. The most recent price and the price 12 months ago.\n"
    "2. Year-over-year change in USD and percentage.\n"
    "3. Month-over-month change for the last 3 months.\n"
    "4. 3-month moving average for the current and prior periods.\n"
    "5. Trend direction (up, down, or stable per the rules in CLAUDE.md).\n"
    "6. Volatility flag (any month in trailing 6 months with change above 5%).\n"
    "7. Inflection points where trend direction changed.\n"
    "Write the full tracker to Drafts/tracker-hot-rolled-steel.md.\n"
    "Include a price table showing trailing 12 months,\n"
    "trend analysis, inflection points, and one recommendation\n"
    "on whether to lock in pricing now."
)

add_para("The folder layout", bold=True)
add_code_block(
    "practice/\n"
    "  commodity-prices.csv         (192 rows, read-only)\n"
    "  CLAUDE.md                    (commodity tracking rules)\n"
    "  Drafts/\n"
    "    tracker-hot-rolled-steel.md  (output)"
)

add_para("What you should see", bold=True)
add_para(
    "A markdown file in Drafts/ with a price table showing 12 months of hot-rolled steel prices, "
    "the current price at $720/ton, a year-over-year change of +7.0%, a trend direction of \"up\" "
    "(current 3-month average of $722 is above the prior 3-month average of $714), a volatility "
    "flag because March 2026 showed a -3.1% decline, and a recommendation to consider locking in "
    "pricing in May or June if prices dip below $710/ton."
)

add_para("What Claude Code did, behind the scenes", bold=True)
add_numbered(
    "Claude Code read all 192 rows of commodity-prices.csv and filtered to rows where "
    "commodity_name equals \"Steel (hot rolled).\" That produced 24 rows, one per month."
)
add_numbered(
    "It sorted the 24 rows by date ascending and identified the most recent price ($720/ton in "
    "2026-04) and the price 12 months prior ($673/ton in 2025-05)."
)
add_numbered(
    "It calculated year-over-year change: ($720 - $673) / $673 = +7.0%."
)
add_numbered(
    "It computed the 3-month moving average for the current period (Jan, Feb, Mar 2026: "
    "$728, $735, $712 = average $725) and the prior period (Oct, Nov, Dec 2025: "
    "$710, $698, $715 = average $708). Since $725 is above $708, the trend direction is \"up.\""
)
add_numbered(
    "It scanned the trailing 6 months for any single-month price change exceeding 5% in absolute "
    "value. March 2026 showed -3.1%, which is below 5%, but if any month exceeded it the commodity "
    "would be flagged as volatile."
)
add_numbered(
    "It identified inflection points: months where the trend changed from up to down or vice versa. "
    "Two inflection points appeared at 2025-08 (up to down) and 2025-09 (down to up)."
)
add_numbered(
    "It wrote the recommendation based on the upward trend and the March dip, suggesting a "
    "fixed-price agreement at $720/ton to protect against further increases."
)

# ── Worked Example 2: Demand Consolidation ──
doc.add_heading("Worked Example 2: Consolidating Polymer Resin Demand Across Departments", level=2)

add_para(
    "Two departments submitted overlapping requests for polymer resin this month. Manufacturing "
    "needs 450 metric tons for production line gaskets. R&D needs 120 metric tons for prototype "
    "testing. Both require industrial grade, pellet form. You want to consolidate these into a "
    "single sourcing action to capture volume pricing."
)

add_para("The prompt to type", bold=True)
add_code_block(
    "Read all files in demand-intake/. Structure each requirement using\n"
    "the Demand Specification Format from CLAUDE.md. Then group\n"
    "requirements that reference the same commodity. For each group\n"
    "with two or more requirements:\n"
    "1. Check specification compatibility.\n"
    "2. Calculate combined volume.\n"
    "3. Estimate volume discount (3% per doubling of volume).\n"
    "4. Check delivery date gap (flag if more than 90 days apart).\n"
    "Write the consolidation report to\n"
    "Drafts/demand-consolidation-report.md.\n"
    "Include a structured requirements table, the consolidation\n"
    "opportunity detail, and a recommendation for sourcing approach."
)

add_para("The folder layout", bold=True)
add_code_block(
    "practice/\n"
    "  demand-intake/               (6 requirement files, read-only)\n"
    "  supplier-capabilities.csv    (20 suppliers, read-only)\n"
    "  CLAUDE.md                    (consolidation rules)\n"
    "  Drafts/\n"
    "    demand-consolidation-report.md  (output)"
)

add_para("What you should see", bold=True)
add_para(
    "A markdown report showing 6 structured requirements from 5 departments. One consolidation "
    "opportunity: polymer resin. Combined volume of 570 metric tons (450 + 120). Specifications "
    "compatible (both industrial grade, pellet form). Delivery gap of 16 days (within the 90-day "
    "window). Estimated volume discount of 1.5% on combined spend of $1,054,500, saving approximately "
    "$15,818. Recommendation: issue a single blanket PO with two delivery dates."
)

add_para("What Claude Code did, behind the scenes", bold=True)
add_numbered(
    "Claude Code read each of the 6 files in demand-intake/ and extracted structured fields: "
    "department, requestor, commodity, quantity, specification, and delivery date."
)
add_numbered(
    "It compared the commodity field across all 6 requirements and found two entries for polymer "
    "resin (Manufacturing and R&D). The other four commodities (steel, natural gas, electronic "
    "components, diesel fuel) each appeared only once."
)
add_numbered(
    "For the polymer resin group, it checked specification compatibility. Both entries specified "
    "industrial grade, pellet form. Compatible."
)
add_numbered(
    "It calculated combined volume: 450 + 120 = 570 metric tons. Using the 3% per doubling rule, "
    "570/450 = 1.27x (not a full doubling), so the estimated discount is approximately 1.5%."
)
add_numbered(
    "It checked the delivery date gap: 2026-06-15 versus 2026-07-01 = 16 days. Within the "
    "90-day window. A blanket order with split delivery dates is viable."
)
add_numbered(
    "It calculated the savings: $1,054,500 (combined spend at $1,850/metric ton) x 1.5% = $15,818."
)
add_numbered(
    "It wrote the recommendation: issue a single blanket PO for 570 metric tons of polymer resin "
    "with two delivery dates, and negotiate volume pricing with Heartland Polymers."
)

# ── Worked Example 3: Market-Linked Sourcing Brief ──
doc.add_heading("Worked Example 3: Adjusting RFP Evaluation Weights Based on Market Signals", level=2)

add_para(
    "Your category manager is about to issue an RFP for industrial gaskets using last year's "
    "evaluation weights: price 50%, quality 25%, delivery 15%, service 10%. But steel prices are "
    "up 7% year-over-year. A tariff on imported gasket materials takes effect in 90 days. Two Midwest "
    "suppliers face logistics disruptions. The old weights will optimize for price in a rising-price "
    "market and ignore supply security. You need to adjust."
)

add_para("The prompt to type", bold=True)
add_code_block(
    "Read Drafts/market_signals.json and Drafts/commodity_tracker.json.\n"
    "The current RFP evaluation weights are: price 50%, quality 25%,\n"
    "delivery 15%, service 10%.\n"
    "For each active market signal, determine which criterion it affects:\n"
    "- Price movement signals: reduce price weight, shift to supply security.\n"
    "- Supply disruption signals: increase delivery weight.\n"
    "- Regulatory signals: increase quality/compliance weight.\n"
    "Calculate adjusted weights (must sum to 100%, no criterion above 40%\n"
    "or below 5%). Write a sourcing brief to\n"
    "Drafts/market-sourcing-brief.md with: market context table,\n"
    "weight adjustment table with justifications citing signal IDs,\n"
    "supplier landscape, and recommended sourcing approach.\n"
    "Valid for 90 days from 2026-04-26."
)

add_para("The folder layout", bold=True)
add_code_block(
    "practice/\n"
    "  Drafts/\n"
    "    market_signals.json        (from Lesson 1)\n"
    "    commodity_tracker.json     (from Lesson 2)\n"
    "  supplier-capabilities.csv    (read-only)\n"
    "  Drafts/\n"
    "    market-sourcing-brief.md   (output)"
)

add_para("What you should see", bold=True)
add_para(
    "A sourcing brief with adjusted weights: price drops from 50% to 35%, delivery increases from "
    "15% to 25%, quality stays at 25%, service adjusts to 15%. Each adjustment cites a specific "
    "signal ID. The brief names at least three suppliers from supplier-capabilities.csv and "
    "identifies which gain or lose competitive advantage under the new weights. The recommended "
    "approach is competitive bid with adjusted criteria."
)

add_para("What Claude Code did, behind the scenes", bold=True)
add_numbered(
    "Claude Code read the market signals JSON and identified price movement signals (steel up 7%), "
    "a regulatory signal (tariff in 90 days), and a supply disruption signal (Midwest logistics)."
)
add_numbered(
    "It mapped each signal to the evaluation criterion it affects using the mapping rules from "
    "the prompt: rising prices reduce price weight, disruptions increase delivery weight, and "
    "tariffs increase quality/compliance weight."
)
add_numbered(
    "It calculated specific weight adjustments for each criterion, then checked that no single "
    "criterion exceeded 40% or fell below 5% and that all four weights summed to 100%."
)
add_numbered(
    "It read supplier-capabilities.csv to identify suppliers in the Midwest (affected by the "
    "disruption), imported-material suppliers (affected by the tariff), and high-delivery-score "
    "suppliers (who benefit from the increased delivery weight)."
)
add_numbered(
    "It wrote the sourcing brief with all six sections: purpose, market context table, weight "
    "adjustments, supplier landscape, recommended approach, and 90-day validity note."
)

# ============================================================================
# 7. DAY IN THE LIFE
# ============================================================================
doc.add_heading("Day in the Life: Maria, Category Analyst", level=1)

add_para(
    "Maria Rodriguez is a Category Analyst at Atlas Manufacturing, a US-based industrial company "
    "with $58M in annual procurement spend. She covers raw materials (steel, polymers, aluminum) and "
    "reports to Karen Webb, Director of Strategic Sourcing. Maria has been using Claude Code (in the "
    "terminal) for two weeks. Today is a typical Thursday."
)

doc.add_heading("07:45. The CPO's morning question", level=3)

add_para(
    "Maria checks her phone on the way to her desk. An email from the CPO, David Torres: \"Board "
    "meeting next Tuesday. I need a one-page market summary: steel, polymers, and copper. Price "
    "trends, risks, and whether we should lock in any pricing. By end of day Friday.\" Maria used to "
    "spend four hours on this. She opens her terminal."
)

add_code_block(
    "cd market-intelligence-2026 && claude")
add_code_block(
    "Read commodity-prices.csv. For steel (hot rolled), polymer resin, and\n"
    "copper wire, calculate: current price, year-over-year change,\n"
    "trend direction, and volatility flag per the rules in CLAUDE.md.\n"
    "Read Drafts/market_signals.json for forward-looking context.\n"
    "Write a one-page executive summary to\n"
    "Drafts/board-market-summary.md with a commodity table,\n"
    "three key findings, and three recommendations (one per commodity).\n"
    "Date: 2026-04-26. Addressee: David Torres, CPO."
)

add_para(
    "Claude Code reads the CSV, filters to the three commodities, calculates all metrics, "
    "cross-references the market signals, and writes the summary. Maria reviews it in 3 minutes. "
    "She adjusts one recommendation (she knows the copper supplier is already locked in through "
    "Q3) and forwards it to David at 08:12. Total time: 15 minutes."
)

add_para(
    "What to learn from this. A commodity tracker is not a one-time report. It is a reusable "
    "data structure. When Maria runs the same prompt next month with updated price data, she gets "
    "a fresh summary without rebuilding anything. The CLAUDE.md rules (3-month moving average, "
    "5% volatility threshold) ensure consistency across months and analysts.",
    italic=True
)

doc.add_heading("09:00. New stakeholder requirement arrives", level=3)

add_para(
    "The plant manager, Jeff Park, sends Maria an email: \"Need 300 tons of cold-rolled steel, "
    "ASTM A1008, 0.5mm gauge, delivered by August 1. Budget code CAPEX-2026-014.\" Maria adds it "
    "to the demand-intake/ folder and processes it."
)

add_code_block(
    "Read demand-intake/jeff_park_cold_rolled_apr26.md.\n"
    "Structure it using the Demand Specification Format from CLAUDE.md.\n"
    "Check for missing fields. Append to Drafts/demand_specs.json."
)

add_para(
    "Claude Code reads the email, extracts all fields (item: cold-rolled steel, quantity: 300 tons, "
    "spec: ASTM A1008 0.5mm, delivery: 2026-08-01, budget: CAPEX-2026-014), and marks it complete. "
    "No missing fields. Maria moves on. Total time: 3 minutes."
)

add_para(
    "What to learn from this. Processing requirements one at a time as they arrive is faster than "
    "batching them at the end of the week. The structured JSON file grows with each addition, and "
    "the consolidation analysis in the next step always works against the latest data.",
    italic=True
)

doc.add_heading("10:30. Consolidation check before the sourcing meeting", level=3)

add_para(
    "Karen Webb messages Maria: \"Sourcing meeting at 11:00. Can you check if any of this month's "
    "requirements overlap? I do not want to issue five POs when two would do.\" Maria runs the "
    "consolidation prompt."
)

add_code_block(
    "Read Drafts/demand_specs.json. Group by commodity.\n"
    "For groups with two or more specs, check specification\n"
    "compatibility, calculate combined volume, and estimate\n"
    "volume discount (3% per doubling). Flag delivery date gaps\n"
    "above 90 days. Write to Drafts/consolidation-update.md."
)

add_para(
    "Claude Code identifies the polymer resin overlap (Manufacturing 450 tons + R&D 120 tons = "
    "570 tons, estimated savings $15,818) and a new potential overlap: Jeff Park's cold-rolled "
    "steel request could combine with the existing hot-rolled steel request if specifications are "
    "compatible (they are not, different grades). Maria brings the consolidation report to the "
    "meeting. Total time: 5 minutes."
)

add_para(
    "What to learn from this. Consolidation is not a one-time exercise. New requirements arrive "
    "throughout the month. Running the consolidation check before every sourcing meeting ensures "
    "you catch overlaps as they form, not after POs have already been issued.",
    italic=True
)

doc.add_heading("13:00. Make-versus-buy request from the plant", level=3)

add_para(
    "After lunch, Jeff Park stops by Maria's desk: \"We are paying $14.80 per unit for precision "
    "bushings from Apex Machining. Our CNC shop could make them for $9.00. Should we bring it "
    "in-house?\" Maria knows the $9.00 figure only covers raw material and labor. She runs the "
    "full analysis."
)

add_code_block(
    "Read supplier-capabilities.csv and commodity-prices.csv.\n"
    "Build a make-versus-buy analysis for precision bushings.\n"
    "Buy side: $14.80/unit + $0.60 freight + $0.25 inspection\n"
    "+ 3% risk premium. Make side: raw material from commodity\n"
    "prices + 10% waste, 0.15 hrs labor at $32/hr, 0.10 hrs\n"
    "machine at $85/hr, $28,000 tooling over 24 months at\n"
    "annual volume, $0.40 quality, $2.00 opportunity cost.\n"
    "Apply the 15% threshold from CLAUDE.md.\n"
    "Write to Drafts/make-vs-buy-bushings.md."
)

add_para(
    "Claude Code builds both cost models. The buy cost comes to $15.89/unit (including freight, "
    "inspection, and risk). The make cost comes to $13.42/unit (including all overhead that Jeff's "
    "$9.00 estimate missed). The make option is 15.5% cheaper, which just exceeds the 15% threshold. "
    "But Claude Code also notes that the CNC shop has only 22% capacity available, which is above "
    "the 20% floor but leaves little margin. Maria adds a risk note about capacity constraints and "
    "sends the analysis to Jeff with a recommendation: pilot 500 units in-house before committing "
    "to full production. Total time: 12 minutes."
)

add_para(
    "What to learn from this. The make-versus-buy framework in CLAUDE.md prevents the common mistake "
    "of comparing raw unit costs without overhead. The 15% threshold and the capacity check are "
    "guardrails that apply consistently across every make-versus-buy analysis Maria runs. Without "
    "them, each analysis would use different assumptions.",
    italic=True
)

doc.add_heading("14:30. Market report arrives, needs processing", level=3)

add_para(
    "A new Q2 2026 polymers market report arrives by email from the industry association. Maria "
    "saves it to market-intelligence/ and processes it immediately."
)

add_code_block(
    "Read market-intelligence/q2_2026_polymers_outlook.md.\n"
    "Extract market signals using the Market Signal Format\n"
    "from CLAUDE.md. Assign signal IDs starting after the\n"
    "highest existing ID in Drafts/market_signals.json.\n"
    "Append to Drafts/market_signals.json."
)

add_para(
    "Claude Code reads the report and extracts two signals: polymer resin prices forecast to rise "
    "8% through Q3 2026 (SIG-013, high confidence), and a supply constraint in Southeast Asia "
    "affecting pellet-form resin availability (SIG-014, medium confidence). Maria immediately "
    "connects this to the polymer resin consolidation: locking in pricing now on the 570-ton "
    "blanket order is even more urgent. She updates the consolidation recommendation. "
    "Total time: 6 minutes."
)

add_para(
    "What to learn from this. Market signals are not static. New reports arrive throughout the "
    "quarter. By appending to the existing signals file (instead of creating a new one), Maria "
    "keeps a running record that every downstream analysis can reference. The signal format in "
    "CLAUDE.md ensures consistency: every signal has an ID, a magnitude, a confidence level, and "
    "a recommended action.",
    italic=True
)

doc.add_heading("15:45. Preparing the weekly sourcing brief", level=3)

add_para(
    "Every Friday morning, Maria sends Karen a one-page sourcing brief summarizing the week's "
    "market intelligence, demand changes, and sourcing recommendations. She prepares it Thursday "
    "afternoon so she can review it fresh Friday morning."
)

add_code_block(
    "Read Drafts/market_signals.json, Drafts/commodity_tracker.json,\n"
    "Drafts/demand_specs.json, and Drafts/consolidation-update.md.\n"
    "Write a weekly sourcing brief to Drafts/weekly-brief-2026-04-26.md.\n"
    "Include: (1) commodity watch list (any commodity with YoY change\n"
    "above 10% or a new market signal this week), (2) demand summary\n"
    "(total open requirements, consolidation opportunities, missing\n"
    "fields count), (3) three recommendations, each citing a specific\n"
    "data point. Date: 2026-04-26. Addressee: Karen Webb."
)

add_para(
    "Claude Code reads all four data sources and produces the brief. The recommendations are: "
    "(1) lock in polymer resin pricing now because prices rose 11% year-over-year and the Q2 report "
    "forecasts a further 8% increase through Q3. (2) Issue the consolidated polymer resin blanket "
    "PO for 570 tons with Heartland Polymers at an estimated savings of $15,818. (3) Initiate a "
    "pilot of 500 precision bushings for in-house production while the CNC shop has 22% capacity "
    "available. Maria reviews, tweaks one sentence, and saves. Total time: 8 minutes."
)

add_para(
    "What to learn from this. The weekly brief is not written from scratch each week. It pulls "
    "from structured data files (signals, tracker, specs, consolidation) that Maria has been "
    "building all week. Each prompt adds to the data. The weekly brief prompt just reads and "
    "synthesizes what is already there. This pattern (accumulate structured data, then summarize) "
    "scales to any reporting cadence: weekly, monthly, or quarterly.",
    italic=True
)

doc.add_heading("16:30. End of day review", level=3)

add_para(
    "Maria checks her outputs folder. Today she produced: a board-ready market summary for the CPO "
    "(15 minutes), a structured requirement for cold-rolled steel (3 minutes), an updated "
    "consolidation report (5 minutes), a make-versus-buy analysis for precision bushings (12 minutes), "
    "two new market signals from the Q2 polymers report (6 minutes), and a draft weekly sourcing "
    "brief (8 minutes). Total productive time: 49 minutes. In a manual workflow, the same outputs "
    "would have taken roughly 8 hours."
)

add_para(
    "What to learn from this. Maria's day is not about running Claude Code. It is about making "
    "sourcing decisions. Claude Code handles the data processing, the calculations, and the first "
    "draft. Maria handles the judgment: adjusting recommendations based on supplier relationships "
    "she knows, flagging risks Claude cannot see (like the copper contract already locked in), "
    "and deciding what to send to whom. The tool does the work. The analyst makes the calls.",
    italic=True
)

# ============================================================================
# 8. 20-MINUTE SPRINT
# ============================================================================
doc.add_heading("20-Minute Sprint: Your First Market Intelligence Output", level=1)

add_para(
    "This section gets you from zero to a usable commodity tracker in twenty minutes. Follow the "
    "time blocks exactly. If a step takes longer than its block, skip the optional parts and move on."
)

doc.add_heading("Minutes 0 to 5: Open the project", level=2)
add_numbered("Open your terminal (Command Prompt, PowerShell, or Terminal on Mac).")
add_numbered("Navigate to the practice folder:")
add_code_block("cd Course_17_Market_Intelligence/practice")
add_numbered("Confirm the data file exists:")
add_code_block("ls commodity-prices.csv")
add_para("You should see the file listed. If not, check that you are in the right folder.")
add_numbered("Start Claude Code:")
add_code_block("claude")
add_para(
    "You should see the Claude Code prompt. It reads CLAUDE.md automatically and knows your role "
    "as Market Intelligence Analyst at Atlas Manufacturing."
)

doc.add_heading("Minutes 5 to 10: Build the commodity tracker", level=2)
add_numbered("Type this prompt:")
add_code_block(
    "Read commodity-prices.csv. For each of the 8 commodities, calculate:\n"
    "current price, price 12 months ago, year-over-year change (USD and %),\n"
    "trend direction (per CLAUDE.md rules), and volatility flag.\n"
    "Write to Drafts/commodity_dashboard.md as a summary table\n"
    "sorted by absolute YoY change descending."
)
add_para(
    "Wait for Claude Code to finish. You should see it create the Drafts/ folder (if needed) and "
    "write the dashboard file."
)

doc.add_heading("Minutes 10 to 15: Review and refine", level=2)
add_numbered("Review the output:")
add_code_block(
    "Read Drafts/commodity_dashboard.md. Does every commodity have\n"
    "a current price, a YoY change, and a trend direction?\n"
    "Are any fields missing or marked as unknown?"
)
add_para(
    "Fix any issues Claude Code flags. If a commodity is missing data, Claude will tell you which "
    "months are absent from the CSV."
)
add_numbered("Add a watch list:")
add_code_block(
    "Add a 'Watch List' section to Drafts/commodity_dashboard.md.\n"
    "Include any commodity with a YoY change exceeding 10% in either\n"
    "direction. For each, write one sentence explaining the trend."
)

doc.add_heading("Minutes 15 to 20: Read a market report and connect it", level=2)
add_numbered("Process one market report:")
add_code_block(
    "Read market-intelligence/steel_price_outlook.md.\n"
    "Extract market signals using the format in CLAUDE.md.\n"
    "Write to Drafts/market_signals.json."
)
add_numbered("Connect the signal to the tracker:")
add_code_block(
    "Read Drafts/commodity_dashboard.md and Drafts/market_signals.json.\n"
    "For any commodity on the watch list that has a matching signal,\n"
    "add a forward outlook sentence to the dashboard."
)
add_numbered("Exit Claude Code:")
add_code_block("/quit")

add_para(
    "You now have a commodity dashboard with trend analysis and forward-looking market intelligence. "
    "This is a usable output you can share with your sourcing team today."
)

# ============================================================================
# 9. FIRST WEEK DAY-BY-DAY PLANNER
# ============================================================================
doc.add_heading("First Week Day-by-Day Planner", level=1)

add_para(
    "Five days to build market intelligence fluency. Each day adds one capability."
)

doc.add_heading("Day 1: Install, set up, and first commodity read (Monday)", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Install Claude Code and confirm it runs.")
add_bullet("Open the Course 17 practice folder and verify all files are present.")
add_bullet("Run one prompt that reads commodity-prices.csv and shows the column names, row count, and commodity list.")
add_bullet("Confirm that CLAUDE.md is being read by asking Claude Code: \"What is my role at Atlas Manufacturing?\"")

add_para(
    "By end of day, you know that Claude Code reads your files and follows the rules in CLAUDE.md. "
    "You have not built anything yet. That is fine. Day 1 is about trust: confirming the tool works "
    "as described."
)

doc.add_heading("Day 2: Build the commodity tracker (Tuesday)", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Run the 20-Minute Sprint from this handout.")
add_bullet("Build a full commodity dashboard for all 8 commodities with current price, YoY change, trend direction, and volatility flag.")
add_bullet("Process one market report and extract signals.")
add_bullet("Add forward-looking commentary to the dashboard for at least one commodity.")

add_para(
    "By end of day, you have a reusable commodity dashboard. This is the output you will refresh "
    "monthly. Save the exact prompt you used so you can re-run it next month with updated data."
)

doc.add_heading("Day 3: Process stakeholder requirements (Wednesday)", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Work through Lesson 3 (Requirements Processing).")
add_bullet("Read all 6 files in demand-intake/ and structure them into demand_specs.json.")
add_bullet("Identify which requirements are complete and which have missing fields.")
add_bullet("Draft follow-up messages for the incomplete requirements.")

add_para(
    "By end of day, you have a structured demand register and follow-up messages ready to send. "
    "Every future requirement that arrives goes through the same process: save to demand-intake/, "
    "run the extraction prompt, append to the specs file."
)

doc.add_heading("Day 4: Consolidate demand and run a make-versus-buy (Thursday)", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Work through Lesson 4 (Demand Consolidation). Identify the polymer resin overlap and calculate the $15,818 savings opportunity.")
add_bullet("Work through Lesson 5 (Make vs. Buy). Build a full cost model for precision bushings and compare buy ($15.89/unit) versus make ($13.42/unit).")
add_bullet("Save both reports to Drafts/.")

add_para(
    "By end of day, you have demonstrated two high-value capabilities: finding money left on the "
    "table through volume consolidation, and preventing bad make-versus-buy decisions by including "
    "all costs. Both outputs are ready for your category manager."
)

doc.add_heading("Day 5: Connect everything into a sourcing brief (Friday)", level=2)
add_para("Goals for today:", bold=True)
add_bullet("Work through Lesson 6 (Sourcing Brief). Adjust RFP evaluation weights based on market signals.")
add_bullet("Write a weekly sourcing brief pulling from all data files built during the week.")
add_bullet("Review all outputs in Drafts/. Move the best ones to Outputs/.")
add_bullet("Plan next week: identify which real commodity or category you will apply this workflow to first.")

add_para(
    "By end of day, you have a complete market intelligence workflow: ingest reports, track prices, "
    "process requirements, consolidate demand, analyze make-versus-buy, and produce sourcing briefs. "
    "Next week, apply it to your actual categories."
)

# ============================================================================
# 10. THE PATTERN
# ============================================================================
doc.add_heading("The Pattern: How to Apply This to Any Category", level=1)

add_para(
    "Course 17 uses Atlas Manufacturing and 8 commodities. Your organization tracks different "
    "commodities with different rules. Here is the pattern for adapting the workflow to any category."
)

doc.add_heading("Step 1: Set up your project folder", level=2)
add_code_block(
    "market-intelligence-<your-org>/\n"
    "  CLAUDE.md               (your role, your commodities, your rules)\n"
    "  data/\n"
    "    commodity-prices.csv   (your price history)\n"
    "    supplier-capabilities.csv  (your supplier list)\n"
    "    demand-intake/         (stakeholder requirement files)\n"
    "    market-intelligence/   (market reports, PDFs, analyst notes)\n"
    "  Drafts/                  (working files)\n"
    "  Outputs/                 (final reports)"
)

doc.add_heading("Step 2: Customize CLAUDE.md", level=2)
add_para(
    "Copy the CLAUDE.md from the Course 17 practice folder and edit these sections:"
)
add_bullet("Role: ", bold_prefix="Role: ")
add_para("Replace Atlas Manufacturing with your company name, your title, your Director's name, and your annual spend figure.")
add_bullet("Category definitions: ", bold_prefix="Category definitions: ")
add_para("List your commodities, their units, and their annual spend.")
add_bullet("Commodity tracking rules: ", bold_prefix="Tracking rules: ")
add_para("Adjust the moving average window, the volatility threshold, and the YoY comparison period if your organization uses different standards.")
add_bullet("Consolidation rules: ", bold_prefix="Consolidation rules: ")
add_para("Adjust the volume discount formula and the timeline conflict window if your purchasing terms differ.")
add_bullet("Make-versus-buy rules: ", bold_prefix="Make-vs-buy rules: ")
add_para("Adjust the cost threshold (15% in the course), the capacity floor (20%), and the opportunity cost estimate for your production environment.")

doc.add_heading("Step 3: Load your data", level=2)
add_para(
    "Export your commodity price history from your ERP or market data subscription. The CSV needs "
    "at minimum: commodity name, date, price, and unit. More columns are fine. Claude Code (in the "
    "terminal) adapts to whatever columns your export contains."
)
add_para(
    "Save stakeholder requirements to demand-intake/ as they arrive. Any format works: emails saved "
    "as .txt, forms saved as .md or .docx, even voicemail transcripts. Claude Code reads all of them."
)
add_para(
    "Save market reports to market-intelligence/. PDFs, Word documents, and text files all work. "
    "Claude Code reads PDFs directly."
)

doc.add_heading("Step 4: Run the workflow", level=2)
add_para("The workflow is the same regardless of your commodities:")
add_numbered("Process market reports into structured signals (Lesson 1 pattern).")
add_numbered("Build commodity trackers from price history (Lesson 2 pattern).")
add_numbered("Structure stakeholder requirements (Lesson 3 pattern).")
add_numbered("Consolidate overlapping demand (Lesson 4 pattern).")
add_numbered("Run make-versus-buy on high-value items (Lesson 5 pattern).")
add_numbered("Produce market-linked sourcing briefs (Lesson 6 pattern).")

add_para(
    "Each step produces a structured data file. Each subsequent step reads the files from earlier "
    "steps. The workflow is cumulative: the sourcing brief in step 6 cites signals from step 1, "
    "prices from step 2, and demand from steps 3 and 4."
)

doc.add_heading("The personalization pattern for Claude Code", level=2)

add_para(
    "In Claude Code (in the terminal), project-level context lives in one CLAUDE.md at the project "
    "root. For market intelligence, keep one CLAUDE.md with all your rules, category definitions, "
    "and output standards. If you manage multiple categories with different rules, add a sub-folder "
    "CLAUDE.md for each category. Example:"
)

add_code_block(
    "market-intelligence-2026/\n"
    "  CLAUDE.md                    (global rules: output format, date format, currency)\n"
    "  raw-materials/\n"
    "    CLAUDE.md                  (rules specific to steel, polymers, aluminum)\n"
    "  IT-services/\n"
    "    CLAUDE.md                  (rules specific to cloud hosting, software, support)"
)

add_para(
    "Why this matters. A single CLAUDE.md that covers all categories becomes long and hard to "
    "maintain. Splitting context by category keeps each file focused. When you start Claude Code "
    "inside the raw-materials/ folder, it reads both the root CLAUDE.md (global rules) and the "
    "sub-folder CLAUDE.md (category-specific rules). This is the CLAUDE.md stacking behavior that "
    "Claude Code supports natively.",
    italic=True
)

# ============================================================================
# 11. CAUTIONS AND TROUBLESHOOTING
# ============================================================================
doc.add_heading("Cautions, Ground Rules, and Troubleshooting", level=1)

doc.add_heading("Cautions and ground rules", level=2)

add_bullet(
    "Claude Code (in the terminal) reads local files. It does not access the internet, live "
    "commodity feeds, or your ERP. Your commodity-prices.csv must be exported and saved locally "
    "before Claude Code can analyze it."
)
add_bullet(
    "Market signals extracted by Claude Code are only as good as the reports you feed it. If "
    "a report is vague (\"prices are expected to increase\"), the signal will be vague. Feed "
    "Claude Code reports with specific numbers, and the signals will have specific numbers."
)
add_bullet(
    "Volume discount estimates use the 3% per doubling rule from CLAUDE.md. Your actual discount "
    "tiers may differ. Treat Claude Code's estimates as directional, not contractual. Confirm "
    "with your supplier before committing."
)
add_bullet(
    "Make-versus-buy analyses depend on cost assumptions you provide. If your labor rate is $45/hour "
    "instead of $32/hour, update the prompt. Claude Code uses the numbers you give it."
)
add_bullet(
    "Always review Claude Code's output before sending it to stakeholders. Claude Code is fast "
    "and consistent, but it does not know about supplier relationships, internal politics, or "
    "verbal commitments that are not in the data files."
)

doc.add_heading("Troubleshooting", level=2)

add_table(
    ["Symptom", "Cause", "Fix"],
    [
        [
            "Claude Code says \"I cannot find commodity-prices.csv\"",
            "You started Claude Code in the wrong folder, or the file name has a typo.",
            "Exit Claude Code. Run 'ls' to check the folder contents. Navigate to the practice/ folder and restart."
        ],
        [
            "Year-over-year change shows as 0% for every commodity",
            "The date column format does not match what Claude Code expected, or the data covers less than 12 months.",
            "Ask Claude Code: \"Show me the five most recent dates in commodity-prices.csv for hot-rolled steel. What format are they in?\" Then adjust the prompt to match."
        ],
        [
            "Market signals have no specific magnitude (just says 'increase expected')",
            "The source market report did not include specific numbers.",
            "Add to your prompt: \"If the report gives a percentage or dollar figure, use it. If it gives a range, use the range. If no number is available, write [TBC: figure] and set confidence to low.\""
        ],
        [
            "Demand consolidation groups unrelated items together (steel gaskets grouped with steel brackets)",
            "Claude Code matched on the material adjective (steel) instead of the item noun (gasket vs. bracket).",
            "Add to your prompt: \"Group only by the primary item noun (gasket, bracket, fitting), not by material or adjective.\""
        ],
        [
            "Make-versus-buy recommends 'make' but the make cost looks too low",
            "Tooling amortization or opportunity cost was not included.",
            "Check the make-side cost model. Confirm it includes tooling ($28,000 amortized over volume), opportunity cost ($2.00/unit), and quality cost ($0.40/unit). If any are missing, re-run with explicit values."
        ],
        [
            "RFP evaluation weights do not sum to 100% after adjustment",
            "Rounding error from multiple percentage adjustments.",
            "Ask Claude Code: \"Adjust the final criterion by the rounding difference so all four weights sum to exactly 100.0%.\""
        ],
    ],
    col_widths=[2.2, 2.0, 2.8]
)

# ============================================================================
# 12. DONE CHECKLIST
# ============================================================================
doc.add_heading("Done Checklist", level=1)

add_para(
    "Run this checklist before treating any output as final. Each item is marked done, deferred, or N/A."
)

checklist_items = [
    ("1.", "The S2P problem is named in the first paragraph or opening section.", "Done"),
    ("2.", "The outcome is stated in business terms before any command appears.", "Done"),
    ("3.", "Every S2P task has a worked example with four parts: prompt (code block), folder layout (code block), what you should see, and behind-the-scenes walkthrough.", "Done"),
    ("4.", "Every capability statement names the specific Claude: Claude Code (in the terminal), Claude AI Web, or Claude Desktop with Cowork.", "Done"),
    ("5.", "For lessons, every step has: what you do, what you type, and what you see.", "N/A (handout, not lesson)"),
    ("6.", "At least one full worked example with realistic fake data.", "Done (three worked examples)"),
    ("7.", "Troubleshooting section with symptom and fix entries.", "Done (six entries)"),
    ("8.", "No em-dashes or en-dashes anywhere.", "Done"),
    ("9.", "No banned phrases from the general or procurement-specific lists.", "Done"),
    ("10.", "Oxford commas applied everywhere.", "Done"),
    ("11.", "No rhetorical questions as openers.", "Done"),
    ("12.", "Risk and issue text in active voice with the actor named.", "Done"),
    ("13.", "Every figure is a real number, not 'significant' or 'material.'", "Done"),
    ("14.", "Sample executive summaries name a supplier, a value, and a date.", "Done (Heartland Polymers, $15,818, 2026-04-26)"),
    ("15.", "Recommendation lists have three items or fewer.", "Done"),
    ("16.", "File name matches the naming convention.", "Done"),
    ("17.", "Screenshots are cropped, captioned, and use fake data.", "N/A (no screenshots in this handout)"),
    ("18.", "Standard folder layout referenced (Master/, Drafts/, Outputs/).", "Done"),
    ("19.", "A procurement analyst with no coding background can read and act on this.", "Done"),
    ("20.", "Comprehensive guide: Time savings table, Day-in-the-Life, 20-Minute Sprint, First Week Planner, personalization pattern.", "Done (all five present)"),
    ("21.", "Course-specific checks (self-contained folder, data volumes, scenarios).", "N/A (handout, not course folder)"),
    ("22.", "Style check reports zero violations.", "Deferred (run after save)"),
    ("23.", "Every concept, folder, or file explanation has a 'Why this matters' paragraph.", "Done"),
    ("24.", "Every Day-in-the-Life scenario has a 'What to learn from this' paragraph.", "Done (all seven scenarios)"),
]

add_table(
    ["#", "Check", "Status"],
    [[item[0], item[1], item[2]] for item in checklist_items],
    col_widths=[0.4, 4.8, 1.8]
)

# ============================================================================
# SAVE
# ============================================================================
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(OUTPUT))
print(f"Saved: {OUTPUT}")
print(f"Sections: 13")
