# Document 04 — Operational Workflow Map

> **Hospitality Technology Capability Assessment — The Inn Collection Group**  
> **Phase**: System Architecture & Technical Verification  
> **Standard Key**: `[Observed]` · `[Code-verified]` · `[Database-verified]` · `[Tested]` · `[Inferred]` · `[Proposed]` · `[Unknown]`

---

## 1. Overview & Operational Persona

In a multi-site hospitality estate of 31 coaching inns, the **Food & Beverage (F&B) Systems Coordinator** serves as the operational linchpin connecting central commercial teams, marketing design agencies, development chefs, site general managers, and EPOS engineers.

This document maps the eight core operational workflows of this role, clearly distinguishing between:
* **Automated & Code-Verified Stages** (green/solid): Currently functioning in the codebase.
* **Manual Interventions & Operational Friction** (amber): Human steps required due to missing tooling.
* **Unimplemented / Conceptual Stages** (grey/dashed): Capabilities modeled in UI mockups but absent from the backend.

---

## 2. Operational Hospitality Workflows

### 2.1 Workflow 1: Intake & Quality Control of a New Seasonal Menu PDF

```mermaid
flowchart TD
    W1_1["Creative Agency uploads Menu PDF<br/>(e.g., Autumn/Winter 2026)"] --> W1_2["Manual / External Extraction Tool<br/>(Converts PDF to Markdown)"]
    W1_2 --> W1_3["Save to menus_md/*.md<br/>(Adhering to MENU-MD-SPEC)"]
    W1_3 --> W1_4["Open Menu Review UI<br/>(menu-review.html)"]
    W1_4 --> W1_5["Automated Issue Scanner<br/>(GET /api/issues)"]
    W1_5 --> W1_6{"Reviewer Triage"}
    W1_6 -->|Repeated Lines Detected| W1_7["Click 'Fix Duplicates'<br/>(POST /api/issues/fix-duplicates)"]
    W1_7 --> W1_8["Atomic Markdown Rewrite &<br/>SQLite Status: 'fixed'"]
    W1_6 -->|Typography / OCR Flaw| W1_9["Record Note & Status: 'open' / 'intentional'<br/>(POST /api/issues)"]
    W1_8 & W1_9 --> W1_10["Manual Terminal Execution<br/>(python3 build_venue_export.py)"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef manual fill:#f57f17,stroke:#e65100,color:#fff;
    classDef absent fill:#616161,stroke:#212121,stroke-dasharray: 5 5,color:#fff;
    class W1_4,W1_5,W1_7,W1_8 auto;
    class W1_1,W1_2,W1_3,W1_6,W1_9,W1_10 manual;
```

* **Primary User**: F&B Systems Coordinator / Marketing Coordinator.
* **Inputs**: PDF menu files from graphic design agencies.
* **Outputs**: Validated, cleaned Markdown menu stored in `menus_md/` and tracked in SQLite.
* **Manual Interventions**:
  1. `[Code-verified]`: Converting the PDF into Markdown is an external, manual task before the file enters `menus_md/`.
  2. `[Code-verified]`: After resolving issues in `menu-review.html`, the coordinator must manually switch to a terminal and run `python3 build_venue_export.py` to update downstream JSON files.

---

### 2.2 Workflow 2: Reconciling Printed Dishes to Kafoodie Central Recipes

```mermaid
flowchart TD
    W2_1["Markdown Menu in menus_md/"] & W2_2["Kafoodie API Crawl in kafoodie/"] --> W2_3["Execute build_venue_export.py"]
    
    subgraph MatchingEngine["3-Stage Matching Cascade (build_venue_export.py:637-771)"]
        M1{"1. Alias Lookup in config/aliases.json?"}
        M1 -->|Yes| M_SUCCESS["Match Found: via 'alias' (Score 1.0)"]
        M1 -->|No| M2{"2. Exact Name Match?"}
        M2 -->|Yes| M_SUCCESS2["Match Found: via 'exact' (Score 1.0)"]
        M2 -->|No| M3{"3. Token Overlap Score >= 0.55?"}
        M3 -->|Yes| M_SUCCESS3["Match Found: via 'tokens' (Score >= 0.55)"]
        M3 -->|No| M_FAIL["Unmatched Dish Logged to matchReport"]
    end
    
    W2_3 --> MatchingEngine
    M_FAIL --> W2_4["Manual Inspection of matchReport.unmatchedDishes"]
    W2_4 --> W2_5["Coordinator Manually Edits config/aliases.json"]
    W2_5 --> W2_3

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef manual fill:#f57f17,stroke:#e65100,color:#fff;
    class W2_3,M1,M2,M3,M_SUCCESS,M_SUCCESS2,M_SUCCESS3,M_FAIL auto;
    class W2_4,W2_5 manual;
```

* **Primary User**: F&B Systems Coordinator.
* **Inputs**: Cleaned menu Markdown, Kafoodie outlet JSON files, `config/aliases.json`.
* **Outputs**: `venue.json` with linked `product` IDs and `matchReport` metrics.
* **Manual Interventions**:
  1. `[Code-verified]`: When dishes fail to match (e.g. printed "Classic Whitby Scampi" vs Kafoodie "Scampi & Chips"), the coordinator must open `config/aliases.json` in a text editor, write a JSON entry, and rerun the build script.

---

### 2.3 Workflow 3: Cross-Venue Variance Auditing (Allergen & Calorie Inconsistencies)

```mermaid
flowchart TD
    W3_1["Executive Chef / Compliance Officer"] --> W3_2["Open Menu Explorer (menu-explorer.html)"]
    W3_2 --> W3_3["Click 'Compare Venues' Tab"]
    W3_3 --> W3_4["Click 'Differences only' Button (st.only = true)"]
    W3_4 --> W3_5["System Evaluates Dish Signatures Across All 29 Venues"]
    W3_5 --> W3_6["Table Renders Discrepancies<br/>(e.g., Venue A declares Sulphites; Venue B does not)"]
    W3_6 --> W3_7["Manual Investigation of Kitchen Recipe Divergence"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef manual fill:#f57f17,stroke:#e65100,color:#fff;
    class W3_2,W3_3,W3_4,W3_5,W3_6 auto;
    class W3_1,W3_7 manual;
```

* **Primary User**: Group Executive Chef / Food Safety Compliance Officer (`[Inferred]` operational role).
* **Inputs**: `menu-explorer-data.js` compiled across all outlets (offline static snapshot).
* **Outputs**: Client-side comparison table of a generated data snapshot highlighting differences in available recipe, allergen, and nutritional declarations across properties.
* **Operational Reality**: `[Tested]`. Evaluates dish signatures across the static dataset. Identifying differences does not establish whether those differences are current, approved, intentional, or operationally accurate; it requires human investigation to establish cause and operational significance. It does not provide live monitoring or automatic change detection.

---

### 2.4 Workflow 4: Identifying Missing Information & Compliance Blockers

```mermaid
flowchart TD
    W4_1["Coordinator runs build_venue_export.py --check"] --> W4_2["System Generates venue.json:gaps[]"]
    W4_2 --> W4_3{"Automated Compliance Checks"}
    W4_3 -->|Check 1: Missing Allergens| W4_4["Flag: is_pw_allergen_not_set == true"]
    W4_3 -->|Check 2: Unmatched Dishes| W4_5["Flag: Dishes on printed menu with no recipe"]
    W4_3 -->|Check 3: Missing Outlets| W4_6["Flag: NO_KAFFODIE (Dean Court, Bull's Head)"]
    W4_4 & W4_5 & W4_6 --> W4_7["Gaps Array Written to venue.json"]
    W4_7 --> W4_8["Manual Email to Site Chefs to resolve data"]

    classDef auto fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef manual fill:#f57f17,stroke:#e65100,color:#fff;
    class W4_1,W4_2,W4_3,W4_4,W4_5,W4_6,W4_7 auto;
    class W4_8 manual;
```

* **Primary User**: F&B Coordinator / Head of Food.
* **Inputs**: Venue crawl files, Markdown files.
* **Outputs**: Generated plain-English gap register inside `venue.json:gaps`.
* **Code Evidence**: `build_venue_export.py:1268-1290` automatically evaluates and generates text warnings:
  * *"12 dishes have no matched Kafoodie recipe and cannot show allergens or nutrition."*
  * *"3 recipes have no allergen data set in Kafoodie."*

---

### 2.5 Workflow 5: Seasonal Launch Preparation (Current vs. Intended)

| Operational Stage | Intended Workflow (from `launch-readiness.html`) | Actual Code Reality | Operational Gap |
| :--- | :--- | :--- | :--- |
| **1. Milestone Triage** | Central F&B sets completion dates for Print, EPOS, Recipe Specs, and FOH Briefing. | Hardcoded in client-side JS; no database storage. | `[Code-verified]` Reset on reload; cannot be shared across team. |
| **2. Recipe Signoff** | Head Chefs verify culinary specs and portion grammages. | Detailed specs exist **only** for Chicken Liver Parfait (`pages/recipes/`). | `[Observed]` No digital spec sheets exist for other 200+ dishes. |
| **3. EPOS Setup** | PLU numbers assigned, tills programmed, modifier groups verified. | **Zero implementation**. No EPOS codes exist in any file. | `[Code-verified]` Completely manual process outside the system. |
| **4. Site Readiness** | General Managers check off staff tasting and allergen briefing. | Checklist clicks update DOM progress bars only. | `[Code-verified]` Unpersisted; no multi-site progress tracking. |
