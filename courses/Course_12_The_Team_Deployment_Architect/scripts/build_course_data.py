"""
Course 12: The Team Deployment Architect
Generates practice data for Summit Procurement Group team deployment.
Run: python scripts/build_course_data.py
"""

import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = SCRIPT_DIR.parent / "practice"


def ensure_dirs():
    dirs = [
        PRACTICE_DIR / "shared" / "skills",
        PRACTICE_DIR / "shared" / "commands",
        PRACTICE_DIR / "hooks",
        PRACTICE_DIR / "governance",
        PRACTICE_DIR / "analyst-workspace-template" / ".claude" / "commands",
        PRACTICE_DIR / "analyst-workspace-template" / "data",
        PRACTICE_DIR / "analyst-workspace-template" / "outputs",
        PRACTICE_DIR / "scripts",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def build_shared_claude_md():
    content = """# Summit Procurement Group: Shared Context

## Organization

Summit Procurement Group is a US-based procurement team with $124M in annual spend across six categories. Three offices: Chicago (IL), Dallas (TX), and Atlanta (GA). Eight analysts.

## Categories

| Category | Annual spend | Lead analyst | Office |
|---|---|---|---|
| IT services | $22.4M | Sarah Kim | Chicago |
| Raw materials | $24.8M | James Park | Chicago |
| MRO | $12.6M | Lisa Chen | Chicago |
| Logistics | $21.2M | Marcus Davis | Dallas |
| Facilities | $16.8M | Ana Torres | Dallas |
| Professional services | $14.4M | Kevin Wright | Dallas |

Cross-category support: Priya Sharma (supplier risk) and Tom Bradley (reporting), both in Atlanta.

## Output standards

- All currency in USD with commas.
- Dates in YYYY-MM-DD format.
- Short sentences. Active voice.
- No em-dashes or en-dashes.
- Every output that leaves the team must include a `[REVIEWED]` tag.
- Recommendations capped at three.
- Supplier names use legal entity names (e.g., "Great Lakes Steel Corp", not "the steel supplier").

## Scoring standards

Supplier scorecards use a 1 to 5 scale across four dimensions:
- Quality (weight: 30%)
- Delivery (weight: 25%)
- Cost (weight: 25%)
- Responsiveness (weight: 20%)

Overall score = weighted average. Below 3.0 = at risk. Below 2.5 = corrective action required.

## Audit rules

- Every Write and Bash tool call is logged to the audit trail.
- Audit logs are append-only. Never delete entries.
- Every significant output includes an audit reference ID.
"""
    with open(PRACTICE_DIR / "shared" / "CLAUDE.md", "w", encoding="utf-8") as f:
        f.write(content)


def build_shared_skills():
    spend_analysis = """# Spend Analysis Skill

Analyze spend data for a single category.

## Input
- Category name
- Path to spend data CSV

## Steps
1. Read the spend CSV and filter to the specified category.
2. Calculate total spend, transaction count, and average transaction size.
3. Group by supplier. Rank suppliers by total spend.
4. Identify the top 3 suppliers by spend and their percentage of category total.
5. Flag any supplier with fewer than 5 transactions (possible maverick spend).
6. Calculate month-over-month spend trend for the trailing 6 months.

## Output format
Save to outputs/ as `spend-analysis-<category>.md` with sections:
- Summary (total spend, transaction count, supplier count)
- Top suppliers table
- Trend (up, down, stable with percentage)
- Flags (maverick spend, concentration risk)
"""
    supplier_scorecard = """# Supplier Scorecard Skill

Generate a quarterly scorecard for a single supplier.

## Input
- Supplier name or ID
- Path to scorecard data CSV

## Steps
1. Read the scorecard CSV and filter to the specified supplier.
2. Extract scores for the most recent quarter across all four dimensions.
3. Calculate the weighted overall score.
4. Compare to the previous quarter. Note any dimension that changed by more than 0.5 points.
5. Flag if overall score is below 3.0 (at risk) or below 2.5 (corrective action).

## Output format
Save to outputs/ as `scorecard-<supplier_id>.md` with sections:
- Current quarter scores (table)
- Quarter-over-quarter change
- Risk flags
- Recommended actions (if below threshold)
"""
    contract_review = """# Contract Review Skill

Review a contract for completeness and upcoming deadlines.

## Input
- Contract ID
- Path to contract calendar CSV

## Steps
1. Read the contract calendar and find the specified contract.
2. Check if the contract expires within 90 days.
3. If auto-renewal is "yes", check if the notice period deadline has passed.
4. Calculate days until expiry and days until notice deadline.
5. Flag contracts expiring within 60 days without a renewal plan.

## Output format
Save to outputs/ as `contract-review-<contract_id>.md` with sections:
- Contract summary (supplier, category, dates, value)
- Timeline (days to expiry, days to notice deadline)
- Risk level (green, amber, red)
- Recommended action
"""
    skills = {
        "spend-analysis.md": spend_analysis,
        "supplier-scorecard.md": supplier_scorecard,
        "contract-review.md": contract_review,
    }
    for name, content in skills.items():
        with open(PRACTICE_DIR / "shared" / "skills" / name, "w", encoding="utf-8") as f:
            f.write(content)


def build_shared_commands():
    daily_check = """# Daily Check

Run a quick status check across all categories.

## What this command does
1. Read program-state.json for current risk flags.
2. Check contract-calendar.csv for contracts expiring within 30 days.
3. Check initiative-pipeline.csv for initiatives with status "at_risk" or "behind_schedule".
4. Produce a one-page summary with three sections: risk flags, expiring contracts, and troubled initiatives.

## Output
Save to outputs/ as `daily-check-YYYY-MM-DD.md`.
"""
    category_brief = """# Category Brief

Generate a deep-dive brief for a single category.

## Usage
Provide the category name as the argument: `/category-brief IT services`

## What this command does
1. Filter spend data to the specified category.
2. Pull supplier scorecards for all suppliers in the category.
3. Check contract status for contracts in the category.
4. Review initiative progress for the category.
5. Produce a structured brief with spend summary, supplier performance, contract status, and initiative progress.

## Output
Save to outputs/ as `category-brief-<category>-YYYY-MM-DD.md`.
"""
    risk_scan = """# Risk Scan

Scan all suppliers for risk indicators.

## What this command does
1. Read supplier scorecards. Flag any supplier with overall score below 3.0.
2. Read contract calendar. Flag any contract expiring within 60 days without a renewal plan.
3. Read initiative pipeline. Flag any initiative behind schedule with more than $200,000 at risk.
4. Produce a risk summary sorted by severity (critical, high, medium).

## Output
Save to outputs/ as `risk-scan-YYYY-MM-DD.md`.
"""
    commands = {
        "daily-check.md": daily_check,
        "category-brief.md": category_brief,
        "risk-scan.md": risk_scan,
    }
    for name, content in commands.items():
        with open(PRACTICE_DIR / "shared" / "commands" / name, "w", encoding="utf-8") as f:
            f.write(content)


def build_hooks():
    audit_log = '''"""
Audit log hook (PostToolUse).
Appends a JSONL entry to audit/audit.jsonl after every Write or Bash tool call.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    """Read tool result from stdin and append audit entry."""
    input_data = json.loads(sys.stdin.read())

    tool_name = input_data.get("tool_name", "unknown")
    tool_input = input_data.get("tool_input", {})

    # Only log Write and Bash calls
    if tool_name not in ("Write", "Bash"):
        return

    audit_dir = Path("audit")
    audit_dir.mkdir(exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool_name,
        "file_path": tool_input.get("file_path", tool_input.get("command", "n/a")),
        "analyst": "ANALYST_NAME_PLACEHOLDER",
        "session_id": "SESSION_PLACEHOLDER",
    }

    with open(audit_dir / "audit.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\\n")


if __name__ == "__main__":
    main()
'''
    review_gate = '''"""
Review gate hook (PreToolUse).
Blocks any Write to outputs/ unless the content includes a [REVIEWED] tag.
"""

import json
import sys


def main():
    """Read tool input from stdin. Block if writing to outputs/ without [REVIEWED] tag."""
    input_data = json.loads(sys.stdin.read())

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name != "Write":
        # Approve non-Write calls
        result = {"decision": "approve"}
        print(json.dumps(result))
        return

    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")

    if "outputs/" in file_path or "outputs\\\\" in file_path:
        if "[REVIEWED]" not in content:
            result = {
                "decision": "block",
                "reason": "Output files must include a [REVIEWED] tag before saving. Add [REVIEWED] to the document header or footer."
            }
            print(json.dumps(result))
            return

    result = {"decision": "approve"}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
'''
    team_notify = '''"""
Team notification hook (PostToolUse).
Writes a notification file when a critical risk is detected.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    """Check tool output for critical risk mentions. Write notification if found."""
    input_data = json.loads(sys.stdin.read())

    tool_name = input_data.get("tool_name", "")
    tool_output = input_data.get("tool_output", "")

    if tool_name != "Write":
        return

    # Check for critical risk keywords in written content
    content = input_data.get("tool_input", {}).get("content", "")
    critical_keywords = ["corrective action required", "critical risk", "contract expired", "immediate escalation"]

    found = [kw for kw in critical_keywords if kw.lower() in content.lower()]
    if not found:
        return

    notify_dir = Path("notifications")
    notify_dir.mkdir(exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    notification = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "critical_risk",
        "triggers": found,
        "source_file": input_data.get("tool_input", {}).get("file_path", "unknown"),
        "action_required": "Review the flagged output and escalate to the Procurement Operations Manager.",
    }

    with open(notify_dir / f"notify-{ts}.json", "w", encoding="utf-8") as f:
        json.dump(notification, f, indent=2)


if __name__ == "__main__":
    main()
'''
    hooks = {
        "audit-log.py": audit_log,
        "review-gate.py": review_gate,
        "team-notify.py": team_notify,
    }
    for name, content in hooks.items():
        with open(PRACTICE_DIR / "hooks" / name, "w", encoding="utf-8") as f:
            f.write(content)


def build_governance():
    what_is_shared = """# What Is Shared

These files are managed centrally by the Procurement Operations Manager. Analysts use them but do not edit them.

## Shared files

| File or folder | Purpose | Update frequency |
|---|---|---|
| shared/CLAUDE.md | Base context: org structure, categories, standards | Monthly or when org changes |
| shared/skills/ | Canonical analysis patterns | When a pattern is approved |
| shared/commands/ | Team-wide slash commands | When a new command is approved |
| hooks/ | Audit, review gate, notifications | When policy changes |
| governance/ | Team rules and escalation paths | Quarterly review |

## Update process

1. Operations Manager drafts the update.
2. One analyst from each office tests the update in their workspace.
3. Operations Manager publishes the update to shared/.
4. All analysts pull the update (or the onboarding script refreshes their workspace).

## Version tracking

Each shared file includes a version comment at the top (e.g., `v2.1, updated 2026-04-25`). Analysts report issues referencing the version number.
"""
    what_is_personal = """# What Is Personal

Each analyst has a personal workspace. These files belong to them and can be customized.

## Personal files

| File or folder | Purpose | Who owns it |
|---|---|---|
| CLAUDE.md (in analyst workspace) | Analyst-specific context: categories, preferences, working notes | The analyst |
| data/ | Working data for current analysis | The analyst |
| outputs/ | Analysis outputs, drafts, reports | The analyst |

## Rules for personal files

1. Personal CLAUDE.md must not contradict shared CLAUDE.md. If there is a conflict, shared wins.
2. Analysts may add skills to their personal workspace, but personal skills do not become shared without approval.
3. Analysts may not disable or modify hooks. Hooks run on every workspace.
4. Output files in outputs/ must include the `[REVIEWED]` tag before sending outside the team.
"""
    escalation_policy = """# Escalation Policy

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
"""
    docs = {
        "what-is-shared.md": what_is_shared,
        "what-is-personal.md": what_is_personal,
        "escalation-policy.md": escalation_policy,
    }
    for name, content in docs.items():
        with open(PRACTICE_DIR / "governance" / name, "w", encoding="utf-8") as f:
            f.write(content)


def build_workspace_template():
    # Template CLAUDE.md
    claude_md = """# [Analyst Name]: Personal Workspace

## Role
[Your title] at Summit Procurement Group, [Office] office.

## Categories
[List your assigned categories here.]

## Personal preferences
[Add any personal working preferences, shortcuts, or notes here.]

## Notes
- This file is yours to customize.
- Do not contradict the shared CLAUDE.md.
- Your hooks (audit, review gate) run automatically. Do not disable them.
"""
    template_dir = PRACTICE_DIR / "analyst-workspace-template"
    with open(template_dir / "CLAUDE.md", "w", encoding="utf-8") as f:
        f.write(claude_md)

    # Template settings.json
    settings = {
        "permissions": {
            "allow": ["Read", "Glob", "Grep"],
            "deny": []
        },
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Write",
                    "command": "python hooks/review-gate.py"
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Write|Bash",
                    "command": "python hooks/audit-log.py"
                },
                {
                    "matcher": "Write",
                    "command": "python hooks/team-notify.py"
                }
            ]
        }
    }
    with open(template_dir / ".claude" / "settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def build_onboarding_script():
    script = """#!/usr/bin/env bash
# onboard-analyst.sh
# Creates a new analyst workspace from the template.
# Usage: bash scripts/onboard-analyst.sh <analyst_name> <office>
# Example: bash scripts/onboard-analyst.sh sarah_kim chicago

set -euo pipefail

ANALYST_NAME="${1:?Usage: onboard-analyst.sh <analyst_name> <office>}"
OFFICE="${2:?Usage: onboard-analyst.sh <analyst_name> <office>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")/practice"
TEMPLATE_DIR="$PROJECT_DIR/analyst-workspace-template"
TARGET_DIR="$PROJECT_DIR/workspaces/$ANALYST_NAME"

if [ -d "$TARGET_DIR" ]; then
    echo "Error: Workspace already exists at $TARGET_DIR"
    exit 1
fi

echo "Creating workspace for $ANALYST_NAME ($OFFICE office)..."

# Copy template
cp -r "$TEMPLATE_DIR" "$TARGET_DIR"

# Copy shared files
cp "$PROJECT_DIR/shared/CLAUDE.md" "$TARGET_DIR/shared-context.md"
cp -r "$PROJECT_DIR/shared/skills" "$TARGET_DIR/skills"
cp -r "$PROJECT_DIR/shared/commands" "$TARGET_DIR/.claude/commands"
cp -r "$PROJECT_DIR/hooks" "$TARGET_DIR/hooks"

# Personalize CLAUDE.md
sed -i "s/\\[Analyst Name\\]/$ANALYST_NAME/g" "$TARGET_DIR/CLAUDE.md"
sed -i "s/\\[Office\\]/$OFFICE/g" "$TARGET_DIR/CLAUDE.md"

# Create audit directory
mkdir -p "$TARGET_DIR/audit"

echo "Workspace created at $TARGET_DIR"
echo "Next steps:"
echo "  1. Edit $TARGET_DIR/CLAUDE.md with your role and categories."
echo "  2. Open Claude Code in $TARGET_DIR."
echo "  3. Run /daily-check to verify everything works."
"""
    with open(PRACTICE_DIR / "scripts" / "onboard-analyst.sh", "w", encoding="utf-8", newline="\n") as f:
        f.write(script)


def main():
    ensure_dirs()
    build_shared_claude_md()
    build_shared_skills()
    build_shared_commands()
    build_hooks()
    build_governance()
    build_workspace_template()
    build_onboarding_script()
    print("Course 12 data generated.")
    print(f"  Practice directory: {PRACTICE_DIR}")
    print("  Shared context, skills, commands, hooks, governance, workspace template, and onboarding script created.")


if __name__ == "__main__":
    main()
