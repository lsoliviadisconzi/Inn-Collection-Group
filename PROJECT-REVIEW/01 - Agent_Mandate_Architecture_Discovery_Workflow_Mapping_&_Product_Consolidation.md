HOSPITALITY TECHNOLOGY WORKSPACE

Agent Mandate: Architecture Discovery, Workflow Mapping & Product Consolidation

Project: The Inn Collection Group — Hospitality Technology Capability Workspace
Phase: Architecture Discovery and Product Refinement
Primary objective: Understand, document and refine the existing collection of interfaces into a coherent, logically structured hospitality technology workspace.

⸻

1. YOUR ROLE

Act as a senior software architect, product systems analyst and hospitality technology specialist.

You have direct access to the complete project repository, including:

* Application source code.
* HTML, CSS and JavaScript.
* Backend scripts and services.
* Data structures and sample datasets.
* Configuration files.
* Existing documentation and specifications.
* Assets and supporting resources.
* The seven existing interfaces.
* Previous assessment reports supplied alongside these instructions.

Your responsibility is to examine the project as a whole, understand its architecture, identify how its components relate, and produce the documentation necessary to guide its next stage of development.

Do not approach this as a conventional code audit.

This is a product architecture and consolidation exercise.

The objective is not simply to describe what exists. It is to understand what the system is trying to become and how its existing components should evolve into a coherent working environment.

2. PROJECT CONTEXT

The project explores a technology workspace for coordinating Food & Beverage operations across a multi-site hospitality organisation.

Its operational context includes:

* Food and beverage product management.
* Menu administration.
* Recipe specifications.
* Ingredients and supplier information.
* Allergen and nutritional information.
* Product codes and EPOS preparation.
* Menu costing and pricing.
* Procurement and ordering.
* Site-level operational information.
* Menu launches and seasonal changes.
* Cross-site consistency.
* Commercial coordination.
* Operational reporting.
* Training and communication.

The intended users may include central F&B teams, site managers, chefs, operational coordinators and other relevant departments.

The system should support people in their existing operational responsibilities.

A fundamental design principle is:

Software should adapt to the way people work, rather than forcing people to adapt to the internal structure of software.

The workspace should make complex information accessible, connected and understandable without introducing unnecessary administrative complexity.

3. EXISTING INTERFACES

The current collection contains seven principal interfaces.

Inspect each independently before attempting to consolidate them.

3.1 Chicken Liver Parfait — Product Page

Route:
/recipes/chicken-liver-parfait-the-lindisfarne-inn.html

Investigate its product-centred presentation.

Areas of interest:

* Product identity.
* Recipe and ingredients.
* Suppliers.
* Ordering and delivery.
* Preparation.
* Plate standards.
* Guest-facing information.
* Nutritional and costing information.
* Connections between product information and operational execution.

Determine whether this is a standalone presentation, an example of a future product record, or an existing component of a wider system.

3.2 Discovered Media

Route:
/discovered-media

Investigate the document and media acquisition workflow.

Areas of interest:

* Menu PDFs.
* Other documents.
* Images and archives.
* Region and venue classification.
* Category and file-type filters.
* CSV ingestion.
* File selection.
* Export functionality.
* Local download mechanisms.
* Manifest generation.
* Connections with menu review.

Pay particular attention to the relationship between the hosted interface and the local Python server.

3.3 F&B Role Cross-check

Route:
/fnb-crosscheck

Investigate the relationship between operational requirements and software capabilities.

Areas of interest:

* Requirement identification.
* Capability comparison.
* Coverage classifications.
* Human responsibilities.
* Software responsibilities.
* Gap identification.
* Documentation references.
* Export or reporting functionality.

This interface should be understood as a requirements and capability analysis tool, not automatically as an operational module.

3.4 Launch Readiness

Route:
/launch-readiness

Investigate the proposed launch coordination model.

Areas of interest:

* Launch milestones.
* Workstreams.
* Checklists.
* Completion criteria.
* Site readiness.
* Dependencies.
* Risks and blockers.
* Central and site-level responsibilities.
* Connections to products, recipes, menus and EPOS records.

Determine what information this interface needs from other components.

3.5 Menu Explorer

Route:
/menu-explorer

Investigate the menu browsing and comparison experience.

Areas of interest:

* Menu browsing.
* Guest-facing menu presentation.
* Allergen matrix.
* May-contain information.
* Free-from filtering.
* Venue comparisons.
* Venue and menu data.
* Allergen reference information.

Pay particular attention to the distinction between menu information and authoritative product or recipe information.

3.6 Menu Review

Route:
/menu-review

Investigate the document review and quality-control workflow.

Areas of interest:

* Menu document selection.
* Region and venue filters.
* Menu categories.
* Review statuses.
* Original PDF display.
* Extracted Markdown.
* Source and rendered views.
* Duplicate detection.
* Corrections and intentional content.
* Review status management.
* Local server dependencies.
* Downstream data availability.

Determine whether this is an intermediate document-processing stage or whether it has responsibilities extending into product administration.

3.7 Product Data

Route:
/product-data

Investigate the proposed structured product information model.

Areas of interest:

* Product records.
* Recipe relationships.
* Allergen information.
* Nutritional information.
* Pricing.
* Product codes.
* Validation checks.
* Warnings and blocking issues.
* Allergen matrix.
* Record states.

Determine whether this should become the central product information layer of the workspace.

Do not assume that the current demonstration interface already implements this model.

4. FIRST TASK: INSPECT THE COMPLETE PROJECT

Before making architectural recommendations, inspect the repository.

Do not rely exclusively on the previous reports or the visible interfaces.

Establish:

1. Repository structure.
2. Application entry points.
3. Routes and navigation.
4. Frontend frameworks and libraries.
5. Backend services and scripts.
6. Data sources and storage mechanisms.
7. API endpoints.
8. Shared components.
9. Data schemas and entity definitions.
10. Dependencies between pages and services.
11. Existing documentation.
12. Development and deployment configuration.

Identify duplicated functionality, disconnected components, inconsistent terminology and abandoned or partially implemented functionality.

Inspect the implementation sufficiently to understand how each interface works.

Where relevant, examine the actual event handlers, data-loading functions, persistence mechanisms, API calls and backend processing.

Do not assume that a visible button works because it exists.

Do not assume that a function is integrated because its name suggests integration.

5. RECONCILE THE PREVIOUS ASSESSMENT REPORTS

Previous interface assessments have already been supplied.

Treat these reports as an initial research corpus.

Use them to guide your investigation, but independently verify their findings against the repository.

The reports establish several important preliminary observations:

* Discovered Media appears to represent an information acquisition stage.
* Menu Review appears to represent a document quality-control stage.
* Menu Explorer appears to represent an information exploration and comparison stage.
* Product Data appears to represent a structured product information model.
* Chicken Liver Parfait demonstrates a product-centred presentation.
* Launch Readiness represents a proposed coordination layer.
* F&B Role Cross-check represents a requirements and capability analysis layer.

These are preliminary architectural interpretations, not established integrations.

Investigate whether the components actually share data, identifiers, services or storage.

In particular, resolve the following questions:

A. Document and menu information

* Does Discovered Media feed Menu Review?
* How are discovered files identified?
* Where is extracted Markdown stored?
* Is review information persistent?
* Can a reviewed menu be traced back to its original PDF?
* Does Menu Explorer consume reviewed information?

B. Product information

* Is Product Data intended to be the authoritative product record?
* Does Chicken Liver Parfait represent a product record or a manually assembled page?
* How are recipes, products, ingredients and menu items related?
* Can a product appear on several menus or at several venues?
* Are allergens derived from ingredients, entered manually or imported?

C. Launch coordination

* Does Launch Readiness consume information from Product Data?
* How are menu, recipe and product completion criteria established?
* How are site-specific variations handled?
* Are EPOS items represented anywhere in the actual implementation?
* Are launch statuses calculated or manually assigned?

D. Requirements and capability analysis

* How does F&B Role Cross-check derive its requirements?
* Does it read repository documentation or maintain its own dataset?
* Can it identify missing capabilities automatically?
* How are documented capabilities distinguished from implemented ones?

Document the answers with references to the actual source files, functions, schemas and routes.

6. SECOND TASK: BUILD THE INFORMATION ARCHITECTURE

Develop a unified conceptual model for the workspace.

Do not start by deciding which pages should be combined.

Start by understanding the information.

Identify the principal entities and their relationships.

Investigate, at minimum, the following possible entities:

* Organisation
* Region
* Venue / Site
* Menu
* Menu Version
* Menu Section
* Menu Item
* Product
* Recipe
* Ingredient
* Supplier
* Purchase Specification
* Allergen
* Nutritional Profile
* Price
* Product Code
* EPOS Item
* Document / Media Asset
* Review
* Validation Check
* Launch
* Milestone
* Workstream
* Checklist
* Responsibility
* Operational Status

Do not assume that every entity needs to become a separate database table.

Establish which entities already exist in the code and which are conceptual requirements.

For each principal entity, document:

* Purpose.
* Important attributes.
* Relationships.
* Data ownership.
* Source of information.
* Whether it is currently implemented.
* Whether it is duplicated elsewhere.
* Potential downstream consumers.

Pay particular attention to the distinction between:

Product vs Menu Item

A product is not necessarily identical to the way it appears on a particular menu.

The same product may have different descriptions, prices, availability or approved variations across venues.

Recipe vs Product

A recipe describes preparation and composition. A product record may contain additional commercial, nutritional and administrative information.

Menu Document vs Menu Data

A PDF is a document. Extracted menu content is structured or semi-structured information. Neither should automatically be treated as a verified recipe or authoritative allergen record.

Allergen Reference vs Allergen Assessment

The list of regulated allergens is different from the verified allergen composition of an individual product.

7. THIRD TASK: MAP THE OPERATIONAL WORKFLOWS

Create workflow maps showing how information and responsibilities move through the proposed system.

Investigate these potential workflows:

Workflow A — Menu document intake

Discovery → Classification → File selection → Extraction → Review → Correction → Approval → Availability to downstream components.

Workflow B — Product administration

Product identification → Recipe association → Ingredient information → Supplier information → Allergen assessment → Nutrition → Pricing → Product validation → Publication.

Workflow C — Menu management

Menu creation or import → Menu structure → Product association → Venue assignment → Pricing and description → Review → Publication.

Workflow D — Menu and allergen exploration

Verified product information → Menu relationships → Allergen presentation → Guest-facing information → Staff reference.

Workflow E — Launch coordination

Launch planning → Product and menu preparation → Dependencies → EPOS preparation → Site readiness → Validation → Launch → Post-launch review.

Workflow F — Cross-site management

Central product information → Venue-specific configuration → Local variations → Comparison → Exceptions → Corrective action.

These are candidate workflows.

Verify which stages are already represented and identify missing stages.

For each workflow, identify:

* Starting event.
* Inputs.
* Processing stages.
* Responsible people or roles.
* Outputs.
* Dependencies.
* Required information.
* Potential automation.
* Failure points.
* Relevant interfaces.

Produce diagrams that clearly distinguish existing implementation from proposed architecture.

8. FOURTH TASK: INVESTIGATE THE WORKSPACE STRUCTURE

Now consider how the seven interfaces should evolve into a coherent workspace.

The objective is not to preserve seven separate pages simply because they already exist.

Explore the possibility of consolidating functions into a smaller number of logical working areas.

Potential areas for investigation include:

Products

* Product records.
* Recipes.
* Ingredients.
* Suppliers.
* Allergens.
* Nutrition.
* Pricing.
* Codes.

Menus

* Menu documents.
* Menu review.
* Menu construction.
* Menu exploration.
* Venue comparisons.

Operations

* Ordering.
* Preparation.
* Supplier information.
* Site-level information.
* Operational specifications.

Launches

* Launch planning.
* Milestones.
* Responsibilities.
* Readiness.
* Dependencies.
* Exceptions.

Intelligence

* Requirements cross-check.
* Data quality.
* Reporting.
* Cross-site analysis.
* Commercial insights.

These are architectural hypotheses, not predetermined navigation requirements.

Explore alternative structures.

For each proposed structure, explain:

* Which existing pages would be retained.
* Which functions would be combined.
* Which functions should become tabs or panels.
* Which components should become shared services.
* Which information should be shared.
* Which functions should remain independent.
* Why the structure would be easier to use operationally.

Consider the difference between:

1. Navigation structure.
2. Functional modules.
3. Data architecture.
4. Shared services.
5. User-specific working views.

These are not necessarily the same thing.

9. FIFTH TASK: IDENTIFY ARCHITECTURAL GAPS AND DESIGN DECISIONS

Produce a prioritised register of unresolved architectural questions.

Investigate:

* Source-of-truth ownership.
* Data duplication.
* Product and menu identifiers.
* Venue-specific overrides.
* Menu and recipe versioning.
* Audit history.
* Validation rules.
* Allergen information provenance.
* Nutritional data provenance.
* Pricing and VAT treatment.
* Recipe costing.
* Supplier relationships.
* Product codes.
* EPOS dependencies.
* User permissions.
* Review and approval responsibilities.
* Data import and export.
* Document traceability.
* Error handling.
* Notifications.
* Multi-site scalability.

Do not attempt to solve every issue immediately.

Distinguish between:

* Decisions required before architecture can be finalised.
* Decisions that can be deferred.
* Features that are optional.
* Dependencies requiring external systems.
* Capabilities requiring human approval.

10. SIXTH TASK: IDENTIFY OPPORTUNITIES FOR AI AND AUTOMATION

AI should be considered only after understanding the information architecture and workflows.

Identify opportunities where AI could reduce repetitive work or help people make better decisions.

Examples for investigation:

* Extracting menu information from PDFs.
* Identifying missing product information.
* Comparing menu versions.
* Suggesting ingredient-to-allergen relationships.
* Detecting inconsistencies across venues.
* Identifying products requiring review.
* Preparing launch documentation.
* Identifying incomplete launch dependencies.
* Generating staff-facing product information.
* Supporting natural-language queries.
* Identifying commercial anomalies.

For each opportunity, document:

* Input data.
* Expected output.
* Operational value.
* Required integrations.
* Human verification requirements.
* Risks.
* Whether deterministic automation would be more appropriate than AI.

Allergen, nutritional and food-safety information must have explicit provenance and human verification.

AI-generated suggestions must never silently become authoritative operational records.

11. SEVENTH TASK: PRODUCE THE DOCUMENTATION

Create a coherent documentation package in the project repository.

Suggested location:

docs/architecture/

Use the following proposed structure, adapting it if the repository already has an established documentation convention.

01 — PROJECT_OVERVIEW.md

Explain:

* Project purpose.
* Operational context.
* Intended users.
* Existing components.
* Overall architectural direction.
* Core design principles.

02 — EXISTING_SYSTEM_INVENTORY.md

Document each of the seven interfaces.

Include:

* Route.
* Source files.
* Technologies.
* Dependencies.
* Existing functionality.
* Data sources.
* Interactions.
* Current implementation status.
* Limitations.

03 — INFORMATION_ARCHITECTURE.md

Document:

* Principal entities.
* Relationships.
* Data ownership.
* Source-of-truth proposals.
* Shared information.
* Entity distinctions.
* Existing versus proposed models.

Include an ER diagram where appropriate.

04 — WORKFLOW_MAP.md

Document the principal operational workflows.

Include Mermaid flowcharts and descriptions of each stage.

05 — COMPONENT_RELATIONSHIPS.md

Explain how the seven existing interfaces relate.

Show:

* Existing connections.
* Proposed connections.
* Missing connections.
* Shared dependencies.
* Potential consolidation.

06 — WORKSPACE_PROPOSAL.md

Explore the proposed consolidated workspace.

Include:

* Navigation architecture.
* Functional areas.
* Page consolidation opportunities.
* User journeys.
* Shared components.
* Alternative structures considered.
* Recommended direction and rationale.

Do not implement the proposed interface at this stage.

07 — ARCHITECTURAL_GAPS.md

Document unresolved issues, dependencies, risks and decisions.

Prioritise them by importance.

08 — AI_AUTOMATION_OPPORTUNITIES.md

Document possible AI and deterministic automation opportunities.

09 — IMPLEMENTATION_STATUS.md

Create an evidence-based component status register.

Use the following classifications:

* Documented.
* Designed.
* Implemented.
* Tested.
* Populated.
* Integrated.
* Operational.

These are separate evidence dimensions.

Do not treat them as a simple linear progression.

10 — NEXT_STAGE_RECOMMENDATIONS.md

Recommend the next logical development stages.

Focus on architecture and product refinement before feature implementation.

12. REPORTING AND EVIDENCE STANDARDS

This section is critical.

Every significant finding must be classified as one of the following:

OBSERVED

Directly visible or demonstrated through actual interaction.

CODE-VERIFIED

Confirmed by examining source code, functions, schemas, API calls or backend implementation.

INFERRED

A reasonable interpretation based on available evidence, but not directly confirmed.

PROPOSED

A recommendation or future architectural direction.

Never present an inference as an implemented feature.

Never describe an intended integration as an existing integration.

Never describe sample data as real operational data.

Never assume that a frontend control has working backend functionality.

Where possible, reference:

* File paths.
* Function names.
* Routes.
* Schemas.
* API endpoints.
* Configuration.
* Relevant documentation sections.

Include confidence levels for significant architectural conclusions.

Where evidence is missing, state what would be required to verify it.

13. IMPORTANT PROJECT CONSTRAINTS

During this exercise:

* Do not redesign the interfaces.
* Do not modify existing application functionality.
* Do not delete files.
* Do not replace existing components.
* Do not migrate the project to another framework.
* Do not introduce a new database.
* Do not install unnecessary dependencies.
* Do not implement speculative integrations.
* Do not publish or deploy changes.
* Do not submit information to external systems.

Your task is investigation, analysis, architecture design and documentation.

You may create and update documentation files under the designated documentation directory.

Preserve the existing application.

If existing documentation conflicts with implementation, document the discrepancy rather than silently changing either.

14. EXPECTED FINAL DELIVERABLE

At the end of the exercise, the project should have a clear and usable architectural knowledge base.

A person unfamiliar with the repository should be able to understand:

1. What the project contains.
2. What each interface is intended to do.
3. How the components relate.
4. What information moves between them.
5. What the principal operational workflows look like.
6. Which entities and relationships underpin the system.
7. Where functionality overlaps.
8. Which pages could be consolidated.
9. What a coherent workspace could look like.
10. What architectural decisions remain unresolved.
11. Where AI and automation could genuinely help.
12. What should be developed next.

The documentation should be sufficiently detailed that another developer or AI coding agent can use it as the foundation for the next development phase without having to repeat the entire discovery exercise.

15. FINAL INSTRUCTION

Do not optimise for producing the largest amount of documentation.

Optimise for producing the clearest understanding of the system.

Do not assume the existing seven-page structure is correct.

Do not assume it is incorrect either.

Understand the underlying information, responsibilities and workflows first.

The central question is:

How do we transform this collection of individual hospitality technology capabilities into one coherent working environment, where information is connected, responsibilities are clear and operational work becomes easier?

Investigate thoroughly. Document accurately. Challenge assumptions. Explain architectural decisions.

Do not start implementation until the documentation has been produced and reviewed.