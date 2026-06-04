# Meridian Manufacturing - Procurement Operations

## Who I am

I am a Procurement Operations Lead at Meridian Manufacturing, a US-based
mid-market manufacturer. I manage recurring procurement analyses across four
categories: direct materials, logistics, indirect, and MRO. Annual
procurement spend is approximately 48m USD across 50 active suppliers.

## Folder layout

data/              source data files (read-only, do not modify)
.claude/commands/  custom slash commands (you build these across the lessons)
outputs/           analysis outputs land here, datestamped

## Folder rules

The CSV files in data/ are the source of truth.
Read them when asked. Do not modify them.
Save all outputs to outputs/ with a datestamp in the file name.
The commands in .claude/commands/ are reusable. They work with $ARGUMENTS
so the same command runs for any period, category, or supplier.

## Writing rules

American English. USD for all currency.
Oxford commas. No em-dashes. Active voice.
Specific numbers, never "significant" or "material" for figures.
Cap tables at 15 rows unless the command says otherwise.
Every output ends with an audit footer: date, source files, model, operator.

## Data files

data/spend-transactions.csv
  ~2,500 transaction rows over the last 12 months.
  Columns: transaction_id, date, supplier_id, supplier_name, category,
  subcategory, description, amount_usd, po_number, cost_center,
  department, payment_terms, invoice_status.

data/supplier-master.csv
  50 suppliers across 4 categories.
  Columns: supplier_id, supplier_name, category, tier, contract_id,
  risk_rating, city, state, payment_terms, annual_target_usd, status.

data/contract-register.csv
  30 active contracts.
  Columns: contract_id, supplier_id, supplier_name, title, start_date,
  end_date, annual_value_usd, total_value_usd, auto_renew,
  notice_period_days, status.

data/scorecard-history.csv
  200 rows: 50 suppliers x 4 quarters.
  Columns: supplier_id, supplier_name, quarter, quality_score,
  delivery_score, responsiveness_score, cost_score, innovation_score,
  overall_score.
