# 04 — Operational Workflow Mapping

## 1. Overview of Hospitality Workflows

This document maps the movement of information, assets, and operational responsibilities across the six primary workflows required to run Food & Beverage operations at The Inn Collection Group.

Each workflow distinguishes between:
* **Solid boxes / arrows**: Currently implemented and code-verified pipelines.
* **Dashed boxes / arrows**: Missing, disconnected, or proposed stages required for full operational maturity.

---

## 2. Workflow Maps

### Workflow A: Menu Document Intake & Quality Control

```mermaid
flowchart TD
    subgraph Intake["1. Document Ingestion"]
        A1["Website Media Scrape"] --> A2["discovered_media.csv"]
        A2 --> A3["Discovered Media UI<br/>(Filter & Select)"]
        A3 -->|POST /api/export| A4["Local Directory Export /<br/>Netlify ZIP Archive"]
        A5["Physical PDF Menus<br/>(Creative Agency)"] --> A6["extracted-to-md/*.pdf"]
    end

    subgraph Extraction["2. Markdown Conversion"]
        A6 -->|External Extraction Tool| B1["Raw Markdown Files<br/>(menus_md/*.md)"]
    end

    subgraph Review["3. Quality Control (Menu Review UI)"]
        B1 --> C1["Menu Review UI<br/>(menu-review.html)"]
        A6 --> C1
        C1 -->|GET /api/issues| C2["Automated Rule Scanner<br/>(Headings, Repeats, Chars)"]
        C2 --> C3["Reviewer Audit & Triage"]
        C3 -->|POST /api/issues| C4["SQLite Database<br/>(issue_reviews)"]
        C3 -->|POST /api/issues/fix-duplicates| C5["Automatic Duplicate Line Fixer"]
        C5 -->|Rewrites File| B1
    end

    subgraph Downstream["4. Downstream Availability"]
        B1 -.->|Proposed Automated Trigger| D1["build_venue_export.py"]
        D1 -.-> D2["exports/<Venue>/venue.json"]
    end

    classDef implemented fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef missing fill:#424242,stroke:#212121,stroke-dasharray: 5 5,color:#fff;
    class A1,A2,A3,A4,A5,A6,B1,C1,C2,C3,C4,C5 implemented;
    class D1,D2 missing;
```

* **Starting Event**: Marketing uploads a new seasonal menu PDF or updates an existing card.
* **Inputs**: PDF menu files, crawl CSVs.
* **Processing**: PDF inspection, optical/text markdown conversion, issue scanning (`headings`, `repeated_lines`), human review of intentional anomalies.
* **Outputs**: Validated Markdown adhering to `docs/MENU-MD-SPEC.md`.
* **Identified Gaps**: Markdown extraction is performed externally without automated pipeline integration; completion in `menu-review.html` does not automatically trigger rebuilds of `venue.json`.

---

### Workflow B: Product Administration & Recipe Reconciliation

```mermaid
flowchart TD
    subgraph Culinary["1. Central Recipe Authoring"]
        P1["Kafoodie Portal<br/>(Central Food Team)"] --> P2["Recipe Authoring & Spec"]
        P2 --> P3["Kafoodie API Export<br/>(*_all_menus.json)"]
    end

    subgraph Parsing["2. Automated Ingestion & Cleaning"]
        P3 --> Q1["build_menu_explorer.py"]
        Q1 --> Q2["menu-explorer-data.js"]
        Q2 --> Q3["Menu Explorer UI"]
    end

    subgraph Matching["3. Menu Line Reconciliation"]
        P3 --> R1["build_venue_export.py"]
        R2["menus_md/*.md"] --> R1
        R3["config/aliases.json<br/>(Rename Rules)"] --> R1
        R1 -->|1. Alias Match| R4["Matched Product Record"]
        R1 -->|2. Exact Name Match| R4
        R1 -->|3. Token Overlap Scoring| R4
        R1 --> R5["matchReport & Gaps List"]
    end

    subgraph Master["4. Product Administration"]
        R4 -.-> S1["Product Data UI<br/>(product-data.html)"]
        S2["Chicken Liver Parfait<br/>Product Specification Pattern"] -.-> S1
        S1 -.->|Write Back Changes| P1
    end

    classDef implemented fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef missing fill:#424242,stroke:#212121,stroke-dasharray: 5 5,color:#fff;
    class P1,P2,P3,Q1,Q2,Q3,R1,R2,R3,R4,R5 implemented;
    class S1,S2 missing;
```

* **Starting Event**: Development Chef updates recipe ingredients, grammages, or allergens in Kafoodie.
* **Inputs**: Kafoodie JSON payloads, Markdown menus, `config/aliases.json`.
* **Processing**: Exact name matching, alias resolution, token similarity scoring, ambiguity checking (runner-up score difference < 0.05).
* **Outputs**: Comprehensive `venue.json` containing linked dish-to-product data.
* **Identified Gaps**: The reconciliation is one-way (read-only from Kafoodie); no administrative interface exists to edit or approve aliases directly in the browser.

---

### Workflow C: Cross-Site Menu Management & Venue Variance

```mermaid
flowchart TD
    M1["Central Menu Blueprint<br/>(e.g. Crown Autumn/Winter)"] --> M2["31 Venue Outlets"]
    M2 --> M3["Local Printed Menus (PDF)"]
    M2 --> M4["Local Kafoodie Outlet Feeds"]
    M3 & M4 --> M5["build_venue_export.py"]
    M5 --> M6["exports/<Venue>/venue.json"]
    M6 --> M7["Menu Explorer<br/>(Compare Venues Tab)"]
    M7 --> M8["Allergen & Calorie Variance Table"]
    M8 -.->|Flag Anomaly| M9["Corrective Action Alert"]
    M9 -.->|Update Central Recipe / Print| M1

    classDef implemented fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef missing fill:#424242,stroke:#212121,stroke-dasharray: 5 5,color:#fff;
    class M1,M2,M3,M4,M5,M6,M7,M8 implemented;
    class M9 missing;
```

* **Operational Reality**: The same dish (e.g. "Venison Lasagne") served across 20 inns may have varying allergen declarations if one kitchen sources a different cheese or regional supplier.
* **Implemented Capability**: `pages/menu-explorer.html:cmp()` dynamically compares all venues across the entire estate and highlights differences with a single toggle (`Differences only`).
* **Missing Capability**: No automated workflow to notify executive chefs when variance indicates an unapproved local substitution.

---

### Workflow D: Seasonal Launch Readiness Coordination

```mermaid
flowchart TD
    L1["Seasonal Menu Launch Directive<br/>(e.g., Festive 2026)"] --> L2["Launch Readiness Dashboard<br/>(launch-readiness.html)"]
    
    subgraph ExistingWorkstreams["Workstreams Tracked (Client-Side)"]
        W1["Culinary & Recipe Signoff"]
        W2["Allergen & Safety Compliance"]
        W3["EPOS PLU Programming"]
        W4["Kitchen & FOH Training"]
        W5["Print & Media Delivery"]
    end
    
    L2 --> ExistingWorkstreams
    
    subgraph ProposedDataIntegration["Proposed Data-Driven Automation"]
        D1["venue.json: matchReport"] -.->|Auto-populate| W1
        D2["is_pw_allergen_not_set Count"] -.->|Safety Blocker Flag| W2
        D3["menu_review_state: fixed count"] -.->|Print Audit Check| W5
    end

    classDef implemented fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef missing fill:#424242,stroke:#212121,stroke-dasharray: 5 5,color:#fff;
    class L1,L2,W1,W2,W3,W4,W5 implemented;
    class D1,D2,D3 missing;
```

* **Current Implementation**: A comprehensive prototype in `pages/launch-readiness.html` modeling the operational checklist across 31 properties.
* **Proposed Architecture**: Connecting readiness calculations directly to real data metrics:
  1. A venue's "Recipe Signoff" completes automatically when `dishesMatchedToProduct == dishes` in `venue.json`.
  2. A venue's "Allergen Audit" is blocked if any recipe has `allergenDataMissing == true`.
  3. "Print Collateral" completes when all menu issues in `menu_review_state.sqlite3` are marked `fixed` or `intentional`.
