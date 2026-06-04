# Lesson 4: Renewal Calendar

**Time:** 30 minutes.

## The renewal you almost missed

It is 09:00 Thursday. You get a call from your logistics director at Vanguard Manufacturing: "Did you know our freight contract with Apex Logistics expires in 42 days? We need at least 90 days to run a competitive bid." You did not know. The contract was buried in the register with no alert, no escalation, and no calendar entry. If you had seen it 50 days ago, you would have had time to negotiate. Now you are stuck renewing on the incumbent's terms or scrambling for a last-minute bid.

## What Claude Code is going to do for you

Claude Code reads the contract register, sorts every contract by expiry date, and creates a renewal calendar with 90-day, 60-day, and 30-day escalation flags. You get a single view of what needs attention now, what needs attention next month, and what is safely in the future.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_13_Contract_Intelligence/practice/`.
3. `Drafts/contract_register.json` from Lesson 3 (21 records).

## Step-by-step

### Generate the renewal calendar

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Build the renewal calendar from the register.

```
Read Drafts/contract_register.json. For each active or expiring_soon contract, calculate the number of days until expiry from today (2026-04-25). Add an escalation_flag field using these rules: "red" if 30 days or fewer remain, "amber" if 31 to 60 days remain, "yellow" if 61 to 90 days remain, "green" if more than 90 days remain. Sort by days_until_expiry ascending. Write the result to Drafts/renewal_calendar.json.
```

You should see Claude confirm it wrote the calendar with all active contracts sorted by urgency.

**Step 3.** Get the executive summary.

```
Read Drafts/renewal_calendar.json. Give me a summary: how many contracts are red, amber, yellow, and green? List the red and amber contracts by name, value, and days remaining.
```

You should see something like: 2 red (under 30 days), 3 amber (31 to 60 days), 4 yellow (61 to 90 days), 12 green. The red and amber contracts are listed with supplier names and values.

### Create a CSV for calendar sharing

**Step 4.** Export to a format your team can use.

```
Convert Drafts/renewal_calendar.json to Drafts/renewal_calendar.csv. Include these columns: party_b, contract_file, effective_date, expiry_date, days_until_expiry, escalation_flag, total_value_usd, payment_terms. Keep the sort order by days_until_expiry ascending.
```

You should see Claude confirm the CSV was written.

### Add escalation actions

**Step 5.** Assign default actions to each escalation level.

```
Read Drafts/renewal_calendar.json. Add an action_required field to each record using these rules: red = "Immediate: notify CPO, begin emergency renewal or extension negotiation", amber = "Urgent: issue RFP or begin sole-source justification", yellow = "Plan: add to next sourcing pipeline review, assign category manager", green = "Monitor: no action required this month". Write the updated file back to Drafts/renewal_calendar.json.
```

You should see Claude confirm it updated all records with the action field.

**Step 6.** Generate the board-ready summary.

```
Write a one-page renewal summary to Drafts/renewal_board_summary.md. Include: (1) a table of all red and amber contracts with supplier name, value, expiry date, and recommended action, (2) total value at risk in the next 60 days, (3) total value at risk in the next 90 days. Use today's date (2026-04-25) as the report date.
```

You should see Claude write the summary. The total value at risk should be a specific dollar figure, not a vague estimate.

**Step 7.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── Drafts/
│   └── contract_register.json (21 records)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── renewal_calendar.json (active contracts with escalation flags)
│   ├── renewal_calendar.csv (shareable version)
│   └── renewal_board_summary.md (executive summary for the board)
```

**What Claude did, behind the scenes:**

1. Claude read the contract register and filtered out any contracts with status "expired."
2. It calculated `days_until_expiry` by subtracting today's date from each contract's expiry date.
3. It applied the escalation rules (red/amber/yellow/green) based on the days remaining.
4. It sorted the results so the most urgent contracts appear first.
5. It added action recommendations keyed to each escalation level.
6. It calculated the total USD value of contracts in the red and amber bands for the board summary.

## Common mistakes and how to recover

- **Symptom:** All contracts show "green" because the dates in your practice data are far in the future. **Fix:** check that your practice data includes contracts expiring within 90 days. If not, update two or three contract expiry dates in the register to dates within the next 60 days, then re-run.

- **Symptom:** The days_until_expiry calculation is off by one day. **Fix:** this depends on whether Claude counts today as day zero or day one. Confirm by asking: "What is the days_until_expiry for a contract expiring on 2026-04-26?" The answer should be 1.

- **Symptom:** Expired contracts still appear in the calendar. **Fix:** add a filter to your prompt: "Exclude any contract where expiry_date is before 2026-04-25."

- **Symptom:** The board summary shows "significant value at risk" instead of a dollar amount. **Fix:** re-run with explicit instructions: "State the exact total USD value. Do not use words like significant, substantial, or considerable."
