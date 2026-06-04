<!-- v1.0 2026-04-25 Initial. -->

# Deployment Checklist (Reference Solution)

Use this checklist before, during, and after deploying Claude Code to the team.

## Pre-deployment (complete before day 1)

- [ ] Shared CLAUDE.md finalized and reviewed by VP.
- [ ] Three canonical skills tested against sample data from all six categories.
- [ ] Three canonical commands tested and producing correct output format.
- [ ] Audit log hook tested: creates .jsonl file, appends entries, does not block.
- [ ] Review gate hook tested: blocks Write to outputs/ without `[REVIEWED]` tag, approves with tag.
- [ ] Team notify hook tested: logs entries for trigger keywords, does not block.
- [ ] Onboarding script tested on a clean machine (no pre-existing configuration).
- [ ] Governance documents (what-is-shared.md, what-is-personal.md, escalation-policy.md) reviewed by team lead.
- [ ] Python version compatibility confirmed: all three hooks run on Python 3.9, 3.10, 3.11, and 3.12.
- [ ] Analyst workspace template tested: placeholder replacement works for all fields.

## Day 1: First wave (Chicago office, 3 analysts)

- [ ] Run onboarding script for Sarah Kim.
- [ ] Run onboarding script for James Park.
- [ ] Run onboarding script for Lisa Chen.
- [ ] Each analyst updates their personal CLAUDE.md with current priorities.
- [ ] Each analyst runs `/daily-check` and confirms output.
- [ ] Each analyst runs `/category-brief [category]` for their primary category.
- [ ] Audit log files exist for all three analysts.
- [ ] No review gate false positives reported.

## Day 2: Second wave (Dallas office, 3 analysts)

- [ ] Run onboarding script for Marcus Davis.
- [ ] Run onboarding script for Ana Torres.
- [ ] Run onboarding script for Kevin Wright.
- [ ] Each analyst updates their personal CLAUDE.md with current priorities.
- [ ] Each analyst runs `/daily-check` and confirms output.
- [ ] Each analyst runs `/category-brief [category]` for their primary category.
- [ ] Audit log files exist for all three analysts.
- [ ] Check in with Chicago analysts for any issues from day 1.

## Day 3: Third wave (Atlanta office, 2 analysts)

- [ ] Run onboarding script for Priya Sharma.
- [ ] Run onboarding script for Tom Bradley.
- [ ] Each analyst updates their personal CLAUDE.md with current priorities.
- [ ] Each analyst runs `/daily-check` and confirms output.
- [ ] Priya runs `/risk-scan` and confirms cross-category risk output.
- [ ] Audit log files exist for all eight analysts.
- [ ] Check in with Chicago and Dallas analysts for any issues.

## Week 1 review (end of day 5)

- [ ] Run audit log analysis across all eight analyst workspaces.
- [ ] Calculate adoption rate (target: 100%).
- [ ] Calculate average onboarding time (target: under 10 minutes).
- [ ] Collect time-saved estimates from each analyst.
- [ ] Identify any analysts with zero or low usage and follow up.
- [ ] Identify any recurring review gate blocks and provide training.
- [ ] Document any shared resource issues raised during the week.
- [ ] Update shared CLAUDE.md or skills if any issues required changes.

## Week 2 review (end of day 10)

- [ ] Run audit log analysis for week 2.
- [ ] Compare week 2 metrics to week 1 (adoption, usage, time saved).
- [ ] Confirm all eight analysts are active.
- [ ] Confirm no unresolved escalations.
- [ ] Present deployment summary to VP: adoption rate, time saved, and next steps.
- [ ] Plan monthly review cadence for shared resources.

## Success criteria

The deployment is successful when:

1. All 8 analysts ran at least 3 sessions in week 2.
2. Average onboarding time was under 10 minutes.
3. Average time saved is 3 or more hours per analyst per week.
4. Zero unresolved escalations at end of week 2.
5. Audit logs are complete for all sessions (no gaps).
