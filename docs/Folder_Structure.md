# Folder and file discipline

Long-form guidance behind the "Folder and file discipline" rules in `CLAUDE.md`. Open this when you set up a new lesson, a new engagement, or a new category folder.

## Why folder layout matters

Claude Code operates on the files in the folder you start it in. What it can see, edit, and save is decided by where you start it and how the folder is structured. Three things go wrong when the layout is loose:

1. Claude edits the master template by accident, because draft and master sit in the same folder.
2. Output files land in the wrong place, get overwritten by the next run, or get lost in a sync conflict.
3. Prompts have to spell out the full path on every step, slowing the lesson and making it brittle.

A clear folder layout removes all three.

## The standard layout

Every project, engagement, or category folder should follow this shape:

```
2026-Q2_Office_Supplies_RFP/
├── Master/        (untouchable templates and source documents)
│   ├── Office_Supplies_RFP_Master.docx
│   └── Suppliers_Q2.xlsx
├── Drafts/        (working files, versioned by suffix)
│   ├── RFP_Q2_v1.docx
│   ├── RFP_Q2_v2.docx
│   └── RFP_Q2_v3.docx
├── Outputs/       (final, signed-off, ready to send)
│   └── RFP_Q2_Final.docx
├── Reference/     (prior RFPs, market data, supplier emails)
└── Archive/       (superseded versions, kept for audit)
```

Adapt the names to the document type, but keep the four roles: master, drafts, outputs, reference. Every project must have a Master/ folder.

## Naming rules

- Use `Title_Case` or `kebab-case`. Pick one per project and stay with it.
- No spaces in any folder or file name that will appear in a prompt. Spaces force quoting on every step and break copy/paste.
- Date prefix any time-bounded work: `2026-Q2_Office_Supplies_RFP/`. Use ISO dates (`YYYY-MM-DD`) so folders sort chronologically.
- Version drafts with a numeric suffix: `_v1`, `_v2`, `_v3`. Promote the chosen draft to `_Final` only when signed off.
- Do not use `:`, `/`, `\`, `*`, `?`, `"`, `<`, `>`, or `|` in file names. Windows blocks them and OneDrive sync silently drops files containing them.
- Avoid apostrophes in supplier names in file names. Use `McDonalds`, not `Mc'Donalds`.
- Keep folder names short. OneDrive paths can hit the Windows 260-character limit. `RFP_Q2/` beats `Office_Supplies_Request_For_Proposal_Quarter_Two_Working_Copy/`.

## Where to start Claude Code

- Always `cd` into the **project folder** (the parent of Master/, Drafts/, and so on), not into a subfolder. That way every prompt can refer to `Master/...` or `Drafts/...` without ambiguity.
- Never start Claude Code at the OneDrive root, the Desktop, `Documents/`, or any folder that contains other unrelated projects. Claude reads what it can see. A wide starting folder means slow startup and a real risk of touching the wrong file.

## Telling Claude what is read-only

In the first prompt of any session, name the read-only areas. One line, every time:

```
The folder Master/ holds the source templates. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

This single instruction prevents most accidental overwrites.

## OneDrive and SharePoint notes

Most S2P work happens inside OneDrive or SharePoint folders. That brings sync into play.

- **Pause sync before a multi-file build.** OneDrive can hold a lock on a file mid-sync. Claude will then see "file in use" or save to a `.tmp` copy. Right-click the OneDrive icon, choose "Pause syncing", do the work, then resume.
- **Wait for the green tick.** Before you start a session, every file in the project folder should show a green tick (synced) icon, not a blue arrow (syncing) or red cross (error).
- **One device at a time.** Do not run Claude Code on the same project folder from a laptop and a desktop in the same session. Sync conflicts produce duplicate files like `RFP_Q2_v3-DESKTOP-AB12.docx` that pollute the folder.
- **Path length.** Keep paths short. See the naming rules above.

## Per-folder CLAUDE.md

You can drop a `CLAUDE.md` inside a project folder for project-specific rules: who the suppliers are, which clauses are mandatory, what the deadline is. That file loads only when Claude is started in that folder. Use this for engagement-specific context that should not bloat the course-wide `CLAUDE.md`.

## Worked example: setting up a new RFP project

1. Create the project folder under your category root:
   ```
   Categories/Office_Supplies/2026-Q2_Office_Supplies_RFP/
   ```
2. Create the four subfolders: `Master/`, `Drafts/`, `Outputs/`, `Reference/`.
3. Move the source files into `Master/`. Confirm a green tick on each file.
4. Pause OneDrive sync.
5. Start Claude Code:
   ```
   cd "Categories/Office_Supplies/2026-Q2_Office_Supplies_RFP"
   claude
   ```
6. First prompt:
   ```
   The folder Master/ holds the source templates and should not be edited.
   Read freely from Master/ and Reference/.
   Save all output to Drafts/ with a _vN suffix.
   Use Outputs/ only when I tell you the draft is final.
   ```
7. Do the work.
8. Resume OneDrive sync. Wait for green ticks.

## Common mistakes and how to recover

- **Symptom:** Claude edited the master file. **Fix:** restore the master from OneDrive version history (right-click in browser, "Version history"). Move the bad edit to `Archive/`. Re-state the read-only rule for `Master/` in your next prompt.
- **Symptom:** A draft file shows a red cross sync icon. **Fix:** open OneDrive, click the icon, follow the conflict prompt. Keep the most recent version, move the conflict copy to `Archive/`.
- **Symptom:** Claude reports "file not found" for a file you can see. **Fix:** check that the prompt uses the exact name, including extension and subfolder. `Drafts/RFP_Q2_v3.docx`, not `RFP_Q2_v3` or `RFP Q2 v3.docx`.
- **Symptom:** Output files appear with a `.tmp` suffix. **Fix:** sync was running. Pause sync, rename the file by removing the `.tmp` suffix, resume sync.
- **Symptom:** Two files appear named `RFP_Q2_v3.docx` and `RFP_Q2_v3-DESKTOP-AB12.docx`. **Fix:** sync conflict from a second device. Pick the correct version, move the other to `Archive/`, do not run Claude on this folder from two devices in parallel again.
