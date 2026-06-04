# Lesson 4: Writing the bid-scorer skill

**Time:** 60 minutes. **You need:** Lesson 3 complete.

## A typical Thursday morning

It is 09:00 Thursday. The RFP went out three weeks ago. Yesterday afternoon, six bids landed in your inbox: FastRoad UK, Globex Freight, Continental Roads, OceanLine, Pacific Forwarders, Helios Air Freight. Each one is a 4-page document with an executive summary, capability statement, pricing table, references, and terms.

Yesterday you read the first one in detail. You took 90 minutes. You started reading the second one and gave up; the format was different and you could not compare like-for-like.

Today you write a skill that scores all six bids in 5 minutes. Each bid gets a weighted score against the same criteria. The skill tells you the top three and why.

## The big idea

A scoring skill is the same shape as the rfp-builder you wrote yesterday: five sections (what it does, inputs, process, output format, quality criteria). The difference is that the inputs are now **multiple files of the same shape** (six bid responses) instead of one file. The skill processes each bid the same way, then ranks them.

This is where skills shine. Six bids, the same methodology applied to each, ranked into one comparison table. No human can do that consistently across six documents in 30 minutes; a skill does it in 60 seconds.

## Set up

**Step 1.** Open your terminal.

**Step 2.** Move to the practice folder:

```
cd "Course_03_The_Skill_Builder/practice"
```

**Step 3.** Look at the bid responses you will score:

```
ls bid-responses
```

You should see six files: BID_CAR001_FastRoad_UK.md, BID_CAR003_OceanLine.md, BID_CAR008_Pacific_Forwarders.md, BID_CAR010_Globex_Freight.md, BID_CAR012_Helios_Air_Freight.md, BID_CAR017_Continental_Roads.md.

**Step 4.** Open one bid response (any one). Read it. Notice the structure: every bid has the same six sections in the same order. That is what makes them scoreable.

**Step 5.** Open `templates/scorecard-template.md`. Read it. The skeleton has eight columns: Bidder, Price (40%), Service (25%), Capability (20%), Sustainability (10%), Implementation (5%), Total, Recommended.

## Write the bid-scorer skill

**Step 6.** Create a new file at `practice/skills/bid-scorer.md`.

**Step 7.** Type the title and the first section:

```
# bid-scorer

## What this skill does

Scores every bid response in a folder using a fixed weighted criteria set,
then ranks them. Use this skill once after all bids are received and the
bid-responses folder is complete. The skill produces a single comparison
table with weighted scores, plus a one-paragraph commentary per bid.
```

Save.

**Step 8.** Add the inputs section:

```
## Inputs

bid-responses/*.md
  Multiple bid response files, one per bidder. Each file follows the same
  six-section structure: Executive summary, Capability statement, Pricing
  table, Service commitments, Contract terms, References. The pricing
  table has columns: Lane, Mode, Volume per year, Unit rate (GBP per
  shipment), Annual value (GBP).

inputs/supplier-longlist.csv
  Used to look up the carrier_id from the bid filename and pull
  background data: capacity_tier, financial_health, otd_pct_12m, incumbent.
  Columns: carrier_id, carrier_name, modes, primary_geography,
  certifications, capacity_tier, financial_health, otd_pct_12m,
  contract_terms_offered, incumbent.

templates/scorecard-template.md
  Skeleton with eight columns. Use as the structure for the output table.
```

Save.

**Step 9.** Add the process section. This is the longest part:

```
## Process

1. List every file in bid-responses/. For each file, extract the carrier_id
   from the filename (the BID_CARxxx prefix).
2. For each bid, score the five criteria below. Each score is 0 to 100
   before weighting.

3. Score Price (40% weight):
   - Read the pricing table. Sum the Annual value (GBP) column.
   - The lowest total annual price among the six bids gets 100. The
     highest gets 60. Linear interpolation between.
   - If the implementation cost is non-zero, deduct (implementation /
     total annual) percentage points, capped at 10 points.

4. Score Service (25% weight):
   - Read the on-time delivery commitment from the bid.
   - 95% or higher = 90 to 100. 92 to 95% = 75 to 89. Below 92% = 60 to 74.
   - Adjust by damage rate: subtract 5 points per 1% damage rate above 1%.
   - Adjust by invoice accuracy: subtract 3 points per 1% below 99%.

5. Score Capability (20% weight):
   - Read the bidder's modes from the longlist (carrier_id lookup).
   - Multi-mode capability that matches our scope adds points; single-mode
     restricts the score.
   - 4 or more in-scope modes = 90 to 100. 2 or 3 modes = 75 to 89.
     1 mode = 60 to 74.
   - Adjust by capacity_tier: tier_1 = +5, tier_2 = 0, tier_3 = -5.
   - Adjust by financial_health: strong = +5, stable = 0, weak = -10.

6. Score Sustainability (10% weight):
   - Read the bid's sustainability section.
   - SBT-aligned + carbon neutral verified = 90 to 100.
   - Carbon-neutral committed but not verified = 75 to 89.
   - No specific commitments = 60 to 74.

7. Score Implementation (5% weight):
   - Read the bid's implementation cost and timeline.
   - Implementation cost zero = 90 to 100.
   - Implementation cost up to 1% of annual = 75 to 89.
   - Implementation cost over 1% of annual = 60 to 74.

8. Compute the weighted total per bidder:
   Total = (Price * 0.40) + (Service * 0.25) + (Capability * 0.20)
         + (Sustainability * 0.10) + (Implementation * 0.05).

9. Sort bidders by Total, descending.

10. Mark the top three Recommended = "Yes". The rest "No".

11. For each bidder, write a one-paragraph commentary (50 to 80 words)
    that names the strongest score, the weakest score, and the
    decision-relevant trade-off.
```

Save. The skill is now around 65 lines.

**Step 10.** Add the output format section:

```
## Output format

Save outputs/bid-comparison.md.

Structure:
- Title: Bid comparison - <category name from category-brief.md>.
- Section 1: Comparison table. Eight columns matching the scorecard
  template. Rows sorted descending by Total.
- Section 2: Commentary. One paragraph per bidder, in score order.
- Section 3: Top three summary. Three bullet points naming the top three
  bidders, the total score, and the headline reason each is recommended.

Cap the file at 600 words excluding the table.

Add an audit footer at the bottom (separated from the body by a row of
three dashes) with five lines: Generated, Source files, Model, Operator,
Output path.
```

Save.

**Step 11.** Add the quality criteria section:

```
## Quality criteria

- Every bidder in bid-responses/ appears as a row in the comparison table.
  No bid is silently dropped.
- Every score is between 60 and 100. No criterion is left blank.
- The weighted total for every row equals (P*0.40 + S*0.25 + C*0.20 +
  Sus*0.10 + I*0.05). Round each total to one decimal place.
- The top three are marked Recommended = "Yes" and the others "No".
- Each commentary names the strongest and weakest score for that bidder,
  drawn from the scoring above. No invented strengths or weaknesses.
- The audit footer is present and has all five lines.
```

Save. Final file should be around 75 to 85 lines.

## Test the skill: run it

**Step 12.** Start Claude in the practice folder:

```
claude
```

**Step 13.** Type:

```
Use the bid-scorer skill in skills/bid-scorer.md. Process every file in
bid-responses/. Save the output to outputs/bid-comparison.md.
```

Press Enter.

Wait. Claude reads each of the six bid responses (about 2.5 KB each), reads the longlist for capability data, computes five scores per bid, applies the weights, sorts, and produces the comparison table. This takes 90 to 120 seconds.

**What you should see.** A confirmation that `outputs/bid-comparison.md` has been written.

**Step 14.** Open `outputs/bid-comparison.md`. Read the table. The top three bidders should be (within reasonable variation):

- **Continental Roads** - high score driven by lowest annual price (1.25m GBP) plus solid 95.0% OTD plus strong service commitments. But not an incumbent, so capability and trust scores are slightly lower.
- **FastRoad UK** - second on price (1.41m GBP), highest capability (multi-mode incumbent with strong OTD), strong sustainability.
- **Globex Freight** - third overall. Higher price than Continental but stronger sustainability and longer-term commitment.
- **Helios Air Freight** - separate from the road three; wins the air lane category (98.6% OTD, IATA-certified).
- **OceanLine and Pacific Forwarders** - separately compete on the sea FCL lane; Pacific scores slightly higher on price.

The exact totals will vary because Claude has some discretion within the scoring bands, but the ordering should be stable across runs.

**Step 15.** Open one of the bid commentaries. Read it. The commentary should name the bidder's strongest and weakest score and the decision-relevant trade-off. Examples of good commentary:

> "Continental Roads scores highest on Price (98) by undercutting the road incumbents by 11.8% on equivalent lanes. Their weakest score is Capability (74), reflecting non-incumbent status and a smaller depot network. The trade-off is short-term saving versus integration risk; they offset this with a 4% performance-based fee at risk in Year 1."

**Step 16.** Quit Claude (`/quit`).

## Compare against the solution

**Step 17.** Open `solutions/bid_scorer_solution.md`. Compare against your file. The solution is one good answer; yours is another. Borrow scoring rules where the solution is sharper.

## What just happened, in plain words

1. You wrote 80 lines of methodology.
2. Claude applied that methodology consistently to six bid responses.
3. The output is a comparison table you can take to the panel meeting.
4. Next event, you point the same skill at a new `bid-responses/` folder. The skill works without modification because it names input shapes, not specific files.

## Three things that trip beginners up

- **Your scoring bands are vague ("medium" and "high").** Numbers (60-74, 75-89, 90-100) are the only way the skill produces consistent scores across runs.
- **You wrote one row of commentary that says "good bid".** Commentary that does not name the strongest and weakest score is filler. Re-run with the constraint enforced.
- **One bidder did not appear in the table.** The skill did not list every file in bid-responses/. Add a quality check: "the table has the same number of rows as files in bid-responses/".

## You are done with Lesson 4 when

- `practice/skills/bid-scorer.md` is your file, 75 to 90 lines, with the five sections.
- You ran the skill and produced `practice/outputs/bid-comparison.md`.
- The table has six rows (one per bid), ranked by total, with the top three flagged Recommended.
- Each commentary names the strongest and weakest score.
- The audit footer is present.

Take a break. Move to Lesson 5 next, the finale: chain three skills together to produce a complete sourcing event package.
