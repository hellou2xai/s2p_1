# Three-Way Match Solution

## Logic

1. Start with purchase-orders.csv. For each PO, find matching goods-receipts by po_number.
2. For each matched PO-GR pair, find matching invoices by po_number.
3. Compare quantities: PO ordered quantity vs. GR received quantity. Flag if difference exceeds 5%.
4. Compare prices: PO unit price vs. invoice unit price. Flag if difference exceeds 2%.
5. Classify each match result:
   - **Full match**: Quantity within 5%, price within 2%.
   - **Quantity exception**: Quantity outside 5% tolerance.
   - **Price exception**: Price outside 2% tolerance.
   - **Missing GR**: PO exists but no goods receipt found.
   - **Missing invoice**: PO and GR exist but no invoice found.

## Sample output

### Three-Way Match Report
**Date**: 2026-04-25
**POs reviewed**: 384
**GRs matched**: 273
**Invoices matched**: 168

### Match results

| Result | Count | % of POs | Dollar value |
|---|---|---|---|
| Full match | 128 | 33.3% | $4,280,000 |
| Quantity exception | 55 | 14.3% | $1,840,000 |
| Price exception | 17 | 4.4% | $620,000 |
| Missing GR | 111 | 28.9% | $3,200,000 |
| Missing invoice | 73 | 19.0% | $2,460,000 |

### Top exceptions by dollar value

| PO | Supplier | Type | PO value | Actual | Variance | Impact |
|---|---|---|---|---|---|---|
| PO-2841 | Great Lakes Steel | Quantity | 500 units | 540 units | +8.0% | $12,400 |
| PO-3102 | Heartland Polymers | Price | $14.50/kg | $15.20/kg | +4.8% | $8,400 |
| PO-2956 | Apex Electronics | Quantity | 200 units | 168 units | -16.0% | $6,400 |
