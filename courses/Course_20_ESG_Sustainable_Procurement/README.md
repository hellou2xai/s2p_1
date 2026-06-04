# Course 20: ESG and Sustainable Procurement

A short course (about 4.5 hours) that teaches you to build an **ESG
assessment and reporting system**: supplier questionnaire processing,
weighted ESG scoring, Scope 3 carbon estimation, and portfolio dashboard
generation. No coding required.

## What you will end up with

An ESG assessment portfolio covering 15 suppliers with individual action
plans, a Scope 3 baseline using the spend-based method, and a board
dashboard with score distributions and SBTi progress. Five suppliers have
incomplete questionnaires, and the system handles benchmark estimation for
missing data.

## What is in this course folder

```
Course_20_ESG_Sustainable_Procurement/
  README.md                       (this file)
  COURSE_OVERVIEW.md              (the story)
  lessons/                        (six lessons, in order)
  practice/
    CLAUDE.md                     (role, data files, scoring rules)
    data/
      spend-by-supplier.csv       (15 suppliers with emission factors)
      esg-framework.csv           (6 ESG dimensions with weights)
      esg-benchmarks.md           (industry benchmarks, emission factors)
      supplier-assessments/       (15 questionnaire .md files)
    Drafts/                       (working output files)
    Outputs/                      (final signed-off files)
  solutions/
  scripts/
    build_course_data.py          (regenerates all practice data)
```

## What is in the practice data

| File | Contents |
|---|---|
| spend-by-supplier.csv (15 suppliers) | Annual spend, category, and emission factor (kg CO2 per USD) per supplier. Spend ranges from $520,000 (Eagle Transport) to $4,200,000 (Great Lakes Steel). |
| esg-framework.csv (6 dimensions) | Environmental Management (20%), Carbon Emissions and Reduction (25%), Waste Management and Circular Economy (15%), Labor Practices and Human Rights (15%), Diversity and Inclusion (10%), and Governance and Ethics (15%). Minimum threshold: 40. Target: 70. |
| supplier-assessments/ (15 files) | Ten complete assessments (SUP001 through SUP010) and five partial (SUP011 through SUP015) with one or more dimensions left blank. Pacific Aluminum (SUP003) and Eagle Transport (SUP008) carry red-flag scores below 40. Summit Components (SUP006) and National Facilities (SUP009) inflated their self-scores to 90 or above on dimensions where the industry benchmark is in the 50s. |
| esg-benchmarks.md | Industry average score per dimension, ISO 14001 and safety statistics, and Scope 3 emission factors by category (EPA EEIO v1.1, USD 2026). |

Today's date is **2026-04-25**.

## Regenerating the practice data

If you delete or change any file under `practice/data/` and want to start
over, run the regenerator from the course root:

```
python scripts/build_course_data.py
```

The script is deterministic (uses `random.seed(42)`), so you get the same
files every time. It also creates `practice/Drafts/` and `practice/Outputs/`
if they are missing.
