# /weekly-review

Generate the Monday morning weekly review for the VP of Procurement.

## What this command does

1. Read state/program-state.json for current initiative status.
2. Read state/initiative-tracker.md for detailed notes and next milestones.
3. Read state/decisions-log.md for decisions made since the last review.
4. Read savings-log.csv and compute realized savings by initiative for the trailing 7 days.
5. Produce a one-page review document.

## Output format

Save to outputs/weekly-review-YYYY-MM-DD.md with these sections:

### 1. Headline
One sentence: total realized savings YTD, percentage of target, and number of initiatives on track.

### 2. Initiative status table

| Initiative | Target | Realized YTD | % | Stage | Status |
|---|---|---|---|---|---|

### 3. At risk and behind schedule
For each initiative not on track:
- What went wrong (one sentence).
- What action was taken (one sentence).
- Next milestone and date.

### 4. Decisions since last review
Pull from decisions-log.md. List each decision with the initiative ID and one-line summary.

### 5. Three actions for this week
The three highest-priority actions across all initiatives, ranked by impact.

## After generating

Update state/program-state.json with the current date as the last review date.
Append to state/decisions-log.md if any new decisions were made during the review.
