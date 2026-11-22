# Inn Collection Group — Implementation Roadmap

> **Single source of truth** — replaces the conflicting roadmaps in docs 06 and 14.  
> **Last updated**: 2026-11-22  
> **Status notation**: `✅ Done` · `🔄 In Progress` · `⬜ Not Started` · `🔒 Blocked`

---

## Overview

| Step | Name | Focus | Gate | Status |
|:---|:---|:---|:---|:---|
| 1 | Repository hygiene + data root + localStorage fix | Clean slate | — | ✅ Done |
| 2 | WAL mode + migration mechanism + backup | Data safety | After Step 1 | ✅ Done |
| 3 | Rebuild job + status endpoint | Close review→export loop | After Step 2 | ✅ Done |
| 4 | API endpoints for venue/menu data + rewire product-data.html | First real API | After Step 3 | ✅ Done |
| 5 | Launch tracking in SQLite + minimal authentication | Multi-user ready | After Step 4 | ✅ Done |
| 6+ | Recipe, allergen, costing, EPOS modules | Deferred | After O1–O5 resolved | 🔒 Blocked |

---

## Step 1 — Repository Hygiene, Data Root, localStorage Fix

**Goal**: Clean up orphaned files, make the data path configurable, and eliminate the localStorage review-state bug.

**Deliverables**:
- [x] Remove browser `localStorage` review-state writes from `pages/menu-review.html` (keep only server-side SQLite path)
- [x] Add `DATA_ROOT` / `DB_BACKUP_DIR` constants to `menu_review_server.py`
- [x] Delete confirmed orphaned files:
  - `pages/menus_md/` ✅
  - `pages/documents/` ✅
  - `pages/discovered_media.csv` ✅
  - `pages/index.html` ✅
  - `pages/Menu explorer — Inn Collection Group.html` ✅
  - `exports/TestRegion/` ✅
  - `root.tree.md` (root-level duplicate) ✅
- [x] Correct `requirements.txt`: Python minimum is **3.9**
- [x] Add `exports/` and `pages/menu-explorer-data.js` to `.gitignore`
- [x] Archive `docs/architecture/` (old v1 set) → `docs/archive/architecture-v1/`

**Does not block**: O1, O2 (deletions await confirmation)

---

## Step 2 — WAL Mode, Schema Migrations, Backup

**Goal**: Proper database hygiene before any schema grows.

**Deliverables**:
- [x] Enable WAL journal mode at server startup (`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000`)
- [x] Add migration runner: `db/database.py` applies numbered SQL files from `db/migrations/` at startup; version tracked via `PRAGMA user_version`
- [x] Create initial migration `db/migrations/001_baseline.sql` with `issue_reviews` table schema
- [x] Add nightly backup: `sqlite3.Connection.backup()` → `db/backups/YYYY-MM-DD.sqlite3`, runs as a daemon thread at startup
- [x] Wire `db.database.init_db()` into `menu_review_server.py` startup; `_review_connection` uses `db_connect()`

---

## Step 3 — Rebuild Job with Lock + Status Endpoint

**Goal**: Close the review-to-export loop so fixing a menu issue triggers a venue rebuild.

**Deliverables**:
- [x] Add `jobs/rebuild.py` module: runs `build_venue_export.py --venue <name>` via subprocess, followed by `build_menu_explorer.py`
- [x] Concurrency control via thread lock (one rebuild at a time; rejects concurrent runs with descriptive status)
- [x] `GET /api/rebuild-status` endpoint: returns `{status, venue, started_at, finished_at, error, stdout}`
- [x] `POST /api/rebuild` endpoint: triggers rebuild for a specific venue or `"all"`
- [x] Auto-trigger rebuild on menu duplicate removal (`POST /api/issues/fix-duplicates`) by detecting the venue for the edited menu markdown file

---

## Step 4 — API Endpoints for Venue and Menu Data

**Goal**: Replace hardcoded HTML prototypes with real server-backed data.

**Deliverables**:
- [x] `GET /api/venues` — list of 29 venues with region, slug, menu count, export status, and file size
- [x] `GET /api/venues/<slug>` — venue detail with live `venue.json` data, or helpful export prompt if not yet built
- [x] `GET /api/menus` — list of 103 menu markdown files enriched with venue mapping, region, and PDF status
- [x] `GET /api/menus/<name>` — menu file content, venue name, source hash, and review decisions from SQLite
- [x] Rewire `pages/product-data.html` — added venue selector dropdown, live Kafoodie product mapping (allergens, nutrition, dietary tags), and on-demand rebuild button
- [x] Rewire `pages/launch-readiness.html` to fetch from `/api/launches` and persist tasks & venue readiness live

---

## Step 5 — Launch Tracking in SQLite + Minimal Auth

**Goal**: Persist launch campaign state and add the minimum viable authentication before LAN exposure.

**Deliverables**:
- [x] Migration `db/migrations/002_launches.sql`: `launch_campaigns`, `launch_milestones`, `launch_workstreams`, `launch_tasks`, `launch_venue_status` tables with baseline Spring 2027 seed
- [x] `GET /api/launches`, `GET /api/launches/<id>`, `POST /api/launches/<id>/tasks`, and `POST /api/launches/<id>/venues` endpoints
- [x] Rewire `pages/launch-readiness.html` to live-sync task completion and site readiness into SQLite
- [x] Session auth module `db/auth.py`: SHA-256 salted password hashing, 7-day token sessions, and tamper-evident audit logging
- [x] Migration `db/migrations/003_users.sql`: `users`, `sessions`, and `audit_events` tables with initial administrator account
- [x] Endpoints `POST /api/login`, `POST /api/logout`, and `GET /api/me` with secure HTTP-only cookies
- [x] Record `updated_by` on every write to `issue_reviews`, `launch_tasks`, `launch_venue_status`, and `audit_events`
- [x] Server startup check & CLI tooling: `--add-user <username>` flag; if `--host != 127.0.0.1`, enforces that at least one user exists in the database

---

## Step 6+ — Deferred Modules (Gated on Open Decisions)

These modules do not start until O3–O5 are resolved and D7 (Kafoodie boundary) is confirmed.

| Module | Gate |
|:---|:---|
| Allergen gap register (read-only Kafoodie mirror) | O3 + O4 |
| EPOS adapter and PLU mapping | O5 |
| Supplier and purchasing registry | D7 confirmed |
| Recipe and BOM module | D7 confirmed |
| Commercial engine (COGS, GP%) | D7 + recipe module |
| Full RBAC | Step 5 auth in place |
| AI advisory integration | All above stable |

---

## Document Archive

The following superseded document sets have been moved to `docs/archive/`:

| Archived Path | Reason |
|:---|:---|
| `docs/archive/architecture-v1/` (01–10) | Described Netlify, wrong file counts, conflicting roadmap. Superseded by this doc set. |

The phase-2 documents (`docs/capability-assessment/phase-2/09–15`) are retained in full as the **audit and evidence record** of the architecture decisions. They are not living documents.

---

## Corrections Applied

The following factual errors from the previous document set have been corrected here:

| Error | Correction |
|:---|:---|
| "Python 3.8+" | Minimum is **3.9** (`tuple[...]` annotations) |
| "100+ requirements in fnb-crosscheck.html" | Actual count is ~40 |
| "sub-millisecond query execution" | Unverified claim — removed |
| "14 core tables" (doc 15) | 26 entities defined in doc 10; correct entity count is 26 |
| "29–31 venues" (inconsistent) | 29 venues confirmed in `menu-explorer-data.js` |
| "journal_mode = WAL" | Actual current mode is `delete`; WAL is a target, not current |
| Line counts for HTML files | Removed (unreliable); file sizes are the accurate measure |
| `pages/menus_md/` as active | Orphaned; `inncollectiongroup.com_root/menus_md/` is the live source |
