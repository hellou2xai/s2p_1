# Lesson 02: Requisition Compliance Screening: Checking Every Requisition Against the Approval Matrix

**Estimated time:** 55 minutes
**Role:** P2P Analytics Lead, Meridian Corp
**Tool:** Claude Code (in the terminal)
**Prerequisite:** Complete Lesson 01 first. You need the data architecture from that lesson to understand the file structure.

---

## Part 1: The S2P Problem

It is 09:15 Tuesday. Your internal audit lead emails you with one line: "REQ-0347 was approved by a department manager. The value was $78,000. That is three levels below what the policy allows." The purchase went through, the PO was issued, and the goods arrived. Nobody caught it until audit sampled the data. You need to know how many other requisitions have the same problem: the wrong approver level, a non-preferred supplier used when a preferred one exists, or a buying channel that was bypassed. Meridian Corp processes 500 requisitions per quarter. Checking each one by hand against the approval matrix takes a full day. Claude Code screens all 500 in minutes and gives audit a ranked exception list to work from.

---

## Part 2: What Claude Code Is Going to Do for You

Claude Code will read every requisition, cross-reference each one against the approval matrix (five levels, from Analyst at $5,000 to CFO with no limit), and flag every case where the approver's authority was below the requisition value. It will also check each requisition against the preferred supplier list. The output is a compliance report with every violation named, the dollar amount at risk, and the requester responsible. You hand that report to audit, not a pile of spreadsheets to sort by hand.

---

## Part 3: Set Up

1. Claude Code is installed and you are signed in.
2. The project folder `Course_15_Purchase_To_Pay_Intelligence/` is open in your terminal.
3. These files are in `practice/`:
   - `requisitions.csv` (500 rows)
   - `approval-matrix.csv` (5 rows, one per approval level)
   - `preferred-suppliers.csv` (20 rows)
4. `Drafts/` exists inside the project folder. If it does not, create it by running `mkdir Drafts` in the terminal before starting Claude Code.
5. OneDrive sync is paused.

---

## Part 4: Step-by-Step

**Step 1.** Open your terminal in the project folder and start Claude Code.

```
cd "Course_15_Purchase_To_Pay_Intelligence"
claude
```

You should see the Claude Code prompt with the folder name at the top.

**Step 2.** Set the read-only rule and tell Claude where to save output.

```
The folder Master/ holds the source reference files. Do not edit any file in Master/.
Read from practice/ freely. Save all output to Drafts/ unless I tell you otherwise.
```

You should see Claude Code confirm it understands. Nothing changes on disk at this step.

**Step 3.** Read the approval matrix and confirm the five authority levels.

```
Read practice/approval-matrix.csv. Show me the approval authority levels as a table:
Role, Approval_Limit_USD. Include all five levels.
```

You should see a table like this:

```
Role        Approval_Limit_USD
Analyst     5,000
Manager     25,000
Director    100,000
VP          500,000
CFO         Unlimited
```

If the table has fewer than five rows: ask Claude to "Show me all rows in practice/approval-matrix.csv, including any rows with a null or blank limit value."

**Step 4.** Read the preferred supplier list and confirm the categories covered.

```
Read practice/preferred-suppliers.csv. How many preferred suppliers are listed?
What categories do they cover? List each category with its supplier count.
```

You should see a count of 20 preferred suppliers and a category breakdown. This tells you which categories have a preferred supplier that requisitions must use.

**Step 5.** Screen all 500 requisitions for approval authority violations.

```
Read practice/requisitions.csv and practice/approval-matrix.csv.
For each requisition, check whether the approver's role has sufficient authority
for the requisition's amount. Flag every requisition where the approver's dollar limit
is below the requisition value. Write the results to Drafts/approval_violations.csv
with columns: REQ_ID, REQ_DATE, REQUESTER, DEPT, AMOUNT, APPROVER, APPROVER_ROLE,
APPROVER_LIMIT, OVERAGE_USD. Sort by OVERAGE_USD descending.
```

You should see Claude process all 500 rows and write the file. The terminal will print how many violations were found. Expect approximately 25 violations based on the 5% violation rate in this dataset.

If Claude says the APPROVER_ROLE values in `requisitions.csv` do not match the role names in `approval-matrix.csv`: ask it to "List all unique values in the APPROVER_ROLE column of requisitions.csv and all role names in approval-matrix.csv. Map them to each other, then rerun the check using the mapped values."

**Step 6.** Screen all requisitions for preferred supplier compliance.

```
Read practice/requisitions.csv and practice/preferred-suppliers.csv.
For each requisition, check whether the supplier used is on the preferred supplier list
for that category. Flag any requisition that used a non-preferred supplier when a
preferred supplier exists for that category.
Write to Drafts/supplier_violations.csv with columns: REQ_ID, DEPT, CATEGORY,
SUPPLIER_USED, PREFERRED_SUPPLIER, AMOUNT.
Sort by AMOUNT descending.
```

You should see the file created with all supplier violations listed. Note: if no preferred supplier exists for a category, that purchase is not a violation. Claude will exclude those automatically.

**Step 7.** Combine both violation types into a single ranked report.

```
Read Drafts/approval_violations.csv and Drafts/supplier_violations.csv.
Create Drafts/Requisition_Compliance_Report.csv combining both violation types.
Add a column VIOLATION_TYPE with value "Approval_Authority" or "Non_Preferred_Supplier".
Add a column SEVERITY: "High" if AMOUNT is above $50,000, "Medium" if $10,000 to $50,000,
"Low" if below $10,000.
Sort by SEVERITY (High first), then by AMOUNT descending.
```

You should see one consolidated CSV with all violations ranked by severity and dollar value.

**Step 8.** Ask Claude to write the compliance summary for the CFO review package.

```
Read Drafts/Requisition_Compliance_Report.csv. Write a compliance summary to
Drafts/Requisition_Compliance_Summary.txt with these exact sections:
1. Report date: 2026-04-25. Total requisitions reviewed: 500.
2. Total violations found: [count] ([percentage]% of all requisitions).
3. Total dollar value of non-compliant requisitions: $[amount].
4. Breakdown by violation type: Approval_Authority ([count], $[value]),
   Non_Preferred_Supplier ([count], $[value]).
5. Top three departments by violation count.
Every figure must be a specific number. No estimates.
```

You should see the file saved to `Drafts/`. Open it to confirm all five sections are present with real numbers.

**Step 9.** Exit Claude Code.

```
/quit
```

You should see the terminal return to its normal command prompt.

---

## Part 5: Worked Example, End to End

**Starting files:**

```
Course_15_Purchase_To_Pay_Intelligence/
├── Master/          (read-only reference)
├── Drafts/          (output goes here)
└── practice/
    ├── requisitions.csv        (500 rows)
    ├── approval-matrix.csv     (5 rows)
    └── preferred-suppliers.csv (20 rows)
```

**Prompt 1:** read-only rule (same as Step 2 above).

**Prompt 2:** the screening prompt from Step 5.
```
Read practice/requisitions.csv and practice/approval-matrix.csv.
For each requisition, check whether the approver's role has sufficient authority
for the requisition's amount. Flag every requisition where the approver's dollar limit
is below the requisition value. Write the results to Drafts/approval_violations.csv
with columns: REQ_ID, REQ_DATE, REQUESTER, DEPT, AMOUNT, APPROVER, APPROVER_ROLE,
APPROVER_LIMIT, OVERAGE_USD. Sort by OVERAGE_USD descending.
```

**What you should see** when this succeeds: Claude prints "Found 25 approval authority violations. Saved to Drafts/approval_violations.csv." (The exact count depends on your practice data.)

**Sample rows from `Drafts/approval_violations.csv`:**

```
REQ_ID,   REQ_DATE,   REQUESTER,       DEPT,       AMOUNT,   APPROVER,       APPROVER_ROLE, APPROVER_LIMIT, OVERAGE_USD
REQ-0347, 2026-03-12, D. Holloway,     Operations, 78000,    T. Renshaw,     Manager,       25000,          53000
REQ-0219, 2026-02-28, A. Fontaine,     IT,         62500,    S. Obi,         Manager,       25000,          37500
REQ-0412, 2026-04-01, R. Tanaka,       Facilities, 44000,    M. Castillo,    Manager,       25000,          19000
```

**What Claude Code did, behind the scenes:**

1. Claude Code read `approval-matrix.csv` and built an internal lookup table: each role name mapped to its dollar limit.
2. It read all 500 rows of `requisitions.csv` and for each row extracted the APPROVER_ROLE and AMOUNT fields.
3. It looked up the approver's limit from the lookup table built in step 1.
4. It compared the AMOUNT to the APPROVER_LIMIT. If AMOUNT was greater, it calculated OVERAGE_USD as the difference.
5. It collected all rows where OVERAGE_USD was greater than zero into a violations list.
6. It sorted the list by OVERAGE_USD descending so the largest violations appeared first.
7. It wrote the results to `Drafts/approval_violations.csv` and reported the count in the terminal.

**Finished artifacts:**
- `Drafts/approval_violations.csv`: all approval authority violations, sorted by overage.
- `Drafts/supplier_violations.csv`: all non-preferred supplier violations, sorted by amount.
- `Drafts/Requisition_Compliance_Report.csv`: combined, ranked report with severity flags.
- `Drafts/Requisition_Compliance_Summary.txt`: the four-section briefing note for the CFO package.

---

## Part 6: Common Mistakes and How to Recover

- **Symptom:** The approval violation count is zero, but you know REQ-0347 should be flagged. **Fix:** the APPROVER_ROLE values in `requisitions.csv` may use different names than the roles in `approval-matrix.csv` (for example, "Dept Manager" vs. "Manager"). Ask Claude: "List all unique values in APPROVER_ROLE in requisitions.csv and all role names in approval-matrix.csv. Show me which ones do not match." Then ask it to map them and rerun.

- **Symptom:** The preferred supplier check flags purchases in a category where no preferred supplier exists. **Fix:** ask Claude: "Before flagging a requisition for using a non-preferred supplier, confirm that practice/preferred-suppliers.csv contains at least one supplier for that category. If no preferred supplier exists for the category, do not flag the requisition."

- **Symptom:** Some requisitions appear in both the approval violation list and the supplier violation list, inflating the total count. **Fix:** the combined report should count unique REQ_IDs, not total violation rows. Ask Claude: "In Drafts/Requisition_Compliance_Summary.txt, count the number of unique REQ_IDs in Drafts/Requisition_Compliance_Report.csv, not the total row count."

- **Symptom:** The compliance summary shows "significant" or "several" instead of a specific number. **Fix:** ask Claude: "Replace every vague word in Drafts/Requisition_Compliance_Summary.txt with the exact number from the data. No approximations."

- **Symptom:** `Drafts/Requisition_Compliance_Report.csv` opens in Excel but the AMOUNT column shows text instead of numbers. **Fix:** ask Claude: "Ensure the AMOUNT, APPROVER_LIMIT, and OVERAGE_USD columns in Drafts/Requisition_Compliance_Report.csv are formatted as plain numbers without currency symbols or commas, so Excel reads them as numeric."
