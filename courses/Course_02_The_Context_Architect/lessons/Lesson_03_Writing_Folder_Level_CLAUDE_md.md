# Lesson 3: Writing the three category files

**Time:** 50 minutes. **You need:** Lesson 2 complete.

## A typical Tuesday afternoon

It is 14:00. You sit back down. The global is done. Now you give Claude the **category-specific** background: the suppliers, the rules, the data files for each of your three categories. Three short files, one per folder. About 15 minutes per file.

The pattern is the same for all three. You will do direct materials in detail, then repeat the same shape for logistics and indirect.

## The big idea

Each category file has three sections:

1. **What this folder is.** One paragraph. Tells Claude what category this is.
2. **Files in this folder.** Lists the data files in this folder so Claude knows what to read.
3. **Rules.** Anything specific to this category that Claude needs (the at-risk supplier, an approval threshold, etc.).

The same three sections work for all three categories. What changes is the content.

## Set up

**Step 1.** Open your terminal.

**Step 2.** Look at what is in the direct-materials folder so you know what data exists. Type:

```
cd "Course_02_The_Context_Architect/practice/direct-materials"
ls
```

You should see three things: `CLAUDE.md` (the stub you fix in this lesson), `orders.csv`, and `suppliers.csv`. No subfolders. Everything is right here.

**The folder layout for direct materials.**

```
practice/direct-materials/
├── CLAUDE.md               (stub, you replace it in Step 6)
├── orders.csv              (2,500 PO rows)
└── suppliers.csv           (50 suppliers)
```

**Step 3.** Take a quick look at suppliers.csv. On Windows or Mac, double-click to open in Excel. Or, in your terminal:

```
head suppliers.csv
```

You will see the column headers (`supplier_id, supplier_name, state, makes, annual_value_usd, contract_end, status`) and the first ten suppliers. There are 50 suppliers in total. **Note that SUP004 Apex Electronics has status `at_risk`.** That detail goes in your CLAUDE.md.

**Step 4.** Take a quick look at orders.csv:

```
head orders.csv
```

Column headers: `po_number, supplier_id, item, units, total_usd, po_date`. There are 2,500 PO rows across the last year. You do not need to read them all. Claude will, when you ask.

You now know what data exists. Time to write the file that tells Claude.

## Write direct-materials/CLAUDE.md

**Step 5.** Open `direct-materials/CLAUDE.md` in your editor. It is a stub. Select all and delete.

**Step 6.** Type or paste this content:

```
# Direct materials - folder instructions

## What this folder is

This folder is direct materials. Steel, aluminum, plastics, electronics chips,
and castings. We have 50 active suppliers across Michigan, California, Texas,
Ohio, and other US states. The category lead is
the engineering team.

## Files in this folder

suppliers.csv
- the active supplier list, 50 rows
- columns: supplier_id, supplier_name, state, makes,
  annual_value_usd, contract_end, status

orders.csv
- recent purchase orders, around 2,500 rows across the last 12 months
- columns: po_number, supplier_id, item, units, total_usd, po_date

## Rules

- SUP004 Apex Electronics is currently flagged at_risk. Their contract ends
  2026-05-31. We need a sourcing decision before then.
- For any spend question, sum total_usd from orders.csv and group by
  supplier_id (then look up supplier_name in suppliers.csv).
- For any contract question, read suppliers.csv directly.
- Folder rules and writing rules from the global apply.
```

**Step 7.** Save. About 25 lines.

## Test direct-materials/CLAUDE.md

**Step 8.** In your terminal, you are still in the direct-materials folder. Start Claude:

```
claude
```

**Step 9.** Try a real Tuesday-afternoon question. Type:

```
List my top 10 suppliers by annual value, sorted highest first.
```

**What you should see.** A small table or list with ten supplier names, each with their annual value. Great Lakes Steel should be near the top ($2,400,000). The list comes from `suppliers.csv`, which Claude opened because your CLAUDE.md said it was there.

**Step 10.** Try a more interesting question that needs the activity file:

```
Sum my total spend across all orders for the last year, grouped by
supplier. Show me the top 5 suppliers by spend, with the figure for each.
```

**What you should see.** Claude reads `orders.csv` (all 2,500 rows), aggregates by supplier_id, joins to supplier_name from `suppliers.csv`, and returns five rows. Great Lakes Steel should be top by spend (lots of steel orders, high unit prices). This is the kind of question that takes 30 minutes in Excel and 30 seconds with Claude.

**Step 11.** One more question, the kind your CPO actually asks:

```
Which supplier is at risk and when does their contract end?
```

**What you should see.** Apex Electronics (SUP004). Contract ends 2026-05-31. Claude found this from the `status` column of `suppliers.csv`.

**Step 12.** Quit Claude (`/quit`).

## Now do logistics

**Step 13.** Move to the logistics folder:

```
cd ../logistics
ls
```

You should see `CLAUDE.md`, `carriers.csv`, `shipments.csv`.

**The folder layout for logistics.**

```
practice/logistics/
├── CLAUDE.md               (stub, you replace it in Step 15)
├── carriers.csv            (20 carriers)
└── shipments.csv           (5,000 shipment rows)
```

**Step 14.** Skim the data:

```
head carriers.csv
```

20 carriers. Note **CAR004 ParcelPlus is at_risk**.

**Step 15.** Open `logistics/CLAUDE.md`. Replace its stub with:

```
# Logistics - folder instructions

## What this folder is

This folder is logistics. The carriers that move our goods.
We have 20 active carriers covering road, sea, air, and parcel.
Lanes include domestic US, US-Asia, and US-Europe routes.
The category lead is the operations team.

## Files in this folder

carriers.csv
- the active carrier list, 20 rows
- columns: carrier_id, carrier_name, mode, annual_value_usd,
  contract_end, status

shipments.csv
- recent shipments, around 5,000 rows across the last 12 months
- columns: shipment_id, carrier_id, from_location, to_location,
  total_usd, ship_date

## Rules

- CAR004 ParcelPlus is currently flagged at_risk. Their contract ends
  2026-06-30. Service quality has been below standard.
- For spend questions, sum total_usd from shipments.csv and group
  by carrier_id (then look up carrier_name in carriers.csv).
- Folder rules and writing rules from the global apply.
```

Save.

**Step 16.** Test it. Start Claude:

```
claude
```

Type:

```
Sum my total shipment spend across the year, grouped by mode (road,
sea, air, parcel). Show the four totals.
```

**What you should see.** Four totals. Road and sea will be the biggest. Air will be next. Parcel will be smallest. Claude has just aggregated 5,000 shipment rows for you.

Quit Claude.

## Now do indirect

**Step 17.** Move to the indirect folder:

```
cd ../indirect
ls
```

You should see `CLAUDE.md`, `invoices.csv`, `vendors.csv`.

**The folder layout for indirect.**

```
practice/indirect/
├── CLAUDE.md               (stub, you replace it in Step 19)
├── invoices.csv            (3,000 invoice rows, 18 violations)
└── vendors.csv             (80 vendors)
```

**Step 18.** Skim the data:

```
head vendors.csv
```

80 vendors. Note **VEN005 Prism Print is at_risk**.

**Step 19.** Open `indirect/CLAUDE.md`. Replace with:

```
# Indirect - folder instructions

## What this folder is

This folder is indirect spend. Office, software, marketing, legal, audit,
MRO, telecoms, fleet, and facilities. We have 80 active vendors. The
category lead is finance, with the CFO as the approver for high-value spend.

## Files in this folder

vendors.csv
- the active vendor list, 80 rows
- columns: vendor_id, vendor_name, what_they_provide, annual_value_usd,
  contract_end, status

invoices.csv
- recent invoices, around 3,000 rows across the last 12 months
- columns: invoice_number, vendor_id, what_for, amount_usd,
  invoice_date, approval_path

## Rules

- VEN005 Prism Print is currently flagged at_risk. Their contract ends
  2026-05-31.
- Approval rule: any invoice for $25,000 or more must use the
  approval_path "cfo_over_25k". Any invoice with amount_usd 25000 or
  above and approval_path "manager_under_25k" is a policy violation.
- Folder rules and writing rules from the global apply.
```

Save.

**Step 20.** Test it. Start Claude:

```
claude
```

Try the kind of compliance question your audit team would ask:

```
Find every invoice in invoices.csv that breaks the $25,000 approval
rule. Show me invoice number, vendor, amount, and the approval path used.
Cap at 20 rows.
```

**What you should see.** A list of about 18 invoices that have `amount_usd` of 25,000 or more but used `manager_under_25k` instead of `cfo_over_25k`. These are real policy violations buried in 3,000 rows of normal activity. Claude found them by following the rule you wrote in CLAUDE.md.

Quit Claude.

## Compare against the three solutions

**Step 21.** Open the three solution files in turn:

- `solutions/direct_materials_CLAUDE_md.md`
- `solutions/logistics_CLAUDE_md.md`
- `solutions/indirect_CLAUDE_md.md`

Compare each against your file. They will not match exactly. They are reference answers, not the only correct answer. Borrow ideas where the solution is sharper.

## What Claude did, behind the scenes

You wrote three small files. Each one tells Claude what the folder is, what data files live in it, and what rules apply. Here is what Claude Code actually did at each step, so you can apply the same pattern to your own categories.

1. In direct materials, Claude loaded two instruction files at session start: the global (from `practice/CLAUDE.md`) and the category file (from `direct-materials/CLAUDE.md`). Together, those two files gave Claude the writing rules, the folder rules, and the category-specific context.
2. When you asked "top 10 suppliers by annual value" (Step 9), Claude opened `suppliers.csv`, read all 50 rows, sorted by `annual_value_usd` descending, and returned the top 10.
3. When you asked "total spend grouped by supplier" (Step 10), Claude opened `orders.csv` (all 2,500 rows), summed `total_usd` by `supplier_id`, joined `supplier_name` from `suppliers.csv`, sorted descending, and returned the top 5.
4. When you asked about the at-risk supplier (Step 11), Claude filtered `suppliers.csv` for `status` = "at_risk" and returned SUP004 Apex Electronics with `contract_end` = 2026-05-31.
5. In logistics, Claude loaded the logistics category file instead. When you asked for spend by mode (Step 16), it read 5,000 shipment rows, joined to `carriers.csv` for the `mode` column, and summed `total_usd` by mode.
6. In indirect, Claude loaded the indirect category file. When you asked for approval violations (Step 20), it scanned 3,000 invoice rows, filtered for `amount_usd` >= 25,000 AND `approval_path` = "manager_under_25k", and found exactly 18 violations.

## Three things that trip beginners up

- **Wrong path in the file.** When you write `suppliers.csv` inside the direct-materials CLAUDE.md, that path is relative to the direct-materials folder. Do not write `direct-materials/suppliers.csv` and do not write `data/suppliers.csv` (there is no `data/` subfolder in this course; the CSVs sit alongside CLAUDE.md).
- **You repeated the writing rules.** The writing rules are in the global. Adding them to the category file is duplication. Just say "writing rules from the global apply."
- **Claude says "I cannot find the file."** You have a typo in the path or the file name. Run `ls` in your terminal to see the exact file names and copy them carefully.

## You are done with Lesson 3 when

- All three category files have three sections each, between 20 and 35 lines.
- A test prompt in each folder gets a sensible answer based on the right CSVs.
- You compared against the three solution files.

Take a break. Move to Lesson 4 next.
