# Risk Register Solution

## Supply Chain Risk Register
**Date**: 2026-04-25
**Prepared by**: Supply Chain Risk Analyst
**Scope**: 25 suppliers, 5 categories

### Risk scoring matrix

| Factor | Weight | Scale |
|---|---|---|
| Financial health | 25% | 0-100 (D&B or equivalent) |
| Single-source exposure | 25% | Any single-source item with criticality "high" or "critical" |
| Disruption history | 20% | Any event in past 12 months affecting this supplier |
| Alternate availability | 15% | No qualified alternate = high risk |
| Geographic concentration | 15% | "high" = 3 or more suppliers in same state |

### Top 10 risks (sorted by risk score, descending)

| Rank | Supplier | Category | Risk score | Financial health | Single source | Key risk |
|---|---|---|---|---|---|---|
| 1 | Apex Electronics (SUP004) | Components | 84 | 44.8 | Yes | Sole source for ITEM-0025 Microcontroller ARM ($480,000/year, criticality critical). No qualified alternate. Financial distress event ongoing since November 2025. |
| 2 | Continental Freight (SUP006) | Logistics | 76 | 41.7 | No | Lowest financial health score in portfolio. $3,600,000 annual spend. Carries $720,000 of steel plate freight (ITEM-0081). |
| 3 | Pacific Aluminum (SUP003) | Raw materials | 72 | 52.3 | Yes | Sole source for ITEM-0013 Aluminum sheet 2mm ($620,000/year). One alternate (Summit Metals SUP016) qualified. 5 single-source items total. |
| 4 | CloudBridge Systems (SUP010) | IT services | 68 | 78.6 | Yes | Sole source for ITEM-0037 Cloud hosting ($500,000/year). Cybersecurity incident March 2026, 5 days offline, $95,000 business interruption. |
| 5 | Heartland Polymers (SUP002) | Raw materials | 64 | 80.8 | Yes | Hurricane disruption September 2025, 12 days, $420,000 in delayed shipments. TX-based, geographic concentration high. |
| 6 | Eagle Transport (SUP008) | Logistics | 58 | 58.1 | No | Logistics capacity crunch January 2026, 21 days, $180,000 incremental cost. 2 single-source items in portfolio. |
| 7 | Great Lakes Steel (SUP001) | Raw materials | 54 | 75.2 | Yes | Sole source for ITEM-0001 Steel plate 4mm ($840,000/year). Two alternates available (Summit Metals qualified, Liberty Composites in qualification). |
| 8 | SafeGuard Fire (SUP025) | Facilities | 46 | 73.8 | Yes | Sole source for ITEM-0049 Fire inspection ($140,000/year). Compliance-critical service. 15-week qualification time for an alternate. |
| 9 | Frontier Plastics (SUP018) | Raw materials | 42 | 56.9 | No | Financial health below 60. TX-based (3 suppliers in TX). 1 single-source item. |
| 10 | TechForward Solutions (SUP009) | IT services | 38 | 70.9 | No | $2,800,000 annual spend. TX-based, geographic concentration high. 2 single-source items. |

### Risk summary

- **2 suppliers** with financial health below 50: Continental Freight (41.7), and Apex Electronics (44.8).
- **5 single-source items** totaling $2,580,000 in annual spend (ITEM-0001 $840,000, ITEM-0013 $620,000, ITEM-0037 $500,000, ITEM-0025 $480,000, and ITEM-0049 $140,000).
- **4 disruption events** in the trailing 24 months affecting Heartland Polymers, Apex Electronics, Eagle Transport, and CloudBridge Systems.
- **Geographic concentration**: TX holds 3 suppliers (Heartland Polymers, TechForward Solutions, and Frontier Plastics). IL and CA each hold 2.
- **No qualified alternate** for ITEM-0025 Microcontroller ARM. The other 4 single-source items have either a qualified alternate or one in qualification.
