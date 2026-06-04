#!/usr/bin/env python3
"""Build Course 08 The Project Architect comprehensive handout as .docx"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT = PROJECT_ROOT / "Handouts" / "Course_08_The_Project_Architect_Handout.docx"

doc = Document()

# ── Style setup ──────────────────────────────────────────────────
style_normal = doc.styles['Normal']
style_normal.font.name = 'Calibri'
style_normal.font.size = Pt(11)
style_normal.paragraph_format.space_after = Pt(6)
style_normal.paragraph_format.line_spacing = 1.15

# Heading 1
h1 = doc.styles['Heading 1']
h1.font.name = 'Calibri'
h1.font.size = Pt(14)
h1.font.bold = True
h1.font.color.rgb = RGBColor(0x36, 0x5F, 0x91)

# Heading 2
h2 = doc.styles['Heading 2']
h2.font.name = 'Calibri'
h2.font.size = Pt(13)
h2.font.bold = True
h2.font.color.rgb = RGBColor(0x4F, 0x81, 0xBD)

# Heading 3
h3 = doc.styles['Heading 3']
h3.font.name = 'Calibri'
h3.font.size = Pt(11)
h3.font.bold = True
h3.font.color.rgb = RGBColor(0x4F, 0x81, 0xBD)

# Title
title_style = doc.styles['Title']
title_style.font.name = 'Calibri'
title_style.font.size = Pt(26)
title_style.font.color.rgb = RGBColor(0x17, 0x36, 0x5D)


def add_para(text, style='Normal', bold=False, italic=False, alignment=None):
    p = doc.add_paragraph(text, style=style)
    if bold or italic:
        for run in p.runs:
            if bold:
                run.bold = True
            if italic:
                run.italic = True
    if alignment:
        p.alignment = alignment
    return p


def add_code_block(text):
    """Add a code block as a styled paragraph with monospace font and gray background."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    # Add shading
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), 'F2F2F2')
    shading.set(qn('w:val'), 'clear')
    p.paragraph_format.element.get_or_add_pPr().append(shading)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    return p


def add_bold_then_normal(bold_text, normal_text):
    p = doc.add_paragraph()
    r1 = p.add_run(bold_text)
    r1.bold = True
    r2 = p.add_run(normal_text)
    return p


def add_table(headers, rows):
    """Add a formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for par in cell.paragraphs:
            for run in par.runs:
                run.bold = True
                run.font.name = 'Calibri'
                run.font.size = Pt(10)
    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10)
    doc.add_paragraph()  # spacing
    return table


# ======================================================================
# HEADER
# ======================================================================
add_para('U2xAI', alignment=WD_ALIGN_PARAGRAPH.LEFT)
add_para('PROCUREAI ACADEMY', alignment=WD_ALIGN_PARAGRAPH.LEFT)
add_para('Series 2 (Engineering Track) | Course 8', alignment=WD_ALIGN_PARAGRAPH.LEFT)
doc.add_paragraph('The Project Architect', style='Title')
add_para('Cross-session memory for savings program management with persistent state files, decisions logs, and slash commands.')
add_para('Six lessons. No coding. Use this handout alongside the course folder at Detailed Course Content/Course_08_The_Project_Architect/.')

# ======================================================================
# 1. HOW TO USE THIS HANDOUT
# ======================================================================
doc.add_heading('1. How to use this handout', level=1)

add_para('This handout is your reading companion. The hands-on work happens in the course folder you received with the training materials. The folder has the data, the starter files, the six lessons, and the reference solutions.')

add_para('How to read this guide:')

add_para(
    '1. Read sections 2 and 3 to understand what the course is and what you end up with.\n'
    '2. Read section 4 to see how much time the project pattern saves you per week.\n'
    '3. Read section 5 for the mental model of what a Claude Code project is.\n'
    '4. Open the course folder and start Lesson 1.\n'
    '5. Come back to this handout when you want context (sections 6 and 7 are useful while you work).\n'
    '6. Use section 11 (troubleshooting) if something does not look right.'
)

add_para('Keep this handout open beside your terminal. When a lesson references a concept (state file, decisions log, slash command, settings.json), the explanation is here.')

# ======================================================================
# 2. WHAT THIS COURSE TEACHES
# ======================================================================
doc.add_heading('2. What this course teaches', level=1)

doc.add_heading('A Monday morning you have lived before', level=2)

add_para(
    'It is Monday morning, 09:15. You open Claude Code (in the terminal) to check on the savings program. '
    'You type: "What is the status of the direct materials consolidation initiative?" '
    'Claude Code responds: "I don\'t have context about a direct materials consolidation initiative. Could you provide more details?"'
)

add_para(
    'You spent 45 minutes last Thursday building a detailed status update for that exact initiative. '
    'You reviewed the savings log. You checked two overdue milestones. You drafted an escalation note to Lisa Torres, '
    'VP of Procurement. All of that context vanished when you closed the terminal session.'
)

add_para(
    'This happens because Claude Code conversations are temporary. When a session ends, the conversation history goes with it. '
    'Every Monday, you re-explain the program, re-read the data files, and re-state decisions you already made. '
    'For a Savings Program Manager running eight initiatives with a combined $14.9M target, rebuilding context takes 20 to 30 minutes per session. '
    'Over a month, that is 80 to 120 minutes of wasted re-explanation.'
)

doc.add_heading('What this course fixes', level=2)

add_para(
    'You build a Claude Code project: a folder with a .claude/ directory, a CLAUDE.md file, persistent state files, '
    'a decisions log, and reusable slash commands. When you open Claude Code (in the terminal) on Monday, it reads the '
    'initiative tracker, sees the current stage and status of all eight initiatives, and picks up where you left off. '
    'No more rebuilding context. No more lost decisions.'
)

add_para(
    'The course uses a realistic scenario. You are the Savings Program Manager at Pinnacle Procurement, a US-based '
    'procurement team. Your eight category initiatives span direct materials, logistics, IT services, facilities, '
    'professional services, and MRO. Your VP wants a weekly review every Monday. Your CFO wants a monthly savings update. '
    'Both need current data and context from the last session.'
)

doc.add_heading('The six lessons', level=2)

add_table(
    ['#', 'Lesson title', 'Time'],
    [
        ['1', 'What a Claude Code project is: .claude/, settings.json, and project vs. global config', '30 min'],
        ['2', 'Project CLAUDE.md: encoding all eight initiatives with stage and status', '45 min'],
        ['3', 'Persistent state with files: maintaining an initiative tracker across sessions', '50 min'],
        ['4', 'The decisions log pattern: appending decisions to a persistent file', '40 min'],
        ['5', 'Project-level settings.json: tool permissions, hooks, and slash commands', '40 min'],
        ['6', 'Team project sharing: git repository, CLAUDE.md updates, state file conventions', '35 min'],
    ]
)

add_para('Total: about 4.5 hours. Comfortable in two afternoon sessions.')

# ======================================================================
# 3. WHAT IS IN THE COURSE FOLDER
# ======================================================================
doc.add_heading('3. What is in the course folder', level=1)

add_para('The course folder is self-contained. Everything you need is inside it.')

add_code_block(
    'Course_08_The_Project_Architect/\n'
    '  README.md\n'
    '  COURSE_OVERVIEW.md\n'
    '  lessons/\n'
    '    Lesson_01_What_A_Project_Is.md\n'
    '    Lesson_02_Project_CLAUDE_MD.md\n'
    '    Lesson_03_Persistent_State_Files.md\n'
    '    Lesson_04_Decisions_Log.md\n'
    '    Lesson_05_Project_Settings.md\n'
    '    Lesson_06_Team_Project_Sharing.md\n'
    '  practice/\n'
    '    CLAUDE.md\n'
    '    data/\n'
    '      initiatives.csv\n'
    '      savings-log.csv\n'
    '      stakeholders.csv\n'
    '      milestone-tracker.csv\n'
    '  solutions/\n'
    '    claude_md_solution.md\n'
    '    initiative_tracker_solution.md\n'
    '    decisions_log_solution.md\n'
    '    weekly_review_command_solution.md\n'
    '    program_state_solution.json\n'
    '  scripts/\n'
    '    build_course_data.py'
)

doc.add_heading('README.md', level=3)
add_para('Course navigation. What is in the folder. How to start. Read this first.')
add_para('Why this matters. Without it, you open the folder and see 20 files with no map. The README tells you which file to open next and what order the lessons follow.')

doc.add_heading('COURSE_OVERVIEW.md', level=3)
add_para('The scenario, the eight initiatives, the target folder structure you will build, and the rubric for "done." Read this before Lesson 1.')
add_para('Why this matters. The overview sets the success criteria. When you finish the course, you check your work against the rubric. If you skip the overview, you will not know when you are done.')

doc.add_heading('lessons/', level=3)
add_para('Six numbered lesson files. Each lesson opens with a day-to-day scenario, walks through every step with exact commands, and ends with a "you are done when" checklist. Follow them in order.')
add_para('Why this matters. The lessons build on each other. Lesson 3 (state files) assumes Lesson 2 (CLAUDE.md) is complete. Lesson 5 (slash commands) assumes Lesson 4 (decisions log) exists. Skipping a lesson breaks the chain.')

doc.add_heading('practice/', level=3)
add_para('Your working folder. It contains a starter CLAUDE.md and a data/ subfolder with four CSV files: initiatives.csv (8 rows), savings-log.csv (120 rows), stakeholders.csv (12 rows), and milestone-tracker.csv (40 rows). You run Claude Code (in the terminal) from inside this folder.')
add_para('Why this matters. Running Claude Code from the wrong folder means it will not find CLAUDE.md, the .claude/ directory, or the data files. Every lesson assumes you are inside practice/.')

doc.add_heading('solutions/', level=3)
add_para('Reference answers for each lesson. Look at them only after attempting the lesson yourself. The learning happens in the attempt, not in reading the answer.')
add_para('Why this matters. If you read the solution first, you copy instead of build. Building the CLAUDE.md yourself teaches you what to include and what to leave out. Reading someone else\'s version does not.')

doc.add_heading('scripts/build_course_data.py', level=3)
add_para('Regenerates all practice data deterministically using random.seed(42). If you accidentally delete or corrupt a data file, run: python scripts/build_course_data.py')
add_para('Why this matters. Practice data must be reproducible. If your savings-log.csv gets corrupted mid-lesson, you need a one-command restore, not a re-download from a shared drive.')

# ======================================================================
# 4. TIME SAVINGS TABLE
# ======================================================================
doc.add_heading('4. What the project pattern saves you each week', level=1)

add_para(
    'The table below compares five common savings-program tasks before and after you set up a Claude Code project. '
    'Times are based on a program with eight initiatives, 120 savings log entries, 40 milestones, and 12 stakeholders.'
)

add_table(
    ['Task', 'Without a project', 'With a project', 'Time saved'],
    [
        ['Re-establish program context at session start', '20 to 30 min (re-type portfolio, stages, owners)', '0 min (CLAUDE.md loads automatically)', '20 to 30 min'],
        ['Check status of a single initiative', '8 to 12 min (read CSV, filter, calculate variance)', '30 sec (type /initiative-status INIT-001)', '8 to 11 min'],
        ['Produce the weekly VP review', '35 to 45 min (read all files, format, save)', '2 min (type /weekly-review)', '33 to 43 min'],
        ['Recall a decision from last week', '5 to 15 min (search email, Slack, notes)', '30 sec (read state/decisions-log.md)', '5 to 14 min'],
        ['Onboard a teammate to the program setup', '30 to 45 min (walk through files, explain context)', '5 min (clone repo, run claude, context loads)', '25 to 40 min'],
    ]
)

add_para('Total weekly savings across these five tasks: roughly 90 to 140 minutes per week, or 6 to 9 hours per month. For a $14.9M savings program, that time goes back into initiative execution instead of context rebuilding.')

# ======================================================================
# 5. WHAT A CLAUDE CODE PROJECT IS
# ======================================================================
doc.add_heading('5. What a Claude Code project is', level=1)

doc.add_heading('The mental model', level=2)

add_para(
    'A Claude Code project is a folder on your computer that contains three things: '
    'a .claude/ directory with settings, a CLAUDE.md file with standing context, and your working files. '
    'When you run the command "claude" inside that folder, Claude Code (in the terminal) reads .claude/settings.json '
    'for permissions and hook registrations. It reads CLAUDE.md for your role, your program, your data locations, '
    'and your output rules. It reads any state files you have created.'
)

add_para(
    'The key insight: conversation history is temporary, but files are permanent. '
    'If you write a decision to a file during a session, the next session can read that file. '
    'If you maintain an initiative tracker as a markdown file, every session starts with current state. '
    'The project pattern turns Claude Code from a tool with amnesia into a tool with a filing cabinet.'
)

doc.add_heading('What a project gives you (compared to a bare session)', level=2)

add_table(
    ['Without a project', 'With a project'],
    [
        ['Every session starts blank', 'Every session reads CLAUDE.md and state files'],
        ['Decisions are lost when the session ends', 'Decisions are appended to state/decisions-log.md'],
        ['Initiative status is re-derived every time', 'Initiative status is read from state/initiative-tracker.md'],
        ['Slash commands do not exist', 'Slash commands persist in .claude/commands/'],
        ['Permissions must be granted manually', 'Permissions are pre-set in .claude/settings.json'],
        ['Teammates start from zero', 'Teammates clone the repo and get full context on first run'],
    ]
)

doc.add_heading('CLAUDE.md: the standing context file', level=2)

add_para(
    'CLAUDE.md is a markdown file at the root of your project folder. Claude Code (in the terminal) reads it '
    'automatically at session start. It should contain what every session needs: your role, the program name, '
    'the initiative portfolio (IDs, names, owners, targets, stages, statuses), key stakeholders, stage definitions, '
    'file locations, and output formatting rules.'
)

add_para(
    'Keep CLAUDE.md between 60 and 120 lines. If it grows past 150 lines, move detail into separate files '
    'and reference them from CLAUDE.md. Put in what every session needs. Leave out what only some sessions need.'
)

add_para(
    'Why this matters. Without CLAUDE.md, you spend the first 10 to 20 minutes of every session re-explaining '
    'your program. With it, Claude Code already knows you manage eight initiatives at Pinnacle Procurement with a '
    '$14.9M target. You skip straight to the work.'
)

doc.add_heading('Persistent state files', level=2)

add_para(
    'State files live in the state/ folder. They persist across sessions because they are files on disk. '
    'Two patterns matter for savings program management:'
)

add_bold_then_normal(
    'initiative-tracker.md (updated in place). ',
    'Records the current status, realized savings, variance, next milestone, and notes for each initiative. '
    'Claude Code reads it at session start and updates it before session end. Think of it as the "current snapshot" of your program.'
)

add_bold_then_normal(
    'decisions-log.md (append only). ',
    'Records every program decision with date, initiative, decision text, context, and approver. '
    'Claude Code appends new entries at the bottom. It never deletes or edits old entries. '
    'Think of it as the audit trail your CFO or VP will ask for.'
)

add_para(
    'Why this matters. Without state files, you close the session and lose 30 minutes of analysis. '
    'With them, the next session picks up exactly where you left off. The initiative tracker tells Claude what changed. '
    'The decisions log tells Claude (and your stakeholders) why it changed.'
)

doc.add_heading('The decisions log pattern', level=2)

add_para(
    'The decisions log deserves special attention because it solves a specific procurement problem: accountability. '
    'When Marcus Rivera asks "did we push the INIT-007 bid evaluation milestone to June, or did we keep it in May?", '
    'you need a dated, attributed answer. Not a vague memory.'
)

add_para(
    'Each decision entry has six fields: date (YYYY-MM-DD), initiative (ID and name), decision (what was decided), '
    'context (why), approved by (who approved it), and recorded by (who wrote the entry). '
    'The append-only rule means no one can quietly change history. The log grows session by session.'
)

add_para(
    'Why this matters. Procurement decisions need an audit trail. When the CFO asks "why did the timeline slip?", '
    'you open decisions-log.md and show the entry. Date, rationale, approver. No searching through Slack threads or email.'
)

doc.add_heading('.claude/settings.json: project-level permissions', level=2)

add_para(
    'The .claude/settings.json file inside your project folder controls what Claude Code (in the terminal) can read and write. '
    'For a savings program, a sensible default is: read access to data/* and state/*, write access to state/* and outputs/*. '
    'This prevents Claude from accidentally modifying your source data in data/.'
)

add_para(
    'Project settings override global settings. Your global ~/.claude/settings.json applies everywhere. '
    'Your project .claude/settings.json applies only when you run claude inside this folder. '
    'Keep program-specific rules in the project file. Keep machine-wide defaults in the global file.'
)

add_para(
    'Why this matters. Without explicit permissions, you risk Claude overwriting your source CSVs or reading files '
    'outside the project. With them, data/ is read-only and outputs go to the right folder every time.'
)

doc.add_heading('Slash commands: repeatable workflows', level=2)

add_para(
    'Slash commands are markdown files in .claude/commands/. Each file contains instructions that Claude Code '
    '(in the terminal) follows when you type the command name. For example, typing /initiative-status INIT-001 '
    'triggers the instructions in .claude/commands/initiative-status.md. The $ARGUMENTS placeholder in the file '
    'is replaced with "INIT-001".'
)

add_para(
    'Two commands cover most savings-program workflows: /initiative-status (per-initiative deep check) '
    'and /weekly-review (consolidated VP review across all eight initiatives).'
)

add_para(
    'Why this matters. Without slash commands, you type the same 50-word prompt every Monday. '
    'With them, you type 3 words and Claude Code runs the full workflow. The commands persist across sessions '
    'and across teammates because they are files in the repo.'
)

# ======================================================================
# 6. WORKED EXAMPLES
# ======================================================================
doc.add_heading('6. Worked examples', level=1)

doc.add_heading('Example A: checking a single initiative with /initiative-status', level=2)

add_para(
    'You want to know the current status of INIT-002 (Logistics Network Optimization). '
    'The initiative is at risk. Your VP asked for an update before the Monday meeting.'
)

add_bold_then_normal('The prompt you type in Claude Code (in the terminal).', '')
add_code_block('/initiative-status INIT-002')

add_bold_then_normal('The folder layout.', '')
add_code_block(
    'savings-program-2026/\n'
    '  .claude/\n'
    '    settings.json\n'
    '    commands/\n'
    '      initiative-status.md\n'
    '  CLAUDE.md\n'
    '  state/\n'
    '    initiative-tracker.md\n'
    '    decisions-log.md\n'
    '  data/\n'
    '    initiatives.csv\n'
    '    savings-log.csv\n'
    '    milestone-tracker.csv\n'
    '    stakeholders.csv'
)

add_bold_then_normal('What you should see.', '')
add_para(
    'A status update showing: INIT-002 Logistics Network Optimization, owner Marcus Rivera, stage Sourcing, '
    'status At risk, $297,115 realized savings to date, variance -$168,269 versus cumulative target, '
    'next milestone "Market analysis complete" due 2026-05-02, and the note about two carriers declining to bid.'
)

add_bold_then_normal('What Claude Code did, behind the scenes.', '')
add_para(
    '1. Claude Code read .claude/commands/initiative-status.md and replaced $ARGUMENTS with "INIT-002".\n'
    '2. Claude Code read state/initiative-tracker.md and found the INIT-002 section with current status and notes.\n'
    '3. Claude Code read data/savings-log.csv (120 rows), filtered for initiative_id = INIT-002, and summed realized_savings_usd to get $297,115.\n'
    '4. Claude Code read data/milestone-tracker.csv (40 rows), filtered for INIT-002, identified the next pending milestone and any overdue milestones.\n'
    '5. Claude Code combined the tracker state, the live savings data, and the milestone data into a single formatted status update.\n'
    '6. Claude Code included the note from the tracker ("two carriers declined to bid") because the command file instructs it to include notes.'
)

doc.add_heading('Example B: producing the weekly VP review with /weekly-review', level=2)

add_para(
    'It is Monday morning. Lisa Torres, VP of Procurement, needs the weekly review for her 10:00 leadership meeting. '
    'You open Claude Code (in the terminal) and type one command.'
)

add_bold_then_normal('The prompt you type in Claude Code (in the terminal).', '')
add_code_block('/weekly-review')

add_bold_then_normal('The folder layout.', '')
add_para('Same as Example A. The /weekly-review command reads all data and state files.')

add_bold_then_normal('What you should see.', '')
add_para(
    'Claude Code saves a file to outputs/weekly-reviews/weekly-review-2026-04-25.md. The file contains five sections: '
    '(1) an executive summary naming the $14.9M target, $4,500,000 realized year-to-date (30.2% of target), '
    'five initiatives on track, one at risk, one behind schedule, and one not started; '
    '(2) an initiative-by-initiative status table with all eight rows; '
    '(3) a key risks section naming INIT-002 (at risk, two carriers declined to bid) and INIT-007 (behind schedule, '
    'two milestones overdue, qualification testing blocked by engineering); '
    '(4) decisions made this week from the decisions log; '
    '(5) next week priorities listing the nearest pending milestones sorted by date.'
)

add_bold_then_normal('What Claude Code did, behind the scenes.', '')
add_para(
    '1. Claude Code read .claude/commands/weekly-review.md for the full review instructions.\n'
    '2. Claude Code read state/initiative-tracker.md for current status and notes on all eight initiatives.\n'
    '3. Claude Code read state/decisions-log.md and filtered for entries from the past 7 days.\n'
    '4. Claude Code read data/savings-log.csv and calculated realized savings by initiative, summing 120 rows.\n'
    '5. Claude Code read data/milestone-tracker.csv and identified pending and overdue milestones across 40 rows.\n'
    '6. Claude Code assembled all five sections, formatted the initiative table, and saved the output to outputs/weekly-reviews/weekly-review-2026-04-25.md.\n'
    '7. Claude Code updated the "Last updated" timestamp in state/initiative-tracker.md to 2026-04-25.'
)

doc.add_heading('Example C: recording a decision to the append-only log', level=2)

add_para(
    'You and Marcus Rivera just decided to add two alternate carriers (Estes Express and Old Dominion) to the INIT-002 bid list '
    'because FedEx Freight and XPO Logistics declined. Tom Baker, Supply Chain Director, approved the change. '
    'You need to record this decision so the next session (and any teammate) can see it.'
)

add_bold_then_normal('The prompt you type in Claude Code (in the terminal).', '')
add_code_block(
    'Append a new entry to state/decisions-log.md. Do not modify any existing content.\n\n'
    'Date: 2026-04-25\n'
    'Initiative: INIT-002 (Logistics Network Optimization)\n'
    'Decision: Add Estes Express and Old Dominion to the bid list to replace declined bidders.\n'
    'Context: FedEx Freight and XPO Logistics declined to bid. Both replacements meet the $50M revenue threshold.\n'
    'Approved by: Tom Baker (Supply Chain Director)\n'
    'Recorded by: Savings Program Manager'
)

add_bold_then_normal('The folder layout.', '')
add_para('Same as Examples A and B. The decisions log lives at state/decisions-log.md.')

add_bold_then_normal('What you should see.', '')
add_para(
    'Claude Code confirms it appended the entry to the bottom of state/decisions-log.md. '
    'All previous entries remain unchanged. The new entry appears below the last separator line.'
)

add_bold_then_normal('What Claude Code did, behind the scenes.', '')
add_para(
    '1. Claude Code read state/decisions-log.md to find the end of the file.\n'
    '2. Claude Code appended a new section with the H2 heading "2026-04-25: INIT-002 (Logistics Network Optimization)".\n'
    '3. Claude Code wrote the six fields (date, initiative, decision, context, approved by, recorded by) in bold-label format.\n'
    '4. Claude Code added a horizontal rule separator after the entry.\n'
    '5. Claude Code did not modify any existing content in the file. The append-only rule was followed.'
)

# ======================================================================
# 7. DAY IN THE LIFE
# ======================================================================
doc.add_heading('7. A day in the life: Dana, Savings Program Manager', level=1)

doc.add_heading('Meet Dana', level=2)

add_para(
    'Dana is a Savings Program Manager at Pinnacle Procurement, a US-based procurement team. '
    'She manages eight category initiatives with a combined annual savings target of $14.9M. '
    'Her VP, Lisa Torres, expects a weekly review every Monday morning. Her CFO, Robert Hayes, '
    'gets a monthly savings update on the last business day of each month. '
    'Dana set up her Claude Code project three weeks ago using the pattern from this course.'
)

doc.add_heading('08:30. Monday morning: the VP review', level=2)

add_para(
    'Dana opens her terminal, navigates to the savings-program-2026/ folder, and starts Claude Code (in the terminal).'
)
add_code_block('cd savings-program-2026\nclaude')

add_para(
    'Claude Code loads CLAUDE.md, reads the eight-initiative portfolio, and loads .claude/settings.json. '
    'Dana types one command.'
)
add_code_block('/weekly-review')

add_para(
    'Claude Code reads state/initiative-tracker.md, state/decisions-log.md, data/savings-log.csv, '
    'and data/milestone-tracker.csv. Two minutes later, the weekly review is saved to '
    'outputs/weekly-reviews/weekly-review-2026-04-28.md. The executive summary reads: '
    '"Pinnacle Procurement savings program: $4,500,000 realized year-to-date against a $14.9M annual target '
    '(30.2%). Five initiatives on track. INIT-002 (Logistics Network Optimization) at risk. '
    'INIT-007 (Packaging Material Switch) behind schedule. INIT-006 not started."'
)

add_para('Dana opens the file, reads through it, fixes one typo in the INIT-005 section, and emails it to Lisa Torres. Total time: 7 minutes.')

add_bold_then_normal('What to learn from this. ',
    'The /weekly-review command does in 2 minutes what used to take 35 to 45 minutes. '
    'The command is a file in .claude/commands/. It runs the same workflow every week, but the data changes. '
    'You write the instructions once. Claude Code follows them every Monday.'
)

doc.add_heading('09:15. A VP question about a specific initiative', level=2)

add_para(
    'Lisa Torres replies to the weekly review email: "What is the backup plan for INIT-002 if the replacement carriers '
    'also decline?" Dana switches to her Claude Code terminal.'
)
add_code_block('/initiative-status INIT-002')

add_para(
    'Claude Code shows the full status: at risk, $297,115 realized, -$168,269 variance, two carriers declined. '
    'Dana sees the note from last week\'s session. She types a follow-up.'
)
add_code_block(
    'What would happen to the INIT-002 savings target if we reduced the carrier count from 4 to 3? '
    'Read data/savings-log.csv for the current run rate.'
)

add_para(
    'Claude Code calculates: at 3 carriers, the estimated annual savings drops from $2,200,000 to $1,870,000, '
    'a reduction of $330,000. Dana has the number she needs to answer Lisa. Total time: 4 minutes.'
)

add_bold_then_normal('What to learn from this. ',
    'State files and slash commands work together. The /initiative-status command gave Dana the baseline. '
    'The follow-up question worked because Claude Code already had the context from CLAUDE.md and the tracker. '
    'No re-explanation was needed.'
)

doc.add_heading('10:30. Recording a new decision', level=2)

add_para(
    'After a call with Marcus Rivera, Dana and Marcus agree to request a two-week extension on the INIT-002 RFP '
    'evaluation deadline, from 2026-05-01 to 2026-05-15. Lisa Torres approves the extension over email. '
    'Dana records the decision.'
)
add_code_block(
    'Append a new entry to state/decisions-log.md. Do not modify any existing content.\n\n'
    'Date: 2026-04-28\n'
    'Initiative: INIT-002 (Logistics Network Optimization)\n'
    'Decision: Extend RFP evaluation deadline from 2026-05-01 to 2026-05-15.\n'
    'Context: Two replacement carriers (Estes Express and Old Dominion) need two additional weeks to prepare bids. '
    'Extending does not affect the Q3 execution window.\n'
    'Approved by: Lisa Torres (VP of Procurement)\n'
    'Recorded by: Dana, Savings Program Manager'
)

add_para(
    'Claude Code appends the entry. Dana also updates the tracker.'
)
add_code_block(
    'Update the INIT-002 section in state/initiative-tracker.md. Change the next milestone date to 2026-05-15. '
    'Add this note: "RFP evaluation extended to 2026-05-15 per VP approval on 2026-04-28."'
)

add_para('Total time: 3 minutes.')

add_bold_then_normal('What to learn from this. ',
    'The decisions log and the initiative tracker serve different purposes. '
    'The log records why something changed (audit trail). The tracker records what the current state is (snapshot). '
    'You update both. The log is append-only. The tracker is edited in place.'
)

doc.add_heading('13:00. Onboarding Priya to the project', level=2)

add_para(
    'After lunch, Priya Patel asks Dana to set her up with the same Claude Code project. '
    'Priya manages INIT-003 (IT Services Rationalization) and INIT-008 (Temp Staffing Consolidation). '
    'Dana walks Priya through the setup.'
)
add_code_block(
    'git clone <repo-url> savings-program-2026\n'
    'cd savings-program-2026\n'
    'claude'
)

add_para(
    'Priya starts Claude Code. It reads CLAUDE.md and sees all eight initiatives, the stage definitions, '
    'the stakeholders, and the output rules. She types:'
)
add_code_block('/initiative-status INIT-003')

add_para(
    'Claude Code shows INIT-003: IT Services Rationalization, owner Priya Patel, stage Execution, on track, '
    '$1,050,000 realized (55.3% of target), next milestone "License audit review" due 2026-06-01. '
    'Priya has full context in 5 minutes. No 30-minute walkthrough needed.'
)

add_bold_then_normal('What to learn from this. ',
    'The project pattern makes onboarding fast because the context is in files, not in one person\'s head. '
    'CLAUDE.md, the state files, and the slash commands travel with the repo. '
    'A new teammate clones, runs claude, and starts working. '
    'The 25 to 40 minutes you used to spend walking a colleague through the program setup becomes 5 minutes.'
)

doc.add_heading('14:30. Preparing for the monthly CFO update', level=2)

add_para(
    'Dana starts preparing the monthly update for CFO Robert Hayes. The update is due 2026-04-30. '
    'She needs realized savings by initiative, the overall program variance, and a list of decisions made this month.'
)
add_code_block(
    'Read data/savings-log.csv. Calculate realized savings by initiative for 2026-04-01 through 2026-04-28. '
    'Compare against the prorated monthly target for each initiative. '
    'Read state/decisions-log.md and list all entries from April 2026. '
    'Save a draft to outputs/monthly-update-2026-04-draft.md.'
)

add_para(
    'Claude Code produces a two-page draft. The summary line reads: "April 2026: $1,180,000 realized against '
    '$1,241,667 prorated target. Variance: -$61,667 (5.0% below plan). Primary driver: INIT-002 logistics shortfall." '
    'Dana reviews the draft, adds commentary about the carrier replacement plan, and saves the final version. Total time: 12 minutes.'
)

add_bold_then_normal('What to learn from this. ',
    'A Claude Code project is not limited to pre-built slash commands. You can type ad hoc prompts and they work well '
    'because CLAUDE.md gives Claude Code the context it needs. '
    'The monthly update used a custom prompt, not a slash command, but it still benefited from the project structure '
    'because Claude Code already knew the initiatives, the data file locations, and the output formatting rules.'
)

doc.add_heading('16:00. End-of-day state update', level=2)

add_para(
    'Before closing Claude Code for the day, Dana updates the initiative tracker with everything that changed.'
)
add_code_block(
    'Update state/initiative-tracker.md with these changes:\n'
    '- INIT-002: Next milestone date changed to 2026-05-15. Add note about VP-approved extension.\n'
    '- Update the "Last updated" timestamp to 2026-04-28.\n'
    'Do not change any other initiative sections.'
)

add_para(
    'Claude Code updates the tracker. Dana commits and pushes the changes so Priya and Marcus can see the updated state.'
)
add_code_block(
    'git add state/initiative-tracker.md state/decisions-log.md\n'
    'git commit -m "INIT-002: Record RFP extension decision, update milestone date"\n'
    'git push'
)

add_para('Dana closes the session. Total time for the end-of-day update: 3 minutes.')

add_bold_then_normal('What to learn from this. ',
    'The end-of-day state update takes 3 minutes but saves 20 to 30 minutes tomorrow. '
    'Writing the current state to files before you close the session is the single most important habit in the project pattern. '
    'If you skip it, the next session starts from stale data. If you do it, the next session is instant.'
)

doc.add_heading('16:45. Quick risk check before tomorrow\'s supplier meeting', level=2)

add_para(
    'Dana has a meeting with Great Lakes Steel tomorrow morning about the INIT-001 contract. '
    'She needs the latest performance numbers. She is still in Claude Code from the state update.'
)
add_code_block('/initiative-status INIT-001')

add_para(
    'Claude Code shows INIT-001: Direct Materials Consolidation, owner Sarah Chen, stage Execution, on track, '
    '$1,420,000 realized (50.7% of $2,800,000 target). Next milestone: quarterly savings validation due 2026-05-15. '
    'Note: "Steel consolidation with Great Lakes Steel generating consistent monthly savings of approximately $180,000. '
    'On pace to exceed annual target by 5%." Dana copies two numbers ($1,420,000 realized and $180,000 per month) '
    'into her meeting prep notes. Total time: 90 seconds.'
)

add_bold_then_normal('What to learn from this. ',
    'Quick lookups are the most common use of the project pattern. You do not need a complex prompt. '
    'You type a slash command, read two numbers, and move on. The slash command works because the tracker file '
    'already has the current state. The work you did during the day (updating the tracker, recording decisions) '
    'makes every subsequent lookup instant.'
)

doc.add_heading("Dana's day: the numbers", level=2)

add_table(
    ['Task', 'Time spent', 'Time without project'],
    [
        ['Weekly VP review', '7 min', '40 min'],
        ['Initiative deep-dive for VP question', '4 min', '15 min'],
        ['Record decision and update tracker', '3 min', '10 min'],
        ['Onboard Priya', '5 min', '35 min'],
        ['Monthly CFO draft', '12 min', '45 min'],
        ['End-of-day state update', '3 min', 'N/A (no equivalent)'],
        ['Quick supplier meeting prep', '2 min', '10 min'],
        ['Total', '36 min', '155 min'],
    ]
)

add_para('Dana spent 36 minutes on administrative program management tasks. Without the project pattern, those same tasks would take about 155 minutes. That is 119 minutes saved in a single day.')

# ======================================================================
# 8. THE 20-MINUTE SPRINT
# ======================================================================
doc.add_heading('8. The 20-minute sprint: your first initiative status check', level=1)

add_para('This section gets you from zero to your first usable output in 20 minutes. Follow the four blocks in order. Do not skip steps.')

doc.add_heading('Minutes 0 to 5: open the practice folder and create the project', level=2)

add_para(
    '1. Open a terminal.\n'
    '2. Navigate to the course folder: cd "Course_08_The_Project_Architect/practice"\n'
    '3. Confirm you see CLAUDE.md and data/ by running: ls\n'
    '4. Create the .claude directory: mkdir .claude\n'
    '5. Start Claude Code: claude'
)

add_para('You should see the Claude Code prompt. Claude Code reads CLAUDE.md and knows you are the Savings Program Manager at Pinnacle Procurement.')

doc.add_heading('Minutes 5 to 10: create settings.json and the state directory', level=2)

add_para('Type this prompt in Claude Code (in the terminal):')
add_code_block(
    'Create a file at .claude/settings.json with this content:\n'
    '{\n'
    '  "permissions": {\n'
    '    "allow": [\n'
    '      "Read(data/*)",\n'
    '      "Read(state/*)",\n'
    '      "Write(state/*)",\n'
    '      "Write(outputs/*)"\n'
    '    ]\n'
    '  }\n'
    '}\n\n'
    'Then create a directory called state/.'
)

add_para('You should see Claude Code create both. Type /quit to exit, then type claude to restart so Claude Code picks up the new settings.')

doc.add_heading('Minutes 10 to 15: build the initiative tracker', level=2)

add_para('Type this prompt in Claude Code (in the terminal):')
add_code_block(
    'Read data/initiatives.csv, data/savings-log.csv, and data/milestone-tracker.csv.\n'
    'Create state/initiative-tracker.md with one section per initiative.\n'
    'Each section: ID, name, owner, stage, status, target, realized savings to date, '
    'variance, next milestone, and a blank notes field.\n'
    'Set "Last updated" to 2026-04-25.'
)

add_para(
    'You should see Claude Code read three CSV files and produce an eight-section tracker file. '
    'Each initiative shows its current savings position and next milestone date.'
)

doc.add_heading('Minutes 15 to 20: create the initiative-status command and run it', level=2)

add_para('Type this prompt in Claude Code (in the terminal):')
add_code_block(
    'Create .claude/commands/initiative-status.md with instructions to:\n'
    '1. Read state/initiative-tracker.md for the current status of initiative "$ARGUMENTS".\n'
    '2. Read data/savings-log.csv, filter for the matching initiative, calculate realized savings and variance.\n'
    '3. Read data/milestone-tracker.csv, list completed and pending milestones.\n'
    '4. Output a concise status update with name, owner, stage, status, savings summary, and milestones.'
)

add_para('Exit with /quit, restart with claude, then type:')
add_code_block('/initiative-status INIT-001')

add_para(
    'You should see a status update for Direct Materials Consolidation: Sarah Chen, Execution, on track, '
    'approximately $746,500 realized savings. You have a working project in 20 minutes.'
)

# ======================================================================
# 9. FIRST WEEK PLANNER
# ======================================================================
doc.add_heading('9. Your first week with a Claude Code project', level=1)

doc.add_heading('Day 1 (Monday): install and first contact', level=2)

add_para('Goals for today:')
add_para(
    '1. Complete the 20-minute sprint from section 8.\n'
    '2. Have a working .claude/settings.json and a CLAUDE.md that Claude Code reads automatically.\n'
    '3. Have state/initiative-tracker.md with all eight initiatives.\n'
    '4. Successfully run /initiative-status for one initiative.'
)

add_para('By end of day, you should be able to start Claude Code (in the terminal) and ask "which initiatives are at risk?" without typing any context.')

doc.add_heading('Day 2 (Tuesday): the decisions log and your first weekly review', level=2)

add_para('Goals for today:')
add_para(
    '1. Complete Lesson 4 (create state/decisions-log.md and record three decisions).\n'
    '2. Create the /weekly-review slash command (Lesson 5).\n'
    '3. Run /weekly-review and save your first weekly review to outputs/weekly-reviews/.\n'
    '4. Close Claude Code, reopen it, and confirm decisions persist.'
)

add_para('By end of day, you should have two working slash commands and a decisions log with three entries.')

doc.add_heading('Day 3 (Wednesday): apply the pattern to your real program', level=2)

add_para('Goals for today:')
add_para(
    '1. Create a new folder for your real savings program or category portfolio.\n'
    '2. Write a CLAUDE.md with your real initiatives, real owners, and real targets.\n'
    '3. Create .claude/settings.json with permissions for your real data files.\n'
    '4. Build state/initiative-tracker.md from your real data.\n'
    '5. Test with /initiative-status on a real initiative.'
)

add_para('By end of day, you should have a working Claude Code project for your actual work, not just the practice data.')

doc.add_heading('Day 4 (Thursday): slash commands and automation', level=2)

add_para('Goals for today:')
add_para(
    '1. Create /weekly-review for your real program.\n'
    '2. Create a custom slash command for a task you repeat often (monthly update, risk summary, or stakeholder brief).\n'
    '3. Record your first real decision in state/decisions-log.md.\n'
    '4. Practice the end-of-day state update: update the tracker and commit.'
)

add_para('By end of day, you should have at least two slash commands tailored to your real workflow.')

doc.add_heading('Day 5 (Friday): share and refine', level=2)

add_para('Goals for today:')
add_para(
    '1. Initialize a git repository in your real project folder (Lesson 6).\n'
    '2. Share the repo with one teammate.\n'
    '3. Have the teammate clone, run claude, and test /initiative-status.\n'
    '4. Review your CLAUDE.md: is it between 60 and 120 lines? Does it have everything a session needs?\n'
    '5. Plan next week: which slash commands do you want to add?'
)

add_para('By end of day, at least two people can work from the same project. Your state files and commands are shared.')

# ======================================================================
# 10. THE PATTERN
# ======================================================================
doc.add_heading('10. The pattern: files beat memory', level=1)

add_para(
    'The project pattern from this course applies to any multi-initiative, multi-session Claude Code workflow. '
    'The structure stays the same. The content changes.'
)

add_para(
    'Three rules summarize the pattern:'
)

add_bold_then_normal(
    '1. Store context in CLAUDE.md, not in conversation. ',
    'Your role, your portfolio, your data locations, and your formatting rules. '
    'Put in what every session needs. Keep it under 120 lines. '
    'Claude Code (in the terminal) reads it automatically on startup.'
)

add_bold_then_normal(
    '2. Store state in files, not in memory. ',
    'Current status goes in initiative-tracker.md (updated in place). '
    'Decision history goes in decisions-log.md (append only). '
    'Read state at session start. Write state before session end.'
)

add_bold_then_normal(
    '3. Store workflows in slash commands, not in prompts you re-type. ',
    'If you type the same prompt twice, turn it into a slash command file in .claude/commands/. '
    'The command persists across sessions and travels with the repo.'
)

add_para(
    'This pattern is not limited to savings programs. It works for contract portfolios, supplier risk programs, '
    'category management dashboards, and any procurement workflow that spans more than one session. '
    'The folder structure, the state file conventions, and the slash command format stay constant. '
    'Only the CLAUDE.md content, the data files, and the command instructions change.'
)

add_para(
    'Apply this pattern to the next multi-week program you manage. Start with CLAUDE.md. Add state/ when you need '
    'cross-session memory. Add slash commands when you catch yourself typing the same prompt twice. '
    'The project grows with your workflow, not ahead of it.'
)

doc.add_heading('The pattern applied to other procurement workflows', level=2)

add_para(
    'The project structure adapts to any multi-session procurement workflow. Here are three concrete examples.'
)

add_bold_then_normal(
    'Contract portfolio management. ',
    'CLAUDE.md lists 30 contracts with vendor name, contract value, effective date, expiry date, and renewal status. '
    'state/contract-tracker.md records current renewal stage for each contract. state/decisions-log.md records '
    'renewal decisions (renew, renegotiate, or terminate) with dates and approvers. '
    'The /contract-status slash command checks a single contract. '
    'The /renewal-dashboard command produces a 90-day renewal horizon report.'
)

add_bold_then_normal(
    'Supplier risk monitoring. ',
    'CLAUDE.md lists 50 suppliers with risk tier, annual spend, and primary contact. '
    'state/risk-tracker.md records current risk signals (financial health, delivery performance, compliance status) per supplier. '
    'state/incidents-log.md records risk events (quality failures, delivery delays, financial downgrades) as an append-only log. '
    'The /risk-status slash command checks one supplier. '
    'The /risk-dashboard command lists all suppliers above the risk threshold.'
)

add_bold_then_normal(
    'Category strategy execution. ',
    'CLAUDE.md describes one category (for example, packaging) with current suppliers, annual spend of $8.2M, '
    'and the three-year strategy. state/strategy-tracker.md records progress against each strategic initiative. '
    'state/market-notes.md records market intelligence gathered across sessions. '
    'The /strategy-status command shows progress against the annual plan. '
    'The /market-brief command compiles the latest market intelligence into a one-page summary.'
)

add_para(
    'In every case, the structure is the same: CLAUDE.md for what every session needs, state/ for what changes '
    'between sessions, and .claude/commands/ for workflows you run more than once. '
    'The names of the files change. The pattern does not.'
)

# ======================================================================
# 11. TROUBLESHOOTING
# ======================================================================
doc.add_heading('11. Quick reference and troubleshooting', level=1)

doc.add_heading('Things to remember', level=2)

add_para(
    '1. Always run Claude Code (in the terminal) from inside the project folder that contains CLAUDE.md and .claude/.\n'
    '2. Always update state/initiative-tracker.md before ending a session.\n'
    '3. Always use "append" when adding to decisions-log.md. Never overwrite.\n'
    '4. Exit and restart Claude Code after creating new slash command files so it picks them up.\n'
    '5. Keep CLAUDE.md between 60 and 120 lines. Move detail to separate files if it grows past 150.'
)

doc.add_heading('Common problems and the matching fix', level=2)

add_bold_then_normal(
    'Problem: Claude Code does not read CLAUDE.md on startup. ',
    'Fix: check that you started Claude Code inside the folder that contains CLAUDE.md. Run pwd (Mac/Linux) or '
    'cd (Windows) to see your current directory. If you are in a parent or child folder, navigate to the correct one.'
)

add_bold_then_normal(
    'Problem: settings.json is ignored. ',
    'Fix: the .claude/ directory must be at the root of your project folder, not inside a subfolder like data/.claude/. '
    'Check the path: ls .claude/settings.json. If the file is in the wrong location, move it.'
)

add_bold_then_normal(
    'Problem: the slash command /initiative-status is not recognized. ',
    'Fix: the command file must be at .claude/commands/initiative-status.md. Check with ls .claude/commands/. '
    'If you just created the file, exit Claude Code with /quit and restart with claude. '
    'Claude Code loads command files at startup, not mid-session.'
)

add_bold_then_normal(
    'Problem: Claude overwrote the entire decisions log instead of appending. Previous entries are gone. ',
    'Fix: always say "append" and "do not modify any existing content" in your prompt. '
    'If entries were lost, check your file version history (OneDrive or git log). '
    'Restore the previous version and re-append the new entry. '
    'Add a reminder to CLAUDE.md: "state/decisions-log.md is append-only. Never delete or edit existing entries."'
)

add_bold_then_normal(
    'Problem: the initiative tracker shows stale data from two weeks ago. ',
    'Fix: you forgot to update the tracker at the end of recent sessions. '
    'Re-derive it from the source CSVs: "Read all four data files and rebuild state/initiative-tracker.md from scratch. '
    'Preserve any notes from the existing file." '
    'Then add a habit: before typing /quit, always update the tracker.'
)

add_bold_then_normal(
    'Problem: $ARGUMENTS in the slash command file does not expand. Claude treats it as literal text. ',
    'Fix: the placeholder must be written as $ARGUMENTS (all caps, with the dollar sign). '
    'Check .claude/commands/initiative-status.md for typos. '
    'A common mistake is writing $arguments (lowercase) or ${ARGUMENTS} (with braces).'
)

# ======================================================================
# 12. DONE CHECKLIST
# ======================================================================
doc.add_heading('12. You are done with Course 8 when', level=1)

add_para(
    '1. Your project has a .claude/ directory with settings.json and two slash commands (initiative-status.md and weekly-review.md).\n'
    '2. Your CLAUDE.md lists all eight initiatives with ID, name, category, owner, target, stage, and status. It is between 60 and 120 lines.\n'
    '3. You have state/initiative-tracker.md with current status, realized savings, variance, next milestone, and notes for each initiative.\n'
    '4. You have state/decisions-log.md with at least three dated, attributed decision entries.\n'
    '5. You can type /initiative-status INIT-001 in Claude Code (in the terminal) and get a scoped status update without re-explaining the program.\n'
    '6. You can type /weekly-review and get a full program review saved to outputs/weekly-reviews/.\n'
    '7. You can close Claude Code, reopen it, and confirm the state from the previous session is preserved.\n'
    '8. You can explain the difference between project settings (.claude/settings.json) and global settings (~/.claude/settings.json).\n'
    '9. A teammate can clone your repo and start working with the same context, commands, and state files.\n'
    '10. You understand the pattern: CLAUDE.md for standing context, state files for current status and decision history, slash commands for repeatable workflows.'
)

# ── Save ─────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(str(OUTPUT)), exist_ok=True)
doc.save(str(OUTPUT))

# Word count estimate
total_words = 0
for p in doc.paragraphs:
    total_words += len(p.text.split())
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            total_words += len(cell.text.split())
print(f"Saved to: {OUTPUT}")
print(f"Estimated word count: {total_words}")
print(f"Paragraphs: {len(doc.paragraphs)}")
print(f"Tables: {len(doc.tables)}")
