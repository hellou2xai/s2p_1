"""
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

    if "outputs/" in file_path or "outputs\\" in file_path:
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
