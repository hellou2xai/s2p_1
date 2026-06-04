# Course 21: Compliance, Policy, and Audit Readiness

A short course (about 4.5 hours) that teaches you to build a **compliance monitoring system**: policy encoding as testable rules, automated compliance checking, append-only audit trails, and audit evidence packaging. No coding required.

## What you will end up with

A compliance monitoring pipeline that checks 200 transactions against encoded policy rules, generates exception reports, maintains an append-only compliance ledger, and assembles audit evidence packages. The breach escalation hook triggers when the violation count exceeds the threshold.

## What is in this course folder

```
Course_21_Compliance_Policy_Audit/
├── README.md                          (this file)
├── COURSE_OVERVIEW.md                 (the story)
├── lessons/                           (six lessons, in order)
├── practice/
│   ├── CLAUDE.md                      (Meridian Corp compliance context)
│   └── data/
│       ├── transactions.csv           (200 rows, 55 planted violations)
│       ├── approval-matrix.csv        (5 authority levels)
│       ├── preferred-suppliers.csv    (10 preferred suppliers)
│       ├── contract-documentation.csv (required docs per contract type)
│       └── policy-rules.json          (testable compliance rules)
├── solutions/
└── scripts/build_course_data.py
```

You create `Drafts/`, `outputs/`, `hooks/`, and `.claude/` as you work through the lessons. Lessons 2 to 4 save reports under `Drafts/`. Lesson 5 sets up the hook directories and the compliance ledger at `outputs/compliance-ledger.jsonl`. Lesson 6 builds the audit package under `outputs/audit-packages/`.

## What is in the practice data

| File | Contents |
|---|---|
| transactions.csv (200 rows) | 145 compliant transactions and 55 violations: approval authority breaches, non-preferred suppliers, missing documentation, and suspected split orders. |
| approval-matrix.csv (5 levels) | Authority thresholds: Analyst ($0-5K), Manager ($5K-25K), Director ($25K-100K), VP ($100K-500K), CFO ($500K+). |
| preferred-suppliers.csv (10 suppliers) | The approved supplier list. Any purchase from a non-listed supplier is a violation. |
| contract-documentation.csv (15 rows) | Required documents per contract type (MSA, SOW, NDA, SLA, amendment). |
| policy-rules.json | Testable rules: approval authority, preferred supplier, documentation completeness, split order detection (5-day window, $5K threshold), breach escalation at 15 violations. |

Today's date is **2026-04-25**.
