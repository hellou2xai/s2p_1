# When Sub-Agents Are the Right Design

It is 08:45 Monday morning, the first week after Q1 close. Your VP of Procurement sends a Teams message: "Need all 50 supplier scorecards refreshed by Wednesday COB. Board wants the portfolio risk summary Thursday." You open Claude Code and start scoring suppliers one by one. By supplier 12, the output starts drifting. Supplier 12's quality commentary mentions "similar reject-rate issues seen with Frontier Plastics," but Frontier Plastics is supplier 8. You never asked Claude to compare them. Claude's context window is now packed with 11 prior scorecards, and the model is blending data across suppliers. That is context contamination, and it will only get worse as you keep going.

## What Claude Code does for you

Instead of grinding through 50 suppliers in one long conversation, you will learn to recognize when a task should be split into independent sub-agents. Each sub-agent gets its own clean context window. No bleed-over. No contamination. Every scorecard uses the same weights and format because every sub-agent receives the same instructions. The result: 50 scorecards produced in parallel, each one accurate and self-contained.

## Set up

1. Claude Code installed and signed in.
2. Your terminal open in the `practice/` folder inside `Course_05_The_Orchestrator/`.
3. The `data/` folder contains `supplier-master.csv`, `q1-performance.csv`, `scorecard-history.csv`, `risk-signals.csv`, `spend-by-supplier.csv`, and `scorecard-weights.json`.

## Step by step

### Step 1. Open Claude Code in the practice folder.

Navigate to the practice folder and start a Claude Code session.

```
cd practice
claude
```

You should see the Claude Code prompt with `practice` in the path indicator.

### Step 2. Set the read-only rule for data files.

Tell Claude where the data lives and that it should not modify it.

```
The folder data/ holds all source files. Do not edit any file in data/. Read from it freely. Save all output to batch-outputs/ unless I tell you otherwise.
```

Claude confirms it understands the constraint. No files change on disk.

### Step 3. Try scoring three suppliers sequentially.

Ask Claude to score three raw-materials suppliers one after another in the same conversation.

```
Score these three suppliers for Q1 2026 using the weights in data/scorecard-weights.json. For each supplier, read data/q1-performance.csv and data/scorecard-history.csv, compute the weighted overall score, identify the trend direction, and write a two-paragraph scorecard summary.

1. SUP001 Great Lakes Steel
2. SUP004 Apex Electronics
3. SUP008 Frontier Plastics
```

You should see three scorecard summaries, one after another. Read them carefully. At three suppliers, the output is likely clean. Claude's context window still has room, and the model can keep the three suppliers separate.

### Step 4. Check the context size.

Ask Claude how much of its context window is in use.

```
How many tokens have we used in this conversation so far? Give me a rough estimate.
```

Claude reports an estimate. After three scorecards with supporting data, you are likely at 8,000 to 15,000 tokens. With 50 suppliers, that number would reach 130,000 to 250,000 tokens, well beyond what fits in a single session without quality degradation.

### Step 5. See the contamination risk.

Look at the third scorecard summary (Frontier Plastics). Does it reference data or language from the first two? At three suppliers, it probably does not. But picture supplier 12 in a session that already holds 11 full scorecards. The model has all that text in context. When it writes "quality score declined, similar to trends seen in other raw-materials suppliers," it is pulling from prior scorecards you did not ask it to reference.

## The decision rule: sequential vs. sub-agents

Use this table to decide which approach fits your task.

| Factor | Sequential (one session) | Sub-agents (parallel workers) |
|---|---|---|
| Number of items | Under 10 | 10 or more |
| Items depend on each other | Yes (e.g., cross-supplier comparison) | No (each scored independently) |
| Same template for every item | Not required | Yes, same weights and format |
| Context contamination risk | Low at small counts | High at 10+ items |
| Total time | Manageable for small batches | Much faster for large batches |
| Error isolation | One bad output can affect the rest | One worker fails, others continue |

The quarterly scorecard task hits every sub-agent criterion: 50 independent items, same scoring template, same weights, no cross-supplier dependency in individual scorecards.

## Worked example

**Starting files:** `data/supplier-master.csv` (50 suppliers), `data/q1-performance.csv` (50 rows), `data/scorecard-weights.json` (five weights).

**What you typed:** The prompt in Step 3 above.

**What you saw:** Three scorecard summaries for Great Lakes Steel (overall 93.7), Apex Electronics (overall 69.6), and Frontier Plastics (overall 72.9). Each summary listed dimension scores, trend direction, and a recommendation. The context grew by roughly 4,000 to 5,000 tokens per supplier.

**Key takeaway:** Three suppliers fit comfortably. Fifty would not. The next lesson shows you how to use the Agent tool to launch independent workers that each score a batch of 10 suppliers in their own context window.

## Common mistakes and how to recover

- **Symptom:** You use sub-agents for a task that needs cross-item context, like ranking all 50 suppliers against each other. **Fix:** Cross-item comparison requires all data in one place. Do the ranking in the orchestrator after workers return their batch summaries, not inside the workers.

- **Symptom:** You create batches of 2 suppliers each, spawning 25 sub-agents. **Fix:** Too many sub-agents adds overhead and slows the run. Batch by category (10 per batch, 5 workers) or by a natural grouping. Five to ten workers is a practical range.

- **Symptom:** You put all 50 suppliers into one sub-agent, defeating the purpose. **Fix:** A single sub-agent with 50 items has the same context contamination problem as a sequential session. Split into batches of 10 to 15.

- **Symptom:** Supplier 12's commentary references Supplier 8's data. **Fix:** This is context contamination from a sequential approach. Switch to sub-agents so each worker only sees its own batch. Re-run the affected scorecards.

- **Symptom:** You try sub-agents for a 5-supplier shortlist. **Fix:** Five items fit easily in one session. Sub-agents add complexity you do not need. Use sequential for anything under 10.
