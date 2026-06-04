# Encoding Procurement Policy as Testable Rules

It is 08:00 Tuesday morning. Internal Audit sent the letter yesterday. Three areas of concern: approval authority breaches, preferred supplier non-compliance, and incomplete contract documentation. You have 90 days. The last audit took six weeks of manual checking. This time, you encode the procurement policy into CLAUDE.md as testable rules. Every rule has a threshold, a severity, and a pass/fail condition. When Claude Code checks a transaction, it applies the rules automatically. No judgment calls. No inconsistency between analysts.

## The S2P problem

Procurement policies live in PDF documents that nobody reads after onboarding. When audit asks "does this transaction comply," an analyst opens the policy PDF, finds the relevant section, interprets the threshold, and makes a judgment call. Different analysts interpret differently. One flags a $4,800 purchase approved by a Manager as compliant. Another flags it because it is "close to the $5,000 threshold." Without machine-readable rules, compliance checking is subjective. Subjective compliance checking fails audits.

## What Claude Code does for you

You translate each policy rule from the PDF into a structured rule in CLAUDE.md. Each rule has a name, a description, specific thresholds with dollar amounts, a severity level, and a clear pass/fail condition. Claude Code reads these rules every time it processes a transaction. A $4,800 purchase approved by a Manager either passes (because $4,800 is within the $0-$5,000 Manager tier) or fails (because the approver is wrong). There is no interpretation. The rule is the rule.

## Set up

1. Claude Code open in `Course_21_Compliance_Policy_Audit/practice/`.
2. The existing `CLAUDE.md` has the role, data files, and compliance rules.
3. `data/policy-rules.json` is present with the policy rules in JSON format.
4. `data/approval-matrix.csv` is present with authority levels.

## Step-by-step

### Step 1. Read the existing CLAUDE.md.

```
Read CLAUDE.md and show me the compliance rules section.
```

You should see five rules: approval authority, preferred supplier, documentation completeness, split order detection, and breach escalation. Each has a description and severity.

### Step 2. Read the policy rules JSON.

```
Read data/policy-rules.json and show me the full contents.
```

You should see the same five rules in JSON format with specific thresholds: approval authority tiers ($0-$5,000 Manager, $5,001-$25,000 Director, and so on), split order detection window of 5 days and $5,000 threshold, and breach escalation at 15 violations.

### Step 3. Read the approval matrix.

```
Read data/approval-matrix.csv and show me all rows.
```

You should see 5 levels: Analyst ($0-$5,000 requires Manager approval), Manager ($5,001-$25,000 requires Director), Director ($25,001-$100,000 requires VP), VP ($100,001-$500,000 requires CFO), and CFO ($500,001+ requires Board).

### Step 4. Enhance CLAUDE.md with testable rule definitions.

```
Update the compliance rules section in CLAUDE.md to make each rule fully testable. For each rule, add:

1. Approval authority:
   - Test: compare transaction amount_usd to approval-matrix.csv thresholds. Look up the required approver for the amount range. Compare to the actual approver_title on the transaction.
   - Pass: actual approver meets or exceeds required level.
   - Fail: actual approver is below required level, OR the transaction is self-approved (approver equals requester).
   - Severity: high.

2. Preferred supplier:
   - Test: check if the transaction's supplier_id exists in preferred-suppliers.csv.
   - Pass: supplier_id found in preferred list.
   - Fail: supplier_id not found AND no approved exception documented.
   - Severity: medium.

3. Documentation completeness:
   - Test: for the transaction's contract_type, look up required documents in contract-documentation.csv. Check if all mandatory documents are present.
   - Pass: all mandatory documents present.
   - Fail: one or more mandatory documents missing.
   - Severity: medium.

4. Split order detection:
   - Test: find transactions from the same supplier within 5 business days where each transaction is below $5,000 but the combined total exceeds $5,000.
   - Pass: no matching pattern found.
   - Fail: matching pattern detected.
   - Severity: high.

5. Breach escalation:
   - Test: count total breaches across all rules. If count exceeds 15, trigger escalation.
   - Threshold: 15 breaches.
   - Escalation: notify VP of Procurement.
```

You should see CLAUDE.md updated with all five rules in testable format.

### Step 5. Verify the rules with a test case.

```
Test case: A transaction for $28,000 approved by a Manager (not a VP). The policy requires VP approval for $25,001-$100,000. Does this transaction pass or fail the approval authority rule? Explain your reasoning step by step.
```

You should see: Fail. The amount of $28,000 falls in the $25,001-$100,000 range. The required approver is VP. The actual approver is Manager, which is below VP. This is an approval authority breach with severity "high."

### Step 6. Verify the split order rule with a test case.

```
Test case: Supplier SUP005 has two transactions. Transaction A is $4,200 on 2026-03-10. Transaction B is $4,500 on 2026-03-12. Each is below $5,000, but combined they are $8,700. Are they within 5 business days? Does this trigger the split order rule?
```

You should see: Yes, 2026-03-10 to 2026-03-12 is 2 business days (within the 5-day window). Combined total of $8,700 exceeds $5,000. This triggers the split order detection rule with severity "high."

## Worked example

**Starting files:**
- `CLAUDE.md` with existing compliance rules.
- `data/policy-rules.json` (5 rules in JSON).
- `data/approval-matrix.csv` (5 authority levels).

**What you type:**

```
Read data/policy-rules.json and data/approval-matrix.csv. Then update CLAUDE.md to make every compliance rule testable with explicit pass/fail conditions, thresholds, and severity levels. Show me the updated rules section when done.
```

**What you should see:** CLAUDE.md with five fully defined rules, each showing the test logic, pass condition, fail condition, and severity.

**What Claude did, behind the scenes:**

1. Read data/policy-rules.json to get the rule definitions and thresholds.
2. Read data/approval-matrix.csv to get the authority tiers.
3. Read the existing CLAUDE.md to find the compliance rules section.
4. Rewrote each rule with explicit test conditions: what data to read, what comparison to make, what constitutes pass versus fail.
5. Added the self-approval check (approver equals requester) to the approval authority rule.
6. Saved the updated CLAUDE.md.

## Common mistakes and how to recover

- **Symptom:** The approval authority rule uses "greater than" instead of "greater than or equal to" for the threshold boundaries. **Fix:** The matrix uses inclusive boundaries. $5,001 is the start of the Director tier. A transaction at exactly $5,001 requires Director approval. Check that the boundaries do not have gaps or overlaps.

- **Symptom:** The self-approval condition is missing from the approval authority rule. **Fix:** Self-approval (where the approver is the same person as the requester) is a breach regardless of amount. Add "OR approver equals requester" to the fail condition.

- **Symptom:** The split order rule does not account for weekends. **Fix:** The window is 5 business days, not 5 calendar days. A transaction on Friday and the next on the following Wednesday is 3 business days (Monday, Tuesday, Wednesday), not 5 calendar days. The test must skip weekends.

- **Symptom:** The breach escalation threshold is applied per rule instead of across all rules. **Fix:** The escalation counts total breaches from all rules combined. 10 approval breaches plus 6 preferred supplier breaches equals 16 total, which exceeds the 15 threshold. The count must aggregate across rules.
