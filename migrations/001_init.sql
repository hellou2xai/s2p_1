-- License server V1 schema. Idempotent: safe to run at every startup.

CREATE TABLE IF NOT EXISTS licenses (
    key             TEXT PRIMARY KEY,                 -- format: U2X-XXXX-XXXX-XXXX
    email           TEXT NOT NULL UNIQUE,
    org_id          TEXT,                             -- NULL in V1, used when org accounts arrive
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at      TIMESTAMPTZ NOT NULL,             -- created_at + TRIAL_DAYS in V1
    status          TEXT NOT NULL DEFAULT 'active',   -- active | revoked
    max_machines    INTEGER NOT NULL DEFAULT 2
);

CREATE TABLE IF NOT EXISTS activations (
    key             TEXT NOT NULL REFERENCES licenses(key),
    machine_id      TEXT NOT NULL,                    -- client-generated stable hash
    first_seen      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (key, machine_id)
);

CREATE TABLE IF NOT EXISTS fetch_log (
    id              BIGSERIAL PRIMARY KEY,
    key             TEXT NOT NULL REFERENCES licenses(key),
    course_id       TEXT NOT NULL,                    -- course-02 .. course-21
    fetched_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS fetch_log_key_time ON fetch_log (key, fetched_at);

CREATE TABLE IF NOT EXISTS session_log (
    id              BIGSERIAL PRIMARY KEY,
    key             TEXT NOT NULL REFERENCES licenses(key),
    machine_id      TEXT NOT NULL,
    checked_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    result          TEXT NOT NULL                     -- active | lapsed | revoked
);

CREATE TABLE IF NOT EXISTS campaigns (
    id              BIGSERIAL PRIMARY KEY,
    slot            TEXT NOT NULL,                    -- fetch | session
    trigger_course  TEXT,                             -- fire when this course is fetched, NULL = any
    trigger_after_day INTEGER,                        -- fire when key age >= N days, NULL = any
    message         TEXT NOT NULL,
    starts_at       TIMESTAMPTZ NOT NULL,
    ends_at         TIMESTAMPTZ NOT NULL,
    weekly_cap      INTEGER NOT NULL DEFAULT 2
);

CREATE TABLE IF NOT EXISTS message_log (
    id              BIGSERIAL PRIMARY KEY,
    key             TEXT NOT NULL REFERENCES licenses(key),
    campaign_id     BIGINT NOT NULL REFERENCES campaigns(id),
    sent_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
