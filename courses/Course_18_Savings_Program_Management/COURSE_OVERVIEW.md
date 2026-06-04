# Course 18: Savings Program Management

## Tuesday is coming

It is Thursday afternoon. Your CFO's assistant sends a calendar invite: "Savings Program Review, Tuesday 10:00 AM." The invite has no agenda. It does not need one. The CFO wants three things: how much you saved this year, whether you will hit the target, and what went wrong with the initiatives that are behind.

You have eight initiatives. Five are hard savings with contracted rates you can verify against transaction data. One is demand reduction (soft savings). One is specification standardization (cost avoidance). One is payment terms extension (working capital). Your total annual target is $12M.

You open a spreadsheet. You start pulling transactions for each initiative, matching them to baseline rates, computing realized savings line by line. By 6:00 PM you have three initiatives done. Five to go. The weekend is not looking free.

This course fixes that. You build a savings tracking pipeline that reads the transaction file, matches each transaction to its initiative, computes realized savings against baseline rates, models three full-year scenarios, and drafts a CFO memo. One command. One run. Tuesday is covered.

## The practice scenario

Apex Procurement manages a $12M annual savings target across eight sourcing initiatives for a US-based manufacturer.

Today's date is **2026-04-25**. It is Q3 close (for the purposes of this exercise, we treat the data as if Q3 ended). The CFO review is next Tuesday.

Your eight initiatives:

| ID | Initiative | Type | Annual Target |
|---|---|---|---|
| SAV-001 | Steel Consolidation | Hard savings | $2,400,000 |
| SAV-002 | Logistics RFP | Hard savings | $1,800,000 |
| SAV-003 | IT License Rationalization | Hard savings | $1,500,000 |
| SAV-004 | Facilities Rebid | Hard savings | $1,200,000 |
| SAV-005 | Consulting Rate Card | Hard savings | $1,600,000 |
| SAV-006 | Demand Reduction (Travel) | Soft savings | $800,000 |
| SAV-007 | Spec Standardization | Cost avoidance | $1,400,000 |
| SAV-008 | Payment Terms Extension | Working capital | $1,300,000 |

Two initiatives are underperforming: SAV-002 (Logistics RFP, at risk, 55-70% of target) and SAV-006/SAV-007 (behind, 30-50% of target).

## The five lessons

| # | Title | Time |
|---|---|---|
| 1 | Savings methodology encoding: your definitions, not industry averages | 45 min |
| 2 | Transaction-to-initiative matching: calculating realized savings | 50 min |
| 3 | Three-scenario modeling: base, upside, and risk-adjusted projections | 50 min |
| 4 | Writing the CFO memo: headline number first, variance without excuses | 45 min |
| 5 | The monthly refresh: automated savings tracker update | 30 min |

Total: about 4 hours.

## You are done with the course when

1. You have a savings methodology encoded in CLAUDE.md that distinguishes hard savings, soft savings, cost avoidance, and working capital.
2. You have matched Q1-Q3 transactions to initiative baselines and computed realized savings for each initiative.
3. You have three Q4 scenarios: base, upside, and risk-adjusted, each with a specific dollar figure.
4. Your CFO memo leads with the headline number, shows variance by initiative, and names three actions. No excuses, no filler.
5. The monthly refresh runs from a single slash command.
