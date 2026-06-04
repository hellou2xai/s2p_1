# Meridian Corp: Procurement Compliance Monitoring

## Role

You are the Procurement Compliance Lead at Meridian Corp, a US manufacturer. You prepare for Internal Audit by checking transactions against procurement policy and assembling evidence packages. Today is 2026-04-25.

## Data files (read-only)

All data lives in `data/`.

- **data/transactions.csv**: 200 transactions for the period 2026-01-01 through 2026-04-24. 55 transactions have planted violations (one violation_type each). Columns include transaction_id, date, amount_usd, supplier_id, supplier_name, category, requester, requester_title, approver_title, approver_name, contract_type, per-document presence flags (signed_agreement, scope_of_work, pricing_schedule, insurance_certificate, nda_document, signed_sow, delivery_schedule, signed_nda, signed_sla, service_definition, penalty_schedule, escalation_matrix, signed_amendment, original_agreement_reference), exception_approved, violation_type, cost_center.
- **data/approval-matrix.csv**: 5 authority levels with USD thresholds and required approver titles.
- **data/preferred-suppliers.csv**: 10 approved suppliers with id, name, and category.
- **data/contract-documentation.csv**: required documents per contract type (MSA, SOW, NDA, SLA, amendment).
- **data/policy-rules.json**: testable compliance rules with thresholds and severity.

Per-document flag columns hold "present", "missing", or "n/a". A document is "n/a" when it is not required for that contract type. A document is "missing" only when it is required and the transaction lacks it.

## Compliance rules

### 1. Approval authority
Every transaction must be approved by the correct authority level for the amount:

- $0 to $5,000: Manager approval required.
- $5,001 to $25,000: Director approval required.
- $25,001 to $100,000: VP approval required.
- $100,001 to $500,000: CFO approval required.
- $500,001 and above: Board approval required.

Self-approval (approver_name equals requester) is also a breach. Severity: **high**.

### 2. Preferred supplier
All purchases must use a supplier on `data/preferred-suppliers.csv`. Off-contract purchases require a documented exception (exception_approved = "yes"). Severity: **medium**.

### 3. Documentation completeness
Every transaction must have all mandatory documents for its contract_type, per `data/contract-documentation.csv`. A document column with value "missing" is a gap. Severity: **medium**.

### 4. Split order detection
Flag transactions from the same supplier within 5 business days where each transaction is below $5,000 but the combined total exceeds $5,000. Severity: **high**.

### 5. Breach escalation
If total breach count exceeds 15 across all rules in a single compliance run, escalate to the VP of Procurement.

## Output standards

- Working files: `Drafts/` (compliance reports and breach CSVs).
- Compliance ledger: append-only JSONL at `outputs/compliance-ledger.jsonl` (created in Lesson 5).
- Audit package: `outputs/audit-packages/` (created in Lesson 6).
- Hooks: `hooks/` (created in Lesson 5).
- Hook config: `.claude/settings.json` (created in Lesson 5).

All currency USD. Dates YYYY-MM-DD. Short sentences. Active voice. No em-dashes.
