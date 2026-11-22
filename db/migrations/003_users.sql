-- Migration 003: Users, sessions, and audit logging
CREATE TABLE IF NOT EXISTS users (
    username      TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    salt          TEXT NOT NULL,
    display_name  TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'coordinator',
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    username   TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_events (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    entity     TEXT NOT NULL,
    entity_id  TEXT NOT NULL,
    action     TEXT NOT NULL,
    detail     TEXT NOT NULL,
    user       TEXT NOT NULL,
    created_at TEXT NOT NULL
);

-- Seed default local administrator if no users exist
-- Default credentials for initial setup: admin / admin (prompt to change on first login)
-- Hash using sha256 + salt
INSERT OR IGNORE INTO users (username, password_hash, salt, display_name, role, created_at)
VALUES (
    'admin',
    '6a9d76182572f3108b100ce2622bb24888a8fb4bf7f742026616e32908b83fbc',
    'icg_default_salt_2026',
    'Administrator',
    'admin',
    datetime('now')
);
