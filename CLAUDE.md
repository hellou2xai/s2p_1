# Claude Code Foundation for Source-to-Pay (S2P) Professionals

This file is the style and structure guide for every lesson, handout, exercise, and example produced for this course. Follow it. If a piece of content does not match this guide, rewrite it.

## Reference files

When drafting course material, open the relevant reference file as well:

- `docs/Lesson_Template.md`. The full worked RFP example, the six-part structure in detail, screenshot rules, and file naming conventions. Open this when drafting or reviewing any lesson.
- `docs/Use_Cases.md`. The catalog of S2P documents to build lessons around. Open this when picking the next lesson topic.
- `docs/Prompt_Library.md`. Reusable prompt patterns and rules for writing new prompts. Open this when writing a new prompt for the course.
- `docs/Folder_Structure.md`. The standard project folder layout, naming rules, and OneDrive/SharePoint guidance. Open this when setting up a new lesson, engagement, or category folder.

## Pre-flight check (run this before producing any artifact)

Before saving any course artifact (lesson, handout, briefing, exercise sheet, prompt-library entry, slide, screenshot caption, or any other learner-facing file), do these two things in order. Skipping is not optional.

1. **Run the done checklist** at the bottom of this file. Reply to the user with the checklist marked item-by-item: done, deferred, or N/A. The point is to catch structural problems before the file exists, when the fix is cheap.
2. **Then write the file.**

After saving, the `PostToolUse` hook in `.claude/settings.json` runs `scripts/check_style.py` against the file. If it reports any violation, fix the file before moving on. The hook covers `.md`, `.txt`, and `.docx`. For other formats (`.pptx`, `.pdf`, images), run the relevant check by hand.

## Audience

Working S2P professionals: sourcing managers, category managers, contract managers, AP leads, supplier risk managers, and procurement operations staff. Comfortable with Word, Excel, and an ERP. Not software developers. Assume zero coding background. Where a technical word is unavoidable, explain it in brackets the first time, for example "the terminal (the black window where you type commands)".

## Writing rules

These rules apply to every lesson, every screenshot caption, every exercise prompt, every script, every email template, and every commit message in this repo.

### Punctuation

- Do not use em-dashes (`—`) or en-dashes (`–`). Anywhere. Ever.
- Replace them with a full stop, a comma, a colon, brackets, or a plain word like "and", "but", "so", or "because".
- If you are editing existing text and find a dash, rewrite the sentence. Do not swap one dash for another.
- Oxford commas, always. "Suppliers, contracts, and risk." Not "Suppliers, contracts and risk." Apply this in body text, bullets, table cells, table headers, slide titles, captions, and prompts.

### Voice

- Write like a person, not a brochure.
- Short sentences. One idea per sentence. If a sentence has two "and"s, split it.
- Plain words. "Use" not "leverage". "Buy" not "procure" when "buy" fits. "Start" not "kick off". "Set up" not "onboard".
- Specific nouns. "A draft NDA in Word" beats "a contract artifact".
- Contractions are fine (it's, you're, don't, won't).
- American English by default: organize, analyze, behavior, color, center. Use US spelling, US date format (MM/DD/YYYY in prose, YYYY-MM-DD in file names and data), and USD for all currency figures.

### Words and phrases to avoid

- dive into, delve into, unlock, unleash, supercharge, harness, leverage, elevate, empower, revolutionize.
- in today's fast-paced world, in the ever-evolving landscape, in the realm of.
- it's important to note that, it's worth mentioning, needless to say.
- whether you're a beginner or an expert.
- game-changer, cutting-edge, state-of-the-art, seamless, robust, holistic, synergy.
- triads of adjectives ("fast, reliable, and scalable").
- rhetorical questions as section openers.
- not only X but also Y.
- opening with "Certainly!", "Absolutely!", or "Great question!".
- closing with "I hope this helps!" or "Let me know if you have any other questions!".

### Lists and formatting

- Use bullets only when the content is a real list. Do not bullet-ify prose.
- Use numbered lists for ordered steps.
- Bold a phrase only when the reader needs to spot it on a fast scan.
- Tables are good for comparisons.

## Folder and file discipline

Every lesson teaches Claude Code through a real folder. Treat the folder layout as part of the lesson, not an afterthought. Full guidance, including the standard layout, naming rules, and OneDrive/SharePoint notes, is in `docs/Folder_Structure.md`. The non-negotiable rules:

- Always run Claude Code in a dedicated project folder. Never at the OneDrive root, the Desktop, `Documents/`, or any folder that holds unrelated work.
- Every project folder has at least three subfolders: `Master/` (read-only source), `Drafts/` (working files), and `Outputs/` (signed-off final files). Add `Reference/` and `Archive/` as needed.
- The first prompt in any session must name the read-only areas. Example: "Do not edit any file in Master/. Save all output to Drafts/ unless I tell you otherwise."
- No spaces in folder or file names that appear in prompts. `Office_Supplies_RFP_Q2/` not `Office Supplies RFP Q2/`. If a name does contain spaces, quote the path.
- Reference files by full name, extension, and subfolder in every prompt: `Drafts/RFP_Q2_v3.docx`, not `RFP_Q2_v3`.
- Pause OneDrive or SharePoint sync before a multi-file build. Resume after. Half-synced files cause "file in use" errors and `.tmp` outputs.
- **No hardcoded absolute paths.** Never hardcode an absolute path (like `C:/Users/someone/...`) in any script, configuration file, or lesson. Use relative paths derived from the script's own location (for example, `Path(__file__).resolve().parent` in Python, or `$(dirname "$0")` in shell). The only exception is `.claude/settings.json`, where the hook command must use an absolute path because Claude Code does not expand variables in hook commands. Even there, document the path so the next person knows to update it.

## Procurement-specific anti-AI rules

These sit on top of the general writing rules. They reflect how procurement documents need to read in front of a CPO, a CFO, or a board.

- **Banned procurement filler.** Never use "leverage", "synergies", "holistic approach", "robust framework", or "deep dive". Replace each with the concrete thing it stands in for. "Combined annual volume of 18,400 units across BU1 and BU2" beats "synergies".
- **No rhetorical questions as openers.** Open with the fact, the recommendation, or the decision being asked for. Example: "We recommend awarding the office supplies contract to Northwind Office Ltd at $1.42m over 24 months. Decision needed by 2026-05-15."
- **Active voice in risk sections.** "We identified three suppliers with sanctions exposure: Acme Ltd, Northwind GmbH, and Globex SA." Not "It was noted that three suppliers were identified as having sanctions exposure."
- **Specific numbers, every time.** Never write "significant savings", "material reduction", or "considerable improvement". Use the figure: "$1.4m savings, equal to 8.2% of FY25 indirect spend." If the number is not yet known, write `[TBC: figure]`. Drafts carrying `[TBC: figure]` cannot ship.
- **Executive summaries name names.** Every executive summary, board paper, or sponsor update must include at least one supplier name (the legal entity, not "the incumbent"), one contract value or spend figure, and one date (effective, expiry, or decision deadline). If any of those three is missing, the summary is not finished.
- **Three recommendations, no more.** Cap any recommendation list at three. The exception is a document explicitly labeled "Prioritized actions, ranked".
- **USD and US context.** All currency figures use USD. All geographic examples use US locations, US suppliers, and US regulatory context. Personas are based at US companies. Do not use GBP, EUR, or UK/EU geography unless the user explicitly requests it.

## The standard lesson structure

Every lesson, demo, lab, and worked example must follow the same six-part shape. Do not skip parts. Do not reorder them. The full template, with a worked RFP example, lives in `docs/Lesson_Template.md`.

1. **The S2P problem in one paragraph.** Name the document, the role, and the time it usually takes.
2. **What Claude Code is going to do for you.** State the outcome in business terms before mentioning any command.
3. **Set up.** A numbered checklist of just what this lesson needs.
4. **Step-by-step.** Each step has three parts: what you do, what you type or click (in a code block), and what you should see.
5. **A worked example, end to end.** With realistic fake data: suppliers like "Northwind Office Ltd", round-number spend, no real client names.
6. **Common mistakes and how to recover.** Three to six entries, each one symptom and one fix.

## Handouts, briefings, and other learner-facing artifacts

Not every artifact is a lesson. Handouts, quick-start guides, slide decks, prompt-library entries, exercise sheets, and reference Word or PDF files do not need the full six-part shape. They must still meet these rules:

- Every S2P task or capability the artifact describes must have a worked example with **four** parts:
  1. **The prompt to type** (in a code block).
  2. **The folder layout** where applicable (in a code block).
  3. **What the reader should see** when it succeeds (one line).
  4. **What Claude did, behind the scenes.** A short numbered list (three to seven steps) that walks through, in plain English, what Claude actually did to produce that result: what files it opened, in what order, what it filtered or sorted, what assumptions it made, where it asked clarifying questions, what library or technique it used. This is the part that teaches the reader to apply Claude to a new task on their own. Without it, the example only trains rote use.
- Concepts on their own are not enough. If a section explains what a Claude feature does without showing the prompt, the folder, the expected result, and the behind-the-scenes walkthrough, the section is not finished.
- All writing rules and procurement-specific anti-AI rules apply, in full.
- File names follow the naming convention in `docs/Lesson_Template.md`.
- Save artifacts under `Handouts/`, `Briefings/`, or another named folder at the course root, not loose at the top level.
- **Name the specific Claude.** Every capability or limitation statement must name which Claude it applies to: **Claude AI Web** (claude.ai in a browser), **Claude Desktop with Cowork**, or **Claude Code** (in the terminal). If it applies to all three, say "all three" explicitly. If it differs, say which one it works in and which it does not. Never write "Claude can do X" without naming the place. The reader must never wonder where a feature lives.

If you find yourself producing a list of capabilities without prompts, expected outputs, and behind-the-scenes walkthroughs, stop and rebuild it as worked examples.

- **"Why it matters" after every concept, folder, or file explanation.** When a section introduces a concept (what a CLAUDE.md stack is, what a SKILL.md is), a folder (inputs/, skills/, outputs/), or a file (CLAUDE.md, supplier-longlist.csv), follow the explanation with a short "Why it matters" paragraph (two to four sentences). The paragraph must name the concrete consequence of having or not having the thing. Example: "Without this file, Claude produces generic output. With it, every output uses Acme's context, Acme's rules, and Acme's folder structure." Do not write "Why it matters" as a heading. Write it as a labeled paragraph: "Why this matters." followed by the explanation.
- **"What to learn from this" after every Day-in-the-Life scenario.** Every scenario in a Day-in-the-Life section must end with a "What to learn from this" paragraph (two to four sentences). The paragraph names the transferable principle the reader should take away, not a summary of what happened. Example: "A skill works across categories because it names input shapes, not specific values. The bid-scorer says 'read every file in bid-responses/' and 'look up the carrier_id in supplier-longlist.csv'. It does not say 'read FastRoad UK'." A scenario without this teaching takeaway is not finished.
- **Every section needs Claude Code examples.** Every section of a handout or briefing must include at least one Claude Code terminal example: the prompt the reader would type, the command they would run, and the output they would see. Sections that explain a concept without connecting it to a concrete terminal interaction are not finished.
- **Natural progression, not course-based learning.** Handout sections should follow a natural workflow progression (the way a practitioner would actually use the tool across a workday) rather than a course-based learning sequence. The reader is a professional looking for practical application, not a student completing modules.

## Comprehensive training guides

A **comprehensive training guide** is an artifact longer than 3,000 words that teaches one Claude product (Claude AI Web, Claude Desktop with Cowork, or Claude Code) end to end, from install to advanced use. The Claude-for-Dummies handout is a quick-start; a training guide is the full reference.

In addition to the rules above for handouts, every training guide must include all five of:

1. **A "Time savings reference table" near the top.** A two-column or three-column table comparing typical procurement tasks "without Claude" and "with Claude". Use real, named tasks (monthly spend variance report, supplier portfolio scoring of 50 suppliers, contract clause extraction across 10 contracts). Quantify in specific minutes or hours. Never "much faster".
2. **A "Day in the Life" narrative.** A named procurement persona (for example, "Sarah, a Senior Category Manager at a medical device company") walked through five to seven hour-stamped scenarios across one workday. Each scenario shows the prompt the persona typed, what Claude produced, what the persona edited, and how long it took. The persona must stay consistent across the full narrative. The narrative is what makes the guide stick in the reader's memory. **Critical: the Day in the Life must represent a real analyst's workday with genuine procurement scenarios (a CPO deadline, new bids arriving, a CFO rule change, onboarding a colleague, preparing for a supplier meeting). It must NOT read like a course lesson walkthrough or a learning progression. The reader should see themselves in the narrative, not see a student doing exercises.**
3. **A "20-Minute Sprint" section.** An accelerated, no-frills onboarding path that gets a first-time reader to their first usable output in twenty minutes flat. Budget the time in five-minute blocks. Example block structure: 0 to 5 install, 5 to 10 setup, 10 to 13 connect folder, 13 to 18 first task, 18 to 20 review and next steps.
4. **A "First Week Day-by-Day Planner".** Five days of escalating sophistication. Day 1: install and first contact. Day 2: first real task. Day 3: a more advanced feature. Day 4: automation or scheduled work. Day 5: reflect, refine, and plan next week. Each day has explicit goals listed at the top.
5. **The personalization pattern.** When the artifact teaches a folder-based workflow, instruct the reader to split context into separate, single-purpose instruction files rather than one big file:
   - For **Claude Desktop with Cowork** (ABOUT ME folder): `about-me.md` (role, categories, standards), `anti-ai-writing-style.md` (the AI tells to avoid in your voice), `my-company.md` (this year's strategy, savings target, KPIs), `procurement-standards.md` (scoring weights, payment terms, audit rules).
   - For **Claude Code** (project root): one `CLAUDE.md` at the root, with optional sub-folder `CLAUDE.md` files for engagement-specific context.

Comprehensive training guides also follow the worked-example rule (four parts: prompt, folder layout, what you should see, behind-the-scenes walkthrough) for every Use Case and Day-in-the-Life vignette.

## Course materials (e-learning courses with practice data)

A **course** is an e-learning unit that teaches a specific Claude Code capability against a hands-on data set. The student receives the course as a self-contained folder; everything they need is inside. Courses live under `Detailed Course Content/Course_NN_<Title>/`. Each course also gets a companion handout in `Handouts/`.

In addition to the rules above, every course folder must hold these six things:

1. `README.md` (course navigation, what is in the folder, how to start).
2. `COURSE_OVERVIEW.md` (the day-to-day scenario, what gets produced by the end, the rubric for "done").
3. `lessons/` (numbered lesson `.md` files, in order).
4. `practice/` (the hands-on workspace with starter files and realistic data).
5. `solutions/` (reference answers; the lessons say "look only after attempting").
6. `scripts/` (at minimum a regenerator for the practice data).

### Practice folder rules

- **Self-contained.** Every file the student needs is inside the course folder. No external downloads, no separate data store, no shared S3 bucket. Ship the folder, ship the course.
- **Flat structure.** No more than three levels from the course root to any data file. Beginners get lost in deep nesting. Acceptable: `practice/<category>/<file>.csv`. Not acceptable: `reference_data/portfolio/<category>/data/<file>.csv`.
- **Realistic data volumes.** Master files (suppliers, vendors, carriers, contracts, products) stay small (20 to 100 rows) so the learner can read them by hand. Activity files (orders, invoices, shipments, transactions, bid responses) are large (1,000 to 5,000 rows or about 6 to 12 documents) so the learner experiences what Claude does on real volumes. A 5-row CSV does not feel like real procurement work.
- **Date-stamped data.** Every row has a date within the last twelve months so the practice feels current. Document today's date in the README and the OVERVIEW.
- **Real-world file formats.** Bid responses, supplier documents, contracts, and other business documents must use the formats they arrive in during real procurement work: PDF for bid responses, Word (.docx) for contracts and draft documents, Excel (.xlsx) for spend data and scorecards. Do not use markdown (.md) files as stand-ins for business documents in practice data. Claude Code reads PDF and Word files directly.
- **Deterministic regeneration.** A Python script in `scripts/` regenerates all data deterministically (use `random.seed(42)`). If a learner deletes or corrupts the data during practice, one command restores it.

### Lesson rules (course materials are stricter than handouts)

Course lessons follow the standard six-part lesson structure with two additions every beginner needs:

- **Day-to-day scenario at the start.** Every lesson opens with a one-paragraph "It is 09:30 Tuesday. Your CPO Slacks..." that gives a real procurement reason to do this lesson. Not a generic "in this lesson you will learn" intro. The scenario hooks the learner before any abstract concept arrives.
- **Ultra-explicit physical instructions.** Every step has three lines: what to do (one short sentence), the exact command in a code block (copy-paste-able, no placeholders the learner has to fill in), and what you should see (one line describing the on-screen result). Where a step can fail, add an "if you see X, here's the fix" line. Beginners cannot infer; they need exact commands.

## Tone for the learner-facing voice

- Address the reader as "you".
- Use "we" only when the author and the reader are doing the same thing in a worked example.
- Do not call the reader a "user" in body text. "User" is fine in screenshots of software.
- Praise sparingly. One "nice work" at the end of a lab is enough. No exclamation marks in lesson body text.

## What "done" looks like for any artifact

Run this list before saving any artifact: lesson, handout, briefing, exercise, prompt entry, slide, or anything else learner-facing. Reply to the user with the list, item by item, marked **done**, **deferred**, or **N/A** for the artifact at hand. Then build.

1. The S2P problem is named in the first paragraph (or the opening section, for non-lesson artifacts).
2. The outcome is stated in business terms before any command appears.
3. **Every S2P task described has a worked example with four parts: the prompt to type (code block), the folder layout where applicable (code block), what the reader should see when it succeeds, and a "What Claude did, behind the scenes" walkthrough (three to seven plain-English steps).** A list of capabilities without these four parts is not finished. The behind-the-scenes walkthrough is what teaches the reader to apply Claude to new tasks on their own.
4. **Every capability or limitation statement names the specific Claude it applies to**: Claude AI Web, Claude Desktop with Cowork, Claude Code, or "all three" if true everywhere. No bare "Claude can do X" sentences.
5. For lessons, every step has: what you do, what you type, and what you see.
6. There is at least one full worked example with realistic fake data.
7. For lessons, there are three to six troubleshooting entries. For handouts, a "Cautions and ground rules" section is enough.
8. No em-dashes or en-dashes anywhere in the file.
9. No banned phrases from the general or procurement-specific lists above.
10. Oxford commas applied everywhere a list of three or more uses "and" or "or".
11. No rhetorical questions as openers, in any section of the artifact or in any sample document the artifact produces.
12. Risk and issue text is in active voice, with the actor named.
13. Every figure is a real number, not "significant", "material", or "considerable". Any unknown is marked `[TBC: figure]`.
14. Any sample executive summary names a supplier, a value, and a date.
15. Any sample recommendation list has three items or fewer, unless explicitly labeled as a ranked priority list.
16. File names match the convention in `docs/Lesson_Template.md`.
17. Screenshots are cropped, captioned, and use fake data.
18. The artifact uses or references the standard folder layout from `docs/Folder_Structure.md`: `Master/` for source, `Drafts/` for working files, `Outputs/` for final files. Sample prompts name `Master/` as read-only.
19. A procurement analyst with no coding background can read and act on the artifact alone.
20. **For comprehensive training guides only**: a Time savings reference table near the top, a Day-in-the-Life narrative with a named persona, a 20-Minute Sprint, and a First Week Day-by-Day Planner are all present. Folder-based workflows use the personalization pattern (multiple single-purpose instruction files).
21. **For courses only**: the course folder is self-contained (no external downloads), the practice/ tree is no more than three levels deep, master data files are 20 to 100 rows, activity data files are 1,000 to 5,000 rows, every lesson opens with a day-to-day scenario, every step has three lines (what to do, exact command, what you should see) plus a fix line where it can fail, and a regenerator script exists in `scripts/`.
22. `scripts/check_style.py` reports zero violations on the saved file (the `PostToolUse` hook runs this automatically; for `.pptx` or `.pdf`, run an equivalent check by hand).
23. **Every concept, folder, or file explanation has a "Why it matters" paragraph** (two to four sentences naming the concrete consequence). Descriptions without a "why" are not finished.
24. **Every Day-in-the-Life scenario ends with a "What to learn from this" paragraph** (two to four sentences naming the transferable principle, not a summary). Scenarios without a teaching takeaway are not finished.

If any item fails, fix it before the artifact goes out.
