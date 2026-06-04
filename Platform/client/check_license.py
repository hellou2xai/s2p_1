#!/usr/bin/env python3
"""License session check. Runs as a Claude Code hook; never run by hand.

Modes:
    --session-start   at session start: refresh the token, show any message
    --pre-tool        before each tool call: fast local check, blocks when lapsed

Fast path: a cached signed token under .u2xai/ is valid for 72 hours
(server-controlled), so the network is only touched when it expires.
Exit 0 allows. Exit 2 blocks, with the server's message on stderr.
Standard library only. Contract: Platform/License_Server_Spec.md.
"""

import base64
import getpass
import hashlib
import json
import platform
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PACK_ROOT / "u2xai_config.json"
TOKEN_PATH = PACK_ROOT / ".u2xai" / "token"
TIMEOUT = 10

OFFLINE_BLOCK = (
    "Cannot reach the license server and the 72-hour offline window has "
    "ended. Connect to the internet once and start the session again. "
    "Your work in Drafts/ and Outputs/ is untouched."
)


def block(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


def token_seconds_left() -> float:
    """Reads exp from the cached JWT payload. Signature verification is the
    server's job; locally only the expiry matters."""
    try:
        token = TOKEN_PATH.read_text(encoding="utf-8").strip()
        payload_part = token.split(".")[1]
        payload_part += "=" * (-len(payload_part) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_part))
        return payload["exp"] - time.time()
    except (OSError, IndexError, KeyError, ValueError):
        return -1


def machine_id() -> str:
    raw = f"{platform.node()}|{getpass.getuser()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def session_check() -> dict | None:
    """Returns the server response, or None when the network is unreachable."""
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None  # pack not activated yet; stay out of the way
    key = config.get("license_key", "")
    if not key:
        return None  # not activated yet; fetch.py handles first contact
    request = urllib.request.Request(
        config.get("server_url", "").rstrip("/") + "/session-check",
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=json.dumps({"machine_id": machine_id()}).encode("utf-8"),
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read().decode("utf-8")).get("detail", {})
            return {"status": detail.get("code", "error"), "message": detail.get("message", "")}
        except (ValueError, AttributeError):
            return {"status": "error", "message": f"License server error {error.code}."}
    except (urllib.error.URLError, TimeoutError):
        return None


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--pre-tool"
    seconds_left = token_seconds_left()

    # Fast path: a valid cached token allows everything, no network.
    # At session start, refresh early (under 24 hours left) so a weekend
    # offline never lands on an expired token mid-week.
    if seconds_left > 0 and not (mode == "--session-start" and seconds_left < 86400):
        sys.exit(0)

    result = session_check()

    if result is None:  # unreachable server or unactivated pack
        if seconds_left > 0 or not CONFIG_PATH.exists():
            sys.exit(0)  # still inside grace, or pack not set up yet
        block(OFFLINE_BLOCK)

    if result.get("status") == "active":
        token = result.get("token", "")
        if token:
            TOKEN_PATH.parent.mkdir(exist_ok=True)
            TOKEN_PATH.write_text(token, encoding="utf-8")
        message = result.get("message", "")
        if message and mode == "--session-start":
            print(message)  # session-start stdout is shown, not blocking
        sys.exit(0)

    # lapsed, revoked, or key_invalid: print the server's wording verbatim
    block(result.get("message", "License check failed. See START_HERE.md."))


if __name__ == "__main__":
    main()
