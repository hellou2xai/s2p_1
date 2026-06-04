# Lesson 02: Onboarding Automation

**Course:** Course 14, Supplier Lifecycle Management
**Role:** Supplier Relationship Manager, Crestview Industries
**Duration:** 50 minutes

---

## Part 1. The S2P Problem

It is 09:00 Tuesday. Summit Electrical has been in onboarding for three weeks. Purchasing wants to start placing orders, but you have not confirmed that all compliance documents are in. Your onboarding checklist lives in a Word file. Compliance-status.csv has partial data. Checking each field against the checklist, noting what is missing, writing a follow-up email to the supplier, and updating the status file by hand takes about 90 minutes per supplier. Crestview has two more suppliers entering onboarding next month.

---

## Part 2. What Claude Code Is Going to Do for You

Claude Code will read your compliance-status.csv and your onboarding checklist template, identify every missing or expired item for Summit Electrical, generate a follow-up email ready for you to send, and update the supplier's status record in Drafts. You confirm the email wording, send it, and move on. The whole process takes about 12 minutes.

---

## Part 3. Set Up

1. Claude Code installed and signed in. See Lesson 01 for folder setup steps.
2. The project folder `Supplier_Lifecycle_2026/` already set up from Lesson 01, with `Master/`, `Drafts/`, and `Outputs/` subfolders.
3. The following files in `Master/`:
   - `compliance-status.csv` (30 rows, one per supplier, fields for W-9, insurance certificate, NDA, and onboarding checklist completion date)
   - `Onboarding_Checklist_Template.docx` (the standard 12-item checklist Crestview uses for all new suppliers)
4. `Drafts/Supplier_Segmentation_v1.csv` from Lesson 01 already present.
5. OneDrive sync paused. Resume when done.

---

## Part 4. Step-by-Step

**Step 1.** Open Claude Code in the project folder.

```
cd "Supplier_Lifecycle_2026"
claude
```

You should see the Claude Code prompt showing `Supplier_Lifecycle_2026` as the working folder.

**Step 2.** State the read-only rule for Master/.

```
The folder Master/ holds the source data files and templates. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

Claude should confirm. Nothing changes on disk.

**Step 3.** Ask Claude to read the compliance status for Summit Electrical.

```
Read Master/compliance-status.csv. Find the row for Summit Electrical.
List every compliance field and its current value.
Tell me which fields are blank, expired, or show a value other than "Complete" or "Received".
```

You should see a list of Summit Electrical's compliance fields and a clear list of gaps. If Summit Electrical does not appear, check the spelling in compliance-status.csv: the name must match exactly, including capitalization.

**Step 4.** Ask Claude to read the onboarding checklist template and compare it to Summit Electrical's status.

```
Read Master/Onboarding_Checklist_Template.docx.
Compare every checklist item against the compliance fields you just read for Summit Electrical.
Produce a two-column table: Checklist Item, Status (Complete, Missing, or Expired).
Save the table as Drafts/Summit_Electrical_Checklist_v1.txt.
```

You should see the table printed in the terminal and a confirmation that `Drafts/Summit_Electrical_Checklist_v1.txt` was saved. If the Word file cannot be read, check that it is saved in .docx format, not the older .doc format.

**Step 5.** Ask Claude to draft a follow-up email to the supplier.

```
Using Drafts/Summit_Electrical_Checklist_v1.txt, write a professional email to Summit Electrical.
The email should:
- State that Crestview is ready to move them to Active status once outstanding items are received.
- List only the missing or expired items, not the complete ones.
- Give a deadline of 2026-05-02 for submission.
- Be addressed to their onboarding contact (use [Onboarding Contact Name] as a placeholder).
- Be signed from me as Supplier Relationship Manager, Crestview Industries.
Save the email as Drafts/Summit_Electrical_Followup_Email_v1.txt.
```

You should see the email text in the terminal and confirmation the file was saved. Read the email before sending. Replace [Onboarding Contact Name] with the actual contact.

**Step 6.** Ask Claude to update the status record for Summit Electrical.

```
Read Drafts/Supplier_Segmentation_v1.csv.
Find the row for Summit Electrical.
Update the Reason field to:
"Follow-up sent 2026-04-25. Outstanding items: [list the missing items from Step 3]. Deadline 2026-05-02."
Save the updated file as Drafts/Supplier_Segmentation_v2.csv.
Do not change any other rows.
```

You should see a confirmation that `Drafts/Supplier_Segmentation_v2.csv` was saved. Open it and verify that only Summit Electrical's row has changed.

---

## Part 5. Worked Example, End to End

**Starting files:**

- `Master/compliance-status.csv`: 30 rows. Summit Electrical row shows W-9 received, NDA received, insurance certificate blank, onboarding checklist completion date blank.
- `Master/Onboarding_Checklist_Template.docx`: 12-item checklist. Items include W-9, NDA, Certificate of Insurance (COI), ACH banking form, supplier code of conduct acknowledgment, and quality agreement signature.

**Prompts used, in order:**

```
The folder Master/ holds the source data files and templates. Do not edit any file in Master/.
Read from it freely. Save all output to Drafts/ unless I tell you otherwise.
```

```
Read Master/compliance-status.csv. Find the row for Summit Electrical.
List every compliance field and its current value.
Tell me which fields are blank, expired, or show a value other than "Complete" or "Received".
```

```
Read Master/Onboarding_Checklist_Template.docx.
Compare every checklist item against the compliance fields for Summit Electrical.
Produce a two-column table: Checklist Item, Status.
Save as Drafts/Summit_Electrical_Checklist_v1.txt.
```

```
Using Drafts/Summit_Electrical_Checklist_v1.txt, write a professional email to Summit Electrical.
List only missing or expired items. Deadline 2026-05-02.
Address to [Onboarding Contact Name]. Sign from me as Supplier Relationship Manager, Crestview Industries.
Save as Drafts/Summit_Electrical_Followup_Email_v1.txt.
```

**Extract of output (email draft):**

```
Subject: Crestview Industries Onboarding: Outstanding Documents Required by 2026-05-02

Dear [Onboarding Contact Name],

Thank you for your cooperation during the onboarding process. Crestview Industries is ready
to move Summit Electrical to Active status and begin placing orders as soon as the following
items are received:

1. Certificate of Insurance (COI): not yet on file
2. Onboarding checklist: completion date not recorded

Please submit both documents by 2026-05-02. Send them to supplier.onboarding@crestview.com.

Best regards,
[Your Name]
Supplier Relationship Manager, Crestview Industries
```

**Finished artifacts:**
- `Drafts/Summit_Electrical_Checklist_v1.txt`: 12-row checklist with status for each item.
- `Drafts/Summit_Electrical_Followup_Email_v1.txt`: ready-to-send email with two action items.
- `Drafts/Supplier_Segmentation_v2.csv`: updated with follow-up details for Summit Electrical.

---

## Part 6. Common Mistakes and How to Recover

- **Symptom:** Claude cannot read Onboarding_Checklist_Template.docx and returns an error. **Fix:** Confirm the file is in .docx format, not the older .doc format. Open it in Word, choose Save As, and select .docx. Then rerun the step.

- **Symptom:** The checklist table shows all items as "Complete" even though you know some are missing. **Fix:** The compliance-status.csv column headers may not match what Claude expected. Ask: "List the exact column names in Master/compliance-status.csv." Then restate your prompt using the exact column names from that output.

- **Symptom:** Claude updated more than one row when you asked it to update only Summit Electrical. **Fix:** Open Drafts/Supplier_Segmentation_v2.csv and check. If other rows changed, ask Claude: "Re-read Drafts/Supplier_Segmentation_v1.csv and Drafts/Supplier_Segmentation_v2.csv side by side. List every row that is different between the two files." Restore from v1 and rerun with a more specific prompt: "Update only the row where Supplier_Name equals exactly 'Summit Electrical'."

- **Symptom:** The email draft includes complete items in the missing-items list. **Fix:** Ask Claude to re-read Drafts/Summit_Electrical_Checklist_v1.txt and list only the rows where Status is Missing or Expired. Use that list to rewrite the email.

- **Symptom:** The follow-up email saved with garbled formatting in the .txt file. **Fix:** Ask Claude to re-save as a plain UTF-8 text file with line breaks between sections. Open in Notepad to verify before copying into Outlook.

- **Symptom:** Drafts/Supplier_Segmentation_v2.csv shows 29 rows instead of 30. **Fix:** Claude may have dropped the header row during the update. Ask: "Re-read Drafts/Supplier_Segmentation_v1.csv and confirm how many data rows it has. Then re-save v2 making sure all rows are preserved, including the header."
