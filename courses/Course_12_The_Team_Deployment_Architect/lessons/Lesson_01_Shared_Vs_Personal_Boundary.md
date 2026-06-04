# Lesson 01: Shared vs. Personal Boundary

**Course:** The Team Deployment Architect
**Time:** 45 minutes
**Prerequisites:** Claude Code installed and signed in. Course practice folder open.

---

## Part 1: The S2P problem

It is 08:45 Monday. Your VP has approved the Claude Code deployment. You have 8 analysts across Chicago, Dallas, and Atlanta, and a two-week window to get everyone operational. You already built the system on your own laptop: a shared CLAUDE.md with team standards, three canonical skills, three slash commands, and two hooks. Now you need to give each analyst a workspace that runs those shared resources without letting any one analyst break them for everyone else. Getting this boundary wrong is the most common cause of team deployments falling apart. If Sarah in Chicago can edit the shared scoring weights, and Marcus in Dallas has different weights by Thursday, you have eight different Claude Code instances producing inconsistent outputs with no way to reconcile them.

---

## Part 2: What Claude Code is going to do for you

By the end of this lesson, you will have a documented file boundary that every analyst understands. Shared files live in `shared/` and `hooks/`, are managed only by you, and are read by every analyst workspace. Personal files live in each analyst's own workspace and can be customized freely, as long as they do not contradict the shared context. Claude Code will read both layers in every session. The result: consistent outputs across all eight analysts, with room for each person to add their own working notes and category-specific preferences.

---

## Part 3: Set up

1. Claude Code is installed and you are signed in.
2. The course practice folder is open: `Course_12_The_Team_Deployment_Architect/practice/`.
3. The shared context file exists at `practice/shared/CLAUDE.md`.
4. The governance documents exist in `practice/governance/`.
5. The analyst workspace template exists at `practice/analyst-workspace-template/`.
6. OneDrive sync is paused for the duration of this lesson. Resume when finished.

Open Claude Code in the practice folder:

```
cd "Course_12_The_Team_Deployment_Architect/practice"
claude
```

Set the read-only rule for shared resources at the start of every session:

```
The folders shared/, hooks/, and governance/ are read-only. Do not edit any file in those folders.
Read from them freely. Save all output to the relevant analyst workspace or to a new file I specify.
```

---

## Part 4: Step-by-step

**Step 1.** Open Claude Code in the practice folder.

```
cd "Course_12_The_Team_Deployment_Architect/practice"
claude
```

You should see the Claude Code prompt with `practice` in the path shown at the top.

**Step 2.** State the read-only rule for shared resources.

```
The folders shared/, hooks/, and governance/ are read-only. Do not edit any file in those folders.
Read from them freely. Save all output to the relevant analyst workspace or to a new file I specify.
```

Claude should confirm it understands. Nothing changes on disk.

**Step 3.** Ask Claude to read the shared context and summarize what every analyst inherits.

```
Read shared/CLAUDE.md and list: (1) the org details every analyst inherits, (2) the output standards every analyst must follow, and (3) the audit rules that apply to everyone. Do not change the file.
```

You should see three numbered sections summarizing the shared context. If the list is empty, check that `shared/CLAUDE.md` exists and is not blank.

**Step 4.** Ask Claude to read the governance boundary documents and produce a two-column summary table.

```
Read governance/what-is-shared.md and governance/what-is-personal.md.
Produce a table with two columns: "Shared (managed centrally)" and "Personal (analyst owns)".
List every file or folder category mentioned in both documents.
Save the table to a new file: governance/boundary-summary.md.
```

You should see confirmation that `governance/boundary-summary.md` was saved. Open it to verify the two-column layout.

If Claude says it cannot write to `governance/`, you forgot to allow writes there. The read-only rule in Step 2 covers all three shared folders. Adjust the rule: "Do not edit shared/, hooks/, or analyst-workspace-template/. You may write to governance/ only when I ask for a new summary file."

**Step 5.** Ask Claude to read the analyst workspace template and identify which parts are placeholders that each analyst fills in.

```
Read analyst-workspace-template/CLAUDE.md.
List every placeholder (text in square brackets) and describe what information goes there.
Do not change the file.
```

You should see a list of the two placeholders: `[Analyst Name]` and `[Office]`, with a one-line description of each. If no placeholders are listed, open the file by hand and confirm the brackets are intact.

**Step 6.** Test the boundary by asking Claude to explain what happens if an analyst edits `shared/CLAUDE.md` directly.

```
Based on governance/what-is-shared.md, explain in two sentences what an analyst should do instead of editing shared/CLAUDE.md directly.
```

You should see a two-sentence answer that names the Operations Manager as the owner and the governance update process as the path.

---

## Part 5: Worked example, end to end

**Scenario.** Lisa Chen in Chicago wants to add a personal note that her MRO category uses Net-45 payment terms, not the team default of Net-30. She should not change `shared/CLAUDE.md`. She should add the note to her personal workspace CLAUDE.md.

**Starting files:**

- `shared/CLAUDE.md`: team context, v1.0, 2026-04-25.
- `analyst-workspace-template/CLAUDE.md`: blank personal template with two placeholders.
- `governance/what-is-personal.md`: rules for personal files.

**Prompts, in order:**

**Prompt 1.** Confirm shared context is intact.

```
Read shared/CLAUDE.md. What is the team-wide payment terms standard?
Do not change the file.
```

Expected output: "No payment terms standard is specified in shared/CLAUDE.md. The output standards cover currency, dates, and writing style."

**Prompt 2.** Add Lisa's personal note to her workspace.

```
Read analyst-workspace-template/CLAUDE.md.
Create a new file at workspaces/lisa_chen/CLAUDE.md with the template content.
Replace [Analyst Name] with Lisa Chen and [Office] with Chicago.
Add a personal note under "Personal preferences": "MRO category uses Net-45 payment terms. Flag any invoice with Net-30 terms for review."
```

Expected output: Confirmation that `workspaces/lisa_chen/CLAUDE.md` was created.

**Prompt 3.** Verify the boundary is clean.

```
Read workspaces/lisa_chen/CLAUDE.md and shared/CLAUDE.md.
Does Lisa's personal file contradict anything in the shared file?
```

Expected output: "No contradictions. The personal file adds a MRO-specific note not present in the shared file."

**Short extract from `workspaces/lisa_chen/CLAUDE.md`:**

```
## Personal preferences
MRO category uses Net-45 payment terms. Flag any invoice with Net-30 terms for review.
```

**Finished artifact:** `workspaces/lisa_chen/CLAUDE.md`. A personal context file that extends the shared context without overwriting it.

---

## Part 6: Common mistakes and how to recover

- **Symptom:** An analyst edits `shared/CLAUDE.md` directly and changes the scoring weights. **Fix:** Restore `shared/CLAUDE.md` from version history (SharePoint or Git). Ask the analyst to add their preference to their personal CLAUDE.md instead. Review the governance documents with the whole team.

- **Symptom:** An analyst's personal CLAUDE.md contradicts the shared file (for example, it sets recommendations capped at five instead of three). **Fix:** Ask Claude to read both files and list contradictions. Ask the analyst to remove the contradicting line and add a comment explaining why they wanted the change. Bring it to the next shared-resource review if it reflects a real gap in the team standard.

- **Symptom:** Claude reads only the personal CLAUDE.md and ignores `shared/CLAUDE.md`. **Fix:** Check that your session-opening prompt tells Claude to read both. Add a line at the top of the analyst's personal CLAUDE.md: "Also read shared-context.md in this folder for team-wide standards."

- **Symptom:** The `governance/boundary-summary.md` file was saved with outdated information after a shared resource update. **Fix:** Rerun Step 4 after any change to `what-is-shared.md` or `what-is-personal.md`. The summary table should always reflect the current governance documents.

- **Symptom:** A new analyst cannot find the shared skills because the onboarding script did not copy them. **Fix:** Check that `workspaces/<analyst_name>/skills/` exists and contains the three skill files. If not, run: `cp -r practice/shared/skills workspaces/<analyst_name>/skills`.
