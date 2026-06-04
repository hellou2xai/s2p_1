"""Build the Course 3: The Skill Builder e-learning handout.

Companion document for Course 3. Same structure as the Course 2 handout:
day-to-day scenario, time savings, mental model, worked example,
day in the life, 20-minute sprint, first week, troubleshooting.

Style follows CLAUDE.md: no em-dashes, Oxford commas, British English,
no banned phrases, four-part rule on every worked example.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt


OUTPUT_PATH = Path(
    r"C:\Users\sambi\OneDrive - U2xAI\Claude Code Projects"
    r"\S2p Training\Course List\Claude Code Foundation for S2P"
    r"\Handouts\Course_03_The_Skill_Builder_Handout.docx"
)


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

    # Cover
    para(doc, "U2xAI", italic=True, size=12)
    para(doc, "PROCUREAI ACADEMY", italic=True, size=10)
    para(doc, "Series 2 (Engineering Track) | Course 3", italic=True)
    doc.add_heading("The Skill Builder", level=0)
    para(doc, "Reusable methodologies for sourcing events, captured as SKILL.md files.", italic=True, size=14)
    para(doc, "Four hours. Six lessons. No coding. Real bid data with 25 carriers, 1,500 historical shipments, and six full bid responses.", italic=True)
    para(doc, "Use this handout alongside the course folder at "
         "Detailed Course Content/Course_03_The_Skill_Builder/.", italic=True)

    # 1
    heading(doc, "1. How to use this handout", 1)
    para(doc, "This handout is your reading companion. The hands-on work happens "
         "in the course folder you got with this guide. The folder has the data, "
         "the starter files, the six lessons, and the reference answers.")
    para(doc, "How to read this guide:")
    numbered(doc, "Read sections 2 and 3 to understand what the course is and what you end up with.")
    numbered(doc, "Read section 4 to see what the course saves you per sourcing event.")
    numbered(doc, "Read section 5 for the mental model of what a SKILL.md is.")
    numbered(doc, "Open the course folder and start Lesson 1.")
    numbered(doc, "Come back to this handout when you want context (sections 6 to 8 are useful while you work).")
    numbered(doc, "Use section 11 (troubleshooting) if something does not look right.")

    # 2
    heading(doc, "2. What this course teaches", 1)
    para(doc, "Every sourcing event you run produces the same artefacts: an RFP "
         "package, a bid scorecard, a risk profile, a savings case, an award memo. "
         "Most procurement teams write each one from scratch every time, taking "
         "two to three weeks per event.")
    para(doc, "This course teaches you to capture each artefact as a **SKILL.md** "
         "file: a methodology Claude can re-run any number of times, with "
         "different inputs, producing consistent output.")
    para(doc, "You write five skills:")
    bullet(doc, "**rfp-builder.md** - the RFP package methodology.")
    bullet(doc, "**bid-scorer.md** - the weighted scoring methodology.")
    bullet(doc, "**risk-profiler.md** - the supplier risk assessment framework.")
    bullet(doc, "**savings-calculator.md** - the savings methodology.")
    bullet(doc, "**award-memo.md** - the recommendation memo structure.")
    para(doc, "Then you chain them together: one Claude session, five skills run "
         "in order, six deliverables produced. The next sourcing event uses the "
         "same five skills with new inputs.")

    # 3
    heading(doc, "3. What is in the course folder", 1)
    para(doc, "Open the course folder before you start. Everything is inside, "
         "in a flat structure (no nested data folders deeper than three levels).")
    code_block(
        doc,
        "Course_03_The_Skill_Builder/\n"
        "├── README.md                       (start here)\n"
        "├── COURSE_OVERVIEW.md              (the story)\n"
        "├── lessons/                        (six lessons in order)\n"
        "├── practice/                       (your hands-on workspace)\n"
        "│   ├── CLAUDE.md                   (project context)\n"
        "│   ├── inputs/\n"
        "│   │   ├── category-brief.md\n"
        "│   │   ├── supplier-longlist.csv  (25 carriers)\n"
        "│   │   └── spend-baseline.csv     (~1,500 shipments)\n"
        "│   ├── bid-responses/             (6 bid response files)\n"
        "│   ├── templates/                 (RFP, scorecard, memo skeletons)\n"
        "│   ├── skills/                    (you fill this folder)\n"
        "│   └── outputs/                   (deliverables land here)\n"
        "├── solutions/                      (5 reference SKILL.md files)\n"
        "└── scripts/build_course_data.py    (regenerates data)"
    )
    para(doc, "Today's date in the practice data is 2026-04-25.")

    # 4
    heading(doc, "4. What the course saves you per sourcing event", 1)
    fill_table(
        doc,
        ["Task per sourcing event", "Without skills", "With your skill library"],
        [
            ("Build the RFP package",
             "5 to 10 days of writing",
             "60 seconds: rfp-builder runs against the brief and longlist"),
            ("Score 6 bids consistently",
             "1 to 2 days of reading and Excel work",
             "90 seconds: bid-scorer applies fixed weights to all bids"),
            ("Build the supplier risk profile",
             "Half a day of analyst time",
             "60 seconds: risk-profiler runs against the longlist and bids"),
            ("Compute the savings case",
             "Half a day in Excel against historical spend",
             "60 seconds: savings-calculator sums baseline and proposed spend"),
            ("Write the award memo",
             "Half a day of synthesis",
             "60 seconds: award-memo reads the four other outputs"),
            ("Run the next event",
             "Repeat all the above. 2 to 3 weeks.",
             "Configure new inputs, run the chain, 7 minutes."),
        ],
    )

    # 5
    heading(doc, "5. What a SKILL.md actually is", 1)
    para(doc, "A SKILL.md is a 40 to 90 line markdown file with five sections:")
    fill_table(
        doc,
        ["Section", "What goes in it"],
        [
            ("**What this skill does**",
             "One paragraph in plain English. Use case, audience, when to invoke."),
            ("**Inputs**",
             "The shape of every input. Path, column headers (CSV), or section structure (markdown). Not specific values."),
            ("**Process**",
             "Six to twelve numbered steps in plain English. No code. Names input shapes, not specific suppliers."),
            ("**Output format**",
             "The path, structure, and length of the file the skill produces."),
            ("**Quality criteria**",
             "Three to five checks the skill (or you) can run on the output."),
        ],
    )
    para(doc, "**A skill versus a prompt:** a prompt names specific files (`Master/RFP_v3.docx`); a skill names input shapes (`a category brief in markdown with these sections`). The shape is what makes the skill reusable.")

    # 6
    heading(doc, "6. Worked example: the bid-scorer skill", 1)
    para(doc, "The bid-scorer skill is the most data-rigorous of the five. It "
         "reads six bid response markdown files, scores each on five weighted "
         "criteria, and ranks them. Same methodology applied to every bid; no "
         "human inconsistency.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "practice/\n"
        "├── skills/bid-scorer.md            (your skill, 80 lines)\n"
        "├── bid-responses/                  (6 bid response files)\n"
        "│   ├── BID_CAR001_FastRoad_UK.md\n"
        "│   ├── BID_CAR003_OceanLine.md\n"
        "│   ├── BID_CAR008_Pacific_Forwarders.md\n"
        "│   ├── BID_CAR010_Globex_Freight.md\n"
        "│   ├── BID_CAR012_Helios_Air_Freight.md\n"
        "│   └── BID_CAR017_Continental_Roads.md\n"
        "├── inputs/supplier-longlist.csv    (25 carriers, capability data)\n"
        "├── templates/scorecard-template.md\n"
        "└── outputs/bid-comparison.md       (the output)"
    )
    para(doc, "**The exact prompt to type after starting Claude in `practice/`:**")
    code_block(
        doc,
        "Use the bid-scorer skill in skills/bid-scorer.md.\n"
        "Process every file in bid-responses/.\n"
        "Use inputs/supplier-longlist.csv for capacity_tier, financial_health,\n"
        "and incumbent lookups.\n"
        "Save the output to outputs/bid-comparison.md."
    )
    para(doc, "**What you should see (after 90 to 120 seconds).** A markdown "
         "file at outputs/bid-comparison.md with three sections: a comparison "
         "table (8 columns, 6 rows sorted by Total descending), one paragraph "
         "of commentary per bidder, and a top-three summary. Continental Roads "
         "leads on Price (98). FastRoad UK leads on Capability (94). Helios Air "
         "Freight leads on Service (97). The audit footer at the bottom names "
         "the source files used.")
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Loaded the global CLAUDE.md from practice/ and read the bid-scorer skill from skills/.")
    numbered(doc, "Listed every file in bid-responses/. Counted six.")
    numbered(doc, "For each bid, read the executive summary, capability statement, pricing table, and service commitments.")
    numbered(doc, "Looked up each carrier_id in supplier-longlist.csv to pull capacity_tier, financial_health, and incumbent flag.")
    numbered(doc, "Scored each bid on Price (40%), Service (25%), Capability (20%), Sustainability (10%), Implementation (5%) using the bands the skill specified.")
    numbered(doc, "Computed the weighted total to one decimal place. Sorted descending.")
    numbered(doc, "Wrote the table, the per-bidder commentary, and the top-three summary. Added the audit footer.")

    # 7
    heading(doc, "7. A day in the life: Anwar works through the course", 1)
    para(doc, "This section follows Anwar, a Strategic Sourcing Lead at a UK "
         "manufacturer. He has Course 1 and Course 2 finished. He sets aside "
         "Tuesday and Wednesday afternoons for Course 3.")

    heading(doc, "13:00 Tuesday. Lesson 1: see a skill in action", 2)
    para(doc, "Anwar copies the rfp-builder solution into his skills folder, "
         "starts Claude, and runs the skill. In 90 seconds he has a populated "
         "RFP package in outputs/. He reads it. The executive overview names "
         "the 1.6m GBP savings target and the 2026-06-30 award date. The "
         "evaluation criteria are 40/25/20/10/5. He thinks: \"This is what I "
         "spent two weeks writing on the last RFP.\"")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "practice/\n"
        "├── skills/rfp-builder.md           (Anwar copied from solutions)\n"
        "├── inputs/                          (category brief, longlist, baseline)\n"
        "└── outputs/rfp-package.md           (Claude produced this)"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Loaded the practice CLAUDE.md and the rfp-builder skill.")
    numbered(doc, "Read inputs/category-brief.md for today's date, savings target, and scope.")
    numbered(doc, "Read inputs/supplier-longlist.csv (25 carriers) to ground the response template.")
    numbered(doc, "Read templates/rfp-template.md for the six-section structure.")
    numbered(doc, "Wrote the populated RFP package to outputs/rfp-package.md, applying the writing rules from the global CLAUDE.md.")

    heading(doc, "13:30 Tuesday. Lesson 2: take a skill apart", 2)
    para(doc, "Anwar dissects the rfp-builder skill section by section. He "
         "writes a tiny `list-incumbents` skill (12 lines) and runs it. Claude "
         "filters the longlist for incumbent=yes and prints a table of 9 carriers. "
         "Anwar can now write his own skills.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "practice/\n"
        "└── skills/list-incumbents.md       (Anwar's first own skill, 12 lines)"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Read the list-incumbents skill (12 lines).")
    numbered(doc, "Opened supplier-longlist.csv. Filtered rows where incumbent = yes.")
    numbered(doc, "Sorted by carrier_id. Output a five-column table to the chat.")
    numbered(doc, "Did not save a file (the skill said to print to chat).")

    heading(doc, "14:00 Tuesday. Lesson 3: write rfp-builder from scratch", 2)
    para(doc, "Anwar deletes the rfp-builder he copied. He writes his own "
         "from a blank file, one section at a time. By 15:00 his skill is 65 "
         "lines and produces a fresh RFP package. He runs the quality criteria "
         "check from the skill. Four of five pass; the timeline section was "
         "missing the Q&A close date. He tightens the Process section, re-runs, "
         "all five pass.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "practice/\n"
        "├── skills/rfp-builder.md           (Anwar's own version, 65 lines)\n"
        "└── outputs/rfp-package.md           (re-generated)"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Loaded Anwar's new rfp-builder skill (different from the solution but with the same five sections).")
    numbered(doc, "Followed the nine process steps: read brief, group longlist by mode, write each of the six RFP sections.")
    numbered(doc, "Saved a fresh outputs/rfp-package.md.")
    numbered(doc, "On the second run with the timeline fix, ran the quality criteria check; all five passed.")

    heading(doc, "(End of Tuesday afternoon. Anwar comes back Wednesday.)", 2)
    para(doc, "")

    heading(doc, "13:30 Wednesday. Lesson 4: bid-scorer on six real bids", 2)
    para(doc, "Six bid responses landed yesterday. Anwar writes bid-scorer (80 "
         "lines, with explicit numeric scoring bands). He runs it. In 90 seconds "
         "Claude produces a comparison table with the six bidders ranked. "
         "Continental Roads first (lowest price), FastRoad UK second, Globex "
         "Freight third. Helios Air wins the air-only category. Anwar reads "
         "each commentary and confirms each one names the strongest and weakest "
         "score for that bidder.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "practice/\n"
        "├── skills/bid-scorer.md            (Anwar's 80-line skill)\n"
        "├── bid-responses/                  (6 bid files)\n"
        "└── outputs/bid-comparison.md       (the table and commentary)"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Loaded the bid-scorer skill.")
    numbered(doc, "Listed bid-responses/. Found six files.")
    numbered(doc, "For each file, parsed executive summary, pricing table, service commitments. Looked up the carrier_id in supplier-longlist.csv for capability scoring inputs.")
    numbered(doc, "Applied the numeric scoring bands from the Process section.")
    numbered(doc, "Computed weighted totals, sorted, marked top-three Recommended.")
    numbered(doc, "Wrote per-bidder commentary, each naming the strongest and weakest score.")
    numbered(doc, "Saved the file with audit footer.")

    heading(doc, "14:30 Wednesday. Lesson 5: chain five skills", 2)
    para(doc, "Anwar writes risk-profiler (35 lines), savings-calculator (45 "
         "lines), and award-memo (55 lines). He runs the full chain in one "
         "session. Claude executes the five skills in order. Each step reads "
         "the previous outputs as inputs. Total elapsed: 7 minutes for 6 "
         "deliverables. Anwar walks into a hypothetical 10:00 panel meeting "
         "with the package complete.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "practice/\n"
        "├── skills/                          (5 skills now)\n"
        "└── outputs/                         (6 deliverables)\n"
        "    ├── rfp-package.md\n"
        "    ├── bid-comparison.md\n"
        "    ├── risk-profile.md\n"
        "    ├── savings-case.md\n"
        "    └── award-memo.md"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Step 1: ran rfp-builder. Output: outputs/rfp-package.md.")
    numbered(doc, "Step 2: ran bid-scorer. Output: outputs/bid-comparison.md.")
    numbered(doc, "Step 3: ran risk-profiler. Read bids and longlist; output one paragraph per bidder.")
    numbered(doc, "Step 4: ran savings-calculator. Summed 1,500 shipment rows for baseline (10.86m GBP). Read bid-comparison for proposed annual values. Computed savings (around 1.55m GBP, 14.3% off baseline).")
    numbered(doc, "Step 5: ran award-memo. Read all four prior outputs plus the brief. Drafted the four-carrier panel recommendation, named three risks with mitigations, quoted the savings figure verbatim from savings-case.md.")
    numbered(doc, "Each step ran the skill's own quality criteria after writing the output.")

    heading(doc, "16:30 Wednesday. Lesson 6: version a skill safely", 2)
    para(doc, "The CFO has tightened the soft-savings rule. Anwar updates "
         "savings-calculator to v1.1, adds a soft-savings supplemental rule, "
         "re-runs only that skill plus the downstream award-memo. He adds a "
         "two-line changelog to skills/README.md so the next person to run "
         "the chain knows the rule changed.")
    para(doc, "**Folder layout for this scenario.**")
    code_block(
        doc,
        "practice/\n"
        "├── skills/savings-calculator.md    (v1.1 update with soft-savings rule)\n"
        "└── skills/README.md                 (changelog entry added)"
    )
    para(doc, "**What Claude did, behind the scenes.**")
    numbered(doc, "Loaded the v1.1 savings-calculator. Recomputed the savings case with the new rule.")
    numbered(doc, "Re-ran award-memo, which now quotes the new headline (hard savings only).")
    numbered(doc, "Did not run the other three skills. They are unaffected.")

    # 8
    heading(doc, "8. The 20-minute sprint: a quick taste", 1)
    para(doc, "If you have only 20 minutes, do this. You will not finish "
         "Course 3 but you will see one skill produce one real deliverable.")

    heading(doc, "Minutes 0 to 5: open the practice folder", 2)
    numbered(doc, "Open your terminal.")
    numbered(doc, "Type:")
    code_block(doc, 'cd "Course_03_The_Skill_Builder/practice"\nls')
    numbered(doc, "You should see CLAUDE.md, bid-responses/, inputs/, outputs/, skills/, templates/. Skim each folder briefly.")

    heading(doc, "Minutes 5 to 10: copy the rfp-builder solution", 2)
    numbered(doc, "Copy the reference skill into your practice folder:")
    code_block(doc, "cp ../solutions/rfp_builder_solution.md skills/rfp-builder.md")
    numbered(doc, "Open skills/rfp-builder.md and read it. About 65 lines, five sections.")

    heading(doc, "Minutes 10 to 15: run the skill", 2)
    numbered(doc, "Start Claude:")
    code_block(doc, "claude")
    numbered(doc, "Type:")
    code_block(
        doc,
        "Use the rfp-builder skill in skills/rfp-builder.md. Inputs in\n"
        "inputs/. Templates in templates/. Save to outputs/rfp-package.md."
    )
    numbered(doc, "Wait 60 to 90 seconds.")

    heading(doc, "Minutes 15 to 20: read the result", 2)
    numbered(doc, "Quit Claude (`/quit`).")
    numbered(doc, "Open outputs/rfp-package.md. Read the executive overview. It should name the 1.6m GBP savings target.")
    numbered(doc, "Read Section 5 (Supplier response template). It should list the same fields the bidders responded against.")

    para(doc, "After this sprint you have proven a SKILL.md works on real "
         "procurement data. Lessons 2 to 5 teach you to write your own.")

    # 9
    heading(doc, "9. Your first week with skills in your real work", 1)
    heading(doc, "Day 1 (Monday): copy your first real skill", 2)
    bullet(doc, "Goal: rfp-builder running on your real next sourcing event.")
    bullet(doc, "Tasks: copy your practice rfp-builder.md into your real procurement folder. Edit the inputs section to point at your real category brief and your real supplier longlist. Run.")
    bullet(doc, "Time: 30 minutes.")

    heading(doc, "Day 2 (Tuesday): bid-scorer on your last sourcing event", 2)
    bullet(doc, "Goal: the bid-scorer skill scores your last sourcing event's bids.")
    bullet(doc, "Tasks: copy bid-scorer.md. Drop your last sourcing event's bid responses into a folder. Run.")
    bullet(doc, "Time: 60 minutes.")

    heading(doc, "Day 3 (Wednesday): risk-profiler and savings-calculator", 2)
    bullet(doc, "Goal: both skills running against the same data.")
    bullet(doc, "Tasks: copy both skills. Configure the inputs sections for your data files. Run each. Compare outputs against your manual analysis.")
    bullet(doc, "Time: 60 minutes.")

    heading(doc, "Day 4 (Thursday): award-memo and the first chain run", 2)
    bullet(doc, "Goal: the full chain produces a complete sourcing event package.")
    bullet(doc, "Tasks: copy award-memo.md. Run the full chain on your last sourcing event. Compare the chain output against the memo you actually sent.")
    bullet(doc, "Time: 90 minutes.")

    heading(doc, "Day 5 (Friday): show your team and start versioning", 2)
    bullet(doc, "Goal: the skill library belongs to your team, not just to you.")
    bullet(doc, "Tasks: commit your skills folder to your team's shared procurement repository or SharePoint. Add a changelog entry. Walk one colleague through running the chain on a hypothetical new event.")
    bullet(doc, "Time: 90 minutes.")

    # 10
    heading(doc, "10. The pattern: write methodology once, reuse forever", 1)
    para(doc, "What you build in Course 3 is your team's shared methodology library.")
    bullet(doc, "Each SKILL.md is small (40 to 90 lines) and focused on one job.")
    bullet(doc, "The skill names input shapes, not specific values, so it works across categories and events.")
    bullet(doc, "Skills compose: the output of one becomes the input of another. The chain is the sourcing event.")
    bullet(doc, "Versioning is a discipline: comment the version at the top, run the practice chain after every change, write a changelog entry.")
    para(doc, "Future courses build on this. Course 4 (custom slash commands) "
         "wraps your most-used skill chains in single-word commands. Course 5 "
         "(sub-agents) parallelises skill execution across many bidders or "
         "categories at once.")

    # 11
    heading(doc, "11. Quick reference and troubleshooting", 1)
    heading(doc, "Things to remember", 2)
    bullet(doc, "A skill names input shapes, not specific values. If your skill says 'Forge Steel UK' or '11.2m GBP', it is a prompt, not a skill.")
    bullet(doc, "Every skill has the same five sections. Five lines for what it does, then inputs, process, output format, quality criteria.")
    bullet(doc, "The chain runs in order. Every step's output is the next step's input. If step N fails, do not run step N+1 until step N is fixed.")
    bullet(doc, "Version your skills. v1.0, v1.1, with a date and a one-line reason. Future you will thank present you.")

    heading(doc, "Common problems and the matching fix", 2)
    bullet(doc, "**Symptom:** Claude returns a generic answer ignoring your skill. **Fix:** the skill is not being loaded. Check the file path and that the file is at practice/skills/<name>.md.")
    bullet(doc, "**Symptom:** the skill works on Acme bids but fails on a new event. **Fix:** the skill probably has Acme-specific values embedded. Search for any number or name from Acme's data and remove it.")
    bullet(doc, "**Symptom:** the skill output passes some quality criteria but not all. **Fix:** the Process section is missing a step. Look at the failed criterion and add the matching process step.")
    bullet(doc, "**Symptom:** the chain stops at step 3. **Fix:** step 2 produced output that step 3 cannot consume. Re-run step 2, confirm it passes its quality criteria, then re-run step 3.")
    bullet(doc, "**Symptom:** two analysts produce different scores from the same skill. **Fix:** the scoring bands are not numeric enough. Replace 'medium' and 'high' with 60-74, 75-89, 90-100.")
    bullet(doc, "**Symptom:** the award memo savings figure does not match the savings case. **Fix:** the award-memo skill is recomputing instead of quoting. Add a quality criterion that says 'savings figure quoted from savings-case.md'.")

    # 12
    heading(doc, "12. You are done with Course 3 when", 1)
    numbered(doc, "Five SKILL.md files in your practice/skills/ folder, between 40 and 90 lines each.")
    numbered(doc, "The full chain runs end to end and produces six deliverables in practice/outputs/.")
    numbered(doc, "The award memo recommends a four-carrier panel covering road FTL, road LTL or pallet, sea FCL, and air.")
    numbered(doc, "The savings case shows a saving close to the 1.6m GBP target.")
    numbered(doc, "You can copy your skills folder into your real procurement project and run the next event.")
    numbered(doc, "Move to Course 4 (The Command Engineer) when you are ready; it wraps your most-used chains in one-word slash commands.")

    doc.save(str(OUTPUT_PATH))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
