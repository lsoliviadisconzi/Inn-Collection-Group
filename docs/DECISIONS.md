# Inn Collection Group — Decision Log

> **Format**: Each decision records the question, the choice made, the rationale, and its current status.  
> **Status values**: `Decided` · `Open` · `Superseded`  
> **Last updated**: 2026-11-22

---

## Decided

### D1 — Deployment Topology
**Question**: Should this run on one machine, or be synced across several computers?  
**Decision**: One server process owns all data. Every other user connects via browser. The same code runs on `localhost` today and on a shared host machine later, switched via `--host`.  
**Rationale**: SQLite is reliable with one writer. Syncing copies between machines (via git, NFS, or SMB) causes divergence. No DevOps overhead, no distributed transactions.  
**Status**: `Decided`

---

### D2 — Database Engine
**Question**: SQLite or PostgreSQL?  
**Decision**: SQLite in WAL mode, on the host's local disk.  
**Migration trigger**: Only if multiple concurrent server processes are needed, or hosting moves off-site.  
**Rationale**: SQLite is embedded in Python stdlib, zero-configuration, and provides strong ACID consistency. WAL mode supports concurrent reads from the browser while a write is in progress.  
**Status**: `Decided`

---

### D3 — Browser localStorage for Review State
**Question**: Should menu-review.html continue saving review state in localStorage?  
**Decision**: No. localStorage is for UI preferences only (e.g. column visibility, scroll position). All review state is server-side in SQLite.  
**Rationale**: localStorage silently diverges across browsers and machines. It is the primary multi-computer bug in the current system.  
**Status**: `Decided` — fix is Step 1

---

### D4 — Data Layout
**Question**: Should the data directory structure be reorganised?  
**Decision**: Keep the current layout for now. Add one configurable `DATA_ROOT` path so the server can point to a different directory without code changes. The four zones are:
- `source/` — PDFs, raw crawls, CSV files. Never edited by the app.
- `working/` — `menus_md/`, `config/`. Edited by users. In git.
- `generated/` — `venue.json`, `menu-explorer-data.js`, `exports/`. Rebuildable. Excluded from git.
- `state/` — `icg_hospitality.sqlite3`. Backed up nightly.

**Status**: `Decided`

---

### D5 — Automated Rebuild on Menu Fix
**Question**: Should saving a menu fix trigger a rebuild of venue.json?  
**Decision**: Yes. A server-side job calls `build_venue_export.py --venue <name>` via subprocess after a successful menu write. The job uses a file lock (one rebuild at a time). The job exposes a status endpoint so the UI can poll it.  
**Rationale**: `build_venue_export.py` already supports `--venue`. The rebuild hook is a small subprocess call with no refactor needed.  
**Status**: `Decided` — Step 3

---

### D6 — Authentication
**Question**: When should authentication be added?  
**Decision**: Before the server is bound to anything beyond `127.0.0.1`. A simple session-cookie login (username + bcrypt-hashed password stored in SQLite) is sufficient for Phase 2. Full RBAC comes in Phase 3.  
**Rationale**: The current `--host` flag exposes file-rewrite endpoints to anyone on the LAN without credentials. This must be fixed before LAN deployment.  
**Status**: `Decided` — Step 5

---

### D7 — Kafoodie Scope Boundary
**Question**: Should this platform build a second allergen master, recipe BOM, and COGS engine alongside Kafoodie?  
**Decision**: No. Kafoodie is the authoritative master for recipes, ingredient BOMs, and allergen declarations. This platform:
- Reads Kafoodie data (crawl or export) for reconciliation and gap-register purposes.
- Flags items where Kafoodie allergen data is unset (gap, not a local override).
- Does not build a competing allergen engine or recipe master.

**Deferred to Kafoodie decision**: Supplier registry, Ingredient entities, Recipe entities, BOM entities, Allergen Declaration entities, NutritionProfile entities, COGS engine.  
**Status**: `Decided` — scope boundary firm for Phases 1–3

---

### D8 — Netlify
**Question**: Any residual Netlify deployment path?  
**Decision**: None. Netlify is fully decommissioned. No public hosting is planned.  
**Evidence**: Zero runtime or configuration references remain (`[Code-verified]` in doc 07).  
**Status**: `Decided`

---

### D9 — Backups
**Question**: How is data protected?  
**Decision**: 
- `icg_hospitality.sqlite3`: nightly `.backup` to a dated file (Python `sqlite3.Connection.backup()`).
- `menus_md/` and `config/`: in git.
- `generated/` and `exports/`: excluded from git; always rebuildable.
**Status**: `Decided` — Step 2

---

### D10 — AI Role
**Question**: What role does AI play in this system?  
**Decision**: Advisory only. AI suggestions are always staged for human review and approval before any data is changed. AI automation is later in the plan, after core data integrity is established.  
**Status**: `Decided`

---

### D11 — Orphaned File Deletions (O2 Resolved)
**Question**: Confirm deletion of confirmed orphaned files (Netlify remnants, stale root copies, leftover test data).  
**Decision**: Approved and executed. Deleted `pages/menus_md/`, `pages/documents/`, `pages/discovered_media.csv`, `pages/index.html`, `pages/Menu explorer — Inn Collection Group.html`, `exports/TestRegion/`, and `root.tree.md`.  
**Status**: `Decided` — Completed in Step 1

---

### D12 — Allergen Publication Hard Gate (O3 Resolved)
**Question**: What happens when a venue tries to publish or print a menu where an item has unset allergen flags (`is_pw_allergen_not_set = true` / missing allergen declarations)?  
**Decision**: Hard block. If any item on a menu has unset statutory allergen declarations, the system strictly refuses to mark the menu "Release Ready" or export print assets. An audit record is logged with the user, timestamp, menu name, and the specific blocking products.  
**Rationale**: Mandatory statutory compliance under FIC Regulation (EU) 1169/2011 and FIR 2014. Serving dishes with unverified allergens presents unacceptable guest health, civil liability, and criminal penalties.  
**Status**: `Decided` — Enforced in backend review validation and UI inspector

---

### D13 — Kafoodie Direct API Ingestion (O4 Resolved)
**Question**: How should fresh recipe, allergen, and nutrition data from Kafoodie enter the monolith?  
**Decision**: Direct Kafoodie REST API Ingestion. Replace fragile web crawl scrapers with an authenticated API client syncing directly with Kafoodie's backend.  
**Status**: `Decided` — Selected architecture for ongoing synchronization

---

## Open

### O1 — Outlet IDs for Dean Court and The Bull's Head Inn
**Question**: What are the Kafoodie outlet IDs for Dean Court and The Bull's Head Inn?  
**Investigation Evidence**: As documented in `inncollectiongroup.com_root/kafoodie/ALL_MENUS_CHECKLIST.md`, both venues have extracted Markdown menus in `menus_md/` but have no corresponding Kafoodie all-menus JSON crawl in `inncollectiongroup.com_root/kafoodie/`. Consequently, `build_venue_export.py` cannot generate `venue.json` for them until their Kafoodie outlet IDs or direct Kafoodie exports are provided.  
**Status**: `Open` — awaiting Kafoodie outlet identifiers from estate management / Kafoodie administrator

---

### O5 — EPOS Vendor & PLU Mapping Scope
**Question**: Which EPOS / till system does the Inn Collection Group estate run (Zonal Aztec, Tevalis, Oracle Micros, or other)?  
**Status**: `Open` — awaiting confirmation from estate IT / operations before scoping Step 7 EPOS adapter

---

## Superseded

### S1 — "Single Source of Truth" for venue.json
Withdrawn in doc 08. `venue.json` is a **generated artifact**, not an authoritative source. Replaced by D4 and the Data Authority Matrix in ARCHITECTURE.md.

### S2 — Microservices Architecture
Rejected in doc 11. Modular monolith decision is final for Phases 1–3.

### S3 — PostgreSQL for Phases 1–3
Withdrawn. PostgreSQL deferred to Phase 4+ (see D2).
