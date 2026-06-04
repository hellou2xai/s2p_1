"""Escalation email script: sends structured email for critical findings.

Called by session-complete-hook.sh when severity is Critical.
Reads the monitor output file, extracts critical anomaly data, and writes
an email draft to notifications/email-drafts/.

Reference solution for Course 7, Lesson 4.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path


def extract_summary(content: str) -> str:
    """Pull the summary paragraph from the monitor output."""
    match = re.search(r"## Summary\s*\n\n(.+?)(?=\n\n##|\n\n---)", content, re.DOTALL)
    return match.group(1).strip() if match else "No summary available."


def extract_actions(content: str) -> list[str]:
    """Pull recommended actions from the monitor output."""
    actions = []
    match = re.search(r"## Recommended Actions\s*\n\n(.+?)(?=\n\n---|\Z)", content, re.DOTALL)
    if match:
        for line in match.group(1).strip().split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                actions.append(re.sub(r"^\d+\.\s*", "", line))
    return actions


def build_email(monitor_file: str, content: str) -> dict:
    """Build a structured email draft."""
    date_match = re.search(r"monitor-(\d{4}-\d{2}-\d{2})", monitor_file)
    monitor_date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")

    summary = extract_summary(content)
    actions = extract_actions(content)

    email = {
        "to": ["vp-procurement@ironclad-group.com", "category-manager@ironclad-group.com"],
        "cc": ["procurement-analytics@ironclad-group.com"],
        "subject": f"CRITICAL: Spend Monitor Alert for {monitor_date}",
        "body": (
            f"Subject: CRITICAL Spend Monitor Alert for {monitor_date}\n\n"
            f"The nightly spend monitor detected a critical anomaly.\n\n"
            f"SUMMARY\n"
            f"{summary}\n\n"
            f"RECOMMENDED ACTIONS\n"
        ),
    }

    for i, action in enumerate(actions, 1):
        email["body"] += f"{i}. {action}\n"

    email["body"] += (
        f"\nThis email was generated automatically by the spend monitoring pipeline. "
        f"Review the full report at: outputs/daily-monitors/{Path(monitor_file).name}\n\n"
        f"Response required within 4 hours for critical findings.\n"
    )

    return email


def main():
    if len(sys.argv) < 2:
        print("Usage: python escalation-email.py <monitor-file>")
        sys.exit(1)

    monitor_file = sys.argv[1]
    with open(monitor_file, "r", encoding="utf-8") as f:
        content = f.read()

    email = build_email(monitor_file, content)

    # Save email draft
    script_dir = Path(__file__).resolve().parent
    drafts_dir = script_dir.parent / "notifications" / "email-drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    date_match = re.search(r"monitor-(\d{4}-\d{2}-\d{2})", monitor_file)
    monitor_date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")
    output_path = drafts_dir / f"escalation-{monitor_date}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(email, f, indent=2)
    print(f"Email draft saved to {output_path}")


if __name__ == "__main__":
    main()
