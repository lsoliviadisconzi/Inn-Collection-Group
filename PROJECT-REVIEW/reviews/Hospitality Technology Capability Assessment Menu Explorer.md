# Hospitality Technology Capability Assessment: Menu Explorer

**Service:** Menu explorer — Inn Collection Group **URL:** https://inn-collection-group.netlify.app/menu-explorer **Assessment date:** 22 November 2026

## 0. Evidence basis (read first)

Two sources were used: the page retrieved as text, and the screenshot you attached of the tab bar. I could **not** click any tab, apply any filter, open any record or read the page's JavaScript.

What that means for the tabs you flagged as important: **the screenshot shows only their names, and the retrieved text shows only their names plus two control labels.** No granular content (allergen values, venue data, counts, dishes) reached me from either source. Everything below about what the tabs contain is therefore Inferred from their names. To go deeper I would need a screenshot, or text export, of each tab's content (see section 10).

Evidence classes used:

- **Observed (strict, by interaction): none.**
- **Observed (page text / screenshot):** a label or statement present in the page text or image. It records what is shown, not that it works.
- **Code-verified: none.**
- **Inferred:** suggested by labels, unverified.
- **Proposed:** a possible future capability.

Unlike Launch readiness and Product data, this page carries **no** "sample data" declaration in the text I retrieved. That does not show the data is real. I cannot tell whether it is real, sample, or empty.

## 1. Service identification

| Item | Finding | Status |
| --- | --- | --- |
| Name | Menu explorer, within the Inn Collection Group tool set | Observed (page text) |
| Purpose | A read-oriented view of menu data across venues, with allergen analysis and venue comparison | Inferred from tab names |
| Intended users | Central F&B and compliance staff; possibly site managers and chefs; a "Guest view" implies a guest-facing perspective | Inferred |
| Place in the tool set | The reading and analysis end of the chain: Discovered media (collect) → Menu review (check) → Menu explorer (read, compare). The sequence is inferred from navigation and wording on sibling pages | Inferred |

## 2. Interface and architecture

### 2.1 Tabs (screenshot and page text)

The page text lists six tabs: **Menu, Guest view, Allergen matrix, Compare venues, Venue & menu data, Allergen reference.** The screenshot shows the last five, on a dark theme; "Menu" is not visible in the image (probably cropped to the left) but is in the page text.

Two further control labels appear in the page text with no context: **"may-contain counts"** and **"Free from"**. Their location (which tab) is unknown.

The shared navigation links to Menu review, Discovered media, F&B role cross-check, Launch readiness, Product data and Menu explorer.

### 2.2 Architecture signals

- A client-side, tabbed single page, with content filled at run time. The fetched text contained no data, so the source of the data is not evidenced here.
- No login, roles or save function is visible.
- The page uses the same navigation as its siblings, so it presumably reads from the same underlying menu dataset as Menu review, but no evidence shows this (Inferred).

## 3. Capability map (all Inferred unless stated)

| # | Tab or control | What it likely does | Information it would use or produce | What a hospitality user would do with it | Status |
| --- | --- | --- | --- | --- | --- |
| E1 | **Menu** | Browse menu content, probably by venue and menu type | Menu sections, dishes, descriptions, prices, allergen marks | Read what a venue is serving | Inferred |
| E2 | **Guest view** | Present a menu as a guest would see it, perhaps with allergen or dietary filtering | Dishes and dietary or allergen flags | Check what the guest-facing experience shows and how well it answers allergen questions | Inferred |
| E3 | **Allergen matrix** | A grid of dishes against allergens | Allergen status per dish | Answer "which dishes contain X"; spot dishes with no allergen information | Inferred |
| E4 | **may-contain counts** | Counts of dishes carrying a "may contain" (precautionary) statement, probably per allergen or venue | Aggregate counts from the matrix | See how heavily a venue or allergen is affected by cross-contamination wording | Inferred |
| E5 | **Free from** | Filter or summary of dishes free of selected allergens or ingredients | Dish-level allergen state | Find safe options for a guest with a stated allergy | Inferred |
| E6 | **Compare venues** | Side-by-side comparison of venues | Menu, price, allergen or dish differences between sites | Find where sites diverge, and whether that is deliberate | Inferred |
| E7 | **Venue & menu data** | A data view of the underlying venues and menu records | Venue and menu metadata; possibly the raw tabular data | Audit what the explorer is built from, check coverage | Inferred |
| E8 | **Allergen reference** | A reference list of allergens and their definitions or codes | Allergen list, possibly with symbols or notes | Standardise how allergens are named and coded across menus | Inferred |

I have not assumed what the allergen list is, how many allergens it holds, or how "may contain" is represented. Those are open questions.

## 4. Observed workflows

No workflow was run. The journeys the design suggests (Inferred):

1. **Guest-allergy query.** A manager opens Free from or the Allergen matrix, selects an allergen, and sees which dishes at a venue are free of it or carry a may-contain note.
2. **Venue comparison.** A central coordinator opens Compare venues to see how comparable dishes differ between sites in price, allergens or description.
3. **Data audit.** A reviewer opens Venue & menu data to see which venues and menus are present, and Allergen reference to confirm what each allergen mark means.
4. **Guest-experience check.** A marketer or manager opens Guest view to see what a guest would see.

## 5. Information architecture

### 5.1 Entities and relationships (Inferred)

- **Venue** has **Menus** (types Food, Drinks, Sunday, Events, Other per the Menu review filters).
- **Menu** has **Sections** and **Dishes**.
- **Dish** has allergen statuses (contains, may contain, free from) and probably a price.
- **Allergen** is a controlled list, described by the Allergen reference tab.
- **Comparison** is a derived view across venues.

### 5.2 Information characteristics

| Question | Finding |
| --- | --- |
| Live, static, calculated? | Counts, matrix and comparison are likely calculated from underlying records (Inferred). Whether the records are live is unknown |
| Source | Plausibly menu text reviewed in Menu review, but unproven. The Product data page describes allergen state as a field on a product record in a future build, so the current source of allergen data here is unclear |
| Allergen state | Unknown whether declared on the menu, extracted from text, entered by hand, or derived from recipes |
| Updating and storage | Not evidenced |
| Validation | Not evidenced |
| Sharing | Not evidenced |

### 5.3 Consequences when information changes

Because the matrix, counts, comparison and guest view are likely derived from the same records, a corrected allergen on one dish would change several views at once. That is useful if the change is checked and risky if it is not. It also means a wrong extraction in Menu review could propagate into the guest view. Whether any status shows how recent or how verified a value is, I cannot say.

## 6. Hospitality applications

These rely on the tabs behaving as their names suggest (Inferred).

- **Allergen and compliance.** The strongest relevance. A matrix and a free-from filter would give a central team and each site's management one place to answer allergen questions, instead of leafing through PDFs. Public menu text is not a verified specification, so this would assist rather than replace the chef's check.
- **Menu consistency across sites.** Compare venues would let a central coordinator see where a shared dish differs, and decide whether that is a legitimate local variation.
- **Pricing.** If prices are held, comparison supports price consistency checks. Cost and margin are not indicated.
- **Guest experience.** A Guest view lets management see the guest's perspective of the same data.
- **Management information.** may-contain counts are a simple indicator of where a venue's allergen wording is cautious or unclear.

Not addressed: suppliers, procurement, inventory, staff training and communication.

## 7. AI and automation opportunities (all Proposed)

No AI function is evidenced.

| Opportunity | Description | Human-workflow angle |
| --- | --- | --- |
| Natural-language allergen queries | "What can a guest with a nut allergy eat at this venue?" answered with dish names, source menu and a clear statement of how confident the data is | Staff ask in plain words; a chef verifies edge cases |
| Conversational guest assistant | The Guest view could answer questions in the guest's own words, with a hard rule to refer allergy-critical decisions to staff | Reduces repeated questions to the floor team |
| Inconsistency detection | Flag dishes whose allergens differ between sites, or whose names match but descriptions do not | The central team is shown differences, not asked to find them |
| Missing-data detection | Flag dishes with no allergen information and menus with unusually high may-contain counts | Directs review effort to where it matters |
| Cross-checking against recipes | Compare menu allergens with recipe ingredients once a recipe source exists | Catches omissions before guests do |
| Change alerts | When a menu or allergen changes, notify the affected site in a channel it already uses | Software goes to people |

Guardrail: allergen answers are safety-critical. Any assistant must cite the source, state the date and verification status, and defer to a named person when uncertain.

## 8. Limitations and dependencies

- **Evidence limit.** Tab names only; no tab content seen.
- **Unknown data status.** No label says whether the data is real, sample or empty.
- **Source of truth.** The Product data mock-up also has an "Allergen matrix" and treats allergen state as a product-record field. If Menu explorer derives allergens from menu text, the two could disagree. Which is authoritative is not defined.
- **Public versus verified data.** Menu text is a public document, not a verified internal record.
- **Undefined allergen handling.** How "contains", "may contain" and "free from" are determined and tracked is not evidenced.
- **Dependency on upstream quality.** Menu explorer is only as accurate as the extraction and review behind it.
- **No access control evident.** Whether a guest-facing view is separate from internal views is unknown.

## 9. Ecosystem contribution

What this component would contribute: **a read-and-compare layer that turns reviewed menu data into allergen and venue insight.** It would serve central F&B and compliance staff most directly, and site managers and guests through the Guest view.

How it could fit a larger system (Proposed):

- **Downstream of Menu review**, taking only reviewed data and showing review status on each dish.
- **Fed by Product data** once product records carry verified allergens, so the matrix reads one source rather than two.
- **Linked to Launch readiness**, so a menu launch cannot be marked ready while allergen gaps remain.
- **Reached through existing channels** such as messaging or email for site teams, rather than asking them to learn another screen.

## 10. Further investigation

The most valuable evidence, given your note that the tabs hold important detail:

1. A screenshot or text export of **each tab** (Menu, Guest view, Allergen matrix, Compare venues, Venue & menu data, Allergen reference), including the may-contain counts and Free from controls. With that I can replace most Inferred entries with Observed (screenshot) ones.
2. The allergen list and how it is coded.
3. How "may contain" and "free from" are produced.
4. Whether the data shown is real, sample, or partial, and how many venues and menus it covers.
5. Where the data is loaded from and how often it changes.
6. Whether review status from Menu review is visible on dishes.
7. How Allergen matrix here relates to Allergen matrix in Product data.
8. Whether the Guest view is intended for public use, and what safeguards apply.
9. The page source, to verify any calculations, filters and data loading.

## 11. Summary judgement

- **Evidenced:** six tab names and two control labels, in the page text and screenshot.
- **Not evidenced:** every tab's content, any data, calculation, persistence or integration.
- **Value:** the tab set describes a sensible allergen-and-comparison layer. The assessment cannot go further without seeing what each tab contains.
