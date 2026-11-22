# 07 — Architectural Gaps & Decision Register

## 1. Prioritised Gap & Decision Matrix

This register classifies unresolved architectural tensions, technical debt, and system boundaries across the repository.

Each item is categorized by urgency and dependency:
* `[CRITICAL]`: Must be resolved before the workspace architecture can be finalized.
* `[HIGH]`: Necessary for production operational safety and multi-site reliability.
* `[MEDIUM]`: Structural improvements that can be scheduled during product evolution.
* `[LOW]`: Quality-of-life and interface refinements.
* `[EXTERNAL]`: Blocked on third-party systems (Kafoodie, EPOS vendor, print agency).
* `[APPROVAL]`: Operational capability requiring explicit culinary/legal governance.

---

## 2. Critical Architectural Gaps

### GAP-01: Dual Source of Truth (Kafoodie vs. Printed Menus)
* **Classification**: `[CRITICAL]`
* **Code Evidence**: In `build_venue_export.py:58-69`, printed menu items from Markdown provide section names, dish titles, and guest prices, while Kafoodie outlet JSON provides allergens, nutrition, and dietary tags.
* **The Tension**: If a dish description or ingredient changes, which system is authoritative? Currently, Kafoodie holds recipe components, but printed PDFs often contain updated chef descriptions and marketing tags not present in Kafoodie.
* **Decision Required**: Establish that **Kafoodie is the authoritative source for culinary ingredients, allergens, and nutritional profiles**, while **the Menu Export (`venue.json`) is the authoritative source for guest presentation, price, and venue availability**.

### GAP-02: Allergen Provenance & The "Un-set" Vulnerability
* **Classification**: `[CRITICAL]` / `[APPROVAL]`
* **Code Evidence**: `pages/menu-explorer.html:78`, `pages/menu-explorer.html:139`, and `build_venue_export.py:581` explicitly track the field `is_pw_allergen_not_set`.
* **The Tension**: When `is_pw_allergen_not_set` is true, the recipe has no declared allergens not because it is allergen-free, but because a chef has **not yet filled in the allergen profile**. In the current explorer, this displays a small amber warning, but does not block the dish from appearing on menus.
* **Decision Required**: Enforce a strict food safety rule: any dish with `is_pw_allergen_not_set == true` must be marked with a prominent compliance blocker and automatically excluded from guest-facing "free-from" filtering.

### GAP-03: File Duplication Across Repository Directories
* **Classification**: `[HIGH]`
* **Code Evidence**: Extracted Markdown files are stored in two duplicate folders:
  1. `inncollectiongroup.com_root/menus_md/` (104 files)
  2. `pages/menus_md/` (104 files)
* **The Tension**: Editing a menu via `menu_review_server.py` modifies the file in `inncollectiongroup.com_root/menus_md/`. However, Netlify deploys from `pages/`, meaning changes made during local review do not automatically deploy to Netlify unless manually copied.
* **Decision Required**: Eliminate `pages/menus_md/` as a static duplicate. Configure Netlify build scripts or symlinks to publish directly from the canonical data root.

---

## 3. High-Priority Gaps

### GAP-04: Lack of Universal Product / EPOS Identifiers
* **Classification**: `[HIGH]` / `[EXTERNAL]`
* **Code Evidence**: Kafoodie uses internal numeric recipe IDs (e.g. `5323684`). Printed menus have no codes. EPOS PLU numbers are mentioned in `pages/launch-readiness.html` but do not exist anywhere in the code or data schemas.
* **The Tension**: Reconciliation between printed dishes and recipes currently relies on heuristic text matching and alias tables (`config/aliases.json`). If an inn changes "Cumberland Sausage" to "Cumberland Bangers", matching drops unless an alias is manually written.
* **Decision Required**: Introduce a persistent `product_code` (PLU / Master SKU) into both Kafoodie recipe metadata and menu Markdown files (e.g. `<!-- plu: 1042 -->`).

### GAP-05: Unpersisted Editorial State in Launch Readiness & Cross-Check
* **Classification**: `[HIGH]`
* **Code Evidence**: Both `pages/launch-readiness.html` and `pages/fnb-crosscheck.html` store all state in client-side JavaScript memory.
* **The Tension**: Any edits, checklist tick-offs, or note additions are lost upon page reload.
* **Decision Required**: Extend the SQLite schema (`menu_review_state.sqlite3`) or Netlify persistence layer to include tables for `launch_checklists` and `operational_notes`.

### GAP-06: Missing Outlets for Discovered Venues
* **Classification**: `[HIGH]`
* **Code Evidence**: `build_menu_explorer.py:43` explicitly defines:
  ```python
  NO_KAFFODIE = ["Dean Court", "The Bull's Head Inn"]
  ```
* **The Tension**: While 29 inns have full Kafoodie outlet crawls, Dean Court and The Bull's Head Inn have printed menu Markdown but zero Kafoodie recipe data. Consequently, they cannot appear in Menu Explorer.
* **Decision Required**: Obtain the Kafoodie outlet IDs for these two properties or establish a fallback local recipe data store for properties pending Kafoodie onboarding.

---

## 4. Medium & Architectural Scaling Considerations

### GAP-07: Versioning and Historical Traceability
* **Classification**: `[MEDIUM]`
* **Code Evidence**: Menu versioning is currently managed via filename suffix conventions (`Crown-Menu-The-Tynemouth-Castle-Inn-DIGITAL-WEB-v2.md`). `build_venue_export.py:189-197` implements a regex `latest_versions()` function that keeps only the highest `-vN`.
* **Recommendation**: Formalize version metadata into the YAML/Markdown frontmatter of menu files (e.g., `version: 2.1`, `effective_date: 2026-10-01`, `supersedes: v2.0`).

### GAP-08: Access Control, Permissions & Multi-Tenant Boundaries
* **Classification**: `[MEDIUM]`
* **Code Evidence**: All endpoints in `menu_review_server.py` and `netlify/functions/api.py` are unauthenticated. Anyone with network access can trigger `/api/issues/fix-duplicates` or modify review records.
* **Recommendation**: Introduce role-based access control (RBAC) distinguishing between Read-Only (Front of House, General Managers) and Read-Write/Approve (Head Chefs, Central F&B Directors).
