# Lesson 01: Risk Signal Architecture

## Opening scenario

It is 08:30 Wednesday. Your CPO calls from the airport: "The board meeting moved up to next Thursday. They want the full supply chain risk posture. Don't give me last quarter's spreadsheet, where every analyst scored suppliers differently. I need one consistent method, applied to all 25 suppliers, and I need to be able to defend every number." You have the data. What you don't have is a shared, written scoring logic that Claude Code can apply the same way every time. That's what you build in this lesson.

## The S2P problem

Supply chain risk assessments break down when analysts apply different criteria to different suppliers. One analyst considers a financial health score of 55 acceptable. Another flags it as medium risk. Without a written scoring matrix, the risk register reflects who scored which supplier, not the actual risk level. A board that sees inconsistent ratings loses confidence in the entire assessment. Building a scoring matrix in CLAUDE.md solves this. Every session starts with the same rules. Every supplier gets scored against the same thresholds. The output is defensible because the logic is visible.

## What Claude Code is going to do for you

You will encode five risk factors, their weights, and their scoring bands into CLAUDE.md. Claude Code reads this matrix at the start of every session and applies it to `data/supplier-master.csv`. Financial health below 50 is high risk. Geographic concentration above a threshold is elevated. Single-source exposure with no qualified alternate is critical. The rules are explicit, weighted, and consistent. By the end of this lesson, you can score any supplier in the portfolio in under two minutes.

## Set up

1. Claude Code installed and signed in. Open a terminal window.
2. Navigate to the practice folder for this course:

```
cd "Course_19_Supply_Chain_Risk/practice"
claude
```

3. Confirm `CLAUDE.md` is present in the practice folder. It holds the role definition and a starter scoring matrix.
4. Confirm `data/supplier-master.csv` is present with 25 supplier rows.
5. Pause OneDrive sync before this session. Resume when finished.

Open Claude Code with this first prompt:

```
The folder data/ holds the source files. Do not edit any file in data/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

Claude Code should confirm the read-only rule. Nothing changes on disk.

## Step-by-step

### Step 1. Read the existing CLAUDE.md.

Read the role and scoring matrix that are already in the file.

```
Read CLAUDE.md and show me the risk scoring matrix section.
```

You should see a table with five risk factors: financial health (25%), geographic concentration (15%), single-source exposure (25%), disruption history (20%), and alternate availability (15%). If the file reads as empty, check that you are in the `practice/` folder, not the course root.

### Step 2. Inspect the supplier master data.

Confirm the data columns Claude Code will use for scoring.

```
Read data/supplier-master.csv and show me all columns for the first 5 rows.
```

You should see columns including supplier_id, supplier_name, category, tier, city, state, annual_spend_usd, financial_health_score, geographic_concentration, and single_source_items. If you see fewer columns, the file may be truncated. Ask Claude to show the header row separately.

### Step 3. Add detailed scoring bands to CLAUDE.md.

Update the matrix with explicit numeric thresholds for each factor.

```
Update the risk scoring matrix in CLAUDE.md with these detailed scoring bands:

Financial health (25% weight):
- Score 0-49: high risk (score = 3)
- Score 50-69: medium risk (score = 2)
- Score 70-100: low risk (score = 1)

Geographic concentration (15% weight):
- "high" in supplier-master.csv: elevated (score = 3)
- "medium": moderate (score = 2)
- "low": acceptable (score = 1)

Single-source exposure (25% weight):
- 3 or more single-source items: critical (score = 3)
- 1-2 single-source items: elevated (score = 2)
- 0 single-source items: acceptable (score = 1)

Disruption history (20% weight):
- Any disruption event in disruption-events.md naming this supplier: elevated (score = 3)
- No events: acceptable (score = 1)

Alternate availability (15% weight):
- No qualified alternate for any single-source item: critical (score = 3)
- Alternate in qualification: moderate (score = 2)
- Qualified alternate available: acceptable (score = 1)

Overall risk score = weighted sum. Range 1.00 to 3.00.
- 2.50-3.00: critical risk (red)
- 2.00-2.49: high risk (orange)
- 1.50-1.99: medium risk (yellow)
- 1.00-1.49: low risk (green)
```

You should see CLAUDE.md updated with the full scoring bands. If Claude Code reports a write error, check that CLAUDE.md is not open in another application.

### Step 4. Test the scoring on one supplier.

Apply the matrix to Apex Electronics to confirm it works.

```
Using the updated risk scoring matrix in CLAUDE.md, score supplier SUP004 (Apex Electronics)
from data/supplier-master.csv. Show the score for each factor and the weighted overall score.
```

You should see Apex Electronics scored as follows: financial_health_score of 44.8 falls below 50, so factor score 3. Geographic concentration is "high," so factor score 3. Single_source_items is 4, which is 3 or more, so factor score 3. Disruption history: Apex Electronics appears in disruption-events.md (Event 2), so factor score 3. Alternate availability: check approved-alternates.csv. Overall weighted score should be in the critical range (2.50 to 3.00). If you see a score below 2.00, check that CLAUDE.md was saved after Step 3.

### Step 5. Map each factor to its data source.

Document exactly which file and column Claude Code must read for each factor.

```
List each of the five risk factors and name the specific data file and column Claude Code must
read to score it. Format as a table with columns: risk_factor, data_file, column_or_section.
```

You should see a clean mapping table. Financial health maps to `data/supplier-master.csv` / `financial_health_score`. Geographic concentration maps to `data/supplier-master.csv` / `geographic_concentration`. Single-source exposure maps to `data/supplier-master.csv` / `single_source_items`. Disruption history maps to `data/disruption-events.md` / supplier name match. Alternate availability maps to `data/approved-alternates.csv` / `qualification_status`.

### Step 6. Add the data source mapping to CLAUDE.md.

Save the mapping so future sessions know where to find each input.

```
Add the risk-factor-to-data-source mapping table from the previous step to CLAUDE.md,
under the scoring matrix section. Title it "Data source mapping." Save CLAUDE.md.
```

You should see CLAUDE.md updated with the mapping table. Confirm by asking Claude Code to read CLAUDE.md and show the last section.

## Worked example

**Starting files:**
- `CLAUDE.md` with role definition and starter scoring matrix (already in the practice folder).
- `data/supplier-master.csv` with 25 suppliers, including financial_health_score, geographic_concentration, and single_source_items columns.

**What you type:**

```
Score SUP006 (Continental Freight) using the risk matrix in CLAUDE.md. Their
financial_health_score is 41.7, geographic_concentration is "low", and
single_source_items is 0. Read disruption-events.md and approved-alternates.csv
for the remaining two factors. Show each factor score and the weighted total.
```

**What you should see:**

Continental Freight scored: financial health 41.7 is below 50, so score 3 (high risk). Geographic concentration "low" scores 1. Single-source items 0 scores 1. Disruption history: Continental Freight does not appear in disruption-events.md, so score 1. Alternate availability: no single-source items means this factor scores 1. Weighted total: (3 x 0.25) + (1 x 0.15) + (1 x 0.25) + (1 x 0.20) + (1 x 0.15) = 1.50. Risk level: medium (yellow).

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the scoring matrix with weights and scoring bands.
2. Read `data/supplier-master.csv` to find SUP006: financial health 41.7, geographic concentration "low," single-source items 0.
3. Applied the financial health band: 41.7 falls in 0 to 49, so score 3.
4. Applied the geographic band: "low" maps to score 1.
5. Applied the single-source band: 0 items maps to score 1.
6. Searched `data/disruption-events.md` for any event naming "Continental Freight." Found no match, so disruption history scores 1.
7. Checked `data/approved-alternates.csv` for any row linked to SUP006. No single-source items means this factor defaults to score 1.
8. Calculated the weighted sum and matched it to the overall risk band.

## Common mistakes and how to recover

- **Symptom:** All 25 suppliers receive the same overall score. **Fix:** Check that the scoring bands in CLAUDE.md have different thresholds. If every factor maps to score 2 for every supplier, the bands are too broad or the data column names are wrong. Confirm that `financial_health_score` in the CSV matches exactly what CLAUDE.md references.

- **Symptom:** The weighted score exceeds 3.00. **Fix:** The maximum score per factor is 3. The maximum weighted total is 3.00 exactly. If you see a number above 3.00, confirm that the five weights sum to 1.00: 0.25 + 0.15 + 0.25 + 0.20 + 0.15 = 1.00. A typo in one weight (for example, 0.30 instead of 0.25) breaks the total.

- **Symptom:** Disruption history scores "acceptable" for a supplier that had a documented event. **Fix:** Claude Code matches supplier names between disruption-events.md and supplier-master.csv. If the event file says "Apex Electronics" and the CSV says "Apex Electronics Inc.", the match fails. Check for trailing words, abbreviations, or punctuation differences.

- **Symptom:** CLAUDE.md reverts to the old content after you restart Claude Code. **Fix:** Claude Code loads CLAUDE.md from the folder where you started it. If you started Claude in a different folder, it reads a different CLAUDE.md (or none). Always `cd` into `Course_19_Supply_Chain_Risk/practice/` before running `claude`.

- **Symptom:** A supplier with 5 single-source items scores the same as one with 3. **Fix:** This is correct behavior. The bands are: 3 or more equals score 3, 1 to 2 equals score 2, 0 equals score 1. Both 5 and 3 fall in the "3 or more" band. If finer granularity matters, add a "5 or more" band with score 3.5, but note that this pushes the maximum weighted total above 3.00 and requires rescaling.

- **Symptom:** The data source mapping table in CLAUDE.md disappears after you add it. **Fix:** Claude Code may have overwritten the whole file instead of appending. Ask Claude to read CLAUDE.md and confirm both the scoring matrix and the mapping table are present. If the matrix is gone, restore it from the course `Master/` folder and redo Steps 3 and 6.
