# Lesson 6: Measuring Deployment Success

**Time:** 25 minutes.

## The CPO asks: "Is this working?"

It is 09:00 on a Monday, 30 days after you deployed Claude Code to eight analysts. Your CPO calls: "We spent $14,000 on licenses and training. What have we gotten back? I need numbers for the quarterly business review." You open your laptop. You have audit logs, output files, and analyst feedback. But nobody has been tracking metrics. You cannot answer the question. In this lesson, you define six procurement metrics, build a measurement framework, and show how to report deployment ROI in the first 90 days.

## What Claude Code is going to do for you

You will create a metrics tracking file and a measurement command. The command reads the audit log, counts outputs by type, estimates time saved, and produces a deployment report. After this lesson, you can answer "Is this working?" with numbers, not opinions.

## Set up

1. Navigate to the practice folder:

```
cd "Course_12_The_Team_Deployment_Architect/practice"
```

2. Start Claude Code:

```
claude
```

3. Confirm you have an audit log with entries:

```
Read governance/audit-log.csv. How many entries are there?
```

You should see at least 5 entries from the previous lessons.

**Folder layout:**

```
practice/
├── governance/
│   ├── audit-log.csv
│   └── access-rules.md
├── analyst-workspaces/
│   ├── analyst_01_chen/
│   ├── analyst_02_reeves/
│   └── analyst_03_sharma/
├── shared/
└── Outputs/
```

## Step-by-step

### Step 1: Define the six metrics

```
Create a file at governance/metrics-framework.md. Define six metrics for measuring Claude Code deployment success in the first 90 days: 1) Documents produced per analyst per week (count from audit log). 2) Average time to first draft (estimated from audit log timestamps, in minutes). 3) Review gate pass rate (percentage of Outputs/ writes that pass the review gate on the first attempt). 4) Audit compliance rate (percentage of file writes that have a matching audit log entry). 5) Estimated hours saved per week (based on document type and pre-Claude baseline times). 6) Error escalation rate (percentage of outputs routed to human review). For each metric, define: the metric name, the data source, the calculation method, the target for 90 days, and the baseline (pre-Claude) value.
```

**What you should see.** Claude creates the file with six metric definitions. Each one has a clear calculation method and target.

### Step 2: Set baseline values

```
Update governance/metrics-framework.md. For each metric, add a baseline value based on pre-Claude manual work: 1) Documents produced: 3 per analyst per week. 2) Time to first draft: 120 minutes average. 3) Review gate pass rate: N/A (no gate existed). 4) Audit compliance: 40% (manual log was often skipped). 5) Hours saved: 0 (baseline). 6) Error escalation rate: N/A (no escalation process existed). Set 90-day targets: 1) 8 documents per analyst per week. 2) 15 minutes average. 3) 85% first-attempt pass rate. 4) 100% compliance. 5) 12 hours saved per analyst per week. 6) Below 10% escalation rate.
```

**What you should see.** Claude updates the file with baseline and target values for each metric.

### Step 3: Calculate metrics from the audit log

```
Read governance/audit-log.csv. Calculate: 1) Total documents produced (count of unique file paths). 2) Documents per analyst (group by analyst_id). 3) Audit compliance rate (are there any file writes in Outputs/ that do NOT have an audit log entry? If all writes are logged, compliance is 100%).
```

**What you should see.** Claude reports the counts. For example: "Total documents: 7. Lisa Chen: 3. Marcus Reeves: 2. Priya Sharma: 2. Audit compliance: 100% (all writes are logged)."

### Step 4: Estimate time savings

```
For each document type in the audit log (contract recommendation, scorecard refresh, spend analysis, etc.), estimate the pre-Claude time (in minutes) and the with-Claude time. Use these baselines: contract recommendation: 90 minutes manual, 12 minutes with Claude. Scorecard refresh: 60 minutes manual, 8 minutes with Claude. Spend analysis: 120 minutes manual, 15 minutes with Claude. Test files: 0 savings. Calculate total estimated time saved across all logged documents.
```

**What you should see.** A table showing document types, counts, time per document (before and after), and total minutes saved. For example: "Total estimated time saved: 6.2 hours across 7 documents."

### Step 5: Build the measurement command

```
Create a command file at .claude/commands/deployment-report.md with this content: "Generate a deployment metrics report. Steps: 1) Read governance/audit-log.csv. 2) Count documents produced per analyst. 3) Calculate audit compliance rate. 4) Estimate time saved using the baselines in governance/metrics-framework.md. 5) Check Drafts/human_review.md (if it exists) for escalation count. 6) Write the report to Outputs/deployment_report_[date].md with: date, analyst activity summary, six metrics with current values versus targets, and a three-sentence executive summary for the CPO."
```

**What you should see.** Claude creates the command file.

### Step 6: Run the command

```
/deployment-report
```

**What you should see.** Claude reads the audit log, calculates the metrics, and writes a report to `Outputs/deployment_report_2026-04-25.md`. The report includes the six metrics, current values versus targets, and an executive summary.

### Step 7: Review the executive summary

```
Read the executive summary in Outputs/deployment_report_2026-04-25.md. Does it name the number of analysts, the total documents produced, and the estimated hours saved? Does it include a dollar figure for the ROI calculation?
```

**What you should see.** A summary like: "In the first 30 days, 3 analysts produced 7 documents using Claude Code. Estimated time savings: 6.2 hours, equivalent to $930 in analyst labor at $150 per hour. Audit compliance is 100%, up from a 40% baseline."

### Step 8: Quit Claude

```
/quit
```

## Worked example: the 90-day deployment report

**The prompt you type:**

```
/deployment-report
```

**Folder layout:**

```
practice/
├── governance/
│   ├── audit-log.csv                (data source)
│   └── metrics-framework.md         (baselines and targets)
├── Drafts/
│   └── human_review.md              (escalation data, if any)
├── .claude/
│   └── commands/
│       └── deployment-report.md     (command definition)
└── Outputs/
    └── deployment_report_2026-04-25.md  (output)
```

**What you should see:**

A report with six metric rows:

| Metric | Baseline | Current | Target | Status |
|---|---|---|---|---|
| Docs per analyst per week | 3 | 2.3 | 8 | Below target (early stage) |
| Time to first draft | 120 min | 12 min | 15 min | On target |
| Review gate pass rate | N/A | 75% | 85% | Below target |
| Audit compliance | 40% | 100% | 100% | On target |
| Hours saved per week | 0 | 2.1 | 12 | Below target (early stage) |
| Escalation rate | N/A | 14% | Below 10% | Above target |

And an executive summary: "Three analysts have produced 7 documents in the first 30 days. Estimated time savings of 6.2 hours ($930 at $150 per hour) have been realized. Audit compliance has improved from 40% to 100%. The review gate pass rate and escalation rate need improvement before the 90-day review."

**What Claude did behind the scenes:**

1. Claude read the deployment-report command file.
2. It read `governance/audit-log.csv` and counted entries by analyst.
3. It read `governance/metrics-framework.md` for baselines and targets.
4. It calculated each metric using the formulas defined in the framework.
5. It checked `Drafts/human_review.md` for escalation entries.
6. It wrote the report with the six-metric table and executive summary.
7. It saved to `Outputs/deployment_report_2026-04-25.md`.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| The report shows zero documents because the audit log is empty. | Run the previous lessons to generate audit log entries. Or create test entries by writing files in each analyst workspace. |
| Time savings estimates seem too high. | Check the baseline times. If your team already used templates, the manual time may be 60 minutes instead of 120. Adjust baselines in `governance/metrics-framework.md`. |
| The CPO wants dollar figures, not hours. | Multiply hours saved by the loaded hourly rate for a procurement analyst. At $150 per hour, 6.2 hours equals $930. Include this in the executive summary. |
| The escalation rate is 100% because every output was escalated. | Your quality criteria may be too strict. Review the quality-checker skill and relax criteria that are cosmetic (formatting) versus substantive (missing data). |
| The report does not include all eight analysts. | The practice data only has three analysts. In production, the audit log will have entries from all eight. The report framework scales to any number of analysts. |

## You are done with Lesson 6 when

- You have a metrics framework at `governance/metrics-framework.md` with six metrics, baselines, and targets.
- The `/deployment-report` command produces a report with current values versus targets.
- The report includes an executive summary with analyst count, document count, hours saved, and a dollar figure.
- You can answer the CPO's question "Is this working?" with specific numbers.

This completes Course 12. You have built a team deployment system: shared versus personal configuration, an append-only audit trail, a review gate for stakeholder-ready documents, a one-command onboarding script, workspace isolation governance, and a metrics framework for measuring ROI. The system supports eight analysts across three offices with consistent standards and full auditability.
