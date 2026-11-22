# Inn Collection Group — Architecture

> **Status**: Active Living Document  
> **Last updated**: 2026-11-22  
> **Evidence key**: `[Code-verified]` · `[Database-verified]` · `[Observed]` · `[Proposed]`

---

## 1. What This System Is

A local hospitality management platform for the Inn Collection Group (ICG) estate: 29 inns across 7 regions in England and Wales.

Its scope (confirmed):
- Menu QC: side-by-side PDF/Markdown review and triage
- Menu data: multi-venue menu markdown files, section and item catalogue
- Venue export: heuristic reconciliation of printed menus to Kafoodie recipes
- Media discovery: batch export of website media assets
- Launch tracking: milestone and venue sign-off workflows
- Multi-site explorer: cross-venue menu variance and gap analysis

Its scope (deferred — see DECISIONS.md D7):
- Recipe Bills of Materials, ingredient costing, COGS
- Allergen master engine
- EPOS adapter and PLU mapping
- Full role-based access control

---

## 2. Current State

### 2.1 Runtime

| Component | File | Status |
|:---|:---|:---|
| Application server | `menu_review_server.py` | `[Code-verified]` — Python stdlib `ThreadingHTTPServer`, 615 lines |
| Menu review UI | `pages/menu-review.html` | `[Code-verified]` — operational |
| Discovered media UI | `pages/discovered-media.html` | `[Code-verified]` — operational |
| Menu explorer UI | `pages/menu-explorer.html` | `[Code-verified]` — operational |
| Product data UI | `pages/product-data.html` | `[Observed]` — static prototype, hardcoded HTML |
| Launch readiness UI | `pages/launch-readiness.html` | `[Observed]` — client-side simulation, no persistence |
| F&B role cross-check | `pages/fnb-crosscheck.html` | `[Observed]` — static analysis SPA (~40 requirements) |
| Index redirect | `pages/index.html` | `[Code-verified]` — byte-identical to `menu-explorer.html`, redundant |
| Venue export build | `build_venue_export.py` | `[Code-verified]` — operational |
| Menu explorer build | `build_menu_explorer.py` | `[Code-verified]` — operational |

### 2.2 Data

| Store | Path | Role | Status |
|:---|:---|:---|:---|
| Menu markdown files | `inncollectiongroup.com_root/menus_md/*.md` | Authoritative working menus | `[Code-verified]` |
| Kafoodie recipe crawl | `inncollectiongroup.com_root/kafoodie/` | Authoritative recipe/allergen source | `[Code-verified]` |
| Venue configs | `config/venues.json` | Venue registry | `[Code-verified]` |
| Alias rules | `config/aliases.json` | Dish-to-recipe heuristic rules | `[Code-verified]` |
| Generated venue export | `exports/<Region>/<Venue>/venue.json` | Compiled snapshot — not a source of truth | `[Code-verified]` |
| Explorer bundle | `pages/menu-explorer-data.js` | Generated JS bundle (9.0 MB, 29 venues) | `[Code-verified]` |
| Review state DB | `menu_review_state.sqlite3` | One table: `issue_reviews` | `[Database-verified]` |
| Browser localStorage | `pages/menu-review.html` lines 437–438 | Duplicate review state — **to be removed** | `[Code-verified]` |

### 2.3 Known Issues in Current State

| Ref | Issue | Fix |
|:---|:---|:---|
| I-01 | SQLite journal mode is `delete`, not WAL | Enable WAL mode at startup (Step 2) |
| I-02 | Review state saved in both SQLite and localStorage | Remove localStorage path from menu-review.html (Step 1) |
| I-03 | Server binds to `127.0.0.1` by default; `--host` flag is unauthenticated | Add minimal session auth before exposing to LAN (Step 5) |
| I-04 | Python `tuple[...]` annotations require ≥ 3.9 (not 3.8 as documented) | Correct docs; keep 3.9+ requirement |
| I-05 | `pages/menus_md/` is an orphaned second copy of menus | Delete after confirmation |
| I-06 | `pages/documents/` is a duplicate of `inncollectiongroup.com_root/documents/` | Delete after confirmation |
| I-07 | `pages/discovered_media.csv` duplicates `inncollectiongroup.com_root/discovered_media.csv` | Delete after confirmation |
| I-08 | `exports/TestRegion/` is leftover test data | Delete |
| I-09 | `pages/index.html` is byte-identical to `menu-explorer.html` | Delete or keep as simple redirect |
| I-10 | `pages/Menu explorer — Inn Collection Group.html` is a stale copy | Delete |
| I-11 | `root.tree.md` and `root_tree.md` both exist at root | Delete `root_tree.md` (the one without dot) is the keeper — confirm |

---

## 3. Target State

### 3.1 Topology (Decision D1)

```
┌─────────────────────────────────────────────────┐
│          ONE HOST MACHINE (server process)        │
│                                                   │
│  menu_review_server.py  ←─── Python stdlib        │
│  ├── routing/           modules, no frameworks    │
│  ├── services/                                    │
│  ├── db/                SQLite WAL                │
│  └── jobs/              rebuild with lock         │
│                                                   │
│  data/                                            │
│  ├── source/   PDFs, crawls, CSV  (read-only)     │
│  ├── working/  menus_md, config   (edited)        │
│  ├── generated/ venue.json, explorer-data.js      │
│  │             (rebuildable, excluded from git)   │
│  └── state/    icg_hospitality.sqlite3            │
│                                                   │
│  --host 127.0.0.1  (default: local only)          │
│  --host 0.0.0.0    (LAN access, requires login)   │
└─────────────────────────────────────────────────┘
         ▲  ▲  ▲
         │  │  │  HTTP (browser)
     [User 1][User 2][User 3]
```

One server process owns all data. All users connect via browser. The same codebase runs on a local laptop today and on a shared host machine later — switched by `--host`.

### 3.2 Database (Decision D2)

- **Engine**: SQLite 3 in WAL mode, stored on the host's local disk
- **Database file**: `menu_review_state.sqlite3` (renamed → `icg_hospitality.sqlite3` when schema grows)
- **Migration mechanism**: numbered migration scripts run at server startup
- **Backup**: nightly `.backup` to a dated file; `menus_md/` and `config/` are in git

**Migration boundary**: PostgreSQL only if two or more server processes are needed, or hosting moves off-site.

### 3.3 Module Decomposition (Target, Phase 1–3)

```
REST ROUTING & DISPATCH
├── 1. Menu Management       — CRUD menus, sections, items; lifecycle states
├── 2. Multi-Site Recon      — 29-inn directory, heuristic matcher, explorer
├── 3. Media & Document QC   — menu-review, discovered-media, batch export
├── 4. Launch Orchestrator   — campaign milestones, venue sign-offs, spec books
├── 5. Governance & Audit    — users, sessions, append-only event log
│
└── DEFERRED (after D7 Kafoodie decision)
    ├── 6. Product & Recipe  — SKU catalogue, BOM, recipe formulation
    ├── 7. Food Safety        — 14 FIR allergen engine, compliance gates
    ├── 8. Commercial Engine  — COGS, GP%, price tiers
    ├── 9. Supplier & Purchase — purveyor registry, pack sizes
    └── 10. EPOS Adapter      — PLU codes, till configuration
```

### 3.4 Core Entities (Phase 1–3)

Persisted in SQL from Phase 1: `Organisation`, `Region`, `Venue`, `Menu`, `MenuSection`, `MenuItem`, `VenueOffering`, `Price`, `SourceDocument`, `IssueReview`, `LaunchCampaign`, `LaunchTask`, `LaunchVenueStatus`, `User`, `AuditEvent`.

Deferred: `Supplier`, `SupplierProduct`, `Ingredient`, `Recipe`, `RecipeVersion`, `RecipeBOM`, `CommercialProduct`, `ProductCode`, `AllergenDeclaration`, `NutritionProfile`, `VerificationRecord`.

### 3.5 Security Model

- **Phase 1 (localhost only)**: No authentication. Single user. `--host 127.0.0.1`.
- **Phase 2 (LAN)**: Minimal session-cookie login (username + password, stored hashed in SQLite). Every write records `updated_by`. No roles yet.
- **Phase 3+**: Role-based access control — Chef, F&B Coordinator, Compliance Officer, Commercial Manager, Systems Admin.
- **Never**: Public hosting. Netlify is decommissioned. No cloud deployment planned.

---

## 4. Data Authority Matrix

| Domain | Authoritative Source | This Platform's Role |
|:---|:---|:---|
| Recipes & culinary formulations | **Kafoodie** | Read-only mirror / reconciliation |
| Allergen declarations | **Kafoodie** | Read-only flag; gap-register only |
| Printed menu copy | **Menu markdown files** (`menus_md/`) | Authoritative; edited here |
| Venue identity & amenities | `config/venues.json` + website crawl | Authoritative |
| Commercial prices | Menu markdown + future Commercial module | Authoritative here |
| Review workflow state | SQLite `issue_reviews` | Authoritative here (not localStorage) |
| Generated exports | `exports/*/venue.json` | Derived artifact — always rebuildable |

---

## 5. What Is Not This System

- **Not a public website.** No hosting, no CDN, no Netlify.
- **Not a POS system.** EPOS/till integration is deferred.
- **Not an allergen master.** Kafoodie owns this until D7 is resolved.
- **Not a microservices architecture.** Modular monolith only.
