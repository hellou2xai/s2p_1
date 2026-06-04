# Solution: logistics/CLAUDE.md

Reference answer for Lesson 3 (logistics portion).

## The reference content

Save at `practice/logistics/CLAUDE.md`.

```
# Logistics - folder instructions

## What this folder is

This folder is logistics. The carriers that move our goods.
We have 20 active carriers covering road, sea, air, and parcel.
Lanes include domestic US, US-Asia, and US-Europe routes.
The category lead is the operations team.

## Files in this folder

carriers.csv
- the active carrier list, around 20 rows
- columns: carrier_id, carrier_name, mode, annual_value_usd,
  contract_end, status
- refreshed when a new carrier is added or a contract changes;
  last reviewed 2026-04-25

shipments.csv
- recent shipments, around 5,000 rows over the last 12 months
- columns: shipment_id, carrier_id, from_location, to_location,
  total_usd, ship_date
- refreshed weekly from the TMS export; last reviewed 2026-04-25

## Rules

- CAR004 ParcelPlus is currently flagged at_risk in carriers.csv.
  Their contract ends 2026-06-30. Service quality has been below standard.
- For any spend question, sum total_usd from shipments.csv and group by
  carrier_id, then look up carrier_name in carriers.csv.
- For mode-level analysis, group shipments by mode (after joining to carriers).
- Folder rules and writing rules from the global apply.
```

## Why this works

- About 25 lines.
- Tells Claude the scope, the two files, the at-risk carrier, and how to do spend aggregation.
- No carriers are typed out by name; Claude reads carriers.csv when asked.

## How it differs from the other two

- Names carriers (CAR-prefixed), not suppliers or vendors.
- Has a mode-level analysis hint, which only applies in logistics.
- Refers to operations as the category lead.
