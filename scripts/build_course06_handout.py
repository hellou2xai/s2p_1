"""
Build Course 06 The Guardian Handout as .docx
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os
from pathlib import Path

doc = Document()

# ── Global style defaults ──
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

# Heading styles
for level, size, color in [(1, 18, '1B3A5C'), (2, 14, '1B3A5C'), (3, 12, '2D5F8A')]:
    h = doc.styles[f'Heading {level}']
    h.font.name = 'Calibri'
    h.font.size = Pt(size)
    h.font.bold = True
    h.font.color.rgb = RGBColor(*bytes.fromhex(color))
    h.paragraph_format.space_before = Pt(12 if level > 1 else 18)
    h.paragraph_format.space_after = Pt(6)


# ── Helper functions ──
def add_para(text, bold=False, italic=False, space_after=6):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def add_code_block(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    pf = p.paragraph_format
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    pf.left_indent = Inches(0.3)
    # Light gray shading
    shading = p.paragraph_format.element.get_or_add_pPr()
    shd = shading.makeelement(qn('w:shd'), {
        qn('w:val'): 'clear',
        qn('w:color'): 'auto',
        qn('w:fill'): 'F2F2F2',
    })
    shading.append(shd)
    return p


def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.bold = True
        run_b.font.name = 'Calibri'
        run_b.font.size = Pt(11)
        run_n = p.add_run(text)
        run_n.font.name = 'Calibri'
        run_n.font.size = Pt(11)
    else:
        # Clear default run and add our text
        for r in p.runs:
            r.text = ''
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    return p


def add_numbered(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Number')
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.bold = True
        run_b.font.name = 'Calibri'
        run_b.font.size = Pt(11)
        run_n = p.add_run(text)
        run_n.font.name = 'Calibri'
        run_n.font.size = Pt(11)
    else:
        for r in p.runs:
            r.text = ''
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    return p


def add_table(headers, rows):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = 'Light Grid Accent 1'
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, h in enumerate(headers):
        cell = tbl.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.name = 'Calibri'
                r.font.size = Pt(10)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = tbl.rows[ri + 1].cells[ci]
            cell.text = val
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(10)
    doc.add_paragraph()  # spacer
    return tbl


# ===================================================================
# HEADER
# ===================================================================
h_para = doc.add_paragraph()
h_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = h_para.add_run('U2xAI  |  PROCUREAI ACADEMY')
run.bold = True
run.font.name = 'Calibri'
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = sub.add_run(
    'Series 2: Claude Code Foundation for Source-to-Pay Professionals  |  Course 6'
)
run.font.name = 'Calibri'
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run(
    'The Guardian: Hooks for Quality Gates, Audit Trails, and Risk Alerts'
)
run.bold = True
run.font.name = 'Calibri'
run.font.size = Pt(20)
run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
title.paragraph_format.space_after = Pt(4)

date_para = doc.add_paragraph()
date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = date_para.add_run('April 2026  |  Estimated study time: 4 hours')
run.font.name = 'Calibri'
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x77, 0x77, 0x77)
date_para.paragraph_format.space_after = Pt(18)

# ===================================================================
# SECTION 1: HOW TO USE THIS HANDOUT
# ===================================================================
doc.add_heading('1. How to Use This Handout', level=1)

add_para(
    'This handout is your reference companion for Course 6: The Guardian. '
    'It covers every concept, every hook script, and every terminal interaction '
    'from the six lessons. Keep it open while you work through the course, and '
    'use it afterward as a quick-reference when you build hooks for your own projects.'
)

add_para(
    'The handout is organized to follow your natural workflow, not the lesson sequence. '
    'It starts with the problem hooks solve, moves through the mechanics of how hooks work, '
    'gives you three complete worked examples you can adapt, walks through a full day of '
    'hook-powered contract operations, and ends with a sprint plan to get your first hook '
    'running in 20 minutes.'
)

add_para('How to read the examples in this handout:', bold=True)

add_para(
    'Every worked example has four parts. First, the prompt you type in the Claude Code terminal. '
    'Second, the folder layout that should be in place before you type the prompt. '
    'Third, what you should see on screen when it succeeds. Fourth, a "What Claude did, behind '
    'the scenes" walkthrough that explains, step by step, what Claude Code (in the terminal) '
    'actually did. That fourth part is what teaches you to apply hooks to new tasks on your own.'
)

add_para(
    'All examples use Claude Code (in the terminal). Claude AI Web and Claude Desktop with '
    'Cowork do not support hooks. Hooks are a Claude Code feature only.'
)

add_para(
    'All data in this handout is fictional. Sentinel Contract Services, Great Lakes Steel, '
    'Heartland Polymers, MedLine Procurement Group, and all other company names are made up. '
    'No real client data appears anywhere.'
)

# ===================================================================
# SECTION 2: WHAT THIS COURSE TEACHES
# ===================================================================
doc.add_heading('2. What This Course Teaches', level=1)

add_para(
    'It is Thursday afternoon. Your team lead reviews the 12 contract review reports your '
    'automated pipeline produced this morning. In five minutes she finds three problems. '
    'Contract CTR-2025-003 has no risk assessment section at all. Contract CTR-2025-006 lists '
    'a risk level of "Extreme," which is not in your taxonomy (your taxonomy uses Low, Medium, '
    'High, and Critical). Contract CTR-2025-011 is flagged Critical risk, but the report has no '
    'recommendation section. A Critical-risk contract with no recommended action is worse than '
    'no report at all.'
)

add_para(
    'She sends you a Teams message: "These reports cannot go to the legal team in this state. '
    'We need a quality gate. No report should save to outputs/ unless it passes validation. And '
    'I want a log of everything Claude Code does so we can audit it."'
)

add_para('The fix: hooks.', bold=True)

add_para(
    'Claude Code (in the terminal) supports hooks: small Python scripts that run automatically '
    'before or after every tool call. You register a hook once in your project settings. From that '
    'point on, Claude Code calls your script every time the matching tool fires. No manual checking. '
    'No missed reports. The quality gate runs itself.'
)

add_para(
    'By the end of this course, you will have three hooks running in a single project. A validation '
    'hook that blocks bad reports before they save. An audit hook that logs every action Claude Code '
    'takes. A risk alert hook that flags High and Critical contracts the moment they pass validation.'
)

doc.add_heading('Worked example: your first hook in action', level=2)

add_para('The prompt to type (in the Claude Code terminal):', bold=True)
add_code_block(
    'Read data/contracts/review-CTR-2025-006.md and save it to\n'
    'outputs/review-CTR-2025-006.md exactly as written.'
)

add_para('The folder layout:', bold=True)
add_code_block(
    'Course_06_The_Guardian/practice/\n'
    '+-- .claude/settings.json        (hooks registered here)\n'
    '+-- data/contracts/              (12 contract review files)\n'
    '+-- hooks/validate-report-hook.py\n'
    '+-- outputs/                     (validated reports land here)\n'
    '+-- audit/                       (audit log)\n'
    '+-- alerts/                      (risk alert files)'
)

add_para('What you should see:', bold=True)
add_para(
    'Claude Code (in the terminal) reports that the write was blocked. The error message reads: '
    '"Invalid risk level: \'Extreme\'. Must be one of: Critical, High, Low, Medium."'
)

add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) read the contents of '
    'data/contracts/review-CTR-2025-006.md.'
)
add_numbered(
    'Claude Code attempted to write the content to '
    'outputs/review-CTR-2025-006.md.'
)
add_numbered(
    'Before the write executed, Claude Code ran '
    'hooks/validate-report-hook.py and passed the file '
    'path and content as JSON on stdin.'
)
add_numbered(
    'The hook found the risk level "Extreme" and checked it against the allowed set: Low, Medium, '
    'High, and Critical. It did not match.'
)
add_numbered(
    'The hook returned a JSON response with "decision": "block" and the specific error reason.'
)
add_numbered(
    'Claude Code received the block response, did not write the file, and showed you the error message.'
)

# ===================================================================
# SECTION 3: WHAT IS IN THE COURSE FOLDER
# ===================================================================
doc.add_heading('3. What Is in the Course Folder', level=1)

add_para(
    'The course folder is self-contained. Everything you need is inside. No external downloads, '
    'no shared drives, no separate data stores.'
)

add_code_block(
    'Course_06_The_Guardian/\n'
    '+-- README.md\n'
    '+-- COURSE_OVERVIEW.md\n'
    '+-- lessons/\n'
    '|   +-- Lesson_01_The_Four_Hook_Types.md\n'
    '|   +-- Lesson_02_Writing_The_Validation_Hook.md\n'
    '|   +-- Lesson_03_Writing_The_Audit_Hook.md\n'
    '|   +-- Lesson_04_The_Risk_Alert_Hook.md\n'
    '|   +-- Lesson_05_Hook_Error_Handling.md\n'
    '|   +-- Lesson_06_Integration_Test.md\n'
    '+-- practice/\n'
    '|   +-- CLAUDE.md\n'
    '|   +-- data/\n'
    '|   |   +-- contract-register.csv    (30 contracts)\n'
    '|   |   +-- clause-taxonomy.csv      (12 clause types)\n'
    '|   |   +-- contracts/               (12 review files)\n'
    '|   +-- hooks/       (your hook scripts go here)\n'
    '|   +-- outputs/     (validated reports land here)\n'
    '|   +-- audit/       (audit log JSONL file)\n'
    '|   +-- alerts/      (risk alert text files)\n'
    '+-- solutions/\n'
    '|   +-- validate_report_hook_solution.py\n'
    '|   +-- audit_log_hook_solution.py\n'
    '|   +-- risk_alert_hook_solution.py\n'
    '|   +-- settings_json_solution.md\n'
    '|   +-- flaw-manifest.md\n'
    '+-- scripts/          (data regeneration script)'
)

# File-by-file with "Why this matters"
doc.add_heading('CLAUDE.md (in practice/)', level=3)
add_para(
    'The project-level instruction file. It tells Claude Code (in the terminal) your role '
    '(Contract Operations Lead at Sentinel Contract Services), which files are read-only '
    '(everything in data/), the report quality standards (six required sections, four valid '
    'risk levels), and the output rules (USD with commas, YYYY-MM-DD dates).'
)
add_para(
    'Why this matters. Without this file, Claude Code produces generic output with no awareness '
    'of your report structure, your risk taxonomy, or your folder rules. With it, every prompt '
    'response uses Sentinel\'s standards, Sentinel\'s taxonomy, and Sentinel\'s folder layout. '
    'The CLAUDE.md is the reason hooks can validate against consistent rules.',
    italic=True
)

doc.add_heading('data/contract-register.csv', level=3)
add_para(
    'A register of 30 contracts with columns: contract_id, supplier_id, supplier_name, category, '
    'tier, contract_type, start_date, end_date, annual_value_usd, status, auto_renew, and '
    'risk_level. This is the master list your hooks reference for valid contract IDs and '
    'expected risk levels.'
)
add_para(
    'Why this matters. The register gives you a ground truth to validate against. If a review '
    'report claims CTR-2025-006 is "Extreme" risk but the register says "High," you know the '
    'report is wrong. Without a register, the hook has nothing to compare against.',
    italic=True
)

doc.add_heading('data/clause-taxonomy.csv', level=3)
add_para(
    'Twelve standard clause types (termination, liability, indemnification, and so on) with '
    'display names, which contract types require them, and risk weights from 1 to 5.'
)
add_para(
    'Why this matters. The taxonomy defines which clauses the validation hook looks for in the '
    '"Key Clauses" section. A report that lists no clauses, or lists clauses not in the taxonomy, '
    'fails validation. Without the taxonomy, "Key Clauses" would be unverifiable.',
    italic=True
)

doc.add_heading('data/contracts/ (12 review files)', level=3)
add_para(
    'Twelve markdown files, each a contract review report. Six are valid. Six have planted flaws: '
    'missing risk assessment, invalid risk level ("Extreme"), missing supplier name, missing key '
    'clauses section, Critical risk with no recommendation, and empty clause references.'
)
add_para(
    'Why this matters. The flawed files are your test suite. Each flaw matches a real-world '
    'problem your team lead identified. If your validation hook catches all six, it is production-ready. '
    'If it misses even one, you know exactly which regex pattern to fix.',
    italic=True
)

doc.add_heading('hooks/ (your scripts)', level=3)
add_para(
    'The folder where you save your three hook scripts: validate-report-hook.py, audit-log-hook.py, '
    'and risk-alert-hook.py. Claude Code (in the terminal) runs these scripts automatically when '
    'the matching tool fires.'
)
add_para(
    'Why this matters. Keeping hooks in a dedicated folder separates automation logic from data '
    'and outputs. If you need to share your hooks with another project, you copy one folder. '
    'If you need to disable all hooks, you edit one settings file.',
    italic=True
)

doc.add_heading('outputs/, audit/, alerts/', level=3)
add_para(
    'Three output folders. outputs/ holds validated contract review reports. audit/ holds the '
    'append-only JSONL audit log. alerts/ holds plain-text risk alert files for High and Critical '
    'contracts.'
)
add_para(
    'Why this matters. Separating outputs by purpose means the legal team checks outputs/, '
    'the compliance team checks audit/, and the risk team checks alerts/. Nobody opens the '
    'wrong folder. Nobody misses a file.',
    italic=True
)

doc.add_heading('solutions/', level=3)
add_para(
    'Reference answers for all three hook scripts and the settings.json configuration. Also '
    'includes a flaw manifest listing which contract reviews have which planted flaws. Look at '
    'solutions only after attempting the lessons yourself.'
)
add_para(
    'Why this matters. If your hook does not catch a flaw, you can compare your script line by '
    'line against the solution. The flaw manifest tells you exactly what each flawed file is '
    'missing, so you can write targeted tests.',
    italic=True
)

# ===================================================================
# SECTION 4: TIME SAVINGS REFERENCE TABLE
# ===================================================================
doc.add_heading('4. Time Savings Reference Table', level=1)

add_para(
    'These figures come from the practice scenario: a batch of 12 contract reviews at Sentinel '
    'Contract Services. "Without hooks" means a human reviews each report by hand. "With hooks" '
    'means the three hooks from this course are registered in Claude Code (in the terminal).'
)

add_table(
    ['Task', 'Without hooks', 'With hooks', 'Time saved'],
    [
        [
            'Validate 12 contract review reports for required sections, '
            'valid risk levels, and named suppliers',
            '120 to 180 min (10 to 15 min per report, manual checklist)',
            '8 seconds (hooks run automatically on each write attempt)',
            '119 to 179 min per batch',
        ],
        [
            'Build an audit trail of every Claude Code action during a '
            'batch run (reads, writes, searches)',
            '45 to 60 min (reconstruct from terminal history after the fact)',
            '0 min (audit hook logs every action in real time)',
            '45 to 60 min per batch',
        ],
        [
            'Identify which contracts in a batch are High or Critical risk '
            'and flag them for legal review',
            '30 to 45 min (open each report, find the risk level, copy to a tracker)',
            '0 min (alert hook writes a file to alerts/ automatically)',
            '30 to 45 min per batch',
        ],
        [
            'Re-check a rejected report after fixing and confirm the fix '
            'before re-saving',
            '15 to 20 min (re-read the report, re-run the checklist)',
            '3 seconds (fix the issue, re-save, hook validates automatically)',
            '14 to 19 min per rejected report',
        ],
        [
            'Produce a post-batch summary for the VP of Procurement showing '
            'what was processed, blocked, and alerted',
            '30 to 40 min (compile manually from terminal output)',
            '5 min (read audit/audit.jsonl, ask Claude Code to summarize)',
            '25 to 35 min per summary',
        ],
    ],
)

# ===================================================================
# SECTION 5: WHAT A HOOK ACTUALLY IS
# ===================================================================
doc.add_heading('5. What a Hook Actually Is', level=1)

add_para(
    'A hook is a Python script that Claude Code (in the terminal) runs automatically before or '
    'after a tool call. You do not call the script yourself. You register it once in '
    '.claude/settings.json, and Claude Code calls it every time the matching tool fires.'
)

doc.add_heading('The mental model: an interceptor on the pipeline', level=2)
add_para(
    'Think of Claude Code as a pipeline. You type a prompt. Claude decides which tool to use '
    '(Read, Write, Edit, Glob, Grep, or Bash). Before the tool runs, Claude Code checks: "Is there '
    'a PreToolUse hook registered for this tool?" If yes, it runs your script and waits for the '
    'result. If the script says "approve," the tool runs. If it says "block," the tool stops and '
    'Claude sees the error. After the tool runs (if it was approved), Claude Code checks again: '
    '"Is there a PostToolUse hook?" If yes, it runs your script with the result details.'
)

add_para(
    'The script is a plain Python file. It reads JSON from stdin, does its work, and prints JSON '
    'to stdout. No special library is required. No SDK. No API key. Just Python, json, sys, and '
    'whatever standard library modules you need.'
)

doc.add_heading('The four hook types', level=2)

add_table(
    ['Hook type', 'When it fires', 'What it can do', 'Use it for'],
    [
        [
            'PreToolUse',
            'Before a tool call executes',
            'Approve, block, or modify the call',
            'Validation gates. Stop a bad file from saving.',
        ],
        [
            'PostToolUse',
            'After a tool call completes',
            'Read the result, log it, trigger actions',
            'Audit logs, risk alerts, and notifications.',
        ],
        [
            'Stop',
            'When a Claude Code session ends',
            'Run cleanup, write summaries',
            'Session reports and cleanup scripts.',
        ],
        [
            'Notification',
            'When Claude Code emits an event',
            'React to events like errors',
            'Error monitoring and status updates.',
        ],
    ],
)

add_para(
    'This course builds one PreToolUse hook and two PostToolUse hooks. Course 7 covers Stop '
    'and Notification hooks.'
)

doc.add_heading('How a PreToolUse hook intercepts a write', level=2)

add_para('Here is the sequence, step by step:')
add_numbered(
    'You type a prompt that asks Claude Code (in the terminal) to save a file to outputs/.'
)
add_numbered('Claude Code prepares a Write tool call with the file path and content.')
add_numbered(
    'Before executing, Claude Code checks .claude/settings.json for PreToolUse hooks '
    'with a matcher of "Write".'
)
add_numbered(
    'Claude Code runs your hook script (for example, python hooks/validate-report-hook.py) '
    'and passes the tool call details as JSON on stdin.'
)
add_numbered(
    'Your script reads the JSON, runs its checks, and prints a JSON response to stdout: '
    'either {"decision": "approve"} or {"decision": "block", "reason": "..."}.'
)
add_numbered(
    'If approved, the write proceeds. If blocked, Claude Code shows you the error and does not '
    'write the file.'
)

doc.add_heading('How a PostToolUse hook reacts to a completed action', level=2)

add_para('The sequence for a PostToolUse hook is shorter:')
add_numbered(
    'The tool call completes (a file is written, a file is read, or a search finishes).'
)
add_numbered(
    'Claude Code checks .claude/settings.json for PostToolUse hooks matching the tool name.'
)
add_numbered(
    'Claude Code runs your hook script and passes the tool call result as JSON on stdin.'
)
add_numbered(
    'Your script does its work (append a log line, write an alert file) and exits. '
    'A PostToolUse hook does not need to print anything to stdout.'
)

doc.add_heading('The settings.json structure', level=2)

add_para(
    'Hooks are registered in .claude/settings.json inside the project folder. '
    'The structure looks like this:'
)

add_code_block(
    '{\n'
    '  "hooks": {\n'
    '    "PreToolUse": [\n'
    '      {\n'
    '        "matcher": "Write",\n'
    '        "hooks": [\n'
    '          {\n'
    '            "type": "command",\n'
    '            "command": "python hooks/validate-report-hook.py"\n'
    '          }\n'
    '        ]\n'
    '      }\n'
    '    ],\n'
    '    "PostToolUse": [\n'
    '      {\n'
    '        "matcher": "*",\n'
    '        "hooks": [\n'
    '          {\n'
    '            "type": "command",\n'
    '            "command": "python hooks/audit-log-hook.py"\n'
    '          }\n'
    '        ]\n'
    '      },\n'
    '      {\n'
    '        "matcher": "Write",\n'
    '        "hooks": [\n'
    '          {\n'
    '            "type": "command",\n'
    '            "command": "python hooks/risk-alert-hook.py"\n'
    '          }\n'
    '        ]\n'
    '      }\n'
    '    ]\n'
    '  }\n'
    '}'
)

add_para('Key fields:', bold=True)
add_bullet(
    'Which tool triggers the hook. Use "Write" for file writes only. Use "*" for every tool call.',
    bold_prefix='matcher: ',
)
add_bullet(
    'The shell command Claude Code runs. Use relative paths from the project root.',
    bold_prefix='command: ',
)
add_bullet(
    'Always "command" for script-based hooks.',
    bold_prefix='type: ',
)

add_para(
    'Why this matters. The settings.json file is the single source of truth for all hooks in a project. '
    'If you want to disable a hook, remove its entry. If you want to add a new hook, add an entry. '
    'You never need to edit Claude Code itself. You never need to change a prompt. The hooks just run.',
    italic=True,
)

doc.add_heading('Worked example: registering your first hook', level=2)

add_para('The prompt to type (in the Claude Code terminal):', bold=True)
add_code_block(
    'Create the file .claude/settings.json with an empty hooks structure.\n'
    'Include both PreToolUse and PostToolUse as empty arrays.\n'
    'Do not add any hook entries yet.'
)

add_para('The folder layout:', bold=True)
add_code_block(
    'Course_06_The_Guardian/practice/\n'
    '+-- .claude/          (will be created)\n'
    '+-- data/\n'
    '+-- hooks/'
)

add_para('What you should see:', bold=True)
add_para(
    'Claude Code (in the terminal) creates .claude/settings.json with a hooks object containing '
    'two empty arrays: PreToolUse and PostToolUse. The file is valid JSON.'
)

add_para('What Claude did, behind the scenes:', bold=True)
add_numbered('Checked whether .claude/settings.json already existed.')
add_numbered('Created the .claude/ directory because it did not exist.')
add_numbered('Wrote a JSON file with a hooks object containing two empty arrays.')
add_numbered(
    'Saved the file. No hooks are active yet because both arrays are empty.'
)

# ===================================================================
# SECTION 6: WORKED EXAMPLES
# ===================================================================
doc.add_heading('6. Worked Examples', level=1)

add_para(
    'This section gives you three complete, end-to-end worked examples. Each one shows the prompt, '
    'the folder layout, the expected result, and a behind-the-scenes walkthrough. The first example '
    'builds the validation hook (PreToolUse). The second builds the audit hook (PostToolUse). '
    'The third shows the risk alert hook in action.'
)

# --- Example 1: Validation Hook ---
doc.add_heading('Example 1: The validation hook blocks a flawed report', level=2)

add_para(
    'Scenario: Contract CTR-2025-003 is a $2,400,000 raw materials agreement with Great Lakes Steel. '
    'The review report is missing its Risk Assessment section entirely. Your validation hook should '
    'catch this and block the save.'
)

add_para('The prompt to type (in the Claude Code terminal):', bold=True)
add_code_block(
    'Read data/contracts/review-CTR-2025-003.md and save it to\n'
    'outputs/review-CTR-2025-003.md exactly as it is. Do not change\n'
    'anything in the file.'
)

add_para('The folder layout:', bold=True)
add_code_block(
    'Course_06_The_Guardian/practice/\n'
    '+-- .claude/settings.json\n'
    '|   (PreToolUse hook registered for Write tool)\n'
    '+-- data/contracts/\n'
    '|   +-- review-CTR-2025-003.md   (missing Risk Assessment)\n'
    '+-- hooks/\n'
    '|   +-- validate-report-hook.py\n'
    '+-- outputs/                      (empty, waiting for validated files)'
)

add_para('What you should see:', bold=True)
add_para(
    'Claude Code (in the terminal) reports that the write was blocked. The error message reads: '
    '"Report validation failed. Fix these issues before saving: 1. Missing required section: '
    'Risk Assessment."'
)

add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) read the contents of '
    'data/contracts/review-CTR-2025-003.md into memory.'
)
add_numbered(
    'Claude Code prepared a Write tool call with the file path '
    'outputs/review-CTR-2025-003.md and the full report content.'
)
add_numbered(
    'Before executing the write, Claude Code checked .claude/settings.json and found a '
    'PreToolUse hook registered for the Write tool.'
)
add_numbered(
    'Claude Code ran python hooks/validate-report-hook.py and passed the tool name ("Write"), '
    'the file path, and the file content as JSON on stdin.'
)
add_numbered(
    'The hook script parsed the JSON, checked the content for the pattern **Risk Level:**, '
    'and did not find it. It added "Missing required section: Risk Assessment" to the error list.'
)
add_numbered(
    'The hook returned {"decision": "block", "reason": "Report validation failed..."} '
    'as JSON on stdout.'
)
add_numbered(
    'Claude Code received the block response, did not write the file, and displayed the error '
    'message in the terminal.'
)

# --- Example 2: Audit Hook ---
doc.add_heading(
    'Example 2: The audit hook logs every action', level=2
)

add_para(
    'Scenario: Your VP of Procurement wants a record of every action Claude Code takes during a '
    'batch run. You have registered the audit hook with a matcher of "*" (all tools). Every Read, '
    'Write, Glob, Grep, and Bash call will be logged.'
)

add_para('The prompt to type (in the Claude Code terminal):', bold=True)
add_code_block(
    'Read data/contracts/review-CTR-2025-001.md and tell me the\n'
    'supplier name and the risk level.'
)

add_para('The folder layout:', bold=True)
add_code_block(
    'Course_06_The_Guardian/practice/\n'
    '+-- .claude/settings.json\n'
    '|   (PostToolUse hook registered for * matcher)\n'
    '+-- data/contracts/\n'
    '|   +-- review-CTR-2025-001.md\n'
    '+-- hooks/\n'
    '|   +-- audit-log-hook.py\n'
    '+-- audit/\n'
    '    +-- audit.jsonl               (log entries appended here)'
)

add_para('What you should see:', bold=True)
add_para(
    'Claude Code (in the terminal) reads the file and tells you the supplier is Great Lakes Steel '
    'and the risk level is Medium. After the command completes, a new JSON line appears in '
    'audit/audit.jsonl.'
)

add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) called the Read tool on '
    'data/contracts/review-CTR-2025-001.md.'
)
add_numbered(
    'After the Read completed, Claude Code checked .claude/settings.json for PostToolUse hooks '
    'matching the Read tool. The "*" matcher matched.'
)
add_numbered(
    'Claude Code ran python hooks/audit-log-hook.py and passed the tool call details as JSON '
    'on stdin.'
)
add_numbered(
    'The hook parsed the JSON, built a log entry with five fields: UTC timestamp, tool name '
    '("Read"), action type ("read"), file path, and session ID.'
)
add_numbered(
    'The hook opened audit/audit.jsonl in append mode and wrote one JSON line.'
)
add_numbered(
    'Claude Code continued and displayed the supplier name and risk level to you in the terminal.'
)

add_para('A sample audit log entry looks like this:')
add_code_block(
    '{"timestamp": "2026-04-25T15:30:00.000000+00:00",\n'
    ' "tool": "Read", "action": "read",\n'
    ' "file_path": "data/contracts/review-CTR-2025-001.md",\n'
    ' "session_id": "abc123"}'
)

# --- Example 3: Risk Alert Hook ---
doc.add_heading(
    'Example 3: The risk alert hook flags a Critical contract', level=2
)

add_para(
    'Scenario: Contract CTR-2025-002 with Heartland Polymers is a Critical-risk agreement worth '
    '$1,800,000 per year. After it passes validation and saves to outputs/, the risk alert hook '
    'should create an alert file in alerts/.'
)

add_para('The prompt to type (in the Claude Code terminal):', bold=True)
add_code_block(
    'Read data/contracts/review-CTR-2025-002.md and save it to\n'
    'outputs/review-CTR-2025-002.md exactly as it is.'
)

add_para('The folder layout:', bold=True)
add_code_block(
    'Course_06_The_Guardian/practice/\n'
    '+-- .claude/settings.json\n'
    '|   (all three hooks registered)\n'
    '+-- data/contracts/review-CTR-2025-002.md\n'
    '+-- hooks/\n'
    '|   +-- validate-report-hook.py\n'
    '|   +-- audit-log-hook.py\n'
    '|   +-- risk-alert-hook.py\n'
    '+-- outputs/\n'
    '+-- audit/\n'
    '+-- alerts/'
)

add_para('What you should see:', bold=True)
add_para(
    'Claude Code (in the terminal) saves the file to outputs/. Then an alert file appears in '
    'alerts/ named 2026-04-25-CTR-2025-002-critical-risk.txt. The alert contains the risk level '
    '(Critical), the contract ID (CTR-2025-002), the supplier name (Heartland Polymers), and a '
    'line saying "Action required: Review this contract and confirm risk mitigation."'
)

add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) prepared a Write tool call to '
    'outputs/review-CTR-2025-002.md.'
)
add_numbered(
    'The PreToolUse validation hook ran first. It checked all six quality rules (required sections, '
    'valid risk level, named supplier, non-empty clauses, and recommendation present). All passed. '
    'It returned {"decision": "approve"}.'
)
add_numbered('The file was written to disk.')
add_numbered(
    'The PostToolUse audit hook fired and appended a log entry for the Write action to '
    'audit/audit.jsonl.'
)
add_numbered(
    'The PostToolUse risk alert hook fired. It found **Risk Level:** Critical in the content. '
    'It extracted the contract ID (CTR-2025-002) and supplier name (Heartland Polymers).'
)
add_numbered(
    'The hook created alerts/2026-04-25-CTR-2025-002-critical-risk.txt with the alert details.'
)
add_numbered(
    'Low and Medium risk contracts do not trigger alerts. Only High and Critical do.'
)

# ===================================================================
# SECTION 7: DAY IN THE LIFE
# ===================================================================
doc.add_heading('7. Day in the Life: Rachel, Contract Manager', level=1)

add_para(
    'Rachel is a Contract Manager at MedLine Procurement Group, a US-based healthcare procurement '
    'firm in Chicago, IL. She manages supplier agreements for medical devices, lab supplies, and '
    'facilities maintenance. Her team reviews 40 to 60 contracts per month. She has been using '
    'Claude Code (in the terminal) for three weeks. Last week she set up the three hooks from '
    'this course on her contract review pipeline.'
)

add_para('Here is her Thursday.', bold=True)

# Scenario 1
doc.add_heading('08:30. Overnight batch results', level=3)
add_para(
    'Rachel arrives and checks her pipeline. Last night, Claude Code processed 15 contract reviews. '
    'She opens her terminal to check how many passed.'
)
add_para('The prompt:', bold=True)
add_code_block(
    'List the files in outputs/ and count them. Then list\n'
    'the files in alerts/ and show me each alert.'
)
add_para(
    'Claude Code (in the terminal) reports: 11 files in outputs/, 4 files blocked by the '
    'validation hook overnight. Two alert files in alerts/: one for CTR-2026-044 (Critical, '
    'Apex Surgical Instruments, $890,000) and one for CTR-2026-051 (High, Great Plains Lab Supply, '
    '$340,000). Rachel forwards the alert files to the legal team lead, Karen, by 08:45.'
)
add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) ran a Glob tool call on the outputs/ folder and counted 11 files.'
)
add_numbered('Claude Code ran a Glob tool call on the alerts/ folder and found 2 files.')
add_numbered(
    'Claude Code read each alert file and displayed the risk level, contract ID, and supplier name.'
)
add_numbered(
    'The PostToolUse audit hook logged all tool calls (two Glob calls and two Read calls) to '
    'audit/audit.jsonl.'
)
add_para(
    'What to learn from this. The alerts/ folder replaces the manual step of opening every report '
    'to find the urgent ones. Rachel checks one folder, not 15 files. The legal team gets notified '
    'in 15 minutes instead of after Rachel finishes reading every report.',
    italic=True,
)

# Scenario 2
doc.add_heading('09:15. Fixing a blocked report', level=3)
add_para(
    'Rachel checks which 4 reports were blocked. One is CTR-2026-047, a $520,000 facilities '
    'maintenance contract with CleanSpace Services. The validation hook blocked it because the '
    'risk level said "Moderate" instead of "Medium."'
)
add_para('The prompt:', bold=True)
add_code_block(
    'Read data/contracts/review-CTR-2026-047.md. Change the risk\n'
    'level from "Moderate" to "Medium". Save the corrected file to\n'
    'outputs/review-CTR-2026-047.md.'
)
add_para(
    'Claude Code (in the terminal) reads the file, changes "Moderate" to "Medium," and attempts '
    'the write. The validation hook runs, checks all six rules, and approves. The file saves to '
    'outputs/. The audit log records the read and the write. No alert fires because Medium is not '
    'High or Critical.'
)
add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) read the contract review file and found **Risk Level:** Moderate.'
)
add_numbered('Claude Code changed "Moderate" to "Medium" in the content.')
add_numbered(
    'Claude Code attempted a Write to outputs/. The PreToolUse validation hook ran.'
)
add_numbered(
    'The hook checked the risk level "Medium" against the allowed set (Low, Medium, High, and '
    'Critical). It matched.'
)
add_numbered(
    'The hook checked the other five rules. All passed. It returned {"decision": "approve"}.'
)
add_numbered(
    'The file was written. The audit hook logged the action. No risk alert was needed.'
)
add_para(
    'What to learn from this. The hook catches vocabulary mismatches that a human reviewer might '
    'overlook. "Moderate" sounds close enough to "Medium," but it is not in the taxonomy. The hook '
    'enforces the exact taxonomy every time, without judgment calls.',
    italic=True,
)

# Scenario 3
doc.add_heading('10:45. CPO asks for an audit summary', level=3)
add_para(
    'Rachel\'s CPO, David, messages her: "I need a summary of what Claude Code did during last '
    'night\'s batch. Which files were read, which were written, which were blocked. The board '
    'audit committee wants to see our AI controls."'
)
add_para('The prompt:', bold=True)
add_code_block(
    'Read audit/audit.jsonl. Summarize it as a table: for each\n'
    'unique file, show the tool used, the action type, and the\n'
    'timestamp. Group by file path. Sort by timestamp.'
)
add_para(
    'Claude Code (in the terminal) reads the JSONL file (84 entries from last night\'s batch), '
    'groups by file path, and produces a table. David gets a one-page summary showing that 15 '
    'contracts were read, 11 were written to outputs/, 4 writes were blocked, and 2 alerts were '
    'generated. Total processing time: 47 seconds.'
)
add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) read audit/audit.jsonl and parsed 84 JSON lines.'
)
add_numbered(
    'It grouped entries by the file_path field and sorted each group by timestamp.'
)
add_numbered(
    'It identified four distinct action types in the log: read, write, search, and other.'
)
add_numbered(
    'It formatted the results as a table with columns: file, tool, action, and timestamp.'
)
add_numbered(
    'The audit hook logged this Read action to audit/audit.jsonl (creating entry 85).'
)
add_para(
    'What to learn from this. The audit log is not just for compliance. It is a diagnostic tool. '
    'When something goes wrong in a batch, the log tells you exactly which file was being processed '
    'and which tool call failed. Without the log, you reconstruct from memory.',
    italic=True,
)

# Scenario 4
doc.add_heading('13:00. New contracts arrive mid-day', level=3)
add_para(
    'A supplier, Pinnacle Medical Devices, sends three revised contracts by email. Rachel saves them '
    'to data/contracts/ and asks Claude Code to process them.'
)
add_para('The prompt:', bold=True)
add_code_block(
    'Read each file in data/contracts/ that starts with\n'
    '"review-CTR-2026-06". Save each one to outputs/ with the same\n'
    'filename. Do not modify the contents. Process them one at a\n'
    'time and report the result.'
)
add_para(
    'Claude Code (in the terminal) processes three files. Two pass validation and save. One is '
    'blocked because the Recommendation section is empty (it says "TBD"). Rachel sees the block '
    'reason, drafts a recommendation in the file, and re-saves. All three are now in outputs/. '
    'One triggers a High risk alert for CTR-2026-063 ($1,200,000 surgical instrument supply '
    'agreement).'
)
add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) ran a Glob search for files matching review-CTR-2026-06*.'
)
add_numbered(
    'For each of the three files, Claude Code read the file and attempted a Write to outputs/.'
)
add_numbered(
    'The validation hook ran on each write. Two passed all six checks. One was blocked for an '
    'empty Recommendation.'
)
add_numbered(
    'After Rachel fixed the recommendation and re-saved, the hook approved the corrected file.'
)
add_numbered(
    'The risk alert hook fired on CTR-2026-063 (High risk) and created an alert file in alerts/.'
)
add_numbered(
    'The audit hook logged all actions: 3 reads, 2 approved writes, 1 blocked write, and 1 '
    're-write.'
)
add_para(
    'What to learn from this. Hooks handle ad-hoc work the same way they handle batch work. '
    'Rachel does not need to remember to run a validation checklist for mid-day arrivals. The '
    'hooks run automatically whether the batch is 15 files or 3.',
    italic=True,
)

# Scenario 5
doc.add_heading('14:30. Onboarding a colleague', level=3)
add_para(
    'Rachel\'s colleague, James, is starting to use Claude Code for his own category (office '
    'supplies, not medical). He wants to set up hooks for his pipeline. Rachel walks him through '
    'the setup.'
)
add_para('The prompt:', bold=True)
add_code_block(
    'Show me the contents of .claude/settings.json so I can explain\n'
    'the hook registration format to my colleague.'
)
add_para(
    'Claude Code (in the terminal) displays the settings.json with all three hooks. Rachel '
    'explains each entry to James: the matcher field, the command field, and when each hook fires. '
    'James copies the structure, changes the validation rules to match his office supplies taxonomy '
    '(different required sections, different risk levels), and registers his hooks.'
)
add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) read .claude/settings.json and displayed its contents.'
)
add_numbered('The audit hook logged the Read action.')
add_numbered(
    'No PreToolUse hook fired because this was a Read, not a Write.'
)
add_para(
    'What to learn from this. Hooks are portable across categories. The structure (PreToolUse '
    'for validation, PostToolUse for audit, PostToolUse for alerts) stays the same. Only the '
    'validation rules inside the script change. James changes the regex patterns and the allowed '
    'risk levels. He does not need to learn a new framework.',
    italic=True,
)

# Scenario 6
doc.add_heading('16:00. End-of-day compliance check', level=3)
add_para(
    'Before leaving, Rachel runs a final check. She wants to confirm that every contract processed '
    'today has an audit trail entry and that no file was saved to outputs/ without passing validation.'
)
add_para('The prompt:', bold=True)
add_code_block(
    'Read audit/audit.jsonl. For every file written to outputs/ today,\n'
    'confirm there is a corresponding Read entry and a Write entry.\n'
    'Flag any file that has a Write entry but no Read entry.'
)
add_para(
    'Claude Code (in the terminal) parses the audit log, filters for today\'s entries, and '
    'confirms: 14 files in outputs/ (11 from overnight and 3 from mid-day). All 14 have matching '
    'Read and Write entries. No orphan writes. Rachel screenshots the summary and sends it to '
    'David for the audit file.'
)
add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) read audit/audit.jsonl (now 97 entries for the day).'
)
add_numbered(
    'It filtered entries where the action was "write" and the file_path contained "outputs/".'
)
add_numbered(
    'For each Write entry, it searched for a matching Read entry with the same base filename.'
)
add_numbered('It found 14 matched pairs and zero orphans.')
add_numbered('It formatted the result as a confirmation summary.')
add_para(
    'What to learn from this. The audit log is machine-readable (JSONL), so Claude Code can query '
    'it the same way you would query a database. This turns compliance checks from manual reviews '
    'into prompts. The log answers the question "was every output validated?" in 5 seconds.',
    italic=True,
)

# Scenario 7
doc.add_heading('16:30. Planning tomorrow\'s batch', level=3)
add_para(
    'Rachel has 8 new contracts arriving tomorrow morning. She sets up the data folder and confirms '
    'the hooks are ready.'
)
add_para('The prompt:', bold=True)
add_code_block(
    'Clear the outputs/, audit/, and alerts/ folders. Confirm the\n'
    'three hooks are still registered in .claude/settings.json.'
)
add_para(
    'Claude Code (in the terminal) deletes files from the three output folders and reads '
    'settings.json. All three hooks are registered. Rachel is ready for tomorrow\'s batch. Total '
    'time spent on hook-related work today: 35 minutes, replacing what would have been 3 to 4 '
    'hours of manual review, audit trail construction, and risk flagging.'
)
add_para('What Claude did, behind the scenes:', bold=True)
add_numbered(
    'Claude Code (in the terminal) ran Bash commands to remove files from outputs/, audit/, '
    'and alerts/.'
)
add_numbered(
    'Claude Code read .claude/settings.json and confirmed three hook entries.'
)
add_numbered('The audit hook logged the Bash and Read actions.')
add_para(
    'What to learn from this. Hooks are persistent. Once registered, they stay active across '
    'sessions. Rachel did not re-register anything today. She set up the hooks once, and they '
    'ran on every batch since then. The setup cost is 30 minutes. The daily time saving is 3+ '
    'hours.',
    italic=True,
)

# ===================================================================
# SECTION 8: 20-MINUTE SPRINT
# ===================================================================
doc.add_heading('8. 20-Minute Sprint: Your First Hook in 20 Minutes', level=1)

add_para(
    'This section gets you from zero to a working validation hook in 20 minutes. Follow the '
    'time blocks exactly. Do not stop to read background material. You can read the theory later. '
    'The goal is one working hook, one blocked file, and one successful save.'
)

doc.add_heading('Minutes 0 to 5: Install and open', level=2)
add_numbered('Confirm Claude Code is installed. Open your terminal.')
add_numbered(
    'Navigate to the course folder: cd Course_06_The_Guardian/practice'
)
add_numbered('Start Claude Code: type claude and press Enter.')
add_numbered(
    'Confirm you see the Claude Code prompt with the folder path.'
)
add_numbered('Type the setup prompt:')
add_code_block(
    'The folder data/ holds source files. Do not edit any file in\n'
    'data/. Save all output to outputs/ unless I tell you otherwise.'
)

doc.add_heading('Minutes 5 to 10: Create the hook', level=2)
add_numbered('Create the hooks directory:')
add_code_block('mkdir -p hooks')
add_numbered(
    'Ask Claude Code to create the validation hook script. Type this prompt:'
)
add_code_block(
    'Create the file hooks/validate-report-hook.py with a\n'
    'PreToolUse validation script that checks for six required\n'
    'sections in contract review reports: Parties, Term, Value,\n'
    'Risk Assessment, Key Clauses, and Recommendation. It should\n'
    'block writes to outputs/ if any section is missing or if the\n'
    'risk level is not Low, Medium, High, or Critical.'
)
add_numbered('Create .claude/settings.json and register the hook:')
add_code_block(
    'Create .claude/settings.json with a PreToolUse hook entry.\n'
    'Matcher: "Write". Command: "python hooks/validate-report-hook.py".'
)

doc.add_heading('Minutes 10 to 15: Test with a flawed file', level=2)
add_numbered('Try to save a flawed report:')
add_code_block(
    'Read data/contracts/review-CTR-2025-003.md and save it to\n'
    'outputs/review-CTR-2025-003.md exactly as it is.'
)
add_numbered(
    'You should see the hook block the write with: "Missing required section: Risk Assessment."'
)
add_numbered('Now try a valid report:')
add_code_block(
    'Read data/contracts/review-CTR-2025-001.md and save it to\n'
    'outputs/review-CTR-2025-001.md exactly as it is.'
)
add_numbered('The file should save successfully. No error message.')

doc.add_heading('Minutes 15 to 20: Review and plan next steps', level=2)
add_numbered('Confirm the results:')
add_code_block('List the files in outputs/.')
add_numbered(
    'You should see review-CTR-2025-001.md (the valid one) and no review-CTR-2025-003.md '
    '(the blocked one).'
)
add_numbered(
    'You now have a working quality gate. Every file write to outputs/ goes through your '
    'validation hook. No report with a missing section or invalid risk level can reach the '
    'legal team.'
)
add_numbered(
    'Next steps: work through Lessons 3 and 4 to add the audit hook and the risk alert hook. '
    'Then Lesson 5 for error handling and Lesson 6 for the integration test.'
)

# ===================================================================
# SECTION 9: FIRST WEEK PLANNER
# ===================================================================
doc.add_heading('9. First Week Day-by-Day Planner', level=1)

add_para(
    'This planner assumes you spend 45 to 90 minutes per day on the course. By Friday you will '
    'have all three hooks running, tested, and error-hardened.'
)

# Day 1
doc.add_heading('Day 1 (Monday): Install, explore, and understand hook types', level=2)
add_para('Goals:', bold=True)
add_bullet(
    'Install Claude Code (in the terminal) if not already installed.'
)
add_bullet('Open the practice folder and explore the data files.')
add_bullet(
    'Complete Lesson 1: understand the four hook types (PreToolUse, PostToolUse, Stop, '
    'and Notification).'
)
add_bullet('Create .claude/settings.json with an empty hooks structure.')
add_para(
    'Deliverable: A working Claude Code session with .claude/settings.json in place, ready '
    'for hook registration.'
)

# Day 2
doc.add_heading('Day 2 (Tuesday): Build the validation hook', level=2)
add_para('Goals:', bold=True)
add_bullet(
    'Complete Lesson 2: write and register the PreToolUse validation hook.'
)
add_bullet('Test with at least two flawed files and two valid files.')
add_bullet(
    'Understand the flow: stdin JSON in, validation checks, stdout JSON response out.'
)
add_para(
    'Deliverable: hooks/validate-report-hook.py registered and blocking flawed reports.'
)

# Day 3
doc.add_heading(
    'Day 3 (Wednesday): Build the audit and alert hooks', level=2
)
add_para('Goals:', bold=True)
add_bullet(
    'Complete Lesson 3: write and register the PostToolUse audit hook.'
)
add_bullet(
    'Complete Lesson 4: write and register the PostToolUse risk alert hook.'
)
add_bullet('Test all three hooks together on at least three files.')
add_para(
    'Deliverable: All three hooks registered. Audit log and alert files appearing as expected.'
)

# Day 4
doc.add_heading(
    'Day 4 (Thursday): Error handling and defensive coding', level=2
)
add_para('Goals:', bold=True)
add_bullet(
    'Complete Lesson 5: add try/except blocks to all three hooks.'
)
add_bullet('Test with invalid JSON input and missing fields.')
add_bullet(
    'Understand the rule: PreToolUse hooks default to approve on error. PostToolUse hooks '
    'fail silently.'
)
add_para(
    'Deliverable: All three hooks handle unexpected input without crashing.'
)

# Day 5
doc.add_heading(
    'Day 5 (Friday): Integration test and reflection', level=2
)
add_para('Goals:', bold=True)
add_bullet(
    'Complete Lesson 6: run all 12 contract reviews through the full pipeline.'
)
add_bullet(
    'Confirm 6 blocked, 6 saved, audit log complete, and alerts generated for high-risk '
    'contracts.'
)
add_bullet('Review the audit log and produce a summary table.')
add_bullet(
    'Plan how to adapt these hooks for your own contract types and categories.'
)
add_para(
    'Deliverable: A clean integration test with 6 saved reports in outputs/, a complete audit '
    'log in audit/audit.jsonl, and alert files in alerts/ for High and Critical risk contracts.'
)

# ===================================================================
# SECTION 10: THE PATTERN
# ===================================================================
doc.add_heading(
    '10. The Pattern: Hooks as Automated Quality Gates', level=1
)

add_para(
    'The transferable principle from this course is straightforward: any rule you check by hand, '
    'you can enforce with a hook.'
)

add_para(
    'The validation hook checks six rules against every contract review report. But the same '
    'pattern works for any document type. An RFP response that must have a pricing table, a scope '
    'section, and a compliance matrix. A supplier onboarding form that must have a tax ID, a DUNS '
    'number, and a bank account. A purchase order that must not exceed $50,000 without a second '
    'approver\'s name in the header.'
)

add_para(
    'The audit hook logs every tool call to a JSONL file. But the same pattern works for any '
    'audit requirement. SOX compliance for financial document changes. ISO 27001 evidence of '
    'controlled access to sensitive files. Internal audit trails for category strategy decisions.'
)

add_para(
    'The risk alert hook watches for High and Critical values in a specific field. But the same '
    'pattern works for any threshold-based alert. A spend amount that exceeds a budget ceiling. '
    'A contract expiry date within 90 days. A supplier risk score that crosses from acceptable '
    'to watch-list.'
)

add_para('The pattern has three parts:', bold=True)

add_numbered(
    'Define the rule in plain language. "Every report must have a Risk Assessment section."'
)
add_numbered(
    'Write a Python script that checks the rule. Read JSON from stdin, check the content, '
    'print JSON to stdout.'
)
add_numbered(
    'Register the script in .claude/settings.json with the right hook type and matcher.'
)

add_para(
    'Once registered, the hook runs on every matching tool call. You do not need to remember to '
    'run it. You do not need to add it to a checklist. You do not need to train a colleague to '
    'check it. The hook just runs, every time, automatically.'
)

add_para(
    'This is what "The Guardian" means. The hook guards the quality of your outputs the way a '
    'gate guard checks IDs. It does not do the work. It checks the work before it leaves the '
    'building.'
)

doc.add_heading('Adapting the pattern to a new document type', level=2)

add_para(
    'To apply this pattern to a different procurement document (for example, an RFP evaluation '
    'scorecard), follow these steps:'
)

add_numbered(
    'List the required sections for your document. For an RFP scorecard: Scoring Criteria, '
    'Supplier Scores, Weighted Totals, and Recommendation.'
)
add_numbered(
    'List the valid values for any constrained fields. For a scorecard: scores must be integers '
    'from 1 to 5. Recommendation must be "Award," "Shortlist," or "Reject."'
)
add_numbered(
    'Copy validate-report-hook.py. Change the REQUIRED_SECTIONS list to match your document. '
    'Change the VALID_RISK_LEVELS set to match your constrained field values.'
)
add_numbered(
    'Register the new hook in .claude/settings.json. The matcher and command fields work the '
    'same way.'
)
add_numbered(
    'Test with at least one valid file and one file with a planted flaw. If the hook misses '
    'the flaw, check the regex pattern.'
)

add_para(
    'The audit hook and risk alert hook need no changes for a new document type. The audit hook '
    'logs every tool call regardless of content. The risk alert hook only needs a change if the '
    'field name or threshold values differ.'
)

# ===================================================================
# SECTION 11: TROUBLESHOOTING
# ===================================================================
doc.add_heading('11. Troubleshooting', level=1)

doc.add_heading('Things to remember', level=2)

add_bullet(
    'Hooks are a Claude Code (in the terminal) feature only. Claude AI Web and Claude Desktop '
    'with Cowork do not support hooks.'
)
add_bullet(
    'Hook scripts must read JSON from stdin and (for PreToolUse) write JSON to stdout. No other '
    'input/output mechanism works.'
)
add_bullet(
    'PreToolUse hooks can approve or block. PostToolUse hooks can only react. They cannot undo '
    'a completed action.'
)
add_bullet(
    'Tool names are case-sensitive. "Write" works. "write" does not.'
)
add_bullet(
    'The matcher "*" fires on every tool call. Use it for audit hooks that must capture everything.'
)
add_bullet(
    'Hook commands use relative paths from the project root. Claude Code runs them in the project '
    'directory.'
)
add_bullet(
    'Always wrap hook logic in try/except. A crashed PreToolUse hook can block the entire pipeline. '
    'A crashed PostToolUse hook can lose log entries.'
)
add_bullet(
    'PreToolUse hooks should default to approve on error. Blocking production writes because your '
    'hook is broken is worse than letting one report through unchecked.'
)

doc.add_heading('Symptom and fix reference', level=2)

add_table(
    ['Symptom', 'Likely cause', 'Fix'],
    [
        [
            'Hook never fires. Claude Code saves the file without validation.',
            'The matcher in settings.json is wrong (lowercase "write" instead of "Write"), '
            'or the settings.json file is in the project root instead of .claude/settings.json.',
            'Change the matcher to "Write" (capital W). Move settings.json into the .claude/ '
            'directory.',
        ],
        [
            'Hook blocks every file, including valid ones.',
            'The path filter in the script does not match. The regex for a required section '
            'does not match the actual section format in the report.',
            'Print the file_path to stderr for debugging: print(file_path, file=sys.stderr). '
            'Check each regex pattern against a known-valid file.',
        ],
        [
            'Hook crashes with "json.decoder.JSONDecodeError".',
            'The script is trying to read from a file or from command-line arguments instead '
            'of stdin.',
            'The script must use json.loads(sys.stdin.read()) to read input. Check the main() '
            'function.',
        ],
        [
            'Audit log overwrites itself, keeping only the last entry.',
            'The file is opened in write mode ("w") instead of append mode ("a").',
            'Change the open() call to use mode "a": open(AUDIT_FILE, "a", encoding="utf-8").',
        ],
        [
            'Alert files appear for Low and Medium risk contracts.',
            'The HIGH_RISK_LEVELS set includes "Low" or "Medium".',
            'Change the set to {"High", "Critical"} only.',
        ],
        [
            'Claude Code says the hook returned an invalid response.',
            'The PreToolUse hook is printing something other than valid JSON to stdout, or the '
            'JSON is missing the "decision" field.',
            'The response must be valid JSON with a "decision" field set to "approve" or '
            '"block". Nothing else should go to stdout. Print debug info to stderr instead.',
        ],
    ],
)

# ===================================================================
# SECTION 12: DONE CHECKLIST
# ===================================================================
doc.add_heading('12. Done Checklist', level=1)

add_para(
    'Use this checklist to confirm you have completed the course. Each item maps to a specific '
    'skill or deliverable.'
)

checklist_items = [
    'You can explain the difference between PreToolUse and PostToolUse hooks and when to use each.',
    'Your .claude/settings.json has three hooks registered: validate-report (PreToolUse on Write), '
    'audit-log (PostToolUse on *), and risk-alert (PostToolUse on Write).',
    'You can ask Claude Code (in the terminal) to save a flawed contract review to outputs/ and '
    'the PreToolUse hook blocks the write with a specific error message.',
    'You can ask Claude Code (in the terminal) to save a valid contract review and the file saves. '
    'The audit log has an entry. If the risk level is High or Critical, an alert file appears in '
    'alerts/.',
    'You have run the full batch of 12 contract reviews. Six are blocked (the flawed ones). Six '
    'are saved. The audit log has entries for every tool call. Alert files exist for the high-risk '
    'contracts.',
    'All three hook scripts have try/except error handling. A crashed hook defaults to approve '
    '(PreToolUse) or fails silently (PostToolUse).',
    'You can feed invalid JSON to each hook script from the terminal and it exits cleanly without '
    'a traceback.',
    'You can read audit/audit.jsonl and produce a summary of what Claude Code did during a batch run.',
    'You can explain the three-part pattern (define the rule, write the script, and register in '
    'settings.json) and describe how to apply it to a different document type.',
    'You have compared your hook scripts against the solutions in solutions/ and resolved any '
    'differences.',
]

for item in checklist_items:
    add_bullet(item)

add_para('')  # spacer

# Footer
footer_para = doc.add_paragraph()
footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = footer_para.add_run(
    'U2xAI  |  ProcureAI Academy  |  Series 2  |  Course 6: The Guardian  |  April 2026'
)
run.font.name = 'Calibri'
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

# ── Save ──
output_path = (
    Path(__file__).resolve().parent.parent
    / "Handouts"
    / "Course_06_The_Guardian_Handout.docx"
)
os.makedirs(output_path.parent, exist_ok=True)
doc.save(str(output_path))
print(f"Saved to: {output_path}")

# Word count estimate
text = '\n'.join([p.text for p in doc.paragraphs])
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            text += ' ' + cell.text
wc = len(text.split())
print(f"Estimated word count: {wc}")
