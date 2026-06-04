# Lesson template

This file is the long-form expansion of the six-part lesson skeleton in `CLAUDE.md`. Open it when drafting or reviewing a lesson.

## The six-part structure, expanded

### 1. The S2P problem in one paragraph

Start with the real-world pain. Name the document or task. Name the role. Name the time it usually takes.

Example opener:

> A category manager has to issue an RFP for office supplies across 14 sites. The base RFP template is a 38-page Word file. Updating it for the new scope, refreshing the supplier list, and re-numbering sections by hand normally takes a full afternoon.

### 2. What Claude Code is going to do for you

One short paragraph. State the outcome in business terms before you mention any command.

Example:

> Claude Code will read the master RFP, swap in the new scope, refresh the supplier shortlist from your Excel file, and save a clean draft to your project folder. You review and send. Total time: about ten minutes.

### 3. Set up (only what is needed for this lesson)

Build the project folder using the standard layout in `docs/Folder_Structure.md`: `Master/` for source files, `Drafts/` for working files, `Outputs/` for final files. Do not skip this step. The folder layout is what keeps Claude from editing the master template by accident.

List the prerequisites as a numbered checklist. Keep it to what this specific lesson needs.

1. Claude Code installed and signed in.
2. The project folder `2026-Q2_Office_Supplies_RFP/` created, with `Master/`, `Drafts/`, and `Outputs/` subfolders inside it.
3. `Office_Supplies_RFP_Master.docx` saved in `Master/`.
4. The supplier shortlist saved as `Suppliers_Q2.xlsx` in `Master/`.
5. OneDrive sync paused for the duration of the lesson. Resume when finished.

The first prompt of the session must name `Master/` as read-only and tell Claude to save output to `Drafts/`. Example:

```
The folder Master/ holds the source templates. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

If a setup step has been covered in an earlier lesson, link to that lesson by name. Do not repeat full instructions.

### 4. Step-by-step, with the exact words to type

This is the core of every lesson. Each step has three parts:

1. **What you do.** One short sentence in plain English.
2. **What you type or click.** The exact prompt, command, or menu path, in a code block.
3. **What you should see.** A one-line description of the result, so the reader knows it worked.

Worked example for the RFP task:

**Step 1.** Open Claude Code in the project folder (the parent of `Master/` and `Drafts/`).

```
cd "2026-Q2_Office_Supplies_RFP"
claude
```

You should see the Claude Code prompt with the folder name at the top.

**Step 2.** State the read-only rule for `Master/`.

```
The folder Master/ holds the source templates. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

Claude should confirm it understands. Nothing else changes on disk.

**Step 3.** Ask Claude to read the master RFP and summarise the sections.

```
Read Master/Office_Supplies_RFP_Master.docx and list every section heading with its page number. Do not change the file.
```

You should see a numbered list of headings with page numbers.

**Step 4.** Ask Claude to update the scope section and save the draft.

```
Using Master/Office_Supplies_RFP_Master.docx as the source, replace the "Scope" section with this new scope:
- 14 UK sites listed in Master/Suppliers_Q2.xlsx, sheet "Sites"
- Annual spend band: GBP 1.2m to GBP 1.5m
- Contract length: 24 months with one 12-month extension
Save the result as Drafts/Office_Supplies_RFP_Q2_v1.docx. Leave the master file untouched.
```

You should see a confirmation that `Drafts/Office_Supplies_RFP_Q2_v1.docx` has been created. The file in `Master/` should be unchanged.

**Step 5.** Open the draft from `Drafts/` and skim section 3 (Scope) and section 7 (Supplier List). Confirm the numbers match the brief above.

Every lesson must use this three-part step pattern. If a step has no visible result, say so explicitly ("nothing visible changes; this just sets the working folder").

### 5. A worked example, end to end

After the steps, give one fully worked example with realistic data. Include:

- The starting files (names and a one-line description of each).
- The exact prompts used, in order.
- A short extract of the output (two or three lines is enough).
- The finished artefact (name and one-line description).

Use realistic but fake data. Suppliers like "Northwind Office Ltd" or "Acme Stationery". Spend in round numbers. No real client names.

### 6. Common mistakes and how to recover

End every lesson with a short troubleshooting list. Three to six entries. Each entry is one line of symptom and one line of fix.

Example:

- **Symptom:** Claude rewrote the master file by mistake. **Fix:** ask Claude to restore from the most recent Word autosave, or paste the original back from version history in SharePoint.
- **Symptom:** the supplier list is empty in the draft. **Fix:** check that `Suppliers_Q2.xlsx` is in the same folder and that sheet "Sites" exists with that exact name.
- **Symptom:** the file saved as `.docx` will not open. **Fix:** ask Claude to "save as plain `.docx` for Word 2016 compatibility" and try again.

## Screenshots and visuals

- Every lesson with a UI step has at least one screenshot of that step.
- Crop tight to the relevant area. No full desktop captures.
- Highlight the click target with a thin red rectangle. No arrows, no clip art, no emojis.
- Caption every screenshot with the step number it belongs to.
- Use fake supplier and spend data in any visible content.

## Naming conventions for course files

Keep file names predictable so learners can find them later.

- Lessons: `Lesson_NN_Short_Topic.md`. Example: `Lesson_03_Build_RFP_From_Master.md`.
- Sample inputs: `Sample_<DocType>_<Scenario>.<ext>`. Example: `Sample_RFP_Office_Supplies.docx`.
- Expected outputs: `Expected_<DocType>_<Scenario>.<ext>`.
- Prompt library entries: `Prompt_<Action>_<DocType>.md`. Example: `Prompt_Review_NDA.md`.

Use underscores, not spaces, in file names. Use Title_Case.
