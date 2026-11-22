-- Migration 004: Menu status reviews persistence in SQLite
-- Eliminates client-side localStorage reliance for menu review state

CREATE TABLE IF NOT EXISTS menu_reviews (
  menu_name TEXT PRIMARY KEY,
  status TEXT NOT NULL DEFAULT 'pending',
  note TEXT NOT NULL DEFAULT '',
  updated_at TEXT NOT NULL,
  updated_by TEXT NOT NULL DEFAULT 'system'
);

CREATE INDEX IF NOT EXISTS idx_menu_reviews_status ON menu_reviews(status);
