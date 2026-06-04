"""Build the Course 3: The Skill Builder e-learning handout (v2).

Revised version with scenario-led section 2, folder explanations with
examples in section 3, a real SKILL.md extract in section 5, expanded
worked examples in section 6, and Claude Code terminal examples
throughout every section so learners connect each concept to the tool.

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

OUTPUT_PATH = _PROJECT_ROOT / "Handouts" / "Course_03_The_Skill_Builder_Handout_v2.docx"


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
    para(doc, "Series 2 (Engineering Track) | Course 3", italic=True)
    doc.add_heading("The Skill Builder", level=0)
    para(
        doc,
        "Reusable methodologies for sourcing events, captured as "
        "SKILL.md files.",
        italic=True,
        size=14,
    )
    para(
        doc,
        "Four hours. Six lessons. No coding. Real bid data with 25 "
        "carriers, 1,500 historical shipments, and six full bid "
        "responses.",
        italic=True,
    )
    para(
        doc,
        "Use this handout alongside the course folder at "
        "Detailed Course Content/Course_03_The_Skill_Builder/.",
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
        "folder has the data, the starter files, the six lessons, and "
        "the reference answers.",
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
        "sourcing event.",
    )
    numbered(doc, "Read section 5 for the mental model of what a SKILL.md is.")
    numbered(doc, "Open the course folder and start Lesson 1.")
    numbered(
        doc,
        "Come back to this handout when you want context (sections "
        "6 to 8 are useful while you work).",
    )
    numbered(
        doc,
        "Use section 11 (troubleshooting) if something does not "
        "look right.",
    )

    # ===================================================================
    # 2. What this course teaches  (REVISED)
    # ===================================================================
    heading(doc, "2. What this course teaches", 1)

    # --- Opening scenario ---
    heading(doc, "A Monday morning you have lived before", 2)
    para(
        doc,
        "It is 09:00 Monday. Your CPO has just approved the next "
        "sourcing event: a logistics consolidation RFP. Annual "
        "baseline spend is 11.2m USD. The savings target is 1.6m "
        "USD. Award by 2026-06-30.",
    )
    para(
        doc,
        "You open a blank Word document and start writing the RFP "
        "package. By Wednesday afternoon you have 28 pages. "
        "Thursday you build the evaluation scorecard in Excel, "
        "hand-scoring each bid against five criteria. The following "
        "Monday you write the award memo, cross-referencing the "
        "scorecard, the risk notes you scribbled in a notebook, and "
        "the savings estimate you computed in a separate spreadsheet. "
        "Total elapsed: two and a half weeks.",
    )
    para(
        doc,
        "Six weeks later the next sourcing event lands. You open "
        "another blank Word document. Same work. Same time. Same "
        "risk of inconsistency between events.",
    )
    para(
        doc,
        "This course breaks that cycle. Instead of writing each "
        "deliverable from scratch, you write the **methodology** "
        "that creates each deliverable. The methodology is a "
        "SKILL.md file: a 40- to 90-line markdown file that Claude "
        "Code (in the terminal) reads and follows every time you "
        "run it. You write it once. Every future sourcing event "
        "reuses the same methodology with new inputs.",
    )

    # --- The five skills with descriptions and examples ---
    heading(doc, "The five skills you will write", 2)
    para(
        doc,
        "Each skill captures one step of a sourcing event. Below "
        "is what each skill does, what it reads, what it produces, "
        "and a short extract of what the output looks like.",
    )

    # rfp-builder
    heading(doc, "rfp-builder.md", 3)
    para(
        doc,
        "**What it does.** Reads your category brief, your supplier "
        "longlist, and a skeleton template, then builds a complete "
        "six-section RFP package: executive overview, scope of work, "
        "commercial terms, evaluation criteria, supplier response "
        "template, and process timeline.",
    )
    para(
        doc,
        "**Why it matters.** Without this skill, writing the RFP "
        "package takes 5 to 10 days. With it, you type one prompt "
        "in Claude Code and get the package in 60 seconds. The "
        "package names your real savings target (1.6m USD), your "
        "real close date (2026-06-15), and your real evaluation "
        "weights (Price 40%, Service 25%, Capability 20%, "
        "Sustainability 10%, Implementation 5%).",
    )
    para(doc, "**Example: the prompt you type in Claude Code.**")
    code_block(
        doc,
        "Use the rfp-builder skill in skills/rfp-builder.md.\n"
        "Inputs are in inputs/ and bid-responses/.\n"
        "Templates in templates/.\n"
        "Save the output to outputs/rfp-package.md.",
    )
    para(
        doc,
        "**Example: what appears in outputs/rfp-package.md.** "
        "The executive overview opens with: \"Acme Plc invites bids "
        "for the consolidation of its logistics carrier base from "
        "14 incumbents to 4 strategic partners. Annual baseline "
        "spend is 11.2m USD. The savings target is 1.6m USD "
        "(14% of baseline). Bids close 2026-06-15. Award by "
        "2026-06-30.\"",
    )

    # bid-scorer
    heading(doc, "bid-scorer.md", 3)
    para(
        doc,
        "**What it does.** Reads every bid response PDF in "
        "bid-responses/, scores each bidder on five weighted "
        "criteria (Price, Service, Capability, Sustainability, "
        "Implementation), and ranks them in a comparison table.",
    )
    para(
        doc,
        "**Why it matters.** Scoring six bids by hand in Excel "
        "takes 1 to 2 days and introduces inconsistency: you "
        "read the first bid fresh but score the sixth one tired. "
        "The bid-scorer skill applies the same numeric bands to "
        "every bid in 90 seconds. Two analysts running the same "
        "skill on the same bids get the same rank order.",
    )
    para(doc, "**Example: the prompt you type in Claude Code.**")
    code_block(
        doc,
        "Use the bid-scorer skill in skills/bid-scorer.md.\n"
        "Process every file in bid-responses/.\n"
        "Use inputs/supplier-longlist.csv for capacity_tier,\n"
        "financial_health, and incumbent lookups.\n"
        "Save the output to outputs/bid-comparison.md.",
    )
    para(
        doc,
        "**Example: what the comparison table looks like.** "
        "A markdown table with eight columns (Carrier, Price, "
        "Service, Capability, Sustainability, Implementation, "
        "Total, Recommended). Continental Roads scores 87.4, "
        "FastRoad UK 85.1, Globex Freight 82.6. Each row has a "
        "Yes or No in the Recommended column.",
    )

    # risk-profiler
    heading(doc, "risk-profiler.md", 3)
    para(
        doc,
        "**What it does.** Reads each bid response and the supplier "
        "longlist, then scores every bidder on three risk dimensions: "
        "financial risk (based on financial_health from the longlist), "
        "operational risk (based on capacity_tier and incumbent "
        "status), and commercial risk (based on contract terms and "
        "implementation cost in the bid).",
    )
    para(
        doc,
        "**Why it matters.** Risk assessment is often the most "
        "subjective part of a sourcing event. One analyst calls a "
        "supplier \"medium risk\"; another calls the same supplier "
        "\"high risk\". The risk-profiler skill uses numeric bands "
        "(1 to 5 per dimension, total 3 to 15) so the assessment "
        "is repeatable. Each bidder's paragraph names the highest "
        "risk and a specific mitigation tied to that risk.",
    )
    para(doc, "**Example: the prompt you type in Claude Code.**")
    code_block(
        doc,
        "Use the risk-profiler skill in skills/risk-profiler.md.\n"
        "Read bid-responses/ and inputs/supplier-longlist.csv.\n"
        "Save to outputs/risk-profile.md.",
    )
    para(
        doc,
        "**Example: what a risk paragraph looks like.** "
        "\"Pacific Forwarders. Total risk: 9/15. Key risk: "
        "financial (4/5). Financial health is rated weak in the "
        "longlist. Mitigation: require a parent company guarantee "
        "and quarterly financial reporting as a contract condition.\"",
    )

    # savings-calculator
    heading(doc, "savings-calculator.md", 3)
    para(
        doc,
        "**What it does.** Sums the baseline spend from 1,500 "
        "historical shipments, reads the proposed annual values "
        "from the bid comparison, and computes annualized savings "
        "for the recommended panel. Produces a headline figure, "
        "a calculation table, and a sensitivity paragraph.",
    )
    para(
        doc,
        "**Why it matters.** Savings calculations done by hand "
        "in Excel are error-prone and hard to audit. The "
        "savings-calculator skill traces every figure back to "
        "a named source file (spend-baseline.csv or "
        "bid-comparison.md). The CFO sees a single table: "
        "Baseline 10.86m, Proposed 9.31m, Savings 1.55m "
        "(14.3%), Target 1.6m (96.9% of target).",
    )
    para(doc, "**Example: the prompt you type in Claude Code.**")
    code_block(
        doc,
        "Use the savings-calculator skill in\n"
        "skills/savings-calculator.md.\n"
        "Read inputs/spend-baseline.csv and outputs/bid-comparison.md.\n"
        "Save to outputs/savings-case.md.",
    )
    para(
        doc,
        "**Example: what the headline looks like.** "
        "\"Baseline spend (1,487 shipments, 12 months): 10.86m "
        "USD. Proposed panel spend: 9.31m USD. Annualized "
        "savings: 1.55m USD (14.3%). Against the 1.6m target, "
        "this is 96.9% achievement. Year 1 risk-adjusted savings "
        "(after 42,000 USD implementation): 1.51m USD.\"",
    )

    # award-memo
    heading(doc, "award-memo.md", 3)
    para(
        doc,
        "**What it does.** Reads the bid comparison, the risk "
        "profile, the savings case, and the category brief, then "
        "synthesises everything into a one-page award "
        "recommendation memo. The memo names a four-carrier "
        "panel (one road FTL, one road LTL or pallet, one sea "
        "FCL, one air), the contract value per carrier, three "
        "risks with mitigation owners, and the savings headline.",
    )
    para(
        doc,
        "**Why it matters.** The award memo is the document that "
        "goes to the panel meeting. Writing it by hand means "
        "re-reading the scorecard, the risk notes, and the "
        "savings spreadsheet, then synthesising them under time "
        "pressure. The award-memo skill does the synthesis in 60 "
        "seconds. It quotes the savings figure from "
        "savings-case.md (it does not recompute), so the memo "
        "and the savings case always agree.",
    )
    para(doc, "**Example: the prompt you type in Claude Code.**")
    code_block(
        doc,
        "Use the award-memo skill in skills/award-memo.md.\n"
        "Read outputs/bid-comparison.md, outputs/risk-profile.md,\n"
        "outputs/savings-case.md, and inputs/category-brief.md.\n"
        "Save to outputs/award-memo.md.",
    )
    para(
        doc,
        "**Example: what the recommendation opens with.** "
        "\"We recommend awarding the logistics consolidation "
        "contract to a four-carrier panel: Continental Roads "
        "(road FTL, 3.2m USD), FastRoad UK (road LTL, 2.8m "
        "USD), OceanLine (sea FCL, 2.1m USD), and Helios Air "
        "Freight (air, 1.2m USD). Annualized savings: 1.55m "
        "USD (14.3% of baseline). Decision needed by "
        "2026-06-30.\"",
    )

    # --- Chaining ---
    heading(doc, "The chain: five skills, one session, six deliverables", 2)
    para(
        doc,
        "The real power is composition. You run the five skills in "
        "order within a single Claude Code session. Each skill's "
        "output becomes the next skill's input. Here is the "
        "exact prompt that runs the full chain:",
    )
    code_block(
        doc,
        "Run these five skills in order. After each step, confirm\n"
        "the output file exists before moving to the next.\n\n"
        "Step 1: Use skills/rfp-builder.md. Save to outputs/rfp-package.md.\n"
        "Step 2: Use skills/bid-scorer.md. Save to outputs/bid-comparison.md.\n"
        "Step 3: Use skills/risk-profiler.md. Save to outputs/risk-profile.md.\n"
        "Step 4: Use skills/savings-calculator.md. Save to outputs/savings-case.md.\n"
        "Step 5: Use skills/award-memo.md. Save to outputs/award-memo.md.",
    )
    para(
        doc,
        "Total elapsed: about 7 minutes for six deliverables. The "
        "next sourcing event uses the same five skills with new "
        "inputs. You configure; Claude executes.",
    )

    # ===================================================================
    # 3. What is in the course folder  (REVISED)
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
        "Course_03_The_Skill_Builder/\n"
        "+-  README.md\n"
        "+-  COURSE_OVERVIEW.md\n"
        "+-  lessons/\n"
        "+-  practice/\n"
        "|   +-  CLAUDE.md\n"
        "|   +-  inputs/\n"
        "|   +-  bid-responses/\n"
        "|   +-  templates/\n"
        "|   +-  skills/\n"
        "|   +-  outputs/\n"
        "+-  solutions/\n"
        "+-  scripts/build_course_data.py",
    )
    para(doc, "Today's date in the practice data is **2026-04-25**.")
    para(
        doc,
        "Below is what each folder and file does, with an example "
        "of what you will find inside.",
    )

    # README.md
    heading(doc, "README.md", 3)
    para(
        doc,
        "The starting point. It lists what is in the course, "
        "what you need before you start (Course 1 and Course 2 "
        "finished, Claude Code installed), and a step-by-step "
        "guide for how to work through the six lessons.",
    )
    para(
        doc,
        "**Example.** The README tells you: \"Open "
        "COURSE_OVERVIEW.md. It tells you the story. Then open "
        "lessons/Lesson_01_What_A_Skill_Is.md. Follow along on "
        "your laptop.\"",
    )

    # COURSE_OVERVIEW.md
    heading(doc, "COURSE_OVERVIEW.md", 3)
    para(
        doc,
        "The scenario. It describes the logistics consolidation "
        "RFP you are running, the practice data you have, the "
        "six lessons with time estimates, and the rubric for "
        "\"done\". Read this before Lesson 1 so you understand "
        "the story behind the exercises.",
    )
    para(
        doc,
        "**Example.** The overview says: \"Acme Plc is "
        "consolidating its logistics carrier base from 14 "
        "incumbents down to 4 strategic partners. Annual baseline "
        "spend is 11.2m USD. Savings target is 1.6m USD.\"",
    )

    # lessons/
    heading(doc, "lessons/", 3)
    para(
        doc,
        "Six markdown files, one per lesson, numbered in order. "
        "Each lesson opens with a scenario (\"It is 09:00 Monday. "
        "Your CPO has just approved...\"), then walks you through "
        "step by step: what to type in the terminal, what Claude "
        "does, what you should see on screen.",
    )
    para(
        doc,
        "**Example.** Lesson 1 tells you: \"Copy the reference "
        "rfp-builder skill into your skills folder. Start Claude. "
        "Type this prompt. Watch Claude produce "
        "outputs/rfp-package.md in 60 seconds.\"",
    )

    # practice/CLAUDE.md
    heading(doc, "practice/CLAUDE.md", 3)
    para(
        doc,
        "The project context file Claude Code reads automatically "
        "when you start a session in the practice folder. It tells "
        "Claude who you are (Strategic Sourcing Lead at Acme Plc), "
        "what the folder layout is, what the folder rules are "
        "(inputs/ is read-only, outputs/ is where deliverables go), "
        "and what writing rules to follow (American English, Oxford "
        "commas, active voice, specific numbers).",
    )
    para(
        doc,
        "**Example.** The CLAUDE.md says: \"Save any new files "
        "(drafts, scorecards, memos) to outputs/. The skills in "
        "skills/ are methodologies, not one-off prompts.\"",
    )
    para(
        doc,
        "**Why this matters.** Without this file, Claude produces "
        "generic output. With it, every output Claude produces "
        "uses Acme's context, Acme's rules, and Acme's folder "
        "structure. You set this up once and it applies to every "
        "session automatically.",
    )

    # inputs/
    heading(doc, "practice/inputs/", 3)
    para(
        doc,
        "Three source documents that drive the sourcing event. "
        "These are read-only. Claude reads them but does not "
        "modify them.",
    )
    bullet(
        doc,
        "**category-brief.md** (one page). The sourcing brief "
        "your CPO approved. It names the savings target (1.6m "
        "USD), the close date (2026-06-15), the award date "
        "(2026-06-30), the in-scope modes (road FTL, road LTL, "
        "sea FCL, air), and the stakeholders (Director of "
        "Operations as sponsor, CFO as decision authority).",
    )
    bullet(
        doc,
        "**supplier-longlist.csv** (25 rows). One row per "
        "candidate carrier. Columns include carrier_id, "
        "carrier_name, modes, primary_geography, certifications, "
        "capacity_tier, financial_health, otd_pct_12m, "
        "contract_terms_offered, and incumbent. Example row: "
        "CAR001, FastRoad UK, road_ftl;road_ltl, US+Canada, "
        "ISO_9001;ISO_14001, tier_1, strong, 96.2, "
        "net_30;net_45, yes.",
    )
    bullet(
        doc,
        "**spend-baseline.csv** (about 1,500 rows). One row per "
        "historical shipment over the last 12 months. Columns: "
        "shipment_id, carrier_id, mode, from_location, "
        "to_location, total_gbp, ship_date. This is the data "
        "that establishes baseline spend by lane.",
    )
    para(doc, "**Example: how a skill uses inputs/.**")
    para(
        doc,
        "When you run the rfp-builder skill, Claude opens "
        "category-brief.md, extracts the savings target and "
        "close date, opens supplier-longlist.csv, groups "
        "carriers by mode, and uses both to populate the RFP "
        "package. You do not tell Claude which columns to read. "
        "The skill file tells Claude which columns to read.",
    )

    # bid-responses/
    heading(doc, "practice/bid-responses/", 3)
    para(
        doc,
        "Six PDF files, one per shortlisted bidder. Each file "
        "follows the same six-section structure: Executive "
        "summary, Capability statement, Pricing table, Service "
        "commitments, Contract terms, and References. In real "
        "life, bid responses arrive as PDF or Word attachments. "
        "Claude Code reads PDFs directly, so no conversion is "
        "needed. This consistent structure is what makes the "
        "bid-scorer skill possible.",
    )
    para(doc, "The six bidders are:")
    bullet(doc, "BID_CAR001_FastRoad_UK.pdf (road FTL and LTL, incumbent)")
    bullet(doc, "BID_CAR003_OceanLine.pdf (sea FCL)")
    bullet(doc, "BID_CAR008_Pacific_Forwarders.pdf (sea FCL, non-incumbent)")
    bullet(doc, "BID_CAR010_Globex_Freight.pdf (road FTL)")
    bullet(doc, "BID_CAR012_Helios_Air_Freight.pdf (air)")
    bullet(doc, "BID_CAR017_Continental_Roads.pdf (road FTL and LTL)")
    para(
        doc,
        "**Example: what a pricing table looks like inside a bid.** "
        "A table with columns Lane, Mode, Volume per year, "
        "Unit rate (USD per shipment), and Annual value (USD). "
        "FastRoad UK's pricing table might show: US Domestic, "
        "road_ftl, 420, 285, 119,700. Claude Code reads the "
        "PDF directly and extracts the table data.",
    )

    # templates/
    heading(doc, "practice/templates/", 3)
    para(
        doc,
        "Three skeleton documents. Each has the section headings "
        "and column headers but no content. Your skills read these "
        "skeletons and fill them in with data from inputs/ and "
        "bid-responses/.",
    )
    bullet(
        doc,
        "**rfp-template.md.** Six section headings: Executive "
        "overview, Scope of work, Commercial terms, Evaluation "
        "criteria, Supplier response template, Process and "
        "timeline. The rfp-builder skill uses this as its "
        "output structure.",
    )
    bullet(
        doc,
        "**scorecard-template.md.** An eight-column table header: "
        "Carrier, Price, Service, Capability, Sustainability, "
        "Implementation, Total, Recommended. The bid-scorer "
        "skill fills in one row per bidder.",
    )
    bullet(
        doc,
        "**award-memo-template.md.** Six sections: Recommendation, "
        "Bid comparison summary, Risks and mitigations, Savings "
        "case, Process and decisions, Audit footer. The award-memo "
        "skill reads the other outputs and populates this.",
    )
    para(
        doc,
        "**Example: why templates matter.** Without a template, "
        "each run of the rfp-builder might produce sections in a "
        "different order. The template pins the structure, so "
        "every RFP your team produces has the same shape.",
    )

    # skills/
    heading(doc, "practice/skills/", 3)
    para(
        doc,
        "**Starts empty.** This is the folder you fill across "
        "Lessons 3 to 5. By the end of the course it holds five "
        "SKILL.md files (rfp-builder.md, bid-scorer.md, "
        "risk-profiler.md, savings-calculator.md, award-memo.md). "
        "Each file is 40 to 90 lines.",
    )
    para(
        doc,
        "**Example: how you check what is in the folder.** In "
        "your terminal, type:",
    )
    code_block(doc, "ls skills")
    para(
        doc,
        "Before Lesson 3, you see only README.md. After Lesson 5, "
        "you see all five skill files plus the README.",
    )

    # outputs/
    heading(doc, "practice/outputs/", 3)
    para(
        doc,
        "**Starts empty.** This is where Claude saves every "
        "deliverable the skills produce. By the end of the course "
        "it holds six files: rfp-package.md, bid-comparison.md, "
        "risk-profile.md, savings-case.md, award-memo.md, and "
        "optionally category-brief-2026.md.",
    )
    para(
        doc,
        "**Example: how you check what Claude produced.** After "
        "running the full chain, type:",
    )
    code_block(doc, "ls outputs")
    para(
        doc,
        "You should see five or six files. Open any one in your "
        "text editor to read the content Claude generated.",
    )

    # solutions/
    heading(doc, "solutions/", 3)
    para(
        doc,
        "Five reference SKILL.md files (one per skill). These "
        "are the \"answer key\". Look at them only after you have "
        "made your own attempt. They are useful for comparing "
        "your process steps, your scoring bands, and your quality "
        "criteria against a working reference.",
    )
    para(
        doc,
        "**Example.** In Lesson 1, you copy the rfp-builder "
        "solution into your skills folder to see a skill run "
        "before you write one yourself. After Lesson 3, you "
        "compare your own rfp-builder against the solution to "
        "check if you missed a process step.",
    )

    # scripts/
    heading(doc, "scripts/build_course_data.py", 3)
    para(
        doc,
        "A Python script that regenerates all practice data "
        "deterministically (it uses a fixed random seed). If you "
        "accidentally delete or corrupt a file during practice, "
        "run this script once and every CSV, every bid response, "
        "and every template is restored exactly as it was.",
    )
    para(doc, "**Example: how to restore the data.** In your terminal, type:")
    code_block(doc, "python scripts/build_course_data.py")
    para(
        doc,
        "All files in inputs/, bid-responses/, and templates/ "
        "are regenerated. Your skills/ and outputs/ folders are "
        "not touched.",
    )

    # ===================================================================
    # 4. What the course saves you per sourcing event
    # ===================================================================
    heading(doc, "4. What the course saves you per sourcing event", 1)
    para(
        doc,
        "The table below compares each sourcing event task without "
        "skills (manual work) and with your skill library (Claude "
        "Code running the skill). These are realistic estimates "
        "based on a six-bidder logistics event.",
    )
    fill_table(
        doc,
        ["Task per sourcing event", "Without skills", "With your skill library"],
        [
            (
                "Build the RFP package",
                "5 to 10 days of writing",
                "60 seconds: rfp-builder runs against the brief and longlist",
            ),
            (
                "Score 6 bids consistently",
                "1 to 2 days of reading and Excel work",
                "90 seconds: bid-scorer applies fixed weights to all bids",
            ),
            (
                "Build the supplier risk profile",
                "Half a day of analyst time",
                "60 seconds: risk-profiler runs against the longlist and bids",
            ),
            (
                "Compute the savings case",
                "Half a day in Excel against historical spend",
                "60 seconds: savings-calculator sums baseline and proposed spend",
            ),
            (
                "Write the award memo",
                "Half a day of synthesis",
                "60 seconds: award-memo reads the four other outputs",
            ),
            (
                "Run the next event",
                "Repeat all the above. 2 to 3 weeks.",
                "Configure new inputs, run the chain. 7 minutes.",
            ),
        ],
    )
    para(
        doc,
        "**Example: what \"configure new inputs\" means.** For "
        "the next sourcing event, you replace the files in inputs/ "
        "with your new category brief and new supplier longlist, "
        "drop the new bid responses into bid-responses/, and run "
        "the same chain prompt. The skills do not change. The "
        "inputs change.",
    )

    # ===================================================================
    # 5. What a SKILL.md actually is  (REVISED)
    # ===================================================================
    heading(doc, "5. What a SKILL.md actually is", 1)

    para(
        doc,
        "A SKILL.md is a 40- to 90-line markdown file with five "
        "sections. It captures a methodology, not a one-off "
        "request. Think of it as a recipe: the recipe works "
        "regardless of whether you are making the dish for four "
        "guests or forty. The inputs change; the method stays "
        "the same.",
    )

    # The five sections table
    heading(doc, "The five sections every skill has", 2)
    fill_table(
        doc,
        ["Section", "What goes in it", "Example from rfp-builder"],
        [
            (
                "What this skill does",
                "One paragraph. Use case, audience, when to invoke.",
                "\"Builds an RFP package for a sourcing event. Use once at "
                "the start of the event, after the category brief is "
                "approved and the supplier longlist is finalised.\"",
            ),
            (
                "Inputs",
                "The shape of every input: path, column headers "
                "(CSV), or section structure (markdown). Not "
                "specific values.",
                "\"inputs/category-brief.md: a markdown brief with "
                "sections Today, Current state, Goal, Scope, "
                "Stakeholders.\"",
            ),
            (
                "Process",
                "Six to twelve numbered steps in plain English. "
                "No code. Names input shapes, not specific "
                "suppliers.",
                "\"Step 1: Read the category brief. Extract today's "
                "date, the savings target, the close date, the "
                "in-scope modes, the panel ambition.\"",
            ),
            (
                "Output format",
                "The path, structure, and length of the file the "
                "skill produces.",
                "\"Save outputs/rfp-package.md. Six top-level "
                "sections matching templates/rfp-template.md. "
                "4 to 6 pages.\"",
            ),
            (
                "Quality criteria",
                "Three to five checks the skill (or you) can run "
                "on the output.",
                "\"Every figure cited has a source named in "
                "inputs/category-brief.md or "
                "inputs/supplier-longlist.csv.\"",
            ),
        ],
    )

    # Real extract
    heading(doc, "A real SKILL.md extract: the first 20 lines of rfp-builder", 2)
    para(
        doc,
        "Below is a shortened extract from the reference "
        "rfp-builder skill, exactly as it appears in the "
        "solutions folder. This is what 20 lines of a skill "
        "look like.",
    )
    code_block(
        doc,
        "<!-- v1.0 2026-04-25 Initial. -->\n\n"
        "# rfp-builder\n\n"
        "## What this skill does\n\n"
        "Builds an RFP package for a sourcing event. Use this\n"
        "skill once at the start of the event, after the category\n"
        "brief is approved and the supplier longlist is finalised.\n\n"
        "## Inputs\n\n"
        "inputs/category-brief.md\n"
        "  A markdown brief with sections: Today, Current state,\n"
        "  Goal, Scope, Stakeholders. Today's date drives the\n"
        "  timeline. The Goal section drives the executive overview.\n\n"
        "inputs/supplier-longlist.csv\n"
        "  Columns: carrier_id, carrier_name, modes,\n"
        "  primary_geography, certifications, capacity_tier,\n"
        "  financial_health, otd_pct_12m ...",
    )
    para(
        doc,
        "The full skill is about 65 lines. You write it in "
        "Lesson 3. The extract above shows the pattern: plain "
        "English, no code, no specific supplier names or spend "
        "figures baked in.",
    )

    # Prompt vs. Skill comparison
    heading(doc, "A skill versus a prompt: the same task, two approaches", 2)
    para(
        doc,
        "This comparison shows why a skill is reusable and a "
        "prompt is not.",
    )
    para(doc, "**Approach A: a one-off prompt (works once).**")
    code_block(
        doc,
        "Write me an RFP for the logistics consolidation.\n"
        "Annual spend 11.2m USD. Close date 2026-06-15.\n"
        "Award by 2026-06-30. Savings target 1.6m USD.\n"
        "14 incumbents down to 4. Evaluation weights:\n"
        "Price 40%, Service 25%, Capability 20%,\n"
        "Sustainability 10%, Implementation 5%.",
    )
    para(
        doc,
        "This prompt produces an RFP. But it names Acme's "
        "specific values: 11.2m, 2026-06-15, 14 incumbents. "
        "When the next sourcing event arrives with different "
        "values, you write a new prompt from scratch.",
    )
    para(doc, "**Approach B: a skill (works every time).**")
    code_block(
        doc,
        "Use the rfp-builder skill in skills/rfp-builder.md.\n"
        "Inputs are in inputs/. Templates in templates/.\n"
        "Save the output to outputs/rfp-package.md.",
    )
    para(
        doc,
        "This prompt does not name any values. The values "
        "live in the input files (category-brief.md, "
        "supplier-longlist.csv). The methodology lives in the "
        "skill file. Change the inputs, get a different RFP. "
        "Change the skill, change the methodology for every "
        "future RFP. The prompt stays the same.",
    )

    # How Claude Code uses a skill
    heading(doc, "What happens when Claude Code reads a skill", 2)
    para(
        doc,
        "When you type the prompt above and press Enter, here "
        "is exactly what happens inside Claude Code (in the "
        "terminal):",
    )
    numbered(
        doc,
        "Claude Code loads the practice/CLAUDE.md file "
        "automatically (this happened when you started "
        "the session with `claude`).",
    )
    numbered(
        doc,
        "Claude Code reads your prompt. It sees \"Use the "
        "rfp-builder skill in skills/rfp-builder.md.\"",
    )
    numbered(
        doc,
        "Claude Code opens skills/rfp-builder.md and reads "
        "all five sections.",
    )
    numbered(
        doc,
        "The Inputs section tells Claude which files to open: "
        "inputs/category-brief.md, inputs/supplier-longlist.csv, "
        "templates/rfp-template.md. Claude opens each one.",
    )
    numbered(
        doc,
        "The Process section tells Claude the nine steps to "
        "follow. Claude follows them in order: extract the "
        "savings target, group carriers by mode, write each "
        "RFP section.",
    )
    numbered(
        doc,
        "The Output format section tells Claude where to save "
        "the file, how long it should be, and what writing "
        "rules to follow. Claude writes outputs/rfp-package.md.",
    )
    numbered(
        doc,
        "The Quality criteria section gives Claude five checks "
        "to verify against the output. If any check fails, "
        "Claude flags it.",
    )
    para(
        doc,
        "You see a progress message in the terminal, then a "
        "confirmation that the file was saved. The whole "
        "process takes 60 to 90 seconds.",
    )

    # ===================================================================
    # 6. Worked examples  (REVISED with two full examples)
    # ===================================================================
    heading(doc, "6. Worked examples", 1)
    para(
        doc,
        "Two complete worked examples follow. The first shows a "
        "single skill (bid-scorer) in detail. The second shows "
        "the full five-skill chain end to end.",
    )

    # --- Example A: bid-scorer ---
    heading(doc, "Example A: scoring six bids with the bid-scorer skill", 2)
    para(
        doc,
        "You are a sourcing lead at Acme Plc. Six carriers have "
        "submitted bid responses for your logistics consolidation "
        "RFP. You need a comparison table with weighted scores so "
        "you can present a shortlist to the panel. Doing this by "
        "hand in Excel took you a day and a half on the last "
        "sourcing event.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "practice/\n"
        "+- CLAUDE.md                       (project context, loaded automatically)\n"
        "+- skills/bid-scorer.md            (your skill, 80 lines)\n"
        "+- bid-responses/                  (6 bid response files)\n"
        "|  +- BID_CAR001_FastRoad_UK.pdf\n"
        "|  +- BID_CAR003_OceanLine.pdf\n"
        "|  +- BID_CAR008_Pacific_Forwarders.pdf\n"
        "|  +- BID_CAR010_Globex_Freight.pdf\n"
        "|  +- BID_CAR012_Helios_Air_Freight.pdf\n"
        "|  +- BID_CAR017_Continental_Roads.pdf\n"
        "+- inputs/supplier-longlist.csv    (25 carriers, capability data)\n"
        "+- templates/scorecard-template.md\n"
        "+- outputs/bid-comparison.md       (the output Claude produces)",
    )
    para(
        doc,
        "**Step 1. Start Claude Code in the practice folder.** "
        "Open your terminal and type:",
    )
    code_block(doc, 'cd "Course_03_The_Skill_Builder/practice"\nclaude')
    para(doc, "Wait for the Claude Code prompt (a blinking cursor next to >).")

    para(doc, "**Step 2. Type the prompt.**")
    code_block(
        doc,
        "Use the bid-scorer skill in skills/bid-scorer.md.\n"
        "Process every file in bid-responses/.\n"
        "Use inputs/supplier-longlist.csv for capacity_tier,\n"
        "financial_health, and incumbent lookups.\n"
        "Save the output to outputs/bid-comparison.md.",
    )
    para(doc, "Press Enter.")

    para(
        doc,
        "**What you should see (after 90 to 120 seconds).** "
        "Claude confirms it saved outputs/bid-comparison.md. "
        "Open the file. It has three sections:",
    )
    bullet(
        doc,
        "A **comparison table** with eight columns and six rows, "
        "sorted by Total descending. Continental Roads leads "
        "on Price (98). FastRoad UK leads on Capability (94). "
        "Helios Air Freight leads on Service (97).",
    )
    bullet(
        doc,
        "**One paragraph of commentary per bidder.** Each "
        "paragraph names that bidder's strongest score, "
        "weakest score, and the key trade-off.",
    )
    bullet(
        doc,
        "A **top-three summary** with three bullet points "
        "naming the recommended carriers.",
    )
    bullet(
        doc,
        "An **audit footer** listing the source files used, "
        "the date, and the model.",
    )

    para(doc, "**What Claude did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the global CLAUDE.md from practice/ and read "
        "the bid-scorer skill from skills/.",
    )
    numbered(doc, "Listed every file in bid-responses/. Counted six.")
    numbered(
        doc,
        "For each bid, read the executive summary, capability "
        "statement, pricing table, and service commitments.",
    )
    numbered(
        doc,
        "Looked up each carrier_id in supplier-longlist.csv to "
        "pull capacity_tier, financial_health, and incumbent flag.",
    )
    numbered(
        doc,
        "Scored each bid on Price (40%), Service (25%), "
        "Capability (20%), Sustainability (10%), Implementation "
        "(5%) using the numeric bands the skill specified. "
        "Example: a bidder with the lowest total annual value "
        "gets Price = 100; the highest gets Price = 60; others "
        "are interpolated linearly.",
    )
    numbered(
        doc,
        "Computed the weighted total to one decimal place. "
        "Sorted descending. Marked the top three Recommended = "
        "\"Yes\".",
    )
    numbered(
        doc,
        "Wrote the table, the per-bidder commentary, and the "
        "top-three summary. Added the audit footer listing all "
        "source files.",
    )

    # --- Example B: the full chain ---
    heading(
        doc,
        "Example B: the full chain (five skills, six deliverables, one session)",
        2,
    )
    para(
        doc,
        "It is Wednesday afternoon. You have written all five "
        "skills. You want to produce the complete sourcing event "
        "package in one session so you can walk into the panel "
        "meeting tomorrow morning with everything ready.",
    )
    para(doc, "**Folder layout.**")
    code_block(
        doc,
        "practice/\n"
        "+- CLAUDE.md\n"
        "+- skills/                   (5 skill files)\n"
        "|  +- rfp-builder.md\n"
        "|  +- bid-scorer.md\n"
        "|  +- risk-profiler.md\n"
        "|  +- savings-calculator.md\n"
        "|  +- award-memo.md\n"
        "+- inputs/                   (category brief, longlist, baseline)\n"
        "+- bid-responses/            (6 bid files)\n"
        "+- templates/                (3 skeleton templates)\n"
        "+- outputs/                  (starts empty, ends with 6 files)",
    )

    para(doc, "**Step 1. Start Claude Code.**")
    code_block(doc, 'cd "Course_03_The_Skill_Builder/practice"\nclaude')

    para(doc, "**Step 2. Type the chain prompt.**")
    code_block(
        doc,
        "Run these five skills in order. After each step, confirm\n"
        "the output file exists before moving to the next.\n\n"
        "Step 1: Use skills/rfp-builder.md.\n"
        "  Inputs in inputs/ and templates/.\n"
        "  Save to outputs/rfp-package.md.\n"
        "Step 2: Use skills/bid-scorer.md.\n"
        "  Process bid-responses/. Lookups from inputs/supplier-longlist.csv.\n"
        "  Save to outputs/bid-comparison.md.\n"
        "Step 3: Use skills/risk-profiler.md.\n"
        "  Read bid-responses/ and inputs/supplier-longlist.csv.\n"
        "  Save to outputs/risk-profile.md.\n"
        "Step 4: Use skills/savings-calculator.md.\n"
        "  Read inputs/spend-baseline.csv and outputs/bid-comparison.md.\n"
        "  Save to outputs/savings-case.md.\n"
        "Step 5: Use skills/award-memo.md.\n"
        "  Read outputs/bid-comparison.md, outputs/risk-profile.md,\n"
        "  outputs/savings-case.md, and inputs/category-brief.md.\n"
        "  Save to outputs/award-memo.md.",
    )
    para(doc, "Press Enter. Wait about 7 minutes for all five steps.")

    para(doc, "**What you should see after each step.**")
    numbered(
        doc,
        "**rfp-builder completes** (about 90 seconds). Claude "
        "confirms outputs/rfp-package.md saved. The executive "
        "overview names the 1.6m USD savings target.",
    )
    numbered(
        doc,
        "**bid-scorer completes** (about 90 seconds). Claude "
        "confirms outputs/bid-comparison.md saved. The table "
        "ranks six bidders with weighted totals.",
    )
    numbered(
        doc,
        "**risk-profiler completes** (about 60 seconds). Claude "
        "confirms outputs/risk-profile.md saved. Six paragraphs, "
        "one per bidder, each naming the highest risk and a "
        "specific mitigation.",
    )
    numbered(
        doc,
        "**savings-calculator completes** (about 60 seconds). "
        "Claude confirms outputs/savings-case.md saved. Headline: "
        "Baseline 10.86m, Proposed 9.31m, Savings 1.55m (14.3%).",
    )
    numbered(
        doc,
        "**award-memo completes** (about 60 seconds). Claude "
        "confirms outputs/award-memo.md saved. The memo "
        "recommends a four-carrier panel and quotes the savings "
        "figure from savings-case.md.",
    )

    para(doc, "**Step 3. Check the outputs folder.**")
    code_block(doc, "/quit\nls outputs")
    para(
        doc,
        "You should see five files: rfp-package.md, "
        "bid-comparison.md, risk-profile.md, savings-case.md, "
        "award-memo.md. Open award-memo.md. The recommendation "
        "opens with the four-carrier panel, names each carrier's "
        "contract value, lists three risks with mitigation "
        "owners, and quotes the 1.55m USD savings figure.",
    )

    para(doc, "**What Claude did, behind the scenes (full chain).**")
    numbered(
        doc,
        "Step 1 (rfp-builder): read the brief and longlist, "
        "grouped carriers by mode, wrote the six-section RFP "
        "package to outputs/.",
    )
    numbered(
        doc,
        "Step 2 (bid-scorer): listed six bid files, scored each "
        "on five criteria using numeric bands, computed weighted "
        "totals, wrote the comparison table and commentary.",
    )
    numbered(
        doc,
        "Step 3 (risk-profiler): read each bid's contract terms "
        "and looked up financial_health and capacity_tier from "
        "the longlist. Scored three risk dimensions (1 to 5 each). "
        "Wrote one paragraph per bidder.",
    )
    numbered(
        doc,
        "Step 4 (savings-calculator): summed 1,487 shipment rows "
        "from spend-baseline.csv (baseline: 10.86m USD). Read "
        "bid-comparison.md for proposed annual values. Computed "
        "savings of 1.55m USD (14.3%). Subtracted 42,000 USD "
        "implementation for Year 1 risk-adjusted figure.",
    )
    numbered(
        doc,
        "Step 5 (award-memo): read all four prior outputs plus "
        "the brief. Drafted the four-carrier panel recommendation. "
        "Quoted the savings figure verbatim from savings-case.md "
        "(did not recompute). Named three risks with mitigation "
        "owners from risk-profile.md.",
    )
    numbered(
        doc,
        "Each step ran the skill's own quality criteria after "
        "writing the output. If any criterion failed, Claude "
        "flagged it before moving to the next step.",
    )

    # ===================================================================
    # 7. A day in the life: Anwar, Strategic Sourcing Lead
    # ===================================================================
    heading(doc, "7. A day in the life: Anwar, Strategic Sourcing Lead", 1)

    # --- Explanation of what this section is and why it matters ---
    para(
        doc,
        "This is the most important section of the handout. It "
        "shows you, step by step, how a real procurement analyst "
        "uses SKILL.md files across a full working day. Each "
        "scenario is something you will recognise from your own "
        "week: a CPO asking for a deliverable at short notice, "
        "new bids landing that need scoring, a policy change from "
        "Finance, a colleague who needs onboarding, a supplier "
        "meeting that needs preparation.",
    )
    para(
        doc,
        "For every scenario, you will see four things:",
    )
    numbered(
        doc,
        "**The situation.** What happened and what Anwar needs "
        "to produce.",
    )
    numbered(
        doc,
        "**The exact commands.** What Anwar types in the terminal, "
        "copied word for word, so you can do the same thing.",
    )
    numbered(
        doc,
        "**What Claude produced.** The output Anwar sees and what "
        "he checks before sending it on.",
    )
    numbered(
        doc,
        "**What Claude did, behind the scenes.** A numbered list "
        "of the steps Claude followed inside the skill, so you "
        "understand why the output looks the way it does.",
    )
    para(
        doc,
        "By the end of this section you will have seen the five "
        "skills applied to five different procurement problems "
        "across three sourcing events. You will understand when "
        "to run the full chain, when to run a single skill, "
        "when to update a skill, and how to hand a skill library "
        "to a colleague.",
    )

    # --- Meet Anwar ---
    heading(doc, "Meet Anwar", 2)
    para(
        doc,
        "Anwar is a Strategic Sourcing Lead at a US manufacturer. "
        "He manages three active sourcing events (logistics "
        "consolidation, packaging materials, IT hardware). He "
        "reports to a CPO who wants numbers by Friday. He sits "
        "in a team of four analysts who share a OneDrive folder.",
    )
    para(
        doc,
        "Three weeks ago, Anwar built his skill library: five "
        "SKILL.md files (rfp-builder, bid-scorer, risk-profiler, "
        "savings-calculator, award-memo). Each file is 40 to 80 "
        "lines of plain English. They live in a skills/ folder "
        "inside each sourcing project.",
    )
    para(
        doc,
        "This is a typical Thursday. Five procurement problems "
        "land on his desk. Watch how he handles each one.",
    )

    # --- 08:15 ---
    heading(doc, "08:15. The CPO Slack: \"Where are we on logistics?\"", 2)
    para(
        doc,
        "Anwar opens his laptop. The first message is from his "
        "CPO: \"Board meeting moved to Monday. I need the "
        "logistics award recommendation by end of Friday. Where "
        "are we?\"",
    )
    para(
        doc,
        "Three weeks ago this message would have started a "
        "two-day scramble: re-reading six bid responses, "
        "rebuilding the scorecard in Excel, writing the award "
        "memo from scratch. Today Anwar opens his terminal and "
        "navigates to the logistics sourcing folder:",
    )
    code_block(
        doc,
        "cd logistics-consolidation-2026\nclaude",
    )
    para(
        doc,
        "He already has his five skills in the skills/ folder "
        "and the six bid responses in bid-responses/. He runs "
        "the full chain:",
    )
    code_block(
        doc,
        "Run these five skills in order. After each step, confirm\n"
        "the output file exists before moving to the next.\n\n"
        "Step 1: Use skills/rfp-builder.md. Save to outputs/rfp-package.md.\n"
        "Step 2: Use skills/bid-scorer.md. Save to outputs/bid-comparison.md.\n"
        "Step 3: Use skills/risk-profiler.md. Save to outputs/risk-profile.md.\n"
        "Step 4: Use skills/savings-calculator.md. Save to outputs/savings-case.md.\n"
        "Step 5: Use skills/award-memo.md. Save to outputs/award-memo.md.",
    )
    para(
        doc,
        "Seven minutes later, five files sit in outputs/. Anwar "
        "opens outputs/award-memo.md. The recommendation names "
        "a four-carrier panel: Continental Roads (road FTL, "
        "3.2m USD), FastRoad UK (road LTL, 2.8m USD), OceanLine "
        "(sea FCL, 2.1m USD), Helios Air Freight (air, 1.2m "
        "USD). Savings: 1.55m USD (14.3% of baseline). He reads "
        "the three risks and their mitigations. Everything traces "
        "back to the bid data. He replies to the CPO: \"Draft "
        "award memo ready. Sending for your review by 09:00.\"",
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(
        doc,
        "Ran rfp-builder: read the category brief and longlist, "
        "produced the six-section RFP package.",
    )
    numbered(
        doc,
        "Ran bid-scorer: scored all six bids on five weighted "
        "criteria, produced the comparison table.",
    )
    numbered(
        doc,
        "Ran risk-profiler: scored financial, operational, and "
        "commercial risk per bidder.",
    )
    numbered(
        doc,
        "Ran savings-calculator: summed 1,487 shipments for "
        "baseline (10.86m USD), computed savings against "
        "proposed panel spend.",
    )
    numbered(
        doc,
        "Ran award-memo: read all four prior outputs, drafted "
        "the recommendation, quoted the savings figure verbatim "
        "from savings-case.md.",
    )
    para(
        doc,
        "**Time spent:** 7 minutes of Claude running plus 15 "
        "minutes of Anwar reviewing. Total: 22 minutes. "
        "Previous method: 2 days.",
    )
    para(
        doc,
        "**What to learn from this.** The full chain prompt is "
        "the most powerful pattern in the skill library. You type "
        "one prompt, name the five skills in order, and Claude "
        "runs each one using the previous step's output as "
        "input. You do not need to copy-paste between files or "
        "re-type any data. The chain is the sourcing event.",
    )

    # --- 09:30 ---
    heading(doc, "09:30. Six new bids land for the packaging RFP", 2)
    para(
        doc,
        "Anwar's second active event is a packaging materials "
        "RFP. The bid deadline was yesterday. Six suppliers have "
        "emailed their responses as PDF attachments. His analyst, "
        "Priya, has saved them into the packaging-rfp/"
        "bid-responses/ folder.",
    )
    para(
        doc,
        "Anwar does not need to write a new scoring methodology. "
        "He copies his bid-scorer skill into the packaging "
        "project:",
    )
    code_block(
        doc,
        "cd ../packaging-rfp-2026\n"
        "cp ../logistics-consolidation-2026/skills/bid-scorer.md skills/\nclaude",
    )
    para(doc, "He types:")
    code_block(
        doc,
        "Use the bid-scorer skill in skills/bid-scorer.md.\n"
        "Process every file in bid-responses/.\n"
        "Use inputs/supplier-longlist.csv for lookups.\n"
        "Save to outputs/bid-comparison.md.",
    )
    para(
        doc,
        "Ninety seconds later, the comparison table is ready. "
        "The same scoring methodology, applied to completely "
        "different suppliers and a different category. Anwar "
        "did not rewrite a single line of the skill. He changed "
        "the inputs.",
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the bid-scorer skill (identical to the logistics "
        "version).",
    )
    numbered(
        doc,
        "Read six new bid files from bid-responses/. Different "
        "suppliers, different pricing structures, different "
        "modes.",
    )
    numbered(
        doc,
        "Looked up each supplier_id in the packaging project's "
        "supplier-longlist.csv (not the logistics one).",
    )
    numbered(
        doc,
        "Applied the same scoring bands. Produced a ranked "
        "comparison table with commentary per bidder.",
    )
    para(
        doc,
        "**Time spent:** 90 seconds of Claude plus 10 minutes "
        "of Anwar reviewing. Previous method: a full day in "
        "Excel.",
    )
    para(
        doc,
        "**What to learn from this.** A skill works across "
        "categories because it names input shapes, not specific "
        "values. The bid-scorer says \"read every file in "
        "bid-responses/\" and \"look up the carrier_id in "
        "supplier-longlist.csv\". It does not say \"read "
        "FastRoad UK\" or \"look up CAR001\". That is why the "
        "same skill scores logistics bids and packaging bids "
        "without a single edit.",
    )

    # --- 11:00 ---
    heading(doc, "11:00. The CFO changes the savings rules", 2)
    para(
        doc,
        "An email from Finance: \"Effective immediately, all "
        "savings reports must separate hard savings from soft "
        "savings. Soft savings (avoided cost, productivity "
        "gains, rebate projections) must not appear in the "
        "headline figure.\"",
    )
    para(
        doc,
        "Anwar opens his savings-calculator skill in a text "
        "editor. He updates the version comment at the top:",
    )
    code_block(
        doc,
        "<!-- v1.1 2026-04-25 Tightened soft-savings rule per\n"
        "     CFO directive. Soft savings now in supplemental\n"
        "     section, not headline. -->",
    )
    para(
        doc,
        "He adds one new process step (3a): \"Soft savings "
        "MUST NOT appear in the headline savings figure. Soft "
        "savings appear only in a separate Soft savings, "
        "supplemental paragraph at the bottom.\" He adds a "
        "quality criterion: \"Soft savings, if any, appear "
        "ONLY in the supplemental paragraph, never in the "
        "headline.\" Total edit: 4 lines changed in a 50-line "
        "file.",
    )
    para(
        doc,
        "He re-runs only the two affected skills on the "
        "logistics event:",
    )
    code_block(
        doc,
        "cd ../logistics-consolidation-2026\nclaude\n\n"
        "Use skills/savings-calculator.md. Save to outputs/savings-case.md.\n"
        "Then use skills/award-memo.md. Save to outputs/award-memo.md.",
    )
    para(
        doc,
        "The updated savings case shows hard savings only in "
        "the headline (1.55m USD). Soft savings appear in a "
        "separate paragraph at the bottom. The award memo "
        "quotes the new headline. The rfp-builder, bid-scorer, "
        "and risk-profiler outputs are untouched.",
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the v1.1 savings-calculator. Applied the new "
        "soft-savings separation rule.",
    )
    numbered(
        doc,
        "Re-ran award-memo, which quoted the updated headline "
        "(hard savings only).",
    )
    numbered(
        doc,
        "Did not re-run the other three skills. They are "
        "unaffected by the rule change.",
    )
    para(
        doc,
        "**Time spent:** 5 minutes editing the skill, 2 "
        "minutes re-running. The same change applies "
        "automatically to every future sourcing event that "
        "uses this skill.",
    )
    para(
        doc,
        "**What to learn from this.** When a business rule "
        "changes, you update the skill file, not every "
        "document the skill has ever produced. The version "
        "comment at the top of the file records what changed "
        "and why. You only re-run the skills that are affected "
        "by the change. Skills that sit upstream (rfp-builder, "
        "bid-scorer, risk-profiler) are untouched because the "
        "savings rule does not affect them.",
    )

    # --- 13:30 ---
    heading(
        doc,
        "13:30. A colleague needs help with a new category",
        2,
    )
    para(
        doc,
        "Priya, one of Anwar's analysts, is starting a "
        "sourcing event for IT hardware. She has never used "
        "skills before. Anwar copies the five skill files "
        "into her project folder and walks her through the "
        "first run:",
    )
    code_block(
        doc,
        "cd priya-it-hardware-2026\nclaude\n\n"
        "Use the rfp-builder skill in skills/rfp-builder.md.\n"
        "Inputs in inputs/. Templates in templates/.\n"
        "Save to outputs/rfp-package.md.",
    )
    para(
        doc,
        "Priya watches Claude produce a populated RFP package "
        "for IT hardware in 60 seconds. The executive overview "
        "names her savings target (480,000 USD), her close date "
        "(2026-07-31), and her evaluation weights. She did not "
        "edit the skill. She only replaced the input files with "
        "her own category brief and supplier longlist.",
    )
    para(
        doc,
        "Anwar shows her how to check the output against the "
        "quality criteria in the skill file. Four of five pass. "
        "The supplier response template is missing a field "
        "specific to IT hardware (warranty terms). Priya adds "
        "one line to the rfp-builder Process section: \"Include "
        "warranty terms in the supplier response template.\" "
        "She re-runs. All five pass.",
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the same rfp-builder skill Anwar wrote for "
        "logistics.",
    )
    numbered(
        doc,
        "Read Priya's category brief (different category, "
        "different numbers, different stakeholders).",
    )
    numbered(
        doc,
        "Read Priya's supplier longlist (IT hardware vendors, "
        "not carriers).",
    )
    numbered(
        doc,
        "Produced an IT hardware RFP package using the same "
        "six-section structure. The skill is category-agnostic "
        "because it names input shapes, not specific values.",
    )
    para(
        doc,
        "**Time spent:** 15 minutes, including Priya's first "
        "edit to the skill. She now owns a working skill "
        "library for her event.",
    )
    para(
        doc,
        "**What to learn from this.** Onboarding a colleague "
        "is a copy-paste operation: copy the skills folder, "
        "replace the input files, run the prompt. If a skill "
        "needs a category-specific tweak (warranty terms for "
        "IT hardware), the colleague adds one line to the "
        "Process section and re-runs. The skill library is a "
        "team asset, not personal knowledge locked in one "
        "analyst's head.",
    )

    # --- 15:00 ---
    heading(doc, "15:00. Quick risk check before a supplier meeting", 2)
    para(
        doc,
        "Anwar has a 16:00 call with Pacific Forwarders, one "
        "of the logistics bidders. He wants a quick risk "
        "summary before the call. He does not need the full "
        "chain. He runs one skill:",
    )
    code_block(
        doc,
        "cd ../logistics-consolidation-2026\nclaude\n\n"
        "Use the risk-profiler skill in skills/risk-profiler.md.\n"
        "Read bid-responses/BID_CAR008_Pacific_Forwarders.pdf\n"
        "and inputs/supplier-longlist.csv.\n"
        "Print the result to chat. Do not save a file.",
    )
    para(
        doc,
        "Claude prints a single paragraph: \"Pacific Forwarders. "
        "Total risk: 9/15. Key risk: financial (4/5). Financial "
        "health is rated weak in the longlist. Mitigation: "
        "require a parent company guarantee and quarterly "
        "financial reporting as a contract condition.\" Anwar "
        "copies this into his meeting notes. The call prep took "
        "60 seconds.",
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(
        doc,
        "Loaded the risk-profiler skill.",
    )
    numbered(
        doc,
        "Read only the Pacific Forwarders bid (not all six).",
    )
    numbered(
        doc,
        "Looked up CAR008 in supplier-longlist.csv: "
        "financial_health = weak, capacity_tier = tier_2, "
        "incumbent = no.",
    )
    numbered(
        doc,
        "Scored three risk dimensions and produced one "
        "paragraph with a specific mitigation.",
    )
    para(
        doc,
        "**What to learn from this.** You do not always need "
        "the full chain. A single skill works on its own. "
        "Anwar pointed the risk-profiler at one bid file "
        "instead of all six. He told Claude to print to chat "
        "instead of saving a file. Skills are flexible: you "
        "can run them individually, change the scope, and "
        "choose whether the output goes to a file or to "
        "the screen.",
    )

    # --- 16:45 ---
    heading(doc, "16:45. End of day: update the team changelog", 2)
    para(
        doc,
        "Before logging off, Anwar opens skills/README.md and "
        "adds today's changelog entry:",
    )
    code_block(
        doc,
        "## Changelog\n"
        "v1.1 2026-04-25  savings-calculator: separated hard and\n"
        "                  soft savings per CFO directive.\n"
        "v1.0 2026-04-07  Initial library: rfp-builder, bid-scorer,\n"
        "                  risk-profiler, savings-calculator, award-memo.",
    )
    para(
        doc,
        "He commits the updated skill to the team's shared "
        "folder. Tomorrow, every analyst who runs the "
        "savings-calculator skill will automatically use the "
        "new soft-savings rule. No retraining. No email "
        "explaining the change. The skill file is the single "
        "source of truth.",
    )

    # --- Summary ---
    heading(doc, "Anwar's day: the numbers", 2)
    fill_table(
        doc,
        ["Task", "Time with skills", "Time without skills"],
        [
            (
                "Full award package for logistics",
                "22 minutes",
                "2 days",
            ),
            (
                "Score 6 packaging bids",
                "12 minutes",
                "1 day",
            ),
            (
                "Update savings rule across all events",
                "7 minutes",
                "Half a day per event",
            ),
            (
                "Onboard Priya on IT hardware RFP",
                "15 minutes",
                "2 days of shadowing",
            ),
            (
                "Risk prep for supplier call",
                "60 seconds",
                "30 minutes reading the bid file",
            ),
        ],
    )
    para(
        doc,
        "Anwar handled five distinct procurement tasks across "
        "three sourcing events in a single working day. The "
        "skill library did the repetitive analytical work. "
        "Anwar directed the work, reviewed the outputs, and "
        "made the decisions.",
    )

    # ===================================================================
    # 8. The 20-minute sprint
    # ===================================================================
    heading(doc, "8. The 20-minute sprint: a quick taste", 1)
    para(
        doc,
        "If you have only 20 minutes, do this. You will not "
        "finish Course 3 but you will see one skill produce one "
        "real deliverable on real procurement data.",
    )

    heading(doc, "Minutes 0 to 5: open the practice folder", 2)
    numbered(doc, "Open your terminal.")
    numbered(doc, "Type:")
    code_block(doc, 'cd "Course_03_The_Skill_Builder/practice"\nls')
    numbered(
        doc,
        "You should see CLAUDE.md, bid-responses/, inputs/, "
        "outputs/, skills/, templates/. Open any folder briefly "
        "to see what is inside.",
    )

    heading(doc, "Minutes 5 to 10: copy the rfp-builder solution", 2)
    numbered(doc, "Copy the reference skill into your practice folder:")
    code_block(
        doc, "cp ../solutions/rfp_builder_solution.md skills/rfp-builder.md"
    )
    numbered(
        doc,
        "Open skills/rfp-builder.md in your text editor and "
        "read it. About 65 lines, five sections. Notice that it "
        "names no specific supplier or spend figure. It names "
        "input shapes: \"a markdown brief with sections Today, "
        "Current state, Goal, Scope, Stakeholders.\"",
    )

    heading(doc, "Minutes 10 to 15: run the skill", 2)
    numbered(doc, "Start Claude Code:")
    code_block(doc, "claude")
    numbered(doc, "Type this prompt:")
    code_block(
        doc,
        "Use the rfp-builder skill in skills/rfp-builder.md.\n"
        "Inputs in inputs/. Templates in templates/.\n"
        "Save to outputs/rfp-package.md.",
    )
    numbered(doc, "Wait 60 to 90 seconds. Claude confirms the file is saved.")

    heading(doc, "Minutes 15 to 20: read the result", 2)
    numbered(doc, "Quit Claude:")
    code_block(doc, "/quit")
    numbered(
        doc,
        "Open outputs/rfp-package.md. Read the executive "
        "overview. It should name the 1.6m USD savings target, "
        "the 2026-06-15 close date, and the 40/25/20/10/5 "
        "evaluation weights.",
    )
    numbered(
        doc,
        "Read Section 5 (Supplier response template). It should "
        "list the same fields the bidders responded against in "
        "bid-responses/.",
    )
    numbered(
        doc,
        "Compare the RFP against inputs/category-brief.md. "
        "Every figure in the RFP should trace back to the brief "
        "or the longlist.",
    )

    para(
        doc,
        "After this sprint you have proven a SKILL.md works on "
        "real procurement data. You wrote nothing. You configured "
        "one prompt. Claude followed the methodology. Lessons 2 "
        "to 5 teach you to write your own skills.",
    )

    # ===================================================================
    # 9. First week with skills in your real work
    # ===================================================================
    heading(doc, "9. Your first week with skills in your real work", 1)
    para(
        doc,
        "After finishing Course 3, use this five-day plan to "
        "move skills into your real procurement work.",
    )

    heading(doc, "Day 1 (Monday): copy your first real skill", 2)
    bullet(doc, "**Goal:** rfp-builder running on your real next sourcing event.")
    bullet(
        doc,
        "**Tasks:** Copy your practice rfp-builder.md into your "
        "real procurement folder's skills/ directory. Replace the "
        "files in inputs/ with your real category brief and your "
        "real supplier longlist. Run the same prompt you used in "
        "Course 3.",
    )
    bullet(
        doc,
        "**Example prompt for your real folder:**",
    )
    code_block(
        doc,
        "Use the rfp-builder skill in skills/rfp-builder.md.\n"
        "Inputs in inputs/. Templates in templates/.\n"
        "Save to outputs/rfp-package.md.",
    )
    bullet(doc, "**Time:** 30 minutes.")

    heading(doc, "Day 2 (Tuesday): bid-scorer on your last sourcing event", 2)
    bullet(
        doc,
        "**Goal:** the bid-scorer skill scores your last sourcing "
        "event's bids.",
    )
    bullet(
        doc,
        "**Tasks:** Copy bid-scorer.md. Drop your last sourcing "
        "event's bid responses into bid-responses/ (rename them "
        "to match the BID_<id>_<name>.md pattern if needed). Run.",
    )
    bullet(
        doc,
        "**Validation:** Compare the skill's ranking against the "
        "ranking you produced by hand. If they differ, check the "
        "scoring bands in your skill's Process section.",
    )
    bullet(doc, "**Time:** 60 minutes.")

    heading(doc, "Day 3 (Wednesday): risk-profiler and savings-calculator", 2)
    bullet(doc, "**Goal:** both skills running against the same data.")
    bullet(
        doc,
        "**Tasks:** Copy both skills. Configure the inputs "
        "sections for your data files. Run each. Compare outputs "
        "against your manual analysis.",
    )
    bullet(
        doc,
        "**Validation:** The savings figure should match your "
        "manual calculation within 2%. If it does not, check that "
        "spend-baseline.csv has the correct date range and "
        "currency.",
    )
    bullet(doc, "**Time:** 60 minutes.")

    heading(doc, "Day 4 (Thursday): award-memo and the first chain run", 2)
    bullet(
        doc,
        "**Goal:** the full chain produces a complete sourcing "
        "event package.",
    )
    bullet(
        doc,
        "**Tasks:** Copy award-memo.md. Run the full five-skill "
        "chain on your last sourcing event using the chain prompt "
        "from section 6, Example B. Compare the chain output "
        "against the memo you actually sent.",
    )
    bullet(doc, "**Time:** 90 minutes.")

    heading(doc, "Day 5 (Friday): show your team and start versioning", 2)
    bullet(
        doc,
        "**Goal:** the skill library belongs to your team, not "
        "just to you.",
    )
    bullet(
        doc,
        "**Tasks:** Commit your skills folder to your team's "
        "shared procurement repository or SharePoint. Add a "
        "changelog entry in skills/README.md. Walk one colleague "
        "through running the chain on a hypothetical new event.",
    )
    bullet(
        doc,
        "**Example changelog entry in skills/README.md:**",
    )
    code_block(
        doc,
        "## Changelog\n"
        "v1.0 2026-04-28  Initial skill library: rfp-builder,\n"
        "                  bid-scorer, risk-profiler,\n"
        "                  savings-calculator, award-memo.\n"
        "                  Tested on logistics consolidation event.",
    )
    bullet(doc, "**Time:** 90 minutes.")

    # ===================================================================
    # 10. The pattern
    # ===================================================================
    heading(doc, "10. The pattern: write methodology once, reuse forever", 1)
    para(
        doc,
        "What you build in Course 3 is your team's shared "
        "methodology library. Here is how the pattern works:",
    )
    bullet(
        doc,
        "**Each SKILL.md is small (40 to 90 lines) and focused "
        "on one job.** The rfp-builder builds RFPs. The "
        "bid-scorer scores bids. One skill, one deliverable.",
    )
    bullet(
        doc,
        "**The skill names input shapes, not specific values.** "
        "The rfp-builder says \"a category brief with sections "
        "Today, Current state, Goal, Scope, Stakeholders\". It "
        "does not say \"11.2m USD\" or \"FastRoad UK\". That is "
        "why the same skill works for logistics this quarter and "
        "direct materials next quarter.",
    )
    bullet(
        doc,
        "**Skills compose.** The output of one becomes the input "
        "of another. rfp-builder produces the RFP; bid-scorer "
        "reads the bids; savings-calculator reads the bid "
        "comparison; award-memo reads everything. The chain is "
        "the sourcing event.",
    )
    bullet(
        doc,
        "**Versioning is a discipline.** Comment the version at "
        "the top of the skill (<!-- v1.0 2026-04-25 Initial. -->). "
        "After every change, run the practice chain to confirm "
        "nothing breaks. Write a changelog entry in "
        "skills/README.md.",
    )

    para(
        doc,
        "**Example: reusing the library on a new event.** In "
        "Q3 you run a direct materials sourcing event. You "
        "replace category-brief.md with the materials brief, "
        "replace supplier-longlist.csv with the materials "
        "longlist, drop the new bids into bid-responses/, and "
        "run the same chain prompt. The five skills produce six "
        "deliverables for materials. No rewriting. No new skills.",
    )

    para(
        doc,
        "Future courses build on this. Course 4 (The Command "
        "Engineer) wraps your most-used skill chains in "
        "single-word slash commands so you type `/rfp-launch "
        "logistics 2026-06-15` instead of the full chain prompt. "
        "Course 5 (The Orchestrator) parallelises skill execution "
        "across many bidders or categories at once.",
    )

    # ===================================================================
    # 11. Quick reference and troubleshooting
    # ===================================================================
    heading(doc, "11. Quick reference and troubleshooting", 1)

    heading(doc, "Things to remember", 2)
    bullet(
        doc,
        "**A skill names input shapes, not specific values.** "
        "If your skill says \"Forge Steel UK\" or \"11.2m USD\", "
        "it is a prompt, not a skill. Those values should come "
        "from the input files, not the skill file.",
    )
    bullet(
        doc,
        "**Every skill has the same five sections.** What this "
        "skill does, Inputs, Process, Output format, Quality "
        "criteria. If you miss one, Claude has less guidance "
        "and the output quality drops.",
    )
    bullet(
        doc,
        "**The chain runs in order.** Every step's output is "
        "the next step's input. If step N fails, do not run "
        "step N+1 until step N is fixed. Example: if bid-scorer "
        "fails, savings-calculator has no bid-comparison.md to "
        "read.",
    )
    bullet(
        doc,
        "**Version your skills.** v1.0, v1.1, with a date and "
        "a one-line reason. Example: <!-- v1.1 2026-06-30 "
        "Tightened soft-savings rule per CFO request. -->. "
        "Future you will thank present you.",
    )

    heading(doc, "Common problems and the matching fix", 2)
    bullet(
        doc,
        "**Symptom:** Claude returns a generic answer ignoring "
        "your skill. **Fix:** the skill file is not being loaded. "
        "Check the file path. Run `ls skills` to confirm the "
        "file exists at practice/skills/<name>.md. Common mistake: "
        "saving the file as .txt instead of .md.",
    )
    bullet(
        doc,
        "**Symptom:** the skill works on Acme's logistics bids "
        "but fails on a new event. **Fix:** the skill probably "
        "has Acme-specific values embedded. Open the skill file "
        "and search for any number or name from Acme's data "
        "(11.2m, FastRoad, 2026-06-15). Remove them. The skill "
        "should read those values from the input files.",
    )
    bullet(
        doc,
        "**Symptom:** the skill output passes some quality "
        "criteria but not all. **Fix:** the Process section is "
        "missing a step. Look at the failed criterion and add "
        "the matching process step. Example: if the quality "
        "criterion says \"timeline has four dates\" and the "
        "output has three, add a process step for the missing "
        "date.",
    )
    bullet(
        doc,
        "**Symptom:** the chain stops at step 3. **Fix:** step "
        "2 produced output that step 3 cannot consume. Re-run "
        "step 2 alone, confirm it passes its own quality "
        "criteria, then re-run step 3. Check that the output "
        "path matches what step 3 expects to read.",
    )
    bullet(
        doc,
        "**Symptom:** two analysts produce different scores "
        "from the same skill. **Fix:** the scoring bands are "
        "not numeric enough. Replace words like \"medium\" and "
        "\"high\" with numeric ranges: 60-74, 75-89, 90-100. "
        "The more explicit the bands, the more consistent the "
        "scores.",
    )
    bullet(
        doc,
        "**Symptom:** the award memo savings figure does not "
        "match the savings case. **Fix:** the award-memo skill "
        "is recomputing instead of quoting. Add a quality "
        "criterion: \"savings figure quoted verbatim from "
        "savings-case.md, not recomputed.\"",
    )

    # ===================================================================
    # 12. You are done with Course 3 when
    # ===================================================================
    heading(doc, "12. You are done with Course 3 when", 1)
    numbered(
        doc,
        "Five SKILL.md files in your practice/skills/ folder, "
        "between 40 and 90 lines each. Check with `ls skills`.",
    )
    numbered(
        doc,
        "The full chain runs end to end and produces six "
        "deliverables in practice/outputs/. Check with "
        "`ls outputs`.",
    )
    numbered(
        doc,
        "The award memo recommends a four-carrier panel "
        "covering road FTL, road LTL or pallet, sea FCL, and "
        "air.",
    )
    numbered(
        doc,
        "The savings case shows a saving close to the 1.6m "
        "USD target (approximately 1.55m USD, 14.3%).",
    )
    numbered(
        doc,
        "You can copy your skills folder into your real "
        "procurement project and run the next event.",
    )
    numbered(
        doc,
        "Move to Course 4 (The Command Engineer) when you are "
        "ready. It wraps your most-used skill chains in "
        "single-word slash commands so you type "
        "`/rfp-launch logistics 2026-06-15` instead of the "
        "full chain prompt.",
    )

    # Save
    doc.save(str(OUTPUT_PATH))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
