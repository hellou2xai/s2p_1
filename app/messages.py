"""Campaign selection for the two message slots (fetch, session).

Rules, in order:
1. Campaign window contains now() and the slot matches.
2. Trigger matches: the fetched course, or the key age in days. NULL matches anything.
3. The per-campaign weekly cap for this key is not exhausted.
4. At most one message returned. Ties break by newest campaign. No match: empty string.
"""

from .db import pool


def pick_message(key: str, slot: str, course_id: str | None = None) -> str:
    with pool().connection() as conn:
        row = conn.execute(
            """
            SELECT c.id, c.message
            FROM campaigns c
            JOIN licenses l ON l.key = %(key)s
            WHERE c.slot = %(slot)s
              AND now() BETWEEN c.starts_at AND c.ends_at
              AND (c.trigger_course IS NULL OR c.trigger_course = %(course_id)s)
              AND (c.trigger_after_day IS NULL
                   OR now() >= l.created_at + make_interval(days => c.trigger_after_day))
              AND (SELECT count(*) FROM message_log m
                   WHERE m.key = %(key)s AND m.campaign_id = c.id
                     AND m.sent_at > now() - interval '7 days') < c.weekly_cap
            ORDER BY c.id DESC
            LIMIT 1
            """,
            {"key": key, "slot": slot, "course_id": course_id},
        ).fetchone()
        if row is None:
            return ""
        conn.execute(
            "INSERT INTO message_log (key, campaign_id) VALUES (%s, %s)",
            (key, row["id"]),
        )
        return row["message"]
