# Audit Package Solution

## Audit Evidence Package: Approval Authority Compliance
**Scope**: Transactions from 2026-01-01 through 2026-06-30
**Prepared**: 2026-04-25
**Prepared by**: Procurement Compliance Lead

### 1. Executive summary

We reviewed 200 transactions against the five-level approval authority matrix. We identified 55 violations across four rule categories: approval authority breaches, non-preferred supplier purchases, documentation gaps, and suspected split orders.

Total violations exceed the 15-violation escalation threshold. This package has been escalated to the VP of Procurement per policy rule 5.

### 2. Violation summary

| Rule | Violations | Severity | Dollar impact |
|---|---|---|---|
| Approval authority | 15 | High | $842,000 in under-approved transactions |
| Preferred supplier | 12 | Medium | $380,000 in off-contract spend |
| Documentation completeness | 18 | Medium | $520,000 in transactions with missing documents |
| Split order detection | 10 | High | $92,000 in suspected split orders |
| **Total** | **55** | | **$1,834,000** |

### 3. Supporting evidence: Approval authority violations

| # | Transaction ID | Date | Amount | Approver | Approver level | Required level |
|---|---|---|---|---|---|---|
| 1 | TXN-0042 | 2026-02-14 | $28,500 | Sarah Kim | Manager | Director |
| 2 | TXN-0067 | 2026-01-22 | $112,000 | James Park | Director | VP |
| 3 | TXN-0089 | 2026-03-08 | $7,200 | Lisa Chen | Analyst | Manager |
| ... | ... | ... | ... | ... | ... | ... |

(Full list: 15 entries. See compliance-ledger.jsonl for complete records.)

### 4. Methodology

- **Data source**: transactions.csv (200 rows, date range 2026-01-01 to 2026-06-30).
- **Approval matrix**: approval-matrix.csv (5 levels: Analyst $0-$5K, Manager $5K-$25K, Director $25K-$100K, VP $100K-$500K, CFO $500K+).
- **Preferred supplier list**: preferred-suppliers.csv (10 approved suppliers).
- **Documentation rules**: contract-documentation.csv (required documents per contract type).
- **Split order window**: 5 business days, $5,000 threshold per policy-rules.json.
- **Escalation threshold**: 15 violations per compliance run.

### 5. Compliance ledger reference

All 200 transaction checks are recorded in outputs/compliance-ledger.jsonl. Each entry includes:
- Timestamp (UTC)
- Transaction ID
- Rule checked
- Result (pass or violation)
- Severity (high, medium, or n/a)
- Evidence details

The ledger is append-only. No entries have been modified or deleted.

### 6. Recommended actions

1. **Implement automated approval routing** that blocks requisitions above the requestor's authority level. Estimated implementation: 4 weeks. This eliminates the most common violation category (15 of 55 violations).

2. **Require documented exception forms** for non-preferred supplier purchases above $1,000. Current violations show 12 purchases with no rationale on file.

3. **Run monthly split-order scans** using the 5-day window and $5,000 threshold. The 10 suspected split orders suggest deliberate threshold avoidance in at least two cost centers.
