# 05 — Component Relationships

## 1. System Relationship Topology

The Inn Collection Group hospitality workspace currently consists of loosely coupled subsystems. This document categorizes existing verified links, shared dependencies, missing integrations, and architectural consolidation pathways.

```mermaid
graph TD
    subgraph DataIngestionLayer["Ingestion & Scraping Pipeline"]
        SCRAPE["Website Scraper"] --> CSV["discovered_media.csv"]
        SCRAPE --> TXT["pages_text/*.txt"]
        KAF_API["Kafoodie Portal API"] --> KAF_JSON["kafoodie/*_all_menus.json"]
        PDF_SOURCE["Creative Print Ingestion"] --> PDFS["extracted-to-md/*.pdf"]
        PDFS --> MD_EXTRACT["PDF-to-MD Script"] --> MD_FILES["menus_md/*.md"]
    end

    subgraph BuildAndReconciliation["Reconciliation & Build Layer"]
        KAF_JSON --> BUILD_EXP["build_menu_explorer.py"]
        BUILD_EXP --> EXP_DATA["menu-explorer-data.js"]
        
        MD_FILES --> BUILD_VENUE["build_venue_export.py"]
        KAF_JSON --> BUILD_VENUE
        TXT --> BUILD_VENUE
        CSV --> BUILD_VENUE
        CONFIG["config/*.json<br/>(venues, aliases, rules)"] --> BUILD_VENUE
        BUILD_VENUE --> VENUE_JSON["exports/<Venue>/venue.json"]
        BUILD_VENUE --> VENUE_MD["exports/<Venue>/venue.md"]
    end

    subgraph PersistenceAndAPILayer["Server & Persistence Layer"]
        MD_FILES --> SERVER["menu_review_server.py<br/>/ netlify/functions/api.py"]
        PDFS --> SERVER
        SERVER <--> SQLITE[("menu_review_state.sqlite3<br/>(issue_reviews)")]
        SERVER --> EXPORT_DIR["exports/<Region>/<Venue>/..."]
    end

    subgraph PresentationLayer["User Interfaces"]
        EXP_DATA --> UI_EXP["Menu Explorer<br/>(menu-explorer.html)"]
        CSV --> UI_MEDIA["Discovered Media<br/>(discovered-media.html)"]
        SERVER <--> UI_REV["Menu Review<br/>(menu-review.html)"]
        SERVER <--> UI_MEDIA
        
        UI_RECIPE["Chicken Liver Parfait<br/>(chicken-liver-parfait...)"]
        UI_PROD["Product Data<br/>(product-data.html)"]
        UI_CROSS["F&B Cross-check<br/>(fnb-crosscheck.html)"]
        UI_LAUNCH["Launch Readiness<br/>(launch-readiness.html)"]
    end

    %% Navigation Links (Observed)
    UI_EXP -.->|HTML Nav Header| UI_REV
    UI_EXP -.->|HTML Nav Header| UI_MEDIA
    UI_EXP -.->|HTML Nav Header| UI_CROSS
    UI_EXP -.->|HTML Nav Header| UI_LAUNCH
    UI_EXP -.->|HTML Nav Header| UI_PROD

    %% Proposed Real Data Connections
    VENUE_JSON -.->|Proposed Canonical Feed| UI_PROD
    VENUE_JSON -.->|Proposed Automated Metrics| UI_LAUNCH
    VENUE_JSON -.->|Target Presentation Spec| UI_RECIPE
    UI_REV -.->|Trigger Rebuild| BUILD_VENUE
```

---

## 2. Existing Connections [CODE-VERIFIED]

1. **Shared Navigation Bar**:
   * `pages/menu-explorer.html:63` contains a top navigation bar (`<nav class="nav" aria-label="Pages">`) providing direct hyperlinks to `menu-review.html`, `discovered-media.html`, `fnb-crosscheck.html`, `launch-readiness.html`, and `product-data.html`.
2. **Kafoodie to Menu Explorer Pipeline**:
   * `build_menu_explorer.py` aggregates and deduplicates `kafoodie/*_all_menus.json`.
   * Normalizes disparate venue names via `FILTER_NAMES` dictionary.
   * Compiles and outputs `pages/menu-explorer-data.js` as an inlined `window.MENU_DATA` global object.
   * `pages/menu-explorer.html` consumes `window.MENU_DATA` immediately on initialization.
3. **Menu Review and Local Server / Netlify Function**:
   * `pages/menu-review.html` issues standard asynchronous `fetch()` requests against `/api/menus`, `/api/menu?name=...`, `/api/pdf?name=...`, and `/api/issues?name=...`.
   * Both `menu_review_server.py` and `netlify/functions/api.py` implement these endpoints identically.
   * Concurrency is protected via SHA256 header verification (`X-Source-Hash`).
   * Review notes and issue statuses (`open`, `fixed`, `intentional`) write directly to the `issue_reviews` SQLite table.
4. **Discovered Media to Export Endpoints**:
   * `pages/discovered-media.html` parses `discovered_media.csv` client-side.
   * On batch export, issues a JSON `POST /api/export` payload.
   * `menu_review_server.py` creates local nested directories in `exports/<Region>/<Venue>/<Category>/<timestamp>/` and streams down assets via Python's standard `urllib`.
   * `netlify/functions/api.py` packages the selected assets into an in-memory ZIP and returns a Base64-encoded stream.
5. **Venue Export Reconciliation Pipeline**:
   * `build_venue_export.py` merges `menus_md/*.md`, `kafoodie/*_all_menus.json`, `pages_text/*.txt`, `discovered_media.csv`, and `config/*.json`.
   * Evaluates name matching using `config/aliases.json`, exact string matching, and token overlap scoring.
   * Outputs the single most comprehensive, structured data artifact in the entire repository: `exports/<Region>/<Venue>/venue.json`.

---

## 3. Disconnected & Isolated Components [CODE-VERIFIED]

1. **Menu Review to Downstream Pipelines**:
   * When a reviewer fixes duplicate lines via `/api/issues/fix-duplicates` or approves a menu layout, this status is written to SQLite, but **no event or trigger notifies `build_venue_export.py` or `build_menu_explorer.py`**.
   * Corrected Markdown files remain in the review stage until a developer manually runs Python scripts in the terminal.
2. **Product Data & Live Kafoodie Data**:
   * `pages/product-data.html` is an isolated UI prototype containing mock rows. It does not read `venue.json` or `menu-explorer-data.js`.
3. **Launch Readiness Isolation**:
   * `pages/launch-readiness.html` maintains hardcoded in-memory state. It does not pull real metrics from `venue.json` (such as percentage of matched dishes or un-set allergens) nor does it save checklist changes to SQLite.
4. **Chicken Liver Parfait Prototype**:
   * While architecturally rich, `pages/recipes/chicken-liver-parfait-the-lindisfarne-inn.html` is completely hardcoded. No dynamic mechanism exists to render other dishes (e.g. Fish & Chips, Cumberland Sausage) using this layout template.
5. **F&B Role Cross-check**:
   * Completely static evaluation dashboard; not connected to issue trackers or live codebase status registers.

---

## 4. Shared Dependencies & Redundancy

* **Duplicate Markdown Directories**:
  * Extracted menu markdown files exist in two separate locations: `inncollectiongroup.com_root/menus_md/` and `pages/menus_md/`.
  * `menu_review_server.py` reads from `inncollectiongroup.com_root/menus_md/`, whereas `netlify/functions/api.py` falls back through candidate paths (`/tmp/menus_md`, `pages/menus_md`, `inncollectiongroup.com_root/menus_md`).
* **Venue Name Discrepancies**:
  * The Kafoodie API uses names like "The Black Swan Inn", "The Midland Hotel", and "The Stables At Cross Butts".
  * The marketing PDF menus use "The Black Swan", "The Midland", and "The Stables, Whitby".
  * Reconciled in code via `build_menu_explorer.py:FILTER_NAMES` and `config/aliases.json`.
