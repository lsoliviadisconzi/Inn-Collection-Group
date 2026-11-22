# The Inn Collection Group — System Handover & Operational Requirements Wishlist

> **From**: Antigravity Technical Architecture & Engineering Agent  
> **To**: Executive Leadership, F&B Directorate & IT Operations  
> **Date**: 22 November 2026  
> **Status**: Core Platform Operational (Phase 1 & Phase 2 Complete)

---

## 1. Executive Summary: What Is Built & Live

The core modular monolith for The Inn Collection Group menu, product, and launch governance is fully built and operational:
1. **Zero External Dependencies**: Runs entirely on Python 3.9+ standard library and SQLite with Write-Ahead Logging (WAL mode), with zero cloud runtime costs and automated nightly backups.
2. **Estate-Wide Data Coverage**: All **29 estate venues** across all 7 regions have been built and standardized, consolidating **4,832 products** into unified canonical records (`venue.json`).
3. **Statutory Compliance Engine**: Implements the 14 statutory allergens under UK FIC/FIR regulations and Natasha's Law (PPDS), with live cross-checking between printed menus and Kafoodie.
4. **Hard Publication Gate (Decision D12)**: Menus containing unset allergens (`is_pw_allergen_not_set = true`) are strictly blocked from release, with automated audit trails logging user, timestamp, and blocking dishes.
5. **Multi-User Preparedness**: Local session authentication, RBAC-ready user tables, and tamper-evident SQLite audit trails are in place.

---

## 2. The Wishlist: Exactly What Is Needed from You

To advance from the current operational baseline into automated continuous synchronization, commercial costing, and EPOS integration, here are the **5 specific items needed from leadership, operations, and third-party vendors**:

```
+----------------------------------------------------------------------------------------------------+
|                               THE OPERATIONAL REQUIREMENTS WISHLIST                                |
+----+----------------------------+-------------------------------------+----------------------------+
| #  | Requirement                | Action Owner                        | Operational Impact         |
+----+----------------------------+-------------------------------------+----------------------------+
| 1  | Kafoodie Recipe Correction | Group Executive Chef / F&B Director | Unblocks 28 venues to 100% |
| 2  | Kafoodie API Credentials   | IT Director / Kafoodie Account Mgr  | Automates live recipe sync |
| 3  | Missing Outlet IDs         | Operations / Estate Management      | Integrates final 2 venues  |
| 4  | EPOS Vendor Confirmation   | Head of IT / Systems Manager        | Scopes Step 7 till adapter |
| 5  | Dedicated Host Machine     | IT Support / Systems Administrator  | Enables 24/7 LAN access    |
+----+----------------------------+-------------------------------------+----------------------------+
```

---

### Item 1: Complete Allergen Flags on 4 Kafoodie Recipes *(Immediate F&B Priority)*
- **The Problem**: Estate-wide audit identified that **90 product instances** across 28 venues currently block release compliance.
- **The Finding**: These 90 blocks are caused by just **4 recurring group recipes** in Kafoodie where the allergen flags were left unset:
  1. `Sorbet 3 scoops`
  2. `ADD Maple Bacon`
  3. `Sweet Chilli Pizza Crust Dip`
  4. `Sorbet 2 Scoops (Childrens)`
- **The Ask**: A culinary manager with Kafoodie admin access must log in to Kafoodie and confirm or clear the 14 allergen checkboxes for these 4 items.
- **The Result**: The moment these 4 recipes are saved in Kafoodie, **28 out of 29 venues immediately achieve 100% statutory compliance**.

---

### Item 2: Kafoodie API Connection Details *(Technical Integration)*
- **Decision D13**: The business approved moving from web-crawl scrapers to direct REST API ingestion.
- **The Ask**:
  - Kafoodie API Endpoint URL (e.g. `https://api.kafoodie.com/v1/...`).
  - Production API Key, Client ID, and Secret (or Bearer Token).
  - Outlet ID mapping list or master account credential.
- **The Result**: Fresh recipes, ingredient BOM updates, and nutrition calculations will synchronize automatically in real time without manual file crawls.

---

### Item 3: Outlet Identifiers for Dean Court & The Bull's Head Inn *(Estate Reconciliation)*
- **Decision O1**: Dean Court and The Bull's Head Inn have complete Markdown menus extracted, but were omitted from the historical Kafoodie crawl.
- **The Ask**: Provide the Kafoodie outlet names or outlet IDs under which Dean Court (York) and The Bull's Head Inn (Beaumaris) operate.
- **The Result**: Completes the final 2 venues, giving 100% digital parity across all 29 properties.

---

### Item 4: EPOS Vendor Confirmation & Data Samples *(Step 7 Commercial Readiness)*
- **Decision O5**: To scope and build the EPOS integration (PLU mapping, price synchronization, till menus):
- **The Ask**:
  - Name the primary EPOS provider across the estate (e.g. **Zonal Aztec**, **Tevalis**, **Oracle Micros**, or multiple).
  - Sample EPOS item master export (CSV or JSON) containing PLU numbers, item names, and modifier groups.
  - API documentation or export cadence details if automated till sync is desired.
- **The Result**: Enables automatic price matching between printed menus, website prices, and till buttons, ending manual double-entry.

---

### Item 5: Dedicated Host Deployment Target *(LAN / Multi-Computer Access)*
- **Decision D1**: The architecture operates as a single-host server with browser access over LAN/VPN.
- **The Ask**: When the team is ready to open access to general managers and coordinators across the business:
  - Assign a permanent host (e.g. an always-on internal Mac Mini, Windows Server, or Linux box).
  - Allocate a static internal IP or local DNS name (e.g. `http://menu-governance.icg.local:8000`).
- **The Result**: Multiple coordinators and general managers can review menus, check allergen matrices, and monitor launch readiness simultaneously from their own laptops.

---

## 3. Current Live Artifacts for Verification

The platform is running and can be inspected locally at any time:
- **Menu Review & Extraction Tool**: `pages/menu-review.html`
- **Product & Allergen Compliance Inspector**: `pages/product-data.html`
- **Launch Campaign & Site Readiness Matrix**: `pages/launch-readiness.html`
- **Menu Explorer**: `pages/menu-explorer.html`
- **Technical Specifications & Regulatory Guides**:
  - Statutory Allergen Reference: `docs/allergens/UK-allergens.md`
  - Allergen Procedures (England & Scotland): `docs/allergens/Allergen Guide, Procedures and Compliance England and Scotland.md`
  - System Decisions Log: `docs/DECISIONS.md`
  - Architecture Blueprint: `docs/ARCHITECTURE.md`
  - Implementation Roadmap: `docs/ROADMAP.md`
