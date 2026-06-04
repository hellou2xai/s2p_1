# U2xAI License Server (s2p_1)

The server behind the S2P course pack: key issuance, per-course data delivery, session checks, and message slots. V1 issues free 30-day keys with everything included. Payments arrive later; renewal will flip one column (`expires_at`) and nothing shipped to students changes.

The full contract (endpoints, response shapes, lapse behavior, message rules) lives in the course repository at `Platform/License_Server_Spec.md`. This README covers running and deploying the code.

## Layout

```
render.yaml            Render blueprint: web service + Postgres, all env vars declared
requirements.txt
migrations/001_init.sql   idempotent schema, runs at every startup
app/
  main.py              FastAPI routes: /health, /signup, /activate, /fetch/{course}, /session-check
  auth.py              key format, bearer extraction, 72-hour session tokens (JWT)
  bundles.py           presigned Cloudflare R2 URLs for the 20 course bundles
  messages.py          campaign selection for the fetch and session message slots
  db.py                pool, migrations, queries, derived license status
```

## Deploy to Render

1. Push this repository to GitHub (already done if you are reading this there).
2. In the Render dashboard: New, Blueprint, pick this repo. Render reads `render.yaml`, creates the `u2xai-license` web service (plan: starter, always warm) and the `u2xai-licenses` Postgres (plan: basic-1gb), wires `DATABASE_URL`, and deploys.
3. Set the three R2 secrets in the service's Environment tab: `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, and `R2_SECRET_ACCESS_KEY`. Everything else is declared in the blueprint.
4. Upload the 20 course bundles to the private R2 bucket `u2xai-course-bundles` under `bundles/course-NN.zip`, each with a `sha256` metadata entry. The bundle splitter in the course repository produces and uploads them.
5. Check `https://u2xai-license.onrender.com/health` returns `{"ok": true}`.

Every later `git push` to the default branch redeploys automatically.

## Run locally

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set DATABASE_URL=postgresql://localhost/u2xai_dev
set TOKEN_SIGNING_SECRET=dev-secret-not-for-production
uvicorn app.main:app --reload
```

Migrations run automatically at startup. R2 env vars are only needed for `/fetch`.

## Policy levers (no redeploy needed for message changes)

| Lever | Where |
|---|---|
| Trial length | `TRIAL_DAYS` env var (30) |
| Offline grace | `GRACE_HOURS` env var (72) |
| Message campaigns | `campaigns` table rows: slot, trigger, window, weekly cap |
| Revoke a key | set `licenses.status = 'revoked'` |
| Extend or renew | update `licenses.expires_at` |

## Not in V1, designed for

Stripe webhook (renewal), org accounts and seats (`org_id` column exists), admin reports (built from `fetch_log` and `session_log`), the `/mcp` connected-mode endpoint (Phase B, blocked on the canonical schema document), and certificate issuance.
