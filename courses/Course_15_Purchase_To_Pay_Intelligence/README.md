# Course 15: Purchase to Pay Intelligence

A short course (about 6 hours) that teaches you to build a Claude Code system for detecting compliance violations across the purchase-to-pay cycle. You work with requisitions, purchase orders, goods receipts, and invoices to find approval bypasses, PO splitting, price mismatches, maverick spend, and payment terms gaps. No coding required beyond copy-paste prompts.

## What you will end up with

A P2P intelligence layer. You point Claude Code at your transactional data and it screens requisitions against the approval matrix, checks PO prices against contracted rates, runs three-way matches across POs, goods receipts, and invoices, flags maverick spend outside preferred suppliers, and identifies payment terms optimization opportunities. One command produces a compliance dashboard with specific violations, dollar amounts, and recommended actions.

After Course 15, you catch compliance gaps that would take an analyst two days to find manually.

## What you need before you start

- Courses 1 through 14 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, pipelines, projects, MCP, composition, category management, supplier risk, contract intelligence, and supplier lifecycle.
- A laptop with Claude Code installed and signed in.
- About 6 hours, in two or three sittings.

## What is in this course folder

```
Course_15_Purchase_To_Pay_Intelligence/
├── README.md                            (this file)
├── COURSE_OVERVIEW.md                   (the story behind the course)
├── lessons/                             (six lessons, do them in order)
├── practice/                            (your hands-on workspace)
│   ├── CLAUDE.md                        (project context for Meridian Corp)
│   ├── requisitions.csv                 (500 rows, 5% with approval violations)
│   ├── purchase-orders.csv              (384 rows, pricing deviations planted)
│   ├── goods-receipts.csv               (273 rows, 20% quantity mismatches)
│   ├── invoices.csv                     (168 rows, 25% three-way-match exceptions)
│   ├── contracted-rates.csv             (10 items with contracted pricing)
│   ├── approval-matrix.csv              (5 approval levels by dollar threshold)
│   └── preferred-suppliers.csv          (20 preferred suppliers by category)
├── solutions/                           (reference answers; look only after attempting)
└── scripts/build_course_data.py         (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| practice/ | requisitions.csv | 500 requisitions over a 6-month window. Fields: REQ_ID, REQ_DATE, REQUESTER, DEPT, CATEGORY, SUPPLIER_ID, SUPPLIER_NAME, AMOUNT, APPROVER, APPROVER_ROLE, STATUS. About 5% (25 rows) carry approval-authority violations (for example, an Analyst approving a $12,000 requisition). |
| practice/ | purchase-orders.csv | 384 POs (one line per PO). Fields: PO_ID, LINE_NUMBER, REQ_ID, PO_DATE, SUPPLIER_ID, SUPPLIER_NAME, CATEGORY, ITEM_CODE, QUANTITY, PO_UNIT_PRICE, LINE_TOTAL, DEPT, REQUESTER, STATUS. Pricing deviations and PO-splitting patterns planted. |
| practice/ | goods-receipts.csv | 273 goods receipts. Fields: GR_ID, PO_ID, GR_DATE, SUPPLIER_ID, SUPPLIER_NAME, ITEM_CODE, PO_QTY, GR_QTY, QUALITY_ACCEPTED. About 20% have quantity mismatches. |
| practice/ | invoices.csv | 168 invoices. Fields: INV_ID, INV_DATE, PO_ID, SUPPLIER_ID, SUPPLIER_NAME, ITEM_CODE, INV_QTY, INV_UNIT_PRICE, INV_AMOUNT, DUE_DATE, PAYMENT_DATE, PAYMENT_TERMS. About 25% trigger three-way-match exceptions. 24 invoices carry "2/10 Net 30" early-payment discount terms. |
| practice/ | contracted-rates.csv | 10 contracted items. Fields: SUPPLIER_ID, SUPPLIER_NAME, ITEM_CODE, CATEGORY, CONTRACTED_UNIT_PRICE, UNIT_OF_MEASURE, EFFECTIVE_FROM, EFFECTIVE_TO. |
| practice/ | approval-matrix.csv | 5 levels: Analyst ($5,000), Manager ($25,000), Director ($100,000), VP ($500,000), CFO (Unlimited). |
| practice/ | preferred-suppliers.csv | 20 preferred suppliers by category. Fields: SUPPLIER_ID, SUPPLIER_NAME, CATEGORY, PREFERRED_FROM. |

Today's date in the data is **2026-04-25**. Annual spend: $140M. The data covers a 6-month transaction window.

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_P2P_Data_Architecture.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order. Each lesson adds a new compliance check to the system.
5. When stuck, check `solutions/`.
6. Lesson 6 teaches you to identify payment terms optimization opportunities so the system covers both compliance and savings.
