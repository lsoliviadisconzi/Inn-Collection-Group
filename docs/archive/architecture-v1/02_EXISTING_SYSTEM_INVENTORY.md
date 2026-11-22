# 02 — Existing System Inventory

## 1. Overview of Interfaces & Components

The repository comprises seven primary web interfaces, two backend HTTP/API services, two automated build and reconciliation pipelines, configuration datasets, and source archives.

---

## 2. Detailed Interface Inventory

### 2.1 Interface 1: Chicken Liver Parfait — Product Page

* **Routes**:
  * Production route: `/recipes/chicken-liver-parfait-the-lindisfarne-inn.html`
  * Aliases / Redirects in `netlify.toml`: `/recipes`, `/recipes/` -> `/recipes/chicken-liver-parfait.html`
  * Dev Prototypes: `_dev/Chicken Liver Parfait · The Lindisfarne Inn.html`, `_dev/Chicken Liver Parfait · The Lindisfarne Inn-v2.html`, `_dev/Chicken Liver Parfait Carousel.html`, `_dev/Chicken Liver Parfait_ Reel Storyboard.html`
* **Source File**: `pages/recipes/chicken-liver-parfait-the-lindisfarne-inn.html` (2,575 lines)
* **Technology Stack**:
  * Vanilla HTML5, modern CSS custom properties (variables), native CSS Grid & Flexbox.
  * Typography: Google Fonts (`Barlow Semi Condensed`, `Cormorant Garamond`).
  * Zero runtime JavaScript dependencies (no React, Vue, jQuery).
* **Architecture & Interaction Design**:
  * Dark luxury aesthetic (`--bg: #0b0a09; --gold: #d4af6a;`).
  * "Hub-and-spoke" interaction pattern: a central plated dish photo with interactive modal sheets that grow dynamically out of buttons upon selection.
  * Comprehensive operational coverage:
    1. *Identity*: Autumn/Winter 2026 starter for The Lindisfarne Inn.
    2. *Recipe & Composition*: Ingredients, exact grammages, prep method.
    3. *Procurement & Suppliers*: Specific supplier codes (e.g. Brakes, local bakery), pack sizes, shelf life.
    4. *Plating & Standards*: Step-by-step assembly, temperature standards, crockery specs.
    5. *Allergen & Dietary*: Comprehensive allergen breakdown (Gluten, Milk, Eggs, Sulphites).
    6. *Nutrition & Costing*: Gross profit margin target (72%), portion cost calculation, calories per serving.
* **Evidence Classification**:
  * `[OBSERVED]`: High-fidelity, responsive UI with functioning interactive tabs, modal sheets, and zoomable photography.
  * `[CODE-VERIFIED]`: **Completely static and hardcoded**. Contains zero API requests (`fetch` / `XMLHttpRequest`). All recipe numbers, supplier names, and nutritional values are inlined directly into HTML/CSS attributes.
* **Limitations**: It is currently an isolated showcase dish rather than a dynamic view generated from a recipe database.

---

### 2.2 Interface 2: Discovered Media

* **Routes**: `/discovered-media`, `/pages/discovered-media.html`
* **Source File**: `pages/discovered-media.html` (670 lines)
* **Data Sources**: `pages/discovered_media.csv` (and `inncollectiongroup.com_root/discovered_media.csv`) containing 1,500+ media entries scraped from the live domain.
* **Technology Stack**:
  * Vanilla client-side Single-Page Application (SPA).
  * Inlines client-side CSV parser and DOM rendering engine.
* **Functional Capabilities**:
  * Dynamic multi-filtering by Region, Venue, Category (Food, Drinks, Property, Events), and File Type (PDF, JPEG, PNG, WEBP).
  * Media preview gallery with lazy loading and fallback handling.
  * Selection state management (Select All, Invert, Clear).
  * Batch export integration: issues `POST /api/export` payload containing selected media items.
* **Evidence Classification**:
  * `[OBSERVED]`: Rapid filtering across hundreds of media assets; multi-select checkbox management; detailed download progress modal.
  * `[CODE-VERIFIED]`: When running against `menu_review_server.py`, `POST /api/export` writes downloaded files to the local `exports/` folder grouped as `<Region>/<Venue>/<Category>/<timestamp>/`. When running on Netlify (`netlify/functions/api.py`), it creates and streams an in-memory ZIP archive (`icg-media-export.zip`).
* **Limitations**: Relies on a static snapshot CSV. Does not auto-detect newly uploaded media without re-running the external crawler.

---

### 2.3 Interface 3: F&B Role Cross-check

* **Routes**: `/fnb-crosscheck`, `/pages/fnb-crosscheck.html`
* **Source File**: `pages/fnb-crosscheck.html` (520 lines)
* **Data Sources**: Inlined JavaScript array of 100+ operational requirements across hospitality personas.
* **Technology Stack**:
  * Vanilla HTML, CSS Grid, client-side JS data filtering.
* **Functional Capabilities**:
  * Benchmarks F&B operational requirements against system capabilities.
  * Coverage classification: `Full`, `Partial`, `Not Yet`, `Planned`, `Manual`, `Human Only`.
  * Filtering by operational domain (Kitchen, Front of House, Central Procurement, Safety & Compliance) and persona.
  * Gap analysis metrics showing percentage of software coverage vs human dependency.
* **Evidence Classification**:
  * `[OBSERVED]`: Clean requirements dashboard with real-time summary statistics and filterable requirement cards.
  * `[CODE-VERIFIED]`: Completely client-side and standalone. Contains zero network requests. The dataset is an internal static audit model.
* **Limitations**: Requirements are not synchronized with GitHub issues, Jira, or real codebase testing results.

---

### 2.4 Interface 4: Launch Readiness

* **Routes**: `/launch-readiness`, `/pages/launch-readiness.html`
* **Source File**: `pages/launch-readiness.html` (710 lines)
* **Data Sources**: Hardcoded JavaScript data structures defining menu rollout workstreams, milestones, and venue checklists.
* **Technology Stack**:
  * Vanilla client-side JS application.
* **Functional Capabilities**:
  * Milestone tracking (e.g., Recipe Signoff, Allergen Audit, EPOS Programming, Staff Briefing, Print Delivery).
  * Multi-venue launch readiness matrix across 31 properties.
  * Risk and blocker triage system (e.g., missing allergen certificates, photography delays).
  * Client-side calculation of completion percentages by venue and workstream.
* **Evidence Classification**:
  * `[OBSERVED]`: High-density coordination dashboard with status chips, progress bars, and expandable venue accordions.
  * `[CODE-VERIFIED]`: Fully isolated from backend persistence. Checking or unchecking tasks calculates numbers in local DOM memory only; refreshing the browser reverts to hardcoded seed states.
* **Limitations**: Not connected to real menu review statuses or Kafoodie completeness metrics.

---

### 2.5 Interface 5: Menu Explorer

* **Routes**: `/menu-explorer`, `/pages/menu-explorer.html`, `/` (redirects here)
* **Source Files**:
  * HTML: `pages/menu-explorer.html` (170 lines)
  * Data payload: `pages/menu-explorer-data.js` (~3 MB compiled JavaScript object)
* **Technology Stack**:
  * High-performance vanilla JavaScript rendering engine.
  * CSS Custom Properties with light/dark theme toggle.
* **Functional Capabilities & Views**:
  1. **Menu View**: Venue-filtered catalog of dishes grouped by printed course, with calories, allergen tags, and dietary labels.
  2. **Guest View**: Clean customer-facing digital menu with allergen preference filters ("Avoiding Gluten, Milk...").
  3. **Allergen Matrix**: Grid table matching dishes against the 14 statutory allergens, distinguishing "Contains" (●) and "May Contain" (◐).
  4. **Compare Venues**: Cross-venue dish comparison engine identifying where allergen declarations or calorie counts diverge across properties for identically named dishes.
  5. **Venue & Menu Data**: Raw JSON and API inspector for debugging Kafoodie payloads.
  6. **Allergen Reference**: Statutory definition dictionary with legacy flags and icon mapping.
* **Evidence Classification**:
  * `[OBSERVED]`: Production-grade speed, extensive data depth, instant client-side filtering.
  * `[CODE-VERIFIED]`: Data is populated directly from `window.MENU_DATA` generated by `build_menu_explorer.py`. Replaces raw duplicated allergen objects with an indexed integer dictionary, shrinking file size significantly.
* **Limitations**: Read-only explorer. Does not support editing or approving recipes. Excludes venues lacking a Kafoodie outlet crawl (e.g., Dean Court).

---

### 2.6 Interface 6: Menu Review

* **Routes**: `/menu-review`, `/pages/menu-review.html`
* **Source Files**: `pages/menu-review.html` (980 lines), `pages/pdf_map.json`, `pages/seed_reviews.json`
* **Technology Stack**:
  * Dynamic client-side app communicating with backend endpoints.
  * Markdown parsing and rendering engine, split-pane layout with synchronized scrolling.
* **Functional Capabilities**:
  * Lists all Markdown menus from `/api/menus`.
  * Renders original printed PDF in an `<iframe>` beside extracted Markdown (`/api/pdf?name=...` and `/api/menu?name=...`).
  * Automated issue detection:
    * `headings`: Identifies improperly nested sections.
    * `repeated_lines`: Finds duplicate lines generated during PDF extraction.
    * `unusual_chars`: Highlights OCR and typography anomalies.
    * `pdf_missing`: Flags Markdown files missing original PDF counterparts.
  * Interactive Review Workflow: Persists triage statuses (`open`, `fixed`, `intentional`) and review notes to SQLite.
  * Automated Remediation: Features a "Fix Duplicates" action that sends line numbers to `/api/issues/fix-duplicates`, rewriting the Markdown file via atomic temporary replacement.
* **Evidence Classification**:
  * `[OBSERVED]`: True bi-directional editorial environment.
  * `[CODE-VERIFIED]`: Uses real endpoints in `menu_review_server.py` and `netlify/functions/api.py`. State is saved to `menu_review_state.sqlite3` with SHA256 concurrency checks (`X-Source-Hash`).
* **Limitations**: Focused purely on Markdown text cleanup; does not match extracted lines to Kafoodie recipe IDs (that occurs in `build_venue_export.py`).

---

### 2.7 Interface 7: Product Data

* **Routes**: `/product-data`, `/pages/product-data.html`
* **Source File**: `pages/product-data.html` (820 lines)
* **Technology Stack**:
  * Client-side administrative UI prototype with tabular data views and drawer editors.
* **Functional Capabilities**:
  * Models a multi-site Master Product Record:
    * SKU / Product Code
    * Central Name vs Venue Display Name
    * Recipe association & ingredient spec
    * Allergen verification checklist
    * Pricing, Cost of Goods Sold (COGS), Margin %
    * Publication states (`Draft`, `Review`, `Approved`, `Active`, `Archived`)
* **Evidence Classification**:
  * `[OBSERVED]`: Demonstrates the visual layout for a centralized F&B master catalog.
  * `[CODE-VERIFIED]`: **Demonstration only**. Contains static mock rows. No API integration or persistence.
* **Limitations**: Currently disconnected from both Kafoodie JSON feeds and printed Markdown menus.

---

## 3. Backend Services & Build Pipelines

| Script / Service | Path | Lines | Primary Responsibility | Data Stores / Endpoints |
| :--- | :--- | :--- | :--- | :--- |
| **Local Dev Server** | `menu_review_server.py` | 615 | Local HTTP server (`ThreadingHTTPServer`) hosting static pages and review/export API. | SQLite (`menu_review_state.sqlite3`), Local filesystem (`exports/`). Endpoints: `/api/menus`, `/api/menu`, `/api/pdf`, `/api/issues`, `/api/issues/fix-duplicates`, `/api/export`. |
| **Serverless API** | `netlify/functions/api.py` | 594 | Production serverless equivalent of dev server for Netlify hosting. | In-memory SQLite seeded from `seed_reviews.json`. Endpoints identical to local server; exports returned as Base64 ZIP. |
| **Menu Explorer Builder** | `build_menu_explorer.py` | 411 | Ingests raw Kafoodie JSONs, deduplicates outlet files, extracts shared allergen maps, outputs client JS bundle. | In: `kafoodie/*_all_menus.json`. Out: `pages/menu-explorer-data.js`, `ALL_MENUS_CHECKLIST.md`, `duplicates_removed.json`. |
| **Venue Export Engine** | `build_venue_export.py` | 1,376 | Comprehensive reconciliation engine. Merges printed Markdown menus, Kafoodie recipes, website crawl, and media into canonical venue JSON. | In: `menus_md/`, `kafoodie/`, `pages_text/`, `discovered_media.csv`, `config/*.json`. Out: `exports/<Region>/<Venue>/venue.json` and `venue.md`. |

---

## 4. Configuration & Specification Files

* **`config/venues.json`**: Per-venue metadata overrides (e.g. assigning The Kingslodge Inn to "County Durham" and Offshore to "Lancashire").
* **`config/aliases.json`**: Dish-to-recipe name translation matrix (~80 global aliases, 6 children's aliases). Maps printed dishes (e.g. `classic prawn sandwich`) to Kafoodie recipe names (`Prawn Marie Rose Sandwich`).
* **`config/rules.json`**: Heuristics for token parsing, dietary codes (`V`, `VG`, `GFA`), promo patterns, menu classification rules, and web scraping boundary markers.
* **`docs/MENU-MD-SPEC.md`**: Architectural specification defining the standardized structure of PDF-extracted Markdown menus.
* **`docs/VENUE-EXPORT-SPEC.md`**: JSON schema specification for canonical `venue.json` exports.
