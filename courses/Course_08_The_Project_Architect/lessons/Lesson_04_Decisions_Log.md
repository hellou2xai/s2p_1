# Lesson 4: The decisions log pattern

**Time:** 40 minutes.

## Nobody remembers what we decided

It is 09:00 Monday. Marcus Rivera messages you: "Did we push the INIT-007 bid evaluation milestone to June, or did we keep it in May?" You know you made that decision last Thursday. You and Marcus discussed the packaging material switch timeline, agreed to push bid evaluation from 2026-05-24 to 2026-06-15, and Lisa Torres approved the change over email. But you cannot find the record. Your Claude Code session from Thursday is gone. The initiative tracker shows the current milestone dates, but it does not say why you changed them or who approved the change.

Procurement decisions need an audit trail. When the CFO asks "why did the timeline slip?", you need a dated, attributed entry. Not a vague memory.

## What Claude Code is going to do for you

You will create an append-only decisions log at `state/decisions-log.md`. Each decision gets a dated entry with context, the decision itself, and who approved it. Claude appends new entries to the bottom of the file. It never overwrites or removes old entries. The log grows session by session, and every future session can read the full history.

## Set up

1. Lessons 1 through 3 complete (`.claude/settings.json`, updated `CLAUDE.md`, and `state/initiative-tracker.md` all exist).
2. A terminal open in `Course_08_The_Project_Architect/practice/`.

## Step-by-step

### Create the decisions log

**Step 1.** Start Claude Code in the practice folder.

```
cd "Course_08_The_Project_Architect/practice"
claude
```

You should see the Claude Code prompt with CLAUDE.md loaded.

**Step 2.** Create the decisions log file with a header.

```
Create a file at state/decisions-log.md with this content:

# Decisions Log

This file is append-only. New entries go at the bottom. Never delete or edit previous entries.

Format for each entry:
- Date
- Initiative (ID and name)
- Decision
- Context (why)
- Approved by
- Recorded by

---
```

You should see Claude create `state/decisions-log.md` with the header and format instructions.

### Record three decisions

**Step 3.** Record the first decision.

```
Append a new entry to state/decisions-log.md. Do not modify any existing content. Add this decision:

Date: 2026-04-24
Initiative: INIT-007 (Packaging Material Switch)
Decision: Push bid evaluation milestone from 2026-05-24 to 2026-06-15.
Context: Two of five shortlisted suppliers requested additional time to prepare samples. Delaying evaluation by three weeks avoids receiving incomplete bids.
Approved by: Lisa Torres (VP of Procurement)
Recorded by: Savings Program Manager
```

You should see Claude append the entry to the bottom of the file, below the `---` separator.

**Step 4.** Record a second decision.

```
Append another entry to state/decisions-log.md. Do not modify any existing content. Add this decision:

Date: 2026-04-25
Initiative: INIT-002 (Logistics Network Optimization)
Decision: Add two alternate carriers to the bid list to replace declined bidders.
Context: FedEx Freight and XPO Logistics declined to bid. Marcus Rivera identified Estes Express and Old Dominion as replacements. Both meet the minimum $50M revenue threshold.
Approved by: Tom Baker (Supply Chain Director)
Recorded by: Savings Program Manager
```

You should see Claude append the second entry below the first.

**Step 5.** Record a third decision.

```
Append another entry to state/decisions-log.md. Do not modify any existing content. Add this decision:

Date: 2026-04-25
Initiative: INIT-006 (MRO Catalog Standardization)
Decision: Delay scope definition start from 2026-05-21 to 2026-06-01.
Context: David Kim is supporting the INIT-004 scope definition through May. Concurrent scope work on two initiatives would split his time and reduce quality. Sequential is better.
Approved by: Lisa Torres (VP of Procurement)
Recorded by: Savings Program Manager
```

You should see Claude append the third entry below the second.

**Step 6.** Review the full log.

```
Read state/decisions-log.md and show me all three entries.
```

You should see the header followed by three dated entries, each with the six fields (date, initiative, decision, context, approved by, recorded by). All three entries are present. None of the earlier entries were modified.

### Test the append-only pattern

**Step 7.** Exit Claude Code.

```
/quit
```

**Step 8.** Restart Claude Code.

```
claude
```

You should see the Claude Code prompt.

**Step 9.** Ask Claude to recall a decision.

```
Read state/decisions-log.md. What decision was made about INIT-007 on 2026-04-24, and who approved it?
```

You should see: the bid evaluation milestone for Packaging Material Switch was pushed from 2026-05-24 to 2026-06-15, approved by Lisa Torres. The decision survived the session restart.

**Step 10.** Exit Claude Code.

```
/quit
```

## Worked example

**The decisions-log.md after this lesson should look like this:**

```markdown
# Decisions Log

This file is append-only. New entries go at the bottom. Never delete or edit previous entries.

Format for each entry:
- Date
- Initiative (ID and name)
- Decision
- Context (why)
- Approved by
- Recorded by

---

## 2026-04-24: INIT-007 (Packaging Material Switch)

**Decision:** Push bid evaluation milestone from 2026-05-24 to 2026-06-15.

**Context:** Two of five shortlisted suppliers requested additional time to prepare samples. Delaying evaluation by three weeks avoids receiving incomplete bids.

**Approved by:** Lisa Torres (VP of Procurement)

**Recorded by:** Savings Program Manager

---

## 2026-04-25: INIT-002 (Logistics Network Optimization)

**Decision:** Add two alternate carriers to the bid list to replace declined bidders.

**Context:** FedEx Freight and XPO Logistics declined to bid. Marcus Rivera identified Estes Express and Old Dominion as replacements. Both meet the minimum $50M revenue threshold.

**Approved by:** Tom Baker (Supply Chain Director)

**Recorded by:** Savings Program Manager

---

## 2026-04-25: INIT-006 (MRO Catalog Standardization)

**Decision:** Delay scope definition start from 2026-05-21 to 2026-06-01.

**Context:** David Kim is supporting the INIT-004 scope definition through May. Concurrent scope work on two initiatives would split his time and reduce quality. Sequential is better.

**Approved by:** Lisa Torres (VP of Procurement)

**Recorded by:** Savings Program Manager
```

**What Claude did, behind the scenes:**

1. Claude created the file with a header that states the append-only rule.
2. For each decision entry, Claude opened the file, scrolled to the end, and appended the new entry below the last separator.
3. Claude never modified the header or any previous entry.
4. On the next session start, Claude read the full log and had the decision history in context.
5. The format (H2 heading with date and initiative, bold field names) makes entries scannable for both Claude and human readers.

## Common mistakes and how to recover

- **Symptom:** Claude overwrote the entire decisions log instead of appending. All previous entries are gone. **Fix:** always say "append" and "do not modify any existing content." If entries are lost, check your file's version history (OneDrive or git). Restore the previous version and re-append the new entry.

- **Symptom:** Entries have no dates. A week later, you cannot tell when a decision was made. **Fix:** every entry must include a date. Add a line to your CLAUDE.md: "Every decisions-log entry must include a date in YYYY-MM-DD format."

- **Symptom:** Entries have no "approved by" field. The CFO asks who approved a timeline change, and you cannot answer. **Fix:** the approval field is not optional. If a decision is not yet approved, write "Pending: [name]" and update the entry when approval arrives.

- **Symptom:** The log file is getting long (50+ entries) and Claude takes a while to read it. **Fix:** this is normal for a multi-month program. If the file exceeds 200 entries, archive older entries to `state/decisions-log-archive.md` and keep only the last 60 days in the active log.

## You are done with Lesson 4 when

- You have a file at `state/decisions-log.md` with three dated, attributed decision entries.
- You closed Claude Code, reopened it, and retrieved a decision from the log.
- You understand the difference between the initiative tracker (current state, updated in place) and the decisions log (history, append only).

Move to Lesson 5, where you configure project-level settings for tool permissions and slash commands.
