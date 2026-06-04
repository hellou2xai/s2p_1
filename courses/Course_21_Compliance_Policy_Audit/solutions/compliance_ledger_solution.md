# Compliance Ledger Solution

## Format

Each entry in outputs/compliance-ledger.jsonl follows this structure:

```json
{
  "timestamp": "2026-04-25T10:15:32Z",
  "transaction_id": "TXN-0042",
  "rule": "approval_authority",
  "result": "violation",
  "severity": "high",
  "details": "Transaction amount $28,500 approved by Manager (limit $25,000). Required level: Director.",
  "evidence": {
    "amount_usd": 28500,
    "approver_level": "Manager",
    "required_level": "Director",
    "approver_name": "Sarah Kim"
  }
}
```

## Rules checked per transaction

### 1. Approval authority
```json
{
  "rule": "approval_authority",
  "check": "Compare transaction amount to approver's authority level in approval-matrix.csv",
  "violation_if": "approver level limit < transaction amount",
  "severity": "high"
}
```

### 2. Preferred supplier
```json
{
  "rule": "preferred_supplier",
  "check": "Check if supplier_name exists in preferred-suppliers.csv",
  "violation_if": "supplier not in preferred list AND no documented exception",
  "severity": "medium"
}
```

### 3. Documentation completeness
```json
{
  "rule": "documentation_completeness",
  "check": "Check if PO, receipt, and invoice exist for the transaction per contract-documentation.csv requirements",
  "violation_if": "any required document missing",
  "severity": "medium"
}
```

### 4. Split order detection
```json
{
  "rule": "split_order",
  "check": "Group transactions by supplier within 5 business days. Flag if individual amounts < $5,000 but combined > $5,000",
  "violation_if": "pattern detected",
  "severity": "high"
}
```

### 5. Breach escalation
```json
{
  "rule": "breach_escalation",
  "check": "Count total violations in current compliance run",
  "violation_if": "total violations > 15",
  "severity": "high",
  "action": "Escalate to VP of Procurement"
}
```

## Sample ledger entries

```jsonl
{"timestamp":"2026-04-25T10:15:32Z","transaction_id":"TXN-0042","rule":"approval_authority","result":"violation","severity":"high","details":"Amount $28,500 approved by Manager (limit $25,000). Director required."}
{"timestamp":"2026-04-25T10:15:33Z","transaction_id":"TXN-0042","rule":"preferred_supplier","result":"pass","severity":"n/a","details":"Supplier Great Lakes Steel is on the preferred list."}
{"timestamp":"2026-04-25T10:15:34Z","transaction_id":"TXN-0042","rule":"documentation_completeness","result":"pass","severity":"n/a","details":"PO, receipt, and invoice all present."}
{"timestamp":"2026-04-25T10:15:35Z","transaction_id":"TXN-0087","rule":"preferred_supplier","result":"violation","severity":"medium","details":"Supplier QuickParts LLC is not on the preferred supplier list. No exception documented."}
{"timestamp":"2026-04-25T10:15:36Z","transaction_id":"TXN-0103","rule":"split_order","result":"violation","severity":"high","details":"Two orders from Apex Electronics within 3 days: $4,800 and $4,900. Combined $9,700 exceeds $5,000 threshold."}
```
