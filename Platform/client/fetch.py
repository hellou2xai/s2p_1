#!/usr/bin/env python3
"""Fetch one course's practice data from the U2xAI license server.

Usage:
    python fetch.py course-02

Standard library only: the student never runs pip install.
Contract: Platform/License_Server_Spec.md in the course repository.
"""

import getpass
import hashlib
import json
import platform
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PACK_ROOT / "u2xai_config.json"
TOKEN_PATH = PACK_ROOT / ".u2xai" / "token"
HOOK_SCRIPT = PACK_ROOT / "scripts" / "check_license.py"
TIMEOUT = 30


def fail(message: str) -> None:
    print(f"\n{message}")
    sys.exit(1)


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        fail("u2xai_config.json is missing. Re-download the course pack zip.")
    # utf-8-sig tolerates the BOM marker Windows editors add to saved files
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))


def save_config(config: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")


def machine_id() -> str:
    raw = f"{platform.node()}|{getpass.getuser()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def api(server: str, path: str, key: str, method: str = "GET", body: dict | None = None) -> dict:
    request = urllib.request.Request(
        server.rstrip("/") + path,
        method=method,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=json.dumps(body).encode("utf-8") if body is not None else None,
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read().decode("utf-8")).get("detail", {})
            fail(detail.get("message", f"Server error {error.code}."))
        except (ValueError, AttributeError):
            fail(f"Server error {error.code}. Try again in a few minutes.")
    except urllib.error.URLError:
        fail(
            "Cannot reach the license server. Check your internet connection "
            "and try again."
        )
    return {}  # unreachable; fail() exits


def install_hooks() -> None:
    """Write .claude/settings.local.json into every course practice folder
    (and its first-level subfolders) with the ABSOLUTE path to the license
    hook. Claude Code does not expand variables in hook commands, and the
    absolute path is only known here, at the student's machine, at runtime.
    settings.local.json merges with the settings.json files the lessons
    create, so course exercises are never overwritten."""
    script = str(HOOK_SCRIPT).replace("\\", "/")
    settings = {
        "hooks": {
            "SessionStart": [
                {"hooks": [{"type": "command", "command": f'python "{script}" --session-start'}]}
            ],
            "PreToolUse": [
                {"hooks": [{"type": "command", "command": f'python "{script}" --pre-tool'}]}
            ],
        }
    }
    payload = json.dumps(settings, indent=2)
    for course_dir in sorted(PACK_ROOT.glob("Course_*")):
        practice = course_dir / "practice"
        if not practice.is_dir():
            continue
        targets = [practice] + [d for d in practice.iterdir() if d.is_dir() and d.name != ".claude"]
        for target in targets:
            claude_dir = target / ".claude"
            claude_dir.mkdir(exist_ok=True)
            (claude_dir / "settings.local.json").write_text(payload, encoding="utf-8")


def activate(server: str, key: str) -> None:
    result = api(server, "/activate", key, method="POST", body={"machine_id": machine_id()})
    TOKEN_PATH.parent.mkdir(exist_ok=True)
    TOKEN_PATH.write_text(result["token"], encoding="utf-8")
    install_hooks()
    if result.get("message"):
        print(result["message"])


def safe_extract(zip_path: Path, destination: Path) -> int:
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            if member.startswith(("/", "\\")) or ".." in member:
                fail(f"Bundle contains an unsafe path: {member}. Contact support.")
        archive.extractall(destination)
        return len(archive.namelist())


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python fetch.py course-NN   (course-02 through course-21)")
    course_id = sys.argv[1].lower()

    config = load_config()
    server = config.get("server_url", "")
    key = config.get("license_key", "")
    if not key:
        key = input("Paste your license key (U2X-XXXX-XXXX-XXXX): ").strip()
        if not key:
            fail("No key entered. Sign up for a free key first; see START_HERE.md.")
        config["license_key"] = key
        save_config(config)

    if not TOKEN_PATH.exists():
        activate(server, key)

    result = api(server, f"/fetch/{course_id}", key)

    print(f"Downloading {course_id} data...")
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as handle:
        temp_path = Path(handle.name)
    try:
        urllib.request.urlretrieve(result["url"], temp_path)
        expected = result.get("sha256", "")
        if expected:
            actual = hashlib.sha256(temp_path.read_bytes()).hexdigest()
            if actual != expected:
                fail("Download arrived corrupted. Run the same command again.")
        count = safe_extract(temp_path, PACK_ROOT)
    finally:
        temp_path.unlink(missing_ok=True)

    install_hooks()
    print(f"{count} files installed.")
    if result.get("message"):
        print(result["message"])


if __name__ == "__main__":
    main()
