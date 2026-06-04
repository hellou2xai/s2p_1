# Lesson 06: The Board Resilience Brief

## Opening scenario

It is 08:00 Friday. The board meeting is next Thursday. Your CPO sends one final message: "I need the brief by Monday morning. Three pages. Lead with the findings, not the methodology. The CFO wants to know what we're asking them to approve and why. If I have to explain what a risk score is, the brief is too long." You have five draft files in `Drafts/` covering every angle of Fortis Manufacturing's supply chain risk. This lesson assembles all of it into the three-section brief the board will actually read: three key findings, a top-five risk table, and an investment case. One pass. Done by end of day Friday.

## The S2P problem

Board members read the first page. If the first page does not answer "Are we protected, and what does it cost to get protected?", they stop reading. A 28-page risk report buries that answer under methodology sections, scoring details, and data appendices. The board brief must lead with findings stated as numbers, not as process descriptions. Three pages. No filler. Every sentence earns its place by carrying a dollar amount, a supplier name, a date, or a percentage.

## What Claude Code is going to do for you

Claude Code reads the five draft files from Lessons 1 through 5: the concentration risk summary, the single-source exposure map, the disruption scenarios, the mitigation plan, and CLAUDE.md for output standards. It writes a three-section brief with an executive summary at the top. Section one: three key findings, each starting with a number. Section two: a five-row risk table sorted by financial exposure. Section three: the investment case with total cost, total exposure reduced, payback ratio, and a three-action recommendation. The brief saves to `Drafts/board-resilience-brief.md`. This lesson takes about 35 minutes.

## Set up

1. Lessons 1 through 5 completed. All five draft files are saved in `Drafts/`.
2. Claude Code open in `Course_19_Supply_Chain_Risk/practice/`. If you closed it, reopen:

```
cd "Course_19_Supply_Chain_Risk/practice"
claude
```

3. Confirm all five draft files exist:
   - `Drafts/concentration-risk-summary.md`
   - `Drafts/single-source-exposure-map.md`
   - `Drafts/disruption-scenarios.md`
   - `Drafts/mitigation-plan.md`
4. CLAUDE.md output standard: board brief is 3 pages maximum, recommendations capped at three, every summary names a supplier, a value, and a date.

Open the session with the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

## Step-by-step

### Step 1. Confirm the brief structure with Claude Code before drafting.

State the exact structure first. This prevents Claude from inventing a different format.

```
I need a board resilience brief with this exact structure:

Executive summary: one sentence. States the overall risk posture, the total
unprotected exposure in USD, and the investment ask.

Section 1 - Three key findings: one paragraph per finding. Each paragraph starts
with a specific number (dollar amount, count, or percentage). Each paragraph names
at least one supplier. Each paragraph is three sentences maximum.

Section 2 - Top 5 risks: a table with columns: rank, risk_description,
affected_supplier, annual_exposure_usd, current_risk_level, mitigation_status.

Section 3 - Investment case: total mitigation cost, total exposure reduced,
payback ratio, and a recommendation paragraph naming three actions with deadlines.

Confirm you understand this structure before we begin drafting.
```

You should see Claude Code confirm the four-part structure (executive summary, three findings, risk table, investment case) with the column names and the three-sentence limit per finding. If Claude starts drafting instead of confirming, repeat the instruction and add: "Do not write any content yet. Only confirm the structure."

### Step 2. Draft the three key findings.

Pull the three most impactful facts from the analysis drafts.

```
Using Drafts/concentration-risk-summary.md, Drafts/single-source-exposure-map.md,
and Drafts/disruption-scenarios.md, write three key findings for the board brief.
Rules for each finding:
- First word must be a number written as a figure (not spelled out).
- Must name at least one supplier by legal name.
- Must state one business consequence.
- Maximum three sentences.
Do not start any finding with "We found that" or "Our analysis shows."
```

You should see three findings. A strong example: "Finding 1: $620,000 in annual spend has no qualified alternate supplier. ITEM-0025 (Microcontroller ARM) and ITEM-0049 (Fire inspection) are both sole-sourced with no approved backup. A 60-day disruption at Apex Electronics would cost Fortis an estimated $480,000 in direct and indirect costs plus a 6 to 12-month recovery period." If any finding starts with a word instead of a number, ask Claude to rewrite it.

### Step 3. Build the top five risks table.

Rank all identified risks by annual financial exposure and select the top five.

```
From all risk analysis drafts, select the top 5 risks by annual financial exposure.
Build a table with these columns: rank, risk_description, affected_supplier,
annual_exposure_usd, current_risk_level, mitigation_status (planned/in_progress/none).
Sort by annual_exposure_usd descending. Use exactly 5 rows.
```

You should see a 5-row table. The top rows should reflect the highest-exposure risks: the Pacific Aluminum 60-day disruption scenario ($1,052,877 total impact), the Continental Freight outage scenario ($610,959), and single-source gaps for critical items. If Claude produces more than 5 rows, ask it to keep only the top 5 by annual_exposure_usd and remove the rest.

### Step 4. Write the investment case section.

Build the financial argument for the mitigation budget.

```
Using Drafts/mitigation-plan.md, write the investment case section. Include:
- Total mitigation investment: sum of all planned action costs.
- Total annual exposure reduced: sum of all exposure reductions.
- Payback ratio: exposure reduced divided by investment.
- Recommendation paragraph: names the three highest-priority actions, states each
  action's deadline, and states how much exposure each removes.
  Three actions maximum. Dollar figures required for each action.
```

You should see the investment case with a specific payback ratio. For example: "$340,000 investment reduces $4,200,000 in annual supply chain exposure, a 12.4x payback ratio." The recommendation paragraph names three actions with specific deadlines (for example, "by 2026-07-31") and specific exposure reductions. If the paragraph lists four or more actions, ask Claude to trim to three.

### Step 5. Assemble and save the full brief.

Combine all four parts into one document.

```
Combine the executive summary, three key findings, top 5 risks table, and investment
case into a single board resilience brief. Title the document:
"Supply Chain Risk and Resilience Brief, Q2 2026 - Fortis Manufacturing."
Date it 2026-04-25.
Save to Drafts/board-resilience-brief.md.
```

You should see the complete brief saved. The executive summary must appear first, followed by Section 1, Section 2, and Section 3 in order. If the file saves but the sections are in the wrong order, ask Claude to rewrite the file with the sections in the specified sequence.

### Step 6. Validate the brief against the output standards.

Run the brief through a structured check before it leaves your hands.

```
Read Drafts/board-resilience-brief.md and check it against these rules from CLAUDE.md:
1. Does the executive summary name a supplier, a dollar value, and a date?
2. Does each key finding start with a number written as a figure?
3. Does the risk table have exactly 5 rows?
4. Does the recommendation paragraph name 3 actions or fewer?
5. Are all currency figures in USD with commas (no "USD" suffix needed, just commas)?
6. Are there any em-dashes, en-dashes, or banned phrases?
Report pass or fail for each rule. If any rule fails, state exactly what needs to change.
```

You should see six pass results. If any rule fails, ask Claude to fix only the failing element without rewriting the rest of the document. If rule 6 fails (banned phrase or dash found), ask Claude to show the exact sentence and then rewrite it.

## Worked example

**Starting files:**
- `Drafts/concentration-risk-summary.md` (three concentration views with named suppliers and dollar amounts).
- `Drafts/single-source-exposure-map.md` (5 items, $620,000 in unprotected spend, 2 critical gaps).
- `Drafts/disruption-scenarios.md` (2 scenarios, total impacts $1,052,877 and $610,959).
- `Drafts/mitigation-plan.md` (5 ranked actions, investment case with payback ratio).

**What you type:**

```
Assemble the board resilience brief from the four draft files in Drafts/. Structure:
executive summary (one sentence, name a supplier, a value, and a date), three key
findings (number first, supplier named, three sentences max), top 5 risks table
(by annual_exposure_usd), investment case (cost, exposure reduced, payback ratio,
three-action recommendation). Title: "Supply Chain Risk and Resilience Brief,
Q2 2026 - Fortis Manufacturing." Date: 2026-04-25. Save to
Drafts/board-resilience-brief.md.
```

**What you should see:**

A brief titled "Supply Chain Risk and Resilience Brief, Q2 2026 - Fortis Manufacturing" dated 2026-04-25. The executive summary reads something like: "Fortis Manufacturing carries $620,000 in unprotected single-source exposure across two critical items and faces up to $1,052,877 in disruption costs if Pacific Aluminum fails; a $340,000 mitigation investment approved by 2026-05-15 reduces total annual exposure by $4,200,000." Three findings follow, each leading with a number. The risk table has exactly 5 rows. The investment case recommendation names three actions with deadlines.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the output standards: 3-page maximum, three findings, five-risk table, three-action recommendation cap, USD with commas, no em-dashes.
2. Read `Drafts/concentration-risk-summary.md` and extracted the highest-impact concentration finding.
3. Read `Drafts/single-source-exposure-map.md` and extracted the two critical gaps ($620,000 combined with no alternate).
4. Read `Drafts/disruption-scenarios.md` and extracted the two scenario totals ($1,052,877 and $610,959).
5. Selected the three most impactful facts and wrote each as a number-first paragraph of three sentences or fewer.
6. Ranked all identified risks by annual_exposure_usd and selected the top five for the table.
7. Read `Drafts/mitigation-plan.md` and extracted total investment, total exposure reduction, and the three highest-ratio actions with their deadlines.
8. Assembled all four parts in the specified order and saved the file.

## Common mistakes and how to recover

- **Symptom:** The executive summary does not name a supplier. **Fix:** Every executive summary in this course must include at least one supplier name, one dollar value, and one date. Ask Claude to rewrite the executive summary and include the highest-exposure supplier (likely Apex Electronics or Pacific Aluminum) and the investment deadline.

- **Symptom:** A key finding starts with a word instead of a number. **Fix:** The brief rules require every finding to open with a figure. Ask Claude to identify which finding starts with a word and rewrite only that finding. "Five single-source items..." must become "5 single-source items..." and "$620,000 in unprotected spend..." stays as is.

- **Symptom:** The risk table has 6 or more rows. **Fix:** The output standard caps the table at 5 rows. Ask Claude to re-rank all risks by annual_exposure_usd and keep only the top 5. Move the remaining risks to a note below the table: "Additional risks are documented in Drafts/mitigation-plan.md."

- **Symptom:** The investment case recommendation lists four or five actions. **Fix:** CLAUDE.md caps recommendation lists at three unless the list is explicitly labeled "Prioritized actions, ranked." Ask Claude to keep the three actions with the highest risk reduction ratio and remove the rest.

- **Symptom:** The brief is much longer than three pages when printed. **Fix:** Cut every sentence that describes process or methodology. The board does not need to know how you scored suppliers or which files you read. They need the scores, the risks, and the ask. Move any methodology explanation to a separate `Drafts/methodology-note.md` file if a board member requests it.

- **Symptom:** The validation in Step 6 fails on rule 6 (banned phrase found). **Fix:** Ask Claude to show the exact sentence that contains the flagged phrase. Then ask it to rewrite that sentence with a concrete replacement. Vague filler about "frameworks" or "approaches" should become a specific description: "five-factor scoring model" or "end-to-end assessment covering financial health, geography, single-source exposure, disruption history, and alternate availability." Vague action verbs should become specific ones: "use" instead of the L-word, "apply" instead of "deploy."
