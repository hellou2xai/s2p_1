# Course 14: Supplier Lifecycle Management

## Thirty suppliers, zero visibility

It is Tuesday morning, 07:45. You are the Supplier Relationship Manager at Crestview Industries, a US-based manufacturer with $38.6M in annual supplier spend. Your phone buzzes. The VP of Operations forwards a message from a plant manager: "Our fastener supplier missed the third delivery this quarter. Why are we still using them?"

You open your supplier tracker. It is a shared Excel file with 30 rows. The last update was six weeks ago. Three suppliers are marked "under review" but no one documented why. Two suppliers started onboarding in January and you do not know if they finished their compliance paperwork. One supplier was flagged for exit in Q3 2025, but they are still receiving orders.

The problem is not that you lack information. Performance scores exist. Compliance records exist. Development plans exist. The problem is that nothing connects them. Each lifecycle stage (onboarding, active, strategic, at risk, corrective action, exit) lives in a different file, owned by a different person, updated on a different schedule.

This course fixes that. You build a Claude Code system that tracks every supplier through every lifecycle stage. It detects when a supplier's performance drops below threshold and triggers corrective action. It monitors onboarding checklists and flags incomplete items. It generates exit plans when a relationship needs to end. One command gives you the full picture.

## What a supplier lifecycle system does

A supplier lifecycle system tracks each supplier's journey from first contact to final exit. It connects performance data, compliance status, and development plans into a single view. Instead of checking four spreadsheets, you run one command.

| Without lifecycle management | With lifecycle management |
|---|---|
| Supplier stages tracked in a shared spreadsheet, updated monthly | Stages computed from live data, updated on demand |
| At-risk suppliers discovered only after a delivery failure | Performance trends detected before they become incidents |
| Onboarding checklists tracked by email | Automated checklist with compliance validation |
| Exit decisions delayed because no one owns the process | Exit workflow triggered by criteria, with clear steps |
| Development plans reviewed quarterly at best | Plans tracked with next-review alerts |

## The practice scenario

Crestview Industries is a US-based manufacturer with $38.6M in annual supplier spend across 30 suppliers. You are the Supplier Relationship Manager, reporting to the Director of Procurement. Your supplier portfolio breaks down by lifecycle stage:

| Lifecycle stage | Supplier count | Example supplier | Key concern |
|---|---|---|---|
| Onboarding | 3 | Summit Electrical (SUP025) | Compliance paperwork incomplete |
| Active | 15 | Great Lakes Steel (SUP001) | Routine monitoring, no action needed |
| Strategic | 3 | Heartland Polymers (SUP002) | Development plan review due |
| At risk | 3 | Apex Electronics (SUP004) | Quality score dropped 18 points in 2 quarters |
| Corrective action | 2 | Frontier Machining (SUP015) | 90-day improvement plan, 30 days remaining |
| Exit | 2 | Regional Supply Co (SUP023) | Transition plan needed, orders still active |
| Under review | 2 | Coastal Coatings (SUP010) | Stage assignment pending data review |

Today's date is **2026-04-25**. Your Director wants a full lifecycle status report by Friday.

## What you will build

```
supplier-lifecycle-2026/
├── .claude/
│   ├── settings.json                (permissions, hooks)
│   └── commands/
│       ├── lifecycle-status.md      (full portfolio status report)
│       ├── onboard-supplier.md      (run onboarding checklist for a supplier)
│       └── trigger-exit.md          (initiate exit workflow)
├── CLAUDE.md                        (role, lifecycle stages, transition criteria)
├── data/
│   ├── supplier-master.csv          (30 suppliers, read-only)
│   ├── performance-history.csv      (120 rows, read-only)
│   ├── compliance-status.csv        (30 rows, read-only)
│   └── development-plans.csv        (10 plans, read-only)
├── state/
│   ├── lifecycle-state.json         (current stage for each supplier)
│   └── transition-log.md            (stage changes with timestamps)
├── outputs/
│   ├── segmentation-report.md       (tier and stage analysis)
│   ├── onboarding-checklists/       (per-supplier onboarding status)
│   ├── corrective-action-plans/     (improvement plans for at-risk suppliers)
│   └── exit-plans/                  (transition plans for exiting suppliers)
└── skills/
    ├── assess-lifecycle-stage.md    (stage assessment pattern)
    └── detect-risk-triggers.md      (at-risk detection pattern)
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | Supplier segmentation and lifecycle stages: classifying 30 suppliers by tier and stage | 55 min |
| 2 | Onboarding automation: building checklists that validate compliance before activation | 50 min |
| 3 | Strategic development plans: tracking improvement targets and review dates | 55 min |
| 4 | At-risk detection and corrective action: spotting declining performance and triggering response | 60 min |
| 5 | Exit management: building transition plans and tracking order wind-down | 50 min |
| 6 | Relationship state persistence: saving lifecycle state between sessions | 50 min |

Total: about 6 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. You run `/lifecycle-status` and Claude Code produces a report showing all 30 suppliers grouped by lifecycle stage, with the correct stage for each based on performance, compliance, and development data.
2. The onboarding command generates a compliance checklist for a new supplier and flags any missing items (insurance, NDA, ISO certification, background check, financial review).
3. The system detects at least two suppliers whose performance scores dropped below threshold across two consecutive quarters and recommends corrective action.
4. A corrective action plan for an at-risk supplier includes three specific improvement targets, a 90-day timeline, and a review date.
5. An exit plan for a departing supplier lists active orders to transition, alternative suppliers, a timeline, and a risk summary.
6. Lifecycle state persists in state/lifecycle-state.json. When you close and reopen Claude Code, the system remembers each supplier's current stage and last transition date.
