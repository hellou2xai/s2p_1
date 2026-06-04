# Savings Methodology Solution

## Definitions encoded in CLAUDE.md

### Hard savings
Contracted price reduction that appears on a purchase order or invoice. Calculated as: (baseline unit price - new unit price) x actual quantity purchased. Verifiable against transaction data.

### Soft savings
Demand reduction or volume decrease. Calculated as: (baseline quantity - actual quantity) x baseline unit price. Requires baseline volume documentation and approval that the reduction is intentional (not a shortfall).

### Cost avoidance
Prevented price increase. Calculated as: (proposed increase per unit - negotiated increase per unit) x forecasted quantity. Not reflected in year-over-year spend comparisons. Tracked separately.

### Working capital
Cash flow improvement from extended payment terms. Calculated as: (annual spend x days extended / 365) x cost of capital (use 5.5% unless CFO specifies otherwise). Does not reduce spend.

## Matching rules

1. For hard savings: match each transaction in q1-q3-transactions.csv to its initiative by initiative_id. Compare the transaction unit price to the baseline rate in sourcing-initiatives-log.csv. Multiply savings per unit by quantity.
2. For soft savings: compare actual quarterly volumes to baseline quarterly volumes. Only count reductions explicitly approved (status = "approved" in the demand reduction log).
3. For cost avoidance: calculate the difference between the proposed increase and the negotiated increase. Apply to the forecasted annual volume.
4. For working capital: use the payment terms change (old days vs. new days) and apply the cost of capital formula.

## Sample calculation

Initiative SAV-001 (Steel Consolidation, hard savings):
- Baseline rate: $720/ton
- New contracted rate: $648/ton (10% reduction)
- Q1 actual: 420 tons at $648 = $272,160
- Savings: (720 - 648) x 420 = $30,240 for Q1
- Annualized run rate: $30,240 x 4 = $120,960

Target: $2,400,000. Q1-Q3 realized: $1,480,000 (61.7% of target).
