# Lesson 4: The Onboarding Script

**Time:** 25 minutes.

## A new analyst starts on Monday

It is Friday afternoon. Your team lead tells you: "Priya Sharma starts Monday in the Atlanta office. She covers Professional Services and Facilities. Get her set up by end of day." Right now, onboarding means 12 manual steps: clone the shared folder, copy the workspace template, fill in the personal CLAUDE.md, set the environment variable, register the hooks, test each hook, run a first query, and verify the audit log. If you miss a step, Priya will hit an error on her first day. In this lesson, you build an onboarding script that does all of those steps in one command.

## What Claude Code is going to do for you

You will create a script that takes four inputs (analyst name, office, categories, and approval limit), creates the workspace, configures the personal CLAUDE.md, links the shared skills and hooks, and runs a verification test. One command. No missed steps. Every new analyst starts the same way.

## Set up

1. Navigate to the practice folder:

```
cd "Course_12_The_Team_Deployment_Architect/practice"
```

2. Confirm the template exists:

```
ls analyst-workspace-template/
```

You should see `CLAUDE.md`, `Drafts/`, `Outputs/`, and `Master/`.

3. Start Claude Code:

```
claude
```

**Folder layout:**

```
practice/
├── shared/
│   ├── CLAUDE.md
│   ├── skills/
│   └── commands/
├── hooks/
├── analyst-workspace-template/
├── analyst-workspaces/
│   ├── analyst_01_chen/
│   └── analyst_02_reeves/
└── governance/
```

## Step-by-step

### Step 1: Design the onboarding steps

```
List the steps needed to onboard a new analyst named Priya Sharma in Atlanta, covering Professional Services and Facilities, with a $60,000 approval limit. Include: workspace creation, CLAUDE.md configuration, hooks registration, environment variable setup, and a verification test. Number each step.
```

**What you should see.** A numbered list of 8 to 12 steps covering folder creation, file editing, settings configuration, and testing.

### Step 2: Create the onboarding script

```
Create a Python script at scripts/onboard_analyst.py. The script should accept four command-line arguments: analyst_name, office, categories (comma-separated), and approval_limit. It should: 1) Create a folder at analyst-workspaces/analyst_XX_lastname/ where XX is the next number and lastname is the lowercase last name. 2) Copy all files and folders from analyst-workspace-template/ to the new folder. 3) Open the new CLAUDE.md and replace [ANALYST_NAME], [OFFICE_LOCATION], [CATEGORIES], [APPROVAL_LIMIT_USD], and [MANAGER_NAME] with the provided values (use "Assigned at orientation" for manager name). 4) Create a .claude/settings.json in the new workspace that registers the three hooks from hooks/. 5) Print each step as it runs. 6) Print "Onboarding complete" at the end.
```

**What you should see.** Claude creates the script with argument parsing, file copying, template replacement, and settings generation.

### Step 3: Run the script for Priya

Quit Claude first:

```
/quit
```

Run the onboarding script:

```
python scripts/onboard_analyst.py "Priya Sharma" "Atlanta" "Professional Services,Facilities" "$60,000"
```

**What you should see.** The script prints each step: "Creating workspace... Copying template... Configuring CLAUDE.md... Registering hooks... Onboarding complete."

### Step 4: Verify the workspace

Start Claude Code:

```
claude
```

```
Read analyst-workspaces/analyst_03_sharma/CLAUDE.md. Confirm it shows Priya Sharma, Atlanta, Professional Services and Facilities, and $60,000.
```

**What you should see.** All four fields are filled in correctly.

### Step 5: Verify the hooks are registered

```
Read analyst-workspaces/analyst_03_sharma/.claude/settings.json. Does it register the audit-log, review-gate, and team-notify hooks?
```

**What you should see.** A JSON file with all three hooks listed under PostToolUse and PreToolUse as appropriate.

### Step 6: Run a test write in Priya's workspace

```
Write "Test file for Priya Sharma onboarding verification" to analyst-workspaces/analyst_03_sharma/Drafts/onboarding_test.md.
```

**What you should see.** The file is written. If the audit hook is active, a log entry appears in `governance/audit-log.csv`.

### Step 7: Verify the audit log entry

```
Read governance/audit-log.csv. Does the most recent entry reference Priya's workspace?
```

**What you should see.** An entry with the file path pointing to `analyst_03_sharma/Drafts/onboarding_test.md`.

### Step 8: Quit Claude

```
/quit
```

## Worked example: onboarding in one command

**The prompt you type (in the terminal, not Claude Code):**

```
python scripts/onboard_analyst.py "Priya Sharma" "Atlanta" "Professional Services,Facilities" "$60,000"
```

**Folder layout after onboarding:**

```
practice/
├── analyst-workspaces/
│   ├── analyst_01_chen/
│   ├── analyst_02_reeves/
│   └── analyst_03_sharma/
│       ├── CLAUDE.md               (Priya's identity)
│       ├── .claude/
│       │   └── settings.json       (hooks registered)
│       ├── Drafts/
│       │   └── onboarding_test.md  (verification file)
│       ├── Outputs/
│       └── Master/
└── governance/
    └── audit-log.csv               (entry for test write)
```

**What you should see:**

The script output:
```
Step 1: Creating workspace at analyst-workspaces/analyst_03_sharma/
Step 2: Copying template files...
Step 3: Configuring CLAUDE.md for Priya Sharma...
Step 4: Registering hooks in .claude/settings.json...
Step 5: Onboarding complete. Workspace ready at analyst-workspaces/analyst_03_sharma/
```

**What Claude did behind the scenes (the script logic):**

1. The script parsed the four arguments from the command line.
2. It counted existing analyst folders to determine the next number (03).
3. It extracted the last name ("Sharma") and lowercased it for the folder name.
4. It copied the template folder using `shutil.copytree`.
5. It opened `CLAUDE.md`, replaced the five placeholder tokens with the real values, and saved.
6. It created `.claude/settings.json` with hook registrations pointing to the shared `hooks/` folder.
7. It printed each step and confirmed completion.

## Common mistakes and how to recover

| Symptom | Fix |
|---|---|
| The script fails with "template folder not found." | Check the relative path. If you run the script from outside the practice folder, the path `analyst-workspace-template/` will not resolve. Run the script from inside `practice/`. |
| The CLAUDE.md still has `[ANALYST_NAME]` after running the script. | The placeholder text in the template must match exactly. Check for extra spaces or different bracket styles. Open the template and confirm the placeholders are `[ANALYST_NAME]`, not `{ANALYST_NAME}` or `<ANALYST_NAME>`. |
| The hooks folder path in settings.json is wrong. | The path in settings.json should be relative to where Claude Code runs. If Claude runs from the analyst workspace, the path to hooks is `../../hooks/`. If it runs from the practice root, the path is `hooks/`. |
| Two analysts get the same folder number. | The script counts existing folders. If two people run the script at the same time, they may get the same number. Add a check: if the folder already exists, increment the number. |
| The onboarding test file does not trigger the audit log. | The audit hook may not be registered correctly in the new workspace's settings.json. Check the hook command path and confirm Claude Code was started from the correct directory. |

## You are done with Lesson 4 when

- You have an onboarding script at `scripts/onboard_analyst.py`.
- The script created Priya Sharma's workspace with the correct identity, hooks, and folder structure.
- A test write in Priya's workspace produced an audit log entry.
- You can onboard the next analyst by running one command with four arguments.

Move to Lesson 5 when ready.
