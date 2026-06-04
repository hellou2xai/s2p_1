# Lesson 1: What a Claude Code project is

**Time:** 30 minutes.

## Every Monday starts from scratch

It is 09:15 Monday. You open Claude Code to check on Pinnacle Procurement's $14.9M savings program. You type: "What is the status of the direct materials consolidation initiative?" Claude Code responds: "I don't have context about a direct materials consolidation initiative. Could you provide more details?"

You spent 45 minutes last Thursday building a detailed status update for that exact initiative. You reviewed the savings log, checked two overdue milestones, and drafted an escalation note to Lisa Torres. All of that context vanished when you closed the session. Now you are rebuilding it from scratch. Again.

This happens because Claude Code conversations are temporary. When a session ends, the conversation history goes with it. Every Monday, you re-explain the program, re-read the data files, and re-state decisions you already made.

## What Claude Code is going to do for you

A Claude Code project stores context in files, not in conversation memory. You create a `.claude/` directory and a `CLAUDE.md` file in your project folder. When you start Claude Code in that folder, it reads those files automatically. Your eight initiatives, their stages, their owners, and their current status are all there before you type a single word. No more rebuilding context. No more lost decisions.

## Set up

1. Claude Code installed and signed in.
2. A terminal open.
3. The practice folder for this course available at `Course_08_The_Project_Architect/practice/`.

## Step-by-step

### Understand the two levels of configuration

Claude Code has two levels of settings: global and project.

| Level | Location | Scope |
|---|---|---|
| Global | `~/.claude/settings.json` | Every Claude Code session on your machine |
| Project | `your-project-folder/.claude/settings.json` | Only sessions started inside this folder |

Global settings apply everywhere. Project settings apply only when you run `claude` inside the folder that contains the `.claude/` directory. Project settings override global settings when both exist.

For a savings program with eight initiatives, project-level configuration is the right choice. Your program context should not bleed into other work.

### Create the .claude directory

**Step 1.** Open a terminal and navigate to the practice folder.

```
cd "Course_08_The_Project_Architect/practice"
```

Your terminal prompt should end in `practice`.

**Step 2.** Confirm the practice folder contents.

```
ls
```

You should see: `CLAUDE.md`, `data/`.

**Step 3.** Create the `.claude` directory.

On Windows (PowerShell):

```
mkdir .claude
```

On Mac or Linux:

```
mkdir .claude
```

You should see the `.claude` folder created. If you run `ls -la`, you will see it listed (it starts with a dot, so a plain `ls` may hide it).

### Create settings.json

**Step 4.** Create a minimal `settings.json` file inside `.claude/`.

```
claude
```

Wait for the Claude Code prompt. Then type:

```
Create a file at .claude/settings.json with this content:
{
  "permissions": {
    "allow": [
      "Read(data/*)",
      "Read(state/*)",
      "Write(state/*)",
      "Write(outputs/*)"
    ]
  }
}
```

You should see Claude confirm that `.claude/settings.json` has been created.

**Step 5.** Verify the file exists.

```
Read .claude/settings.json and show me the contents.
```

You should see the JSON you just defined, with permissions for reading data files and reading and writing state files.

**Step 6.** Exit Claude Code.

```
/quit
```

### Verify project detection

**Step 7.** Start Claude Code again in the same folder.

```
claude
```

You should see Claude Code start. It reads `.claude/settings.json` and `CLAUDE.md` automatically. The key test: Claude Code now knows this is a project folder. It loads the settings and context files without you asking.

**Step 8.** Ask Claude a question to confirm context loaded.

```
What is my role according to CLAUDE.md?
```

You should see Claude respond that you are the Savings Program Manager at Pinnacle Procurement, managing eight category initiatives with a $14.9M savings target. Claude read this from the `CLAUDE.md` file that already exists in the practice folder.

**Step 9.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

- `practice/CLAUDE.md` (pre-existing, describes the role and data files)
- `practice/data/initiatives.csv` (8 initiatives)

**What you created:**

- `practice/.claude/settings.json` (project-level permissions)

**What the project looks like now:**

```
practice/
├── .claude/
│   └── settings.json
├── CLAUDE.md
└── data/
    ├── initiatives.csv
    ├── savings-log.csv
    ├── stakeholders.csv
    └── milestone-tracker.csv
```

**What Claude did, behind the scenes:**

1. On startup, Claude Code checked for a `.claude/` directory in the current folder.
2. It found `.claude/settings.json` and loaded the permission rules.
3. It found `CLAUDE.md` in the project root and read it as standing context.
4. It applied the permissions: read access to `data/*` and `state/*`, write access to `state/*` and `outputs/*`.
5. When you asked about your role, Claude answered from `CLAUDE.md` without needing a prompt to read the file.

## Common mistakes and how to recover

- **Symptom:** Claude Code does not read your `CLAUDE.md` on startup. **Fix:** make sure you started Claude Code inside the folder that contains `CLAUDE.md`, not in a parent or child folder. Run `pwd` to check.

- **Symptom:** You created `.claude/settings.json` but Claude Code ignores it. **Fix:** the `.claude/` directory must be at the root of your project folder, not inside a subfolder like `data/.claude/`. Move it to the correct location.

- **Symptom:** You edited the global `~/.claude/settings.json` by mistake. **Fix:** global settings live in your home directory. Project settings live inside the project folder. Check both locations with `ls ~/.claude/` and `ls .claude/` to confirm which one you changed.

- **Symptom:** The JSON file has a syntax error and Claude Code reports a parse failure. **Fix:** check for missing commas, mismatched braces, or trailing commas (JSON does not allow trailing commas). Ask Claude to "read .claude/settings.json and fix any JSON syntax errors."

## You are done with Lesson 1 when

- Your practice folder has a `.claude/` directory with a `settings.json` inside it.
- You can start Claude Code in the practice folder and confirm it reads `CLAUDE.md` automatically.
- You can explain the difference between global settings (`~/.claude/settings.json`) and project settings (`your-project/.claude/settings.json`).

Take a short break. In Lesson 2, you will write a `CLAUDE.md` that encodes all eight initiatives with their stages, owners, and current status.
