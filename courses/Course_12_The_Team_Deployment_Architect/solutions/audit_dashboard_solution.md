<!-- v1.0 2026-04-25 Initial. -->

# Audit Log Analysis (Reference Solution)

A pattern for analyzing the team audit trail to track adoption, usage patterns, and compliance.

## Reading the audit log

Each analyst's workspace produces a daily audit log file in `audit-logs/audit-YYYY-MM-DD.jsonl`. Each line is a JSON object:

```json
{
  "timestamp": "2026-04-25T14:32:18.000000+00:00",
  "tool": "Write",
  "target": "outputs/category-brief-it-services-2026-04-25.md",
  "analyst": "Sarah Kim",
  "session": "20260425-091500"
}
```

## Analysis prompt

Use this prompt in Claude Code to analyze a day's audit logs:

```
Read all .jsonl files in audit-logs/ from the last 7 days. For each day,
calculate:

1. Total tool calls per analyst.
2. Most-used tools per analyst (top 3).
3. Number of Write calls to outputs/ (completed deliverables).
4. Number of review gate blocks (Write attempts to outputs/ that were blocked).
5. Number of unique sessions per analyst.

Produce a weekly usage summary table:

| Analyst | Sessions | Tool calls | Outputs produced | Review blocks |
|---|---|---|---|---|

Then answer these questions:
- Which analyst is using Claude Code most actively?
- Which analyst has not used it in the last 3 days? (May need support.)
- Are any analysts consistently getting review gate blocks? (May need training
  on the [REVIEWED] tag.)

Save the summary to outputs/audit-summary-YYYY-MM-DD.md.
```

## Three deployment metrics

Track these three metrics weekly:

### 1. Adoption rate

**Definition**: Number of analysts who ran at least one Claude Code session in the past 7 days, divided by total analysts (8).

**Target**: 100% by week 2.

**How to calculate**: Count unique `analyst` values across all audit log files from the past 7 days.

### 2. Average onboarding time

**Definition**: Time from running the onboarding script to the analyst's first completed output (first Write to outputs/).

**Target**: Under 10 minutes.

**How to calculate**: Compare the `.env` creation timestamp with the first audit log entry where `target` contains `outputs/`.

### 3. Weekly time saved per analyst

**Definition**: Hours saved per analyst per week compared to doing the same tasks manually.

**Target**: 3 to 5 hours per analyst per week.

**How to calculate**: Survey each analyst at the end of week 1 and week 2. Ask: "List the tasks you used Claude Code for this week and estimate how long each would have taken without it." Track the total.

## Sample dashboard output

```
## Team Deployment Dashboard: Week of 2026-04-21

### Adoption
- Active analysts: 7 of 8 (87.5%)
- Inactive: Tom Bradley (Atlanta). Last session: 2026-04-22. Follow up.

### Usage
| Analyst | Sessions | Tool calls | Outputs | Blocks |
|---|---|---|---|---|
| Sarah Kim | 8 | 142 | 12 | 1 |
| James Park | 5 | 89 | 7 | 0 |
| Lisa Chen | 4 | 67 | 5 | 2 |
| Marcus Davis | 7 | 128 | 10 | 0 |
| Ana Torres | 6 | 104 | 8 | 0 |
| Kevin Wright | 5 | 91 | 6 | 1 |
| Priya Sharma | 6 | 112 | 9 | 0 |
| Tom Bradley | 1 | 12 | 1 | 0 |

### Time savings (self-reported, week 1)
- Average: 3.2 hours saved per analyst per week
- Range: 1.5 hours (Tom Bradley) to 5.1 hours (Sarah Kim)
- Top use case: category briefings (saved 45 minutes each, 3 per week)

### Actions
1. Follow up with Tom Bradley. Only one session this week. May need
   additional onboarding support.
2. Lisa Chen had 2 review gate blocks. Remind her about the [REVIEWED]
   tag requirement.
3. Schedule week 2 check-in with all analysts for Friday.
```
