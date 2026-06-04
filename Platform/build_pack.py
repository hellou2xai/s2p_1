#!/usr/bin/env python3
"""Build the student-facing course pack from the canonical tree.

Produces, under Platform/dist/:
  S2P_Course_Pack_v1.zip      the public zip: client files plus every lesson,
                              with practice data, solutions, and regenerator
                              scripts stripped out
  bundles/course-NN.zip       20 gated bundles for the R2 bucket, holding
                              exactly what the public zip strips
  bundles/manifest.json       sha256, file count, and size per bundle, for
                              upload metadata and fetch.py verification

Split rule, per course folder:
  PUBLIC: lessons/**, README.md, COURSE_OVERVIEW.md, practice CLAUDE.md
          files, practice README.md files, anything under a templates/ folder
  GATED:  everything else (practice data, solutions/, scripts/)

Run from anywhere: paths derive from this file's location. Pause OneDrive
sync before running.
"""

import hashlib
import json
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "courses"
CLIENT = REPO_ROOT / "Platform" / "client"
DIST = REPO_ROOT / "Platform" / "dist"
PACK_NAME = "S2P_Course_Pack_v1.zip"

JUNK = {"Thumbs.db", "desktop.ini", ".DS_Store"}
CLIENT_FILES = {
    "START_HERE.md": "START_HERE.md",
    "fetch.py": "fetch.py",
    "u2xai_config.json": "u2xai_config.json",
    "check_license.py": "scripts/check_license.py",
}


def is_public(relative: Path) -> bool:
    parts = relative.parts
    if parts[0] == "lessons":
        return True
    if len(parts) == 1 and relative.name in ("README.md", "COURSE_OVERVIEW.md"):
        return True
    if parts[0] == "practice":
        if relative.name in ("CLAUDE.md", "README.md"):
            return True
        if "templates" in parts:
            return True
    return False


def course_dirs() -> list[Path]:
    return sorted(d for d in SOURCE.iterdir() if d.is_dir() and d.name.startswith("Course_"))


def course_id(course_dir: Path) -> str:
    number = course_dir.name.split("_")[1]
    return f"course-{number}"


def split_course(course_dir: Path) -> tuple[list[Path], list[Path], list[Path]]:
    """Returns (public_files, gated_files, gated_empty_dirs)."""
    public, gated = [], []
    for path in sorted(course_dir.rglob("*")):
        if path.is_dir() or path.name in JUNK or ".claude" in path.parts:
            continue
        relative = path.relative_to(course_dir)
        (public if is_public(relative) else gated).append(path)
    # Folders that end up with no files at all (intake/, outputs/) still need
    # to exist after a fetch, because lessons reference them. Ship them as
    # directory entries in the gated bundle.
    empty_dirs = [
        d for d in sorted(course_dir.rglob("*"))
        if d.is_dir() and ".claude" not in d.parts and not any(
            f.is_file() and f.name not in JUNK for f in d.rglob("*")
        )
    ]
    return public, gated, empty_dirs


def build() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"Canonical tree not found: {SOURCE}")
    DIST.mkdir(exist_ok=True)
    (DIST / "bundles").mkdir(exist_ok=True)

    manifest: dict[str, dict] = {}
    public_zip_path = DIST / PACK_NAME

    with zipfile.ZipFile(public_zip_path, "w", zipfile.ZIP_DEFLATED) as public_zip:
        for client_file, arcname in CLIENT_FILES.items():
            public_zip.write(CLIENT / client_file, arcname)

        for course_dir in course_dirs():
            public, gated, empty_dirs = split_course(course_dir)

            for path in public:
                public_zip.write(path, f"{course_dir.name}/{path.relative_to(course_dir)}")

            bundle_path = DIST / "bundles" / f"{course_id(course_dir)}.zip"
            with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as bundle:
                for path in gated:
                    bundle.write(path, f"{course_dir.name}/{path.relative_to(course_dir)}")
                for directory in empty_dirs:
                    bundle.writestr(
                        f"{course_dir.name}/{directory.relative_to(course_dir)}/", ""
                    )

            digest = hashlib.sha256(bundle_path.read_bytes()).hexdigest()
            manifest[course_id(course_dir)] = {
                "sha256": digest,
                "files": len(gated),
                "bytes": bundle_path.stat().st_size,
            }
            print(
                f"{course_id(course_dir)}: {len(public):4d} public, "
                f"{len(gated):4d} gated, bundle {bundle_path.stat().st_size // 1024} KB"
            )

    (DIST / "bundles" / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"\nPublic pack: {public_zip_path} ({public_zip_path.stat().st_size // 1024} KB)")
    print(f"Bundles and manifest: {DIST / 'bundles'}")


if __name__ == "__main__":
    build()
