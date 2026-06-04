# Course 12: The Team Deployment Architect

## It works on your laptop, but not on theirs

You built the system. It runs perfectly on your machine. Six categories monitored. Hooks logging every action. Skills producing consistent outputs. Commands saving you two hours every Monday.

Then your VP says: "Roll this out to the team."

You send the folder to Sarah in Chicago. She opens Claude Code and types the first command. Nothing works. Her CLAUDE.md is missing the category definitions. She does not have the skills folder. The hooks reference a path that does not exist on her machine. She spends 45 minutes troubleshooting before giving up.

You try again with Marcus in Dallas. You add better instructions. He gets further, but the audit hook fails because he has Python 3.9 instead of 3.11. The review gate blocks his first output because he did not know about the review tag convention. He calls you. You walk him through it over the phone for 30 minutes.

By the third analyst, you realize: building the system was the easy part. Deploying it to a team is the hard part.

This course teaches you to make the deployment reproducible, governed, and auditable. A new analyst runs one onboarding script and gets a fully configured workspace in under 10 minutes. Every analyst uses the same shared context, the same canonical skills, and the same audit trail. Personal customization happens in a defined space that does not break the shared configuration.

## What team deployment requires

Team deployment is not just copying a folder. It requires five things:

| Requirement | What it means |
|---|---|
| Reproducibility | Every analyst gets the same base configuration, every time. No manual setup steps. |
| Governance | Clear rules about what is shared (and cannot be modified by individuals) and what is personal. |
| Auditability | Every significant action is logged. A manager can review what the system did and when. |
| Onboarding speed | A new analyst goes from zero to operational in under 10 minutes. |
| Graceful evolution | Updates to shared resources propagate to all analysts without breaking personal customizations. |

## The practice scenario

Summit Procurement Group is a US-based procurement team with $124M in annual spend. You are the Procurement Operations Manager responsible for tooling and process. Your team:

| Office | Analysts | Categories covered |
|---|---|---|
| Chicago, IL | 3 | IT services, raw materials, MRO |
| Dallas, TX | 3 | Logistics, facilities, professional services |
| Atlanta, GA | 2 | Cross-category support, supplier risk, reporting |

Today's date is **2026-04-25**. Your VP has approved the Claude Code deployment. You have 2 weeks to get all 8 analysts operational.

The team analysts:

| Name | Office | Role | Experience |
|---|---|---|---|
| Sarah Kim | Chicago | Senior Category Manager, IT | 8 years |
| James Park | Chicago | Category Analyst, Raw Materials | 3 years |
| Lisa Chen | Chicago | Category Analyst, MRO | 2 years |
| Marcus Davis | Dallas | Senior Category Manager, Logistics | 10 years |
| Ana Torres | Dallas | Category Analyst, Facilities | 4 years |
| Kevin Wright | Dallas | Category Analyst, Professional Services | 5 years |
| Priya Sharma | Atlanta | Supplier Risk Analyst | 6 years |
| Tom Bradley | Atlanta | Reporting Analyst | 3 years |

## What you will build

```
team-deployment/
├── shared/                              (team-wide resources, managed centrally)
│   ├── CLAUDE.md                        (base context all analysts inherit)
│   ├── skills/                          (canonical skills, same for everyone)
│   │   ├── spend-analysis.md
│   │   ├── supplier-scorecard.md
│   │   └── contract-review.md
│   └── commands/                        (canonical commands, same for everyone)
│       ├── daily-check.md
│       ├── category-brief.md
│       └── risk-scan.md
├── hooks/                               (team hooks, managed centrally)
│   ├── audit-log.py
│   ├── review-gate.py
│   └── team-notify.py
├── analyst-workspace-template/          (template for new analyst setup)
│   ├── .claude/
│   │   ├── settings.json               (pre-configured with hooks and permissions)
│   │   └── commands/                    (symlinks or copies of shared commands)
│   ├── CLAUDE.md                        (analyst-specific context placeholder)
│   ├── data/                            (analyst's working data)
│   └── outputs/                         (analyst's outputs)
├── governance/
│   ├── what-is-shared.md
│   ├── what-is-personal.md
│   └── escalation-policy.md
└── scripts/
    └── onboard-analyst.sh               (one-command setup for new analysts)
```

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | Shared vs. personal boundary: what the team shares and what each analyst owns | 45 min |
| 2 | Audit hook for teams: logging every significant action to a central trail | 50 min |
| 3 | Review gate hook: requiring approval tags before outputs ship | 50 min |
| 4 | Onboarding script: zero to operational in under 10 minutes | 55 min |
| 5 | Governance in practice: update propagation, conflict resolution, and escalation | 45 min |
| 6 | Measuring deployment: adoption metrics, quality metrics, and time savings | 35 min |

Total: about 5 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. You can explain which files are shared (same for all analysts) and which are personal (customized per analyst), and why.
2. The audit hook logs every Write and Bash tool call to a timestamped audit trail file.
3. The review gate hook blocks any Write to the outputs/ folder unless the content includes a `[REVIEWED]` tag.
4. You run the onboarding script for a new analyst and they have a working workspace in under 10 minutes, with shared context, skills, commands, and hooks.
5. You have a governance document that defines escalation paths for three scenarios: hook failure, shared resource conflict, and output quality dispute.
6. You can report three deployment metrics: analyst adoption rate, average onboarding time, and weekly time saved per analyst.
