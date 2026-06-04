# Lesson 2: Anatomy of a well-written skill

**Time:** 30 minutes. **You need:** Lesson 1 complete.

## A typical Tuesday afternoon

It is 14:00 Tuesday. You sat down to write your first SKILL.md from scratch. You stared at the empty file for ten minutes. You wrote three lines. You deleted them. You opened the rfp-builder skill from yesterday and copied a few sections. You closed your laptop.

The reason this is hard is that you are missing the **shape** of a good SKILL.md. Once you know the five sections every skill needs and what goes in each one, writing one from scratch takes 30 minutes, not three days.

In this lesson you will dissect the rfp-builder skill, name the five sections, and learn the rule for each. By the end you can write any new skill from a blank file.

## The five sections every skill has

Open `practice/skills/rfp-builder.md` again. Read it slowly. Notice the structure:

| # | Section | What goes in it | Example from rfp-builder |
|---|---|---|---|
| 1 | **What this skill does** | One paragraph, plain English. Use case, audience, when to invoke. | "Builds an RFP package for a sourcing event. Use this skill at the start of every event, after the category brief is approved." |
| 2 | **Inputs** | The shape of every input the skill needs. Path, column headers (for CSV), or section structure (for markdown). Not specific files. | "category-brief.md (the sourcing brief, with sections: Today, Current state, Goal, Scope, Stakeholders). supplier-longlist.csv (with columns carrier_id, carrier_name, modes, primary_geography, certifications, capacity_tier, financial_health, otd_pct_12m, contract_terms_offered, incumbent)." |
| 3 | **Process** | A numbered list of steps Claude follows. Plain English. No code. | "1. Read the category brief. Extract today's date, the goal, the scope. 2. Read the longlist. Group by mode. 3. ..." |
| 4 | **Output format** | The shape and location of every file the skill produces. | "Save outputs/rfp-package.md with these six sections in order: Executive overview, Scope of work, Commercial terms, Evaluation criteria, Supplier response template, Process and timeline." |
| 5 | **Quality criteria** | What counts as good output. Used by reviewers (and by the skill itself, when it self-checks). | "Every figure cited has a source named in CLAUDE.md or the inputs. No vague phrases. Every named entity is in the longlist. The total RFP is 4 to 6 pages." |

That is it. Five sections. Every skill in this course follows the same shape.

## Set up

**Step 1.** Open your terminal.

**Step 2.** Move to the practice folder:

```
cd "Course_03_The_Skill_Builder/practice"
```

**Step 3.** Open `skills/rfp-builder.md` in your editor. Keep this file open while you work through the lesson.

## Take it apart, section by section

For each of the five sections, you will read the rfp-builder version and answer one question. The questions train your eye to spot what makes each section work.

**Question 1 (What this skill does).** In the rfp-builder skill's first section, find the sentence that names **when** to invoke the skill. Highlight it.

The answer should be something like "Use at the start of every sourcing event, after the category brief is approved." This sentence stops the skill being run at the wrong moment. Without it, a learner could run rfp-builder during bid scoring and get a confusing rebuild.

**Question 2 (Inputs).** Find the inputs section. Count how many inputs the skill names. There should be three: `inputs/category-brief.md`, `inputs/supplier-longlist.csv`, and `templates/rfp-template.md`.

Now look at the column list for `supplier-longlist.csv`. The columns are listed by name and order. Why? Because a skill that says "read the longlist" without naming columns will work today, then break next month when the data team renames a column. Naming the columns makes the skill a contract with the data, not a gamble.

**Question 3 (Process).** Find the process section. Count the numbered steps. There should be six to nine. Each step is one sentence. None of them mention specific suppliers, specific GBP figures, or specific dates from the practice scenario.

A skill cannot say "compute the savings against the 11.2m GBP baseline". That number is specific to this RFP. The skill says "compute the savings against the baseline figure named in the category brief". The skill points; the brief provides.

**Question 4 (Output format).** Find the output format section. Count the named output files. There should be one (or two). Each one has a path and a structure (sections, columns, length cap).

If the output section just says "save the result", the skill is broken. Two runs will save to different places. Reviewers will not know where to look.

**Question 5 (Quality criteria).** Find the quality criteria section. Count the criteria. There should be three to five. Each one is a check the skill (or you) can run on the output.

Examples of good criteria: "Every figure has a source." "Every supplier named is in the longlist." "Total length is 4 to 6 pages."

Bad criteria: "The output is high quality." "It looks professional." These are not checkable.

## Try it: write a tiny skill from scratch

You will write a one-section skill (the smallest skill possible) and run it.

**Step 4.** Create a new file at `practice/skills/list-incumbents.md`.

**Step 5.** Paste this content:

```
# list-incumbents

## What this skill does

Lists every incumbent carrier in the supplier longlist with their current
contract terms. Use this when starting any review where you want to see
who you are already working with before considering challengers.

## Inputs

inputs/supplier-longlist.csv
- columns: carrier_id, carrier_name, modes, primary_geography, certifications,
  capacity_tier, financial_health, otd_pct_12m, contract_terms_offered, incumbent

## Process

1. Read inputs/supplier-longlist.csv.
2. Filter rows where incumbent = "yes".
3. Sort the result by carrier_id.
4. Output the result as a markdown table.

## Output format

Print to the chat (do not save a file). Table columns:
carrier_id, carrier_name, modes, otd_pct_12m, contract_terms_offered.

## Quality criteria

- Every row has a non-empty carrier_id from the longlist.
- The table has at most 14 rows (current incumbents).
- No carrier from outside the longlist appears.
```

Save the file.

**Step 6.** Start Claude in the practice folder:

```
claude
```

**Step 7.** Type:

```
Use the list-incumbents skill in skills/list-incumbents.md.
```

Press Enter.

**What you should see.** Claude reads the skill, opens `inputs/supplier-longlist.csv`, filters for `incumbent = yes`, sorts, and prints a markdown table to the chat. The table has around 9 rows (the current incumbents in the practice data). Each row has the five columns the skill named.

You just wrote and ran your first SKILL.md. Twelve lines.

**Step 8.** Quit Claude (`/quit`).

## What just happened, in plain words

1. You took 12 lines of structured markdown and used it as a methodology.
2. The skill named the input shape, the process, the output, and the quality criteria.
3. Claude did the work. The work was repeatable: every time you run the skill, you get the same shape of output.
4. If next month a new incumbent is added to the longlist, the skill picks them up automatically. You do not edit the skill.

This is the entire point. A skill is a contract: "given input of this shape, produce output of this shape." The contract is reusable.

## Three things that trip beginners up

- **You wrote a prompt and called it a skill.** A prompt would say "list the carriers in suppliers.csv". A skill names the input shape and the output shape so it works on any future longlist with the same columns.
- **You skipped the quality criteria.** Without them, you have no way to tell if the skill ran correctly. Every skill in this course must end with three to five checkable criteria.
- **You named specific suppliers in the skill.** The skill should never say "Forge Steel UK" or "11.2m GBP". Those are inputs, not methodology. If they appear in the skill, the skill becomes a one-off prompt.

## You are done with Lesson 2 when

- You can name the five sections of any SKILL.md without looking.
- You wrote the `list-incumbents` skill and ran it successfully.
- You understand the rule: a skill names input shapes and output shapes; specific values come from the inputs.

Take a break. Move to Lesson 3 next, where you write your first real skill from scratch (rfp-builder), without copying.
