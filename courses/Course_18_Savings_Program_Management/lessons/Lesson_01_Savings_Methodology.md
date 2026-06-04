# Savings Methodology Encoding

It is 09:00 Thursday morning. Your CFO's assistant just sent a calendar invite for Tuesday at 10:00 AM: "Savings Program Review." You have eight initiatives, each with a different savings type. Your finance team defines hard savings differently from your sourcing team. The last CFO review turned into a 30-minute argument about whether a specification change counts as "real savings." You need a single, written definition for each savings type before you touch a single number.

## The S2P problem

Savings programs fail at the definition stage, not the calculation stage. When "hard savings" means one thing to the category manager and another to the finance controller, the CFO loses trust in the entire program. Most teams carry these definitions in someone's head or in a slide deck from two years ago. When that person leaves or the slide gets lost, the definitions drift. A $12M target with ambiguous definitions is a $12M argument waiting to happen.

## What Claude Code does for you

You encode your savings methodology directly into CLAUDE.md as structured rules. Every time Claude Code processes a transaction, it applies the same definitions. Hard savings use the formula (baseline_rate minus negotiated_rate) times actual_volume. Soft savings use estimated avoided spend versus prior year. Cost avoidance and working capital each have their own formula. The definitions live in the project, not in someone's memory.

## Set up

1. Claude Code open in `Course_18_Savings_Program_Management/practice/`.
2. The file `data/sourcing-initiatives-log.csv` is present with 8 initiatives.
3. The file `data/market-benchmarks.md` is present.
4. You have read the existing `CLAUDE.md` in the practice folder.

## Step-by-step

### Step 1. Read the existing CLAUDE.md to see what is already there.

```
Read CLAUDE.md and show me its contents.
```

You should see a role definition, a list of data files, a savings methodology table, and reporting standards.

### Step 2. Read the sourcing initiatives log to understand the four savings types in use.

```
Read data/sourcing-initiatives-log.csv and list the unique savings_type values with the initiative names that use each type.
```

You should see four types: hard (SAV-001 through SAV-005), soft (SAV-006), cost_avoidance (SAV-007), and working_capital (SAV-008).

### Step 3. Add detailed calculation rules to CLAUDE.md.

Ask Claude Code to update the methodology section with explicit formulas and validation rules.

```
Update the savings methodology section in CLAUDE.md to include these rules:

1. Hard savings: (baseline_rate - negotiated_rate) x actual_volume. Only count if both baseline and negotiated rates exist in the initiative log. Match transactions by initiative_id.

2. Soft savings: Compare actual spend to prior-year spend for the same category. The reduction is the savings. Mark as "estimated" in all outputs because no contract enforces it.

3. Cost avoidance: (market_price_increase_pct x baseline_spend) - actual_spend. Use market-benchmarks.md for the increase percentage. Mark as "avoided cost, not P&L impact" in outputs.

4. Working capital: (additional_days / 365) x annual_spend x 0.05 cost_of_capital. The 0.05 is Apex's weighted average cost of capital.

5. Validation rule: if a transaction's initiative_id does not match any row in sourcing-initiatives-log.csv, flag it as "unmatched" and exclude it from realized savings.

6. Rounding rule: all USD figures rounded to two decimal places. Display with commas.
```

You should see CLAUDE.md updated with the new methodology section containing all six rules.

### Step 4. Verify the update by asking Claude Code to apply the definitions.

```
Using the methodology in CLAUDE.md, tell me: what savings type is SAV-007 and what formula would you use to calculate its realized savings?
```

You should see Claude Code respond with "cost_avoidance" and the formula: (market_price_increase_pct x baseline_spend) minus actual_spend, with a note that this is avoided cost, not P&L impact.

### Step 5. Test with a boundary case.

```
If a transaction has initiative_id "SAV-099" which does not exist in sourcing-initiatives-log.csv, what should happen according to the methodology rules?
```

You should see Claude Code respond that the transaction is flagged as "unmatched" and excluded from realized savings, per rule 5.

## Worked example

**Starting files:**
- `CLAUDE.md` with the original methodology table.
- `data/sourcing-initiatives-log.csv` with 8 initiatives.

**What you type:**

```
Read data/sourcing-initiatives-log.csv. For SAV-001 (Steel Consolidation), the baseline_rate is $720 per ton and the negotiated_rate is $648 per ton. If a transaction shows 500 tons, what are the realized savings for that transaction? Show me the formula step by step.
```

**What you should see:** Claude Code responds with: (720 minus 648) times 500 equals $36,000.00. It identifies this as a hard savings calculation per the methodology.

**What Claude did, behind the scenes:**

1. Read CLAUDE.md to load the savings methodology rules.
2. Read sourcing-initiatives-log.csv to confirm SAV-001 is a "hard" savings type with baseline $720 and negotiated $648.
3. Applied the hard savings formula: (baseline_rate minus negotiated_rate) times volume.
4. Computed: (720 minus 648) times 500 equals 36,000.
5. Formatted the result as $36,000.00 per the rounding and display rules.

## Common mistakes and how to recover

- **Symptom:** Claude Code treats cost avoidance the same as hard savings. **Fix:** Check CLAUDE.md. The cost avoidance formula must reference market-benchmarks.md for the price increase percentage. Hard savings use baseline and negotiated rates from the initiative log. The two formulas are different.

- **Symptom:** Working capital savings show unrealistic numbers. **Fix:** Confirm the cost_of_capital rate is 0.05 (5%), not 0.5 (50%). A decimal place error here inflates the figure by 10x.

- **Symptom:** Soft savings are reported with the same confidence as hard savings. **Fix:** Check that the methodology in CLAUDE.md includes the "estimated" label for soft savings. Every output that includes soft savings must carry that label.

- **Symptom:** A transaction with an unknown initiative_id gets counted in the total. **Fix:** The validation rule (rule 5) must flag unmatched transactions. Ask Claude Code to re-read CLAUDE.md and reprocess the transaction.
