-- Migration 001: Baseline schema
-- Captures the existing issue_reviews table (already in production).
-- The migration runner checks PRAGMA user_version; this file is applied
-- when user_version < 1 and sets it to 1 on completion.

CREATE TABLE IF NOT EXISTS issue_reviews (
    menu_name   TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    issue_id    TEXT NOT NULL,
    status      TEXT NOT NULL,
    note        TEXT NOT NULL DEFAULT '',
    updated_at  TEXT NOT NULL,
    PRIMARY KEY (menu_name, source_hash, issue_id)
);
