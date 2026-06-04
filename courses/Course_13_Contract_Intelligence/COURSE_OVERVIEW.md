# Course 13: Contract Intelligence

## 180 contracts, six weeks, one board review

It is Monday morning, 08:00. You are the new Contract Intelligence Lead at Vanguard Manufacturing, a US-based industrial company. Your predecessor left three weeks ago. The handover was a shared drive with 180 supplier agreements in mixed formats, a half-finished Excel tracker, and a sticky note that says "board risk review June 6."

The General Counsel's office wants a full contract risk profile before that board meeting. That means: every agreement cataloged, every obligation mapped, every renewal date flagged, every liability cap documented. Six weeks to go. The Excel tracker has 40 contracts entered. The other 140 are sitting in folders, unread.

You cannot read 140 contracts in six weeks while also doing your day job. You need a system that extracts key terms from contracts, maps obligations, tracks renewals, and alerts you when action is needed. This course teaches you to build that system with Claude Code.

## What a contract intelligence system does

A contract intelligence system reads supplier agreements, extracts structured data, and maintains a living register of obligations, dates, and risks. Instead of opening each contract and copying terms into a spreadsheet, you point Claude Code at a folder. It reads each agreement, extracts the fields you define, validates the output against your clause taxonomy, and writes the results to a structured register.

| Without contract intelligence | With contract intelligence |
|---|---|
| Read each contract manually, 45 min per agreement | Claude Code extracts key terms in under 2 min per contract |
| Obligation tracking in a spreadsheet, updated quarterly | Obligations mapped automatically, flagged when due |
| Renewal dates buried in contract text | Renewal calendar generated from extracted dates |
| New contracts arrive by email, sit unprocessed for weeks | Intake trigger detects new files and processes them on arrival |
| Contract drafting starts from scratch each time | Templates with pre-filled terms from existing agreements |

## The practice scenario

Vanguard Manufacturing is a US-based industrial company with $42M in annual procurement spend. You are the Contract Intelligence Lead, reporting to the VP of Legal and Procurement. Your portfolio includes 180 active supplier agreements. For this course, you work with a representative sample of 20 contracts across five categories.

| Category | Contracts | Combined annual value | Key risk |
|---|---|---|---|
| Raw materials | 5 | $3.2M | Price escalation clauses, single-source exposure |
| IT services | 4 | $2.4M | Auto-renewal traps, SLA compliance |
| Facilities | 4 | $1.8M | Liability caps below market standard |
| Logistics | 4 | $1.6M | Termination notice windows closing soon |
| Professional services | 3 | $0.8M | IP ownership ambiguity |

Today's date is **2026-04-25**. The board risk review is scheduled for **2026-06-06**. You have six weeks.

## What you will build

```
contract-intelligence-2026/
├── .claude/
│   ├── settings.json                (permissions, hooks)
│   └── commands/
│       ├── extract-contract.md      (extract terms from a single contract)
│       ├── scan-intake.md           (process all new contracts in intake/)
│       └── renewal-report.md        (generate renewal calendar)
├── CLAUDE.md                        (role, extraction standards, clause taxonomy)
├── data/
│   ├── contract-register.csv        (structured register, updated by extraction)
│   ├── clause-taxonomy.csv          (15 clause types with risk weights)
│   ├── contracts/                   (source contract files, read-only)
│   ├── intake/                      (new contracts land here)
│   └── processed/                   (extracted contracts move here)
├── outputs/
│   ├── extraction-reports/          (per-contract extraction summaries)
│   ├── obligation-map.md            (consolidated obligation tracker)
│   └── renewal-calendar.md          (60-day and 90-day renewal alerts)
└── skills/
    ├── extract-clauses.md           (clause extraction pattern)
    └── draft-contract.md            (contract drafting from template)
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | Contract data extraction: reading agreements and pulling structured fields | 55 min |
| 2 | Obligation mapping: building a tracker from extracted terms | 50 min |
| 3 | Building the contract register: validating and cataloging 20 agreements | 55 min |
| 4 | Renewal calendar and monitoring: flagging what expires and when | 50 min |
| 5 | Intake trigger hook: auto-processing new contracts on arrival | 50 min |
| 6 | Contract drafting from templates: generating new agreements with pre-filled terms | 60 min |

Total: about 6 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. You point Claude Code at a contract file and it extracts all 15 clause types from the taxonomy, with values, dates, and risk flags for each.
2. The obligation map lists every material obligation from the 20 contracts, grouped by supplier and sorted by due date.
3. The contract register has 20 rows with no missing fields. Every row has a contract ID, supplier name, annual value, start date, end date, and risk level.
4. The renewal calendar flags every contract expiring within 90 days and every auto-renewal notice window closing within 60 days.
5. When you drop a new contract file into intake/, the intake trigger extracts its terms, updates the register, and moves the file to processed/.
6. You can generate a draft contract for a new supplier using an existing agreement as a template, with terms pre-filled from the register.
