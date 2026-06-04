<!-- v1.0 2026-04-25 Initial. -->

# Multi-Category Orchestrator Prompt (Reference Solution)

The master prompt that coordinates six category sub-agents and produces a consolidated Monday briefing.

## The slash command file

Save this as `.claude/commands/monday-briefing.md`:

```markdown
# Monday Briefing: All Categories

Read data/program-state.json to get the current status of all six categories.

For each category, launch a sub-agent with this instruction:

"You are a category analyst for [CATEGORY]. Read the following files and produce a category summary:
1. data/category-spend.csv (filter to your category only)
2. data/supplier-scorecards.csv (filter to your category only)
3. data/contract-calendar.csv (filter to your category only)
4. data/initiative-pipeline.csv (filter to your category only)

Your summary must include:
- Total spend for the last 3 months vs. prior 3 months (trend direction and dollar amount)
- Any supplier with an overall scorecard below 3.70 in the most recent quarter (name the supplier and score)
- Any contract expiring within 90 days (name the contract, supplier, and expiration date)
- Status of each active initiative (name, stage, status, and any risk flags)
- One recommended action for this category

Format: use short sentences. Active voice. No em-dashes. Name specific suppliers, dollar figures, and dates."

After all six sub-agents return, validate each summary:
- Does it name at least one supplier? If not, flag it and re-run.
- Does it include at least one dollar figure? If not, flag it and re-run.
- Does it include at least one date? If not, flag it and re-run.
- Maximum 3 re-runs per sub-agent. After 3 failures, include the error in the briefing and note "manual review needed."

Assemble the six summaries into a consolidated briefing with:
1. An executive summary (3 sentences maximum, naming top risk and top action)
2. Six category sections (one per category, in spend order: IT services, logistics, raw materials, facilities, professional services, MRO)
3. A "Top 3 actions this week" section at the end

Save the briefing to outputs/briefings/briefing-2026-04-25.md.
```

## Key points

- The orchestrator reads `program-state.json` first to know which categories exist and their current status.
- Each sub-agent receives scoped instructions: it only reads data for its own category.
- The validation step checks three minimums: a supplier name, a dollar figure, and a date.
- The retry limit (3 attempts) prevents infinite loops. After 3 failures, the orchestrator escalates to the user.
- The final assembly step imposes a consistent structure across all six categories.
- The executive summary is capped at 3 sentences to keep it scannable for the VP.
