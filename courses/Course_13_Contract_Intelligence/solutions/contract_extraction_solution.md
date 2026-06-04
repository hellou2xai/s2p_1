# Contract Extraction Solution

## Sample extraction: MSA_Northwind_Office_Ltd.md

### Extracted fields

```json
{
  "file": "MSA_Northwind_Office_Ltd.md",
  "contract_type": "MSA",
  "party_a": "Vanguard Manufacturing Inc.",
  "party_b": "Northwind Office Ltd",
  "effective_date": "2025-07-01",
  "expiry_date": "2027-06-30",
  "term_months": 24,
  "total_value_usd": 284000,
  "annual_value_usd": 142000,
  "payment_terms": "Net 30",
  "auto_renewal": true,
  "notice_period_days": 90,
  "liability_cap": "Twelve months of fees paid",
  "termination_for_convenience": true,
  "termination_notice_days": 90,
  "category": "IT services",
  "governing_law": "Ohio",
  "key_clauses": [
    "Insurance: General liability $2,000,000 per occurrence, Buyer named as additional insured",
    "SLA: Monthly uptime 99.5%, service credits per Schedule A",
    "IP: Deliverables owned by Buyer, Supplier retains pre-existing IP",
    "Confidentiality: 5 years after expiry or termination",
    "Audit: Once per calendar year on 14 days' notice"
  ]
}
```

### Batch extraction prompt

```
Read every contract in contracts/. For each contract, extract these fields: contract_type, party_a, party_b, effective_date, expiry_date, term_months, total_value_usd, annual_value_usd, payment_terms, auto_renewal, notice_period_days, liability_cap, termination_for_convenience, termination_notice_days, category, governing_law, and key_clauses (list of up to 5 important clauses). Write the results to Drafts/contract-register-extract.csv with one row per contract.
```

### What Claude did behind the scenes

1. Read the CLAUDE.md in the practice root for extraction field definitions and clause taxonomy.
2. Listed all .md files in contracts/.
3. Read each contract sequentially.
4. For each contract: parsed the document structure, identified the parties section, term section, compensation, payment terms, and clause sections.
5. Mapped each extracted clause to the taxonomy in clause-taxonomy.csv.
6. Wrote the structured output to CSV in Drafts/.
7. Flagged contracts where a liability cap, governing law, or insurance minimum was missing or unclear.
