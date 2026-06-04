"""Build 'Prompt techniques for S2P professionals' as a Word file.

Fourth comprehensive training guide in the course. Same structure as the
Cowork, Code Desktop, and terminal training docs.

Style follows CLAUDE.md: no em-dashes, Oxford commas, British English,
no banned phrases, every worked example has the four parts (prompt,
folder, what you should see, what Claude did behind the scenes).
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt


OUTPUT_PATH = Path(
    r"C:\Users\sambi\OneDrive - U2xAI\Claude Code Projects"
    r"\S2p Training\Course List\Claude Code Foundation for S2P"
    r"\Handouts\Claude_Prompt_Techniques_S2P_Training.docx"
)


# ---------------- helpers (auto-restart numbering) ---------------------

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


# ---------------- content ---------------------------------------------------

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

    # ---------------- Cover ----------------
    para(doc, "U2xAI", italic=True, size=12)
    para(doc, "PROCUREMENT AI EXCELLENCE SERIES", italic=True, size=10)
    doc.add_heading("Claude Prompt Techniques for S2P Professionals", level=0)
    para(doc, "How to write prompts that produce procurement-grade output.", italic=True, size=14)
    para(doc, "Foundational patterns | Advanced patterns | Anti-patterns | Voice matching | Few-shot | Audit footers", italic=True)
    para(doc, "Step-by-step | Daily use scenarios | Full worked examples", italic=True)
    para(doc, "Prepared by U2xAI | u2xai.com", italic=True, size=10)

    # ---------------- 1. How to use ----------------
    heading(doc, "1. How to use this guide", 1)
    para(
        doc,
        "This guide teaches you how to write Claude prompts that produce "
        "procurement-grade output: specific suppliers, real numbers, "
        "audit-ready trails, and writing your CFO will accept. The "
        "techniques apply in all three Claudes (Web, Cowork, and Code), "
        "but the examples lean toward Cowork and Code, where most "
        "procurement work happens.",
    )
    para(
        doc,
        "You do not need any technical background. You need three things: "
        "a real procurement task in front of you, a willingness to iterate "
        "on a prompt, and the discipline to save what works.",
    )
    para(
        doc,
        "Recommended path for a first-time reader: read sections 2 and 3 "
        "for context. Read section 4 (the four parts of a prompt) and "
        "section 5 (setup). Pick one of the five foundational patterns "
        "in section 6 that maps to your real task. Apply it. Move to "
        "the advanced patterns in section 7 once the foundations feel "
        "natural. Use section 12 (the 20-minute sprint) for your first "
        "real win.",
    )

    # ---------------- 2. Executive summary ----------------
    heading(doc, "2. Executive summary", 1)
    para(
        doc,
        "A weak prompt produces a weak output. The output is grammatical, "
        "the format looks right, and a quick reader does not notice the "
        "problem. But the figures are vague, the supplier names are "
        "missing, the dates are absent, and a CFO sends it back. You "
        "blame Claude. The fault was in the prompt.",
    )
    para(
        doc,
        "A strong prompt is the difference between a 30-minute first "
        "draft and a two-hour rebuild. Same Claude, same source files, "
        "same model. The prompt is the variable.",
    )
    para(
        doc,
        "This guide gives you the patterns that turn a weak prompt into "
        "a strong one, the anti-patterns that explain why your last six "
        "outputs disappointed you, and the team workflow that turns "
        "individual prompts into a shared library.",
    )

    heading(doc, "Time savings reference table", 2)
    para(doc, "Source: U2xAI practitioner benchmarks comparing weak prompts against the patterns in this guide on the same source files.")
    fill_table(
        doc,
        ["Procurement task", "Weak prompt time-to-final", "Strong prompt time-to-final"],
        [
            ("Quarterly variance memo for the CFO", "3 to 4 hours of edit cycles", "20 to 30 minutes, one or two passes"),
            ("Pre-negotiation brief for a 4m GBP renewal", "Half a day", "45 minutes, including clarifying questions"),
            ("Supplier scorecard pack (10 suppliers)", "1 hour for draft, 2 hours for cleanup", "15 minutes total, audit footer included"),
            ("Voice-matched supplier email", "20 minutes (rewriting Claude's draft)", "3 minutes (Claude matches on first pass)"),
            ("CFO savings case", "Multiple chats, lost context, 2 hours", "60 minutes, single session, audit-ready"),
            ("Bulk RFP refresh across four categories", "1 day per category", "20 to 30 minutes per category"),
        ],
    )

    # ---------------- 3. The four parts of a procurement prompt ----------------
    heading(doc, "3. The anatomy of a procurement prompt", 1)
    para(
        doc,
        "Every procurement-grade prompt has four parts. If any part is "
        "missing, the output disappoints. Memorise the four parts. "
        "Every pattern in this guide is a variation on them.",
    )
    fill_table(
        doc,
        ["Part", "What it does", "Example phrasing"],
        [
            ("**Inputs**", "Names every source file by exact path and tells Claude what each one contains.",
             "Read Master/q3_kpi_export.csv (the columns are Supplier, Spend_GBP, On_Time_Pct, Defect_Pct)."),
            ("**Action**", "Names the work to be done in plain verbs.",
             "Build a Q3 supplier scorecard for the top 10 suppliers by spend."),
            ("**Output**", "Names the output file by exact path, the format, and the cap on length.",
             "Save as Drafts/scorecard_q3_v1.xlsx. Cap the table at 10 rows."),
            ("**Constraints**", "Names what NOT to do.",
             "Master/ is read-only. Do not modify any file in Master/. No vague figures: every number must be from the source file."),
        ],
    )
    para(doc, "**Folder layout used by this guide's examples.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── ABOUT ME/                  (Cowork-style personalisation)\n"
        "│   ├── about-me.md\n"
        "│   ├── my-company.md\n"
        "│   └── procurement-standards.md\n"
        "├── CLAUDE.md                  (Code-style personalisation)\n"
        "├── Master/\n"
        "│   └── source files\n"
        "├── Drafts/\n"
        "├── Outputs/\n"
        "└── prompt_library/\n"
        "    ├── voice_matched_email.md\n"
        "    ├── variance_memo.md\n"
        "    └── ..."
    )

    # ---------------- 4. Setup ----------------
    heading(doc, "4. Set up your prompt library", 1)
    para(
        doc,
        "A prompt library is a folder of saved prompts that work. Each "
        "prompt is a Markdown file. You build the library once and "
        "extend it every week. By month three, your library is the "
        "single most valuable thing you own.",
    )
    para(doc, "Set it up in five minutes:")
    numbered(doc, "Create the folder `prompt_library/` at the root of your project.")
    numbered(doc, "Inside it, create three subfolders: `read_only/`, `single_file/`, `multi_file/` (matching the three reference patterns).")
    numbered(doc, "Save your CLAUDE.md (Code) or your four ABOUT ME files (Cowork) at the root. The personalisation pattern is non-negotiable; without it, every prompt has to repeat the same setup.")
    numbered(doc, "Use the naming convention `Prompt_<Action>_<DocType>.md`. Example: `Prompt_Review_NDA.md`, `Prompt_Build_Scorecard.md`, `Prompt_Refresh_RFP.md`.")
    numbered(doc, "Commit the prompt library to Git or sync it to SharePoint. The library is shared infrastructure, not personal notes.")

    # ---------------- 5. Five foundational patterns ----------------
    heading(doc, "5. Five foundational prompt patterns", 1)
    para(
        doc,
        "Use one of these five patterns as the spine of every procurement "
        "prompt. They are general; the next section adds the procurement-"
        "specific advanced patterns. Each foundational pattern below is "
        "shown as a fill-in-the-blank template, then a worked example, "
        "then a behind-the-scenes walkthrough.",
    )

    heading(doc, "Pattern 1: Read-only review", 2)
    para(doc, "When to use: you want Claude to read and report on a file without changing it. Most contract reviews, summaries, and clause checks fit here.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "Read <file path> and <verb that does not modify, e.g. list, summarise, compare>.\n"
        "For each <unit, e.g. clause, supplier, line item>, give:\n"
        "- <field 1>,\n"
        "- <field 2>,\n"
        "- <field 3>.\n"
        "Cap the output at <N rows / words>.\n"
        "Do not edit the file."
    )
    para(doc, "**Worked example: clause review of an MSA.**")
    code_block(
        doc,
        "Read Master/Acme_MSA_v3.pdf and list every clause that mentions\n"
        "'data', 'personal information', or 'confidential'.\n"
        "For each one, give: clause number, page number, the clause text\n"
        "in one sentence, and whether it favours us (the customer) or\n"
        "Acme (the supplier).\n"
        "Cap the output at 15 rows.\n"
        "Do not edit the file."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "└── Master/\n"
        "    └── Acme_MSA_v3.pdf"
    )
    para(doc, "**What you should see.** A 12-to-15-row table with clause numbers, page numbers, plain-English summaries, and the favours-us / favours-them column.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Open the file at the named path. Read it cover to cover.")
    numbered(doc, "Search for the three named keywords across every clause.")
    numbered(doc, "For each hit, capture the clause number and page number from the document structure.")
    numbered(doc, "Decide which side the clause favours by asking: whose obligation does this create, and whose risk does it cap?")
    numbered(doc, "Stop at 15 rows. The cap protects you from a 40-row response that you have to skim.")
    numbered(doc, "Write nothing back to the source PDF. The 'do not edit' constraint blocks the modify path entirely.")

    heading(doc, "Pattern 2: Single-file edit", 2)
    para(doc, "When to use: you want Claude to modify exactly one file and produce a new version, leaving everything else untouched. Most scorecard builds, RFP refreshes, and template fills fit here.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "Take <input file path> as the source.\n"
        "Apply these changes:\n"
        "- <change 1>,\n"
        "- <change 2>,\n"
        "- <change 3>.\n"
        "Save the result as <output file path> in <output folder>.\n"
        "Leave the source file untouched."
    )
    para(doc, "**Worked example: refresh an RFP scope section.**")
    code_block(
        doc,
        "Take Master/Office_Supplies_RFP_Master.docx as the source.\n"
        "Replace the Scope section with:\n"
        "- 14 UK sites listed in Master/Suppliers_Q2.xlsx, sheet 'Sites',\n"
        "- annual spend band: 1.2m to 1.5m GBP,\n"
        "- contract length: 24 months with one 12-month extension.\n"
        "Save as Drafts/RFP_Q2_v1.docx.\n"
        "Leave Master/ untouched."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Master/\n"
        "│   ├── Office_Supplies_RFP_Master.docx\n"
        "│   └── Suppliers_Q2.xlsx\n"
        "└── Drafts/\n"
        "    └── RFP_Q2_v1.docx"
    )
    para(doc, "**What you should see.** A new file in Drafts/ with the Scope section rewritten and the rest of the RFP untouched.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Open the source RFP and walk the structure to find the Scope heading.")
    numbered(doc, "Read the existing Scope content to know what is being replaced.")
    numbered(doc, "Open the supplier Excel and read the named sheet.")
    numbered(doc, "Write the new Scope content using the three bullets, formatted in the same Word style as the surrounding section.")
    numbered(doc, "Save the result to the named draft path. The source file is not modified.")

    heading(doc, "Pattern 3: Multi-file build", 2)
    para(doc, "When to use: you want Claude to combine inputs from multiple files into one new artefact. Onboarding packs, savings cases, and RFP packages fit here.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "Using <input file 1> and <input file 2> and <...>,\n"
        "produce <named artefact>.\n"
        "Pull from <file 1>: <fields>.\n"
        "Pull from <file 2>: <fields>.\n"
        "Combine into <output structure>.\n"
        "Save as <output path>.\n"
        "Leave inputs untouched."
    )
    para(doc, "**Worked example: a renewal brief from a live contract.**")
    code_block(
        doc,
        "Using Master/Contract_Northwind_Live.docx and Templates/Renewal_Brief_Template.docx,\n"
        "produce a renewal brief for the Northwind Office Ltd contract.\n"
        "Pull the contract value, end date, notice period, and auto-renewal\n"
        "clause from the live contract.\n"
        "Drop them into the matching fields in the template.\n"
        "Today is 2026-04-25. Flag the notice deadline status at the top.\n"
        "Save as Drafts/Renewal_Brief_Northwind_2026.docx.\n"
        "Leave Master/ and Templates/ untouched."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Master/\n"
        "│   └── Contract_Northwind_Live.docx\n"
        "├── Templates/\n"
        "│   └── Renewal_Brief_Template.docx\n"
        "└── Drafts/\n"
        "    └── Renewal_Brief_Northwind_2026.docx"
    )
    para(doc, "**What you should see.** A populated renewal brief in Drafts/, with a notice deadline status line at the top.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Open the live contract and read it end to end.")
    numbered(doc, "Search for the four named fields by language pattern.")
    numbered(doc, "Open the brief template and find the placeholder fields.")
    numbered(doc, "Substitute each value into the matching placeholder. Keep long clauses verbatim.")
    numbered(doc, "Compute the notice deadline as end_date minus notice_period; compare to today; write the status line.")
    numbered(doc, "Save the populated brief to Drafts/. Master/ and Templates/ are not touched.")

    heading(doc, "Pattern 4: Persona prompting", 2)
    para(doc, "When to use: you want the output written in a specific voice. Procurement-relevant personas: a CFO reviewer, a junior analyst, a category lead, a supplier-facing buyer, a board chair.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "You are <named persona, e.g. 'a CFO reviewer'>.\n"
        "<persona's known concerns: e.g. 'You distrust soft savings.\n"
        "You expect specific suppliers, dates, and figures.'>\n"
        "Read <input>.\n"
        "Produce <output> as that persona would write it.\n"
        "Specifics required: <list>.\n"
        "Avoid: <list>."
    )
    para(doc, "**Worked example: a CFO-voice savings case.**")
    code_block(
        doc,
        "You are a CFO reviewing a procurement savings case.\n"
        "You distrust soft savings. You expect specific suppliers,\n"
        "dates, and figures. You read the headline first.\n"
        "Read Master/logistics_consolidation_data.csv.\n"
        "Produce a one-page savings memo as that CFO would write it.\n"
        "Specifics required: at least one supplier name (legal entity),\n"
        "the contract value, the effective date, and the realised\n"
        "savings figure with the calculation shown.\n"
        "Avoid: vague phrases. Every number must trace to a source row.\n"
        "Save as Drafts/CFO_Savings_Memo_Logistics.md."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── ABOUT ME/\n"
        "│   └── procurement-standards.md\n"
        "├── Master/\n"
        "│   └── logistics_consolidation_data.csv\n"
        "└── Drafts/\n"
        "    └── CFO_Savings_Memo_Logistics.md"
    )
    para(doc, "**What you should see.** A memo that opens with the headline figure (1.42m GBP annualised), names the four consolidated suppliers, names the start date, and shows the calculation. No vague phrases.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Adopt the persona stated. The persona's known concerns become Claude's writing constraints.")
    numbered(doc, "Lead with the headline (CFO behaviour: read top first).")
    numbered(doc, "Pull every figure from the source CSV, not from any cached intuition.")
    numbered(doc, "Show the calculation inline so the CFO can audit it without opening the source.")
    numbered(doc, "Refuse to write a paragraph that lacks a supplier name, a date, or a number.")

    heading(doc, "Pattern 5: Few-shot examples", 2)
    para(doc, "When to use: when an instruction is hard to verbalise but easy to demonstrate. Voice matching, classification taxonomies, and consistent formatting all benefit.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "I want output in the same style as these examples:\n\n"
        "Example 1: <full sample of the desired output>\n"
        "Example 2: <full sample of the desired output>\n"
        "Example 3: <full sample of the desired output>\n\n"
        "Now produce the same kind of output for: <new input>."
    )
    para(doc, "**Worked example: classifying supplier risk into a five-tier taxonomy.**")
    code_block(
        doc,
        "I want each supplier classified into one of five risk tiers:\n"
        "Critical, High, Medium, Low, Watch. Use these examples:\n\n"
        "Example 1:\n"
        "Supplier: Acme Stationery. Tier: Watch.\n"
        "Reason: 12% of indirect spend, no single-source dependency,\n"
        "two alternative qualified suppliers, stable financials.\n\n"
        "Example 2:\n"
        "Supplier: TechSource MCU. Tier: Critical.\n"
        "Reason: single-source for MCU chips, 45,000 unit Q4 demand,\n"
        "supplier announced gallium shortage. No qualified alternative.\n\n"
        "Example 3:\n"
        "Supplier: Globex Logistics. Tier: Medium.\n"
        "Reason: 8% of logistics spend, one alternative qualified,\n"
        "current contract expires in 90 days, recent price increase\n"
        "request pending.\n\n"
        "Now classify each supplier in Master/supplier_master.csv\n"
        "into one of the five tiers, using the same format."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Master/\n"
        "│   └── supplier_master.csv\n"
        "└── Drafts/\n"
        "    └── supplier_risk_classification.md"
    )
    para(doc, "**What you should see.** One short block per supplier with the tier and a two-sentence reason. The format matches the three examples.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Read the three examples and infer the implicit rules: format, length, fields named.")
    numbered(doc, "Build a five-tier rubric from the examples (Critical = single-source plus disruption, Watch = stable plus alternatives, Medium = single alternative plus a current event, etc.).")
    numbered(doc, "Apply the rubric to every supplier in the source CSV.")
    numbered(doc, "Output one block per supplier in the same shape as the examples.")
    numbered(doc, "Stay consistent: same field names, same length, same tone.")

    # ---------------- 6. Five advanced patterns ----------------
    heading(doc, "6. Five advanced procurement prompt patterns", 1)

    heading(doc, "Pattern 6: Voice matching from your old samples", 2)
    para(doc, "When to use: you want a draft in your team's voice or in your own voice, not in generic AI prose.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "Read the three sample memos at <paths>. Match this voice in your\n"
        "next output: same sentence length, same vocabulary level, same\n"
        "level of hedging, same use of headings or no headings.\n"
        "Now write <new output> in that voice."
    )
    para(doc, "**Worked example.**")
    code_block(
        doc,
        "Read the three memos at Reference/memos/jan_2026.md,\n"
        "Reference/memos/feb_2026.md, Reference/memos/mar_2026.md.\n"
        "Match this voice: short sentences, no headings inside the memo,\n"
        "lead with the figure, no marketing words.\n"
        "Now write the April variance memo using\n"
        "Master/oracle_apr_export.csv as the source.\n"
        "Save as Drafts/variance_memo_apr.md."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Reference/\n"
        "│   └── memos/\n"
        "│       ├── jan_2026.md\n"
        "│       ├── feb_2026.md\n"
        "│       └── mar_2026.md\n"
        "├── Master/\n"
        "│   └── oracle_apr_export.csv\n"
        "└── Drafts/\n"
        "    └── variance_memo_apr.md"
    )
    para(doc, "**What you should see.** An April memo that reads like the three samples: short sentences, headline first, no AI tells.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Read each sample memo and extract recurring traits (sentence length, vocabulary, hedging, structure).")
    numbered(doc, "Build a stylistic profile from the recurring traits.")
    numbered(doc, "Read the source CSV and compute the April variance.")
    numbered(doc, "Write the new memo using the stylistic profile as the constraint, the CSV as the content.")
    numbered(doc, "Refuse to introduce phrases that did not appear in the samples.")

    heading(doc, "Pattern 7: Structured output (named columns, capped rows)", 2)
    para(doc, "When to use: anywhere you want a table you can drop straight into Word, Excel, or a deck. Naming the columns and capping the rows protects you from a 40-row sprawl.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "Output the result as a table with these columns, in this order:\n"
        "<col 1>, <col 2>, <col 3>, <col 4>.\n"
        "Cap at <N> rows.\n"
        "Sort descending by <col>.\n"
        "Where a cell is unknown, write 'not detected'."
    )
    para(doc, "**Worked example.**")
    code_block(
        doc,
        "Read Master/q3_kpi_export.csv. Output a table with these columns,\n"
        "in this order:\n"
        "Supplier, Spend_GBP, On_Time_Pct, RAG_Status, One_Line_Commentary.\n"
        "Cap at 10 rows.\n"
        "Sort descending by Spend_GBP.\n"
        "Where a cell is unknown, write 'not detected'.\n"
        "Save as Drafts/scorecard_q3.md."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Master/\n"
        "│   └── q3_kpi_export.csv\n"
        "└── Drafts/\n"
        "    └── scorecard_q3.md"
    )
    para(doc, "**What you should see.** A 10-row Markdown table, columns in the named order, sorted by spend, with empty cells marked 'not detected'.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Read the source CSV and detect the columns.")
    numbered(doc, "Apply the RAG bands from the project's procurement-standards.md to compute RAG_Status.")
    numbered(doc, "Write a one-line commentary per supplier based on their KPI mix.")
    numbered(doc, "Sort by spend, descending. Stop at 10 rows.")
    numbered(doc, "Mark missing cells explicitly rather than leaving them blank.")

    heading(doc, "Pattern 8: Clarifying questions first", 2)
    para(doc, "When to use: when the task is non-routine and you would rather Claude ask before guessing. Saves a full failed run and the wasted tokens.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "I want to <task>. Before you start, ask me <N> clarifying\n"
        "questions about the parts that are not obvious from the source\n"
        "files. Wait for my answers. Then build the output."
    )
    para(doc, "**Worked example.**")
    code_block(
        doc,
        "I want to build a pre-negotiation brief for our renewal with\n"
        "Northwind Office Ltd. Their current contract is 1.42m GBP annual.\n"
        "Before you start, ask me four clarifying questions about:\n"
        "- our walk-away position,\n"
        "- which of the open issues (use the list in OUTPUTS/northwind/) are\n"
        "  hard asks vs soft asks,\n"
        "- the audience for the brief (negotiator alone, or category lead too),\n"
        "- whether the recent gallium shortage news affects the deal.\n"
        "Wait for my answers. Then build the brief."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "└── OUTPUTS/\n"
        "    └── northwind/\n"
        "        └── open_issues.md  (input notes)"
    )
    para(doc, "**What you should see.** Claude asks the four named questions, one block. You answer. Claude then produces the brief informed by your answers.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Read the prompt and identify the four named ambiguities.")
    numbered(doc, "Stop the work. Output exactly four questions, one per ambiguity.")
    numbered(doc, "Wait. Do not produce the brief yet.")
    numbered(doc, "On receiving your answers, integrate them as additional constraints.")
    numbered(doc, "Build the brief with the answers baked in.")

    heading(doc, "Pattern 9: Iterative refinement (Restart from here)", 2)
    para(doc, "When to use: a long chat has drifted, the output is now wrong, and you would otherwise paste a follow-up correction. The correction adds tokens and rarely fixes the root cause.")
    para(doc, "**Technique.** Right-click the message where the prompt first went wrong. Choose 'Restart from here'. Edit the original prompt to fix the root cause. Send. Everything after that point in the conversation is dropped, and Claude starts again with the corrected prompt.")
    para(doc, "**Worked example.**")
    code_block(
        doc,
        "Original prompt at message 3:\n"
        "  Build a savings case for the logistics consolidation. Use\n"
        "  Master/logistics.csv. Save to Drafts/.\n\n"
        "Result at message 4: too long, no specific suppliers named,\n"
        "  no audit footer, the headline figure is rounded to 'about 2m'.\n\n"
        "Wrong move: paste at message 5 'remember to name suppliers and\n"
        "  add an audit footer'. The chat now has eight messages, four of\n"
        "  them corrections. Tokens wasted.\n\n"
        "Right move: right-click message 3, choose 'Restart from here'.\n"
        "  Replace the prompt with:\n\n"
        "  Build a CFO savings case for the logistics consolidation.\n"
        "  Use Master/logistics.csv as the source.\n"
        "  Required: name every supplier (legal entity), every effective\n"
        "  date, and every figure to two decimal places.\n"
        "  Required: add an audit footer with the timestamp, the source\n"
        "  file path, and the model used.\n"
        "  Cap the case at 600 words.\n"
        "  Save to Drafts/savings_case_logistics.md."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Master/\n"
        "│   └── logistics.csv\n"
        "└── Drafts/\n"
        "    └── savings_case_logistics.md"
    )
    para(doc, "**What you should see after the restart.** A clean, audit-ready savings case. The chat is short (one prompt, one response). Tokens spent are roughly half what the corrected long-chat version would have cost.")
    para(doc, "**What this technique directs Claude to do.**")
    numbered(doc, "Drop the entire conversation tail after the restart point. Claude no longer sees the bad output or your corrections.")
    numbered(doc, "Read the corrected prompt as a fresh instruction.")
    numbered(doc, "Build the output to the new constraints in one pass.")
    numbered(doc, "Pay tokens only for the original context plus the new prompt and response, not for the entire failed branch.")

    heading(doc, "Pattern 10: The audit footer", 2)
    para(doc, "When to use: any output that lands with a CFO, a board, an auditor, or a supplier counterparty. The footer turns the output into a self-contained, audit-ready document.")
    para(doc, "**Template.**")
    code_block(
        doc,
        "At the bottom of the output, add an audit footer with these fields:\n"
        "- Generated: <timestamp, ISO date and time>\n"
        "- Source files: <every file you read, with full path>\n"
        "- Model: <the Claude model used>\n"
        "- Operator: <the user's name from CLAUDE.md or about-me.md>\n"
        "- Output saved to: <full path of the output file>"
    )
    para(doc, "**Worked example.** Combine this with the CFO-voice savings memo. Add the line to the prompt:")
    code_block(
        doc,
        "...\n"
        "At the bottom of the memo, add an audit footer with these fields:\n"
        "- Generated: <today's date and time, ISO format>\n"
        "- Source files: every file you read, full path\n"
        "- Model: the Claude model used\n"
        "- Operator: <my name>\n"
        "- Output: Drafts/CFO_Savings_Memo_Logistics.md"
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "└── Drafts/\n"
        "    └── CFO_Savings_Memo_Logistics.md   (memo + audit footer)"
    )
    para(doc, "**What you should see.** A memo with five footer lines at the bottom, in plain text. The footer is the difference between an output a CFO challenges and an output a CFO files.")
    para(doc, "**What this prompt directs Claude to do.**")
    numbered(doc, "Capture the timestamp at the moment of save.")
    numbered(doc, "List every source file path it actually opened during the run.")
    numbered(doc, "Name the model from its own runtime context.")
    numbered(doc, "Look up the operator name from the personalisation files.")
    numbered(doc, "Append the five-field block as the last lines of the output, separated from the body by a horizontal rule.")

    # ---------------- 7. Anti-patterns ----------------
    heading(doc, "7. Common anti-patterns and their fixes", 1)
    para(
        doc,
        "Five anti-patterns explain ninety percent of disappointing "
        "outputs. Each row below shows the bad shape, the result, and "
        "the fix.",
    )
    fill_table(
        doc,
        ["Anti-pattern", "What goes wrong", "Fix"],
        [
            ("**Vague task.** A prompt like 'help me with this RFP'.",
             "Claude fills the gap with a generic answer that does not match your situation.",
             "Use the four parts (section 3). Name the input file, the action, the output file, and what NOT to change."),
            ("**Massive context dump.** Pasting a 200-page contract into the chat box every turn.",
             "Tokens burn fast. Long chats start forgetting the early context. Cost rises.",
             "Save the file to Master/. Reference it by path: 'Read Master/Acme_MSA_v3.pdf'. Cowork and Code load on demand."),
            ("**Five tasks in one prompt.** 'Review the contract, draft a redline, build a scorecard, write a memo, prepare talking points.'",
             "Claude does the easy ones well and the hard ones poorly, all in one undifferentiated wall of text.",
             "Split into five separate prompts. Save the working ones to your prompt library."),
            ("**No output cap.** 'Summarise the contract.'",
             "You get a four-page summary when you wanted a half-page.",
             "Always cap: 'Summarise in 10 rows', 'Cap at 600 words', 'One paragraph maximum'."),
            ("**Keyword soup.** 'Apex Q3 KPI scorecard QBR tomorrow'.",
             "Claude has nothing to anchor on. The output is thin.",
             "Speak (or type) full sentences. Treat Claude like a junior analyst who has just walked into the room."),
            ("**Follow-up correction in a long chat.** Pasting 'remember to add the audit footer' at message 9 when you should have restarted from message 3.",
             "Tokens wasted. Original instructions still in context, fighting the corrections.",
             "Use Pattern 9: Restart from here. Edit the original prompt at the divergence point."),
        ],
    )

    # ---------------- 8. Day in the life ----------------
    heading(doc, "8. A day in the life: prompt techniques in a real workday", 1)
    para(
        doc,
        "This section follows Priya, a Strategic Sourcing Lead at a global "
        "retail group. She runs Indirects (office, IT services, logistics, "
        "professional services). She has the prompt library from section 4 "
        "in place, the personalisation pattern set up, and a Pro plan.",
    )

    heading(doc, "08:00. Voice-matched supplier email before her first meeting", 2)
    para(
        doc,
        "Priya needs a four-sentence email to John at Acme Logistics "
        "asking him to confirm the new lead time on PO 5824. She has "
        "three of her own previous emails saved in Reference/voice/ and "
        "she runs the voice-matching pattern (Pattern 6).",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Reference/\n"
        "│   └── voice/\n"
        "│       ├── email_jan.md\n"
        "│       ├── email_feb.md\n"
        "│       └── email_mar.md\n"
        "└── Drafts/\n"
        "    └── acme_lead_time_email.md"
    )
    para(doc, "**The prompt:**")
    code_block(
        doc,
        "Read the three emails in Reference/voice/. Match my voice.\n"
        "Now write a four-sentence email to John at Acme Logistics.\n"
        "Subject: PO 5824 lead time confirmation.\n"
        "Facts: PO placed 2026-04-15. Confirmed delivery was 2026-04-22.\n"
        "Today is 2026-04-25. Goods not received. Ask for new firm date\n"
        "by close of business 2026-04-26.\n"
        "Sign off as Priya, Strategic Sourcing.\n"
        "Save as Drafts/acme_lead_time_email.md."
    )
    para(doc, "**What you should see.** A four-sentence email that reads like Priya wrote it. No AI hedging, no marketing tone.")
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Read the three sample emails and extracted Priya's traits: short sentences, no hedging openers, signs off with role.")
    numbered(doc, "Built a stylistic profile from the recurring traits.")
    numbered(doc, "Composed a four-sentence email using the five named facts.")
    numbered(doc, "Held to four sentences (the cap).")
    numbered(doc, "Refused to introduce hedging language not present in the samples.")

    heading(doc, "10:30. Pre-negotiation brief with clarifying questions first", 2)
    para(
        doc,
        "Priya has a renewal meeting with Globex Logistics in three days. "
        "The contract is 4.2m GBP. She uses Pattern 8 (clarifying "
        "questions first) so Claude does not guess on the high-stakes "
        "details.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── ABOUT ME/\n"
        "│   ├── my-company.md\n"
        "│   └── procurement-standards.md\n"
        "└── OUTPUTS/\n"
        "    └── globex/\n"
        "        ├── open_issues.md         (input notes)\n"
        "        └── pre_negotiation_brief.md  (output)"
    )
    para(doc, "**The prompt:**")
    code_block(
        doc,
        "I want a pre-negotiation brief for our renewal with Globex Logistics.\n"
        "Current contract: 4.2m GBP annual. Renewal meeting on 2026-04-28.\n"
        "Source notes: OUTPUTS/globex/open_issues.md.\n"
        "Before you build the brief, ask me four clarifying questions about:\n"
        "- our walk-away position,\n"
        "- which of the open issues are hard asks vs soft asks,\n"
        "- the audience (negotiator alone, or category lead too),\n"
        "- whether the recent gallium shortage news materially affects the deal.\n"
        "Wait for my answers. Then build the brief.\n"
        "Cap at one page. Save to OUTPUTS/globex/pre_negotiation_brief.md."
    )
    para(doc, "**What you should see.** Claude asks the four questions in one block. Priya answers. Claude builds the brief informed by the answers.")
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Stopped at the named ambiguities and produced exactly four questions.")
    numbered(doc, "Waited. Did not produce the brief until Priya answered.")
    numbered(doc, "Once answers arrived, integrated them as additional constraints alongside the source notes.")
    numbered(doc, "Read OUTPUTS/globex/open_issues.md for the contract and supplier facts.")
    numbered(doc, "Built a one-page brief: their position, our position, three exposure points each side, recommended opening, soft asks, hard asks.")
    numbered(doc, "Capped at one page because the prompt said so.")

    heading(doc, "13:00. CFO savings case with persona prompting and audit footer", 2)
    para(
        doc,
        "Priya combines two patterns: persona prompting (Pattern 4) for "
        "voice, and the audit footer (Pattern 10) for the CFO trail. "
        "Total savings claim: 1.42m GBP annualised.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── ABOUT ME/\n"
        "│   ├── my-company.md\n"
        "│   └── procurement-standards.md\n"
        "├── Master/\n"
        "│   └── logistics_consolidation_data.csv\n"
        "└── Drafts/\n"
        "    └── CFO_Savings_Memo_Logistics.md"
    )
    para(doc, "**The prompt:**")
    code_block(
        doc,
        "You are a CFO reviewing a procurement savings case.\n"
        "You distrust soft savings and you read the headline first.\n"
        "Read Master/logistics_consolidation_data.csv.\n"
        "Produce a one-page savings memo. Required:\n"
        "- supplier names (legal entities),\n"
        "- contract values,\n"
        "- effective dates,\n"
        "- the calculation behind every figure shown inline.\n"
        "Add an audit footer with: Generated (today's date and time, ISO),\n"
        "Source files (full paths), Model (the Claude model used),\n"
        "Operator (Priya), Output: Drafts/CFO_Savings_Memo_Logistics.md.\n"
        "Cap the memo at 600 words. Save to the named output path."
    )
    para(doc, "**What you should see.** A 580-word memo, headline first, named suppliers, named dates, calculation inline, with the five-field audit footer at the bottom.")
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Adopted the CFO persona; led with the headline figure.")
    numbered(doc, "Read every figure from the source CSV; did not invent.")
    numbered(doc, "Showed each calculation inline, near the figure it produced.")
    numbered(doc, "Held the memo to 580 words because the prompt capped it at 600.")
    numbered(doc, "Captured the timestamp at save and listed every file it had opened.")
    numbered(doc, "Appended the five-field audit footer below a horizontal rule.")

    heading(doc, "15:00. Bulk supplier risk classification using few-shot", 2)
    para(
        doc,
        "Priya needs every supplier in the indirect master classified "
        "into one of five risk tiers for the quarterly governance pack. "
        "She uses Pattern 5 (few-shot) with three carefully chosen "
        "examples spanning the range of tiers.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Master/\n"
        "│   └── indirect_supplier_master.csv\n"
        "└── Drafts/\n"
        "    └── supplier_risk_classification.md"
    )
    para(doc, "**The prompt** uses the few-shot block from section 5 Pattern 5, applied to her real supplier master.")
    para(doc, "**What you should see.** One short block per supplier with tier and a two-sentence reason. The format matches the three examples Priya provided.")
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Inferred the rubric from the three examples (Critical, Watch, Medium each have one example).")
    numbered(doc, "Filled in the missing tiers (High, Low) by interpolation between the examples Priya provided.")
    numbered(doc, "Applied the rubric to each supplier in the master CSV.")
    numbered(doc, "Wrote each result block in the same shape as the examples.")
    numbered(doc, "Did not invent reasons; pulled justifications from the supplier master columns.")

    heading(doc, "17:00. Restart from here saves the day", 2)
    para(
        doc,
        "End of day. Priya is on a long chat (eighteen messages deep) "
        "iterating on a category strategy deck. The output has drifted "
        "from her earlier rules. She catches it: 'Restart from here' on "
        "message 4.",
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "└── Drafts/\n"
        "    └── indirects_strategy_deck_outline.md"
    )
    para(doc, "**The technique:** right-click message 4 (the original strategy prompt). Choose 'Restart from here'. Edit the prompt to bake in the constraints she had been pasting as corrections (cap at 12 slides, no soft savings claims, supplier names mandatory). Send.")
    para(doc, "**What you should see.** A clean strategy deck outline in one pass. Token spend roughly half what the long-chat version cost.")
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Dropped the entire conversation tail after message 4.")
    numbered(doc, "Read the corrected prompt as a fresh instruction with the new constraints baked in.")
    numbered(doc, "Built the deck outline in one response.")
    numbered(doc, "Held to the constraints because they were now in the original prompt, not in follow-up corrections.")
    numbered(doc, "Did not see the bad earlier output, so was not tempted to repeat its mistakes.")

    # ---------------- 9. Use case walkthroughs ----------------
    heading(doc, "9. Three use case walkthroughs: weak prompt to strong prompt", 1)
    para(
        doc,
        "Three use cases below show the full evolution: the weak first "
        "attempt, why it fails, the strong rewrite, and the result. Use "
        "this section as a worked reference when you are building a new "
        "prompt for a familiar S2P task.",
    )

    heading(doc, "Use Case 1: Quarterly variance memo for the CFO", 2)
    para(doc, "**Weak first attempt:**")
    code_block(doc, "Summarise the Q3 spend variance.")
    para(doc, "**Why it fails.** No source named, no output format, no length cap, no audience signalled. Claude produces a generic three-page essay full of hedging.")
    para(doc, "**Strong rewrite (combines patterns 4, 7, and 10):**")
    code_block(
        doc,
        "You are a CFO reviewer. You expect specific commodities, named\n"
        "suppliers, and concrete GBP figures.\n"
        "Read Master/oracle_q3_export.csv (Oracle Purchasing Q3 export)\n"
        "and Master/q3_budget.xlsx (the approved Q3 budget).\n"
        "Produce a CFO-style variance narrative.\n"
        "Sections:\n"
        "- Headline: Q3 actual vs budget, total and percentage.\n"
        "- Top three commodities by absolute over-budget variance.\n"
        "- Top three suppliers driving the over-budget commodities.\n"
        "- Three recommended actions, each tied to a specific overrun.\n"
        "Cap at 600 words.\n"
        "Add an audit footer (Generated, Source files, Model, Operator,\n"
        "Output path).\n"
        "Save to Drafts/variance_memo_q3.md."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Master/\n"
        "│   ├── oracle_q3_export.csv\n"
        "│   └── q3_budget.xlsx\n"
        "└── Drafts/\n"
        "    └── variance_memo_q3.md"
    )
    para(doc, "**What you should see.** A 580-word memo with named sections, named commodities, named suppliers, GBP figures, three-action recommendation, and a five-field audit footer.")
    para(doc, "**What the strong prompt directed Claude to do.**")
    numbered(doc, "Read both source files and join on commodity_code.")
    numbered(doc, "Compute variance per commodity, sort descending by absolute over-budget.")
    numbered(doc, "Pick the top three commodities and trace each to the suppliers responsible.")
    numbered(doc, "Adopt the CFO voice: lead with the headline, no hedging.")
    numbered(doc, "Hold to the four-section structure.")
    numbered(doc, "Cap at 580 words because the prompt said 600.")
    numbered(doc, "Append the audit footer with timestamp, sources, model, operator, output path.")

    heading(doc, "Use Case 2: Bulk NDA review across 24 supplier contracts", 2)
    para(doc, "**Weak first attempt:**")
    code_block(doc, "Look at the NDAs and tell me what's wrong with them.")
    para(doc, "**Why it fails.** No folder named, no comparison baseline, no output format, no flag rules. Claude produces 24 paragraphs of impressionistic prose nobody can act on.")
    para(doc, "**Strong rewrite (combines patterns 1, 5, and 7):**")
    code_block(
        doc,
        "Read every PDF in Master/nda_batch_april/. Compare each one\n"
        "against standards/our_standard_nda.docx.\n"
        "Output a table with these columns, in this order:\n"
        "Supplier, Effective_Date, Term_Months, Governing_Law, Mutual,\n"
        "Arbitration_Present, Review_Needed.\n"
        "Sort alphabetically by Supplier.\n"
        "Cap at 24 rows.\n"
        "Where a cell is unknown, write 'not detected'.\n"
        "Set Review_Needed to 'Yes' when: term > 36 months, OR governing law\n"
        "is not 'England and Wales', OR arbitration is missing where required.\n"
        "Save to Drafts/NDA_Summary.xlsx.\n"
        "Master/ is read-only."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── Master/\n"
        "│   └── nda_batch_april/   (24 supplier NDAs)\n"
        "├── standards/\n"
        "│   └── our_standard_nda.docx\n"
        "└── Drafts/\n"
        "    └── NDA_Summary.xlsx"
    )
    para(doc, "**What you should see.** A 24-row Excel with the seven named columns, sorted by supplier, flagged rows clearly marked, missing fields explicit.")
    para(doc, "**What the strong prompt directed Claude to do.**")
    numbered(doc, "List every PDF in the batch folder. Count them.")
    numbered(doc, "Read the comparison baseline once and hold it in working memory.")
    numbered(doc, "For each PDF, parse the text and extract the six named fields.")
    numbered(doc, "Apply the three-condition flag rule and set Review_Needed accordingly.")
    numbered(doc, "Mark missing fields explicitly rather than guessing.")
    numbered(doc, "Sort alphabetically and cap at 24 rows.")
    numbered(doc, "Did not write to Master/. Saved to the named draft path only.")

    heading(doc, "Use Case 3: On-demand supplier risk brief from a Slack trigger", 2)
    para(doc, "**Weak first attempt:**")
    code_block(doc, "Tell me about Globex.")
    para(doc, "**Why it fails.** No audience, no length, no source, no format. Claude produces a 400-word Wikipedia-style entry that does not answer the question Priya's CFO will ask.")
    para(doc, "**Strong rewrite (combines patterns 4, 7, and 8):**")
    code_block(
        doc,
        "You are writing for our VP of Operations. She has 3 minutes.\n"
        "Build a supplier risk brief for Globex SA.\n"
        "Source: data/supplier_master.csv (look up Globex SA).\n"
        "Use the connected web-search tool for current news on Globex SA.\n"
        "Output sections:\n"
        "- Risk summary (3 sentences leading with the supply gap or financial state).\n"
        "- Supply gap analysis (current Q4 demand vs last confirmed delivery).\n"
        "- Three alternative source options ranked by speed to qualify.\n"
        "- Three recommended immediate actions ranked by speed of impact.\n"
        "Cap at 400 words.\n"
        "Save to Outputs/risk_briefs/globex-<today>.md.\n"
        "If you cannot find current news, say so explicitly rather than\n"
        "guessing."
    )
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "Procurement_Prompts/\n"
        "├── data/\n"
        "│   └── supplier_master.csv\n"
        "└── Outputs/\n"
        "    └── risk_briefs/\n"
        "        └── globex-2026-04-25.md"
    )
    para(doc, "**What you should see.** A 380-word brief, four sections, no padding, ready for the VP's three minutes.")
    para(doc, "**What the strong prompt directed Claude to do.**")
    numbered(doc, "Looked up Globex SA in the supplier master for spend, contract value, and contact.")
    numbered(doc, "Called the web-search tool for current news on Globex SA.")
    numbered(doc, "Computed the supply gap from the data and the current Q4 demand the prompt provided.")
    numbered(doc, "Ranked alternatives by speed-to-qualify, not by cost or preference.")
    numbered(doc, "Ranked actions by speed of impact, not by completeness.")
    numbered(doc, "Held to 380 words because the cap was 400.")
    numbered(doc, "Where current news was thin, said so rather than guessing.")

    # ---------------- 10. First week ----------------
    heading(doc, "10. Your first week with prompt techniques", 1)

    heading(doc, "Day 1 (Monday): the four-part prompt", 2)
    bullet(doc, "Goals: write your first procurement prompt that names inputs, action, output, and constraints.")
    bullet(doc, "Tasks: pick a real task on your desk today. Apply the structure in section 3. Run it. Compare against a one-line version of the same prompt.")
    bullet(doc, "Time budget: 30 minutes.")

    heading(doc, "Day 2 (Tuesday): structured output", 2)
    bullet(doc, "Goals: produce a table with named columns, a row cap, and missing-cell handling.")
    bullet(doc, "Tasks: take Tuesday's first task. Add Pattern 7 (named columns, row cap, 'not detected' for unknowns). Run. Note the difference.")
    bullet(doc, "Time budget: 30 minutes.")

    heading(doc, "Day 3 (Wednesday): persona prompting", 2)
    bullet(doc, "Goals: produce a draft in a specific voice. CFO is the most useful persona to start with.")
    bullet(doc, "Tasks: take a memo or update you wrote last week. Re-run with Pattern 4 (CFO persona). Read the difference. Save the prompt to your library.")
    bullet(doc, "Time budget: 30 minutes.")

    heading(doc, "Day 4 (Thursday): clarifying questions and audit footer", 2)
    bullet(doc, "Goals: get Claude to ask before it acts on a non-routine task. Add an audit footer to a CFO-bound output.")
    bullet(doc, "Tasks: pick a high-stakes task (a savings case, a pre-negotiation brief). Apply Patterns 8 and 10. Save the working prompts to your library.")
    bullet(doc, "Time budget: 60 minutes.")

    heading(doc, "Day 5 (Friday): few-shot and Restart from here", 2)
    bullet(doc, "Goals: classify a list of items consistently using examples. Recover from a drifted long chat.")
    bullet(doc, "Tasks: classify your supplier list (or some other set you score routinely) using Pattern 5. When the chat drifts at any point, use Pattern 9.")
    bullet(doc, "Time budget: 45 minutes.")

    para(doc, "End-of-week reflection: count the prompts you saved to `prompt_library/` this week. Aim for 3 to 5 by Friday. By month three, the library is your most valuable asset and your team's strongest training tool.")

    # ---------------- 11. Twenty-minute sprint ----------------
    heading(doc, "11. The 20-minute prompt-techniques sprint", 1)
    para(
        doc,
        "Use this when you have already worked through one of the other "
        "training guides (Cowork, Code Desktop, or terminal) and you want "
        "your first measurable prompt-quality lift in twenty minutes flat.",
    )

    heading(doc, "Minutes 0 to 5: pick a real task", 2)
    numbered(doc, "Find a real procurement task on your desk that you would write a prompt for today: a memo, a brief, a clause review, a scorecard.")
    numbered(doc, "Save the source files to Master/ if they are not already there.")
    numbered(doc, "Decide which of the five foundational patterns fits (read-only, single-file, multi-file, persona, few-shot).")

    heading(doc, "Minutes 5 to 10: write the four-part prompt", 2)
    numbered(doc, "Use the matching template from section 5.")
    numbered(doc, "Fill in: inputs (with paths), action, output (with path and cap), constraints.")
    numbered(doc, "Read the prompt back to yourself. Any of the four parts missing? Add it.")

    heading(doc, "Minutes 10 to 13: run and read", 2)
    numbered(doc, "Run the prompt.")
    numbered(doc, "Read the output once. Compare against what you would have produced manually.")
    numbered(doc, "If it is right, save it. If not, name the specific gap.")

    heading(doc, "Minutes 13 to 18: refine using one technique", 2)
    numbered(doc, "Pick one of the advanced patterns from section 6 that addresses the gap. Voice off (Pattern 6), structure off (Pattern 7), ambiguity (Pattern 8), drifted (Pattern 9), missing audit (Pattern 10).")
    numbered(doc, "Apply it. Re-run.")

    heading(doc, "Minutes 18 to 20: save what worked", 2)
    numbered(doc, "Copy the working prompt to `prompt_library/<action>_<doctype>.md`.")
    numbered(doc, "Add a one-line note at the top: when to use, what it produced.")
    numbered(doc, "Quit cleanly. The prompt is now reusable next time the same task appears.")

    # ---------------- 12. Team deployment ----------------
    heading(doc, "12. Team deployment: the shared prompt library", 1)
    para(
        doc,
        "Individual prompts are useful. A shared prompt library is "
        "transformative. The first analyst writing /variance-memo costs "
        "60 minutes of careful prompt design. The tenth analyst running "
        "/variance-memo costs eight seconds. The library is where the "
        "compounding value lives.",
    )
    heading(doc, "What goes in the shared library", 2)
    bullet(doc, "**One prompt per S2P task.** /variance-memo, /risk-brief, /nda-review, /scorecard-build, /onboarding-pack, /pre-negotiation-brief, /audit-trail.")
    bullet(doc, "**A prompt for the audit footer.** Reused at the bottom of every CFO-bound output. Stored as `prompt_library/_partials/audit_footer.md`.")
    bullet(doc, "**A prompt for the read-only rule.** Reused as the first line of every prompt. Stored as `prompt_library/_partials/master_readonly.md`.")
    bullet(doc, "**A prompt for the writing-style rules.** Cap, Oxford commas, no hedging, named suppliers, etc. Stored as `prompt_library/_partials/writing_style.md`.")
    heading(doc, "How the team maintains it", 2)
    numbered(doc, "Designate one Claude lead. They own the master library copy on SharePoint or Git.")
    numbered(doc, "When an analyst nails a prompt, they paste it into a draft folder. The Claude lead reviews weekly and promotes the best ones.")
    numbered(doc, "Every promoted prompt has a one-line header: when to use, what it produces, who to ask.")
    numbered(doc, "When a rule changes (a new RAG band, a different scoring weight), the Claude lead updates the partials. Every prompt that references the partial picks up the new rule automatically.")
    numbered(doc, "Quarterly, prune. Drop the prompts nobody used. Keep the library tight.")

    heading(doc, "How shared prompts plug into Code, Cowork, and Web", 2)
    bullet(doc, "**Claude Code (terminal or Desktop):** save each prompt as `.claude/commands/<name>.md`. The team commits to Git. Every analyst gets the same /variance-memo just by syncing.")
    bullet(doc, "**Cowork:** the prompt library lives in `Claude Cowork/PROMPTS/` (synced via SharePoint). Analysts copy-paste into the prompt box. Or save the prompt as a Skill (custom slash command in Cowork) for one-click use.")
    bullet(doc, "**Web (claude.ai):** the prompt library is the same set of Markdown files. Analysts copy-paste into the chat box. Skills work here too on Pro.")

    # ---------------- 13. Quick reference and troubleshooting ----------------
    heading(doc, "13. Quick reference and troubleshooting", 1)

    heading(doc, "The five foundational patterns at a glance", 2)
    fill_table(
        doc,
        ["Pattern", "When to use"],
        [
            ("Read-only review", "Read and report on a file without changing it."),
            ("Single-file edit", "Modify exactly one file, leave the rest untouched."),
            ("Multi-file build", "Combine inputs from multiple files into one new artefact."),
            ("Persona prompting", "Output in a specific voice (CFO, junior analyst, board chair)."),
            ("Few-shot examples", "Demonstrate desired output rather than describe it."),
        ],
    )

    heading(doc, "The five advanced patterns at a glance", 2)
    fill_table(
        doc,
        ["Pattern", "When to use"],
        [
            ("Voice matching", "Match your team's voice from sample memos."),
            ("Structured output", "Named columns, row caps, explicit missing-cell handling."),
            ("Clarifying questions first", "Non-routine task; let Claude ask before guessing."),
            ("Restart from here", "A long chat has drifted; correct at the divergence point."),
            ("Audit footer", "Any output bound for a CFO, board, auditor, or counterparty."),
        ],
    )

    heading(doc, "Common prompt failures and the matching fix", 2)
    bullet(doc, "**Symptom:** output is generic, no specific suppliers or figures. **Fix:** add the constraint 'every figure must trace to a source row; every supplier named as legal entity'.")
    bullet(doc, "**Symptom:** output is twice as long as you wanted. **Fix:** add a word or row cap. 'Cap at 600 words' or 'Cap the table at 10 rows'.")
    bullet(doc, "**Symptom:** Claude rewrote a master file. **Fix:** restore from version history, then add 'Master/ is read-only. Do not modify any file in Master/.' as the first line of every prompt in this folder.")
    bullet(doc, "**Symptom:** the chat is 30 messages deep and Claude is forgetting the early context. **Fix:** Pattern 9 (Restart from here). Edit the original prompt at the divergence point.")
    bullet(doc, "**Symptom:** the output uses an AI tone (hedging, no headlines, padded). **Fix:** Pattern 6 (voice matching) with three of your own samples. Or Pattern 4 (persona prompting) with the CFO persona.")
    bullet(doc, "**Symptom:** Claude invented a supplier name or a figure. **Fix:** add the constraint 'do not invent. If a value is missing in the source, write \"not detected\"'.")
    bullet(doc, "**Symptom:** the output looks fine but the CFO bounces it for lack of audit trail. **Fix:** Pattern 10 (audit footer) on every CFO-bound output.")
    bullet(doc, "**Symptom:** Claude produced five tasks' worth of output and none of them are good. **Fix:** anti-pattern, Five Tasks in One Prompt. Split into separate prompts.")

    heading(doc, "Essential resources", 2)
    bullet(doc, "**The course CLAUDE.md.** The writing rules and procurement-specific anti-AI rules referenced throughout this guide.")
    bullet(doc, "**docs/Prompt_Library.md** in the course root. The reference shapes (read-only, single-file, multi-file).")
    bullet(doc, "**docs/Folder_Structure.md** in the course root. The standard folder layout (Master, Drafts, Outputs, Reference, Archive).")
    bullet(doc, "**Lesson 02 (Token Efficiency)** in the course Lessons/. Pairs with this guide; the prompt techniques here also save tokens.")

    doc.save(str(OUTPUT_PATH))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
