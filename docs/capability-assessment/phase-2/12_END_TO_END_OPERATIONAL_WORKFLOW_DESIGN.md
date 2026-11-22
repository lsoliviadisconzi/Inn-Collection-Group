# Document 12 — End-to-End Operational Workflow Design

> **Knowledge Base** · Inn Collection Group (ICG) Hospitality Technology Workspace  
> **Document** 12 of 15 · Published: 2026-11-22  
> **Phase**: Phase 2 — Hospitality Technology Requirements, Target Architecture & Implementation Blueprint  
> **Evidence Standards**: `[Proposed]` · `[Code-verified]` · `[Observed]` · `[Requires-confirmation]`

---

## 1. Executive Summary & Design Principles

This document defines the operational workflows that govern how people and software collaborate within the target Inn Collection Group (ICG) hospitality technology architecture.

A core operational principle guides this workflow specification:
> *"Do not design a system that assumes every operational decision can or should be automated. Software should handle calculation, indexing, cross-referencing, and validation, while humans make culinary, commercial, and food safety decisions."*

Seven core operational workflows are modeled, detailing the exact triggers, roles, system actions, human gates, data mutations, exceptions, and audit criteria across the hospitality lifecycle.

---

## 2. The Seven End-to-End Operational Workflows

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   SEVEN CORE HOSPITALITY OPERATIONAL WORKFLOWS                   │
├────────────────────────┬────────────────────────┬────────────────────────────────┤
│ E1. NEW PRODUCT INTRO  │ E2. MENU CHANGE        │ E3. SEASONAL LAUNCH CAMPAIGN   │
│ Supplier -> Recipe ->  │ Proposal -> Recipe ->  │ Milestones -> Spec Books ->    │
│ Allergen -> Price -> Inn│ Price -> Sign-off -> Web│ Till Prep -> Venue Readiness   │
├────────────────────────┼────────────────────────┼────────────────────────────────┤
│ E4. SUPPLIER COST SHIFT│ E5. CROSS-SITE VARIANCE│ E6. FOOD SAFETY & ALLERGENS    │
│ Wholesale Up -> COGS ->│ Compare 29 Inns ->     │ Spec Update -> Recipe Impact ->│
│ Margin Erosion -> Price│ Isolate Kitchen Diverge│ Audit Log -> Menu Re-publish   │
├────────────────────────┴────────────────────────┴────────────────────────────────┤
│ E7. EPOS CONFIGURATION & TILL QA                                                 │
│ Menu Approval -> PLU Assignment -> Modifier Group -> Till Payload -> Price QA     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.1 Workflow E1: New Product Introduction (NPI)

* **Trigger**: Commercial strategy or culinary development proposes a new dish, drink, or retail item to be introduced across estate menus.
* **Participants**: Development Chef, F&B Coordinator, Commercial Manager, Food Safety Compliance Officer.
* **Required Inputs**: Supplier technical specifications, ingredient pricing, kitchen recipe formulation, proposed selling price, target venues.

```mermaid
flowchart TD
    E1_1["1. Procurement Enters Supplier Product & Cost"] --> E1_2["2. Chef Builds Recipe BOM & Prep SOP"]
    E1_2 --> E1_3["3. System Computes Preliminary Allergens & Nutrition"]
    E1_3 --> E1_4{"4. Compliance Officer Signs Off Allergens?"}
    E1_4 -->|No: Incomplete Data| E1_4A["Flagged: Unverified Spec / Held"]
    E1_4 -->|Yes: Verified| E1_5["5. F&B Coordinator Creates Master Product SKU"]
    E1_5 --> E1_6["6. Commercial Manager Models Net Price & Target GP%"]
    E1_6 --> E1_7["7. F&B Coordinator Binds Product to Venue Offerings"]
    E1_7 --> E1_8["8. Systems Assigns EPOS PLU Code & Kitchen Route"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef human fill:#1565c0,stroke:#0d47a1,color:#fff;
    classDef gate fill:#f57f17,stroke:#e65100,color:#fff;
    class E1_3,E1_6 auto;
    class E1_1,E1_2,E1_5,E1_7,E1_8 human;
    class E1_4,E1_4A gate;
```

* **System Actions**:
  1. Converts purchasing pack units (e.g. 6x1kg case) to recipe units (grams).
  2. Aggregates allergen bitmasks across all recipe ingredients into a composite dish allergen profile.
  3. Calculates Cost of Goods Sold (COGS) and gross profit margin ($\text{GP\%}$).
  4. Automatically blocks product publication if `is_pw_allergen_not_set == true`.
* **Human Decisions**:
  1. Chef approves culinary portion sizes, cooking temperatures, and presentation photography.
  2. Compliance Officer formally signs off statutory allergen declarations against supplier documentation.
  3. Commercial Manager approves price point and margin threshold.
* **Data Created / Updated**: `supplier_products`, `ingredients`, `recipes`, `recipe_ingredients`, `commercial_products`, `allergen_declarations`, `prices`, `venue_offerings`.
* **Exceptions**: Missing allergen data from supplier halts workflow at Step 4; low gross profit margin (<68%) triggers commercial review before Step 7.
* **Completion Criteria**: Product record is marked `Active` with signed-off allergens, approved selling price, and mapped PLU code.
* **Audit Requirements**: Immutable entry in `audit_events` with timestamps and user IDs for allergen certification and pricing sign-off.

---

### 2.2 Workflow E2: Menu Change & Price Revision

* **Trigger**: Periodic menu refresh, dish replacement, or planned seasonal menu adjustment.
* **Participants**: F&B Coordinator, Head of F&B, General Managers, Marketing Manager.
* **Required Inputs**: Existing menu hierarchy, proposed dish additions/removals, revised pricing, target publication date.

```mermaid
flowchart TD
    E2_1["1. F&B Coordinator Clones Menu to 'Draft' State"] --> E2_2["2. Reorder Sections & Swap Menu Items"]
    E2_2 --> E2_3["3. Update Guest Descriptions & Dietary Markers"]
    E2_3 --> E2_4["4. System Validates Price Integrity & Allergen Completeness"]
    E2_4 --> E2_5{"5. Head of F&B Formally Approves Menu?"}
    E2_5 -->|Revisions Needed| E2_2
    E2_5 -->|Approved| E2_6["6. System Transitions Menu to 'Published'"]
    E2_6 --> E2_7["7. Automated Pipeline Compiles venue.json & Markdown"]
    E2_7 --> E2_8["8. Spec Books & Print Artwork Generated for Sites"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef human fill:#1565c0,stroke:#0d47a1,color:#fff;
    classDef gate fill:#f57f17,stroke:#e65100,color:#fff;
    class E2_4,E2_6,E2_7,E2_8 auto;
    class E2_1,E2_2,E2_3 human;
    class E2_5 gate;
```

* **System Actions**:
  1. Clones existing menu into a draft version with full audit history.
  2. Validates that every menu item links to an active commercial product with certified allergens.
  3. Compiles canonical `venue.json` and human-readable `venue.md` per venue upon publication.
  4. Generates updated printable allergen matrices for guest display.
* **Human Decisions**:
  1. Coordinator reviews section balance, pricing flow, and layout constraints.
  2. Head of F&B conducts final sign-off before publication.
* **Data Created / Updated**: `menus`, `menu_sections`, `menu_items`, `approvals`, `exports/<Region>/<Venue>/venue.json`.
* **Completion Criteria**: Menu status changes from `Draft` to `Published`; build pipeline executes cleanly; updated files are pushed to venue interfaces.

---

### 2.3 Workflow E3: Seasonal Menu Launch Orchestration

* **Trigger**: Annual culinary calendar milestone (e.g. 8 weeks prior to Festive or Spring menu changeover).
* **Participants**: F&B Coordinator (Lead), Operations Director, Commercial Manager, Procurement, Area Operations Managers, Site General Managers.
* **Required Inputs**: Seasonal launch calendar, approved menu definitions, marketing print schedule, supplier delivery schedules.

```mermaid
flowchart TD
    E3_1["1. Coordinator Creates Launch Campaign in Platform"] --> E3_2["2. Assign Workstream Milestones & Deadlines"]
    E3_2 --> E3_3["3. Procurement Locks Supplier Availability & Order Windows"]
    E3_3 --> E3_4["4. Systems Programs & Audits EPOS Databases"]
    E3_4 --> E3_5["5. Platform Compiles Venue Kitchen Spec Books (PDF)"]
    E3_5 --> E3_6["6. Marketing Dispatches Print Packs to 29 Inns"]
    E3_6 --> E3_7["7. General Managers Conduct Kitchen Training & Sign Off"]
    E3_7 --> E3_8["8. Platform Launch Dashboard Reaches 100% Green -> Go-Live"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef human fill:#1565c0,stroke:#0d47a1,color:#fff;
    class E3_5,E3_8 auto;
    class E3_1,E3_2,E3_3,E3_4,E3_6,E3_7 human;
```

* **System Actions**:
  1. Initializes `launch_campaigns` record and seeds 40+ standard milestone tasks.
  2. Assembles printable kitchen Spec Books (recipe cards, photos, allergens, plating SOPs) via PDF engine.
  3. Computes real-time estate readiness score based on milestone completion across 29 properties.
* **Human Decisions**:
  1. Procurement confirms delivery cut-off dates with suppliers.
  2. Site General Managers verify delivery of print packs and kitchen team training sign-off.
* **Data Created / Updated**: `launch_campaigns`, `launch_tasks`, `launch_venue_statuses`.
* **Completion Criteria**: All 29 inns record 100% readiness sign-off; EPOS terminals verified; launch declared live.

---

### 2.4 Workflow E4: Supplier Cost Change & Recipe Margin Impact

* **Trigger**: Supplier notifies wholesale price increase on a core raw material (e.g. Scottish butter, beef rump, frying oil).
* **Participants**: Procurement Manager, Commercial Manager, F&B Coordinator, Executive Chef.
* **Required Inputs**: Supplier price adjustment notification, affected ingredient codes, effective date.

```mermaid
flowchart TD
    E4_1["1. Procurement Updates Supplier Product Case Cost"] --> E4_2["2. System Recalculates Ingredient Unit Cost (£/g)"]
    E4_2 --> E4_3["3. System Scans All Recipes Using Ingredient (BOM)"]
    E4_3 --> E4_4["4. System Computes New Dish COGS & Margin Degradation"]
    E4_4 --> E4_5["5. Dashboard Highlights Affected Dishes Below Target GP%"]
    E4_5 --> E4_6{"6. Commercial Action Required?"}
    E4_6 -->|Absorb Cost| E4_7["Document Variance & Monitor"]
    E4_6 -->|Re-engineer Recipe| E4_8["Chef Adjusts Portion / Sub-recipe"]
    E4_6 -->|Retail Price Rise| E4_9["Coordinator Schedules Price Update"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef human fill:#1565c0,stroke:#0d47a1,color:#fff;
    classDef gate fill:#f57f17,stroke:#e65100,color:#fff;
    class E4_2,E4_3,E4_4,E4_5 auto;
    class E4_1,E4_7,E4_8,E4_9 human;
    class E4_6 gate;
```

* **System Actions**:
  1. Updates ingredient unit cost.
  2. Evaluates all recipes containing the ingredient and updates total recipe cost and portion COGS.
  3. Computes revised gross profit percentage against current retail prices.
  4. Generates an exception report listing all dishes where GP% falls below commercial targets (e.g. <70%).
* **Human Decisions**:
  1. Commercial Manager determines whether to absorb the cost, re-engineer the recipe, or raise menu price.
  2. Executive Chef evaluates culinary impact of ingredient substitutions.
* **Data Created / Updated**: `supplier_products.case_cost_net`, `ingredients.unit_cost`, `recipes.cogs_per_portion`, `prices.margin_percentage`.

---

### 2.5 Workflow E5: Cross-Site Variance Auditing

* **Trigger**: Routine menu compliance audit or customer inquiry regarding cross-venue recipe differences.
* **Participants**: Group Executive Chef, Food Safety Officer, F&B Coordinator.
* **Required Inputs**: Generated venue data models across 29 properties (`venue.json`), Menu Explorer dataset.

```mermaid
flowchart TD
    E5_1["1. Auditor Opens Menu Explorer 'Compare Venues'"] --> E5_2["2. Filters by 'Differences Only' across 29 Inns"]
    E5_2 --> E5_3["3. Platform Compares Recipe Signatures & Allergens"]
    E5_3 --> E5_4["4. Discrepancy Identified (e.g. Venue A declares Sulphites; Venue B does not)"]
    E5_4 --> E5_5["5. Coordinator Investigates Upstream Ingestion & Kitchen Practice"]
    E5_5 --> E5_6{"6. Root Cause Established?"}
    E5_6 -->|Data-Entry Omission| E5_7["Update Master Recipe & Push Sync"]
    E5_6 -->|Local Kitchen Deviation| E5_8["Area Chef Remediates Kitchen SOP"]
    E5_6 -->|Approved Local Variation| E5_9["Document Approved Exception in Platform"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef human fill:#1565c0,stroke:#0d47a1,color:#fff;
    classDef gate fill:#f57f17,stroke:#e65100,color:#fff;
    class E5_2,E5_3,E5_4 auto;
    class E5_1,E5_5,E5_7,E5_8,E5_9 human;
    class E5_6 gate;
```

* **System Actions**:
  1. Cross-references identical dish names across all 29 outlet datasets.
  2. Compares allergen bitmasks, nutritional values, and ingredient declarations.
  3. Renders a side-by-side discrepancy table isolating differences in under one second.
* **Human Decisions**:
  1. Chef determines whether the difference represents an unauthorized kitchen shortcut, supplier substitution, or clerical data-entry error.
  2. Compliance Officer authorizes the required operational remediation.
* **Outputs**: Variance investigation log and corrective action report.

---

### 2.6 Workflow E6: Food Safety & Allergen Information Update

* **Trigger**: Ingredient manufacturer notifies recipe reformulation, change in "may contain" allergen warnings, or new supplier spec sheet.
* **Participants**: Food Safety Compliance Officer, F&B Coordinator, Head of Food.
* **Required Inputs**: Manufacturer technical specification sheet, affected ingredient ID, effective delivery date.

```mermaid
flowchart TD
    E6_1["1. Compliance Officer Uploads New Manufacturer Spec Sheet"] --> E6_2["2. Updates Allergen Declaration on Ingredient Record"]
    E6_2 --> E6_3["3. Platform Traverses All Active Recipes & Menu Items"]
    E6_3 --> E6_4["4. Platform Generates Immediate Impact List (Dishes & Inns)"]
    E6_4 --> E6_5["5. Automated Alert Dispatched to Kitchens & Digital Menus"]
    E6_5 --> E6_6["6. Regenerate Estate Allergen Matrix PDFs for Guest Display"]
    E6_6 --> E6_7["7. Immutable Audit Record Stored with Timestamp & Spec Hash"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef human fill:#1565c0,stroke:#0d47a1,color:#fff;
    class E6_3,E6_4,E6_5,E6_6,E6_7 auto;
    class E6_1,E6_2 human;
```

* **System Actions**:
  1. Immediately cascades allergen updates to all child recipes and menu offerings.
  2. Invalidates published allergen matrices and triggers automated PDF re-compilation.
  3. Records SHA-256 hash of supplier specification in audit history.
* **Human Decisions**:
  1. Compliance Officer certifies the authenticity and regulatory validity of the change.
* **Data Created / Updated**: `ingredients.allergen_bitmask`, `allergen_declarations`, `source_documents`, `audit_events`.
* **Completion Criteria**: All digital menus reflect the updated allergen status; new physical matrices printed for venue display.

---

### 2.7 Workflow E7: EPOS Configuration Preparation & Till QA

* **Trigger**: Menu publication completed; till system must be programmed 2 weeks prior to menu launch.
* **Participants**: F&B Coordinator, Systems Administrator, Till Programming Vendor.
* **Required Inputs**: Approved menu item hierarchy, retail pricing tiers, kitchen printer routing rules.

```mermaid
flowchart TD
    E7_1["1. Coordinator Triggers 'Generate EPOS Payload' for Target Season"] --> E7_2["2. Platform Formats PLUs, Button Labels, Taxes & Prices"]
    E7_2 --> E7_3["3. Platform Exports Structured Payload (CSV / XML / JSON)"]
    E7_3 --> E7_4["4. Systems Vendor Imports Configuration into Till Master"]
    E7_4 --> E7_5["5. Systems Administrator Conducts Automated Price QA Check"]
    E7_5 --> E7_6{"6. Price Discrepancies Found Between Till & Menu?"}
    E7_6 -->|Discrepancy Detected| E7_7["Block Till Deployment & Generate Exception Report"]
    E7_6 -->|100% Match| E7_8["Authorize Till Master Package for Site Download"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef human fill:#1565c0,stroke:#0d47a1,color:#fff;
    classDef gate fill:#f57f17,stroke:#e65100,color:#fff;
    class E7_2,E7_3,E7_5 auto;
    class E7_1,E7_4,E7_7,E7_8 human;
    class E7_6 gate;
```

* **System Actions**:
  1. Maps `venue_offerings` to target EPOS schema (PLU, category, price, VAT rate 20%, printer group).
  2. Executes pre-release price comparison between EPOS database and approved menu specs.
* **Human Decisions**:
  1. Systems Admin authorizes release of till package following 100% validation pass.
* **Outputs**: EPOS configuration export payload; Till QA Verification Certificate.
