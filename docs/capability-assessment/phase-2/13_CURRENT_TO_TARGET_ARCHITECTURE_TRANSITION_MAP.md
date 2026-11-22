# Document 13 — Current-to-Target Architecture Transition Map

> **Knowledge Base** · Inn Collection Group (ICG) Hospitality Technology Workspace  
> **Document** 13 of 15 · Published: 2026-11-22  
> **Phase**: Phase 2 — Hospitality Technology Requirements, Target Architecture & Implementation Blueprint  
> **Evidence Standards**: `[Code-verified]` · `[Database-verified]` · `[Proposed]`

---

## 1. Executive Summary & Transition Philosophy

This document defines the transition strategy bridging the existing Inn Collection Group (ICG) software artifacts to the proposed target architecture.

The guiding transition principle is **asset preservation without architectural compromise**:
> *"Do not discard working software, verified data pipelines, or effective user interfaces simply because the overall platform needs to evolve. Equally, do not preserve technical debt or redundant directories out of inertia. Clearly categorize every existing component to maximize reuse while eliminating disconnects."*

Every file, interface, script, database structure, and data directory in the current repository is assessed and assigned an explicit architectural disposition.

---

## 2. Component Disposition Matrix

The seven disposition classifications define the future role of every repository asset:
* **Retain**: Existing implementation remains fully suitable as-is.
* **Extend**: Existing implementation is sound, but should be augmented with additional capabilities.
* **Rebuild**: Existing implementation is a static mockup or proof-of-concept that requires full re-engineering against active data structures.
* **Integrate**: Existing component is functional in isolation, but must be connected to upstream/downstream services.
* **Replace**: Existing solution should be superseded by a more robust mechanism.
* **Retire**: Existing component is redundant, orphaned, or obsolete.
* **Investigate**: Decision deferred pending business confirmation.

| Component / Artifact | Current Path | Current Role & Maturity | Recommended Disposition | Transition Rationale & Future Architectural Role | Evidence Base |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Menu Review UI** | `pages/menu-review.html` | Level 1: Operational document review tool (vanilla SPA). Synchronized PDF/MD viewer, structural triage. | **Extend** | Highly functional and well-architected. Augment with: (1) Direct dish editing; (2) Price validation; (3) One-click "Trigger Venue Rebuild" button. | `[Code-verified]` |
| **Discovered Media UI** | `pages/discovered-media.html` | Level 1: Operational media discovery and batch export SPA. Reads CSV client-side. | **Retain** | Performs its designated role cleanly. Retain as the primary media asset acquisition interface for marketing and digital teams. | `[Code-verified]` |
| **Menu Explorer UI** | `pages/menu-explorer.html` | Level 1: Operational multi-outlet explorer and cross-venue variance comparison tool. | **Extend** | Excellent cross-venue comparison capability. Extend by wiring it directly to the operational database / unified API, replacing static bundle dependency. | `[Code-verified]` |
| **Product Data UI** | `pages/product-data.html` | Level 3: Static prototype mockup. Hardcoded HTML table with dummy product records. | **Rebuild** | Wire layout to live `GET /api/products` and `venue.json:products[]`, transforming it into an active master product catalog with live search and SKU management. | `[Observed]` |
| **Launch Readiness UI** | `pages/launch-readiness.html` | Level 3: Client-side prototype simulation. Interactive sliders and milestone checkboxes without persistence. | **Rebuild** | Retain excellent UX wireframe; connect milestone checkboxes to `launch_tasks` in SQLite and populate readiness percentages from `venue.json:coverage`. | `[Observed]` |
| **F&B Role Cross-check** | `pages/fnb-crosscheck.html` | Level 3: Internal role-coverage analysis SPA. Encapsulates 40 operational requirements. | **Retain** | Retain as an internal auditing and onboarding artifact demonstrating compliance against F&B Coordinator operational duties. | `[Code-verified]` |
| **Chicken Liver Parfait** | `pages/recipes/chicken-liver-parfait...html` | Level 3: Static, rich dish specification demo (2,575 lines). Hardcoded culinary, costing, supplier data. | **Rebuild** | Refactor layout into a parameterized dynamic template (`pages/spec-book.html?id=<recipe_id>`) populated from the operational recipe database. | `[Code-verified]` |
| **Local Application Server** | `menu_review_server.py` | Level 1: Python stdlib HTTP server (615 lines). Serves APIs, static pages, and duplicate line fixes. | **Extend** | Proven, robust, zero-dependency core. Extend router to support REST endpoints for menus, products, recipes, and launch tasks. | `[Runtime-tested]` |
| **Review State Database** | `menu_review_state.sqlite3` | Level 1: Single-table SQLite database (`issue_reviews`, 1 record). Disk persistence. | **Extend** | Expand schema to encompass master data tables (`venues`, `products`, `recipes`, `menus`, `allergens`, `prices`, `launches`). Enable WAL mode. | `[Database-verified]` |
| **Menu Explorer Builder** | `build_menu_explorer.py` | Level 1: Operational offline build script (411 lines). Derives `menu-explorer-data.js` from Kafoodie JSONs. | **Integrate** | Retain deduplication and allergen mapping logic. Integrate into backend synchronization pipeline rather than running as disconnected offline script. | `[Code-verified]` |
| **Venue Export Engine** | `build_venue_export.py` | Level 1: Operational offline reconciliation engine (1,376 lines). Heuristic matching -> `venue.json`. | **Integrate** | The core intellectual property of the repo. Retain matching cascade; trigger automatically upon menu approval via server webhook. | `[Code-verified]` |
| **Venue Export Output** | `exports/<Region>/<Venue>/venue.json` | Level 2: Comprehensive canonical generated venue model. Currently unconsumed by interfaces. | **Integrate** | Connect as the authoritative data provider for rebuilt Product Data, Launch Readiness, and Spec Book interfaces. | `[Code-verified]` |
| **Master Markdown Menus** | `inncollectiongroup.com_root/menus_md/` | Master flat-file repository store (103 `.md` files). Consumed by server and build pipelines. | **Retain** | Retain as the authoritative physical menu card representation. | `[Code-verified]` |
| **Orphaned Markdown Copy** | `pages/menus_md/` | Redundant duplicate copy (103 `.md` files, 100% byte-for-byte identical to master). | **Retire** | Created solely for decommissioned Netlify static hosting. Delete upon business confirmation to eliminate data drift risk. | `[Code-verified]` |
| **Crawled Kafoodie Data** | `inncollectiongroup.com_root/kafoodie/` | Ingestion crawl files (`*_all_menus.json`). Source for recipes and preliminary allergens. | **Retain** | Retain as the upstream staging cache for recipe synchronization. | `[Data-verified]` |
| **Media CSV Snapshot** | `inncollectiongroup.com_root/discovered_media.csv` | Ingestion crawl file (1,438 lines) indexing photography and documents. | **Retain** | Retain as the static catalog for `pages/discovered-media.html`. | `[Data-verified]` |
| **Configuration Files** | `config/venues.json`, `aliases.json`, `rules.json` | Human-maintained JSON override files consumed by build pipelines. | **Retain** | Retain as operational configuration; eventually provide UI editor in platform settings. | `[Code-verified]` |

---

## 3. Reuse and Asset Salvage Assessment

The target architecture achieves a remarkably high rate of intellectual property reuse, avoiding the waste of a complete rewrite:

### 3.1 Reusable Code Assets (100% Retained)
* **Heuristic Matching Cascade (`build_venue_export.py`)**: The three-stage token overlap algorithm, alias resolution, and fuzzy string scoring (lines 423–530) represent battle-tested hospitality string reconciliation.
* **Atomic File Rewriting Engine (`menu_review_server.py`)**: The safe, atomic temporary-file replacement mechanism with fsync (`_remove_duplicate_lines`, lines 409–426) provides rock-solid document editing.
* **PDF Inspection & Locating Logic (`pages/menu-review.html`)**: The client-side PDF.js integration, text highlight coordinates, and dual-pane synchronization.
* **Batch Downloader with Domain Safety (`menu_review_server.py`)**: The safe URL validator, domain lock (`ASSET_HOST = www.inncollectiongroup.com`), and multi-status HTTP 207 handling (`_export_items`).

### 3.2 Reusable Data Assets (100% Retained)
* **Cleaned Markdown Menu Corpus**: 103 audited menu documents formatted strictly according to `docs/MENU-MD-SPEC.md`.
* **Kafoodie Outlet Cache**: Structured JSON datasets for 29 properties, complete with statutory allergen sequences and nutrition.
* **Venue Hierarchy Master**: Clean mapping of 29 venues across 7 operational regions with standardized slugs.

### 3.3 Reusable UX & Interface Concepts (100% Retained)
* **Single-Page Vanilla JS Architecture**: Zero npm dependencies, sub-50ms load times, and clean semantic DOM layouts.
* **Color System & Design Tokens**: Consistent visual hierarchy established in `pages/` (ICG brand colors, status chips, RAG indicators).
* **Launch Readiness UX**: The milestone checklist and spec-pack compilation wireframe from `pages/launch-readiness.html`.

---

## 4. Technical Debt, Redundancies & Architectural Conflicts

To reach the target architecture, four specific instances of technical debt must be addressed:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TECHNICAL DEBT RECONCILIATION                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. ORPHANED DUPLICATE DIRECTORY (pages/menus_md/)                      │
│ • Problem: 103 files duplicating master menus. Risk of silent drift.   │
│ • Action: Remove directory once business confirms Netlify removal.     │
├────────────────────────────────────────────────────────────────────────┤
│ 2. BROKEN LOOP: REVIEW QC -> VENUE EXPORT                              │
│ • Problem: Duplicate line fixes write to SQLite, but not venue.json.   │
│ • Action: Add webhook trigger to re-run build_venue_export.py on fix.   │
├────────────────────────────────────────────────────────────────────────┤
│ 3. DISCONNECTED CANONICAL ARTIFACT (venue.json)                        │
│ • Problem: Richest data model in the repo is unconsumed by interfaces. │
│ • Action: Re-wire product-data.html and launch-readiness.html to it.   │
├────────────────────────────────────────────────────────────────────────┤
│ 4. ISOLATED MOCKUP DOMAIN ENTITIES                                     │
│ • Problem: Parfait has supplier codes; Kafoodie has allergens; neither  │
│   talks to product-data.html.                                          │
│ • Action: Migrate entities into unified icg_hospitality.sqlite3 schema.│
└────────────────────────────────────────────────────────────────────────┘
```
