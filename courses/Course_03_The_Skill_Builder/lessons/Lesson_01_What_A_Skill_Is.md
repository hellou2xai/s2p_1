# Lesson 1: What a SKILL.md is and is not

**Time:** 25 minutes.

## A typical Monday morning

It is 09:00 Monday. Your CPO has just approved the logistics consolidation RFP. You open the calendar and block out three weeks for the sourcing event: one week to write the RFP package, two weeks to score bids and write the award memo.

That is the same pattern you ran six weeks ago for indirect services. And six weeks before that for direct materials. Three different sourcing events, the same writing work, three times.

This week you will break the cycle. You will not write the RFP package. You will write the **methodology** that creates the RFP package. The methodology is a SKILL.md file. You write it once. Every future RFP runs the methodology with new inputs.

In this 25-minute lesson, you will see your first SKILL.md, run it against the practice data, and watch Claude produce a real deliverable.

## The big idea

A SKILL.md is a markdown file that captures a methodology, stored in `practice/skills/<name>.md`. When you tell Claude "use the rfp-builder skill on these inputs", Claude reads the skill file and follows the methodology. If you change the inputs, you get a different output. If you change the skill, every future run uses the new methodology.

Two examples to make the difference clear:

| Prompt (one-off) | Skill (reusable) |
|---|---|
| "Write me an RFP for logistics consolidation. Annual spend 11.2m GBP. Award by 2026-06-30." | A skill called `rfp-builder` that says: read the category brief, read the supplier longlist, read the spend baseline, build a six-section RFP package using the methodology below, save to outputs/. |

The first one works once. The second one works for every RFP you ever run.

## Set up

**Step 1.** Open a terminal.

- Windows: press the Windows key, type `Terminal`, press Enter.
- Mac: press Cmd+Space, type `Terminal`, press Enter.

**Step 2.** Move into the practice folder for this course:

```
cd "Course_03_The_Skill_Builder/practice"
```

Press Enter. Your terminal prompt should end in `practice`.

**Step 3.** Look at what is here:

```
ls
```

You should see six items: `CLAUDE.md`, `bid-responses`, `inputs`, `outputs`, `skills`, `templates`.

**Step 4.** Look inside the `skills/` folder:

```
ls skills
```

You should see one file: `README.md`. The folder is empty otherwise. You will fill it across Lessons 3 to 5.

## Try it: see your first skill in action

You will copy a ready-made skill from `solutions/` into your practice folder, then run it. The point is to see what a skill **does** before you write one yourself.

**Step 5.** Copy the reference rfp-builder skill from solutions into your skills folder.

- On Windows in PowerShell:

```
Copy-Item ../solutions/rfp_builder_solution.md skills/rfp-builder.md
```

- On Mac or Linux:

```
cp ../solutions/rfp_builder_solution.md skills/rfp-builder.md
```

Press Enter. The file is copied.

**Step 6.** Confirm it is there:

```
ls skills
```

You should now see two files: `README.md` and `rfp-builder.md`.

**Step 7.** Open `skills/rfp-builder.md` in your editor. Read it. It is around 60 lines. Notice the structure: a "What this skill does" section, an "Inputs" section, a "Process" section, an "Output format" section, and a "Quality criteria" section. We will dissect this in Lesson 2.

**Step 8.** Start Claude Code in the practice folder:

```
claude
```

Press Enter. Wait for the Claude prompt.

**Step 9.** Tell Claude to use the skill. Type:

```
Use the rfp-builder skill in skills/rfp-builder.md.
Inputs are in inputs/ and bid-responses/. Templates in templates/.
Save the output to outputs/ as named in the skill.
```

Press Enter.

**What you should see.** Claude reads the skill file. Then Claude reads `inputs/category-brief.md`, `inputs/supplier-longlist.csv`, and the templates. Within 60 to 90 seconds, Claude saves a populated RFP package draft to `outputs/rfp-package.md` (or one or more named files; the skill decides).

**Step 10.** Open `outputs/rfp-package.md` in your editor. Read the first page. You should see a populated RFP package: an executive overview that names the 11.2m GBP baseline, a scope of work that lists the in-scope lanes, evaluation criteria with the 40/25/20/10/5 weights, and a process timeline that sets the close date as 2026-06-15.

This is not a generic RFP. It is your RFP, populated from your real inputs. Claude did all of it by reading one 60-line skill file.

**Step 11.** Quit Claude:

```
/quit
```

## What just happened, in plain words

1. The `rfp-builder` skill described a methodology in 60 lines: what to read, what to do, what to produce, and what counts as good output.
2. When you told Claude "use the skill", Claude opened the skill file, then opened the inputs the skill named, applied the process, and produced output in the format the skill required.
3. The skill is now sitting in `practice/skills/rfp-builder.md`. The next time you run a sourcing event, you tell Claude "use the rfp-builder skill on these new inputs". You write nothing new.

A SKILL.md is the difference between writing the same RFP three times and writing the methodology once.

## Three things that trip beginners up

- **You confused a skill with a prompt.** A prompt names specific files (`Master/RFP_v3.docx`). A skill names input **shapes** (`a category brief in markdown`, `a supplier longlist in CSV with these columns`). The shape is what makes the skill reusable.
- **You put the skill in the wrong folder.** Skills live in `practice/skills/` (in this course; in your real Claude Code setup they go in `.claude/skills/<name>/SKILL.md`). If Claude says it cannot find the skill, run `ls skills` to confirm the path.
- **You copied the solution wholesale.** Across Lessons 3 to 5 you write your own skills. The solutions are reference answers; the value is in writing them yourself. You copied the rfp-builder skill in this lesson only because Lesson 1 is about seeing a skill in action, not writing one.

## You are done with Lesson 1 when

- You can find the file `practice/skills/rfp-builder.md` and have read its 60 lines.
- You ran the skill and produced `practice/outputs/rfp-package.md`.
- You can answer this question: "What is the difference between a skill and a prompt?" The answer is: a prompt runs once on named files; a skill runs many times on inputs of a named shape.

Take a five-minute break. Move to Lesson 2 next, where you take apart the rfp-builder skill and learn to write your own.
