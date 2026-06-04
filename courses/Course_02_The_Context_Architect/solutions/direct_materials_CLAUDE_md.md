# Solution: direct-materials/CLAUDE.md

Reference answer for Lesson 3 (direct materials portion) and Lesson 5 (last-reviewed line).

## The reference content

Save at `practice/direct-materials/CLAUDE.md`. About 25 lines, three sections.

```
# Direct materials - folder instructions

## What this folder is

This folder is direct materials. Steel, aluminum, plastics, electronics
chips, and castings. We have 50 active suppliers across Michigan, California,
Texas, Ohio, and other US states. The category
lead is the engineering team.

## Files in this folder

suppliers.csv
- the active supplier list, around 50 rows
- columns: supplier_id, supplier_name, state, makes,
  annual_value_usd, contract_end, status
- refreshed when a new supplier is added or a contract changes;
  last reviewed 2026-04-25

orders.csv
- recent purchase orders, around 2,500 rows over the last 12 months
- columns: po_number, supplier_id, item, units, total_usd, po_date
- refreshed weekly from the orders system; last reviewed 2026-04-25

## Rules

- SUP004 Apex Electronics is currently flagged at_risk in suppliers.csv.
  Their contract ends 2026-05-31. We need a sourcing decision before then.
- For any spend question, sum total_usd from orders.csv and group by
  supplier_id, then look up supplier_name in suppliers.csv.
- For any contract question, read suppliers.csv directly.
- Folder rules and writing rules from the global apply.
```

## Why this works

- About 25 lines.
- The "What this folder is" section gives Claude the scope in three sentences.
- "Files in this folder" lists the two CSVs by name, with column headers and a refresh note. No data is embedded.
- "Rules" holds only what is specific to direct materials: the at-risk supplier flag and the join hint for spend questions.

## How it differs from the logistics and indirect files

- Names suppliers (SUP-prefixed), not carriers or vendors.
- The at-risk entity is a supplier, not a carrier or vendor.
- Refers to engineering as the category lead, not operations or finance.
