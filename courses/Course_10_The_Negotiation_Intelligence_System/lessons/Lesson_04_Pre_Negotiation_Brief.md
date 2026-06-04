# Lesson 4: Pre-Negotiation Brief with a PreToolUse Block

**Course:** The Negotiation Intelligence System
**Time:** 50 minutes

---

## Opening scenario

It is 14:30 on Tuesday. Your VP forwards a pre-negotiation brief from last quarter. The brief went to the CPO before a supplier meeting. The CPO read it, called your colleague, and said: "There is no BATNA in here. What do we do if the supplier walks? What is our walk-away price?" The brief had to be rewritten overnight. The supplier meeting was rescheduled. It cost two days.

The fix is not a checklist reminder. It is a gate. In this lesson, you build a PreToolUse hook that fires before Claude Code writes the pre-negotiation brief. If the brief content is missing a BATNA section or a walk-away price, the hook blocks the write entirely. The file cannot land on disk until both fields are present. Your VP will never receive an incomplete brief from this system again.

---

## What Claude Code is going to do for you

You will create a Python script that acts as a PreToolUse hook. Every time Claude Code tries to write `Outputs/pre-negotiation-brief.md`, the hook intercepts the content before it hits disk. It checks for two required fields: a BATNA section and a walk-away price (a dollar figure within 300 characters of the words "walk-away" or "walk away"). If either is missing, the hook prints exactly what is missing and exits with code 1. Claude Code sees the exit code, does not write the file, and reports the problem back to you. When both fields are present, the hook exits with code 0, the write proceeds, and the brief is saved.

---

## Set up

1. Confirm you completed Lesson 3. Check for both Lesson 2 and Lesson 3 outputs:

```
ls Outputs/
```

You should see `intelligence-brief.md` and `deviation-costs.md`.

2. Navigate to the practice folder if you are not already there:

```
cd "Course_10_The_Negotiation_Intelligence_System/practice"
```

3. Start Claude Code:

```
claude
```

4. Restate the read-only rule:

```
The folder data/ holds the source files. Do not edit any file in data/. Save all output to Outputs/.
```

**Folder layout at the start of this lesson:**

```
practice/
├── CLAUDE.md
├── .claude/
│   └── settings.json          (PostToolUse hook from Lesson 3 is registered here)
├── data/
├── scripts/
│   └── check-deviation-costs.py
└── Outputs/
    ├── system-design.md
    ├── intelligence-brief.md
    └── deviation-costs.md
```

---

## Step-by-step

### Step 1: Draft a brief without the required fields, to see what gets through

Ask Claude Code to write an initial brief that is missing the two required fields.

```
Read Outputs/intelligence-brief.md and Outputs/deviation-costs.md. Write a pre-negotiation brief to Outputs/pre-negotiation-brief.md. Include these sections: Objective, Supplier Background, Performance Summary, Market Position, Deviation Cost Summary, and Recommended Strategy. Do not include a BATNA or a walk-away price yet.
```

You should see Claude Code write the file. It will succeed, because the hook does not exist yet. Open `Outputs/pre-negotiation-brief.md` and confirm that BATNA and walk-away are both absent. This is what the hook will prevent going forward.

### Step 2: Write the PreToolUse hook script

Ask Claude Code to create the hook.

```
Create a Python script at scripts/check-brief-completeness.py. The script must do the following:
1. Read content from stdin. This content is the text Claude Code is about to write to a file.
2. Check whether the text contains "BATNA" or "Best Alternative to a Negotiated Agreement" (case-insensitive).
3. Check whether the text contains "walk-away" or "walk away" (case-insensitive) within 300 characters of a dollar sign.
4. If the BATNA check fails, add "BATNA section" to the list of missing items.
5. If the walk-away dollar figure check fails, add "walk-away price with a dollar figure" to the list of missing items.
6. If any items are missing, print: "BLOCKED: Pre-negotiation brief is missing: [list the missing items]. Add these before saving." Then exit with code 1.
7. If both checks pass, print "Brief completeness check passed." and exit with code 0.
Use only Python standard library modules.
```

You should see Claude Code create `scripts/check-brief-completeness.py`. The script reads from `sys.stdin` and uses `re.search` for pattern matching.

### Step 3: Register the PreToolUse hook in settings.json

Exit Claude Code:

```
/quit
```

Open `.claude/settings.json` in your text editor. You already have a `PostToolUse` entry from Lesson 3. Add a `PreToolUse` block alongside it. The full file should look like this:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "command": "python scripts/check-brief-completeness.py"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "python scripts/check-deviation-costs.py"
      }
    ]
  }
}
```

Save the file. Confirm the JSON is valid before continuing.

If you see a JSON parse error when you restart Claude Code, the file has a formatting problem. Check for missing commas, mismatched brackets, or trailing commas after the last item in an array.

### Step 4: Test the block

Start Claude Code again:

```
claude
```

Ask Claude to write a brief that is deliberately missing both required fields:

```
Write a pre-negotiation brief to Outputs/pre-negotiation-brief.md. Include Objective, Supplier Background, Performance Summary, Market Position, and Recommended Strategy. Do not include a BATNA section or a walk-away price.
```

You should see the PreToolUse hook fire. The terminal will print: "BLOCKED: Pre-negotiation brief is missing: BATNA section, walk-away price with a dollar figure. Add these before saving." The file will not be written. Confirm by checking that `Outputs/pre-negotiation-brief.md` either does not exist or still contains the old version from Step 1.

If the hook does not fire, check that `settings.json` is in `.claude/` inside the `practice/` folder and that you restarted Claude Code after editing the file.

### Step 5: Write the complete brief

Now write the brief with all required fields.

```
Write a complete pre-negotiation brief for the CTR-2024-LG-001 renewal with Redline Logistics LLC. Save it to Outputs/pre-negotiation-brief.md. Include these sections:
1. Objective: state what TransGlobal wants to achieve in this negotiation.
2. Supplier Background: summarize Redline's role and the contract history.
3. Performance Summary: use the findings from Outputs/intelligence-brief.md (OTD decline from 96.8% to 93.1%).
4. Market Position: use the market rate comparison from Outputs/intelligence-brief.md.
5. Deviation Cost Summary: use the figures from Outputs/deviation-costs.md (total $1,378,000).
6. BATNA: TransGlobal can rebid the logistics corridor to three qualified carriers. Estimated rebid timeline: 90 days. Estimated transition cost: $280,000.
7. Walk-Away Price: TransGlobal will not agree to a total annual cost above $9.75M. Any proposal above $9.75M triggers the rebid process.
8. Recommended Strategy: three recommendations, no more.
The brief must name Redline Logistics LLC, state the $9.2M current annual value, and include the 2026-05-07 negotiation deadline.
```

You should see the PreToolUse hook fire, confirm both required fields are present, and print "Brief completeness check passed." Claude Code then writes the file.

If the hook still blocks the write, ask Claude: "Read the brief content you are about to save. Does it contain the word BATNA? Does it contain a dollar figure within three sentences of the phrase walk-away? If not, add both."

### Step 6: Verify the saved brief

```
Read Outputs/pre-negotiation-brief.md. Confirm it has a BATNA section, a walk-away price of $9.75M, the supplier name, the $9.2M current value, and the 2026-05-07 deadline. List any item that is missing.
```

You should see Claude Code confirm all five elements are present.

### Step 7: Check that the brief has three recommendations or fewer

```
Read the Recommended Strategy section of Outputs/pre-negotiation-brief.md. How many recommendations are listed? If there are more than three, remove the lowest-priority ones until three remain.
```

You should see Claude Code count the recommendations and confirm there are three or fewer.

### Step 8: Exit Claude Code

```
/quit
```

---

## Worked example, end to end

**Starting files:**

- `Outputs/intelligence-brief.md`: OTD decline from 96.8% to 93.1%, Redline pricing 8% above market median.
- `Outputs/deviation-costs.md`: Three-row deviation table with total annual cost impact of $1,378,000.

**The prompts you type, in order:**

```
Create scripts/check-brief-completeness.py. Check stdin for a BATNA section and a walk-away price with a dollar figure. Block the write and print what is missing if either is absent. Use only standard library modules.
```

After registering in `settings.json` and restarting:

```
Write a complete pre-negotiation brief to Outputs/pre-negotiation-brief.md. Include BATNA (rebid to three carriers, 90-day timeline, $280,000 transition cost) and walk-away price ($9.75M). Name Redline Logistics LLC, $9.2M current value, 2026-05-07 deadline.
```

**Extract from the output (BATNA and walk-away sections):**

```
## BATNA

TransGlobal can rebid the logistics corridor to three qualified carriers: Apex Freight
Solutions, Summit Transport LLC, and Central Distribution Partners. The estimated rebid
timeline is 90 days. Estimated transition cost: $280,000. This alternative is credible
and has been communicated internally to the VP of Procurement.

## Walk-Away Price

TransGlobal will not agree to a total annual contract value above $9.75M. Any proposal
above $9.75M triggers the rebid process. The negotiating team is authorized to agree
to any value at or below $9.75M without further VP approval.
```

**Finished artifact:** `Outputs/pre-negotiation-brief.md`, a complete eight-section brief that passed the PreToolUse completeness check, and `scripts/check-brief-completeness.py`, the hook that enforces completeness on every future brief.

**What Claude Code did behind the scenes:**

1. Claude Code drafted the brief content, including all eight sections.
2. Before writing the file, the PreToolUse hook received the full text via stdin.
3. The hook searched for "BATNA" using a case-insensitive regex. It found the heading `## BATNA`.
4. The hook searched for "walk-away" within 300 characters of a dollar sign. It found "$9.75M" in the Walk-Away Price section.
5. Both checks passed. The hook printed "Brief completeness check passed." and exited with code 0.
6. Claude Code wrote the file to `Outputs/pre-negotiation-brief.md`.
7. The PostToolUse hook from Lesson 3 also fired. Since the file is not a deviation costs table, the deviation check script found no matching table rows and exited cleanly.

---

## Common mistakes and how to recover

**Symptom:** The PreToolUse hook blocks every file write, including files that are not the brief.
**Fix:** Add a filename check at the top of the hook script. Read the filename from the `CLAUDE_TOOL_INPUT` environment variable (Claude Code sets this). If the filename does not contain "brief," exit with code 0 immediately.

**Symptom:** Claude includes the word "BATNA" in a sentence but not as a section heading. The hook passes but the VP asks where the BATNA section is.
**Fix:** Tighten the hook check. Instead of searching for the word "BATNA" anywhere, search for a markdown heading: `## BATNA` or `## Best Alternative`. Update the regex in `scripts/check-brief-completeness.py` to require a heading, not just a mention.

**Symptom:** The walk-away check fails even though the brief has a walk-away price.
**Fix:** The dollar figure may be formatted as "9.75 million" instead of "$9.75M." Update the prompt: "Express the walk-away price as a dollar figure with a dollar sign, for example $9.75M."

**Symptom:** The PreToolUse and PostToolUse hooks conflict, both printing errors at the same time.
**Fix:** They do not conflict. PreToolUse runs before the write. PostToolUse runs after. If you see both errors, the PreToolUse error means the file was not written. The PostToolUse error is from a previous file version. Fix the PreToolUse issue first.

**Symptom:** The brief has five recommendations instead of three.
**Fix:** Add this sentence to your prompt: "List no more than three recommendations. If you have more, combine or drop the lowest-priority ones."

---

## You are done with Lesson 4 when

- `Outputs/pre-negotiation-brief.md` exists with all eight sections, including BATNA and walk-away price.
- `scripts/check-brief-completeness.py` exists and correctly blocks writes when either required field is missing.
- The hook is registered in `.claude/settings.json` under `PreToolUse`.
- You tested the block and confirmed the file was not written when the fields were absent.
- The brief names Redline Logistics LLC, states the $9.2M current value, and includes the 2026-05-07 deadline.
- The Recommended Strategy section has three recommendations or fewer.

Move to Lesson 5 when ready.
