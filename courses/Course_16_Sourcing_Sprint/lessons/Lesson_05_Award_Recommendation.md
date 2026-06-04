# Lesson 5: Award Recommendation

**Time:** 35 minutes.

## The recommendation your CPO will question

It is 14:00 Wednesday of week three at Ironbridge Manufacturing. You have the evaluation matrix from Lesson 4. Titan Precision LLC is the top-ranked supplier with a weighted score of 87.4. Cascade Metals is second at 83.1. Your CPO will ask three questions: "Why Titan?", "What if the second-place supplier challenges?", and "What about the risk of moving volume from our incumbent?" If your recommendation says "Titan scored highest" and nothing else, it will not survive the meeting. You need a defensible document that names the winner, justifies the selection, anticipates objections, and presents the savings case.

## What Claude Code is going to do for you

Claude Code reads the evaluation matrix, the pricing comparison, and the technical scores, then writes a complete award recommendation document. The document names the recommended supplier, states the savings versus baseline, addresses the three most likely objections with data-backed responses, and includes a risk section covering transition, incumbent reaction, and dual-source strategy.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_16_Sourcing_Sprint/practice/`.
3. `Drafts/bid_evaluation_matrix.csv`, `Drafts/pricing_comparison.json`, `Drafts/technical_scores.json` from Lesson 4.
4. `spend-baseline.csv` and `CLAUDE.md` with sourcing context.

## Step-by-step

### Build the recommendation narrative

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt with the full sourcing context.

**Step 2.** Generate the award recommendation.

```
Read Drafts/bid_evaluation_matrix.csv, Drafts/pricing_comparison.json, and Drafts/technical_scores.json. Write an award recommendation document to Drafts/award_recommendation.md with these sections:

1. Executive Summary: name the recommended supplier, state the total annual contract value, the savings versus baseline (dollar amount and percentage), and the recommended contract term. Include the decision deadline (2026-06-06).

2. Evaluation Results: a summary table showing all six suppliers ranked by weighted score. Highlight the top two.

3. Recommended Supplier Profile: the winner's pricing position, technical scores with justifications, and any notable strengths.

4. Savings Analysis: total annual savings versus baseline, savings by part number for the top five parts, and projected savings over the 24-month contract term.

5. Anticipated Objections: three likely objections (e.g., "Why not stay with the incumbent?", "The second-place bid is close in price", "The recommended supplier has no history with Ironbridge") and a data-backed response to each.

6. Risk Assessment: three risks specific to this award with likelihood, impact, and mitigation. Risks should cover transition disruption, quality during ramp-up, and supplier financial stability.

7. Recommendation: a clear, one-paragraph statement recommending award to the named supplier, with conditions if applicable.
```

You should see Claude write the full recommendation document.

**Step 3.** Verify the numbers.

```
Read Drafts/award_recommendation.md. Check: (1) the total annual contract value matches the winning bid's total from pricing_comparison.json, (2) the savings percentage is correctly calculated against the spend baseline, (3) the evaluation scores match bid_evaluation_matrix.csv. Report any discrepancies.
```

You should see Claude confirm all numbers are consistent, or flag specific discrepancies for correction.

**Step 4.** Strengthen the objection responses.

```
Read the Anticipated Objections section of Drafts/award_recommendation.md. For each objection, ensure the response includes at least one specific number (a score, a dollar amount, or a percentage) and references a specific data source (the evaluation matrix, the pricing comparison, or the technical scores). If any response is generic, rewrite it with data.
```

You should see improved objection responses with specific references.

### Create the CPO briefing summary

**Step 5.** Write a one-page executive brief.

```
Write Drafts/cpo_briefing.md as a one-page summary for the CPO. Include: (1) the recommendation in one sentence, (2) total annual savings and percentage, (3) the top two suppliers and their scores, (4) the decision deadline (2026-06-06), (5) three conditions for award (e.g., satisfactory reference checks, first article approval, insurance certificate). No section longer than three lines.
```

You should see a tight one-page brief.

**Step 6.** Generate the supplier notification drafts.

```
Write two notification drafts:
1. Drafts/notification_winner.md: a letter to the winning supplier confirming intent to award, subject to final contract negotiation. Include the contract value, term, and next steps (contract drafting timeline).
2. Drafts/notification_unsuccessful.md: a template letter for unsuccessful bidders thanking them, offering a debrief session, and noting they remain on the qualified supplier list. Do not name the winning supplier.
```

You should see two professional letters.

**Step 7.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── spend-baseline.csv
├── Drafts/
│   ├── bid_evaluation_matrix.csv (6 suppliers ranked)
│   ├── pricing_comparison.json
│   └── technical_scores.json
├── CLAUDE.md (with sourcing context)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── award_recommendation.md (7-section document)
│   ├── cpo_briefing.md (one-page summary)
│   ├── notification_winner.md
│   └── notification_unsuccessful.md
```

**What Claude did, behind the scenes:**

1. Claude read the evaluation matrix and identified the top-ranked supplier by weighted score.
2. It pulled the winner's total bid value from the pricing comparison and calculated savings against the $2.4M baseline.
3. It projected savings over the 24-month contract term.
4. It generated three objections by identifying the most likely challenges: incumbent preference (the current supplier scored lower but has a track record), close competition (the second-place supplier's score gap), and new supplier risk (no prior relationship).
5. For each objection, it pulled specific data points from the evaluation files to build the response.
6. It assessed three transition risks and proposed specific mitigations (pilot order, quality gate at first article, staged volume transfer).

## Common mistakes and how to recover

- **Symptom:** The savings figure in the executive summary does not match the savings analysis section. **Fix:** both sections should calculate from the same baseline. Ask Claude to "Use the total from spend-baseline.csv as the baseline. Recalculate savings consistently across all sections."

- **Symptom:** The objection responses are vague ("Titan scored higher on quality"). **Fix:** require data: "Titan scored 92 on quality vs. the incumbent's 71, driven by ISO 13485 certification and a 0.2% defect rate vs. the incumbent's 1.1%."

- **Symptom:** The recommendation includes more than three conditions. **Fix:** the CLAUDE.md rules cap recommendation lists at three unless the document is explicitly labeled as a ranked priority list. Remove conditions beyond three, or rank and label the list.

- **Symptom:** The unsuccessful bidder letter accidentally reveals the winner's identity or bid price. **Fix:** review the letter carefully. Ask Claude to "Remove any reference to the winning supplier's name, bid value, or ranking from notification_unsuccessful.md."

- **Symptom:** The risk assessment uses passive voice ("It was determined that transition risk exists"). **Fix:** rewrite in active voice: "We assessed three risks specific to this award. The highest risk is production disruption during the 8-week transition from Atlas Metalworks to Titan Precision."
