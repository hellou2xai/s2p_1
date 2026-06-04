# What Is Shared

These files are managed centrally by the Procurement Operations Manager. Analysts use them but do not edit them.

## Shared files

| File or folder | Purpose | Update frequency |
|---|---|---|
| shared/CLAUDE.md | Base context: org structure, categories, standards | Monthly or when org changes |
| shared/skills/ | Canonical analysis patterns | When a pattern is approved |
| shared/commands/ | Team-wide slash commands | When a new command is approved |
| hooks/ | Audit, review gate, notifications | When policy changes |
| governance/ | Team rules and escalation paths | Quarterly review |

## Update process

1. Operations Manager drafts the update.
2. One analyst from each office tests the update in their workspace.
3. Operations Manager publishes the update to shared/.
4. All analysts pull the update (or the onboarding script refreshes their workspace).

## Version tracking

Each shared file includes a version comment at the top (e.g., `v2.1, updated 2026-04-25`). Analysts report issues referencing the version number.
