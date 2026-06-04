# Category Brief

Generate a deep-dive brief for a single category.

## Usage
Provide the category name as the argument: `/category-brief IT services`

## What this command does
1. Filter spend data to the specified category.
2. Pull supplier scorecards for all suppliers in the category.
3. Check contract status for contracts in the category.
4. Review initiative progress for the category.
5. Produce a structured brief with spend summary, supplier performance, contract status, and initiative progress.

## Output
Save to outputs/ as `category-brief-<category>-YYYY-MM-DD.md`.
