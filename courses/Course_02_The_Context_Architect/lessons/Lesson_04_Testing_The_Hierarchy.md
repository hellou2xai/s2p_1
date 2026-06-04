# Lesson 4: Checking the files load correctly

**Time:** 20 minutes. **You need:** Lessons 2 and 3 complete.

## A typical Wednesday morning

It is 09:00. You have four CLAUDE.md files written: one global plus three category files. Before you trust them in a real brief that goes to your CPO, you want a quick five-minute check that confirms the right files load when you start Claude in different folders.

This lesson gives you that check. You run a small five-question test from each of the three folders. You can re-run it any time you change a CLAUDE.md.

## The big idea

A test is just a prompt. The prompt asks Claude to tell you what background it has loaded. If the answers are right, the hierarchy is right.

**Question 1 should give the same answer** in all three folders. It comes from the global.

**Questions 2 to 5 should give different answers** per folder. They come from each folder's own CLAUDE.md.

## Save the test for re-use

**Step 1.** Open your terminal.

**Step 2.** Move to the practice folder:

```
cd "Course_02_The_Context_Architect/practice"
```

**Step 3.** In your text editor, create a new file in this folder called `test.md`. Paste this:

```
# Five-question hierarchy test

Run this prompt from each of the three category folders. Question 1
should give the same answer everywhere. Questions 2 to 5 should give
different answers per folder.

Prompt to type into Claude:

Answer these five questions using only the CLAUDE.md context loaded in
this session. Do not read any data file.

1. What is my role at the portfolio level?
2. What is the scope of this folder?
3. What data files live in this folder?
4. What at-risk entity is in this category?
5. What rules apply only in this category?

Cap your reply at 200 words.
```

Save the file.

**The folder layout for this test.**

```
practice/
├── CLAUDE.md                   (global, from Lesson 2)
├── test.md                     (the test you just saved)
├── direct-materials/
│   ├── CLAUDE.md               (category file, from Lesson 3)
│   ├── orders.csv
│   └── suppliers.csv
├── logistics/
│   ├── CLAUDE.md               (category file, from Lesson 3)
│   ├── carriers.csv
│   └── shipments.csv
└── indirect/
    ├── CLAUDE.md               (category file, from Lesson 3)
    ├── invoices.csv
    └── vendors.csv
```

## Run the test in each folder

**Step 4.** Move into the direct-materials folder:

```
cd direct-materials
```

**Step 5.** Start Claude:

```
claude
```

**Step 6.** Open `practice/test.md` in your editor. Copy the prompt body (the text from "Answer these five questions" through "Cap your reply at 200 words"). Paste into Claude. Press Enter.

**What you should see for direct-materials.** A five-section reply:

1. (Same as the other two folders.) Senior Category Lead at Acme Inc, looking after direct materials, logistics, and indirect, running a $5.4m cost reduction program this year.
2. Direct materials. Steel, aluminum, plastics, electronics chips, castings.
3. suppliers.csv (50 rows: supplier_id, supplier_name, state, makes, annual_value_usd, contract_end, status). orders.csv (~2,500 rows: po_number, supplier_id, item, units, total_usd, po_date).
4. SUP004 Apex Electronics. Contract ends 2026-05-31.
5. The sourcing decision must be made before SUP004's contract end.

**Step 7.** Quit Claude (`/quit`). Move to logistics:

```
cd ../logistics
```

**Step 8.** Start Claude. Paste the same prompt.

**What you should see for logistics.**

1. (Same as direct-materials.) Senior Category Lead etc.
2. Logistics. Carriers that move our goods.
3. carriers.csv (20 rows). shipments.csv (~5,000 rows).
4. CAR004 ParcelPlus. Contract ends 2026-06-30.
5. ParcelPlus quality has been below standard.

**Step 9.** Quit. Move to indirect:

```
cd ../indirect
```

**Step 10.** Start Claude. Paste the same prompt.

**What you should see for indirect.**

1. (Same as the others.) Senior Category Lead etc.
2. Indirect spend. Office, software, marketing, legal, audit, MRO, telecoms, fleet, facilities.
3. vendors.csv (80 rows). invoices.csv (~3,000 rows).
4. VEN005 Prism Print. Contract ends 2026-05-31.
5. Invoices for $25,000 or more must use cfo_over_25k. Anything $25,000 or above using manager_under_25k is a violation.

If all three folders give the same answer to question 1 and different answers to questions 2 to 5, your hierarchy works. You are ready for Lesson 5.

## What to do when an answer is wrong

| Wrong answer | Probable cause | Quick fix |
|---|---|---|
| Question 1 returns nothing useful or names a specific supplier. | The global is empty, or category content leaked into the global. | Open `practice/CLAUDE.md`. Check it has the three sections from Lesson 2. Move any specific supplier or vendor out. |
| Question 2 returns "I work in procurement" only. | The category file is still a stub. | Open the category file. Re-do Lesson 3 for that folder. |
| Question 3 lists files from a different category (carriers when you are in direct-materials). | You started Claude in the wrong folder. | Quit. Run `pwd` to confirm where you are. `cd` to the right folder if needed. Restart Claude. |
| Question 4 says "no at-risk entity in this category". | The at-risk note is missing from the category file. | Add a Rules line: "SUP004 (or CAR004, or VEN005) is at_risk." |
| Question 5 returns rules from a different category (the $25k approval rule shows up in direct-materials). | Rules are in the wrong file. | Open the file that has the wrong rule. Move it to the right folder. The $25k rule belongs only in indirect. |

## What Claude did, behind the scenes

1. In direct-materials, Claude Code loaded two files at session start: the global (practice/CLAUDE.md) and the category file (direct-materials/CLAUDE.md). It stacked them into one background document.
2. For question 1 ("What is my role?"), Claude Code answered from the global's "Who I am" section. This answer is the same in all three folders because the global is always loaded.
3. For questions 2 to 5, Claude Code answered from direct-materials/CLAUDE.md: scope is direct materials, files are suppliers.csv and orders.csv, at-risk entity is SUP004 Apex Electronics, and rule is the sourcing deadline.
4. In logistics, Claude Code loaded the global plus logistics/CLAUDE.md. Question 1 gave the same answer. Questions 2 to 5 gave logistics-specific answers: carriers, CAR004 ParcelPlus, and service quality.
5. In indirect, Claude Code loaded the global plus indirect/CLAUDE.md. Questions 2 to 5 gave indirect-specific answers: vendors, VEN005 Prism Print, and the $25,000 approval rule.
6. Claude Code never read any CSV file. All five questions are answerable from the CLAUDE.md files alone. The test proves the hierarchy loads correctly without touching the data.

## Three things that trip beginners up

- **The test passed once but fails after you edit a CLAUDE.md.** Quit Claude (`/quit`) and run `claude` again. CLAUDE.md is read once at session start.
- **Claude is slow on every reply.** The global is too long. Trim it back to 25 to 40 lines.
- **The test passes but Claude still mixes content in real briefs.** Lesson 6 is where one prompt can still go wrong if it forgets to ask for the right file. Stick with Lesson 4 for now; Lesson 6 covers the prompt itself.

## You are done with Lesson 4 when

- `test.md` is saved at `practice/test.md`.
- The test passes from all three category folders.
- Question 1 gives the same answer everywhere.
- Questions 2 to 5 give correctly different answers per folder.
- You re-ran the test once after a small edit, just to confirm you can re-verify in five minutes.

Move to Lesson 5 next.
