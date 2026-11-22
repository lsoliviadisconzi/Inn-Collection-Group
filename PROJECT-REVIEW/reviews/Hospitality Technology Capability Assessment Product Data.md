# Hospitality Technology Capability Assessment: Product Data

**Service:** Product data — Inn Collection Group **URL:** https://inn-collection-group.netlify.app/product-data **Assessment date:** 22 November 2026

## 0. Evidence basis (read first)

I retrieved this page, and the sibling pages linked from its navigation, as text. I could **not** click, filter, open a record, switch views, or read the page's JavaScript. The retrieved text contained a heading, a short description, filter and tab labels, and a closing note. No product records were visible in it.

The page describes itself in words, and that matters more than anything else in this assessment:

> "Sample data · front-end skin only" and "All products, figures and checks are invented to show the layout. In the real build the allergen state, nutrition and prices would be fields on a product record, and every check below would run on save."

So this page is, by its own declaration, a **layout demonstration**. It is not a working product database.

How I use the evidence classes:

- **Observed (strict, by interaction): none.**
- **Observed (page text):** something the page states in words. It records the page's claim, not tested behaviour.
- **Code-verified: none.** No source or documentation was available to me.
- **Inferred:** suggested by labels, unverified.
- **Proposed:** intended or possible future capability. Because the page says its checks "would run on save" in a real build, most of what it describes sits here.

## 1. Service identification

| Item | Finding | Status |
| --- | --- | --- |
| Name | Product data, within the Inn Collection Group tool set | Observed (page text) |
| Stated purpose | "One record per product: allergens, nutrition, recipe, price and codes, each with its own accuracy check" | Observed (page text) |
| Nature | Mock-up of a product-record interface using invented data | Observed (page text) |
| Intended users | A central F&B, product-data or compliance role; site managers and chefs as possible readers | Inferred |
| Place in the tool set | Downstream of menu collection and review (Discovered media, Menu review) and alongside Menu explorer and Launch readiness | Inferred from shared navigation |

## 2. Interface and architecture

### 2.1 Visible components

1. Title with the badge "Sample data · front-end skin only".
2. One-sentence description of the product record (above).
3. Shared navigation to Menu review, Discovered media, F&B role cross-check, Launch readiness, Product data and Menu explorer.
4. A **record-state filter**: Any record state, Has blocking issues, Warnings only, Clean.
5. Two views: **Products** and **Allergen matrix**.
6. A closing note saying all products, figures and checks are invented.

The retrieved text did not include a product list, record detail, matrix cells or check results, so I cannot describe them. They may exist in the rendered page.

### 2.2 Architecture signals

- A front-end only: the page says "front-end skin only", meaning no back end is evidenced for it.
- No login, roles, audit trail or save function is visible.
- The "would run on save" wording shows the intended design is a **validated save**: a record cannot be saved clean until its checks pass or are reviewed. That is intention, not behaviour.

## 3. Capability map

| # | Capability | What it would do | Information used or produced | Status |
| --- | --- | --- | --- | --- |
| P1 | Single product record | One record per product holding allergens, nutrition, recipe, price and codes | Product entity with five attribute groups | Observed (page text) as a stated design; working behaviour not evidenced; Proposed |
| P2 | Per-field accuracy checks | Each attribute group has its own check, run on save | Check results per field (blocking, warning, clean) | Observed (page text) as a statement of intent; Proposed |
| P3 | Record-state filter | Narrow products to those with blocking issues, warnings only or clean | Aggregate state of each record | Inferred from labels; operates on invented data |
| P4 | Products view | A list or table of product records | Invented data | Inferred |
| P5 | Allergen matrix view | A product-by-allergen grid | Allergen state per product | Inferred. The Menu explorer page has a separate "Allergen matrix" tab, so the two could duplicate or complement each other |
| P6 | Allergen state, nutrition and prices as record fields | Replaces data scattered across documents with structured fields | Structured product data | Observed (page text) as plan; Proposed |
| P7 | Codes | An unspecified set of identifiers on each product | Unknown. They could be internal, supplier or point-of-sale codes; the page does not say which | Observed (word only); meaning Unknown |

Nothing on this page is a working, evidenced capability. The value of the page is as a specification of intent.

## 4. Observed workflows

No workflow was executed. The intended journey, as described by the page's own wording (Proposed):

1. A product record is created or edited with allergens, nutrition, recipe, price and codes.
2. On save, each field group's accuracy check runs.
3. The record gets a state: Has blocking issues, Warnings only, or Clean.
4. A reviewer filters to blocking issues first and resolves them.
5. The allergen matrix gives a cross-product view, for example to see which dishes contain a given allergen.

How checks are defined, who resolves a warning, and whether a blocking issue prevents publication are not stated.

## 5. Information architecture

### 5.1 Entities and relationships

- **Product** is the central entity (Observed, page text). Its stated attributes are allergens, nutrition, recipe, price and codes.
- **Recipe** is a child of a product in the description. How it connects to ingredients, suppliers or portion sizes is not stated (Unknown).
- **Allergen state** is a field on the product. The page does not say whether it is derived from ingredients or entered by hand, which is the key design question for safety.
- **Check** is a rule per attribute group producing blocking or warning results (Inferred).
- **Menu line** would relate to a product, since the surrounding pages work on menus. The link is not shown on this page (Inferred).

### 5.2 Information characteristics

| Question | Finding |
| --- | --- |
| Live, static, imported, calculated? | Invented static sample data. In the "real build", fields on a record, with checks calculated on save (Proposed) |
| Sources | Not stated. Menu text from Menu review is a plausible upstream source for names and prices; recipes and nutrition would need other sources (Inferred) |
| Updating and storage | Not evidenced. The page says nothing about where records live |
| Validation | Per-field checks on save (Proposed) |
| Sharing | Not evidenced |

### 5.3 Operational consequences when information changes

If one field changes, other things should follow. Examples a real build would need to handle:

- A changed ingredient should change the allergen state and nutrition values, and the recipe version.
- A price change affects the menu line and any gross-profit view.
- A changed allergen state must reach every menu and guest view that shows the product, and may require a reprint.

None of this propagation is shown. These are design questions, not findings.

## 6. Hospitality applications

The relevance depends on the real build existing; the examples below are Proposed.

- **Allergens and compliance.** A single record where allergen status is checked, rather than spread across menu PDFs, would give a central team and each site's chef a common answer for a guest query.
- **Recipes and specifications.** A recipe held on the product record lets a head chef and the central team see whether sites are cooking the same dish, and where local variation is deliberate.
- **Pricing and costing.** Price on the record is a precondition for comparing price across sites. Cost data is not mentioned on the page, so margin analysis would need more fields (Proposed).
- **Nutrition.** Stated as a record field. The F&B role cross-check page says the SegStudio documents it reviewed do not mention nutrition, EPOS or menu engineering, which suggests this page goes beyond what those documents plan (self-reported there; I did not verify).
- **Central coordination versus site execution.** A shared record allows sites to see the master data while flagging a local change for approval; no such workflow is shown.

Not addressed: suppliers, procurement, inventory, training and staff communication. The cross-check page lists supplier liaison data and training materials as gaps.

## 7. AI and automation opportunities (all Proposed)

No AI function is evidenced on this page.

| Opportunity | Description | Human-workflow angle |
| --- | --- | --- |
| Populate records from existing material | Extract product name, description, price and allergen declarations from reviewed menu text to pre-fill records | Staff confirm rather than type |
| Ingredient-to-allergen inference with review | Suggest allergen state from a recipe's ingredients and flag disagreement with the declared state | A chef verifies; the system catches omissions |
| Consistency checks across sites | Compare the same dish across venues and flag differences in price, allergens or description | Central coordinator sees outliers without asking each site |
| Change impact alerts | When a field changes, list affected menus and sites | A manager is told what needs reprinting or retraining |
| Natural-language questions | "Which starters contain sesame?" or "Show products with blocking issues in the north" | Asking in plain words, not learning filters |
| Delivery in existing channels | Send a chef a short message when a recipe allergen changes, with a one-tap confirmation | Fits existing habits; software learns people |
| Anomaly detection | Flag nutrition values or prices that are implausible for the product type | Early warning before publication |

Guardrail: allergen and nutrition data is safety-critical. AI suggestions must stay clearly marked as suggestions, keep their source, and require a named person's confirmation before being treated as verified.

## 8. Limitations and dependencies

- **Mock-up status.** The page says its data and checks are invented. It cannot be used to assess data quality, validation rules or performance.
- **Evidence limit.** Static text only; no interaction and no code.
- **Undefined data model.** Codes, the recipe structure, and the origin of allergen state are not specified.
- **Undefined checks.** "Accuracy check" is not defined: whether it tests format, range, cross-field consistency, or comparison to a source is unknown.
- **Authority of data.** Public menu text is not the same as verified recipe or specification data. A product record is only as reliable as the people and sources that fill it.
- **Duplicate allergen views.** This page and Menu explorer both have an allergen matrix. Which is authoritative is unknown (Inferred).
- **Date confusion risk.** The sibling Launch readiness page shows "as of 8 Feb 2027", a future date, in sample data. A reader could mistake invented context for real.
- **Inconsistency.** The page text says checks run "on save" while also being a "front-end skin only", so there is nothing to save to in the current build. That is consistent, but easy to overlook if only the filters are read.

## 9. Ecosystem contribution

What this component contributes now: **a specification of what a product record should hold and how it should be checked,** shown in the form a user would see. It makes no real product information available.

What it could contribute in a real build (Proposed):

- **Master record.** The product becomes the shared reference that menus, the allergen matrix, launch tracking and, with identifiers, recipes, suppliers and point-of-sale items link to.
- **Downstream of review.** Menu review would supply names, descriptions and prices; Product data would hold verified attributes.
- **Upstream of guest and site views.** Menu explorer and Launch readiness would read from records, as the Launch readiness page itself says its statuses should.
- **Human-centred direction.** Sites continue working as they do; the system pre-fills, checks and asks a named person to confirm only where it is unsure.

## 10. Further investigation

1. A rendered browser view of the page, to see what the Products and Allergen matrix views contain, without saving anything.
2. The page source, to see whether any back end, file or API is referenced.
3. A definition of each "accuracy check": inputs, rules, severity levels, and who resolves them.
4. What "codes" means: internal, supplier, EPOS or other.
5. How allergen state is determined: entered, inferred from recipe, or both, and what review applies.
6. Whether Product data and Menu explorer share one allergen source.
7. Where real product data would come from, who maintains it, and how often.
8. The planned relationship to menu lines, recipes, suppliers and point-of-sale items.
9. Governance: who is accountable for allergen accuracy, and how changes are approved and recorded.

## 11. Summary judgement

- **Evidenced (page text):** a self-declared sample-data layout for a one-record-per-product design, with a record-state filter and two views.
- **Not evidenced:** any real data, storage, validation, integration, or AI.
- **Value:** a clear statement of the target data model and the "check on save" principle. Its worth will be decided by whether real, accountable data can be put behind it.
