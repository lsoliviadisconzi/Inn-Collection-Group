# Document 07 — Architecture Verification, Evidence Reconciliation & Netlify Removal Report

> **Hospitality Technology Capability Assessment — The Inn Collection Group**  
> **Phase**: Architecture Verification, Evidence Reconciliation & Netlify Decommissioning  
> **Standard Key**: `[Observed]` · `[Code-verified]` · `[Database-verified]` · `[Tested]` · `[Inferred]` · `[Proposed]` · `[Unknown]`

---

## 1. Executive Summary

This report concludes the architecture verification and evidence reconciliation phase for The Inn Collection Group (ICG) hospitality technology workspace, executing the instructions set forth in `PROJECT-REVIEW/03.1 - Architecture Verification Evidence Reconciliation and Netlify Removal.md` and addressing the technical review in `PROJECT-REVIEW/03.md`.

### Core Outcomes:
1. **Complete Netlify Decommissioning**: All Netlify configuration files, serverless function implementations, local CLI metadata, and redundant file bundles have been completely excised from the repository. Zero Netlify dependencies remain.
2. **File-Path & Redundancy Reconciliation**: The relationship between `inncollectiongroup.com_root/menus_md/` and `pages/menus_md/` has been verified via byte-for-byte checksums and code tracing. The actual local runtime reads and modifies exclusively `inncollectiongroup.com_root/menus_md/`.
3. **Database Reality Clarification**: The SQL database is confirmed as SQLite (`menu_review_state.sqlite3`) with exactly one table (`issue_reviews`) holding review-state metadata. No domain models or business records are stored in SQL.
4. **Build Pipeline Reconciliation**: The number of build pipelines is formally reconciled to **exactly two**: `build_menu_explorer.py` and `build_venue_export.py`.
5. **Data Authority Boundaries**: `venue.json` is formally classified as a **canonical generated data artifact**, not a global source of truth.
6. **Regulatory Deferral**: Compliance rules (such as un-set allergen blocking policies) have been separated from technical architecture and designated for future policy review.

---

## 2. Deliverable A: Netlify Removal Manifest

Every file and directory touched during the Netlify decommissioning is cataloged below:

| Path | Classification | Action | Reason | Application Impact |
| :--- | :--- | :--- | :--- | :--- |
| `netlify.toml` | Netlify-only | **Removed** | Development deployment configuration (redirects, functions path, headers). Obsolete for local runtime. | **None** (`[Tested]`). Local server handles its own routing. |
| `netlify/functions/api.py` | Netlify-only | **Removed** | Ephemeral serverless duplicate of `menu_review_server.py`. | **None** (`[Tested]`). `menu_review_server.py` is the actual local API service. |
| `netlify/functions/__pycache__/` | Netlify-only | **Removed** | Compiled Python bytecode for serverless function. | **None**. |
| `netlify/functions/data/seed_reviews.json` | Netlify-only | **Removed** | Cold-start seed database for serverless function. Original master copy preserved at `pages/seed_reviews.json`. | **None**. Master copy preserved. |
| `netlify/functions/data/menus_md/` (103 files) | Netlify-only | **Removed** | Third duplicate copy of menu markdown packaged for AWS Lambda execution. | **None**. Master menus preserved in `inncollectiongroup.com_root/menus_md/`. |
| `netlify/` | Netlify-only | **Removed** | Directory tree hosting former serverless infrastructure. | **None**. |
| `.netlify/state.json` | Netlify-only | **Removed** | Local Netlify CLI state and site ID cache. | **None**. |
| `.netlify/` | Netlify-only | **Removed** | Netlify CLI cache directory. | **None**. |
| `.gitignore` | Shared | **Edited** | Removed lines referencing `.netlify/`. | **None** (`[Code-verified]`). |
| `requirements.txt` | Mixed | **Edited** | Replaced Netlify Python runtime detection notice with clean standard-library statement. | **None** (`[Code-verified]`). Application uses stdlib only. |
| `05_COMPONENT_RELATIONSHIPS.md` (root) | Obsolete Draft | **Removed** | Legacy root-level markdown file containing un-reconciled Netlify serverless claims. | **None**. Replaced by reconciled `docs/capability-assessment/` suite. |

---

## 3. Deliverable B: Architecture Verification Report

### 3.1 Actual Application Architecture & Runtime
* `[Code-verified]`: The application is a self-contained local web environment running on Python 3.8+ standard library.
* `[Code-verified]`: Application server is `menu_review_server.py`, an instance of `ThreadingHTTPServer` binding to `http://127.0.0.1:8000/`.
* `[Code-verified]`: Zero third-party web frameworks (no Flask, Django, FastAPI) and zero package dependencies.

### 3.2 File-Path Verification: The Markdown Directories
Investigation into the relationship between `inncollectiongroup.com_root/menus_md/` and `pages/menus_md/`:
1. **Content Comparison**:
   * `[Code-verified]`: Both directories contain exactly 103 Markdown files.
   * `[Code-verified]`: A deep binary comparison (`filecmp.cmp()`) across all 103 files confirms they are **100% byte-for-byte identical**. Zero content drift currently exists.
2. **Code Consumption Analysis**:
   * `[Code-verified]`: In `menu_review_server.py:26`, `MENUS = ROOT / "inncollectiongroup.com_root" / "menus_md"`.
   * `[Code-verified]`: `GET /api/menus` reads exclusively from `inncollectiongroup.com_root/menus_md/`.
   * `[Code-verified]`: `GET /api/menu` reads exclusively from `inncollectiongroup.com_root/menus_md/`.
   * `[Code-verified]`: `POST /api/issues/fix-duplicates` rewrites files exclusively in `inncollectiongroup.com_root/menus_md/`.
   * `[Code-verified]`: In `build_venue_export.py:47`, `MENUS_MD = CRAWL / "menus_md" = inncollectiongroup.com_root/menus_md`.
   * `[Code-verified]`: **`pages/menus_md/` is never read or written by any local server or build script**.
3. **Origin & Next Steps**:
   * `[Inferred]`: `pages/menus_md/` was created solely because Netlify was configured with `publish = "pages"`, requiring static files to reside under that web root.
   * `[Proposed]`: In accordance with Section 2.2 of the mandate, `pages/menus_md/` has been left intact for now. However, because Netlify is now removed, `pages/menus_md/` is completely redundant and can be safely deleted in a future cleanup phase once confirmed.

### 3.3 Database Implementation Verification
* `[Database-verified]`: Engine is **SQLite 3**, located at `/Users/leandrodisconzi/repos/Inn-Collection-Group/menu_review_state.sqlite3`.
* `[Database-verified]`: Schema consists of exactly one table:
  ```sql
  CREATE TABLE issue_reviews (
      menu_name TEXT NOT NULL,
      source_hash TEXT NOT NULL,
      issue_id TEXT NOT NULL,
      status TEXT NOT NULL,
      note TEXT NOT NULL DEFAULT '',
      updated_at TEXT NOT NULL,
      PRIMARY KEY (menu_name, source_hash, issue_id)
  );
  ```
* `[Database-verified]`: Constraints: Composite Primary Key on `(menu_name, source_hash, issue_id)`.
* `[Database-verified]`: Records: Exactly 1 row recording duplicate line fixes on `Crown-Menu-The-Tynemouth-Castle-Inn-DIGITAL-WEB-v2.md`.
* `[Database-verified]`: Consumers: Only `menu_review_server.py` reads and writes to this database. No other script or interface connects to SQLite.
* `[Database-verified]`: Persistence: Changes persist across process restarts because the database is written directly to the filesystem disk file.

### 3.4 Build Pipelines Reconciliation
* `[Code-verified]`: Reconciled the count discrepancy: **There are exactly two build pipelines**:
  1. **`build_menu_explorer.py` (411 lines)**:
     * *Inputs*: `inncollectiongroup.com_root/kafoodie/*_all_menus.json`, `config/venues.json`, `config/rules.json`.
     * *Outputs*: `pages/menu-explorer-data.js` (exported as `window.MENU_DATA`) and `ALL_MENUS_CHECKLIST.md`.
     * *Consumers*: `pages/menu-explorer.html` consumes `menu-explorer-data.js`.
  2. **`build_venue_export.py` (1,376 lines)**:
     * *Inputs*: `inncollectiongroup.com_root/menus_md/*.md`, `inncollectiongroup.com_root/kafoodie/`, `pages_text/*.txt`, `discovered_media.csv`, `config/*.json`.
     * *Outputs*: `exports/<Region>/<Venue>/venue.json` and `exports/<Region>/<Venue>/venue.md`.
     * *Consumers*: Currently an offline compilation output; **no interface currently consumes `venue.json`**.
* `[Code-verified]`: Neither pipeline depends on the other; both read raw crawl files independently. Neither pipeline contained any Netlify-specific logic.

### 3.5 Generated Data: `venue.json` Classification
* `[Code-verified]`: `venue.json` is a **canonical generated data artifact**, derived by merging four separate upstream sources via heuristic matching rules.
* **Source of Authority per Field**:
  * *Recipe identifiers, allergen declarations, nutritional values*: Sourced from Kafoodie crawl (`inncollectiongroup.com_root/kafoodie/`).
  * *Printed dish titles, printed descriptions, section placement, retail prices*: Sourced from extracted Markdown (`menus_md/`).
  * *Venue identity, phone, address, amenities*: Sourced from website text (`pages_text/`) and `config/venues.json`.
  * *Dish-to-recipe links*: Sourced from `config/aliases.json` and algorithmic token scoring.
* `[Code-verified]`: It is **not** an authoritative database; it is a compiled snapshot that must be regenerated whenever upstream files or alias rules change.

---

## 4. Deliverable C: Final Netlify Reference Audit

* **Files & Directories Removed**:
  * 1 configuration file (`netlify.toml`)
  * 2 directory trees (`netlify/` and `.netlify/`) containing 107 total files (including bytecode, seeds, and duplicated markdown files)
  * 1 legacy root draft (`05_COMPONENT_RELATIONSHIPS.md`)
* **Shared Files Edited**:
  * `.gitignore`: Removed `.netlify/` rule.
  * `requirements.txt`: Cleaned of Netlify runtime detection wording.
* **Remaining Netlify References**:
  * **Zero runtime or configuration references** remain in application source files (`*.py`, `*.html`, `*.js`, `*.json`, `*.csv`).
  * The only occurrences of the word "Netlify" in the entire repository exist in historical review and audit documents (`PROJECT-REVIEW/` and `docs/capability-assessment/`) explicitly documenting its decommissioning.
* **Local Dependency Check**:
  * `[Code-verified]`: The local application has **zero remaining Netlify dependency**.

---

## 5. Deliverable D: Local Application Verification Report

All core application services were verified through live execution tests following Netlify removal:

| Component Tested | Test Command / Method | Verification Target | Test Result |
| :--- | :--- | :--- | :--- |
| **Local Application Server** | `python3 menu_review_server.py --port 8766` | Clean socket bind, route initialization | **PASS** (`[Tested]`). Server started without warnings. |
| **Menu Catalog API** | `GET http://127.0.0.1:8766/api/menus` | JSON menu array, size, PDF detection | **PASS** (`[Tested]`). Returned HTTP 200, 103 menus cataloged. |
| **Menu Content API** | `GET http://127.0.0.1:8766/api/menu?name=2026-Christmas-Day-Lunch.md` | Raw UTF-8 stream, `X-Source-Hash` header | **PASS** (`[Tested]`). Returned HTTP 200, 1,252 bytes. |
| **Review Issues API** | `GET http://127.0.0.1:8766/api/issues?name=2026-Christmas-Day-Lunch.md` | SQLite lookup for current hash | **PASS** (`[Tested]`). Returned HTTP 200, valid JSON payload. |
| **Menu Review UI Delivery** | `GET http://127.0.0.1:8766/pages/menu-review.html` | Static HTML serving | **PASS** (`[Tested]`). Returned HTTP 200. |
| **Menu Explorer UI Delivery** | `GET http://127.0.0.1:8766/pages/menu-explorer.html` | Static HTML serving | **PASS** (`[Tested]`). Returned HTTP 200. |
| **Menu Explorer Data Bundle** | `python3 build_menu_explorer.py --check` | Data currency, SHA verification | **PASS** (`[Tested]`). Output: *"Menu explorer data and checklist are current."* |
| **Venue Export Pipeline** | `python3 build_venue_export.py --list` | Venue registry discovery, menu mapping | **PASS** (`[Tested]`). Discovered and registered 29 venues across 7 regions. |

---

## 6. Deliverable E: Clean Project Architecture Map (Netlify-Free)

```mermaid
flowchart TD
    subgraph DataSources["1. Raw & Ingestion Data Sources"]
        PDF["Printed Menu Cards<br/>(documents/extracted-to-md/*.pdf)"]
        KAF["Kafoodie API Crawl<br/>(kafoodie/*_all_menus.json)"]
        TXT["Website Scrape Text<br/>(pages_text/*.txt)"]
        CSV["Media Asset Catalog<br/>(discovered_media.csv)"]
        CFG["Configuration Rules<br/>(config/venues.json, aliases.json, rules.json)"]
    end

    subgraph StorageLayer["2. Repository Storage Layer"]
        MD["Markdown Menus (Master)<br/>(inncollectiongroup.com_root/menus_md/*.md)"]
        SQL[("Local SQLite Database<br/>(menu_review_state.sqlite3)<br/>Table: issue_reviews")]
    end

    subgraph LocalRuntime["3. Local Runtime Services"]
        SRV["menu_review_server.py<br/>(ThreadingHTTPServer · Port 8000)"]
    end

    subgraph BuildPipelines["4. Reconciliation & Build Pipelines"]
        B1["build_menu_explorer.py<br/>(Allergen Indexing & Deduplication)"]
        B2["build_venue_export.py<br/>(3-Stage Dish-to-Recipe Reconciliation)"]
    end

    subgraph GeneratedArtifacts["5. Derived Canonical Artifacts"]
        EXP_DATA["pages/menu-explorer-data.js<br/>(window.MENU_DATA bundle)"]
        VENUE_JSON["exports/<Region>/<Venue>/venue.json<br/>(Canonical Generated Venue Model)"]
        VENUE_MD["exports/<Region>/<Venue>/venue.md<br/>(Human-Readable View)"]
    end

    subgraph UserInterfaces["6. User Interfaces (pages/)"]
        UI_EXP["Menu Explorer (menu-explorer.html)<br/>(Operational Inquiry Tool)"]
        UI_REV["Menu Review (menu-review.html)<br/>(Operational Review Tool)"]
        UI_MED["Discovered Media (discovered-media.html)<br/>(Media Export Tool)"]
        UI_PROTO["Static Demonstrations & Mockups<br/>• Product Data (product-data.html)<br/>• Launch Readiness (launch-readiness.html)<br/>• F&B Cross-check (fnb-crosscheck.html)<br/>• Chicken Liver Parfait (recipes/chicken-liver-parfait...)"]
    end

    PDF -->|External Extraction| MD
    MD --> SRV
    PDF --> SRV
    SRV <-->|Read / Write Triage & Deduplication| SQL
    SRV <-->|GET /api/menus, /api/menu, /api/issues<br/>POST /api/issues, /api/issues/fix-duplicates| UI_REV
    CSV --> UI_MED
    SRV <-->|POST /api/export (Local Downloads)| UI_MED

    KAF --> B1
    CFG --> B1
    B1 --> EXP_DATA
    EXP_DATA --> UI_EXP

    MD --> B2
    KAF --> B2
    TXT --> B2
    CSV --> B2
    CFG --> B2
    B2 --> VENUE_JSON
    B2 --> VENUE_MD

    VENUE_JSON -.->|Proposed Data Source| UI_PROTO
```

---

## 7. Operational & Regulatory Safeguards Enforced

In accordance with the review in `PROJECT-REVIEW/03.md`:
1. **Hypothetical Workflows Separated**: Workflow descriptions in the capability assessment suite are officially classified as **illustrative operational scenarios** rather than confirmed ICG corporate standards.
2. **Regulatory Restraint Preserved**: Technical documentation records where allergen information originates, detects where fields like `is_pw_allergen_not_set` are absent, and highlights data provenance. It leaves the establishment of mandatory critical blockers and legal compliance policy to a dedicated future governance phase.
3. **Execution Reality Established**: The system is definitively documented as a working data-processing, document-review, and cross-venue inquiry suite, with master operational data management identified as the primary future development priority.
