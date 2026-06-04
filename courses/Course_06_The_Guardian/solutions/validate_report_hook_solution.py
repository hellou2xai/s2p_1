"""PreToolUse hook: validate contract review reports before saving.

Registered in .claude/settings.json as a PreToolUse hook on the Write tool.
Claude Code passes tool call details as JSON on stdin.
This script checks for required sections, valid risk levels, and complete
supplier references. Returns approve or block as JSON on stdout.

Reference solution for Course 6, Lesson 2.
"""

import json
import re
import sys


VALID_RISK_LEVELS = {"Low", "Medium", "High", "Critical"}

REQUIRED_SECTIONS = [
    ("Parties", r"\*\*Parties:\*\*"),
    ("Term", r"\*\*Term:\*\*"),
    ("Value", r"\*\*(Annual )?Value:\*\*"),
    ("Risk Assessment", r"\*\*Risk Level:\*\*"),
    ("Key Clauses", r"\*\*Key Clauses:\*\*"),
    ("Recommendation", r"\*\*Recommendation:\*\*"),
]


def validate_report(content: str) -> list[str]:
    """Check content against report quality standards. Return list of errors."""
    errors = []

    # Check required sections
    for section_name, pattern in REQUIRED_SECTIONS:
        if not re.search(pattern, content):
            errors.append(f"Missing required section: {section_name}")

    # Check risk level value
    risk_match = re.search(r"\*\*Risk Level:\*\*\s*(\w+)", content)
    if risk_match:
        risk_value = risk_match.group(1).strip().rstrip(".")
        if risk_value not in VALID_RISK_LEVELS:
            errors.append(
                f"Invalid risk level: '{risk_value}'. "
                f"Must be one of: {', '.join(sorted(VALID_RISK_LEVELS))}"
            )

    # Check supplier name in parties section
    parties_match = re.search(r"\*\*Parties:\*\*.*?and\s+(.*?)\s*\(Supplier\)", content)
    if parties_match:
        supplier_name = parties_match.group(1).strip()
        if not supplier_name or len(supplier_name) < 2:
            errors.append("Supplier name is missing or empty in Parties section")

    # Check key clauses are not empty
    clauses_match = re.search(
        r"\*\*Key Clauses:\*\*\s*\n(.*?)(?=\n\*\*|\Z)", content, re.DOTALL
    )
    if clauses_match:
        clauses_content = clauses_match.group(1).strip()
        if not clauses_content or clauses_content == "(none reviewed)":
            errors.append("Key Clauses section is empty or contains no actual clause references")

    # Check high/critical risk has recommendation
    if risk_match:
        risk_value = risk_match.group(1).strip().rstrip(".")
        if risk_value in {"High", "Critical"}:
            if not re.search(r"\*\*Recommendation:\*\*", content):
                errors.append(
                    f"Risk level is {risk_value} but no Recommendation section found. "
                    f"High and Critical risk contracts require a specific recommendation."
                )

    return errors


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # If we cannot parse the input, approve by default to avoid blocking
        print(json.dumps({"decision": "approve"}))
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only validate Write tool calls to outputs/
    if tool_name != "Write":
        print(json.dumps({"decision": "approve"}))
        return

    file_path = tool_input.get("file_path", "")
    if "outputs/" not in file_path and "outputs\\" not in file_path:
        print(json.dumps({"decision": "approve"}))
        return

    content = tool_input.get("content", "")
    errors = validate_report(content)

    if errors:
        error_message = "Report validation failed. Fix these issues before saving:\n"
        for i, error in enumerate(errors, 1):
            error_message += f"  {i}. {error}\n"
        print(json.dumps({"decision": "block", "reason": error_message}))
    else:
        print(json.dumps({"decision": "approve"}))


if __name__ == "__main__":
    main()
