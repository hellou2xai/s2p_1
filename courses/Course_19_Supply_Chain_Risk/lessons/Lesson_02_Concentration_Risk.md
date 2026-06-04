# Lesson 02: Concentration Risk

## Opening scenario

It is 10:15 Wednesday. The scoring matrix is encoded. Your CPO calls back: "Good. Now tell me where we're exposed if something goes wrong in one region or with one supplier. I don't want a ranked list of 25. I want to know which single failure point would hurt us most." That question has three answers: share of wallet (which supplier takes the biggest slice of spend), geographic clustering (which state holds multiple suppliers that could go down together), and category dominance (which supplier controls more than half a category). You need all three in one pass.

## The S2P problem

Concentration risk is the most common blind spot in supply base management. A category manager knows their top supplier. They do not always know that the same supplier also appears in two other categories, making total exposure three times what any single category shows. Geographic concentration is worse: five suppliers in Texas look acceptable in a list. After a hurricane or a power grid failure, five suppliers offline simultaneously is a production crisis. Finding these patterns manually requires pivot tables across two files, cross-referencing spend by supplier, state, and category. With 25 suppliers and 200 line items, that takes hours.

## What Claude Code is going to do for you

Claude Code reads `data/supplier-master.csv` and `data/spend-by-item.csv` together. It calculates each supplier's share of total portfolio spend, identifies states with multiple suppliers, and flags any supplier that holds more than 50% of spend in a single category. You get three concentration views with specific dollar amounts and percentages. The output goes to `Drafts/concentration-risk-summary.md`, ready for the board brief in Lesson 6. This lesson takes about 50 minutes.

## Set up

1. Lesson 1 completed. CLAUDE.md has the full scoring matrix with scoring bands and data source mapping.
2. Claude Code open in `Course_19_Supply_Chain_Risk/practice/`. If you closed it, reopen:

```
cd "Course_19_Supply_Chain_Risk/practice"
claude
```

3. Confirm `data/supplier-master.csv` (25 suppliers) and `data/spend-by-item.csv` (200 items) are both present.
4. Confirm `Drafts/` folder exists. If it does not, ask Claude Code to create it before saving output.

Open the session with the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

## Step-by-step

### Step 1. Calculate supplier share of wallet.

Find which suppliers represent the largest portions of total annual spend.

```
Read data/supplier-master.csv. Calculate each supplier's percentage of total annual spend.
Sort by percentage descending. Show the top 10 in a table with columns:
supplier_name, annual_spend_usd, pct_of_total.
Flag any supplier above 10% of total spend as "concentrated."
```

You should see a table with Great Lakes Steel near the top at $4,200,000. Total portfolio spend across all 25 suppliers is approximately $52,050,000. A supplier above $5,205,000 would exceed 10%. If no supplier exceeds that threshold, Claude Code should report that the portfolio has no single-supplier concentration above the 10% flag. If you see a total that looks much lower than $52M, ask Claude to confirm it read all 25 rows.

### Step 2. Analyze geographic concentration.

Find which states hold multiple suppliers and what combined spend those states represent.

```
Read data/supplier-master.csv. Group suppliers by state. Show a table with columns:
state, supplier_count, combined_annual_spend_usd, pct_of_total.
Flag any state with 3 or more suppliers, or with more than 20% of total spend.
```

You should see Texas (Houston: Heartland Polymers, Austin: TechForward Solutions, Dallas: Frontier Plastics) flagged for having 3 suppliers. Illinois (Chicago: Great Lakes Steel, Chicago: Sterling Advisory) has 2. California (San Jose: Apex Electronics, San Francisco: CloudBridge Systems) has 2. If the state column is inconsistent ("TX" versus "Texas"), ask Claude to normalize to two-letter abbreviations before grouping.

### Step 3. Analyze category concentration.

Find suppliers that dominate individual categories by spend share.

```
Read data/spend-by-item.csv. Group spend by category. Within each category, calculate each
supplier's share of category spend. Flag any supplier holding more than 50% of spend in any
single category. Show a table with columns: category, supplier_name, supplier_spend_usd,
category_total_usd, supplier_share_pct. Sort by supplier_share_pct descending.
```

You should see one or more suppliers with a dominant share in raw-materials or logistics. A supplier holding 60% share in a single category is a concentration risk the board needs to understand. If spend-by-item.csv uses different supplier names from supplier-master.csv, Claude Code will split one supplier into two and hide the concentration. Ask it to flag any name that appears in spend-by-item.csv but not in supplier-master.csv.

### Step 4. Build a combined concentration risk summary.

Combine all three views into a single structured document.

```
Combine the three concentration analysis results into a risk summary. For each type (share of wallet,
geographic, category), list the top 3 findings. Each finding must name the specific supplier
or state, state the dollar amount, and state the percentage. Save to
Drafts/concentration-risk-summary.md.
```

You should see a three-section document saved to `Drafts/`. Each section holds three findings. If any finding lacks a dollar amount or percentage, ask Claude to go back and fill in the number. A statement like "high concentration in raw-materials" is not a finding.

### Step 5. Identify suppliers that appear in more than one risk view.

Find the suppliers whose failure would create the widest exposure across all three concentration types.

```
Which supplier or suppliers appear in more than one concentration risk category
(share of wallet, geographic, or category dominance)? Name each one, list the
concentration types they appear in, and state their combined exposure in dollars.
```

You should see at least one supplier that crosses two views. Great Lakes Steel or Heartland Polymers are likely candidates. The combined exposure for a multi-view supplier is the most important number in this analysis.

### Step 6. Add concentration thresholds to CLAUDE.md.

Document the thresholds so every future session applies the same rules.

```
Add a "Concentration risk thresholds" section to CLAUDE.md with these rules:
- Share of wallet: flag any supplier above 10% of total spend.
- Geographic: flag any state with 3 or more suppliers or above 20% of total spend.
- Category: flag any supplier with above 50% share in any single category.
Save CLAUDE.md.
```

You should see CLAUDE.md updated with the concentration thresholds section. Confirm by asking Claude to read CLAUDE.md and show the new section.

## Worked example

**Starting files:**
- `data/supplier-master.csv` with 25 suppliers, including state, annual_spend_usd, and category columns.
- `data/spend-by-item.csv` with 200 items, including category, supplier_name, and annual_spend_usd columns.

**What you type:**

```
Which supplier has the highest share of wallet across the Fortis Manufacturing portfolio?
Name the supplier, their annual spend, their percentage of total spend, and whether they
also appear as a geographic or category concentration risk.
```

**What you should see:**

Great Lakes Steel at $4,200,000, representing approximately 8.1% of total portfolio spend. No single supplier exceeds the 10% threshold. Great Lakes Steel is in Chicago, Illinois, alongside Sterling Advisory, so Illinois holds 2 suppliers. Not flagged for geographic concentration (threshold is 3 or more). In the raw-materials category, Great Lakes Steel holds the largest raw-materials share. If raw-materials spend from all suppliers totals approximately $16,680,000, Great Lakes Steel's $4,200,000 share is 25.2% of that category, below the 50% flag.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the concentration risk thresholds (10% share of wallet, 3+ suppliers per state, 50% category share).
2. Read `data/supplier-master.csv` and summed annual_spend_usd across all 25 suppliers to get the portfolio total.
3. Calculated each supplier's percentage: annual_spend_usd divided by portfolio total, multiplied by 100.
4. Sorted by percentage descending and identified Great Lakes Steel as the top supplier.
5. Checked whether Great Lakes Steel's share exceeded the 10% threshold. It did not.
6. Looked up Great Lakes Steel's state (IL) and counted other suppliers in Illinois. Found Sterling Advisory also in Chicago, IL. Two suppliers, below the 3-supplier flag.
7. Filtered spend-by-item.csv to the raw-materials category and summed by supplier to check category dominance.
8. Reported all three concentration checks in one answer.

## Common mistakes and how to recover

- **Symptom:** The share of wallet percentages do not sum to 100%. **Fix:** Confirm that Claude read all 25 rows from supplier-master.csv. Ask: "How many rows did you read from supplier-master.csv?" If it says fewer than 25, the file may have a blank line or a formatting issue that stopped the read early.

- **Symptom:** Geographic analysis shows every state with only one supplier, when you know Texas has three. **Fix:** Check the state column for formatting inconsistency. "TX" and "Texas" do not group together. Ask Claude: "Show me the unique values in the state column." Standardize to two-letter codes before re-running the group.

- **Symptom:** Category concentration analysis misses a dominant supplier. **Fix:** Check that spend-by-item.csv uses the same supplier names as supplier-master.csv. A one-word difference ("Great Lakes Steel" versus "Great Lakes Steel Co.") splits one supplier into two, halving the apparent concentration. Ask Claude to compare the supplier_name lists from both files and flag any mismatches.

- **Symptom:** The summary document in Drafts/ lists findings without dollar amounts. **Fix:** Every concentration finding must include the supplier name, the dollar figure, and the percentage. Ask Claude to rewrite any finding that uses vague language. "$4,200,000 (25.2% of raw-materials spend) from Great Lakes Steel" is a finding. "High concentration in raw-materials" is not.

- **Symptom:** Claude cannot find Drafts/ when saving. **Fix:** The Drafts/ folder must exist before Claude Code can write to it. Ask: "Create the Drafts/ folder if it does not exist, then save the file." Claude Code can create folders as part of a save instruction.
