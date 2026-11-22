# Document 15 — Architecture Blueprint Executive Summary

> **Knowledge Base** · Inn Collection Group (ICG) Hospitality Technology Workspace  
> **Document** 15 of 15 · Published: 2026-11-22  
> **Phase**: Phase 2 — Hospitality Technology Requirements, Target Architecture & Implementation Blueprint  
> **Evidence Standards**: `[Code-verified]` · `[Database-verified]` · `[Runtime-tested]` · `[Proposed]`

---

## 1. Executive Statement & Strategic Purpose

This executive summary synthesizes the findings and architectural specifications established across **Phase 2 (Documents 09 through 14)** for The Inn Collection Group (ICG) hospitality technology ecosystem.

It answers the five central strategic questions established in the Phase 2 mandate:
1. **What does the current system actually do?**
2. **What does a multi-site F&B operation need the system to support?**
3. **What architecture would support those requirements coherently?**
4. **How can existing work evolve into that architecture without unnecessary redevelopment?**
5. **What is the most sensible first implementation that demonstrates genuine operational value?**

---

## 2. Current Reality vs. Target State

```
CURRENT REPOSITORY REALITY                          TARGET ARCHITECTURAL SYSTEM
┌──────────────────────────────────────┐            ┌──────────────────────────────────────┐
│ • Local Python Server (stdlib)       │            │ • Integrated Modular Python Backend  │
│ • Single-table SQLite (issue_reviews)│            │ • Unified SQLite WAL Master Database │
│ • 103 Markdown master files          │            │ • Central Product, Recipe & Menu DB  │
│ • Unconsumed venue.json outputs      │   ═════►   │ • venue.json Wired to Active UIs     │
│ • Static prototype mockups (Product, │            │ • Active Operational Tools (Specs,   │
│   Launch Readiness, Costing Demo)    │            │   Launches, EPOS Prep, Margins)      │
│ • Heuristic token-matching build     │            │ • Automated Closed-Loop Pipelines    │
│ • Netlify excised; local runtime     │            │ • Secure, Multi-Role Governance      │
└──────────────────────────────────────┘            └──────────────────────────────────────┘
```

### Key Distinctions:
* **Current State**: The repository is an effective local data-processing, review, and reconciliation environment. It possesses operational document-review tools and sophisticated offline matching pipelines, but **it does not yet have an integrated operational data-management system**. Rich data exists in `venue.json`, but no user interface reads from it; the product catalog, launch tracker, and recipe specs are static mockups.
* **Target State**: A unified, modular hospitality management platform where commercial products, culinary recipes, ingredient costs, statutory allergens, printed menu cards, and till configurations are transactionally linked across all 29 estate inns.

---

## 3. Why the Proposed Architecture is Proportionate and Appropriate

1. **Rejects Premature Microservices**: The system serves 29–31 properties managed by a lean head-office culinary and operations team. A microservices architecture would introduce distributed network failures, eventual consistency lag in food safety data, and unnecessary DevOps complexity. The **modular monolith** approach provides strong ACID guarantees, sub-millisecond query execution, and rapid development velocity within a single Python runtime.
2. **Leverages SQLite in WAL Mode**: SQLite is already embedded in Python, requires zero server configuration or daemon management, and in Write-Ahead Logging (WAL) mode effortlessly handles concurrent multi-threaded reads and writes. A migration to PostgreSQL is established as an explicit Phase 4 trigger, warranted only if remote multi-tenant hosting or complex clustering becomes necessary.
3. **Enhances Vanilla Web Workspaces**: The existing single-page applications in `pages/` have zero external framework overhead, load in under 50 milliseconds, and run in any modern browser without npm compilation pipelines. Extending them with shared design tokens preserves speed and eliminates build tooling friction.

---

## 4. Mapping Operational Requirements to Technical Capabilities

In [Document 09](./09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md), 40 operational responsibilities from the F&B Coordinator role were mapped into the technical architecture. The core functional mappings are summarized below:

| Operational Responsibility | Target Technical Capability | Supporting Architecture / Module | Target Milestone |
| :--- | :--- | :--- | :---: |
| **Menu Administration** | Structured CRUD API for menus, sections, and items | Menu Management Module & REST API | Phase 1 & 2 |
| **Recipe Specifications** | Structured Bills of Materials (BOM), portion yields, prep SOPs | Product & Recipe Module (`recipes`, `recipe_ingredients`) | Phase 2 |
| **Food Safety & Allergens** | 14 statutory allergen bitmask calculation & un-set compliance gate | Food Safety & Allergen Module (`allergen_declarations`) | Phase 2 |
| **Commercial Management** | Dish COGS calculation & Gross Profit % margin modeling (20% VAT) | Commercial Engine Module (`prices`, margin formulas) | Phase 2 |
| **Supplier Purchasing** | Purveyor catalog, pack sizes, and kitchen unit conversion (£/g) | Supplier & Purchasing Module (`supplier_products`) | Phase 3 |
| **EPOS Coordination** | PLU code assignment, screen formatting, and till price QA audits | EPOS Adapter Module (`epos_mappings`, CSV exporter) | Phase 3 |
| **Seasonal Launches** | Campaign milestone checklist, RAG tracker, kitchen Spec Books | Launch Orchestrator (`launch_tasks`, WeasyPrint PDF) | Phase 3 |
| **Multi-Site Coordination**| 29-inn estate directory, regional menus, variance comparison | Multi-Site Module (`build_venue_export.py`, Explorer) | Phase 1 & 3 |
| **Data Quality Governance**| Closed-loop rebuilds, gap registers, tamper-evident audit logs | Governance Module (`audit_events`, automated triggers)| Phase 1 & 4 |

---

## 5. Asset Salvage vs. What Needs to be Built

As established in [Document 13](./13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md), the architecture maximizes asset reuse:

* **100% Reused Without Re-engineering**:
  * The heuristic token-matching algorithm in `build_venue_export.py` (lines 423–530).
  * The atomic file-rewriting engine with fsync in `menu_review_server.py`.
  * The PDF inspection and dual-pane synchronization logic in `pages/menu-review.html`.
  * The batch media downloader with domain safety locks in `menu_review_server.py`.
  * The 103 audited Markdown menu files in `inncollectiongroup.com_root/menus_md/`.
* **What Needs to be Built / Rebuilt**:
  * Expand SQLite schema from 1 table to 14 core operational tables.
  * Rebuild `pages/product-data.html` from a static table into an active master catalog consuming `venue.json:products[]`.
  * Rebuild `pages/launch-readiness.html` milestone checkboxes to persist in SQLite `launch_tasks`.
  * Rebuild the hardcoded Parfait layout into a dynamic, parameterized Spec Book template.
  * Connect Menu Review duplicate line fixes directly to automated `build_venue_export.py` execution.

---

## 6. Implementation Priorities: The "Walking Skeleton" First

As detailed in [Document 14](./14_IMPLEMENTATION_ROADMAP_AND_PRIORITISATION.md), implementation begins with the **Walking Skeleton** in Sprint 1:

```
[Menu Review UI]
      │ 1. Coordinator remediates duplicate line in menu markdown
      ▼
[menu_review_server.py]
      │ 2. Atomically rewrites markdown & updates SQLite issue_reviews
      │ 3. Automated hook immediately triggers build_venue_export.py
      ▼
[venue.json]
      │ 4. Recompiled canonical venue model updates coverage & products
      ▼
[Product Data UI (pages/product-data.html)]
      │ 5. Reads recompiled venue.json:products[] via GET /api/products
      ▼
[Verified Outcome]
A document edit in Menu Review instantly reflects in the Master Product Catalog!
```

### Full Four-Phase Rollout:
1. **Phase 1: Foundation & Canonical Persistence (Weeks 1–3)**: Walking skeleton, unified SQLite WAL schema, closed-loop rebuild triggers, and purging the orphaned `pages/menus_md/` duplicate directory.
2. **Phase 2: Core Operational Functionality (Weeks 4–7)**: Master SKU catalog, recipe BOM formulations, 14 statutory allergen governance, and commercial margin modeling.
3. **Phase 3: Workflow Orchestration & Systems Prep (Weeks 8–11)**: Seasonal launch trackers, automated kitchen Spec Book PDF generation, EPOS PLU mapping, and supplier unit conversions.
4. **Phase 4: Advanced Intelligence & Integration (Weeks 12+)**: Menu engineering scatter plots (Stars/Dogs), supplier inflation modeling, and enterprise SSO.

---

## 7. Outstanding Governance Decisions Requiring Business Ratification

The following non-technical decisions must be confirmed by business and culinary leadership:
1. **Source of Truth Ratification**: Formal adoption of the proposed authority boundary: Kafoodie as authoritative for central recipes/allergens; the Menu Management module as authoritative for guest presentation and retail prices.
2. **Allergen Publication Policy**: Executive approval of the software compliance rule that strictly blocks public menu publication for any dish with `is_pw_allergen_not_set == true`.
3. **Orphaned Directory Deletion**: Final administrative authorization to permanently delete the redundant `pages/menus_md/` directory.
4. **Missing Kafoodie Properties**: Operational investigation to obtain Kafoodie outlet IDs for Dean Court and The Bull's Head Inn.
5. **Real-World IT Vendor Selection**: Identification of actual ICG production vendors for EPOS (till integration) and Procurement/ERP to tailor Phase 3 export adapters.

---

## 8. Directory of Phase 2 Architectural Deliverables

* [Document 09 — Operational Requirements and Capability Mapping](./09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md)
* [Document 10 — Target Data Architecture and Entity Model](./10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md)
* [Document 11 — Target Application and Integration Architecture](./11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md)
* [Document 12 — End-to-End Operational Workflow Design](./12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md)
* [Document 13 — Current-to-Target Architecture Transition Map](./13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md)
* [Document 14 — Implementation Roadmap and Prioritisation](./14_IMPLEMENTATION_ROADMAP_AND_PRIORITISATION.md)
* [Document 15 — Architecture Blueprint Executive Summary](./15_ARCHITECTURE_BLUEPRINT_EXECUTIVE_SUMMARY.md)
