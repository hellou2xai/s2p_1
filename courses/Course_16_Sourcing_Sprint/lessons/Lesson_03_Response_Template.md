# Lesson 3: Response Template

**Time:** 30 minutes.

## The bid that arrived as a 47-page PDF

It is 09:00 Wednesday, day three of your sourcing sprint at Ironbridge Manufacturing. You sent the RFP to 12 suppliers on the longlist. The first response arrives from Titan Precision LLC: a 47-page PDF with pricing buried in paragraph text on page 23, quality certifications as scanned images, and delivery commitments scattered across three different sections. Extracting comparable data from this format will take an hour per bid. With six bids expected, that is six hours of manual data entry before you can even start comparing. You need a response template that forces structured, machine-readable answers.

## What Claude Code is going to do for you

Claude Code generates a response template that makes every bid file processable by Claude Code in Lesson 4. The template defines exact column headers, field formats, and validation rules. Suppliers fill in the template. Claude reads the template. No manual extraction needed.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_16_Sourcing_Sprint/practice/`.
3. `CLAUDE.md` with the Sourcing Event Context from Lesson 1.
4. `Drafts/RFP_03_Pricing_Template.md` from Lesson 2.

## Step-by-step

### Design the pricing response template

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Create the pricing response template as a CSV structure.

```
Read Drafts/RFP_03_Pricing_Template.md and spend-baseline.csv. Create Drafts/response_template_pricing.csv with these pre-filled columns: part_number (from spend-baseline.csv, all unique part numbers), description (from spend-baseline.csv), unit_of_measure, annual_volume (from spend-baseline.csv). Leave these columns blank for the supplier to fill: unit_price_usd, total_annual_price, tooling_cost_usd, freight_terms, lead_time_days, minimum_order_quantity. Include a header row and one example row filled in with sample data.
```

You should see a CSV with all part numbers pre-populated and blank supplier columns. The example row shows the expected format.

**Step 3.** Create the technical response template.

```
Create Drafts/response_template_technical.csv with these columns: question_id (T1 through T10), question (pre-filled), response (blank for supplier). Pre-fill these questions:
T1: Describe your ISO 9001 or equivalent quality certification (include certificate number and expiry date).
T2: What is your current defect rate (PPM) for precision-machined steel parts?
T3: List your three largest customers for similar parts, with annual volumes.
T4: Describe your inspection process for machined tolerances.
T5: What is your standard lead time for first article and production orders?
T6: Describe your capacity for this category (current utilization percentage and maximum monthly units).
T7: Do you have secondary or backup production capability? If yes, describe.
T8: Describe your freight and logistics capabilities to Detroit, MI.
T9: Provide your Dun and Bradstreet number and most recent credit rating.
T10: Describe any value-add services (kitting, consignment, VMI) you offer.
```

You should see a CSV with 10 pre-filled questions and blank response columns.

### Create the response instructions

**Step 4.** Write supplier instructions for completing the templates.

```
Write Drafts/response_instructions.md with these sections:

1. File Naming: Suppliers must name their files as: <SupplierName>_Pricing.csv and <SupplierName>_Technical.csv. No spaces in names, use underscores.
2. Pricing Rules: all prices in USD, no formulas in cells, total_annual_price must equal unit_price_usd times annual_volume, tooling costs are one-time and separate from unit pricing.
3. Technical Rules: answer every question in the response column, if a question does not apply write "N/A" with a reason.
4. Submission: both files submitted together by the deadline (2026-05-09).
5. Validation: before submitting, suppliers should verify that total_annual_price = unit_price_usd x annual_volume for every row.
```

You should see clear, specific instructions that leave no room for misinterpretation.

### Add processing rules to CLAUDE.md

**Step 5.** Tell Claude Code how to process incoming responses.

```
Append to CLAUDE.md a section called "## Bid Response Processing Rules" with:

1. Bid files arrive in bid-responses/ folder.
2. Pricing files are CSVs with the exact column structure from response_template_pricing.csv.
3. Technical files are CSVs with the exact column structure from response_template_technical.csv.
4. When processing a bid, validate: (a) all required columns present, (b) no blank unit_price_usd values, (c) total_annual_price equals unit_price_usd x annual_volume within $1 tolerance, (d) all 10 technical questions answered.
5. Score each bid against the evaluation criteria weights in CLAUDE.md.
```

You should see Claude append the processing rules.

**Step 6.** Verify the template is complete by simulating a supplier response.

```
Read Drafts/response_template_pricing.csv. Fill in the blank columns with realistic sample data for a fictional supplier called "Sample Supplier Inc." Save as Drafts/sample_bid_pricing.csv. Use prices that are 5-10% below the current spend-baseline.csv average per part.
```

You should see a complete sample bid that demonstrates the expected format.

**Step 7.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── spend-baseline.csv (356 rows)
├── Drafts/
│   └── RFP_03_Pricing_Template.md
├── CLAUDE.md (with sourcing context)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── response_template_pricing.csv
│   ├── response_template_technical.csv
│   ├── response_instructions.md
│   └── sample_bid_pricing.csv
├── CLAUDE.md (updated with bid processing rules)
```

**What Claude did, behind the scenes:**

1. Claude read the pricing template from Lesson 2 and the unique part numbers from `spend-baseline.csv`.
2. It pre-populated the pricing CSV with part numbers, descriptions, and annual volumes so suppliers only need to fill in their pricing.
3. It created 10 technical questions mapped to the four evaluation criteria (quality, delivery, financial stability, value-add).
4. It wrote processing rules so that Lesson 4's bid scoring can be automated.
5. It generated a sample bid by reading current average prices and applying a 5-10% reduction to simulate a competitive response.

## Common mistakes and how to recover

- **Symptom:** Suppliers return the pricing template with extra columns or renamed headers. **Fix:** the response instructions should state: "Do not add, remove, or rename any columns. Use the template exactly as provided."

- **Symptom:** The sample bid has prices that do not look realistic for machined steel parts. **Fix:** use the current spend data as a baseline. Ask Claude to "Read spend-baseline.csv, calculate the average unit price per part, and set the sample bid prices at 92% of that average."

- **Symptom:** Technical question T9 (Dun and Bradstreet number) gets "N/A" from every supplier. **Fix:** this is a real possibility for smaller suppliers. The instructions should say: "If you do not have a D&B number, provide your most recent audited financial statement instead."

- **Symptom:** The bid processing rules in CLAUDE.md do not match the template columns. **Fix:** after writing both, ask Claude to "Read response_template_pricing.csv headers and the Bid Response Processing Rules in CLAUDE.md. Confirm they reference the same column names."
