# Lesson 5: Skill composition - chaining skills together

**Time:** 60 minutes. **You need:** Lessons 3 and 4 complete.

## A typical Friday morning

It is 09:00 Friday. The award panel meeting is at 10:00. You need: the RFP package (have it from Lesson 3), the bid comparison (have it from Lesson 4), a savings case showing how the recommendation hits the 1.6m GBP target, a per-bidder risk profile, and a one-page award memo with three named recommendations.

You have 60 minutes.

You write three small skills (`risk-profiler`, `savings-calculator`, `award-memo`) and then chain all five skills together in one session. By 10:00 you have a complete sourcing package in `outputs/`. You walk into the panel meeting with the deliverables, not the to-do list.

## The big idea

A skill takes inputs of a known shape and produces output of a known shape. **Output of one skill can be input to another.** That is composition.

The chain you will run today:

```
1. rfp-builder       → outputs/rfp-package.md          (had this from Lesson 3)
2. bid-scorer        → outputs/bid-comparison.md       (had this from Lesson 4)
3. risk-profiler     → outputs/risk-profile.md         (write today, run today)
4. savings-calculator → outputs/savings-case.md         (write today, run today)
5. award-memo        → outputs/award-memo.md           (write today, run today; reads ALL the above)
```

Each step in the chain reads the previous outputs as additional inputs. The award memo reads the bid comparison, the risk profile, and the savings case to produce the recommendation. That is composition: every skill is a small piece; together they are a sourcing event.

## Set up

**Step 1.** Open your terminal.

**Step 2.** Move to the practice folder:

```
cd "Course_03_The_Skill_Builder/practice"
```

**Step 3.** Confirm you have the two outputs from Lessons 3 and 4:

```
ls outputs
```

You should see at least `rfp-package.md` and `bid-comparison.md`. If either is missing, go back and re-run Lesson 3 or Lesson 4.

## Write three more skills

You will write three skills in the next 30 minutes. Each one is short (40 to 60 lines), because by now the pattern is familiar.

### 5a. Write risk-profiler

**Step 4.** Create `practice/skills/risk-profiler.md` with this content:

```
# risk-profiler

## What this skill does

Produces a one-paragraph risk profile per bidder, drawing on the longlist
data and the bid response. Use after bid-scorer has run; the output feeds
into the award memo.

## Inputs

bid-responses/*.md (the bid response files).
inputs/supplier-longlist.csv (capacity_tier, financial_health, otd_pct_12m,
incumbent columns are most important).
outputs/bid-comparison.md (the score table from bid-scorer).

## Process

1. List bidders from the bid-responses folder.
2. For each bidder, look up financial_health, capacity_tier, and incumbent
   from the longlist (keyed by carrier_id from filename).
3. Read each bid response for: implementation cost, term length, exit terms,
   indexation rules.
4. Score risk on three dimensions: Financial (1 to 5; 5 is highest risk),
   Operational (1 to 5), Commercial (1 to 5).
5. For each bidder, write a one-paragraph risk profile (60 to 100 words)
   that names the highest-risk dimension and a mitigation.

## Output format

Save outputs/risk-profile.md. One section per bidder. Each section:
- Title (bidder name and total risk score).
- One paragraph (60 to 100 words) covering the three risk dimensions
  and the proposed mitigation.

Cap the file at 800 words.

## Quality criteria

- Every bidder in bid-responses/ has a risk profile section.
- Every section names a specific mitigation tied to the highest risk.
- Total risk score per bidder is between 3 and 15 (sum of three 1-5 scores).
- No invented financial or operational data; trace every claim to longlist
  or bid response.
```

Save. About 35 lines.

### 5b. Write savings-calculator

**Step 5.** Create `practice/skills/savings-calculator.md`:

```
# savings-calculator

## What this skill does

Computes the annualised savings against the baseline if a named bidder
or panel were awarded the contract. Use once you have a recommended
panel from bid-scorer plus baseline data.

## Inputs

inputs/spend-baseline.csv
  Columns: shipment_id, carrier_id, mode, from_location, to_location,
  total_gbp, ship_date. Around 1,500 rows of historical shipments.

outputs/bid-comparison.md (to read the bidders' annual values).

inputs/category-brief.md (to read the savings target).

## Process

1. Sum total_gbp from spend-baseline.csv across the last 12 months. This
   is the baseline.
2. Read the bid comparison for each bid's annual value.
3. For the recommended panel (top three from bid-scorer, plus the air
   winner if separate), sum their annual values. This is the proposed
   spend.
4. Compute annualised savings = baseline minus proposed spend.
5. Compute the saving percentage = savings / baseline.
6. Compare against the savings target named in the category brief.
7. Note any one-off implementation costs from the bids; subtract those
   from Year 1 savings to produce risk-adjusted Year 1 savings.

## Output format

Save outputs/savings-case.md. Three sections:
- Headline (one paragraph, 50 words): baseline figure, proposed figure,
  savings figure (GBP and %), comparison against target.
- Calculation (a small table with: Baseline, Proposed, Savings, Year 1
  implementation, Year 1 risk-adjusted savings, Year 2+ run-rate savings).
- Sensitivity (one paragraph, 80 words): named bidder substitutions and
  the savings impact of each.

Cap at 400 words excluding the table.

## Quality criteria

- The baseline figure is computed from spend-baseline.csv (sum of
  total_gbp). Show the row count used.
- Every figure has a source named.
- Savings percentage is computed, not invented.
- The headline names whether the savings target (from category brief)
  is met, narrowly missed, or exceeded.
```

Save. About 45 lines.

### 5c. Write award-memo

**Step 6.** Create `practice/skills/award-memo.md`:

```
# award-memo

## What this skill does

Produces a one-page award recommendation memo, drawing on the bid
comparison, the risk profile, and the savings case. Use as the final
step of any sourcing event before the panel meeting.

## Inputs

outputs/bid-comparison.md (from bid-scorer).
outputs/risk-profile.md (from risk-profiler).
outputs/savings-case.md (from savings-calculator).
inputs/category-brief.md (for the goal and stakeholders).
templates/award-memo-template.md (skeleton).

## Process

1. Read all four input files. Build a single mental model of the bid
   landscape, the risks, and the savings.
2. Draft the recommendation. The recommendation must name a four-carrier
   panel: one road FTL, one road LTL or pallet, one sea FCL, one air.
3. For each recommended carrier, name the contract value, the key
   strength, and a mitigation for the highest risk identified by
   risk-profiler.
4. Construct the bid comparison summary (top 3 bidders by score).
5. Pull three named risks from risk-profiler with mitigations.
6. Pull the savings case headline and sensitivity from savings-case.md.
7. Construct a process and decisions paragraph (one paragraph, 80 words)
   naming the evaluators, dates, and source documents.
8. Build the audit footer.

## Output format

Save outputs/award-memo.md. Six sections, in order:
- Recommendation (50 to 80 words).
- Bid comparison summary (top 3 bidders, one line each).
- Risks and mitigations (three named risks with mitigation owner).
- Savings case (one paragraph plus a one-row table: Baseline, Proposed,
  Savings, % of target).
- Process and decisions (80 words).
- Audit footer (five lines: Generated, Source files, Model, Operator,
  Output path).

Cap the body at 500 words excluding the audit footer.

## Quality criteria

- The recommendation names a four-carrier panel covering all four
  required modes.
- Every recommended carrier has a contract value drawn from
  bid-comparison.md or savings-case.md.
- Three risks are named, each with a mitigation owner. No more than three.
- The savings figure matches the headline in savings-case.md.
- The audit footer is present.
- Total length is 4 to 5 paragraphs of body plus the table plus the footer.
```

Save. About 55 lines.

## Run the chain end to end

**Step 7.** Confirm all five skills are in place:

```
ls skills
```

You should see: `README.md`, `award-memo.md`, `bid-scorer.md`, `list-incumbents.md`, `rfp-builder.md`, `risk-profiler.md`, `savings-calculator.md`. Seven items total (including the README and the toy list-incumbents from Lesson 2).

**Step 8.** Start Claude in the practice folder:

```
claude
```

**Step 9.** Run the full chain. Type:

```
Run my full sourcing-event skill chain in this order.
1. Use the rfp-builder skill on inputs/category-brief.md and
   inputs/supplier-longlist.csv. Save to outputs/rfp-package.md.
2. Use the bid-scorer skill on every file in bid-responses/.
   Save to outputs/bid-comparison.md.
3. Use the risk-profiler skill on bid-responses/ and
   inputs/supplier-longlist.csv. Save to outputs/risk-profile.md.
4. Use the savings-calculator skill on inputs/spend-baseline.csv and
   outputs/bid-comparison.md. Save to outputs/savings-case.md.
5. Use the award-memo skill on the four outputs above plus
   inputs/category-brief.md and templates/award-memo-template.md.
   Save to outputs/award-memo.md.

After each step, run the quality criteria from the matching skill and
report any failures before moving to the next step.
```

Press Enter.

Wait. Claude runs the five skills in order. Each step reads inputs and produces an output. Total time: 4 to 7 minutes.

**What you should see.** Five confirmations, one per step. Each confirmation names the output file produced and any quality criteria results. By the end, `practice/outputs/` contains five new files (or six if rfp-package was overwritten).

**Step 10.** Open `outputs/award-memo.md`. Read the recommendation. It should name four carriers covering road FTL, road LTL or pallet, sea FCL, and air. The contract values should sum to roughly 9.6m GBP (close to the 11.2m baseline minus the 1.6m savings target). Three risks. A savings figure that matches the savings-case file.

**Step 11.** Quit Claude (`/quit`).

## What just happened, in plain words

1. You ran five skills in one session.
2. Each skill produced one file. The next skill read that file plus other inputs.
3. The chain produced six deliverables in seven minutes.
4. Doing the same work without skills would take about three weeks.

This is what skill composition looks like in practice. Each skill is small. Together they are a sourcing event.

## Three things that trip beginners up

- **The chain stopped at step 3.** Risk-profiler depends on bid-comparison.md, which Step 2 produced. If Step 2 failed quality criteria, Step 3 cannot run cleanly. Re-run Step 2 with the gap fixed before continuing.
- **The award memo recommended only one carrier.** You need a panel of four. The award-memo skill must say "name a four-carrier panel covering road FTL, road LTL or pallet, sea FCL, and air". If your skill says "name the recommended carrier", you get one. Tighten the skill.
- **The savings figure does not match the savings case.** Award-memo must read savings-case.md and quote it directly. If award-memo recomputes savings on its own, the figures drift. Add a quality criterion: "savings figure matches the headline in savings-case.md".

## You are done with Lesson 5 when

- All five skills are in `practice/skills/` and each is between 40 and 90 lines.
- Six deliverables are in `practice/outputs/`: rfp-package.md, bid-comparison.md, risk-profile.md, savings-case.md, award-memo.md (you may also have a category-brief copy from rfp-builder).
- The award memo recommends a four-carrier panel, names three risks, and quotes the savings figure from savings-case.md.
- You can copy your `skills/` folder into your real procurement project and run the same chain on a new sourcing event.

Take a break. Move to Lesson 6 next, a short one about updating skills without breaking the chain.
