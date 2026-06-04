# Solution: a strong global CLAUDE.md

This is one good answer for Lesson 2. Compare it to your own global only after you have made your own attempt. Adopt anything from below that improves your file. Do not copy wholesale.

## The reference content

Save this at `practice/CLAUDE.md`. About 25 lines, three sections.

```
# Procurement portfolio - global instructions

## Who I am

I am a Senior Category Lead at Acme Inc.
I look after three category folders inside this practice portfolio:
direct materials (steel, aluminum, plastics, electronics, castings),
logistics (the carriers that move our goods),
and indirect (office, software, marketing, legal, audit, MRO, telecoms).

This year I am running a $5.4m cost reduction program across the portfolio.

## Folder rules

The CSV files in any folder are the source of truth. Read them when I ask
data questions. Do not modify any CSV unless I tell you to.
Save any new files (briefs, summaries, scorecards) into the folder I
am working in, named with a clear file name like category_brief.md.
Each category folder has its own CLAUDE.md with category-specific rules.
When I start Claude in a category folder, follow that file's rules
on top of these.

## Writing rules

Use American English. Use organize, summarize, behavior, color.
Use Oxford commas. No em-dashes. Active voice.
Specific numbers, never "significant" or "material" for figures.
Cap tables at 10 rows. Cap recommendations at 3.
Every brief that goes to a CFO or board ends with an audit footer
listing the source files used, the date, and the model used.
```

## Why this works

- About 25 lines, well under the 40-line ceiling.
- Holds only what is universal across all three categories.
- Names no specific supplier, carrier, vendor, or stakeholder.
- Names no certification specific to one category.
- Names no specific data file path inside a category folder.
- The writing rules and folder rules apply equally to a direct-materials brief, a logistics scorecard, and an indirect savings memo.

## What is deliberately NOT in here

- Supplier names. There are 50 in direct materials, 20 carriers, 80 vendors. Three different lists. They live in their respective category files (or, more precisely, in the CSV the category file points at).
- IATF, ISO, or any other certification. Each applies only to one category.
- The $25,000 approval threshold. Indirect only.
- Specific contract end dates.
- The list of stakeholders.
