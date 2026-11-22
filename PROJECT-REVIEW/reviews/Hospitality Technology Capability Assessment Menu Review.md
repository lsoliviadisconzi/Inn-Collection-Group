# Hospitality Technology Capability Assessment: Menu Review

**Service:** Menu review — Inn Collection Group **URL:** https://inn-collection-group.netlify.app/menu-review **Assessment date:** 22 November 2026

## 0. Evidence basis (read first)

I retrieved the page, and the sibling pages linked from its navigation, as text. I could **not** click, filter, load data, mark a line, open a PDF, or read the JavaScript behind the page. The page text shows interface labels and an empty state only. No menu content was visible, so nothing was tested.

- **Observed (strict, by interaction): none.**
- **Observed (page text):** used only for labels and statements actually present in the retrieved page. It records what the page says, not that it works.
- **Code-verified: none.** No source or technical documentation was accessible to me. The only references to code are page copy on a sibling page naming `menu_review_server.py`, and a self-description on the F&B role cross-check page, which says its author read the `menu-review.html` and `menu_review_server.py` code and that nothing was run. I treat those as claims, not verification.
- **Inferred:** a capability suggested by labels, behaviour unverified.
- **Proposed:** future capability needing development or integration.

**Important caveat on the empty state.** The page shows "Loading…", "Loading menus..." and "0 of — reviewed". The retrieval tool may not run page scripts, so I cannot say whether the live page would fill with data in a browser. I report the state I saw, not a fault.

## 1. Service identification

| Item | Finding | Status |
| --- | --- | --- |
| Name | Menu review, within the Inn Collection Group tool set | Observed (page text) |
| Purpose | Side-by-side checking of text extracted from menu PDFs (as markdown) against the original PDF, with review statuses and tools for handling duplicated lines | Inferred |
| Intended users | A central F&B, content or menu-data reviewer. No site-staff or guest function is shown | Inferred |
| Place in the tool set | The review stage after Discovered media (collection) and before Menu explorer (reading, allergens, comparison). Shared navigation links six pages | Observed (navigation); sequence Inferred |
| Data source | Not stated on the page itself. The Discovered media page says a local `menu_review_server.py` loads the review "automatically" | Observed (sibling page text) |

## 2. Interface and architecture

### 2.1 Layout

1. **Header:** a menu icon (☰), the title "Inn Collection Group / Menu review", and navigation links to Menu review, Discovered media, F&B role cross-check, Launch readiness, Product data and Menu explorer.
2. **Progress counters:** "0 of — reviewed" and "0 flagged".
3. **Filter bar:** a "Minimal" control; All regions; All venues; All menu types (Food, Drinks, Sunday, Events, Other); All review statuses (Needs review, Reviewed, Flagged); a Clear button.
4. **Menu files list:** headed "MENU FILES" with a count placeholder "—".
5. **Extracted markdown pane:** with a Rendered / Source toggle and a file-name placeholder.
6. **Original PDF pane:** zoom controls (− and +), an "Open PDF" link, and a file-name placeholder.
7. **Action bar:** Keep open, Mark intentional, Mark fixed, Remove selected duplicate lines, and a Close control.

All of the above is Observed (page text) as labels. What each control does is Inferred.

### 2.2 Architecture signals

- The page is a single client-side view that depends on data supplied at run time. On this deployment I could not see where that data comes from.
- The sibling Discovered media page says to start `python3 menu_review_server.py` "to load this page and the menu review automatically". That implies a local Python server supplying menus to the page. If that is how the tool is meant to run, the public Netlify URL is a copy of the front end without its data (Inferred).
- No login, user identity, role or approval step is visible (Observed by absence in text; not a proof of absence in the code).

## 3. Capability map

| # | Capability | What it does and how (as far as can be known) | Information used or produced | Status |
| --- | --- | --- | --- | --- |
| M1 | Menu file list | Lists available menu files for review, filtered by the controls below | Menu file records: venue, region, type, review status | Inferred |
| M2 | Filter by region, venue, menu type, review status | Narrows the list, for example to one venue's Sunday menu still marked Needs review | Metadata on each menu file | Inferred |
| M3 | Review status model | Three states per menu: Needs review, Reviewed, Flagged, rolled up into "n of N reviewed, n flagged" | Status per file; progress counts | Inferred (labels) |
| M4 | Extracted markdown view | Shows the markdown extracted from the PDF, either rendered or as raw source | Markdown text derived from PDF | Inferred |
| M5 | Original PDF view | Shows the source PDF with zoom and an Open PDF link, so the reviewer can check extracted text against the original | The source PDF | Inferred |
| M6 | Duplicate-line handling | Actions to keep a duplicated line open, mark it intentional, mark it fixed, or remove selected duplicate lines | Line-level marks; edited markdown | Inferred |
| M7 | "Minimal" mode | A reduced-chrome display option; exact effect unknown | UI preference | Inferred |
| M8 | Clear filters | Resets filters | None | Inferred |
| M9 | Cross-navigation | Links to the other five pages | None | Observed (page text) |

**What is not evidenced:** how extracted markdown is produced, where review marks and edits are saved, whether "Remove selected duplicate lines" changes a file or only a view, and whether corrections ever reach any other system. Anything beyond the labels above is a Proposal.

## 4. Observed workflows

No workflow was executed. The journey the layout implies (Inferred):

1. Reviewer opens the page and filters to a region, venue and menu type, typically to the Needs review status.
2. Reviewer selects a menu file from the list.
3. The extracted markdown and the original PDF appear side by side.
4. Reviewer compares them, switching between Rendered and Source, zooming the PDF, or opening it in a new tab.
5. Where the extraction contains repeated lines, the reviewer selects them and either removes them or marks them intentional, fixed or kept open.
6. The file is set to Reviewed or Flagged, and the counters at the top update.

This is a quality-control loop for PDF-to-text conversion. The page gives no indication of how a flagged file gets fixed upstream or who is informed.

## 5. Information architecture

### 5.1 Entities and relationships (Inferred)

- **Region** contains **Venues**; each **Venue** has **Menus**.
- A **Menu** has a **type** (Food, Drinks, Sunday, Events, Other), an **original PDF**, an **extracted markdown** version and a **review status**.
- A markdown file contains **lines**; some lines are flagged as duplicates and carry a **line status** (open, intentional, fixed).

The page also hints at a **two-level status model**: file-level (Needs review, Reviewed, Flagged) and line-level (Keep open, Mark intentional, Mark fixed). How the two relate, for example whether unresolved duplicate lines block a file being Reviewed, is unknown.

### 5.2 Information characteristics

| Question | Finding |
| --- | --- |
| Live or static? | Not evidenced. Menus appear to be files rather than a live feed |
| Source | Menu PDFs and markdown derived from them; origin upstream is likely the Discovered media list (Inferred from the shared navigation and the sibling page's wording) |
| Calculated | Progress counts and flagged counts, plus possibly duplicate-line detection (Inferred) |
| Updated and stored | Unknown. The "Source" toggle and removal action suggest the markdown can be edited, but where results are saved is not visible |
| Validated | By human review. No automated validation of prices, dishes or allergens is evidenced |
| Shared | No sharing, comments or multi-reviewer function is visible |

### 5.3 Consequences when information changes

If a venue replaces a menu PDF, any earlier extraction and review marks refer to a superseded document. Nothing shown indicates version tracking or stale-review warnings. Removing lines from the extracted markdown creates a reviewed text that no longer matches the PDF exactly, which is fine if intended and risky if the removed line was a real repeated item (for example the same side dish offered under two headings). The page offers "Mark intentional" to cover that case.

## 6. Hospitality applications

### Central operations

- **Menu data quality.** Before menus are used for allergen matrices, comparison or launch planning, someone must confirm that the text is right. Example: a Sunday menu PDF with a two-column layout can extract with lines out of order or doubled; the side-by-side view lets a reviewer catch that against the source.
- **Audit trail of effort.** A "reviewed / flagged" counter provides a simple progress measure across a group with many venues. The F&B cross-check page cites a job advert covering 31 sites, which gives a sense of scale. It is the advert's figure, not verified data.
- **Prioritisation.** Filtering by region or menu type lets a central coordinator work through a launch's priority menus first.

### Individual sites

No function addressed to a general manager, chef or front-of-house team is visible. Sites would benefit only indirectly if reviewed text later feeds a guest view or allergen reference.

### Not relevant here

Suppliers, procurement, inventory, costing, training and staff communication are not addressed by this page.

## 7. AI and automation opportunities (all Proposed)

No AI functionality is evidenced on this page.

| Opportunity | Description | Human-workflow angle |
| --- | --- | --- |
| Layout-aware extraction | Use a vision-language model to read the PDF as a human would, handling columns, symbols and dietary icons, and output structured items (name, description, price, allergen marks) | Reduces the duplicate and out-of-order lines the page has tools to repair |
| Confidence-ranked review | Highlight only lines the extraction is unsure of, and jump the reviewer to them | The reviewer's time goes on judgement, not on rereading whole menus |
| Click-to-source linking | Selecting a line in the text highlights the matching region of the PDF | Faster checking of a price or allergen against the original |
| Automated checks | Flag prices with odd formats, missing prices, unknown allergen codes, or differences from the previous version of the same menu | Warns before a human sees it |
| Version comparison | When a venue publishes a new PDF, show only what changed | Avoids re-reviewing unchanged menus |
| Natural-language lookup | "Which Sunday menus in this region are still unreviewed?" or "show every menu mentioning a vegan option" | Questions asked in plain words rather than by learning filters |
| Reviewer assistance in familiar channels | Send a coordinator a short digest of flagged files by email or messaging with a link to the exact line | Fits existing habits; the principle that software should learn people |

Guardrail: menu text feeds allergen information. Any automated extraction or correction needs a named human reviewer, retained source references and a record of what changed.

## 8. Limitations and dependencies

- **Evidence limit.** Static text only; every behavioural statement is inference.
- **No visible data.** The deployed page shows no menus, so the quality of extraction, the duplicate detection and the review experience are unassessed.
- **Local-server dependency.** Data loading appears tied to `menu_review_server.py` (per sibling page text). Public deployment alone would not provide it.
- **Persistence unknown.** A review tool that cannot save marks and edits would lose its value. Nothing here shows where they go, whether they are shared, or whether they survive a reload.
- **Single-user assumption.** No identity, concurrency control or approval is visible.
- **Source quality.** Menu PDFs are public-facing documents; they are not recipes, specifications or verified allergen records. A correct transcription can still be wrong about what is in the dish.
- **Inconsistencies.** (a) The page route is `/menu-review` while the F&B cross-check page refers to `menu-review.html`. (b) The Discovered media page documents a local run mode that the public URL cannot provide. (c) The Launch readiness and Product data pages declare themselves sample data, while Menu review and Discovered media make no such statement, so a reader cannot tell from the pages alone which are working tools and which are mock-ups.

## 9. Ecosystem contribution

What this component contributes: **a human quality gate between raw extracted text and anything that will rely on it.** It makes available reviewed menu text, plus status and duplicate-line decisions, and it serves a central reviewer or coordinator.

How it could fit a larger system (Proposed):

- **Upstream:** receives menu files from Discovered media.
- **Downstream:** supplies reviewed menu items to Menu explorer, the allergen matrix and, in the proposed design, product records and Launch readiness.
- **Traceability:** each reviewed line keeps a link to its source PDF and page, so an allergen answer can be traced back.
- **Other systems:** recipes, supplier specifications and EPOS items would need shared identifiers to connect to reviewed menu lines. None are evidenced.
- **Human-centred direction:** sites keep publishing menus as they do now; the system extracts and checks, and asks a person only where it is unsure.

## 10. Further investigation

1. A browser session with real data to test every control, without saving or submitting anything.
2. The page source and `menu_review_server.py`, to verify data loading, save behaviour, endpoints and any external calls.
3. A sample menu with its PDF and markdown, to judge extraction quality and how duplicates are detected.
4. What "Minimal" does, and what "Close" and "Keep open" apply to.
5. How file-level and line-level statuses relate.
6. Where review marks and edits are stored, and whether more than one reviewer can work at once.
7. How menus are converted to markdown, and who owns the conversion.
8. Whether the public deployment is intended to be public, and what it exposes once data is present.
9. Whether any identifier links reviewed menu lines to products, recipes or POS items.

## 11. Summary judgement

- **Evidenced (page text):** a review interface with filters, status counters, markdown and PDF panes and duplicate-line actions, linked to five sibling pages.
- **Not evidenced:** working behaviour, data, persistence, validation, integration or AI.
- **Value:** a well-targeted review step whose worth depends on how good the extraction is, where decisions are stored, and whether reviewed output reaches the pages that rely on it.
