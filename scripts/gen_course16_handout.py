"""
Generate comprehensive Course 16 Sourcing Sprint handout.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
HANDOUT_PATH = PROJECT_DIR / "Handouts" / "Course_16_Sourcing_Sprint_Handout.docx"


def set_cell_shading(cell, color):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)


def make_table_compact(table, font_size=10):
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_before = Pt(2)
                paragraph.paragraph_format.space_after = Pt(2)
                for run in paragraph.runs:
                    run.font.size = Pt(font_size)
                    run.font.name = 'Calibri'


def shade_header_row(table, color='2E4057'):
    for cell in table.rows[0].cells:
        set_cell_shading(cell, color)
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                run.bold = True


def add_code_block(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.3)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), 'F0F0F0')
    shading.set(qn('w:val'), 'clear')
    run_element = run._element
    rPr = run_element.get_or_add_rPr()
    rPr.append(shading)
    return p


def add_bold_text(doc, bold_part, normal_part):
    p = doc.add_paragraph()
    run_b = p.add_run(bold_part)
    run_b.bold = True
    run_b.font.size = Pt(11)
    run_b.font.name = 'Calibri'
    run_n = p.add_run(normal_part)
    run_n.font.size = Pt(11)
    run_n.font.name = 'Calibri'
    return p


def add_why_matters(doc, text):
    p = doc.add_paragraph()
    run_b = p.add_run("Why this matters. ")
    run_b.bold = True
    run_b.font.size = Pt(11)
    run_b.font.name = 'Calibri'
    run_n = p.add_run(text)
    run_n.font.size = Pt(11)
    run_n.font.name = 'Calibri'
    return p


def add_what_to_learn(doc, text):
    p = doc.add_paragraph()
    run_b = p.add_run("What to learn from this. ")
    run_b.bold = True
    run_b.font.size = Pt(11)
    run_b.font.name = 'Calibri'
    run_n = p.add_run(text)
    run_n.font.size = Pt(11)
    run_n.font.name = 'Calibri'
    return p


def build():
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # Heading styles
    for i in range(4):
        style_name = f'Heading {i+1}'
        if style_name in [s.name for s in doc.styles]:
            hs = doc.styles[style_name]
            hs.font.name = 'Calibri'

    # ============================================================
    # HEADER
    # ============================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('U2xAI')
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Calibri'
    run.font.color.rgb = RGBColor(0x2E, 0x40, 0x57)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('PROCUREAI ACADEMY')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Calibri'
    run.font.color.rgb = RGBColor(0x2E, 0x40, 0x57)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Series 2 (Engineering Track) | Course 16')
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_heading('Sourcing Sprint', level=0)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        'Running a competitive sourcing event from category analysis '
        'through award recommendation.'
    )
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    run.italic = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('5 lessons. About 5 hours total. No coding required.')
    run.font.size = Pt(10)
    run.font.name = 'Calibri'

    # ============================================================
    # 1. HOW TO USE THIS HANDOUT
    # ============================================================
    doc.add_heading('1. How to use this handout', level=1)

    doc.add_paragraph(
        'This handout is your reading companion for Course 16: Sourcing Sprint. '
        'The hands-on work happens in the course folder you received with the '
        'training materials, located at '
        'Detailed Course Content/Course_16_Sourcing_Sprint/practice/.'
    )

    doc.add_paragraph(
        'Read this handout before you open the course folder. It explains the '
        'full sourcing sprint workflow, shows you what every file does, and gives '
        'you worked examples you can reference while you work through the lessons. '
        'When you hit a problem, check the troubleshooting section at the end.'
    )

    doc.add_paragraph('How to read this guide:')

    steps = [
        'Read sections 2 and 3 to understand what the course covers and what '
        'is in the folder.',
        'Read section 4 (time savings table) to see the business case for using '
        'Claude Code (in the terminal) for sourcing events.',
        'Read section 5 to understand what a sourcing sprint is and how the five '
        'stages connect.',
        'Study the worked examples in section 6. Each one shows the prompt, the '
        'folder layout, the expected output, and what Claude Code did behind the '
        'scenes.',
        'Read section 7 (Day in the Life) to see how a real sourcing manager uses '
        'this workflow across a full workday.',
        'Use sections 8, 9, and 10 for your first session, your first week, and '
        'the pattern to apply on your own events.',
        'Check section 11 (troubleshooting) when something does not look right.',
    ]
    for i, s in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {s}')

    # ============================================================
    # 2. WHAT THIS COURSE TEACHES
    # ============================================================
    doc.add_heading('2. What this course teaches', level=1)

    doc.add_paragraph(
        'A Senior Category Manager at a US industrial company has six weeks to '
        'run a competitive sourcing event covering $22.2M in direct materials '
        'spend. The event spans six sub-categories (steel, polymers, aluminum, '
        'electronic components, fasteners, and coatings) across 10 active '
        'suppliers and 2 prospective ones. The CPO wants the award recommendation '
        'on her desk before the board meets. Normally, this takes 8 to 10 weeks. '
        'The course compresses it to six.'
    )

    doc.add_paragraph(
        'Course 16 teaches you to use Claude Code (in the terminal) to execute '
        'each stage of that sprint: ingest spend data and build a category '
        'context summary, generate an RFP package from scope notes, create a '
        'standardized supplier response template, process and score six bids '
        'against weighted evaluation criteria, and draft a VP-ready award '
        'recommendation memo. Five lessons, five stages, one complete sourcing '
        'event.'
    )

    doc.add_paragraph(
        'By the end, you will have a repeatable system. Every future sourcing '
        'event follows the same folder structure, the same prompt patterns, and '
        'the same scoring logic. The system is portable. Copy the folder, swap '
        'the data, and you are running a new event.'
    )

    doc.add_heading('The practice scenario', level=2)

    doc.add_paragraph(
        'Ironbridge Manufacturing is a US-based industrial company. You are Sarah '
        'Chen, the Senior Category Manager, reporting to Tom Baker (Supply Chain '
        'Director). Lisa Torres (VP of Procurement) approves the award. The CPO '
        'deadline is 2026-06-20. The board meets 2026-06-25.'
    )

    doc.add_paragraph('The sourcing event covers six sub-categories:')

    # Sub-category table
    tbl = doc.add_table(rows=7, cols=4)
    tbl.style = 'Table Grid'
    headers = [
        'Sub-category', 'Current annual spend',
        'Incumbent supplier', 'Key issue',
    ]
    for i, h in enumerate(headers):
        tbl.rows[0].cells[i].text = h
    data = [
        ['Steel', '$4,200,000', 'Great Lakes Steel (SUP001)',
         'Single source, price volatility'],
        ['Polymers', '$3,800,000', 'Heartland Polymers (SUP002)',
         'Long lead times'],
        ['Aluminum', '$3,400,000', 'Pacific Aluminum (SUP003)',
         'Quality consistent, pricing competitive'],
        ['Electronic components', '$2,900,000', 'Apex Electronics (SUP004)',
         'Declining quality scores, at risk'],
        ['Fasteners', '$2,100,000', 'Cascade Fasteners (SUP005)',
         'Reliable but above-market pricing'],
        ['Coatings', '$1,600,000', 'Various',
         'Fragmented supply base'],
    ]
    for r, row_data in enumerate(data, 1):
        for c, val in enumerate(row_data):
            tbl.rows[r].cells[c].text = val
    shade_header_row(tbl)
    make_table_compact(tbl)

    doc.add_paragraph('')

    doc.add_paragraph(
        'Six suppliers submitted bids: Great Lakes Steel, Heartland Polymers, '
        'Pacific Aluminum, Cascade Fasteners, Northland Alloys (new), and '
        'Bayshore Materials (new). Evaluation criteria are: price competitiveness '
        '(35%), quality and reliability (25%), delivery performance (20%), '
        'innovation and value-add (10%), and financial stability (10%).'
    )

    # ============================================================
    # 3. WHAT IS IN THE COURSE FOLDER
    # ============================================================
    doc.add_heading('3. What is in the course folder', level=1)

    doc.add_paragraph(
        'The course folder is self-contained. Everything you need is inside. No '
        'external downloads, no shared drives, no separate data files. Copy the '
        'folder to your machine and you are ready to start.'
    )

    add_code_block(doc,
        'Course_16_Sourcing_Sprint/\n'
        '  README.md                    Course navigation and how to start\n'
        '  COURSE_OVERVIEW.md           The scenario, what you produce, rubric\n'
        '  lessons/\n'
        '    Lesson_01_Category_Context.md\n'
        '    Lesson_02_RFP_Package.md\n'
        '    Lesson_03_Response_Template.md\n'
        '    Lesson_04_Bid_Processing.md\n'
        '    Lesson_05_Award_Recommendation.md\n'
        '  practice/\n'
        '    CLAUDE.md                  Role, criteria, stakeholders, standards\n'
        '    data/\n'
        '      spend-baseline.csv       356 rows, 12 months direct materials\n'
        '      supplier-longlist.csv    12 suppliers (10 active, 2 prospective)\n'
        '      scope-notes.md           Event scope, objectives, timeline\n'
        '      bid-responses/           6 supplier bid files\n'
        '    outputs/                   Where your deliverables land\n'
        '    skills/\n'
        '      score-bid-response.md    Reusable bid scoring pattern\n'
        '  solutions/\n'
        '    rfp_package_solution.md\n'
        '    bid_scorecard_solution.md\n'
        '    award_recommendation_solution.md\n'
        '  scripts/\n'
        '    build_course_data.py       Regenerates all practice data'
    )

    doc.add_heading('Key files explained', level=2)

    add_bold_text(doc, 'CLAUDE.md (in practice/). ',
        'This file tells Claude Code (in the terminal) who you are, what files '
        'are read-only, what the evaluation criteria are, who the stakeholders '
        'are, and how to format outputs. Claude Code reads this file automatically '
        'every time you start a session in the practice/ folder.'
    )
    add_why_matters(doc,
        'Without CLAUDE.md, Claude Code has no context. It would not know the '
        'evaluation weights, the savings target, or the stakeholder names. Every '
        'prompt would need to repeat that context. With it, you type shorter '
        'prompts and get outputs that match your event from the first try.'
    )

    add_bold_text(doc, 'spend-baseline.csv (356 rows). ',
        'Twelve months of purchase order data across six sub-categories. Fields '
        'include transaction date, supplier name, item description, quantity, '
        'unit price, total amount, and category. This is the baseline against '
        'which all bids are compared.'
    )
    add_why_matters(doc,
        'The spend baseline is your negotiation anchor. If a supplier bids $720 '
        'per ton for steel and your baseline average is $724 per ton, the savings '
        'calculation comes directly from this file. Without it, Claude Code '
        'cannot compute savings or flag above-baseline bids.'
    )

    add_bold_text(doc, 'supplier-longlist.csv (12 suppliers). ',
        'Each row has the supplier ID, legal name, city, state, tier '
        'classification, annual spend, status (active or prospective), capability '
        'match, and risk rating. This file separates incumbents from new entrants.'
    )
    add_why_matters(doc,
        'Sourcing events need to know who is new and who is incumbent. The '
        'longlist lets Claude Code flag single-source risks and identify where '
        'adding a new supplier reduces concentration. Without it, the category '
        'context summary would miss the new entrant opportunity.'
    )

    add_bold_text(doc, 'bid-responses/ (6 files). ',
        'Each file contains one supplier bid with pricing, delivery commitments, '
        'quality certifications, payment terms, and value-add proposals. These '
        'arrive after the RFP closes. Claude Code reads all six and scores them '
        'against the weighted criteria in CLAUDE.md.'
    )
    add_why_matters(doc,
        'Processing six bids manually takes 6 to 8 hours: opening each file, '
        'extracting pricing, reading technical responses, building a comparison '
        'spreadsheet. Claude Code reads all six in one prompt and applies '
        'consistent scoring. The time drops to about 30 minutes.'
    )

    add_bold_text(doc, 'score-bid-response.md (in skills/). ',
        'A reusable skill file that defines the bid scoring pattern. It tells '
        'Claude Code how to read a bid file, extract pricing and technical data, '
        'apply the evaluation weights, and write a scorecard. The skill works '
        'across different sourcing events because it names input shapes, not '
        'specific values.'
    )
    add_why_matters(doc,
        'Skills are what make the system reusable. This skill says "read every '
        'file in bid-responses/" and "apply the weights from CLAUDE.md." It does '
        'not say "read Great Lakes Steel" or "use 35% for price." Swap the data '
        'and the weights, and the same skill scores a different event.'
    )

    add_bold_text(doc, 'solutions/ folder. ',
        'Reference answers for the RFP package, a sample bid scorecard, and the '
        'award recommendation. Look at these only after you attempt each lesson. '
        'The learning happens in the attempt.'
    )
    add_why_matters(doc,
        'Solutions let you check your work against a known-good output. If your '
        'scorecard gives Great Lakes Steel a total weighted score of 80.8 and the '
        'solution shows 80.6, you know you are close. If you are off by 15 '
        'points, something in your prompt or criteria application went wrong.'
    )

    # ============================================================
    # 4. TIME SAVINGS TABLE
    # ============================================================
    doc.add_heading('4. Time savings reference table', level=1)

    doc.add_paragraph(
        'These estimates come from the Ironbridge Manufacturing practice '
        'scenario. Your actual times will vary by data volume and complexity, '
        'but the ratios hold. Claude Code (in the terminal) handles the '
        'extraction, calculation, and drafting. You handle the review, judgment, '
        'and stakeholder communication.'
    )

    tbl = doc.add_table(rows=6, cols=3)
    tbl.style = 'Table Grid'
    headers = [
        'Task',
        'Without Claude Code',
        'With Claude Code (in the terminal)',
    ]
    for i, h in enumerate(headers):
        tbl.rows[0].cells[i].text = h
    savings_data = [
        [
            'Category context summary from 356-row spend file and '
            '12-supplier longlist',
            '3 to 4 hours (pivot tables, cross-referencing, drafting)',
            '25 minutes (one session, review the output)',
        ],
        [
            'RFP package generation (6 sections, scope through terms)',
            '2 to 3 days (multiple authors, review rounds, '
            'inconsistencies)',
            '40 minutes (one chained session, consistent '
            'cross-references)',
        ],
        [
            'Supplier response template aligned to evaluation criteria',
            '2 to 3 hours (designing formats, writing instructions, '
            'testing)',
            '30 minutes (template, instructions, and sample bid in '
            'one session)',
        ],
        [
            'Bid processing and scoring for 6 suppliers against 5 '
            'weighted criteria',
            '6 to 8 hours (manual extraction, spreadsheet scoring, '
            'consistency checks)',
            '35 minutes (all 6 bids validated, scored, and ranked '
            'in one pass)',
        ],
        [
            'Award recommendation memo with savings analysis and '
            'objection responses',
            '4 to 6 hours (pulling data, drafting narrative, building '
            'savings case)',
            '30 minutes (scored data assembled into VP-ready memo '
            'with risk section)',
        ],
    ]
    for r, row_data in enumerate(savings_data, 1):
        for c, val in enumerate(row_data):
            tbl.rows[r].cells[c].text = val
    shade_header_row(tbl)
    make_table_compact(tbl, 9.5)

    doc.add_paragraph('')
    doc.add_paragraph(
        'Total for all five tasks: 18 to 25 hours without Claude Code. About '
        '2.5 hours with Claude Code. The difference is not speed alone. It is '
        'consistency. Claude Code applies the same scoring rubric to every bid, '
        'the same formatting to every section, and the same baseline to every '
        'savings calculation.'
    )

    # ============================================================
    # 5. WHAT A SOURCING SPRINT IS
    # ============================================================
    doc.add_heading('5. What a sourcing sprint is', level=1)

    doc.add_paragraph(
        'A sourcing sprint is a time-boxed competitive sourcing event that moves '
        'from category analysis through award recommendation in a structured '
        'sequence. Each stage produces a specific deliverable. The next stage '
        'consumes that deliverable as input. Nothing is ad hoc. Nothing is '
        'drafted from memory. Every output traces back to data.'
    )

    doc.add_heading('Stage 1: Category context ingestion', level=2)

    doc.add_paragraph(
        'You start with raw data: a spend export from the ERP, a supplier '
        'longlist, and scope notes from the business. Claude Code (in the '
        'terminal) reads the spend CSV, calculates totals by sub-category and '
        'by supplier, flags concentration risks and single-source positions, '
        'and identifies new entrants from the longlist. The output is a one-page '
        'category context summary addressed to your stakeholders. It quantifies '
        'where the spend is, where the risk is, and where the cost reduction '
        'opportunity sits.'
    )
    add_why_matters(doc,
        'Category context is the foundation of every decision in the event. If '
        'you do not know that Great Lakes Steel holds 100% of the steel '
        'sub-category ($4.2M), you cannot assess the risk of switching suppliers. '
        'If you do not know that Northland Alloys is on the longlist as a '
        'prospective steel supplier, you miss the dual-source opportunity.'
    )

    doc.add_heading('Stage 2: RFP package generation', level=2)

    doc.add_paragraph(
        'With the category context confirmed, Claude Code generates the RFP. It '
        'reads the scope notes, spend data, and evaluation criteria from '
        'CLAUDE.md, then writes the cover letter, scope of work, pricing template '
        'structure, evaluation criteria section, submission instructions, and '
        'terms and conditions. All six sections are generated in one chained '
        'session. Cross-references stay consistent because one model wrote every '
        'section from the same source data.'
    )
    add_why_matters(doc,
        'RFPs with multiple authors always have inconsistencies. The scope '
        'section says "24-month term" but the terms section says "36 months." '
        'The pricing template lists 12 part numbers but the scope lists 18. When '
        'Claude Code writes all sections from the same data, these mismatches '
        'disappear. You review for judgment calls, not for typos.'
    )

    doc.add_heading('Stage 3: Supplier response template', level=2)

    doc.add_paragraph(
        'Before bids arrive, you need a template that forces structured, '
        'machine-readable answers. Claude Code creates a pricing CSV with '
        'pre-populated part numbers and blank supplier columns, a technical '
        'questionnaire mapped to the evaluation criteria, and supplier '
        'instructions. The template is designed so that Lesson 4 can process '
        'every bid automatically. No manual data extraction.'
    )
    add_why_matters(doc,
        'If suppliers return 47-page PDFs with pricing buried on page 23, you '
        'spend an hour per bid extracting comparable data. With a structured '
        'template, every bid arrives in the same format. Claude Code reads all '
        'six in one pass. The template is not just a convenience. It is the '
        'automation enabler.'
    )

    doc.add_heading('Stage 4: Bid processing and scoring', level=2)

    doc.add_paragraph(
        'Six bids arrive. Claude Code reads all six, validates each against the '
        'template rules (all columns present, no blank pricing, arithmetic '
        'checks), scores pricing against the spend baseline, evaluates technical '
        'responses against the criteria, applies the weighted scoring model, and '
        'produces a ranked evaluation matrix. The lowest bidder gets a pricing '
        'score of 100. Others are scored proportionally. Technical scores use a '
        'rubric: specific certifications and data score 80 to 100, general '
        'statements with some evidence score 50 to 79, vague or missing answers '
        'score 0 to 49.'
    )
    add_why_matters(doc,
        'Manual bid scoring is slow and inconsistent. One evaluator gives a '
        'vague answer 70 points. Another gives the same answer 45. Claude Code '
        'applies the same rubric to every response. If you ask it to re-score, '
        'you can require: "If Supplier A scores 45 for a vague answer on T3, '
        'Supplier B scores the same for an equally vague answer." Consistency '
        'is auditable.'
    )

    doc.add_heading('Stage 5: Award recommendation', level=2)

    doc.add_paragraph(
        'Claude Code reads the evaluation matrix, pricing comparison, and '
        'technical scores, then writes a seven-section award recommendation: '
        'executive summary, evaluation results table, recommended supplier '
        'profile, savings analysis, anticipated objections with data-backed '
        'responses, risk assessment, and a clear recommendation statement. The '
        'document names the recommended supplier (the legal entity, not "the '
        'winner"), the total contract value, the expected savings versus baseline '
        '($2.1M, equal to 9.5% of the $22.2M spend), and the decision deadline '
        '(2026-06-20).'
    )
    add_why_matters(doc,
        'A recommendation that says "Supplier A scored highest" does not survive '
        'a CPO meeting. The CPO will ask "Why not the incumbent?" and "What if '
        'the second-place supplier challenges?" The memo must anticipate these '
        'objections and answer them with specific scores, dollar amounts, and '
        'risk mitigations. Claude Code builds those answers from the scored data, '
        'not from memory.'
    )

    # ============================================================
    # 6. WORKED EXAMPLES
    # ============================================================
    doc.add_heading('6. Worked examples', level=1)

    doc.add_paragraph(
        'Each worked example has four parts: the prompt you type in Claude Code '
        '(in the terminal), the folder layout, what you should see when it '
        'succeeds, and what Claude Code did behind the scenes.'
    )

    # --- Example 1: Category Context ---
    doc.add_heading(
        'Example 1: Build the category context summary', level=2
    )

    doc.add_paragraph(
        'This is the first deliverable in the sourcing sprint. You take 356 '
        'rows of spend data, a 12-supplier longlist, and scope notes. You end '
        'up with a one-page briefing that shows spend by sub-category, risk '
        'flags, new entrant opportunities, and cost reduction observations. The '
        'briefing goes to Tom Baker and Lisa Torres before the kick-off call.'
    )

    doc.add_heading('The prompt to type', level=3)

    add_code_block(doc,
        'Read data/spend-baseline.csv. Calculate total spend by sub-category\n'
        'and by supplier. For each sub-category, show: the sub-category name,\n'
        'total USD spend, share of the $22.2M total, and the name and spend of\n'
        'the top supplier. Sort from highest to lowest. Then flag any\n'
        'sub-category where a single supplier holds 80% or more of spend. Read\n'
        'data/supplier-longlist.csv and list every supplier not in the spend\n'
        'data (these are new entrants). Read data/scope-notes.md and summarize\n'
        'the scope. Finally, write a one-page category context summary with a\n'
        'spend table, risk flags, new entrant list, and three cost reduction\n'
        'observations. Address it to Tom Baker and Lisa Torres. Date it\n'
        '2026-04-25. Save as outputs/category-context-v1.md.'
    )

    doc.add_heading('The folder layout', level=3)

    add_code_block(doc,
        'practice/\n'
        '  CLAUDE.md\n'
        '  data/\n'
        '    spend-baseline.csv       (356 rows, read-only)\n'
        '    supplier-longlist.csv    (12 suppliers, read-only)\n'
        '    scope-notes.md           (read-only)\n'
        '  outputs/\n'
        '    category-context-v1.md   (created by Claude Code)'
    )

    doc.add_heading('What you should see', level=3)

    doc.add_paragraph(
        'Claude Code saves outputs/category-context-v1.md. The file contains a '
        'spend table with six rows (one per sub-category) totaling $22.2M. Steel '
        'is flagged as single source (Great Lakes Steel, 100%, $4.2M). Polymers '
        'is flagged as concentration risk (Heartland Polymers, 94%). Northland '
        'Alloys and Bayshore Materials appear as new entrants. Three cost '
        'reduction observations each name a sub-category, a dollar figure, and '
        'a percentage range.'
    )

    doc.add_heading('What Claude Code did, behind the scenes', level=3)

    behind_scenes_1 = [
        'Opened spend-baseline.csv and parsed all 356 rows. Read the '
        'sub-category, supplier name, and spend amount columns.',
        'Grouped rows by sub-category. Summed spend per group. Calculated each '
        'group as a share of the $22.2M total.',
        'Within each sub-category, found the supplier with the highest spend. '
        'Computed their share. Flagged groups where one supplier held 80% or '
        'more, or where only one supplier appeared.',
        'Opened supplier-longlist.csv. Extracted all 12 names. Compared them '
        'against distinct supplier names in the spend data. Names with no match '
        'became the new entrant list.',
        'Opened scope-notes.md as plain text. Identified lines for in-scope '
        'items, out-of-scope items, and constraints.',
        'Combined all five outputs into a business-memo format with addressee, '
        'date, labeled sections, and three cost reduction observations that each '
        'name a sub-category, a spend figure, and a percentage range. Saved to '
        'outputs/.',
    ]
    for i, step in enumerate(behind_scenes_1, 1):
        doc.add_paragraph(f'{i}. {step}')

    # --- Example 2: Score all bids ---
    doc.add_heading(
        'Example 2: Process and score six supplier bids', level=2
    )

    doc.add_paragraph(
        'Six bids have arrived in bid-responses/. Each contains pricing, '
        'delivery commitments, quality certifications, and value-add proposals. '
        'You need every bid validated, scored against five weighted criteria, and '
        'ranked in a single evaluation matrix. This is Lesson 4 in the course.'
    )

    doc.add_heading('The prompt to type', level=3)

    add_code_block(doc,
        'Read every file in data/bid-responses/. For each bid, validate:\n'
        '(1) all required columns present, (2) no blank pricing values,\n'
        '(3) arithmetic checks on totals. Then score each bid against the\n'
        'evaluation criteria in CLAUDE.md: price competitiveness (35%),\n'
        'quality and reliability (25%), delivery performance (20%),\n'
        'innovation and value-add (10%), financial stability (10%). For\n'
        'pricing, the lowest total bid gets 100 and others are scored\n'
        'proportionally. For technical criteria, use the rubric: specific\n'
        'certifications and data = 80-100, general statements with evidence\n'
        '= 50-79, vague or missing = 0-49. Write a scorecard for each\n'
        'supplier to outputs/bid-scorecards/scorecard-SUPNNN.md. Write a\n'
        'summary evaluation matrix to outputs/scoring-summary.md. Rank\n'
        'suppliers by weighted total score, highest first.'
    )

    doc.add_heading('The folder layout', level=3)

    add_code_block(doc,
        'practice/\n'
        '  CLAUDE.md\n'
        '  data/\n'
        '    spend-baseline.csv            (baseline for pricing comparison)\n'
        '    bid-responses/\n'
        '      great-lakes-steel.md\n'
        '      heartland-polymers.md\n'
        '      pacific-aluminum.md\n'
        '      cascade-fasteners.md\n'
        '      northland-alloys.md\n'
        '      bayshore-materials.md\n'
        '  outputs/\n'
        '    bid-scorecards/\n'
        '      scorecard-SUP001.md         (created by Claude Code)\n'
        '      scorecard-SUP002.md         (created by Claude Code)\n'
        '      ...one per supplier...\n'
        '    scoring-summary.md            (created by Claude Code)'
    )

    doc.add_heading('What you should see', level=3)

    doc.add_paragraph(
        'Claude Code creates six scorecard files in outputs/bid-scorecards/ and '
        'one scoring-summary.md. The summary contains a table with all six '
        'suppliers ranked by weighted total. For Great Lakes Steel, the scorecard '
        'shows: price 78, quality 85, delivery 82, innovation 70, financial 88, '
        'total weighted score 80.8. Pacific Aluminum leads with 82.4. Bayshore '
        'Materials trails at 70.4. Each scorecard includes the supplier legal '
        'name, the total bid value, and one-sentence justifications for each '
        'criterion score.'
    )

    doc.add_heading('What Claude Code did, behind the scenes', level=3)

    behind_scenes_2 = [
        'Opened each of the six bid files in bid-responses/ and parsed pricing '
        'sections, delivery commitments, quality certifications, and value-add '
        'proposals.',
        'Validated each bid: checked for required fields, confirmed no blank '
        'pricing, and verified arithmetic (unit price times volume equals total, '
        'within $1 tolerance).',
        'Loaded baseline average prices from spend-baseline.csv. Calculated each '
        'supplier total bid value. Applied proportional pricing scores: lowest '
        'total gets 100, others get 100 times (lowest total divided by their '
        'total).',
        'Evaluated technical responses using the rubric. Suppliers with ISO '
        'certifications, specific defect rates, and named references scored 80 '
        'to 100. Suppliers with general capability statements scored 50 to 79.',
        'Applied the five evaluation weights from CLAUDE.md to each supplier '
        'score set. Calculated weighted totals. Sorted highest to lowest.',
        'Wrote individual scorecards to outputs/bid-scorecards/ and compiled the '
        'ranked summary table to outputs/scoring-summary.md.',
    ]
    for i, step in enumerate(behind_scenes_2, 1):
        doc.add_paragraph(f'{i}. {step}')

    # --- Example 3: Award recommendation ---
    doc.add_heading(
        'Example 3: Draft the award recommendation memo', level=2
    )

    doc.add_paragraph(
        'You have the evaluation matrix. The CPO meeting is Friday. You need a '
        'seven-section award recommendation that names the recommended supplier, '
        'states the savings, anticipates objections, and presents the risk '
        'assessment. This is Lesson 5.'
    )

    doc.add_heading('The prompt to type', level=3)

    add_code_block(doc,
        'Read outputs/scoring-summary.md and all scorecards in\n'
        'outputs/bid-scorecards/. Write an award recommendation to\n'
        'outputs/award-recommendation.md with these sections:\n'
        '1. Executive summary (recommended supplier, contract value,\n'
        '   savings vs baseline, decision deadline 2026-06-20).\n'
        '2. Evaluation results table (all 6 suppliers ranked).\n'
        '3. Recommended supplier profile.\n'
        '4. Savings analysis (total annual, by sub-category, projected\n'
        '   over 24-month term).\n'
        '5. Anticipated objections (3 max, each with data-backed\n'
        '   response).\n'
        '6. Risk assessment (3 risks with likelihood, impact,\n'
        '   mitigation).\n'
        '7. Recommendation statement.\n'
        'Address to Lisa Torres, VP of Procurement. No more than three\n'
        'recommendations. Every number must trace to the scored data.'
    )

    doc.add_heading('The folder layout', level=3)

    add_code_block(doc,
        'practice/\n'
        '  CLAUDE.md\n'
        '  data/\n'
        '    spend-baseline.csv\n'
        '  outputs/\n'
        '    scoring-summary.md\n'
        '    bid-scorecards/               (6 scorecards from Example 2)\n'
        '    award-recommendation.md       (created by Claude Code)'
    )

    doc.add_heading('What you should see', level=3)

    doc.add_paragraph(
        'Claude Code saves outputs/award-recommendation.md. The executive '
        'summary recommends awarding the direct materials contract with a split: '
        'Great Lakes Steel for steel, Heartland Polymers for polymers, Pacific '
        'Aluminum for aluminum, Cascade Fasteners for fasteners and coatings, '
        'and a dual-source for electronic components (Apex Electronics 60%, '
        'Northland Alloys 40%). Total contract value: $20.1M per year. Savings: '
        '$2.1M annually (9.5% reduction against the $22.2M baseline). Decision '
        'deadline: 2026-06-25 (board meeting). Three recommendations, no more. '
        'Three risks with specific mitigations.'
    )

    doc.add_heading('What Claude Code did, behind the scenes', level=3)

    behind_scenes_3 = [
        'Read the scoring summary and all six scorecards. Identified Pacific '
        'Aluminum as the top-ranked supplier by weighted score (82.4), followed '
        'by Cascade Fasteners (80.8) and Great Lakes Steel (80.6).',
        'Pulled each supplier total bid value from the scorecards. Calculated '
        'total contract value by summing the recommended awards across '
        'sub-categories.',
        'Computed savings against the $22.2M baseline: $22.2M minus $20.1M '
        'equals $2.1M, or 9.5%. Broke savings down by sub-category.',
        'Generated three anticipated objections by analyzing the data: incumbent '
        'preference (the current supplier scored lower but has history), close '
        'competition (Pacific Aluminum vs. Cascade Fasteners, a 1.6-point gap), '
        'and new supplier risk (Northland Alloys has no prior relationship). '
        'Backed each response with specific scores and dollar amounts.',
        'Assessed three transition risks (production disruption during 8-week '
        'transition, quality variance during ramp-up, Northland Alloys financial '
        'stability at a 72 score) with likelihood ratings and mitigations (pilot '
        'order, quality gate at first article, staged volume transfer).',
        'Compiled all sections into the seven-part structure addressed to Lisa '
        'Torres. Capped recommendations at three per CLAUDE.md rules.',
    ]
    for i, step in enumerate(behind_scenes_3, 1):
        doc.add_paragraph(f'{i}. {step}')

    # ============================================================
    # 7. DAY IN THE LIFE
    # ============================================================
    doc.add_heading(
        '7. A day in the life: Tom, Strategic Sourcing Manager', level=1
    )

    doc.add_paragraph(
        'Tom Bradshaw is a Strategic Sourcing Manager at Clearwater Industrial, '
        'a US-based manufacturer with $35M in annual indirect and direct '
        'materials spend. He manages three active sourcing events and one in '
        'planning. He has been using Claude Code (in the terminal) for two '
        'months. This is a Tuesday in mid-May. His team of two analysts is in '
        'training this week. He is running the desk alone.'
    )

    # Scenario 1
    doc.add_heading('07:45 - CPO needs a spend summary before 09:00', level=3)

    doc.add_paragraph(
        'Tom opens his email. Julia Reeves, the CPO, forwarded a message from '
        'the CFO: "I need the Q2 indirect spend breakdown by category before the '
        '09:00 leadership call. Which categories are over budget?" Tom has 75 '
        'minutes. The spend file is a 1,200-row export from SAP, sitting in his '
        'Downloads folder.'
    )

    doc.add_paragraph(
        'Tom copies the file into his project folder and opens a terminal.'
    )

    add_code_block(doc,
        'cd Clearwater_Indirect_Q2\n'
        'claude\n\n'
        'Read data/spend-export-q2.csv. Calculate total spend by category.\n'
        'For each category, show actual spend, budget, and variance (over or\n'
        'under). Flag any category more than 10% over budget. Sort by variance\n'
        'descending. Save as outputs/q2-spend-summary.md. Address to Julia\n'
        'Reeves, CPO. Date 2026-05-12.'
    )

    doc.add_paragraph(
        'Claude Code reads the 1,200 rows, groups by category, calculates '
        'variances, and saves the summary. Total time: 8 minutes. Tom reviews '
        'the output, confirms MRO is 14% over budget ($420,000 variance), and '
        'forwards the file to Julia at 07:58.'
    )

    add_what_to_learn(doc,
        'Claude Code is strongest for time-sensitive data summaries. The prompt '
        'names the file, the calculation, the format, and the recipient. Tom did '
        'not write a pivot table or format a spreadsheet. He typed one prompt, '
        'reviewed the output, and sent it. The pattern works for any spend file '
        'and any stakeholder.'
    )

    # Scenario 2
    doc.add_heading(
        '09:30 - Three new bids arrived overnight', level=3
    )

    doc.add_paragraph(
        'Tom is running a sourcing event for packaging materials. Three bids '
        'arrived overnight. He needs them validated, scored, and compared before '
        'his 14:00 review with the category lead. The bids are in his '
        'bid-responses/ folder. His CLAUDE.md already has the evaluation '
        'criteria: price (40%), quality (25%), delivery (20%), and sustainability '
        '(15%).'
    )

    add_code_block(doc,
        'cd Packaging_Sourcing_2026\n'
        'claude\n\n'
        'Read every file in data/bid-responses/. Validate each bid against\n'
        'the template rules in CLAUDE.md. Score each bid on price, quality,\n'
        'delivery, and sustainability using the weights in CLAUDE.md. Write\n'
        'a scorecard for each supplier to outputs/bid-scorecards/. Write a\n'
        'ranked summary to outputs/scoring-summary.md.'
    )

    doc.add_paragraph(
        'Claude Code processes all three bids in one pass. Two pass validation. '
        'One has a blank sustainability response on question S4. Tom notes the '
        'gap, emails the supplier for clarification, and reviews the two clean '
        'scorecards. By 10:15, he has a ranked comparison ready for the 14:00 '
        'meeting.'
    )

    add_what_to_learn(doc,
        'Validation catches data gaps before they become scoring errors. If Tom '
        'had scored the incomplete bid without flagging the blank, his evaluation '
        'would overstate one supplier and understate another. The prompt says '
        '"validate, then score." That order matters.'
    )

    # Scenario 3
    doc.add_heading(
        '11:00 - CFO changes the payment terms policy', level=3
    )

    doc.add_paragraph(
        'Julia forwards a new policy from the CFO: all contracts over $500,000 '
        'must include Net 60 payment terms, up from Net 45. Tom has two active '
        'RFPs in flight. Both reference Net 45 in the terms and conditions '
        'section. He needs to update both without re-drafting the full documents.'
    )

    add_code_block(doc,
        'cd Packaging_Sourcing_2026\n'
        'claude\n\n'
        'Read outputs/rfp-package.md. Find every instance of "Net 45" in\n'
        'the payment terms section and replace with "Net 60". Do not change\n'
        'any other section. Save the updated file. Show me the lines you\n'
        'changed.'
    )

    doc.add_paragraph(
        'Tom runs the same prompt against his second active RFP folder. Both '
        'documents are updated in 4 minutes. He logs the change in his event '
        'tracker.'
    )

    add_what_to_learn(doc,
        'Targeted edits are faster and safer than full re-drafts. The prompt '
        'tells Claude Code exactly what to change and what to leave alone. '
        'Asking Claude to "show me the lines you changed" gives Tom an audit '
        'trail. He copies that output into his event tracker for the record.'
    )

    # Scenario 4
    doc.add_heading(
        '13:00 - Preparing the award recommendation for Thursday', level=3
    )

    doc.add_paragraph(
        'Tom has a completed evaluation matrix for his fasteners sourcing event. '
        'The CPO meeting is Thursday. He needs the full award recommendation '
        'document: executive summary, scoring table, savings analysis, objection '
        'responses, and risk assessment. He types one prompt.'
    )

    add_code_block(doc,
        'cd Fasteners_Sourcing_2026\n'
        'claude\n\n'
        'Read outputs/scoring-summary.md and all scorecards in\n'
        'outputs/bid-scorecards/. Write an award recommendation to\n'
        'outputs/award-recommendation.md with seven sections: executive\n'
        'summary, evaluation results, recommended supplier profile, savings\n'
        'analysis, anticipated objections (3 max), risk assessment (3 risks),\n'
        'and recommendation statement. Address to Julia Reeves, CPO.\n'
        'Decision deadline: 2026-05-22.'
    )

    doc.add_paragraph(
        'Claude Code writes the full memo in 12 minutes. Tom reviews the savings '
        'analysis, confirms the $340,000 annual savings figure (11.2% reduction '
        'on $3.04M baseline), and adjusts one objection response to add context '
        'about the incumbent relationship. He saves the final version and sends '
        'it to Julia for pre-read.'
    )

    add_what_to_learn(doc,
        'The award recommendation prompt follows a fixed structure: seven '
        'sections, three objections, three risks. Tom uses the same structure '
        'for every sourcing event. The data changes. The structure stays the '
        'same. This is what makes the system repeatable. One prompt, one memo, '
        'one review pass.'
    )

    # Scenario 5
    doc.add_heading(
        '15:30 - Setting up a new sourcing event', level=3
    )

    doc.add_paragraph(
        'Tom just learned that Clearwater is adding a new sourcing event for IT '
        'peripherals. Annual spend: $1.8M. Six suppliers on the longlist. He '
        'needs to set up the project folder and get the category context built '
        'before end of day.'
    )

    add_code_block(doc,
        'mkdir IT_Peripherals_Sourcing_2026\n'
        'cd IT_Peripherals_Sourcing_2026\n'
        'mkdir data outputs outputs/bid-scorecards skills\n'
        'cp ../templates/CLAUDE_sourcing.md CLAUDE.md\n'
        'claude\n\n'
        'Read CLAUDE.md. I have updated the role, category, spend baseline,\n'
        'and evaluation criteria for an IT peripherals sourcing event. Read\n'
        'data/spend-baseline.csv (180 rows) and data/supplier-longlist.csv\n'
        '(6 suppliers). Build the category context summary. Save to\n'
        'outputs/category-context-v1.md. Address to Julia Reeves, CPO.'
    )

    doc.add_paragraph(
        'Claude Code reads the new data, builds the context summary, and saves '
        'it. Tom has a new event folder set up with the same structure as every '
        'other event. He copies the score-bid-response.md skill from his '
        'fasteners folder. The skill works without changes because it references '
        '"bid-responses/" and "CLAUDE.md," not specific supplier names.'
    )

    add_what_to_learn(doc,
        'A sourcing sprint system is portable because the folder structure and '
        'skill files are generic. Tom did not rewrite the bid-scoring skill for '
        'IT peripherals. He copied it. The skill says "read every file in '
        'bid-responses/" and "apply the weights from CLAUDE.md." It does not '
        'say "read Great Lakes Steel" or "use 35% for price." Swap the data, '
        'swap the weights, and the system runs a new event.'
    )

    # Scenario 6
    doc.add_heading('16:45 - End-of-day status update', level=3)

    doc.add_paragraph(
        'Julia asks for a quick status on all active events. Tom has four '
        'folders. He opens each one and asks Claude Code the same prompt.'
    )

    add_code_block(doc,
        'Read outputs/ and list every file with its last-modified date. For\n'
        'each deliverable, state whether it is draft, reviewed, or final.\n'
        'Summarize in three lines: event name, current stage, next action.'
    )

    doc.add_paragraph(
        'Tom runs this in each of his four event folders. In 10 minutes, he has '
        'a four-line status table. He pastes it into an email to Julia. '
        '"Packaging: evaluation complete, award memo Thursday. Fasteners: award '
        'memo sent for pre-read. IT Peripherals: category context done, RFP '
        'generation tomorrow. Electrical: bids due May 28, waiting."'
    )

    add_what_to_learn(doc,
        'Status reporting does not require a separate tool or dashboard. Claude '
        'Code reads the outputs/ folder and tells you what exists. The prompt '
        'is the same for every event. Tom did not build a tracker. He asked '
        'Claude Code to read what was already there.'
    )

    # Scenario 7
    doc.add_heading(
        '17:15 - Reviewing a colleague request for scoring help', level=3
    )

    doc.add_paragraph(
        'Before logging off, Tom gets a Slack from Maria, a junior buyer, asking '
        'how to score bids for her first sourcing event (office furniture, $280,000 '
        'annual spend, three bids). Tom walks her through the setup in two minutes.'
    )

    add_code_block(doc,
        'mkdir Office_Furniture_2026\n'
        'cd Office_Furniture_2026\n'
        'mkdir data outputs outputs/bid-scorecards skills\n'
        'cp ../templates/CLAUDE_sourcing.md CLAUDE.md\n'
        'cp ../Fasteners_Sourcing_2026/skills/score-bid-response.md skills/'
    )

    doc.add_paragraph(
        'Tom tells Maria to update CLAUDE.md with her category, her criteria '
        'weights, and her stakeholders. Then place her three bid files in '
        'data/bid-responses/ and type the bid-scoring prompt from the course '
        'handout. Maria runs it and has scored bids in 15 minutes. She would '
        'have spent the afternoon doing it by hand.'
    )

    add_what_to_learn(doc,
        'The system scales down as well as up. Maria used the same folder '
        'structure, the same skill file, and the same prompt for a $280,000 '
        'event that Tom uses for $3M events. The only difference is the data in '
        'CLAUDE.md and the files in bid-responses/. The skill does not care '
        'about the dollar amount. It cares about the structure.'
    )

    # ============================================================
    # 8. 20-MINUTE SPRINT
    # ============================================================
    doc.add_heading(
        '8. 20-minute sprint: your first sourcing output in 20 minutes',
        level=1,
    )

    doc.add_paragraph(
        'This section gets you from zero to your first usable output in 20 '
        'minutes. You will set up the practice folder, run Claude Code (in the '
        'terminal), and produce a category context summary from the Ironbridge '
        'Manufacturing spend data. No prior Claude Code experience needed.'
    )

    doc.add_heading('Minutes 0 to 5: Install and verify', level=2)

    doc.add_paragraph(
        '1. Open a terminal (on Windows: search for "Terminal" in the Start '
        'menu).\n'
        '2. Type: claude --version\n'
        '3. You should see a version number (for example, 1.0.35). If not, '
        'run: npm install -g @anthropic-ai/claude-code\n'
        '4. Sign in: claude auth login\n'
        '5. Confirm your account is active.'
    )

    doc.add_heading('Minutes 5 to 10: Open the practice folder', level=2)

    doc.add_paragraph(
        '1. In the terminal, navigate to the course folder:'
    )
    add_code_block(doc, 'cd "Course_16_Sourcing_Sprint/practice"')
    doc.add_paragraph(
        '2. Pause OneDrive sync (right-click the OneDrive tray icon, choose '
        '"Pause syncing").\n'
        '3. Start Claude Code:'
    )
    add_code_block(doc, 'claude')
    doc.add_paragraph(
        '4. You should see the Claude Code prompt. It reads CLAUDE.md '
        'automatically and loads the Ironbridge Manufacturing context.'
    )

    doc.add_heading('Minutes 10 to 15: Build the category context', level=2)

    doc.add_paragraph('Type this prompt:')
    add_code_block(doc,
        'Read data/spend-baseline.csv and data/supplier-longlist.csv.\n'
        'Calculate total spend by sub-category and by supplier. Flag any\n'
        'sub-category where one supplier holds 80% or more of spend. List\n'
        'suppliers in the longlist that are not in the spend data (new\n'
        'entrants). Write a category context summary to\n'
        'outputs/category-context-v1.md. Address to Tom Baker and Lisa\n'
        'Torres. Date 2026-04-25.'
    )
    doc.add_paragraph(
        'Claude Code reads both files, calculates totals, flags risks, and '
        'saves the summary. This takes 2 to 4 minutes.'
    )

    doc.add_heading('Minutes 15 to 20: Review and next steps', level=2)

    doc.add_paragraph(
        '1. Open outputs/category-context-v1.md in any text editor or Word.\n'
        '2. Check: do the six sub-category spend totals add up to roughly '
        '$22.2M?\n'
        '3. Check: is Steel flagged as single source (Great Lakes Steel, 100%, '
        '$4.2M)?\n'
        '4. Check: do Northland Alloys and Bayshore Materials appear as new '
        'entrants?\n'
        '5. If all three checks pass, you have your first sourcing sprint '
        'output. Resume OneDrive sync.\n'
        '6. Next step: open Lesson 2 and generate the RFP package.'
    )

    doc.add_paragraph(
        'You just built a category context summary that would normally take 3 '
        'to 4 hours. You did it in under 15 minutes. The output is data-driven, '
        'stakeholder-addressed, and ready to share.'
    )

    # ============================================================
    # 9. FIRST WEEK PLANNER
    # ============================================================
    doc.add_heading('9. First week day-by-day planner', level=1)

    doc.add_paragraph(
        'This planner assumes you spend 60 to 90 minutes per day on the course. '
        'By Friday, you will have completed all five lessons and produced every '
        'deliverable in the sourcing sprint.'
    )

    # Day 1
    doc.add_heading(
        'Day 1 (Monday): Install, set up, and category context', level=2
    )
    doc.add_paragraph('Goals:')
    doc.add_paragraph(
        '1. Confirm Claude Code is installed and you are signed in.\n'
        '2. Open the practice/ folder and verify CLAUDE.md loads automatically.\n'
        '3. Complete Lesson 1: produce the category context summary.\n'
        '4. Review the output against the solution in solutions/.'
    )
    doc.add_paragraph(
        'By end of day: outputs/category-context-v1.md exists with spend table, '
        'risk flags, and new entrant list.'
    )

    # Day 2
    doc.add_heading('Day 2 (Tuesday): RFP package generation', level=2)
    doc.add_paragraph('Goals:')
    doc.add_paragraph(
        '1. Complete Lesson 2: generate all six RFP sections in one chained '
        'session.\n'
        '2. Assemble sections into the complete RFP document.\n'
        '3. Verify cross-references (scope section says 24 months, terms '
        'section says 24 months).\n'
        '4. Compare your RFP against solutions/rfp_package_solution.md.'
    )
    doc.add_paragraph(
        'By end of day: outputs/rfp-package.md exists with cover letter, scope, '
        'pricing template, evaluation criteria, submission instructions, and '
        'terms.'
    )

    # Day 3
    doc.add_heading(
        'Day 3 (Wednesday): Response template and bid processing', level=2
    )
    doc.add_paragraph('Goals:')
    doc.add_paragraph(
        '1. Complete Lesson 3: create the pricing CSV template, technical '
        'questionnaire, and supplier instructions.\n'
        '2. Start Lesson 4: validate and score the six bids.\n'
        '3. Produce the evaluation matrix with all six suppliers ranked.'
    )
    doc.add_paragraph(
        'By end of day: outputs/response-template.md exists. '
        'outputs/scoring-summary.md shows six suppliers ranked by weighted '
        'total score.'
    )

    # Day 4
    doc.add_heading(
        'Day 4 (Thursday): Award recommendation and review', level=2
    )
    doc.add_paragraph('Goals:')
    doc.add_paragraph(
        '1. Complete Lesson 5: draft the award recommendation memo.\n'
        '2. Verify all numbers trace back to the scored data.\n'
        '3. Strengthen the anticipated objection responses with specific '
        'figures.\n'
        '4. Compare your memo against '
        'solutions/award_recommendation_solution.md.'
    )
    doc.add_paragraph(
        'By end of day: outputs/award-recommendation.md exists with seven '
        'sections, three recommendations, and three risks.'
    )

    # Day 5
    doc.add_heading(
        'Day 5 (Friday): Reflect, refine, and plan', level=2
    )
    doc.add_paragraph('Goals:')
    doc.add_paragraph(
        '1. Re-read your category context, RFP, scorecards, and award memo '
        'end to end.\n'
        '2. Identify any inconsistencies (a supplier name spelled differently, '
        'a figure that does not match between documents).\n'
        '3. Ask Claude Code (in the terminal) to fix any inconsistencies you '
        'found.\n'
        '4. Plan your first real sourcing event using this system: pick a '
        'category, gather your spend data and supplier list, create a new '
        'project folder with the same structure.\n'
        '5. Copy the score-bid-response.md skill to your new folder. It works '
        'without changes.'
    )
    doc.add_paragraph(
        'By end of day: all five deliverables are reviewed and consistent. You '
        'have a plan and a folder structure for your first real event.'
    )

    # ============================================================
    # 10. THE PATTERN
    # ============================================================
    doc.add_heading(
        '10. The pattern: applying the sourcing sprint to your own events',
        level=1,
    )

    doc.add_paragraph(
        'The sourcing sprint system works because it separates data from logic. '
        'The data changes with every event: new spend files, new suppliers, new '
        'criteria weights. The logic stays the same: ingest, generate RFP, '
        'create templates, score bids, write recommendation. Here is how to '
        'apply the pattern to your own sourcing events.'
    )

    doc.add_heading('Step 1: Create the project folder', level=2)

    add_code_block(doc,
        'mkdir My_Sourcing_Event_2026\n'
        'cd My_Sourcing_Event_2026\n'
        'mkdir data outputs outputs/bid-scorecards skills'
    )

    doc.add_paragraph(
        'Copy CLAUDE.md from the practice folder and update it with your role, '
        'your company, your category, your evaluation criteria and weights, your '
        'stakeholders, and your timeline. Every prompt you type will pull from '
        'this file. Get it right once and every output is consistent.'
    )

    doc.add_heading('Step 2: Load your data', level=2)

    doc.add_paragraph(
        'Place your spend export (CSV or Excel) and supplier longlist in data/. '
        'Place your scope notes (a Word doc, a PDF, or plain text) in data/. '
        'Name the files clearly: spend-baseline.csv, supplier-longlist.csv, '
        'scope-notes.md. Claude Code (in the terminal) reads the file names in '
        'your prompts, so consistency matters.'
    )

    doc.add_heading('Step 3: Run the five stages in order', level=2)

    doc.add_paragraph(
        '1. Category context: read spend and supplier data, produce the context '
        'summary.\n'
        '2. RFP package: generate all sections from scope notes, spend data, '
        'and criteria.\n'
        '3. Response template: create the pricing and technical templates for '
        'suppliers.\n'
        '4. Bid processing: after bids arrive, validate and score them all in '
        'one pass.\n'
        '5. Award recommendation: assemble scores into the VP-ready memo.'
    )

    doc.add_paragraph(
        'Each stage uses the output of the previous stage. If you change '
        'something in stage 2 (for example, adjusting the evaluation weights '
        'in the RFP), re-run stages 3 through 5 to keep everything consistent.'
    )

    doc.add_heading('Step 4: Copy the skill file', level=2)

    doc.add_paragraph(
        'Copy skills/score-bid-response.md from the practice folder to your new '
        'project. This skill tells Claude Code how to read a bid file, extract '
        'data, and apply the scoring rubric. It works for any category because '
        'it references "bid-responses/" and "CLAUDE.md," not specific supplier '
        'names or weights.'
    )

    doc.add_heading('Step 5: Personalize CLAUDE.md', level=2)

    doc.add_paragraph(
        'CLAUDE.md is the single source of truth for your event. It should '
        'contain:'
    )

    doc.add_paragraph(
        '1. Your role and company.\n'
        '2. The category and sub-categories in scope.\n'
        '3. The evaluation criteria with weights (must total 100%).\n'
        '4. The stakeholders (sponsor, approver, lead).\n'
        '5. The timeline (RFP issue, bid deadline, evaluation, award '
        'recommendation, board).\n'
        '6. The savings target (percentage and dollar range).\n'
        '7. Output standards (currency format, date format, file naming, '
        'sentence style).'
    )

    doc.add_paragraph(
        'When CLAUDE.md is complete, every prompt pulls from it automatically. '
        'You type shorter prompts and get consistent outputs from the first '
        'attempt.'
    )

    # ============================================================
    # 11. TROUBLESHOOTING
    # ============================================================
    doc.add_heading('11. Troubleshooting', level=1)

    doc.add_paragraph(
        'These are the most common problems students encounter in Course 16. '
        'Each entry has the symptom (what you see) and the fix (what to do).'
    )

    troubles = [
        (
            'Claude Code reports "file not found" for spend-baseline.csv.',
            'Confirm the file is in data/, not in the project root. The exact '
            'filename must match: spend-baseline.csv with a hyphen, not '
            'spend_baseline.csv with an underscore. Check capitalization. On '
            'some systems, "Spend-Baseline.csv" is not the same as '
            '"spend-baseline.csv."'
        ),
        (
            'Sub-category spend totals do not add up to $22.2M.',
            'Ask Claude Code (in the terminal): "Check whether any rows in '
            'data/spend-baseline.csv have a blank or null value in the '
            'sub-category column and count them." Excluded rows cause the '
            'shortfall. Ask Claude to add them to an "Uncategorized" line so '
            'the total is represented.'
        ),
        (
            'The new entrant list is empty even though Northland Alloys is on '
            'the longlist.',
            'The supplier names in the two files probably differ by spelling or '
            'punctuation. Ask Claude Code: "Show me the exact supplier names in '
            'data/supplier-longlist.csv and the distinct supplier names in '
            'data/spend-baseline.csv side by side." Find the mismatch. Ask '
            'Claude to match on a lower-case, punctuation-stripped version of '
            'each name.'
        ),
        (
            'Bid scoring is inconsistent: one supplier gets 70 for a vague '
            'answer, another gets 45 for an equally vague answer.',
            'Ask Claude Code to re-score all technical responses using the same '
            'rubric. Type: "Re-score all technical responses. Show the scoring '
            'criteria you applied to each answer. If Supplier A gets 45 for a '
            'vague answer on T3, Supplier B must get the same for an equally '
            'vague answer on T3. Ensure consistent treatment across all '
            'suppliers."'
        ),
        (
            'The award recommendation has more than three recommendations.',
            'The CLAUDE.md rules cap recommendation lists at three. Remove '
            'recommendations beyond three, or relabel the section as '
            '"Prioritized actions, ranked" if you genuinely need more. In most '
            'cases, three is enough for a CPO meeting.'
        ),
        (
            'OneDrive creates a sync conflict file (.tmp or a "-conflict" copy).',
            'Another application (Word, Excel, or a second Claude Code session) '
            'had the file open during the session. Pause OneDrive sync before '
            'starting any multi-file build. Close files in other applications. '
            'Move the conflict copy to an archive folder, keep the main file, '
            'and resume sync when finished.'
        ),
    ]

    for symptom, fix in troubles:
        add_bold_text(doc, 'Symptom: ', symptom)
        add_bold_text(doc, 'Fix: ', fix)
        doc.add_paragraph('')

    # ============================================================
    # 12. DONE CHECKLIST
    # ============================================================
    doc.add_heading('12. Done checklist for Course 16', level=1)

    doc.add_paragraph(
        'Use this checklist after you complete all five lessons. Every item '
        'should be "done" before you move to your first real sourcing event.'
    )

    checklist = [
        'The category context summary identifies the top three suppliers by '
        'spend, flags Apex Electronics as at risk, and quantifies the savings '
        'target as $1.8M to $2.7M (8-12% of $22.2M).',
        'The RFP package includes scope, timeline, evaluation criteria with '
        'weights, submission requirements, and terms and conditions. All '
        'cross-references are consistent.',
        'The response template maps directly to the five evaluation criteria so '
        'every bid arrives in a scorable format.',
        'Each of the six bid scorecards shows a score for each criterion (0 to '
        '100), the weighted score, and the total. Scoring is consistent: the '
        'same pricing gets the same price score across suppliers.',
        'The award recommendation memo names the recommended supplier (the '
        'legal entity), the total contract value ($20.1M), the expected savings '
        '($2.1M, 9.5%), and the decision deadline (2026-06-20). It includes no '
        'more than three recommendations.',
        'Every output file is in outputs/. No deliverables are loose in the '
        'project root or in data/.',
        'You can explain the five-stage sourcing sprint sequence from memory: '
        'ingest, RFP, template, score, recommend.',
        'You have a plan for your first real sourcing event: a category picked, '
        'a folder structure created, and CLAUDE.md updated with your real data.',
    ]

    for i, item in enumerate(checklist, 1):
        doc.add_paragraph(f'{i}. {item}')

    # ============================================================
    # FOOTER
    # ============================================================
    doc.add_paragraph('')
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        'U2xAI | PROCUREAI ACADEMY | Course 16: Sourcing Sprint'
    )
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
    run.font.name = 'Calibri'

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('For internal training use only. Not for distribution.')
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
    run.font.name = 'Calibri'

    # Save
    os.makedirs(os.path.dirname(str(HANDOUT_PATH)), exist_ok=True)
    doc.save(str(HANDOUT_PATH))
    print(f"Saved: {HANDOUT_PATH}")

    # Word count estimate
    word_count = 0
    for p in doc.paragraphs:
        word_count += len(p.text.split())
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                word_count += len(cell.text.split())
    print(f"Estimated word count: {word_count}")


if __name__ == '__main__':
    build()
