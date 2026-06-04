# Lesson 6: Skill versioning - updating without breaking

**Time:** 25 minutes. **You need:** Lesson 5 complete; you have all five skills working.

## A typical Monday two months later

It is 09:00 Monday, two months after the logistics RFP closed. The CFO has tightened the savings methodology: from now on, soft savings (avoided cost) cannot be counted in headline savings without a paragraph of justification. Your existing `savings-calculator` skill does not know about this rule. The next sourcing event uses your skill chain on Tuesday.

You have two choices: live-edit the skill (risky; if you break it, Tuesday's event breaks) or version it properly. This lesson teaches the second choice. Twenty-five minutes from now, your savings-calculator is updated, the rest of your chain still runs unchanged, and you have a record of what changed and why.

## The big idea

A skill is shared infrastructure. When you change it, every future run of every chain that uses it changes too. So you need three small habits:

1. **Comment the version at the top.** "v1.0 - 2026-04-25 - Initial". When you update, bump the version: "v1.1 - 2026-06-30 - Tighten soft-savings rule per CFO request 2026-06-25".
2. **Test the change.** Re-run the affected skill on the practice data. Confirm the output still passes quality criteria.
3. **Tell anyone using the skill chain.** A two-line note in the project's README or in a shared channel. "I updated savings-calculator to v1.1. The change tightens the soft-savings rule. Re-run your sourcing event chain after pulling."

## Set up

**Step 1.** Open your terminal.

**Step 2.** Move to the practice folder:

```
cd "Course_03_The_Skill_Builder/practice"
```

**Step 3.** Open `practice/skills/savings-calculator.md` in your editor.

## Add a version line and update the rule

**Step 4.** At the very top of the file, above the title, add a one-line version comment:

```
<!-- v1.0 2026-04-25 Initial. -->
```

Save. Now the file shows its version on first read.

**Step 5.** Now you will update to v1.1. Find the Process section. Find the step that adds soft savings to the headline. (If your skill does not have one, add the rule below as a new step before the headline step.)

**Step 6.** Add a new step that says:

```
3a. Soft savings (avoided cost, productivity gains, supplier rebate
projections, etc.) MUST NOT appear in the headline savings figure.
Soft savings appear only in a separate "Soft savings, supplemental"
paragraph at the bottom of the savings case. The headline figure
contains hard savings only (negotiated unit rate reductions against
the baseline spend computed from spend-baseline.csv).
```

**Step 7.** Update the version comment at the top:

```
<!-- v1.1 2026-06-30 Tightened soft-savings rule per CFO request 2026-06-25.
     Soft savings now go in a separate supplemental section, not the headline. -->
```

Save.

## Test the update

**Step 8.** Start Claude:

```
claude
```

**Step 9.** Re-run only the affected skill:

```
Use the savings-calculator skill in skills/savings-calculator.md.
Use inputs/spend-baseline.csv and outputs/bid-comparison.md.
Save to outputs/savings-case.md (overwrite the previous run).
```

Press Enter. Wait 60 seconds.

**Step 10.** Open `outputs/savings-case.md`. Confirm two things:

- The headline savings figure does not include any soft savings.
- A separate "Soft savings, supplemental" paragraph appears at the bottom (or a note that no soft savings have been claimed for this event).

**Step 11.** Re-run the award-memo skill since it consumes savings-case.md:

```
Use the award-memo skill in skills/award-memo.md. Inputs are the four
output files plus inputs/category-brief.md and templates/award-memo-template.md.
Save to outputs/award-memo.md (overwrite).
```

**Step 12.** Open `outputs/award-memo.md`. The savings figure quoted should match the new headline (hard savings only). The chain still works.

**Step 13.** Quit Claude (`/quit`).

## Tell the team

**Step 14.** Open `practice/skills/README.md` in your editor. Add a note at the bottom:

```
## Changelog

- savings-calculator v1.1 (2026-06-30): tightened soft-savings rule per
  CFO request 2026-06-25. Soft savings now go in a supplemental section,
  not the headline. Re-run any in-flight sourcing event after this date.
```

Save.

This file is the changelog for your skill library. Anyone running the chain glances at it before starting.

## What just happened, in plain words

You updated one skill. You re-ran only that skill plus the downstream skill that consumed its output. You documented the change. The other three skills (`rfp-builder`, `bid-scorer`, `risk-profiler`) were untouched and still work.

This is the discipline that makes skills shared infrastructure rather than personal scripts. Anyone on your team can run the chain tomorrow with the new soft-savings rule applied automatically. Without versioning, two analysts would diverge: one with the new rule, one with the old.

## Three things that trip beginners up

- **You changed the skill but did not re-run anything.** Then on Tuesday the live event runs the new skill on real data and produces a surprise. Always re-run the practice chain after a change. Five minutes of practice testing prevents Tuesday's surprise.
- **You changed the input shape (added or renamed a column) without warning downstream skills.** This breaks the contract. If you must change input shape, do it in two steps: add the new field, give downstream skills a release to consume it, then deprecate the old field.
- **You did not write a changelog entry.** Six months from now, nobody (including you) will remember why the skill works the way it does. The two-line note in the README is the cheapest documentation insurance you can buy.

## You are done with Lesson 6 when

- `savings-calculator.md` has a version line at the top showing v1.1 and the date.
- The skill has the soft-savings rule explicitly stated.
- You re-ran savings-calculator and award-memo, and the chain still produces a clean award memo.
- You added a changelog entry to `skills/README.md`.

## You are done with Course 3 when

- All five skills are in your `practice/skills/` folder, between 40 and 90 lines each.
- The full chain runs end to end and produces six deliverables in `practice/outputs/`.
- You can copy your `skills/` folder into your real procurement project and run the same chain on your real bid data.

Course 3 done. The next sourcing event you run, you write nothing new. You configure inputs, you run the chain, and you walk into the panel meeting with the deliverables.
