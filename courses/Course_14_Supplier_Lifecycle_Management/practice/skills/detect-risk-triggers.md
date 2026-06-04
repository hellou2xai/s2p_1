# Skill: Detect Risk Triggers

Use this skill to find suppliers whose performance is sliding toward at-risk before a delivery failure.

## Inputs

- `Master/performance-history.csv` (Overall_Score, by Quarter)
- `Master/supplier-master.csv` (Annual_Spend_USD, Lifecycle_Stage)

## Triggers

Flag a supplier as at risk if any of these conditions hold:

1. Overall_Score dropped 10 or more points between the last two quarters on file.
2. Overall_Score below 60 for two consecutive quarters.
3. Quality_Score below 65 in the most recent quarter, regardless of trend.
4. Delivery_Score below 65 in the most recent quarter and Annual_Spend_USD above $500,000.

## Output

A ranked list (by point drop, descending) with these columns:
- Supplier_Name
- Q3_Score (or earliest of the two compared quarters)
- Q4_Score (or latest of the two compared quarters)
- Point_Drop
- Annual_Spend_USD

Save to `Drafts/At_Risk_Report_v1.csv` or to `Outputs/corrective-action-plans/at-risk-summary.md`, depending on the calling lesson.
