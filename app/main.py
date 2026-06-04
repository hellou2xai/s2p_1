"""U2xAI license server, V1.

Contract: Platform/License_Server_Spec.md in the course repository.
Policy lives here and in the database. The shipped clients (fetch.py, the
session hook) treat every response as data and print server-provided
messages verbatim, so wording and levers change without re-shipping.
"""

import os
import time
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr

from . import auth, bundles, db, emailer, messages
from .pages import SIGNUP_HTML


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.run_migrations()
    yield


app = FastAPI(title="u2xai-license", lifespan=lifespan)

# ---------------------------------------------------------------- helpers

_signup_hits: dict[str, list[float]] = defaultdict(list)
SIGNUP_LIMIT_PER_HOUR = 5


def _signup_rate_ok(ip: str) -> bool:
    now = time.time()
    hits = [t for t in _signup_hits[ip] if now - t < 3600]
    _signup_hits[ip] = hits
    if len(hits) >= SIGNUP_LIMIT_PER_HOUR:
        return False
    hits.append(now)
    return True


def _lapse_message(row: dict) -> str:
    ended = row["expires_at"].strftime("%m/%d/%Y")
    renew = os.environ.get("RENEWAL_URL", "https://u2xai.com/renew")
    return (
        f"Your trial ended on {ended}. Course access is paused. "
        "Your work in Drafts/ and Outputs/ is untouched, and everything "
        f"resumes where you stopped. Renewal options: {renew}"
    )


def _revoked_message() -> str:
    support = os.environ.get("SUPPORT_EMAIL", "support@u2xai.com")
    return f"This key has been deactivated. Contact {support}"


def _require_license(key: str) -> dict:
    row = db.get_license(key)
    if row is None:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "key_invalid",
                "message": "This key was not recognized. Check for typos, "
                "or sign up at https://u2xai.com/start",
            },
        )
    return row


# --------------------------------------------------------------- endpoints


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/", response_class=HTMLResponse)
def signup_page():
    return SIGNUP_HTML


class SignupBody(BaseModel):
    email: EmailStr


@app.post("/signup")
def signup(body: SignupBody, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not _signup_rate_ok(ip):
        raise HTTPException(
            status_code=429,
            detail={
                "code": "rate_limited",
                "message": "Too many requests. Wait a few minutes and try again.",
            },
        )
    email = body.email.lower()
    if db.email_exists(email):
        raise HTTPException(
            status_code=409,
            detail={
                "code": "email_exists",
                "message": "A key for this email already exists. Check your inbox.",
            },
        )
    trial_days = int(os.environ.get("TRIAL_DAYS", "30"))
    row = db.create_license(auth.new_key(), email, trial_days)
    emailed = emailer.send_key_email(
        email, row["key"], row["expires_at"].strftime("%m/%d/%Y"), trial_days
    )
    return {
        "key": row["key"],
        "expires_at": row["expires_at"].isoformat(),
        "trial_days": trial_days,
        "emailed": emailed,
    }


class MachineBody(BaseModel):
    machine_id: str


@app.post("/activate")
def activate(body: MachineBody, key: str = Depends(auth.bearer_key)):
    row = _require_license(key)
    status = db.license_status(row)
    if status == "revoked":
        raise HTTPException(status_code=403, detail={"code": "revoked", "message": _revoked_message()})
    if status == "lapsed":
        raise HTTPException(status_code=403, detail={"code": "lapsed", "message": _lapse_message(row)})
    if not db.machine_known(key, body.machine_id) and db.machine_count(key) >= row["max_machines"]:
        support = os.environ.get("SUPPORT_EMAIL", "support@u2xai.com")
        raise HTTPException(
            status_code=403,
            detail={
                "code": "machine_limit",
                "message": f"This key is active on {row['max_machines']} machines "
                f"already. Contact {support} to reset.",
            },
        )
    db.upsert_activation(key, body.machine_id)
    return {
        "status": "active",
        "token": auth.issue_token(key, body.machine_id),
        "expires_at": row["expires_at"].isoformat(),
        "message": "Welcome. Run: python fetch.py course-02 to begin.",
    }


FETCHES_PER_DAY = 6


@app.get("/fetch/{course_id}")
def fetch(course_id: str, key: str = Depends(auth.bearer_key)):
    row = _require_license(key)
    status = db.license_status(row)
    if status == "revoked":
        raise HTTPException(status_code=403, detail={"code": "revoked", "message": _revoked_message()})
    if status == "lapsed":
        raise HTTPException(status_code=403, detail={"code": "lapsed", "message": _lapse_message(row)})
    if course_id not in bundles.VALID_COURSES:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "course_unknown",
                "message": "Course id not recognized. Valid ids: course-02 through course-21.",
            },
        )
    if db.fetches_last_24h(key) >= FETCHES_PER_DAY:
        raise HTTPException(
            status_code=429,
            detail={
                "code": "rate_limited",
                "message": "Too many requests. Wait a few minutes and try again.",
            },
        )
    db.log_fetch(key, course_id)
    url, sha256 = bundles.presigned_url(course_id)
    return {
        "status": "active",
        "url": url,
        "url_expires_in_seconds": bundles.URL_TTL_SECONDS,
        "sha256": sha256,
        "message": messages.pick_message(key, "fetch", course_id)
        or f"{course_id.replace('-', ' ').title()} data ready.",
    }


@app.post("/session-check")
def session_check(body: MachineBody, key: str = Depends(auth.bearer_key)):
    """Always HTTP 200 so the hook renders the message cleanly."""
    row = _require_license(key)
    status = db.license_status(row)
    db.log_session(key, body.machine_id, status)
    if status == "revoked":
        return JSONResponse({"status": "revoked", "message": _revoked_message()})
    if status == "lapsed":
        msg = _lapse_message(row).replace("Course access is paused.", "This session is paused.")
        return JSONResponse({"status": "lapsed", "message": msg})
    db.upsert_activation(key, body.machine_id)
    return {
        "status": "active",
        "token": auth.issue_token(key, body.machine_id),
        "message": messages.pick_message(key, "session"),
    }


@app.post("/resend-key")
def resend_key(body: SignupBody, request: Request):
    """Key recovery: the 'forgot password' of a key-based system. The
    response is identical whether the email exists or not, so the form
    cannot be used to probe which emails are registered. The key itself
    only ever travels to the inbox, never back to the page."""
    ip = request.client.host if request.client else "unknown"
    if not _signup_rate_ok(ip):
        raise HTTPException(
            status_code=429,
            detail={
                "code": "rate_limited",
                "message": "Too many requests. Wait a few minutes and try again.",
            },
        )
    row = db.get_license_by_email(body.email.lower())
    if row is not None:
        trial_days = int(os.environ.get("TRIAL_DAYS", "30"))
        emailer.send_key_email(
            row["email"], row["key"], row["expires_at"].strftime("%m/%d/%Y"), trial_days
        )
    return {
        "message": "If a key exists for this email, it is on its way to that "
        "inbox now. No email after a few minutes means no key is registered "
        "under this address; use the signup tab instead."
    }


@app.get("/status")
def status(key: str = Depends(auth.bearer_key)):
    row = _require_license(key)
    return {
        "status": db.license_status(row),
        "expires_at": row["expires_at"].isoformat(),
        "machines_used": db.machine_count(key),
        "machines_max": row["max_machines"],
        "courses_fetched": db.courses_fetched(key),
    }


@app.post("/reset-machines")
def reset_machines(key: str = Depends(auth.bearer_key)):
    row = _require_license(key)
    removed = db.delete_activations(key)
    return {
        "message": f"{removed} machine registrations cleared. Run "
        "python fetch.py on the machine you want to keep using; it "
        "re-registers automatically."
    }


# /mcp: the connected-mode endpoint mounts here in Phase B, once the
# canonical schema document is locked and the dataset migration exists.
