# Lesson 1: How Claude finds your CLAUDE.md files

**Time:** 20 minutes.

## A typical Tuesday morning

It is 09:30. Your CPO Slacks: "What is our top spend supplier in materials this month?" You open Claude Code. You type the question. Claude says: "I do not have access to your supplier data."

The reason is simple: Claude does not know which folder your supplier data lives in, or that you even have supplier data, until you tell it. The file that tells Claude is called **CLAUDE.md**. Claude reads CLAUDE.md automatically when you start a session.

In this lesson you will prove, with your own eyes, **which** CLAUDE.md files Claude actually reads when you start Claude in different folders. Twenty minutes from now, you will know exactly how the file lookup works.

## The big idea, in one sentence

When you start `claude` in a folder, Claude looks in that folder for a CLAUDE.md, then in the folder above, then above again, all the way up to your project root, and **stacks every CLAUDE.md it finds** into one big background document for the session.

So if you have one CLAUDE.md at the top of your project, plus one CLAUDE.md inside a subfolder, Claude reads BOTH when you start in that subfolder. That is the whole hierarchy.

## Set up

**Step 1.** Open a terminal.

- On Windows: press the Windows key, type `Terminal` or `PowerShell`, press Enter.
- On Mac: press Cmd+Space, type `Terminal`, press Enter.
- On Linux: open whatever terminal you normally use.

A black or blue window appears. This is where you type commands.

**Step 2.** Move into the practice folder for this course. Type this exact line and press Enter:

```
cd "Course_02_The_Context_Architect/practice"
```

**What you should see.** Your terminal prompt should now end in `practice` (or `practice$` on Mac/Linux). If you see "no such file or directory", you are not in the course folder yet. Navigate to wherever you saved the course on your laptop, then try again.

**Step 3.** List what is in this folder. Type:

```
ls
```

Press Enter. You should see four things printed:

- `CLAUDE.md`
- `direct-materials`
- `indirect`
- `logistics`

If you only see the three folder names without `CLAUDE.md`, run `ls -a` instead.

**The folder layout you are working in.**

```
practice/
├── CLAUDE.md                   (the global, you edit this in Step 5)
├── direct-materials/
│   ├── CLAUDE.md               (you edit this in Step 6)
│   ├── orders.csv
│   └── suppliers.csv
├── logistics/
│   ├── CLAUDE.md               (stub)
│   ├── carriers.csv
│   └── shipments.csv
└── indirect/
    ├── CLAUDE.md               (stub)
    ├── invoices.csv
    └── vendors.csv
```

## Try it: prove the file stacking with your own eyes

You will add a small test marker to two CLAUDE.md files, then watch Claude obey both at once.

**Step 4.** Open the global CLAUDE.md in any text editor:

- Windows: right-click `CLAUDE.md` in File Explorer, choose "Open with", pick Notepad.
- Mac: open it in TextEdit (right-click, "Open With", TextEdit).
- Or use VS Code, Sublime, anything you already have.

You will see three weak lines:

```
# My procurement work

I work in procurement.

Help me with sourcing tasks.
```

**Step 5.** At the bottom of the file, on a new line, type this exact line:

```
At the start of every reply, say "GLOBAL FILE LOADED".
```

Save (Ctrl+S on Windows, Cmd+S on Mac).

**Step 6.** Now open `direct-materials/CLAUDE.md` (the file inside the direct-materials folder). It is currently a stub. Replace its contents with this exact text:

```
After "GLOBAL FILE LOADED", on the next line, also say "MATERIALS FILE LOADED".
```

Save.

**Step 7.** Back in your terminal, move into the direct-materials folder:

```
cd direct-materials
```

Press Enter. Your prompt should now end in `direct-materials`.

**Step 8.** Confirm what is in this folder:

```
ls
```

You should see three items: `CLAUDE.md`, `orders.csv`, `suppliers.csv`. No subfolders. Everything is right here.

**Step 9.** Start Claude Code:

```
claude
```

Press Enter. Wait a few seconds. You should see the Claude Code prompt appear (a blinking cursor next to a `>`).

**Step 10.** Type any short question:

```
Hello, what files are in this folder?
```

Press Enter.

**What you should see.** Claude's reply opens with two lines you put there:

```
GLOBAL FILE LOADED
MATERIALS FILE LOADED
```

Then a sentence or two listing the three files in this folder. Both CLAUDE.md files were loaded. Claude obeyed both instructions.

If you only see GLOBAL FILE LOADED and not MATERIALS FILE LOADED, your direct-materials/CLAUDE.md did not save. Quit Claude (`/quit`), reopen the file in your editor, save again, and retry.

**Step 11.** Quit Claude. Type:

```
/quit
```

Press Enter.

**Step 12.** Move to the logistics folder:

```
cd ../logistics
```

Press Enter. Your prompt should now end in `logistics`.

**Step 13.** Start Claude again:

```
claude
```

**Step 14.** Type the same question:

```
Hello, what files are in this folder?
```

**What you should see now.** Claude says `GLOBAL FILE LOADED` on the first line. The MATERIALS line is gone. Why? Because the logistics folder does not have the materials test marker; it only has the global plus an empty logistics CLAUDE.md.

Then Claude lists the three files in this folder: `CLAUDE.md`, `carriers.csv`, `shipments.csv`. Different files than direct-materials.

This is the entire point of the course in one paragraph: **the same Claude, started in a different folder, reads a different stack of CLAUDE.md files, and behaves differently as a result.**

**Step 15.** Quit Claude (`/quit`).

**Step 16.** Tidy up. Open both files you edited and remove the test markers:

- Delete the line in the global that says `At the start of every reply, say "GLOBAL FILE LOADED".`
- Restore `direct-materials/CLAUDE.md` to its original stub:

```
# Direct materials

(Empty for now. You will fill this in during Lesson 3.)
```

You will write proper content in Lessons 2 and 3.

## What just happened, in plain words

When you started Claude in `direct-materials/`:

1. Claude looked for a `CLAUDE.md` in `direct-materials/`. Found it. Read it.
2. Claude looked in the folder above (`practice/`). Found another. Read it too.
3. Claude looked higher up. No more.
4. Claude stacked both files into background context. The global on top, the direct-materials file under it.

When you started Claude in `logistics/`:

1. Claude looked in `logistics/`. Found a stub.
2. Claude looked above. Found the global.
3. Claude did not see the direct-materials file because it is in a sibling folder, not on the path up.
4. Result: only the global plus the logistics stub were loaded.

## Three things that trip beginners up

- **You started in the wrong folder.** If you start `claude` in `practice/` (the project root), only the global loads. You need to be in a category folder (`direct-materials/`, `logistics/`, or `indirect/`) for the category file to load.
- **You edited a CLAUDE.md while Claude was running.** Claude reads CLAUDE.md once, at session start. Mid-session edits do not apply. Quit Claude (`/quit`) and run `claude` again.
- **You left a test marker in.** If your real briefs later say "GLOBAL FILE LOADED" you forgot to clean up. Open the file and delete the test line.

## You are done with Lesson 1 when

- You ran the test in both `direct-materials/` and `logistics/` and saw the difference.
- You removed the test markers from both files.
- You can answer this question in one sentence: "How does Claude find CLAUDE.md files?"

The answer is: "It looks in the folder I started in, then walks up to the project root, and stacks every CLAUDE.md it finds into one background document."

Take a five-minute break. Then move to Lesson 2.
