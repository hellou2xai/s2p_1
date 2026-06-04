# Escalation Policy

## Scenario 1: Hook failure

**Trigger**: A hook (audit, review gate, or notification) fails or produces an error.

**Steps**:
1. Analyst stops work and notes the error message.
2. Analyst notifies the Operations Manager via Teams with the error and the file that triggered it.
3. Operations Manager investigates within 2 hours.
4. If the hook cannot be fixed within 4 hours, Operations Manager grants a temporary bypass and logs it in the audit trail.

**Owner**: Operations Manager.

## Scenario 2: Shared resource conflict

**Trigger**: Two analysts need conflicting changes to a shared file (e.g., different scoring weights for the same category).

**Steps**:
1. Both analysts document their requirements in a shared Teams thread.
2. Operations Manager reviews both requests within 1 business day.
3. Decision options: (a) accept one request, (b) merge both, (c) escalate to Director.
4. Operations Manager updates the shared file and notifies all analysts.

**Owner**: Operations Manager, escalation to Director of Procurement.

## Scenario 3: Output quality dispute

**Trigger**: An analyst disagrees with a Claude Code output and the review gate blocks their correction.

**Steps**:
1. Analyst documents the issue: what the output said, what it should say, and why.
2. Analyst adds the `[REVIEWED]` tag with a note: `[REVIEWED - manual override, see issue #NNN]`.
3. Operations Manager reviews the override within 1 business day.
4. If the issue reflects a systematic problem, Operations Manager updates the relevant skill or command.

**Owner**: Analyst (initial), Operations Manager (review).
