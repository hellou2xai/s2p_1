"""Database pool, migrations, and query helpers."""

import os
from datetime import datetime, timezone
from pathlib import Path

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

_pool: ConnectionPool | None = None


def pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            os.environ["DATABASE_URL"],
            min_size=1,
            max_size=10,
            kwargs={"row_factory": dict_row},
        )
    return _pool


def run_migrations() -> None:
    migrations_dir = Path(__file__).resolve().parent.parent / "migrations"
    with pool().connection() as conn:
        for sql_file in sorted(migrations_dir.glob("*.sql")):
            conn.execute(sql_file.read_text(encoding="utf-8"))


def get_license(key: str) -> dict | None:
    with pool().connection() as conn:
        return conn.execute("SELECT * FROM licenses WHERE key = %s", (key,)).fetchone()


def license_status(row: dict) -> str:
    """Derived at request time, never stored: revoked | lapsed | active."""
    if row["status"] == "revoked":
        return "revoked"
    if datetime.now(timezone.utc) > row["expires_at"]:
        return "lapsed"
    return "active"


def create_license(key: str, email: str, trial_days: int) -> dict:
    with pool().connection() as conn:
        return conn.execute(
            "INSERT INTO licenses (key, email, expires_at) "
            "VALUES (%s, %s, now() + make_interval(days => %s)) "
            "RETURNING *",
            (key, email, trial_days),
        ).fetchone()


def extend_license(key: str, days: int):
    """Expiry becomes max(current, now + days). Idempotent for webhook
    retries; a renewal payment extends, a re-applied event changes nothing."""
    with pool().connection() as conn:
        row = conn.execute(
            "UPDATE licenses SET expires_at = GREATEST(expires_at, now() + make_interval(days => %s)) "
            "WHERE key = %s RETURNING expires_at",
            (days, key),
        ).fetchone()
        return row["expires_at"]


def email_exists(email: str) -> bool:
    with pool().connection() as conn:
        row = conn.execute("SELECT 1 FROM licenses WHERE email = %s", (email,)).fetchone()
        return row is not None


def get_license_by_email(email: str) -> dict | None:
    with pool().connection() as conn:
        return conn.execute("SELECT * FROM licenses WHERE email = %s", (email,)).fetchone()


def courses_fetched(key: str) -> int:
    with pool().connection() as conn:
        row = conn.execute(
            "SELECT count(DISTINCT course_id) AS n FROM fetch_log WHERE key = %s", (key,)
        ).fetchone()
        return row["n"]


def delete_activations(key: str) -> int:
    with pool().connection() as conn:
        result = conn.execute("DELETE FROM activations WHERE key = %s", (key,))
        return result.rowcount


def machine_count(key: str) -> int:
    with pool().connection() as conn:
        row = conn.execute(
            "SELECT count(*) AS n FROM activations WHERE key = %s", (key,)
        ).fetchone()
        return row["n"]


def upsert_activation(key: str, machine_id: str) -> None:
    with pool().connection() as conn:
        conn.execute(
            "INSERT INTO activations (key, machine_id) VALUES (%s, %s) "
            "ON CONFLICT (key, machine_id) DO UPDATE SET last_seen = now()",
            (key, machine_id),
        )


def machine_known(key: str, machine_id: str) -> bool:
    with pool().connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM activations WHERE key = %s AND machine_id = %s",
            (key, machine_id),
        ).fetchone()
        return row is not None


def log_fetch(key: str, course_id: str) -> None:
    with pool().connection() as conn:
        conn.execute(
            "INSERT INTO fetch_log (key, course_id) VALUES (%s, %s)", (key, course_id)
        )


def fetches_last_24h(key: str) -> int:
    with pool().connection() as conn:
        row = conn.execute(
            "SELECT count(*) AS n FROM fetch_log "
            "WHERE key = %s AND fetched_at > now() - interval '24 hours'",
            (key,),
        ).fetchone()
        return row["n"]


def log_session(key: str, machine_id: str, result: str) -> None:
    with pool().connection() as conn:
        conn.execute(
            "INSERT INTO session_log (key, machine_id, result) VALUES (%s, %s, %s)",
            (key, machine_id, result),
        )
