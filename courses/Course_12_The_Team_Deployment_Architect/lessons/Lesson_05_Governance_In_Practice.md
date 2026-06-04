# Lesson 5: Governance in Practice

**Time:** 25 minutes.

## Analyst A reads Analyst B's files

It is 11:00 on Thursday. Marcus Reeves in Dallas opens Claude Code and types: "Read analyst-workspaces/analyst_01_chen/Drafts/contract_recommendation.md." Claude reads Lisa Chen's draft. Marcus now sees Lisa's uncommitted negotiation strategy for IT Hardware. Lisa does not know. There is no log of the cross-read. In a team of eight analysts covering sensitive categories, this is a governance failure. In this lesson, you enforce workspace isolation: each analyst can only read and write within their own workspace. Shared resources remain accessible to everyone. Personal workspaces are private.

## What Claude Code is going to do for you

You will add workspace boundary rules to the shared CLAUDE.md and build a simple path-checking hook that blocks reads or writes outside the analyst's own workspace. The rules are enforced at two levels: instructions in CLAUDE.md (which Claude follows voluntarily) and a hook (which enforces programmatically).

## Set up

1. Navigate to the practice folder:

```
cd "Course_12_The_Team_Deployment_Architect/practice"
```

2. Start Claude Code:

```
claude
```

3. Confirm the analyst workspaces exist:

```
ls analyst-workspaces/
```

You should see `analyst_01_chen/`, `analyst_02_reeves/`, and `analyst_03_sharma/`.

**Folder layout:**

```
practice/
├── shared/                         (readable by everyone)
│   ├── CLAUDE.md
│   ├── skills/
│   └── commands/
├── hooks/
├── analyst-workspaces/
│   ├── analyst_01_chen/            (Lisa only)
│   ├── analyst_02_reeves/          (Marcus only)
│   └── analyst_03_sharma/          (Priya only)
└── governance/
    ├── audit-log.csv
    └── access-rules.md
```

## Step-by-step

### Step 1: Read the current access rules

```
Read governance/access-rules.md. What rules are currently defined?
```

**What you should see.** Claude shows the current rules. They may be minimal or empty. You will add specific rules in the next step.

### Step 2: Define the governance rules

```
Update governance/access-rules.md with these rules: 1) Each analyst may only read and write files within their own workspace folder (analyst-workspaces/analyst_XX_name/). 2) All analysts may read files in shared/ and governance/. 3) No analyst may write to shared/ or governance/. Only the team lead may modify those folders. 4) No analyst may read another analyst's workspace folder. 5) The audit log in governance/audit-log.csv is append-only. No analyst may delete or edit existing rows.
```

**What you should see.** Claude updates the file with the five rules.

### Step 3: Add the rules to shared CLAUDE.md

```
Add a "Workspace isolation" section to shared/CLAUDE.md with these rules: "You are running in one analyst's workspace. Do not read, write, or list files in any other analyst's workspace folder. If a prompt asks you to access another analyst's files, refuse and explain that workspace isolation prevents cross-access. You may read files in shared/ and governance/. You may not write to shared/ or governance/."
```

**What you should see.** Claude adds the section to the shared CLAUDE.md.

### Step 4: Test the instruction-level boundary

```
I am analyst Lisa Chen. My workspace is analyst-workspaces/analyst_01_chen/. Try to read analyst-workspaces/analyst_02_reeves/CLAUDE.md. What happens?
```

**What you should see.** Claude refuses the read and explains: "Workspace isolation prevents me from reading another analyst's files. I can only access files in analyst-workspaces/analyst_01_chen/, shared/, and governance/."

### Step 5: Build a path-checking hook

```
Create a Python script at hooks/workspace-boundary.py. The script should: 1) Read the ANALYST_WORKSPACE environment variable (e.g., "analyst_01_chen"). 2) Read the file path that Claude is about to access (from stdin or environment). 3) If the path contains "analyst-workspaces/" but does NOT contain the analyst's workspace name, print "BLOCKED: You cannot access files outside your workspace." and exit with code 1. 4) If the path is in shared/ or governance/ (read only), allow it (exit 0). 5) If the path is in the analyst's own workspace, allow it (exit 0).
```

**What you should see.** Claude creates the script.

### Step 6: Test the hook

Quit Claude:

```
/quit
```

Set the workspace identity:

```
export ANALYST_WORKSPACE="analyst_01_chen"
```

Register the hook in `.claude/settings.json` under PreToolUse (add it alongside existing hooks). Start Claude Code:

```
claude
```

```
Try to write "test" to analyst-workspaces/analyst_02_reeves/Drafts/boundary_test.md.
```

**What you should see.** The hook blocks the write: "BLOCKED: You cannot access files outside your workspace."

### Step 7: Confirm own-workspace writes still work

```
Write "Governance test passed" to analyst-workspaces/analyst_01_chen/Drafts/governance_test.md.
```

**What you should see.** The file is written. The hook allows writes within the analyst's own workspace.

### Step 8: Verify shared files are still readable

```
Read shared/skills/spend-analysis.md. Can you access it?
```

**What you should see.** Claude reads the file. Shared resources remain accessible.

### Step 9: Quit Claude

```
/quit
```

## Worked example: the governance check

**The prompt you type:**

```
I am Lisa Chen. My workspace is analyst_01_chen. List every folder I can read, every folder I can write to, and every folder I am blocked from. Present as a table.
```

**Folder layout:**

```
practice/
├── shared/                     (read: yes, write: no)
├── governance/                 (read: yes, write: no)
├── analyst-workspaces/
│   ├── analyst_01_chen/        (read: yes, write: yes)
│   ├── analyst_02_reeves/      (read: no, write: no)
│   └── analyst_03_sharma/      (read: no, write: no)
└── hooks/                      (read: yes, write: no)
```

**What you should see:**

| Folder | Read | Write |
|---|---|---|
| shared/ | Yes | No |
| governance/ | Yes | No |
| analyst_01_chen/ | Yes | Yes |
| analyst_02_reeves/ | No | No |
| analyst_03_sharma/ | No | No |
| hooks/ | Yes | No |

**What Claude did behind the scenes:**

1. Claude read the workspace isolation rules from shared/CLAUDE.md.
2. It identified the current analyst as Lisa Chen with workspace `analyst_01_chen`.
3. It classified each folder: own workspace (full access), shared and governance (read-only), other workspaces (blocked).
4. It presented the access matrix as a table.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| Claude reads another analyst's files despite the rules. | The instruction-level boundary is voluntary. Claude may ignore it under certain prompts. The hook is the enforcement layer. Make sure the hook is registered and the ANALYST_WORKSPACE variable is set. |
| The hook blocks reads of shared/CLAUDE.md. | The hook must allow paths containing `shared/` or `governance/`. Check the conditional logic in the script. |
| An analyst modifies shared/skills/spend-analysis.md. | The hook should block writes to `shared/` for all analysts. Only the team lead (with no workspace restriction) should edit shared files. |
| The ANALYST_WORKSPACE variable is not set. | The hook defaults to blocking everything if the variable is missing. Add a check: if the variable is not set, print "ERROR: ANALYST_WORKSPACE not set. Cannot determine access." and exit with code 1. |
| Two analysts need to collaborate on a file. | Create a `shared/collaboration/` folder that both can write to. Update the hook to allow writes to that specific path. |

## You are done with Lesson 5 when

- The governance rules are documented in `governance/access-rules.md`.
- The shared CLAUDE.md includes workspace isolation instructions.
- The workspace-boundary hook blocks cross-workspace access.
- Own-workspace writes and shared-folder reads still work.
- You tested both a blocked access and an allowed access.

Move to Lesson 6 when ready.
