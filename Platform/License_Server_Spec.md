# License Server Specification, V1

Internal engineering document. Not learner-facing. This is the contract between the course pack clients (`fetch.py`, the session hook, the Claude Code MCP configuration) and the server. The server implementation lives in its own repository and deploys to Render.

Status: draft for build. Date: 2026-06-04.

## 1. Purpose

One web service issues free 30-day license keys, delivers course practice data per course against a valid key, answers a session check at the start of every working session, serves the connected-mode MCP tools, and carries server-controlled messages back to the student. Payments are out of scope for V1. When Stripe arrives, renewal flips one column (`expires_at`) and nothing shipped to students changes.

## 2. Locked decisions this spec implements

| Decision | Value |
|---|---|
| Key type | Free, time-limited. Everything included: all 20 courses plus connected MCP mode, from Course 02 onward. |
| Trial length | 30 days, server-side config (`TRIAL_DAYS`), changeable without re-shipping. |
| Check granularity | Per course. 20 fetches across the catalog, each one validated and logged. |
| Session check | A hook pings the server at every Claude Code session start in a course folder. |
| Offline grace | 72 hours, via a signed token cached by the hook (`GRACE_HOURS`). |
| Lapse behavior | Stop where they stand. Sessions block after the grace token expires. Fetches and MCP calls refuse immediately. Local work in `Drafts/` and `Outputs/` is never touched. Renewal resumes at the same lesson. |
| Messages | Server-controlled slots in the fetch and session-check responses. Clients print what they receive, including nothing. |
| Hosting | Render paid tier: Starter web service (always warm), Postgres 1GB class. Bundles on Cloudflare R2, delivered by presigned URL. |
| Connected data | Postgres tables plus SQL views. Column names match the local practice data schema exactly (one schema, two backends). |

## 3. Stack

| Layer | Choice |
|---|---|
| Web service | Render Web Service, plan `starter`, always on. Python 3.12, FastAPI, uvicorn. |
| MCP endpoint | FastMCP mounted at `/mcp` on the same service, streamable HTTP transport. |
| Database | Render Postgres, 1GB class. Holds licenses and the connected dataset. |
| Bundle storage | Cloudflare R2, private bucket `u2xai-course-bundles`. Zero egress cost. |
| Scheduled jobs | Render Cron Job (expiry reminder emails). V1 ships without it if time is short. |
| Email | [TBC: email provider for key delivery and expiry reminders, for example Resend or Postmark] |
| Domain | `https://u2xai-license.onrender.com` to start. Custom domain later via CNAME. [TBC: final domain] |

## 4. Component layout

```
license-server/                      (separate git repository)
  render.yaml                        Render blueprint, declares everything
  requirements.txt
  app/
    main.py                          FastAPI app, routes below
    auth.py                          key validation, token signing
    bundles.py                       R2 presigned URL generation
    messages.py                      campaign selection and frequency caps
    mcp_server.py                    FastMCP tools, key middleware
    db.py                            connection, queries
  models/
    forecast_model.json              XGBoost artifact, trained offline, loaded at startup
  migrations/
    001_init.sql                     the DDL in section 5
```

## 5. Database schema

```sql
CREATE TABLE licenses (
    key             TEXT PRIMARY KEY,          -- format: U2X-XXXX-XXXX-XXXX
    email           TEXT NOT NULL,
    org_id          TEXT,                      -- NULL in V1, used when org accounts arrive
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at      TIMESTAMPTZ NOT NULL,      -- created_at + TRIAL_DAYS in V1
    status          TEXT NOT NULL DEFAULT 'active',  -- active | revoked
    max_machines    INTEGER NOT NULL DEFAULT 2
);

CREATE TABLE activations (
    key             TEXT NOT NULL REFERENCES licenses(key),
    machine_id      TEXT NOT NULL,             -- client-generated stable hash
    first_seen      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (key, machine_id)
);

CREATE TABLE fetch_log (
    id              BIGSERIAL PRIMARY KEY,
    key             TEXT NOT NULL REFERENCES licenses(key),
    course_id       TEXT NOT NULL,             -- course-02 .. course-21
    fetched_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE session_log (
    id              BIGSERIAL PRIMARY KEY,
    key             TEXT NOT NULL REFERENCES licenses(key),
    machine_id      TEXT NOT NULL,
    checked_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    result          TEXT NOT NULL              -- active | lapsed | revoked
);

CREATE TABLE campaigns (
    id              BIGSERIAL PRIMARY KEY,
    slot            TEXT NOT NULL,             -- fetch | session
    trigger_course  TEXT,                      -- fire when this course is fetched, NULL = any
    trigger_after_day INTEGER,                 -- fire when key age >= N days, NULL = any
    message         TEXT NOT NULL,
    starts_at       TIMESTAMPTZ NOT NULL,
    ends_at         TIMESTAMPTZ NOT NULL,
    weekly_cap      INTEGER NOT NULL DEFAULT 2
);

CREATE TABLE message_log (
    id              BIGSERIAL PRIMARY KEY,
    key             TEXT NOT NULL REFERENCES licenses(key),
    campaign_id     BIGINT NOT NULL REFERENCES campaigns(id),
    sent_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Connected dataset tables ship in a later migration once the schema
-- document is locked. Column names must match the local practice data
-- exactly. [TBC: SCHEMA.md, Phase B]
```

Derived status, computed at request time, never stored:

```
revoked   if licenses.status = 'revoked'
lapsed    if now() > expires_at
active    otherwise
```

## 6. Endpoints

All request and response bodies are JSON. The key travels in the `Authorization: Bearer <key>` header except at signup.

### POST /signup

Issues a key. Called by the signup form on the website, not by the course clients.

Request:

```json
{ "email": "analyst@acme.com" }
```

Response `200`:

```json
{
  "key": "U2X-7F3K-92MD-Q4XR",
  "expires_at": "2026-07-04T00:00:00Z",
  "trial_days": 30
}
```

The key is also emailed. One key per email; a repeat signup returns `409` with a "check your inbox" message. Rate limit: 5 signups per IP per hour.

### POST /activate

Registers a machine and returns the first session token.

Request:

```json
{ "machine_id": "a1b2c3d4e5f6" }
```

Response `200`:

```json
{
  "status": "active",
  "token": "<JWT, 72h expiry>",
  "expires_at": "2026-07-04T00:00:00Z",
  "message": "Welcome. Run: python fetch.py course-02 to begin."
}
```

Response `403` when the machine limit is reached:

```json
{
  "status": "machine_limit",
  "message": "This key is active on 2 machines already. Contact support@u2xai.com to reset."
}
```

### GET /fetch/{course_id}

Validates the key, logs the fetch, returns a presigned R2 URL. `course_id` is one of `course-02` through `course-21`.

Response `200`:

```json
{
  "status": "active",
  "url": "https://...r2.cloudflarestorage.com/bundles/course-04.zip?X-Amz-...",
  "url_expires_in_seconds": 600,
  "sha256": "<bundle checksum, client verifies after download>",
  "message": "Course 04 data ready. 6 lessons."
}
```

Response `403` when lapsed:

```json
{
  "status": "lapsed",
  "message": "Your trial ended on 07/04/2026. Course access is paused. Your work in Drafts/ and Outputs/ is untouched, and everything resumes where you stopped. Renewal options: https://u2xai.com/renew"
}
```

Rate limit: 6 course fetches per key per day. Twenty fetches inside one hour on a young key is a scripted bulk pull, not a learner; the limiter slows it and flags the key for review.

### POST /session-check

Called by the session hook at every Claude Code session start in a course folder. Must answer fast; target under 300 ms server time.

Request:

```json
{ "machine_id": "a1b2c3d4e5f6" }
```

Response `200` (active):

```json
{
  "status": "active",
  "token": "<fresh JWT, 72h expiry>",
  "message": ""
}
```

Response `200` (lapsed; the HTTP status stays 200 so the hook can render the message cleanly):

```json
{
  "status": "lapsed",
  "message": "Your trial ended on 07/04/2026. This session is paused. Your drafts are untouched and everything resumes where you stopped after renewal: https://u2xai.com/renew"
}
```

### /mcp

The remote MCP endpoint, streamable HTTP. Key middleware runs before every tool call: it reads the same `licenses` table in-process and refuses `lapsed` and `revoked` keys with a tool error whose text matches the lapse message above. Tool list: [TBC: tool names and schemas, Phase B, depends on SCHEMA.md].

Student-side configuration, taught in the Course 09 remote lesson:

```json
{
  "mcpServers": {
    "u2xai-procurement": {
      "type": "http",
      "url": "https://u2xai-license.onrender.com/mcp",
      "headers": { "Authorization": "Bearer U2X-7F3K-92MD-Q4XR" }
    }
  }
}
```

### GET /health

Returns `200` and `{"ok": true}`. Render uses it as the health check path.

## 7. Token design

The session token is a JWT signed with `TOKEN_SIGNING_SECRET` (HS256). Claims:

```json
{ "sub": "<key>", "mid": "<machine_id>", "exp": "<now + GRACE_HOURS>" }
```

The hook caches the token in `.claude/.u2xai_token` and only calls `/session-check` when the cached token is missing or expired. The token is the offline grace: a valid cached token means the session proceeds without network. The server never needs to see or store issued tokens; expiry plus signature is the whole contract.

## 8. Lapse contract, client side

What the clients must do, and must not do, when they receive `lapsed`:

1. The session hook prints the server message and blocks the session start. It must not delete, lock, or alter any file.
2. `fetch.py` prints the server message and exits nonzero. It must not remove previously fetched data.
3. The MCP middleware refuses the call with the message text. Local skills fall back to local files where they have them, as designed in the skill pack.
4. Every lapse message names three things: the date the trial ended, the promise that local work is untouched and progress resumes, and the renewal link. Wording comes from the server, never hardcoded in clients.

## 9. Message slots

Two slots, both server-controlled: the `message` field on `/fetch/{course_id}` and on `/session-check`. Selection logic in `messages.py`:

1. Find campaigns where `slot` matches, `now()` is inside the window, and the trigger matches (the fetched course, or the key age in days).
2. Drop any campaign that would push this key past its `weekly_cap` (count rows in `message_log` for the last 7 days).
3. Return at most one message. Ties break by newest campaign. No match returns an empty string.

Frequency rules: at most one message per fetch, one per session check, and the per-campaign weekly cap (default 2). Lesson files never carry promotional text; the slots and email are the only channels.

## 10. Configuration

Environment variables, all set in Render:

| Variable | Value | Notes |
|---|---|---|
| `DATABASE_URL` | from Render Postgres | wired by the blueprint |
| `TOKEN_SIGNING_SECRET` | generated | `generateValue: true` in render.yaml |
| `TRIAL_DAYS` | 30 | the trial length lever |
| `GRACE_HOURS` | 72 | the offline grace lever |
| `R2_ACCOUNT_ID` | [TBC: from Cloudflare dashboard] | |
| `R2_ACCESS_KEY_ID` | secret, dashboard only | |
| `R2_SECRET_ACCESS_KEY` | secret, dashboard only | |
| `R2_BUCKET` | u2xai-course-bundles | |
| `EMAIL_API_KEY` | secret, dashboard only | [TBC: provider] |

## 11. render.yaml

```yaml
services:
  - type: web
    name: u2xai-license
    runtime: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: u2xai-licenses
          property: connectionString
      - key: TOKEN_SIGNING_SECRET
        generateValue: true
      - key: TRIAL_DAYS
        value: "30"
      - key: GRACE_HOURS
        value: "72"
      - key: R2_ACCESS_KEY_ID
        sync: false
      - key: R2_SECRET_ACCESS_KEY
        sync: false

databases:
  - name: u2xai-licenses
    plan: basic-1gb
```

## 12. Error catalog

Student-facing texts the server returns. Clients print them verbatim.

| Code | Status | Text |
|---|---|---|
| `key_invalid` | 401 | "This key was not recognized. Check for typos, or sign up at https://u2xai.com/start" |
| `lapsed` | 200/403 | See section 6. Always includes the date, the untouched-work promise, and the renewal link. |
| `revoked` | 403 | "This key has been deactivated. Contact support@u2xai.com" |
| `machine_limit` | 403 | See `/activate` in section 6. |
| `rate_limited` | 429 | "Too many requests. Wait a few minutes and try again." |
| `course_unknown` | 404 | "Course id not recognized. Valid ids: course-02 through course-21." |

## 13. Out of scope for V1, designed for

| Later feature | What V1 already carries for it |
|---|---|
| Stripe renewal | `expires_at` column; the webhook will update it and nothing else. |
| Org accounts and seats | `org_id` column, NULL for now. |
| Admin reports | `fetch_log` and `session_log` are the data source. A Render Cron Job groups by org and emails. |
| Certificate issuance | A future `/capstone` endpoint verifying a Course 22 run server-side. |
| Stretch-task ceiling answers | Served by `/mcp` once the connected dataset loads. |

## 14. Open inputs

1. [TBC: SCHEMA.md] The canonical column schema shared by local practice data and the Postgres views. Blocks the connected dataset migration and the MCP tool definitions.
2. [TBC: email provider] for key delivery and expiry reminders.
3. [TBC: final domain] and the signup page URL.
4. [TBC: support address] confirm support@u2xai.com is real before it ships in error texts.
