# Course 21: Compliance, Policy, and Audit Readiness

## The audit letter

It is Tuesday morning. Your inbox has an email from Internal Audit: "Procurement Compliance Review. Scope: approval authority, preferred supplier usage, and contract documentation. Fieldwork begins in 90 days. Please prepare the following evidence for the sample period January 1 through June 30, 2026."

The email lists three areas of concern:

1. **Approval authority breaches.** Audit found 12 transactions in the last review where the approver's authority level was below the transaction amount. They want every transaction checked against the approval matrix for the current period.
2. **Preferred supplier non-compliance.** 8% of purchases went to suppliers not on the preferred list, without approved exceptions. They want the full list of off-contract purchases with rationale.
3. **Incomplete contract documentation.** 15 contracts were missing required documents (signed agreements, pricing schedules, insurance certificates). They want a documentation completeness check for all active contracts.

You have 90 days. The last time this happened, a team of three spent six weeks pulling evidence manually. They checked transactions in spreadsheets, cross-referenced the approval matrix by hand, and assembled binders of supporting documents.

This course builds the automated version. You encode procurement policy as testable rules in CLAUDE.md, run every transaction through compliance checks, maintain an append-only compliance ledger via a PostToolUse hook, and assemble audit evidence packages from the ledger.

## The practice scenario

Meridian Corp is a US-based manufacturer. Internal audit has flagged three procurement compliance concerns. You are the Procurement Compliance Lead.

Today's date is **2026-04-25**. You have:

- 200 transactions from the last 6 months. 55 have planted violations:
  - Approval authority breaches (self-approved or under-approved for amount)
  - Non-preferred supplier purchases (from suppliers not on the approved list)
  - Missing documentation (missing PO, receipt, or invoice)
  - Suspected split orders (multiple orders from the same supplier, each just under $5,000)
- An approval matrix with 5 authority levels.
- A preferred supplier list of 10 suppliers.
- Required documentation rules by contract type.
- Policy rules encoded as JSON for automated checking.

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | Encoding procurement policy as testable CLAUDE.md rules | 45 min |
| 2 | Approval authority compliance: transactions vs. authority matrix | 50 min |
| 3 | Preferred supplier compliance: off-contract spend quantified | 45 min |
| 4 | Contract documentation completeness: gap flagging as audit findings | 40 min |
| 5 | The compliance ledger: append-only JSONL via PostToolUse hook | 45 min |
| 6 | Audit package assembly: ledger entries to structured evidence | 35 min |

Total: about 4.5 hours.

## You are done with the course when

1. You have procurement policy encoded in CLAUDE.md as testable rules with specific thresholds.
2. You have processed all 200 transactions and identified the 55 violations with correct categorization.
3. Your compliance ledger (JSONL) has one entry per compliance check with timestamp, rule, result, and severity.
4. The breach escalation hook fires when violations exceed 15 (it will fire, because the data has 55).
5. You can assemble an audit evidence package for a defined scope: relevant ledger entries, supporting transactions, and a structured summary.
