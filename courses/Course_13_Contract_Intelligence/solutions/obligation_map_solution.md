# Obligation Map Solution

## Sample: Obligations from MSA_Northwind_Office_Ltd.md

### Obligation register

| # | Obligation | Owner | Type | Frequency | Due date | Status |
|---|---|---|---|---|---|---|
| 1 | Pay invoices within Net 30 of receipt | Vanguard (buyer) | Payment | Ongoing | Per invoice | Active |
| 2 | Maintain general liability insurance of $2,000,000 per occurrence and name Buyer as additional insured | Northwind Office Ltd (supplier) | Compliance | Annual | Before renewal | Verify by 2026-06-01 |
| 3 | Provide a quarterly business review presentation | Northwind Office Ltd (supplier) | Reporting | Quarterly | Quarter end + 15 days | Next: 2026-07-15 |
| 4 | Maintain monthly system uptime of 99.5% or higher | Northwind Office Ltd (supplier) | Service Levels | Monthly | Each month end | Active |
| 5 | Submit a monthly service level report by the third business day | Northwind Office Ltd (supplier) | Reporting | Monthly | 3rd business day | Active |
| 6 | Maintain SOC 2 Type II attestation throughout the term | Northwind Office Ltd (supplier) | Compliance | Annual | Annual recertification | Verify on renewal |
| 7 | Report security incidents within 24 hours of detection | Northwind Office Ltd (supplier) | Compliance | On trigger | Within 24 hours | Dormant |
| 8 | Complete an annual penetration test and share remediation plan | Northwind Office Ltd (supplier) | Compliance | Annual | Each contract year | Next: 2026-07-01 |
| 9 | Provide 90 days' written notice for termination for convenience | Either party | Administrative | One-time | 2027-04-01 (for non-renewal) | Not yet due |
| 10 | Hold Confidential Information in confidence for 5 years post-termination | Both parties | Post-termination | Ongoing | If triggered | Dormant |

### Obligation extraction prompt

```
Read contracts/MSA_Northwind_Office_Ltd.md and extract every obligation. For each obligation, identify: what must be done, who owns it (buyer or supplier or both), the type (payment, compliance, reporting, service levels, commercial, administrative, post-termination), frequency, due date or trigger, and current status. Write the results to Drafts/obligations/MSA_Northwind_Office_Ltd_obligations.md.
```

### Batch obligation mapping

```
For each contract in contracts/, extract all obligations following the same format. Write one obligation file per contract to Drafts/obligations/. After processing all contracts, create a summary file at Drafts/obligation-summary.md listing: total obligations, obligations by owner (buyer vs supplier), obligations due in the next 90 days, and overdue obligations.
```
