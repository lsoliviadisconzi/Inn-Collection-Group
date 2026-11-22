# Hospitality Technology Capability Assessment: Chicken Liver Parfait Product Page (The Lindisfarne Inn)

**Service:** Chicken Liver Parfait · The Lindisfarne Inn (product journey page) **URL:** https://inn-collection-group.netlify.app/recipes/chicken-liver-parfait-the-lindisfarne-inn.html **Assessment date:** 22 November 2026

## 0. Evidence basis (read first)

I retrieved the page as text. I could **not** hover over or click any card, open any stage, see the images beyond their captions, or read the page's JavaScript, CSS or data. The text contains headings, five stage-card labels, a central product caption and a closing heading. **None of the detail behind the five stage cards was visible to me.**

Evidence classes used:

- **Observed (strict, by interaction): none.**
- **Observed (page text):** something present in the retrieved text. It records what the page shows, not that anything works.
- **Code-verified: none.**
- **Inferred:** suggested by labels, unverified.
- **Proposed:** a possible future capability.

**Data status.** The retrieved text does not label its figures as sample or real. A single product with a clean cost (£2.10), weight (280 g) and calorie value (462 kcal) is the kind of figure that may be illustrative in a demonstration page. I have no evidence that these come from a recipe costing system, a supplier price list or a nutritional analysis. Treat every figure as **unverified** until its source is shown.

## 1. Service identification

| Item | Finding | Status |
| --- | --- | --- |
| Name | Chicken Liver Parfait · The Lindisfarne Inn | Observed (page text) |
| Type | A single-product page that presents the information chain around one dish, from ingredients to guest | Observed (headings) / Inferred (purpose) |
| Subject | Chicken liver parfait with red onion chutney, seeded toast and leaves on a speckled plate (from the image caption) | Observed (page text) |
| Venue | The Lindisfarne Inn | Observed (page text) |
| Headline figures | 280 g plated · £2.10 cost · 462 kcal | Observed (page text); source unknown |
| Intended users | Central F&B and product staff, site managers and chefs, and training or onboarding audiences. A decision-maker looking for a worked example of connected product information is another plausible reader | Inferred |
| Nature | A demonstration or explainer of how one product's information could be connected. Not shown to be a live operational tool | Inferred |

## 2. Interface and architecture

### 2.1 Page structure (page text)

The page is organised in three bands, each with a numbered heading:

1. **"1. From ingredients to guest"**: a venue label (**The Lindisfarne Inn**), an instruction "Hover to preview · click to open" (and "Tap a card to open" for touch), and **five cards**:
   1. Ingredients — *Recipe*
   2. Suppliers — *Suppliers*
   3. Ordering & Delivery — *Weekly order*
   4. Preparation — *Plate standard*
   5. The Guest Experience — *What the guest is told*
2. **"2. One product. Connected information."**: the central dish image and caption: **Chicken Liver Parfait, 280 g plated · £2.10 cost · 462 kcal.**
3. **"3. Learn. Adapt. Improve."** with the label **"A Smarter Operation"**, which appears to introduce a feedback loop.

### 2.2 Interaction model

Cards are previewed on hover and opened on click or tap (Observed, page text as instruction). What a card opens is not visible to me (unknown).

### 2.3 Architecture signals

- A **static HTML file** under a `/recipes/` path on the same Netlify site as the other tools. The path suggests a family of recipe pages, but I found none listed, and no index page.
- **Not linked from the shared navigation** used by Menu review, Discovered media, F&B role cross-check, Launch readiness, Product data and Menu explorer. That navigation does not include recipes (Observed from those pages' text). The recipe page appears to stand apart from the tool set.
- No visible login, save, edit or data-entry feature in the page text.

## 3. Capability map

| # | Element | What it presents | Information it likely carries | Who it would help | Status |
| --- | --- | --- | --- | --- | --- |
| R1 | **Ingredients → Recipe** card | The recipe for the product | Ingredients, quantities, method (unseen) | Chefs, central F&B, training | Observed (label); content Inferred |
| R2 | **Suppliers** card | Where the ingredients come from | Supplier names, products or specifications (unseen) | Central buying, chefs | Observed (label); content Inferred |
| R3 | **Ordering & Delivery → Weekly order** card | How the product's ingredients are ordered and delivered | Order pattern, cut-offs, delivery days (unseen) | Site managers, head chefs, buyers | Observed (label); content Inferred |
| R4 | **Preparation → Plate standard** card | How the dish is prepared and presented | Preparation method and presentation standard, probably with an image or spec (unseen) | Kitchen team, trainers, site managers | Observed (label); content Inferred |
| R5 | **The Guest Experience → What the guest is told** card | What the guest sees or hears about the dish | Menu description, allergen information, possibly front-of-house talking points (unseen) | Front-of-house, managers, compliance | Observed (label); content Inferred |
| R6 | **Central product summary** | One dish tied to weight, cost and calories | 280 g, £2.10, 462 kcal | All of the above | Observed (page text); sources unknown |
| R7 | **"Learn. Adapt. Improve." / "A Smarter Operation"** | A loop that suggests information flows back from operation to the product record | Unknown | Central teams, managers | Observed (label); meaning Inferred |
| R8 | **Hover preview / click-to-open** | The interaction pattern for the five cards | None | Any viewer | Observed (instruction text); behaviour not tested |

**What the page shows by structure:** the five cards describe the journey of one product through recipe, supply, ordering, preparation and guest communication. The page's headline claim, "One product. Connected information.", is a design statement. I have no evidence that the five cards are connected by anything other than layout.

## 4. Observed workflows

No workflow was run. The intended reading journey from the page text (Inferred):

1. A viewer sees the five stages from ingredients to guest.
2. They hover over a card to preview it, or click it to open the detail.
3. They see the central product with its weight, cost and calorie figures.
4. They read the closing "Learn. Adapt. Improve." message.

The operational journey the page represents is that of the product itself: an ingredient is specified, bought, delivered, prepared, plated and described to a guest. The page appears to be a presentation of that journey, not a tool to carry it out.

## 5. Information architecture

### 5.1 Entities and relationships (Inferred)

- **Product (dish)** is the hub: Chicken Liver Parfait with red onion chutney, seeded toast and leaves.
- **Recipe** belongs to the product, with **Ingredients** and quantities.
- **Ingredient** is supplied by a **Supplier** and is bought through an **Order** with a **Delivery** schedule.
- **Preparation standard (plate standard)** belongs to the product and venue.
- **Guest-facing information** (description, allergens) is derived from, or should be consistent with, the recipe.
- **Venue** (The Lindisfarne Inn) is the context for ordering, preparation and guest information.

These relationships are what the page's headline implies. Which of them are implemented, as opposed to shown, is unknown.

### 5.2 Information characteristics

| Question | Finding |
| --- | --- |
| Live, static, calculated? | A static page. Whether the cost and calorie figures are calculated from recipe data or typed in is unknown |
| Source of cost | Unknown. A £2.10 portion cost would normally need ingredient prices, pack sizes and recipe quantities. None is shown in the text |
| Source of calories | Unknown. 462 kcal would normally need a nutritional analysis of the recipe |
| Updating and storage | Not evidenced |
| Validation | Not evidenced |
| Sharing | Via the URL |
| Gaps in the text | No selling price, gross profit, allergen statement, shelf life or sales information appears in the retrieved text. They may sit behind the cards |

### 5.3 Consequences when information changes

If the page's idea were implemented as connected data, a change of supplier price would change portion cost; a change of ingredient would change allergens, calories and what the guest is told; a change of delivery day would change the weekly order. In the page as retrieved, nothing shows these effects, and any change to one figure would have to be made by hand in each place.

## 6. Hospitality applications

The value is as a **worked example of connected product information**. The examples below depend on the real data behind the cards.

- **Recipes and specifications.** One product page that holds the recipe, plate standard and guest wording lets a central team and a site chef check they are working from the same dish.
- **Suppliers and procurement.** Putting supplier and weekly-order information on the product page shows a chef or buyer which products depend on which supplier, helpful when a supplier fails to deliver.
- **Costing.** A visible portion cost supports conversations about price and margin. Selling price and gross profit are not shown in the text, so margin analysis is not evidenced.
- **Allergens and nutrition.** The Guest Experience card suggests allergen and description information is part of the same record. Nutrition is shown as a calorie figure only.
- **Training and knowledge.** The Plate standard card could serve as a training reference for new kitchen or front-of-house staff.
- **Central coordination with local execution.** The venue label implies the same dish could appear for other inns with local variations in supplier, ordering and plating. No second venue is shown.

Not evidenced: inventory and stocktake, sales performance, site-to-site comparison, staff communication.

## 7. AI and automation opportunities (all Proposed)

No AI function is evidenced.

| Opportunity | Description | Human-workflow angle |
| --- | --- | --- |
| Cost recalculation | Recompute portion cost automatically when a supplier price or pack size changes, and alert the chef or coordinator when it crosses a threshold | The team is told the effect of a change instead of searching for it |
| Allergen derivation with review | Suggest the allergen statement from the recipe ingredients and flag any mismatch with what the guest is told | A chef confirms; omissions are caught |
| Nutrition estimation | Estimate calories and key nutrients from recipe quantities, marked clearly as estimates unless analysed | Removes manual calculation |
| Order forecasting | Suggest the weekly order from sales trends, events and cut-off times | The buyer reviews a draft rather than starting from scratch |
| Supplier-failure impact | When an ingredient is unavailable, show which products and venues are affected and propose substitutes for chef approval | A decision is supported, not made |
| Plain-language questions | "What goes in the parfait and who supplies the liver?" answered from the record with the source cited | Staff ask in their own words |
| Training prompts | Turn the plate standard into a short briefing for new starters or for a menu launch | Training is delivered to people, in context |
| Learning loop | Use waste, guest feedback and sales to suggest recipe, portion or ordering changes (the page's "Learn. Adapt. Improve.") | Suggestions go to the chef for decision |

Guardrail: allergen, nutrition and cost figures drive safety and commercial decisions. Automated values need a source, a date and a named person who confirms them.

## 8. Limitations and dependencies

- **Evidence limit.** Only five card labels and a few figures were visible. The detail behind every card is untested.
- **Unverified data.** No source is given for £2.10, 280 g or 462 kcal. A page that presents one product cleanly may be an illustration, not an extract from live data.
- **Connection is asserted, not shown.** "Connected information" is a heading. I could not see any link between the cards other than their shared layout.
- **Single product, single venue.** Nothing demonstrates scale across a group or variation between sites.
- **Isolation.** The page is not in the navigation of the other tools, and I found no link from this page to them. Relationships to Menu review, Product data or Menu explorer are not evidenced.
- **Relationship to Product data.** The Product data mock-up proposes one record per product with allergens, nutrition, recipe, price and codes. This page shows a similar idea as a narrative. Whether one is meant to feed the other is unknown.
- **Planned scope.** The F&B role cross-check page reports that the documents it reviewed do not cover retail, supplier liaison data or training materials. This page touches suppliers and training, so it appears to go beyond those documents (that page's own claim, not verified by me).
- **Interaction dependence.** Detail is behind hover and click. A reader on a printed or text-only copy sees only the labels.

## 9. Ecosystem contribution

What this component contributes: **a clear, human-readable picture of what "connected product information" would look like for one dish,** from recipe to guest. It makes available the idea and the shape of the information, and, if the cards hold real content, the recipe, supplier, ordering, plate-standard and guest-wording details for this product.

How it could fit a larger system (Proposed):

- **As the product view of a master record.** Product data would hold the verified fields; a page like this would be the readable view for chefs, trainers and managers.
- **Fed by reviewed menu data.** The dish name, description and price could come from Menu review and Menu explorer, so the guest wording is consistent.
- **Linked to procurement and EPOS.** Supplier and weekly-order cards would draw on supplier and ordering data, and sales would feed the learning loop. None of these connections is evidenced.
- **Replicated per venue.** The same template, filled with each site's local supplier and plating, would show where sites legitimately differ.
- **Human-centred direction.** Chefs and managers keep working as they do; the system gathers, checks and presents. Employees see the information in the form they already recognise: a dish, a spec, an order, a plate.

## 10. Further investigation

1. A screenshot or text export of each of the five cards when opened, and of the closing "A Smarter Operation" section, to replace the Inferred entries with observed ones.
2. The source and date of the figures: portion cost (£2.10), plated weight (280 g) and calories (462 kcal). Are they real, calculated, or illustrative?
3. Whether other recipe pages exist under `/recipes/`, and whether they share a template or data source.
4. The page source, to see whether the content is hard-coded or loaded from a data file, and whether anything is calculated.
5. Whether the allergen statement and guest wording match the recipe.
6. Whether the supplier, ordering and delivery details are real and who maintains them.
7. Whether selling price, gross profit, shelf life, stocktake and sales data exist behind the cards.
8. How the page relates to Product data, Menu explorer and Launch readiness.
9. Whether the page is meant for internal use, training, or presentation to stakeholders, and who can access the URL.

## 11. Summary judgement

- **Evidenced (page text):** a one-product page with a five-stage journey (recipe, suppliers, weekly order, plate standard, guest information), three headline figures and a closing "Learn. Adapt. Improve." section.
- **Not evidenced:** the content of any stage, the source of any figure, any calculation or connection between stages, any integration, persistence or AI.
- **Value:** an effective statement of the idea. Whether it is also a working capability depends on what is behind the cards and where the figures come from.
