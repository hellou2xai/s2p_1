# Writing the CFO Memo

It is 16:00 Friday. You have the YTD savings, the variance by initiative, and three Q4 scenarios. Now you need to write the memo. Your CFO reads memos bottom-up: she looks at the headline number first, then the table, then the narrative. If the headline number is buried on page two, she will not find it. If the variance explanation starts with "despite challenging market conditions," she will stop reading. You need a one-page memo that leads with the number, explains the gaps without excuses, and gives her three actions she can approve on Tuesday.

## The S2P problem

Most savings memos are written defensively. They start with context, explain the methodology, describe each initiative in three paragraphs, and bury the headline number in a summary at the end. The CFO reads the first paragraph, skips to the last page, and asks the question the memo should have answered on line one: "Are we going to hit the target?" A memo that does not answer that question in the first sentence is a memo that wastes executive time.

## What Claude Code does for you

Claude Code drafts a CFO memo that follows a strict format: headline number in the first sentence, initiative variance table, three-scenario projection, and exactly three recommended actions. The format is encoded in CLAUDE.md, so every monthly memo follows the same structure. No filler. No excuses. The CFO gets the number, the gap, the outlook, and the ask.

## Set up

1. Lessons 1 through 3 completed. `Drafts/savings-summary-ytd.csv` and `Drafts/scenario-projections.csv` exist.
2. Claude Code open in `Course_18_Savings_Program_Management/practice/`.
3. CLAUDE.md has the reporting standards and scenario definitions.

## Step-by-step

### Step 1. Review the reporting standards in CLAUDE.md.

```
Read CLAUDE.md and show me the reporting standards section.
```

You should see rules including: lead with the headline number, show variance by initiative, CFO memo format (headline, initiative table, three scenarios, three actions), and no filler.

### Step 2. Draft the headline paragraph.

```
Using Drafts/savings-summary-ytd.csv and Drafts/scenario-projections.csv, write the opening paragraph of the CFO memo. The first sentence must state the YTD realized savings, the annual target, and the current trajectory. The second sentence must name the gap. The third sentence must state the range of full-year outcomes across the three scenarios. No more than three sentences.
```

You should see something like: "Apex Procurement has realized $6,855,836 in savings YTD against a $12,000,000 annual target. The program is $2,144,164 behind the YTD target of $9,000,000. Full-year projections range from $8.8M (risk-adjusted) to $9.8M (upside), leaving a gap of $2.2M to $3.2M."

### Step 3. Build the initiative variance table.

```
Create a markdown table for the memo showing all 8 initiatives with columns: Initiative, Type, YTD Target, YTD Realized, Variance, Status. Sort by variance (largest negative first). Add a totals row.
```

You should see SAV-002 (Logistics RFP) and SAV-007 (Spec Standardization) at the top with the largest negative variances.

### Step 4. Add the scenario projection section.

```
Add a section titled "Q4 Outlook: Three Scenarios" to the memo. Show a compact table with columns: Scenario, Full-Year Projection, Gap to Target. List base, upside, and risk-adjusted. Below the table, write one sentence per scenario explaining the key assumption.
```

You should see three rows with the projections and one-sentence explanations.

### Step 5. Write three recommended actions.

```
Write exactly three recommended actions for the CFO. Each action must name the initiative, the specific step, the expected recovery amount, and the deadline. Format as a numbered list. Do not exceed three items.
```

You should see three actions, such as: (1) Renegotiate the Logistics RFP contract with Patriot Logistics by 2026-05-15 to recover $200,000 in Q4. (2) Approve the two specification changes for SAV-007 by 2026-05-01 to recover $150,000. (3) Implement the revised travel policy for SAV-006 effective 2026-05-01 to recover $80,000.

### Step 6. Assemble and save the complete memo.

```
Combine the headline paragraph, initiative variance table, Q4 outlook section, and recommended actions into a single memo. Title it "Savings Program Review: Q3 YTD and Q4 Outlook." Save it to Drafts/cfo-memo-savings-review.md.
```

You should see the complete memo saved. It should be no longer than one page when printed.

## Worked example

**Starting files:**
- `Drafts/savings-summary-ytd.csv` with 8 initiatives.
- `Drafts/scenario-projections.csv` with three scenarios.
- `CLAUDE.md` with reporting standards.

**What you type:**

```
Draft the CFO savings memo using Drafts/savings-summary-ytd.csv and Drafts/scenario-projections.csv. Follow the format in CLAUDE.md exactly: headline number first, initiative variance table sorted by largest gap, three-scenario outlook table, and exactly three recommended actions with dollar amounts and dates. Save to Drafts/cfo-memo-savings-review.md.
```

**What you should see:** A memo starting with the realized savings figure, a table of 8 initiatives sorted by variance, a three-row scenario table, and three numbered actions.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the reporting standards and memo format rules.
2. Read Drafts/savings-summary-ytd.csv to get YTD realized and variance by initiative.
3. Read Drafts/scenario-projections.csv to get the three full-year projections.
4. Wrote the headline paragraph with the YTD number, gap, and projection range.
5. Built the variance table sorted by largest negative variance first.
6. Added the scenario table with one-sentence assumption explanations.
7. Wrote three actions, each naming the initiative, step, dollar amount, and deadline.

## Common mistakes and how to recover

- **Symptom:** The memo starts with background context instead of the headline number. **Fix:** Delete the first paragraph and start with the dollar figure. The CFO does not need context. She set the target.

- **Symptom:** The variance explanation uses phrases like "due to challenging market conditions." **Fix:** Name the specific cause. "SAV-002 is $602,435 behind target because fuel surcharges increased 12% in Q2 and the renegotiation window opens in May" is a fact. "Challenging conditions" is an excuse.

- **Symptom:** The memo has four or five recommended actions. **Fix:** Cut to three. The CLAUDE.md rules cap recommendations at three. Prioritize by dollar recovery potential.

- **Symptom:** The recommended actions do not include dollar amounts or dates. **Fix:** Every action needs a specific recovery figure and a deadline. "Renegotiate the logistics contract" is not an action. "Renegotiate with Patriot Logistics by 2026-05-15 to recover $200,000 in Q4" is an action.

- **Symptom:** The scenario section does not explain its assumptions. **Fix:** Each scenario needs one sentence naming the key assumption. The reader must be able to decide which scenario to believe.
