# Lesson 3: Requirements Processing

**Time:** 35 minutes.

## The requirement that arrived as a voicemail transcript

It is 11:00 Wednesday. Your demand-intake folder at Atlas Manufacturing has eight new requirement submissions from stakeholders across the business. One is a structured form from engineering with part numbers and specs. Another is a three-paragraph email from the plant manager that says "we need more of those blue gaskets, the ones from last year, but bigger." A third is a voicemail transcript that mentions a quantity but no part number. You cannot run a sourcing event against this mix of formats. You need clean procurement specifications: item description, quantity, unit of measure, required delivery date, technical specifications, and budget reference.

## What Claude Code is going to do for you

Claude Code reads each unstructured stakeholder submission, extracts the procurement-relevant fields, flags missing information, and writes clean specification records. You get a standardized intake register instead of a pile of emails and transcripts.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_17_Market_Intelligence/practice/`.
3. `demand-intake/` folder containing 8 requirement files.

## Step-by-step

### Review the raw submissions

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** List and categorize the intake files.

```
List all files in demand-intake/. For each file, read the first 20 lines and classify the format: structured_form, email, memo, transcript, or other. Show the file name and format in a table.
```

You should see eight files with a mix of formats: some structured, some freeform.

**Step 3.** Read the most unstructured submission.

```
Read the file from demand-intake/ that you classified as "transcript" or "email" (whichever is least structured). Show me the full content and identify: what is the requester asking for, what information is present, and what is missing?
```

You should see the raw text and Claude's analysis of what can be extracted versus what is missing.

### Define the specification format

**Step 4.** Create a standard specification template.

```
Append to CLAUDE.md a section called "## Demand Specification Format" with these required fields:

- spec_id: auto-incrementing (SPEC-001, SPEC-002, etc.)
- source_file: the intake file name
- requester_name: who submitted the requirement
- requester_department: which department or plant
- item_description: clear, specific description of what is needed
- quantity: numeric amount
- unit_of_measure: each, kg, meters, liters, etc.
- required_delivery_date: when it is needed (YYYY-MM-DD)
- technical_specs: any dimensions, materials, tolerances, standards mentioned
- budget_reference: cost center, project code, or budget line if provided
- priority: high, medium, or low (based on delivery urgency)
- completeness: "complete" if all required fields are present, "incomplete" with a list of missing fields
```

You should see Claude append the specification format.

### Process all submissions

**Step 5.** Extract specifications from all eight files.

```
Read every file in demand-intake/. For each file, extract one or more demand specifications using the Demand Specification Format from CLAUDE.md. If a file contains multiple distinct requirements, create a separate spec record for each. For any field that cannot be determined from the submission, write "[MISSING: <field_name>]" and set completeness to "incomplete." Write all specs to Drafts/demand_specs.json.
```

You should see Claude process all eight files and write the specs. Expect 10 to 14 spec records (some files may contain more than one requirement). Several should be incomplete.

**Step 6.** Get the completeness summary.

```
Read Drafts/demand_specs.json. Tell me: (1) total spec records, (2) how many are complete, (3) how many are incomplete, (4) for the incomplete records, which fields are most commonly missing. Show as a table of field_name and missing_count.
```

You should see a summary. Example: 12 specs total, 5 complete, 7 incomplete. Most commonly missing: technical_specs (5), required_delivery_date (4), budget_reference (6).

### Generate follow-up requests

**Step 7.** Draft follow-up messages for incomplete submissions.

```
Read Drafts/demand_specs.json. For each incomplete spec, draft a follow-up message to the requester asking for the specific missing fields. Write all follow-ups to Drafts/demand_followups.md. Each follow-up should include: the requester name, the item description, and a numbered list of the exact fields needed. Keep each follow-up to five lines or fewer.
```

You should see concise follow-up messages for each incomplete requirement.

**Step 8.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── demand-intake/
│   ├── engineering_request_042.md
│   ├── plant_manager_email.md
│   ├── voicemail_transcript_apr15.md
│   ├── ... (5 more files)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── demand_specs.json (10-14 spec records)
│   └── demand_followups.md
├── CLAUDE.md (updated with Demand Specification Format)
```

**What Claude did, behind the scenes:**

1. Claude read each intake file and determined its format (structured form, email, memo, transcript).
2. For structured forms, it mapped form fields directly to specification fields.
3. For unstructured text (emails, transcripts), it used natural language understanding to identify the item, quantity, timing, and technical details.
4. It flagged ambiguous descriptions (e.g., "those blue gaskets from last year") as needing clarification and set technical_specs to "[MISSING: technical_specs]."
5. It assigned priority based on language cues: words like "urgent," "ASAP," or "shutdown risk" got "high"; specific future dates got "medium"; no urgency language got "low."
6. It compiled the completeness report by counting missing fields across all records.

## Common mistakes and how to recover

- **Symptom:** Claude creates one spec record per file, even when a file contains three separate items. **Fix:** add to your prompt: "If a submission mentions multiple distinct items, create a separate spec record for each item. A request for 'gaskets, o-rings, and seals' should produce three spec records."

- **Symptom:** The item_description is too vague ("parts as discussed"). **Fix:** Claude cannot invent details. Set completeness to "incomplete" and add "[MISSING: specific item description]." The follow-up message will ask the requester to clarify.

- **Symptom:** Quantities are extracted incorrectly from text like "a couple hundred." **Fix:** ask Claude to "Convert informal quantities to specific numbers with a note. 'A couple hundred' becomes quantity: 200 with a note: 'Estimated from informal language. Confirm exact quantity with requester.'"

- **Symptom:** All priorities are set to "medium" because Claude defaults conservatively. **Fix:** provide specific rules: "Set priority to high if the delivery date is within 14 days, or if the text contains words like urgent, critical, ASAP, or shutdown. Set to low if the delivery date is more than 60 days out and no urgency language is present."
