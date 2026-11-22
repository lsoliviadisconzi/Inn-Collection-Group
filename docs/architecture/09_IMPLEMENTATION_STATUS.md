# 09 — Implementation Status Register

## 1. Evidence-Based Assessment Standards

To ensure complete technical rigor and eliminate speculation, every component in this repository is evaluated across **seven distinct evidence dimensions**. 

These dimensions are not a linear progression; a component may be implemented and populated with real data without being documented or tested:

1. **Documented**: Clear specifications, schemas, or architectural markdown exist explaining its design.
2. **Designed**: UI/UX patterns, user flows, and interface layouts have been established.
3. **Implemented**: Working, executable code (HTML, JS, Python, SQL) exists in the repository.
4. **Tested**: Automated unit/integration tests or formal validation flags exist.
5. **Populated**: Loaded with real, production-grade operational data rather than synthetic placeholder text.
6. **Integrated**: Programmatically connected to other systems, services, or data pipelines.
7. **Operational**: Actively deployed and usable in daily hospitality operations.

---

## 2. Comprehensive Component Status Matrix

| Component / Subsystem | Documented | Designed | Implemented | Tested | Populated | Integrated | Operational | Evidence & Code References |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Chicken Liver Parfait Page** | Partial | **Yes** | **Yes** | No | **Yes** | No | `[OBSERVED]` | `pages/recipes/chicken-liver-parfait...html`. Rich static UI with real recipe & pricing data; hardcoded, zero backend. |
| **Discovered Media Interface** | No | **Yes** | **Yes** | No | **Yes** | Partial | `[OBSERVED]` | `pages/discovered-media.html`. Loads real `discovered_media.csv`; connected to export endpoints in API. |
| **F&B Role Cross-check** | No | **Yes** | **Yes** | No | Partial | No | `[OBSERVED]` | `pages/fnb-crosscheck.html`. Inlines 100+ static requirements; no backend persistence or external syncing. |
| **Launch Readiness Interface** | No | **Yes** | **Yes** | No | No | No | `[OBSERVED]` | `pages/launch-readiness.html`. Comprehensive UI prototype; operates entirely in volatile client-side memory. |
| **Menu Explorer** | Partial | **Yes** | **Yes** | No | **Yes** | **Yes** | `[CODE-VERIFIED]` | `pages/menu-explorer.html`. Full 6-view suite; loads `menu-explorer-data.js` compiled from real Kafoodie crawls. |
| **Menu Review Interface** | Partial | **Yes** | **Yes** | No | **Yes** | **Yes** | `[CODE-VERIFIED]` | `pages/menu-review.html`. Real API integration (`/api/menus`, `/api/issues`); writes directly to SQLite database. |
| **Product Data Interface** | No | **Yes** | Partial | No | No | No | `[OBSERVED]` | `pages/product-data.html`. Demonstrates master catalog layout; populated with mock/dummy records. |
| **Local Dev Server** | No | **Yes** | **Yes** | No | — | **Yes** | `[CODE-VERIFIED]` | `menu_review_server.py`. 615 lines of stdlib Python; hosts static files, issues review API, and file downloads. |
| **Netlify Serverless API** | No | **Yes** | **Yes** | No | — | **Yes** | `[CODE-VERIFIED]` | `netlify/functions/api.py`. AWS Lambda / Netlify Function implementation; in-memory SQLite + ZIP exports. |
| **Menu Explorer Builder** | Partial | **Yes** | **Yes** | Partial | **Yes** | **Yes** | `[CODE-VERIFIED]` | `build_menu_explorer.py`. CLI pipeline with `--check` and `--prune` flags; builds data bundle for 29 venues. |
| **Venue Export Engine** | **Yes** | **Yes** | **Yes** | Partial | **Yes** | Partial | `[CODE-VERIFIED]` | `build_venue_export.py` (1,376 lines) & `docs/VENUE-EXPORT-SPEC.md`. Merges Markdown, Kafoodie, web crawl. |
| **Menu Markdown Spec** | **Yes** | **Yes** | **Yes** | No | **Yes** | **Yes** | `[CODE-VERIFIED]` | `docs/MENU-MD-SPEC.md`. 104 menu markdown files strictly follow this structural specification. |
| **SQLite Review Database** | No | **Yes** | **Yes** | No | **Yes** | **Yes** | `[CODE-VERIFIED]` | `menu_review_state.sqlite3`. Contains real `issue_reviews` table seeded with menu triage decisions. |
| **Configuration Subsystem** | Partial | **Yes** | **Yes** | No | **Yes** | **Yes** | `[CODE-VERIFIED]` | `config/venues.json`, `config/aliases.json`, `config/rules.json`. Actively loaded by build pipelines. |

---

## 3. Detailed Component Evidence Notes

### High-Maturity Components (Ready for Immediate Consolidation)
1. **`build_venue_export.py` & `VENUE-EXPORT-SPEC.md`**:
   * *Status*: This is the architectural crown jewel of the backend. It successfully parses complex multi-column printed Markdown menus, loads Kafoodie JSON feeds, maps dietary codes, and matches dishes via exact, alias, and token heuristics.
   * *Evidence*: Produces production-grade `exports/<Region>/<Venue>/venue.json` with comprehensive `matchReport` audits.
2. **`pages/menu-explorer.html` & `build_menu_explorer.py`**:
   * *Status*: Highly polished, extremely fast client-side explorer. Real data across 29 properties.
   * *Evidence*: Zero-latency allergen matrix filtering, cross-venue diffing, and nutrition breakdown.
3. **`pages/menu-review.html` & `menu_review_server.py`**:
   * *Status*: True bi-directional editorial environment with working persistence and concurrency protection (`X-Source-Hash`).
   * *Evidence*: Successfully identifies repeated lines and OCR issues; atomic duplicate line removal operates reliably.

### Prototypes & Demonstration Components (Requiring Engineering Backing)
1. **`pages/recipes/chicken-liver-parfait-the-lindisfarne-inn.html`**:
   * *Status*: Outstanding UI/UX design and operational depth, but strictly a hardcoded static prototype.
   * *Action*: Deconstruct into a dynamic template populated from `venue.json`.
2. **`pages/product-data.html`**:
   * *Status*: Pure design mockup. No live data feeds.
   * *Action*: Bind to the `products[]` array generated by `build_venue_export.py`.
3. **`pages/launch-readiness.html`**:
   * *Status*: High-fidelity visual mockup. All checklist state is in volatile DOM memory.
   * *Action*: Wire into SQLite backend and auto-populate metrics from `venue.json:coverage`.
