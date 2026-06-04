# Lesson 4: Retry Limits and Human Escalation: When to Stop and Ask for Help

**Time:** 45 minutes.

## It is 08:40 on Monday. The validation loop is running. One sub-agent keeps failing.

You built the feedback loop in Lesson 3. It catches errors and fixes them. Most of the time, it works on the first or second pass. But this morning the scorecard sub-agent for the Raw materials category has now failed validation three times. The first pass produced "unknown" trend values. The second pass tried to fix them but set every trend to "flat" even for suppliers with clear upward scores. The third pass produced a file with one fewer row than the source data.

The system is in a loop. Each fix attempt introduces a different problem. The loop has no exit condition. Left alone, it will keep retrying indefinitely, burning time and tokens.

This lesson adds a stop condition. After a set number of retries, the system stops trying to fix the problem on its own. Instead, it escalates to you with a clear description of what went wrong, what was tried, and what you need to do to resolve it.

## What Claude Code is going to do for you

Claude Code will track the number of fix attempts for each output file. If a file fails validation after three attempts, Claude Code will stop the retry loop, write an escalation note to `Drafts/escalations.md`, and wait for you to resolve the issue manually. The escalation note will name the file, the rule that failed, the attempts made, and the specific question you need to answer or action you need to take. You get a clean stop instead of an infinite loop.

This capability applies to Claude Code in the terminal. It does not apply to Claude AI Web or Claude Desktop with Cowork.

## Set up

1. Confirm Lesson 3 is complete and all five Drafts/ files pass validation:

```
ls "Course_11_The_Category_Management_System/practice/Drafts/"
```

You should see the five files from Lesson 3 plus any corrections applied.

2. Navigate to the practice folder and start Claude Code:

```
cd "Course_11_The_Category_Management_System/practice"
claude
```

3. Restate the read-only rule:

```
The files in data/ are source data. Do not edit any file in data/.
Save all output to Drafts/. Write escalation notes to Drafts/escalations.md.
```

**Folder layout:**

```
practice/
├── CLAUDE.md
├── data/                     (read-only)
├── Drafts/
│   ├── orchestrator_plan.md
│   ├── savings_tracker.md
│   ├── contract_review.md
│   ├── scorecard_refresh.md
│   └── ps_update.md
└── Outputs/
```

## Step-by-step

### Step 1: Define the retry policy

Tell Claude Code the retry limit and the escalation behavior before running anything.

```
I am setting a retry policy for all validation and fix operations in this session.

Policy:
- Maximum fix attempts per file: 3.
- After 3 failed fix attempts, stop retrying.
- Write an escalation entry to Drafts/escalations.md.
- The escalation entry must include: the file name, the rule number that failed, the number of attempts made, a one-sentence description of what each attempt did, and a one-sentence question for me to resolve.
- After writing the escalation, do not attempt further fixes on that file until I give explicit instructions.

Confirm you have this policy.
```

You should see Claude Code confirm the policy, listing all four requirements. If it omits one, repeat just that requirement.

### Step 2: Introduce a deliberate validation failure

To practice the retry and escalation flow, you need a file that fails repeatedly. This step introduces a problem on purpose so you can watch the policy trigger.

```
Edit Drafts/scorecard_refresh.md. In the trend column, replace every value with "unknown".
Do not change any other column. Save the file.
```

You should see Claude Code confirm the edit. The trend column now has all "unknown" values, which violates Rule 3 from Lesson 3.

### Step 3: Trigger the retry loop with a bad fix rule

Now run validation and a deliberately incomplete fix rule. This simulates the sub-agent that cannot resolve the problem on its own.

```
Validate Drafts/scorecard_refresh.md. Rule 3: no trend value may be "unknown".
If you find violations, apply this fix: set all "unknown" trend values to "unknown_v2".
Re-validate. If it still fails, apply the fix again with a different label: "unknown_v3".
Track how many attempts you have made. Apply the retry policy after 3 attempts.
```

You should see Claude Code attempt the fix three times. Each time, the file still fails Rule 3 because "unknown_v2" and "unknown_v3" are still not valid trend values. After the third attempt, Claude Code should stop and write the escalation.

If Claude Code simply keeps retrying without stopping, it has not applied the retry policy. Interrupt it with Ctrl+C, then re-read Step 1 and restate the policy explicitly before continuing.

### Step 4: Read the escalation note

```
Read Drafts/escalations.md.
```

You should see an entry like this:

```
Escalation: scorecard_refresh.md
Rule violated: Rule 3 (trend values must be up, down, flat, or "insufficient data")
Attempts: 3
Attempt 1: Replaced "unknown" with "unknown_v2". File still failed Rule 3.
Attempt 2: Replaced "unknown_v2" with "unknown_v3". File still failed Rule 3.
Attempt 3: Replaced "unknown_v3" with "unknown_v4". File still failed Rule 3.
Question for you: What are the valid trend values, and how should I calculate them from the source data?
```

If the escalation note is missing any of the four required fields (file name, rule number, attempt descriptions, question), ask Claude Code: "Update the escalation entry to include all four fields from the retry policy."

### Step 5: Resolve the escalation manually

Now you act as the human escalation point and give Claude Code the information it needs.

```
I am resolving the escalation for scorecard_refresh.md.
The valid trend values are: up, down, flat, insufficient data.
To calculate trend:
1. Read data/supplier-scorecards.csv.
2. For each supplier in scorecard_refresh.md, find all rows in the scorecard CSV.
3. Calculate the average of quality, delivery, cost, responsiveness for the most recent quarter and for the previous quarter.
4. If the most recent average is more than 0.1 higher: set trend to "up".
5. If the most recent average is more than 0.1 lower: set trend to "down".
6. If the difference is 0.1 or less: set trend to "flat".
7. If only one quarter of data exists: set trend to "insufficient data".
Apply this calculation now. Fix scorecard_refresh.md. Do not count this as a retry attempt.
```

You should see Claude Code read the scorecard CSV, compute the trend values, and rewrite the file. The trend column should now contain only "up," "down," "flat," or "insufficient data."

### Step 6: Re-validate after the manual resolution

```
Validate Drafts/scorecard_refresh.md against Rule 3.
If it passes, update the escalation entry in Drafts/escalations.md to add: "Resolved: [today's date]. Fix applied: trend calculated from supplier-scorecards.csv using quarterly averages."
```

You should see "PASS: scorecard_refresh.md" and a confirmation that the escalation note has been updated.

### Step 7: Test the escalation with a missing-data scenario

This step practices the second type of escalation: a sub-agent cannot find the data it needs.

```
Run a sub-agent with this task:
"Read data/category-spend.csv. Find all transactions for the category 'Aerospace components'.
Calculate total spend for that category in Q1 2026. Write to Drafts/aerospace_spend.md."
Apply the retry policy. If the category does not exist in the data, escalate immediately (no retries needed for a missing category). Write the escalation to Drafts/escalations.md.
```

You should see Claude Code search the CSV, find no "Aerospace components" category, and immediately escalate. The escalation entry should say: "Category 'Aerospace components' does not exist in data/category-spend.csv. No retry attempted. Action required: confirm the correct category name."

### Step 8: Read the full escalations file

```
Read Drafts/escalations.md. How many escalation entries are present? List the file name and resolution status for each.
```

You should see two entries: the `scorecard_refresh.md` entry (resolved) and the `aerospace_spend.md` entry (open).

### Step 9: Quit Claude Code

```
/quit
```

## Worked example: the three-attempt retry and escalation

**The prompt you type:**

```
Retry policy: maximum 3 fix attempts per file. After 3 failures, write escalation to Drafts/escalations.md.
Validate Drafts/contract_review.md. Rule 1: no supplier cell may be empty.
If violations found, attempt up to 3 fixes. Escalate if not resolved after 3 attempts.
```

**Folder layout:**

```
practice/
├── data/
│   └── contract-calendar.csv   (input for lookups during fix attempts)
└── Drafts/
    ├── contract_review.md       (validated and fixed in place)
    └── escalations.md           (escalation log, appended if needed)
```

**What you should see:**

If `contract_review.md` passes on the first fix attempt, Claude Code reports "PASS: contract_review.md after 1 fix attempt." No escalation is written.

If the file cannot be fixed in three attempts, Claude Code writes to `Drafts/escalations.md`:

```
Escalation: contract_review.md
Rule violated: Rule 1 (supplier name must not be empty or "N/A")
Attempts: 3
Attempt 1: Searched contract-calendar.csv for CTR-007 supplier. Found "Horizon Distribution". Applied. File still failed (second empty row found).
Attempt 2: Fixed second empty row for CTR-009. Applied. File still failed (third empty row found).
Attempt 3: Fixed CTR-013 row. Applied. File still failed (fourth empty row found).
Question for you: There appear to be more than 3 empty supplier rows. Should I continue fixing, or is the source data in contract-calendar.csv incomplete?
```

**What Claude Code did behind the scenes:**

1. Claude Code ran the validator against `Drafts/contract_review.md` and found one or more Rule 1 violations.
2. On each attempt, it looked up the supplier name in `data/contract-calendar.csv` using the contract ID.
3. It applied the correction, saved the file, and re-ran the validator.
4. After the third failed attempt, it stopped, wrote the escalation entry to `Drafts/escalations.md`, and waited for instructions.
5. It did not attempt a fourth fix, following the retry policy set in the session.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Claude Code ignores the retry policy and keeps trying beyond 3 attempts. | Restate the policy as the first message in a new session: "Retry limit is 3. After 3 failed fixes, write escalation to Drafts/escalations.md and stop." Session context resets when you quit and restart. |
| The escalation note is missing the question for you to resolve. | Ask Claude Code: "Update the escalation entry for [filename] to add a specific question I need to answer before you can resolve it." |
| Claude Code escalates on the first attempt instead of retrying. | Check whether the task itself said "escalate immediately." Only missing data scenarios should escalate on the first attempt. Validation failures should retry up to 3 times. |
| After a manual resolution, Claude Code tries to count the manual fix as one of the 3 retry attempts. | Clarify: "Manual resolutions following a human escalation do not count toward the retry limit. The retry counter resets to 0 when I provide a resolution instruction." |
| Two different files share one escalation entry and the descriptions are mixed. | Ask Claude Code: "Rewrite Drafts/escalations.md. Each escalation entry must start with 'Escalation: [filename]' on its own line. Do not merge entries." |

## You are done with Lesson 4 when

- You have set a retry policy and confirmed Claude Code accepted it.
- You have triggered a three-attempt retry and seen Claude Code escalate automatically.
- `Drafts/escalations.md` has at least two entries: one resolved and one open.
- You have resolved one escalation manually and confirmed the file passes validation.

Move to Lesson 5 when ready.
