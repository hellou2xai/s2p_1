# Solution: indirect/CLAUDE.md

Reference answer for Lesson 3 (indirect portion). Slightly longer than the other two because the approval rule needs a clear statement.

## The reference content

Save at `practice/indirect/CLAUDE.md`.

```
# Indirect - folder instructions

## What this folder is

This folder is indirect spend. Office, software, marketing, legal, audit,
MRO, telecoms, fleet, and facilities. We have 80 active vendors across
nine subcategories. The category lead is finance, with the CFO as the
approver for high-value spend.

## Files in this folder

vendors.csv
- the active vendor list, around 80 rows
- columns: vendor_id, vendor_name, what_they_provide, annual_value_usd,
  contract_end, status
- refreshed when a new vendor is added or a contract changes;
  last reviewed 2026-04-25

invoices.csv
- recent invoices, around 3,000 rows over the last 12 months
- columns: invoice_number, vendor_id, what_for, amount_usd,
  invoice_date, approval_path
- refreshed weekly from the AP system; last reviewed 2026-04-25

## Rules

- VEN005 Prism Print is currently flagged at_risk in vendors.csv.
  Their contract ends 2026-05-31.

- Approval rule (the most important rule in this folder):
  Any invoice with amount_usd of $25,000 or more must use approval_path
  "cfo_over_25k". Any invoice with amount_usd of $25,000 or more that
  has approval_path "manager_under_25k" is a policy violation. There
  are around 18 such violations across the year in invoices.csv.
  When asked about violations, list the invoice_number, vendor_name,
  amount_usd, and approval_path used.

- For spend questions, sum amount_usd from invoices.csv and group by
  vendor_id, then look up vendor_name in vendors.csv.

- Folder rules and writing rules from the global apply.
```

## Why this works

- About 35 lines, slightly longer than the other two folder files because the approval rule needs to be stated precisely. Claude needs the rule in plain English to find violations across 3,000 invoice rows.
- The at-risk flag and the approval rule are the only category-specific items.
- No vendors are typed out by name.

## How it differs from the other two

- Names vendors (VEN-prefixed), not suppliers or carriers.
- The $25,000 approval rule has no equivalent in direct materials or logistics.
- Refers to finance and the CFO as approvers.
