# Document 11 — Target Application and Integration Architecture

> **Knowledge Base** · Inn Collection Group (ICG) Hospitality Technology Workspace  
> **Document** 11 of 15 · Published: 2026-11-22  
> **Phase**: Phase 2 — Hospitality Technology Requirements, Target Architecture & Implementation Blueprint  
> **Evidence Standards**: `[Code-verified]` · `[Database-verified]` · `[Proposed]` · `[Requires-confirmation]`

---

## 1. Executive Summary & Architecture Strategy

This document establishes the application, API, integration, security, and technology architecture for the target Inn Collection Group (ICG) hospitality technology platform.

A foundational architectural principle governs this design:
> **Proportionate Engineering**: Avoid premature microservices, distributed complexity, and excessive infrastructure. Build a clean, maintainable **modular application** centered around operational workflows rather than theoretical software patterns.

The current system is an effective local data-processing environment comprising a single-threaded/multi-threaded Python standard library server (`menu_review_server.py`), two batch build scripts, and seven isolated HTML interfaces. 

The target application architecture unifies these capabilities into a **cohesive modular architecture** powered by an extended local Python backend, structured REST APIs, an integrated SQLite operational database, and unified web workspaces.

---

## 2. Target Application Component Decomposition

The application layer is structured into ten cohesive functional modules:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   TARGET APPLICATION ARCHITECTURE (MODULAR BACKEND)             │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                 REST ROUTING & DISPATCH                          │
├────────────────────────┬────────────────────────┬────────────────────────────────┤
│ 1. MENU MANAGEMENT     │ 2. PRODUCT & RECIPE    │ 3. FOOD SAFETY & ALLERGENS     │
│ • Menu Authoring API   │ • Master SKU Catalog   │ • 14 FIR Allergen Engine       │
│ • Section Ordering     │ • Recipe Formulation   │ • Un-set Allergen Gate         │
│ • Item Pricing Sync    │ • Ingredient BOM Cost  │ • Supplier Spec Sheets         │
├────────────────────────┼────────────────────────┼────────────────────────────────┤
│ 4. COMMERCIAL ENGINE   │ 5. SUPPLIER & PURCHASE │ 6. EPOS ADAPTER & MAPPING      │
│ • Margin & GP% Calc    │ • Purveyor Registry    │ • PLU Code Assignment          │
│ • Price Tier Hierarchy │ • Pack-to-Kitchen Unit │ • Till Category Formatting     │
│ • Cost Shift Modeling  │ • Price Change History │ • Pre-launch Till QA           │
├────────────────────────┼────────────────────────┼────────────────────────────────┤
│ 7. LAUNCH ORCHESTRATOR │ 8. MULTI-SITE RECON    │ 9. MEDIA & DOCUMENT QC         │
│ • Campaign Milestones  │ • 29-Inn Directory     │ • Menu Review & Triage         │
│ • Spec Book Generator  │ • Cross-Site Variance  │ • Duplicate Line Remediation   │
│ • Venue Readiness RAG  │ • Heuristic Matcher    │ • Batch Media Exporter         │
├────────────────────────┴────────────────────────┴────────────────────────────────┤
│ 10. GOVERNANCE, RBAC & AUDIT LOGGING                                             │
│ • User Roles & Permissions • Tamper-evident Audit Trail • Provenance Tracking    │
├──────────────────────────────────────────────────────────────────────────────────┤
│                  OPERATIONAL DATA LAYER (SQLite WAL / ACID)                      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Module Responsibilities:
1. **Menu Management Module**: Provides CRUD operations for master menus, sections, and menu items. Manages menu lifecycle states (`Draft`, `Review`, `Approved`, `Published`, `Archived`). Replaces raw manual markdown editing with structured endpoints.
2. **Product & Recipe Module**: Manages commercial product records (SKUs), culinary recipes, ingredient lists (Bills of Materials), yields, portion sizes, and prep instructions. Bridges central kitchen formulations to sellable menu items.
3. **Food Safety & Allergen Module**: Manages the 14 statutory allergens per UK Food Information Regulations (FIR). Provides automated bitmask calculation, tracks containment types (`Contains`, `May Contain`), and enforces compliance gates for un-set flags (`is_pw_allergen_not_set`).
4. **Commercial Engine Module**: Computes dish Cost of Goods Sold (COGS), net selling prices excluding 20% VAT, and gross profit percentages ($\text{GP\%} = \frac{\text{Net Price} - \text{COGS}}{\text{Net Price}}$). Models price-tier variations and cost-inflation impact across recipes.
5. **Supplier & Purchasing Module**: Catalogs approved suppliers, purchasing pack sizes, order units, and net case costs. Handles unit conversions (e.g. converting a 6x1kg case into recipe gram portions).
6. **EPOS Adapter & Mapping Module**: Assigns Price Look-Up (PLU) numbers, button labels, and kitchen printer routes. Prepares importable till configuration files and conducts pre-release price-verification audits.
7. **Launch Orchestrator Module**: Manages seasonal menu campaigns, cross-functional milestone checklists (Marketing, Operations, F&B, Finance), compiles kitchen "Spec Books" (PDF recipe/plating cards), and tracks venue-by-venue sign-offs.
8. **Multi-Site Reconciliation Module**: Houses the 29-inn estate directory across 7 operating regions. Executes heuristic token reconciliation between printed menu titles and Kafoodie recipes (`build_venue_export.py`).
9. **Media & Document QC Module**: Retains and extends the verified capabilities of `menu_review_server.py`: side-by-side PDF/Markdown inspection, atomic duplicate line fixes, and batch media downloading.
10. **Governance & Audit Module**: Manages user identities, role-based access control (RBAC), and writes append-only event logs capturing all menu, recipe, allergen, and price modifications.

---

## 3. Justification for a Modular Monolith (Vs. Microservices)

A deliberate architectural decision has been made: **Do NOT adopt a microservices architecture**.

| Architectural Dimension | Microservices Approach | Proposed Modular Monolith | Rationale & Justification |
| :--- | :--- | :--- | :--- |
| **Operational Complexity** | High. Multiple services, RPC protocols, network latency, distributed transactions. | Low. Single unified Python application running locally or on a standard internal VM. | The ICG estate comprises 29–31 properties managed by a lean head-office F&B team. Distributed infrastructure adds immense overhead with zero operational benefit. |
| **Data Consistency** | Eventual consistency; complex saga patterns across menu, recipe, and price services. | Strong ACID consistency via SQLite WAL mode. | Culinary recipes, allergens, and menu prices require strict transactional consistency; food safety compliance cannot tolerate eventual-consistency lag. |
| **Deployment Footprint** | Docker, Kubernetes, API Gateways, service meshes, distributed monitoring. | Zero-dependency or single virtualenv standard Python deployment. | Matches existing repository reality; can be run on a local workstation or deployed on an internal server in minutes without DevOps overhead. |
| **Development Velocity** | Significant cross-service boilerplate, contract testing, and network mocking. | Direct Python module imports and shared data models. | Allows rapid implementation of end-to-end operational workflows (e.g. Product -> Recipe -> Allergen -> Menu Item -> Price). |

---

## 4. API and Integration Architecture

### 4.1 Internal RESTful API Specification

The target architecture defines a clean RESTful interface extending the existing `menu_review_server.py`:

```
MENU & ITEM MANAGEMENT
GET    /api/menus                      List all master menus with metadata and review status
POST   /api/menus                      Create a new seasonal menu definition
GET    /api/menus/{id}                 Retrieve complete menu hierarchy (sections + items)
PUT    /api/menus/{id}                 Update menu metadata (dates, brand, title)
POST   /api/menus/{id}/sections        Add a section to a menu
POST   /api/menus/{id}/items           Add a menu item to a section (with price & copy)
PUT    /api/menus/{id}/items/{item_id} Update item details, pricing, or dietary tags
POST   /api/menus/{id}/publish         Publish approved menu (triggers export compile)

PRODUCT & RECIPE CATALOG
GET    /api/products                   List commercial products (master SKUs)
POST   /api/products                   Register a new commercial product
GET    /api/products/{id}              Retrieve product with linked recipe, allergens, and venues
GET    /api/recipes                    List culinary recipe specifications
POST   /api/recipes                    Create or update recipe specification (BOM ingredients)
GET    /api/recipes/{id}/allergens     Retrieve statutory allergen matrix and verification status

COMMERCIAL & PRICING
GET    /api/pricing/tiers              List estate pricing tiers and assigned venues
POST   /api/pricing/calculate-margin   Model GP% from cost and retail price
POST   /api/pricing/simulate-cost-rise Simulate margin impact of supplier price increases

EPOS & INTEGRATION
GET    /api/epos/mappings              List PLU code mappings across products and venues
POST   /api/epos/mappings              Assign or update PLU codes and till screen categories
GET    /api/epos/export?format={csv}   Generate importable till configuration payload
POST   /api/epos/validate-pricing      Audit till prices against approved menu prices

LAUNCH ORCHESTRATION
GET    /api/launches                   List seasonal launch campaigns
POST   /api/launches                   Create seasonal launch campaign
GET    /api/launches/{id}/readiness    Retrieve estate readiness breakdown across 29 inns
PUT    /api/launches/{id}/tasks/{task} Update milestone RAG status
GET    /api/launches/{id}/spec-book    Generate compiled kitchen Spec Book (PDF stream)

EXISTING & QC APIS (RETAINED)
GET    /api/issues?name=...            Retrieve menu triage issues from SQLite [RETAINED]
POST   /api/issues                     Persist issue review status [RETAINED]
POST   /api/issues/fix-duplicates      Atomic duplicate line removal [RETAINED]
POST   /api/export                     Batch download media assets [RETAINED]
GET    /api/pdf?name=...               Stream original menu PDF [RETAINED]
```

---

### 4.2 External Integration Boundaries

The integration landscape strictly separates verified internal systems from hypothetical external platforms:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL INTEGRATION BOUNDARIES                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. UPSTREAM RECIPE INGESTION (Kafoodie Enterprise Portal)              │
│ • Mechanism: Scheduled script / API client (caching to kafoodie/*.json) │
│ • Boundary: Read-only ingestion. No writes back to Kafoodie.           │
│ • Data Flow: Recipe text, preliminary allergens, nutrition profiles.   │
├────────────────────────────────────────────────────────────────────────┤
│ 2. SUPPLIER CATALOG & PROCUREMENT FEEDS                                │
│ • Mechanism: Standardized CSV / Excel batch import.                    │
│ • Boundary: Ingests supplier SKU, pack size, and case price.           │
│ • Vendor Platform: Unspecified (abstracted via generic import schema). │
├────────────────────────────────────────────────────────────────────────┤
│ 3. POINT-OF-SALE (EPOS) EXPORT BOUNDARY                                │
│ • Mechanism: File-based export (CSV / XML) & Pre-release QA validator. │
│ • Boundary: Prepares verified PLUs and prices; till vendor imports.    │
│ • Vendor Platform: Unspecified (e.g. Zonal, Micros, Tevalis abstract). │
├────────────────────────────────────────────────────────────────────────┤
│ 4. SINGLE SIGN-ON (SSO) & STAFF DIRECTORY                              │
│ • Mechanism: OIDC / SAML 2.0 reverse-proxy integration (Phase 4).      │
│ • Boundary: Maps corporate identity to platform roles (Chef, Coord).   │
│ • Identity Provider: Unspecified (e.g. Okta, Azure AD abstract).       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Security, Access Control & Data Governance

1. **Authentication & Session Security**:
   * *Phase 1–3*: Lightweight session token authentication built on standard secure HTTP-only cookies.
   * *Phase 4*: Enterprise Single Sign-On (SSO) via OpenID Connect (OIDC).
2. **Role-Based Access Control (RBAC)**:
   * **F&B Coordinator**: Full access to menus, products, pricing, launch checklists, and triage tools.
   * **Development / Executive Chef**: Authoring rights for recipes, ingredients, and prep SOPs; read-only for commercial margins.
   * **Food Safety Compliance Officer**: Exclusive certification authority for allergen declarations and supplier spec sheet sign-offs.
   * **Commercial Manager**: Exclusive approval authority for retail selling prices and target margin thresholds.
   * **General Manager / Site Team**: Read-only access to published venue menus, kitchen Spec Books, and site readiness sign-off.
3. **Data Provenance & Audit Trails**:
   * Every write operation writes an immutable entry to `audit_events` recording `(user_id, timestamp, entity_table, entity_id, diff_json)`.
   * Allergen modifications require an explicit audit note and attached supplier spec reference.

---

## 6. Technology Evaluation & Recommendations

| Architectural Layer | Current Prototype | Evaluated Options | Target Recommendation | Rationale & Trade-offs |
| :--- | :--- | :--- | :--- | :--- |
| **Backend Runtime** | Python 3 standard library `http.server` | 1. Retain `http.server`<br/>2. **FastAPI** (Python 3.11+)<br/>3. Flask | **FastAPI (or enhanced stdlib)** | FastAPI provides automatic OpenAPI documentation, strict Pydantic data validation, async support, and rapid endpoint definition while staying within the Python ecosystem. Alternatively, stdlib can be extended with a lightweight router to keep zero pip dependencies for initial phases. |
| **Operational Database** | SQLite 3 (single table `issue_reviews`) | 1. **SQLite (WAL Mode)**<br/>2. PostgreSQL<br/>3. MongoDB | **SQLite 3 in WAL Mode** | SQLite is already embedded in Python, requires zero server administration, and handles multi-threaded concurrent reads/writes with ease. Criteria to migrate to PostgreSQL: multi-user remote hosting, concurrent multi-master writes, or database clustering (Phase 4). |
| **Frontend Architecture** | Vanilla HTML5, CSS3, ES6 JavaScript | 1. **Vanilla JS Modular SPA**<br/>2. React + Vite<br/>3. Streamlit | **Vanilla JS (Enhanced) / Vite SPA** | The existing seven HTML interfaces are fast, lightweight, and have zero external framework dependencies. Extending them with shared CSS design tokens and a unified client navigation shell maintains rapid execution and eliminates build tooling friction. |
| **Document Generation** | Static HTML / DOM rendering | 1. Client-side print CSS<br/>2. **WeasyPrint** (Python)<br/>3. ReportLab | **WeasyPrint** | Converts HTML5/CSS3 templates directly into high-fidelity, print-ready PDF Spec Books and Allergen Matrices with precise page breaks, headers, and CMYK color profiles. |
