# Hospitality Technology Capability Assessment: Launch Readiness

**Service:** Launch readiness — Inn Collection Group **URL:** https://inn-collection-group.netlify.app/launch-readiness **Assessment date:** 22 November 2026

## 0. Evidence basis (read first)

I retrieved the page as text. I could **not** click a workstream, view a checklist, see the timeline or site grid drawn, or read the page's code. The retrieved text contains headings, short descriptions and a closing note. It contains no milestone names, workstream names, checklist items, site names or status counts.

The page declares its own nature in words, twice:

- Next to the title: **"Sample data · front-end skin only"**.
- In the closing note: "Everything here is invented to show the layout. In the real build each checklist item would link to its source record (menu, recipe, product, POS item) and statuses would come from those records, not be set by hand."

So this page is, by its own declaration, a **layout demonstration with invented data**. It is not a working launch-tracking tool. The assessment therefore describes a *design intent*, and nearly all capabilities are Proposed.

Evidence classes used:

- **Observed (strict, by interaction): none.**
- **Observed (page text):** present in the retrieved text. It records what the page says, not that anything works.
- **Code-verified: none.**
- **Inferred:** suggested by labels, unverified.
- **Proposed:** intended or possible future capability. The page's own wording places its real functionality here.

## 1. Service identification

| Item | Finding | Status |
| --- | --- | --- |
| Name | Launch readiness, within the Inn Collection Group tool set | Observed (page text) |
| Scenario shown | "Spring menu 2027 · launch 1 Mar 2027", "Shown as of 8 Feb 2027" | Observed (page text); invented |
| Purpose | Show how readiness for a menu launch across sites could be tracked: milestones, workstreams with completion rules, and per-site status | Inferred from headings |
| Intended users | A central F&B coordinator or launch lead; site managers and head chefs reading their own site's position; senior management reading overall readiness | Inferred |
| Nature | Mock-up with invented data | Observed (page text) |

## 2. Interface and architecture

### 2.1 Components (page text)

1. **Header:** title, the badge "Sample data · front-end skin only", the scenario line (Spring menu 2027 · launch 1 Mar 2027) and the line "Shown as of 8 Feb 2027".
2. **Timeline:** "four milestones, today marked". A line of four milestones with a marker for the current date.
3. **Workstreams:** "select one for its checklist and the rule for calling it complete". A set of workstreams; selecting one shows a checklist and the criterion for completion.
4. **Site readiness:** a section showing readiness per site, with a five-value status legend: **Done, In progress, At risk, Blocked, Not started.**
5. **Shared navigation** to Menu review, Discovered media, F&B role cross-check, Launch readiness, Product data and Menu explorer.
6. **Closing note** (above).

The names of the milestones, workstreams and sites did not appear in the retrieved text.

### 2.2 Architecture signals

- A **front-end only** page. No back end, data source or save function is evidenced.
- The "as of 8 Feb 2027" date is **fixed**. It is a future date relative to today (22 November 2026), consistent with an invented snapshot, not a live clock.
- The note says statuses "would come from those records", which describes a future design: statuses derived from source records instead of being set by hand.

## 3. Capability map

| # | Capability | What it would do | Information used or produced | Status |
| --- | --- | --- | --- | --- |
| L1 | Launch definition | Name a launch and give it a date (Spring menu 2027, 1 Mar 2027) | Launch record: name, date | Observed (page text) as an example; invented |
| L2 | Milestone timeline | Four milestones with today marked | Milestone dates; the current date | Observed (heading); content not seen; Proposed as a working feature |
| L3 | Workstreams with checklists | Break a launch into streams, each with a checklist | Workstream names, checklist items | Observed (heading); content not seen; Proposed |
| L4 | **Rule for calling a workstream complete** | Each workstream carries an explicit completion criterion, shown with its checklist | A "definition of done" per workstream | Observed (heading wording); Proposed. The most significant design idea on the page, because it replaces opinion with a stated rule |
| L5 | Site readiness grid | Readiness per site with five statuses | Status per site (and presumably per workstream) | Observed (legend); content not seen; Proposed |
| L6 | Status from source records | Each checklist item links to its source record (menu, recipe, product, POS item), and status is computed, not typed | Links to menu, recipe, product and POS records; computed statuses | **Stated intention only** (page text); Proposed. Requires integration that is not evidenced |
| L7 | Cross-navigation | Links to the other tools | None | Observed (page text) |

Nothing on the page is evidenced as working. The value is in the design: milestones, completion rules, per-site status and computed progress.

## 4. Observed workflows

No workflow was run. The intended journeys, from the headings and note (Proposed):

1. **Central lead:** opens the page, checks the timeline against today's date, selects a workstream, reads its checklist and the rule for completion, and looks at which sites are At risk or Blocked.
2. **Site manager:** looks at the readiness of their own site and sees what remains before the launch date.
3. **Computed status:** when a menu is reviewed, a recipe signed off, a product record cleared or a POS item created, the linked checklist item turns Done without anyone ticking it.
4. **Escalation:** a Blocked or At risk status draws attention to a site or workstream before the launch date.

How a status is overridden, who is notified, and how a blocked item is resolved are not stated.

## 5. Information architecture

### 5.1 Entities and relationships

- **Launch** (for example Spring menu 2027) has a date and **Milestones**.
- **Workstream** belongs to a launch and has a **Checklist** and a **Completion rule**.
- **Checklist item** links to a **source record**: menu, recipe, product or POS item (stated intention).
- **Site** has a readiness status, presumably per workstream (Inferred).
- **Status** is one of Done, In progress, At risk, Blocked, Not started.

### 5.2 Information characteristics

| Question | Finding |
| --- | --- |
| Live, static, calculated? | Static and invented today. In the proposed build, calculated from source records |
| Sources | None evidenced. Proposed sources: menu, recipe, product, POS item records |
| How status is set | Today, by hand or hard-coded (by implication of the note). Proposed: derived from records |
| Updating and storage | Not evidenced |
| Validation | Not evidenced. The completion rule would act as validation in a real build |
| Sharing | Not evidenced |

### 5.3 Consequences when information changes

In the proposed design, a change in a source record changes a status: a menu reverting to Needs review (Menu review), a product with blocking issues (Product data) or a missing POS item would turn a checklist item from Done to In progress or Blocked, and could move a site to At risk. That propagation is the value of the design and is exactly what is not shown. A hand-set status, by contrast, can go stale without anyone noticing.

## 6. Hospitality applications

The relevance is high if the real build is made, because a seasonal menu launch is a multi-department, multi-site coordination problem. These are Proposed.

- **Menu launch coordination.** One view of what must be ready by launch day, by site: reviewed menus, signed-off recipes, verified allergens, products in the POS, staff briefed.
- **Central control with local execution.** The central team sets the launch, milestones and completion rules; each site sees its own readiness and its blockers.
- **Compliance.** A completion rule such as "allergen state verified for every product on the menu" ties launch readiness to safety, not to a tick.
- **Management information.** A single readiness picture across sites, with At risk and Blocked highlighted, supports decisions on where to spend attention.
- **Reducing disconnected information.** Instead of asking each site by email whether it is ready, the status is read from the records the site already maintains.
- **Link to the F&B coordinator role.** The cross-check page reports that the job advert includes requirements such as testing products before release, informing all departments of launch requirements and deadlines, and launching in line with commercial objectives and brand standards. It describes those as present in the PDF but not in the markdown copy of the advert. This page is a plausible expression of those requirements (that page's own account, not verified by me).

Not addressed by the page as seen: suppliers and procurement, costing, staff training and communication, though each could be a workstream.

## 7. AI and automation opportunities (all Proposed)

No AI function is evidenced.

| Opportunity | Description | Human-workflow angle |
| --- | --- | --- |
| Computed readiness | Calculate checklist status from menu, recipe, product and POS records, as the page's own note proposes | Nobody has to tick boxes or chase for updates |
| Risk prediction | Flag sites likely to miss the launch from the pace of completion so far and the time left | A coordinator acts earlier |
| Draft launch plan | Generate milestones, workstreams and completion rules from a previous launch or from the new menu's contents | The coordinator edits a draft, not a blank page |
| Dependency detection | Identify that a new dish needs a new supplier item, allergen sign-off and a POS entry, and add them as checklist items | Nothing is forgotten |
| Summaries and nudges | Send each site manager a short message on what remains for their site, in the channel they already use | Software reaches the person |
| Plain-language questions | "Which sites are blocked on allergens?" answered from the records | Managers ask in their own words |
| Post-launch learning | Compare plan to outcome and suggest changes for the next launch | Improves the process over time |

Guardrail: a computed "Done" must be traceable to its source record and its reviewer. An automated status that looks green while a check is unverified would mislead.

## 8. Limitations and dependencies

- **Mock-up status.** Invented data. It cannot be used to judge real readiness, performance or usability.
- **Evidence limit.** Only headings, a legend and a note were visible. The timeline, workstreams, checklists and site grid were not seen.
- **Dependency on other components.** Computed status requires reliable menu, recipe, product and POS records. The Product data page is also a mock-up, and Menu explorer and Menu review show no data in my retrieval, so the source records the design depends on are not evidenced.
- **POS dependency.** The note names POS items as a source. The F&B role cross-check page says the SegStudio documents it reviewed do not address EPOS (its own claim). So the page's design refers to an integration the documented plans reportedly do not cover.
- **Definition quality.** Computed status is only as good as the completion rules. Poorly defined rules would produce misleading greens.
- **Fixed date.** "Shown as of 8 Feb 2027" is a future date. A reader could take the invented scenario as a real schedule.
- **Governance.** Who may override a status, who owns each workstream, and how a site disputes a status are not described.

## 9. Ecosystem contribution

What this component contributes now: **a clear picture of the coordination layer a connected hospitality system would need,** with milestones, completion rules and per-site status. It makes no real information available.

How it could fit a larger system (Proposed):

- **A consumer of every other component.** It reads Menu review (is the menu reviewed?), Product data (are allergens and prices verified?), recipes such as the Lindisfarne parfait page (is the spec signed off?), Menu explorer (is guest-facing information consistent?) and POS data (is the item live?).
- **The control tower, not a data store.** It holds launches, milestones and rules, and relies on links to hold the facts.
- **A route for communication.** Central teams, managers and sites share one status rather than separate email chains.
- **Human-centred direction.** Sites keep doing their normal work in the systems they use; readiness is read from the results, and people are asked only where something is Blocked or At risk.

## 10. Further investigation

1. A browser view or screenshots of the timeline, a selected workstream (checklist and completion rule) and the site grid, to see what is actually drawn.
2. The names and number of milestones, workstreams and sites in the mock-up, and whether the layout is modelled on a real previous launch.
3. How the completion rules are written, and who writes them.
4. The page source, to see whether any data file or back end is referenced.
5. Whether source records for menus, recipes, products and POS items exist, and with what identifiers, so that links are possible.
6. Whether the POS data is available to the project at all.
7. How statuses, overrides and notifications are meant to work.
8. Who the intended users are, and whether sites would see only their own readiness.
9. How the page relates to the existing Spring 2027 plans, if any.

## 11. Summary judgement

- **Evidenced (page text):** a self-declared sample-data layout with a timeline of four milestones, workstreams with completion rules, a five-status site readiness section, and a statement that real statuses would be computed from menu, recipe, product and POS records.
- **Not evidenced:** any real launch data, any computation, any link to a source record, any integration, persistence or AI.
- **Value:** a persuasive design for launch coordination. Its worth depends on the other components providing reliable records, and on well-defined completion rules.
