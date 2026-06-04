# /onboard-supplier

Run the onboarding compliance check for a single supplier and produce a checklist.

## Inputs

- The supplier name (passed as an argument).
- `Master/compliance-status.csv`
- `Master/Onboarding_Checklist_Template.docx`

## Steps

1. Find the supplier row in `Master/compliance-status.csv`.
2. Read every field in the row.
3. Compare each field to the 12-item checklist in the Word template.
4. Produce a two-column table: Checklist Item, Status (Complete, Missing, or Expired).
5. If any item is Missing or Expired, draft a follow-up email to the supplier with a 7-day deadline.
6. Save the checklist to `Outputs/onboarding-checklists/<supplier-name>-checklist.md`.

## Output format

A markdown file with the supplier name, the date, the 12-row checklist table, and the draft follow-up email at the bottom.
