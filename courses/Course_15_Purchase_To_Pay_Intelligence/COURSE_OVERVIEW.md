# Course 15: Purchase to Pay Intelligence

## $140M in spend, zero compliance visibility

It is Wednesday morning, 09:00. You are the P2P Analytics Lead at Meridian Corp, a US-based manufacturer with $140M in annual procurement spend. Your CFO just forwarded an internal audit finding: "Procurement controls are insufficient. We found 14 purchase orders approved above the requestor's authority level in a single month. We also suspect PO splitting to avoid approval thresholds."

The audit sampled 50 transactions. You have 384 POs, 500 requisitions, 273 goods receipts, and 168 invoices from the past month alone. The auditors want a full compliance review by end of next week. Manually cross-referencing four data sets against approval thresholds, contracted rates, and preferred supplier lists would take two analysts five full days.

This course fixes that. You build a Claude Code system that screens every transaction against your policy rules. It checks approval levels, detects PO splitting patterns, matches PO prices to contracted rates, runs three-way matches across POs, goods receipts, and invoices, flags maverick spend outside preferred suppliers, and identifies payment terms gaps. One command produces a compliance dashboard with every violation, the dollar impact, and recommended actions.

## What a P2P intelligence system does

A P2P intelligence system connects requisitions, purchase orders, goods receipts, and invoices into a single compliance view. It applies policy rules to every transaction and surfaces violations that would otherwise require manual cross-referencing.

| Without P2P intelligence | With P2P intelligence |
|---|---|
| Approval violations found only in quarterly audits | Every requisition screened against the approval matrix on demand |
| PO splitting detected only by pattern recognition in Excel | Automated detection: same supplier, same day, amounts below threshold |
| Three-way match done manually, 15 min per invoice | Claude Code matches PO, GR, and invoice in seconds |
| Maverick spend discovered in annual category reviews | Preferred supplier check on every PO, violations flagged immediately |
| Payment terms inconsistencies found during contract renewal | Terms compared to contracted rates across all active invoices |

## The practice scenario

Meridian Corp is a US-based manufacturer with $140M in annual procurement spend. You are the P2P Analytics Lead, reporting to the Director of Procurement Operations. The CFO has requested a full P2P compliance review after an internal audit flagged control gaps.

Your data covers one month of transactions:

| Data set | Rows | Known issues |
|---|---|---|
| Requisitions | 500 | 5% have approval-level violations |
| Purchase orders | 384 | PO splitting patterns planted across multiple POs |
| Goods receipts | 273 | 20% have quantity mismatches (over or under delivery) |
| Invoices | 168 | 10% have price mismatches against contracted rates |

Your approval matrix has five levels:

| Level | Approval limit |
|---|---|
| Analyst | Up to $5,000 |
| Manager | Up to $25,000 |
| Director | Up to $100,000 |
| VP | Up to $500,000 |
| CFO | Unlimited |

Today's date is **2026-04-25**. The CFO wants the compliance review by **2026-05-02**.

## What you will build

```
p2p-intelligence-2026/
├── .claude/
│   ├── settings.json                (permissions, hooks)
│   └── commands/
│       ├── compliance-dashboard.md  (full P2P compliance scan)
│       ├── three-way-match.md       (PO-GR-invoice matching)
│       └── maverick-report.md       (non-preferred supplier spend)
├── CLAUDE.md                        (role, approval rules, policy thresholds)
├── data/
│   ├── requisitions.csv             (500 rows, read-only)
│   ├── purchase-orders.csv          (384 rows, read-only)
│   ├── goods-receipts.csv           (273 rows, read-only)
│   ├── invoices.csv                 (168 rows, read-only)
│   ├── contracted-rates.csv         (10 items, read-only)
│   ├── approval-matrix.csv          (5 levels, read-only)
│   └── preferred-suppliers.csv      (20 suppliers, read-only)
├── outputs/
│   ├── compliance-dashboard.md      (consolidated compliance report)
│   ├── approval-violations.md       (requisitions above authority level)
│   ├── po-splitting-report.md       (suspected split POs)
│   ├── three-way-match-report.md    (PO-GR-invoice mismatches)
│   ├── maverick-spend-report.md     (non-preferred supplier transactions)
│   └── payment-terms-analysis.md    (terms optimization opportunities)
└── skills/
    ├── screen-approvals.md          (approval matrix screening pattern)
    └── detect-po-splitting.md       (PO splitting detection pattern)
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | P2P data architecture: understanding the four transaction files and how they connect | 50 min |
| 2 | Requisition compliance screening: checking every requisition against the approval matrix | 55 min |
| 3 | PO pricing compliance: matching PO amounts to contracted rates and flagging overcharges | 55 min |
| 4 | Three-way match automation: connecting POs, goods receipts, and invoices to find mismatches | 60 min |
| 5 | Maverick spend detection: identifying purchases outside preferred suppliers | 50 min |
| 6 | Payment terms optimization: finding gaps between contracted terms and actual invoice terms | 50 min |

Total: about 6 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. You run `/compliance-dashboard` and Claude Code produces a report listing every approval violation, with the requisition ID, the approver, the amount, and the correct approval level.
2. The PO splitting detector identifies at least three sets of split POs (same supplier, same day, individual amounts below threshold but combined total above it) and calculates the combined value.
3. The three-way match connects POs, goods receipts, and invoices and flags every quantity mismatch (tolerance: 5%) and every price mismatch (tolerance: 2%).
4. The maverick spend report lists every PO placed with a non-preferred supplier, grouped by category, with the total maverick spend as a percentage of total spend.
5. The payment terms analysis compares invoice payment terms to contracted rates and identifies at least $200,000 in potential savings from terms standardization.
6. The consolidated compliance dashboard summarizes all five checks in a single document with a severity rating (critical, high, medium) for each finding.
