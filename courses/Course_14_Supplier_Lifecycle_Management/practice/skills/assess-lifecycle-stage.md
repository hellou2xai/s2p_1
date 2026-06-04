# Skill: Assess Lifecycle Stage

Use this skill when classifying any Crestview Industries supplier into one of the seven lifecycle stages.

## Inputs

- `Master/supplier-master.csv` (Lifecycle_Stage column, Onboarded_Date, Last_Review_Date)
- `Master/performance-history.csv` (4 quarters of Overall_Score)
- `Master/compliance-status.csv` (W9, COI, ACH_Banking_Form, Code_of_Conduct, Quality_Agreement)
- `Master/development-plans.csv` (active plan flag)

## Stage rules, in order

Apply the rules from top to bottom. Stop at the first match.

1. **Exit.** Lifecycle_Stage in supplier-master is `exit`, or supplier_master shows an exit flag with an off-boarding date.
2. **Corrective Action.** Lifecycle_Stage is `corrective_action`, or an open CAP exists.
3. **Under Review.** Lifecycle_Stage is `under_review`, or an audit is pending, or a stage dispute is unresolved.
4. **At Risk.** Overall_Score dropped 10 or more points between Q3 2025 and Q4 2025, or any compliance field is Expired.
5. **Onboarding.** Onboarded_Date within last 90 days from today (2026-04-25), or any compliance field is blank or Pending.
6. **Strategic.** Active development plan on file, Tier is `strategic`, and Overall_Score above 85 for the last 3 quarters.
7. **Active.** All compliance fields Received, no open issues, Overall_Score above 60.

## Output

A row per supplier with: Supplier_Name, Stage, Reason. Save to `Outputs/segmentation-report.md` or to `Drafts/Supplier_Segmentation_v1.csv`, depending on the calling lesson.
