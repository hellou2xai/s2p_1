# Lesson 1: System Design Mapping

**Course:** The Negotiation Intelligence System
**Time:** 40 minutes

---

## Opening scenario

It is 08:30 on Monday. Your VP of Procurement has just forwarded you an email from Redline Logistics LLC. The subject line is "CTR-2024-LG-001 Renewal Proposal." You open it. Redline is asking for a 12% price increase, a narrowed force majeure clause, and a shortened auto-renewal notice period. The face-to-face negotiation is in 12 days, on 2026-05-07. Your VP wants a pre-negotiation brief by Friday. That is four days from now.

You have five source files: the current contract, the renewal proposal, 24 months of supplier performance data, market benchmarks, and a history of past negotiations with Redline. You need to turn those five files into a counter-proposal that your negotiator can take to the table. Normally, this takes two analysts a full week. You have Claude Code and a plan.

This lesson is about the plan. You will map every stage of the negotiation workflow to the Claude Code component that handles it best. By the end of this lesson, you will have a system design document in your project folder. The remaining five lessons build each component.

---

## What Claude Code is going to do for you

Claude Code will read your source files and help you design a five-component system: sub-agents for parallel intelligence gathering, a PostToolUse hook for automatic deviation costing, a PreToolUse block for brief completeness validation, a slash command for generating the pre-negotiation brief, and a second slash command for drafting the counter-proposal. You will map each component to its inputs and outputs, then save the design as a reference document. Every build decision in Lessons 2 through 6 will trace back to this map.

---

## Set up

1. Open your terminal. Navigate to the course practice folder:

```
cd "Course_10_The_Negotiation_Intelligence_System/practice"
```

2. List the contents to confirm the source files are present:

```
ls data/
```

You should see: `current-contract.md`, `proposed-renewal.md`, `supplier-performance.csv`, `market-benchmarks.md`, and `negotiation-history.csv`.

3. Confirm the project subfolders exist:

```
ls
```

You should see: `data/`, `CLAUDE.md`, and at least `Outputs/` (if it is missing, create it with `mkdir Outputs`).

4. Start Claude Code in the practice folder:

```
claude
```

You should see the Claude Code prompt with the practice folder name displayed.

5. State the read-only rule for `data/`:

```
The folder data/ holds the source files for this negotiation. Do not edit any file in data/. Read from it freely. Save all output to Outputs/ unless I tell you otherwise.
```

Claude should confirm it understands. Nothing changes on disk.

**Folder layout at the start of this lesson:**

```
practice/
├── CLAUDE.md
├── data/
│   ├── current-contract.md
│   ├── proposed-renewal.md
│   ├── supplier-performance.csv
│   ├── market-benchmarks.md
│   └── negotiation-history.csv
└── Outputs/
```

---

## Step-by-step

### Step 1: Survey the source files

Ask Claude to read each source file and summarize its contents in one sentence.

```
Read each file in data/ and give me a one-sentence description of what it contains and what role it plays in a contract negotiation.
```

You should see five descriptions. For example: "`current-contract.md` contains the active terms of contract CTR-2024-LG-001 with Redline Logistics LLC, including pricing, service levels, and legal clauses."

If you see "No such file or directory," check that you navigated to the `practice/` folder, not the course root.

### Step 2: Identify the negotiation workflow stages

Ask Claude to outline the stages you need to complete before you can send a counter-proposal.

```
I need to prepare a counter-proposal for the CTR-2024-LG-001 renewal with Redline Logistics LLC. The proposed changes include a 12% price increase, a narrowed force majeure clause, and a shortened notice period. List the five stages I need to complete before I can present a counter-proposal. For each stage, name the goal in one sentence.
```

You should see five stages: intelligence gathering, deviation costing, brief writing, counter-proposal drafting, and post-close capture. The exact wording may vary, but the sequence from data to decision should be clear.

If Claude lists fewer than five stages, prompt it: "Include a stage for capturing lessons learned after the negotiation closes."

### Step 3: Map Claude Code components to each stage

Ask Claude to recommend the best Claude Code component for each stage.

```
For each of the five negotiation stages, tell me which Claude Code component fits best: CLAUDE.md for persistent context, a skill for repeatable analysis, a slash command for one-click execution, a PostToolUse or PreToolUse hook for automatic quality gates, or a sub-agent for parallel work. Explain why each mapping makes sense for this logistics contract negotiation.
```

You should see a mapping like:
- Intelligence gathering: sub-agents (three research tasks can run in parallel).
- Deviation costing: PostToolUse hook (fires automatically after every deviation file write).
- Brief writing: PreToolUse hook (blocks the brief from saving if key fields are missing).
- Counter-proposal: slash command (one-click generation from the approved brief).
- Post-close capture: slash command (one-click archival and lessons-learned record).

If Claude recommends running everything sequentially, push back: "Which of these stages produce independent outputs that could run at the same time?"

### Step 4: Review the key contract changes

Ask Claude to compare the current contract to the renewal proposal.

```
Read data/current-contract.md and data/proposed-renewal.md. Create a table with four columns: Term, Current Value, Proposed Value, and Direction (increase, decrease, or restriction). List every term that changed between the two documents.
```

You should see a table. Look for three rows at minimum: price (12% increase), force majeure scope (narrowed), and notice period (180 days reduced to 90 days). If additional terms changed, they will appear here too.

If the table is empty, check that both files contain text: `cat data/current-contract.md` and `cat data/proposed-renewal.md`.

### Step 5: Write the system design document

Ask Claude to save the design as a reference file.

```
Write a system design document to Outputs/system-design.md. For each of the five negotiation stages, include: the stage name, the Claude Code component, the input files it needs, the output file it produces, and a one-sentence description of what it does. Format each stage as a section with a markdown table. At the top, add a summary paragraph naming Redline Logistics LLC, the $9.2M contract value, the 2026-05-07 negotiation deadline, and the three proposed changes.
```

You should see a confirmation that `Outputs/system-design.md` was created. The file should have five sections, each with a table.

If Claude saves to a different path, tell it: "Move that file to Outputs/system-design.md."

### Step 6: Verify the design document

Read the file back to confirm it is complete.

```
Read Outputs/system-design.md. Does the summary paragraph name Redline Logistics LLC, state $9.2M, list 2026-05-07, and mention all three proposed changes? If anything is missing, add it.
```

You should see Claude confirm all four elements are present, or add the missing ones.

### Step 7: Exit Claude Code

```
/quit
```

---

## Worked example, end to end

**Starting files:**

- `data/current-contract.md`: CTR-2024-LG-001, $9.2M/year, Redline Logistics LLC, expires 2027-05-31.
- `data/proposed-renewal.md`: Redline's renewal proposal with three changes.
- `data/supplier-performance.csv`: 24 months of on-time delivery, damage rate, and SLA compliance data.
- `data/market-benchmarks.md`: US logistics market rate comparisons for the Midwest corridor.
- `data/negotiation-history.csv`: Outcomes from prior Redline negotiations.

**The prompts you type, in order:**

```
Read each file in data/ and give me a one-sentence description of what it contains.
```

```
List the five stages I need to complete before I can present a counter-proposal for the Redline Logistics LLC renewal. For each, name the goal in one sentence.
```

```
Map each stage to the Claude Code component that fits best. Explain why.
```

```
Read data/current-contract.md and data/proposed-renewal.md. Table the differences: Term, Current Value, Proposed Value, Direction.
```

```
Write the system design document to Outputs/system-design.md. Five stages, each with a table showing component, inputs, output, and purpose. Add a summary paragraph naming Redline Logistics LLC, $9.2M, 2026-05-07, and the three changes.
```

**Extract from the output:**

```
## Summary

This system supports the CTR-2024-LG-001 renewal negotiation with Redline Logistics LLC,
currently valued at $9.2M per year. The negotiation deadline is 2026-05-07. Redline has
proposed a 12% price increase, a narrowed force majeure clause, and a reduction in the
auto-renewal notice period from 180 days to 90 days.
```

**Finished artifact:** `Outputs/system-design.md`, a five-section reference document mapping each negotiation stage to its Claude Code component, inputs, and output file.

**What Claude Code did behind the scenes:**

1. Claude Code read each file in `data/` and identified its content type and negotiation role.
2. It applied knowledge of the five Claude Code component types (CLAUDE.md, skills, commands, hooks, sub-agents) to match each stage by its characteristics: parallel work goes to sub-agents, automatic gates go to hooks, one-click actions go to commands.
3. It compared the two contract files term by term, flagging every changed value.
4. It assembled the design document with one section per stage, structuring each as a markdown table.
5. It placed the summary paragraph at the top of the file, including all four required fields (supplier name, contract value, deadline, and the three changes).
6. It saved the file to `Outputs/system-design.md` and left `data/` untouched.

---

## Common mistakes and how to recover

**Symptom:** Claude edits a file in `data/` by mistake.
**Fix:** Check Git history or OneDrive version history to restore the original. Add this line to `CLAUDE.md`: "data/ is read-only. Never write to any file in data/."

**Symptom:** The system design has no output file names, only stage names.
**Fix:** Tell Claude: "For each stage, name the specific output file, including the subfolder path. For example, Outputs/intelligence-brief.md."

**Symptom:** Claude maps everything to a single component type, like putting all five stages in sub-agents.
**Fix:** Ask it to reconsider: "Which stages need to block execution until a quality check passes? Those stages need hooks, not sub-agents."

**Symptom:** The summary paragraph is missing the negotiation deadline.
**Fix:** Prompt: "Add the 2026-05-07 negotiation deadline to the summary paragraph in Outputs/system-design.md."

**Symptom:** Claude saves the file as `system_design.md` instead of `system-design.md`.
**Fix:** Tell Claude to rename it: "Rename Outputs/system_design.md to Outputs/system-design.md." File names in this project use hyphens, not underscores.

---

## You are done with Lesson 1 when

- `Outputs/system-design.md` exists and has five sections.
- The summary paragraph names Redline Logistics LLC, states $9.2M, lists 2026-05-07, and mentions all three proposed changes.
- You can explain why sub-agents fit intelligence gathering and why hooks fit quality gates.

Move to Lesson 2 when ready.
