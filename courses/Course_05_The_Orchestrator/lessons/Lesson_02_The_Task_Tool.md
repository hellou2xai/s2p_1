# The Task Tool

It is 09:15 Monday morning. You decided in the last lesson that 50 supplier scorecards need sub-agents, not a single sequential session. But before you design the full orchestrator, you need to understand how sub-agents actually work. What can they see? What do they inherit from the parent conversation? What happens if you forget to tell them where the files are? This lesson answers those questions by launching one simple sub-agent and observing exactly what it does.

## What Claude Code does for you

Claude Code's Agent tool (also called the Task tool) launches a separate Claude Code session inside your current session. The sub-agent gets its own context window, runs its own tools, and returns a result to the parent. You control what it knows by writing a clear task prompt. This lesson walks you through launching one sub-agent, reading its output, and understanding the boundary between parent and child context.

## Set up

1. Claude Code installed and signed in.
2. Your terminal open in the `practice/` folder inside `Course_05_The_Orchestrator/`.
3. The `data/` folder contains `supplier-master.csv` and the other five data files from Lesson 1.
4. The `batch-outputs/` subfolder exists. If it does not, create it.

**Step 1.** Confirm the batch-outputs folder exists.

```
mkdir -p batch-outputs
```

You should see no output. The folder now exists (or already existed).

**Step 2.** Open Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

## What the Agent tool does

When you write a prompt that says "use the Agent tool to do X," Claude Code launches a sub-agent. Here is what that sub-agent gets and does not get.

**What the sub-agent receives:**
- The task prompt you write (the instructions you pass to it).
- Access to the same file system. It can read and write files on disk, just like the parent.
- Its own fresh context window. No prior conversation history.

**What the sub-agent does NOT receive:**
- The parent's conversation history. It does not know what you discussed before launching it.
- The parent's CLAUDE.md context. Sub-agents may not automatically load the project's CLAUDE.md file. You must include any critical rules (like scorecard weights or output format) directly in the task prompt.
- Knowledge of other sub-agents. If you launch five workers, each one operates in isolation. Worker B does not know Worker A exists.

This isolation is the feature, not a bug. It is what prevents context contamination.

## Step by step

### Step 3. Set the read-only rule.

```
The folder data/ holds all source files. Do not edit any file in data/. Read from it freely. Save all output to batch-outputs/.
```

Claude confirms the constraint.

### Step 4. Launch one sub-agent.

Type this prompt. It asks Claude to use the Agent tool to read supplier-master.csv and count suppliers by category.

```
Use the Agent tool to perform this task:

"Read the file data/supplier-master.csv. Count the number of suppliers in each category. Return the result as a simple table with two columns: Category and Count. Do not write any files. Just return the table."
```

You should see Claude launch a sub-agent. The sub-agent reads supplier-master.csv, processes the data, and returns a table like this:

| Category | Count |
|---|---|
| raw-materials | 10 |
| logistics | 10 |
| it-services | 10 |
| facilities | 10 |
| professional-services | 10 |

The parent session displays the sub-agent's result.

### Step 5. Confirm the sub-agent did not see your earlier conversation.

Ask the parent session a follow-up question.

```
Did the sub-agent you just launched know about the read-only rule I set for data/?
```

Claude explains that the sub-agent did not inherit the read-only instruction. The sub-agent only received the task prompt you wrote in Step 4. If you need the sub-agent to respect a rule, you must include that rule in the task prompt itself.

### Step 6. Launch a sub-agent that writes a file.

Now launch a sub-agent that does something more useful: it reads the supplier master, filters to raw-materials, and writes a summary file.

```
Use the Agent tool to perform this task:

"Read data/supplier-master.csv. Filter to rows where category is raw-materials. For each supplier, list the supplier_id, supplier_name, tier, and annual_spend_usd. Save the result as a markdown table in batch-outputs/raw-materials-suppliers.md. Do not modify any file in data/."
```

You should see the sub-agent run, read the CSV, filter to 10 rows, and create `batch-outputs/raw-materials-suppliers.md`.

### Step 7. Verify the output file.

Check that the file exists and contains the right data.

```
Read the file batch-outputs/raw-materials-suppliers.md and confirm it lists exactly 10 suppliers, all in the raw-materials category.
```

Claude reads the file and confirms 10 raw-materials suppliers: Great Lakes Steel, Heartland Polymers, Pacific Aluminum, Apex Electronics, Cascade Fasteners, Summit Metals, Liberty Composites, Frontier Plastics, Harbor Wire, and Keystone Coatings.

## Worked example

**Starting file:** `data/supplier-master.csv` (50 suppliers across 5 categories).

**Prompt typed (Step 4):**

```
Use the Agent tool to perform this task:

"Read the file data/supplier-master.csv. Count the number of suppliers in each category. Return the result as a simple table with two columns: Category and Count. Do not write any files. Just return the table."
```

**What you saw:** The sub-agent returned a table showing 10 suppliers per category, for a total of 50.

**What Claude did, behind the scenes:**

1. The parent session received your prompt and recognized the "Use the Agent tool" instruction.
2. Claude launched a new sub-agent session with its own empty context window.
3. The sub-agent received only the text inside the quotes as its task prompt.
4. The sub-agent used the Read tool to open `data/supplier-master.csv` from the file system.
5. It parsed the CSV, grouped rows by the `category` column, and counted each group.
6. It formatted the counts as a markdown table and returned the result to the parent session.
7. The parent session displayed the sub-agent's response in your conversation.

## Common mistakes and how to recover

- **Symptom:** The sub-agent says "I don't have access to supplier-master.csv" or "file not found." **Fix:** You gave a relative path that does not resolve from the sub-agent's working directory. Use the path relative to where Claude Code was started. If you started in `practice/`, then `data/supplier-master.csv` is correct.

- **Symptom:** The sub-agent ignores your read-only rule and modifies a data file. **Fix:** The sub-agent did not receive the read-only instruction because it was part of the parent conversation, not the task prompt. Add "Do not modify any file in data/" to the task prompt itself.

- **Symptom:** You assume the sub-agent knows the scorecard weights because CLAUDE.md defines them. **Fix:** Sub-agents may not inherit CLAUDE.md context. Pass the weights explicitly in the task prompt: "Scorecard weights: quality 25%, delivery 20%, responsiveness 15%, cost 25%, innovation 15%."

- **Symptom:** The sub-agent returns a result, but you cannot find the output file. **Fix:** You told the sub-agent to "save the file" but did not specify the path. Always include the exact output path: "Save to batch-outputs/raw-materials-suppliers.md."

- **Symptom:** You launch a sub-agent expecting it to continue where the last sub-agent left off. **Fix:** Each sub-agent starts fresh. It does not know what other sub-agents produced. If a second sub-agent needs the first sub-agent's output, tell it to read the file the first sub-agent wrote.
