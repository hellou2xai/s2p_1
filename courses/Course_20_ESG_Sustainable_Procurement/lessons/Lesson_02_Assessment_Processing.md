# Assessment Processing

It is 10:00 Monday. You have 15 supplier assessment files in the `data/supplier-assessments/` folder. Ten are complete. Five are partial, with missing sections. Each file is a markdown document with scores and narrative responses for the six ESG dimensions. The formats are inconsistent. Some suppliers answered with detailed paragraphs. Others gave one-line responses. Two suppliers scored themselves at 95 on everything, which is not credible. You need to extract structured data from all 15, fill gaps with benchmark estimates, and flag the self-scores that look inflated.

## The S2P problem

Supplier ESG questionnaires arrive in different formats with different levels of completeness. Processing each one by hand takes about 40 minutes: read the document, find the score for each dimension, check whether the narrative supports the score, note missing sections, and enter everything into a tracking spreadsheet. At 40 minutes each, 15 assessments take 10 hours. And the quality varies wildly. A supplier that scores itself at 95 on carbon emissions but provides no data to support the claim needs scrutiny.

## What Claude Code does for you

Claude Code reads all 15 assessment files, extracts the dimension scores, flags missing sections, and applies benchmark estimates for gaps. It also identifies inflated self-scores by comparing supplier-reported scores to industry benchmarks. If a supplier claims 95 on carbon emissions but the industry average is 55, Claude Code flags the gap. The output is a structured table with 15 rows and 6 dimension scores per row, plus a completeness and credibility flag for each.

## Set up

1. Lesson 1 completed. CLAUDE.md has the full ESG framework with scoring rules.
2. Claude Code open in `Course_20_ESG_Sustainable_Procurement/practice/`.
3. `data/supplier-assessments/` contains 15 files (assessment-SUP001.md through assessment-SUP015.md).
4. `data/esg-benchmarks.md` is present with industry averages.

## Step-by-step

### Step 1. Read one complete assessment to understand the format.

```
Read data/supplier-assessments/assessment-SUP001.md and show me its structure: what sections does it have, and how are scores presented?
```

You should see a document with sections for each of the 6 ESG dimensions. Each section has a self-reported score and a narrative response.

### Step 2. Read one partial assessment to see what is missing.

```
Read data/supplier-assessments/assessment-SUP011.md and identify which ESG dimensions are present and which are missing.
```

You should see that one or more dimensions have no score or no response. The missing dimensions need benchmark estimates.

### Step 3. Read the benchmarks file.

```
Read data/esg-benchmarks.md and show me the industry average scores for each of the 6 ESG dimensions.
```

You should see benchmark averages for each dimension. For example, Carbon Emissions industry average might be 52, Environmental Management might be 58.

### Step 4. Process all 15 assessments.

```
Read all 15 files in data/supplier-assessments/. For each supplier, extract the score for each of the 6 ESG dimensions. If a dimension is missing, use the industry benchmark average from esg-benchmarks.md and mark it as "estimated." Build a table with columns: supplier_id, environmental_management, carbon_emissions, waste_management, labor_practices, diversity_inclusion, governance_ethics, completeness (complete/partial), estimated_dimensions (list of any estimated dimensions).
```

You should see a 15-row table. Ten rows show "complete" with no estimated dimensions. Five rows show "partial" with one or more estimated dimensions listed.

### Step 5. Flag inflated self-scores.

```
Compare each supplier's self-reported scores to the industry benchmarks in esg-benchmarks.md. Flag any score that exceeds the benchmark by more than 30 points. Show a table of flagged scores with columns: supplier_id, dimension, self_reported_score, benchmark_score, gap.
```

You should see a few flagged entries, particularly from suppliers who scored themselves at 90 or above on dimensions where the benchmark is in the 50s.

### Step 6. Save the extracted data.

```
Save the full assessment data table to Drafts/supplier-esg-scores-raw.csv with columns: supplier_id, supplier_name, environmental_management, carbon_emissions, waste_management, labor_practices, diversity_inclusion, governance_ethics, completeness, estimated_dimensions, inflated_flags. Include a header row.
```

You should see the CSV saved with 15 data rows plus the header.

## Worked example

**Starting files:**
- `data/supplier-assessments/` (15 files).
- `data/esg-benchmarks.md` (industry averages).
- `CLAUDE.md` with ESG framework.

**What you type:**

```
Process assessment-SUP012.md. It is a partial assessment. Extract the scores that are present, use benchmark averages for missing dimensions, and flag any score more than 30 points above the benchmark. Show the result as a single row with all 6 dimension scores and flags.
```

**What you should see:** A row showing SUP012 with actual scores for 4 dimensions and estimated scores for 2 missing dimensions. Any inflated scores are flagged.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the ESG framework and scoring rules.
2. Read data/supplier-assessments/assessment-SUP012.md to extract available scores.
3. Identified 2 missing dimensions with no score data.
4. Read data/esg-benchmarks.md to get industry averages for the missing dimensions.
5. Substituted benchmark averages and marked them as "estimated."
6. Compared all 6 scores to benchmarks and flagged any with a gap greater than 30 points.
7. Produced a single-row summary with completeness and flag columns.

## Common mistakes and how to recover

- **Symptom:** Claude Code reports 10 partial assessments instead of 5. **Fix:** Some assessments may have all 6 dimensions present but with sparse narrative. A dimension with a score of 0 is not "missing." Only dimensions with no score entry at all are missing. Check the extraction logic.

- **Symptom:** Estimated scores are indistinguishable from actual scores in the output. **Fix:** The estimated_dimensions column must list every dimension that used a benchmark substitute. Without this label, the board cannot tell which scores are based on real data.

- **Symptom:** The inflated-score threshold flags too many entries. **Fix:** The threshold is 30 points above benchmark. If the benchmark for Diversity and Inclusion is 45 and a supplier scores 72, the gap is 27 points, which is below the threshold. Adjust the threshold if your benchmarks are different.

- **Symptom:** Claude Code reads only the first assessment file and stops. **Fix:** The prompt must instruct Claude Code to read all 15 files. Use "Read all 15 files in data/supplier-assessments/" to process the full set.
