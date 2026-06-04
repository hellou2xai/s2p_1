# Course 8: The Project Architect

## Every Monday starts from scratch

It is Monday morning. You open Claude Code to check on the savings program. You type: "What is the status of the direct materials consolidation initiative?"

Claude Code responds: "I don't have context about a direct materials consolidation initiative. Could you provide more details?"

You spent 45 minutes last Thursday building a detailed status update for exactly this initiative. You reviewed the savings log, checked the milestone tracker, identified two overdue milestones, and drafted an escalation note. All of that context vanished when you closed the session.

You try again: "Read initiatives.csv and savings-log.csv. Show me INIT-001 status." Claude Code reads the files, but it does not know about the escalation note you wrote Thursday. It does not know you decided to push the milestone deadline to May 15. It does not know the VP approved the revised timeline.

Every Monday, you rebuild context from scratch. Every Thursday's decisions evaporate by Friday.

This course fixes that. You build a **Claude Code project**: a persistent workspace where initiative status, decisions, and program state are maintained in files that survive between sessions. When you open Claude Code on Monday, it reads the initiative tracker, sees the current stage and status, and picks up where you left off.

## What a Claude Code project is

A Claude Code project is a folder with a `.claude/` directory inside it. When you run `claude` inside that folder, Claude Code reads `.claude/settings.json` for hook registrations, tool permissions, and MCP connections. It reads `CLAUDE.md` for standing context. These persist across sessions because they are files on disk, not conversation history.

The key insight: **conversation history is ephemeral, but files are permanent.** If you write a decision to a file during a session, the next session can read that file. If you maintain an initiative tracker as a markdown file, every session starts with current state.

What a project gives you:

| Without a project | With a project |
|---|---|
| Every session starts blank | Every session reads CLAUDE.md and state files |
| Decisions are lost when the session ends | Decisions are appended to decisions-log.md |
| Initiative status is re-derived every time | Initiative status is read from initiative-tracker.md |
| Hooks must be registered manually | Hooks are registered in .claude/settings.json |
| Commands are temporary | Commands persist in .claude/commands/ |

## The practice scenario

Pinnacle Procurement is a US-based procurement team managing a $14.9M annual savings program across eight category initiatives. You are the Savings Program Manager.

Today's date is **2026-04-25**. Your eight initiatives:

| Initiative | Category | Target | Stage | Status |
|---|---|---|---|---|
| Direct Materials Consolidation | direct-materials | $2.8M | Execution | On track |
| Logistics Network Optimization | logistics | $2.2M | Sourcing | At risk |
| IT Services Rationalization | it-services | $1.9M | Execution | On track |
| Facilities Management Rebid | facilities | $1.5M | Planning | On track |
| Professional Services Rate Card | professional-services | $1.8M | Negotiation | On track |
| MRO Catalog Standardization | mro | $1.2M | Planning | Not started |
| Packaging Material Switch | direct-materials | $1.6M | Evaluation | Behind schedule |
| Temp Staffing Consolidation | professional-services | $1.9M | Execution | On track |

Your VP wants a weekly review every Monday. Your CFO wants a monthly savings update. Both need current data and context from the last session.

## What you will build

```
savings-program-2026/
├── .claude/
│   ├── settings.json            (permissions, hooks, MCP connections)
│   └── commands/
│       ├── initiative-status.md (per-initiative status check)
│       └── weekly-review.md     (consolidated weekly review)
├── CLAUDE.md                    (full portfolio, stage definitions, contacts)
├── state/
│   ├── initiative-tracker.md    (current status per initiative, updated each session)
│   └── decisions-log.md         (key decisions recorded across sessions)
├── initiatives/                 (initiative-specific working files)
├── data/                        (source data files)
└── outputs/weekly-reviews/      (weekly review outputs)
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | What a Claude Code project is: .claude/, settings.json, and project vs. global config | 30 min |
| 2 | Project CLAUDE.md: encoding all eight initiatives with stage and status | 45 min |
| 3 | Persistent state with files: maintaining an initiative tracker across sessions | 50 min |
| 4 | The decisions log pattern: appending decisions to a persistent file | 40 min |
| 5 | Project-level settings.json: tool permissions, hooks, and MCP connections | 40 min |
| 6 | Team project sharing: git repository, CLAUDE.md updates, state file conventions | 35 min |

Total: about 4.5 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. Your project has a CLAUDE.md with all eight initiatives, stages, and stakeholders encoded.
2. You have an initiative-tracker.md in state/ that the session reads on startup and updates on close.
3. You run `/initiative-status direct-materials` and get a scoped update with savings data and milestone status.
4. You close the session, reopen Claude Code, and run `/initiative-status direct-materials` again. The state from the previous session is preserved.
5. You have a decisions-log.md with at least three entries from different sessions.
6. You can explain the difference between project-level and global settings, and when to use each.
