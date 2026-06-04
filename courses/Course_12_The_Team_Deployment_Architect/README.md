# Course 12: The Team Deployment Architect

A short course (about 5 hours) that teaches you to deploy your Claude Code agentic system to a team of 8 procurement analysts across 3 offices. The system must be reproducible, governed, and auditable. A new analyst gets operational in under 10 minutes. No coding required beyond copy-paste prompts and scripts.

## What you will end up with

A deployment package that any procurement analyst can install in under 10 minutes. It includes a shared CLAUDE.md, three canonical skills, three canonical commands, audit and review hooks, and a governance framework. When a new analyst joins the team, you run one onboarding script and they have a fully configured workspace with the same context, commands, and guardrails as everyone else.

After Course 12, your agentic system works for a team, not just for you.

## What you need before you start

- Courses 1 through 11 finished. You know CLAUDE.md, skills, commands, sub-agents, hooks, projects, MCP, composition systems, and orchestration.
- A laptop with Claude Code installed and signed in.
- About 5 hours, in two or three sittings.

## What is in this course folder

```
Course_12_The_Team_Deployment_Architect/
├── README.md                              (this file)
├── COURSE_OVERVIEW.md                     (the story behind the course)
├── lessons/                               (six lessons, do them in order)
├── practice/                              (your hands-on workspace)
│   ├── CLAUDE.md                          (project context for Summit Procurement Group)
│   ├── shared/
│   │   ├── CLAUDE.md                      (base context shared by all analysts)
│   │   ├── skills/
│   │   │   ├── spend-analysis.md          (canonical spend analysis skill)
│   │   │   ├── supplier-scorecard.md      (canonical scorecard skill)
│   │   │   └── contract-review.md         (canonical contract review skill)
│   │   └── commands/
│   │       ├── daily-check.md             (canonical daily check command)
│   │       ├── category-brief.md          (canonical category brief command)
│   │       └── risk-scan.md               (canonical risk scan command)
│   ├── hooks/
│   │   ├── audit-log.py                   (logs every tool call to audit trail)
│   │   ├── review-gate.py                 (blocks writes without review tag)
│   │   └── team-notify.py                 (sends notification on key events)
│   ├── analyst-workspace-template/        (template folder for new analysts)
│   └── governance/
│       ├── what-is-shared.md              (what the team shares and why)
│       ├── what-is-personal.md            (what each analyst customizes)
│       └── escalation-policy.md           (when to escalate, to whom)
├── solutions/                             (reference answers; look only after attempting)
│   ├── onboarding_script_solution.md      (reference onboarding script)
│   ├── audit_dashboard_solution.md        (reference audit log analysis)
│   └── deployment_checklist_solution.md   (reference deployment checklist)
└── scripts/build_course_data.py           (regenerates the practice data if you delete it)
```

## What is in the practice data (data quality)

| Location | File | Contents |
|---|---|---|
| shared/ | CLAUDE.md | Base context for all analysts: team name, categories, standards, output rules. |
| shared/skills/ | 3 skill files | Spend analysis, supplier scorecard, and contract review patterns. |
| shared/commands/ | 3 command files | Daily check, category brief, and risk scan commands. |
| hooks/ | 3 hook scripts | Audit logging, review gating, and team notification hooks. |
| analyst-workspace-template/ | (template) | Starter folder structure for a new analyst workspace. |
| governance/ | 3 governance docs | Shared vs. personal boundaries, and escalation policy. |

Today's date in the data is **2026-04-25**. Team: 8 analysts across 3 US offices (Chicago, Dallas, Atlanta).

## How to work through it

1. Read `COURSE_OVERVIEW.md`. It tells you the story.
2. Open `lessons/Lesson_01_Shared_vs_Personal_Boundary.md`. Follow along.
3. Each lesson tells you exactly what to type and what you should see.
4. Do each lesson in order. Each lesson builds on the previous one.
5. When stuck, check `solutions/`.
6. Lesson 6 teaches you to measure deployment success with concrete metrics.
