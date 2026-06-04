# Start Here

You are a procurement professional about to practice spend analysis, sourcing, contract review, and supplier management on realistic fake data, with no risk to real client files. This pack holds 20 hands-on courses for Claude Code (the terminal version of Claude; everything in this pack runs there). Between unzipping and Lesson 1 sit two things: a free license key, and the first course's practice data. Both take about 10 minutes, once, and this guide walks you through them.

By the end of this page you will have a working course folder, your key saved, Course 02's data installed, and your first answer from Claude Code about a supplier portfolio.

## What is in the pack, and what is not

The zip you downloaded contains every lesson of every course, readable right away. It does not contain the practice data, the solutions, or the data-repair scripts. Those arrive per course, through a small download tool called `fetch.py`, which checks your license key each time.

Why this matters. The lessons teach you the method, but the learning happens against the data: 2,500 purchase orders, 50 suppliers, 20 contracts, real volumes. Without a key the pack is a book. With a key it is a training environment. Your key is free for 30 days and covers all 20 courses.

## What you need before starting

1. A Windows or Mac laptop with Claude Code installed and signed in.
2. Python 3.10 or newer (the download tool uses it; most laptops with Claude Code already have it).
3. An internet connection for setup and for the start of each course. The lessons themselves run without internet.

## One-time setup

**Step 1. Unzip the pack to a dedicated folder.**

What you do: extract the zip somewhere sensible, for example `Documents/S2P_Course_Pack/`. Not the Desktop, not the OneDrive root, not a folder holding unrelated work.

What you should see: a folder containing `START_HERE.md`, `fetch.py`, `u2xai_config.json`, a `scripts/` folder, and 20 course folders named `Course_02_...` through `Course_21_...`.

**Step 2. Check Python.**

What you type, in a terminal (the black window where you type commands), from inside the pack folder:

```
python --version
```

What you should see: `Python 3.10` or higher. If you see "python is not recognized", install Python from python.org, tick "Add python to PATH" during install, then close and reopen the terminal.

**Step 3. Get your free key.**

Sign up with your work email at https://api.u2xai.academy. The key shows on screen and arrives by email from U2xAI Academy. It looks like `U2X-7F3K-92MD-Q4XR`, is valid for 30 days, and works on up to 2 machines. The same page recovers a lost key and shows your key's status any time.

**Step 4. Fetch your first course.**

What you type:

```
python fetch.py course-02
```

What you should see: a prompt asking for your key (paste it once; it is saved to `u2xai_config.json` after that), then a download, then a line like `142 files installed. Course 02 data ready.`

If you see "Cannot reach the license server", check your internet connection and run the same command again. If you see "This key was not recognized", compare the key against the email character by character; the letters O and I are never used in keys.

**Step 5. Open the course.**

What you type:

```
cd Course_02_The_Context_Architect
```

Then open `lessons/Lesson_01_How_Claude_Reads_CLAUDE_md.md` and follow it. Every lesson tells you exactly what to type and what you should see.

## Your first answer, end to end

Here is the whole flow once, with real output, so you know what working looks like.

The folder after a successful fetch:

```
S2P_Course_Pack/
├── START_HERE.md
├── fetch.py
├── u2xai_config.json          your key lives here
├── scripts/
│   └── check_license.py       the license check, runs automatically
└── Course_02_The_Context_Architect/
    ├── lessons/
    └── practice/
        └── direct-materials/
            ├── suppliers.csv   50 suppliers
            └── orders.csv      2,500 purchase orders
```

The prompt to type, after starting Claude Code inside `practice/direct-materials/`:

```
Do not edit any file in this folder. Read from it freely.
List my top 10 suppliers by annual value from suppliers.csv.
```

What you should see: a ranked table of 10 suppliers with names like Northwind Office Ltd and their annual values in USD, in a few seconds.

What Claude did, behind the scenes:

1. Claude Code read your instruction and noted the folder is read-only for edits.
2. It opened `suppliers.csv` and parsed the 50 rows.
3. It sorted the rows by the annual value column, descending.
4. It took the top 10 and formatted them as a table with names and USD figures.
5. It kept the file untouched, because your first line told it to.

That pattern, you describe the task and name the file, Claude Code does the reading and the arithmetic, is the heart of all 20 courses.

## How the license works while you study

Your key is checked at two moments: when you fetch a course's data, and quietly at the start of each working session. The session check uses a saved pass that lasts 72 hours, so you can work offline for up to three days at a stretch; the tool only goes online when the pass needs renewing.

Why this matters. Nothing interrupts you mid-lesson, ever. The checks happen between courses and between sessions, never between steps. If your trial ends, the courses pause where you stand, every file you produced in Drafts/ and Outputs/ stays yours, and renewing resumes exactly where you stopped.

The file `u2xai_config.json` holds your key and the server address. Treat it like a building pass: do not email it around, and do not commit it anywhere shared. Why this matters. The key identifies you. If it leaks and someone else activates it, you lose one of your 2 machine slots, and support has to reset it.

## Starting each new course

At the start of every course, fetch its data first:

```
python fetch.py course-05
```

Valid names run from `course-02` to `course-21`. The limit is 6 course fetches per day, which is more than anyone studies in a day. If you delete or break a course's data during practice, run the same fetch command again; it reinstalls cleanly.

## Cautions and ground rules

- Pause OneDrive or SharePoint sync before running a fetch, and resume after. Half-synced files cause "file in use" errors.
- Never edit the source data files the lessons read. The first prompt of every session names the read-only folders; keep that habit.
- All data in this pack is fake: invented suppliers, invented spend, invented contracts. Never paste real client data into practice folders.
- Your key works on 2 machines. A desk machine and a laptop are fine; a team is not. Teams need their own keys.

## When something goes wrong

| What you see | The fix |
|---|---|
| "This key was not recognized" | Re-copy the key from the signup email. Check `u2xai_config.json` has no extra spaces around it. |
| "Your trial ended on ..." | The 30 days are up. Follow the renewal link in the message. Your drafts and outputs are untouched, and you resume where you stopped. |
| "Cannot reach the license server" | Check your internet, then run the command again. If your network blocks unknown sites, ask IT to allow the server address shown in `u2xai_config.json`. |
| "Too many requests" | You hit the 6-fetches-per-day limit. Wait until tomorrow, or contact support if you believe this is wrong. |
| "Course id not recognized" | Use the exact form `course-NN`, for example `course-07`, with the hyphen and two digits. |
| Files end in `.tmp` or refuse to open after a fetch | OneDrive was syncing during the download. Pause sync, run the fetch again, resume sync after. |

Support: support@u2xai.com [TBC: confirm address]. Include the command you ran and the exact message you saw.
