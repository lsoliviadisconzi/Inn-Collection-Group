# Document 09 — Operational Requirements and Capability Mapping

> **Knowledge Base** · Inn Collection Group (ICG) Hospitality Technology Workspace  
> **Document** 09 of 15 · Published: 2026-11-22  
> **Phase**: Phase 2 — Hospitality Technology Requirements, Target Architecture & Implementation Blueprint  
> **Evidence Standards**: `[Code-verified]` · `[Database-verified]` · `[Runtime-tested]` · `[Data-verified]` · `[Documented]` · `[Observed]` · `[Inferred]` · `[Proposed]` · `[Unknown]` · `[Requires-confirmation]`

---

## 1. Executive Summary & Purpose

This document establishes the operational requirements foundation for the Inn Collection Group (ICG) hospitality technology architecture. Moving from the technical baseline established in Documents 01–08, this document translates the real-world operational responsibilities of the Food & Beverage (F&B) Coordinator into a structured, technical capability model.

A core operational principle guides this requirements engineering:
> *"Software always asks people to learn software. The objective is to make software understand the way people actually work."*

Rather than designing technology for its own sake or proposing premature enterprise abstractions, this document grounds every system requirement in concrete hospitality activities: maintaining menus, managing recipes, verifying food safety and allergens, tracking costs and margins, preparing till configurations, orchestrating seasonal rollouts across 29–31 properties, and facilitating cross-departmental coordination.

---

## 2. Deliverable A: Technical Baseline Correction Register

In accordance with Workstream A instructions, the six outstanding qualifications from the technical baseline review have been verified through direct repository inspection and are resolved below:

| Ref | Topic | Technical Investigation & Evidence | Resolution Applied | Evidence Classification |
| :--- | :--- | :--- | :--- | :--- |
| **A1** | **Browser `localStorage` Role** | Inspected `pages/menu-review.html` lines 437–438 (`localStorage.getItem("icg_review_" + current + "_" + issueHash)`) and line 524. Code reveals `localStorage` is used as a **client-side fallback cache** when the server `/api/issues` endpoint is unreachable (e.g. static hosting). | Clarified distinction: `localStorage` is persistent *within a specific browser profile*, but is isolated per-device, volatile if cache is cleared, and completely decoupled from server SQLite (`menu_review_state.sqlite3`) and on-disk Markdown files. | `[Code-verified]` |
| **A2** | **OCR & Document Ingestion** | Inspected `menu_review_server.py`, `build_venue_export.py`, and repository binaries. Code reveals zero OCR libraries (e.g. Tesseract, AWS Textract, pdf2image). | Clarified that PDF-to-Markdown extraction was performed **upstream and externally** prior to repository ingestion. The repository contains zero automated OCR pipelines; `menu-review.html` simply audits structural defects in pre-extracted Markdown alongside original PDFs via `pdf.js`. | `[Code-verified]` |
| **A3** | **Menu-to-Kafoodie Matching Terminology** | Inspected `build_venue_export.py` lines 423–530. The matching cascade consists of: (1) Exact alias lookup in `config/aliases.json` (score 1.0); (2) Exact normalized string match (score 1.0); (3) Token overlap similarity (`len(tokens_dish & tokens_recipe) / len(tokens_dish) >= 0.55`). | Replaced ambiguous terms with precise technical definition: *heuristic string reconciliation in Python memory*. Clarified that this is an offline token-matching algorithm, **not** a persistent relational foreign key or database entity relationship. | `[Code-verified]` |
| **A4** | **Generated Data Bundle Size** | Executed file measurements on `pages/menu-explorer-data.js`: (1) Raw size: `9,038,918 bytes`; (2) Decimal SI: `9.04 MB` (printed by `build_menu_explorer.py` as `9.0 MB`); (3) Binary IEC: `8.62 MiB` (printed by macOS `ls -lh` as `8.6M`); (4) Gzip compressed: `1,147,492 bytes` (~1.1 MB). | Resolved discrepancy: Earlier draft mentions of ~3 MB referred to legacy crawl subsets with fewer outlets. The full 29-outlet compiled bundle is exactly 9.0 MB uncompressed and 1.1 MB gzipped. | `[Data-verified]` |
| **A5** | **Netlify Removal Boundary** | Inspected git history and removal commits. Verified deletion of `netlify.toml`, `netlify/functions/`, `.netlify/` CLI cache, and cleanup of `.gitignore` and `requirements.txt`. | Confirmed exact boundary: Netlify cleanup was strictly **confined to local repository files**. Zero modifications were made to external cloud Netlify accounts, external DNS, or hosted cloud resources. | `[Code-verified]` |
| **A6** | **Repository Portability** | Audited file links across `docs/capability-assessment/`. Found machine-specific absolute path strings (`/Users/leandrodisconzi/...`) in historical narrative. | Replaced machine-specific references in documentation with standard repository-relative links (e.g. `./07_ARCHITECTURE_VERIFICATION_AND_NETLIFY_REMOVAL.md`), ensuring documentation is fully portable across developer environments. | `[Documented]` |

---

## 3. Operational Domains of the F&B Coordinator

Based on the F&B Coordinator job mandate, the F&B Role Cross-check (`pages/fnb-crosscheck.html`), and operational analysis across the 29 estate properties, the operational domain is structured into nine functional areas:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     F&B COORDINATOR OPERATIONAL ECOSYSTEM                        │
├────────────────────────┬────────────────────────┬────────────────────────────────┤
│ 1. MENU ADMINISTRATION │ 2. PRODUCT & RECIPES   │ 3. FOOD SAFETY & ALLERGENS     │
│ • Printed Menu Specs   │ • Commercial SKUs      │ • 14 Statutory Allergens       │
│ • Section Layouts      │ • Prep SOPs & Yields   │ • Dietary Flags (V, Ve, GF)    │
│ • Regional Variants    │ • Sub-recipes          │ • Data Provenance Audit        │
├────────────────────────┼────────────────────────┼────────────────────────────────┤
│ 4. COMMERCIAL MGMT     │ 5. SUPPLIERS & PURCHASING│ 6. SYSTEMS & EPOS              │
│ • Selling Prices & VAT │ • Vendor Master Data   │ • PLU Code Mapping             │
│ • Cost of Goods (COGS) │ • Pack Sizes & Units   │ • Till Category Structuring    │
│ • Target GP% Margins   │ • Price Shift Tracking │ • Modifier Configuration       │
├────────────────────────┼────────────────────────┼────────────────────────────────┤
│ 7. SEASONAL LAUNCHES   │ 8. MULTI-SITE OPS      │ 9. REPORTING & PERFORMANCE     │
│ • Milestone Checklists │ • 29–31 Inn Properties │ • Menu Engineering (Stars/Dogs)│
│ • Spec Books / Packs   │ • 7 Operating Regions  │ • Cross-Site Variance Audits   │
│ • Cross-Dept Deadlines │ • Regional Menus       │ • Launch Progress Tracking     │
└────────────────────────┴────────────────────────┴────────────────────────────────┘
```

### 3.1 Domain 1: Menu Administration
* **Operational Scope**: Maintaining guest-facing food and drinks menus across all estate venues.
* **Key Activities**: Creating new menu definitions, structuring sections (Starters, Mains, Desserts, Sunday Lunch, Drinks), maintaining guest descriptions, ensuring dietary markers (V, Ve, GF, GFi) match culinary specifications, managing printed pricing, tracking menu lifecycle (Draft, Review, Approved, Published, Archived), and ensuring print/digital parity.
* **Current Prototype State**: `[Code-verified]`. Reads 103 parsed Markdown files. `menu-review.html` provides synchronized PDF/Markdown auditing and atomic duplicate line fixes. However, there is no UI to create, edit dish descriptions, or change prices directly.

### 3.2 Domain 2: Product and Recipe Administration
* **Operational Scope**: Managing the bridge between culinary kitchen preparations and commercial sales items.
* **Key Activities**: Distinguishing commercial sellable Products (e.g. "Whitby Scampi") from back-of-house Recipes (e.g. "Tartare Sauce Prep", "Beer Batter Base"), capturing ingredient bills-of-materials (BOM), portion sizes, batch yields, prep instructions, cooking SOPs, and handling ingredient substitutions.
* **Current Prototype State**: `[Code-verified]`. Kafoodie outlet JSON crawls contain flat dish records with basic nutritional data. Rich culinary specs exist only as a hardcoded static demo in `pages/recipes/chicken-liver-parfait...html`. Central master product records with SKUs do not exist in code.

### 3.3 Domain 3: Food Safety & Allergen Information
* **Operational Scope**: Ensuring statutory allergen declarations and nutritional information are 100% accurate, verifiable, and legally compliant under UK Food Information Regulations (FIR).
* **Key Activities**: Tracking the 14 major allergens (Gluten, Crustaceans, Eggs, Fish, Peanuts, Soya, Milk, Nuts, Celery, Mustard, Sesame, Sulphites, Lupin, Molluscs) across both "Contains" and "May Contain" declarations; auditing incomplete recipe entries (`is_pw_allergen_not_set`); capturing supplier technical specification sign-offs; and maintaining versioned audit trails of allergen alterations.
* **Current Prototype State**: `[Data-verified]`. `menu-explorer-data.js` indexes statutory allergen sequences from Kafoodie crawls. `pages/menu-explorer.html` allows multi-allergen filtering. However, provenance tracking, supplier spec attachments, and change approval workflows are absent.

### 3.4 Domain 4: Commercial Management
* **Operational Scope**: Food costing, gross profit margin analysis, and pricing governance.
* **Key Activities**: Calculating Cost of Goods Sold (COGS) from recipe ingredient costs, modeling gross profit percentages against retail selling prices (accounting for 20% VAT: $\text{GP\%} = \frac{\text{Net Price} - \text{Cost}}{\text{Net Price}}$), identifying margin erosion from supplier cost increases, and modeling price changes across estate tiers.
* **Current Prototype State**: `[Code-verified]`. Printed retail prices exist in Markdown menus and `venue.json`. However, ingredient purchase costs, cost-per-portion, VAT separation, and target margin calculations do not exist in the codebase.

### 3.5 Domain 5: Supplier and Purchasing Management
* **Operational Scope**: Managing supplier catalogs, pack sizes, purchase pricing, and procurement alignment.
* **Key Activities**: Mapping raw ingredients to approved supplier codes, recording case sizes, pack yields, supplier contact details, tracking wholesale price updates, identifying alternative suppliers during shortages, and auditing procurement compliance.
* **Current Prototype State**: `[Code-verified]`. Zero supplier entities exist in the active data pipelines. A single mock supplier table is hardcoded in the Chicken Liver Parfait HTML demo.

### 3.6 Domain 6: Systems & EPOS Coordination
* **Operational Scope**: Bridging commercial F&B data with point-of-sale till configuration.
* **Key Activities**: Assigning Price Look-Up (PLU) codes, structuring EPOS screen button layouts, configuring menu item modifiers (e.g. "Steak Cooking Temperature", "Side Swaps"), establishing venue-specific till availability, validating pricing prior to launch day, and generating importable configuration payloads for till systems.
* **Current Prototype State**: `[Code-verified]`. Zero EPOS integration exists. No PLU codes, modifier tables, or export interfaces exist in the repository.

### 3.7 Domain 7: Seasonal Launches and Operational Readiness
* **Operational Scope**: Coordinating cross-functional milestones leading up to seasonal menu changes (e.g. Spring/Summer, Autumn/Winter, Festive).
* **Key Activities**: Managing launch project timelines across F&B, Marketing, Procurement, Operations, and Finance; generating kitchen "Spec Books" (recipe cards, plating guides, allergen matrices); ensuring site teams receive training materials and menus on schedule; and tracking venue-by-venue launch readiness.
* **Current Prototype State**: `[Observed]`. `pages/launch-readiness.html` provides an interactive UI prototype featuring milestone checkboxes, readiness sliders, and a launch pack builder. However, all data is in-memory client-side JavaScript without backend persistence.

### 3.8 Domain 8: Multi-Site Coordination
* **Operational Scope**: Managing menu, recipe, and pricing consistency across 29 operating venues organized into 7 geographical regions.
* **Key Activities**: Accommodating regional menu variations (e.g. North Wales vs Lake District vs Northumberland specialties); tracking localized pricing tiers; ensuring brand standards across all properties; and coordinating phased regional rollouts.
* **Current Prototype State**: `[Code-verified]`. `build_venue_export.py` maps 29 venues across 7 regions and generates individual `venue.json` models. `menu-explorer.html` allows cross-venue filtering. However, centralized tools to push regional updates or manage estate-wide exceptions are missing.

### 3.9 Domain 9: Reporting and Performance Analysis
* **Operational Scope**: Evaluating menu performance, recipe variances, and operational data quality.
* **Key Activities**: Conducting menu engineering analysis (categorizing dishes into Stars, Plowhorses, Puzzles, and Dogs based on popularity and margin); comparing recipe and allergen variances across venues; auditing data completeness; and logging operational exceptions.
* **Current Prototype State**: `[Code-verified]`. `pages/menu-explorer.html` includes a "Compare Venues" tab that identifies cross-site variance across static recipe snapshots. Sales mix volume and profitability reporting do not exist.

---

## 4. Deliverable B: Operational Requirements and Capability Matrix

The following matrix formally catalogs 40 operational requirements derived from the F&B Coordinator mandate, evaluating them against the current repository state and establishing target implementation priorities:

| Req ID | Domain | Operational Responsibility | Primary Role | Required Information | Required Functionality | Current Implementation | Evidence Status | Current Maturity | Functional Gap | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **REQ-01** | Menu Admin | Maintain master menu definitions | F&B Coordinator | Menu metadata, validFrom, validTo, menu kind, brand | Create, version, and archive menu shells across seasons | None (reads raw `.md` files) | `[Code-verified]` | **Absent** | No menu authoring UI or persistent menu master | **P1** |
| **REQ-02** | Menu Admin | Structure menu sections & hierarchy | F&B Coordinator | Section names, sort order, display rules | Reorder sections, define headers, multi-column layouts | Extracted in `build_venue_export.py:337` | `[Code-verified]` | **Partial** | Offline parsing only; no interactive editing | **P1** |
| **REQ-03** | Menu Admin | Author guest-facing dish descriptions | F&B Coordinator | Dish title, marketing copy, dietary tags | Rich text editing, dietary badge assignment | `menus_md/*.md` | `[Code-verified]` | **Partial** | Plain text markdown only; manual file editing | **P1** |
| **REQ-04** | Menu Admin | Maintain retail selling prices | F&B Coordinator, Commercial Mgr | Currency, VAT rate, price points | Input retail prices, validate format, detect price anomalies | Parsed from markdown | `[Code-verified]` | **Partial** | No price validation or bulk update capability | **P1** |
| **REQ-05** | Menu Admin | Menu approval & publishing workflow | Head of F&B, Operations Dir | Approval status, reviewer, timestamp | Formal RAG approval gate before menu is marked live | None | `[Code-verified]` | **Absent** | Zero governance or publication states | **P2** |
| **REQ-06** | Product Admin | Central commercial Product Master (SKU) | F&B Coordinator | Master SKU, brand, category, commercial name | Central catalog of all sellable food and drink items | `pages/product-data.html` | `[Observed]` | **Mockup** | UI is hardcoded table; no database backing | **P1** |
| **REQ-07** | Recipe Admin | Maintain culinary recipe specifications | Development Chef, F&B Coord | Ingredients, quantities, prep steps, yield, prep time | Structured recipe builder with sub-recipe nesting | Kafoodie crawl / Parfait demo | `[Code-verified]` | **Partial** | Crawled recipes lack BOM; Parfait is hardcoded | **P1** |
| **REQ-08** | Recipe Admin | Link printed Menu Items to Recipes | F&B Coordinator | Menu Item ID, Recipe ID, Match score | Map physical printed dishes to central kitchen recipes | `build_venue_export.py` | `[Code-verified]` | **Partial** | Heuristic offline script; lacks interactive UI | **P1** |
| **REQ-09** | Food Info | 14 statutory allergen declarations | Food Safety Compliance Officer | Allergen bitmasks, contains, may-contain | Rigorous allergen recording per recipe and dish | `menu-explorer-data.js` | `[Data-verified]` | **Partial** | Read-only static crawl; no data entry or audit | **P1** |
| **REQ-10** | Food Info | Nutritional profile management | Food Safety Compliance Officer | Energy (kcal/kJ), fat, sat fat, carbs, sugar, protein, salt | Nutritional calculation per 100g and per portion | Kafoodie JSON crawls | `[Code-verified]` | **Partial** | Static crawl values; no dynamic calculation | **P2** |
| **REQ-11** | Food Info | Audit un-set allergen flags | Food Safety Compliance Officer | `is_pw_allergen_not_set` boolean flag | Highlight incomplete recipes; prevent uncertified publication | Flagged in `venue.json` | `[Code-verified]` | **Partial** | Field exists in JSON; no workflow enforcement | **P1** |
| **REQ-12** | Food Info | Supplier spec sheet provenance tracking | F&B Coordinator | Supplier spec PDF, sign-off date, verifiedBy | Store and link source documentation to ingredient items | None | `[Code-verified]` | **Absent** | No document attachment or verification log | **P2** |
| **REQ-13** | Commercial | Recipe Cost of Goods Sold (COGS) | Commercial Manager | Ingredient purchase costs, portion quantities | Automatically sum ingredient costs to yield dish COGS | Hardcoded in Parfait demo | `[Observed]` | **Mockup** | No cost engine in backend | **P2** |
| **REQ-14** | Commercial | Gross Profit % & margin modeling | Commercial Manager, F&B Coord | Net price, dish COGS, target GP% | Calculate margin: $(P_{net} - C) / P_{net}$; flag low-margin items | None | `[Code-verified]` | **Absent** | No commercial calculation engine | **P2** |
| **REQ-15** | Commercial | Estate pricing tier management | Commercial Manager | Price tier ID, venue assignment | Define base prices and venue/regional price differentials | Implicit in venue exports | `[Inferred]` | **Absent** | Stored as separate strings; no tier hierarchy | **P2** |
| **REQ-16** | Commercial | Supplier cost inflation impact modeling | Commercial Manager | Old cost, new cost, affected recipes | Recalculate margins across estate when raw ingredient rises | None | `[Code-verified]` | **Absent** | Zero impact analysis tooling | **P3** |
| **REQ-17** | Suppliers | Supplier master registry | Procurement Manager | Supplier name, account #, contacts, terms | Directory of approved estate food/drink purveyors | Parfait demo table | `[Observed]` | **Mockup** | Single mock table; no database entity | **P2** |
| **REQ-18** | Suppliers | Supplier product catalog & pack sizes | Procurement Manager | Supplier SKU, pack size, order unit, split charge | Maintain purchasing units and conversion to kitchen units | None | `[Code-verified]` | **Absent** | No pack-size conversion logic | **P2** |
| **REQ-19** | Systems/EPOS | EPOS PLU code assignment | Systems Administrator | PLU number, button label, tax code | Map commercial products to EPOS terminal keys | None | `[Code-verified]` | **Absent** | No PLU fields in any schema | **P2** |
| **REQ-20** | Systems/EPOS | EPOS modifier group configuration | Systems Administrator | Modifier group, options, price delta | Define cooking temps, side swaps, sauce choices | None | `[Code-verified]` | **Absent** | No modifier architecture | **P3** |
| **REQ-21** | Systems/EPOS | Pre-release till configuration QA | Systems Administrator, F&B Coord | Expected vs configured price, tax, printer routing | Validate till database against approved menu specs | None | `[Code-verified]` | **Absent** | Zero validation tooling | **P2** |
| **REQ-22** | Systems/EPOS | EPOS configuration export payload | Systems Administrator | Target system schema (CSV/JSON) | Generate importable dataset for till system programming | None | `[Code-verified]` | **Absent** | No export generation | **P3** |
| **REQ-23** | Launches | Seasonal launch campaign master | F&B Coordinator | Launch name, target date, brand, season | Central entity tracking seasonal rollout milestones | `pages/launch-readiness.html` | `[Observed]` | **Mockup** | Client-side UI simulation; no DB persistence | **P2** |
| **REQ-24** | Launches | Cross-functional milestone checklist | F&B Coordinator | Workstream, task, owner, deadline, RAG status | Track F&B, Ops, Marketing, Finance launch dependencies | `pages/launch-readiness.html` | `[Observed]` | **Mockup** | Checkboxes do not save to server | **P2** |
| **REQ-25** | Launches | Kitchen Spec Book generation | F&B Coordinator, Exec Chef | Recipe cards, photos, allergens, plating SOPs | Compile printable/downloadable kitchen specification pack | `pages/launch-readiness.html` | `[Observed]` | **Mockup** | UI button exists; does not generate real PDF | **P2** |
| **REQ-26** | Launches | Venue readiness tracking | Operations Director | Venue ID, pack received, staff trained, till ready | Monitor sign-off across all 29 properties | `pages/launch-readiness.html` | `[Observed]` | **Mockup** | Sliders are visual demonstrations | **P2** |
| **REQ-27** | Multi-Site | Venue master directory & profiles | Operations Director | Slug, outlet ID, region, address, serving hours | Maintain estate directory of 29 operating inns | `config/venues.json` | `[Code-verified]` | **Partial** | Static JSON file; no administrative UI | **P1** |
| **REQ-28** | Multi-Site | Regional menu inheritance & overrides | F&B Coordinator | Core menu ID, local overrides | Define core estate menu with local dish additions/swaps | Handled via separate files | `[Code-verified]` | **Partial** | File duplication; no inheritance engine | **P2** |
| **REQ-29** | Multi-Site | Cross-venue variance analysis | Group Executive Chef | Dish title, signature across sites | Isolate differences in allergens/ingredients across sites | `menu-explorer.html:Compare` | `[Runtime-tested]` | **Implemented** | Working tool; operates over static crawl | **P2** |
| **REQ-30** | Multi-Site | Missing outlet resolution | F&B Coordinator | Venue name, missing Kafoodie ID | Integrate excluded venues (Dean Court, Bull's Head) | `NO_KAFFODIE` in script | `[Code-verified]` | **Partial** | Excluded in script; needs operational data | **P2** |
| **REQ-31** | Reporting | Menu engineering matrix (Stars/Dogs) | Commercial Manager | Sales volume, unit margin, category rank | Categorize dishes into Stars, Plowhorses, Puzzles, Dogs | Mentioned in notes | `[Documented]` | **Absent** | Requires sales mix and cost data | **P3** |
| **REQ-32** | Reporting | Data completeness & gap register | F&B Coordinator | Unmatched dishes, missing photos, un-set allergens | Automated audit report of data readiness per venue | `venue.json:coverage` | `[Code-verified]` | **Partial** | Generated in JSON; no UI dashboard | **P1** |
| **REQ-33** | Reporting | Operational change audit log | Compliance Officer | User, timestamp, entity changed, old val, new val | Immutable history of all menu, price, and allergen edits | `issue_reviews.updated_at` | `[Database-verified]` | **Partial** | Tracks review triage only; no general audit log | **P2** |
| **REQ-34** | Media | Media asset discovery & cataloging | Marketing Manager | Asset URL, venue, category, MIME type | Discover and categorize photography and PDF menus | `discovered_media.csv` | `[Code-verified]` | **Implemented** | Working tool; static crawl snapshot | **P2** |
| **REQ-35** | Media | Batch media asset export | Marketing Manager | Selected assets, destination folder | Download media assets locally with folder structuring | `POST /api/export` | `[Runtime-tested]` | **Implemented** | Working tool in `menu_review_server.py` | **P2** |
| **REQ-36** | Quality QA | Menu extraction defect triage | F&B Coordinator | Issue type, line numbers, status, notes | Review OCR/markdown conversion errors side-by-side | `menu-review.html` | `[Runtime-tested]` | **Implemented** | Fully working tool with SQLite persistence | **P1** |
| **REQ-37** | Quality QA | Atomic duplicate line removal | F&B Coordinator | Menu name, source hash, target lines | Clean repeated markdown lines with safety locks | `POST /api/issues/fix-duplicates` | `[Runtime-tested]` | **Implemented** | Fully working atomic file rewrite tool | **P1** |
| **REQ-38** | Governance | Role-based access control (RBAC) | Systems Administrator | User, role (Chef, Coordinator, Commercial) | Restrict editing of prices, recipes, and approvals | None | `[Code-verified]` | **Absent** | Local server has zero authentication | **P2** |
| **REQ-39** | Governance | Single master menu file directory | Technical Lead | Master directory path | Eliminate orphaned duplicate `pages/menus_md/` | `menus_md/` duplicated | `[Code-verified]` | **Partial** | 103 identical files in 2 folders; awaiting cleanup | **P1** |
| **REQ-40** | Governance | Closed-loop review-to-export rebuild | Technical Lead | Trigger webhook, build script | Automatically rebuild `venue.json` after menu edit | None | `[Code-verified]` | **Absent** | Requires manual terminal execution today | **P2** |

---

## 5. Requirements Synthesis & Priority Breakdown

Across the 40 audited operational requirements, the system status is categorized as follows:
* **Fully Implemented Today**: 4 requirements (10%) — Menu extraction triage, atomic duplicate fixing, media cataloging, and media batch export.
* **Partially Implemented**: 13 requirements (32.5%) — Menu explorer comparisons, allergen indexing, static recipe crawls, coverage statistics, and venue export generation.
* **Prototype / Mockup Only**: 8 requirements (20%) — Product data master, launch checklists, spec book builder, supplier mockups, and costing tables.
* **Completely Absent**: 15 requirements (37.5%) — Central database master, recipe builder, EPOS mapping, menu publishing governance, RBAC, and automated closed-loop pipelines.

### Priority Horizons for Implementation:
* **Priority 1 (P1 — Core Master Data & Reconciliation)**: 14 requirements establishing the essential data loop: Product Master, Recipe-to-Menu Item association, Allergen provenance tracking, Menu authoring, and Master Directory consolidation.
* **Priority 2 (P2 — Operational Workflows & Governance)**: 21 requirements establishing business execution: Seasonal launch tracking, Spec Book publishing, Cost/Margin modeling, Supplier master data, EPOS configuration QA, and RBAC governance.
* **Priority 3 (P3 — Advanced Commercial Intelligence & Integrations)**: 5 requirements: Menu engineering matrices (Stars/Dogs), supplier inflation modeling, and direct EPOS API connectors.
