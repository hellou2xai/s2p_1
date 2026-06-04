"""Build Course 09: The Integration Architect Handout (.docx)."""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import os

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)

# Configure heading styles
for level, size, color in [
    ('Heading 1', 16, RGBColor(0x1B, 0x3A, 0x5C)),
    ('Heading 2', 14, RGBColor(0x1B, 0x3A, 0x5C)),
    ('Heading 3', 12, RGBColor(0x2E, 0x4A, 0x6E)),
]:
    h = doc.styles[level]
    h.font.name = 'Calibri'
    h.font.size = Pt(size)
    h.font.color.rgb = color
    h.font.bold = True

title_style = doc.styles['Title']
title_style.font.name = 'Calibri'
title_style.font.size = Pt(26)
title_style.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)


def add_code_block(text):
    """Add a code block with Consolas font and light gray background."""
    p = doc.add_paragraph()
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F2F2F2" w:val="clear"/>')
    p._element.get_or_add_pPr().append(shading)
    pf = p.paragraph_format
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    pf.left_indent = Inches(0.25)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return p


def add_table(headers, rows):
    """Add a formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.style = 'Table Grid'
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1B3A5C" w:val="clear"/>')
        cell._element.get_or_add_tcPr().append(shading)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    # Data rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.name = 'Calibri'
            run.font.size = Pt(10)
            if r_idx % 2 == 1:
                shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F7FA" w:val="clear"/>')
                cell._element.get_or_add_tcPr().append(shading)
    doc.add_paragraph()  # spacing after table
    return table


def add_bold_para(bold_text, normal_text=""):
    """Add paragraph with bold prefix."""
    p = doc.add_paragraph()
    run = p.add_run(bold_text)
    run.bold = True
    if normal_text:
        p.add_run(" " + normal_text)
    return p


def add_normal(text):
    return doc.add_paragraph(text)


def add_why_matters(text):
    """Add a 'Why this matters' paragraph."""
    p = doc.add_paragraph()
    run = p.add_run("Why this matters. ")
    run.bold = True
    run.font.size = Pt(11)
    p.add_run(text)
    return p


def add_what_to_learn(text):
    """Add a 'What to learn from this' paragraph."""
    p = doc.add_paragraph()
    run = p.add_run("What to learn from this. ")
    run.bold = True
    run.font.size = Pt(11)
    p.add_run(text)
    return p


# ============================================================
# HEADER
# ============================================================
p = doc.add_paragraph()
run = p.add_run("U2xAI")
run.font.size = Pt(12)
run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)

p = doc.add_paragraph()
run = p.add_run("PROCUREAI ACADEMY")
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)

add_normal("Series 2 (Engineering Track) | Course 9")

doc.add_paragraph("The Integration Architect", style='Title')

p = doc.add_paragraph()
run = p.add_run(
    "MCP servers that connect Claude Code to procurement databases for live data queries."
)
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

add_normal(
    "Six lessons. About five hours. No coding experience required. "
    "Use this handout alongside the course folder at "
    "Detailed Course Content/Course_09_The_Integration_Architect/."
)

# ============================================================
# 1. HOW TO USE THIS HANDOUT
# ============================================================
doc.add_heading("1. How to use this handout", level=1)

add_normal(
    "This handout is your reading companion. The hands-on work happens "
    "in the course folder you received with the training materials."
)

add_normal("How to read this guide:")

guide_steps = [
    "Read sections 2 and 3 to understand what the course teaches and what is in the course folder.",
    "Read section 4 for the time savings table, so you know the payoff before you start.",
    "Read section 5 for the mental model of what an MCP server is and how it works.",
    "Open the course folder and start Lesson 1.",
    "Come back to this handout when you want context. Sections 6 and 7 (worked examples, Day in the Life) are useful during and after the course.",
    "Use section 11 (troubleshooting) if something does not look right.",
]
for i, step in enumerate(guide_steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(step)

# ============================================================
# 2. WHAT THIS COURSE TEACHES
# ============================================================
doc.add_heading("2. What this course teaches", level=1)

doc.add_heading("The stale data problem", level=2)

add_normal(
    "It is Tuesday morning. Your VP of Procurement asks: "
    '"What is our open PO exposure with Apex Electronics? '
    'They just missed a delivery." '
    "You open the spend report you exported last Friday. "
    "You find three open POs totaling $184,000. "
    "But that was Friday. Since then, AP approved two more requisitions. "
    "The real number is $247,000, and you do not know it."
)

add_normal(
    "You email the AP team. They reply four hours later with a CSV. "
    "By then, the VP has already made a decision based on stale data. "
    "This happens every week. The data sits in databases, ERP tables, "
    "and procurement platforms. Claude Code (in the terminal) cannot reach it. "
    "You export CSVs, drop them in folders, and hope they are current. "
    "They never are."
)

doc.add_heading("What MCP changes", level=2)

add_normal(
    "The Model Context Protocol (MCP) is an open standard that lets "
    "Claude Code (in the terminal) discover and call external tools at runtime. "
    "Instead of reading a stale CSV, Claude Code sends a structured request "
    "to an MCP server. The server queries the database and returns the result. "
    "Claude Code receives live data, not a last-week export."
)

add_normal(
    "In this course, you build a FastMCP server in Python that exposes "
    "three procurement tools: get_supplier_spend (query spend by supplier, "
    "category, or date range), get_open_pos (return open purchase orders "
    "filtered by supplier or status), and get_contract_status (check contract "
    "terms, expiry dates, and auto-renewal flags). When you finish, you type "
    'a question like "Show me all overdue POs for raw materials suppliers" '
    "and Claude Code (in the terminal) calls your MCP server, runs the SQL "
    "query, and returns the answer. No CSV. No export. Live data."
)

doc.add_heading("What you end up with", level=2)

items = [
    "A running MCP server registered in .claude/settings.json with three procurement tools.",
    'You type "What is our total spend with Great Lakes Steel?" and Claude Code (in the terminal) calls get_supplier_spend, queries procurement.db, and returns the answer.',
    'You type "Show me all overdue POs" and Claude Code (in the terminal) calls get_open_pos with a status filter and returns a table.',
    'You type "Which contracts expire in the next 90 days?" and Claude Code (in the terminal) calls get_contract_status and returns the list.',
    "Your server enforces read-only access. No INSERT, UPDATE, or DELETE queries are possible.",
    "You combine an MCP tool call with a skill to produce a formatted spend variance report from live data.",
]
for i, item in enumerate(items, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(item)

doc.add_heading("Lesson sequence", level=2)

lessons = [
    "Lesson 1: MCP protocol basics (what it is, how it works, why procurement teams need it)",
    "Lesson 2: Connecting to an existing MCP server (registering in settings.json)",
    "Lesson 3: Anatomy of an MCP server (FastMCP, tools, and type hints)",
    "Lesson 4: Building the procurement data MCP server (three tools against procurement.db)",
    "Lesson 5: Security patterns (read-only access, input validation, and error handling)",
    "Lesson 6: Combining MCP with skill-driven analysis (live data meets reusable prompts)",
]
for lesson in lessons:
    doc.add_paragraph(lesson, style='List Bullet')

add_normal("To start the course, open a terminal and navigate to the practice folder:")

add_code_block(
    'cd "Course_09_The_Integration_Architect/practice"\nclaude'
)

add_normal(
    "Claude Code (in the terminal) loads the CLAUDE.md file automatically. "
    "You are ready for Lesson 1."
)

# ============================================================
# 3. WHAT IS IN THE COURSE FOLDER
# ============================================================
doc.add_heading("3. What is in the course folder", level=1)

add_code_block(
    "Course_09_The_Integration_Architect/\n"
    "+-- README.md\n"
    "+-- COURSE_OVERVIEW.md\n"
    "+-- lessons/\n"
    "|   +-- Lesson_01_The_MCP_Protocol.md\n"
    "|   +-- Lesson_02_Connecting_To_An_MCP_Server.md\n"
    "|   +-- Lesson_03_Anatomy_Of_An_MCP_Server.md\n"
    "|   +-- Lesson_04_Building_The_Procurement_MCP.md\n"
    "|   +-- Lesson_05_Security_Patterns.md\n"
    "|   +-- Lesson_06_MCP_Plus_Skills.md\n"
    "+-- practice/\n"
    "|   +-- CLAUDE.md\n"
    "|   +-- data/\n"
    "|   |   +-- procurement.db\n"
    "|   |   +-- supplier-master.csv\n"
    "|   +-- mcp-server/\n"
    "|   |   +-- procurement_server.py    (you build this)\n"
    "|   +-- outputs/\n"
    "+-- solutions/\n"
    "|   +-- mcp_server_solution.py\n"
    "|   +-- settings_json_solution.md\n"
    "+-- scripts/\n"
    "    +-- build_course_data.py"
)

doc.add_heading("README.md", level=3)
add_normal(
    "Navigation page. Lists what is in the folder, how to start, and what order to follow."
)
add_why_matters(
    "Without this file, you spend five minutes clicking around subfolders "
    "before you can begin. With it, you open the folder and know exactly "
    "where to go."
)

doc.add_heading("COURSE_OVERVIEW.md", level=3)
add_normal(
    "The day-to-day scenario (the stale data problem at Nexus Procurement Hub), "
    "the practice data schema, and what 'done' looks like."
)
add_why_matters(
    "This file sets the stakes. You are not doing exercises for the sake of learning. "
    "You are solving a real procurement problem: your VP needs current data and "
    "you cannot deliver it fast enough with CSV exports."
)

doc.add_heading("lessons/", level=3)
add_normal(
    "Six markdown lessons, numbered in order. Each follows the standard "
    "six-part structure: problem, outcome, setup, step-by-step, worked example, "
    "and troubleshooting."
)
add_why_matters(
    "The lessons are the course. Every other file supports them. "
    "If you skip a lesson, the next one assumes knowledge you do not have."
)

doc.add_heading("practice/CLAUDE.md", level=3)
add_normal(
    "The project context file. Describes your role (Procurement Analyst at "
    "Nexus Procurement Hub), the data files, the MCP tools, the five categories, "
    "and the output standards. Claude Code (in the terminal) reads this file "
    "automatically when you start a session in the practice/ folder."
)
add_why_matters(
    "Without CLAUDE.md, Claude Code gives generic answers. With it, every response "
    "uses Nexus's categories, Nexus's supplier names, and Nexus's formatting rules. "
    "The quality difference is immediate."
)

doc.add_heading("practice/data/", level=3)
add_normal(
    "Contains two files. procurement.db is a SQLite database with four tables: "
    "suppliers (20 rows), spend (about 700 rows), contracts (20 rows), and "
    "open_pos (50 rows). supplier-master.csv is a CSV export of the suppliers "
    "table, pulled last week and already out of date."
)
add_why_matters(
    "The database is the live source. The CSV is the stale export. "
    "The gap between them is the whole point of the course. "
    "By the end, you stop using the CSV and query the database directly through MCP."
)

doc.add_heading("practice/mcp-server/", level=3)
add_normal(
    "This starts empty. You build procurement_server.py here during Lesson 4. "
    "The solution version is in solutions/."
)
add_why_matters(
    "Building the server yourself is how you learn what an MCP tool is, "
    "how inputs map to SQL queries, and how to modify a tool when requirements change."
)

doc.add_heading("solutions/", level=3)
add_normal(
    "Reference answers: the complete MCP server script and the settings.json "
    "registration. Look at these only after attempting the lessons."
)
add_why_matters(
    "Seeing the answer before the attempt trains recognition, not skill. "
    "Attempt first. Compare after."
)

doc.add_heading("scripts/build_course_data.py", level=3)
add_normal(
    "Regenerates the SQLite database and CSV with deterministic data "
    "(random.seed(42)). Run this if you corrupt the practice data."
)
add_why_matters(
    "One command restores everything. You never need to re-download "
    "the course folder because of a data mistake."
)

# ============================================================
# 4. TIME SAVINGS TABLE
# ============================================================
doc.add_heading("4. What MCP saves you per week", level=1)

add_normal(
    "These numbers are based on a procurement analyst answering five to ten "
    "ad hoc data questions per week, managing 20 suppliers across five categories, "
    "and producing one weekly spend report."
)

add_table(
    ["Task", "Without MCP (manual export)", "With MCP (live query)"],
    [
        [
            "Answer a VP question about a specific supplier's spend",
            "10 to 15 minutes: log into ERP, run the report, export CSV, open in Excel, filter, answer",
            "30 seconds: type the question, Claude Code calls get_supplier_spend, answer appears",
        ],
        [
            "Check for overdue POs across all suppliers",
            "20 to 30 minutes: export open PO report, filter by delivery date, flag overdue rows, format table",
            '45 seconds: type "Show me all overdue POs," Claude Code calls get_open_pos with status filter',
        ],
        [
            "Verify contract status before a supplier meeting",
            "8 to 12 minutes: open contract management system, search by supplier, check dates manually",
            '20 seconds: type "What is the contract status for Globex SA?" and read the answer',
        ],
        [
            "Produce weekly spend variance report (Q/Q)",
            "40 to 60 minutes: two ERP exports, build pivot tables, calculate variances, write narrative",
            "2 minutes: type one prompt, MCP fetches both quarters, skill produces table and narrative",
        ],
        [
            "Respond to a CFO question about total category spend",
            "15 to 20 minutes: export category-level report, filter, sum, cross-check",
            "30 seconds: type the question with the category name, get the total with transaction count",
        ],
    ],
)

add_normal(
    "Total weekly savings: roughly 2 to 3 hours. Over 48 working weeks, "
    "that is 96 to 144 hours per analyst per year. For a four-person "
    "procurement team, that is 384 to 576 hours redirected from data "
    "retrieval to analysis, negotiation, and supplier management."
)

# ============================================================
# 5. WHAT AN MCP SERVER IS
# ============================================================
doc.add_heading("5. What an MCP server is", level=1)

doc.add_heading("The mental model", level=2)

add_normal(
    "Think of MCP as a translator. Claude Code (in the terminal) speaks "
    "one language. Your database speaks another. The MCP server sits between "
    "them and handles the translation. Claude Code does not connect to SQLite "
    "directly. It sends a structured request to the MCP server. The server "
    "runs the query, formats the result, and sends it back."
)

add_normal(
    "The protocol has two main concepts: tools and resources. "
    "A tool is an action Claude Code (in the terminal) can call, like "
    '"get_supplier_spend." It has a name, a description, and an input schema '
    "(what parameters it accepts). A resource is a piece of data Claude Code "
    "can read, like a configuration file or a lookup table. In this course, "
    "you work with tools. Resources are useful for static context (company "
    "policies, category definitions) but the core workflow is tool-based."
)

doc.add_heading("How a tool call works, step by step", level=2)

steps = [
    'You type a question: "What is our spend with Great Lakes Steel this quarter?"',
    "Claude Code (in the terminal) reads the list of available MCP tools and their descriptions.",
    'It matches your question to get_supplier_spend because the description says "Query spend transactions from the procurement database."',
    'It builds a structured request with the parameters: supplier_id = "SUP003", start_date = "2026-01-01", end_date = "2026-03-31".',
    "The MCP server receives the request, runs the SQL query against procurement.db, and returns a JSON string with the results.",
    "Claude Code reads the JSON and formats a human-readable answer in your terminal.",
]
for i, s in enumerate(steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(s)

doc.add_heading("Tools versus resources", level=2)

add_table(
    ["Concept", "What it does", "Procurement example"],
    [
        [
            "Tool",
            "An action Claude Code can call. Takes inputs, returns a result.",
            "get_supplier_spend: takes a supplier ID and date range, returns spend total",
        ],
        [
            "Resource",
            "A piece of static data Claude Code can read. No inputs needed.",
            "A company policy document or a list of approved payment terms",
        ],
    ],
)

add_why_matters(
    "Understanding the difference prevents you from building tools when a "
    "resource would be simpler (static lookup tables), or using resources "
    "when you need a filtered query (spend by date range). Most procurement "
    "integrations use tools because the data changes daily."
)

doc.add_heading("The tool schema", level=2)

add_normal(
    "Every MCP tool has a schema that tells Claude Code (in the terminal) "
    "three things: what the tool is called, what it does, and what inputs "
    "it expects. Here is the schema for get_supplier_spend:"
)

add_code_block(
    '{\n'
    '  "name": "get_supplier_spend",\n'
    '  "description": "Query spend transactions from the procurement database.",\n'
    '  "inputSchema": {\n'
    '    "type": "object",\n'
    '    "properties": {\n'
    '      "supplier_id": {"type": "string", "description": "Filter by supplier ID."},\n'
    '      "category": {"type": "string", "description": "Filter by category."},\n'
    '      "start_date": {"type": "string", "description": "YYYY-MM-DD."},\n'
    '      "end_date": {"type": "string", "description": "YYYY-MM-DD."}\n'
    '    },\n'
    '    "required": []\n'
    '  }\n'
    '}'
)

add_normal(
    "Claude Code (in the terminal) reads this schema at startup. "
    "When your question mentions spend and a supplier name, Claude matches "
    "it to this tool. If the schema description is vague (\"Returns data\"), "
    "Claude may pick the wrong tool. Clear, specific descriptions are not optional."
)

add_why_matters(
    "The schema is the contract between Claude Code and your MCP server. "
    "If the schema says supplier_id is required but the function treats it "
    "as optional, Claude Code will always pass a supplier_id even when your "
    "question is about all suppliers. Mismatched schemas cause wrong answers."
)

doc.add_heading("How FastMCP builds schemas from Python functions", level=2)

add_normal(
    "FastMCP is a Python library that turns plain Python functions into MCP tools. "
    "You write a function with type hints and a docstring. FastMCP reads those hints "
    "and generates the JSON schema automatically. Here is the pattern:"
)

add_code_block(
    "@mcp.tool()\n"
    "def get_supplier_spend(\n"
    '    supplier_id: str = None,\n'
    '    category: str = None,\n'
    '    start_date: str = None,\n'
    '    end_date: str = None,\n'
    ") -> str:\n"
    '    """Query spend transactions from the procurement database."""\n'
    "    # ... SQL query ...\n"
    "    return json.dumps(result)"
)

add_normal(
    "The @mcp.tool() decorator registers the function. The function name becomes "
    "the tool name. Parameters with no default (like supplier_id: str) are required. "
    "Parameters with a default (like supplier_id: str = None) are optional. "
    "The docstring becomes the tool description. The return type is always a string."
)

add_why_matters(
    "You do not write JSON schemas by hand. FastMCP generates them from your code. "
    "This means your tool schema stays in sync with your function signature. "
    "If you add a parameter, the schema updates automatically the next time "
    "Claude Code connects."
)

# ============================================================
# 6. WORKED EXAMPLES
# ============================================================
doc.add_heading("6. Worked examples", level=1)

doc.add_heading("Example A: querying supplier spend through MCP", level=2)

add_normal(
    "You are a category manager at Nexus Procurement Hub. Your VP asks: "
    '"How much did we spend with Great Lakes Steel last quarter?" '
    "Your MCP server is running and registered in .claude/settings.json."
)

add_bold_para("The prompt you type in Claude Code (in the terminal):")
add_code_block(
    "What is our total spend with Great Lakes Steel in Q4 2025?\n"
    "Break it down by month."
)

add_bold_para("Folder layout:")
add_code_block(
    "practice/\n"
    "+-- CLAUDE.md\n"
    "+-- data/\n"
    "|   +-- procurement.db        (live database, queried via MCP)\n"
    "|   +-- supplier-master.csv   (stale CSV, not used)\n"
    "+-- mcp-server/\n"
    "|   +-- procurement_server.py (MCP server with 3 tools)\n"
    "+-- .claude/\n"
    "    +-- settings.json         (server registered here)"
)

add_bold_para("What you should see.")
add_normal(
    "Claude Code returns a table with three rows (October 2025, November 2025, "
    "December 2025), each showing the monthly spend amount and transaction count. "
    'The total line reads: "Total Q4 2025 spend with Great Lakes Steel: '
    '$487,200 across 18 transactions."'
)

add_bold_para("What Claude Code did, behind the scenes.")
steps = [
    "Claude Code read the list of MCP tools at session start and found get_supplier_spend, get_open_pos, and get_contract_status.",
    'Your prompt mentioned "spend" and "Great Lakes Steel," so Claude matched it to get_supplier_spend.',
    'Claude called get_supplier_spend with supplier_id = "SUP003", start_date = "2025-10-01", end_date = "2025-12-31".',
    "The MCP server connected to procurement.db, ran a SELECT query against the spend table filtered by supplier_id and date range, and returned a JSON string with 18 transaction rows and a total.",
    "Claude parsed the JSON, grouped transactions by month, and formatted the result as a table with a total line.",
    "The entire process took about 3 seconds. The manual version (ERP export, Excel pivot, email reply) would have taken 12 to 15 minutes.",
]
for i, s in enumerate(steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(s)

doc.add_heading(
    "Example B: combining MCP with a skill for a spend variance report", level=2
)

add_normal(
    "It is Friday at 15:30. You produce a weekly spend variance report for the VP. "
    "Before MCP and skills, this took 40 to 60 minutes: two ERP exports, a pivot table, "
    "and a written narrative. Now you have a spend-variance-analysis skill and a "
    "variance-narrative skill saved in .claude/skills/."
)

add_bold_para("The prompt you type in Claude Code (in the terminal):")
add_code_block(
    "Run a spend variance analysis for Q1 2026 versus Q4 2025.\n"
    "Include the executive narrative.\n"
    "Save to Drafts/spend_variance_Q1_2026.md."
)

add_bold_para("Folder layout:")
add_code_block(
    "practice/\n"
    "+-- CLAUDE.md\n"
    "+-- data/\n"
    "|   +-- procurement.db\n"
    "|   +-- supplier-master.csv\n"
    "+-- Drafts/\n"
    "|   +-- spend_variance_Q1_2026.md    (output goes here)\n"
    "+-- .claude/\n"
    "|   +-- settings.json\n"
    "|   +-- skills/\n"
    "|       +-- spend-variance-analysis.md\n"
    "|       +-- variance-narrative.md\n"
    "+-- mcp-server/\n"
    "    +-- procurement_server.py"
)

add_bold_para("What you should see.")
add_normal(
    "A file at Drafts/spend_variance_Q1_2026.md with two parts. First, a markdown "
    "table with 20 supplier rows showing Prior Quarter spend, Current Quarter spend, "
    'Dollar Change, Percent Change, and a Flag column ("YES" for any change over 10%). '
    "Second, a three-sentence executive narrative: "
    '"Apex Electronics saw the largest spend increase at $42,300 (14.2%). '
    "Northwind Logistics had the largest decrease at $28,100 (9.8%). "
    'Five of twenty suppliers are flagged for changes exceeding 10%."'
)

add_bold_para("What Claude Code did, behind the scenes.")
steps = [
    "Claude Code loaded the two skill files (.claude/skills/spend-variance-analysis.md and variance-narrative.md) at session start.",
    "Your prompt triggered the spend-variance-analysis skill, which instructs Claude to pull current and prior quarter spend for every supplier.",
    "Claude read supplier-master.csv to get the list of 20 supplier IDs.",
    "It called get_supplier_spend 40 times (20 suppliers, 2 quarters each), collecting spend totals from procurement.db for each combination.",
    "It calculated dollar and percentage changes, flagged any supplier with an absolute change over 10%, and sorted by absolute dollar change descending.",
    "It then triggered the variance-narrative skill, which told Claude to write exactly three sentences: the largest increase (named supplier, dollar figure, percentage), the largest decrease, and the total flagged count.",
    "Claude saved the combined table and narrative to Drafts/spend_variance_Q1_2026.md.",
]
for i, s in enumerate(steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(s)

doc.add_heading(
    "Example C: running a security audit on the MCP server", level=2
)

add_normal(
    "Your manager wants to confirm the MCP server is safe to deploy to the team. "
    "You run a security review using Claude Code (in the terminal)."
)

add_bold_para("The prompt you type in Claude Code (in the terminal):")
add_code_block(
    "Review mcp-server/procurement_server.py and .claude/settings.json\n"
    "for security issues. Check for: hardcoded paths, embedded credentials,\n"
    "write access to the database, and secrets in CLAUDE.md.\n"
    "Give me a pass/fail for each check."
)

add_bold_para("Folder layout:")
add_code_block(
    "practice/\n"
    "+-- CLAUDE.md                (no secrets)\n"
    "+-- data/\n"
    "|   +-- procurement.db       (read-only access)\n"
    "+-- mcp-server/\n"
    "|   +-- procurement_server.py (reads DB path from env var)\n"
    "+-- .claude/\n"
    "    +-- settings.json        (env var set here)"
)

add_bold_para("What you should see.")
add_normal(
    "A four-line report: "
    "Hardcoded paths: PASS (database path comes from environment variable). "
    "Embedded credentials: PASS (no passwords in source code). "
    "Write access: PASS (connection uses mode=ro). "
    "Secrets in CLAUDE.md: PASS (no credentials found)."
)

add_bold_para("What Claude Code did, behind the scenes.")
steps = [
    "Claude opened mcp-server/procurement_server.py and searched for hardcoded file paths and credential strings.",
    "It checked each sqlite3.connect() call for the mode=ro flag.",
    "It opened .claude/settings.json and confirmed the database path is in the env block, not in the script.",
    "It opened CLAUDE.md and scanned for patterns that look like secrets (API keys, passwords, connection strings).",
    "It reported pass or fail for each of the four checks.",
]
for i, s in enumerate(steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(s)

# ============================================================
# 7. DAY IN THE LIFE
# ============================================================
doc.add_heading(
    "7. A day in the life: David, Procurement Systems Analyst", level=1
)

doc.add_heading("Meet David", level=2)

add_normal(
    "David is a Procurement Systems Analyst at a mid-size medical device "
    "manufacturer based in Minneapolis. The company manages $46.9M in annual "
    "indirect and direct spend across 20 key suppliers. David's job is to "
    "keep procurement data accessible, accurate, and actionable. He built a "
    "procurement MCP server two weeks ago using Course 9. Today is a normal "
    "Tuesday. Here is how it goes."
)

# Scenario 1
doc.add_heading("08:15. The VP's morning question", level=2)

add_normal(
    "David opens Slack. The VP of Procurement has posted: "
    '"What is our open PO exposure with Meridian Chemicals? '
    'They flagged a force majeure on their Baton Rouge plant."'
)

add_normal(
    "Two weeks ago, this would have taken 12 minutes. David would log into "
    "the ERP, run an open PO report, export it to CSV, open it in Excel, "
    "filter for Meridian, and reply with the total. By the time the VP saw it, "
    "she might already be in another meeting."
)

add_normal("David opens his terminal and starts Claude Code in the procurement project folder.")

add_code_block("cd Nexus_Procurement/\nclaude")

add_normal("He types one prompt:")

add_code_block(
    "Show me all open POs with Meridian Chemicals. Include PO number, amount,\n"
    "order date, delivery date, and status. Flag any that are overdue."
)

add_normal(
    'Claude Code (in the terminal) calls get_open_pos with supplier_id = "SUP007". '
    "Four seconds later, David has a table: 4 open POs totaling $67,400. "
    "Two are overdue by 8 and 14 days. He copies the table into Slack. "
    "Total time: 45 seconds."
)

add_what_to_learn(
    "The value of MCP is not the technology. It is the speed of the response loop. "
    "When a VP asks a question, the answer needs to arrive before the VP moves on "
    "to the next topic. A 12-minute turnaround is a missed opportunity. "
    "A 45-second turnaround changes how procurement is perceived by the business."
)

# Scenario 2
doc.add_heading("09:30. Contract renewal review for the quarterly meeting", level=2)

add_normal(
    "David's manager asks him to prepare a list of contracts expiring in the "
    "next 90 days for the quarterly business review. Normally, David would open "
    "the contract management system, export the full register, filter by expiry "
    "date, and manually build a summary table in PowerPoint. That takes about 25 minutes."
)

add_code_block(
    "Which contracts expire within the next 90 days? Include supplier name,\n"
    "contract value, expiry date, and auto-renewal flag.\n"
    "Sort by expiry date, earliest first."
)

add_normal(
    "Claude Code (in the terminal) calls get_contract_status for all suppliers and "
    "filters for expiry before 2026-07-25. Three contracts appear: Meridian Chemicals "
    "($1,440,000, expiring 2026-05-31, auto-renew: no), TechForward Inc ($960,000, "
    "expiring 2026-06-15, auto-renew: yes), and Pinnacle Staffing ($720,000, "
    "expiring 2026-07-01, auto-renew: no). David saves the output to Drafts/."
)

add_code_block(
    "Save that table to Drafts/contract_renewals_Q2_2026.md with a one-paragraph\n"
    "executive summary that names the three suppliers, their combined value,\n"
    "and the earliest deadline."
)

add_normal(
    'Claude Code writes the summary: "Three contracts totaling $3,120,000 expire '
    "before 2026-07-25. Meridian Chemicals ($1,440,000) expires first on 2026-05-31 "
    'and does not auto-renew. Decision needed by 2026-05-15." '
    "David pastes this into the quarterly deck. Total time: 2 minutes."
)

add_what_to_learn(
    "MCP is most powerful when combined with a save-to-file step. The live query "
    "gives you current data. Saving it with an executive summary gives you a "
    "ready-to-present artifact. The two-step pattern (query, then format and save) "
    "is the core workflow for any recurring procurement report."
)

# Scenario 3
doc.add_heading("11:00. A CFO question about category spend", level=2)

add_normal(
    'The CFO\'s office emails David\'s VP: "What was our total IT services spend '
    'in Q1 2026? How does it compare to Q1 2025?" The VP forwards it to David '
    'with "Can you get me this in 10 minutes?"'
)

add_normal("David already has the MCP server running. He types:")

add_code_block(
    "What was our total IT services spend in Q1 2026 (January through March)?\n"
    "Compare it to Q1 2025 (same months). Show the dollar and percentage change."
)

add_normal(
    "Claude Code (in the terminal) calls get_supplier_spend twice: once with "
    'category = "it-services" and Q1 2026 dates, once with Q1 2025 dates. '
    "It returns: \"IT services spend in Q1 2026: $1,840,000 across 42 transactions. "
    "Q1 2025: $1,620,000 across 38 transactions. Increase: $220,000 (13.6%).\" "
    "David replies to the VP in under 90 seconds."
)

add_what_to_learn(
    "CFO questions always need specific numbers: a dollar figure, a date range, "
    "and a comparison point. MCP tools handle the data retrieval. Your job is to "
    "frame the question with the right filters (category, date range, comparison "
    'period). The better your prompt, the more useful the answer. "Total IT spend" '
    'is less useful than "Q1 2026 versus Q1 2025, dollar and percentage change."'
)

# Scenario 4
doc.add_heading("13:30. Onboarding a colleague to MCP", level=2)

add_normal(
    "David's colleague Sarah, a Category Manager for raw materials, watches him "
    'answer a question in 30 seconds. She asks: "Can I use that on my machine?" '
    "David walks her through the setup."
)

add_normal("He shows Sarah the three files she needs:")

steps = [
    "The MCP server script (mcp-server/procurement_server.py). She copies this to her project folder.",
    "The settings.json registration. She creates .claude/settings.json with the server entry and her own PROCUREMENT_DB_PATH environment variable pointing to the shared database.",
    'The CLAUDE.md file. She copies it and edits the role line to say "Category Manager for raw materials."',
]
for i, s in enumerate(steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(s)

add_normal("Sarah starts Claude Code, verifies three tools are available, and runs her first query:")

add_code_block(
    "Show me year-to-date spend for all raw materials suppliers,\n"
    "sorted by total spend descending."
)

add_normal(
    "It works. She sees five suppliers with a combined $15.3M in annual spend. "
    "The setup took 8 minutes. The first query took 20 seconds."
)

add_what_to_learn(
    "An MCP server is reusable across team members. The server script and the "
    "database stay the same. Each person configures their own settings.json with "
    "their own environment variables and their own CLAUDE.md with their role. "
    "This is why you put the database path in an environment variable, not in the "
    "script. Portability across machines is the payoff."
)

# Scenario 5
doc.add_heading(
    "15:00. Building a supplier risk brief with live data and a skill", level=2
)

add_normal(
    "David needs to prepare a supplier risk brief for the quarterly review. "
    "He has a skill file (.claude/skills/supplier-risk-brief.md) that defines "
    "the format: open PO exposure, contract status, spend trend, and a risk "
    "recommendation."
)

add_code_block(
    "Prepare a supplier risk brief for Meridian Chemicals.\n"
    "Use the supplier-risk-brief skill.\n"
    "Pull all data from the MCP tools.\n"
    "Save to Drafts/meridian_risk_brief_2026-04-26.md."
)

add_normal(
    "Claude Code (in the terminal) calls all three MCP tools: get_supplier_spend "
    "for spend trend, get_open_pos for PO exposure, and get_contract_status for "
    "the contract terms. It then applies the skill to format the brief: "
    '"Meridian Chemicals: $1,440,000 annual contract expiring 2026-05-31. '
    "Current open PO exposure: $67,400 with 2 overdue POs. "
    "Q1 2026 spend is $412,000, up 11.3% from Q4 2025. "
    "Recommendation: initiate renewal discussions by 2026-05-01 and escalate "
    'the 2 overdue POs to the logistics team."'
)

add_normal(
    "David reviews the brief, makes one edit (adds a note about the force "
    "majeure), and saves it. Total time: 3 minutes."
)

add_what_to_learn(
    "The combination of MCP (live data) and skills (consistent analysis format) "
    "is the most powerful pattern in this course. MCP gets you current numbers. "
    "Skills ensure the analysis is structured the same way every time. "
    "Neither is sufficient alone. Raw data without structure is noise. "
    "Structure without current data is fiction."
)

# Scenario 6
doc.add_heading(
    "16:30. Security review before sharing the server with the team", level=2
)

add_normal(
    'David\'s manager asks: "Before we roll this out to the full team, '
    "can you confirm it is read-only? I do not want anyone accidentally "
    'deleting spend records." David runs the security check.'
)

add_code_block(
    "Review mcp-server/procurement_server.py and .claude/settings.json\n"
    "for security issues. Check for: hardcoded paths, embedded credentials,\n"
    "write access to the database, and secrets in CLAUDE.md.\n"
    "Give me a pass/fail for each."
)

add_normal(
    "Claude Code (in the terminal) reads both files and reports: "
    "Hardcoded paths: PASS (database path comes from PROCUREMENT_DB_PATH "
    "environment variable). Embedded credentials: PASS (no passwords in "
    "source code). Write access: PASS (connection uses mode=ro, and the "
    "_validate_read_only function blocks INSERT, UPDATE, DELETE, DROP, ALTER, "
    "CREATE, and TRUNCATE). Secrets in CLAUDE.md: PASS (no credentials found). "
    "David forwards the results to his manager. Rollout approved."
)

add_what_to_learn(
    "Security is not an afterthought. It is a deployment prerequisite. "
    "The read-only check and the credential scan should run every time the "
    "server script changes. Build this into your workflow: modify the server, "
    "run the security check, then restart Claude Code. Three steps, every time."
)

# Scenario 7
doc.add_heading("17:00. End-of-day: updating the team changelog", level=2)

add_normal(
    "David opens his team's shared changelog and adds a one-line entry for the day:"
)

add_code_block(
    "2026-04-26: Added Sarah (raw-materials category manager) to MCP server access.\n"
    "Confirmed read-only security posture. No credential exposure. Server running\n"
    "stable with three tools. Next: add get_invoice_aging tool for AP team\n"
    "(target: 2026-05-03)."
)

add_normal(
    "He shuts down Claude Code for the day. His terminal sessions today totaled "
    "about 12 minutes of active prompting. The work those 12 minutes replaced "
    "would have taken over 2 hours with manual exports and Excel."
)

add_what_to_learn(
    "Tracking MCP usage (who has access, what tools exist, what is coming next) "
    "is essential for a team deployment. A simple changelog in a shared file is "
    "enough. The log also helps you measure the time savings over weeks, which is "
    "the data you need when your VP asks whether Claude Code is worth the license cost."
)

doc.add_heading("David's day: the numbers", level=2)

add_table(
    ["Task", "Time with MCP", "Time without MCP"],
    [
        ["VP's open PO question (08:15)", "45 seconds", "12 minutes"],
        ["Contract renewal list (09:30)", "2 minutes", "25 minutes"],
        ["CFO category spend comparison (11:00)", "90 seconds", "15 minutes"],
        ["Onboard Sarah to MCP (13:30)", "8 minutes", "N/A (manual process)"],
        ["Supplier risk brief (15:00)", "3 minutes", "35 minutes"],
        ["Security review (16:30)", "1 minute", "20 minutes"],
        ["Total", "About 17 minutes", "About 107 minutes"],
    ],
)

# ============================================================
# 8. THE 20-MINUTE SPRINT
# ============================================================
doc.add_heading(
    "8. The 20-minute sprint: your first live query in 20 minutes", level=1
)

add_normal(
    "This section gets you from zero to your first MCP query in twenty minutes. "
    "No detours. No theory beyond the minimum. You can do this before starting Lesson 1."
)

doc.add_heading("Minutes 0 to 5: install and verify", level=2)

steps = [
    "Open a terminal (Command Prompt on Windows, Terminal on Mac).",
    "Confirm Python is installed: python --version (you need 3.10 or later).",
    "Install the FastMCP library: pip install fastmcp.",
    "Confirm Claude Code is installed: claude --version.",
    'Navigate to the course practice folder: cd "Course_09_The_Integration_Architect/practice".',
]
for i, s in enumerate(steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(s)

doc.add_heading(
    "Minutes 5 to 10: copy the solution server and register it", level=2
)

p = doc.add_paragraph()
run = p.add_run("1. ")
run.bold = True
p.add_run(
    "Copy the solution server into your mcp-server/ folder. "
    "On Windows: copy solutions\\mcp_server_solution.py mcp-server\\procurement_server.py. "
    "On Mac or Linux: cp solutions/mcp_server_solution.py mcp-server/procurement_server.py."
)

p = doc.add_paragraph()
run = p.add_run("2. ")
run.bold = True
p.add_run("Create the .claude/ directory if it does not exist: mkdir -p .claude.")

p = doc.add_paragraph()
run = p.add_run("3. ")
run.bold = True
p.add_run("Create .claude/settings.json with the server registration:")

add_code_block(
    '{\n'
    '  "mcpServers": {\n'
    '    "nexus-procurement": {\n'
    '      "command": "python",\n'
    '      "args": ["mcp-server/procurement_server.py"],\n'
    '      "cwd": "."\n'
    '    }\n'
    '  },\n'
    '  "permissions": {\n'
    '    "allow": [\n'
    '      "mcp__nexus-procurement__get_supplier_spend",\n'
    '      "mcp__nexus-procurement__get_open_pos",\n'
    '      "mcp__nexus-procurement__get_contract_status"\n'
    '    ]\n'
    '  }\n'
    '}'
)

p = doc.add_paragraph()
run = p.add_run("4. ")
run.bold = True
p.add_run(
    "Test the server manually: python mcp-server/procurement_server.py. "
    "It should start without errors. Press Ctrl+C to stop it."
)

doc.add_heading("Minutes 10 to 15: run your first live query", level=2)

p = doc.add_paragraph()
run = p.add_run("1. ")
run.bold = True
p.add_run("Start Claude Code: claude.")

p = doc.add_paragraph()
run = p.add_run("2. ")
run.bold = True
p.add_run(
    'Verify the connection: type "What MCP tools do you have access to?" '
    "You should see three tools listed."
)

p = doc.add_paragraph()
run = p.add_run("3. ")
run.bold = True
p.add_run("Run your first query:")

add_code_block("What is our total spend with Great Lakes Steel?")

add_normal(
    "Claude Code (in the terminal) calls get_supplier_spend and returns a "
    "dollar figure from procurement.db. That number came from a live database "
    "query, not a CSV file."
)

p = doc.add_paragraph()
run = p.add_run("4. ")
run.bold = True
p.add_run("Run a second query to confirm it is not a fluke:")

add_code_block(
    "Show me all open POs over $5,000. Include supplier name, amount,\n"
    "and delivery date."
)

add_normal("You should see a filtered table of open POs from the database.")

doc.add_heading("Minutes 15 to 20: review and plan next steps", level=2)

steps = [
    'Run one more query: "Which contracts expire in the next 90 days?" Confirm the get_contract_status tool works.',
    "Type /quit to exit Claude Code.",
    "Open mcp-server/procurement_server.py in any text editor. Find the three @mcp.tool() decorators. Those are the three tools you just called.",
    "Plan your next step: start Lesson 1 for the full explanation, or jump to Lesson 4 if you want to build your own server from scratch.",
]
for i, s in enumerate(steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(s)

add_normal(
    "You have now queried a live procurement database through Claude Code "
    "(in the terminal) in under 20 minutes. The rest of the course teaches "
    "you how to build, modify, secure, and combine MCP servers with skills."
)

# ============================================================
# 9. FIRST WEEK PLANNER
# ============================================================
doc.add_heading("9. Your first week with MCP in your real work", level=1)

doc.add_heading("Day 1 (Monday): install and first query", level=2)

add_bold_para(
    "Goals:",
    "Install FastMCP. Copy the course server. Register it. Run your first "
    "live query against procurement.db.",
)

add_normal(
    "Follow the 20-minute sprint in section 8. By the end of the day, you "
    "should have Claude Code (in the terminal) calling get_supplier_spend, "
    "get_open_pos, and get_contract_status against the practice database. "
    "If you have extra time, start Lesson 1 and Lesson 2."
)

doc.add_heading(
    "Day 2 (Tuesday): understand the server internals", level=2
)

add_bold_para(
    "Goals:",
    "Read the server script. Identify the three tools, their inputs, and "
    "their SQL queries. Modify one tool description.",
)

add_normal(
    "Work through Lesson 3 (Anatomy of an MCP Server). By the end of the day, "
    "you should be able to open procurement_server.py and explain to a colleague "
    "what each @mcp.tool() function does. Bonus: change the description of "
    "get_open_pos to be more specific (for example, add \"Includes PO number, "
    'amount, dates, and status") and observe whether Claude Code (in the terminal) '
    "calls it more accurately."
)

doc.add_heading(
    "Day 3 (Wednesday): build your own server from scratch", level=2
)

add_bold_para(
    "Goals:",
    "Delete the solution server. Rebuild all three tools with Claude Code's help. "
    "Test each one.",
)

add_normal(
    "Work through Lesson 4 (Building the Procurement MCP Server). This is the "
    "most important lesson. Building the server yourself teaches you how tools "
    "map to SQL queries. By the end of the day, you should have a working server "
    "that you wrote (with Claude's help), not a copy of the solution."
)

doc.add_heading("Day 4 (Thursday): lock it down", level=2)

add_bold_para(
    "Goals:",
    "Make the database read-only. Move the database path to an environment "
    "variable. Remove any secrets from CLAUDE.md.",
)

add_normal(
    "Work through Lesson 5 (Security Patterns). By the end of the day, your "
    "server should pass all four security checks: no hardcoded paths, no embedded "
    "credentials, read-only database access, and no secrets in CLAUDE.md. "
    "Test that a write attempt is blocked."
)

doc.add_heading("Day 5 (Friday): combine MCP with skills", level=2)

add_bold_para(
    "Goals:",
    "Create a spend-variance-analysis skill. Run it with live MCP data. "
    "Save the output to Drafts/.",
)

add_normal(
    "Work through Lesson 6 (MCP Plus Skills). By the end of the day, you should "
    "have a saved spend variance report at Drafts/spend_variance_Q1_2026.md that "
    "was generated from live database queries and formatted by a skill. Show the "
    'result to a colleague. If they ask "How did you do that?", walk them through '
    "the setup."
)

# ============================================================
# 10. THE PATTERN
# ============================================================
doc.add_heading("10. The pattern: connect once, query forever", level=1)

add_normal(
    "Every MCP integration follows the same four-step pattern, regardless "
    "of the data source."
)

steps = [
    (
        "Build the server.",
        "Write a Python script with FastMCP. One @mcp.tool() function per query "
        "type. Each function takes typed inputs, runs a query, and returns a JSON string.",
    ),
    (
        "Register the server.",
        "Add the server to .claude/settings.json with the command, args, and cwd "
        "fields. Add tool names to the permissions.allow array so Claude Code (in the "
        "terminal) does not prompt on every call.",
    ),
    (
        "Secure the server.",
        "Make the database connection read-only (mode=ro for SQLite, read-only roles "
        "for PostgreSQL or MySQL). Move credentials to environment variables. "
        "Scan CLAUDE.md for secrets. Block all non-SELECT SQL.",
    ),
    (
        "Combine with skills.",
        "Write skill files that describe the analysis steps (what to query, how to "
        "compare, how to format). The MCP tool handles data retrieval. The skill handles "
        "methodology. Together, they produce repeatable, high-quality outputs.",
    ),
]
for i, (bold, text) in enumerate(steps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. {bold} ")
    run.bold = True
    p.add_run(text)

add_normal(
    "This pattern works for SQLite, PostgreSQL, REST APIs, ERP connectors, "
    "and any other data source that can be wrapped in a Python function. "
    "The protocol is the same. The server does the translation. Claude Code "
    "(in the terminal) does not need to know what database engine you use."
)

add_why_matters(
    "Once you understand this four-step pattern, you can connect Claude Code "
    "(in the terminal) to any procurement system your organization runs. "
    "The first integration takes five hours (this course). The second takes under "
    "an hour. The third takes 20 minutes. The pattern compounds because each new "
    "server reuses the same registration, security, and skill-combination techniques."
)

# ============================================================
# 11. TROUBLESHOOTING
# ============================================================
doc.add_heading("11. Quick reference and troubleshooting", level=1)

doc.add_heading("Things to remember", level=2)

bullets = [
    "Always restart Claude Code after editing settings.json. Claude Code reads settings at startup, not at runtime.",
    "Tool descriptions matter. If Claude Code (in the terminal) calls the wrong tool, the description is probably too vague. Make each description specific to one query type.",
    "MCP tools return strings. If your Python function returns a dictionary, wrap it in json.dumps() first.",
    "Read-only mode is not optional for production. Use mode=ro for SQLite and read-only database roles for PostgreSQL or MySQL.",
    "CLAUDE.md is visible to anyone who opens the folder. Never put passwords, API keys, or connection strings in it.",
    "The permissions.allow array in settings.json pre-approves specific tools. Without it, Claude Code (in the terminal) prompts for permission on every tool call, which slows down multi-tool queries.",
]
for b in bullets:
    doc.add_paragraph(b, style='List Bullet')

doc.add_heading("Common problems and the matching fix", level=2)

add_table(
    ["Problem", "Likely cause", "Fix"],
    [
        [
            'Claude Code says "No MCP tools found" at startup',
            "settings.json is missing, has a syntax error, or points to the wrong script path",
            'Open .claude/settings.json and verify: 1) the file is valid JSON (no trailing commas), 2) the "command" field works in your terminal (try "python3" on Mac), 3) the "args" path points to the actual server script',
        ],
        [
            "\"ModuleNotFoundError: No module named 'fastmcp'\"",
            "FastMCP is installed in a different Python environment than the one Claude Code uses",
            '"pip install fastmcp" in the same terminal where you run Claude Code. If you use conda or venv, activate the environment first',
        ],
        [
            "Claude Code calls the wrong tool for your question",
            "Tool descriptions overlap or are too vague",
            'Rewrite the docstring for each @mcp.tool() function. "Returns spend totals by supplier and date range" is better than "Returns procurement data." Each tool needs a unique, specific description',
        ],
        [
            "The query returns no results for a supplier you know exists",
            "The supplier name or ID in your prompt does not match the database exactly",
            "Check the exact value in supplier-master.csv. Use the supplier_id (SUP001) instead of the name. Or add COLLATE NOCASE to your SQL WHERE clause for case-insensitive matching",
        ],
        [
            '"attempt to write a readonly database" on a legitimate read query',
            "Your SQL includes CREATE TEMP TABLE, a PRAGMA, or another statement that requires write access",
            "Rewrite the query to avoid temporary tables. Use subqueries or CTEs (WITH clauses) instead. Avoid PRAGMAs that modify state",
        ],
        [
            "Claude Code prompts for permission on every MCP tool call",
            "The permissions.allow array in settings.json does not list the tool names, or the names are misspelled",
            "Add each tool to permissions.allow using the pattern mcp__<server-name>__<tool-name>. Restart Claude Code after editing",
        ],
    ],
)

# ============================================================
# 12. DONE CHECKLIST
# ============================================================
doc.add_heading("12. You are done with Course 9 when", level=1)

checklist = [
    "Your MCP server runs and registers in .claude/settings.json without errors.",
    'You type "What is our total spend with Great Lakes Steel?" and Claude Code (in the terminal) calls get_supplier_spend, queries procurement.db, and returns the answer.',
    'You type "Show me all overdue POs" and Claude Code (in the terminal) calls get_open_pos with a status filter and returns a table.',
    'You type "Which contracts expire in the next 90 days?" and Claude Code (in the terminal) calls get_contract_status and returns the list.',
    "Your server enforces read-only access. No INSERT, UPDATE, or DELETE queries are possible.",
    "You combine an MCP tool call with a skill to produce a formatted supplier risk brief or spend variance report from live data.",
    "You can explain MCP in one sentence to a colleague who has never seen it.",
    "You can read a tool schema and name the required inputs, optional inputs, and return format.",
    "Your CLAUDE.md contains zero secrets, and your database path comes from an environment variable.",
]
for i, item in enumerate(checklist, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. ")
    run.bold = True
    p.add_run(item)

# ============================================================
# SET PAGE MARGINS
# ============================================================
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# ============================================================
# SAVE
# ============================================================
output_path = os.path.join(
    r"C:\Users\SambitTripathy\OneDrive - U2xAI\Claude Code Projects"
    r"\S2p Training\Course List\Claude Code Foundation for S2P\Handouts",
    "Course_09_The_Integration_Architect_Handout.docx",
)

# Delete existing file
if os.path.exists(output_path):
    os.remove(output_path)

doc.save(output_path)
print(f"Saved to: {output_path}")

# Word count estimate
total_text = []
for p in doc.paragraphs:
    total_text.append(p.text)
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            total_text.append(cell.text)
word_count = sum(len(t.split()) for t in total_text)
print(f"Estimated word count: {word_count}")
print(f"Paragraphs: {len(doc.paragraphs)}")
print(f"Tables: {len(doc.tables)}")
