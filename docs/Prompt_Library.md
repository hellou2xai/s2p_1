# Prompt library

Reusable prompt patterns for course material. Every prompt in the course is built from one of these shapes.

## Rules for every prompt

Each prompt must be:

- Written in full sentences.
- Specific about input files and output file names.
- Explicit about what not to change.

Every new prompt added to the course must follow the same shape: name the inputs, name the output, name what stays untouched.

## Reference patterns

### Read-only review

```
Read Master_NDA_v4.docx and list every clause that mentions "data" or "personal information".
For each one, give the clause number, a one-line summary, and the page number. Do not edit the file.
```

### Single-file edit

```
In Supplier_Scorecard_Q1.xlsx, sheet "Scores", add a column called "Trend".
Fill it with "up", "flat", or "down" based on the change from column "Q4" to column "Q1".
Save as Supplier_Scorecard_Q1_v2.xlsx. Leave the original file untouched.
```

### Multi-file build

```
Using Contract_Live.docx and Renewal_Brief_Template.docx,
produce a renewal brief for the contract with Northwind Office Ltd.
Pull the contract value, end date, notice period, and auto-renewal clause from the live contract.
Drop them into the matching fields in the template.
Save the result as Renewal_Brief_Northwind_2026.docx in the "Renewals" folder.
```
