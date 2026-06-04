# Lesson 4: Demand Consolidation

**Time:** 35 minutes.

## Eight requests, three that are basically the same thing

It is 14:00 Thursday. You have processed eight stakeholder requirement submissions into clean specs at Atlas Manufacturing. Now you notice something: three of them are requesting the same type of industrial gasket with slightly different dimensions. Two more are requesting similar hydraulic fittings. If you source each one separately, you get five purchase orders to five suppliers at retail prices. If you consolidate them, you get two purchase orders at volume pricing. But spotting these overlaps manually across 12 spec records takes a careful eye and an hour of cross-referencing. Your category manager will not do it.

## What Claude Code is going to do for you

Claude Code reads the demand specifications from Lesson 3, groups them by specification similarity, calculates the combined volume for each group, and recommends which requests should be bundled into a single sourcing action. The output is a consolidation report showing how many purchase events you actually need versus how many requests you received.

## Set up

1. Claude Code installed and signed in.
2. A terminal open in `Course_17_Market_Intelligence/practice/`.
3. `Drafts/demand_specs.json` from Lesson 3.
4. `supplier-capabilities.csv` (20 suppliers).

## Step-by-step

### Group by similarity

**Step 1.** Start Claude Code in the practice folder.

```
claude
```

You should see the Claude Code prompt.

**Step 2.** Ask Claude to identify groupable specifications.

```
Read Drafts/demand_specs.json. Compare all spec records by item_description and technical_specs. Group specs that describe the same type of item (even if dimensions, quantities, or requesters differ). For each group, list: the spec_ids in the group, the common item type, and how the individual specs differ. Write to Drafts/demand_groups.json.
```

You should see Claude identify 4 to 6 groups. Some groups have one spec (unique items). Others have two or three related specs. Example: Group 1 contains SPEC-002, SPEC-005, SPEC-009, all requesting industrial gaskets with different diameters.

**Step 3.** Review the groupings.

```
Read Drafts/demand_groups.json. Show me a table with columns: group_id, item_type, spec_count, combined_quantity, unit_of_measure. Sort by spec_count descending.
```

You should see the groups ranked by how many specs they contain. Groups with more specs offer the most consolidation benefit.

### Calculate consolidation benefits

**Step 4.** Estimate the volume benefit of consolidation.

```
Read Drafts/demand_groups.json and Drafts/demand_specs.json. For each group with two or more specs, calculate: (1) total combined quantity, (2) number of distinct requesters (to show cross-departmental demand), (3) estimated volume discount: assume a 5% discount for orders over 500 units and a 10% discount for orders over 2,000 units. If quantity data is available from the specs, apply the discount percentage to estimate savings. Write to Drafts/consolidation_benefits.json.
```

You should see the benefits calculated for each consolidable group.

**Step 5.** Check supplier capabilities for consolidated volumes.

```
Read supplier-capabilities.csv and Drafts/demand_groups.json. For each group, identify which suppliers from supplier-capabilities.csv can fulfill the consolidated requirement (match by item type or category). List the capable suppliers and note if any can handle the full combined volume. Write to Drafts/group_supplier_match.json.
```

You should see each group matched to potential suppliers.

### Build the consolidation recommendation

**Step 6.** Generate the recommendation report.

```
Write Drafts/demand_consolidation_report.md with these sections:

1. Summary: total spec records received, number of consolidation groups identified, number of separate sourcing actions needed (one per group, not one per spec).

2. Consolidation Table: a table with group_id, item_type, spec_ids, combined_quantity, estimated_savings_pct, number_of_capable_suppliers.

3. Bundling Recommendations: for each group with two or more specs, a one-paragraph recommendation stating: what to bundle, the volume benefit, which suppliers can fulfill, and the recommended sourcing approach (competitive bid, catalog, or sole source based on supplier count).

4. Standalone Items: list any spec that did not group with others and explain why (unique item, one-time need, or insufficient volume for consolidation).

Use today's date.
```

You should see a complete report showing the consolidation opportunities.

**Step 7.** Create a sourcing action list.

```
Read Drafts/demand_consolidation_report.md. Create Drafts/sourcing_actions.csv with columns: action_id (ACT-001, etc.), action_type (competitive_bid, catalog_order, sole_source), item_type, combined_quantity, spec_ids, estimated_value, priority (from the highest-priority spec in the group), target_completion_date (from the earliest required_delivery_date in the group). Sort by priority descending, then by target_completion_date ascending.
```

You should see a CSV with one row per sourcing action, fewer rows than the original spec count.

**Step 8.** Exit Claude Code.

```
/quit
```

## Worked example

**Starting files:**

```
practice/
├── supplier-capabilities.csv (20 suppliers)
├── Drafts/
│   └── demand_specs.json (12 spec records)
```

**What you created:**

```
practice/
├── Drafts/
│   ├── demand_groups.json
│   ├── consolidation_benefits.json
│   ├── group_supplier_match.json
│   ├── demand_consolidation_report.md
│   └── sourcing_actions.csv
```

**What Claude did, behind the scenes:**

1. Claude read all 12 spec records and compared item_description fields using keyword similarity (e.g., "industrial gasket" matched across three specs despite different dimension values).
2. It grouped specs where the item type matched, creating consolidated demand groups.
3. It summed quantities within each group and applied volume discount tiers.
4. It cross-referenced each group's item type against the capability descriptions in `supplier-capabilities.csv`.
5. It determined the sourcing approach: competitive bid if three or more suppliers are capable, sole source if only one, catalog if the item is a standard commodity.
6. It carried forward the highest priority and earliest delivery date from the individual specs to the group level.

## Common mistakes and how to recover

- **Symptom:** Claude groups unrelated items because their descriptions share common words (e.g., "steel gasket" and "steel bracket" grouped together). **Fix:** ask Claude to "Group only by the primary item noun (gasket, bracket, fitting, seal), not by material or adjective. Steel gaskets and steel brackets are different item types."

- **Symptom:** The combined quantity uses mixed units (some specs in kg, others in units). **Fix:** add a rule: "Only combine specs where the unit_of_measure is the same. If units differ, flag the group as 'mixed units, manual review required.'"

- **Symptom:** The estimated savings percentage is applied to specs with no price data. **Fix:** the savings estimate requires a baseline price. If no price exists in the specs, write "Savings estimate not available. Baseline price needed." Do not fabricate a number.

- **Symptom:** Every spec ends up in its own group because descriptions are too different. **Fix:** ask Claude to "Use broader category matching. Group by the general item category (gaskets, fittings, fasteners, seals) before comparing specific descriptions. Two specs for 'Viton O-ring 2-inch' and 'Viton O-ring 3-inch' should be in the same group."
