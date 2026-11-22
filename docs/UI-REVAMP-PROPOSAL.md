# Inn Collection Group — UI Revamp Proposal

> **Document type**: Reference proposal — no code changed  
> **Author**: Antigravity Technical Architecture Agent  
> **Date**: 2026-11-22  
> **Status**: Draft — awaiting stakeholder review before implementation  
> **Companion docs**: Review alongside `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md`, `docs/OPERATIONAL-REQUIREMENTS-HANDOVER.md`

---

## 1. What This Document Is

This is a **read-first, change-later** proposal. It documents the current state of all six frontend UIs, identifies their gaps and overlaps, and proposes a coherent refinement path — without modifying any file.

Nothing here is implemented. When approved, implementation becomes a Step 7 UI sprint.

---

## 2. Current UI Inventory

| File | Lines | Title | Status (per ARCHITECTURE.md) | Navigation consistency |
|:---|---:|:---|:---|:---|
| `pages/menu-review.html` | 1,529 | Menu review | `[Code-verified]` — operational | Partial nav (2 links only) |
| `pages/product-data.html` | 376 | Product data | `[Observed]` — static prototype | Full nav (6 links) |
| `pages/launch-readiness.html` | 314 | Launch readiness | `[Observed]` — client-side simulation | Full nav (6 links) |
| `pages/discovered-media.html` | 987 | Discovered Media | `[Code-verified]` — operational | Inline link buttons, no nav pill |
| `pages/fnb-crosscheck.html` | 155 | F&B Coordinator cross-check | `[Observed]` — static analysis SPA | Full nav (6 links) |
| `pages/menu-explorer.html` | 169 | Menu explorer | `[Code-verified]` — operational | Sparse nav |

**Common design system** (all pages): `--bg:#171513`, `--accent:#e07b4a`, serif/sans/mono font stack, dark card surfaces, pill-style navigation, consistent CSS variable tokens.

---

## 3. Cross-Cutting Problems Found

### 3.1 Navigation Inconsistency

The nav bar is **not the same across all pages**:

- `menu-review.html` lists only **2 links** (Menu review, Menu explorer) — the other four pages are invisible from here
- `discovered-media.html` has **no pill nav** at all — navigation is done with ad-hoc link buttons inside the toolbar bar
- `product-data.html`, `launch-readiness.html`, `fnb-crosscheck.html` all carry a **6-link full nav** — but `fnb-crosscheck.html` is missing from the nav on some pages

**Impact**: A user landing on `menu-review.html` (the most-used tool) cannot see that `product-data.html`, `launch-readiness.html`, or `fnb-crosscheck.html` even exist.

**Files to review together**: `pages/menu-review.html` (line 965–968), `pages/discovered-media.html` (lines 207–252), all other pages (nav block, top of each `<header>`).

---

### 3.2 "Sample data" Badges Are Still Visible

Both `product-data.html` and `launch-readiness.html` carry a visible **"Sample data · front-end skin only"** badge in their `<h1>`. These were placeholders added during design — now that the APIs are live and data is real, the badge is misleading.

```
// product-data.html line 50
<span class="sample" id="sampleBadge">Sample data · front-end skin only</span>

// launch-readiness.html line 56
<span class="sample" id="launchBadge">Sample data · front-end skin only</span>
```

**Files to review together**: `pages/product-data.html` (line 50, 65), `pages/launch-readiness.html` (line 56, 70).

---

### 3.3 Allergen Compliance — Surface Across Multiple UIs

Allergen gap data now flows through **three separate UIs** with no shared visual language:
- `launch-readiness.html` → estate-wide compliance KPI + site grid cell colour
- `product-data.html` → per-product gap badge + FIC filter dropdown + compliance alert banner
- `menu-review.html` → review sidebar status + publication hard block dialog (D12)

A user investigating a gap has to navigate between all three to get the full picture. There is no **single allergen compliance view**.

**Files to review together**: `pages/product-data.html` (lines 55–65, `kpis()` function), `pages/launch-readiness.html` (lines 79–80, `allergenGapsMap`, `allergenSummary`), `pages/menu-review.html` (review sidebar, `saveReviews()` async block), `menu_review_server.py` (`GET /api/allergens/gaps`).

---

### 3.4 `discovered-media.html` Is Visually Isolated

This page uses a **different dark theme** (`--bg:#0f1216`, `--panel:#161b22`) compared to the rest of the estate (`--bg:#171513`). It also predates the shared nav pill design system, using link buttons instead. It operates entirely offline (file input only), with no server API calls.

**Files to review together**: `pages/discovered-media.html` (lines 9–46, 207–258), all other pages (CSS variable blocks at top of `<style>`).

---

### 3.5 `fnb-crosscheck.html` Is Effectively Hidden

At 155 lines, `fnb-crosscheck.html` is the smallest page and the most likely to go unnoticed. Its link label in the nav bar is **"F&B role cross-check"** — which is not obvious to a general manager or coordinator. Its content (a cross-check requirements checker for the F&B coordinator role) is distinct and valuable but underexposed.

---

### 3.6 No Role-Based UI Differentiation

All six pages are served flat, with no role awareness. Per ARCHITECTURE.md §3.5, Phase 3 introduces roles: Chef, F&B Coordinator, Compliance Officer, Commercial Manager, Systems Admin. The nav bar has no mechanism to show/hide pages based on role, and no "home" landing page exists to greet different user types with their relevant views.

**Files to review together**: `docs/ARCHITECTURE.md` (§3.5 Security Model), `db/auth.py`, `db/migrations/003_users.sql`.

---

### 3.7 No Mobile Layout

All UIs assume a wide viewport. The 3-pane layout in `menu-review.html`, the allergen matrix in `product-data.html`, and the 29-venue grid in `launch-readiness.html` break below approximately 900 px. While this platform is not intended for mobile-first use (it's an internal back-office tool on host machines), coordinators or GMs may need to check readiness from a laptop or tablet on-site.

---

## 4. Proposed Refinements

> [!IMPORTANT]
> These are proposals only. No implementation begins until this document is approved by the team.

---

### R1 — Unified Navigation Bar (All Pages)

**Proposal**: Extract the shared nav markup into a consistent 6-link pill bar and apply it identically to all pages, including `menu-review.html` and `discovered-media.html`.

**Navigation order** (proposed):
1. Menu review *(primary operational tool)*
2. Menu explorer
3. Product data
4. Launch readiness
5. F&B cross-check
6. Media library *(rename from "Discovered media")*

**Implementation scope**: 6 HTML files — only the `<nav>` block changes.

**Files**: All `pages/*.html` nav blocks.

---

### R2 — Remove Sample Data Badges

**Proposal**: Remove or conditionally hide the `"Sample data · front-end skin only"` badge in `product-data.html` and `launch-readiness.html` once the venue selector is populated from the live API.

The badge should only appear when `venue === "sample"` (the default fallback when no venue exports exist). When real data loads, the badge disappears.

**Files**: `pages/product-data.html` (line 50, `sampleBadge` element and its show/hide logic), `pages/launch-readiness.html` (line 56, `launchBadge`).

---

### R3 — Allergen Compliance Dashboard Panel

**Proposal**: Add a dedicated **Allergen Compliance** panel to `launch-readiness.html` (or as a new lightweight page `pages/allergen-compliance.html`) that consolidates:

- Estate-wide summary (total products, total missing, % compliant)
- Per-venue breakdown table (venues with gaps highlighted)
- Quick-link to `product-data.html?venue=<slug>&filter=gap` to drill into specific products
- Status of the 4 known blocking recipes (from the Operational Requirements Handover)

This panel would be driven entirely by the existing `GET /api/allergens/gaps` endpoint — no new backend work required.

**Decision alignment**: D12 (hard publication block must be surfaced clearly), D7 (read-only mirror only — no allergen editing here).

**Files**: `pages/launch-readiness.html` (extend existing allergen KPI section), `menu_review_server.py` (`GET /api/allergens/gaps` — already implemented).

---

### R4 — Align `discovered-media.html` to Shared Design System

**Proposal**: Update `discovered-media.html` to use the same CSS variable tokens as the rest of the estate:

```css
/* Change from: */
--bg:#0f1216; --panel:#161b22; --panel2:#1c2330; --line:#2a3341;

/* To: */
--bg:#171513; --bg-card: /* match other pages */; --border: /* match */;
```

Also replace the ad-hoc link buttons in the toolbar with the standard pill nav.

**Files**: `pages/discovered-media.html` (lines 9–46 CSS variables, lines 237–240 nav links).

---

### R5 — ICG Home / Dashboard Landing Page

**Proposal**: Create `pages/index.html` as a true **home dashboard** (not a redirect). It would show:

- Estate health summary (venues exported, allergen compliance %, open issues)
- Role-aware quick links (once auth roles are in place — Phase 3)
- Recent activity feed from the `audit_events` SQLite table
- System status (last rebuild timestamp, DB backup timestamp)

This replaces the previously deleted `pages/index.html` (which was byte-identical to `menu-explorer.html` — see Decision D11).

**Decision alignment**: ARCHITECTURE.md §3.5 (home page is the natural role-based entry point for Phase 3 RBAC).

**Files**: New `pages/index.html`, `menu_review_server.py` (add `GET /api/health` summary endpoint), `db/auth.py` (session-aware role check for Phase 3 gating).

---

### R6 — Rename and Reposition F&B Cross-Check

**Proposal**: Rename the nav link from `"F&B role cross-check"` to `"F&B checklist"` or `"Pre-launch checklist"` for clarity. Consider integrating the cross-check results into the `launch-readiness.html` workstreams panel as a sub-view rather than a standalone page, since it directly feeds the `MEN` workstream's completion criteria.

**Files**: `pages/fnb-crosscheck.html` (title, nav label), `pages/launch-readiness.html` (workstream drawer integration).

---

### R7 — Kafoodie Sync Status Indicator (D13 Readiness)

**Proposal**: Once Kafoodie API credentials are received (Item 2 in the Operational Requirements Handover), all UIs that display product or allergen data should show a **"Last synced from Kafoodie: <timestamp>"** indicator. This indicator should:
- Turn amber if the last sync is older than 24 hours
- Turn red if older than 72 hours or if the last sync failed

**Decision alignment**: D13 (direct API ingestion selected — requires sync status surface).

**Files**: `pages/product-data.html` (top bar), `pages/launch-readiness.html` (KPI strip), new `GET /api/kafoodie/sync-status` server endpoint (not yet implemented — blocked on O1 API credentials).

---

## 5. Implementation Priority

| Ref | Change | Effort | Blocked by | Priority |
|:---|:---|:---|:---|:---|
| R2 | Remove sample data badges | Trivial (< 10 lines per file) | Nothing | **Do first** |
| R1 | Unified nav bar | Low (markup only, 6 files) | Nothing | **High** |
| R4 | Align discovered-media CSS | Low (CSS vars swap) | Nothing | **High** |
| R3 | Allergen compliance panel | Medium (new HTML + API call) | Nothing — API exists | **High** |
| R5 | Home dashboard page | Medium (new page + 1 endpoint) | Nothing for MVP | **Medium** |
| R6 | Rename F&B cross-check | Trivial | Nothing | **Medium** |
| R7 | Kafoodie sync status | Medium (new endpoint + indicator) | O1 API credentials | **Low — gated** |

---

## 6. What Requires a Human Decision Before Work Starts

| # | Question | Required from |
|:---|:---|:---|
| A | Should the allergen panel (R3) be a tab within `launch-readiness.html` or a new standalone page? | F&B Director / IT |
| B | Should `fnb-crosscheck.html` remain standalone or be absorbed into `launch-readiness.html`? | F&B Coordinator |
| C | Is there appetite to build the home dashboard (R5) now, or defer to Phase 3 RBAC? | Leadership |
| D | Confirm the preferred nav link labels before R1 implementation | F&B Coordinator |

---

## 7. Files Reference Map

The table below maps each proposal to every file that must be read and edited together when implementing it.

| Proposal | Files to read first | Files to edit |
|:---|:---|:---|
| R1 — Nav bar | All `pages/*.html` nav blocks | All 6 `pages/*.html` nav sections |
| R2 — Sample badges | `pages/product-data.html` L50, 65; `pages/launch-readiness.html` L56, 70 | Same 2 files |
| R3 — Allergen panel | `menu_review_server.py` (`/api/allergens/gaps`); `pages/launch-readiness.html` (allergenSummary block) | `pages/launch-readiness.html` or new `pages/allergen-compliance.html` |
| R4 — CSS alignment | `pages/discovered-media.html` L9–46; any other page CSS vars block | `pages/discovered-media.html` |
| R5 — Home page | `docs/ARCHITECTURE.md` §3.5; `db/auth.py`; `db/migrations/003_users.sql`; `menu_review_server.py` | New `pages/index.html`; `menu_review_server.py` (new endpoint) |
| R6 — F&B rename | `pages/fnb-crosscheck.html` L49; all pages nav labels | `pages/fnb-crosscheck.html`; nav on all pages (combined with R1) |
| R7 — Sync status | `docs/DECISIONS.md` D13; `docs/OPERATIONAL-REQUIREMENTS-HANDOVER.md` Item 2 | New `GET /api/kafoodie/sync-status`; `pages/product-data.html`; `pages/launch-readiness.html` |

---

## 8. What This Proposal Does NOT Change

- **Visual language**: The existing dark design system, accent colour (`#e07b4a`), and typography stack remain unchanged unless explicitly approved to change
- **Data authority**: No UI change alters where data is authored (see `docs/ARCHITECTURE.md` §4 Data Authority Matrix)
- **D12 hard block**: The publication gate is non-negotiable and must remain enforced in any UI revision
- **D7 scope boundary**: Product/allergen data remains read-only from Kafoodie — no editing of allergen declarations in any UI
- **Modular monolith**: No new runtime dependencies are introduced — all UI revisions are plain HTML/CSS/JS on the same Python stdlib server
