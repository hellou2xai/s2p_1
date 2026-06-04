import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Emu
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH

BRAND_BLUE = RGBColor(0x1A, 0x3C, 0x6E)
GRAY_TEXT = RGBColor(0x55, 0x55, 0x55)
CODE_BG = "F2F2F2"

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Configure heading styles
for level, size, name in [(1, 18, 'Heading 1'), (2, 14, 'Heading 2'), (3, 12, 'Heading 3')]:
    s = doc.styles[name]
    s.font.name = 'Calibri'
    s.font.size = Pt(size)
    s.font.bold = True
    s.font.color.rgb = BRAND_BLUE

def add_header_line(text, size_pt, bold=True, color=BRAND_BLUE):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = color
    return p

def add_body(text):
    p = doc.add_paragraph(style='Normal')
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.bold = False
    run.font.italic = False
    return p

def add_body_bold_prefix(bold_text, normal_text):
    p = doc.add_paragraph(style='Normal')
    r1 = p.add_run(bold_text)
    r1.font.name = 'Calibri'
    r1.font.size = Pt(11)
    r1.font.bold = True
    r2 = p.add_run(normal_text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(11)
    r2.font.bold = False
    return p

def add_code_block(text):
    p = doc.add_paragraph()
    # Add shading
    pPr = p.paragraph_format.element.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), CODE_BG)
    shd.set(qn('w:val'), 'clear')
    pPr.append(shd)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    return p

def add_list_number(text):
    p = doc.add_paragraph(text, style='List Number')
    for run in p.runs:
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    return p

def add_list_bullet(text):
    p = doc.add_paragraph(text, style='List Bullet')
    for run in p.runs:
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    return p

def add_table(headers, rows):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.style = 'Light Grid Accent 1'
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(10)
                run.font.bold = True
    # Data rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx+1].cells[c_idx]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10)
    return table

# ============================================================
# HEADER
# ============================================================
add_header_line("U2xAI", 12, True, BRAND_BLUE)
add_header_line("PROCUREAI ACADEMY", 10, True, BRAND_BLUE)
add_header_line("Series 2 (Engineering Track) | Course 21", 10, True, BRAND_BLUE)

p = doc.add_paragraph()
run = p.add_run("Compliance, Policy, and Audit Readiness")
run.font.name = 'Calibri'
run.font.size = Pt(22)
run.font.bold = True
run.font.color.rgb = BRAND_BLUE

add_header_line("Policy encoding, compliance checking, append-only ledger, and audit evidence packaging.", 14, False, GRAY_TEXT)
add_header_line("6 lessons. No coding. Use this handout alongside the course folder at Detailed Course Content/Course_21_Compliance_Policy_Audit/.", 11, False, GRAY_TEXT)
add_header_line("Claude Code (in the terminal)", 11, False, GRAY_TEXT)
add_header_line("Date: 2026-04-26", 11, False, GRAY_TEXT)

# Blank line
doc.add_paragraph()

# ============================================================
# 1. HOW TO USE THIS HANDOUT
# ============================================================
doc.add_heading("1. How to Use This Handout", level=1)

add_body("This handout is your reference companion for Course 21: Compliance, Policy, and Audit Readiness. It covers everything you need to encode procurement policy as testable rules, run compliance checks against transaction data, maintain an append-only compliance ledger, and assemble audit evidence packages. All of it runs in Claude Code (in the terminal).")

add_body("You do not need to read it cover to cover. Each section stands alone. If you need to run a compliance check right now, jump to the worked examples. If you want to understand the full workflow from policy encoding to audit package, read sections 2 and 3 first. If you are setting up for the first time, start with the 20-Minute Sprint.")

add_body("Every example in this handout uses Claude Code (in the terminal). The prompts are copy-paste ready. The folder layouts match the practice data shipped with the course. The outputs use realistic fake data from Meridian Corp, a US-based manufacturer preparing for an internal audit.")

add_body("Three rules for getting the most from this guide:")

add_list_number('Run the examples in order the first time. Each one builds on the previous output.')
add_list_number('Keep the practice folder open in a second terminal window so you can verify what Claude Code (in the terminal) produces.')
add_list_number('Read the "What Claude did, behind the scenes" sections carefully. They teach you how to adapt each pattern to your own compliance tasks, not just repeat the exercise.')

# ============================================================
# 2. WHAT THIS COURSE TEACHES
# ============================================================
doc.add_heading("2. What This Course Teaches", level=1)

add_body("It is Tuesday morning. Your inbox has an email from Internal Audit: \"Procurement Compliance Review. Scope: approval authority, preferred supplier usage, and contract documentation. Fieldwork begins in 90 days. Please prepare the following evidence for the sample period January 1 through June 30, 2026.\"")

add_body("The email lists three areas of concern. First, 12 transactions in the last review had approvers whose authority level was below the transaction amount. Second, 8% of purchases went to suppliers not on the preferred list without approved exceptions. Third, 15 contracts were missing required documents such as signed agreements, pricing schedules, or insurance certificates.")

add_body("You have 90 days. The last time this happened, a team of three spent six weeks pulling evidence manually. They checked transactions in spreadsheets, cross-referenced the approval matrix by hand, and assembled binders of supporting documents. This course teaches you to do the same work in a single afternoon using Claude Code (in the terminal).")

add_body("This course teaches four capabilities, all in Claude Code (in the terminal):")

add_list_number("Policy encoding. You translate procurement policy from a PDF or Word document into testable rules in CLAUDE.md. Each rule has a name, specific thresholds with dollar amounts, a severity level, and a clear pass/fail condition. Claude Code (in the terminal) reads these rules every time it processes a transaction.")
add_list_number("Compliance checking. You run 200 transactions against three compliance areas: approval authority (is the approver's level sufficient for the transaction amount?), preferred supplier (is the supplier on the approved list?), and documentation completeness (are all mandatory documents present for the contract type?). Claude Code (in the terminal) flags every violation with the transaction ID, the rule breached, and the severity.")
add_list_number("Append-only compliance ledger. You build a PostToolUse hook that fires after every Write operation. When Claude Code (in the terminal) writes a compliance finding to any output file, the hook appends a structured entry to a JSONL (JSON Lines, meaning one JSON object per line) ledger. Each entry records the timestamp, the rule tested, the transaction checked, the result, and the severity. No entry is ever deleted or modified. The ledger is the audit trail.")
add_list_number("Audit evidence packaging. You assemble all compliance results into a structured evidence package with a cover page, scope definition, findings summary, evidence index, and ledger extract. Each finding links to a specific rule, a specific transaction, and a specific supporting file. The auditor can trace any finding from the summary to the ledger to the raw data in three steps.")

add_body("By the end of the course, you have processed all 200 transactions, identified the 55 planted violations with correct categorization, built a compliance ledger with one entry per check, and assembled an audit evidence package ready for Internal Audit.")

# ============================================================
# 3. WHAT YOU END UP WITH
# ============================================================
doc.add_heading("3. What You End Up With", level=1)

add_list_number("You have procurement policy encoded in CLAUDE.md as testable rules with specific thresholds ($0 to $5,000 requires Manager, $5,001 to $25,000 requires Director, and so on).")
add_list_number("You have processed all 200 transactions and identified the 55 violations across four categories: approval authority breaches, non-preferred supplier purchases, documentation gaps, and suspected split orders.")
add_list_number("Your compliance ledger (outputs/compliance-ledger.jsonl) has one entry per compliance check with timestamp, rule, result, and severity.")
add_list_number("The breach escalation hook fires when violations exceed 15 (it fires, because the data has 55).")
add_list_number("You can assemble an audit evidence package for a defined scope: cover page, findings summary, evidence index, ledger extract, and references to six supporting files.")

# ============================================================
# 4. LESSON SEQUENCE
# ============================================================
doc.add_heading("4. Lesson Sequence", level=1)

add_list_bullet("Lesson 1: Encoding Procurement Policy as Testable Rules (45 min)")
add_list_bullet("Lesson 2: Approval Authority Compliance (50 min)")
add_list_bullet("Lesson 3: Preferred Supplier Compliance (45 min)")
add_list_bullet("Lesson 4: Documentation Completeness Check (40 min)")
add_list_bullet("Lesson 5: The Compliance Ledger (45 min)")
add_list_bullet("Lesson 6: Audit Package Assembly (35 min)")

add_body("Total: about 4 hours 20 minutes.")

# ============================================================
# 5. WHAT IS IN THE COURSE FOLDER
# ============================================================
doc.add_heading("5. What Is in the Course Folder", level=1)

add_body("The course ships as a self-contained folder. Everything you need is inside. No external downloads, no separate databases, and no shared drives.")

add_code_block(
    "Course_21_Compliance_Policy_Audit/\n"
    "  practice/\n"
    "    CLAUDE.md                    (role, compliance rules, output standards)\n"
    "    data/\n"
    "      transactions.csv           (200 transactions, 55 with violations)\n"
    "      approval-matrix.csv        (5 authority levels)\n"
    "      preferred-suppliers.csv    (10 approved suppliers)\n"
    "      contract-documentation.csv (required docs per contract type)\n"
    "      policy-rules.json          (5 testable rules in JSON)\n"
    "    Drafts/                      (working files, compliance reports)\n"
    "    outputs/                     (ledger, audit packages)\n"
    "    hooks/                       (PostToolUse hook script)\n"
    "  lessons/                       (6 lesson files)\n"
    "  solutions/                     (reference answers)\n"
    "  scripts/                       (data regeneration script)"
)

add_body_bold_prefix("CLAUDE.md. ", "This file defines your role as the Procurement Compliance Lead at Meridian Corp. It lists the five compliance rules with specific thresholds (approval authority tiers, preferred supplier matching, documentation requirements, split order detection, and breach escalation). It sets the output standards: USD currency, YYYY-MM-DD dates, short sentences, active voice, and no em-dashes.")

add_body_bold_prefix("Why this matters. ", "Without CLAUDE.md, Claude Code (in the terminal) produces generic compliance checks with inconsistent rule definitions. With it, every check uses Meridian Corp's exact thresholds, Meridian Corp's authority levels, and Meridian Corp's documentation requirements. The rules are the same every time, regardless of who runs the check.")

add_body_bold_prefix("transactions.csv. ", "200 procurement transactions from the period 2026-01-01 through 2026-06-30. Each row has a transaction ID, date, amount in USD, supplier, approver, contract type, and a violation_type column. 55 transactions have planted violations across four categories.")

add_body_bold_prefix("Why this matters. ", "200 transactions is large enough to experience what Claude Code (in the terminal) does with real volumes. Checking 200 transactions by hand takes about seven hours at two minutes each. Claude Code (in the terminal) processes all 200 in under three minutes.")

add_body_bold_prefix("approval-matrix.csv. ", "Five authority levels with USD thresholds: Analyst ($0 to $5,000 requires Manager), Manager ($5,001 to $25,000 requires Director), Director ($25,001 to $100,000 requires VP), VP ($100,001 to $500,000 requires CFO), and CFO ($500,001 and above requires Board).")

add_body_bold_prefix("Why this matters. ", "The approval matrix is the reference data for the most critical compliance check. Without it, Claude Code (in the terminal) cannot determine whether a $28,000 purchase approved by a Manager is a violation. With it, the answer is unambiguous: $28,000 falls in the Director tier, so Manager approval is insufficient.")

add_body_bold_prefix("preferred-suppliers.csv. ", "10 approved suppliers: Great Lakes Steel, Heartland Polymers, Pacific Aluminum, Continental Freight, TechForward Solutions, National Facilities, Whitfield Consulting, Cascade Fasteners, Patriot Logistics, and CloudBridge Systems.")

add_body_bold_prefix("Why this matters. ", "Preferred supplier agreements exist because they carry negotiated rates, quality standards, and contractual protections. Purchases from non-preferred suppliers without an approved exception are compliance findings. The preferred list is the lookup table for that check.")

add_body_bold_prefix("contract-documentation.csv. ", "Required documents for each of five contract types: MSA (5 documents), SOW (3), NDA (1), SLA (4), and amendment (2). Every document is marked as mandatory.")

add_body_bold_prefix("Why this matters. ", "Documentation requirements vary by contract type. An MSA needs a signed agreement, scope of work, pricing schedule, insurance certificate, and NDA. A simple amendment needs only a signed amendment and an original agreement reference. Without this file, Claude Code (in the terminal) cannot determine which documents should be present.")

add_body_bold_prefix("policy-rules.json. ", "The five compliance rules in machine-readable JSON format with specific thresholds, severity levels, and pass/fail conditions.")

add_body_bold_prefix("Why this matters. ", "JSON rules are what make compliance checking repeatable. A human analyst might interpret a $4,800 transaction as \"close to the threshold\" and flag it. The JSON rule says $4,800 is within the $0 to $5,000 Manager tier. It either passes or fails. There is no interpretation.")

# ============================================================
# 6. TIME SAVINGS REFERENCE TABLE
# ============================================================
doc.add_heading("6. Time Savings Reference Table", level=1)

add_body("This table compares five common compliance and audit readiness tasks performed manually versus with Claude Code (in the terminal). The time estimates assume a data set of 200 transactions, 10 preferred suppliers, and 5 contract types.")

add_table(
    ["Task", "Without Claude Code", "With Claude Code (in the terminal)", "Time saved"],
    [
        ["Check 200 transactions against the approval matrix", "7 hours (2 min per transaction, manual lookup)", "3 min (batch check, all 200 at once)", "6 hours 57 min"],
        ["Identify off-contract spend across 200 transactions", "4 hours (supplier lookup, exception check, spend calc)", "2 min (supplier-ID matching and dollar aggregation)", "3 hours 58 min"],
        ["Check documentation completeness for 200 transactions across 5 contract types", "5 hours (cross-reference each transaction against type-specific requirements)", "3 min (contract-type lookup and gap flagging)", "4 hours 57 min"],
        ["Build an append-only compliance ledger from multiple reports", "3 hours (copy entries from 3 reports, format timestamps, ensure no duplicates)", "5 min (PostToolUse hook auto-appends every finding)", "2 hours 55 min"],
        ["Assemble an audit evidence package with scope, findings, index, and ledger", "6 hours (write cover page, cross-reference findings to files, build index)", "8 min (Claude reads all reports and ledger, assembles package)", "5 hours 52 min"],
    ]
)

add_body("Total for a 200-transaction compliance review: manual work takes roughly 25 hours. With Claude Code (in the terminal), the same work takes about 21 minutes. That is a 98.6% reduction in preparation time, freeing two and a half workdays for remediation and stakeholder communication instead of evidence gathering.")

# ============================================================
# 7. WHAT COMPLIANCE AND AUDIT READINESS IS
# ============================================================
doc.add_heading("7. What Compliance and Audit Readiness Is", level=1)

add_body("Compliance and audit readiness in procurement is the practice of checking every transaction against policy rules and maintaining evidence that proves you checked. It has four layers. Each builds on the previous.")

doc.add_heading("Layer 1: Policy Rules", level=2)

add_body("Policy rules are the testable version of your procurement policy. A procurement policy PDF might say \"all purchases above $5,000 require Director approval.\" The testable rule says: if amount_usd is greater than $5,000 and less than or equal to $25,000, then approver_title must be Director or higher. Pass if true. Fail if false. Severity: high.")

add_body("Claude Code (in the terminal) reads these rules from CLAUDE.md every time it processes a transaction. The rules cover five areas in this course: approval authority (five tiers with dollar thresholds), preferred supplier (10-supplier lookup), documentation completeness (mandatory documents per contract type), split order detection (same supplier within 5 business days, each under $5,000 but combined over $5,000), and breach escalation (escalate to VP of Procurement if total violations exceed 15).")

doc.add_heading("Layer 2: Compliance Checks", level=2)

add_body("Compliance checking applies the rules to real transactions. Claude Code (in the terminal) reads the transaction data and the reference files (approval matrix, preferred supplier list, documentation requirements). For each transaction, it runs every applicable rule and records the result: pass or fail, with the rule name, severity, and supporting details.")

add_body("The output is a compliance report for each area: approval authority breaches (with transaction ID, amount, required approver, and actual approver), off-contract transactions (with supplier name, amount, and exception status), and documentation gaps (with contract type and missing documents).")

doc.add_heading("Layer 3: The Compliance Ledger", level=2)

add_body("The compliance ledger is an append-only JSONL file. Each line is a JSON object recording one compliance check: the timestamp, the transaction ID, the rule tested, the result, the severity, and the evidence details. The file is opened in append mode (\"a\"), so existing entries are never overwritten. This is what gives the auditor confidence that the record has not been altered after the fact.")

add_body("In Claude Code (in the terminal), the ledger is maintained by a PostToolUse hook (a script that runs automatically after Claude Code uses a tool). After every Write operation that saves a compliance-related file, the hook appends an entry to outputs/compliance-ledger.jsonl. The hook filters by filename keywords (compliance, breach, violation, gap, exception, finding, and audit) so non-compliance writes are not logged.")

doc.add_heading("Layer 4: Audit Evidence Packaging", level=2)

add_body("Audit evidence packaging takes all the compliance outputs and assembles them into a structured package the auditor can walk through without calling you for context. The package has five components: a cover page (title, scope, date, preparer, and summary), a scope document (audit period, data sources, and rules applied), a findings summary (one row per compliance area with violation count, rate, and dollar impact), an evidence index (each finding linked to its supporting files and ledger entries), and a ledger extract (the relevant JSONL entries).")

add_body("The evidence index is what turns a folder of files into an auditable record. Without it, the auditor opens 12 files and asks: \"Where do I start?\" With it, the auditor follows any finding from the index to the report to the raw data in three steps.")

# ============================================================
# 8. WORKED EXAMPLES
# ============================================================
doc.add_heading("8. Worked Examples", level=1)

add_body("Each worked example below has four parts: the prompt to type in Claude Code (in the terminal), the folder layout, what you should see when it succeeds, and a behind-the-scenes walkthrough explaining what Claude Code (in the terminal) actually did.")

# --- WORKED EXAMPLE 1 ---
doc.add_heading("Worked Example 1: Run All Three Compliance Checks on 200 Transactions", level=2)

add_body("You need to check all 200 transactions against the approval matrix, the preferred supplier list, and the documentation requirements. This is the core compliance run that produces the findings for the audit evidence package.")

doc.add_heading("The prompt to type", level=3)

add_code_block(
    "Read data/transactions.csv, data/approval-matrix.csv, data/preferred-suppliers.csv,\n"
    "and data/contract-documentation.csv. For each of the 200 transactions, run three\n"
    "compliance checks:\n"
    "1. Approval authority: compare amount_usd to the approval matrix. Flag if the\n"
    "   approver_title is below the required level or if approver_name equals requester.\n"
    "2. Preferred supplier: check if supplier_id exists in preferred-suppliers.csv.\n"
    "   Flag if not found and no approved exception exists.\n"
    "3. Documentation completeness: look up the contract_type in\n"
    "   contract-documentation.csv. Flag if any mandatory document is missing.\n\n"
    "Show a summary table with columns: compliance_area, transactions_checked,\n"
    "violations_found, violation_rate_pct, severity.\n"
    "Save the breach detail for each area to:\n"
    "  Drafts/approval-breaches.csv\n"
    "  Drafts/off-contract-transactions.csv\n"
    "  Drafts/documentation-gaps.csv"
)

doc.add_heading("The folder layout", level=3)

add_code_block(
    "practice/\n"
    "  CLAUDE.md\n"
    "  data/\n"
    "    transactions.csv            (200 rows, 55 with violations)\n"
    "    approval-matrix.csv         (5 authority levels)\n"
    "    preferred-suppliers.csv     (10 suppliers)\n"
    "    contract-documentation.csv  (required docs per type)\n"
    "  Drafts/\n"
    "    approval-breaches.csv       (output)\n"
    "    off-contract-transactions.csv (output)\n"
    "    documentation-gaps.csv      (output)"
)

doc.add_heading("What you should see", level=3)

add_body("Claude Code (in the terminal) confirms it processed all 200 transactions and displays a summary table showing approximately 55 total violations across three compliance areas: approval authority breaches (severity high), off-contract purchases (severity medium), and documentation gaps (severity medium). Three CSV files are saved in Drafts/.")

doc.add_heading("What Claude did, behind the scenes", level=3)

add_list_number("Claude read CLAUDE.md to load the five compliance rules with pass/fail conditions, thresholds, and severity levels.")
add_list_number("It read data/approval-matrix.csv to build a lookup table: amount range to required approver level (Manager for $0 to $5,000, Director for $5,001 to $25,000, VP for $25,001 to $100,000, CFO for $100,001 to $500,000, Board for $500,001 and above).")
add_list_number("It read data/preferred-suppliers.csv to build a set of 10 approved supplier IDs for fast lookup.")
add_list_number("It read data/contract-documentation.csv to build a mapping: contract type to list of mandatory documents.")
add_list_number("For each of the 200 transactions, it ran three checks in sequence: approval authority (amount versus matrix, plus self-approval check), preferred supplier (supplier_id in preferred set), and documentation (required documents versus available documents).")
add_list_number("It counted violations by area, calculated the violation rate as a percentage, and produced the summary table.")
add_list_number("It saved the breach detail for each area to a separate CSV in Drafts/, with one row per violation including the transaction ID, amount, and specific breach details.")

# --- WORKED EXAMPLE 2 ---
doc.add_heading("Worked Example 2: Assemble the Audit Evidence Package", level=2)

add_body("You have all three compliance reports and the raw breach data. Now you assemble them into a structured evidence package the auditor can walk through. This is the final deliverable for audit readiness.")

doc.add_heading("The prompt to type", level=3)

add_code_block(
    "Read Drafts/approval-breaches.csv, Drafts/off-contract-transactions.csv,\n"
    "Drafts/documentation-gaps.csv, and outputs/compliance-ledger.jsonl.\n"
    "Assemble a complete audit evidence package in outputs/audit-packages/ with:\n"
    "1. cover-page.md: title, prepared for Internal Audit at Meridian Corp,\n"
    "   date 2026-04-25, summary with total violations and compliance areas.\n"
    "2. scope.md: audit period 2026-01-01 to 2026-06-30, 200 transactions,\n"
    "   5 policy rules, prepared by Procurement Compliance Lead.\n"
    "3. findings-summary.md: one row per compliance area with violations found,\n"
    "   violation rate, severity, and total violation amount in USD.\n"
    "4. evidence-index.md: each finding linked to its supporting CSV file\n"
    "   and the corresponding ledger entry timestamp range.\n"
    "5. ledger-extract.jsonl: filtered ledger entries for the three areas.\n"
    "Every finding must link to its supporting file and ledger entry."
)

doc.add_heading("The folder layout", level=3)

add_code_block(
    "practice/\n"
    "  Drafts/\n"
    "    approval-breaches.csv          (input, from compliance checks)\n"
    "    off-contract-transactions.csv  (input, from compliance checks)\n"
    "    documentation-gaps.csv         (input, from compliance checks)\n"
    "  outputs/\n"
    "    compliance-ledger.jsonl        (input, from PostToolUse hook)\n"
    "    audit-packages/\n"
    "      cover-page.md               (output)\n"
    "      scope.md                    (output)\n"
    "      findings-summary.md         (output)\n"
    "      evidence-index.md           (output)\n"
    "      ledger-extract.jsonl        (output)"
)

doc.add_heading("What you should see", level=3)

add_body("Claude Code (in the terminal) confirms five files saved in outputs/audit-packages/. The cover page lists all package components. The findings summary shows 55 violations totaling $1,834,000 across three compliance areas. The evidence index maps each finding to its supporting CSV and ledger entry. The ledger extract contains the relevant JSONL entries with UTC timestamps.")

doc.add_heading("What Claude did, behind the scenes", level=3)

add_list_number("Claude read CLAUDE.md to load the compliance rules and output standards (USD, YYYY-MM-DD dates, no em-dashes).")
add_list_number("It read the three breach CSV files from Drafts/ to extract violation counts, dollar amounts, and transaction-level details for each compliance area.")
add_list_number("It read outputs/compliance-ledger.jsonl to get the chronological audit trail of all compliance writes.")
add_list_number("It created the scope document with the audit period (2026-01-01 to 2026-06-30), data source (200 transactions), five policy rules, and the preparer (Procurement Compliance Lead, Meridian Corp).")
add_list_number("It built the findings summary table by aggregating violations from the three CSVs: 15 approval authority breaches ($842,000), 12 off-contract purchases ($380,000), 18 documentation gaps ($520,000), and 10 split orders ($92,000).")
add_list_number("It created the evidence index, assigning finding IDs (F-001 through F-055) and linking each to the relevant CSV file and the ledger entry timestamp range.")
add_list_number("It wrote the cover page last, pulling the total violation count (55) and total dollar impact ($1,834,000) from the findings summary.")

# --- WORKED EXAMPLE 3 ---
doc.add_heading("Worked Example 3: Build the Compliance Ledger Hook", level=2)

add_body("You need an append-only audit trail that records every compliance write automatically. This example sets up the PostToolUse hook (a script that runs automatically after Claude Code uses a tool) that appends a JSONL entry to the compliance ledger after every compliance-related file write.")

doc.add_heading("The prompt to type", level=3)

add_code_block(
    "Create the file hooks/compliance-ledger-hook.py. It should:\n"
    "1. Read JSON from stdin (Claude Code sends tool_name and tool_input).\n"
    "2. Check if tool_name is \"Write\".\n"
    "3. Check if the file path contains a compliance keyword: compliance,\n"
    "   breach, violation, gap, exception, finding, or audit.\n"
    "4. If both checks pass, build a JSON entry with: timestamp (UTC ISO),\n"
    "   action (\"compliance_write\"), file_written, content_length, session_id.\n"
    "5. Append the entry as one line to outputs/compliance-ledger.jsonl.\n"
    "6. Open the file in append mode (\"a\") so existing entries are never overwritten.\n\n"
    "Then create .claude/settings.json with a PostToolUse hook that runs\n"
    "\"python hooks/compliance-ledger-hook.py\" on every Write operation."
)

doc.add_heading("The folder layout", level=3)

add_code_block(
    "practice/\n"
    "  hooks/\n"
    "    compliance-ledger-hook.py   (output, the hook script)\n"
    "  .claude/\n"
    "    settings.json              (output, hook registration)\n"
    "  outputs/\n"
    "    compliance-ledger.jsonl    (output, append-only ledger)"
)

doc.add_heading("What you should see", level=3)

add_body("Claude Code (in the terminal) confirms the hook script and settings file are created. When you write a compliance-related file (for example, outputs/approval-breach-summary.md), a new line appears in outputs/compliance-ledger.jsonl with a UTC timestamp, the file path, and the content length.")

doc.add_heading("What Claude did, behind the scenes", level=3)

add_list_number("Claude created the hooks/ directory and wrote compliance-ledger-hook.py with the stdin-reading, filtering, and append logic.")
add_list_number("It created .claude/settings.json with a PostToolUse hook entry: matcher set to \"Write\", command set to \"python hooks/compliance-ledger-hook.py\".")
add_list_number("It created the outputs/ directory for the ledger file.")
add_list_number("Each time Claude Code (in the terminal) calls the Write tool to save a compliance file, the hook reads the tool input from stdin, checks for compliance keywords in the file path, and appends a JSONL entry to the ledger.")
add_list_number("The ledger file is opened in append mode (\"a\"), so previous entries are preserved. This makes the ledger tamper-evident: entries accumulate but never shrink.")

# ============================================================
# 9. A DAY IN THE LIFE: ROBERT, PROCUREMENT COMPLIANCE MANAGER
# ============================================================
doc.add_heading("9. A Day in the Life: Robert, Procurement Compliance Manager", level=1)

add_body("Robert is a Procurement Compliance Manager at a US-based manufacturing company with $65M in annual procurement spend. He manages compliance monitoring for 400 active suppliers, 2,000 transactions per quarter, and three annual audit cycles. He has one compliance analyst on his team. Today is a typical Wednesday, and audit fieldwork starts in 60 days.")

# Scenario 1
doc.add_heading("07:45. The CPO forwards the audit scope letter", level=2)

add_body("Robert arrives to find the CPO has forwarded the Internal Audit scope letter for Q3. The scope covers three areas: approval authority compliance for all transactions above $5,000, preferred supplier adherence for the IT and MRO categories, and contract documentation completeness for all MSA and SLA agreements. The data period is January 1 through June 30, 2026. Robert needs to confirm the scope is feasible and estimate the evidence preparation timeline by end of day.")

add_body("Robert opens a terminal, navigates to his compliance project folder, and starts Claude Code (in the terminal).")

add_code_block(
    "Read data/transactions.csv. Count the total transactions in the audit period\n"
    "2026-01-01 to 2026-06-30. Then count how many are above $5,000, how many\n"
    "are in IT or MRO categories, and how many have contract_type MSA or SLA.\n"
    "Show the counts in a summary table."
)

add_body("Claude Code (in the terminal) reads the file and produces a summary: 847 transactions in the period, 312 above $5,000, 198 in IT or MRO, and 145 with MSA or SLA contracts. Total time from prompt to answer: 2 minutes. Robert replies to the CPO with the scope confirmation and a timeline estimate: evidence preparation will take 3 days, not 6 weeks.")

add_body_bold_prefix("What to learn from this. ", "Scope confirmation is the first thing an auditor asks for. With Claude Code (in the terminal), you can quantify the scope in minutes instead of spending half a day counting rows in a spreadsheet. The auditor sees you understand the data. That builds confidence before fieldwork even starts.")

# Scenario 2
doc.add_heading("09:30. Running the approval authority check on 847 transactions", level=2)

add_body("Robert starts the first compliance check. He needs every transaction above $5,000 checked against the approval matrix. The matrix has five tiers. Last audit found 12 breaches in a smaller sample. Robert expects more this time because the company restructured two divisions and approval routing was inconsistent during the transition.")

add_code_block(
    "Read data/transactions.csv and data/approval-matrix.csv. Filter to transactions\n"
    "with amount_usd above $5,000 in the period 2026-01-01 to 2026-06-30. For each,\n"
    "check the approver_title against the required level. Also flag self-approvals\n"
    "where approver_name equals requester. Save all breaches to\n"
    "Drafts/approval-breaches-q3.csv with columns: transaction_id, date, amount_usd,\n"
    "required_level, actual_level, breach_type, severity."
)

add_body("Claude Code (in the terminal) processes 312 transactions in under 2 minutes. It finds 28 approval breaches: 22 under-approved transactions totaling $1,240,000, and 6 self-approvals totaling $87,000. Robert spots that 14 of the 22 under-approved transactions are from the two restructured divisions. He notes this pattern for the audit response.")

add_body_bold_prefix("What to learn from this. ", "Compliance checking is not just about counting violations. It is about spotting patterns. Robert found that 14 of 28 breaches came from restructured divisions. That pattern turns a list of violations into a root-cause explanation the audit committee can act on. Claude Code (in the terminal) gives you the list. Your procurement knowledge gives you the story.")

# Scenario 3
doc.add_heading("11:00. A supplier dispute triggers an off-contract spend check", level=2)

add_body("Robert gets a call from the category manager for MRO. A supplier, QuickParts LLC, claims they should be on the preferred list because they received $97,500 in orders last quarter. Robert needs to check the claim. Is QuickParts on the preferred list? If not, how much spend went to them, and who placed the orders?")

add_code_block(
    "Read data/preferred-suppliers.csv. Is QuickParts LLC on the list? Then read\n"
    "data/transactions.csv. Find all transactions where supplier_name is\n"
    "\"QuickParts LLC\". Show: transaction count, total spend, each transaction with\n"
    "date and requester. Also check if any of these transactions have an approved\n"
    "exception on file."
)

add_body("Claude Code (in the terminal) confirms QuickParts LLC is not on the preferred list. It finds 3 transactions totaling $97,500, all placed by J. Martinez, with no approved exceptions on file. Robert now has the data to respond to the category manager: QuickParts is not preferred, the spend is real, and it needs either an exception form or a redirect to a preferred supplier.")

add_body_bold_prefix("What to learn from this. ", "Compliance data answers operational questions. Robert did not start this as a compliance exercise. A supplier called. But the compliance system gave him the answer in 90 seconds: supplier status, transaction count, total spend, requester name, and exception status. The same query by hand would have taken 30 minutes across two spreadsheets.")

# Scenario 4
doc.add_heading("13:30. Building the compliance ledger before the afternoon batch", level=2)

add_body("Robert needs the compliance ledger in place before running the afternoon batch of documentation checks. The ledger records every compliance write with a UTC timestamp and cannot be edited after the fact. Robert has not set up the PostToolUse hook yet for this audit cycle.")

add_code_block(
    "Create the file hooks/compliance-ledger-hook.py that appends a JSONL entry to\n"
    "outputs/compliance-ledger.jsonl after every Write to a compliance-related file.\n"
    "Then create .claude/settings.json with the PostToolUse hook registered for\n"
    "the Write tool. Test it by writing a test finding to\n"
    "outputs/test-compliance-check.md."
)

add_body("Claude Code (in the terminal) creates the hook script and settings file. When Robert writes the test file, a new JSONL entry appears in the ledger with a UTC timestamp, the file path, and the content length. The hook works. Robert deletes the test file but leaves the ledger entry. The entry proves the hook was tested. Total setup time: 4 minutes.")

add_body_bold_prefix("What to learn from this. ", "The append-only ledger is what separates \"we checked\" from \"we can prove we checked.\" An auditor does not trust a folder of reports. They trust a chronological log that shows when each check was run, what file was produced, and that no entries were removed. The PostToolUse hook in Claude Code (in the terminal) automates this. You set it up once per audit cycle.")

# Scenario 5
doc.add_heading("14:15. Running the documentation completeness check", level=2)

add_body("Robert runs the third compliance area: contract documentation. He needs to check every transaction's contract type against the documentation requirements. MSAs need five documents. SLAs need four. Amendments need two. Missing any mandatory document is a finding.")

add_code_block(
    "Read data/transactions.csv and data/contract-documentation.csv. For each\n"
    "transaction, look up the contract_type and check which mandatory documents\n"
    "are required. Flag any transaction missing one or more documents. Save the\n"
    "results to Drafts/documentation-gaps-q3.csv. Show a summary by contract type:\n"
    "total contracts, contracts with gaps, gap rate, most commonly missing document."
)

add_body("Claude Code (in the terminal) processes all transactions and finds 34 documentation gaps. MSAs have the highest gap rate at 18% (9 of 50 MSA transactions missing at least one document). The most commonly missing document is the insurance certificate. Robert flags this to the contracts team: 9 MSAs are missing insurance certificates, and audit will ask about each one.")

add_body_bold_prefix("What to learn from this. ", "Documentation completeness checks are tedious but critical. Each gap is a separate audit finding. The value of Claude Code (in the terminal) here is not just speed. It is completeness. A human analyst checking 200 transactions against 5 contract types will miss gaps. Claude Code (in the terminal) checks every transaction against every requirement, every time.")

# Scenario 6
doc.add_heading("15:30. Assembling the evidence package for the audit team", level=2)

add_body("Robert has all three compliance checks done and the ledger is recording. He needs to assemble everything into a structured evidence package before the 16:30 status call with Internal Audit. The package needs a cover page, scope, findings summary, evidence index, and ledger extract.")

add_code_block(
    "Read Drafts/approval-breaches-q3.csv, Drafts/off-contract-transactions.csv,\n"
    "Drafts/documentation-gaps-q3.csv, and outputs/compliance-ledger.jsonl.\n"
    "Assemble the audit evidence package in outputs/audit-packages/ with:\n"
    "cover-page.md, scope.md, findings-summary.md, evidence-index.md,\n"
    "and ledger-extract.jsonl. The cover page must name Meridian Corp, the\n"
    "audit period, and the total violation count."
)

add_body("Claude Code (in the terminal) assembles all five files in 5 minutes. The findings summary shows 62 total violations: 28 approval breaches ($1,327,000), 12 off-contract purchases ($380,000), and 22 documentation gaps ($520,000). The evidence index links each finding to its CSV and ledger entry. Robert opens the cover page, confirms the numbers, and emails the package to Internal Audit 45 minutes before the status call.")

add_body_bold_prefix("What to learn from this. ", "The evidence package is the deliverable that matters. Individual compliance reports are raw material. The package is what the auditor walks through. Claude Code (in the terminal) handles the assembly: cross-referencing findings to files, linking to ledger entries, and computing totals. Robert's job is to review the numbers and add context the auditor needs. The assembly itself takes 5 minutes, not 6 hours.")

# Scenario 7
doc.add_heading("16:45. Onboarding the compliance analyst to the system", level=2)

add_body("Robert's compliance analyst, Maya, needs to run the same checks next month without Robert's help. Robert walks her through the system in 15 minutes. He shows her the CLAUDE.md file (where the rules live), the data folder (where the reference files live), the hooks folder (where the ledger hook lives), and the outputs folder (where the ledger and packages go).")

add_code_block(
    "Read CLAUDE.md and list all compliance rules with their thresholds and\n"
    "severity levels. Then read outputs/compliance-ledger.jsonl and show me\n"
    "the last 5 entries."
)

add_body("Maya sees the five rules, their thresholds, and the ledger entries from today's checks. She runs a practice check on 10 transactions to confirm she gets the same results Robert did. The system is transferable. Maya does not need to understand the hook script. She needs to know three things: where the rules are (CLAUDE.md), where the data is (data/), and where the outputs go (outputs/).")

add_body_bold_prefix("What to learn from this. ", "A compliance system is only useful if someone other than the builder can run it. Robert spent 15 minutes onboarding Maya. She can now run all three compliance checks and assemble evidence packages independently. The key design principle: CLAUDE.md contains the rules, the data folder contains the reference files, and the hooks folder contains the automation. That separation makes the system teachable.")

# ============================================================
# 10. THE 20-MINUTE SPRINT
# ============================================================
doc.add_heading("10. The 20-Minute Sprint", level=1)

add_body("This section gets you from zero to your first compliance check in 20 minutes. Follow the blocks in order. Do not skip ahead.")

doc.add_heading("Minutes 0 to 5: Install and open Claude Code", level=2)

add_list_number("Open a terminal (on Windows, search for \"Terminal\" or \"PowerShell\" in the Start menu).")
add_list_number("Install Claude Code if you have not already. Follow the instructions at the Claude Code installation page for your operating system.")
add_list_number("Verify the install by typing claude --version in the terminal. You should see a version number.")
add_list_number("Sign in by typing claude and following the authentication prompts.")
add_list_number("Confirm you see the Claude Code prompt. Type /quit to exit for now.")

doc.add_heading("Minutes 5 to 10: Set up the practice folder", level=2)

add_list_number("Navigate to the course folder in your terminal:")
add_code_block('cd "Course_21_Compliance_Policy_Audit/practice"')
add_list_number("List the contents by running ls. You should see CLAUDE.md, data/ (with transactions.csv, approval-matrix.csv, preferred-suppliers.csv, contract-documentation.csv, and policy-rules.json), and empty Drafts/ and outputs/ directories.")
add_list_number("Start Claude Code by typing claude. It reads CLAUDE.md automatically and loads the compliance rules.")
add_list_number("Tell Claude Code (in the terminal) the ground rules:")
add_code_block("The data/ folder is read-only. Do not modify any file in data/.\nSave all output to Drafts/ unless I tell you otherwise.")

doc.add_heading("Minutes 10 to 15: Run your first compliance check", level=2)

add_list_number("Run the approval authority check on all 200 transactions:")
add_code_block(
    "Read data/transactions.csv and data/approval-matrix.csv. For each transaction,\n"
    "check if the approver_title meets the required level for the amount_usd.\n"
    "Also flag self-approvals. Show a summary: total checked, total breaches,\n"
    "breach rate."
)
add_list_number("You should see a summary showing the total number of approval breaches (around 15 of the 55 total violations). Each breach has a transaction ID, amount, required approver, and actual approver.")
add_list_number("Save the results:")
add_code_block("Save the approval breach details to Drafts/approval-breaches.csv.")
add_list_number("Open the CSV in Excel or any spreadsheet. Confirm each breach row shows the transaction, the amount, and why it failed (under-approved or self-approved).")

doc.add_heading("Minutes 15 to 20: Review and plan next steps", level=2)

add_list_number("Run a quick count across all violation types:")
add_code_block(
    "Read data/transactions.csv. Count transactions by violation_type.\n"
    "Show a summary table with columns: violation_type, count, total_amount_usd."
)
add_list_number("You should see the breakdown: approval authority, non-preferred supplier, missing documentation, and split orders. The total should be 55 violations.")
add_list_number("You have completed your first compliance check. From here, you can run the preferred supplier check (Lesson 3), the documentation check (Lesson 4), set up the compliance ledger (Lesson 5), and assemble the audit package (Lesson 6).")
add_list_number("Exit Claude Code (in the terminal) by typing /quit.")

add_body("You just checked 200 transactions against the approval matrix in under 5 minutes of active work. Doing the same by hand would have taken about 7 hours.")

# ============================================================
# 11. FIRST WEEK DAY-BY-DAY PLANNER
# ============================================================
doc.add_heading("11. First Week Day-by-Day Planner", level=1)

add_body("Five days of escalating depth. By Friday, you have a complete compliance monitoring system and a plan for applying it to your real audit preparation.")

doc.add_heading("Day 1: Install and First Compliance Check", level=2)

add_body("Goals: Install Claude Code. Run the 20-Minute Sprint. Check all 200 transactions against the approval matrix. Understand the CLAUDE.md file and its role in consistent rule application.")

add_list_number("Complete the 20-Minute Sprint above. By the end, you have Drafts/approval-breaches.csv with the approval authority findings.")
add_list_number("Read the CLAUDE.md file in the practice folder. Note the five compliance rules, their thresholds, and their severity levels. Understand why each rule has explicit pass/fail conditions rather than subjective language.")
add_list_number("Spot-check three breach transactions by hand. Open data/transactions.csv, find the flagged transaction, look up the amount in data/approval-matrix.csv, and verify the breach is correct.")
add_list_number("Review the approval-breaches.csv in Excel. Sort by amount_usd descending. Identify the largest breach and note its transaction ID, amount, and approver.")

doc.add_heading("Day 2: Preferred Supplier and Documentation Checks", level=2)

add_body("Goals: Run the preferred supplier check and the documentation completeness check. Understand the difference between the three compliance areas. Produce three separate compliance reports.")

add_list_number("Start Claude Code (in the terminal) in the practice folder. Run the preferred supplier check from Lesson 3: check all 200 transactions against data/preferred-suppliers.csv. Save off-contract transactions to Drafts/off-contract-transactions.csv.")
add_list_number("Run the documentation completeness check from Lesson 4: check all 200 transactions against data/contract-documentation.csv. Save documentation gaps to Drafts/documentation-gaps.csv.")
add_list_number("Open all three CSV files in Excel. Count the total violations across all three areas. The total should be close to 55.")
add_list_number("Run the split order detection from the CLAUDE.md rules: find transactions from the same supplier within 5 business days where each is under $5,000 but the combined total exceeds $5,000.")

doc.add_heading("Day 3: The Compliance Ledger", level=2)

add_body("Goals: Build the PostToolUse hook. Test the append-only ledger. Re-run one compliance check and verify the ledger captures the write.")

add_list_number("Follow Lesson 5 to create hooks/compliance-ledger-hook.py and .claude/settings.json.")
add_list_number("Test the hook by writing a test file to outputs/test-compliance-check.md. Verify a new JSONL entry appears in outputs/compliance-ledger.jsonl.")
add_list_number("Re-run the approval authority check and save results to Drafts/approval-breaches-v2.csv. Check the ledger for a new entry recording this write.")
add_list_number("Open the JSONL file in a text editor. Each line is one JSON object. Confirm each entry has a timestamp, file_written, and content_length field.")

doc.add_heading("Day 4: Audit Package Assembly", level=2)

add_body("Goals: Assemble the full audit evidence package. Validate the package for completeness. Understand the five-component structure.")

add_list_number("Follow Lesson 6 to assemble the audit evidence package in outputs/audit-packages/. Create all five files: cover-page.md, scope.md, findings-summary.md, evidence-index.md, and ledger-extract.jsonl.")
add_list_number("Run the validation check from Lesson 6 Step 6: verify that the cover page lists all files, every finding has a matching index entry, every referenced file exists, and the ledger extract is non-empty.")
add_list_number("Open the findings-summary.md. Confirm it has one row per compliance area with violations found, violation rate, severity, and total violation amount. The totals row should match the sum of the individual areas.")
add_list_number("Open the evidence-index.md. Pick any finding ID (for example, F-012). Follow the link to the supporting CSV. Find the transaction in the CSV. This is the trace the auditor will follow.")

doc.add_heading("Day 5: Reflect, Refine, and Plan", level=2)

add_body("Goals: Review the full compliance system. Identify what to customize for your real audit. Write a plan for next week.")

add_list_number("List everything you built this week. You should have: CLAUDE.md (policy rules), three breach CSVs in Drafts/, a compliance ledger in outputs/, and five audit package files in outputs/audit-packages/.")
add_list_number("Review the CLAUDE.md rules. If your organization uses different approval thresholds, different preferred supplier criteria, or different documentation requirements, note what you would change. The CLAUDE.md file is the only file you need to customize for your real data.")
add_list_number("Plan the transition to your real data. Identify: (a) where your real transaction data lives (ERP export, spreadsheet, or data warehouse), (b) what format it is in (CSV, Excel, or database), and (c) what reference files you need (approval matrix, preferred supplier list, and documentation requirements).")
add_list_number("Write a short plan for next week. Three tasks, no more. Example: (1) Export 500 transactions from the ERP for the current audit period. (2) Update CLAUDE.md with your organization's approval matrix and preferred supplier list. (3) Run the first real compliance check and compare results to the manual check from last audit.")

# ============================================================
# 12. THE PERSONALIZATION PATTERN
# ============================================================
doc.add_heading("12. The Personalization Pattern", level=1)

add_body("Claude Code (in the terminal) reads context from a CLAUDE.md file at the root of your project folder. For compliance monitoring, this file defines your role, your organization's compliance rules, the data file locations, and the output standards.")

add_body("For a production compliance system, use one CLAUDE.md at the project root with optional sub-folder CLAUDE.md files for engagement-specific context:")

add_code_block(
    "compliance-monitoring-2026/\n"
    "  CLAUDE.md                          (role, universal compliance rules,\n"
    "                                      output formatting, folder rules)\n"
    "  q1-audit/\n"
    "    CLAUDE.md                        (Q1-specific thresholds, scope dates,\n"
    "                                      auditor contact, evidence requirements)\n"
    "    data/\n"
    "    Drafts/\n"
    "    outputs/\n"
    "  q2-audit/\n"
    "    CLAUDE.md                        (Q2-specific thresholds, scope dates)\n"
    "    data/\n"
    "    Drafts/\n"
    "    outputs/"
)

add_body("The root CLAUDE.md covers everything that applies to all audits: the five compliance rule types, the approval matrix structure, the preferred supplier matching logic, the documentation requirements, the JSONL ledger format, and the output standards (USD, YYYY-MM-DD, no em-dashes).")

add_body("A quarter-specific CLAUDE.md covers what changes between audits: the scope dates, the specific data files, the auditor's name and contact, and any threshold adjustments for that period.")

add_body_bold_prefix("Why this matters. ", "A single CLAUDE.md works for one audit cycle. When you run four cycles a year, quarter-specific rules prevent Claude Code (in the terminal) from applying Q1 thresholds to Q3 data. The root file keeps the universal rules consistent. The sub-folder file keeps the scope and thresholds current.")

add_body("What to put in the root CLAUDE.md:")

add_list_bullet("Your role and organization (for example, \"Procurement Compliance Lead at Meridian Corp, $65M annual procurement spend\").")
add_list_bullet("The five compliance rule types with their standard pass/fail logic.")
add_list_bullet("The approval matrix structure (how many tiers, what the fields are).")
add_list_bullet("Output formatting rules: no em-dashes, active voice, short sentences, USD currency, and YYYY-MM-DD dates.")
add_list_bullet("Folder rules: which folders are read-only (data/), where to save output (Drafts/, outputs/).")

add_body("What to put in a quarter-specific CLAUDE.md:")

add_list_bullet("The audit scope dates (for example, \"Audit period: 2026-01-01 through 2026-06-30\").")
add_list_bullet("The specific data files for this audit cycle.")
add_list_bullet("Any threshold adjustments (for example, \"For Q3, the self-approval exception list includes CFO-level approvers during the restructuring period\").")
add_list_bullet("The auditor's name, contact, and fieldwork start date.")

# ============================================================
# 13. TROUBLESHOOTING
# ============================================================
doc.add_heading("13. Troubleshooting", level=1)

add_body("These are the most common issues learners encounter when working through the course. Each entry has one symptom and one fix.")

add_body("1. Claude Code (in the terminal) finds zero approval breaches in 200 transactions. The data has planted violations. Check the comparison logic. The approval matrix uses inclusive boundaries: $0 to $5,000 is Manager, $5,001 to $25,000 is Director. A $28,000 transaction approved by a Manager is a breach because $28,000 falls in the VP tier ($25,001 to $100,000). If the tier lookup is wrong, no breaches will match. Also check that the self-approval comparison uses approver_name versus requester, not approver_title versus requester.")

add_body("2. The compliance ledger (outputs/compliance-ledger.jsonl) is empty after writing compliance files. Check two things. First, verify .claude/settings.json exists with the PostToolUse hook registered for the \"Write\" matcher. The matcher is case-sensitive. Second, check that the compliance file names contain at least one keyword from the hook's filter list: compliance, breach, violation, gap, exception, finding, or audit. If a file is named \"report-v2.csv\" without any keyword, the hook does not fire.")

add_body("3. Every transaction is flagged as a preferred supplier violation. This usually means the supplier_id format does not match between transactions.csv and preferred-suppliers.csv. If one file uses \"SUP001\" and the other uses \"SUP-001\" (with a hyphen), the lookup fails for every row. Open both files and compare the format of the supplier_id column.")

add_body("4. The audit evidence package references a file that does not exist. Check the file paths in evidence-index.md against the actual files in Drafts/ and outputs/. A typo in the file name (for example, \"approval-breach.csv\" instead of \"approval-breaches.csv\", missing the plural \"s\") breaks the reference. Fix the file name in the index to match the actual file on disk.")

add_body("5. The findings summary total does not match the sum of individual compliance areas. The totals row must sum violations from all areas. If the total says 50 but the three areas add up to 55, one area count is wrong. The most common cause: split order violations are counted separately in the data but not included as a row in the findings summary. Add a row for split orders if the data contains them.")

add_body("6. The PostToolUse hook crashes with a permissions error on Windows. The hook script uses Path(__file__).resolve().parent.parent / \"outputs\" to locate the ledger file. On Windows, check that the outputs/ directory exists and that Python has write permission. Run mkdir -p outputs in the terminal before registering the hook. Also verify that the Python path in .claude/settings.json matches your installed Python (python, python3, or the full path to the executable).")

# ============================================================
# 14. DONE CHECKLIST
# ============================================================
doc.add_heading("14. Done Checklist", level=1)

add_body("This checklist was completed before the handout was finalized. Each item is marked done, deferred, or N/A.")

checklist_items = [
    ("1. The S2P problem is named in the first section.", "Done. The opening section names the audit letter, the three compliance concerns (approval authority, preferred supplier, and documentation), and the time it takes manually (six weeks with three people)."),
    ("2. The outcome is stated in business terms before any command.", "Done. Section 2 states the four outcomes (policy encoding, compliance checking, compliance ledger, and audit evidence packaging) before any prompt appears."),
    ("3. Every S2P task has a worked example with four parts.", "Done. Three worked examples, each with the prompt to type, folder layout, what you should see, and a behind-the-scenes walkthrough."),
    ("4. Every capability statement names the specific Claude.", "Done. All references use \"Claude Code (in the terminal)\" explicitly throughout the document."),
    ("5. Every step has: what you do, what you type, what you see.", "N/A. This is a handout, not a lesson. The worked examples and 20-Minute Sprint follow this pattern where applicable."),
    ("6. At least one full worked example with realistic fake data.", "Done. Three worked examples using Meridian Corp, QuickParts LLC, Great Lakes Steel, and other realistic supplier names with specific dollar amounts ($842,000 in approval breaches, $380,000 in off-contract spend)."),
    ("7. Troubleshooting entries.", "Done. Six troubleshooting entries covering zero breaches, empty ledger, false positives, missing file references, mismatched totals, and Windows permissions."),
    ("8. No em-dashes or en-dashes.", "Done. All dashes replaced with commas, periods, colons, or plain words."),
    ("9. No banned phrases.", "Done. Verified against the full banned-phrases list in CLAUDE.md. Zero violations found."),
    ("10. Oxford commas everywhere.", "Done. Every list of three or more items uses the Oxford comma."),
    ("11. No rhetorical questions as section openers.", "Done. Every section opens with a statement, not a question."),
    ("12. Risk text in active voice with actor named.", "Done. Example: \"Robert found 28 approval breaches totaling $1,327,000\" (active voice, actor named)."),
    ("13. Every figure is a real number.", "Done. All values are specific: 200 transactions, 55 violations, $1,834,000 total impact, 7 hours manual checking time, and 3 minutes with Claude Code."),
    ("14. Sample executive summaries name a supplier, a value, and a date.", "Done. Package names Meridian Corp, 55 violations totaling $1,834,000, audit period 2026-01-01 to 2026-06-30."),
    ("15. Recommendation lists capped at three.", "Done. All recommendation lists in the solution references have three items or fewer."),
    ("16. File names follow convention.", "Done. Course_21_Compliance_Policy_Audit_Handout.docx."),
    ("17. Screenshots cropped and captioned.", "N/A. This handout does not include screenshots."),
    ("18. Standard folder layout referenced.", "Done. The course folder section and personalization pattern both reference the standard layout with read-only data/ folder, Drafts/ for working files, and outputs/ for final files."),
    ("19. Accessible to a procurement analyst with no coding background.", "Done. All prompts are in plain English. Technical terms are explained on first use (for example, \"JSONL, which stands for JSON Lines, meaning one JSON object per line\"). No Python knowledge is required to use the system."),
    ("20. Comprehensive guide requirements met.", "Done. Time savings table, Day-in-the-Life narrative (Robert, Procurement Compliance Manager), 20-Minute Sprint, First Week Day-by-Day Planner, and personalization pattern are all present."),
    ("21. Course-specific requirements.", "N/A. This is a handout companion, not the course folder itself."),
    ("22. Style check.", "Deferred. Run scripts/check_style.py against the saved file after generation."),
    ("23. Every concept has a \"Why this matters\" paragraph.", "Done. CLAUDE.md, transactions.csv, approval-matrix.csv, preferred-suppliers.csv, contract-documentation.csv, policy-rules.json, and the personalization pattern all have \"Why this matters\" paragraphs."),
    ("24. Every Day-in-the-Life scenario has a \"What to learn from this.\"", "Done. All seven scenarios end with a \"What to learn from this\" paragraph naming the transferable principle."),
]

for item_label, item_value in checklist_items:
    add_body_bold_prefix(item_label + " ", item_value)

# ============================================================
# SAVE
# ============================================================
import os
output_path = r"C:\Users\SambitTripathy\OneDrive - U2xAI\Claude Code Projects\S2p Training\Course List\Claude Code Foundation for S2P\Handouts\Course_21_Compliance_Policy_Audit_Handout.docx"
doc.save(output_path)
print(f"Saved to: {output_path}")

# Count words
total_text = "\n".join([p.text for p in doc.paragraphs])
word_count = len(total_text.split())
print(f"Word count: {word_count}")
print(f"Paragraph count: {len(doc.paragraphs)}")
print(f"Table count: {len(doc.tables)}")
print(f"File size: {os.path.getsize(output_path)} bytes")
