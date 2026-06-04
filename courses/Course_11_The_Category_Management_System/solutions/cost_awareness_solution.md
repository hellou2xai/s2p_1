<!-- v1.0 2026-04-25 Initial. -->

# Performance and Cost Awareness (Reference Solution)

A pattern for tracking token usage and setting budgets on multi-agent workflows in Claude Code.

## Why cost awareness matters

Every sub-agent call in Claude Code uses tokens. A Monday briefing that dispatches six sub-agents, each reading four data files, uses roughly 50,000 to 80,000 input tokens and 3,000 to 6,000 output tokens per run. If the feedback loop triggers retries, the cost increases.

Without tracking, a Monday briefing that runs smoothly costs about $0.50 to $1.00 in API usage. A briefing with multiple retries and re-reads can cost $2.00 to $4.00. Over a year of weekly briefings, that is $26 to $208.

## The cost tracking pattern

Add this to the end of your orchestrator prompt:

```
After completing the briefing, add a "Cost estimate" section at the bottom
with these fields:

## Cost estimate

- Sub-agents dispatched: [count]
- Sub-agents that required retries: [count]
- Total retries: [count]
- Estimated input tokens: [count] (rough estimate based on file sizes read)
- Estimated output tokens: [count] (rough estimate based on output length)
- Estimated cost: $[amount] (at $3.00 per 1M input tokens, $15.00 per 1M
  output tokens)

If estimated cost exceeds $2.00 for a single briefing run, add a warning:
"Cost above $2.00 threshold. Consider reducing data file sizes or scoping
sub-agent reads to smaller date ranges."
```

## How to reduce costs

Three techniques, ordered by impact:

1. **Scope the date range.** Instead of reading all 1,500 rows of category-spend.csv, instruct sub-agents to read only the last 6 months. This cuts input tokens by roughly 50%.

2. **Cache stable data.** Supplier scorecards and contract calendars change quarterly, not weekly. Read them once, save a summary to state/, and have sub-agents read the summary instead of the raw file. This saves re-reading 120 scorecard rows and 25 contract rows every Monday.

3. **Skip healthy categories.** If program-state.json shows a category as "on_track" with no risk flags, no expiring contracts, and no at-risk initiatives, skip the sub-agent entirely. Include a one-line note: "MRO: On track. No flags. Skipped detailed scan." This can cut the run from six sub-agents to three or four.

## Budget guardrails

Add this to CLAUDE.md to set a hard limit:

```
## Cost guardrails

- Maximum sub-agent dispatches per session: 10
- Maximum retries per sub-agent: 3
- If total retries across all sub-agents exceed 6, stop and ask for human review
- Weekly briefing cost target: under $1.50
```

These guardrails prevent runaway costs from feedback loops that keep retrying without converging.
