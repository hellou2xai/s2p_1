"""Build 'Claude for Dummies: a Source-to-Pay quick start' as a Word file.

Adapted for S2P professionals from Ruben Sosa,
'Claude for Dummies' (https://ruben.substack.com/p/claude-for-dummies).

Style follows the course CLAUDE.md: no em-dashes, Oxford commas everywhere,
plain English, British spelling, banned-word list respected.
"""

import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


OUTPUT_PATH = Path(
    r"C:\Users\sambi\OneDrive - U2xAI\Claude Code Projects"
    r"\S2p Training\Course List\Claude Code Foundation for S2P"
    r"\Handouts\Claude_For_Dummies_S2P.docx"
)


# ---------- helpers ----------------------------------------------------------

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


# State for manual list numbering. Each numbered list restarts at 1
# whenever any non-numbered helper (heading, para, bullet, code_block,
# fill_table) is called between numbered() calls.
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
    """Numbered list item with hand-rolled numbering.

    Restarts at 1 whenever a non-numbered helper appears between calls,
    so each logical list (each set of behind-the-scenes steps, each
    setup checklist, each test-drive flow) numbers from 1 again.
    """
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
    num_run = p.add_run(f"{n}. ")
    num_run.bold = False
    add_runs(p, text)
    return p


def code_block(doc, text):
    # Code blocks are transparent to numbering: a numbered step followed
    # by its example command should flow into the next numbered step
    # without resetting the counter.
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


# ---------- content ----------------------------------------------------------

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

    # ---------------- Title ----------------
    doc.add_heading("Claude for Dummies", level=0)
    para(doc, "A Source-to-Pay quick start.", italic=True, size=14)
    para(
        doc,
        "Adapted for S2P professionals from Ruben Sosa, "
        '"Claude for Dummies" '
        "(https://ruben.substack.com/p/claude-for-dummies). "
        "Every example below is procurement.",
        italic=True,
    )

    # ---------------- 1. Why this guide exists ----------------
    heading(doc, "1. Why this guide exists", 1)
    para(
        doc,
        "You are a sourcing manager, a category manager, a buyer, a "
        "contract manager, an AP lead, or a procurement analyst. You "
        "spend most of your day in Word, Excel, Outlook, SharePoint, "
        "and an ERP or S2P suite. People keep telling you to try "
        "Claude. This guide tells you, in plain language, what Claude "
        "is, the three places you can run it, what to do in each one, "
        "and the exact prompts to type for real S2P jobs.",
    )
    para(doc, "No code. No jargon. No marketing.")

    # ---------------- 2. What Claude is ----------------
    heading(doc, "2. What Claude is, in 90 seconds", 1)
    para(
        doc,
        "Claude is an AI made by a company called Anthropic. You type "
        "at it, paste files into it, or point it at a folder. It types "
        "back, edits files, and produces outputs.",
    )
    para(doc, "Three things to know about how it behaves:")
    numbered(
        doc,
        "**It predicts the next word.** That is why it sounds confident "
        "even when it is wrong. Sounding right and being right are not "
        "the same thing.",
    )
    numbered(
        doc,
        "**It tries to please you.** If you state something false, "
        "Claude will often agree with it. Read its answers the way you "
        "read a junior analyst's first draft: useful, often right, "
        "sometimes wrong.",
    )
    numbered(
        doc,
        "**It works in tokens.** A token is roughly one word. Long "
        "chats fill up. When it starts forgetting, open a fresh chat.",
    )

    # ---------------- 3. Plans and pricing ----------------
    heading(doc, "3. Plans and pricing", 1)
    para(doc, "Three tiers. Pick based on how often you actually open it.")
    fill_table(
        doc,
        ["Plan", "Cost", "Use when"],
        [
            ("Free", "$0",
             "You are still deciding. Browser only. Daily message limit."),
            ("Pro", "$20 / month",
             "You reach for it three times a week or more. Unlocks the "
             "desktop app, Claude Code, and the better model."),
            ("Max", "$100 to $200 / month",
             "Pro is not enough. You run multi-hour jobs every day."),
        ],
    )
    para(doc, "Three rules of thumb for S2P:")
    numbered(doc, "**Pay monthly, not annually.** Test for 30 days. If you "
                  "have not opened Claude by week three, cancel.")
    numbered(doc, "**Skip Free for serious work.** A free-tier prompt to "
                  "redline an MSA is a waste of your evening.")
    numbered(doc, "**Start at Pro.** Move to Max only when Pro hits its limits.")

    # ---------------- 4. Which Claude do I open? ----------------
    heading(doc, "4. Three places you can run Claude", 1)
    para(
        doc,
        "Same Claude, three places. Pick the one that matches the job. "
        "Sections 5, 6, and 7 cover each in detail, with worked examples.",
    )
    fill_table(
        doc,
        ["Where", "What it looks like", "Best for"],
        [
            ("Claude AI Web (claude.ai)", "A website in your browser.",
             "Quick one-off jobs. A four-line email. A summary of one "
             "contract you upload. Sense-checking a single clause."),
            ("Claude Desktop with Cowork",
             "An app on your Mac or Windows laptop.",
             "Real file work. Building a scorecard from an Excel "
             "export. Reconciling a folder of invoices. Refreshing an "
             "RFP and saving a clean draft."),
            ("Claude Code",
             "A terminal (black command-line window) on your laptop.",
             "Repeatable folder workflows. Bulk reviews of 24 NDAs. "
             "Building supplier onboarding packs from templates."),
        ],
    )
    para(
        doc,
        "**A quick map of common S2P jobs to the right Claude:**",
    )
    fill_table(
        doc,
        ["Task", "Best Claude"],
        [
            ("One-off email to a supplier", "Web"),
            ("Sense-check a clause before signing", "Web"),
            ("Summarise a single contract you can upload", "Web"),
            ("Build a scorecard from an Excel KPI export",
             "Desktop with Cowork"),
            ("Reconcile a folder of invoices", "Desktop with Cowork"),
            ("Refresh an RFP with a new scope and supplier list",
             "Desktop with Cowork or Code"),
            ("Bulk review 24 NDAs in a folder", "Code"),
            ("Build a supplier onboarding pack from templates", "Code"),
            ("Set up a repeatable category workflow", "Code"),
        ],
    )

    # ---------------- 5. Claude AI Web ----------------
    heading(doc, "5. Claude AI Web (claude.ai)", 1)
    heading(doc, "What it is", 2)
    para(
        doc,
        "A website. You go to claude.ai in any browser (Chrome, Edge, "
        "Safari), sign in with your email, and you are typing at Claude. "
        "Nothing to install.",
    )
    heading(doc, "When to use it", 2)
    bullet(doc, "A four-line email to a supplier.")
    bullet(doc, "A summary of a contract or RFP response you can paste or upload.")
    bullet(doc, "A what-is-wrong-with-this-clause check.")
    bullet(doc, "A first-pass rewrite of a paragraph or a memo.")

    heading(doc, "When not to use it", 2)
    para(
        doc,
        "Anything that needs Claude to touch many files at once, or to "
        "remember context between sessions. For that, use the desktop "
        "app or Claude Code.",
    )

    heading(doc, "How to start", 2)
    numbered(doc, "Open https://claude.ai in a browser.")
    numbered(doc, "Sign up with your email. (Use a personal email if your IT has not approved Claude.)")
    numbered(doc, "You land on a chat window. The text box is at the bottom.")
    numbered(doc, "Type a prompt. Hit enter.")
    numbered(
        doc,
        "To upload a file (Word, PDF, Excel, image), click the paperclip "
        "icon next to the text box, pick the file, then type the prompt.",
    )
    numbered(
        doc,
        "Turn on web search by clicking the **+** button in the prompt "
        "bar. The button turns blue when search is on. Use this for any "
        "current question (market prices, supplier news, exchange rates).",
    )

    heading(doc, "Example 1. Draft a chase email to a late supplier", 2)
    para(doc, "Type this into the chat box:")
    code_block(
        doc,
        "Write a four-sentence email to John Smith at Northwind Office Ltd.\n"
        "Subject: PO 4502 update.\n"
        "- We placed PO 4502 on 2026-04-01 for 2,400 reams of paper.\n"
        "- The confirmed delivery date was 2026-04-22.\n"
        "- Today is 2026-04-25 and we have not received the goods.\n"
        "- Ask for a new firm delivery date by close of business tomorrow.\n"
        "Tone: firm, no threats.\n"
        "Sign off as Sambit, Procurement, Acme Plc.",
    )
    para(
        doc,
        "**What you should see.** A four-sentence draft, ready to paste "
        "into Outlook. Check the dates and the PO number before you send.",
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Read your prompt and pulled out the four facts: PO 4502, the order date, the confirmed delivery date, and today's date.")
    numbered(doc, "Worked out the gap (today is three days past the confirmed delivery date) and used that as the lead sentence.")
    numbered(doc, "Wrote one sentence per fact, kept the tone firm but not threatening because that is what you asked for.")
    numbered(doc, "Closed with the explicit ask (a new firm date by close of business tomorrow) and your sign-off block.")
    numbered(doc, "Did not invent any new fact. If the PO number or dates are wrong, the email will be wrong; check before sending.")

    heading(doc, "Example 2. Summarise a 60-page MSA", 2)
    para(
        doc,
        "Click the paperclip. Upload "
        "Master_MSA_Acme_Northwind_2024.pdf. Then type:",
    )
    code_block(
        doc,
        "This is the live MSA between Acme Plc (us) and Northwind Office Ltd.\n"
        "Give me a one-page risk summary as a table. For every risk, list:\n"
        "- the clause number,\n"
        "- the page number,\n"
        "- the risk in one sentence,\n"
        "- whether it favours us or Northwind.\n"
        "Order the rows by risk, highest first. Cap the table at 10 rows.",
    )
    para(
        doc,
        "**What you should see.** A 10-row table with clause numbers, "
        "page numbers, plain-English risk descriptions, and which side "
        "the clause favours. Open the PDF and verify three of the "
        "clause numbers before you trust the rest.",
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Read the whole PDF into its working memory: every page, every footnote, every schedule.")
    numbered(doc, "Identified clause boundaries from the numbering pattern (1.1, 1.2, 2.1, ...) and the bold headings.")
    numbered(doc, "Scanned each clause for risk language: limitation of liability, indemnity, termination, IP, warranty, audit rights, governing law.")
    numbered(doc, "Decided which side the clause favours by asking: 'whose obligation does this create, and whose risk does it cap?'.")
    numbered(doc, "Sorted clauses by severity (loss of money or rights ranked above administrative).")
    numbered(doc, "Capped the table at 10 rows because you asked for a one-page summary; the rest are still in the PDF.")

    heading(doc, "Example 3. Sense-check a clause before signing", 2)
    para(doc, "Paste the clause text into the chat. Then type:")
    code_block(
        doc,
        "This clause comes from Northwind's standard MSA. We are the customer.\n"
        "1. Tell me, in plain English, what this clause obliges us to do.\n"
        "2. Tell me what it obliges Northwind to do.\n"
        "3. Flag any one-sided language.\n"
        "4. Suggest a redline that protects us without blowing up the deal.\n"
        "Keep each part to four sentences or fewer.",
    )
    para(
        doc,
        "**What you should see.** A four-part response. The redline is "
        "a starting point, not a final draft. Send it to Legal.",
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Identified the parties from your prompt: you are the customer, Northwind is the supplier.")
    numbered(doc, "Walked the clause sentence by sentence and assigned each obligation to one side.")
    numbered(doc, "Scanned for one-sided phrases ('at supplier's sole discretion', 'without notice', 'no liability').")
    numbered(doc, "Drafted a redline that softens those phrases (adds notice periods, reciprocal duties, or liability caps).")
    numbered(doc, "Kept the redline narrow enough to look like a normal legal counter, not a rewrite that kills the deal.")

    heading(doc, "Limits to remember", 2)
    bullet(doc, "Free tier has a daily message cap. Pro is much higher.")
    bullet(
        doc,
        "Long chats fill up the token window. If Claude starts forgetting "
        "the early part of the conversation, open a new chat and paste "
        "the key context.",
    )
    bullet(
        doc,
        "Anything you paste here goes to Anthropic's servers. Check "
        "your company's data policy before pasting customer or pricing data.",
    )

    # ---------------- 6. Claude Desktop with Cowork ----------------
    heading(doc, "6. Claude Desktop with Cowork", 1)
    heading(doc, "What it is", 2)
    para(
        doc,
        "An app you install on your Mac or Windows laptop. Same login "
        "as the website. The big difference: it can read and write "
        "files on your local disk, including your OneDrive and "
        "SharePoint folders.",
    )
    para(
        doc,
        "**Cowork** is a mode inside the desktop app. You point Claude "
        "at a folder, give it a job, and it works on the files for "
        "minutes or hours while you do something else. It can read, "
        "edit, and create files. It will ask clarifying questions as "
        "it goes.",
    )

    heading(doc, "When to use it", 2)
    bullet(doc, "When the work needs Claude to touch real files in OneDrive or SharePoint.")
    bullet(doc, "When the job needs more than five files (the web upload limit gets in the way).")
    bullet(doc, "When you want to step away while the work runs.")

    heading(doc, "Pricing", 2)
    para(doc, "Pro plan or higher.")

    heading(doc, "How to start", 2)
    numbered(doc, "Sign up at https://claude.ai. Upgrade to Pro.")
    numbered(doc, "Download the desktop app from https://claude.ai/download. Pick the Mac or Windows build.")
    numbered(doc, "Install. Open it. Sign in with the same email you used for the website.")
    numbered(doc, "Top-left menu inside the app: choose Cowork.")
    numbered(doc, 'Drag a folder into the Cowork pane, or click "Add folder".')
    numbered(doc, "Type a prompt that describes the job. Hit run.")
    numbered(doc, "Pause OneDrive sync before you start a multi-file job. Resume after.")

    heading(doc, "Example 1. Build a supplier scorecard from an Excel KPI export", 2)
    para(doc, "Point Cowork at this folder:")
    code_block(
        doc,
        "Supplier_Performance_Q1/\n"
        "├── Master/\n"
        "│   ├── Scorecard_Template.xlsx\n"
        "│   └── KPI_Export_Q1.csv\n"
        "└── Drafts/",
    )
    para(doc, "Type this prompt:")
    code_block(
        doc,
        "Master/ is read-only.\n"
        "Read Master/KPI_Export_Q1.csv. The columns are:\n"
        "Supplier, On_Time_Delivery_Pct, Defect_Rate_Pct, Spend_GBP, Open_Issues.\n"
        "Take the top 10 suppliers by Spend_GBP.\n"
        "Use Master/Scorecard_Template.xlsx as the layout.\n"
        "For each of the 10 suppliers, fill in:\n"
        "- the four KPIs from the CSV,\n"
        "- a RAG status for On_Time_Delivery_Pct (red below 90%, amber 90 to 95%, green 95% and up),\n"
        "- a one-line commentary.\n"
        "Save the result as Drafts/Supplier_Scorecard_Q1_v1.xlsx.\n"
        "Do not change anything in Master/.",
    )
    para(
        doc,
        "**What you should see.** A new file in Drafts/, ten rows "
        "filled in, each RAG cell colour-coded. Open it and verify "
        "the top supplier's numbers against the CSV.",
    )
    para(doc, "**What Cowork did, behind the scenes.**")
    numbered(doc, "Opened Master/KPI_Export_Q1.csv. Read the header row to find which column is which (Supplier, On_Time_Delivery_Pct, Defect_Rate_Pct, Spend_GBP, Open_Issues).")
    numbered(doc, "Sorted every row by Spend_GBP, descending. Took the first 10.")
    numbered(doc, "Opened Master/Scorecard_Template.xlsx, found the placeholder cells (the empty rows under the header), and worked out where each KPI goes.")
    numbered(doc, "For each of the 10 suppliers, copied the four KPI values from the CSV into the matching template cells.")
    numbered(doc, "Compared On_Time_Delivery_Pct against your RAG bands (red below 90, amber 90 to 95, green 95 and up) and wrote the matching colour into a new status column.")
    numbered(doc, "Wrote a one-line commentary based on each supplier's KPI mix (high spend with high defect rate gets 'watch', stable green gets 'on track').")
    numbered(doc, "Saved the result to Drafts/Supplier_Scorecard_Q1_v1.xlsx. Did not touch Master/.")

    heading(doc, "Example 2. Reconcile a folder of messy invoices and draft chase emails", 2)
    para(doc, "Folder:")
    code_block(
        doc,
        "AP_Exceptions_April/\n"
        "├── Master/        (40 invoice PDFs in five different formats)\n"
        "├── Drafts/\n"
        "└── Outputs/",
    )
    para(doc, "Prompt:")
    code_block(
        doc,
        "Master/ is read-only.\n"
        "Read every PDF in Master/. For each invoice extract:\n"
        "- supplier name,\n"
        "- invoice number,\n"
        "- invoice date,\n"
        "- due date,\n"
        "- amount in GBP,\n"
        "- our PO number if present.\n"
        "Save the result as Drafts/AP_Reconciliation.xlsx.\n"
        "Then group invoices by supplier where the due date is older than 2026-04-01.\n"
        "For each of those suppliers, draft a chase email.\n"
        "Save the drafts as separate .docx files in Drafts/Chase_Emails/.\n"
        "Each email: four sentences, polite, name the invoice numbers, ask for confirmation by 2026-05-02.",
    )
    para(
        doc,
        "**What you should see (after about 20 minutes).** One Excel "
        "reconciliation, one folder of draft emails. Spot-check three "
        "invoices against the source PDFs before you trust the rest.",
    )
    para(doc, "**What Cowork did, behind the scenes.**")
    numbered(doc, "Listed every PDF in Master/ (40 files).")
    numbered(doc, "For each PDF, ran OCR if the file was a scan, then looked for the six fields by common patterns: 'Invoice No.', 'Date', 'Due', a currency string, and a 'PO' reference.")
    numbered(doc, "Wrote one row per invoice into Drafts/AP_Reconciliation.xlsx with the six extracted fields.")
    numbered(doc, "Filtered for due_date older than 2026-04-01. Grouped the late invoices by supplier name.")
    numbered(doc, "For each late supplier, drafted a four-sentence chase email naming the specific invoice numbers and asking for confirmation by 2026-05-02.")
    numbered(doc, "Saved each draft as a separate .docx in Drafts/Chase_Emails/, named after the supplier.")
    numbered(doc, "Where it could not read a field with confidence (a smudged scan, an unusual layout), it left the cell blank and added a note in a 'Review needed' column rather than guessing.")

    heading(doc, "Example 3. Refresh an RFP with a new scope", 2)
    para(doc, "Folder:")
    code_block(
        doc,
        "2026-Q2_Office_Supplies_RFP/\n"
        "├── Master/\n"
        "│   ├── Office_Supplies_RFP_Master.docx\n"
        "│   └── Suppliers_Q2.xlsx\n"
        "├── Drafts/\n"
        "└── Outputs/",
    )
    para(doc, "Prompt:")
    code_block(
        doc,
        "Master/ is read-only.\n"
        "Take Master/Office_Supplies_RFP_Master.docx as the source RFP.\n"
        "Replace the Scope section with:\n"
        '- 14 UK sites listed in Master/Suppliers_Q2.xlsx, sheet "Sites",\n'
        "- Annual spend band: GBP 1.2m to GBP 1.5m,\n"
        "- Contract length: 24 months with one 12-month extension.\n"
        'Refresh the supplier shortlist using Master/Suppliers_Q2.xlsx, sheet "Shortlist".\n'
        "Save the result as Drafts/RFP_Q2_v1.docx. Leave Master/ untouched.",
    )
    para(
        doc,
        "**What you should see.** A new file in Drafts/, with the "
        "Scope section rewritten and the supplier list refreshed. "
        "Compare it to the master before sending.",
    )
    para(doc, "**What Cowork did, behind the scenes.**")
    numbered(doc, "Opened Master/Office_Supplies_RFP_Master.docx and walked the document tree to find the heading 'Scope'.")
    numbered(doc, "Read the existing Scope content so it knew what to replace, not what to delete blind.")
    numbered(doc, "Opened Master/Suppliers_Q2.xlsx, sheet 'Sites'. Read the 14 site rows.")
    numbered(doc, "Replaced the Scope section text with the three bullets you specified, formatted in the same Word style as the surrounding paragraphs.")
    numbered(doc, "Found the supplier shortlist section (a heading + table). Cleared the table rows and wrote in the new shortlist from sheet 'Shortlist'.")
    numbered(doc, "Saved as Drafts/RFP_Q2_v1.docx. Confirmed Master/ files were unchanged before reporting done.")

    heading(doc, "Things to know about Cowork", 2)
    bullet(doc, "Pause OneDrive sync before a multi-file job. Resume after.")
    bullet(
        doc,
        "Always set the read-only rule for Master/ in the first prompt. "
        "Master/ never gets touched.",
    )
    bullet(
        doc,
        "Cowork asks clarifying questions. Read them. Sloppy answers "
        "cost you the run.",
    )
    bullet(doc, "Cowork can run for 10 to 60 minutes on big jobs. Walk away. Come back.")

    # ---------------- 7. Claude Code ----------------
    heading(doc, "7. Claude Code (in the terminal)", 1)
    heading(doc, "What it is", 2)
    para(
        doc,
        "Claude running inside a terminal window (a black command-line "
        "window) on your laptop, with full read and write access to "
        "whatever folder you started it in.",
    )

    heading(doc, "When to use it", 2)
    bullet(doc, "Bulk operations across many files in one folder.")
    bullet(doc, "Repeatable workflows you want to run the same way every quarter.")
    bullet(doc, "Jobs where you want a record of every step in the terminal scrollback.")

    heading(doc, "When not to use it", 2)
    para(
        doc,
        "First time on Claude. Use the web or the desktop app first. "
        "Come here once you understand what Claude can do.",
    )

    heading(doc, "Pricing", 2)
    para(doc, "Pro plan or higher.")

    heading(doc, "How to start, on Windows", 2)
    numbered(doc, "Install Node.js (one-off). Go to https://nodejs.org. Pick the LTS version. Click through the installer.")
    numbered(doc, "Open Terminal (or PowerShell).")
    numbered(doc, "Type the install command:")
    code_block(doc, "npm install -g @anthropic-ai/claude-code")
    numbered(doc, "Cd into your project folder, for example:")
    code_block(doc, 'cd "C:\\Categories\\Office_Supplies\\2026-Q2_Office_Supplies_RFP"')
    numbered(doc, "Start Claude:")
    code_block(doc, "claude")
    numbered(doc, "On first run it asks you to sign in. Open the link, approve, come back to the terminal.")

    heading(doc, "How to start, on Mac", 2)
    numbered(doc, "Install Node.js (one-off) from https://nodejs.org. LTS version.")
    numbered(doc, "Open Terminal (Cmd+Space, type Terminal).")
    numbered(doc, "Type the install command:")
    code_block(doc, "npm install -g @anthropic-ai/claude-code")
    numbered(doc, "Cd into your project folder, for example:")
    code_block(doc, 'cd "~/Documents/Categories/Office_Supplies/2026-Q2_Office_Supplies_RFP"')
    numbered(doc, "Start Claude:")
    code_block(doc, "claude")
    numbered(doc, "Sign in when prompted.")

    heading(doc, "Example 1. Bulk review of 24 supplier NDAs", 2)
    para(doc, "Folder:")
    code_block(
        doc,
        "NDA_Review_April/\n"
        "├── Master/        (24 supplier NDAs as PDFs)\n"
        "└── Drafts/",
    )
    para(doc, "Start Claude in the project folder. First prompt:")
    code_block(
        doc,
        "Master/ is read-only. Save all output to Drafts/.\n"
        "For every PDF in Master/, extract:\n"
        "- supplier name,\n"
        "- NDA effective date,\n"
        "- term in months,\n"
        "- governing law,\n"
        "- mutual or one-way,\n"
        "- whether it has an arbitration clause.\n"
        "Save the result as Drafts/NDA_Summary.xlsx with one row per file.\n"
        'For any NDA where the term is more than 36 months OR governing law is not "England and Wales",\n'
        'add a one-line flag in a column called "Review needed".',
    )
    para(
        doc,
        "**What you should see.** An Excel with 24 rows, each "
        "cross-checkable against its source PDF. Cross-check three "
        "rows before you trust the rest.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Listed every PDF file in Master/. Counted 24.")
    numbered(doc, "For each PDF, read the text and looked for six known fields: supplier name (top of page), effective date (after 'Effective' or near 'dated'), term (a number followed by 'months' or 'years'), governing law ('governed by the laws of'), mutual or one-way (counted obligations on each side), arbitration (presence of 'arbitration' clause).")
    numbered(doc, "Wrote each result as one row in Drafts/NDA_Summary.xlsx.")
    numbered(doc, "After all 24 rows, applied the flagging rule: term > 36 months OR governing law not 'England and Wales' triggers 'Review needed'.")
    numbered(doc, "Where a field could not be found, left the cell blank rather than guessing, and noted 'Could not extract' in the Review column.")
    numbered(doc, "Wrote nothing to Master/. Quitted cleanly so the terminal log shows the full run for audit.")

    heading(doc, "Example 2. Build a supplier onboarding pack from templates", 2)
    para(doc, "Folder:")
    code_block(
        doc,
        "Onboarding_Globex_2026/\n"
        "├── Master/\n"
        "│   ├── NDA_Template.docx\n"
        "│   ├── Code_of_Conduct.docx\n"
        "│   ├── Bank_Details_Form.docx\n"
        "│   └── W8_W9_Form.pdf\n"
        "├── Globex_Profile.txt\n"
        "└── Drafts/",
    )
    para(doc, "First prompt:")
    code_block(
        doc,
        "Master/ is read-only.\n"
        "Read Globex_Profile.txt for supplier details (legal name, address, primary contact, signing authority).\n"
        "Use the four files in Master/ as templates.\n"
        "For each template, replace placeholders like {SupplierName}, {Address}, {ContactName}, {Date} using the profile.\n"
        "Today is 2026-04-25.\n"
        "Combine all four filled-in documents into one PDF: Drafts/Onboarding_Pack_Globex.pdf.\n"
        "Leave Master/ untouched.",
    )
    para(
        doc,
        "**What you should see.** One PDF in Drafts/, four templates "
        "filled in, ready to email to Globex's procurement contact.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Read Globex_Profile.txt and parsed the supplier details into key-value pairs: legal name, address, primary contact, signing authority.")
    numbered(doc, "Opened each of the four templates in Master/ in turn. Scanned each one for placeholder tokens like {SupplierName}, {Address}, {ContactName}, {Date}.")
    numbered(doc, "Substituted each placeholder with the matching value from the profile, using today's date (2026-04-25) for {Date}.")
    numbered(doc, "Saved each filled template into Drafts/ as an interim file (so you have the individual documents if Legal asks).")
    numbered(doc, "Combined the four documents into one PDF using the standard merge tool, in the order you would normally bind them: NDA, Code of Conduct, Bank Details, W-8/W-9.")
    numbered(doc, "Saved the combined file as Drafts/Onboarding_Pack_Globex.pdf. Master/ untouched.")

    heading(doc, "Example 3. Renewal brief from a live contract", 2)
    para(doc, "Folder:")
    code_block(
        doc,
        "Renewal_Q2/\n"
        "├── Master/\n"
        "│   └── Contract_Northwind_Live.docx\n"
        "├── Templates/\n"
        "│   └── Renewal_Brief_Template.docx\n"
        "└── Drafts/",
    )
    para(doc, "First prompt:")
    code_block(
        doc,
        "Master/ is read-only.\n"
        "Use Master/Contract_Northwind_Live.docx as the source.\n"
        "Pull:\n"
        "- annual contract value,\n"
        "- end date,\n"
        "- notice period,\n"
        "- auto-renewal clause text,\n"
        "- price index clause text.\n"
        "Drop those into Templates/Renewal_Brief_Template.docx where placeholders match.\n"
        "Save as Drafts/Renewal_Brief_Northwind_2026.docx.\n"
        'Today is 2026-04-25; flag whether the notice deadline has already passed in a line at the top of the brief called "Notice deadline status".',
    )
    para(
        doc,
        "**What you should see.** A renewal brief in Drafts/, with the "
        "five fields filled in and a clear notice deadline status line "
        "near the top.",
    )
    para(doc, "**What Claude Code did, behind the scenes.**")
    numbered(doc, "Opened Master/Contract_Northwind_Live.docx and read it end to end.")
    numbered(doc, "Searched for the five fields by language pattern: a currency string near 'value' or 'fees' (annual contract value), a date near 'expires' or 'term' (end date), a clause containing 'notice' (notice period), a clause containing 'renew' or 'auto-renew' (auto-renewal text), a clause containing 'index', 'RPI', or 'CPI' (price index text).")
    numbered(doc, "Opened Templates/Renewal_Brief_Template.docx and matched each field to its placeholder.")
    numbered(doc, "Wrote the values in. For long clauses (auto-renewal, price index), kept the original wording verbatim so you can quote it back.")
    numbered(doc, "Computed the notice deadline as end_date minus notice_period, compared against today (2026-04-25), and added a one-line status at the top: 'Notice deadline: not yet passed' or 'Notice deadline: PASSED on YYYY-MM-DD'.")
    numbered(doc, "Saved as Drafts/Renewal_Brief_Northwind_2026.docx. Master/ untouched.")

    heading(doc, "Things to know about Claude Code", 2)
    bullet(doc, "Folder discipline matters more here than anywhere else. See Folder_Structure.md in the course folder.")
    bullet(doc, "Always set the read-only rule for Master/ in the first prompt of the session.")
    bullet(doc, "Quit Claude with /quit when you are done. The terminal scrollback is your record of the session.")
    bullet(doc, "Save your useful prompts as .md files in a Prompt_Library/ folder so you can re-run them next quarter.")

    # ---------------- 8. How to talk to Claude ----------------
    heading(doc, "8. How to talk to Claude: five rules", 1)
    para(doc, "These five rules apply in all three places.")

    heading(doc, "Rule 1. Be specific", 2)
    bullet(doc, "**Weak.** Write me an email to a supplier.")
    bullet(
        doc,
        "**Strong.** Write a four-sentence email to John Smith at "
        "Northwind Office Ltd. Confirm receipt of their RFP response. "
        "Acknowledge the price drop on item code OS-1042. Ask them to "
        "confirm the lead time of 14 days. Friendly but firm.",
    )

    heading(doc, "Rule 2. Give examples", 2)
    para(
        doc,
        "Claude learns faster from examples than from instructions. If "
        "you want a savings memo in your team's voice, paste two old "
        "memos and say match this voice and this format.",
    )

    heading(doc, "Rule 3. Say what to do, not what not to do", 2)
    bullet(doc, "**Weak.** Don't be too formal.")
    bullet(doc, "**Strong.** Write it like a Teams message to a colleague.")

    heading(doc, "Rule 4. Start short, add detail", 2)
    para(
        doc,
        "A 500-word prompt on the first try wastes your time. Two "
        "sentences first. Look at what comes back. Then say what to fix.",
    )

    heading(doc, "Rule 5. Start a fresh chat when it drifts", 2)
    para(
        doc,
        "After many turns, Claude can lose the thread. If it starts "
        "repeating itself, ignoring instructions, or getting facts "
        "wrong, open a fresh chat and paste the key context. Fresh "
        "chats are free.",
    )

    # ---------------- 9. Good at, bad at ----------------
    heading(doc, "9. What Claude is good at, in S2P", 1)
    para(
        doc,
        "Each capability below names which of the three Claudes is the "
        "right place to do it. \"All three\" means it works the same "
        "way in Web, Desktop with Cowork, and Code.",
    )
    fill_table(
        doc,
        ["Capability", "Best in", "Why"],
        [
            ("First drafts. RFPs, supplier emails, board memos, savings narratives, NDAs, and evaluation criteria.",
             "All three (Web is fastest for one-off drafts).",
             "All three can write. Web wins on a single email because there is no setup. Cowork or Code win when the draft has to read a folder of source files first."),
            ("Reading and summarising a single long contract or RFP (up to ~200 pages).",
             "Web (paperclip upload) or Desktop with Cowork.",
             "Web upload is the simplest path for one document. Use Cowork if the contract sits in a OneDrive folder you do not want to copy out."),
            ("Reading and comparing many contracts at once (10 or more).",
             "Claude Code.",
             "Web caps at five uploads per message. Cowork handles tens. Code handles a folder of any size and gives you a terminal log of every step."),
            ("Voice matching from old samples.",
             "Web.",
             "Paste three old emails or memos into a fresh chat. The next draft comes back in your tone. No file plumbing needed."),
            ("File work on your laptop (Excel + Word + PowerPoint combined into one output).",
             "Desktop with Cowork or Claude Code.",
             "Web cannot edit local files. Cowork is best when the job is one-off. Code is best when you want to re-run the same workflow next quarter."),
            ("Thinking partner: argue the other side, find weak logic.",
             "All three (Web is most natural).",
             "It is a chat task. Web is fine. The same conversation in Cowork or Code works equally well."),
            ("Step-by-step reasoning (why a clause is risky, why a supplier ranks where it does, where a savings figure comes from).",
             "All three.",
             "Pure reasoning, no file plumbing. Use whichever you already have open."),
        ],
    )

    heading(doc, "10. What Claude is bad at, in S2P", 1)
    para(
        doc,
        "Each limitation below applies in **all three** Claudes. The "
        "workaround is sometimes different per Claude, so the row says "
        "where to do the workaround.",
    )
    fill_table(
        doc,
        ["Limitation", "Applies in", "Workaround, and where to do it"],
        [
            ("Real-time information. Claude does not know what happened today unless web search is enabled. It will guess and sound certain.",
             "All three.",
             "In Web: click the + button in the prompt bar; it turns blue when search is on. In Desktop and Code: enable the web-search tool in the settings menu before you start."),
            ("Precise maths. Do not use Claude as a calculator on numbers that matter.",
             "All three.",
             "In Web and Desktop: ask Claude to write the formula and paste it into Excel. In Code: ask Claude to run the calculation in Python and show its working. Better still, do the maths in Excel and ask Claude to check your logic."),
            ("Vague prompts. 'Help me with this RFP' gets nothing useful.",
             "All three.",
             "Be specific in every prompt. Name the input file, the output file, and what to leave alone. Same rule in Web, Desktop, and Code."),
            ("Being a source of truth. Claude sounds authoritative when it is wrong.",
             "All three.",
             "Always verify quoted clause numbers, supplier names, contract values, and dates against the source document. Same rule in Web, Desktop, and Code."),
            ("Image generation. Claude can read images but cannot draw them.",
             "All three.",
             "Use ChatGPT, Microsoft Designer, or a dedicated image tool for the picture. Bring the picture back into Claude if you need it described or annotated."),
        ],
    )

    # ---------------- 11. First week ----------------
    heading(doc, "11. Ten things to try in your first week", 1)
    para(
        doc,
        "Each item below tells you which of the three Claudes to use. "
        "Stick to the one named so you build the right muscle memory.",
    )
    numbered(doc, "**[Web]** Paste three of your last RFPs into Claude AI Web. Ask it to write the next one for a different category in the same voice and structure.")
    numbered(doc, "**[Web]** In Claude AI Web, upload a 60-page MSA via the paperclip. Ask for a one-page risk summary with clause numbers and page references.")
    numbered(doc, "**[Web]** In Claude AI Web, upload five sets of meeting notes from a category review. Ask for a decisions log with owner, action, and due date.")
    numbered(doc, "**[Desktop with Cowork]** In the desktop app, open Cowork. Point it at a category folder. Ask what is in it and what duplicates look like.")
    numbered(doc, "**[Web]** In Claude AI Web, paste a long supplier email thread. Ask for the three open issues, who owns each, and a draft reply.")
    numbered(doc, "**[Web or Cowork]** Upload a supplier scorecard Excel (Web for one quick check, Cowork if you want to update the file in place). Ask for the three suppliers most at risk and why, with the numbers.")
    numbered(doc, "**[Web]** In Claude AI Web, paste a competitor's published price list and your last quote from the same supplier. Ask for a price-by-price comparison and a one-page negotiation brief.")
    numbered(doc, "**[Web]** In Claude AI Web, upload your category strategy in Word. Ask for a sharper rewrite and a list of every claim that needs evidence.")
    numbered(doc, "**[Web]** In Claude AI Web, paste an invoice exception report. Ask for the top three reasons for exceptions, in plain language, and a draft note to the requester for each.")
    numbered(doc, "**[Desktop with Cowork]** Connect your Outlook calendar to Claude Desktop (Connectors menu). Ask which meetings to decline next week and why, and what to prepare for the rest.")
    para(
        doc,
        "**Start a file called Prompts_That_Worked.md.** Every time a "
        "prompt earns its keep, paste it in, with the result. After "
        "two weeks you have a personal library worth more than any course.",
    )

    # ---------------- 12. Cautions ----------------
    heading(doc, "12. Cautions and ground rules", 1)
    bullet(doc, "Verify every figure that goes to a CFO, a board, or a supplier.")
    bullet(
        doc,
        "Never paste customer-identifying or pricing information into "
        "the public Claude site without checking your company's policy. "
        "Use the enterprise instance if your company has one.",
    )
    bullet(doc, "Treat Claude's first draft like a junior analyst's first draft: useful, not finished.")
    bullet(doc, "Save what worked. Drop what did not. Build your own prompt library.")
    bullet(doc, "When in doubt, start a fresh chat.")
    para(
        doc,
        "That is enough to get going. Open the browser. Type a real "
        "question. See what comes back.",
    )

    doc.save(str(OUTPUT_PATH))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
