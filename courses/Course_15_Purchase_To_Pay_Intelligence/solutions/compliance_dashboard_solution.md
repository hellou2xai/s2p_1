# /compliance-dashboard

Run all P2P compliance checks and produce a consolidated dashboard.

## What this command does

1. Read data/requisitions.csv. Screen each requisition against data/approval-matrix.csv. Flag any where the approver_level is below the required level for the amount.
2. Read data/purchase-orders.csv. Detect PO splitting: group by supplier and date. Flag groups where individual POs are below $5,000 but the combined total exceeds $5,000.
3. Read data/purchase-orders.csv and data/contracted-rates.csv. Compare each PO unit price to the contracted rate. Flag mismatches above 2% tolerance.
4. Run three-way match: join purchase-orders.csv, data/goods-receipts.csv, and data/invoices.csv on PO number. Flag quantity mismatches above 5% tolerance and price mismatches above 2%.
5. Read data/purchase-orders.csv and data/preferred-suppliers.csv. Flag any PO placed with a supplier not on the preferred list.
6. Consolidate all findings into a single dashboard.

## Output format

Save to outputs/compliance-dashboard.md with these sections:

### 1. Executive summary
One paragraph: total transactions reviewed, total violations found, total dollar impact, severity distribution.

### 2. Approval authority violations

| Req ID | Requestor | Amount | Approver level | Required level | Gap |
|---|---|---|---|---|---|

Severity: Critical if gap is 2+ levels. High if gap is 1 level.

### 3. PO splitting suspects

| Supplier | Date | PO count | Individual amounts | Combined total |
|---|---|---|---|---|

Severity: High.

### 4. Pricing mismatches

| PO number | Item | PO price | Contracted price | Variance % | Dollar impact |
|---|---|---|---|---|---|

Severity: High if variance > 10%. Medium if 2% to 10%.

### 5. Three-way match exceptions

| PO number | Type | PO value | GR value | Invoice value | Variance |
|---|---|---|---|---|---|

### 6. Maverick spend

| PO number | Supplier | Category | Amount |
|---|---|---|---|

Total maverick spend as percentage of total spend.

### 7. Recommended actions
Three actions ranked by dollar impact.
