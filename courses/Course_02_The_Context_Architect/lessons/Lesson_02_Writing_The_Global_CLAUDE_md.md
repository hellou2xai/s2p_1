# Lesson 2: Writing the global CLAUDE.md

**Time:** 25 minutes. **You need:** Lesson 1 complete.

## A typical Tuesday morning

It is 10:00. The CPO's brief is in your inbox: three category briefs by Friday. You decide to set Claude up properly first. You will write the **global** CLAUDE.md: the one file at the top of your procurement folder that gives Claude background that is true for everything you do, regardless of category.

Twenty-five minutes from now, your global is done and you have tested it.

## The big idea

The global is shared. Everything in it applies to direct materials, logistics, AND indirect. So it can hold:

- Who you are.
- The folder rules that apply everywhere (Master is read-only, save to Drafts, etc.).
- The writing rules that apply to every output.

It must NOT hold:

- Anything specific to one category. No supplier names, no certifications, no approval thresholds. Those go in the category file (Lesson 3).

If a line is true in one category but not the others, it does not belong in the global.

## Set up

**Step 1.** Open your terminal.

**Step 2.** Move to the practice folder:

```
cd "Course_02_The_Context_Architect/practice"
```

**Step 3.** Open `CLAUDE.md` in your text editor.

You should see the original three lines:

```
# My procurement work

I work in procurement.

Help me with sourcing tasks.
```

If you still see your test markers from Lesson 1, delete them first.

**The folder layout you are working in.**

```
practice/
├── CLAUDE.md                   (this is the file you edit in this lesson)
├── direct-materials/
│   ├── CLAUDE.md               (stub, you fill this in Lesson 3)
│   ├── orders.csv
│   └── suppliers.csv
├── logistics/
│   ├── CLAUDE.md               (stub)
│   ├── carriers.csv
│   └── shipments.csv
└── indirect/
    ├── CLAUDE.md               (stub)
    ├── invoices.csv
    └── vendors.csv
```

## Write the new global

**Step 4.** Select all (Ctrl+A on Windows, Cmd+A on Mac). Delete everything.

**Step 5.** Type or paste this template:

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

**Step 6.** Save. The global should now be about 25 lines.

## Test the global

**Step 7.** In your terminal, you should still be in the `practice` folder. Start Claude:

```
claude
```

**Step 8.** Type this prompt and press Enter:

```
You just loaded my new global CLAUDE.md. Tell me back the three sections
in 150 words or fewer. Quote the actual content.
```

**What you should see.** A short reply with three sections. Section 1 names you as a Senior Category Lead at Acme Inc and lists the three categories. Section 2 has the folder rules. Section 3 has the writing rules.

If Claude invents a supplier name like "Great Lakes Steel" or makes up a 1.4m figure, the global has a problem. Quit (`/quit`), open the file, check you did not paste something extra. Try again.

**Step 9.** Try a second prompt to confirm Claude really has the writing rules:

```
Write me a one-paragraph note about a fictional supplier called "Test Co" 
with annual spend of $800,000 and a contract ending 2026-09-30.
```

**What you should see.** A short paragraph that:
- Uses American English (organize, etc.).
- Uses Oxford commas if it lists three or more things.
- Names the figure ($800,000) directly. Does not say "significant" or "material".
- Has no em-dashes.

If Claude writes a long dash anywhere, or says something like "this represents a significant supplier", the writing rules in your global are not loading. Quit, recheck the file, restart.

**Step 10.** Quit Claude (`/quit`).

## Compare against the solution

**Step 11.** Open `solutions/global_CLAUDE_md.md`. Compare it side by side with your file. The solution is one good answer; yours does not need to match exactly. If the solution surfaces a section you missed, copy that idea across.

## What just happened, in plain words

1. Claude Code loaded `practice/CLAUDE.md` at session start. This was the only CLAUDE.md on the path, since you started in `practice/`, not in a category folder.
2. Claude Code parsed three sections: "Who I am" (role, categories, savings target), "Folder rules" (CSV is source of truth, do not modify, save new files here), and "Writing rules" (American English, Oxford commas, no em-dashes, active voice, cap tables at 10 rows).
3. When you asked Claude Code to quote what it loaded (Step 8), Claude Code returned the three sections in order, staying within the 150-word cap.
4. When you asked for a paragraph about Test Co (Step 9), Claude Code applied the writing rules from the global: American English, specific figures ($800,000), Oxford commas, no em-dashes. No supplier names were invented because the global names none.

## Three things that trip beginners up

- **You wrote 200 lines.** The global is small on purpose. 25 to 40 lines. Anything longer means category-specific stuff is leaking in. Move it out.
- **You named a specific supplier.** Specific suppliers belong in the category file. Move them out.
- **You repeated yourself.** If the global says "American English" and you also say "use American English", delete one. Repeats waste tokens on every turn.

## You are done with Lesson 2 when

- The global at `practice/CLAUDE.md` has three sections and is between 25 and 40 lines.
- The global names no specific supplier, certification, or category-specific rule.
- The two test prompts (Step 8 and Step 9) produce sensible replies.
- You have looked at the solution and either kept your version or borrowed an idea or two.

Take a break. Move to Lesson 3 next, where you write the three category files.
