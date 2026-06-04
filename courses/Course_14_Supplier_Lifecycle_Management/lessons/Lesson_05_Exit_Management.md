# Lesson 05: Exit Management

**Course:** Course 14, Supplier Lifecycle Management
**Role:** Supplier Relationship Manager, Crestview Industries
**Duration:** 50 minutes

---

## Part 1. The S2P Problem

It is 09:00 Friday. Regional Supply Co was flagged for exit two months ago after a decision to consolidate the MRO Supplies category under a preferred supplier. The off-boarding flag is set in your system, but three purchase orders totaling $48,000 are still active. No one has built a transition plan. The replacement supplier starts delivering in six weeks. If the open orders are not wound down correctly, Crestview will have duplicate deliveries, invoicing disputes, and a supplier contact who does not know they are being replaced. Doing this by hand, writing the transition plan, tracking the orders, and drafting the supplier notification, takes most of a day.

---

## Part 2. What Claude Code Is Going to Do for You

Claude Code will read the supplier record and open order data for Regional Supply Co, identify every active order with its value and delivery date, draft a transition timeline with seven dated milestones, and produce a supplier exit notification letter ready for you to review and send. The whole process takes about 15 minutes.

---

## Part 3. Set Up

1. Claude Code installed and signed in. Project folder `Supplier_Lifecycle_2026/` already set up from Lesson 01.
2. The following files in `Master/`:
   - `supplier-master.csv` (30 rows, includes exit flag and off-boarding date for Regional Supply Co)
   - `open-orders.csv` (active purchase orders, with columns for supplier name, PO number, amount, delivery date, and status)
3. `Drafts/Supplier_Segmentation_v3.csv` from Lesson 04 already present.
4. OneDrive sync paused.

---

## Part 4. Step-by-Step

**Step 1.** Open Claude Code in the project folder.

```
cd "Supplier_Lifecycle_2026"
claude
```

You should see the Claude Code prompt showing `Supplier_Lifecycle_2026` as the working folder.

**Step 2.** State the read-only rule.

```
The folder Master/ holds the source data files and templates. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

Claude should confirm. Nothing changes on disk.

**Step 3.** Pull Regional Supply Co's current record.

```
Read Master/supplier-master.csv.
Find the row for Regional Supply Co.
Show all columns and their values.
```

You should see every field for Regional Supply Co, including the exit flag and off-boarding date.

**Step 4.** Find all active orders for Regional Supply Co.

```
Read Master/open-orders.csv.
Find all rows where Supplier_Name is Regional Supply Co and Status is not Closed or Cancelled.
Show: PO_Number, Amount_USD, Delivery_Date, Status.
Calculate the total value of open orders.
```

You should see a list of open POs and a total. If Claude returns zero results, ask: "What are the unique values in the Status column of Master/open-orders.csv?" Then restate with the exact status labels from the file.

**Step 5.** Build a transition timeline.

```
Today is 2026-04-25. Regional Supply Co exit date is 2026-05-15.
The replacement supplier begins delivery on 2026-06-06.

Build a transition timeline with these milestones:
1. Send exit notification to Regional Supply Co: 2026-04-25
2. Freeze new PO creation for Regional Supply Co: 2026-04-28
3. Confirm delivery dates for all open POs: 2026-04-30
4. Final delivery from Regional Supply Co: on or before 2026-05-15
5. Final invoice receipt deadline: 2026-05-22
6. Supplier account closed in ERP: 2026-05-29
7. Replacement supplier first delivery: 2026-06-06

List each milestone as: Date, Action, Owner. Use [Owner Name] as a placeholder for Owner.
Save as Drafts/Regional_Supply_Co_Transition_Timeline_v1.txt.
```

You should see the timeline printed and a confirmation the file was saved.

**Step 6.** Draft the exit notification letter.

```
Draft a formal supplier exit notification letter for Regional Supply Co.
The letter must include:
- A statement that Crestview will not issue new purchase orders after 2026-04-28.
- A list of the open POs with their delivery dates and amounts. Use the data from Step 4.
- A request to confirm delivery on or before 2026-05-15.
- Final invoice submission deadline: 2026-05-22.
- Contact for invoice queries: ap@crestview.com.
- A statement that this decision reflects a category consolidation, not a performance issue.
- Signed from: Supplier Relationship Manager, Crestview Industries.
- Date: 2026-04-25.
Save as Drafts/Regional_Supply_Co_Exit_Letter_v1.docx.
```

You should see a confirmation that `Drafts/Regional_Supply_Co_Exit_Letter_v1.docx` was saved. Open the file in Word, add the actual signer name, and verify PO details before sending.

**Step 7.** Update the segmentation file.

```
Read Drafts/Supplier_Segmentation_v3.csv.
Find the row for Regional Supply Co.
Update the Reason field to:
"Exit letter sent 2026-04-25. Open POs total $48,000. Final delivery due 2026-05-15. Account closure due 2026-05-29."
Save as Drafts/Supplier_Segmentation_v4.csv. Do not change any other rows.
```

You should see a confirmation that v4 was saved. Open it and verify that only the Regional Supply Co row changed.

---

## Part 5. Worked Example, End to End

**Starting files:**

- `Master/supplier-master.csv`: Regional Supply Co row shows Exit_Flag = Yes, Off_Boarding_Date = 2026-05-15, Category = MRO Supplies, Annual_Spend_USD = 280,000.
- `Master/open-orders.csv`: Three open POs for Regional Supply Co. PO-4412 for $18,000 with delivery 2026-05-02. PO-4487 for $22,000 with delivery 2026-05-10. PO-4501 for $8,000 with delivery 2026-05-14. Total: $48,000.

**Prompts used, in order:**

```
Read Master/supplier-master.csv. Find the row for Regional Supply Co. Show all columns.
```

```
Read Master/open-orders.csv.
Find all rows where Supplier_Name is Regional Supply Co and Status is not Closed or Cancelled.
Show PO_Number, Amount_USD, Delivery_Date, Status. Calculate the total.
```

```
Build a transition timeline for Regional Supply Co.
Exit date 2026-05-15. Replacement supplier starts 2026-06-06.
Seven milestones with these dates: 2026-04-25, 2026-04-28, 2026-04-30, 2026-05-15, 2026-05-22, 2026-05-29, 2026-06-06.
Use [Owner Name] for Owner. Save as Drafts/Regional_Supply_Co_Transition_Timeline_v1.txt.
```

```
Draft a formal exit notification letter for Regional Supply Co.
Include: no new POs after 2026-04-28, list of three open POs from Step 4, delivery by 2026-05-15,
final invoice by 2026-05-22, contact ap@crestview.com, category consolidation context.
Sign from Supplier Relationship Manager, Crestview Industries. Date 2026-04-25.
Save as Drafts/Regional_Supply_Co_Exit_Letter_v1.docx.
```

**Extract of output (transition timeline):**

```
Regional Supply Co: Exit Transition Timeline

2026-04-25  Send exit notification letter                              [Owner Name]
2026-04-28  Freeze new PO creation in ERP                             [Owner Name]
2026-04-30  Confirm delivery dates for PO-4412, PO-4487, PO-4501     [Owner Name]
2026-05-15  Final delivery from Regional Supply Co                    [Owner Name]
2026-05-22  Final invoice receipt deadline                            [Owner Name]
2026-05-29  Close supplier account in ERP                             [Owner Name]
2026-06-06  Replacement supplier first delivery                       [Owner Name]
```

**Finished artifacts:**
- `Drafts/Regional_Supply_Co_Transition_Timeline_v1.txt`: seven-milestone transition timeline.
- `Drafts/Regional_Supply_Co_Exit_Letter_v1.docx`: formal exit letter listing all open POs and deadlines.
- `Drafts/Supplier_Segmentation_v4.csv`: updated with exit letter sent date and total open PO value.

---

## Part 6. Common Mistakes and How to Recover

- **Symptom:** Claude finds no open orders for Regional Supply Co. **Fix:** Ask Claude: "List the unique values in the Supplier_Name column of Master/open-orders.csv." The name may be stored as "Regional Supply" or "Regional Supply Company" rather than "Regional Supply Co". Adjust your prompt to use the exact name from the file.

- **Symptom:** The exit letter lists incorrect PO amounts. **Fix:** Ask Claude: "Re-read Master/open-orders.csv and show me the raw rows for Regional Supply Co." If amounts have dollar signs or commas in the CSV, Claude may have read them as text. Ask Claude to "treat the Amount_USD column as a plain number, removing any $ or comma characters."

- **Symptom:** The transition timeline dates are out of order in the saved file. **Fix:** You may not have specified all dates explicitly. Rerun Step 5 with all seven dates stated in the prompt, as shown above.

- **Symptom:** The Word exit letter will not open in Word. **Fix:** Ask Claude to re-save as a clean .docx: "Re-save Drafts/Regional_Supply_Co_Exit_Letter_v1.docx as a Word document compatible with Word 2016." If it still will not open, ask Claude to save as .txt instead and paste the content manually into a Word template.

- **Symptom:** The segmentation file shows the wrong total in the Reason field for Regional Supply Co. **Fix:** Ask Claude: "What was the total value of open POs for Regional Supply Co from Master/open-orders.csv?" Confirm the number, then ask Claude to update the Reason field with the correct figure and save as v4 again.

- **Symptom:** Claude updated the wrong supplier's row in Supplier_Segmentation_v4.csv. **Fix:** Ask Claude: "Which rows in Drafts/Supplier_Segmentation_v4.csv are different from Drafts/Supplier_Segmentation_v3.csv?" If more than one row changed, restore from v3 and restate: "Update only the row where Supplier_Name equals exactly 'Regional Supply Co'."
