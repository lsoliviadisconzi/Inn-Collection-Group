# Hospitality Technology Capability Assessment: F&B Role Cross-check

**Service:** F&B Coordinator — role cross-check, Inn Collection Group **URL:** https://inn-collection-group.netlify.app/fnb-crosscheck **Assessment date:** 22 November 2026

## 0. Evidence basis (read first)

I retrieved the page as text. I could **not** click a filter, expand a row, use "Expand all" or "Copy as Markdown", or read the page's code. The text I received contains the title, an introduction, filter labels, table column headings and three written notes. **The requirement rows themselves, with their per-requirement statuses, did not appear**, so I cannot report which individual requirements are marked Covered, Partial or Not yet.

This page is different in kind from the others in the tool set. It is not a menu, product or launch tool. It is a **gap analysis**: a document-style page that compares a job advert against what two other components do. Its content is the author's assessment, not operational data. I treat its statements as **claims by the page**, which I read and report but did not verify.

Evidence classes used:

- **Observed (strict, by interaction): none.**
- **Observed (page text):** present in the retrieved text. It records what the page says, not that it is correct.
- **Code-verified: none.** The page itself says it was based on reading code; I did not.
- **Inferred:** suggested by labels, unverified.
- **Proposed:** a possible future capability.

## 1. Service identification

| Item | Finding | Status |
| --- | --- | --- |
| Name | F&B Coordinator — role cross-check | Observed (page text) |
| Purpose | Set each requirement in a job advert against what SegStudio and menu-review.html "do today" | Observed (page text) |
| Source document | A Harri job advert, "captured 20/11/2026, full time, £28,000, closes 16 Dec 2026, 31 sites" | Observed (page text); I did not check the advert |
| Intended users | The project author and stakeholders deciding what to build next or how to present the project against a role; possibly an applicant or adviser preparing a case | Inferred |
| Nature | Analysis and planning document, rendered as an interactive page | Observed (structure) / Inferred |

**Note on the subject matter.** The page analyses a public job advert, not internal operational data. The advert's content is what the advert says; whether the role works that way in practice is not evidenced.

## 2. Interface and architecture

### 2.1 Components (page text)

1. **Header and introduction:** "Each requirement in the Harri job advert ... set against what SegStudio and menu-review.html do today."
2. **Filters:** a status filter with the values **Any status, Not yet (either system), Covered, Partial, Not yet, A person, not software**; and a system filter labelled **Both / SegStudio / menu-review** (the exact control type is not clear from the text).
3. **Actions:** **Expand all** and **Copy as Markdown**.
4. **Table columns:** Requirement (from the PDF), SegStudio, menu-review.html.
5. **Three note sections:**
   - "Correction to the earlier notes"
   - "In the PDF but not in the .md copy"
   - "Not covered by Plan A–E either"
6. **Method statement:** "How this was assessed".
7. **Shared navigation** to the six pages of the tool set.

### 2.2 Architecture signals

- A client-side page with a table of requirements, presumably filled at run time. The rows did not appear in my retrieval.
- **Copy as Markdown** suggests the content is exportable to documents or notes (Inferred).
- No login, edit or save function is visible.

## 3. Capability map

| # | Capability | What it does | Information used or produced | Status |
| --- | --- | --- | --- | --- |
| X1 | Requirement-by-requirement comparison | Lists each advert requirement and shows how far each of two systems addresses it | Advert requirements; coverage judgements for SegStudio and for menu-review.html | Observed (headings and description); rows not seen |
| X2 | Six-value status vocabulary | Classifies each requirement as Covered, Partial, Not yet, or **A person, not software**, plus the filters Any status and Not yet (either system) | Status per requirement per system | Observed (filter labels) |
| X3 | Human-work category | "A person, not software" marks requirements that are relationships or judgement rather than software functions | Subset of requirements | Observed (filter label); content not seen |
| X4 | System filter | Narrows the view to both systems, SegStudio, or menu-review | None | Observed (labels) |
| X5 | Expand all | Opens row detail, presumably reasoning or evidence per requirement | Detail text | Observed (label); content not seen |
| X6 | Copy as Markdown | Copies the table as markdown for reuse | Markdown text | Observed (label); not tested |
| X7 | Correction notes | Records a correction to earlier analysis | Text | Observed (page text) |
| X8 | Gap lists | Lists items in the advert that other documents miss, and items no plan covers | Text | Observed (page text) |
| X9 | Method disclosure | States how the assessment was made and what "covered" means | Text | Observed (page text) |

## 4. What the page states (reported as claims)

These statements are present in the page text. I have **not** verified them against the underlying documents or code.

**Correction to the earlier notes**

- None of the SegStudio documents mention **EPOS, nutrition or menu engineering**.
- Section 14 of `business-asset-intelligence.md` defers only WhatsApp, Drive/Dropbox, inbound email, social import, and auth, roles and approvals.
- So a one-slide map "should say EPOS is **not addressed**, not 'explicitly deferred'".

**In the PDF but not in the .md copy** of the advert:

- "Product information, training materials" in the role summary.
- "Test products before release".
- "Ensure all departments are informed on launch requirements and deadlines".
- "Launched in line with commercial objectives and brand standards".
- A strategic relationships paragraph and the full-lifecycle closing line.

**Not covered by Plan A–E either**

- Training materials for sites.
- Retail products (the advert says food, drink *and* retail).
- Supplier liaison data.
- Menu document history (the page says Plan A versions products, not the menu documents the advert names).

**How this was assessed (the page's own words, summarised)**

- From reading the uploaded SegStudio documents, the gap-closure plan, and the `menu-review.html` and `menu_review_server.py` code. **Nothing was run.**
- SegStudio ships with an empty `data/` folder, so "covered" means **documented in the repository, not populated with ICG data**.

## 5. Information architecture

### 5.1 Entities and relationships (Inferred)

- **Requirement** (from the advert) has a status for each **System** (SegStudio, menu-review.html).
- **System capability** (documented or coded) is the evidence for a status.
- **Plan** (Plans A–E) relates to systems: it describes planned closing of gaps.
- **Source document**: the advert in two forms, the PDF and a markdown copy, which differ.

### 5.2 Information characteristics

| Question | Finding |
| --- | --- |
| Live or static? | Static, a point-in-time analysis (advert captured 20/11/2026) |
| Source | A job advert PDF, SegStudio documentation, a gap-closure plan, and two code files, by the page's own account |
| Calculated or manual? | Manual judgement by the author. I see no evidence of automated comparison |
| Updating and storage | Not evidenced. Presumably edited in the page source |
| Validation | None shown. The page is candid that nothing was run |
| Sharing | By URL, and by copying as markdown |

### 5.3 Consequences when information changes

If the advert changes (it "closes 16 Dec 2026"), if SegStudio acquires a feature, or if menu-review.html changes, statuses on this page become stale unless someone updates them. Nothing shown ties a status to its evidence in a way that would flag that. A "Covered" status recorded when a feature was documented could be read later as "working".

## 6. Hospitality applications

The page does not serve a site or kitchen directly. Its relevance is to **those planning and presenting hospitality technology**.

- **Requirements traceability.** It links what an F&B coordination role is expected to do (product information, training materials, testing before release, informing departments of launch requirements, commercial and brand standards) to what the tools support. That is a way to check whether a system matches a role's real duties.
- **Honest scoping.** The "A person, not software" category acknowledges that parts of the role, such as relationships, are human work. That fits a human-centred approach: software does not claim to replace judgement.
- **Gap visibility.** It names areas not covered: training materials, retail, supplier liaison, menu document history, and EPOS, nutrition and menu engineering. These are the same areas a multi-site F&B function would need: supplier data, training and costing and margin.
- **Scale context.** The advert refers to 31 sites (the page's statement), which frames the coordination problem: consistency across many sites, with local variation.
- **Prioritisation.** The status filters let an author focus on "Not yet (either system)" items when deciding what to build next.

Not addressed: any site operational function (ordering, prep, allergens, stock) is outside this page's scope.

## 7. AI and automation opportunities (all Proposed)

No AI function is evidenced.

| Opportunity | Description | Human-workflow angle |
| --- | --- | --- |
| Requirement extraction | Parse a job advert or role description into discrete requirements, and flag differences between the PDF and its markdown copy, as the page does by hand | Removes copy-and-compare effort |
| Evidence-linked statuses | Link each status to its evidence (a document section, a code file, a test) and mark it stale when that evidence changes | Statuses stay trustworthy |
| Distinguish documented from working | Show separate columns for Documented, Implemented and Tested, with Populated for data | "Covered" cannot be misread as "works with ICG data" |
| Live capability register | Generate the coverage view from the tools themselves (what each page does, what data it holds) | The analysis updates as the tools change |
| Natural-language queries | "Which requirements are not met by either system?" or "What does the role need that no plan covers?" | Readers ask in their own words |
| Role-based maps for other roles | Build the same map for a head chef, a site manager or a general manager from their actual responsibilities | The tools are shaped around people's work, not the other way round |
| Backlog drafting | Turn the "Not yet" items into proposed work items with dependencies | Planning starts from a draft |

The principle that software should learn people is directly relevant: this page starts from a person's role and asks what the software must do, rather than starting from the software and asking people to adapt.

## 8. Limitations and dependencies

- **Evidence limit.** Requirement rows and statuses were not visible, so I cannot report which items are Covered, Partial or Not yet. The notes sections were visible.
- **Self-reported and unrun.** By its own statement, nothing was run, and "covered" means documented, not populated. Statuses are therefore claims about documentation. A reader needs to see that distinction every time they use the word "Covered".
- **Dependency on documents I cannot see.** SegStudio, `business-asset-intelligence.md`, Plans A–E, the gap-closure plan and the advert PDF are not accessible to me. The page is my only evidence about them.
- **Point-in-time.** Captured 20 November 2026; the advert closes 16 December 2026.
- **Naming inconsistency.** The page refers to `menu-review.html`; the deployed route is `/menu-review`. The page's author read the code of a local file, not necessarily the deployed page. The Discovered media page describes a local server (`menu_review_server.py`) that the public deployment cannot provide.
- **Reference to external notes.** "Correction to the earlier notes" and "the one-slide map" refer to material I cannot see, so the correction cannot be placed in context.
- **Scope drift against the other pages.** The cross-check says SegStudio documents do not mention nutrition or EPOS, yet the Product data mock-up has nutrition and codes, and the Launch readiness mock-up names POS items as a source. Either these mock-ups go beyond the documented plan, or the plan has moved on. That is not resolved on the page.
- **Public advert.** The advert is public information; it does not show how the role works in practice.

## 9. Ecosystem contribution

What this component contributes: **a requirements-to-capability map, with candid statements of what is documented, what is missing and what is human work.** It makes available a clear list of gaps and corrections, and it serves whoever decides what the tool set should do next.

How it could fit a larger system (Proposed):

- **As the roadmap layer.** Each "Not yet" requirement points to a component that could be built: supplier data, training materials, retail products, EPOS, nutrition, costing.
- **As a bridge between the mock-ups and the roles.** Launch readiness, Product data and the recipe page each cover parts of the advert (testing before release, informing departments, product information, training). The cross-check could show which requirement each one supports.
- **As a truth-in-labelling tool.** Its distinction between documented and populated is the discipline the whole tool set needs, since several pages carry no label of their own.
- **Extended beyond one role.** The same method applied to site managers and chefs would test whether the tools match how those people work.

## 10. Further investigation

1. A screenshot or text export of the requirements table, with statuses and expanded rows (use Expand all, and Copy as Markdown), so that I can report requirement by requirement.
2. The SegStudio documents referred to: `business-asset-intelligence.md` (section 14), the gap-closure plan and Plans A–E.
3. The advert PDF and its markdown copy, to verify the listed differences.
4. What each status means precisely, and what counts as evidence for Covered versus Partial.
5. How the system filter works.
6. Whether the page is regenerated from a data file or maintained by hand.
7. Whether any requirement has been tested against a running system.
8. How the Product data and Launch readiness mock-ups map to the advert's requirements.
9. What SegStudio is, in operational terms, and how it relates to the tools on this site.
10. Who the page is for, and whether it is public by intention.

## 11. Summary judgement

- **Evidenced (page text):** a cross-check page with a status vocabulary that includes "A person, not software", three notes (a correction, items in the PDF but not the markdown copy, and gaps no plan covers) and a candid method statement.
- **Not evidenced:** the individual requirement statuses, any running functionality in SegStudio or menu-review.html, any populated ICG data, any automation or AI.
- **Value:** a useful and honest planning document. It is analysis, not an operational tool, and its worth depends on keeping statuses tied to evidence.
