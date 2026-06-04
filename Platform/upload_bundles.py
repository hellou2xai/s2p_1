#!/usr/bin/env python3
"""Upload the 20 course bundles to the R2 bucket with sha256 metadata.

Reads dist/bundles/ next to this script, takes checksums from manifest.json,
and puts every zip under the bundles/ prefix where the license server's
/fetch endpoint expects it. Safe to re-run: uploads overwrite in place.

Credentials come from environment variables when set, otherwise the script
asks for them (the secret is typed hidden, never echoed):
  R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY

Requires boto3 on this machine only (students never run this):
  pip install boto3
"""

import getpass
import json
import os
import sys
from pathlib import Path

try:
    import boto3
    from botocore.config import Config
except ImportError:
    sys.exit("boto3 is not installed. Run: pip install boto3")

BUNDLES_DIR = Path(__file__).resolve().parent / "dist" / "bundles"
BUCKET = "u2xai-course-bundles"


def credential(name: str, hidden: bool = False) -> str:
    value = os.environ.get(name, "")
    if not value:
        prompt = f"{name}: "
        value = (getpass.getpass(prompt) if hidden else input(prompt)).strip()
    if not value:
        sys.exit(f"{name} is required. Find it in the Cloudflare R2 dashboard.")
    return value


def main() -> None:
    manifest_path = BUNDLES_DIR / "manifest.json"
    if not manifest_path.exists():
        sys.exit(f"manifest.json not found at {manifest_path}. Run build_pack.py first.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    account_id = credential("R2_ACCOUNT_ID")
    access_key = credential("R2_ACCESS_KEY_ID")
    secret_key = credential("R2_SECRET_ACCESS_KEY", hidden=True)

    client = boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )

    uploaded = 0
    for course_id, info in sorted(manifest.items()):
        zip_path = BUNDLES_DIR / f"{course_id}.zip"
        if not zip_path.exists():
            sys.exit(f"Missing {zip_path}. Run build_pack.py again.")
        object_key = f"bundles/{course_id}.zip"
        client.upload_file(
            str(zip_path),
            BUCKET,
            object_key,
            ExtraArgs={"Metadata": {"sha256": info["sha256"]}},
        )
        head = client.head_object(Bucket=BUCKET, Key=object_key)
        stored = head.get("Metadata", {}).get("sha256", "")
        flag = "ok" if stored == info["sha256"] else "METADATA MISMATCH"
        print(f"{object_key}: {info['bytes'] // 1024} KB, sha256 {flag}")
        uploaded += 1

    print(f"\n{uploaded} bundles uploaded to {BUCKET}/bundles/")


if __name__ == "__main__":
    main()
