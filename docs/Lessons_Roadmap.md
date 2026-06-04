# Lessons roadmap

Course lessons that remain to be authored. Each row is one lesson. Build them against `Lesson_Template.md` and `CLAUDE.md`.

The Phase column is priority. **Phase A** lessons are critical for safe procurement use. **Phase B** lessons add depth and productivity. **Phase C** lessons cover team and integration topics.

## Lessons to build

| Phase | Lesson | Tool | Why it matters |
|---|---|---|---|
| A | Permission modes for Claude Code Desktop | Claude Code Desktop | Safety. Plan / Ask / Auto-accept / Auto / Bypass control how much Claude does on its own. The wrong choice on production data destroys files. |
| A | Token efficiency in Cowork and Code | All three (Web, Cowork, Code) | Cost and time. Long chats and the wrong model burn the daily quota. The "Restart from here" pattern saves a session without spending more tokens. |
| B | Routines: scheduled procurement automation | Claude Code Desktop | Productivity. Nightly Oracle pulls, weekly variance reports, on-demand briefs from a phone-triggered API endpoint. |
| B | Parallel sessions with Git worktree isolation | Claude Code Desktop | Productivity. Run three category analyses at once without crossover. Each session is on its own branch of your project folder. |
| B | Voice input with Wispr Flow | All three | Speed. Spoken prompts capture roughly five times more context per minute than typed prompts. Critical for Cowork's interview-style setup. |
| C | Oracle ERP integration: CSV exports and MCP servers | Cowork and Code | Most procurement data lives in Oracle. The CSV export path works for everyone today; the MCP path unlocks live queries against Oracle Fusion. |
| C | Team deployment, governance, and ROI | All three | Scale. Shared `CLAUDE.md` files, shared Routines, role-based first tasks, ROI calculation. |

## Build standards

Every lesson follows:

- The six-part lesson structure in `CLAUDE.md` (S2P problem, what Claude will do, set up, step-by-step, worked example, common mistakes).
- The worked-example rule: prompt in a code block, folder layout in a code block, what you should see, and a "What Claude did, behind the scenes" walkthrough.
- The "Name the specific Claude" rule: every capability statement names which Claude it applies to (Web, Cowork, Code, or all three).
- All writing rules and procurement-specific anti-AI rules from `CLAUDE.md`.
- The standard folder layout from `docs/Folder_Structure.md` (`Master/` for source, `Drafts/` for working files, `Outputs/` for final files).

## File naming and location

- Each lesson lives at `Lessons/Lesson_NN_<Short_Topic>.md` once authored.
- Use the next available number (Lesson_01, Lesson_02, ...) in the order lessons are written, not the order in this roadmap.
- Sample input files for each lesson live at `Lessons/Lesson_NN/Master/`.

## Source material

The two training guides in `Handouts/Claude_Code_Desktop_S2P_Training.docx` and `Handouts/Claude_Cowork_S2P_Training.docx` cover most of these topics already, at length. Each lesson should distil the relevant content from those guides into a single focused 30-minute lesson with one clean worked example.
