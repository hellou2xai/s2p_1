# Demand Consolidation Solution

## Demand Consolidation Report
**Date**: 2026-04-25
**Requirements processed**: 6
**Departments**: 5
**Consolidation opportunities**: 1

### Structured requirements

| # | Department | Requestor | Commodity | Quantity | Specification | Delivery by |
|---|---|---|---|---|---|---|
| 1 | Manufacturing | J. Park | Polymer resin | 450 metric tons | Industrial grade, pellet form | 2026-06-15 |
| 2 | R&D | M. Chen | Polymer resin | 120 metric tons | Industrial grade, pellet form | 2026-07-01 |
| 3 | Manufacturing | J. Park | Steel (hot rolled) | 800 tons | ASTM A36, plate | 2026-06-01 |
| 4 | Facilities | A. Torres | Natural gas | 12-month contract | Commercial rate | 2026-07-01 |
| 5 | IT | S. Kim | Electronic components | 5,000 units | Control boards, IPC-A-610 Class 2 | 2026-08-01 |
| 6 | Logistics | M. Davis | Diesel fuel | 120,000 gallons | ULSD, bulk delivery | 2026-05-15 |

### Consolidation opportunity: Polymer resin

**Departments**: Manufacturing (J. Park) and R&D (M. Chen)
**Combined volume**: 570 metric tons (450 + 120)
**Specifications**: Compatible. Both require industrial grade, pellet form.
**Delivery gap**: 16 days (2026-06-15 vs. 2026-07-01). Within 90-day window. Blanket order viable.

**Volume discount estimate**:
- Current price: $1.85/kg = $1,850/metric ton
- Individual spend: Manufacturing $832,500 + R&D $222,000 = $1,054,500
- Volume discount rule: 3% per doubling. 570 tons vs. 450 tons = 1.27x (not a full doubling). Estimated discount: ~1.5%.
- **Estimated savings: $15,818** ($1,054,500 x 1.5%)

**Recommendation**: Issue a single blanket PO for 570 metric tons of polymer resin with two delivery dates (450 tons by 2026-06-15, 120 tons by 2026-07-01). Negotiate volume pricing with Heartland Polymers at the combined quantity.

### No consolidation (other commodities)

- Steel, natural gas, electronic components, and diesel fuel each appear only once. No overlap detected.
