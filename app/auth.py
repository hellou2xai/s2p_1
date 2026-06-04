"""Key generation, bearer extraction, and session token signing."""

import os
import secrets
import time

import jwt
from fastapi import Header, HTTPException

# No 0/O, 1/I/L: keys get read aloud and typed by hand.
_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def new_key() -> str:
    block = lambda: "".join(secrets.choice(_ALPHABET) for _ in range(4))
    return f"U2X-{block()}-{block()}-{block()}"


def bearer_key(authorization: str = Header(default="")) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={
                "code": "key_invalid",
                "message": "This key was not recognized. Check for typos, "
                "or sign up at https://u2xai.com/start",
            },
        )
    return authorization.removeprefix("Bearer ").strip()


def issue_token(key: str, machine_id: str) -> str:
    grace_hours = int(os.environ.get("GRACE_HOURS", "72"))
    payload = {
        "sub": key,
        "mid": machine_id,
        "exp": int(time.time()) + grace_hours * 3600,
    }
    return jwt.encode(payload, os.environ["TOKEN_SIGNING_SECRET"], algorithm="HS256")
