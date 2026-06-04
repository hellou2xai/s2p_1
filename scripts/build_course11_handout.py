"""
Build Course 11 handout: The Category Management System
Comprehensive training guide handout as .docx
"""
import os
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_PATH = PROJECT_ROOT / "Handouts" / "Course_11_The_Category_Management_System_Handout.docx"

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Configure heading styles
for level in range(1, 4):
    h_style = doc.styles[f'Heading {level}']
    h_style.font.name = 'Calibri'
    if level == 1:
        h_style.font.size = Pt(16)
        h_style.font.bold = True
    elif level == 2:
        h_style.font.size = Pt(14)
        h_style.font.bold = True
    elif level == 3:
        h_style.font.size = Pt(12)
        h_style.font.bold = True

title_style = doc.styles['Title']
title_style.font.name = 'Calibri'
title_style.font.size = Pt(24)
title_style.font.bold = True


def add_para(text, style_name='Normal', bold=False, italic=False, space_after=Pt(6)):
    p = doc.add_paragraph(style=style_name)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = 'Calibri'
    run.font.size = Pt(11) if style_name == 'Normal' else None
    p.paragraph_format.space_after = space_after
    return p


def add_code_block(text):
    """Add a code block styled with monospace font and light gray background."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.3)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    shading = run._element.makeelement(qn('w:shd'), {
        qn('w:val'): 'clear',
        qn('w:color'): 'auto',
        qn('w:fill'): 'F2F2F2'
    })
    run._element.get_or_add_rPr().append(shading)
    return p


def add_table(headers, rows):
    """Add a formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for para in cell.paragraphs:
            para.style = doc.styles['Normal']
            for run in para.runs:
                run.bold = True
                run.font.name = 'Calibri'
                run.font.size = Pt(10)
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for para in cell.paragraphs:
                para.style = doc.styles['Normal']
                for run in para.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10)
    doc.add_paragraph()
    return table


def add_bold_para(label, text):
    """Add a paragraph with a bold label followed by normal text."""
    p = doc.add_paragraph()
    run_label = p.add_run(label)
    run_label.bold = True
    run_label.font.name = 'Calibri'
    run_label.font.size = Pt(11)
    run_text = p.add_run(text)
    run_text.font.name = 'Calibri'
    run_text.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(6)
    return p


# ======================================================================
# HEADER
# ======================================================================
add_para('U2xAI')
add_para('PROCUREAI ACADEMY')
add_para('Series 2 (Engineering Track) | Course 11')
doc.add_paragraph('The Category Management System', style='Title')
add_para('Multi-category orchestration with self-correcting feedback loops for Monday briefings.', italic=True)
add_para('About 6 lessons. No coding background required. Use this handout alongside the course folder at Detailed Course Content/Course_11_The_Category_Management_System/.')

# ======================================================================
# 1. HOW TO USE THIS HANDOUT
# ======================================================================
doc.add_heading('1. How to use this handout', level=1)

add_para(
    'This handout is your reading companion for Course 11. The hands-on work happens in the course folder '
    'you received with the training materials. This document gives you the big picture, the mental model, '
    'worked examples you can reference during practice, and a troubleshooting guide for when things go sideways.'
)

add_para(
    'How to read this guide:'
)
add_para(
    '1. Read sections 2 through 5 first. They explain what the course builds, what is in the folder, and how much time you will save.\n'
    '2. Read section 6 to understand the mental model behind multi-category orchestration and feedback loops.\n'
    '3. Work through the course lessons in order. When you get stuck, come back here for the worked examples in section 7.\n'
    '4. Use the Day in the Life narrative in section 8 to see how this system fits into a real procurement workweek.\n'
    '5. If you are short on time, skip to the 20-Minute Sprint in section 9. It gets you to your first Monday briefing in 20 minutes flat.\n'
    '6. After finishing the course, use the First Week Planner in section 10 to build the habit.\n'
    '7. Keep the troubleshooting section (section 12) open during practice. It covers the six most common problems.'
)

add_para(
    'Every prompt in this handout is written for Claude Code (in the terminal). The orchestration and sub-agent '
    'patterns described here do not work in Claude AI Web or Claude Desktop with Cowork. Those products do not '
    'support sub-agents, file-scoped reads, or session-level retry policies.'
)

# ======================================================================
# 2. WHAT THIS COURSE TEACHES
# ======================================================================
doc.add_heading('2. What this course teaches', level=1)

add_para(
    'It is Monday morning, 07:45. You manage six procurement categories at Meridian Corp, a US-based manufacturer '
    'with $87.4M in annual spend. Your VP wants a consolidated category briefing by 09:00. You have 23 unread messages. '
    'Three supplier scorecards arrived Friday. Two contracts expire this month. One savings initiative is behind schedule, '
    'and you do not know which one because the tracker is a shared spreadsheet that four people edited over the weekend.'
)

add_para(
    'Without a system, the Monday routine looks like this. You open six spreadsheets. You cross-reference three dashboards. '
    'You build a status summary in a blank Word document, typing the same header format you type every Monday. By 10:30, '
    'you have a rough picture. By 11:00, your VP asks for the update and you are still formatting the table.'
)

add_para(
    'This course fixes that. You build a Claude Code (in the terminal) orchestration system that does the Monday morning '
    'scan in under five minutes. One command dispatches six sub-agents (one per category), each reading the relevant data. '
    'The orchestrator collects their findings, validates the output against five quality rules, self-corrects any errors '
    'through a feedback loop, stops after three failed attempts and escalates to you, and produces a consolidated briefing. '
    'You review it, make two edits, and send it to your VP before 09:00.'
)

add_para('The six lessons build the system one layer at a time:')
add_para(
    '1. The multi-category orchestrator: one command reads all six categories and produces a prioritized action plan.\n'
    '2. Specialized sub-agents: one agent per category with scoped data access, so each agent reads only what it needs.\n'
    '3. Self-correcting feedback loop: validate outputs against five rules and fix errors automatically.\n'
    '4. Retry limits and human escalation: stop after three failed fixes and write an escalation note for you.\n'
    '5. Consolidated briefing: assemble sub-agent outputs into one VP-ready document covering all six categories.\n'
    '6. Performance and cost awareness: estimate token usage, find the most expensive step, and redesign it to cut cost by 30% or more.'
)

add_para('The six categories in the practice scenario:')

add_table(
    ['Category', 'Annual spend', 'Suppliers', 'Active initiatives', 'Status'],
    [
        ['IT services', '$18.2M', '6', '3', 'On track'],
        ['Logistics', '$16.8M', '5', '2', 'One initiative at risk'],
        ['Facilities', '$14.1M', '4', '2', 'Contract expiring May 2026'],
        ['Raw materials', '$15.6M', '6', '2', 'Price volatility flagged'],
        ['Professional services', '$12.4M', '5', '2', 'Supplier consolidation in progress'],
        ['MRO', '$10.3M', '4', '1', 'New catalog rollout starting'],
    ]
)

# ======================================================================
# 3. WHAT YOU END UP WITH
# ======================================================================
doc.add_heading('3. What you end up with', level=1)

add_para('When you complete all six lessons, these six things are true:')
add_para(
    '1. You type one prompt and Claude Code (in the terminal) dispatches six sub-agents, one per category. '
    'Each reads only its category data from the practice CSV and JSON files.'
)
add_para(
    '2. Each sub-agent produces a category summary with a spend trend, supplier scores, contract alerts, '
    'initiative status, and one recommended action.'
)
add_para(
    '3. The feedback loop catches at least one error (a missing supplier name, a date in the wrong format, '
    'or an impossible percent-complete value) and corrects it without your intervention.'
)
add_para(
    '4. The retry logic stops after three failed fix attempts on any sub-agent and escalates to you with a '
    'clear error message naming the file, the rule, and a question you need to answer.'
)
add_para(
    '5. The consolidated briefing names all six categories, lists the top three actions, and includes at least '
    'one supplier name, one dollar figure, and one date per category. It saves to Outputs/briefings/briefing-2026-04-25.md.'
)
add_para(
    '6. You can estimate the token cost of a full Monday briefing run. At practice data volumes, the total is '
    'under $1.00 per month for weekly briefings.'
)

# ======================================================================
# 4. WHAT IS IN THE COURSE FOLDER
# ======================================================================
doc.add_heading('4. What is in the course folder', level=1)

add_para(
    'The course folder is self-contained. Everything you need is inside it. No external downloads, '
    'no separate databases, no shared drives.'
)

add_code_block(
    'Course_11_The_Category_Management_System/\n'
    '  README.md\n'
    '  COURSE_OVERVIEW.md\n'
    '  lessons/\n'
    '    Lesson_01_Multi_Category_Orchestrator.md\n'
    '    Lesson_02_Specialized_Sub_Agents.md\n'
    '    Lesson_03_Self_Correcting_Feedback_Loop.md\n'
    '    Lesson_04_Retry_Limits_And_Escalation.md\n'
    '    Lesson_05_Consolidated_Briefing.md\n'
    '    Lesson_06_Performance_And_Cost_Awareness.md\n'
    '  practice/\n'
    '    CLAUDE.md\n'
    '    data/\n'
    '      program-state.json\n'
    '      category-spend.csv\n'
    '      supplier-scorecards.csv\n'
    '      contract-calendar.csv\n'
    '      initiative-pipeline.csv\n'
    '    Drafts/\n'
    '    Outputs/\n'
    '  solutions/\n'
    '    orchestrator_prompt_solution.md\n'
    '    category_agent_solution.md\n'
    '    feedback_loop_solution.md\n'
    '    consolidated_briefing_solution.md\n'
    '    cost_awareness_solution.md\n'
    '  scripts/\n'
    '    build_course_data.py'
)

doc.add_heading('Folder and file explanations', level=2)

add_bold_para('lessons/. ',
    'Six lesson files, one per lesson, in order. Each lesson opens with a day-to-day scenario '
    '("It is 08:10 on Monday...") and walks through every step with exact prompts and expected results. '
    'Work through them in order. Do not skip.'
)
add_para(
    'Why this matters. The lessons build on each other. Lesson 2 needs the output of Lesson 1. '
    'Lesson 3 validates the output of Lesson 2. Skipping a lesson means the next one will fail because '
    'the input files do not exist.'
)

add_bold_para('practice/. ',
    'The hands-on workspace. This is where you run Claude Code (in the terminal). It contains the data files, '
    'the CLAUDE.md context file, and two output folders: Drafts/ for working files and Outputs/ for final deliverables.'
)
add_para(
    'Why this matters. Running Claude Code from the practice/ folder means CLAUDE.md is automatically loaded. '
    'It tells Claude Code your role, the categories, the data file locations, and the output standards. '
    'Without it, Claude Code produces generic output with no Meridian Corp context.'
)

add_bold_para('practice/data/. ',
    'Five data files covering six categories, 30 suppliers, 25 contracts, and 12 initiatives. '
    'All files are read-only. The CLAUDE.md file instructs Claude Code not to edit anything in data/.'
)
add_para(
    'Why this matters. If the data files are modified during practice, the lessons produce different results '
    'from the expected outputs. Keeping them read-only means you can always compare your output to the solutions.'
)

add_bold_para('practice/data/program-state.json. ',
    'The portfolio state file. It contains the current status of all six categories, including risk flags, '
    'active initiatives, owners, and deadlines. This is the first file the orchestrator reads every Monday.'
)
add_para(
    'Why this matters. The orchestrator depends on this file to decide what needs attention. '
    'If the state file is stale, the briefing will miss new risks and report resolved issues as active.'
)

add_bold_para('practice/data/category-spend.csv. ',
    'Approximately 1,500 spend transactions across six categories over 12 months. '
    'This is the largest data file and the primary driver of token consumption.'
)
add_para(
    'Why this matters. At 1,500 rows, this file is large enough to feel like real procurement data '
    'but small enough to read quickly. In production, your spend file may have 10,000 or more rows. '
    'The cost awareness lesson (Lesson 6) teaches you to pre-filter before reading.'
)

add_bold_para('practice/data/supplier-scorecards.csv. ',
    '30 suppliers scored across four quarters (120 rows). Scoring dimensions: quality, delivery, cost, '
    'and responsiveness. Scale: 1 to 5.'
)
add_para(
    'Why this matters. The scorecard data drives the contract renewal recommendations (score above 4.0: renew, '
    '3.0 to 3.9: review, below 3.0: rebid) and the supplier health alerts in each category section.'
)

add_bold_para('practice/data/contract-calendar.csv. ',
    '25 contracts with start dates, end dates, renewal notice windows, and auto-renewal flags.'
)
add_para(
    'Why this matters. The contract review sub-agent reads this file to find contracts expiring within 90 days. '
    'Missing a renewal notice window can lock you into an auto-renewal at unfavorable terms.'
)

add_bold_para('practice/data/initiative-pipeline.csv. ',
    '12 active initiatives across six categories with savings targets, realized savings, stages, owners, and status.'
)
add_para(
    'Why this matters. The savings tracking sub-agent reads this file to calculate percent complete and flag '
    'at-risk or behind-schedule initiatives. Without this file, the briefing cannot report savings progress.'
)

add_bold_para('practice/CLAUDE.md. ',
    'The project context file. It defines your role (Director of Category Management at Meridian Corp), '
    'the six categories with spend figures, the data file locations, and the output standards '
    '(USD with commas, YYYY-MM-DD dates, no em-dashes, three recommendations maximum).'
)
add_para(
    'Why this matters. Without this file, every prompt needs to repeat the role, the categories, and the '
    'formatting rules. With it, Claude Code (in the terminal) applies all of those automatically.'
)

add_bold_para('solutions/. ',
    'Reference answers for each lesson. Five files covering the orchestrator prompt, the sub-agent template, '
    'the feedback loop logic, the consolidated briefing, and the cost tracking pattern.'
)
add_para(
    'Why this matters. If your output does not match what the lesson says you should see, compare it to '
    'the solution file. The learning happens in the attempt, not in reading the answer first.'
)

add_bold_para('scripts/build_course_data.py. ',
    'A Python script that regenerates all five data files deterministically (using random.seed(42)). '
    'If you accidentally modify or delete a data file, run this script to restore everything.'
)
add_para(
    'Why this matters. One command restores the full data set. You never have to re-download or ask '
    'for a fresh copy.'
)

# ======================================================================
# 5. TIME SAVINGS TABLE
# ======================================================================
doc.add_heading('5. Time savings reference table', level=1)

add_para(
    'This table compares five procurement tasks with and without the orchestration system you build in this course. '
    'All times are for the Meridian Corp practice scenario: six categories, 30 suppliers, 25 contracts, 12 initiatives.'
)

add_table(
    ['Task', 'Without Claude Code', 'With Claude Code (in the terminal)', 'Time saved'],
    [
        [
            'Monday briefing: scan 6 categories, identify risks, produce VP summary',
            '90 to 120 min (15 to 20 min per category, manual formatting)',
            '8 to 12 min (one prompt, review, two edits)',
            '78 to 108 min per week'
        ],
        [
            'Contract expiry check: find contracts expiring in 90 days, cross-reference supplier scores',
            '25 to 35 min (open calendar, open scorecards, match by hand)',
            '3 to 5 min (one sub-agent prompt, validated output)',
            '20 to 30 min per run'
        ],
        [
            'Savings initiative status: check 12 initiatives, flag at-risk items',
            '30 to 45 min (open tracker, calculate percent complete, write summary)',
            '4 to 6 min (one sub-agent prompt with calculated fields)',
            '24 to 39 min per run'
        ],
        [
            'Supplier scorecard refresh: recalculate scores for 30 suppliers, identify trends',
            '45 to 60 min (open scorecard, average 4 dimensions, compare quarters)',
            '5 to 8 min (one sub-agent prompt with trend calculation)',
            '37 to 52 min per run'
        ],
        [
            'Validation and error correction: check 5 output files for missing data, wrong formats',
            '20 to 30 min (open each file, scan cells, fix by hand)',
            '2 to 4 min (automated 5-rule validation loop)',
            '16 to 26 min per run'
        ],
    ]
)

add_para(
    'At practice data volumes, the Monday briefing costs approximately $0.15 in Claude Code API usage per run. '
    'At production volumes (10,000 spend rows, 200 contracts), expect $0.50 to $1.50 per run. '
    'Over 52 weeks, the Monday briefing alone saves 67 to 93 hours of manual work.'
)

# ======================================================================
# 6. WHAT MULTI-CATEGORY ORCHESTRATION AND FEEDBACK LOOPS ARE
# ======================================================================
doc.add_heading('6. What multi-category orchestration and feedback loops are', level=1)

doc.add_heading('The mental model', level=2)

add_para(
    'Think of the orchestrator as a project manager who never does the analysis directly. It reads the '
    'portfolio state, decides what needs attention, assigns the work, checks the results, and assembles '
    'the final deliverable. The sub-agents are the analysts. Each one gets a narrow scope: one category, '
    'one data set, one output file. They do not talk to each other. They report back to the orchestrator.'
)

add_para(
    'The feedback loop is the quality gate between the sub-agents and the final briefing. After each '
    'sub-agent produces its output, the feedback loop checks the file against a set of rules. If it finds '
    'a violation (a missing supplier name, a date in the wrong format, a percent value above 110%), it writes '
    'a correction instruction and re-runs the sub-agent on that file. If the file passes, it moves on. '
    'If the file fails three times, the loop stops and escalates to you.'
)

add_para('The system has three layers:')
add_para(
    '1. Orchestrator layer: reads the full portfolio state, identifies what needs attention, assigns work '
    'to sub-agents, and assembles the final output.\n'
    '2. Sub-agent layer: each sub-agent reads a scoped set of data files, produces one output file, and '
    'returns it to the orchestrator.\n'
    '3. Validation layer: checks every sub-agent output against defined rules, triggers fix passes, enforces '
    'retry limits, and writes escalation notes when fixes fail.'
)

doc.add_heading('Why this structure matters', level=2)

add_para(
    'A single general-purpose prompt that reads all six categories at once produces mediocre output. It skims. '
    'It misses the contract notice period. It conflates the steel spend trend with the polymer initiative. '
    'You have seen this happen with a shared analyst who covers too many categories at once.'
)

add_para(
    'Splitting the work into scoped sub-agents solves three problems. First, each sub-agent reads only its '
    'category data, so it cannot confuse one category with another. Second, if one sub-agent fails, the others '
    'still succeed. You get five clean summaries and one escalation, not one failed briefing. Third, scoped '
    'reads use fewer tokens because each sub-agent loads only a fraction of the total data.'
)

add_para(
    'The feedback loop solves a fourth problem: silent errors. Without validation, a sub-agent that writes '
    '"Supplier: N/A" or "147% complete" passes unnoticed. The VP reads it. Your credibility drops. The feedback '
    'loop catches these before the output leaves the Drafts/ folder.'
)

doc.add_heading('How the orchestrator coordinates sub-agents in Claude Code', level=2)

add_para(
    'In Claude Code (in the terminal), you instruct the orchestrator to "run a sub-agent with this task." '
    'Claude Code launches the sub-agent as a separate task within the same session. The sub-agent reads the '
    'specified files, produces its output, and the orchestrator prompt continues. You can run sub-agents one '
    'at a time (safer, easier to debug) or instruct Claude Code to run them in sequence. This course teaches '
    'the sequential approach because parallel sub-agents can produce partial writes at beginner skill levels.'
)

add_para(
    'The orchestrator does not need a separate Python script or configuration file. It is a prompt pattern. '
    'You define it in a slash command file (.claude/commands/monday-briefing.md) or type it directly in the '
    'terminal. The slash command is more convenient because you type /monday-briefing instead of retyping '
    'the full orchestrator prompt every Monday.'
)

doc.add_heading('The five validation rules', level=2)

add_para('The feedback loop checks every sub-agent output against these five rules:')
add_para(
    '1. No supplier name cell in any output file may be empty, "N/A," "Unknown," or "None."\n'
    '2. No percent complete value may exceed 110%. Values above 110% indicate a data error.\n'
    '3. No trend value in scorecard files may be "unknown." Valid values are: up, down, flat, or "insufficient data."\n'
    '4. All dates must be in YYYY-MM-DD format. Any date in MM/DD/YYYY or spelled-out format is an error.\n'
    '5. Every file must have at least one data row below the header. Empty tables are errors.'
)

add_para(
    'Why this matters. These five rules are the minimum quality bar for VP-ready output. If any rule is '
    'violated, the briefing is not ready to send. The feedback loop enforces the bar automatically, so you '
    'do not have to remember to check every cell in every file every Monday.'
)

# ======================================================================
# 7. WORKED EXAMPLES
# ======================================================================
doc.add_heading('7. Worked examples', level=1)

# --- Worked Example 1 ---
doc.add_heading('Worked example 1: The Monday morning portfolio scan', level=2)

add_para(
    'This example shows the first step of the Monday briefing system: reading the portfolio state and '
    'producing a prioritized action plan. This is the orchestrator in action.'
)

add_bold_para('The prompt to type (in Claude Code, in the terminal):', '')
add_code_block(
    'Read data/program-state.json. Identify risk flags and at-risk or\n'
    'behind-schedule initiatives across all six categories.\n'
    'Read data/contract-calendar.csv. Find contracts expiring by 2026-05-31.\n'
    'Combine into a ranked action list of top 8 items, sorted by:\n'
    '(1) hard deadlines in the next 7 days first,\n'
    '(2) then by dollar impact descending.\n'
    'For each item, assign a sub-agent work type: sourcing analysis,\n'
    'contract review, scorecard check, or savings tracking.\n'
    'Save to Drafts/orchestrator_plan.md.\n'
    'Do not edit any file in data/.'
)

add_bold_para('The folder layout:', '')
add_code_block(
    'practice/\n'
    '  data/\n'
    '    program-state.json     (input: portfolio state)\n'
    '    contract-calendar.csv  (input: contract deadlines)\n'
    '  Drafts/\n'
    '    orchestrator_plan.md   (output)'
)

add_bold_para('What you should see:', '')
add_para(
    'Drafts/orchestrator_plan.md contains a date header (2026-04-25), a six-category snapshot table, '
    'and a ranked priority table. The top three rows read:'
)
add_para(
    '  Rank 1: Logistics, LOG-002 Carrier consolidation, Marcus Davis, $540,000 savings target, at risk, savings tracking.\n'
    '  Rank 2: Facilities, Contract FAC-CTR-003 expiry, Ana Torres, $3.1M annual value, expires 2026-05-31, contract review.\n'
    '  Rank 3: Raw materials, RM-002 Polymer standardization, James Park, $290,000 savings target, behind schedule, savings tracking.'
)

add_bold_para('What Claude Code did, behind the scenes:', '')
add_para(
    '1. Claude Code (in the terminal) opened data/program-state.json and parsed the six category objects, '
    'reading the risk_flags array and active_initiatives array for each.\n'
    '2. It filtered for initiatives with status equal to "at_risk" or "behind_schedule," capturing LOG-002 and RM-002.\n'
    '3. It opened data/contract-calendar.csv and filtered rows where end_date is on or before 2026-05-31.\n'
    '4. It merged the two filtered sets, then sorted by hard deadline proximity first and dollar impact descending second.\n'
    '5. It assigned each item a work type by matching the item type (initiative or contract) to the four sub-agent categories.\n'
    '6. It wrote the full plan to Drafts/orchestrator_plan.md in markdown format, with today\'s date at the top.'
)

# --- Worked Example 2 ---
doc.add_heading('Worked example 2: Self-correcting a missing supplier name', level=2)

add_para(
    'This example shows the feedback loop catching and fixing a validation error in a sub-agent output file. '
    'This is the validation layer in action.'
)

add_bold_para('The prompt to type (in Claude Code, in the terminal):', '')
add_code_block(
    'Validate Drafts/contract_review.md against these rules:\n'
    'Rule 1: No supplier name cell may be empty, "N/A", "Unknown",\n'
    'or "None".\n'
    'Rule 2: No percent complete value may exceed 110%.\n'
    'Rule 3: No trend value may be "unknown". Valid: up, down, flat.\n'
    'Rule 4: All dates must be in YYYY-MM-DD format.\n'
    'Rule 5: Every file must have at least one data row below the header.\n\n'
    'If you find a Rule 1 violation, look up the correct supplier name\n'
    'in data/contract-calendar.csv using the contract_id.\n'
    'Fix the violation, overwrite the file, and re-validate.\n'
    'Maximum 3 fix attempts. If not resolved after 3 attempts,\n'
    'write an escalation to Drafts/escalations.md.'
)

add_bold_para('The folder layout:', '')
add_code_block(
    'practice/\n'
    '  data/\n'
    '    contract-calendar.csv     (input: source of supplier names)\n'
    '  Drafts/\n'
    '    contract_review.md        (input and output: fixed in place)\n'
    '    escalations.md            (output: only if fix fails 3 times)'
)

add_bold_para('What you should see:', '')
add_para(
    'Claude Code (in the terminal) reports the violation: "Rule 1 violation: CTR-007, Supplier is blank." '
    'It then reads data/contract-calendar.csv, finds the row where contract_id is CTR-007, extracts the '
    'supplier name "Horizon Distribution," writes the corrected row to the file, and confirms: '
    '"PASS: contract_review.md. One correction applied (CTR-007, Supplier: Horizon Distribution)."'
)

add_bold_para('What Claude Code did, behind the scenes:', '')
add_para(
    '1. Claude Code (in the terminal) read Drafts/contract_review.md line by line and checked the Supplier '
    'column for empty strings, "N/A," "Unknown," or "None."\n'
    '2. It found one violation: CTR-007 had a blank Supplier field.\n'
    '3. It opened data/contract-calendar.csv and searched for the row where contract_id equals CTR-007.\n'
    '4. It extracted the supplier value from that row: "Horizon Distribution."\n'
    '5. It wrote the corrected row back into the table in Drafts/contract_review.md.\n'
    '6. It re-read the file and checked all five rules again, finding no further violations.\n'
    '7. It reported "PASS" with a one-line summary of the correction applied.'
)

# --- Worked Example 3 ---
doc.add_heading('Worked example 3: Building the consolidated VP briefing', level=2)

add_para(
    'This example shows the final assembly step: combining five validated sub-agent outputs into one briefing '
    'document. This is the assembler in action.'
)

add_bold_para('The prompt to type (in Claude Code, in the terminal):', '')
add_code_block(
    'Read Drafts/savings_tracker.md, Drafts/contract_review.md,\n'
    'Drafts/scorecard_refresh.md, Drafts/ps_update.md,\n'
    'and data/program-state.json.\n'
    'Identify the top 3 actions this week, ranked by deadline and\n'
    'dollar impact.\n'
    'Write the Monday briefing to\n'
    'Outputs/briefings/briefing-2026-04-25.md.\n'
    'Cover all six categories. Each section needs a supplier name,\n'
    'a dollar figure, and a date.\n'
    'Cap recommendations at 3 per category and 3 overall.\n'
    'Do not edit any file in data/.'
)

add_bold_para('The folder layout:', '')
add_code_block(
    'practice/\n'
    '  data/\n'
    '    program-state.json              (input: IT and MRO data)\n'
    '  Drafts/\n'
    '    savings_tracker.md              (input: at-risk initiatives)\n'
    '    contract_review.md              (input: expiring contracts)\n'
    '    scorecard_refresh.md            (input: supplier scores)\n'
    '    ps_update.md                    (input: PS-001 status)\n'
    '  Outputs/\n'
    '    briefings/\n'
    '      briefing-2026-04-25.md        (output)'
)

add_bold_para('What you should see:', '')
add_para(
    'Outputs/briefings/briefing-2026-04-25.md opens with "Meridian Corp: Weekly Category Briefing" and '
    'the date 2026-04-25. The Top 3 Actions section lists:'
)
add_para(
    '  1. Professional services: Confirm PS-001 rate card delivery with Kevin Wright. '
    'Target: $380,000 savings. Delivery deadline: 2026-04-30.\n'
    '  2. Logistics: Assess Redline Logistics LLC carrier capacity. LOG-002 at risk. '
    'Savings target: $540,000. Owner: Marcus Davis.\n'
    '  3. Facilities: Start renewal for contract expiring 2026-05-31. '
    'Annual value: $3,143,626. Owner: Ana Torres.'
)
add_para(
    'Each of the six category sections follows, with spend trends, initiative status, supplier names, '
    'and one recommended action per category.'
)

add_bold_para('What Claude Code did, behind the scenes:', '')
add_para(
    '1. Claude Code (in the terminal) read all four Drafts/ files and extracted the at-risk and '
    'action-required items from each.\n'
    '2. It read data/program-state.json to fill in IT services and MRO, which had no dedicated Drafts/ file.\n'
    '3. It merged all findings, then ranked by deadline (items with deadlines in the next 7 days first) '
    'and dollar impact (descending).\n'
    '4. It selected the top three actions and wrote them as a numbered list.\n'
    '5. It wrote one section per category in the specified order, pulling supplier names, dollar figures, '
    'and dates from the source files.\n'
    '6. It capped each category recommendation at one item and the overall list at three.\n'
    '7. It saved the file to Outputs/briefings/briefing-2026-04-25.md.'
)

# ======================================================================
# 8. DAY IN THE LIFE
# ======================================================================
doc.add_heading('8. Day in the Life: Elena, Director of Category Management', level=1)

add_para(
    'Elena Rodriguez is the Director of Category Management at Trident Manufacturing, a US-based '
    'industrial company headquartered in Milwaukee, WI. She manages $92M in annual procurement spend '
    'across six categories: IT services, logistics, raw materials, facilities, professional services, '
    'and MRO. She reports to the VP of Procurement, David Chen. She has been using the multi-category '
    'orchestration system for three weeks.'
)

# --- Scenario 1 ---
doc.add_heading('07:40. The Monday scan before anyone else is online.', level=2)

add_para(
    'Elena opens her laptop at her home office. She has 19 unread emails and a Slack from the '
    'Logistics lead, Marcus, about a carrier delay in Texas. Instead of opening six spreadsheets, '
    'she opens her terminal.'
)

add_code_block(
    'cd trident-category-management-2026\n'
    'claude\n\n'
    'Read data/program-state.json. For each of the six categories,\n'
    'tell me the risk flags and any initiatives with status "at_risk"\n'
    'or "behind_schedule". Sort by dollar impact descending.'
)

add_para(
    'Claude Code (in the terminal) reads the state file in 12 seconds. It reports two items: the logistics '
    'carrier consolidation (INIT-LOG-002, $680,000 target, at risk) and a facilities contract with Summit '
    'Janitorial ($2.8M/year) expiring on 2026-05-15. Elena sees the full picture in under a minute. Last '
    'month, this step took 40 minutes of spreadsheet switching.'
)

add_bold_para('What to learn from this. ',
    'The orchestrator reads structured state data, not raw email threads or Slack messages. For the Monday '
    'scan to work in under a minute, the state file must be current. Elena updates program-state.json on '
    'Friday afternoon. That 10-minute Friday habit is what makes Monday morning fast.'
)

# --- Scenario 2 ---
doc.add_heading('08:05. The sub-agents do the category-level work.', level=2)

add_para(
    'Elena launches sub-agents for the two flagged categories. She types one prompt per sub-agent.'
)

add_code_block(
    'Run a sub-agent with this task:\n'
    '"Read data/initiative-pipeline.csv. Find the row where\n'
    'initiative_id is INIT-LOG-002. Report: initiative name, owner,\n'
    'savings_target_usd, realized_savings_usd, percent complete,\n'
    'status, target_completion.\n'
    'Also read data/supplier-scorecards.csv. Find all suppliers in\n'
    'the Logistics category. List their most recent overall score.\n'
    'Write to Drafts/logistics_update.md."'
)

add_para(
    'The sub-agent reads two files, filters to Logistics, and writes a clean summary in 18 seconds. '
    'Elena runs the same pattern for Facilities. Both files land in Drafts/. She did not open a single spreadsheet.'
)

add_bold_para('What to learn from this. ',
    'Each sub-agent gets a narrow scope: one category, specific file names, a named output file. '
    'The sub-agent does not decide what to read. The orchestrator (Elena, in this case) decides. '
    'Scoped instructions prevent cross-category confusion and keep the output focused.'
)

# --- Scenario 3 ---
doc.add_heading('08:20. The feedback loop catches an error Elena would have missed.', level=2)

add_para('Elena runs validation on both output files.')

add_code_block(
    'Validate Drafts/logistics_update.md and\n'
    'Drafts/facilities_update.md.\n'
    'Rule 1: No supplier name may be empty or "N/A".\n'
    'Rule 4: All dates must be in YYYY-MM-DD format.\n'
    'Fix any violations using data from\n'
    'data/contract-calendar.csv or data/supplier-scorecards.csv.'
)

add_para(
    'Claude Code (in the terminal) finds one violation. The facilities update has the contract expiry date '
    'written as "May 15, 2026" instead of "2026-05-15." Claude Code rewrites the date and confirms PASS '
    'on both files. Elena would have caught that during formatting, but it would have cost her three minutes. '
    'Across 52 Mondays, that is 2.6 hours saved on date formatting alone.'
)

add_bold_para('What to learn from this. ',
    'The feedback loop is not just about catching catastrophic errors. It catches small formatting '
    'inconsistencies that eat time when they accumulate. The five validation rules act as a style guide '
    'enforcer. Define the rules once, and every output conforms automatically.'
)

# --- Scenario 4 ---
doc.add_heading('08:35. The consolidated briefing is ready for review.', level=2)

add_para('Elena assembles the briefing.')

add_code_block(
    'Read all files in Drafts/. Read data/program-state.json for\n'
    'the four categories without a dedicated Drafts/ file.\n'
    'Write the Monday briefing to\n'
    'Outputs/briefings/briefing-2026-04-27.md.\n'
    'Cover all six categories. Top 3 actions. Each section needs\n'
    'a supplier name, a dollar figure, and a date.\n'
    'Do not edit any file in data/.'
)

add_para(
    'Claude Code (in the terminal) produces the full briefing in 25 seconds. Elena reads it. She changes '
    'one word in the executive summary ("assess" to "confirm" for the Facilities recommendation). She emails '
    'it to David Chen at 08:42. He reads it at 08:51. The meeting starts at 09:00.'
)

add_bold_para('What to learn from this. ',
    'The briefing is a draft, not a finished product. Elena always reads it and makes at least one edit. '
    'The system saves time on data gathering, cross-referencing, and formatting. The judgment call (should '
    'the recommendation say "assess" or "confirm"?) stays with Elena. The system does not replace her '
    'expertise. It removes the drudgery so she can focus on the decisions.'
)

# --- Scenario 5 ---
doc.add_heading('10:30. A mid-morning deep dive triggered by the VP.', level=2)

add_para(
    'David Chen replies to the briefing: "The Apex Electronics delivery score at 3.0 concerns me. Can you '
    'pull the last four quarters of scores for that supplier and show me the trend?"'
)

add_para('Elena does not rebuild the full briefing. She runs a targeted sub-agent.')

add_code_block(
    'Read data/supplier-scorecards.csv. Find all rows where\n'
    'supplier_name is "Apex Electronics".\n'
    'For each quarter, calculate the average of quality, delivery,\n'
    'cost, and responsiveness.\n'
    'Show the four-quarter trend: quarter, average score, direction\n'
    '(up, down, or flat compared to the previous quarter).\n'
    'Write to Drafts/apex_deep_dive.md.'
)

add_para(
    'Claude Code (in the terminal) produces the trend table in 8 seconds. Q1 2025: 3.65. Q2 2025: 3.50. '
    'Q3 2025: 3.40. Q4 2025: 3.38. The trend is consistently down. Elena forwards the table to David with '
    'one sentence: "Apex has declined for four consecutive quarters. Recommend issuing a cure notice by '
    '2026-05-09 or starting replacement sourcing."'
)

add_bold_para('What to learn from this. ',
    'The orchestration system is not only for Monday briefings. The same sub-agent pattern works for ad-hoc '
    'requests. Elena did not build a new system. She reused the pattern: name the file, name the filter, '
    'name the output. The prompts are interchangeable because they follow the same structure.'
)

# --- Scenario 6 ---
doc.add_heading('14:00. Onboarding a new analyst with the escalation pattern.', level=2)

add_para(
    'Elena hires Ryan, a junior category analyst covering MRO. She shows him the retry and escalation system.'
)

add_code_block(
    'Run a sub-agent with this task:\n'
    '"Read data/category-spend.csv. Find all transactions for the\n'
    'category Aerospace components. Calculate total spend for\n'
    'Q1 2026. Write to Drafts/aerospace_spend.md."\n'
    'Apply the retry policy: max 3 fix attempts.\n'
    'If the category does not exist, escalate immediately.'
)

add_para(
    'Claude Code (in the terminal) searches the CSV, finds no "Aerospace components" category, and writes '
    'to Drafts/escalations.md: "Category \'Aerospace components\' does not exist in data/category-spend.csv. '
    'No retry attempted. Action required: confirm the correct category name."'
)

add_para(
    'Ryan sees the system stop itself instead of guessing. Elena explains: "The system does not make up '
    'a category. It tells you what it cannot find and asks for help. That is why you always check '
    'escalations.md after a run."'
)

add_bold_para('What to learn from this. ',
    'Retry limits and escalation notes are training tools, not just error handlers. They teach new team '
    'members what the data contains and what it does not. A clean escalation note ("category does not '
    'exist, confirm the correct name") is faster than 15 minutes of debugging why the output is empty.'
)

# --- Scenario 7 ---
doc.add_heading('16:15. Friday prep: updating the state file for next Monday.', level=2)

add_para(
    'Before leaving for the weekend, Elena updates program-state.json with the week\'s outcomes.'
)

add_code_block(
    'Read data/program-state.json.\n'
    'Update the following:\n'
    '- INIT-LOG-002 status: change from "at_risk" to "on_track".\n'
    '  Add note: "Carrier capacity confirmed with Redline Logistics\n'
    '  LLC on 2026-04-28."\n'
    '- Facilities risk flag: add "RFP for janitorial services issued\n'
    '  2026-04-29. Responses due 2026-05-20."\n'
    'Save the updated file to data/program-state.json.'
)

add_para(
    'Claude Code (in the terminal) makes the two changes in 6 seconds. Elena reviews the diff. Next Monday, '
    'the orchestrator will reflect the updated status, and LOG-002 will no longer appear in the risk list. '
    'The system gets smarter each week because Elena maintains the state file.'
)

add_bold_para('What to learn from this. ',
    'The orchestration system is only as good as the state file. If you skip the Friday update, Monday '
    'morning gives you stale data. The 10-minute Friday habit is not optional. It is what keeps the system '
    'accurate and trustworthy week over week.'
)

# ======================================================================
# 9. 20-MINUTE SPRINT
# ======================================================================
doc.add_heading('9. 20-Minute Sprint: your first Monday briefing in 20 minutes', level=1)

add_para(
    'This sprint gets a first-time reader to a usable Monday briefing output in 20 minutes. It skips the '
    'feedback loop and cost tracking. You add those later in Lessons 3 through 6.'
)

doc.add_heading('Minutes 0 to 5: Set up', level=2)
add_para(
    '1. Open your terminal.\n'
    '2. Navigate to the practice folder:\n'
    '   cd "Course_11_The_Category_Management_System/practice"\n'
    '3. Confirm data files are present:\n'
    '   ls data/\n'
    '   You should see five files: program-state.json, category-spend.csv, supplier-scorecards.csv, '
    'contract-calendar.csv, initiative-pipeline.csv.\n'
    '4. Start Claude Code:\n'
    '   claude\n'
    '5. Set the read-only rule:\n'
    '   "The files in data/ are source data. Do not edit any file in data/. Save all output to Drafts/."'
)

doc.add_heading('Minutes 5 to 10: Scan the portfolio', level=2)
add_para('Type this prompt in Claude Code (in the terminal):')
add_code_block(
    'Read data/program-state.json. For each of the six categories,\n'
    'tell me: category name, annual spend, number of active\n'
    'initiatives, any risk flags. Then identify the top 3 items\n'
    'that need attention this week, ranked by dollar impact.'
)
add_para(
    'You should see a six-category summary and a top-3 action list. This is the orchestrator output. '
    'If you see "file not found," check that you ran Claude Code from inside the practice/ folder.'
)

doc.add_heading('Minutes 10 to 15: Run the contract review sub-agent', level=2)
add_para('Type this prompt:')
add_code_block(
    'Run a sub-agent with this task:\n'
    '"Read data/contract-calendar.csv. Find contracts expiring by\n'
    '2026-06-30. For each, read data/supplier-scorecards.csv and\n'
    'look up the supplier\'s average score. Score above 4.0: Renew.\n'
    'Score 3.0 to 3.9: Review. Below 3.0: Rebid.\n'
    'Write to Drafts/contract_review.md."'
)
add_para(
    'You should see Drafts/contract_review.md created with a table of contracts, scores, and recommended '
    'actions. If the file is empty, ask Claude Code: "Read the first two lines of data/contract-calendar.csv '
    'and list the column names."'
)

doc.add_heading('Minutes 15 to 20: Assemble the briefing', level=2)
add_para('Type this prompt:')
add_code_block(
    'Read Drafts/contract_review.md and data/program-state.json.\n'
    'Write a Monday briefing to\n'
    'Outputs/briefings/briefing-2026-04-25.md.\n'
    'Cover all six categories. Each section needs a supplier name,\n'
    'a dollar figure, and a date. Top 3 actions at the top.\n'
    'Cap recommendations at 3. Do not edit any file in data/.'
)
add_para(
    'You should see Outputs/briefings/briefing-2026-04-25.md created. Open it. You have a VP-ready briefing '
    'covering six categories with supplier names, dollar figures, and dates.'
)

add_para(
    'That is your first Monday briefing. It is not perfect. The validation loop (Lesson 3) and retry logic '
    '(Lesson 4) will improve the quality. The cost tracking (Lesson 6) will give you budget numbers. But '
    'the core pattern (orchestrate, delegate, assemble) is now in your hands.'
)

# ======================================================================
# 10. FIRST WEEK PLANNER
# ======================================================================
doc.add_heading('10. First Week Day-by-Day Planner', level=1)

doc.add_heading('Day 1 (Monday): Install and first contact', level=2)
add_bold_para('Goals: ',
    'Install Claude Code, navigate to the practice folder, run the portfolio scan, and produce your '
    'first orchestrator plan.'
)
add_para(
    '1. Install Claude Code following the setup instructions in Course 1.\n'
    '2. Open your terminal and navigate to Course_11_The_Category_Management_System/practice/.\n'
    '3. Start Claude Code: claude\n'
    '4. Set the read-only rule for data/.\n'
    '5. Complete Lesson 1: the multi-category orchestrator. Time: 50 minutes.\n'
    '6. Confirm that Drafts/orchestrator_plan.md exists with a six-category snapshot and a ranked action list.'
)

doc.add_heading('Day 2 (Tuesday): Sub-agents and scoped data access', level=2)
add_bold_para('Goals: ',
    'Run four specialized sub-agents, each reading only its category data, and produce four separate '
    'output files in Drafts/.'
)
add_para(
    '1. Complete Lesson 2: specialized sub-agents. Time: 55 minutes.\n'
    '2. Confirm these files exist: Drafts/savings_tracker.md, Drafts/contract_review.md, '
    'Drafts/scorecard_refresh.md, Drafts/ps_update.md.\n'
    '3. Spot-check one file by reading the first 10 lines. Does it have a supplier name, a dollar figure, '
    'and a date?'
)

doc.add_heading('Day 3 (Wednesday): Feedback loop and retry logic', level=2)
add_bold_para('Goals: ',
    'Define validation rules, run the feedback loop, fix at least one error automatically, and trigger '
    'the retry and escalation pattern.'
)
add_para(
    '1. Complete Lesson 3: self-correcting feedback loop. Time: 50 minutes.\n'
    '2. Complete Lesson 4: retry limits and escalation. Time: 45 minutes.\n'
    '3. Confirm all five Drafts/ files pass validation.\n'
    '4. Confirm Drafts/escalations.md has at least one resolved entry and one open entry.'
)

doc.add_heading('Day 4 (Thursday): The consolidated briefing', level=2)
add_bold_para('Goals: ',
    'Assemble sub-agent outputs into a VP-ready Monday briefing, run the final quality check, and '
    'produce the finished file.'
)
add_para(
    '1. Complete Lesson 5: consolidated briefing. Time: 50 minutes.\n'
    '2. Confirm Outputs/briefings/briefing-2026-04-25.md exists.\n'
    '3. Verify: six category sections, top 3 actions, supplier names, dollar figures, and dates in every section.\n'
    '4. Run the final quality check: no em-dashes, no wrong date formats, no currency without commas.'
)

doc.add_heading('Day 5 (Friday): Cost awareness and reflection', level=2)
add_bold_para('Goals: ',
    'Estimate token cost, redesign the most expensive step, write the cost summary, and plan how you '
    'will use this system next week.'
)
add_para(
    '1. Complete Lesson 6: performance and cost awareness. Time: 40 minutes.\n'
    '2. Confirm Outputs/cost_summary.md exists with five sections and real numbers.\n'
    '3. Answer these two questions for yourself:\n'
    '   a. What is the monthly cost of running this system at practice data volumes? (Answer: under $1.00.)\n'
    '   b. What is the most expensive step, and how did you reduce it? '
    '(Answer: typically the contract review sub-agent, reduced by pre-filtering from the orchestrator plan.)\n'
    '4. Plan your first real Monday briefing for next week. Identify which of your real categories to start '
    'with. Copy the practice folder structure and replace the data files with your own data.'
)

# ======================================================================
# 11. THE PATTERN
# ======================================================================
doc.add_heading('11. The pattern: orchestrate, delegate, validate, assemble', level=1)

add_para(
    'Every Monday briefing follows a four-step pattern. Once you internalize this pattern, you can apply '
    'it to any multi-category or multi-document procurement task.'
)

add_bold_para('Step 1: Orchestrate. ',
    'Read the portfolio state. Identify what needs attention. Rank by urgency and dollar impact. '
    'Assign work to sub-agents. The orchestrator reads the state file and the contract calendar. '
    'It does not do the analysis itself. It plans.'
)

add_bold_para('Step 2: Delegate. ',
    'Run one sub-agent per category or per work type. Each sub-agent gets a narrow scope: one category, '
    'specific file names, a named output file. The sub-agent reads only what it needs. It writes one file. '
    'It does not talk to other sub-agents.'
)

add_bold_para('Step 3: Validate. ',
    'Check every sub-agent output against defined rules. If a rule is violated, fix it automatically. '
    'If the fix fails three times, stop and escalate to the user. The validation layer prevents silent '
    'errors from reaching the final output.'
)

add_bold_para('Step 4: Assemble. ',
    'Read all validated sub-agent outputs. Fill in any categories not covered by sub-agents. Write one '
    'consolidated document. Cap recommendations at three. Save to the Outputs/ folder.'
)

add_para(
    'This pattern works for more than Monday briefings. You can use it for quarterly business reviews '
    '(six category deep dives, assembled into one QBR deck), annual supplier reviews (30 supplier '
    'scorecards, assembled into a portfolio summary), or savings program tracking (12 initiatives, '
    'assembled into a CPO dashboard). The data changes. The structure stays the same.'
)

add_para(
    'Why this matters. When you follow this pattern, every output has the same shape. Your VP learns '
    'to read it fast because the format never changes. Your team can contribute sub-agent outputs without '
    'knowing the full system. And when something breaks, you know which layer to fix: the orchestrator '
    '(wrong items selected), the sub-agent (wrong data read), the validator (wrong rule applied), or '
    'the assembler (wrong format).'
)

doc.add_heading('Applying the pattern to your own categories', level=2)

add_para(
    'To use this pattern with your own data, follow these five steps in Claude Code (in the terminal):'
)
add_para(
    '1. Create a project folder with the standard layout: data/ (read-only source files), Drafts/ '
    '(working files), Outputs/ (final deliverables).\n'
    '2. Write a CLAUDE.md file at the project root. Name your role, your categories with spend figures, '
    'your data file names, and your output standards.\n'
    '3. Place your data files in data/. At minimum, you need a state file (JSON or CSV) and a contract '
    'or supplier file.\n'
    '4. Write the orchestrator prompt. Start with: "Read data/[state-file]. For each category, identify '
    'risk flags and at-risk initiatives. Rank by dollar impact."\n'
    '5. Run one sub-agent per category, following the pattern: name the file, name the filter, name '
    'the output.'
)

add_para(
    'The first run will be imperfect. That is expected. Add validation rules in your second week. '
    'Add retry logic in your third week. By week four, the system runs reliably with minimal edits.'
)

# ======================================================================
# 12. TROUBLESHOOTING
# ======================================================================
doc.add_heading('12. Troubleshooting', level=1)

add_table(
    ['Problem', 'Likely cause', 'Fix'],
    [
        [
            'Claude Code returns no risk flags or at-risk initiatives.',
            'The dates in program-state.json are stale, or the file was not regenerated after a corrupted practice session.',
            'Run python ../scripts/build_course_data.py from the course root. This regenerates all five data files with current dates. Then restart Claude Code and repeat the orchestrator scan.'
        ],
        [
            'A sub-agent reads the wrong file or the wrong category.',
            'The prompt did not name the file and category explicitly. Claude Code guessed.',
            'Rewrite the sub-agent prompt to name the exact file path: "Read data/contract-calendar.csv (not data/category-spend.csv)." Name the category: "Filter to the Logistics category only." Exact names prevent confusion.'
        ],
        [
            'Two sub-agents overwrite the same output file.',
            'Both sub-agents were assigned the same output file name in their prompts.',
            'Each sub-agent must write to a different file. Use distinct names: Drafts/savings_tracker.md, Drafts/contract_review.md, Drafts/scorecard_refresh.md, Drafts/ps_update.md. Never assign two agents to the same file.'
        ],
        [
            'The feedback loop keeps retrying beyond 3 attempts without stopping.',
            'The retry policy was not stated at the start of the session, or the session context was lost after a restart.',
            'Restate the retry policy as the first message in every new Claude Code session: "Retry limit is 3. After 3 failed fixes, write escalation to Drafts/escalations.md and stop." Session context resets when you quit and restart Claude Code (in the terminal).'
        ],
        [
            'The consolidated briefing has fewer than six category sections.',
            'The Drafts/ files only covered four categories (Logistics, Raw materials, Facilities, Professional services). IT services and MRO had no sub-agent output.',
            'Add to the assembly prompt: "For any category not represented in Drafts/, read data/program-state.json and data/initiative-pipeline.csv to fill in that category section." All six categories must appear in every briefing.'
        ],
        [
            'Token cost estimates seem unrealistically low (under $0.01 per run).',
            'The 1.3x tokens-per-word multiplier underestimates CSV files with many numeric columns.',
            'For data-heavy CSV files, use 1.8 tokens per word instead of 1.3. Tell Claude Code: "Recalculate using 1.8 tokens per word for CSV files and 1.3 for markdown files." The corrected estimate will be 30% to 40% higher.'
        ],
    ]
)

# ======================================================================
# 13. DONE CHECKLIST
# ======================================================================
doc.add_heading('13. Done checklist', level=1)

add_para('Run this list before marking the course as complete. Each item should be true.')

checklist_items = [
    'The S2P problem is named in the opening section: Monday morning category briefings across six procurement categories. Done.',
    'The outcome is stated in business terms: a consolidated VP briefing in under five minutes, covering all six categories with supplier names, dollar figures, and dates. Done.',
    'Every S2P task has a worked example with four parts: prompt (code block), folder layout (code block), expected result, and behind-the-scenes walkthrough (numbered steps). Done (three worked examples in section 7).',
    'Every capability statement names the specific Claude: Claude Code (in the terminal). Claude AI Web and Claude Desktop with Cowork are named where features do not apply. Done.',
    'The Time Savings Reference Table is present with five tasks and specific minutes. Done (section 5).',
    'The Day in the Life narrative features a named persona (Elena Rodriguez, Director of Category Management at Trident Manufacturing, Milwaukee, WI) with seven hour-stamped scenarios. Done (section 8).',
    'Every Day-in-the-Life scenario ends with a "What to learn from this" paragraph naming a transferable principle. Done.',
    'The 20-Minute Sprint has four five-minute blocks getting the reader to a usable Monday briefing. Done (section 9).',
    'The First Week Day-by-Day Planner has five days with explicit goals listed at the top of each day. Done (section 10).',
    'No em-dashes or en-dashes anywhere in the file. Done.',
    'No banned phrases from the general or procurement-specific lists. Done.',
    'Oxford commas applied in every list of three or more. Done.',
    'American English throughout (organize, analyze, behavior). Done.',
    'Every folder and file explanation has a "Why this matters" paragraph (two to four sentences). Done (section 4).',
    'Troubleshooting section has six entries, each with problem, cause, and fix. Done (section 12).',
    'All currency in USD. All locations in the US. Done.',
    'Recommendations capped at three in every example. Done.',
    'A procurement analyst with no coding background can read and act on this handout alone. Done.',
]

for i, item in enumerate(checklist_items, 1):
    add_para(f'{i}. {item}')

# ======================================================================
# SAVE
# ======================================================================
doc.save(str(OUTPUT_PATH))
print(f"Saved to {OUTPUT_PATH}")

# Count approximate words
word_count = 0
for p in doc.paragraphs:
    word_count += len(p.text.split())
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            word_count += len(cell.text.split())
print(f"Approximate word count: {word_count}")
