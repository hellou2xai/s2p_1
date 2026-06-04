# /lifecycle-status

Generate a full lifecycle status report for all 30 suppliers.

## What this command does

1. Read data/supplier-master.csv for supplier details, tier, and current lifecycle stage.
2. Read data/performance-history.csv for the most recent quarter's scores per supplier.
3. Read data/compliance-status.csv for compliance checklist progress.
4. Read data/development-plans.csv for active improvement plans.
5. Group suppliers by lifecycle stage.
6. For each supplier: show current stage, overall performance score, compliance status, and recommended action.

## Stage assignment logic

- **Onboarding**: compliance_status contains "incomplete" items.
- **Active**: overall_score >= 3.0 AND compliance complete AND no development plan overdue.
- **Strategic**: tier = "strategic" AND overall_score >= 4.0.
- **At risk**: overall_score dropped below 3.0 in the last two quarters.
- **Corrective action**: has an active improvement plan in development-plans.csv.
- **Exit**: status = "exit_planned" in supplier-master.csv.
- **Under review**: does not fit any other category clearly.

## Output format

Save to outputs/segmentation-report.md with these sections:

1. **Summary**: Total suppliers by stage (table). Highlight any stage with more than 5 suppliers.
2. **Stage detail**: One section per stage. Each supplier listed with: name, category, tier, overall score, key concern (one sentence), recommended action.
3. **Urgent actions**: Top three actions across all stages, ranked by business impact.

## Quality criteria

- Every supplier appears exactly once.
- Every at-risk or corrective-action supplier has a recommended action.
- Dates use YYYY-MM-DD format.
- No em-dashes.
