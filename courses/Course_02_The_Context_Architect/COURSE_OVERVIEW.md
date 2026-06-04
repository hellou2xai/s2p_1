# Course 2: The Context Architect

## A typical Tuesday morning

It is 09:30. Your CPO Slacks: "Need three short briefs by Friday: one on materials, one on logistics, one on indirect. Top suppliers, anything risky, what we should do about it."

You open Claude Code. You type:

> "Help me write a category brief."

Claude writes something. The grammar is right. The shape is right. The content is wrong. The materials brief talks about preferred-vendor compliance (an indirect rule). The logistics brief asks about chip suppliers (those are materials). The indirect brief talks about transit times (those are logistics).

You spend Tuesday afternoon rewriting brief one. By Wednesday morning, you have not started briefs two and three.

## Why this happens

When Claude Code starts, it looks for a file called `CLAUDE.md`. That file is your background briefing for Claude. Right now, the file at the top of your procurement folder says, in full:

```
# My procurement work

I work in procurement.

Help me with sourcing tasks.
```

That is the entire file. It tells Claude nothing about your actual suppliers, your actual rules, or your actual data files. So every output Claude produces is generic.

## The fix

Instead of one big CLAUDE.md trying to cover everything, you write a small stack of files:

- **One global file at the top** of your procurement folder. It says who you are, your folder rules, and your writing rules.
- **One small file in each category folder.** It says what is special about that category: which suppliers, which rules.

When you start Claude in `direct-materials/`, Claude reads:
- the global (universal stuff),
- AND the direct-materials file (suppliers, materials rules).

When you start Claude in `logistics/`, Claude reads:
- the same global,
- AND the logistics file (carriers, transit rules).

Same global. Different folder file. Different correct answer. **You do not change your prompt.** You change which folder you start Claude in. That is the whole idea.

## What you will produce by Friday

Three category briefs, one per category, each saved as a Markdown file inside its own folder:

- `direct-materials/category_brief.md` (top suppliers, the at-risk supplier, an action with an owner and a deadline).
- `logistics/category_brief.md` (top carriers, the at-risk carrier, an action).
- `indirect/category_brief.md` (top vendors, the policy violations found in invoices, an action).

All three come from the same prompt. The folder you start Claude in does the rest.

## The practice data you will work with

Inside `practice/` you have three small folders, each with a master CSV (small, manageable) and an activity CSV (large, realistic). Today's date in the data is **2026-04-25**.

| Folder | Master file | Activity file | Real meaning |
|---|---|---|---|
| direct-materials/ | suppliers.csv (50 suppliers) | orders.csv (2,500 POs across the year) | Steel, aluminum, plastics, chips, castings, machined parts. SUP004 Apex Electronics flagged at_risk. |
| logistics/ | carriers.csv (20 carriers) | shipments.csv (5,000 shipments across the year) | Road, sea, air, parcel. CAR004 ParcelPlus flagged at_risk. |
| indirect/ | vendors.csv (80 vendors) | invoices.csv (3,000 invoices, 18 break the $25,000 approval rule) | Office, software, marketing, legal, audit, MRO, telecoms, fleet, facilities. VEN005 Prism Print flagged at_risk. |

About 10,500 rows of data total. Realistic volume for a year of activity in a small-to-mid-size procurement function.

You will not read every row. Claude will, when you ask. The whole point of the course is that Claude becomes the analyst who reads the data while you direct the work.

## The six lessons

| # | Title | Time |
|---|---|---|
| 1 | How Claude finds your CLAUDE.md files | 20 min |
| 2 | Writing the global CLAUDE.md | 25 min |
| 3 | Writing the three category files | 50 min |
| 4 | Checking the files load correctly | 20 min |
| 5 | Pointing at data files instead of repeating them | 20 min |
| 6 | One prompt, three briefs | 45 min |

Total: about 3 hours. Comfortable in two afternoon sessions.

## You are done with the course when

1. Each of your four CLAUDE.md files (one global plus three category files) is the right size and holds the right kind of content.
2. A short five-question test (Lesson 4) confirms the right files load when you start Claude in different folders.
3. One Claude prompt, run from each of the three category folders, produces three briefs that name only the right entities.
4. You can copy this whole pattern into your real procurement folder at work, drop your real data in, and ship a real brief on Friday.
