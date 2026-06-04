# Lesson 5: Counter-Proposal Generation

**Course:** The Negotiation Intelligence System
**Time:** 55 minutes

---

## Opening scenario

It is 09:00 on Wednesday. Your VP approved the pre-negotiation brief last night. She added one note at the bottom: "Counter-proposal on my desk by noon. Face-to-face is in nine days." The counter-proposal is the document your negotiator takes to the table. It has to address all three of Redline's proposed changes, stay below the $9.75M walk-away ceiling, cite specific performance data, and read like a professional external communication, not an internal analysis. Writing it from scratch takes three to four hours. You have two.

In this lesson, you create a slash command called `/counter-proposal` in Claude Code. One command reads the approved brief, pulls the deviation costs, checks the negotiation history, and writes a complete counter-proposal document. The command encodes your logic so the same process runs the same way every time, for this negotiation and every future one.

---

## What Claude Code is going to do for you

You will create a file at `.claude/commands/counter-proposal.md` that defines a Claude Code slash command. When you type `/counter-proposal`, Claude Code reads that file and follows the instructions inside it. The command tells Claude to read the pre-negotiation brief for strategy, read the deviation costs for specific figures, read the negotiation history for prior outcomes with Redline, and write a formal counter-proposal addressed to Redline Logistics LLC. The document must address all three proposed changes, propose specific counter-values, keep the total annual cost below $9.75M, and include a response deadline. The PreToolUse and PostToolUse hooks from Lessons 3 and 4 continue to run, so quality gates stay active.

---

## Set up

1. Confirm you completed Lesson 4. Check for the approved brief:

```
ls Outputs/pre-negotiation-brief.md
```

You should see the file listed.

2. Navigate to the practice folder if you are not already there:

```
cd "Course_10_The_Negotiation_Intelligence_System/practice"
```

3. Create the commands folder if it does not exist:

```
mkdir -p .claude/commands
```

4. Start Claude Code:

```
claude
```

5. Restate the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/. Save all output to Outputs/.
```

**Folder layout at the start of this lesson:**

```
practice/
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   └── commands/              (empty until Step 1)
├── data/
│   ├── current-contract.md
│   ├── proposed-renewal.md
│   └── negotiation-history.csv
├── scripts/
│   ├── check-deviation-costs.py
│   └── check-brief-completeness.py
└── Outputs/
    ├── system-design.md
    ├── intelligence-brief.md
    ├── deviation-costs.md
    └── pre-negotiation-brief.md
```

---

## Step-by-step

### Step 1: Read the negotiation history before building the command

Check what Redline has agreed to in past negotiations.

```
Read data/negotiation-history.csv. List every past negotiation with Redline Logistics LLC: the year, the supplier's original ask, the final agreed value, and the key concessions made by each side.
```

You should see a table of past negotiations. Note the most recent outcome. For example: "2024 renewal: Redline asked for 8% increase. Final agreed value: $8.5M (original was $7.88M before the 2024 base rate). TransGlobal conceded on payment terms (Net 45 to Net 30). Redline conceded on fuel surcharge cap." This history strengthens your counter-proposal by showing Redline has negotiated down before.

If the CSV is empty or has no Redline rows, run the data regenerator: `python scripts/build_course_data.py`.

### Step 2: Review the approved brief's key positions

```
Read Outputs/pre-negotiation-brief.md. List the three recommendations, the BATNA, and the walk-away price.
```

You should see the three recommendations, the BATNA (rebid to three carriers, $280,000 transition cost, 90-day timeline), and the walk-away price ($9.75M).

Hold these in mind. The counter-proposal must not reveal the walk-away price and must not commit TransGlobal to positions that conflict with the brief.

### Step 3: Create the slash command file

Ask Claude Code to write the command definition.

```
Create a file at .claude/commands/counter-proposal.md with the following content:

This command generates a counter-proposal for the current contract renewal negotiation.

Steps:
1. Read Outputs/pre-negotiation-brief.md. Extract the BATNA, walk-away price, and three recommendations. Do not reveal the walk-away price in the output document.
2. Read Outputs/deviation-costs.md. For each deviation row, note the term, the current value, the proposed value, and the annual cost impact.
3. Read data/negotiation-history.csv. Find the most recent negotiation with the same supplier and note the final agreed value and key concessions.
4. Write a counter-proposal to Outputs/counter-proposal.md addressed formally to Redline Logistics LLC. The document must include:
   a. Opening paragraph: name the current contract (CTR-2024-LG-001), the current annual value ($9.2M), the contract expiry (2027-05-31), and TransGlobal's commitment to a productive renewal.
   b. Response to Price Increase: propose a specific counter rate. The counter must keep the total annual cost below the walk-away price. Cite Redline's OTD performance decline from 96.8% to 93.1% as a factor in the counter-position.
   c. Response to Force Majeure Change: propose restoring the original clause language. State the reason: supply chain disruptions are a foreseeable risk in logistics, not an exceptional event.
   d. Response to Notice Period Change: propose restoring the 180-day notice period. State the reason: 90 days is insufficient for TransGlobal to re-source four distribution centers.
   e. Summary of Proposed Annual Value: state the total annual value of TransGlobal's counter-proposal.
   f. Reference to alternatives: mention that TransGlobal has assessed alternatives for the corridor, without naming specific carriers or stating the walk-away price.
   g. Response deadline: request Redline's response by a date that is 14 days from today (2026-04-25), which is 2026-05-09.
5. Confirm the total annual value in the counter-proposal is below $9.75M before saving.
```

You should see Claude Code create the file at `.claude/commands/counter-proposal.md`.

### Step 4: Run the command

Type the slash command:

```
/counter-proposal
```

You should see Claude Code read the command file and begin executing the steps. It will read the brief, the deviation costs, and the history, then write `Outputs/counter-proposal.md`. The process takes one to two minutes.

If Claude says "Unknown command," check that the file is at `.claude/commands/counter-proposal.md` (not in a subfolder) and restart Claude Code.

### Step 5: Verify the total annual value

```
Read Outputs/counter-proposal.md. What is the total annual value of TransGlobal's counter-proposal? Is it below $9.75M?
```

You should see Claude Code state the total. It should be below $9.75M. A typical result: TransGlobal counters the price increase at 4% (from $9.2M to $9.568M), proposes restoring both clauses, and puts the total at $9.568M.

If the total exceeds $9.75M, tell Claude: "The counter-proposal total exceeds $9.75M. Reduce the proposed price increase percentage until the total is at or below $9.568M, then rewrite the document."

### Step 6: Verify all three proposed changes are addressed

```
Read Outputs/counter-proposal.md. Does it address the price increase, the force majeure change, and the notice period change? Is there a section for each? List any that are missing.
```

You should see Claude Code confirm all three are addressed, or flag any that were skipped.

### Step 7: Check the tone

```
Read Outputs/counter-proposal.md. Is this document written as a formal external letter to Redline Logistics LLC, or does it read like an internal analysis? If any section uses internal language (BATNA, walk-away, deviation costs), rewrite that section in external supplier-facing language.
```

You should see Claude Code read the document and confirm it uses external language throughout, or rewrite the problematic sections.

### Step 8: Exit Claude Code

```
/quit
```

---

## Worked example, end to end

**Starting files:**

- `Outputs/pre-negotiation-brief.md`: Eight sections including BATNA (rebid, $280,000 transition, 90-day timeline) and walk-away ($9.75M).
- `Outputs/deviation-costs.md`: Three rows: price increase $1,104,000, force majeure restriction $140,000, notice period restriction $134,000. Total: $1,378,000.
- `data/negotiation-history.csv`: 2024 renewal: Redline asked for 8%, final agreed 4.1%, TransGlobal conceded Net 30 payment terms.

**The prompts you type, in order:**

```
Read data/negotiation-history.csv. List every past negotiation with Redline Logistics LLC.
```

```
Read Outputs/pre-negotiation-brief.md. List the three recommendations, the BATNA, and the walk-away price.
```

```
Create .claude/commands/counter-proposal.md with the five-step command definition.
```

```
/counter-proposal
```

**Extract from the output:**

```
## Response to Proposed Price Increase

Redline Logistics LLC's proposed 12% rate increase would bring the annual contract
value from $9.2M to $10.304M. TransGlobal Industries does not accept this position.

On-time delivery performance under CTR-2024-LG-001 has declined from 96.8% in
the period ending October 2025 to 93.1% in the period ending March 2026, falling
below the contractual SLA target of 96.0% for four of the last six months. A price
increase of this magnitude is inconsistent with a declining service record.

TransGlobal proposes a 4% rate adjustment, bringing the annual contract value to
$9.568M. This reflects current market conditions and aligns with Redline's service
performance over the contract period.
```

**Finished artifact:** `Outputs/counter-proposal.md`, a formal external document addressed to Redline Logistics LLC, with specific counter-positions on all three proposed changes and a total annual value of $9.568M.

**What Claude Code did behind the scenes:**

1. Claude Code read the command definition from `.claude/commands/counter-proposal.md` and followed the five steps in order.
2. It read the pre-negotiation brief and extracted the walk-away price ($9.75M), BATNA, and three recommendations. It held these as constraints, not as content to copy into the output.
3. It read the deviation costs and calculated the counter-positions: a 4% increase on price (vs. the proposed 12%), and full restoration on both legal clauses.
4. It read the negotiation history and noted the 2024 precedent: Redline agreed to a 4.1% increase after proposing 8%. This confirmed that a 4% counter was within a realistic negotiation range.
5. It verified the counter-total: $9.2M multiplied by 1.04 equals $9.568M, which is below $9.75M.
6. It wrote the document in external supplier-facing language, citing performance data by name but not mentioning BATNA, walk-away, or deviation costs by those terms.
7. It set the response deadline to 2026-05-09, which is 14 days from 2026-04-25.

---

## Common mistakes and how to recover

**Symptom:** The `/counter-proposal` command is not recognized.
**Fix:** The command name is the filename without the `.md` extension. If your file is `counter-proposal.md`, the command is `/counter-proposal`. If Claude says "Unknown command," check the file path is exactly `.claude/commands/counter-proposal.md` and restart Claude Code.

**Symptom:** The counter-proposal reveals the walk-away price of $9.75M.
**Fix:** The command instructions say not to reveal it, but Claude may have included it anyway. Tell Claude: "Remove any mention of $9.75M from Outputs/counter-proposal.md. Replace it with language about reviewing alternatives for the corridor."

**Symptom:** The counter-proposal total is $10.3M instead of $9.568M.
**Fix:** Claude accepted all three proposed changes without negotiating. Tell it: "Your counter-proposal must not accept the 12% price increase. Counter at 4%. Recalculate the total and rewrite the price section."

**Symptom:** The force majeure and notice period sections are missing from the output.
**Fix:** Claude may have focused only on price. Tell it: "The counter-proposal is missing sections for force majeure and notice period. Add a section for each that proposes restoring the original clause language."

**Symptom:** The document reads like an internal briefing, with terms like "BATNA" and "deviation analysis" visible.
**Fix:** Tell Claude: "Read Outputs/counter-proposal.md. Identify any internal procurement term (BATNA, deviation analysis, walk-away, deviation cost) and rewrite those sentences in plain external language."

**Symptom:** The response deadline in the document is the wrong date.
**Fix:** The command uses today's date (2026-04-25) plus 14 days. If the date is wrong, tell Claude: "Today is 2026-04-25. Set the Redline response deadline to 2026-05-09."

---

## You are done with Lesson 5 when

- `.claude/commands/counter-proposal.md` exists with the five-step command definition.
- `Outputs/counter-proposal.md` exists and was generated by the `/counter-proposal` command.
- The counter-proposal total is below $9.75M.
- All three proposed changes (price increase, force majeure, notice period) have counter-positions.
- The document names Redline Logistics LLC, states the current $9.2M value, and proposes a specific counter-value.
- The document uses external supplier-facing language throughout.

Move to Lesson 6 when ready.
