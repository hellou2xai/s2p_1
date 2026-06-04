"""Key delivery via Resend. Standard library HTTP, no extra dependency.

Email is best-effort by design: the signup response always carries the key,
so a mail outage inconveniences nobody. Failures are printed to the service
log and swallowed.
"""

import json
import os
import urllib.error
import urllib.request

RESEND_URL = "https://api.resend.com/emails"
TIMEOUT = 10


def send_key_email(to_email: str, key: str, expires_at: str, trial_days: int) -> bool:
    api_key = os.environ.get("RESEND_API_KEY", "")
    if not api_key:
        return False  # not configured yet; screen delivery still works

    sender = os.environ.get("EMAIL_FROM", "U2xAI Academy <onboarding@resend.dev>")
    html = f"""
    <p>Here is your S2P Course Pack license key:</p>
    <p style="font-family: Consolas, monospace; font-size: 18px; font-weight: bold;">{key}</p>
    <p>It is valid for {trial_days} days, until {expires_at}. It covers all 20
    courses and connected mode, on up to 2 machines.</p>
    <p>Next steps:</p>
    <ol>
      <li>Download the course pack zip and extract it to a folder of its own.</li>
      <li>Open a terminal in that folder and run: <b>python fetch.py course-02</b></li>
      <li>Paste this key when asked. It is saved after the first time.</li>
    </ol>
    <p>Full setup instructions are in START_HERE.md inside the pack.</p>
    """
    body = {
        "from": sender,
        "to": [to_email],
        "subject": "Your S2P Course Pack key from U2xAI Academy",
        "html": html,
    }
    request = urllib.request.Request(
        RESEND_URL,
        method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(body).encode("utf-8"),
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT):
            return True
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
        print(f"resend: key email to {to_email} failed: {error}")
        return False
