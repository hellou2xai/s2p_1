# Scope 3 Carbon Estimation

It is 14:00 Monday. Your Chief Sustainability Officer needs a Scope 3 baseline by June 30. Scope 3 covers indirect emissions from your supply chain, specifically the carbon your suppliers produce on your behalf. You do not have supplier-level emissions data for most of them. What you do have is spend data and industry emission factors. The spend-based method multiplies annual spend by an emission factor (kg CO2 per USD) to estimate each supplier's carbon contribution. It is not precise, but it is the accepted starting point for organizations that lack primary data.

## The S2P problem

Most procurement teams know their total spend. Very few know their total Scope 3 emissions. Collecting primary emissions data from every supplier takes months or years. In the meantime, the board deadline does not wait. The spend-based method gives a defensible first estimate using data you already have. The challenge is documenting the methodology clearly enough that auditors, the CSO, and the board all understand what the number represents, and what it does not represent.

## What Claude Code does for you

Claude Code reads spend-by-supplier.csv (which includes emission factors by category) and calculates Scope 3 emissions for each supplier using the formula: annual_spend_usd times emission_factor_kg_co2_per_usd divided by 1,000 equals tons CO2. It produces a supplier-level emissions table, a total Scope 3 estimate, and a methodology statement that names the data source, the formula, the assumptions, and the limitations. The methodology statement is what makes the estimate auditable.

## Set up

1. Lessons 1 and 2 completed. CLAUDE.md has the ESG framework and scoring rules.
2. Claude Code open in `Course_20_ESG_Sustainable_Procurement/practice/`.
3. `data/spend-by-supplier.csv` is present with annual spend and emission factors.
4. `data/esg-benchmarks.md` is present with emission factor references.

## Step-by-step

### Step 1. Read the spend data with emission factors.

```
Read data/spend-by-supplier.csv and show me all columns for the first 5 rows.
```

You should see columns including supplier_id, supplier_name, category, annual_spend_usd, and emission_factor_kg_co2_per_usd.

### Step 2. Read the emission factor references.

```
Read data/esg-benchmarks.md and show me the emission factors section. What source are the factors based on?
```

You should see emission factors by category (for example, raw-materials at 0.8 kg CO2/USD, logistics at 1.2 kg CO2/USD) and a reference to the data source (such as EPA EEIO factors or EXIOBASE).

### Step 3. Calculate Scope 3 emissions by supplier.

```
For each supplier in spend-by-supplier.csv, calculate Scope 3 emissions using the formula in CLAUDE.md: annual_spend_usd x emission_factor_kg_co2_per_usd / 1000 = tons CO2. Show a table with columns: supplier_id, supplier_name, category, annual_spend_usd, emission_factor, estimated_tons_co2. Sort by estimated_tons_co2 descending.
```

You should see a 15-row table with the highest emitters at the top. Suppliers with large spend in high-factor categories (like logistics or raw materials) will rank highest.

### Step 4. Calculate the total Scope 3 estimate.

```
Sum the estimated_tons_co2 for all 15 suppliers. Show the total Scope 3 estimate in tons CO2. Also show the breakdown by category: what percentage of total Scope 3 comes from each supplier category?
```

You should see a total Scope 3 figure and a category breakdown. Raw materials and logistics typically contribute the largest shares.

### Step 5. Write the methodology statement.

```
Write a methodology statement for the Scope 3 estimate. It must include:
1. Data source: spend-by-supplier.csv with emission factors from [name the benchmark source].
2. Formula: annual_spend_usd x emission_factor_kg_co2_per_usd / 1000 = tons CO2.
3. Scope: 15 suppliers representing [state the percentage] of total procurement spend.
4. Limitations: spend-based factors are industry averages, not supplier-specific measurements. Actual emissions may be higher or lower.
5. Recommended next step: collect primary emissions data from the top 5 emitters to replace estimated factors with measured values.

Save to Drafts/scope3-methodology.md.
```

You should see a clear, one-page methodology statement saved.

### Step 6. Save the emissions table.

```
Save the full supplier emissions table to Drafts/scope3-emissions-by-supplier.csv with all columns from Step 3 plus a "data_quality" column set to "estimated-spend-based" for all rows.
```

You should see the CSV saved with 15 rows and the data quality flag.

## Worked example

**Starting files:**
- `data/spend-by-supplier.csv` (15 suppliers with emission factors).
- `data/esg-benchmarks.md` (emission factor references).
- `CLAUDE.md` with Scope 3 formula.

**What you type:**

```
Calculate the Scope 3 emissions for SUP001 (Great Lakes Steel). Their annual spend is $4,200,000 and their emission factor is 0.8 kg CO2 per USD. Show the calculation step by step.
```

**What you should see:** $4,200,000 times 0.8 equals 3,360,000 kg CO2. Divide by 1,000 equals 3,360 tons CO2.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the Scope 3 formula: spend times factor divided by 1,000.
2. Read spend-by-supplier.csv to get SUP001's annual spend ($4,200,000) and emission factor (0.8).
3. Multiplied: $4,200,000 times 0.8 equals 3,360,000 kg CO2.
4. Converted to tons: 3,360,000 divided by 1,000 equals 3,360 tons CO2.
5. Labeled the result as "estimated-spend-based" per the data quality standard.

## Common mistakes and how to recover

- **Symptom:** The total Scope 3 estimate is in kilograms, not tons. **Fix:** The formula divides by 1,000 to convert kg to metric tons. If the final number looks 1,000x too large, the division step was skipped.

- **Symptom:** All suppliers show the same emission factor. **Fix:** Emission factors vary by category. Raw materials, logistics, IT services, and professional services each have different factors. Check that spend-by-supplier.csv has a per-supplier or per-category factor, not a single default.

- **Symptom:** The methodology statement does not name the factor source. **Fix:** Every Scope 3 estimate must cite the emission factor source (EPA EEIO, EXIOBASE, or another database). Without the source, auditors cannot verify the factors.

- **Symptom:** The estimate includes only 10 of 15 suppliers. **Fix:** Check that spend-by-supplier.csv has 15 rows. If the emission factor is blank for some suppliers, Claude Code may skip them. Fill blank factors with the category average from esg-benchmarks.md and mark as "estimated."
