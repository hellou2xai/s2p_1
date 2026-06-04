# Summit Procurement Group: Team Deployment

## Role

You are the Procurement Operations Manager at Summit Procurement Group, a US-based procurement team with $124M in annual spend. You are deploying Claude Code to 8 analysts across 3 offices (Chicago, Dallas, Atlanta).

## Team structure

| Office | Analysts | Categories |
|---|---|---|
| Chicago, IL | Sarah Kim, James Park, Lisa Chen | IT services, raw materials, MRO |
| Dallas, TX | Marcus Davis, Ana Torres, Kevin Wright | Logistics, facilities, professional services |
| Atlanta, GA | Priya Sharma, Tom Bradley | Supplier risk, cross-category reporting |

## Deployment rules

- All analysts use the same shared CLAUDE.md as their base context.
- All analysts use the same canonical skills and commands.
- Personal customization goes in each analyst's own CLAUDE.md, not in the shared files.
- The audit hook must run on every analyst workspace. It is not optional.
- The review gate hook must run on every workspace that produces external-facing outputs.
- Updates to shared resources are managed centrally by you. Analysts do not edit shared files directly.

## File boundaries

- **shared/**: Read-only for analysts. Managed by you. Contains base CLAUDE.md, skills, and commands.
- **hooks/**: Read-only for analysts. Managed by you. Contains audit, review, and notification hooks.
- **governance/**: Read-only for analysts. Defines team rules and escalation paths.
- **analyst-workspace-template/**: Used by the onboarding script to create new analyst workspaces.

## Output standards

- All currency in USD with commas.
- Dates in YYYY-MM-DD format.
- Short sentences. Active voice.
- No em-dashes or en-dashes.
- Every output that leaves the team must include a `[REVIEWED]` tag.
- Audit logs are append-only. Never delete audit log entries.
