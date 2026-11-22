# Hospitality Technology Capability Assessment: Discovered Media

**Service:** Discovered Media — Review & Download, part of the Inn Collection Group (ICG) tool set **URL:** https://inn-collection-group.netlify.app/discovered-media **Assessment date:** 22 November 2026

## 0. Evidence basis and method (read first)

This assessment was produced by retrieving the deployed pages as text. I could **not** click, filter, load a CSV, run an export, open DevTools or read the JavaScript and CSS behind the pages. The pages appear to be client-rendered, so the fetched text contains interface labels and page copy but no data.

Consequences for the evidence classes in the brief:

- **Observed (strict sense, tested by interaction): none.** No capability below was exercised.
- **Observed (page text):** I use this label only where the page states something in words (for example "Sample data · front-end skin only"). It is a reading of the page's own claims, not a test.
- **Code-verified: none.** No source was available to me. The only code-related evidence is the page copy naming `menu_review_server.py` and `discovered_media.csv`, and a sibling page that says its author read the code (see section 8).
- **Inferred:** a capability suggested by interface labels, with behaviour unverified.
- **Proposed:** future capability that needs development or integration.

Areas I could not test: every filter, selection control, export format, CSV loading, the local server, and any data. All six pages loaded in an empty or loading state, so no real ICG content (venues, menus, URLs, allergens, prices) was visible to me.

## 1. Service identification

| Item | Finding | Status |
| --- | --- | --- |
| Name | Discovered Media — Review & Download | Observed (page text) |
| Host | Netlify static deployment, sharing one navigation bar with five sibling pages | Observed (page text) / Inferred (Netlify hosting from the domain) |
| Purpose | A review-and-download page for a list of media assets (menus as PDFs, other PDFs, images, archives, other documents) discovered for ICG venues, organised by region, venue and category | Inferred |
| Intended users | Whoever is assembling or auditing venue menu material: a central F&B or content team, not site staff or guests | Inferred |
| Input | A file named `discovered_media.csv`, dragged onto the page or chosen with a file picker | Observed (page text) |
| Output | Downloads, helper scripts or URL lists (section 3) | Observed (page text) |

What it appears to be: the **intake and triage stage** of a menu-data pipeline. Something upstream (not visible here) has crawled or collected ICG venue web assets and written them to a CSV. This page lets a person narrow that list and pull the files down so they can be reviewed in **Menu review** and structured downstream. The upstream discovery process itself is not evidenced anywhere I could access.

## 2. Interface and architecture

### 2.1 The discovered-media page

Controls visible in the page text, in order:

1. **Filters:** All regions, All venues, All categories, and a type filter with the options Menus (PDFs), All PDFs, Images, Archives, Other Docs.
2. **Selection:** Select all visible, Clear, Invert visible.
3. **Counters:** "0 selected", "0 assets · 0 URLs". Assets and URLs are counted separately, which suggests one asset can carry more than one URL (for example variants or duplicates). Unverified.
4. **Cross-links:** Review menus, Menu explorer, Launch readiness, Product data.
5. **Export selected** with six options (section 3).
6. **Load panel:** drag a CSV anywhere on the page or choose a file, plus the instruction "Start the local server with `python3 menu_review_server.py` to load this page and the menu review automatically."

### 2.2 Architecture signals

- **Two run modes (Observed, page text).** Locally, `menu_review_server.py` serves the page and supplies data automatically. On the public Netlify deployment there is no such server, so the page falls back to manual CSV loading. I believe, but did not verify, that the download-to-folder option depends on the local server.
- **Contradiction worth noting.** The page tells the reader to run a local Python server, yet it is published at a public URL. Anyone reaching it publicly gets an empty tool unless they hold the CSV. The deployment is a shell of the tool, not the working tool.
- **No visible authentication, roles or persistence.** Nothing in the text indicates login, user identity or server-side saving. Selection state is probably in browser memory only. Inferred.

### 2.3 Sibling modules reachable from the shared navigation

| Page | What the text shows | Status of the page itself |
| --- | --- | --- |
| Menu review | Filters (region, venue, menu type: Food, Drinks, Sunday, Events, Other; review status: Needs review, Reviewed, Flagged), a "MENU FILES" list, extracted markdown (Rendered / Source) beside the original PDF viewer with zoom and Open PDF, and actions Keep open, Mark intentional, Mark fixed, Remove selected duplicate lines. Counter reads "0 of — reviewed, 0 flagged"; body shows "Loading menus..." | Appears to be a working review UI, empty on the public deployment |
| Menu explorer | Tabs: Menu, Guest view, Allergen matrix, Compare venues, Venue & menu data, Allergen reference; controls "may-contain counts" and "Free from" | No data rendered |
| Launch readiness | "Spring menu 2027 · launch 1 Mar 2027", "Shown as of 8 Feb 2027", a four-milestone timeline, workstreams with completion rules, site readiness with statuses Done / In progress / At risk / Blocked / Not started | **Self-declared** "Sample data · front-end skin only"; "Everything here is invented to show the layout" |
| Product data | "One record per product: allergens, nutrition, recipe, price and codes, each with its own accuracy check"; filters for record state (blocking issues, warnings only, clean); Products and Allergen matrix views | **Self-declared** "Sample data · front-end skin only"; checks "would run on save" in a real build |
| F&B role cross-check | Requirement-by-requirement comparison of an F&B Coordinator job advert against what SegStudio and menu-review do today; filters Covered / Partial / Not yet / A person, not software; "Copy as Markdown" | Analysis document, not an operational tool |

A caution on dates: Launch readiness displays "as of 8 Feb 2027", which is in the future relative to today. This is consistent with its sample-data label (an invented "today" marker), but a reader could mistake it for a real schedule.

## 3. Capability map: Discovered Media

| # | Capability | What it does and how (as far as can be known) | Information used or produced | Status |
| --- | --- | --- | --- | --- |
| C1 | Load discovered-media CSV | Reads `discovered_media.csv` by drag-and-drop or file picker, presumably parsed in the browser | In: CSV of discovered assets. Columns are not visible, but the manifest export implies url, host, path, type, category, and the filters imply region and venue | Observed (page text) for the control; columns Inferred |
| C2 | Auto-load via local server | `python3 menu_review_server.py` serves this page and the menu review and loads data without manual upload | Local data files | Observed (page text); behaviour not tested |
| C3 | Filter by region, venue, category, file type | Narrows the list to a scope (for example one venue's menu PDFs) | Region, venue and category are metadata attached to each asset; type distinguishes menu PDFs from other PDFs, images, archives and other documents | Inferred |
| C4 | "Menus (PDFs)" versus "All PDFs" | Separates PDFs judged to be menus from other PDFs, implying a classification rule exists upstream or in the page | Classification flag or rule, source unknown | Inferred |
| C5 | Bulk selection | Select all visible, Clear, Invert visible, with live counts of assets and URLs | Selection set | Inferred |
| C6 | Export: Download files | Saves files into `exports/` organised by region, venue and category | Files fetched from source URLs; folder structure derived from metadata | Observed (page text); mechanism untested |
| C7 | Export: Bash script | A manual download script with category folders | Generated text | Observed (page text) |
| C8 | Export: PowerShell script | Same, for Windows | Generated text | Observed (page text) |
| C9 | Export: wget list | URLs only, for `wget -i` | URL list | Observed (page text) |
| C10 | Export: plain URL list | One URL per line | URL list | Observed (page text) |
| C11 | Export: manifest CSV | Columns url, host, path, type, category | Tabular manifest | Observed (page text) |
| C12 | Copy URLs to clipboard | Convenience | URL list | Observed (page text) |
| C13 | Open in new tabs | First 15 only, because browsers block more | URLs | Observed (page text) |
| C14 | Hand-off to Menu review | Link to the review page, which consumes downloaded menus converted to markdown | n/a | Observed (link); data flow between the two Inferred |

The range of export routes is telling. Offering scripts and `wget` lists alongside direct download suggests the author expected downloads to be blocked or impractical in some settings, so the page produces instructions for running the job elsewhere. That is a pragmatic design, but it also shows that the tool itself does not guarantee file retrieval.

### Capabilities elsewhere in the tool set that bear on this component

- **Menu review (Inferred from labels):** side-by-side comparison of extracted markdown and source PDF, per-line status marking, duplicate-line removal. The corresponding local file and server are also described in the F&B role cross-check page.
- **Menu explorer (Inferred):** allergen matrix, cross-venue comparison, a guest-facing view and an allergen reference.
- **Product data and Launch readiness:** demonstrations only, by their own declaration (Proposed).

## 4. Observed workflows

No workflow was run. The following is the journey the page structure implies (Inferred):

1. An upstream process (not visible) gathers menu-related files from venue web presences and writes `discovered_media.csv`.
2. The operator loads the CSV, either via the local server or by dragging it in.
3. The operator filters to a region or venue and to "Menus (PDFs)".
4. The operator selects rows and exports, either downloading directly or generating a script or manifest.
5. Downloaded PDFs are converted to markdown (conversion tooling not visible here) and opened in **Menu review**.
6. A reviewer compares markdown to PDF, marks items fixed, intentional or flagged, and removes duplicate lines.
7. Corrected menu data feeds the explorer, allergen views and, in the proposed design, product records and launch tracking.

Steps 1, 5 and 7 are the least evidenced. The page itself does not show how a file moves from download to review.

## 5. Information architecture

### 5.1 Entities and relationships (Inferred unless stated)

- **Region** contains **Venues**.
- **Venue** has many **Media assets** (PDF, image, archive, other document), each with one or more **URLs**.
- **Media asset** has a **category** and a **type**. Some assets are menus, which have a **menu type** (Food, Drinks, Sunday, Events, Other).
- **Menu file** has an **extracted markdown** version, an original PDF, a **review status** (Needs review, Reviewed, Flagged) and line-level marks (Observed in labels on the menu-review page).
- **Product** (proposed) is a record carrying allergens, nutrition, recipe, price and codes, each with an accuracy check (Observed as a self-declared mock-up).
- **Launch / menu change** (proposed) has milestones, workstreams and per-site readiness (mock-up).

### 5.2 Information characteristics

| Question | Finding |
| --- | --- |
| Live or static? | Static. Data enters as a CSV snapshot. No live feed is evidenced. |
| How maintained? | Manually, through CSV regeneration and human review marks. |
| Validated? | Not on this page. Review is human, on the menu-review page. The product-data mock-up describes automated save-time checks, but as a proposal. |
| Where stored? | Unknown. Local files when the local server is used; browser memory otherwise. No evidence of a database. |
| Shared how? | By downloading files and manifests. No shared workspace or permissions are evidenced. |
| Outputs | Folder trees of downloaded files, scripts, URL lists, manifest CSV. |

### 5.3 Operational consequences when information changes

The data is a snapshot of public web assets. If a venue replaces its menu PDF, the CSV goes stale and nothing indicates detection or notification. Any dish, price or allergen correction made in review is separate from the source PDF on the venue site, so the group could end up holding a corrected internal copy while the public PDF stays wrong. Public web material is also not verified internal data: a menu PDF online may not match what the kitchen is serving.

## 6. Hospitality applications

### Central teams (primary users)

- **Menu inventory and audit.** For a group with about 31 sites (the figure in the job advert captured on the cross-check page), finding which venues publish which menu files and in what format is a prerequisite to any consistency work. Example: filter to Sunday menus in one region to see which venues have a current PDF at all.
- **Evidence capture before change.** Downloading and filing the current public menus gives a baseline before a seasonal relaunch such as the Spring 2027 programme named on the Launch readiness mock-up.
- **Preparation for allergen and compliance work.** Menu text extracted from PDFs is the raw material for an allergen matrix. This page is the front of that chain, but it carries no allergen data itself.

### Individual sites

No site-facing function is evidenced. A general manager or chef could benefit indirectly if reviewed menu data later feeds a guest view or allergen matrix, which is a separate component.

### Areas deliberately left out

Nothing on this page concerns suppliers, procurement, inventory, costing, staff training or communication. The cross-check page itself lists training materials, retail products, supplier liaison data and menu document history as not yet covered. EPOS is reported there as not addressed.

## 7. AI and automation opportunities

All items below are **Proposed**. No AI functionality is evidenced on any page I retrieved. The page cross-check describes the tool set in terms of documents and plans, not model use.

| Opportunity | Description | Human-workflow angle |
| --- | --- | --- |
| Scheduled discovery and change detection | Re-crawl venue sites, compare hashes or text, and flag changed or removed menus rather than relying on a manually regenerated CSV | A coordinator is told "three venues changed their Sunday menu this week" instead of re-running a process |
| Menu classification | Classify PDFs as food, drinks, Sunday, events, or not a menu; detect duplicates and superseded versions | Removes manual triage of non-menu files |
| Extraction with confidence scores | Convert PDF to structured items, prices and allergen declarations, highlighting low-confidence lines for human review | Reviewers see only what needs judgement; the existing review UI already models a mark-and-fix pattern |
| Cross-venue anomaly detection | Flag a price or dish naming outlier among comparable venues, or allergen statements that differ between menu versions | Supports a central chef or coordinator without asking sites to report |
| Natural-language questions | "Which venues in the north list a vegan main?" answered from reviewed data, with source PDF and line cited | Chefs and managers ask in plain words; the system finds the record |
| Role-aware assistance via existing channels | Surface menu answers in the tools site teams already use (messaging, email) | Fits the principle that software should learn people. Dependency: requires integration not evidenced here |
| Launch-readiness feeds | Drive the Launch readiness view from real menu, recipe and product records, as its own text proposes | Status stops being hand-set |

Guardrail: allergen and nutrition information is safety-critical. Any AI output must be reviewed by an accountable person, retain its source reference, and never be presented to guests as verified until it is.

## 8. Limitations and dependencies

- **Evidence limit.** My assessment is of static page text only. Behaviour, data, code and the real data model are unverified.
- **Empty public deployment.** All data-bearing pages show zero or loading states, so the live tool's usefulness depends on a CSV and local server I cannot see.
- **Local-server dependency.** Automatic loading and probably folder download depend on a Python script running on the user's machine. Not suited to non-technical site staff.
- **Browser constraints.** The page itself notes the 15-tab limit. Direct download of many files may hit browser or cross-origin restrictions; hence the script exports.
- **Snapshot data.** No evidence of refresh, versioning or scheduling.
- **No access control evident.** A public deployment of an internal tool prompts the question of what, if anything, is exposed once data is loaded. Unknown.
- **Source quality.** Public menus are not equivalent to internal specifications, recipes or supplier data.
- **Self-reported coverage.** The F&B cross-check says it was assessed "from reading the uploaded SegStudio docs, the gap-closure plan, and the menu-review.html and menu\_review\_server.py code. Nothing was run", and that SegStudio ships with an empty data folder, so "covered" means documented rather than populated. I treat that page as a design statement, not as evidence of working functionality.
- **Inconsistency.** The cross-check refers to `menu-review.html` and `menu_review_server.py`; the deployed route is `/menu-review`. The Discovered Media page refers to a local server that cannot exist at the public URL. The tool set is positioned between a local workbench and a hosted product without committing to either.

## 9. Ecosystem contribution

What this component contributes: **a controlled way to turn scattered public venue documents into a reviewable, filterable, exportable corpus.** It makes available the list of what each venue publishes and the files themselves. It serves a central F&B or content person doing audit and preparation work.

How it could fit a larger, human-centred system (Proposed):

- **Intake layer** feeding a product and menu data store, with Menu review as the quality gate and Menu explorer as the read-only view.
- **Source-of-record linkage.** Each downstream menu item and allergen entry keeps a link back to the original asset URL and file, so a manager can see where a statement came from.
- **Connection to other services.** Recipes, supplier specifications, EPOS items and training content are separate datasets that this component does not touch. Linking them needs identifiers (product codes, venue IDs) that the page does not currently show.
- **Human-centred direction.** The least demanding path for sites is that they continue to publish menus as they do now, and the system watches for changes, extracts and asks the central team to confirm, rather than asking each site to learn a new data-entry tool.

## 10. Further investigation

To turn inferences into evidence I would need:

1. A sample `discovered_media.csv` (or the repository) to confirm columns, counts, venue and region coverage and how "menu" is classified.
2. A browser session to test filters, selection, each export and the 15-tab limit, without submitting anything.
3. The page source to verify what runs client-side, whether anything is sent to a server, and whether state persists.
4. Documentation or code for the upstream discovery process: what is crawled, how often, with what permissions.
5. The PDF-to-markdown conversion method and its accuracy, since the menu-review author's own notes say conversion quality has been a problem.
6. Confirmation of whether the public Netlify deployment is meant to be accessible to anyone and whether loaded data is processed only locally.
7. How review marks are saved (file, server, browser) and whether they can be shared between reviewers.
8. Whether any identifier links a discovered asset to a product, recipe or POS item.

## 11. Summary judgement

- **Evidenced:** the page's intended inputs, filters, selection controls and six export routes, and the surrounding set of pages. **Self-declared as demonstration only:** Launch readiness and Product data.
- **Not evidenced:** any live data, persistence, integration, AI or operational outcome.
- **Value:** a sensible, modest intake step in a menu-data pipeline. Its worth will depend on the quality of the upstream CSV and on connecting reviewed output to product, allergen and launch data.
