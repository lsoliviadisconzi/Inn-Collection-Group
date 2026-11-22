# Document 03 — Component and Capability Register

> **Hospitality Technology Capability Assessment — The Inn Collection Group**  
> **Phase**: System Architecture & Technical Verification  
> **Standard Key**: `[Observed]` · `[Code-verified]` · `[Database-verified]` · `[Tested]` · `[Inferred]` · `[Proposed]` · `[Unknown]`

---

## 1. Overview of the Capability Register

This register inventories every user-facing interface, backend script, database, and build pipeline currently present in the Inn Collection Group repository. 

To eliminate confusion between **designed UI elements** and **actual working capabilities**, each component is evaluated across:
* **Declared Role**: What the interface was created to demonstrate or perform.
* **Verified Implementation**: What code and data structures actually exist on disk.
* **Data Sources & Backing**: Flat files, SQLite tables, or in-memory variables.
* **Current Operational Status**: Production-grade, operational tool, or conceptual mockup.

---

## 2. Component Inventory & Capability Evaluation

### 2.1 Interface Components

#### 1. Discovered Media (`pages/discovered-media.html`)
* **Declared Role**: Source-document discovery, cataloging, and media asset acquisition.
* **Verified Capabilities**:
  * `[Code-verified]`: Loads and parses `pages/discovered_media.csv` entirely in client-side JavaScript.
  * `[Code-verified]`: Multi-faceted filtering by Region, Venue, Asset Category (`Food`, `Drinks`, `Property`, `Events`), and MIME file type.
  * `[Code-verified]`: Multi-select batch export. Issues `POST /api/export` payload containing asset URLs and venue classification.
* **Backing & Persistence**:
  * Read Source: Static CSV snapshot on disk (`inncollectiongroup.com_root/discovered_media.csv`).
  * Database: None (`[Database-verified]`).
  * Server Dependency: Requires `menu_review_server.py` to write downloads to local disk.
* **Operational Status**: **Working Tool (Read/Export Only)**. Functional for exporting media, but does not crawl or update the CSV dynamically.

---

#### 2. Menu Review (`pages/menu-review.html`)
* **Declared Role**: Document quality assurance, OCR extraction verification, and Markdown error triage.
* **Verified Capabilities**:
  * `[Code-verified]`: Dynamically queries `/api/menus` to list all extracted Markdown files.
  * `[Code-verified]`: Synchronized side-by-side view rendering original PDF alongside extracted Markdown.
  * `[Code-verified]`: Scans and detects structural issues: `headings`, `list_entries`, `pdf_missing`, `repeated_lines`, `unusual_chars`.
  * `[Database-verified]`: Interacts with SQLite table `issue_reviews`. Persists status (`open`, `fixed`, `intentional`) and reviewer notes.
  * `[Tested]`: Features a working automated remediation tool: `POST /api/issues/fix-duplicates` removes repeated lines from the Markdown file and updates SQLite atomically.
* **Backing & Persistence**:
  * Read/Write Store: SQLite `menu_review_state.sqlite3` (`[Database-verified]`).
  * File System: Directly reads and rewrites `.md` files in `menus_md/`.
* **Operational Status**: **Operational Review Tool**. This is the only interface in the repository with live read/write database persistence.

---

#### 3. Menu Explorer (`pages/menu-explorer.html`)
* **Declared Role**: Guest menu simulation, estate-wide allergen matrix, venue comparison, and nutritional inquiry.
* **Verified Capabilities**:
  * `[Code-verified]`: Instant client-side filtering of dishes by venue, course group, and search text.
  * `[Code-verified]`: 14 statutory allergen matrix distinguishing direct presence (●) from cross-contact advisories (◐).
  * `[Code-verified]`: "Guest View" filtering dishes based on guest food preferences ("Avoiding Gluten, Milk...").
  * `[Code-verified]`: "Compare Venues" engine: performs matrix diff across all 29 venues, identifying where identical dishes have divergent calories or allergen declarations.
* **Backing & Persistence**:
  * Read Source: Static compiled bundle `pages/menu-explorer-data.js` (~3 MB).
  * Database: None (`[Database-verified]`). Operates entirely read-only.
* **Operational Status**: **Operational Inquiry Tool**. Highly mature, extremely fast, populated with real Kafoodie crawl data for 29 properties.

---

#### 4. Product Data (`pages/product-data.html`)
* **Declared Role**: Master product data administration, recipe management, and commercial governance.
* **Verified Capabilities**:
  * `[Observed]`: Visual tabular interface displaying mock product rows with SKU codes, recipe relationships, prices, margins, and validation badges.
  * `[Code-verified]`: **100% Mockup**. Contains no `fetch()` calls, no dynamic data binding, and no form submission logic. All table rows are hardcoded HTML.
* **Backing & Persistence**:
  * None (`[Database-verified]`). No SQL tables, JSON files, or API endpoints exist for product administration.
* **Operational Status**: **Static Visual Prototype**. Represents a desired future capability, not working software.

---

#### 5. Chicken Liver Parfait — Product Page (`pages/recipes/chicken-liver-parfait...html`)
* **Declared Role**: Product-centered operational standard, presenting culinary specs, prep schedules, plating standards, supplier codes, and allergen data.
* **Verified Capabilities**:
  * `[Observed]`: Interactive "hub-and-spoke" interface where sections expand into detailed modal sheets.
  * `[Code-verified]`: **100% Static HTML/CSS**. All recipes, grammages, Brakes supplier codes, prep methods, and costing numbers are hardcoded directly into DOM markup.
* **Backing & Persistence**:
  * None (`[Database-verified]`). Completely self-contained file (2,575 lines).
* **Operational Status**: **Design Specification Prototype**. Outstanding UI/UX design demonstrating what an individual dish record *should* look like, but currently hardcoded for exactly one recipe.

---

#### 6. Launch Readiness (`pages/launch-readiness.html`)
* **Declared Role**: Multi-site rollout coordination, milestone tracking, and launch risk triage across 31 inns.
* **Verified Capabilities**:
  * `[Observed]`: Visual dashboard rendering workstream progress bars, milestone checklists, and venue accordions.
  * `[Code-verified]`: **Client-Side Simulation**. Ticking checklist items updates progress bars in DOM memory only. Refreshing the browser resets all state.
* **Backing & Persistence**:
  * None (`[Database-verified]`). No connection to SQLite, no connection to `venue.json:coverage`, and no API endpoints.
* **Operational Status**: **Functional UI Mockup**. Demonstrates launch coordination workflows without underlying data integration.

---

#### 7. F&B Role Cross-check (`pages/fnb-crosscheck.html`)
* **Declared Role**: Requirements-to-capability gap analysis benchmarking operational needs against software features.
* **Verified Capabilities**:
  * `[Code-verified]`: Client-side filtering of 100+ operational requirements across hospitality personas.
  * `[Code-verified]`: Calculates coverage statistics (% Full, Partial, Not Yet, Manual).
* **Backing & Persistence**:
  * Read Source: Static array hardcoded inside `<script>` tag in `pages/fnb-crosscheck.html:70-180`.
  * Database: None (`[Database-verified]`).
* **Operational Status**: **Static Analytical Tool**. Useful internal assessment artifact, but not an operational application module.

---

### 2.2 Backend & Build Pipeline Components

| Component | Path | Verified Functionality | Data Store | Operational Status |
| :--- | :--- | :--- | :--- | :--- |
| **Local Dev Server** | `menu_review_server.py` | Hosts web UIs on port 8000; serves review and export APIs; executes atomic duplicate line fixes on Markdown files. | SQLite (`menu_review_state.sqlite3`) & Local Filesystem | **Operational Local Server** (`[Tested]`) |
| **Menu Explorer Builder** | `build_menu_explorer.py` | Ingests Kafoodie JSONs, normalizes venue names, indexes allergens, detects duplicate crawls, compiles `menu-explorer-data.js`. | Filesystem (`kafoodie/` -> `pages/`) | **Operational Build Tool** (`[Code-verified]`) |
| **Venue Export Engine** | `build_venue_export.py` | 1,376 lines. Ingests Markdown menus, Kafoodie data, website scrape, and media. Runs alias and token matching. Outputs canonical `venue.json`. | Filesystem (`menus_md/` + `kafoodie/` -> `exports/`) | **Operational Build Tool** (`[Code-verified]`) |
| **SQLite Database** | `menu_review_state.sqlite3` | Single-table database (`issue_reviews`) holding review decisions and duplicate line cleanup logs. | SQLite Engine (Disk file) | **Operational Persistence** (`[Database-verified]`) |

---

## 3. Comprehensive Capability Summary Matrix

| Capability Area | Supported Today? | Implementation Mechanism | Evidence | Gaps & Limitations |
| :--- | :---: | :--- | :---: | :--- |
| **Menu Document Intake & Review** | **Yes** | `menu-review.html` + `menu_review_server.py` + SQLite | `[Code-verified]` | PDF-to-Markdown extraction is external/manual. |
| **Media Asset Discovery & Export** | **Yes** | `discovered-media.html` + `/api/export` | `[Code-verified]` | Static CSV crawl; does not detect live web updates. |
| **Guest Menu & Allergen Browsing** | **Yes** | `menu-explorer.html` + `menu-explorer-data.js` | `[Code-verified]` | Read-only; 2 venues missing from Kafoodie crawl. |
| **Cross-Venue Variance Auditing** | **Yes** | `menu-explorer.html:cmp()` | `[Code-verified]` | Relational diffing works, but no alerting or ticket generation. |
| **Dish-to-Recipe Reconciliation** | **Yes** | `build_venue_export.py` matching cascade | `[Code-verified]` | CLI script only; no browser interface to approve aliases. |
| **Master Product Administration** | No | Visual mockup only (`product-data.html`) | `[Observed]` | Zero backend or database; mock data. |
| **Kitchen Plating & SOP Guidance** | Partial | Hardcoded on 1 dish (`chicken-liver-parfait`) | `[Observed]` | Template not parameterized for other 200+ dishes. |
| **Multi-Site Launch Tracking** | Partial | Client-side simulation (`launch-readiness.html`) | `[Observed]` | Volatile DOM memory; unlinked to real pipeline progress. |
| **EPOS / PLU Programming** | No | None | `[Code-verified]` | Completely absent from code and data models. |
| **Supplier & Cost Management** | No | Hardcoded sample on 1 dish | `[Observed]` | Absent from master schemas; prices are guest-facing only. |
