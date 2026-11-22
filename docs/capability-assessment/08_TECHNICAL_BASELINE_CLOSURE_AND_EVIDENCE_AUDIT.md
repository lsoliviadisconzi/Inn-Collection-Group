# Document 08 — Technical Baseline Closure and Evidence Audit

> **Knowledge Base** · Inn Collection Group (ICG) Hospitality Technology Workspace  
> **Document** 08 of 08 · Published: 2026-11-22  
> **Phase**: Final Technical Baseline Closure, Evidence Reconciliation & Capability Audit  
> **Evidence Standards**: `[Code-verified]` · `[Database-verified]` · `[Runtime-tested]` · `[File-verified]` · `[Inferred]` · `[Proposed]` · `[Unknown]`

---

## 1. Executive Summary

This audit establishes the formal technical baseline closure for The Inn Collection Group (ICG) hospitality technology repository. It addresses the outstanding observations, discrepancies, and evidentiary requirements detailed in `PROJECT-REVIEW/04.md` and fulfills the instructions set forth in `PROJECT-REVIEW/04.1 - Document 08 — Technical Baseline Closure and Evidence Audit.md`.

### 1.1 Summary of Scope & Actions Taken
* **Reviewed**: Documents 01 through 07 in `docs/capability-assessment/`, the git history of root artifacts, all API routes in `menu_review_server.py`, build pipelines `build_menu_explorer.py` and `build_venue_export.py`, the SQLite database `menu_review_state.sqlite3`, and browser client fallback logic in `pages/menu-review.html`.
* **Corrected**: Reconciled all documentation contradictions across Documents 02, 04, 05, 06, and 07. Specifically: corrected `venue.json` terminology to reflect its status as a generated data artifact rather than a master database; removed overstated "real-time" and "unapproved modification" claims in cross-venue variance reporting; removed speculative external vendor names or explicitly labeled them as hypothetical industry examples; debunked the unverified `seed_reviews.json` database recovery claim; and formally designated the operational authority division between Kafoodie and menu exports as `[Proposed]`.
* **Verified**: Completed rigorous, safe, and isolated functional testing across all 9 core application capabilities (including full read, write, mutation, atomic file replacement, export validation, check mode, and single-venue build execution).
* **Investigated**: Audited the history, contents, and disposition of the deleted root document `05_COMPONENT_RELATIONSHIPS.md`.
* **Remains Unresolved**: Business and regulatory governance decisions (e.g. formal policy for un-set allergen flags), stakeholder confirmation for deleting the orphaned `pages/menus_md/` duplicate directory, acquisition of Kafoodie outlet IDs for excluded properties, and discovery of real-world ICG corporate IT systems (EPOS, ERP, SSO).
* **Baseline Status Assessment**: **Ready with caveats**. The technical implementation, actual code boundaries, persistence mechanics, build pipelines, and interface maturity levels are now thoroughly verified and documented. The technical baseline is closed, reliable, and ready to serve as the foundation for the upcoming complete architectural blueprint.

---

## 2. Outstanding Findings Register

The eight technical observations identified in `PROJECT-REVIEW/04.md` have been systematically investigated, verified, and reconciled across the repository documentation:

| Finding ID | Original Issue | Investigation Performed | Evidence Found | Resolution Applied | Documents Amended | Remaining Uncertainty |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **F-01** | **`venue.json` Terminology Contradiction** (Doc 02 stated `venue.json` was the "true canonical data model", contradicting Doc 07). | Inspected `build_venue_export.py` lines 1280–1335 and `exports/` folder structure. | `[Code-verified]`. `venue.json` is generated offline by heuristic token matching across 4 raw crawl feeds. No live interface reads it. It is not an authoritative database. | Replaced all references claiming `venue.json` is the application's "master database" or "canonical data model". Re-classified as a *canonical generated data artifact*. | [Doc 02](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/02_DATA_MODEL_AND_ENTITY_RELATIONSHIPS.md) | None. Classification is now uniform across Docs 01–08. |
| **F-02** | **Overstated Real-Time Cross-Venue Auditing** (Doc 04 described cross-venue variance auditing as "real-time" and isolating "unapproved regional modifications"). | Inspected `pages/menu-explorer.html` (lines 400–550) and `pages/menu-explorer-data.js`. | `[Code-verified]`. The interface performs in-memory JavaScript comparisons over a static snapshot bundle (`window.MENU_DATA`). It has no live network connection to kitchens or till systems. | Replaced "real-time cross-site variance report" with *client-side comparison of a generated data snapshot*. Clarified that identifying variance does not determine whether differences are approved, intentional, or operationally current; human investigation is required. | [Doc 04](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/04_OPERATIONAL_WORKFLOW_MAP.md) | None. Capability is accurately framed as static comparison. |
| **F-03** | **Speculative External Integrations** (Doc 05 named Zonal, Micros, Tevalis, FnB, Access, Birchman, Okta, Azure AD without proof of use by ICG). | Inspected full codebase, git history, configuration files, and network endpoints. | `[Code-verified]`. Zero references to these vendor platforms exist in operational code or configuration. | Formally labeled all named external vendor platforms as *hypothetical hospitality industry examples*, removing any implication that they represent verified ICG infrastructure. | [Doc 05](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/05_INTEGRATION_AND_DEPENDENCY_REGISTER.md) | Actual vendor systems used by ICG remain unknown pending stakeholder consultation. |
| **F-04** | **Unverified Database Fallback Claim (`seed_reviews.json`)** (Doc 05 claimed `seed_reviews.json` served as a database fallback). | Inspected `menu_review_server.py`, `pages/menu-review.html` lines 434–446, and `pages/seed_reviews.json`. | `[Code-verified]`. The local server does **not** read or write `seed_reviews.json`. It was used solely for Netlify Lambda cold starts and as a tertiary browser UI fallback if `/api/issues` fails. It holds exactly 1 static record and provides **zero** automated SQLite database restore functionality. | Corrected Doc 05 dependency matrix. Debunked automated fallback claim; documented true role as static client-side fallback. | [Doc 05](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/05_INTEGRATION_AND_DEPENDENCY_REGISTER.md) | None. Server persistence is strictly local SQLite file I/O. |
| **F-05** | **Overstated Scope of Application Testing** (Doc 07 claimed "all core application services verified", but listed only smoke tests). | Reviewed tests executed in Doc 07 vs total codebase capabilities. Conducted full execution suite across all 9 endpoints and build scripts. | `[Runtime-tested]`. Doc 07 tests were smoke tests (server bind, GET routes, `--check`, `--list`). Full mutation routes (`POST /api/issues`, `fix-duplicates`, `POST /api/export`, and full venue compilation) had not been systematically exercised. | Qualified Doc 07 claims as *selected runtime and build-tool smoke tests*. Authored full verification suite in Doc 08 with isolated write/mutation testing. | [Doc 07](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/07_ARCHITECTURE_VERIFICATION_AND_NETLIFY_REMOVAL.md) & [Doc 08](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md) | None. All 9 capabilities are now directly runtime-tested. |
| **F-06** | **Deletion of Root Document `05_COMPONENT_RELATIONSHIPS.md`** (Deleted during Netlify cleanup; required investigation into provenance and information loss). | Executed git log/show audit (`git show 1cab3de1:05_COMPONENT_RELATIONSHIPS.md`). Evaluated contents against Docs 01–07. | `[File-verified]`. The file was an early 10-part draft that contained superseded Netlify claims (e.g. Netlify as production, API server reading `pages/menus_md/`). All valid architectural observations had already been incorporated into `docs/capability-assessment/`. | Detailed findings in Section 5. Recommended retaining deletion from root to avoid repo clutter and conflicting claims. | [Doc 08](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md) | None. File remains permanently recoverable in Git commit `1cab3de1`. |
| **F-07** | **Operational Authority Boundary Prematurely Hardcoded** (Doc 06 presented Kafoodie vs `venue.json` split as an agreed operational rule). | Reviewed culinary data governance and hospitality system boundaries. | `[Inferred]`. Technical boundaries cannot bind business or legal stakeholders without executive ratification. | Labeled the source-of-truth split between Kafoodie (recipes/allergens) and menu exports (presentation/prices) explicitly as `[Proposed]`. Clarified that ratification belongs to business leadership. | [Doc 06](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/06_CAPABILITY_GAPS_AND_DEVELOPMENT_PRIORITIES.md) | Requires formal business approval during operational rollout. |
| **F-08** | **Venue Offering Mischaracterized as a Relational Entity** (Doc 02 described Venue Offering as an implemented relational entity). | Inspected SQLite schema and generated JSON structure in `exports/`. | `[Database-verified]`. SQLite contains no `venue_offerings` table. The entity exists only as a nested JSON structure in `venue.json`. | Clarified that Venue Offering is a nested representation in generated artifacts, distinguishing conceptual models from implemented database structures. | [Doc 02](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/02_DATA_MODEL_AND_ENTITY_RELATIONSHIPS.md) | None. Database schema reality is established. |

---

## 3. Updated Architecture, System Maturity & Data Model Position

### 3.1 Architectural Maturity Model (The Three Discrete System Levels)

The repository must not be characterized as a single unified enterprise platform. In reality, the codebase comprises three distinct tiers of technical maturity:

```
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 1: OPERATIONAL DATA-PROCESSING & REVIEW TOOLS (WORKING)           │
│ • Menu Review UI (pages/menu-review.html)                              │
│ • Local Python Server (menu_review_server.py: GET & POST routes)       │
│ • SQLite Review Persistence (menu_review_state.sqlite3: issue_reviews)  │
│ • Discovered Media UI & Batch Downloader (pages/discovered-media.html) │
│ • Menu Explorer UI & Offline Explorer Builder (build_menu_explorer.py) │
│ • Venue Export Engine (build_venue_export.py: heuristic matching)      │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ Generates offline snapshots
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 2: DERIVED BUT DISCONNECTED ARTIFACTS (GENERATED / UNCONSUMED)   │
│ • Canonical Venue Export Model (exports/<Region>/<Venue>/venue.json)   │
│ • Human-Readable Venue Markdown (exports/<Region>/<Venue>/venue.md)    │
│ • Match Reports & Gap Registers (coverage metrics, unmatched dishes)   │
│ • Allergen Cross-Reference Indices (embedded in JSON structures)       │
│ *STATUS: Rich reconciled data exists, but NO interface currently reads it│
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ Conceptual alignment only
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 3: STATIC PROTOTYPES & DEMONSTRATION INTERFACES (MOCKUPS)        │
│ • Product Data Hub (pages/product-data.html: hardcoded mock table)     │
│ • Launch Readiness Tracker (pages/launch-readiness.html: demo sliders) │
│ • Chicken Liver Parfait (pages/recipes/chicken-liver-parfait...html)   │
│ • F&B Role Cross-check (pages/fnb-crosscheck.html: static matrix)      │
│ *STATUS: Pure client-side UI simulations; NO API, DB, or JSON backing  │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Level 1 — Working Operational Tools**:
   * *Capabilities*: Document ingestion, OCR/markdown defect triage, duplicate line remediation, local media downloading, multi-outlet menu exploration, and relational reconciliation.
   * *Runtime*: Python standard library HTTP server (`menu_review_server.py`), disk I/O, and single-table SQLite persistence.
2. **Level 2 — Derived but Disconnected Information**:
   * *Capabilities*: Rich data models synthesizing Kafoodie recipes, markdown prices, web metadata, and media assets into `venue.json`.
   * *Disconnect*: While the generation engine is operational and highly sophisticated (1,376 lines), **zero user interfaces consume `venue.json`**. It exists as an offline data compilation output.
3. **Level 3 — Demonstration Interfaces**:
   * *Capabilities*: Visual prototypes showcasing what an eventual product administration hub, dish specification SOP, launch checklist, or role cross-check could look like.
   * *Disconnect*: All data displayed is hardcoded HTML/DOM or in-memory dummy variables. They possess no persistence, no API connections, and no connection to `venue.json`.

---

### 3.2 Five-Tier Data Model Position

To avoid confusing conceptual domain modeling with implemented database structures, the data environment is partitioned into five clearly defined categories:

1. **Source Data (Authoritative Crawl Inputs)**:
   * `kafoodie/*.json`: Downloaded JSON files from Kafoodie outlet endpoints. Holds ingredients, recipe names, statutory allergen bitmasks, and nutrition.
   * `menus_md/*.md`: 103 Markdown files parsed from physical PDF menu cards. Master source for printed dish titles, section layouts, and retail prices.
   * `discovered_media.csv`: Crawled metadata indexing asset URLs, venue mapping, and MIME types.
   * `config/*.json`: Human-maintained configuration (`venues.json`, `aliases.json`, `rules.json`).
2. **Generated Data Artifacts (Offline Derived Snapshots)**:
   * `pages/menu-explorer-data.js`: 9.0 MB JavaScript bundle generated by `build_menu_explorer.py`, exporting `window.MENU_DATA`.
   * `exports/<Region>/<Venue>/venue.json`: Comprehensive structured venue model generated by `build_venue_export.py`.
   * `exports/<Region>/<Venue>/venue.md`: Markdown summary generated alongside `venue.json`.
3. **Runtime Application State**:
   * `menu_review_state.sqlite3`: Single SQLite table `issue_reviews` recording review decisions (`status`, `note`, `updated_at`) and duplicate line remediation history keyed by `(menu_name, source_hash, issue_id)`.
   * Browser `localStorage`: Client-side cache used by `menu-review.html` for local unpersisted UI state.
4. **Conceptual Domain Entities (Abstract Business Concepts)**:
   * Product, Recipe, Ingredient, Menu Item, Venue Offering. Useful for business capability analysis and UI wireframing, but **not** instantiated as individual relational database tables.
5. **Actual Implemented Database Entities**:
   * Exactly **one table** exists in SQL: `issue_reviews`.
   * Zero SQL tables exist for products, recipes, ingredients, prices, venues, or user accounts.

---

## 4. Verification Results: Full Functional Capability Suite

Following the Netlify decommissioning, all nine functional capabilities were subjected to live runtime execution, mutation, persistence, and isolation testing on local port 8769:

| # | Capability / Route | Test Method & Payload | Observed Result | Evidence | Limitations & Boundaries |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **`GET /api/menus`** | HTTP GET request to `/api/menus` | **PASS** (HTTP 200). Returned JSON array of 103 menu entries with `name`, `kind`, `hasPdf`, and file `bytes`. | `[Runtime-tested]`. Sample: `2026-Christmas-Day-Lunch.md` (1,252 bytes, hasPdf=True). | Read-only. Reflects flat files in `inncollectiongroup.com_root/menus_md/`. |
| **2** | **`GET /api/menu`** | HTTP GET with query param `?name=2026-Christmas-Day-Lunch.md` | **PASS** (HTTP 200). Delivered raw UTF-8 Markdown text and `X-Source-Hash` header. | `[Runtime-tested]`. SHA-256 header matched file bytes exactly (`d71306e9...`). | Read-only. Rejects directory traversal attempts. |
| **3** | **`GET /api/pdf`** | HTTP GET with query param `?name=2026-Christmas-Day-Lunch.md` | **PASS** (HTTP 200). Delivered binary stream with `Content-Type: application/pdf`. | `[Runtime-tested]`. Verified binary magic header bytes start with `%PDF-`. | Read-only. Rejects missing PDFs and invalid file paths with HTTP 404. |
| **4** | **`GET /api/issues`** | HTTP GET with query param `?name=2026-Christmas-Day-Lunch.md` | **PASS** (HTTP 200). Returned JSON object containing menu name, SHA-256 source hash, and existing triage decisions. | `[Runtime-tested]`. Successfully read review decisions from SQLite. | Read-only lookup against local SQLite table. |
| **5** | **`POST /api/issues`** | HTTP POST with JSON payload: `name`, `sourceHash`, `issueId: "headings"`, `status: "open"`, `note: "AUTOMATED_TEST..."` | **PASS** (HTTP 200). Persisted decision to SQLite table `issue_reviews`. Directly verified via SQL query, then cleanly removed test record. | `[Runtime-tested]` & `[Database-verified]`. Record wrote cleanly and was deleted with zero residual state. | Requires exact matching `sourceHash` or returns HTTP 409 conflict. |
| **6** | **`POST /api/issues/fix-duplicates`** | HTTP POST targeting an isolated dummy menu with duplicate lines: `lineNumbers: [4]`. | **PASS** (HTTP 200). Atomically rewritten via temporary file, line 4 removed, SHA-256 updated, review record updated to `fixed`. Cleanly removed test file and DB entry. | `[Runtime-tested]`. File was modified in place safely; verify clean recovery and zero lingering records. | Operates strictly on duplicate lines > 12 characters; requires matching `sourceHash`. |
| **7** | **`POST /api/export`** | Tested host validation (untrusted host `evil.com`) and asset fetch behavior (non-existent asset on valid host). | **PASS** (HTTP 400 for bad host; HTTP 207 Multi-Status for 404 asset). Handled failed download cleanly without crash. | `[Runtime-tested]`. Rejects untrusted domains; handles asset 404s gracefully in response payload. | Live media download depends on external host `www.inncollectiongroup.com` availability. |
| **8** | **Menu Explorer Build** | Executed `python3 build_menu_explorer.py --check` | **PASS** (Exit 0). Output: *"Menu explorer data and checklist are current."* | `[Runtime-tested]`. Validated data consistency between `kafoodie/` and `pages/menu-explorer-data.js`. | Check mode verifies data currency without rewriting files. |
| **9** | **Venue Export Build** | Executed `export_venue("The Kingslodge Inn")` inside an isolated temporary subpath. | **PASS** (Exit 0). Successfully generated `venue.json` (165 products, 130 dishes) and `venue.md`. Cleanly removed temporary folder. | `[Runtime-tested]`. Generated comprehensive canonical venue record and coverage statistics without touching master exports. | Compilation is an offline batch process; execution time scales with number of venues. |

---

## 5. Deleted Root Document Investigation (`05_COMPONENT_RELATIONSHIPS.md`)

The investigation into the deletion of `05_COMPONENT_RELATIONSHIPS.md` from the workspace root yielded the following findings:

1. **Git Tracking Status**:
   * The file **was tracked in Git**. It was committed in commit `1cab3de1a0558ffdd51f0ce54d438816bebc9566` (Sun Nov 22 10:47:07 2026) with the commit message *"docs: add comprehensive architecture documentation and project review files"*.
   * It was deleted in commit `e4dd7fc76e67641fbe94d82389dfd73241de7400` (Sun Nov 22 11:25:10 2026) during the Netlify decommissioning cleanup.
2. **Origin & Purpose**:
   * The document header explicitly identifies it as *"Knowledge Base · Document 5 of 10"*, originating from an earlier, uncoordinated 10-document draft sequence created before the structured assessment suite (`docs/capability-assessment/`) was standardized.
3. **Content Audit & Comparison with Document Suite**:
   * *Component Inventory*: Fully replicated in [Document 03](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/03_COMPONENT_AND_CAPABILITY_REGISTER.md).
   * *Existing Connections*: Fully replicated in [Document 05](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/05_INTEGRATION_AND_DEPENDENCY_REGISTER.md) and [Document 04](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/04_OPERATIONAL_WORKFLOW_MAP.md).
   * *Proposed Architecture*: Absorbed and refined in [Document 06](file:///Users/leandrodisconzi/repos/Inn-Collection-Group/docs/capability-assessment/06_CAPABILITY_GAPS_AND_DEVELOPMENT_PRIORITIES.md).
   * *Diagrams*: The Mermaid relationship diagrams in Document 01 and Document 05 represent cleaner, updated evolutions of the diagram in `05_COMPONENT_RELATIONSHIPS.md`.
4. **Superseded & Inaccurate Claims**:
   * `05_COMPONENT_RELATIONSHIPS.md` contained several claims now proven incorrect:
     - It designated Netlify (`SRV-2`) as the "Production" server.
     - It claimed `seed_reviews.json` was consumed on cold start to populate production SQLite.
     - It claimed `fix-duplicates` modified `pages/menus_md/` (whereas code inspection proves `menu_review_server.py` writes to `inncollectiongroup.com_root/menus_md/`).
5. **Recoverability & Recommendation**:
   * *Recoverability*: The file is permanently preserved and fully recoverable in Git history via `git show 1cab3de1:05_COMPONENT_RELATIONSHIPS.md`.
   * *Recommendation*: **Retain its deletion from the repository root**. Restoring it would reintroduce obsolete draft nomenclature ("Document 5 of 10"), conflicting Netlify claims, and root directory pollution. Zero unique or verified architectural information was lost by its removal.

---

## 6. Remaining Technical Uncertainties

The following items cannot be resolved through code inspection alone and require operational, business, or developmental clarification:

1. **Allergen & Regulatory Policy (`is_pw_allergen_not_set`)**:
   * While technical flags exist in `menu-explorer-data.js` and `venue.json` indicating un-set allergens, establishing statutory food safety compliance rules, guest-facing allergen filtering policies, or menu publication blockers is a legal and culinary governance decision that must be resolved by business leadership.
2. **Disposition of Orphaned Directory `pages/menus_md/`**:
   * Both markdown directories (`inncollectiongroup.com_root/menus_md/` and `pages/menus_md/`) are 100% byte-for-byte identical (103 files each).
   * Local server and build tools operate exclusively on `inncollectiongroup.com_root/menus_md/`.
   * With Netlify decommissioned, `pages/menus_md/` is completely orphaned. Deletion has been held in abeyance in compliance with mandate preservation rules, pending final operational authorization.
3. **Real-World ICG Production Systems**:
   * Actual operational platforms used by The Inn Collection Group for Point-of-Sale (EPOS), Enterprise Resource Planning (ERP), stock control, and corporate Single Sign-On (SSO) remain unverified. Vendor references in previous documentation were illustrative industry examples.
4. **Missing Kafoodie Outlets**:
   * Two properties (`Dean Court` and `The Bull's Head Inn`) remain excluded from Kafoodie crawls (`NO_KAFFODIE` in `build_menu_explorer.py:43`). Whether Kafoodie outlet IDs exist for these properties or whether they operate on distinct menu management systems requires external operational confirmation.
5. **Integration of Level 3 Demonstration Interfaces**:
   * Re-wiring `pages/product-data.html` and `pages/launch-readiness.html` to consume `venue.json` represents a core design objective for the upcoming system blueprint phase, transitioning them from static mockups to active data-driven tools.

---

## 7. Baseline Closure Assessment

### Classification: **READY WITH CAVEATS**

### Assessment Justification:
The technical baseline for The Inn Collection Group hospitality technology workspace is now closed and verified. 

1. **Why It Is Ready**:
   * The core application architecture is thoroughly understood and documented without contradiction across Documents 01 through 08.
   * Netlify has been completely excised with zero impact on local application functionality.
   * The local execution environment (`menu_review_server.py`), build pipelines (`build_menu_explorer.py`, `build_venue_export.py`), and SQLite persistence (`issue_reviews`) have been fully verified through live functional testing.
   * The boundaries between what is *working* (Level 1), what is *generated but unconsumed* (Level 2), and what is a *static mockup* (Level 3) are clearly established.
   * Conceptual domain entities have been strictly decoupled from implemented database structures.
2. **The Caveats to Carry Forward**:
   * **Caveat 1 (Data Flow Disconnect)**: The richest data model in the repository (`venue.json`) is not currently consumed by any front-end user interface.
   * **Caveat 2 (Missing Central Product DB)**: No multi-table relational database or centralized product management backend exists; product administration interfaces are static mockups.
   * **Caveat 3 (External Integrations Unknown)**: No connections exist to live EPOS, stock, or recipe management systems; the system operates on static crawl snapshots.
   * **Caveat 4 (Business Governance Needed)**: Allergen safety policies and the deletion of the orphaned `pages/menus_md/` duplicate directory require business stakeholder decisions.

These caveats do not block architectural design. Rather, they provide the exact, unambiguous evidentiary foundation required to design the complete system blueprint in the upcoming phase.
